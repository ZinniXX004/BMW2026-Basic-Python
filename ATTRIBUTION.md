# Atribusi dan Lisensi Data

Berkas ini wajib dibaca sebelum memakai dataset nyata dari PhysioNet, dan wajib disertakan dalam laporan apa pun yang memakai data tersebut.

## 1. Data yang dibundel dalam repositori ini

Seluruh berkas di `data/` yang dihasilkan `data/make_dataset.py` adalah **sinyal sintetis** yang dibangkitkan secara numerik dengan seed tetap. Tidak ada rekaman pasien, tidak ada data pihak ketiga, tidak ada persoalan privasi maupun lisensi. Berkas-berkas itu boleh disalin dan diubah tanpa syarat.

## 2. Data nyata PhysioNet

Ada dua jalur berbeda, dengan kebijakan bundling yang berbeda pula:

- **`data/fetch_physionet.py`** (opsional, bahan eksplorasi/KPP) mengunduh langsung dari server PhysioNet ke folder lokal `data/real/` yang diabaikan Git — **tidak dibundel**. Alasannya bukan lisensi, melainkan agar setiap peserta melewati langkah provenance secara sadar: tahu dari mana data berasal, siapa yang berhak dikutip, dan lisensi apa yang mengikat.
- **`data/demo/`** (live demo pemateri) berisi turunan 30 detik dari MIT-BIH record 100 yang **sengaja dibundel dan di-commit** ke repositori ini — supaya demo panggung tidak bergantung pada internet saat presentasi. Ini pengecualian yang disengaja terhadap prinsip "tidak menyimpan berkas PhysioNet" di atas, dan diizinkan penuh oleh lisensi ODC-BY 1.0 (redistribusi turunan dengan atribusi).

Kedua jalur sama-sama tunduk pada kewajiban atribusi di bawah ini.

### Kewajiban atribusi

Jika laporan atau kode kamu memakai data di bawah ini, sertakan kutipan berikut.

**MIT-BIH Arrhythmia Database** — lisensi *Open Data Commons Attribution License v1.0* (ODC-BY 1.0), akses terbuka.

> Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database. IEEE Engineering in Medicine and Biology 20(3):45-50 (May-June 2001). PMID: 11446209.

**PTB-XL** — lisensi *Creative Commons Attribution 4.0 International* (CC BY 4.0), akses terbuka.

> Wagner P, Strodthoff N, Bousseljot RD, Kreiseler D, Lunze FI, Samek W, Schaeffter T. PTB-XL, a large publicly available electrocardiography dataset. Scientific Data 7:154 (2020).

**BIDMC PPG and Respiration Dataset** — lisensi *Open Data Commons Attribution License v1.0* (ODC-BY 1.0), akses terbuka.

> Pimentel MAF, Johnson AEW, Charlton PH, Birrenkott D, Watkinson PJ, Tarassenko L, Clifton DA. Toward a robust estimation of respiratory rate from pulse oximeters. IEEE Transactions on Biomedical Engineering 64(8):1914-1923 (2017).

### Kutipan platform (selalu sertakan)

> Goldberger A, Amaral L, Glass L, Hausdorff J, Ivanov PC, Mark R, Mietus JE, Moody GB, Peng CK, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation 101(23):e215-e220 (2000). RRID:SCR_007345.

## 3. Perangkat lunak

Paket `wfdb` (WFDB for Python, MIT-LCP) dipakai untuk membaca format WFDB. Lisensi paket mengikuti repositori aslinya di `github.com/MIT-LCP/wfdb-python`.

## 4. Yang TIDAK boleh dipakai di BMW

| Dataset | Kebijakan akses | Alasan dilarang di sini |
| --- | --- | --- |
| MIMIC-III, MIMIC-IV, MIMIC-CXR, dan turunannya | *Credentialed access* | Butuh pelatihan CITI, persetujuan individual, dan penandatanganan Data Use Agreement. DUA melarang berbagi akses ke pihak ketiga, termasuk mengirim data melalui API layanan daring atau model bahasa besar. Tidak dapat dipakai untuk kegiatan kelas. |
| Dataset berlisensi *Open Database License* (ODbL), misalnya Pulse Transit Time PPG Dataset | Terbuka, tetapi ODbL | ODbL memuat kewajiban bertipe *share-alike* pada basis data turunan. Konsekuensinya terhadap tugas mahasiswa tidak sepele, jadi hindari kecuali kamu benar-benar memahaminya. |

Kesimpulan praktis: untuk BMW, pakai dataset berlisensi **ODC-BY** atau **CC BY** saja.
