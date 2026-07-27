"""Test untuk fungsi yang SUDAH jadi di src/signal_utils.py.

Semua test di berkas ini harus hijau sejak instalasimu selesai, bahkan sebelum
satu pun TODO dikerjakan. Kalau ada yang merah di sini, masalahnya di
environment atau dataset, bukan di jawabanmu.

Jalankan dari folder akar repositori:

    pytest tests/test_fungsi_dasar.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))

from src.signal_utils import (  # noqa: E402
    PERSENTIL_DEFAULT,
    REFRACTORY_DEFAULT,
    find_r_peaks,
    hitung_bpm,
    hitung_sdnn_ms,
    klasifikasi_hr,
    muat_sinyal,
    normalisasi_zscore,
    potong_window,
)

FS = 250
DATA = AKAR / "data"
ECG = str(DATA / "ecg_sample.csv")


def test_dataset_sudah_dibangkitkan():
    assert DATA.joinpath("ecg_sample.csv").is_file(), "Jalankan dulu: python data/make_dataset.py"


def test_muat_sinyal_panjangnya_benar():
    waktu, sinyal = muat_sinyal(ECG, "ecg_mv")
    assert sinyal.size == 2500
    assert waktu.size == sinyal.size


def test_selisih_waktu_sesuai_fs():
    waktu, _ = muat_sinyal(ECG, "ecg_mv")
    assert waktu[1] - waktu[0] == pytest.approx(1 / FS, abs=1e-9)


def test_kolom_salah_melempar_valueerror():
    with pytest.raises(ValueError):
        muat_sinyal(ECG, "kolom_ngawur")


def test_potong_window_lima_detik_pertama():
    _, sinyal = muat_sinyal(ECG, "ecg_mv")
    assert potong_window(sinyal, FS, 0.0, 5.0).size == 1250


def test_zscore_mean_nol_std_satu():
    _, sinyal = muat_sinyal(ECG, "ecg_mv")
    z = normalisasi_zscore(sinyal)
    assert float(np.mean(z)) == pytest.approx(0.0, abs=1e-9)
    assert float(np.std(z)) == pytest.approx(1.0, abs=1e-9)


def test_zscore_sinyal_konstan_tidak_membagi_nol():
    assert np.all(normalisasi_zscore(np.ones(100)) == 0.0)


def test_sdnn_pada_puncak_buatan():
    puncak = np.array([0, 200, 400, 610, 800], dtype=int)
    assert hitung_sdnn_ms(puncak, FS) == pytest.approx(32.66, abs=0.05)


def test_sdnn_butuh_minimal_tiga_puncak():
    assert np.isnan(hitung_sdnn_ms(np.array([0, 200], dtype=int), FS))


@pytest.mark.parametrize(
    "bpm,awalan",
    [
        (45.0, "Bradikardia"),
        (59.9, "Bradikardia"),
        (60.0, "Normal"),
        (72.0, "Normal"),
        (100.0, "Normal"),
        (100.1, "Takikardia"),
        (130.0, "Takikardia"),
    ],
)
def test_klasifikasi_hr_di_batas_ambang(bpm, awalan):
    assert klasifikasi_hr(bpm).startswith(awalan)


def test_klasifikasi_hr_nan():
    assert klasifikasi_hr(float("nan")) == "tidak dapat dihitung"


@pytest.mark.parametrize("puncak", [[], [5]])
def test_bpm_nan_kalau_puncak_kurang_dari_dua(puncak):
    assert np.isnan(hitung_bpm(np.asarray(puncak, dtype=int), FS))


def test_parameter_default_sesuai_materi():
    assert PERSENTIL_DEFAULT == 95.0
    assert REFRACTORY_DEFAULT == 0.25


@pytest.mark.parametrize(
    "nama,contoh",
    [
        ("konstan", np.ones(1000)),
        ("sangat pendek", np.array([0.0, 1.0, 0.0])),
        ("nol semua", np.zeros(500)),
    ],
)
def test_kerangka_tidak_meledak_di_kasus_tepi(nama, contoh):
    hitung_bpm(find_r_peaks(contoh, FS), FS)


def test_find_r_peaks_mengembalikan_array_indeks():
    _, sinyal = muat_sinyal(ECG, "ecg_mv")
    puncak = find_r_peaks(sinyal, FS)
    assert isinstance(puncak, np.ndarray)
    assert puncak.dtype.kind in "iu"
