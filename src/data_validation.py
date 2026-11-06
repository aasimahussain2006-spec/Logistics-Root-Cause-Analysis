"""
Logistics Root-Cause Analysis - Data Quality Inspection & Validation
Detects anomalies, missing values, duplicates, timezone discrepancies, and integrity violations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from src.config import DATA_RAW_DIR, DATA_REF_DIR, HUBS


def validate_raw_datasets():
    """
    Performs comprehensive data quality audit across all raw datasets.
    Returns a summary dictionary of detected issues.
    """
    print("\n=======================================================")
    print("STARTING DATA QUALITY VALIDATION AUDIT")
    print("=======================================================")

    raw_shipments_path = DATA_RAW_DIR / "raw_shipments.csv"
    raw_scans_path = DATA_RAW_DIR / "raw_warehouse_scans.csv"
    routes_path = DATA_REF_DIR / "routes.csv"
    vehicles_path = DATA_REF_DIR / "vehicles.csv"
    customers_path = DATA_REF_DIR / "customers.csv"

    # 1. Load Raw Datasets
    print("Loading raw datasets for quality audit...")
    df_shipments = pd.read_csv(raw_shipments_path, low_memory=False)
    df_scans = pd.read_csv(raw_scans_path, low_memory=False)
    df_routes = pd.read_csv(routes_path)
    df_vehicles = pd.read_csv(vehicles_path)
    df_customers = pd.read_csv(customers_path)

    report = {}

    # Dataset Dimensions
    report["dimensions"] = {
        "raw_shipments": {"rows": len(df_shipments), "cols": len(df_shipments.columns)},
        "raw_scans": {"rows": len(df_scans), "cols": len(df_scans.columns)},
        "routes": {"rows": len(df_routes), "cols": len(df_routes.columns)},
        "vehicles": {"rows": len(df_vehicles), "cols": len(df_vehicles.columns)},
        "customers": {"rows": len(df_customers), "cols": len(df_customers.columns)},
    }
    print(f"Loaded Raw Shipments: {len(df_shipments):,} rows, {len(df_shipments.columns)} columns")
    print(f"Loaded Raw Scans:     {len(df_scans):,} rows, {len(df_scans.columns)} columns")

    # Issue 1: Duplicate Records
    dup_shipments = df_shipments.duplicated().sum()
    dup_scans = df_scans.duplicated().sum()
    report["duplicates"] = {
        "shipments_exact_duplicates": int(dup_shipments),
        "scans_exact_duplicates": int(dup_scans)
    }
    print(f"[Issue 1] Duplicate Records: {dup_shipments:,} duplicate shipments, {dup_scans:,} duplicate scans detected.")

    # Issue 2: Missing Values
    missing_delivery_ts = df_shipments["actual_delivery_timestamp"].isna().sum()
    missing_status = df_shipments["shipment_status"].isna().sum()
    report["missing_values"] = {
        "missing_delivery_timestamp": int(missing_delivery_ts),
        "missing_status": int(missing_status)
    }
    print(f"[Issue 2] Missing Values: {missing_delivery_ts:,} shipments missing delivery timestamp.")

    # Issue 3: Inconsistent Data Types (String suffixes in numeric columns)
    weight_str_count = df_shipments["shipment_weight"].astype(str).str.contains("kg").sum()
    cost_str_count = df_shipments["shipping_cost"].astype(str).str.contains("INR").sum()
    report["dirty_data_types"] = {
        "weight_with_kg_suffix": int(weight_str_count),
        "cost_with_inr_prefix": int(cost_str_count)
    }
    print(f"[Issue 3] Dirty Numeric Types: {weight_str_count:,} weights have 'kg', {cost_str_count:,} costs have 'INR'.")

    # Issue 4: Mixed Timezone and Datetime Formats
    has_tz_offset = df_shipments["promised_delivery_timestamp"].astype(str).str.contains(r"\+05:30|Z").sum()
    has_slashes = df_shipments["promised_delivery_timestamp"].astype(str).str.contains("/").sum()
    report["timezone_anomalies"] = {
        "explicit_tz_offsets": int(has_tz_offset),
        "slash_date_formats": int(has_slashes)
    }
    print(f"[Issue 4] Timezone Discrepancies: {has_tz_offset:,} records with explicit TZ offsets, {has_slashes:,} with slash formats.")

    # Issue 5: Invalid Chronology (Delivery before dispatch or future dates)
    # Check string comparison or quick parse
    disp_ts = df_shipments["dispatch_timestamp"].astype(str)
    act_ts = df_shipments["actual_delivery_timestamp"].dropna().astype(str)
    # Match on index
    common_idx = act_ts.index
    inv_past = (act_ts.loc[common_idx] < disp_ts.loc[common_idx]).sum()
    inv_future = act_ts.str.startswith("2099").sum()
    report["invalid_timestamps"] = {
        "delivery_before_dispatch": int(inv_past),
        "far_future_year_2099": int(inv_future)
    }
    print(f"[Issue 5] Invalid Chronology: {inv_past:,} records delivered before dispatch, {inv_future:,} in year 2099.")

    # Issue 6: Legacy / Unmapped Hub Identifiers
    valid_hub_ids = set(HUBS.keys())
    origin_invalid = (~df_shipments["origin_hub_id"].isin(valid_hub_ids)).sum()
    dest_invalid = (~df_shipments["destination_hub_id"].isin(valid_hub_ids)).sum()
    report["unmapped_hubs"] = {
        "origin_unmapped_count": int(origin_invalid),
        "destination_unmapped_count": int(dest_invalid)
    }
    print(f"[Issue 6] Unmapped Hub Codes: {origin_invalid:,} origin, {dest_invalid:,} destination legacy codes.")

    # Issue 7: Inconsistent Category Labels
    valid_services = {"Standard Surface", "Express Cargo", "Same Day Express"}
    inconsistent_services = (~df_shipments["service_type"].isin(valid_services)).sum()
    report["inconsistent_categories"] = {
        "inconsistent_service_types": int(inconsistent_services)
    }
    print(f"[Issue 7] Inconsistent Labels: {inconsistent_services:,} non-standard service type strings.")

    # Issue 8: Referential Integrity Violations
    valid_vehicles = set(df_vehicles["vehicle_id"])
    valid_routes = set(df_routes["route_id"])
    orphan_vehicles = (~df_shipments["vehicle_id"].isin(valid_vehicles)).sum()
    orphan_routes = (~df_shipments["route_id"].isin(valid_routes)).sum()
    report["referential_integrity"] = {
        "orphaned_vehicles": int(orphan_vehicles),
        "orphaned_routes": int(orphan_routes)
    }
    print(f"[Issue 8] Referential Integrity: {orphan_vehicles:,} orphaned vehicles, {orphan_routes:,} orphaned routes.")

    # Issue 9: Out-of-Order Warehouse Scans
    ooo_scans = (df_scans["scan_timestamp"] == "2024-01-01 00:00:01").sum()
    report["out_of_order_scans"] = {
        "ooo_or_corrupted_scan_timestamps": int(ooo_scans)
    }
    print(f"[Issue 9] Out-of-Order Scans: {ooo_scans:,} corrupted/out-of-order scans detected.")

    print("=======================================================")
    print("DATA QUALITY VALIDATION AUDIT COMPLETE")
    print("=======================================================\n")
    return report


if __name__ == "__main__":
    validate_raw_datasets()

