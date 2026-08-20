"""Live demo MIT-BIH untuk presentasi BMW Basic 2026 - Materi I.

Aturan panggung: demo TIDAK BOLEH bergantung pada internet saat presentasi.
Karena itu skrip ini punya dua mode terpisah.

1. MODE PERSIAPAN (di rumah, ada internet, sekali saja)

       pip install -r requirements-physionet.txt
       python demo/live_demo_mitbih.py --siapkan

   Mengunduh MIT-BIH record 100 (30 detik), menurunkan laju cuplik 360 -> 250 Hz,
   lalu menulis data/demo/mitdb_100_250hz.csv beserta berkas acuan dari anotasi
   kardiolog. Berkas hasilnya WAJIB di-commit ke repositori. MIT-BIH berlisensi
   ODC-BY 1.0 sehingga redistribusi turunan diizinkan dengan atribusi
   (lihat ATTRIBUTION.md).

2. MODE PANGGUNG (hari-H, tanpa internet, tanpa wfdb)

       python demo/live_demo_mitbih.py

   Hanya membaca CSV yang sudah di-commit. Bila CSV tidak ada, skrip TIDAK mati:
   ia beralih ke data sintetis dengan peringatan besar, supaya demo tetap jalan.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd

from src.signal_utils import hitung_sdnn_ms, klasifikasi_hr

AKAR = pathlib.Path(__file__).resolve().parents[1]
DEMO_DIR = AKAR / "data" / "demo"
CSV_DEMO = DEMO_DIR / "mitdb_100_250hz.csv"
CSV_ACUAN = DEMO_DIR / "mitdb_100_250hz_acuan.csv"

FS_ASLI = 360
FS_TARGET = 250
REKAMAN = "100"
DURASI_S = 30
SIMBOL_DENYUT = set("NLReAaJSVEFjnQ/f?")

# Parameter ini hasil pengujian, bukan tebakan: persentil 98 gagal pada sinyal
# berpuncak lebar. Persentil 95 lulus pada seluruh dataset repositori.
PERSENTIL = 95.0
REFRACTORY_S = 0.25

SUMBER_MD = """# Sumber data demo

Berkas `mitdb_100_250hz.csv` adalah **turunan** dari:

MIT-BIH Arrhythmia Database v1.0.0, record 100, kanal MLII, 30 detik pertama,
diturunkan laju cupliknya dari 360 Hz ke 250 Hz.

- Sumber: https://physionet.org/content/mitdb/1.0.0/
- Lisensi: Open Data Commons Attribution License v1.0 (ODC-BY 1.0)
- Kutipan wajib: lihat `ATTRIBUTION.md` di akar repositori.

Berkas `mitdb_100_250hz_acuan.csv` berisi laju jantung acuan yang dihitung dari
anotasi denyut `.atr` (anotasi kardiolog), bukan dari algoritma kita sendiri.
"""


def deteksi(sinyal: np.ndarray, fs: int, persentil: float, refractory_s: float) -> np.ndarray:
    """Deteksi R-Peak mandiri, agar demo tidak bergantung pada TODO peserta."""
    simpangan = np.std(sinyal)
    x = np.zeros_like(sinyal) if simpangan == 0 else (sinyal - np.mean(sinyal)) / simpangan
    ambang = np.percentile(x, persentil)
    jarak_min = int(refractory_s * fs)
    kandidat = [
        i for i in range(1, x.size - 1)
        if x[i] > ambang and x[i] > x[i - 1] and x[i] >= x[i + 1]
    ]
    puncak: list[int] = []
    for indeks in kandidat:
        if not puncak:
            puncak.append(indeks)
        elif indeks - puncak[-1] < jarak_min:
            if x[indeks] > x[puncak[-1]]:
                puncak[-1] = indeks
        else:
            puncak.append(indeks)
    return np.asarray(puncak, dtype=int)


def bpm_dari(puncak: np.ndarray, fs: int) -> float:
    if puncak.size < 2:
        return float("nan")
    return float(60.0 / np.mean(np.diff(puncak) / fs))


def siapkan(dari_lokal: str | None = None) -> int:
    """Unduh dan ekspor data demo. Butuh internet dan paket wfdb.

    dari_lokal: kalau diisi (path folder), baca 100.dat/100.hea/100.atr dari
    folder itu alih-alih mengunduh otomatis lewat pn_dir. Berguna kalau
    jaringan kampus/asrama memblokir physionet.org secara langsung -- unduh
    manual 3 berkas itu lewat browser dari:
      https://physionet.org/files/mitdb/1.0.0/100.dat
      https://physionet.org/files/mitdb/1.0.0/100.hea
      https://physionet.org/files/mitdb/1.0.0/100.atr
    lalu taruh ketiganya di satu folder dan jalankan:
      python demo/live_demo_mitbih.py --siapkan --dari folder_unduhan/
    """
    try:
        import wfdb
    except ImportError:
        print("GAGAL: paket wfdb belum terpasang.")
        print("Jalankan: pip install -r requirements-physionet.txt")
        return 1
    try:
        from scipy.signal import resample_poly
    except ImportError:
        print("GAGAL: scipy belum terpasang. Jalankan: pip install -r requirements.txt")
        return 1

    n_sampel = FS_ASLI * DURASI_S

    if dari_lokal:
        folder = pathlib.Path(dari_lokal).expanduser().resolve()
        path_dat = folder / f"{REKAMAN}.dat"
        path_hea = folder / f"{REKAMAN}.hea"
        path_atr = folder / f"{REKAMAN}.atr"
        hilang = [p.name for p in (path_dat, path_hea, path_atr) if not p.is_file()]
        if hilang:
            print(f"GAGAL: berkas berikut tidak ditemukan di {folder}: {', '.join(hilang)}")
            print("Unduh manual dari https://physionet.org/files/mitdb/1.0.0/ lalu coba lagi.")
            return 1
        print(f"Membaca record {REKAMAN} dari berkas lokal di {folder} ...")
        rekaman = wfdb.rdrecord(str(folder / REKAMAN), sampfrom=0, sampto=n_sampel)
        anotasi = wfdb.rdann(str(folder / REKAMAN), "atr", sampfrom=0, sampto=n_sampel)
    else:
        print(f"Mengunduh MIT-BIH record {REKAMAN}, {DURASI_S} detik pertama ...")
        rekaman = wfdb.rdrecord(REKAMAN, pn_dir="mitdb", sampfrom=0, sampto=n_sampel)
        anotasi = wfdb.rdann(REKAMAN, "atr", pn_dir="mitdb", sampfrom=0, sampto=n_sampel)

    if int(rekaman.fs) != FS_ASLI:
        print(f"PERINGATAN: fs rekaman {rekaman.fs} Hz, bukan {FS_ASLI} Hz yang diasumsikan.")

    nama_kanal = list(rekaman.sig_name)
    kanal = nama_kanal.index("MLII") if "MLII" in nama_kanal else 0
    print(f"Kanal dipakai: {nama_kanal[kanal]} ({rekaman.units[kanal]}), fs = {rekaman.fs} Hz")

    mentah = np.asarray(rekaman.p_signal)[:, kanal].astype(float)
    mentah = np.nan_to_num(mentah, nan=0.0)

    from fractions import Fraction
    rasio = Fraction(FS_TARGET, int(rekaman.fs)).limit_denominator(1000)
    turun = resample_poly(mentah, rasio.numerator, rasio.denominator)
    print(f"Resample {rekaman.fs} -> {FS_TARGET} Hz memakai rasio {rasio.numerator}/{rasio.denominator}")

    waktu = np.arange(turun.size) / FS_TARGET
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    # newline="" + lineterminator="\n": paksa LF di semua OS (lihat catatan
    # yang sama di data/make_dataset.py).
    with open(CSV_DEMO, "w", newline="", encoding="utf-8") as f:
        pd.DataFrame({"time_s": np.round(waktu, 5), "ecg_mv": np.round(turun, 5)}).to_csv(
            f, index=False, lineterminator="\n"
        )

    denyut = np.asarray(
        [s for s, sym in zip(anotasi.sample, anotasi.symbol, strict=False) if sym in SIMBOL_DENYUT],
        dtype=int,
    )
    bpm_acuan = (
        float(60.0 / np.mean(np.diff(denyut) / int(rekaman.fs))) if denyut.size >= 2 else float("nan")
    )
    with open(CSV_ACUAN, "w", newline="", encoding="utf-8") as f:
        pd.DataFrame(
            [{
                "sumber": f"mitdb/{REKAMAN}",
                "kanal": nama_kanal[kanal],
                "fs_asli_hz": int(rekaman.fs),
                "fs_hz": FS_TARGET,
                "durasi_s": DURASI_S,
                "jumlah_denyut_anotasi": int(denyut.size),
                "bpm_acuan": round(bpm_acuan, 2),
                "lisensi": "ODC-BY 1.0",
            }]
        ).to_csv(f, index=False, lineterminator="\n")
    (DEMO_DIR / "SUMBER.md").write_text(SUMBER_MD, encoding="utf-8")

    print(f"\nTertulis: {CSV_DEMO.relative_to(AKAR)} ({CSV_DEMO.stat().st_size // 1024} KB)")
    print(f"Tertulis: {CSV_ACUAN.relative_to(AKAR)}")
    print(f"Tertulis: {(DEMO_DIR / 'SUMBER.md').relative_to(AKAR)}")
    print(f"\nDenyut teranotasi: {denyut.size}, BPM acuan kardiolog: {bpm_acuan:.2f}")
    print("\nLANGKAH WAJIB BERIKUTNYA: commit folder data/demo/ ke repositori,")
    print("lalu uji ulang dengan: python demo/live_demo_mitbih.py")
    return 0


def data_cadangan() -> tuple[np.ndarray, np.ndarray, float, str]:
    """Cadangan sintetis bila CSV demo tidak ada. Demo tidak boleh mati di panggung."""
    ekg = AKAR / "data" / "ecg_sample.csv"
    if not ekg.exists():
        print("GAGAL TOTAL: data/ecg_sample.csv juga tidak ada.")
        print("Jalankan: python data/make_dataset.py")
        raise SystemExit(2)
    frame = pd.read_csv(ekg)
    acuan = pd.read_csv(AKAR / "data" / "reference_bpm.csv")
    bpm = float(acuan.loc[acuan["file"] == "ecg_sample.csv", "bpm_acuan"].iloc[0])
    return frame["time_s"].to_numpy(), frame["ecg_mv"].to_numpy(), bpm, "sintetis (cadangan)"


def jalankan(tanpa_gambar: bool) -> int:
    print("=" * 70)
    print("LIVE DEMO - Data EKG nyata MIT-BIH, pipeline yang sama dengan sesi")
    print("=" * 70)

    if CSV_DEMO.exists() and CSV_ACUAN.exists():
        frame = pd.read_csv(CSV_DEMO)
        meta = pd.read_csv(CSV_ACUAN).iloc[0]
        waktu = frame["time_s"].to_numpy()
        sinyal = frame["ecg_mv"].to_numpy()
        bpm_acuan = float(meta["bpm_acuan"])
        fs = int(meta["fs_hz"])
        sumber = f"{meta['sumber']} kanal {meta['kanal']}, {meta['fs_asli_hz']} -> {fs} Hz, {meta['lisensi']}"
        n_anotasi = int(meta["jumlah_denyut_anotasi"])
    else:
        print("\n" + "!" * 70)
        print("! DATA MIT-BIH TIDAK DITEMUKAN di data/demo/")
        print("! Demo beralih ke data sintetis agar presentasi tetap berjalan.")
        print("! Jalankan 'python demo/live_demo_mitbih.py --siapkan' di rumah,")
        print("! lalu commit folder data/demo/.")
        print("!" * 70 + "\n")
        waktu, sinyal, bpm_acuan, sumber = data_cadangan()
        fs, n_anotasi = 250, -1

    print(f"\nSumber        : {sumber}")
    print(f"Jumlah sampel : {sinyal.size} ({sinyal.size / fs:.1f} detik pada {fs} Hz)")
    print(f"Amplitudo     : {sinyal.min():.3f} .. {sinyal.max():.3f} mV")

    puncak = deteksi(sinyal, fs, PERSENTIL, REFRACTORY_S)
    bpm = bpm_dari(puncak, fs)
    sdnn = hitung_sdnn_ms(puncak, fs)

    print(f"\nParameter     : persentil={PERSENTIL}, refractory={REFRACTORY_S} s")
    print(f"R-Peak        : {puncak.size} terdeteksi", end="")
    if n_anotasi >= 0:
        print(f"  (anotasi kardiolog: {n_anotasi} denyut)")
    else:
        print()
    print(f"BPM algoritma : {bpm:.2f}")
    print(f"BPM acuan     : {bpm_acuan:.2f}")
    selisih = abs(bpm - bpm_acuan)
    print(f"Selisih       : {selisih:.2f} BPM -> {'DALAM TOLERANSI' if selisih <= 3 else 'DI LUAR TOLERANSI'}")
    print(f"SDNN          : {sdnn:.2f} ms")
    print(f"Label         : {klasifikasi_hr(bpm)}")

    print("\nJebakan yang wajib disebut di panggung:")
    salah = bpm_dari(puncak, 250) if fs != 250 else bpm_dari(puncak, 360)
    fs_salah = 250 if fs != 250 else 360
    print(f"  Bila fs dianggap {fs_salah} Hz padahal {fs} Hz: BPM terbaca {salah:.2f}")
    print(f"  Salah faktor {fs_salah / fs:.3f}, tanpa satu pun pesan error.")

    if not tanpa_gambar:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 4.2))
        plt.plot(waktu[: sinyal.size], sinyal, linewidth=0.9, label="EKG")
        if puncak.size:
            plt.plot(puncak / fs, sinyal[puncak], "o", markersize=5, label="R-Peak")
        plt.title(f"{sumber} | BPM algoritma {bpm:.1f} vs acuan {bpm_acuan:.1f}")
        plt.xlabel("Waktu (s)")
        plt.ylabel("Amplitudo (mV)")
        plt.xlim(0, min(10, sinyal.size / fs))
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        keluaran = AKAR / "data" / "demo" / "demo_preview.png"
        keluaran.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(keluaran, dpi=110)
        print(f"\nGambar tersimpan: {keluaran.relative_to(AKAR)}")
        plt.show()

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Live demo MIT-BIH untuk BMW Basic 2026.")
    parser.add_argument("--siapkan", action="store_true", help="Unduh data demo (butuh internet + wfdb).")
    parser.add_argument(
        "--dari", metavar="FOLDER", default=None,
        help="Pakai bersama --siapkan: baca 100.dat/100.hea/100.atr dari FOLDER lokal "
             "alih-alih mengunduh otomatis (untuk jaringan yang memblokir physionet.org).",
    )
    parser.add_argument("--tanpa-gambar", action="store_true", help="Jangan tampilkan atau simpan grafik.")
    argumen = parser.parse_args()
    return siapkan(argumen.dari) if argumen.siapkan else jalankan(argumen.tanpa_gambar)


if __name__ == "__main__":
    raise SystemExit(main())
