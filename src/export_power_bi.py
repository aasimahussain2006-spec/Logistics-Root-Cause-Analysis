"""
Logistics Root-Cause Analysis - Power BI Star Schema Exporter
Exports Star Schema CSV tables into data/power_bi_exports/ for direct ingestion into Power BI.
"""

import os
import pandas as pd
import numpy as np
from src.config import DATA_PBI_DIR, DATA_PROCESSED_DIR, DATA_REF_DIR
from src.database import LogisticsDatabase


def export_star_schema_tables():
    """Generates all Fact and Dimension tables for the Power BI Star Schema."""
    print("\n=======================================================")
    print("EXPORTING POWER BI STAR SCHEMA TABLES")
    print("=======================================================")
    os.makedirs(DATA_PBI_DIR, exist_ok=True)
    db = LogisticsDatabase()

    # 1. DimDate
    print("Generating DimDate.csv...")
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    df_date = pd.DataFrame({
        "DateKey": dates.strftime("%Y-%m-%d"),
        "FullDate": dates,
        "Year": dates.year,
        "Quarter": "Q" + dates.quarter.astype(str),
        "Month": dates.month,
        "MonthName": dates.strftime("%B"),
        "WeekNumber": dates.isocalendar().week.astype(int),
        "DayOfWeek": dates.day_name(),
        "IsWeekend": dates.weekday.isin([5, 6]).astype(int),
        "IsFestiveSeason": ((dates.isocalendar().week >= 39) & (dates.isocalendar().week <= 44)).astype(int)
    })
    df_date.to_csv(DATA_PBI_DIR / "DimDate.csv", index=False)

    # 2. DimHub
    print("Generating DimHub.csv...")
    df_hubs = pd.read_csv(DATA_REF_DIR / "hubs.csv")
    df_hubs.rename(columns={
        "hub_id": "HubID",
        "hub_name": "HubName",
        "zone": "GeographicZone",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "hub_type": "FacilityType",
        "capacity_per_day": "DailyThroughputCapacity"
    }, inplace=True)
    df_hubs.to_csv(DATA_PBI_DIR / "DimHub.csv", index=False)

    # 3. DimRoute
    print("Generating DimRoute.csv...")
    df_routes = pd.read_csv(DATA_REF_DIR / "routes.csv")
    df_routes.rename(columns={
        "route_id": "RouteID",
        "origin_hub_id": "OriginHubID",
        "destination_hub_id": "DestinationHubID",
        "distance_km": "DistanceKM",
        "planned_transit_hours": "PlannedTransitHours",
        "route_category": "RouteCategory",
        "toll_plazas": "TollPlazaCount"
    }, inplace=True)
    df_routes.to_csv(DATA_PBI_DIR / "DimRoute.csv", index=False)

    # 4. DimVehicle
    print("Generating DimVehicle.csv...")
    df_veh = pd.read_csv(DATA_REF_DIR / "vehicles.csv")
    df_veh.rename(columns={
        "vehicle_id": "VehicleID",
        "vehicle_type": "VehicleType",
        "capacity": "CapacityKG",
        "maintenance_date": "LastMaintenanceDate",
        "downtime_hours": "DowntimeHours",
        "breakdown_count": "BreakdownCount",
        "availability_status": "AvailabilityStatus",
        "is_aging_fleet": "IsAgingFleet"
    }, inplace=True)
    df_veh.to_csv(DATA_PBI_DIR / "DimVehicle.csv", index=False)

    # 5. DimCustomer
    print("Generating DimCustomer.csv...")
    df_cust = pd.read_csv(DATA_REF_DIR / "customers.csv")
    df_cust.rename(columns={
        "customer_id": "CustomerID",
        "customer_name": "CustomerName",
        "customer_segment": "CustomerSegment",
        "contract_tier": "ContractTier",
        "credit_terms_days": "CreditTermsDays"
    }, inplace=True)
    df_cust.to_csv(DATA_PBI_DIR / "DimCustomer.csv", index=False)

    # 6. DimService
    print("Generating DimService.csv...")
    df_service = pd.DataFrame([
        {"ServiceType": "Standard Surface", "SLAWindowHours": "24-48 Hours", "SpeedTier": "Standard"},
        {"ServiceType": "Express Cargo", "SLAWindowHours": "12-24 Hours", "SpeedTier": "High Speed"},
        {"ServiceType": "Same Day Express", "SLAWindowHours": "6-10 Hours", "SpeedTier": "Critical Express"}
    ])
    df_service.to_csv(DATA_PBI_DIR / "DimService.csv", index=False)

    # 7. FactShipments
    print("Generating FactShipments.csv...")
    sql_ship = """
    SELECT 
        shipment_id AS ShipmentID,
        customer_id AS CustomerID,
        origin_hub_id AS OriginHubID,
        destination_hub_id AS DestinationHubID,
        route_id AS RouteID,
        vehicle_id AS VehicleID,
        service_type AS ServiceType,
        shipment_date AS DateKey,
        dispatch_timestamp AS DispatchTimestamp,
        promised_delivery_timestamp AS PromisedDeliveryTimestamp,
        actual_delivery_timestamp AS ActualDeliveryTimestamp,
        shipment_status AS ShipmentStatus,
        product_category AS ProductCategory,
        shipment_weight_kg AS ShipmentWeightKG,
        shipping_cost_inr AS ShippingCostINR,
        on_time_flag AS OnTimeFlag,
        is_delayed AS IsDelayed,
        delay_hours AS DelayHours,
        quarter AS Quarter,
        year_week AS WeekNumber,
        is_decline_period AS IsDeclinePeriod,
        is_festival_season AS IsFestivalSeason
    FROM fact_shipments;
    """
    df_ship_pbi = db.run_query(sql_ship)
    df_ship_pbi.to_csv(DATA_PBI_DIR / "FactShipments.csv", index=False)
    print(f"  - FactShipments.csv exported: {len(df_ship_pbi):,} rows")

    # 8. FactWarehouseScans (Sample or aggregate for fast import)
    print("Generating FactWarehouseScans.csv...")
    sql_scans = """
    SELECT 
        scan_id AS ScanID,
        shipment_id AS ShipmentID,
        hub_id AS HubID,
        scan_event AS ScanEvent,
        scan_timestamp AS ScanTimestamp,
        scan_status AS ScanStatus,
        processing_duration_minutes AS ProcessingDurationMinutes
    FROM fact_warehouse_scans;
    """
    df_scans_pbi = db.run_query(sql_scans)
    df_scans_pbi.to_csv(DATA_PBI_DIR / "FactWarehouseScans.csv", index=False)
    print(f"  - FactWarehouseScans.csv exported: {len(df_scans_pbi):,} rows")

    print("=======================================================")
    print("POWER BI STAR SCHEMA EXPORT COMPLETE")
    print(f"Path: {DATA_PBI_DIR}")
    print("=======================================================\n")


if __name__ == "__main__":
    export_star_schema_tables()

