"""Pemeriksaan cepat repositori peserta BMW Basic 2026 - Materi I.

Skrip ini sengaja TIDAK menyentuh kunci jawaban. Kunci jawaban tidak tinggal di
repositori ini; ia ada di repositori internal pemateri dan baru dipindahkan ke
sini setelah sesi simulasi selesai.

Yang diperiksa:
  A. Berkas wajib ada, dan tabel acuan konsisten dengan berkas dataset.
  B. Fungsi yang sudah jadi (muat, potong, normalisasi) berperilaku benar.
  C. Fitur HRV dan label laju jantung benar tepat di batas ambangnya.
  D. Kerangka TODO aman: mengembalikan hasil kosong, bukan melempar exception.
  E. Penanda TODO masih utuh, jadi kunci tidak pernah bocor ke repo peserta.

Jalankan dari folder akar repositori:

    python tools/uji_cepat.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

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

BERKAS_WAJIB = [
    "README.md",
    "SETUP.md",
    "TROUBLESHOOTING.md",
    "ATTRIBUTION.md",
    "requirements.txt",
    "requirements-physionet.txt",
    "check_env.py",
    "data/make_dataset.py",
    "data/reference_bpm.csv",
    "data/ecg_sample.csv",
    "data/ppg_sample.csv",
    "data/PHYSIONET.md",
    "data/fetch_physionet.py",
    "demo/live_demo_mitbih.py",
    "exercises/cp1_load_plot.py",
    "exercises/cp2_rpeak_bpm.py",
    "exercises/cp2b_validasi_anotasi.py",
    "src/signal_utils.py",
    "src/app_dashboard.py",
    "tools/build_notebooks.py",
    "kpp/INSTRUKSI_KPP.md",
    "kpp/RUBRIK_PENILAIAN.md",
]

gagal: list[str] = []


def cek(nama: str, kondisi: bool, detail: str = "") -> None:
    tanda = "LULUS" if kondisi else "GAGAL"
    print(f"  [{tanda}] {nama}" + (f" -> {detail}" if detail else ""))
    if not kondisi:
        gagal.append(nama)


def uji_berkas_dan_acuan() -> None:
    print("\nA. Berkas wajib dan tabel acuan")
    for relatif in BERKAS_WAJIB:
        cek(f"ada: {relatif}", (AKAR / relatif).is_file())

    acuan = pd.read_csv(AKAR / "data" / "reference_bpm.csv")
    cek(
        "kolom reference_bpm.csv",
        list(acuan.columns) == ["file", "jenis", "fs_hz", "bpm_acuan"],
        str(list(acuan.columns)),
    )
    cek("jumlah baris acuan = 8", len(acuan) == 8, f"{len(acuan)} baris")
    cek("semua fs acuan = 250 Hz", bool((acuan["fs_hz"] == 250).all()))
    cek(
        "bpm acuan dalam kisaran wajar 40-130",
        bool(acuan["bpm_acuan"].between(40, 130).all()),
        f"{acuan['bpm_acuan'].min():.2f} .. {acuan['bpm_acuan'].max():.2f}",
    )
    hilang = [b for b in acuan["file"] if not (AKAR / "data" / str(b)).is_file()]
    cek("semua berkas dataset pada tabel acuan ada", not hilang, ", ".join(hilang))


def uji_fungsi_siap_pakai() -> None:
    print("\nB. Fungsi yang sudah jadi")
    waktu, sinyal = muat_sinyal(str(AKAR / "data" / "ecg_sample.csv"), "ecg_mv")
    cek("panjang ecg_sample = 10 s x 250 Hz", sinyal.size == 2500, f"{sinyal.size} sampel")
    cek("kolom waktu sepanjang kolom nilai", waktu.size == sinyal.size)
    cek("selisih waktu antar sampel = 1/250 s", abs((waktu[1] - waktu[0]) - 1 / FS) < 1e-9)

    try:
        muat_sinyal(str(AKAR / "data" / "ecg_sample.csv"), "kolom_ngawur")
        cek("kolom salah memicu ValueError", False, "tidak ada exception")
    except ValueError:
        cek("kolom salah memicu ValueError", True)

    potong = potong_window(sinyal, FS, 0.0, 5.0)
    cek("potong_window 0-5 s = 1250 sampel", potong.size == 1250, f"{potong.size} sampel")

    z = normalisasi_zscore(sinyal)
    cek("z-score rata-rata = 0", abs(float(np.mean(z))) < 1e-9)
    cek("z-score simpangan baku = 1", abs(float(np.std(z)) - 1.0) < 1e-9)
    cek(
        "sinyal konstan tidak memicu pembagian nol",
        bool(np.all(normalisasi_zscore(np.ones(100)) == 0.0)),
    )


def uji_hrv_dan_label() -> None:
    print("\nC. Fitur HRV dan label laju jantung")
    puncak = np.array([0, 200, 400, 610, 800], dtype=int)
    sdnn = hitung_sdnn_ms(puncak, FS)
    cek("SDNN puncak uji = 32,66 ms", abs(sdnn - 32.66) < 0.05, f"{sdnn:.2f} ms")
    cek(
        "kurang dari 3 puncak -> SDNN NaN",
        np.isnan(hitung_sdnn_ms(np.array([0, 200], dtype=int), FS)),
    )

    kasus = [(45.0, "Bradikardia"), (72.0, "Normal"), (100.0, "Normal"), (130.0, "Takikardia")]
    for bpm, awalan in kasus:
        label = klasifikasi_hr(bpm)
        cek(f"{bpm:g} BPM -> {awalan}", label.startswith(awalan), label)
    cek(
        "BPM NaN -> tidak dapat dihitung",
        klasifikasi_hr(float("nan")) == "tidak dapat dihitung",
    )


def uji_kerangka_aman() -> None:
    print("\nD. Kerangka TODO aman dijalankan peserta")
    cek("PERSENTIL_DEFAULT = 95", PERSENTIL_DEFAULT == 95.0, str(PERSENTIL_DEFAULT))
    cek("REFRACTORY_DEFAULT = 0,25 s", REFRACTORY_DEFAULT == 0.25, str(REFRACTORY_DEFAULT))

    _, sinyal = muat_sinyal(str(AKAR / "data" / "ecg_sample.csv"), "ecg_mv")
    try:
        puncak = find_r_peaks(sinyal, FS)
        aman = isinstance(puncak, np.ndarray) and puncak.dtype.kind in "iu"
        cek("find_r_peaks mengembalikan array indeks", aman, f"dtype {puncak.dtype}")
    except Exception as galat:  # noqa: BLE001
        cek("find_r_peaks mengembalikan array indeks", False, repr(galat))

    cek(
        "puncak kosong -> BPM NaN",
        np.isnan(hitung_bpm(np.array([], dtype=int), FS)),
    )
    cek("satu puncak -> BPM NaN", np.isnan(hitung_bpm(np.array([5], dtype=int), FS)))

    tepi = {
        "sinyal konstan": np.ones(1000),
        "sinyal sangat pendek": np.array([0.0, 1.0, 0.0]),
        "sinyal nol semua": np.zeros(500),
    }
    for nama, contoh in tepi.items():
        try:
            hitung_bpm(find_r_peaks(contoh, FS), FS)
            cek(f"kasus tepi tanpa exception: {nama}", True)
        except Exception as galat:  # noqa: BLE001
            cek(f"kasus tepi tanpa exception: {nama}", False, repr(galat))


def uji_penanda_todo() -> None:
    print("\nE. Penanda TODO masih utuh")

    def baca(relatif: str) -> str:
        berkas = AKAR / relatif
        return berkas.read_text(encoding="utf-8") if berkas.is_file() else ""

    utils = baca("src/signal_utils.py")
    for penanda in ["TODO (CP2-a)", "TODO (CP2-b)", "TODO (CP2-c)"]:
        cek(f"{penanda} ada di src/signal_utils.py", penanda in utils)

    dashboard = baca("src/app_dashboard.py")
    for penanda in ["CP3-a", "CP3-b"]:
        cek(f"{penanda} ada di src/app_dashboard.py", penanda in dashboard)

    if (AKAR / "solutions").exists():
        print(
            "  [CATATAN] folder solutions/ terlihat di repo ini. Wajar bila sesi\n"
            "            simulasi sudah lewat dan kunci memang sengaja dibuka."
        )


def main() -> int:
    print("=" * 74)
    print("Uji cepat repositori peserta - BMW Basic 2026, Materi I (Python)")
    print(f"Akar repositori: {AKAR}")
    print("=" * 74)

    uji_berkas_dan_acuan()
    uji_fungsi_siap_pakai()
    uji_hrv_dan_label()
    uji_kerangka_aman()
    uji_penanda_todo()

    print("\n" + "=" * 74)
    if gagal:
        print(f"{len(gagal)} pemeriksaan GAGAL:")
        for nama in gagal:
            print(f"  - {nama}")
        print("=" * 74)
        return 1
    print("Semua pemeriksaan LULUS.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
