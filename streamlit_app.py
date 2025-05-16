import streamlit as st
from data_loader import load_testbench_data
from ui_data_cleaning import render_data_cleaning_ui
from anomaly_detection import detect_anomalies

# Set page configuration
st.set_page_config(page_title="TrendForge – Analyzer", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("🧭 TrendForge Navigation")
    section = st.radio("Go to section:", ["Data Loading", "Data Cleaning", "Visualization", "Insight"])

# Section: Data Loading
if section == "Data Loading":
    st.title("📂 Data Loading")
    uploaded_file = st.file_uploader("Upload test bench file", type=["txt", "mf4", "dat", "tdms", "lvm"])

    if uploaded_file:
        metadata, df = load_testbench_data(uploaded_file)
        if df is not None and not df.empty:
            st.session_state["df"] = df
            st.session_state["metadata"] = metadata
            st.session_state["file_name"] = uploaded_file.name
            st.success(f"✅ File '{uploaded_file.name}' loaded.")
        else:
            st.error("❌ Could not load valid measurement data.")

    if "df" in st.session_state:
        st.markdown("### 🧾 Metadata")
        st.code(st.session_state.get("metadata", "No metadata found."), language="text")

        st.markdown("### 🗂️ Data Preview")
        st.dataframe(st.session_state["df"].head(10))

# Section: Data Cleaning
elif section == "Data Cleaning":
    st.title("🧹 Data Cleaning")
    render_data_cleaning_ui()  # Sidebar options are handled inside this module

# Section: Visualization
elif section == "Visualization":
    st.title("📈 Data Visualization")
    if "df" in st.session_state:
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include='number').columns
        if not numeric_cols.empty:
            col = st.selectbox("Select column to plot", numeric_cols)
            st.line_chart(df[col])
        else:
            st.warning("No numeric columns found.")
    else:
        st.warning("Load data first in 'Data Loading' section.")

# Section: Insight
elif section == "Insight":
    st.title("🔍 Data Insights")
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.subheader("🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.write(anomalies)
    else:
        st.warning("Load data first in 'Data Loading' section.")
