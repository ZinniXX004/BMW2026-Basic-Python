"""Uji cepat repo: memastikan kunci jawaban masih menghasilkan BPM yang benar.

Dipakai GitHub Actions, dan boleh kamu jalankan sendiri kapan saja:

    python tools/uji_cepat.py

Kalau ada satu pemeriksaan gagal, skrip keluar dengan kode 1 sehingga CI
langsung merah. Jadi kalau ada yang rusak, kita tahu jauh sebelum hari-H.
Tidak ada yang perlu kamu isi di sini - berkas latihan tetap di exercises/.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))

from solutions import signal_utils_solution as kunci  # noqa: E402
from src.signal_utils import hitung_sdnn_ms, klasifikasi_hr  # noqa: E402

find_r_peaks = kunci.find_r_peaks
hitung_bpm = kunci.hitung_bpm
PERSENTIL = getattr(kunci, "PERSENTIL_DEFAULT", 95.0)
REFRACTORY = getattr(kunci, "REFRACTORY_DEFAULT", 0.25)

TOLERANSI_BPM = 1.0
FS = 250

gagal: list[str] = []


def cek(nama: str, kondisi: bool, detail: str = "") -> None:
    tanda = " OK " if kondisi else "GAGAL"
    print(f"  [{tanda}] {nama}" + (f" -> {detail}" if detail else ""))
    if not kondisi:
        gagal.append(nama)


def cari_berkas(nama: str) -> Path | None:
    langsung = AKAR / "data" / nama
    if langsung.exists():
        return langsung
    kandidat = sorted((AKAR / "data").rglob(Path(nama).name))
    return kandidat[0] if kandidat else None


def sinyal_dari(path: Path) -> np.ndarray:
    tabel = pd.read_csv(path)
    return tabel[tabel.columns[1]].to_numpy()


def uji_akurasi_bpm() -> None:
    print("\n1. Akurasi BPM terhadap data/reference_bpm.csv")
    acuan = pd.read_csv(AKAR / "data" / "reference_bpm.csv")
    for baris in acuan.itertuples(index=False):
        berkas = cari_berkas(str(baris.file))
        if berkas is None:
            cek(f"{baris.file} tersedia", False, "berkas tidak ditemukan")
            continue
        fs = int(baris.fs_hz)
        puncak = find_r_peaks(sinyal_dari(berkas), fs)
        bpm = hitung_bpm(puncak, fs)
        selisih = abs(bpm - float(baris.bpm_acuan))
        cek(
            f"{baris.file} ({baris.jenis})",
            selisih <= TOLERANSI_BPM,
            f"{len(puncak)} puncak, {bpm:.2f} BPM vs acuan {float(baris.bpm_acuan):.2f}, selisih {selisih:.2f}",
        )


def uji_sdnn_dan_label() -> None:
    print("\n2. SDNN dan klasifikasi laju jantung")
    puncak = find_r_peaks(sinyal_dari(AKAR / "data" / "ecg_sample.csv"), FS)
    sdnn = hitung_sdnn_ms(puncak, FS)
    cek("SDNN masuk rentang wajar (0-200 ms)", 0.0 < sdnn < 200.0, f"{sdnn:.2f} ms")
    cek("45 BPM -> Bradikardia", klasifikasi_hr(45.0).startswith("Bradikardia"))
    cek("72 BPM -> Normal", klasifikasi_hr(72.0).startswith("Normal"))
    cek("100 BPM masih Normal", klasifikasi_hr(100.0).startswith("Normal"))
    cek("130 BPM -> Takikardia", klasifikasi_hr(130.0).startswith("Takikardia"))
    cek("NaN ditangani", klasifikasi_hr(float("nan")) == "tidak dapat dihitung")


def uji_kasus_tepi() -> None:
    print("\n3. Kasus tepi tidak boleh melempar exception")
    kasus = {
        "sinyal rata (std = 0)": np.zeros(1000),
        "sinyal 3 sampel": np.array([0.0, 1.0, 0.0]),
        "satu spike": np.concatenate([np.zeros(500), [5.0], np.zeros(499)]),
    }
    for nama, sinyal in kasus.items():
        try:
            puncak = find_r_peaks(sinyal, FS)
            bpm = hitung_bpm(puncak, FS)
            aman = isinstance(bpm, float)
            nilai = "nan" if math.isnan(bpm) else f"{bpm:.2f}"
            detail = f"{len(puncak)} puncak, bpm={nilai}"
        except Exception as galat:  # noqa: BLE001
            aman, detail = False, f"{type(galat).__name__}: {galat}"
        cek(nama, aman, detail)


def uji_jebakan_fs() -> None:
    print("\n4. Jebakan fs: salah fs harus menggeser BPM, bukan diam-diam benar")
    puncak = find_r_peaks(sinyal_dari(AKAR / "data" / "ecg_sample.csv"), FS)
    benar = hitung_bpm(puncak, FS)
    salah = hitung_bpm(puncak, 360)
    rasio = salah / benar
    cek(
        "data 250 Hz dianggap 360 Hz -> BPM naik 1,44x",
        abs(rasio - 360 / 250) < 0.01,
        f"{benar:.2f} -> {salah:.2f} BPM (rasio {rasio:.3f})",
    )


def main() -> int:
    print("=" * 70)
    print("UJI CEPAT REPO BMW BASIC 2026 - MATERI I (PYTHON)")
    print(f"persentil default {PERSENTIL} | refractory default {REFRACTORY} s | toleransi +/- {TOLERANSI_BPM} BPM")
    print("=" * 70)

    uji_akurasi_bpm()
    uji_sdnn_dan_label()
    uji_kasus_tepi()
    uji_jebakan_fs()

    print("\n" + "=" * 70)
    if gagal:
        print(f"HASIL: {len(gagal)} pemeriksaan GAGAL")
        for nama in gagal:
            print(f"  - {nama}")
        print("=" * 70)
        return 1
    print("HASIL: semua pemeriksaan lulus")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
