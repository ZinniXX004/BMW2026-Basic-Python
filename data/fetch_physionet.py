"""Unduh satu rekaman dari PhysioNet dan ubah ke CSV berskema repositori ini.

Jalur OPSIONAL. Sesi hari-H memakai dataset sintetis dari make_dataset.py.
Baca data/PHYSIONET.md dan ATTRIBUTION.md sebelum memakai skrip ini.

Prasyarat:

    pip install -r requirements-physionet.txt

Contoh pemakaian:

    python data/fetch_physionet.py --db mitdb --record 100 --durasi 30
    python data/fetch_physionet.py --db mitdb --record 208 --durasi 60 --fs-target 360
    python data/fetch_physionet.py --daftar

Keluaran ditulis ke data/real/ dan diabaikan oleh Git.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from fractions import Fraction

import numpy as np
import pandas as pd

# Simbol anotasi WFDB yang menandai sebuah denyut jantung. Simbol lain menandai
# perubahan ritme, artefak, atau komentar, dan harus diabaikan saat menghitung RR.
SIMBOL_DENYUT = set("NLReAaJSVEFjnQ/f?")

KATALOG = {
    "mitdb": {
        "pn_dir": "mitdb",
        "nama": "MIT-BIH Arrhythmia Database",
        "lisensi": "Open Data Commons Attribution License v1.0 (ODC-BY 1.0)",
        "fs_asli": 360,
        "kanal_disarankan": "MLII",
        "anotator": "atr",
        "contoh_record": ["100", "101", "103", "108", "203", "207", "208", "212"],
        "terverifikasi": True,
        "catatan": "Satu-satunya dari daftar ini yang punya anotasi per denyut.",
    },
    "bidmc": {
        "pn_dir": "bidmc/1.0.0",
        "nama": "BIDMC PPG and Respiration Dataset",
        "lisensi": "Open Data Commons Attribution License v1.0 (ODC-BY 1.0)",
        "fs_asli": 125,
        "kanal_disarankan": "PLETH",
        "anotator": None,
        "contoh_record": ["bidmc01", "bidmc02"],
        "terverifikasi": False,
        "catatan": (
            "Penamaan rekaman WFDB belum diverifikasi langsung. Bila gagal, "
            "periksa daftar berkas di https://physionet.org/content/bidmc/"
        ),
    },
}

AKAR = pathlib.Path(__file__).resolve().parents[1]
KELUARAN = AKAR / "data" / "real"


def tampilkan_katalog() -> None:
    print("Dataset yang tersedia lewat skrip ini:\n")
    for kode, info in KATALOG.items():
        tanda = "terverifikasi" if info["terverifikasi"] else "BELUM DIUJI"
        print(f"  {kode:8s} {info['nama']}  [{tanda}]")
        print(f"           fs asli   : {info['fs_asli']} Hz")
        print(f"           lisensi   : {info['lisensi']}")
        print(f"           contoh    : {', '.join(info['contoh_record'])}")
        print(f"           catatan   : {info['catatan']}\n")
    print("Keluarga MIMIC tidak tersedia di sini: butuh credentialed access + DUA.")
    print("Baca ATTRIBUTION.md bagian 4 sebelum mencari alternatif lain.")


def pilih_kanal(nama_kanal: list[str], disarankan: str) -> int:
    """Kembalikan indeks kanal yang paling mendekati kanal yang disarankan."""
    for indeks, nama in enumerate(nama_kanal):
        if nama.strip().upper() == disarankan.upper():
            return indeks
    print(
        f"Kanal '{disarankan}' tidak ada. Kanal tersedia: {nama_kanal}. "
        f"Memakai kanal pertama ('{nama_kanal[0]}')."
    )
    return 0


def resample_ke(sinyal: np.ndarray, fs_asal: int, fs_tujuan: int) -> np.ndarray:
    """Resample dengan rasio rasional. 250/360 menjadi 25/36."""
    if fs_asal == fs_tujuan:
        return sinyal
    from scipy.signal import resample_poly

    rasio = Fraction(fs_tujuan, fs_asal).limit_denominator(1000)
    print(f"Resample {fs_asal} Hz -> {fs_tujuan} Hz (rasio {rasio.numerator}/{rasio.denominator})")
    return resample_poly(sinyal, rasio.numerator, rasio.denominator)


def bpm_dari_anotasi(sampel: np.ndarray, simbol: list[str], fs: int) -> tuple[float, int]:
    """BPM acuan dari anotasi denyut manusia. Inilah ground truth sebenarnya."""
    denyut = np.asarray(
        [s for s, sym in zip(sampel, simbol, strict=False) if sym in SIMBOL_DENYUT], dtype=int
    )
    if denyut.size < 2:
        return float("nan"), int(denyut.size)
    rr = np.diff(denyut) / fs
    return float(60.0 / np.mean(rr)), int(denyut.size)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="mitdb", help="kode dataset, lihat --daftar")
    parser.add_argument("--record", default="100", help="nama rekaman, misalnya 100")
    parser.add_argument("--durasi", type=float, default=30.0, help="detik yang diambil")
    parser.add_argument("--mulai", type=float, default=0.0, help="offset awal, detik")
    parser.add_argument(
        "--fs-target",
        type=int,
        default=250,
        help="fs keluaran. 250 agar seragam dengan data sintetis; "
        "pakai fs asli bila ingin tanpa resample",
    )
    parser.add_argument("--daftar", action="store_true", help="tampilkan katalog")
    argumen = parser.parse_args()

    if argumen.daftar:
        tampilkan_katalog()
        return

    if argumen.db not in KATALOG:
        print(f"Dataset '{argumen.db}' tidak dikenal. Jalankan --daftar.")
        sys.exit(1)

    info = KATALOG[argumen.db]
    if not info["terverifikasi"]:
        print(f"PERINGATAN: jalur '{argumen.db}' belum diuji. {info['catatan']}\n")

    try:
        import wfdb
    except ImportError:
        print("Paket wfdb belum terpasang. Jalankan:")
        print("    pip install -r requirements-physionet.txt")
        sys.exit(1)

    fs_asli = info["fs_asli"]
    sampel_mulai = int(argumen.mulai * fs_asli)
    sampel_akhir = sampel_mulai + int(argumen.durasi * fs_asli)

    print(f"Mengunduh {info['nama']} rekaman {argumen.record} dari PhysioNet...")
    print(f"Lisensi: {info['lisensi']}. Wajib dikutip, lihat ATTRIBUTION.md.\n")

    rekaman = wfdb.rdrecord(
        argumen.record,
        pn_dir=info["pn_dir"],
        sampfrom=sampel_mulai,
        sampto=sampel_akhir,
    )

    if rekaman.fs != fs_asli:
        print(f"Catatan: fs sebenarnya {rekaman.fs} Hz, katalog mencatat {fs_asli} Hz.")
        fs_asli = int(rekaman.fs)

    indeks_kanal = pilih_kanal(list(rekaman.sig_name), info["kanal_disarankan"])
    satuan = rekaman.units[indeks_kanal]
    # p_signal sudah dalam satuan fisik karena gain dan baseline dari .hea diterapkan.
    sinyal = np.asarray(rekaman.p_signal[:, indeks_kanal], dtype=float)
    sinyal = sinyal[~np.isnan(sinyal)]

    print(f"Kanal dipakai : {rekaman.sig_name[indeks_kanal]} ({satuan})")
    print(f"Sampel terbaca: {sinyal.size} pada {fs_asli} Hz")

    sinyal_out = resample_ke(sinyal, fs_asli, argumen.fs_target)
    waktu = np.arange(sinyal_out.size) / argumen.fs_target

    KELUARAN.mkdir(parents=True, exist_ok=True)
    dasar = f"{argumen.db}_{argumen.record}_{argumen.fs_target}hz"
    path_csv = KELUARAN / f"{dasar}.csv"
    pd.DataFrame({"time_s": np.round(waktu, 6), "ecg_mv": np.round(sinyal_out, 6)}).to_csv(
        path_csv, index=False
    )
    print(f"\nDitulis: {path_csv.relative_to(AKAR)}  (kolom time_s, ecg_mv)")

    if info["anotator"]:
        anotasi = wfdb.rdann(
            argumen.record,
            info["anotator"],
            pn_dir=info["pn_dir"],
            sampfrom=sampel_mulai,
            sampto=sampel_akhir,
        )
        bpm, jumlah = bpm_dari_anotasi(anotasi.sample, list(anotasi.symbol), fs_asli)
        path_acuan = KELUARAN / f"{dasar}_reference.csv"
        pd.DataFrame(
            [
                {
                    "file": path_csv.name,
                    "bpm_acuan": round(bpm, 4),
                    "jumlah_denyut_anotasi": jumlah,
                    "fs_hz": argumen.fs_target,
                    "fs_asli_hz": fs_asli,
                    "durasi_s": argumen.durasi,
                    "sumber": info["nama"],
                    "lisensi": info["lisensi"],
                }
            ]
        ).to_csv(path_acuan, index=False)
        print(f"Ditulis: {path_acuan.relative_to(AKAR)}")
        print(f"\nBPM acuan dari anotasi kardiolog: {bpm:.2f} ({jumlah} denyut)")
    else:
        print("\nDataset ini tidak punya anotasi per denyut; tidak ada BPM acuan.")

    print("\nLangkah berikutnya:")
    print(f"  python exercises/cp2b_validasi_anotasi.py --record {argumen.record}")
    print("  atau ganti path pd.read_csv pada exercises/cp1_load_plot.py")
    print(f"\nIngat: fs data ini {argumen.fs_target} Hz. Teruskan nilai itu ke find_r_peaks.")


if __name__ == "__main__":
    main()
