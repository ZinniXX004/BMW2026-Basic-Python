"""Verifikasi environment untuk BMW Basic 2026 - Materi I (Python).

Jalankan dari folder akar repositori:

    python check_env.py

Skrip ini memeriksa versi interpreter, keberadaan dan versi pustaka yang
dipatok, serta ketersediaan dataset. Keluaran akhir harus 'ENVIRONMENT SIAP'.
"""

from __future__ import annotations

import importlib
import pathlib
import sys

TARGET_PYTHON = (3, 11)

EXPECTED = {
    "numpy": "1.26.4",
    "pandas": "2.2.2",
    "matplotlib": "3.8.4",
    "scipy": "1.13.1",
    "plotly": "5.22.0",
    "streamlit": "1.35.0",
}

DATA_FILES = [
    "data/ecg_sample.csv",
    "data/ppg_sample.csv",
    "data/reference_bpm.csv",
]

# Berkas ini opsional bagi peserta, tetapi WAJIB bagi pemateri sebelum hari-H.
DEMO_FILES = [
    "data/demo/mitdb_100_250hz.csv",
    "data/demo/mitdb_100_250hz_acuan.csv",
]


def check_python() -> list[str]:
    problems: list[str] = []
    major, minor = sys.version_info[:2]
    print(f"Python            : {sys.version.split()[0]}")
    print(f"Interpreter       : {sys.executable}")
    if (major, minor) != TARGET_PYTHON:
        problems.append(
            f"Versi Python {major}.{minor} bukan target 3.11. "
            "Pustaka yang dipatok belum diuji di versi ini."
        )
    if (major, minor) >= (3, 13):
        problems.append(
            f"Python {major}.{minor} tidak punya wheel untuk numpy 1.26.4 dan "
            "pandas 2.2.2. Instalasi requirements.txt akan gagal. Pasang Python 3.11.9."
        )
    if ".venv" not in sys.executable.replace("\\\\", "/"):
        problems.append(
            "Interpreter tampaknya bukan dari .venv. Aktifkan virtual environment "
            "atau pilih interpreter .venv di VS Code."
        )
    return problems


def check_packages() -> list[str]:
    problems: list[str] = []
    print("\nPustaka:")
    for name, expected in EXPECTED.items():
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"  {name:<12} TIDAK TERPASANG")
            problems.append(f"{name} belum terpasang. Jalankan: pip install -r requirements.txt")
            continue
        found = getattr(module, "__version__", "tidak diketahui")
        status = "ok" if found == expected else f"beda (diharapkan {expected})"
        print(f"  {name:<12} {found:<10} {status}")
        if found != expected:
            problems.append(
                f"{name} versi {found}, diharapkan {expected}. "
                "Perbedaan versi dapat mengubah perilaku pada sesi simulasi."
            )
    return problems


def check_data() -> list[str]:
    problems: list[str] = []
    print("\nDataset:")
    for relative in DATA_FILES:
        path = pathlib.Path(relative)
        if path.exists():
            print(f"  {relative:<34} ada ({path.stat().st_size // 1024} KB)")
        else:
            print(f"  {relative:<34} HILANG")
            problems.append(f"{relative} belum ada. Jalankan: python data/make_dataset.py")
    return problems


def check_demo() -> None:
    """Informasi saja, bukan syarat kelulusan environment peserta."""
    print("\nData live demo MIT-BIH (wajib untuk pemateri, opsional untuk peserta):")
    hilang = False
    for relative in DEMO_FILES:
        path = pathlib.Path(relative)
        if path.exists():
            print(f"  {relative:<34} ada ({path.stat().st_size // 1024} KB)")
        else:
            print(f"  {relative:<34} belum ada")
            hilang = True
    if hilang:
        print("  Untuk menyiapkan: pip install -r requirements-physionet.txt")
        print("                    python demo/live_demo_mitbih.py --siapkan")
        print("  Tanpa berkas ini, live demo tetap jalan tetapi memakai data sintetis.")


def main() -> int:
    print("=" * 62)
    print("BMW Basic 2026 - Materi I | Verifikasi environment")
    print("=" * 62)
    problems = check_python() + check_packages() + check_data()
    check_demo()
    print("-" * 62)
    if problems:
        print("ENVIRONMENT BELUM SIAP. Masalah yang ditemukan:\n")
        for index, problem in enumerate(problems, start=1):
            print(f"  {index}. {problem}")
        print("\nBaca TROUBLESHOOTING.md, lalu jalankan ulang skrip ini.")
        return 1
    print("ENVIRONMENT SIAP")
    print("Simpan tangkapan layar keluaran ini sebagai bukti persiapan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
