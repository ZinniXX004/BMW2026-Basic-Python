# Rubrik Penilaian KPP — Materi I (Python)

Total 100 poin. Penilai: pemateri dan asisten Materi I.

| Komponen | Poin | Kriteria penuh | Kriteria sebagian | Nol |
| --- | --- | --- | --- | --- |
| Kode berjalan | 25 | `exercises/cp2_rpeak_bpm.py` berjalan tanpa error dan menghasilkan puncak | Berjalan dengan peringatan atau perlu perbaikan kecil (maks 15) | Error saat dijalankan |
| Akurasi BPM | 25 | Selisih terhadap `reference_bpm.csv` ≤ 5 BPM | Selisih 5–10 BPM (maks 15) | Selisih > 10 BPM atau NaN |
| SDNN (ms) | 15 | Nilai benar, satuan ms, dua desimal, disertai pembacaan wajar | Nilai benar tetapi satuan atau pembacaan salah (maks 8) | Tidak dilaporkan |
| Dashboard | 15 | CP3-a dan CP3-b terisi; tangkapan layar memperlihatkan 4 metrik dan grafik | Hanya satu TODO terisi, atau tangkapan layar tidak lengkap (maks 8) | Tidak ada tangkapan layar |
| Kualitas kode | 10 | Nama variabel jelas, ada komentar pada bagian non-obvious, tanpa kode mati | Dapat dibaca tetapi berantakan (maks 5) | Tidak dapat dibaca atau hasil salin |
| Refleksi | 10 | 150–250 kata, spesifik, menyebut kesulitan nyata dan konsep yang dipahami | Terlalu umum atau di luar rentang kata (maks 5) | Tidak ada |

## Penambah nilai (maks +5, tidak melebihi 100)

- Membandingkan hasil manual dengan `scipy.signal.find_peaks` dan menjelaskan sumber perbedaannya: **+3**
- Menambahkan penanganan kasus tepi (sinyal terlalu pendek, puncak < 2, elektroda lepas): **+2**

## Pengurang nilai

- Terlambat kurang dari 24 jam: **−10**
- Terlambat lebih dari 24 jam: tidak dinilai, kecuali ada izin tertulis panitia
- Angka hasil analisis tidak sesuai dengan berkas dataset yang ditetapkan untuk NRP tersebut: **−25**
- Indikasi penyalinan kode atau laporan: nilai 0 untuk komponen terkait dan dilaporkan ke Kadep Ilprof

## Catatan untuk penilai

1. Periksa akurasi BPM dengan menjalankan `solutions/signal_utils_solution.py` pada berkas peserta, bukan dengan memercayai angka di laporan.
2. Toleransi KPP adalah ±5 BPM, lebih longgar daripada ±3 BPM saat sesi, karena peserta bekerja tanpa pendampingan.
3. Penalaran fisiologis yang benar dengan angka yang sedikit meleset lebih bernilai daripada angka tepat tanpa penjelasan. Berikan komentar tertulis, bukan hanya angka.
