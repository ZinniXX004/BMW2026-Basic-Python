"""CP3 (15 menit) - dashboard Streamlit + Plotly untuk analisis EKG.

Jalankan dari folder akar repositori:

    streamlit run src/app_dashboard.py

Jika port 8501 terpakai:

    streamlit run src/app_dashboard.py --server.port 8502

Dua bagian bertanda TODO wajib kamu isi. Sisanya sudah disiapkan agar sesi
60 menit tidak habis untuk menulis kode antarmuka.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.signal_utils import (
    find_r_peaks,
    hitung_bpm,
    hitung_sdnn_ms,
    klasifikasi_hr,
)

FS = 250

st.set_page_config(page_title="BMW 2026 - Analisis EKG", layout="wide")
st.title("Dashboard Analisis EKG")
st.caption(
    "BMW Basic 2026, Materi I. Alat pembelajaran rekayasa, bukan perangkat "
    "diagnostik. Jangan dipakai untuk keputusan medis."
)

with st.sidebar:
    st.header("Parameter")
    berkas = st.selectbox(
        "Berkas sinyal",
        options=["data/ecg_sample.csv"] + sorted(
            str(path) for path in pathlib.Path("data/kpp").glob("*.csv")
        ),
    )
    persentil = st.slider("Persentil ambang", 90.0, 99.5, 98.0, 0.5)
    refractory = st.slider("Refractory period (s)", 0.15, 0.40, 0.25, 0.01)
    st.markdown(
        "Turunkan persentil untuk melihat bagaimana derau mulai terdeteksi "
        "sebagai puncak. Perkecil refractory period untuk melihat satu QRS "
        "terhitung ganda."
    )

frame = pd.read_csv(berkas)
ekg = frame["ecg_mv"].to_numpy()
waktu = frame["time_s"].to_numpy()

puncak = find_r_peaks(ekg, FS, persentil=persentil, refractory_s=refractory)
bpm = hitung_bpm(puncak, FS)
sdnn = hitung_sdnn_ms(puncak, FS)

kolom = st.columns(4)
kolom[0].metric("Jumlah R-Peak", f"{puncak.size}")
kolom[1].metric("BPM", "n/a" if np.isnan(bpm) else f"{bpm:.1f}")
# TODO (CP3-a): tampilkan SDNN dalam milidetik pada kolom[2] memakai st.metric.
# TODO (CP3-b): tampilkan hasil klasifikasi_hr(bpm) pada kolom[3].

figur = go.Figure()
figur.add_trace(
    go.Scatter(x=waktu, y=ekg, mode="lines", name="EKG", line=dict(width=1.2))
)
if puncak.size:
    figur.add_trace(
        go.Scatter(
            x=waktu[puncak],
            y=ekg[puncak],
            mode="markers",
            name="R-Peak",
            marker=dict(size=9, symbol="circle-open"),
        )
    )
figur.update_layout(
    height=420,
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis_title="Waktu (s)",
    yaxis_title="Amplitudo (mV)",
    title=f"Sinyal dan puncak terdeteksi (fs = {FS} Hz)",
)
st.plotly_chart(figur, use_container_width=True)

if puncak.size >= 2:
    rr_ms = np.diff(puncak) / FS * 1000.0
    st.subheader("Interval RR")
    st.bar_chart(pd.DataFrame({"RR (ms)": rr_ms}))
    st.caption(
        "Interval RR yang sangat pendek biasanya menandakan puncak ganda, "
        "bukan aritmia. Periksa refractory period sebelum menafsirkan."
    )
else:
    st.warning("Puncak belum cukup untuk menghitung interval RR.")
