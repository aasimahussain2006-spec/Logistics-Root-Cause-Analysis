"""
Unit Tests for Data Generation Module
"""

import pytest
import pandas as pd
from pathlib import Path
from src.config import DATA_RAW_DIR, DATA_REF_DIR, HUBS


def test_reference_datasets_exist():
    """Verify all reference files are generated."""
    assert (DATA_REF_DIR / "hubs.csv").exists()
    assert (DATA_REF_DIR / "hub_mapping.csv").exists()
    assert (DATA_REF_DIR / "routes.csv").exists()
    assert (DATA_REF_DIR / "vehicles.csv").exists()
    assert (DATA_REF_DIR / "customers.csv").exists()


def test_hubs_count_and_keys():
    """Verify exactly 12 Kolkata hubs exist."""
    df_hubs = pd.read_csv(DATA_REF_DIR / "hubs.csv")
    assert len(df_hubs) == 12
    assert set(df_hubs["hub_id"]) == set(HUBS.keys())


def test_raw_datasets_exist_and_non_empty():
    """Verify raw shipments and warehouse scans exist and contain records."""
    raw_ship_path = DATA_RAW_DIR / "raw_shipments.csv"
    raw_scans_path = DATA_RAW_DIR / "raw_warehouse_scans.csv"

    assert raw_ship_path.exists()
    assert raw_scans_path.exists()

    df_ship = pd.read_csv(raw_ship_path, nrows=50)
    df_scans = pd.read_csv(raw_scans_path, nrows=50)

    assert len(df_ship) == 50
    assert len(df_scans) == 50
    assert "shipment_id" in df_ship.columns
    assert "scan_id" in df_scans.columns


def test_routes_directed_graph():
    """Verify 12 hubs generate exactly 12 * 11 = 132 directed routes."""
    df_routes = pd.read_csv(DATA_REF_DIR / "routes.csv")
    assert len(df_routes) == 132
    # Verify origin != destination
    assert (df_routes["origin_hub_id"] == df_routes["destination_hub_id"]).sum() == 0

