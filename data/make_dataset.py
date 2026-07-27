"""Bangkitkan dataset sintetis untuk BMW Basic 2026 - Materi I.

Seluruh sinyal disintesis secara numerik dan deterministik (seed tetap), jadi:

- tidak ada data pasien nyata dan tidak ada persoalan privasi;
- tidak ada persoalan lisensi basis data pihak ketiga;
- tidak perlu koneksi internet pada hari-H;
- nilai BPM acuan diketahui secara pasti karena ditentukan saat sintesis.

Jalankan dari folder akar repositori:

    python data/make_dataset.py
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

FS = 250          # frekuensi sampling, Hz
DURASI = 10.0     # detik
DATA_DIR = pathlib.Path(__file__).resolve().parent


def gauss(t: np.ndarray, amplitudo: float, pusat: float, lebar: float) -> np.ndarray:
    """Satu komponen gelombang berbentuk Gaussian."""
    return amplitudo * np.exp(-0.5 * ((t - pusat) / lebar) ** 2)


def waktu_denyut(bpm: float, durasi: float, jitter: float, rng: np.random.Generator) -> np.ndarray:
    """Deret waktu denyut dengan variabilitas interval RR yang realistis."""
    rr = 60.0 / bpm
    waktu, sekarang = [], 0.6
    while sekarang < durasi - 0.4:
        waktu.append(sekarang)
        sekarang += rr + rng.normal(0.0, jitter)
    return np.asarray(waktu)


def sintesis_ekg(bpm: float, seed: int, jitter: float = 0.02) -> tuple[np.ndarray, np.ndarray, float]:
    """Sinyal EKG sintetis dengan morfologi PQRST, baseline wander, dan derau."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, DURASI, 1.0 / FS)
    sinyal = np.zeros_like(t)
    denyut = waktu_denyut(bpm, DURASI, jitter, rng)
    for tb in denyut:
        sinyal += gauss(t, 0.08, tb - 0.16, 0.022)   # gelombang P
        sinyal += gauss(t, -0.10, tb - 0.022, 0.008)  # Q
        sinyal += gauss(t, 1.20, tb, 0.008)           # R
        sinyal += gauss(t, -0.25, tb + 0.022, 0.010)  # S
        sinyal += gauss(t, 0.30, tb + 0.17, 0.032)    # gelombang T
    sinyal += 0.05 * np.sin(2 * np.pi * 0.3 * t)      # baseline wander pernapasan
    sinyal += rng.normal(0.0, 0.012, size=t.size)     # derau instrumentasi
    bpm_acuan = 60.0 / np.mean(np.diff(denyut))
    return t, sinyal, bpm_acuan


def sintesis_ppg(bpm: float, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Sinyal PPG sintetis dengan puncak sistolik dan notch dikrotik."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, DURASI, 1.0 / FS)
    sinyal = np.zeros_like(t)
    denyut = waktu_denyut(bpm, DURASI, 0.018, rng)
    for tb in denyut:
        sinyal += gauss(t, 1.00, tb + 0.18, 0.045)   # puncak sistolik
        sinyal += gauss(t, 0.32, tb + 0.36, 0.055)   # gelombang dikrotik
    sinyal += 0.03 * np.sin(2 * np.pi * 0.25 * t)
    sinyal += rng.normal(0.0, 0.010, size=t.size)
    bpm_acuan = 60.0 / np.mean(np.diff(denyut))
    return t, sinyal, bpm_acuan


def simpan(path: pathlib.Path, t: np.ndarray, sinyal: np.ndarray, kolom: str) -> None:
    frame = pd.DataFrame({"time_s": np.round(t, 5), kolom: np.round(sinyal, 5)})
    frame.to_csv(path, index=False)


def main() -> None:
    acuan: list[dict[str, object]] = []

    t, ekg, bpm_ekg = sintesis_ekg(bpm=72.0, seed=2026)
    simpan(DATA_DIR / "ecg_sample.csv", t, ekg, "ecg_mv")
    acuan.append({"file": "ecg_sample.csv", "jenis": "ECG", "fs_hz": FS, "bpm_acuan": round(bpm_ekg, 2)})

    t, ppg, bpm_ppg = sintesis_ppg(bpm=88.0, seed=112)
    simpan(DATA_DIR / "ppg_sample.csv", t, ppg, "ppg_au")
    acuan.append({"file": "ppg_sample.csv", "jenis": "PPG", "fs_hz": FS, "bpm_acuan": round(bpm_ppg, 2)})

    # Dataset KPP: satu berkas per kelompok NRP, agar tugas tidak dapat disalin.
    kpp_dir = DATA_DIR / "kpp"
    kpp_dir.mkdir(exist_ok=True)
    target = [52.0, 63.0, 71.0, 84.0, 96.0, 108.0]
    for indeks, bpm in enumerate(target):
        t, ekg, bpm_acuan = sintesis_ekg(bpm=bpm, seed=7000 + indeks, jitter=0.03)
        nama = f"subject_{indeks:02d}.csv"
        simpan(kpp_dir / nama, t, ekg, "ecg_mv")
        acuan.append({"file": f"kpp/{nama}", "jenis": "ECG", "fs_hz": FS, "bpm_acuan": round(bpm_acuan, 2)})

    pd.DataFrame(acuan).to_csv(DATA_DIR / "reference_bpm.csv", index=False)

    print(f"Dataset dibuat di: {DATA_DIR}")
    print(f"fs = {FS} Hz, durasi = {DURASI:.0f} s, jumlah sampel = {int(FS * DURASI)}")
    print("\nBPM acuan (toleransi penilaian +/- 3 BPM untuk sesi, +/- 5 BPM untuk KPP):")
    for baris in acuan:
        print(f"  {baris['file']:<24} {baris['jenis']:<4} {baris['bpm_acuan']:>7.2f} BPM")
    print("\nCatatan: berkas KPP dipilih dengan rumus indeks = dua digit terakhir NRP mod 6.")


if __name__ == "__main__":
    main()
