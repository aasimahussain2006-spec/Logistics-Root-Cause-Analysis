"""
Unit Tests for Analysis, Driver Tree, Hypotheses, and Reporting
"""

import pytest
import pandas as pd
from pathlib import Path
from src.config import (
    DB_PATH,
    DOCS_DIR,
    DRIVER_TREE_DIR,
    VIS_DIR,
    MEMO_DIR
)
from src.database import LogisticsDatabase


def test_database_tables_and_indices():
    """Verify database connection and table counts."""
    assert DB_PATH.exists()
    db = LogisticsDatabase()
    with db.get_connection() as conn:
        ship_cnt = conn.execute("SELECT COUNT(*) FROM fact_shipments;").fetchone()[0]
        scan_cnt = conn.execute("SELECT COUNT(*) FROM fact_warehouse_scans;").fetchone()[0]
        hub_cnt = conn.execute("SELECT COUNT(*) FROM dim_hubs;").fetchone()[0]

    assert ship_cnt > 300000
    assert scan_cnt > 1000000
    assert hub_cnt == 12


def test_otd_formula_consistency():
    """Verify OTD formula calculation."""
    db = LogisticsDatabase()
    df = db.run_query("""
        SELECT 
            COUNT(*) as total_delivered,
            SUM(on_time_flag) as on_time_count,
            ROUND(AVG(on_time_flag) * 100.0, 2) as otd_pct
        FROM fact_shipments 
        WHERE shipment_status != 'Lost / Exception';
    """)
    calc_otd = round((df["on_time_count"].iloc[0] / df["total_delivered"].iloc[0]) * 100.0, 2)
    assert abs(calc_otd - df["otd_pct"].iloc[0]) < 0.05


def test_hypothesis_log_complete():
    """Verify all 6 hypotheses are tested and recorded."""
    hyp_path = DOCS_DIR / "hypothesis_log.csv"
    assert hyp_path.exists()
    df_hyp = pd.read_csv(hyp_path)
    assert len(df_hyp) == 6
    assert set(df_hyp["hypothesis_id"]) == {"H1", "H2", "H3", "H4", "H5", "H6"}
    assert set(df_hyp["decision"]).issubset({"Supported", "Not supported", "Inconclusive"})


def test_driver_tree_explained_target():
    """Verify Driver Tree explains at least 80% of headline OTD decline."""
    decomp_path = DRIVER_TREE_DIR / "driver_tree_decomposition.csv"
    assert decomp_path.exists()
    df_decomp = pd.read_csv(decomp_path)

    # Find total headline decline and residual
    total_row = df_decomp[df_decomp["Driver Category"] == "Current Headline OTD (Q3-Q4)"]
    residual_row = df_decomp[df_decomp["Driver Category"] == "Unexplained Residual / Random Variance"]

    total_decline = abs(total_row["Impact (pp)"].iloc[0])
    residual = abs(residual_row["Impact (pp)"].iloc[0])

    pct_explained = ((total_decline - residual) / total_decline) * 100.0
    assert pct_explained >= 80.0, f"Expected >= 80% explained, got {pct_explained:.1f}%"


def test_visualizations_exist():
    """Verify all 12 EDA charts and driver tree PNG exist on disk."""
    assert (DRIVER_TREE_DIR / "driver_tree.png").exists()

    expected_charts = [
        "01_overall_otd_trend.png",
        "02_quarterly_performance_comparison.png",
        "03_hub_wise_otd_comparison.png",
        "04_route_delay_distribution.png",
        "05_vehicle_downtime_distribution.png",
        "06_warehouse_processing_distribution.png",
        "07_customer_segment_comparison.png",
        "08_service_type_comparison.png",
        "09_shipment_volume_trends.png",
        "10_seasonal_performance_trends.png",
        "11_delivery_delay_heatmap.png",
        "12_correlation_heatmap.png"
    ]
    for chart in expected_charts:
        assert (VIS_DIR / chart).exists(), f"Missing chart: {chart}"


def test_management_memo_pdf_exists():
    """Verify executive management memo PDF exists."""
    memo_path = MEMO_DIR / "management_memo.pdf"
    assert memo_path.exists()
    assert memo_path.stat().st_size > 5000
