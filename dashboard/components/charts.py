"""
Dashboard Interactive Plotly Visualizations
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_weekly_otd_trend(df):
    """Interactive weekly OTD trend line with SLA target threshold."""
    wk = df.groupby("year_week").agg(
        volume=("shipment_id", "count"),
        otd_pct=("on_time_flag", lambda x: round(x.mean() * 100, 2))
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=wk["year_week"], y=wk["volume"],
        name="Weekly Volume", marker_color="#E9ECEF", opacity=0.7, yaxis="y2"
    ))
    fig.add_trace(go.Scatter(
        x=wk["year_week"], y=wk["otd_pct"],
        mode="lines+markers", name="OTD Rate (%)",
        line=dict(color="#1B365D", width=3), marker=dict(size=6)
    ))
    fig.add_hline(y=85.0, line_dash="dash", line_color="green", annotation_text="Target SLA (85%)")

    fig.update_layout(
        title="Weekly On-Time Delivery Rate & Volume Trajectory",
        xaxis=dict(title="ISO Calendar Week"),
        yaxis=dict(title="On-Time Delivery Rate (%)", range=[30, 100]),
        yaxis2=dict(title="Weekly Volume", overlaying="y", side="right", showgrid=False),
        legend=dict(x=0.01, y=0.05),
        template="plotly_white",
        height=450
    )
    return fig


def plot_hub_performance_bar(df):
    """Hub-level OTD ranking with baseline vs decline bars."""
    hubs = df.groupby(["origin_hub_id", "is_decline_period"]).agg(
        otd_pct=("on_time_flag", lambda x: round(x.mean() * 100, 1))
    ).reset_index()
    hubs["Period"] = hubs["is_decline_period"].map({0: "Baseline (H1)", 1: "Decline (H2)"})

    fig = px.bar(
        hubs, x="origin_hub_id", y="otd_pct", color="Period", barmode="group",
        color_discrete_map={"Baseline (H1)": "#008080", "Decline (H2)": "#D9534F"},
        title="Hub-Level On-Time Delivery Performance: Baseline vs Decline Period",
        labels={"origin_hub_id": "Logistics Hub ID", "otd_pct": "OTD Rate (%)"}
    )
    fig.add_hline(y=85.0, line_dash="dash", line_color="green", annotation_text="SLA Target (85%)")
    fig.update_layout(template="plotly_white", height=450)
    return fig


def plot_driver_tree_waterfall(df_decomp):
    """Plotly Waterfall chart representing driver tree attribution."""
    names = []
    measures = []
    values = []

    for i, row in df_decomp.iterrows():
        cat = row["Driver Category"]
        impact = row["Impact (pp)"]
        if i == 0:
            names.append("Baseline OTD")
            measures.append("absolute")
            # Extract float
            values.append(float(row["Metric"].replace("%", "")))
        elif i == len(df_decomp) - 1:
            names.append("Current OTD")
            measures.append("total")
            values.append(float(row["Metric"].replace("%", "")))
        else:
            names.append(cat.split("(")[0].strip())
            measures.append("relative")
            values.append(impact)

    fig = go.Figure(go.Waterfall(
        name="Decline Decomposition",
        orientation="v",
        measure=measures,
        x=names,
        textposition="outside",
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#D9534F"}},
        increasing={"marker": {"color": "#28A745"}},
        totals={"marker": {"color": "#1B365D"}}
    ))
    fig.update_layout(
        title="Empirical Driver Tree: Waterfall Attribution of Headline OTD Decline",
        yaxis_title="OTD Rate (%) / Impact (pp)",
        template="plotly_white",
        height=500
    )
    return fig


def plot_early_warning_risk(df_ews):
    """Interactive risk index trajectory with alert zone bands."""
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=1.2, fillcolor="green", opacity=0.1, line_width=0, annotation_text="NORMAL ZONE")
    fig.add_hrect(y0=1.2, y1=2.0, fillcolor="gold", opacity=0.15, line_width=0, annotation_text="WATCH ZONE")
    fig.add_hrect(y0=2.0, y1=3.0, fillcolor="orange", opacity=0.2, line_width=0, annotation_text="WARNING ZONE")
    fig.add_hrect(y0=3.0, y1=15.0, fillcolor="red", opacity=0.2, line_width=0, annotation_text="CRITICAL ZONE")

    fig.add_trace(go.Scatter(
        x=df_ews["year_week"], y=df_ews["composite_risk_score"],
        mode="lines+markers", name="Composite Operational Risk Index",
        line=dict(color="#1B365D", width=3),
        marker=dict(size=7, color=np.where(df_ews["composite_risk_score"]>=3.0, "red",
                                  np.where(df_ews["composite_risk_score"]>=2.0, "orange",
                                  np.where(df_ews["composite_risk_score"]>=1.2, "gold", "green"))))
    ))
    fig.add_vline(x=23, line_dash="dash", line_color="orange", annotation_text="Earliest Warning (Week 23)")
    fig.add_vline(x=27, line_dash="solid", line_color="red", annotation_text="OTD Collapse (Week 27)")

    fig.update_layout(
        title="Weekly Early-Warning Operational Risk Index (Backtested Lead Time = 4 Weeks)",
        xaxis=dict(title="ISO Calendar Week (1 to 52)"),
        yaxis=dict(title="Composite Operational Risk Score", range=[0, 14]),
        template="plotly_white",
        height=450
    )
    return fig

