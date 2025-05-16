import streamlit as st
from data_loader import load_testbench_data
from data_cleaning import clean_data
from anomaly_detection import detect_anomalies

st.set_page_config(page_title="TrendForge – Analyzer", layout="wide")
st.title("📊 TrendForge – AI-Powered Test Bench Analyzer")

# Navigation Bar
section = st.radio(
    "🔍 Navigate",
    ["Data Loading", "Data Cleaning", "Visualization", "Insight"],
    horizontal=True
)

if section == "Data Loading":
    uploaded_file = st.file_uploader("Upload test bench file", type=["txt", "mf4", "dat", "tdms", "lvm"])

    if uploaded_file is not None:
        metadata, df = load_testbench_data(uploaded_file)
        if df is not None and not df.empty:
            st.session_state["metadata"] = metadata
            st.session_state["df"] = df
            st.session_state["file_name"] = uploaded_file.name
            st.success(f"✅ File '{uploaded_file.name}' loaded successfully.")
        else:
            st.error("❌ Could not load measurement data.")
    elif "df" in st.session_state:
        st.info(f"Showing previously loaded file: {st.session_state.get('file_name', 'unknown')}")
    else:
        st.warning("No file uploaded yet.")

    # Show metadata and data if available
    if "df" in st.session_state:
        if "metadata" in st.session_state:
            st.markdown("### 🧾 Metadata")
            st.code(st.session_state["metadata"], language="text")

        st.markdown("### 🗂️ Measurement Data Preview")
        st.dataframe(st.session_state["df"].head(10))

elif section == "Data Cleaning":
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.markdown("### 🧹 Data Cleaning")
        mode = st.radio("Select cleaning mode:", ["Manual", "Automatic"])

        if mode == "Manual":
            with st.expander("🔧 Column-wise Cleaning"):
                column = st.selectbox("Select column", df.columns)
                method = st.selectbox("Cleaning method", ["Fill with 0", "Forward Fill", "Backward Fill", "Drop Nulls"])
                if st.button("Apply to Selected Column"):
                    df = clean_data(df, method, column)
                    st.session_state["df"] = df
                    st.success(f"Applied '{method}' to '{column}'")

            with st.expander("🧹 Global Cleaning Options"):
                global_method = st.selectbox("Apply to entire dataset", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
                if st.button("Apply Global Cleaning"):
                    df = clean_data(df, global_method)
                    st.session_state["df"] = df
                    st.success(f"Applied global cleaning: {global_method}")

        elif mode == "Automatic":
            if st.button("✨ Run AI-Based Auto Cleaning"):
                df = auto_clean(df)
                st.session_state["df"] = df
                st.success("AI-based automatic cleaning completed!")

        st.markdown("### 🔍 Cleaned Data Preview")
        st.dataframe(df.head(10))
    else:
        st.warning("Please upload and load data first in 'Data Loading' tab.")

elif section == "Visualization":
    if "df" in st.session_state:
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            selected = st.selectbox("Select column to plot", numeric_cols)
            st.line_chart(df[selected])
        else:
            st.warning("No numeric columns found.")
    else:
        st.warning("Please upload and load data first.")

elif section == "Insight":
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.markdown("### 🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.write(anomalies)
    else:
        st.warning("Please upload and load data first.")


# uploaded_file = st.file_uploader("Upload test bench file", type=["txt", "mf4", "dat", "tdms", "lvm"])

# if uploaded_file:
#     metadata, df = load_testbench_data(uploaded_file)

#     if df is not None and not df.empty:
#         st.success("✅ Measurement data loaded successfully!")

#         # Show metadata
#         if metadata:
#             st.markdown("### 🧾 Metadata")
#             st.code(metadata, language="text")

#         st.markdown("### 🗂️ Measurement Data Preview")
#         st.dataframe(df.head(10))

#         # Data Cleaning
#         if df.isnull().sum().sum() > 0:
#             st.markdown("### 🧹 Data Cleaning")
#             method = st.radio("Missing values found. Choose a cleaning method:", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
#             df = clean_data(df, method)
#             st.success("✅ Cleaned missing values.")
#             st.dataframe(df.head(10))
#         else:
#             st.info("No missing values detected.")

#         # Anomaly Detection
#         st.markdown("### 🚨 Anomaly Detection")
#         anomalies = detect_anomalies(df)
#         st.write(anomalies)
#     else:
#         st.error("❌ Could not load measurement data.")
