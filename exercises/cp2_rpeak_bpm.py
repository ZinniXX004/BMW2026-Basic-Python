"""CP2 (25 menit) - lengkapi find_r_peaks dan hitung_bpm, lalu validasi.

Target checkpoint: BPM hasil hitunganmu berada dalam +/- 3 BPM dari nilai pada
data/reference_bpm.csv, dan jumlah puncak yang terdeteksi masuk akal untuk
rekaman 10 detik.

Urutan kerja:
  1. Isi TODO di src/signal_utils.py.
  2. Jalankan berkas ini.
  3. Bandingkan dengan scipy.signal.find_peaks di bagian bawah keluaran.

Jalankan dari folder akar repositori:

    python exercises/cp2_rpeak_bpm.py
"""

from __future__ import annotations

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from src.signal_utils import (
    find_r_peaks,
    hitung_bpm,
    hitung_sdnn_ms,
    klasifikasi_hr,
    normalisasi_zscore,
)

FS = 250


def main() -> None:
    ekg = pd.read_csv("data/ecg_sample.csv")["ecg_mv"].to_numpy()

    puncak = find_r_peaks(ekg, FS)
    bpm = hitung_bpm(puncak, FS)
    sdnn = hitung_sdnn_ms(puncak, FS)

    print(f"Jumlah puncak terdeteksi : {puncak.size}")
    print(f"BPM                      : {bpm:.2f}")
    print(f"SDNN                     : {sdnn:.2f} ms")
    print(f"Label (dewasa istirahat) : {klasifikasi_hr(bpm)}")

    acuan = pd.read_csv("data/reference_bpm.csv")
    bpm_acuan = float(acuan.loc[acuan["file"] == "ecg_sample.csv", "bpm_acuan"].iloc[0])
    print(f"\nBPM acuan                : {bpm_acuan:.2f}")
    if not np.isnan(bpm):
        selisih = abs(bpm - bpm_acuan)
        status = "LULUS" if selisih <= 3.0 else "BELUM LULUS"
        print(f"Selisih                  : {selisih:.2f} BPM -> {status}")

    x = normalisasi_zscore(ekg)
    pembanding, _ = find_peaks(x, height=np.percentile(x, 98), distance=int(0.25 * FS))
    print(f"\nPembanding scipy         : {pembanding.size} puncak")
    print("Implementasi manual untuk paham; pustaka untuk pekerjaan nyata.")

    if puncak.size:
        plt.figure(figsize=(11, 4))
        plt.plot(np.arange(ekg.size) / FS, ekg, linewidth=0.9, label="EKG")
        plt.plot(puncak / FS, ekg[puncak], "o", markersize=5, label="R-Peak")
        plt.title(f"Deteksi R-Peak, BPM = {bpm:.1f} (fs = {FS} Hz)")
        plt.xlabel("Waktu (s)")
        plt.ylabel("Amplitudo (mV)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
    else:
        print("\nBelum ada puncak terdeteksi. Periksa kembali TODO CP2-a dan CP2-b.")


if __name__ == "__main__":
    main()
