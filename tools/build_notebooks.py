"""Bangun notebook .ipynb dari berkas latihan (jalur fail-safe).

Dipakai bila peserta lebih nyaman dengan notebook, atau bila akan diunggah ke
Google Colab sebagai cadangan ketika environment lokal gagal.

    python tools/build_notebooks.py

Hasil: folder notebooks/ berisi satu notebook per berkas latihan.
"""

from __future__ import annotations

import json
import pathlib

AKAR = pathlib.Path(__file__).resolve().parents[1]
SUMBER = [
    ("exercises/cp1_load_plot.py", "01_cp1_load_plot.ipynb"),
    ("exercises/cp2_rpeak_bpm.py", "02_cp2_rpeak_bpm.ipynb"),
    ("solutions/signal_utils_solution.py", "90_solusi_cp2.ipynb"),
]

PEMBUKA = (
    "# BMW Basic 2026 - Materi I\n"
    "\n"
    "Notebook ini dibangkitkan otomatis dari berkas .py di repositori.\n"
    "Jika dijalankan di Google Colab, jalankan dulu dua sel berikut.\n"
)

SEL_COLAB = (
    "# Hanya untuk Google Colab (abaikan bila menjalankan lokal)\n"
    "# !pip install -q plotly==5.22.0\n"
    "# !git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git\n"
    "# %cd BMW2026-Basic-Python\n"
    "# !python data/make_dataset.py\n"
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
            sel_kode("%matplotlib inline\n"),
            sel_kode(isi),
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
    keluaran = AKAR / "notebooks"
    keluaran.mkdir(exist_ok=True)
    for relatif, nama in SUMBER:
        sumber = AKAR / relatif
        if not sumber.exists():
            print(f"Lewat: {relatif} tidak ditemukan")
            continue
        target = keluaran / nama
        target.write_text(json.dumps(bangun(sumber), indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"Dibuat: notebooks/{nama}")
    print("\nBuka notebook di VS Code atau jalankan: jupyter notebook")


if __name__ == "__main__":
    main()
