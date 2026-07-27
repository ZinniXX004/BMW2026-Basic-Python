# Dataset nyata dari PhysioNet

Panduan ini opsional bagi peserta dan **wajib** bagi pemateri, karena live demo
pada presentasi memakai MIT-BIH.

## 1. Mengapa sesi memakai data sintetis lebih dulu

Keputusan ini bukan soal lisensi. MIT-BIH justru berlisensi ODC-BY 1.0 yang
mengizinkan redistribusi turunan dengan atribusi. Alasannya rekayasa:

1. **Determinisme.** Data sintetis punya BPM acuan yang diketahui persis dari
   proses sintesisnya, sehingga checkpoint dapat dinilai otomatis.
2. **Tanpa jaringan.** Wi-Fi Teater B belum terverifikasi. 120 peserta yang
   mengunduh serentak adalah titik kegagalan tunggal.
3. **Ukuran.** Satu rekaman MIT-BIH utuh berukuran sekitar 1,95 MB per berkas
   sinyal.
4. **Beban kognitif.** Artefak data nyata muncul di menit ke-90 sesi, ketika
   peserta belum punya alat untuk menanganinya.

Setelah kode peserta berjalan pada data sintetis, data nyata menjadi bahan ajar
terbaik justru karena **detektor sederhana akan gagal di sana**.

## 2. Katalog dataset yang lisensinya sudah diverifikasi

| Dataset | Akses | Lisensi | Spesifikasi | Catatan |
| --- | --- | --- | --- | --- |
| MIT-BIH Arrhythmia (`mitdb`) | Terbuka | ODC-BY 1.0 | 48 rekaman 30 menit, 47 pasien, 360 Hz, anotasi `.atr` per denyut | Satu-satunya di sini yang punya *ground truth* per denyut. Dipakai untuk live demo |
| PTB-XL | Terbuka | CC BY 4.0 | 21.799 EKG 12-lead, 10 detik per rekaman, 500 Hz dan 100 Hz | Terlalu pendek untuk HRV |
| BIDMC PPG and Respiration | Terbuka | ODC-BY 1.0 | 53 rekaman ICU 8 menit, PPG + EKG + respirasi, 125 Hz | Paling cocok untuk PPG. Penamaan rekaman WFDB-nya **belum diverifikasi** |
| Pulse Transit Time PPG | Terbuka | **ODbL 1.0** | — | **Hindari.** Ada kewajiban bertipe *share-alike* pada basis data turunan |
| Keluarga MIMIC | *Credentialed* | Credentialed Health Data Use Agreement | — | **Dilarang untuk BMW.** DUA melarang berbagi akses ke pihak lain, dan FAQ PhysioNet menyatakan berbagi data dalam tim atau kelas tidak diizinkan |

Aturan praktis untuk BMW: pakai hanya dataset berlisensi **ODC-BY** atau
**CC BY**, dan selalu kutip sesuai `ATTRIBUTION.md`.

## 3. Tiga cara mengambil data

### a. Lewat skrip repositori ini

```bash
pip install -r requirements-physionet.txt
python data/fetch_physionet.py --daftar
python data/fetch_physionet.py --db mitdb --record 100 --durasi 60
```

Hasilnya `data/real/mitdb_100_250hz.csv` berskema sama dengan data sintetis
(`time_s`, `ecg_mv`), sehingga kodemu tidak perlu diubah sama sekali. Folder
`data/real/` sengaja masuk `.gitignore`.

### b. Manual

Unduh **ketiganya**, bukan hanya `.dat`:

- `https://physionet.org/files/mitdb/1.0.0/100.hea` — header: fs, gain, baseline
- `https://physionet.org/files/mitdb/1.0.0/100.dat` — sinyal
- `https://physionet.org/files/mitdb/1.0.0/100.atr` — anotasi denyut

Berkas `.dat` tanpa `.hea` **tidak dapat ditafsirkan**; angka di dalamnya nilai
ADC mentah tanpa satuan.

### c. Lewat peramban, tanpa memasang apa pun

`https://physionet.org/lightwave/?db=mitdb/1.0.0` — berguna untuk melihat bentuk
sinyal dan anotasi sebelum menulis kode.

## 4. Data live demo untuk presentasi

Demo panggung tidak boleh bergantung pada jaringan. Karena itu ada jalur
terpisah yang mengekspor sekali di rumah, lalu di-commit:

```bash
pip install -r requirements-physionet.txt
python demo/live_demo_mitbih.py --siapkan   # butuh internet, sekali saja
git add data/demo && git commit -m "Tambah data demo MIT-BIH"
python demo/live_demo_mitbih.py            # mode panggung, tanpa internet
```

Mode panggung hanya membaca CSV yang sudah di-commit dan **tidak** mengimpor
`wfdb`. Bila berkasnya hilang, skrip beralih ke data sintetis dengan peringatan
besar, sehingga demo tidak pernah mati di depan 120 peserta.

## 5. Tiga jebakan teknis yang pasti kamu temui

### a. Frekuensi cuplik: MIT-BIH 360 Hz, dataset kita 250 Hz

Ini kegagalan paling berbahaya karena **senyap**. Tidak ada exception, hanya
angka yang salah secara sistematis.

BPM dihitung dari `RR = selisih_indeks / fs`. Bila sinyal 360 Hz diproses dengan
`fs = 250`, setiap interval RR dihitung **lebih panjang** daripada seharusnya,
sehingga BPM terbaca **lebih rendah** dengan faktor 250/360 = **0,694**:

| BPM sebenarnya (fs 360 Hz) | Terbaca bila fs diasumsikan 250 Hz | Akibat tafsir |
| --- | --- | --- |
| 52,0 | 36,1 | bradikardia ringan tampak sangat berat |
| 72,0 | 50,0 | **normal tampak bradikardia** |
| 108,0 | 75,0 | takikardia tampak normal |

Arah sebaliknya juga berlaku: sinyal 250 Hz yang diproses dengan `fs = 360` akan
terbaca 1,44 kali lebih tinggi. Angka-angka di tabel ini hasil pengukuran, bukan
perkiraan.

Aturannya: **jangan pernah menuliskan `fs` sebagai konstanta untuk data
PhysioNet.** Baca `record.fs`, atau turunkan laju cupliknya lebih dahulu:

```python
from scipy.signal import resample_poly
turun = resample_poly(sinyal_360hz, 25, 36)   # 250/360 = 25/36
```

### b. Satuan amplitudo

`record.p_signal` sudah dalam satuan fisik (mV) karena `gain` dan `baseline` dari
`.hea` telah diterapkan. Nilai ADC mentah belum. Salah memilih di antara
keduanya membuat ambang berbasis persentil masih bekerja tetapi setiap angka
amplitudo tidak bermakna.

### c. Asumsi detektor yang dilanggar data nyata

Detektor kita mengasumsikan puncak R adalah nilai tertinggi dan garis dasar
stabil. Rekaman manusia melanggar keduanya:

- **Baseline wander** karena pernapasan dan gerakan elektroda menggeser garis dasar.
- **Gelombang T tinggi** pada beberapa subjek melewati ambang dan terhitung ganda.
- **Denyut ektopik** (PVC) beramplitudo jauh lebih besar sehingga menaikkan
  persentil dan menekan denyut normal ke bawah ambang.
- **Artefak gerakan** menghasilkan lonjakan yang lebih tinggi daripada QRS.

Ini bukan bug pada kodemu. Inilah justifikasi konkret mengapa detektor klinis
memakai bandpass 5-15 Hz, ambang adaptif per denyut, dan penolakan artefak.

## 6. Validasi yang jujur, bukan sekadar "tidak error"

Catatan penting: sinyal sintetis repositori ini pun sudah membuktikan bahwa
"tidak error" bukan bukti kebenaran. Ambang persentil 98 pada `ppg_sample.csv`
menghasilkan 67,60 BPM padahal acuannya 87,92 -- salah 20,32 BPM tanpa satu pun
pesan kesalahan. Karena itu setiap detektor wajib diukur terhadap acuan.

Untuk data nyata, acuannya adalah anotasi kardiolog:

```bash
python exercises/cp2b_validasi_anotasi.py --record 100 --durasi 60
```

Skrip itu mencocokkan puncak hasil deteksimu dengan anotasi `.atr` satu-ke-satu
dalam jendela toleransi **±150 ms**, lalu melaporkan:

- **Sensitivitas (Se)** = TP / (TP + FN), berapa persen denyut sebenarnya yang tertangkap.
- **Presisi (+P)** = TP / (TP + FP), berapa persen deteksi yang benar-benar denyut.
- **Selisih BPM** terhadap laju dari anotasi.

Cara membaca hasilnya:

| Pola | Arti | Tindakan |
| --- | --- | --- |
| Se tinggi, +P rendah | ambang terlalu longgar, gelombang T ikut terhitung | naikkan persentil atau perpanjang refractory |
| Se rendah, +P tinggi | ambang terlalu ketat, denyut beramplitudo rendah hilang | turunkan persentil |
| Keduanya rendah | asumsi dasar gagal, bukan soal parameter | tambahkan bandpass dan koreksi baseline |

BPM yang tepat dengan Se dan +P yang buruk berarti kesalahan yang saling
menghapus. Itu kebetulan, bukan detektor yang benar.

## 7. Bonus KPP

Eksperimen dengan data PhysioNet dapat diajukan sebagai penambah nilai maksimum
+5, misalnya: melaporkan Se dan +P pada dua rekaman berkarakter berbeda
(`100` normal versus `208` banyak PVC), atau menunjukkan pengaruh resampling
360 -> 250 Hz terhadap hasil deteksi.

## 8. Rujukan

- MIT-BIH Arrhythmia Database: `https://physionet.org/content/mitdb/1.0.0/`
- Lisensi ODC-BY 1.0: `https://physionet.org/content/mitdb/view-license/1.0.0/`
- Paket `wfdb` untuk Python: `https://physionet.org/content/wfdb-python/`
- Kode simbol anotasi: `https://www.physionet.org/physiobank/annotations.shtml`
- Teks kutipan wajib: `ATTRIBUTION.md`
