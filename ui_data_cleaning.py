import streamlit as st
import pandas as pd
from data_cleaning import clean_data, auto_clean
from io import BytesIO

def render_data_cleaning_ui():
    if "df" not in st.session_state:
        st.warning("Please upload and load data first in 'Data Loading' tab.")
        return

    df = st.session_state["df"]
    st.markdown("### 🧹 Data Cleaning")

    col1, col2 = st.columns(2)

    # 📋 Left: Cleaning Controls
    with col1:
        mode = st.radio("Select cleaning mode:", ["Manual", "Automatic"])

        if mode == "Manual":
            st.subheader("🔧 Manual Column Cleaning")
            column = st.selectbox("Select column", df.columns)
            method = st.selectbox("Cleaning method", ["Fill with 0", "Forward Fill", "Backward Fill", "Drop Nulls"])
            if st.button("Apply to Selected Column"):
                df = clean_data(df, method, column)
                st.session_state["df"] = df
                st.success(f"✅ Applied '{method}' to '{column}'")

            st.subheader("🧹 Global Cleaning")
            global_method = st.selectbox("Apply to entire dataset", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
            if st.button("Apply Global Cleaning"):
                df = clean_data(df, global_method)
                st.session_state["df"] = df
                st.success(f"✅ Applied global cleaning: {global_method}")

        elif mode == "Automatic":
            st.subheader("✨ AI-Based Auto Cleaning")
            if st.button("Run Auto Clean"):
                df = auto_clean(df)
                st.session_state["df"] = df
                st.success("✅ AI-based automatic cleaning completed!")

    # 📊 Right: Null Summary
    with col2:
        st.subheader("📊 Missing Values Summary")
        null_summary = df.isnull().sum()
        null_summary = null_summary[null_summary > 0]
        if not null_summary.empty:
            st.dataframe(null_summary.to_frame("Missing Count"))
        else:
            st.info("✅ No missing values in the dataset.")

    # 🔍 Cleaned Data Preview
    st.markdown("### 🔍 Cleaned Data Preview")
    st.dataframe(df.head(10))

    # ⬇️ Export to Excel
    st.markdown("### ⬇️ Export Cleaned Data")
    towrite = BytesIO()
    df.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)
    st.download_button(
        label="📥 Download as Excel",
        data=towrite,
        file_name="cleaned_testbench_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
