import streamlit as st
from data_loader import load_testbench_data
from data_cleaning import clean_data
from anomaly_detection import detect_anomalies

st.set_page_config(page_title="TrendForge – Analyzer", layout="wide")
st.title("📊 TrendForge – AI-Powered Test Bench Analyzer")

uploaded_file = st.file_uploader("Upload test bench file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    metadata, df = load_testbench_data(uploaded_file)

    if df is not None and not df.empty:
        st.success("✅ Measurement data loaded successfully!")

        # Show metadata
        if metadata:
            st.markdown("### 🧾 Metadata")
            st.code(metadata, language="text")

        st.markdown("### 🗂️ Measurement Data Preview")
        st.dataframe(df.head(10))

        # Data Cleaning
        if df.isnull().sum().sum() > 0:
            st.markdown("### 🧹 Data Cleaning")
            method = st.radio("Missing values found. Choose a cleaning method:", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
            df = clean_data(df, method)
            st.success("✅ Cleaned missing values.")
            st.dataframe(df.head(10))
        else:
            st.info("No missing values detected.")

        # Anomaly Detection
        st.markdown("### 🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.write(anomalies)
    else:
        st.error("❌ Could not load measurement data.")
