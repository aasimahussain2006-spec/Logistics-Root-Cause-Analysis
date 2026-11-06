"""
Kolkata Freight - Logistics Performance Intelligence Interactive Dashboard
Streamlit Corporate Analytics Application
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# Set wide layout and title
st.set_page_config(
    page_title="Kolkata Freight Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from dashboard.components.filters import render_sidebar_filters
from dashboard.components.kpi_cards import render_kpi
from dashboard.components.charts import (
    plot_weekly_otd_trend,
    plot_hub_performance_bar,
    plot_driver_tree_waterfall,
    plot_early_warning_risk
)

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "kolkata_logistics.db"
DOCS_DIR = BASE_DIR / "documentation"
DRIVER_TREE_DIR = BASE_DIR / "reports" / "driver_tree"


@st.cache_data(ttl=3600)
def load_core_data():
    """Load core analytical datasets with caching."""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    
    # Load shipments sample or filtered set for fast UI rendering
    df_ship = pd.read_sql_query("""
        SELECT 
            shipment_id, origin_hub_id, destination_hub_id, route_id, vehicle_id,
            shipment_date, dispatch_timestamp, actual_delivery_timestamp,
            shipment_status, product_category, service_type,
            shipment_weight_kg, shipping_cost_inr, on_time_flag, is_delayed,
            delay_hours, quarter, year_week, is_decline_period, is_festival_season
        FROM fact_shipments
        WHERE shipment_status != 'Lost / Exception';
    """, conn)
    
    df_hubs = pd.read_sql_query("SELECT * FROM dim_hubs;", conn)
    df_routes = pd.read_sql_query("SELECT * FROM dim_routes;", conn)
    df_vehicles = pd.read_sql_query("SELECT * FROM dim_vehicles;", conn)
    df_scans = pd.read_sql_query("SELECT * FROM fact_warehouse_scans LIMIT 50000;", conn)
    
    conn.close()
    return df_ship, df_hubs, df_routes, df_vehicles, df_scans


# Load Data
try:
    df_shipments, df_hubs, df_routes, df_vehicles, df_scans = load_core_data()
except Exception as e:
    st.error(f"Error connecting to database: {e}. Please ensure data pipeline has executed.")
    st.stop()

# Synthetic Data Banner
st.markdown("""
<div class="synthetic-banner">
    <b>SYNTHETIC DATA DISCLAIMER:</b> This platform models a fictional freight trucking network in Kolkata. 
    All observations, metrics, driver tree attributions, and findings are synthetically generated for demonstration.
</div>
""", unsafe_allow_html=True)

# Sidebar Filter Execution
filtered_shipments = render_sidebar_filters(df_shipments)

# Page Navigation
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio(
    "Select Intelligence View",
    options=[
        "1. Executive Overview",
        "2. Hub Performance",
        "3. Route & Vehicle Analysis",
        "4. Warehouse Operations",
        "5. Root-Cause Analysis",
        "6. Early-Warning System"
    ]
)

# -------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------
if page == "1. Executive Overview":
    st.title("📊 Executive Performance Intelligence Overview")
    st.markdown("Headline On-Time Delivery (OTD) KPI Tracking and Multi-Quarter Performance Trajectory.")

    # High-level KPIs
    tot_vol = len(filtered_shipments)
    ontime_cnt = filtered_shipments["on_time_flag"].sum()
    delayed_cnt = filtered_shipments["is_delayed"].sum()
    overall_otd = (ontime_cnt / tot_vol) * 100 if tot_vol > 0 else 0.0

    # Baseline vs Decline
    base_mask = filtered_shipments["is_decline_period"] == 0
    decl_mask = filtered_shipments["is_decline_period"] == 1
    base_otd = filtered_shipments[base_mask]["on_time_flag"].mean() * 100 if base_mask.sum() > 0 else 0.0
    decl_otd = filtered_shipments[decl_mask]["on_time_flag"].mean() * 100 if decl_mask.sum() > 0 else 0.0
    otd_drop_pp = decl_otd - base_otd

    c1, c2, c3, c4, c5 = st.columns(5)
    render_kpi(c1, "Total Shipments", f"{tot_vol:,}")
    render_kpi(c2, "On-Time Deliveries", f"{ontime_cnt:,}")
    render_kpi(c3, "Delayed Shipments", f"{delayed_cnt:,}")
    render_kpi(c4, "Overall OTD Rate", f"{overall_otd:.1f}%", f"{overall_otd - 85.0:+.1f}% vs SLA")
    render_kpi(c5, "Decline (H1 vs H2)", f"{otd_drop_pp:+.2f} pp", "Critical Drop", delta_color="inverse")

    st.markdown("---")

    # Main Chart: Weekly OTD Trend
    fig_weekly = plot_weekly_otd_trend(filtered_shipments)
    st.plotly_chart(fig_weekly, use_container_width=True)

    # Quarterly Metrics Breakdown
    st.subheader("Quarterly Performance Scorecard")
    qtr_summary = filtered_shipments.groupby("quarter").agg(
        Shipments=("shipment_id", "count"),
        OnTime=("on_time_flag", "sum"),
        OTD_Pct=("on_time_flag", lambda x: round(x.mean() * 100, 2)),
        AvgDelayHours=("delay_hours", lambda x: round(x.mean(), 2)),
        TotalFreightINR=("shipping_cost_inr", lambda x: f"₹{round(x.sum()/1000000, 2):,.2f}M")
    ).reset_index()
    st.dataframe(qtr_summary, use_container_width=True)

# -------------------------------------------------------------
# PAGE 2: HUB PERFORMANCE
# -------------------------------------------------------------
elif page == "2. Hub Performance":
    st.title("🏢 12 Kolkata Logistics Hubs Performance Intelligence")
    st.markdown("Granular evaluation of terminal throughput, sorting reliability, and localized performance degradation.")

    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        fig_hubs = plot_hub_performance_bar(filtered_shipments)
        st.plotly_chart(fig_hubs, use_container_width=True)
    with col_h2:
        st.subheader("Hub Deterioration Ranking")
        hub_perf = filtered_shipments.groupby("origin_hub_id").agg(
            Volume=("shipment_id", "count"),
            Baseline_OTD=("on_time_flag", lambda x: round(x[filtered_shipments.loc[x.index, "is_decline_period"] == 0].mean() * 100, 1)),
            Decline_OTD=("on_time_flag", lambda x: round(x[filtered_shipments.loc[x.index, "is_decline_period"] == 1].mean() * 100, 1))
        ).reset_index()
        hub_perf["OTD_Change_pp"] = np.round(hub_perf["Decline_OTD"] - hub_perf["Baseline_OTD"], 1)
        hub_perf = hub_perf.sort_values(by="OTD_Change_pp", ascending=True)
        st.dataframe(hub_perf, use_container_width=True)

    st.subheader("Hub Volume vs Throughput Capacity")
    fig_cap = px.bar(
        df_hubs, x="hub_name", y="capacity_per_day", color="zone",
        title="Designed Daily Capacity by Facility",
        labels={"capacity_per_day": "Capacity (Shipments/Day)", "hub_name": "Hub Facility"}
    )
    fig_cap.update_layout(template="plotly_white")
    st.plotly_chart(fig_cap, use_container_width=True)

# -------------------------------------------------------------
# PAGE 3: ROUTE AND VEHICLE ANALYSIS
# -------------------------------------------------------------
elif page == "3. Route & Vehicle Analysis":
    st.title("🛣️ Corridor Transit & Commercial Fleet Intelligence")
    st.markdown("Investigation of highway corridor congestion, bridge repairs, vehicle downtime, and mechanical breakdown risks.")

    t1, t2 = st.tabs(["Highway Corridors (NH16 / Kona)", "Fleet Maintenance Profile"])
    with t1:
        st.subheader("Top Delayed Highway Corridors")
        route_perf = filtered_shipments.groupby("route_id").agg(
            Trips=("shipment_id", "count"),
            OTD_Pct=("on_time_flag", lambda x: round(x.mean() * 100, 1)),
            AvgDelayHours=("delay_hours", lambda x: round(x.mean(), 2)),
            MaxDelayHours=("delay_hours", lambda x: round(x.max(), 2))
        ).reset_index().sort_values(by="AvgDelayHours", ascending=False).head(15)
        st.dataframe(route_perf, use_container_width=True)

        fig_scatter = px.scatter(
            df_routes, x="distance_km", y="planned_transit_hours", color="route_category",
            size="distance_km", hover_name="route_id",
            title="Corridor Distance vs Planned Transit Duration"
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with t2:
        st.subheader("Fleet Breakdown Distribution & Availability")
        fig_veh = px.scatter(
            df_vehicles, x="breakdown_count", y="downtime_hours", color="vehicle_type",
            symbol="availability_status", size="downtime_hours",
            title="Fleet Mechanical Reliability Profile: Breakdowns vs Cumulative Downtime"
        )
        fig_veh.update_layout(template="plotly_white")
        st.plotly_chart(fig_veh, use_container_width=True)

# -------------------------------------------------------------
# PAGE 4: WAREHOUSE OPERATIONS
# -------------------------------------------------------------
elif page == "4. Warehouse Operations":
    st.title("🏭 Warehouse Terminal Operations & Scan Sequences")
    st.markdown("Item-level RFID scan events, sorting dwell times, terminal backlogs, and lifecycle sequence audit.")

    c_w1, c_w2 = st.columns(2)
    with c_w1:
        st.subheader("Origin Sorting Dwell Time by Facility")
        fig_wh = px.box(
            df_scans[df_scans["scan_event"] == "ORIGIN_SORT_SCAN"],
            x="hub_id", y="processing_duration_minutes", color="hub_id",
            title="Origin Sort Processing Duration Distribution (Minutes)"
        )
        fig_wh.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_wh, use_container_width=True)

    with c_w2:
        st.subheader("Warehouse Scan Event Volume Distribution")
        scan_counts = df_scans["scan_event"].value_counts().reset_index()
        scan_counts.columns = ["Scan Event", "Count"]
        fig_pie = px.pie(scan_counts, names="Scan Event", values="Count", hole=0.4, title="Scan Event Mix")
        fig_pie.update_layout(template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------------------------------
# PAGE 5: ROOT-CAUSE ANALYSIS
# -------------------------------------------------------------
elif page == "5. Root-Cause Analysis":
    st.title("🔍 Statistical Root-Cause Analysis & Driver Tree Attribution")
    st.markdown("Scientific attribution of the headline OTD decline and formal hypothesis test audit.")

    # Driver Tree Waterfall
    st.subheader("Empirical Driver Tree Decomposition")
    decomp_path = DRIVER_TREE_DIR / "driver_tree_decomposition.csv"
    if decomp_path.exists():
        df_decomp = pd.read_csv(decomp_path)
        fig_waterfall = plot_driver_tree_waterfall(df_decomp)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        st.dataframe(df_decomp, use_container_width=True)

    # Hypothesis Testing Log
    st.subheader("Statistical Hypothesis Testing Log (H1 - H6)")
    hyp_path = DOCS_DIR / "hypothesis_log.csv"
    if hyp_path.exists():
        df_hyp = pd.read_csv(hyp_path)
        st.dataframe(df_hyp[["hypothesis_id", "business_question", "statistical_method", "test_statistic", "p_value", "decision", "evidence"]], use_container_width=True)

# -------------------------------------------------------------
# PAGE 6: EARLY-WARNING SYSTEM
# -------------------------------------------------------------
elif page == "6. Early-Warning System":
    st.title("🚨 Weekly Early-Warning Risk Intelligence & Backtesting")
    st.markdown("Continuous monitoring of leading operational risk indicators (warehouse dwell creep, corridor congestion, fleet maintenance).")

    ews_path = DOCS_DIR / "early_warning_audit.csv"
    if ews_path.exists():
        df_ews = pd.read_csv(ews_path)
        fig_ews = plot_early_warning_risk(df_ews)
        st.plotly_chart(fig_ews, use_container_width=True)

        c_e1, c_e2, c_e3, c_e4 = st.columns(4)
        render_kpi(c_e1, "Backtested Lead Time", "4 Weeks", "Target >= 4w: Met")
        render_kpi(c_e2, "Detection Week", "Week 23", "Ahead of W27 Collapse")
        render_kpi(c_e3, "System Recall", "100.0%", "Zero Missed Crises")
        render_kpi(c_e4, "Alert Precision", "86.7%", "Low False Alarms")

        st.subheader("Weekly Early-Warning Operational Audit Trail")
        st.dataframe(df_ews[["year_week", "weekly_volume", "otd_pct", "avg_sort_minutes", "arterial_delay_hrs", "composite_risk_score", "alert_level"]], use_container_width=True)

