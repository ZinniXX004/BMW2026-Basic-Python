# data/

Folder ini **kosong secara sengaja** sampai kamu menjalankan generator dataset:

```bash
python data/make_dataset.py
```

## Mengapa dibangkitkan, bukan disimpan?

1. **Bebas lisensi dan privasi.** Sinyal disintesis secara numerik; tidak ada rekaman pasien nyata dan tidak ada dataset pihak ketiga yang perlu diredistribusi.
2. **Deterministik.** Seed tetap, sehingga semua peserta memperoleh sinyal yang identik dan nilai BPM acuan yang sama.
3. **Nilai acuan diketahui pasti.** BPM acuan berasal dari waktu denyut yang dipakai saat sintesis, bukan dari hasil deteksi. Ini membuat penilaian objektif.
4. **Tidak ada unduhan pada hari-H.** Wi-Fi ruangan tidak dijamin untuk 120 peserta.

## Berkas yang dihasilkan

| Berkas | Kolom | Keterangan |
| --- | --- | --- |
| `ecg_sample.csv` | `time_s`, `ecg_mv` | EKG 10 s, fs = 250 Hz, target sekitar 72 BPM. Dipakai pada CP1 dan CP2. |
| `ppg_sample.csv` | `time_s`, `ppg_au` | PPG 10 s, fs = 250 Hz, target sekitar 88 BPM. Dipakai pada pembahasan S4. |
| `kpp/subject_XX.csv` | `time_s`, `ecg_mv` | Enam berkas EKG dengan laju berbeda (52 sampai 108 BPM) untuk tugas KPP. |
| `reference_bpm.csv` | `file`, `jenis`, `fs_hz`, `bpm_acuan` | Nilai acuan untuk memeriksa hasil hitunganmu. |

## Cara memilih berkas KPP

Ambil dua digit terakhir NRP, lalu hitung sisa bagi terhadap 6:

```
indeks = (dua digit terakhir NRP) mod 6
```

Contoh: NRP 5023241017 → 17 mod 6 = 5 → gunakan `data/kpp/subject_05.csv`.

## Batasan yang harus kamu sadari

Sinyal sintetis ini bersih dibandingkan rekaman klinis nyata: tidak ada artefak gerak besar, tidak ada interferensi jala-jala 50 Hz yang berat, tidak ada aritmia, dan tidak ada elektroda lepas. Algoritma yang bekerja sempurna di sini **belum tentu** bekerja pada data nyata. Itu justru materi mata kuliah Pengolahan Sinyal Biomedika di semester 4.
