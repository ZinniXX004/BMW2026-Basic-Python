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

Uji juga pada PPG untuk melihat bahwa parameter yang cocok untuk satu jenis
sinyal belum tentu cocok untuk jenis lain:

    python exercises/cp2_rpeak_bpm.py --ppg
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from src.signal_utils import (
    PERSENTIL_DEFAULT,
    REFRACTORY_DEFAULT,
    find_r_peaks,
    hitung_bpm,
    hitung_sdnn_ms,
    klasifikasi_hr,
    normalisasi_zscore,
)

FS = 250


def main() -> None:
    parser = argparse.ArgumentParser(description="CP2 - deteksi R-Peak dan hitung BPM.")
    parser.add_argument("--ppg", action="store_true", help="Pakai data/ppg_sample.csv.")
    parser.add_argument("--persentil", type=float, default=PERSENTIL_DEFAULT)
    parser.add_argument("--refractory", type=float, default=REFRACTORY_DEFAULT)
    argumen = parser.parse_args()

    berkas = "ppg_sample.csv" if argumen.ppg else "ecg_sample.csv"
    kolom = "ppg_au" if argumen.ppg else "ecg_mv"
    sinyal = pd.read_csv(f"data/{berkas}")[kolom].to_numpy()

    puncak = find_r_peaks(sinyal, FS, persentil=argumen.persentil, refractory_s=argumen.refractory)
    bpm = hitung_bpm(puncak, FS)
    sdnn = hitung_sdnn_ms(puncak, FS)

    print(f"Berkas                   : data/{berkas}")
    print(f"Parameter                : persentil={argumen.persentil}, refractory={argumen.refractory} s")
    print(f"Jumlah puncak terdeteksi : {puncak.size}")
    print(f"BPM                      : {bpm:.2f}")
    print(f"SDNN                     : {sdnn:.2f} ms")
    print(f"Label (dewasa istirahat) : {klasifikasi_hr(bpm)}")

    acuan = pd.read_csv("data/reference_bpm.csv")
    bpm_acuan = float(acuan.loc[acuan["file"] == berkas, "bpm_acuan"].iloc[0])
    print(f"\nBPM acuan                : {bpm_acuan:.2f}")
    if not np.isnan(bpm):
        selisih = abs(bpm - bpm_acuan)
        status = "LULUS" if selisih <= 3.0 else "BELUM LULUS"
        print(f"Selisih                  : {selisih:.2f} BPM -> {status}")
        if selisih > 3.0:
            print("\nPetunjuk urutan pemeriksaan:")
            print("  1. Jumlah puncak jauh lebih sedikit dari denyut sebenarnya?")
            print("     Ambang persentil terlalu tinggi. Turunkan --persentil.")
            print("  2. Jumlah puncak jauh lebih banyak? Refractory terlalu pendek,")
            print("     gelombang T ikut terhitung. Naikkan --refractory.")
            print("  3. Jumlah puncak benar tetapi BPM tetap salah? Periksa fs.")

    x = normalisasi_zscore(sinyal)
    pembanding, _ = find_peaks(
        x, height=np.percentile(x, argumen.persentil), distance=int(argumen.refractory * FS)
    )
    print(f"\nPembanding scipy         : {pembanding.size} puncak")
    print("Implementasi manual untuk paham; pustaka untuk pekerjaan nyata.")

    if puncak.size:
        plt.figure(figsize=(11, 4))
        plt.plot(np.arange(sinyal.size) / FS, sinyal, linewidth=0.9, label=kolom)
        plt.plot(puncak / FS, sinyal[puncak], "o", markersize=5, label="Puncak")
        plt.title(f"Deteksi puncak, BPM = {bpm:.1f} (fs = {FS} Hz)")
        plt.xlabel("Waktu (s)")
        plt.ylabel("Amplitudo")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
    else:
        print("\nBelum ada puncak terdeteksi. Periksa kembali TODO CP2-a dan CP2-b.")


if __name__ == "__main__":
    main()
