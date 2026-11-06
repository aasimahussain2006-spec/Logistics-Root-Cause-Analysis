"""
Unit Tests for Data Cleaning & Preprocessing Pipeline
"""

import pytest
import pandas as pd
from pathlib import Path
from src.config import DATA_PROCESSED_DIR, DOCS_DIR, DATA_REF_DIR


def test_cleaned_shipments_integrity():
    """Validate cleaned shipments data quality invariants."""
    clean_ship_path = DATA_PROCESSED_DIR / "cleaned_shipments.csv"
    assert clean_ship_path.exists()

    df = pd.read_csv(clean_ship_path, low_memory=False)

    # 1. Unique shipment IDs
    assert df["shipment_id"].duplicated().sum() == 0

    # 2. No invalid far-future year 2099
    assert (~df["actual_delivery_timestamp"].astype(str).str.startswith("2099")).all()

    # 3. No delivery before dispatch
    valid_ts = df[df["actual_delivery_timestamp"].notna()]
    assert (valid_ts["actual_delivery_timestamp"] >= valid_ts["dispatch_timestamp"]).all()

    # 4. Numeric column types
    assert pd.api.types.is_numeric_dtype(df["shipment_weight_kg"])
    assert pd.api.types.is_numeric_dtype(df["shipping_cost_inr"])
    assert (df["shipment_weight_kg"] > 0).all()

    # 5. Normalized service types
    canonical_services = {"Standard Surface", "Express Cargo", "Same Day Express"}
    assert set(df["service_type"].unique()).issubset(canonical_services)

    # 6. OTD flag invariant
    assert set(df["on_time_flag"].unique()).issubset({0, 1})
    assert set(df["is_delayed"].unique()).issubset({0, 1})


def test_referential_integrity():
    """Verify all foreign keys in cleaned shipments match master tables."""
    clean_ship_path = DATA_PROCESSED_DIR / "cleaned_shipments.csv"
    df_ship = pd.read_csv(clean_ship_path, low_memory=False)
    df_routes = pd.read_csv(DATA_REF_DIR / "routes.csv")
    df_vehicles = pd.read_csv(DATA_REF_DIR / "vehicles.csv")

    valid_routes = set(df_routes["route_id"])
    valid_vehicles = set(df_vehicles["vehicle_id"])

    assert df_ship["route_id"].isin(valid_routes).all()
    assert df_ship["vehicle_id"].isin(valid_vehicles).all()


def test_cleaning_audit_log_exists():
    """Verify cleaning audit log was generated and contains transformation records."""
    audit_path = DOCS_DIR / "cleaning_audit.csv"
    assert audit_path.exists()
    df_audit = pd.read_csv(audit_path)
    assert len(df_audit) >= 5
    assert "records_affected" in df_audit.columns
    assert "records_retained" in df_audit.columns

