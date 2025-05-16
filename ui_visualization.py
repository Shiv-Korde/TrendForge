import streamlit as st
import plotly.express as px
import polars as pl
from io import BytesIO

@st.cache_data(show_spinner=False)
def preprocess_data(df: pl.DataFrame, columns, sample_size: int):
    # Drop nulls, sample, convert to pandas for Plotly
    clean_df = df.select(columns).drop_nulls()
    if clean_df.height > sample_size:
        clean_df = clean_df.sample(n=sample_size, seed=42)
    return clean_df.to_pandas()

def render_visualization_ui():
    if "df" not in st.session_state:
        st.warning("Please upload and load data first in 'Data Loading' tab.")
        return

    pdf = st.session_state["df"]
    df = pl.from_pandas(pdf)

    # ✅ Get only float or integer numeric columns
    numeric_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32, pl.UInt32, pl.UInt64)
    ]

    if not numeric_cols:
        st.info("No numeric columns available for visualization.")
        return

    st.markdown("### 📊 Visualize Measurement Signals")

    # Sidebar controls
    with st.sidebar:
        st.subheader("⚙️ Visualization Settings")
        viz_type = st.radio("Chart type", ["Line Plot", "Histogram", "Scatter Plot"])
        selected_cols = st.multiselect("Select signal(s)", numeric_cols, default=[numeric_cols[0]])
        sample_size = st.slider("Max data points", 100, 5000, 1000)

    if not selected_cols:
        st.warning("Please select at least one column.")
        return

    # Preprocess & sample data
    data = preprocess_data(df, selected_cols, sample_size)

    # Plot
    if viz_type == "Line Plot":
        fig = px.line(data, y=selected_cols, title="Signal Line Plot")
    elif viz_type == "Histogram":
        fig = px.histogram(data.melt(var_name="Signal", value_name="Value"), x="Value", color="Signal", barmode="overlay")
    elif viz_type == "Scatter Plot":
        if len(selected_cols) == 2:
            fig = px.scatter(data, x=selected_cols[0], y=selected_cols[1], title="Scatter Plot")
        else:
            st.warning("Please select exactly 2 signals for a scatter plot.")
            return
    else:
        st.error("Invalid chart type.")
        return

    st.plotly_chart(fig, use_container_width=True)
