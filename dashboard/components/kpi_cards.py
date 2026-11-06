"""
Dashboard KPI Card Components
"""

import streamlit as st


def render_kpi(col, title, value, delta=None, delta_color="normal", card_type="default"):
    """Renders a styled corporate KPI card."""
    with col:
        st.metric(label=title, value=value, delta=delta, delta_color=delta_color)

