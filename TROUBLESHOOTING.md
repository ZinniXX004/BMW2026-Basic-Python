# TROUBLESHOOTING

Enam kegagalan yang paling sering terjadi, beserta penanganannya. Coba solusi di sini sebelum memanggil asisten.

## 1. `python` tidak dikenali (Windows)

**Gejala:** `python : The term 'python' is not recognized...`

**Sebab:** Python tidak masuk PATH saat instalasi.

**Solusi:** Jalankan ulang installer Python 3.11.9 → **Modify** → pastikan opsi *Add Python to environment variables* aktif. Tutup dan buka ulang terminal. Alternatif sementara: `py -3.11 -m venv .venv`.

## 2. `venv` gagal aktif di PowerShell

**Gejala:** *cannot be loaded because running scripts is disabled on this system*.

**Solusi:**

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Lalu `\.venv\Scripts\activate` lagi. Alternatif: gunakan `cmd.exe` dan `.venv\Scripts\activate.bat`.

## 3. `ModuleNotFoundError: No module named 'numpy'`

**Sebab:** Kode dijalankan dengan interpreter di luar `.venv`.

**Solusi:** Pastikan prompt terminal menampilkan `(.venv)`. Di VS Code, `Ctrl+Shift+P` → **Python: Select Interpreter** → pilih `.venv`. Verifikasi dengan:

```bash
python -c "import sys; print(sys.executable)"
```

Jalur yang tercetak harus berada di dalam folder `.venv`.

## 4. `FileNotFoundError: data/ecg_sample.csv`

**Sebab:** Dataset belum dibangkitkan, atau terminal berada di folder yang salah.

**Solusi:**

```bash
cd BMW2026-Basic-Python
python data/make_dataset.py
```

Jalankan skrip selalu dari folder akar repositori, bukan dari dalam `src/`.

## 5. Plot tidak muncul / jendela matplotlib kosong

**Solusi:** Pastikan skrip diakhiri dengan `plt.show()`. Jika dijalankan di dalam notebook, tambahkan `%matplotlib inline` pada sel pertama. Jika jendela muncul lalu langsung tertutup, jalankan lewat terminal, bukan lewat tombol *Run* mode debug.

## 6. Streamlit: port sudah terpakai

**Gejala:** *Port 8501 is already in use*.

**Solusi:**

```bash
streamlit run src/app_dashboard.py --server.port 8502
```

Jika browser tidak terbuka otomatis, buka manual alamat yang tercetak di terminal (`http://localhost:8502`).

## 7. BPM yang dihitung terasa mustahil (misal 180 pada sinyal tenang)

**Sebab paling umum:** *refractory period* belum diterapkan, sehingga satu kompleks QRS terdeteksi lebih dari sekali.

**Solusi:** Pastikan jarak minimum antar puncak sebesar `int(0.25 * fs)` sampel diterapkan sebelum menghitung interval RR. Bandingkan hasilmu dengan `data/reference_bpm.csv`.

## 8. `pip install -r requirements-physionet.txt` gagal / mencoba membangun pandas dari source

**Sebab:** versi `wfdb` yang lebih lama (4.1.0) mensyaratkan `pandas<2.0.0`, bentrok dengan `pandas==2.2.2` yang dipatok di `requirements.txt`. `requirements-physionet.txt` di repo ini sudah dipatok ke `wfdb==4.1.2` (mensyaratkan `pandas>=1.3.0`, tanpa batas atas) yang terpasang bersih berdampingan dengan `pandas==2.2.2`.

**Solusi:** pastikan `requirements-physionet.txt` yang kamu pakai berisi `wfdb==4.1.2`, bukan `4.1.0`. Kalau masih gagal, hapus dulu `pip uninstall wfdb pandas -y` lalu pasang ulang urut: `pip install -r requirements.txt` dulu, baru `pip install -r requirements-physionet.txt`.

## Masih gagal?

Catat: (1) sistem operasi, (2) output `python check_env.py`, (3) pesan error lengkap. Kirim ketiganya ke panitia Ilprof. Jangan menghapus dan memasang ulang Python tanpa arahan asisten pada hari-H.
