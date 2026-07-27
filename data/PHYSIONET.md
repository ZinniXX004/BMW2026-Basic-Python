# Panduan Dataset Nyata PhysioNet

Jalur **opsional**. Sesi hari-H tetap memakai dataset sintetis di `data/`. Panduan ini untuk peserta yang ingin menguji kode buatannya pada rekaman manusia sungguhan, dan untuk bonus KPP.

Baca [ATTRIBUTION.md](../ATTRIBUTION.md) lebih dulu. Kewajiban kutipan bukan formalitas administratif; itu syarat lisensi.

---

## 1. Mengapa sesi memakai data sintetis, bukan data nyata

Empat alasan rekayasa, bukan alasan kemalasan:

1. **Determinisme.** Dataset sintetis punya BPM acuan yang diketahui persis. Kamu bisa tahu jawabanmu benar tanpa menebak.
2. **Ukuran.** Satu rekaman MIT-BIH berdurasi 30 menit, berkas `.dat`-nya sekitar 1,95 MB per rekaman. Tiga latihan 5 detik tidak memerlukannya.
3. **Ketiadaan jaringan.** Teater B belum terverifikasi punya Wi-Fi yang mampu melayani 120 peserta mengunduh serentak. Sesi 60 menit tidak boleh bergantung pada itu.
4. **Beban kognitif.** Data nyata membawa artefak gerak, *baseline wander*, dan denyut ektopik sekaligus. Itu materi Semester 4, bukan menit ke-90 hari pertama.

Setelah kodemu berjalan pada data bersih, barulah data nyata menjadi informatif: ia menunjukkan **di mana algoritmamu gagal**, dan itulah nilai sesungguhnya.

---

## 2. Katalog dataset yang aman dipakai

| Kode | Nama | Sinyal | fs | Lisensi | Anotasi denyut | Cocok untuk |
| --- | --- | --- | --- | --- | --- | --- |
| `mitdb` | MIT-BIH Arrhythmia Database | EKG 2 kanal | 360 Hz | ODC-BY 1.0 | Ya, `.atr` per denyut | Validasi deteksi R-Peak. **Pilihan utama.** |
| `ptbxl` | PTB-XL | EKG 12 lead klinis | 500 Hz (tersedia versi 100 Hz) | CC BY 4.0 | Tidak per denyut; label diagnosis SCP-ECG | Latihan multi-lead dan metadata pasien |
| `bidmc` | BIDMC PPG and Respiration | PPG, EKG, impedansi respirasi | 125 Hz | ODC-BY 1.0 | Anotasi napas manual, bukan denyut | Latihan PPG dan hubungan PPG–EKG |

Catatan penting per dataset:

- **`mitdb` adalah satu-satunya yang memberi *ground truth* per denyut.** Hanya dengan dataset ini kamu bisa menghitung sensitivitas dan presisi detektormu secara jujur. Rekaman `100` adalah titik awal konvensional karena morfologinya relatif bersih.
- **PTB-XL** hanya 10 detik per rekaman. Bagus untuk latihan Pandas dengan metadata (`ptbxl_database.csv`), lemah untuk analisis HRV karena terlalu pendek.
- **BIDMC** berisi PPG dan EKG pada subjek ICU. Penamaan rekaman WFDB-nya belum saya verifikasi langsung; jika `fetch_physionet.py` gagal untuk `bidmc`, buka halaman datasetnya dan periksa daftar berkas. Jangan asumsikan skrip selalu benar.

Dataset yang **dihindari**: seluruh keluarga MIMIC (butuh *credentialed access* + CITI + DUA) dan dataset berlisensi ODbL. Rinciannya di [ATTRIBUTION.md](../ATTRIBUTION.md) bagian 4.

---

## 3. Cara mengunduh

### Jalur A: skrip repositori (disarankan)

```bash
pip install -r requirements-physionet.txt
python data/fetch_physionet.py --db mitdb --record 100 --durasi 30
```

Hasilnya:

```
data/real/mitdb_100_250hz.csv        kolom time_s, ecg_mv — skema sama dengan data sintetis
data/real/mitdb_100_reference.csv    BPM acuan dari anotasi .atr
```

Karena skemanya identik, seluruh kode CP1–CP3 langsung jalan: cukup ganti path pada `pd.read_csv`.

### Jalur B: manual lewat peramban

Berkas WFDB dapat diunduh satu per satu. Untuk rekaman `100` MIT-BIH:

```
https://physionet.org/files/mitdb/1.0.0/100.hea    header: fs, gain, jumlah kanal
https://physionet.org/files/mitdb/1.0.0/100.dat    sinyal biner
https://physionet.org/files/mitdb/1.0.0/100.atr    anotasi denyut oleh kardiolog
```

Ketiganya harus berada dalam satu folder dengan nama dasar sama. `100.dat` tanpa `100.hea` tidak dapat dibaca: header memuat *gain*, *baseline*, dan format sampel yang menentukan cara menafsirkan bit di `.dat`.

### Jalur C: pratinjau tanpa mengunduh

PhysioNet menyediakan penampil sinyal daring (LightWAVE):

```
https://physionet.org/lightwave/?db=mitdb/1.0.0
```

Berguna untuk memilih rekaman sebelum mengunduh, dan untuk melihat bentuk anotasi denyut secara visual.

---

## 4. Tiga jebakan teknis yang pasti kamu temui

### 4.1 Frekuensi sampling berbeda

MIT-BIH memakai **360 Hz**, repositori ini memakai **250 Hz**. Jika kamu memasukkan sinyal 360 Hz ke fungsi yang berasumsi `fs = 250`, BPM-mu akan salah dengan faktor 360/250 = 1,44. Bradikardia 55 BPM akan terbaca 79 BPM. Kesalahan ini tidak memunculkan pesan error apa pun — itulah yang membuatnya berbahaya.

Dua pilihan penanganan, keduanya sah:

1. **Teruskan fs asli** sebagai argumen: `find_r_peaks(sinyal, fs=360)`. Paling jujur, tanpa distorsi.
2. **Resample ke 250 Hz** dengan `scipy.signal.resample_poly(x, 25, 36)` karena 250/360 = 25/36. `fetch_physionet.py` memakai cara ini agar seluruh berkas CSV di repo punya `fs` yang sama.

Pelajaran yang lebih besar: **`fs` adalah metadata yang wajib ikut menyertai sinyal.** Array angka tanpa `fs` tidak bermakna secara fisik.

### 4.2 Satuan amplitudo

`wfdb.rdrecord()` mengembalikan `p_signal` dalam satuan fisik (mV untuk EKG) karena telah menerapkan *gain* dan *baseline* dari header. `wfdb.rdsamp()` yang membaca nilai ADC mentah tidak. Selalu pakai `p_signal` bila kamu ingin sumbu-Y bermakna.

Dampak pada kode kita kecil, karena `normalisasi_zscore` menghapus skala. Namun grafik dengan label "mV" yang sebenarnya berisi satuan ADC adalah kesalahan pelaporan, bukan sekadar kosmetik.

### 4.3 Data nyata melanggar asumsi detektormu

Detektor kita memakai ambang persentil 98 global dan *refractory period* 0,25 s. Pada data nyata ini akan gagal pada:

- **Baseline wander** — pergeseran garis dasar akibat pernapasan membuat ambang global terlalu tinggi di satu bagian dan terlalu rendah di bagian lain.
- **Gelombang T tinggi** — pada sebagian subjek gelombang T melewati ambang dan terhitung sebagai R-Peak.
- **Denyut ektopik (PVC)** — amplitudonya bisa jauh lebih besar, menggeser persentil, sehingga denyut normal justru terlewat.
- **Artefak gerak dan elektroda lepas** — lonjakan amplitudo besar yang bukan aktivitas jantung sama sekali.

Kegagalan ini bukan bug. Inilah alasan detektor kelas klinis memakai *bandpass filter* 5–15 Hz, ambang adaptif yang diperbarui tiap denyut, dan penolakan artefak berbasis morfologi. Kode kita sengaja tidak memiliki semuanya — supaya kamu tahu mengapa mereka ada.

---

## 5. Validasi jujur: bandingkan dengan anotasi kardiolog

Inilah nilai utama MIT-BIH. Jalankan:

```bash
python exercises/cp2b_validasi_anotasi.py --record 100
```

Skrip ini menghitung tiga angka yang biasa dipakai dalam evaluasi detektor QRS:

| Metrik | Rumus | Arti |
| --- | --- | --- |
| Sensitivitas (Se) | TP / (TP + FN) | Berapa persen denyut sebenarnya yang berhasil ditemukan |
| Presisi (+P) | TP / (TP + FP) | Berapa persen deteksimu yang benar-benar denyut |
| Selisih BPM | \|BPM kamu − BPM anotasi\| | Dampak akhir kesalahan deteksi terhadap laju jantung |

Sebuah deteksi dihitung *true positive* bila berada dalam jendela toleransi ±150 ms dari anotasi denyut. Angka 150 ms bukan pilihan sembarangan: ia kira-kira sepadan dengan lebar kompleks QRS ditambah ketidakpastian penempatan penanda oleh anotator manusia.

Cara membaca hasilmu:

- **Se dan +P di atas 99% pada rekaman 100** — wajar; rekaman itu memang bersih.
- **+P jauh lebih rendah daripada Se** — detektormu terlalu longgar; ada yang terdeteksi padanya bukan denyut. Naikkan persentil.
- **Se jauh lebih rendah daripada +P** — detektormu terlalu ketat; denyut sebenarnya terlewat. Turunkan persentil.
- **Keduanya jatuh pada rekaman lain (misalnya `108`, `203`, `207`)** — itu memang rekaman sulit dengan banyak artefak dan aritmia. Melaporkan kegagalan beserta penyebabnya bernilai lebih tinggi daripada memilih rekaman termudah lalu mengklaim algoritmamu sempurna.

Jangan melaporkan satu rekaman lalu menyimpulkan kinerja umum. Uji minimal tiga rekaman dengan karakter berbeda.

---

## 6. Bonus KPP

Dapat ditambahkan pada laporan KPP (lihat `kpp/RUBRIK_PENILAIAN.md`, penambah nilai maksimum +5):

1. Jalankan detektormu pada satu rekaman MIT-BIH, laporkan Se, +P, dan selisih BPM, lalu jelaskan **satu** kasus kegagalan konkret dengan menunjukkan potongan grafiknya.
2. Bandingkan hasil `fs = 360` asli dengan hasil setelah *resample* ke 250 Hz. Jelaskan mengapa selisihnya kecil atau besar.
3. Sertakan kutipan lengkap sesuai [ATTRIBUTION.md](../ATTRIBUTION.md). Laporan yang memakai data PhysioNet tanpa atribusi tidak mendapat nilai bonus.

---

## 7. Rujukan

- MIT-BIH Arrhythmia Database: `https://physionet.org/content/mitdb/1.0.0/`
- Lisensi MIT-BIH (ODC-BY 1.0): `https://physionet.org/content/mitdb/view-license/1.0.0/`
- Direktori MIT-BIH (deskripsi tiap rekaman dan subjeknya): `https://physionet.org/physiobank/database/html/mitdbdir/mitdbdir.htm`
- PTB-XL: `https://physionet.org/content/ptb-xl/`
- BIDMC PPG and Respiration: `https://physionet.org/content/bidmc/`
- WFDB for Python: `https://physionet.org/content/wfdb-python/` dan `https://wfdb.readthedocs.io/`
- Kebijakan akses PhysioNet: `https://physionet.org/about/database/`
- Kebijakan penggunaan data ber-DUA dengan layanan daring dan LLM: `https://physionet.org/news/post/llm-responsible-use/`
