import streamlit as st
from helpers import load_testbench_data, detect_anomalies

st.set_page_config(page_title="TrendForge – Test Bench Analyzer", layout="wide")

st.title("📊 TrendForge – AI-Powered Test Bench Data Analyzer")
st.markdown("Upload `.txt`, `.mf4`, `.dat`, `.tdms`, or `.lvm` files to detect anomalies and visualize test trends.")

uploaded_file = st.file_uploader("Choose a test bench data file", type=["txt", "mf4", "dat", "tdms", "lvm"])

if uploaded_file:
    with st.spinner("Loading and analyzing data..."):
        metadata, df = load_testbench_data(uploaded_file)
        if df is not None:
            st.success("Data loaded successfully!")

            # Show Metadata
            if metadata:
                st.markdown("### 🧾 File Metadata")
                st.code(metadata, language="text")

            # Show Data Table
            st.markdown("### 🗂️ Measurement Data Preview")
            st.dataframe(df.head(100))

            # 🧹 Data Cleaning & Export
            st.markdown("---")
            st.markdown("## 🧹 Data Cleaning & Preprocessing")

            # Columns for layout
            left, right = st.columns([1, 2])

            with left:
                st.subheader("👁️ Data Preview Options")
                show_preview = st.checkbox("Show Data Preview", value=True)

                if show_preview:
                    preview_rows = st.slider("Rows to Preview", 5, 100, 10)
                    st.dataframe(df.head(preview_rows), use_container_width=True)

                # Export
                st.subheader("💾 Export Cleaned Data")
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name="cleaned_testbench_data.csv",
                    mime="text/csv"
                )

            with right:
                st.subheader("🔍 Missing Value Summary")
                null_summary = df.isnull().sum()
                missing_cols = null_summary[null_summary > 0]

                if not missing_cols.empty:
                    st.dataframe(missing_cols.rename("Missing Count"), use_container_width=True)

                    st.markdown("### 🛠️ Choose a Cleaning Method")
                    clean_option = st.selectbox("Missing Data Strategy", [
                        "None", "Drop Rows with Nulls", "Fill with 0", "Forward Fill", "Backward Fill"
                    ])
                    if st.button("✅ Apply Cleaning"):
                        if clean_option == "Drop Rows with Nulls":
                            df.dropna(inplace=True)
                            st.success("Dropped rows with missing values.")
                        elif clean_option == "Fill with 0":
                            df.fillna(0, inplace=True)
                            st.success("Filled missing values with 0.")
                        elif clean_option == "Forward Fill":
                            df.ffill(inplace=True)
                            st.success("Forward filled missing values.")
                        elif clean_option == "Backward Fill":
                            df.bfill(inplace=True)
                            st.success("Backward filled missing values.")
                        else:
                            st.info("No changes made.")
                else:
                    st.success("✅ No missing values found.")

            # ➕ Optional Transformation
            st.markdown("---")
            with st.expander("⚙️ Optional Transformations (Normalize / Standardize)"):
                st.markdown("Apply transformations to numeric columns for better scaling.")
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                transformation = st.radio("Choose transformation:", ["None", "Normalize (0-1)", "Standardize (Z-Score)"])
                if st.button("📐 Apply Transformation"):
                    if transformation != "None":
                        for col in numeric_cols:
                            if transformation == "Normalize (0-1)":
                                min_val = df[col].min()
                                max_val = df[col].max()
                                df[col] = (df[col] - min_val) / (max_val - min_val)
                            elif transformation == "Standardize (Z-Score)":
                                df[col] = (df[col] - df[col].mean()) / df[col].std()
                        st.success(f"{transformation} applied.")



            # Anomaly Detection
            st.markdown("### 📌 Anomaly Detection")
            anomalies = detect_anomalies(df)
            st.write(anomalies)
        else:
            st.error("Failed to load the file. Please ensure it's a supported format.")
