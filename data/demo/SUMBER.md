# Sumber data demo

Berkas `mitdb_100_250hz.csv` adalah **turunan** dari:

MIT-BIH Arrhythmia Database v1.0.0, record 100, kanal MLII, 30 detik pertama,
diturunkan laju cupliknya dari 360 Hz ke 250 Hz.

- Sumber: https://physionet.org/content/mitdb/1.0.0/
- Lisensi: Open Data Commons Attribution License v1.0 (ODC-BY 1.0)
- Kutipan wajib: lihat `ATTRIBUTION.md` di akar repositori.

Berkas `mitdb_100_250hz_acuan.csv` berisi laju jantung acuan yang dihitung dari
anotasi denyut `.atr` (anotasi kardiolog), bukan dari algoritma kita sendiri.
