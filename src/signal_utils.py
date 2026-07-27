"""Fungsi inti pemrosesan sinyal untuk BMW Basic 2026 - Materi I.

Bagian bertanda TODO diisi oleh peserta pada sesi simulasi (CP2).
Kunci jawaban ada di solutions/signal_utils_solution.py dan dibuka setelah sesi.

Catatan rekayasa: modul ini alat pembelajaran, bukan perangkat diagnostik.
Deteksi R-Peak kelas klinis membutuhkan pra-filter bandpass, penolakan artefak,
ambang adaptif dinamis, dan validasi terhadap basis data teranotasi.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def muat_sinyal(path: str, kolom_nilai: str) -> tuple[np.ndarray, np.ndarray]:
    """Muat CSV sinyal dan kembalikan (waktu, nilai) sebagai array NumPy.

    Pandas dipakai untuk membaca tabel; NumPy dipakai untuk menghitung.
    Method .to_numpy() adalah jembatan antara kedua lapisan tersebut.
    """
    frame = pd.read_csv(path)
    if "time_s" not in frame.columns or kolom_nilai not in frame.columns:
        raise ValueError(
            f"Kolom yang diharapkan tidak ada. Ditemukan: {list(frame.columns)}"
        )
    return frame["time_s"].to_numpy(), frame[kolom_nilai].to_numpy()


def potong_window(sinyal: np.ndarray, fs: int, mulai_s: float, akhir_s: float) -> np.ndarray:
    """Potong sinyal berdasarkan waktu, memakai hubungan indeks = waktu x fs."""
    indeks_mulai = int(mulai_s * fs)
    indeks_akhir = int(akhir_s * fs)
    return sinyal[indeks_mulai:indeks_akhir]


def normalisasi_zscore(sinyal: np.ndarray) -> np.ndarray:
    """Ubah sinyal menjadi satuan simpangan baku.

    Alasan fisiologis: amplitudo EKG bergantung pada penempatan elektroda,
    impedansi kulit, dan gain penguat. Tanpa normalisasi, ambang absolut yang
    cocok untuk satu subjek akan gagal untuk subjek lain.
    """
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
    """Deteksi indeks R-Peak pada sinyal EKG.

    Algoritma:
      1. Normalisasi z-score agar ambang tidak bergantung amplitudo mentah.
      2. Ambang adaptif pada persentil tertentu dari sinyal ternormalisasi.
      3. Kandidat puncak = titik di atas ambang yang lebih tinggi dari kedua
         tetangganya (maksimum lokal).
      4. Refractory period: dua puncak tidak boleh berjarak kurang dari
         refractory_s detik. Ini bukan trik numerik, tetapi konsekuensi periode
         refrakter miokardium; dua depolarisasi ventrikel dalam 250 ms tidak
         mungkin secara fisiologis.

    Kembalian: array indeks sampel puncak, urut naik.
    """
    x = normalisasi_zscore(sinyal)
    ambang = np.percentile(x, persentil)
    jarak_min = int(refractory_s * fs)

    kandidat: list[int] = []
    for i in range(1, x.size - 1):
        # TODO (CP2-a): tambahkan indeks i ke kandidat bila x[i] melebihi ambang
        # DAN x[i] lebih besar dari x[i - 1] serta x[i + 1].
        pass

    puncak: list[int] = []
    for indeks in kandidat:
        # TODO (CP2-b): terapkan refractory period.
        # Jika daftar puncak masih kosong, terima indeks ini.
        # Jika jarak ke puncak terakhir kurang dari jarak_min, simpan hanya yang
        # amplitudonya lebih besar (ganti puncak terakhir bila perlu).
        # Selain itu, tambahkan sebagai puncak baru.
        pass

    return np.asarray(puncak, dtype=int)


def hitung_bpm(puncak: np.ndarray, fs: int) -> float:
    """Hitung laju jantung rata-rata dari indeks puncak.

    Interval RR dalam detik = selisih indeks dibagi fs.
    BPM = 60 dibagi rata-rata interval RR.
    Kurang dari dua puncak berarti laju tidak dapat dihitung; kembalikan NaN
    daripada menghasilkan angka yang menyesatkan.
    """
    if puncak.size < 2:
        return float("nan")
    # TODO (CP2-c): hitung interval RR, lalu kembalikan 60 / rata-rata RR.
    return float("nan")


def hitung_sdnn_ms(puncak: np.ndarray, fs: int) -> float:
    """SDNN: simpangan baku interval RR dalam milidetik.

    SDNN adalah indeks variabilitas laju jantung (HRV) paling dasar. Nilai
    absolutnya tidak dapat ditafsirkan tanpa konteks durasi rekaman dan kondisi
    subjek; di sini ia dipakai sebagai latihan ekstraksi fitur.
    """
    if puncak.size < 3:
        return float("nan")
    rr = np.diff(puncak) / fs
    return float(np.std(rr, ddof=1) * 1000.0)


def klasifikasi_hr(bpm: float) -> str:
    """Label kasar laju jantung untuk dewasa saat istirahat.

    PERINGATAN: ambang 60 dan 100 hanya berlaku untuk dewasa saat istirahat.
    Neonatus 120-160 BPM adalah normal, dan atlet terlatih dapat berada di
    kisaran 40-an tanpa patologi. Label ini bukan diagnosis.
    """
    if np.isnan(bpm):
        return "tidak dapat dihitung"
    if bpm < 60:
        return "Bradikardia (dewasa istirahat)"
    if bpm <= 100:
        return "Normal (dewasa istirahat)"
    return "Takikardia (dewasa istirahat)"
