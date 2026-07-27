# SETUP — Environment Materi I

Target: **Python 3.11.9**, virtual environment lokal, VS Code sebagai editor. Selesaikan ini **sebelum** 22 Agustus 2026.

## 0. Prinsip

- Jangan memasang pustaka ke Python sistem. Selalu gunakan virtual environment (`.venv`).
- Jangan mengubah versi di `requirements.txt`. Versi dipatok agar seluruh kelas berperilaku identik.
- Satu kelas dengan 120 peserta tidak punya waktu untuk debug instalasi. Semua verifikasi terjadi sebelum hari-H.

## 1. Windows 10/11

1. Unduh **Python 3.11.9** dari <https://www.python.org/downloads/release/python-3119/> (Windows installer 64-bit).
2. Pada layar pertama installer, centang **Add python.exe to PATH**. Ini wajib.
3. Jangan gunakan Python dari Microsoft Store. Versi Store membatasi akses folder dan sering menggagalkan `venv`.
4. Pasang **VS Code** dari <https://code.visualstudio.com/>, lalu pasang ekstensi **Python** (Microsoft).
5. Buka PowerShell di folder kerja:

   ```powershell
   git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git
   cd BMW2026-Basic-Python
   python --version          # harus 3.11.9
   python -m venv .venv
   .venv\Scripts\activate    # prompt berubah menjadi (.venv)
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python data/make_dataset.py
   python check_env.py
   ```

6. Jika PowerShell menolak aktivasi dengan pesan *running scripts is disabled*, jalankan sekali:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

7. Di VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → pilih interpreter di dalam `.venv`.

## 2. macOS

```bash
git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git
cd BMW2026-Basic-Python
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python data/make_dataset.py
python check_env.py
```

Jika `python3.11` tidak ada, pasang lewat installer python.org atau `brew install python@3.11`.

## 3. Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt install -y python3.11 python3.11-venv git
git clone https://github.com/ZinniXX004/BMW2026-Basic-Python.git
cd BMW2026-Basic-Python
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data/make_dataset.py
python check_env.py
```

## 4. Kriteria lulus

`python check_env.py` harus mencetak `ENVIRONMENT SIAP` beserta tabel versi. Simpan tangkapan layarnya; panitia dapat memintanya saat registrasi.

## 5. Pengaturan untuk hari-H

- Bawa **charger**. Sesi berjalan sekitar 7 jam.
- Naikkan ukuran font editor ke minimal 16 pt agar asisten dapat membantu dari samping.
- Matikan pembaruan otomatis Windows pada hari-H.
- Unduh repositori **sebelum** datang. Wi-Fi ruangan tidak dijamin cukup untuk 120 peserta.
