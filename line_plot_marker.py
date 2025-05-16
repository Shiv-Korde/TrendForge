import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_line_plot_with_marker(data: pd.DataFrame, selected_cols: list):
    fig = go.Figure()

    for col in selected_cols:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode='lines',
            name=col
        ))

    # Add interactive vertical marker functionality
    fig.update_layout(
        title="📈 Signal Line Plot with Interactive Marker",
        hovermode="x unified",
        dragmode="drawline",
        newshape=dict(
            line_color='red',
            line_width=2,
            line_dash='dot',
            drawdirection='vertical'
        )
    )

    # Optional: start with a central marker
    midpoint = data.index[len(data) // 2]
    fig.add_shape(
        type="line",
        x0=midpoint,
        x1=midpoint,
        y0=min(data[selected_cols].min()),
        y1=max(data[selected_cols].max()),
        line=dict(color="red", width=2, dash="dot")
    )

    st.plotly_chart(fig, use_container_width=True)
