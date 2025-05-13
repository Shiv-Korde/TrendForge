# import streamlit as st
# from helpers import load_testbench_data, detect_anomalies

# st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")

# st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")
# st.markdown("Upload `.txt`, `.mf4`, `.dat`, `.tdms`, or `.lvm` files to detect anomalies and visualize test trends.")

# uploaded_file = st.file_uploader("Choose a test bench data file", type=["txt", "mf4", "dat", "tdms", "lvm"])

# if uploaded_file:
#     with st.spinner("Loading and analyzing data..."):
#         df = load_testbench_data(uploaded_file)
#         if df is not None:
#             st.success("Data loaded successfully!")
#             st.dataframe(df.head(10))

#             st.markdown("### 📌 Anomaly Detection")
#             anomalies = detect_anomalies(df)
#             st.write(anomalies)
#         else:
#             st.error("Failed to load the file. Please ensure it's a supported format.")


import streamlit as st
from helpers import load_testbench_data, detect_anomalies
import matplotlib.pyplot as plt

st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")

st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")
st.markdown("Upload `.txt`, `.mf4`, `.dat`, `.tdms`, or `.lvm` files to detect anomalies and visualize test trends.")

uploaded_file = st.file_uploader("Choose a test bench data file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    with st.spinner("Loading and analyzing data..."):
        df = load_testbench_data(uploaded_file)

        if df is not None and not df.empty:
            st.success("✅ Data loaded successfully!")
            
            # Table Preview
            st.markdown("### 🗂️ Preview of Data")
            st.dataframe(df.head(100))

            # Visualizations
            st.markdown("### 📈 Visualizations")
            numeric_cols = df.select_dtypes(include=['number']).columns

            if len(numeric_cols) == 0:
                st.warning("No numeric columns found for visualization.")
            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Line Chart")
                    selected_col = st.selectbox("Select a column for line plot", numeric_cols)
                    st.line_chart(df[selected_col])

                with col2:
                    st.markdown("#### Histogram")
                    st.bar_chart(df[selected_col].value_counts().head(50))

            # Anomaly Detection
            st.markdown("### 🚨 Anomaly Detection")
            anomalies = detect_anomalies(df)
            if isinstance(anomalies, dict):
                for col, count in anomalies.items():
                    st.error(f"Anomalies detected in **{col}**: {count} outliers")
            else:
                st.success(anomalies)
        else:
            st.error("❌ Failed to load the file. Please ensure it's a supported format and not empty.")
