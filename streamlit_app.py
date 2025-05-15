import streamlit as st
from helpers import load_testbench_data, detect_anomalies
import pandas as pd

st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")
st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")

uploaded_file = st.file_uploader("Choose a test bench data file (.txt, .mf4, .dat, .tdms, .lvm)", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    df = None
    metadata, df = load_testbench_data(uploaded_file) if uploaded_file.name.endswith(".txt") else (None, load_testbench_data(uploaded_file))

    if df is not None and not df.empty:
        st.success("✅ File loaded successfully!")

        with st.sidebar:
            st.header("🧹 Data Cleaning Settings")
            clean_mode = st.radio("Choose Cleaning Mode", ["Manual", "Automatic (ML)"])

            show_preview = st.checkbox("Show Data Preview", value=True)
            preview_rows = st.slider("Preview Rows", 5, 100, 10)

            st.markdown("---")
            export_csv = st.button("💾 Export Preview as CSV")

        # Data Preview
        if show_preview:
            st.markdown("### 📄 Data Preview")
            st.dataframe(df.head(preview_rows), use_container_width=True)

        # Show Metadata
        if metadata:
            st.markdown("### 🧾 File Metadata")
            st.code(metadata, language="text")

        # MANUAL CLEANING MODE
        if clean_mode == "Manual":
            st.markdown("---")
            st.header("🧼 Manual Data Cleaning")

            # Missing Summary
            null_summary = df.isnull().sum()
            missing_cols = null_summary[null_summary > 0]

            if not missing_cols.empty:
                st.subheader("🔍 Missing Value Summary")
                st.dataframe(missing_cols.rename("Missing Count"))

                st.subheader("🛠 Global Cleaning")
                global_method = st.selectbox("Global Cleaning Method", [
                    "None", "Drop Rows with Nulls", "Drop Columns with Nulls", "Fill with 0", "Forward Fill", "Backward Fill"
                ])
                if st.button("✅ Apply Global Cleaning"):
                    if global_method == "Drop Rows with Nulls":
                        df.dropna(inplace=True)
                    elif global_method == "Drop Columns with Nulls":
                        df.dropna(axis=1, inplace=True)
                    elif global_method == "Fill with 0":
                        df.fillna(0, inplace=True)
                    elif global_method == "Forward Fill":
                        df.ffill(inplace=True)
                    elif global_method == "Backward Fill":
                        df.bfill(inplace=True)
                    st.success(f"Global cleaning applied using: {global_method}")

                # Column-wise cleaning
                st.subheader("🧬 Column-wise Cleaning")
                clean_cols = df.columns[df.isnull().any()].tolist()
                if clean_cols:
                    col_to_clean = st.selectbox("Select Column", clean_cols)
                    col_method = st.radio("Method for selected column", [
                        "Fill with 0", "Forward Fill", "Backward Fill", "Fill with Mean", "Drop Column"
                    ])
                    if st.button("🧽 Clean Selected Column"):
                        if col_method == "Fill with 0":
                            df[col_to_clean] = df[col_to_clean].fillna(0)
                        elif col_method == "Forward Fill":
                            df[col_to_clean] = df[col_to_clean].ffill()
                        elif col_method == "Backward Fill":
                            df[col_to_clean] = df[col_to_clean].bfill()
                        elif col_method == "Fill with Mean":
                            df[col_to_clean] = df[col_to_clean].fillna(df[col_to_clean].mean())
                        elif col_method == "Drop Column":
                            df.drop(columns=[col_to_clean], inplace=True)
                        st.success(f"{col_to_clean} cleaned using '{col_method}'")

            else:
                st.success("✅ No missing values detected.")

        # AUTOMATIC CLEANING MODE
        if clean_mode == "Automatic (ML)":
            st.markdown("---")
            st.header("🤖 Smart Auto-Cleaning (Heuristics)")

            if st.button("✨ Run Auto Clean"):
                for col in df.columns:
                    null_pct = df[col].isnull().mean()
                    if null_pct == 0:
                        continue
                    elif null_pct > 0.5:
                        df.drop(columns=[col], inplace=True)
                    elif null_pct <= 0.1:
                        df[col] = df[col].fillna(0)
                    elif null_pct <= 0.3:
                        df[col] = df[col].fillna(df[col].mean())
                    else:
                        df[col] = df[col].ffill().bfill()
                st.success("Auto-cleaning applied based on data patterns!")

        # Export
        if export_csv:
            st.markdown("### 📤 Export")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Cleaned Preview as CSV",
                data=csv,
                file_name="cleaned_preview.csv",
                mime="text/csv"
            )

        # ANOMALY DETECTION
        st.markdown("---")
        st.header("🚨 Anomaly Detection Summary")
        anomalies = detect_anomalies(df)
        st.write(anomalies)
    else:
        st.error("❌ Failed to load the file or file is empty.")
