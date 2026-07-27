# BMW Basic 2026 — Materi I: Applied Python for Medical Devices

Repositori resmi **Materi I (Software / Python)** untuk *Biomedical Engineering Workshop (BMW) Basic 2026*, Departemen Keilmuan dan Keprofesian, Himpunan Mahasiswa Teknik Biomedik ITS.

- **Hari-1 (materi + simulasi):** Sabtu, 22 Agustus 2026, Teater B ITS
- **Durasi Materi I:** 70 menit materi + 10 menit QnA + 60 menit simulasi
- **Pemateri:** Jeremia Christ Immanuel Manalu (5023231017)

## Apa yang akan kamu bisa setelah sesi ini

1. Membaca file CSV sinyal medis dan mengubahnya menjadi array numerik.
2. Memotong sinyal berdasarkan waktu menggunakan hubungan `indeks = waktu × fs`.
3. Mendeteksi R-Peak pada sinyal EKG dengan ambang adaptif dan *refractory period*.
4. Menghitung laju jantung (BPM) dari interval RR.
5. Menjalankan dashboard Streamlit + Plotly untuk menampilkan hasil analisis.

> **Disclaimer akademik.** Seluruh kode di repositori ini adalah alat pembelajaran rekayasa, **bukan alat diagnostik**. Nilai BPM yang benar secara numerik tidak berarti interpretasi klinis yang benar. Jangan gunakan untuk pengambilan keputusan medis.

## Struktur repositori

```
requirements.txt        versi pustaka yang dipatok (wajib dipakai)
check_env.py            verifikasi environment sebelum hari-H
SETUP.md                langkah instalasi Windows/macOS/Linux
TROUBLESHOOTING.md      6 error paling sering + solusinya
data/make_dataset.py    generator dataset sintetis (offline, deterministik)
exercises/              berkas latihan sesi simulasi (CP1, CP2)
src/signal_utils.py     fungsi inti dengan TODO untuk diisi peserta
src/app_dashboard.py    dashboard Streamlit + Plotly (2 TODO)
solutions/              kunci jawaban, dibuka setelah sesi selesai
tools/build_notebooks.py membuat notebook .ipynb (jalur fail-safe)
kpp/                    instruksi dan rubrik penilaian tugas rumah
```

## Persiapan wajib sebelum 22 Agustus 2026

Lakukan **sebelum** hari-H. Tidak ada waktu instalasi di Teater B.

```bash
git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git
cd BMW2026-Basic-Python
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python data/make_dataset.py
python check_env.py
```

Langkah terakhir harus mencetak `ENVIRONMENT SIAP`. Jika tidak, baca `TROUBLESHOOTING.md`, lalu hubungi panitia Ilprof paling lambat H-3.

Detail lengkap ada di [SETUP.md](SETUP.md).

## Jalur fail-safe

Jika instalasi lokal gagal pada hari-H, urutan cadangannya:

1. **Notebook lokal** — `python tools/build_notebooks.py`, lalu buka di VS Code atau Jupyter.
2. **Google Colab** — unggah notebook hasil langkah 1 ke Colab, jalankan `!pip install -q plotly` bila perlu, dan bangkitkan dataset dengan menjalankan `data/make_dataset.py` di sel pertama.
3. **Berpasangan** — kerjakan bersama peserta lain yang environment-nya sudah jalan. Menyelesaikan checkpoint tetap dihitung.

## Tugas rumah (KPP)

Instruksi dan rubrik: [kpp/INSTRUKSI_KPP.md](kpp/INSTRUKSI_KPP.md) dan [kpp/RUBRIK_PENILAIAN.md](kpp/RUBRIK_PENILAIAN.md). Batas pengumpulan: 7 hari setelah hari-1.

## Lisensi dan atribusi data

Seluruh dataset di repositori ini **disintesis secara numerik** oleh `data/make_dataset.py`. Tidak ada rekaman pasien nyata dan tidak ada data dari basis data pihak ketiga, sehingga tidak ada persoalan lisensi maupun privasi. Jika kamu ingin bereksperimen dengan rekaman nyata (misalnya MIT-BIH di PhysioNet), unduh sendiri dan patuhi lisensi masing-masing dataset.
