# KPP — Kertas Pengembangan Peserta (Materi I: Python)

**Batas pengumpulan:** 7 hari setelah hari-1 (H+7 dari 22 Agustus 2026), pukul 23.59 WIB.
**Bobot:** individu. **Total nilai:** 100 poin.

## Tujuan

Memastikan pipeline yang dilatih pada sesi simulasi benar-benar dapat kamu jalankan sendiri, di luar ruangan, tanpa asisten di samping.

## Dataset milikmu

Setiap peserta memakai berkas yang berbeda. Tentukan berkas dengan NRP-mu:

```
indeks = (dua digit terakhir NRP) mod 6
berkas = data/kpp/subject_{indeks:02d}.csv
```

Contoh: NRP 5023241017 → 17 mod 6 = 5 → `data/kpp/subject_05.csv`.

Bangkitkan dataset lebih dulu bila belum ada:

```bash
python data/make_dataset.py
```

## Yang harus dikerjakan

1. **Lengkapi `src/signal_utils.py`** — semua TODO pada `find_r_peaks` dan `hitung_bpm` harus terisi dan berjalan tanpa error.
2. **Analisis berkas milikmu** — laporkan:
   - jumlah R-Peak yang terdeteksi;
   - BPM rata-rata (dua angka desimal);
   - SDNN dalam milidetik (dua angka desimal);
   - label `klasifikasi_hr` beserta catatan mengapa label itu belum tentu bermakna klinis.
3. **Lengkapi dashboard** — isi TODO CP3-a dan CP3-b pada `src/app_dashboard.py`, jalankan, lalu ambil tangkapan layar yang memperlihatkan keempat metrik dan grafik Plotly.
4. **Eksperimen parameter** — turunkan *refractory period* ke 0,15 s dan catat perubahan BPM. Jelaskan penyebabnya secara fisiologis, bukan hanya secara numerik.
5. **Refleksi 150–250 kata** — satu kesulitan teknis yang kamu alami, cara kamu menyelesaikannya, dan satu konsep sinyal biomedis yang baru kamu pahami.

## Format pengumpulan

Satu berkas PDF bernama `KPP_MateriI_<NRP>_<Nama>.pdf`, berisi:

1. Identitas: nama, NRP, angkatan, berkas dataset yang dipakai.
2. Tabel hasil analisis (poin 2).
3. Tangkapan layar dashboard (poin 3).
4. Tabel eksperimen parameter dan penjelasannya (poin 4).
5. Refleksi (poin 5).
6. Lampiran: potongan kode `find_r_peaks` dan `hitung_bpm` milikmu.

Unggah ke tautan pengumpulan yang dibagikan panitia Ilprof.

## Aturan integritas

- Dataset berbeda per peserta, sehingga angka hasil analisis juga berbeda. Angka yang identik antar peserta dengan berkas berbeda akan ditinjau.
- Berdiskusi diperbolehkan; menyalin kode dan laporan tidak. Tulis kodemu sendiri.
- Menggunakan `scipy.signal.find_peaks` diperbolehkan **sebagai pembanding**, tetapi implementasi manual tetap wajib ada dan dijelaskan.
- Jika ada bagian yang tidak selesai, tulis apa adanya beserta pesan error yang kamu dapat. Laporan jujur yang belum selesai bernilai lebih tinggi daripada hasil yang dibuat-buat.
