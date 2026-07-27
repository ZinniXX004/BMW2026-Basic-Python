"""Penanda kemajuan CP2. Merah di awal itu normal.

Semua test di sini ditandai xfail ("expected to fail"), jadi pytest tidak
menganggapnya kegagalan selagi kerangka CP2 masih kosong. Begitu detektormu
benar, statusnya berubah jadi XPASS:

    pytest tests/test_cp2_progres.py -v

    xfail  = belum jalan, wajar
    XPASS  = sudah jalan, selamat

Jadi target belajarmu untuk CP2 sederhana: ubah sepuluh xfail jadi XPASS.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))

from src.signal_utils import find_r_peaks, hitung_bpm, hitung_sdnn_ms  # noqa: E402

FS = 250
DATA = AKAR / "data"
TOLERANSI_BPM = 3.0


def _baris_acuan() -> list[tuple[str, float]]:
    berkas = DATA / "reference_bpm.csv"
    if not berkas.is_file():
        return []
    acuan = pd.read_csv(berkas)
    return [(str(b["file"]), float(b["bpm_acuan"])) for _, b in acuan.iterrows()]


def _sinyal(berkas: str):
    kolom = "ppg_au" if "ppg" in berkas else "ecg_mv"
    return pd.read_csv(DATA / berkas)[kolom].to_numpy()


@pytest.mark.xfail(reason="menunggu TODO CP2-a/b/c dikerjakan", strict=False)
@pytest.mark.parametrize("berkas,target", _baris_acuan())
def test_bpm_mendekati_acuan(berkas, target):
    bpm = hitung_bpm(find_r_peaks(_sinyal(berkas), FS), FS)
    assert bpm == pytest.approx(target, abs=TOLERANSI_BPM)


@pytest.mark.xfail(reason="menunggu TODO CP2-a/b dikerjakan", strict=False)
def test_jumlah_puncak_ekg_wajar():
    puncak = find_r_peaks(_sinyal("ecg_sample.csv"), FS)
    assert 8 <= puncak.size <= 20


@pytest.mark.xfail(reason="menunggu TODO CP2 dikerjakan", strict=False)
def test_sdnn_ekg_masuk_kisaran_wajar():
    sdnn = hitung_sdnn_ms(find_r_peaks(_sinyal("ecg_sample.csv"), FS), FS)
    assert 5.0 < sdnn < 40.0
