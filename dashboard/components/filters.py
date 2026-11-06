"""
Dashboard Interactive Sidebar Filters
"""

import streamlit as st
import pandas as pd
from datetime import datetime


def render_sidebar_filters(df_shipments):
    """Renders comprehensive interactive filters in the sidebar."""
    st.sidebar.image("https://img.icons8.com/color/96/delivery-truck.png", width=64)
    st.sidebar.title("Kolkata Freight")
    st.sidebar.markdown("**Performance Intelligence Portal**")
    st.sidebar.markdown("---")

    # Disclaimer in sidebar
    st.sidebar.info("⚠️ **Synthetic Dataset Notice**\nThis platform uses modeled synthetic data for Kolkata logistics demonstration.")

    # 1. Date Range Filter
    min_date = pd.to_datetime(df_shipments["shipment_date"]).min().date()
    max_date = pd.to_datetime(df_shipments["shipment_date"]).max().date()
    selected_dates = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 2. Hub Filter
    hubs = sorted(df_shipments["origin_hub_id"].unique())
    selected_hubs = st.sidebar.multiselect(
        "🏢 Logistics Hubs",
        options=hubs,
        default=hubs
    )

    # 3. Service Type Filter
    services = sorted(df_shipments["service_type"].unique())
    selected_services = st.sidebar.multiselect(
        "⚡ Service Type",
        options=services,
        default=services
    )

    # 4. Product Category Filter
    categories = sorted(df_shipments["product_category"].unique())
    selected_categories = st.sidebar.multiselect(
        "📦 Product Category",
        options=categories,
        default=categories
    )

    # Apply Filters
    filtered_df = df_shipments.copy()
    if len(selected_dates) == 2:
        start_d, end_d = str(selected_dates[0]), str(selected_dates[1])
        filtered_df = filtered_df[(filtered_df["shipment_date"] >= start_d) & (filtered_df["shipment_date"] <= end_d)]
    
    if selected_hubs:
        filtered_df = filtered_df[filtered_df["origin_hub_id"].isin(selected_hubs) | filtered_df["destination_hub_id"].isin(selected_hubs)]
    
    if selected_services:
        filtered_df = filtered_df[filtered_df["service_type"].isin(selected_services)]
        
    if selected_categories:
        filtered_df = filtered_df[filtered_df["product_category"].isin(selected_categories)]

    return filtered_df

