import streamlit as st
from data_loader import load_testbench_data
from data_cleaning import clean_data
from anomaly_detection import detect_anomalies

st.set_page_config(page_title="TrendForge – Analyzer", layout="wide")

st.title("📊 TrendForge – Test Bench Data Analyzer")

uploaded_file = st.file_uploader("Upload test bench file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    df = load_testbench_data(uploaded_file)

    if df is not None and not df.empty:
        st.success("✅ Data loaded successfully!")
        st.dataframe(df.head(10))

        # 🧹 Data Cleaning
        st.markdown("### 🧹 Data Cleaning")
        if df.isnull().sum().sum() > 0:
            st.warning(f"Missing values: {df.isnull().sum().sum()}")
            method = st.radio("Choose cleaning method", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
            df = clean_data(df, method)
            st.success("Missing values cleaned.")
            st.dataframe(df.head(10))
        else:
            st.info("No missing values detected.")

        # 🚨 Anomaly Detection
        st.markdown("### 🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.write(anomalies)
    else:
        st.error("❌ Failed to load or parse the file.")
