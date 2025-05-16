import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from io import BytesIO
import pandas as pd

def draw_marker_line_plot(data: pd.DataFrame, selected_cols, max_points=1000):
    st.markdown("### 📍 Interactive Marker Line")

    # Limit data for performance
    sampled_data = data[selected_cols].dropna().copy()
    if len(sampled_data) > max_points:
        sampled_data = sampled_data.sample(n=max_points, random_state=42).sort_index()

    index = st.slider("Move marker", min_value=0, max_value=len(sampled_data)-1, step=1)

    # Build fast line plot using Scattergl
    fig = go.Figure()

    for col in selected_cols:
        fig.add_trace(go.Scattergl(
            x=sampled_data.index, y=sampled_data[col],
            mode='lines', name=col
        ))

    # Add efficient vertical marker
    fig.add_vline(
        x=sampled_data.index[index],
        line_width=2, line_dash="dot", line_color="red",
        annotation_text=f"Index {index}", annotation_position="top right"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display signal values at the marker
    st.markdown("### 🔎 Signal Values at Marker")
    values = sampled_data.iloc[index]
    st.dataframe(values.reset_index().rename(columns={'index': 'Signal', 0: 'Value'}))


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
        draw_marker_line_plot(data, selected_cols)
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
