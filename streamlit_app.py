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

            left, right = st.columns([1, 2])

            with left:
                st.subheader("🔍 Missing Value Summary")
                null_summary = df.isnull().sum()
                missing_cols = null_summary[null_summary > 0]
                if not missing_cols.empty:
                    st.dataframe(missing_cols.rename("Missing Count"), use_container_width=True)

                    st.markdown("### 🛠️ Global Cleaning Options")
                    clean_option = st.selectbox("Choose method for handling missing data globally", [
                        "None", "Drop Rows with Nulls", "Drop Columns with Nulls", "Fill with 0", "Forward Fill", "Backward Fill"
                    ])
                    if st.button("✅ Apply Global Cleaning"):
                        if clean_option == "Drop Rows with Nulls":
                            df.dropna(inplace=True)
                            st.success("Dropped rows with missing values.")
                        elif clean_option == "Drop Columns with Nulls":
                            df.dropna(axis=1, inplace=True)
                            st.success("Dropped columns with missing values.")
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
                

            with right:
                st.subheader("👁️ Data Preview")
                show_preview = st.checkbox("Show Data Preview", value=True)

                if show_preview:
                    preview_rows = st.slider("Rows to Preview", 5, 100, 10)
                    st.dataframe(df.head(preview_rows), use_container_width=True)

                st.subheader("💾 Export Cleaned Data")
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name="cleaned_testbench_data.csv",
                    mime="text/csv"
                )
                

            # 🧠 Smart Auto-Clean Button
            st.markdown("### 🤖 Auto Clean (AI-based Heuristics)")
            if st.button("✨ Auto Clean Data"):
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
                st.success("Smart cleaning applied based on missing value patterns!")

            # ⚙️ Per-column cleaning
            st.markdown("---")
            with st.expander("🧬 Clean Specific Signals/Columns"):
                clean_cols = df.columns[df.isnull().any()].tolist()
                if clean_cols:
                    selected_col = st.selectbox("Select a column to clean", clean_cols)
                    col_method = st.radio("Choose cleaning method", ["Fill with 0", "Forward Fill", "Backward Fill", "Fill with Mean", "Drop Column"])
                    if st.button("🧼 Clean Selected Column"):
                        if col_method == "Fill with 0":
                            df[selected_col] = df[selected_col].fillna(0)
                        elif col_method == "Forward Fill":
                            df[selected_col] = df[selected_col].ffill()
                        elif col_method == "Backward Fill":
                            df[selected_col] = df[selected_col].bfill()
                        elif col_method == "Fill with Mean":
                            df[selected_col] = df[selected_col].fillna(df[selected_col].mean())
                        elif col_method == "Drop Column":
                            df.drop(columns=[selected_col], inplace=True)
                        st.success(f"{selected_col} cleaned using '{col_method}'.")
                else:
                    st.info("No columns with missing data.")


            # Anomaly Detection
            st.markdown("### 📌 Anomaly Detection")
            anomalies = detect_anomalies(df)
            st.write(anomalies)
        else:
            st.error("Failed to load the file. Please ensure it's a supported format.")
