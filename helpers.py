import streamlit as st
from helpers import load_testbench_data, detect_anomalies

st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")

st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")
st.markdown("Upload `.txt`, `.mf4`, `.dat`, `.tdms`, or `.lvm` files to detect anomalies and visualize test trends.")

uploaded_file = st.file_uploader("Choose a test bench data file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    with st.spinner("Loading and analyzing data..."):
        df = load_testbench_data(uploaded_file)
        if df is not None:
            st.success("Data loaded successfully!")
            st.dataframe(df.head(100))

            st.markdown("### 📌 Anomaly Detection")
            anomalies = detect_anomalies(df)
            st.write(anomalies)
        else:
            st.error("Failed to load the file. Please ensure it's a supported format.")
