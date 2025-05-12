import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import detect_anomalies, load_testbench_data
import json
import os

CONFIG_FILE = "config.json"

st.set_page_config(layout="wide")
st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")

uploaded_file = st.file_uploader("Upload Test Bench File (.txt)", type=["txt"])

if uploaded_file:
    df = load_testbench_data(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows.")
    signals = df.columns[1:]

    with st.sidebar:
        st.header("🛠️ Visualization Config")
        signal_choice = st.selectbox("Choose signal to plot", signals)
        show_anomalies = st.checkbox("Highlight anomalies", value=True)
        save_cfg = st.button("💾 Save Config")
        load_cfg = st.button("🔁 Load Config")

    if save_cfg:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"signal": signal_choice}, f)
        st.sidebar.success("Config saved.")

    if load_cfg and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            signal_choice = cfg["signal"]
        st.sidebar.success("Config loaded.")

    st.subheader(f"📈 Signal: {signal_choice}")
    plot_df = df[["timestamp", signal_choice]].copy()

    if show_anomalies:
        anoms = detect_anomalies(plot_df, signal_choice)
        fig = px.line(plot_df, x="timestamp", y=signal_choice, title="Signal Plot with Anomalies")
        fig.add_scatter(x=anoms["timestamp"], y=anoms[signal_choice], mode="markers", name="Anomalies", marker=dict(color="red", size=10))
    else:
        fig = px.line(plot_df, x="timestamp", y=signal_choice, title="Signal Plot")

    st.plotly_chart(fig, use_container_width=True)