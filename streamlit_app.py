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

            # 🧹 DATA CLEANING SECTION
            st.markdown("### 🧹 Data Cleaning & Preprocessing")

            # Toggle data preview visibility
            show_preview = st.checkbox("👁️ Show Data Preview", value=True)
            if show_preview:
                st.dataframe(df.head(100))

            # Show missing value summary
            st.markdown("#### 🔍 Missing Value Summary")
            null_summary = df.isnull().sum()
            missing_cols = null_summary[null_summary > 0]

            if not missing_cols.empty:
                st.dataframe(missing_cols.rename("Missing Count"))

                # Global Cleaning Options
                st.markdown("#### 🛠️ Handle Missing Values Globally")
                clean_option = st.selectbox("Select global cleaning method", [
                    "None", "Drop Rows with Nulls", "Fill with 0", "Forward Fill", "Backward Fill"
                ])

                apply_cleaning = st.button("✅ Apply Cleaning")

                if apply_cleaning:
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
                        st.info("No cleaning applied.")
                    
                    # Refresh preview
                    if show_preview:
                        st.markdown("#### 🔁 Updated Data Preview")
                        st.dataframe(df.head(100))
            else:
                st.success("✅ No missing values found.")

            # Optional Normalization/Standardization
            st.markdown("#### ⚙️ Optional Transformations")
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                with st.expander("📊 Normalize or Standardize Columns"):
                    transformation = st.radio("Choose a transformation:", ["None", "Normalize (0-1)", "Standardize (Z-Score)"])
                    apply_transform = st.button("📐 Apply Transformation")

                    if apply_transform and transformation != "None":
                        for col in numeric_cols:
                            if transformation == "Normalize (0-1)":
                                min_val = df[col].min()
                                max_val = df[col].max()
                                df[col] = (df[col] - min_val) / (max_val - min_val)
                            elif transformation == "Standardize (Z-Score)":
                                df[col] = (df[col] - df[col].mean()) / df[col].std()
                        st.success(f"{transformation} applied to all numeric columns.")

            # 📤 Export cleaned data
            st.markdown("### 💾 Export Cleaned Data")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download as CSV",
                data=csv,
                file_name="cleaned_testbench_data.csv",
                mime="text/csv"
            )



            # Anomaly Detection
            st.markdown("### 📌 Anomaly Detection")
            anomalies = detect_anomalies(df)
            st.write(anomalies)
        else:
            st.error("Failed to load the file. Please ensure it's a supported format.")
