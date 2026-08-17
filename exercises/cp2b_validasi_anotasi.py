"""Bonus - ukur kinerja detektormu terhadap anotasi kardiolog MIT-BIH.

Jalur OPSIONAL, bukan bagian dari sesi 60 menit. Dipakai untuk bonus KPP.

Prasyarat:

    pip install -r requirements-physionet.txt
    python data/fetch_physionet.py --db mitdb --record 100 --durasi 60

Jalankan:

    python exercises/cp2b_validasi_anotasi.py --record 100 --durasi 60

Yang dihitung:
  Sensitivitas Se = TP / (TP + FN)   berapa persen denyut nyata yang ditemukan
  Presisi     +P  = TP / (TP + FP)   berapa persen deteksimu yang benar
  Selisih BPM       dampak akhir kesalahan deteksi terhadap laju jantung

Toleransi pencocokan 150 ms kira-kira sepadan dengan lebar kompleks QRS
ditambah ketidakpastian penempatan penanda oleh anotator manusia.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np

from src.signal_utils import find_r_peaks, hitung_bpm

SIMBOL_DENYUT = set("NLReAaJSVEFjnQ/f?")
TOLERANSI_S = 0.150


def cocokkan(
    deteksi: np.ndarray, acuan: np.ndarray, fs: int, toleransi_s: float = TOLERANSI_S
) -> tuple[int, int, int]:
    """Cocokkan deteksi dengan anotasi secara satu-ke-satu.

    Setiap anotasi hanya boleh dipasangkan dengan satu deteksi, dan sebaliknya.
    Tanpa aturan ini, detektor yang menghasilkan dua puncak per denyut akan
    tampak sempurna padahal salah.
    """
    toleransi = int(toleransi_s * fs)
    terpakai = np.zeros(deteksi.size, dtype=bool)
    tp = 0

    for titik_acuan in acuan:
        jarak = np.abs(deteksi - titik_acuan)
        jarak[terpakai] = np.iinfo(np.int64).max
        if jarak.size == 0:
            continue
        kandidat = int(np.argmin(jarak))
        if jarak[kandidat] <= toleransi:
            terpakai[kandidat] = True
            tp += 1

    fn = int(acuan.size - tp)
    fp = int(deteksi.size - tp)
    return tp, fp, fn


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", default="100")
    parser.add_argument("--durasi", type=float, default=60.0)
    parser.add_argument("--mulai", type=float, default=0.0)
    parser.add_argument("--persentil", type=float, default=98.0)
    parser.add_argument("--refractory", type=float, default=0.25)
    argumen = parser.parse_args()

    try:
        import wfdb
    except ImportError:
        print("Paket wfdb belum terpasang. Jalankan:")
        print("    pip install -r requirements-physionet.txt")
        sys.exit(1)

    fs = 360  # fs asli MIT-BIH. Dipakai apa adanya, tanpa resample.
    mulai = int(argumen.mulai * fs)
    akhir = mulai + int(argumen.durasi * fs)

    rekaman = wfdb.rdrecord(argumen.record, pn_dir="mitdb", sampfrom=mulai, sampto=akhir)
    anotasi = wfdb.rdann(argumen.record, "atr", pn_dir="mitdb", sampfrom=mulai, sampto=akhir)

    kanal = 0
    for indeks, nama in enumerate(rekaman.sig_name):
        if nama.strip().upper() == "MLII":
            kanal = indeks
            break

    sinyal = np.asarray(rekaman.p_signal[:, kanal], dtype=float)
    sinyal = np.nan_to_num(sinyal, nan=float(np.nanmean(sinyal)))

    # Anotasi memakai indeks absolut terhadap awal rekaman; geser ke awal potongan.
    acuan = np.asarray(
        [
            s - mulai
            for s, sym in zip(anotasi.sample, anotasi.symbol, strict=False)
            if sym in SIMBOL_DENYUT
        ],
        dtype=int,
    )
    acuan = acuan[(acuan >= 0) & (acuan < sinyal.size)]

    deteksi = find_r_peaks(
        sinyal, fs, persentil=argumen.persentil, refractory_s=argumen.refractory
    )

    if deteksi.size == 0:
        print("Detektor tidak menemukan satu puncak pun.")
        print("Periksa TODO CP2-a dan CP2-b di src/signal_utils.py sebelum lanjut.")
        sys.exit(1)

    tp, fp, fn = cocokkan(deteksi, acuan, fs)
    se = tp / (tp + fn) if (tp + fn) else float("nan")
    pp = tp / (tp + fp) if (tp + fp) else float("nan")

    bpm_deteksi = hitung_bpm(deteksi, fs)
    rr_acuan = np.diff(acuan) / fs
    bpm_acuan = 60.0 / rr_acuan.mean() if rr_acuan.size else float("nan")

    print(f"Rekaman MIT-BIH {argumen.record}, {argumen.durasi:.0f} s, fs = {fs} Hz")
    print(f"Kanal           : {rekaman.sig_name[kanal]} ({rekaman.units[kanal]})")
    print(f"Parameter       : persentil {argumen.persentil}, refractory {argumen.refractory} s")
    print("-" * 58)
    print(f"Denyut anotasi  : {acuan.size}")
    print(f"Deteksi kamu    : {deteksi.size}")
    print(f"TP / FP / FN    : {tp} / {fp} / {fn}")
    print(f"Sensitivitas Se : {se * 100:.2f} %")
    print(f"Presisi +P      : {pp * 100:.2f} %")
    print("-" * 58)
    print(f"BPM anotasi     : {bpm_acuan:.2f}")
    print(f"BPM kamu        : {bpm_deteksi:.2f}")
    print(f"Selisih         : {abs(bpm_deteksi - bpm_acuan):.2f} BPM")
    print("-" * 58)

    if fp > fn * 2 and fp > 3:
        print("Diagnosis: banyak deteksi palsu. Detektor terlalu longgar.")
        print("Coba naikkan --persentil ke 99, atau perbesar --refractory.")
    elif fn > fp * 2 and fn > 3:
        print("Diagnosis: banyak denyut terlewat. Detektor terlalu ketat.")
        print("Coba turunkan --persentil ke 95. Periksa juga baseline wander.")
    else:
        print("Kesalahan seimbang. Sisanya kemungkinan artefak atau denyut ektopik.")

    print("\nSumber data: MIT-BIH Arrhythmia Database (Moody & Mark, 2001), ODC-BY 1.0.")
    print("Sertakan kutipan lengkap dari ATTRIBUTION.md dalam laporanmu.")


if __name__ == "__main__":
    main()
