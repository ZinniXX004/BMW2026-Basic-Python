"""CP1 (15 menit) - muat CSV medis dan plot window 5 detik pertama.

Target checkpoint: grafik EKG 5 detik muncul, dengan label sumbu yang benar
(waktu dalam detik, amplitudo dalam mV) dan judul yang menyebutkan fs.

Jalankan dari folder akar repositori:

    python exercises/cp1_load_plot.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

FS = 250          # Hz. Tanpa nilai ini, sumbu waktu tidak punya makna.
DURASI_PLOT = 5   # detik


def main() -> None:
    frame = pd.read_csv("data/ecg_sample.csv")
    print("Kolom yang tersedia :", list(frame.columns))
    print("Jumlah baris        :", len(frame))
    print("Ringkasan statistik :")
    print(frame.describe())

    waktu = frame["time_s"].to_numpy()
    ekg = frame["ecg_mv"].to_numpy()

    # indeks = waktu x fs. Inilah satu-satunya rumus yang perlu dihafal hari ini.
    jumlah_sampel = DURASI_PLOT * FS
    waktu_window = waktu[:jumlah_sampel]
    ekg_window = ekg[:jumlah_sampel]

    plt.figure(figsize=(11, 4))
    plt.plot(waktu_window, ekg_window, linewidth=1.0)
    plt.title(f"EKG sintetis, {DURASI_PLOT} detik pertama (fs = {FS} Hz)")
    plt.xlabel("Waktu (s)")
    plt.ylabel("Amplitudo (mV)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
