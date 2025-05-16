import streamlit as st
import pandas as pd
from data_cleaning import clean_data, auto_clean
from io import BytesIO

def render_data_cleaning_ui():
    if "df" not in st.session_state:
        st.warning("Please upload and load data first in 'Data Loading' tab.")
        return

    df = st.session_state["df"]

    with st.sidebar:
        st.subheader("⚙️ Cleaning Controls")
        mode = st.radio("Cleaning Mode", ["Manual", "Automatic"])

        if mode == "Manual":
            column = st.selectbox("Select column", df.columns)
            method = st.selectbox("Cleaning method", ["Fill with 0", "Forward Fill", "Backward Fill", "Drop Column"])
            if st.button("Apply to Selected Column"):
                if method == "Drop Column":
                    df = df.drop(columns=[column])
                else:
                    df = clean_data(df, method, column)
                st.session_state["df"] = df
                st.success(f"✅ Applied '{method}' to '{column}'")

            st.markdown("---")
            st.subheader("🧹 Global Cleaning")
            global_method = st.selectbox("Global method", ["Drop Rows", "Fill with 0", "Forward Fill", "Backward Fill"])
            if st.button("Apply Global Cleaning"):
                df = clean_data(df, global_method)
                st.session_state["df"] = df
                st.success(f"✅ Global cleaning: {global_method}")

        elif mode == "Automatic":
            if st.button("✨ Run AI Clean"):
                df = auto_clean(df)
                st.session_state["df"] = df
                st.success("✅ AI cleaning completed!")

    # Main section: Summary + Preview + Export
    st.subheader("📊 Missing Values Summary")
    null_summary = df.isnull().sum()
    null_summary = null_summary[null_summary > 0]
    if not null_summary.empty:
        st.dataframe(null_summary.to_frame("Missing Count"))
    else:
        st.info("✅ No missing values in the dataset.")

    st.subheader("🔍 Cleaned Data Preview")
    st.dataframe(df.head(10))

    # st.subheader("⬇️ Export Cleaned Data")
    # towrite = BytesIO()
    # df.to_excel(towrite, index=False, engine='openpyxl')
    # towrite.seek(0)
    # st.download_button("📥 Download Excel", towrite, "cleaned_testbench_data.xlsx")
