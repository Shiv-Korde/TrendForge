import streamlit as st
from helpers import load_testbench_data, detect_anomalies
import pandas as pd

st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")

st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")
st.markdown("Upload `.txt`, `.mf4`, `.dat`, `.tdms`, or `.lvm` files to detect anomalies and visualize test trends.")

uploaded_file = st.file_uploader("Choose a test bench data file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    with st.spinner("Loading and analyzing data..."):
        df = load_testbench_data(uploaded_file)

        if df is not None and not df.empty:
            st.success("✅ Data loaded successfully!")

            st.markdown("### 🗂️ Data Preview")
            st.dataframe(df.head(10))

            # ➕ Data Cleaning Section
            st.markdown("### 🧹 Data Cleaning")
            if df.isnull().sum().sum() > 0:
                st.warning(f"Found {df.isnull().sum().sum()} missing values in the dataset.")
                cleaning_method = st.radio("Choose how to handle missing values:", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])

                if cleaning_method == "Drop Rows":
                    df = df.dropna()
                elif cleaning_method == "Fill with 0":
                    df = df.fillna(0)
                elif cleaning_method == "Forward Fill":
                    df = df.ffill()
                elif cleaning_method == "Backward Fill":
                    df = df.bfill()

                st.success("✅ Missing values handled.")
                st.dataframe(df.head(10))
            else:
                st.info("✅ No missing values found.")

            # ➕ Anomaly Detection Section
            st.markdown("### 🚨 Anomaly Detection")
            anomalies = detect_anomalies(df)
            st.write(anomalies)
        else:
            st.error("❌ Failed to load the file. Please ensure it's a supported format and not empty.")
