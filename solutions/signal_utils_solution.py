"""Kunci jawaban CP2 - dibuka setelah sesi simulasi selesai.

Bandingkan pendekatanmu dengan versi ini, lalu bandingkan keduanya terhadap
scipy.signal.find_peaks. Tujuannya bukan menghafal kode, tetapi memahami
mengapa setiap langkah ada.

Jalankan dari folder akar repositori:

    python solutions/signal_utils_solution.py
"""

from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks

PERSENTIL_DEFAULT = 95.0
REFRACTORY_DEFAULT = 0.25


def normalisasi_zscore(sinyal: np.ndarray) -> np.ndarray:
    simpangan = np.std(sinyal)
    if simpangan == 0:
        return np.zeros_like(sinyal)
    return (sinyal - np.mean(sinyal)) / simpangan


def find_r_peaks(
    sinyal: np.ndarray,
    fs: int,
    persentil: float = PERSENTIL_DEFAULT,
    refractory_s: float = REFRACTORY_DEFAULT,
) -> np.ndarray:
    x = normalisasi_zscore(sinyal)
    ambang = np.percentile(x, persentil)
    jarak_min = int(refractory_s * fs)

    kandidat = [
        i
        for i in range(1, x.size - 1)
        if x[i] > ambang and x[i] > x[i - 1] and x[i] >= x[i + 1]
    ]

    puncak: list[int] = []
    for indeks in kandidat:
        if not puncak:
            puncak.append(indeks)
            continue
        if indeks - puncak[-1] < jarak_min:
            if x[indeks] > x[puncak[-1]]:
                puncak[-1] = indeks
            continue
        puncak.append(indeks)

    return np.asarray(puncak, dtype=int)


def find_r_peaks_scipy(
    sinyal: np.ndarray,
    fs: int,
    persentil: float = PERSENTIL_DEFAULT,
    refractory_s: float = REFRACTORY_DEFAULT,
) -> np.ndarray:
    """Versi pustaka. Inilah yang dipakai di pekerjaan nyata."""
    x = normalisasi_zscore(sinyal)
    ambang = np.percentile(x, persentil)
    jarak_min = int(refractory_s * fs)
    puncak, _ = find_peaks(x, height=ambang, distance=jarak_min)
    return puncak


def hitung_bpm(puncak: np.ndarray, fs: int) -> float:
    if puncak.size < 2:
        return float("nan")
    rr = np.diff(puncak) / fs
    return float(60.0 / np.mean(rr))


if __name__ == "__main__":
    import pandas as pd

    FS = 250

    print("=" * 74)
    print("Perbandingan implementasi manual vs scipy pada seluruh dataset")
    print("=" * 74)
    acuan = pd.read_csv("data/reference_bpm.csv")
    print(f"{'file':<24}{'acuan':>8}{'manual':>9}{'scipy':>9}{'selisih':>9}  status")
    for _, baris in acuan.iterrows():
        berkas = str(baris["file"])
        kolom = "ppg_au" if "ppg" in berkas else "ecg_mv"
        sinyal = pd.read_csv(f"data/{berkas}")[kolom].to_numpy()
        b_manual = hitung_bpm(find_r_peaks(sinyal, FS), FS)
        b_scipy = hitung_bpm(find_r_peaks_scipy(sinyal, FS), FS)
        target = float(baris["bpm_acuan"])
        selisih = abs(b_manual - target)
        status = "LULUS" if selisih <= 3.0 else "GAGAL"
        print(f"{berkas:<24}{target:>8.2f}{b_manual:>9.2f}{b_scipy:>9.2f}{selisih:>9.2f}  {status}")

    print()
    print("=" * 74)
    print("Mengapa persentil default 95 dan bukan 98")
    print("=" * 74)
    ppg = pd.read_csv("data/ppg_sample.csv")["ppg_au"].to_numpy()
    target_ppg = float(acuan.loc[acuan["file"] == "ppg_sample.csv", "bpm_acuan"].iloc[0])
    for persentil in [90.0, 95.0, 98.0]:
        puncak = find_r_peaks(ppg, FS, persentil=persentil)
        bpm = hitung_bpm(puncak, FS)
        print(
            f"  PPG, persentil {persentil:>5} -> {puncak.size:>3} puncak, "
            f"BPM {bpm:>6.2f}, selisih {abs(bpm - target_ppg):>6.2f} dari acuan {target_ppg:.2f}"
        )
    print("\n  Ambang yang terlalu tinggi melewatkan denyut, dan kegagalan itu SENYAP:")
    print("  tidak ada exception, hanya BPM yang salah. Inilah alasan setiap detektor")
    print("  wajib divalidasi terhadap nilai acuan, bukan sekadar 'tidak error'.")
