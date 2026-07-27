"""Bungkus berkas latihan .py jadi notebook .ipynb (jalur fail-safe).

Dua notebook kurasi sudah ada dan siap dipakai:

    notebooks/01_cp1_load_plot.ipynb
    notebooks/02_cp2_rpeak_bpm.ipynb

Skrip ini untuk kebutuhan lain: kalau kamu mengubah berkas .py dan mau versi
notebook yang isinya persis sama. Hasilnya ditulis ke notebooks/otomatis/
supaya tidak menimpa dua notebook kurasi di atas.

    python tools/build_notebooks.py
"""

from __future__ import annotations

import json
import pathlib

AKAR = pathlib.Path(__file__).resolve().parents[1]
KELUARAN = AKAR / "notebooks" / "otomatis"

# Kunci jawaban sengaja tidak ada di repo peserta sebelum sesi selesai, jadi
# berkas itu tidak didaftarkan di sini. Kalau folder solutions/ nanti muncul
# (setelah 22 Agustus 2026), skrip ini otomatis ikut memprosesnya.
SUMBER = [
    ("exercises/cp1_load_plot.py", "01_cp1_load_plot.ipynb"),
    ("exercises/cp2_rpeak_bpm.py", "02_cp2_rpeak_bpm.ipynb"),
    ("exercises/cp2b_validasi_anotasi.py", "03_cp2b_validasi_anotasi.ipynb"),
    ("solutions/signal_utils_solution.py", "90_solusi_cp2.ipynb"),
]

PEMBUKA = (
    "# BMW Basic 2026 - Materi I\n"
    "\n"
    "Notebook ini dibangkitkan otomatis dari berkas .py di repositori, jadi\n"
    "isinya satu sel besar. Untuk belajar bertahap, pakai notebook kurasi di\n"
    "folder notebooks/ (01_cp1_load_plot.ipynb dan 02_cp2_rpeak_bpm.ipynb).\n"
    "\n"
    "Jika dijalankan di Google Colab, jalankan dulu sel bootstrap di bawah.\n"
)

SEL_COLAB = (
    "# Hanya untuk Google Colab (abaikan bila menjalankan lokal)\n"
    "# !pip install -q plotly==5.22.0\n"
    "# !git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git\n"
    "# %cd BMW2026-Basic-Python\n"
    "# !python data/make_dataset.py\n"
)

SEL_AKAR = (
    "# Pindah ke folder akar repo supaya path seperti data/ecg_sample.csv benar\n"
    "import os\n"
    "import pathlib\n"
    "\n"
    "akar = pathlib.Path.cwd()\n"
    "while not (akar / 'data').is_dir() and akar != akar.parent:\n"
    "    akar = akar.parent\n"
    "os.chdir(akar)\n"
    "print('Folder kerja:', akar)\n"
)


def sel_markdown(teks: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": teks.splitlines(keepends=True)}


def sel_kode(teks: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": teks.splitlines(keepends=True),
    }


def bangun(path_sumber: pathlib.Path) -> dict:
    isi = path_sumber.read_text(encoding="utf-8")
    isi = isi.replace("%matplotlib", "# %matplotlib")
    return {
        "cells": [
            sel_markdown(PEMBUKA),
            sel_kode(SEL_COLAB),
            sel_kode(SEL_AKAR),
            sel_kode("%matplotlib inline\n"),
            sel_kode(isi),
            sel_kode("# Berkas .py di repo ini dijalankan lewat main(); panggil di sini.\nmain()\n"),
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11.9"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    KELUARAN.mkdir(parents=True, exist_ok=True)
    dibuat = 0
    for relatif, nama in SUMBER:
        sumber = AKAR / relatif
        if not sumber.exists():
            print(f"Lewat  : {relatif} tidak ada di repo ini")
            continue
        target = KELUARAN / nama
        target.write_text(
            json.dumps(bangun(sumber), indent=1, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Dibuat : notebooks/otomatis/{nama}")
        dibuat += 1

    print(f"\nSelesai, {dibuat} notebook.")
    print("Buka di VS Code, atau jalankan: jupyter notebook")
    print("Notebook kurasi yang lebih enak dipakai: notebooks/01_*.ipynb dan 02_*.ipynb")


if __name__ == "__main__":
    main()
