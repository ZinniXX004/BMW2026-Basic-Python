"""Kunci jawaban CP2 - dibuka setelah sesi simulasi selesai.

Bandingkan pendekatanmu dengan versi ini, lalu bandingkan keduanya terhadap
scipy.signal.find_peaks. Tujuannya bukan menghafal kode, tetapi memahami
mengapa setiap langkah ada.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks


def normalisasi_zscore(sinyal: np.ndarray) -> np.ndarray:
    simpangan = np.std(sinyal)
    if simpangan == 0:
        return np.zeros_like(sinyal)
    return (sinyal - np.mean(sinyal)) / simpangan


def find_r_peaks(
    sinyal: np.ndarray,
    fs: int,
    persentil: float = 98.0,
    refractory_s: float = 0.25,
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
    persentil: float = 98.0,
    refractory_s: float = 0.25,
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
    frame = pd.read_csv("data/ecg_sample.csv")
    ekg = frame["ecg_mv"].to_numpy()

    manual = find_r_peaks(ekg, FS)
    pustaka = find_r_peaks_scipy(ekg, FS)

    print(f"Puncak manual : {manual.size} puncak, BPM = {hitung_bpm(manual, FS):.2f}")
    print(f"Puncak scipy  : {pustaka.size} puncak, BPM = {hitung_bpm(pustaka, FS):.2f}")
    print("Selisih indeks:", np.setdiff1d(manual, pustaka))
    print("\nBandingkan dengan data/reference_bpm.csv.")
