# Notebook (jalur cadangan)

Jalur utama sesi ini tetap **VS Code + `.py`**, sesuai ToR. Folder ini untuk
keadaan darurat: instalasi lokal gagal, laptop pinjaman, atau kamu memang lebih
nyaman dengan notebook.

Dua berkas di sini **sudah siap dibuka** — tidak perlu membangkitkan apa pun:

| Berkas | Isi | Colab |
| --- | --- | --- |
| `01_cp1_load_plot.ipynb` | CP1: muat CSV, plot 5 detik pertama | [![Buka di Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZinniXX004/BMW2026-Basic-Python/blob/main/notebooks/01_cp1_load_plot.ipynb) |
| `02_cp2_rpeak_bpm.ipynb` | CP2: deteksi R-peak, BPM, validasi ke acuan | [![Buka di Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZinniXX004/BMW2026-Basic-Python/blob/main/notebooks/02_cp2_rpeak_bpm.ipynb) |

## Cara pakai

**Lokal (VS Code atau Jupyter)**

```bash
pip install -r requirements.txt
python data/make_dataset.py
# lalu buka notebooks/01_cp1_load_plot.ipynb
```

VS Code akan menawarkan memasang ekstensi Jupyter saat kamu membuka `.ipynb`
pertama kali. Terima saja. Pilih interpreter `.venv` di kanan atas.

**Google Colab**

Sel pertama tiap notebook sudah berisi perintah *bootstrap* (clone repo,
bangkitkan dataset). Jalankan sel itu lebih dulu, sisanya tinggal urut ke bawah.

## Dua hal yang wajib kamu tahu soal notebook

1. **Urutan sel bukan urutan tampilan, tapi urutan eksekusi.** Notebook yang
   dijalankan acak bisa memberi hasil yang tidak bisa diulang. Kalau ada yang
   aneh: `Runtime → Restart and run all`. Ini bukan kerewelan gaya — di kerja
   nyata, hasil analisis sinyal yang tidak bisa direproduksi sama saja dengan
   tidak ada hasil.
2. **Notebook bukan pengganti berkas `.py`.** Untuk KPP, yang dikumpulkan tetap
   sesuai [instruksi KPP](../kpp/INSTRUKSI_KPP.md). Notebook boleh jadi alat
   kerja, bukan bentuk akhir.

## Kalau mau membangkitkan notebook sendiri

```bash
python tools/build_notebooks.py
```

Skrip itu membungkus berkas `.py` mentah jadi notebook di
`notebooks/otomatis/`, terpisah dari dua notebook kurasi di folder ini. Berguna
kalau kamu mengubah berkas latihan dan mau versi notebooknya ikut berubah.
