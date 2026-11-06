"""
Logistics Root-Cause Analysis - Configuration and Constants
Kolkata Freight & Logistics Performance Intelligence
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_REF_DIR = DATA_DIR / "reference"
DATA_PBI_DIR = DATA_DIR / "power_bi_exports"

REPORTS_DIR = PROJECT_ROOT / "reports"
VIS_DIR = REPORTS_DIR / "visualizations"
MEMO_DIR = REPORTS_DIR / "management_memo"
DRIVER_TREE_DIR = REPORTS_DIR / "driver_tree"
DOCS_DIR = PROJECT_ROOT / "documentation"
TESTS_DIR = PROJECT_ROOT / "tests"

DB_PATH = DATA_PROCESSED_DIR / "kolkata_logistics.db"

# Reproducibility
RANDOM_SEED = 42

# Timeframe Configuration
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
BASELINE_START_WEEK = 1
BASELINE_END_WEEK = 26
DECLINE_START_WEEK = 27
DECLINE_END_WEEK = 52
FESTIVAL_START_WEEK = 39  # Durga Puja / Festive peak in Kolkata
FESTIVAL_END_WEEK = 44

# Scale Configuration
TOTAL_SHIPMENTS_TARGET = 350_000
TOTAL_RECORDS_TARGET = 1_500_000

# 12 Kolkata Logistics Hubs
HUBS = {
    "HUB_DKN": {
        "name": "Dankuni Freight Terminal",
        "zone": "Northwest Industrial Corridor",
        "lat": 22.6865,
        "lon": 88.2917,
        "type": "Mega Freight Hub",
        "capacity_per_day": 8500
    },
    "HUB_HWH": {
        "name": "Howrah Logistics Park",
        "zone": "West Rail-Road Junction",
        "lat": 22.5958,
        "lon": 88.2636,
        "type": "Container & Express Hub",
        "capacity_per_day": 7500
    },
    "HUB_TRT": {
        "name": "Taratala Central Hub",
        "zone": "South Kolkata Industrial",
        "lat": 22.5050,
        "lon": 88.3075,
        "type": "Urban Distribution Hub",
        "capacity_per_day": 6500
    },
    "HUB_DHU": {
        "name": "Dhulagarh Truck Terminal",
        "zone": "Southwest NH16 Corridor",
        "lat": 22.5539,
        "lon": 88.1965,
        "type": "Heavy Freight Depot",
        "capacity_per_day": 7000
    },
    "HUB_KSB": {
        "name": "Kasba Regional Depot",
        "zone": "East Kolkata Urban",
        "lat": 22.5168,
        "lon": 88.3846,
        "type": "Retail & Parcel Hub",
        "capacity_per_day": 4500
    },
    "HUB_SLK": {
        "name": "Salt Lake Sector V Hub",
        "zone": "East Kolkata IT Corridor",
        "lat": 22.5769,
        "lon": 88.4339,
        "type": "E-Commerce Tech Depot",
        "capacity_per_day": 5500
    },
    "HUB_ALP": {
        "name": "Alipore West Terminal",
        "zone": "Central South Gateway",
        "lat": 22.5280,
        "lon": 88.3240,
        "type": "Commercial Freight Depot",
        "capacity_per_day": 4000
    },
    "HUB_BST": {
        "name": "Barasat North Gateway",
        "zone": "North 24 Parganas Arterial",
        "lat": 22.7214,
        "lon": 88.4816,
        "type": "Regional Gateway",
        "capacity_per_day": 4500
    },
    "HUB_KLY": {
        "name": "Kalyani Industrial Depot",
        "zone": "Nadia Industrial Link",
        "lat": 22.9751,
        "lon": 88.4345,
        "type": "Bulk Storage & Transit",
        "capacity_per_day": 4000
    },
    "HUB_HLD": {
        "name": "Haldia Port Feeder Depot",
        "zone": "South Coastal Link",
        "lat": 22.0644,
        "lon": 88.0700,
        "type": "Port Container Link",
        "capacity_per_day": 5000
    },
    "HUB_KNA": {
        "name": "Kona Expressway Transit Hub",
        "zone": "West Highway Corridor",
        "lat": 22.6100,
        "lon": 88.2900,
        "type": "Transit Cross-Dock",
        "capacity_per_day": 6000
    },
    "HUB_CCU": {
        "name": "Central Kolkata Sealdah Hub",
        "zone": "Urban Core Central",
        "lat": 22.5697,
        "lon": 88.3697,
        "type": "Urban Consolidation Center",
        "capacity_per_day": 5000
    }
}

# Network Renaming Reference (Introduced in raw data)
HUB_RENAMING_MAPPING = [
    {
        "old_hub_id": "HUB_KNA",
        "old_hub_name": "Kona Expressway Transit Hub",
        "new_hub_id": "HUB_KEX",
        "new_hub_name": "Kona Express Highway Logistics Center",
        "effective_date": "2024-07-01",
        "mapping_status": "Active"
    },
    {
        "old_hub_id": "HUB_SLK",
        "old_hub_name": "Salt Lake Sector V Hub",
        "new_hub_id": "HUB_NWN",
        "new_hub_name": "New Town Rajarhat E-Commerce Terminal",
        "effective_date": "2024-07-01",
        "mapping_status": "Active"
    },
    {
        "old_hub_id": "HUB_HLD_PORT",
        "old_hub_name": "Haldia Port Feeder Depot Old",
        "new_hub_id": "HUB_HLD",
        "new_hub_name": "Haldia Port Feeder Depot",
        "effective_date": "2024-04-01",
        "mapping_status": "Active"
    },
    {
        "old_hub_id": "HUB_DKN",
        "old_hub_name": "Dankuni Freight Terminal",
        "new_hub_id": "HUB_DKN",
        "new_hub_name": "Dankuni Multi-Modal Freight Terminal",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_HWH",
        "old_hub_name": "Howrah Logistics Park",
        "new_hub_id": "HUB_HWH",
        "new_hub_name": "Howrah Integrated Logistics Park",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_TRT",
        "old_hub_name": "Taratala Central Hub",
        "new_hub_id": "HUB_TRT",
        "new_hub_name": "Taratala Industrial Logistics Hub",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_DHU",
        "old_hub_name": "Dhulagarh Truck Terminal",
        "new_hub_id": "HUB_DHU",
        "new_hub_name": "Dhulagarh Heavy Freight Terminal",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_KSB",
        "old_hub_name": "Kasba Regional Depot",
        "new_hub_id": "HUB_KSB",
        "new_hub_name": "Kasba Regional Distribution Depot",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_ALP",
        "old_hub_name": "Alipore West Terminal",
        "new_hub_id": "HUB_ALP",
        "new_hub_name": "Alipore Central West Terminal",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_BST",
        "old_hub_name": "Barasat North Gateway",
        "new_hub_id": "HUB_BST",
        "new_hub_name": "Barasat North Freight Gateway",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_KLY",
        "old_hub_name": "Kalyani Industrial Depot",
        "new_hub_id": "HUB_KLY",
        "new_hub_name": "Kalyani Bulk Industrial Depot",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    },
    {
        "old_hub_id": "HUB_CCU",
        "old_hub_name": "Central Kolkata Sealdah Hub",
        "new_hub_id": "HUB_CCU",
        "new_hub_name": "Kolkata Central Rail-Road Depot",
        "effective_date": "2024-01-01",
        "mapping_status": "Unchanged"
    }
]

# Vehicle Types and Specifications
VEHICLE_TYPES = {
    "32ft Multi-Axle Truck": {"capacity_kg": 18000, "count": 250, "avg_speed_kmh": 32},
    "20ft Container Truck": {"capacity_kg": 9000, "count": 400, "avg_speed_kmh": 36},
    "14ft LCV": {"capacity_kg": 4000, "count": 450, "avg_speed_kmh": 40},
    "Tata Ace / Mini Truck": {"capacity_kg": 1200, "count": 300, "avg_speed_kmh": 45}
}

# Product Categories
PRODUCT_CATEGORIES = [
    "Industrial Machinery & Spares",
    "FMCG & Packaged Goods",
    "Consumer Electronics",
    "Apparel & Textiles",
    "Chemicals & Raw Materials",
    "Pharmaceuticals"
]

# Service Types
SERVICE_TYPES = [
    "Standard Surface",
    "Express Cargo",
    "Same Day Express"
]

# Customer Segments
CUSTOMER_SEGMENTS = [
    "Enterprise B2B",
    "SME Industrial",
    "E-Commerce Marketplace",
    "Retail Distribution"
]

# Scan Event Types
SCAN_EVENTS = [
    "ORIGIN_PICKUP_SCAN",
    "ORIGIN_SORT_SCAN",
    "DISPATCH_SCAN",
    "TRANSIT_INTERMEDIATE_SCAN",
    "DESTINATION_ARRIVAL_SCAN",
    "OUT_FOR_DELIVERY_SCAN",
    "DELIVERY_CONFIRMATION_SCAN"
]

# Data Quality Injection Rates
DQ_ISSUE_RATES = {
    "duplicate_shipments": 0.015,
    "duplicate_scans": 0.020,
    "missing_delivery_timestamp": 0.018,
    "legacy_hub_id": 0.045,
    "out_of_order_scans": 0.025,
    "dirty_timezone": 0.080,
    "invalid_timestamps": 0.007,
    "inconsistent_categories": 0.050,
    "referential_integrity_orphans": 0.008,
    "dirty_numeric_types": 0.060
}

# Headline Metric
HEADLINE_METRIC = "On-Time Delivery Rate (OTD)"
OTD_TARGET_PERCENT = 85.0
BASELINE_OTD_BENCHMARK = 86.4
DECLINE_OTD_BENCHMARK = 73.6

