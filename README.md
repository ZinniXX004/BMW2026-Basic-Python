<div align="center">

# 🐍 BMW Basic 2026 — Materi I

### Applied Python for Medical Devices

**Biomedical Engineering Workshop** · Departemen Keilmuan dan Keprofesian<br>
Himpunan Mahasiswa Teknik Biomedik ITS

[![Uji Kode](https://github.com/ZinniXX004/BMW2026-Basic-Python/actions/workflows/uji-kode.yml/badge.svg)](https://github.com/ZinniXX004/BMW2026-Basic-Python/actions/workflows/uji-kode.yml)
[![Uji Environment](https://github.com/ZinniXX004/BMW2026-Basic-Python/actions/workflows/uji-environment.yml/badge.svg)](https://github.com/ZinniXX004/BMW2026-Basic-Python/actions/workflows/uji-environment.yml)

![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26.4-013243?logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2.2-150458?logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-1.13.1-8CAAE6?logo=scipy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22.0-3F4F75?logo=plotly&logoColor=white)

![Dataset](https://img.shields.io/badge/dataset-sintetis%20%2B%20MIT--BIH-2C7A4B)
![Lisensi data](https://img.shields.io/badge/lisensi%20data-ODC--BY%201.0-lightgrey)
![Hari-H](https://img.shields.io/badge/hari--H-22%20Agustus%202026-orange)

</div>

---

Repo ini isinya semua bahan **Materi I (Software / Python)** BMW Basic 2026. Berkas latihan, dataset, kunci jawaban, panduan setup, sampai tugas rumah — semuanya di sini, jadi kamu tidak perlu mengunduh apa pun saat sesi berlangsung.

| | |
| --- | --- |
| **Hari-1 (materi + simulasi)** | Sabtu, 22 Agustus 2026 · Teater B ITS |
| **Durasi Materi I** | 70 menit materi + 10 menit QnA + 60 menit simulasi |
| **Pemateri** | Jeremia Christ Immanuel Manalu (5023231017) |

## Yang bakal kamu bisa setelah sesi ini

1. Membaca CSV sinyal medis dan mengubahnya jadi array numerik.
2. Memotong sinyal berdasarkan waktu pakai hubungan `indeks = waktu × fs`.
3. Mendeteksi R-Peak pada EKG dengan ambang adaptif dan *refractory period*.
4. Menghitung laju jantung (BPM) dari interval RR.
5. Menjalankan dashboard Streamlit + Plotly untuk menampilkan hasilnya.

> [!WARNING]
> Semua kode di sini alat belajar rekayasa, **bukan alat diagnostik**. BPM yang benar secara angka tidak berarti tafsir klinisnya benar. Jangan dipakai untuk keputusan medis apa pun.

## Mulai dari sini

Kerjakan **sebelum** hari-H. Di Teater B tidak ada waktu buat instalasi.

```bash
git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git
cd BMW2026-Basic-Python

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
python data/make_dataset.py
python check_env.py
```

Langkah terakhir harus mencetak `ENVIRONMENT SIAP`. Kalau belum, mampir ke [TROUBLESHOOTING.md](TROUBLESHOOTING.md) dulu, lalu hubungi panitia Ilprof paling lambat H-3. Versi panjangnya ada di [SETUP.md](SETUP.md).

> [!IMPORTANT]
> Pakai **Python 3.11.9**. `numpy 1.26.4` dan `pandas 2.2.2` belum punya wheel untuk Python 3.13, jadi `pip install` pasti gagal di versi itu. Alasan tiap pin ditulis sebagai komentar di dalam `requirements.txt`.
>
> Jangan pasang `requirements-physionet.txt` untuk sesi hari-H — itu khusus jalur dataset nyata yang sifatnya opsional.

## Struktur repo

```text
BMW2026-Basic-Python/
│
├── README.md                    ← kamu sedang membacanya
├── SETUP.md                     panduan instalasi Windows / macOS / Linux
├── TROUBLESHOOTING.md           enam error paling sering + solusinya
├── ATTRIBUTION.md               lisensi & kutipan wajib untuk dataset nyata
├── check_env.py                 cek environment, cetak SIAP / BELUM SIAP
├── requirements.txt             versi terpaku, wajib dipakai
├── requirements-physionet.txt   hanya untuk jalur PhysioNet (opsional)
├── .gitattributes               normalisasi akhir baris lintas OS
│
├── .github/
│   ├── CODEOWNERS               peninjau otomatis untuk tiap perubahan
│   ├── PULL_REQUEST_TEMPLATE.md daftar cek sebelum PR dibuka
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01-error-teknis.yml      form lapor error (OS, versi, log)
│   │   ├── 02-pertanyaan-materi.yml form tanya konsep & KPP
│   │   └── config.yml               pintasan ke SETUP, TROUBLESHOOTING, KPP
│   └── workflows/
│       ├── uji-kode.yml         uji tiap push: dataset, BPM, kasus tepi
│       ├── uji-environment.yml  instal bersih di Windows/macOS/Linux
│       └── rilis.yml            tag v* → ZIP + GitHub Release otomatis
│
├── data/
│   ├── make_dataset.py          generator dataset sintetis, deterministik
│   ├── ecg_sample.csv           EKG 10 s @250 Hz, acuan 72,21 BPM
│   ├── ppg_sample.csv           PPG 10 s @250 Hz, acuan 87,92 BPM
│   ├── reference_bpm.csv        nilai acuan semua dataset (dipakai CI)
│   ├── PHYSIONET.md             panduan dataset nyata + tiga jebakan teknis
│   ├── fetch_physionet.py       unduh rekaman PhysioNet → CSV skema repo ini
│   ├── kpp/
│   │   └── subject_00.csv … subject_05.csv   dataset tugas rumah per NRP
│   └── demo/                    turunan MIT-BIH untuk live demo (ODC-BY 1.0)
│       ├── mitdb_100_250hz.csv       30 s kanal MLII, sudah di-resample
│       ├── mitdb_100_250hz_acuan.csv jumlah denyut & BPM anotasi kardiolog
│       └── SUMBER.md                 atribusi + cara berkas ini dibuat
│
├── exercises/                   ← yang kamu kerjakan saat simulasi
│   ├── cp1_load_plot.py         CP1: muat CSV, plot 5 detik pertama
│   ├── cp2_rpeak_bpm.py         CP2: deteksi R-peak, hitung BPM, bandingkan acuan
│   └── cp2b_validasi_anotasi.py bonus: Se & +P terhadap anotasi kardiolog
│
├── src/
│   ├── signal_utils.py          fungsi inti, berisi TODO CP2-a/b/c
│   └── app_dashboard.py         dashboard Streamlit + Plotly, TODO CP3-a/b
│
├── solutions/
│   └── signal_utils_solution.py kunci jawaban + pembanding scipy
│
├── demo/
│   └── live_demo_mitbih.py      demo panggung MIT-BIH, aman tanpa internet
│
├── tools/
│   ├── uji_cepat.py             18 pemeriksaan otomatis, dipakai CI
│   └── build_notebooks.py       ubah latihan jadi .ipynb (jalur fail-safe)
│
└── kpp/
    ├── INSTRUKSI_KPP.md         deliverable, format berkas, tenggat
    └── RUBRIK_PENILAIAN.md      bobot nilai, bonus, dan penalti
```

## Kalau instalasi lokal bermasalah

Urutan cadangannya begini:

1. **Notebook lokal** — `python tools/build_notebooks.py`, lalu buka di VS Code atau Jupyter.
2. **Google Colab** — unggah notebook hasil langkah 1, jalankan `!pip install -q plotly` kalau perlu, dan bangkitkan dataset dengan menjalankan `data/make_dataset.py` di sel pertama.
3. **Berpasangan** — kerjakan bareng peserta lain yang environment-nya sudah jalan. Checkpoint tetap dihitung, jadi tidak perlu merasa rugi.

## Otomasi yang jalan di repo ini

Tiga workflow GitHub Actions, dan semuanya ada gunanya buat kamu:

| Workflow | Kapan jalan | Yang dijaga |
| --- | --- | --- |
| **Uji Kode** | tiap push & pull request | Dataset tetap deterministik, BPM semua berkas masih akurat, kasus tepi tidak melempar exception, dan live demo tetap jalan walau data MIT-BIH belum ada |
| **Uji Environment** | saat `requirements.txt` berubah + tiap Senin | Instal bersih di Windows, macOS, dan Linux; `check_env.py` harus mencetak `ENVIRONMENT SIAP` |
| **Paket Rilis** | saat tag `v*` didorong | Merakit ZIP siap unggah ke Google Drive HMTB dan menerbitkan GitHub Release |

Manfaat praktisnya: kalau badge di atas hijau, artinya materi ini **baru saja terbukti jalan** di tiga sistem operasi. Kalau merah, jangan buang waktu menyalahkan laptopmu — buka tab **Actions**, lognya kelihatan.

Mau menjalankan pemeriksaan yang sama di mesin sendiri? Satu perintah:

```bash
python tools/uji_cepat.py
```

> [!NOTE]
> Selama repo masih privat, badge di atas bisa tampil abu-abu bagi orang luar. Setelah repo dipublikkan di H-7, statusnya muncul normal.

## Cara bertanya biar cepat dibantu

Buka tab **Issues**, pilih formnya:

- **Lapor error teknis** — formnya sudah menanyakan OS, versi Python, perintah, dan log error. Kelihatan repot, tapi justru itu yang membuat kami bisa menjawab dalam satu balasan, bukan lima.
- **Pertanyaan materi** — konsep, algoritma, fisiologi sinyal, atau soal KPP.

Pertanyaan yang jawabannya berguna untuk banyak orang akan kami angkat jadi FAQ. Jadi bertanya di Issues jauh lebih berdampak daripada DM.

## Live demo MIT-BIH (bagian pemateri)

Sinyal yang ditayangkan saat presentasi adalah rekaman manusia sungguhan: MIT-BIH Arrhythmia Database record 100, kanal MLII, lisensi ODC-BY 1.0. Demo memakai data yang sudah di-commit, bukan unduhan langsung — demo panggung tidak boleh bergantung pada Wi-Fi.

Sekali saja, di rumah, saat ada internet:

```bash
pip install -r requirements-physionet.txt
python demo/live_demo_mitbih.py --siapkan
git add data/demo && git commit -m "Tambah data demo MIT-BIH"
```

Saat presentasi, tanpa internet dan tanpa `wfdb`:

```bash
python demo/live_demo_mitbih.py
```

Kalau `data/demo/` kosong, skripnya tidak mati: ia beralih ke data sintetis dengan peringatan besar, dan demo tetap tuntas.

## Data sintetis dulu, data nyata kemudian

Sesi hari-H pakai sinyal sintetis dari `data/make_dataset.py`: BPM acuannya diketahui persis, tidak butuh jaringan, dan belum membawa artefak yang alatnya belum kamu punya.

Setelah kodemu jalan, lanjut ke rekaman manusia. Di situ detektormu akan **gagal**, dan bagian itulah yang paling banyak mengajari:

```bash
pip install -r requirements-physionet.txt
python data/fetch_physionet.py --daftar
python data/fetch_physionet.py --db mitdb --record 100 --durasi 60
python exercises/cp2b_validasi_anotasi.py --record 100 --durasi 60
```

Perintah terakhir membandingkan deteksimu dengan anotasi denyut buatan kardiolog, lalu melaporkan sensitivitas, presisi, dan selisih BPM.

Tiga jebakan yang pasti kamu temui — frekuensi cuplik (MIT-BIH 360 Hz, dataset kita 250 Hz; salah asumsi membuat BPM terbaca **0,694 kali lebih rendah** tanpa satu pun pesan error), satuan amplitudo, dan asumsi detektor yang dilanggar data nyata — dibahas lengkap dengan angka hasil pengukuran di [data/PHYSIONET.md](data/PHYSIONET.md).

## Soal parameter detektor

Default `persentil=95` bukan tebakan. Persentil 98 lulus di tujuh berkas EKG tapi gagal di `data/ppg_sample.csv`: BPM terbaca 67,60 padahal acuannya 87,92 — **tanpa pesan error apa pun**. Persentil 95 diuji pada delapan berkas dengan refractory 0,20–0,40 s, selisih maksimumnya 0,04 BPM.

Lihat sendiri bedanya:

```bash
python solutions/signal_utils_solution.py     # setelah sesi selesai
python exercises/cp2_rpeak_bpm.py --ppg --persentil 98
```

Ini alasan tiap detektor wajib divalidasi ke nilai acuan, bukan cuma dipastikan "tidak error".

## Tugas rumah (KPP)

Semua ketentuannya ada di [kpp/INSTRUKSI_KPP.md](kpp/INSTRUKSI_KPP.md) dan [kpp/RUBRIK_PENILAIAN.md](kpp/RUBRIK_PENILAIAN.md). Tenggat 7 hari setelah hari-1. Eksperimen dengan data PhysioNet bisa diajukan sebagai bonus maksimum +5.

## Lisensi dan atribusi data

Dataset sintetis di repo ini dibangkitkan secara numerik oleh `data/make_dataset.py` — tidak ada rekaman pasien nyata dan tidak ada data pihak ketiga di dalamnya.

Satu pengecualian yang disengaja: `data/demo/` berisi turunan MIT-BIH record 100 untuk live demo. MIT-BIH berlisensi ODC-BY 1.0 yang mengizinkan redistribusi turunan **dengan atribusi**, dan atribusinya ada di `data/demo/SUMBER.md` serta [ATTRIBUTION.md](ATTRIBUTION.md).

Dataset PhysioNet lain tidak disimpan di sini; ia diunduh saat kamu menjalankan skripnya. Yang dipakai berlisensi ODC-BY 1.0 atau CC BY 4.0 dan **wajib dikutip**. Keluarga MIMIC tidak dipakai karena butuh *credentialed access* dan Data Use Agreement yang melarang berbagi akses ke pihak ketiga.

<div align="center">

---

Dibuat untuk mahasiswa Teknik Biomedik ITS, angkatan 2024–2026.<br>
Kalau materi ini masih berguna tahun depan, berarti tugas kami beres.

</div>
