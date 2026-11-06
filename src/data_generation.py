"""
Logistics Root-Cause Analysis - Synthetic Data Generation Engine
Generates ~1.5 million interconnected records across Shipments, Routes, Vehicles, and Warehouse Scans
with controlled, auditable data quality anomalies.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from src.config import (
    RANDOM_SEED,
    DATA_RAW_DIR,
    DATA_REF_DIR,
    HUBS,
    HUB_RENAMING_MAPPING,
    VEHICLE_TYPES,
    PRODUCT_CATEGORIES,
    SERVICE_TYPES,
    CUSTOMER_SEGMENTS,
    TOTAL_SHIPMENTS_TARGET
)


def set_seed(seed=RANDOM_SEED):
    """Ensure complete reproducibility across random generators."""
    random.seed(seed)
    np.random.seed(seed)


def generate_reference_data():
    """Generates Hubs, Hub Mapping, Routes, Vehicles, and Customers."""
    print("[1/5] Generating reference datasets...")
    os.makedirs(DATA_REF_DIR, exist_ok=True)
    os.makedirs(DATA_RAW_DIR, exist_ok=True)

    # 1. Hubs Reference
    hubs_data = []
    for hub_id, info in HUBS.items():
        hubs_data.append({
            "hub_id": hub_id,
            "hub_name": info["name"],
            "zone": info["zone"],
            "latitude": info["lat"],
            "longitude": info["lon"],
            "hub_type": info["type"],
            "capacity_per_day": info["capacity_per_day"]
        })
    df_hubs = pd.DataFrame(hubs_data)
    df_hubs.to_csv(DATA_REF_DIR / "hubs.csv", index=False)

    # 2. Hub Renaming Mapping
    df_hub_mapping = pd.DataFrame(HUB_RENAMING_MAPPING)
    df_hub_mapping.to_csv(DATA_REF_DIR / "hub_mapping.csv", index=False)

    # 3. Routes Master (All directed pairs of the 12 hubs: 12 * 11 = 132 routes)
    hub_ids = list(HUBS.keys())
    routes_data = []
    for orig in hub_ids:
        for dest in hub_ids:
            if orig == dest:
                continue
            r_id = f"R_{orig.replace('HUB_', '')}_{dest.replace('HUB_', '')}"
            
            # Coordinate distance calculation
            lat1, lon1 = HUBS[orig]["lat"], HUBS[orig]["lon"]
            lat2, lon2 = HUBS[dest]["lat"], HUBS[dest]["lon"]
            # Rough Euclidean to approx road distance in km for Kolkata region
            d_lat = (lat2 - lat1) * 111.0
            d_lon = (lon2 - lon1) * 102.0
            dist_km = round(np.sqrt(d_lat**2 + d_lon**2) * 1.35 + np.random.uniform(5.0, 15.0), 1)
            dist_km = max(12.0, dist_km)

            # Planned transit hours based on distance and city terrain
            planned_hours = round(dist_km / np.random.uniform(22.0, 32.0), 2)
            planned_hours = max(0.75, planned_hours)

            # Route category based on corridor function
            if any("HLD" in x for x in [orig, dest]):
                category = "Industrial Bypass / Port Link"
            elif any(k in x for x in [orig, dest] for k in ["DKN", "HWH", "KNA", "KEX"]):
                category = "Arterial Highway (NH16/Kona)"
            elif any(k in x for x in [orig, dest] for k in ["CCU", "TRT", "ALP"]):
                category = "Urban Core Arterial"
            else:
                category = "Suburban Corridor"

            routes_data.append({
                "route_id": r_id,
                "origin_hub_id": orig,
                "destination_hub_id": dest,
                "distance_km": dist_km,
                "planned_transit_hours": planned_hours,
                "route_category": category,
                "toll_plazas": 1 if dist_km > 35 else 0
            })
    df_routes = pd.DataFrame(routes_data)
    df_routes.to_csv(DATA_REF_DIR / "routes.csv", index=False)
    # Also save raw copy
    df_routes.to_csv(DATA_RAW_DIR / "raw_routes.csv", index=False)

    # 4. Vehicles Master (1,400 vehicles across 4 types)
    vehicles_data = []
    v_counter = 1
    for v_type, spec in VEHICLE_TYPES.items():
        count = spec["count"]
        for _ in range(count):
            v_id = f"VEH_{v_counter:04d}"
            # Maintenance date distributed throughout the year
            maint_day = np.random.randint(1, 365)
            maint_date = (datetime(2024, 1, 1) + timedelta(days=maint_day)).strftime("%Y-%m-%d")
            
            # Baseline vs aging vehicles
            is_aging = (v_counter % 5 == 0)
            breakdown_cnt = np.random.poisson(3.5 if is_aging else 0.8)
            downtime_hrs = round(breakdown_cnt * np.random.uniform(8.0, 24.0) + (15.0 if is_aging else 2.0), 1)
            
            status = "Breakdown" if breakdown_cnt >= 5 and downtime_hrs > 60 else ("Maintenance" if downtime_hrs > 40 else "Active")

            vehicles_data.append({
                "vehicle_id": v_id,
                "vehicle_type": v_type,
                "capacity": spec["capacity_kg"],
                "maintenance_date": maint_date,
                "downtime_hours": downtime_hrs,
                "breakdown_count": breakdown_cnt,
                "availability_status": status,
                "is_aging_fleet": 1 if is_aging else 0
            })
            v_counter += 1
    df_vehicles = pd.DataFrame(vehicles_data)
    df_vehicles.to_csv(DATA_REF_DIR / "vehicles.csv", index=False)
    df_vehicles.to_csv(DATA_RAW_DIR / "raw_vehicles.csv", index=False)

    # 5. Customers Master (3,000 business accounts)
    customers_data = []
    for c_idx in range(1, 3001):
        c_id = f"CUST_{c_idx:05d}"
        seg = np.random.choice(CUSTOMER_SEGMENTS, p=[0.25, 0.35, 0.25, 0.15])
        tier = "Gold" if seg == "Enterprise B2B" else np.random.choice(["Silver", "Bronze", "Standard"])
        customers_data.append({
            "customer_id": c_id,
            "customer_name": f"Kolkata Freight Client {c_idx:04d}",
            "customer_segment": seg,
            "contract_tier": tier,
            "credit_terms_days": np.random.choice([15, 30, 45, 60])
        })
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_csv(DATA_REF_DIR / "customers.csv", index=False)

    print(f"Reference datasets created: {len(df_hubs)} hubs, {len(df_routes)} routes, {len(df_vehicles)} vehicles, {len(df_customers)} customers.")
    return df_hubs, df_hub_mapping, df_routes, df_vehicles, df_customers


def generate_shipments_and_scans(n_shipments=TOTAL_SHIPMENTS_TARGET):
    """
    Vectorized generation of ~350,000 shipments and ~1,150,000 warehouse scans
    simulating operational decline in Q3-Q4 and realistic anomalies.
    """
    print(f"[2/5] Generating {n_shipments:,} shipments with operational variation...")
    set_seed(RANDOM_SEED)

    # Load reference files
    df_routes = pd.read_csv(DATA_REF_DIR / "routes.csv")
    df_vehicles = pd.read_csv(DATA_REF_DIR / "vehicles.csv")
    df_customers = pd.read_csv(DATA_REF_DIR / "customers.csv")
    route_ids = df_routes["route_id"].values
    route_origins = df_routes.set_index("route_id")["origin_hub_id"].to_dict()
    route_dests = df_routes.set_index("route_id")["destination_hub_id"].to_dict()
    route_planned_hrs = df_routes.set_index("route_id")["planned_transit_hours"].to_dict()
    route_categories = df_routes.set_index("route_id")["route_category"].to_dict()
    vehicle_ids = df_vehicles["vehicle_id"].values
    vehicle_types = df_vehicles.set_index("vehicle_id")["vehicle_type"].to_dict()
    aging_vehicles = set(df_vehicles[df_vehicles["is_aging_fleet"] == 1]["vehicle_id"].values)
    customer_ids = df_customers["customer_id"].values
    customer_segments = df_customers.set_index("customer_id")["customer_segment"].to_dict()

    # Generate dates across 52 weeks (365 days)
    # Give festival season (weeks 39-44 / days 266-308) a +45% volume surge
    days = np.arange(0, 365)
    day_weights = np.ones(365)
    # Seasonal surge in Bengal autumn (Durga Puja festival)
    day_weights[266:308] *= 1.45
    # Slight weekly pattern (lower Sunday volume)
    for d in days:
        dt = datetime(2024, 1, 1) + timedelta(days=int(d))
        if dt.weekday() == 6:  # Sunday
            day_weights[d] *= 0.65
        elif dt.weekday() in [0, 1]:  # Monday/Tuesday dispatch rush
            day_weights[d] *= 1.15
    day_weights /= day_weights.sum()

    chosen_day_offsets = np.random.choice(days, size=n_shipments, p=day_weights)
    start_dt = datetime(2024, 1, 1, 6, 0, 0)
    
    # Minute offsets within the day (log-normal dispatch during business hours)
    dispatch_hour = np.random.beta(2, 2, size=n_shipments) * 14 + 6  # 6 AM to 8 PM
    shipment_datetimes = [
        start_dt + timedelta(days=int(d), hours=float(h), minutes=int(np.random.randint(0, 60)))
        for d, h in zip(chosen_day_offsets, dispatch_hour)
    ]

    # Service Types with mix shift in decline period
    # Baseline: 70% Standard, 22% Express, 8% Same Day
    # Decline: 52% Standard, 32% Express, 16% Same Day (mix shift puts pressure on SLAs!)
    is_decline_period = np.array([dt.month >= 7 for dt in shipment_datetimes])
    
    service_type_choices = []
    for is_dec in is_decline_period:
        if is_dec:
            st = np.random.choice(SERVICE_TYPES, p=[0.52, 0.32, 0.16])
        else:
            st = np.random.choice(SERVICE_TYPES, p=[0.70, 0.22, 0.08])
        service_type_choices.append(st)
    service_types_arr = np.array(service_type_choices)

    # Routes assignment
    chosen_routes = np.random.choice(route_ids, size=n_shipments)
    origins = [route_origins[r] for r in chosen_routes]
    destinations = [route_dests[r] for r in chosen_routes]
    planned_hrs_arr = np.array([route_planned_hrs[r] for r in chosen_routes])
    
    # Vehicles assignment
    chosen_vehicles = np.random.choice(vehicle_ids, size=n_shipments)
    chosen_customers = np.random.choice(customer_ids, size=n_shipments)
    chosen_categories = np.random.choice(PRODUCT_CATEGORIES, size=n_shipments)

    # Weights and costs
    weights = np.round(np.random.lognormal(mean=4.2, sigma=0.8, size=n_shipments), 1)
    weights = np.clip(weights, 2.5, 17500.0)
    base_cost = weights * 1.8 + planned_hrs_arr * 120.0 + np.random.uniform(150, 400, size=n_shipments)
    # Service premium
    cost_multiplier = np.where(service_types_arr == "Same Day Express", 2.2,
                      np.where(service_types_arr == "Express Cargo", 1.5, 1.0))
    shipping_costs = np.round(base_cost * cost_multiplier, 2)

    # Realistic Promised Delivery Window (SLA) calibrated to ~86.4% baseline OTD
    sla_buffer = np.where(service_types_arr == "Same Day Express", np.random.uniform(1.2, 2.2, size=n_shipments),
                 np.where(service_types_arr == "Express Cargo", np.random.uniform(2.2, 3.8, size=n_shipments),
                          np.random.uniform(4.2, 6.8, size=n_shipments)))
    promised_sla_hours = planned_hrs_arr + sla_buffer

    # Baseline Handling and Transit Duration
    base_handling_hours = np.random.uniform(1.2, 2.2, size=n_shipments)
    actual_transit_hrs = planned_hrs_arr * np.random.lognormal(mean=0.04, sigma=0.18, size=n_shipments)

    # In Baseline period (H1), slight natural operational friction gives ~86.5% OTD
    baseline_friction = np.random.exponential(scale=0.42, size=n_shipments)

    # 2. Root Cause 1: Route Inefficiencies & Highway Bottlenecks in Decline period (Q3-Q4)
    # Kona Expressway (KNA/KEX) & Dankuni (DKN) corridors undergo heavy bridge repairs & diversions
    route_delay_hours = np.zeros(n_shipments)
    for i, (is_dec, orig, dest) in enumerate(zip(is_decline_period, origins, destinations)):
        if is_dec and any(k in [orig, dest] for k in ["HUB_DKN", "HUB_KNA", "HUB_HWH", "HUB_KEX"]):
            if np.random.rand() < 0.38:
                route_delay_hours[i] = np.random.exponential(scale=2.8)

    # 3. Root Cause 2: Vehicle Downtime & Breakdowns
    # Aging fleet in Q3-Q4 suffers frequent roadside breakdowns
    vehicle_delay_hours = np.zeros(n_shipments)
    for i, (is_dec, v_id) in enumerate(zip(is_decline_period, chosen_vehicles)):
        if is_dec and (v_id in aging_vehicles):
            if np.random.rand() < 0.25:
                vehicle_delay_hours[i] = np.random.uniform(3.2, 7.5)

    # 4. Root Cause 3 & 4: Warehouse Processing Bottlenecks at Dhulagarh (HUB_DHU) & Taratala (HUB_TRT)
    # Sorting conveyor failures and staffing crunches cause huge delays in decline period
    warehouse_delay_hours = np.zeros(n_shipments)
    for i, (is_dec, orig, dest) in enumerate(zip(is_decline_period, origins, destinations)):
        if is_dec:
            if "HUB_DHU" in [orig, dest]:
                if np.random.rand() < 0.44:
                    warehouse_delay_hours[i] += np.random.exponential(scale=3.2)
            if "HUB_TRT" in [orig, dest]:
                if np.random.rand() < 0.38:
                    warehouse_delay_hours[i] += np.random.exponential(scale=2.8)

    # 5. Root Cause 6: Festive Surge Volume Impact (Weeks 39 to 44)
    festive_delay_hours = np.zeros(n_shipments)
    for i, dt in enumerate(shipment_datetimes):
        week_num = dt.isocalendar()[1]
        if 39 <= week_num <= 44:
            if np.random.rand() < 0.30:
                festive_delay_hours[i] = np.random.exponential(scale=2.2)

    # Total Operational Duration
    total_elapsed_hours = (
        actual_transit_hrs
        + base_handling_hours
        + baseline_friction
        + route_delay_hours
        + vehicle_delay_hours
        + warehouse_delay_hours
        + festive_delay_hours
    )

    # Generate Delivery Timestamps
    promised_delivery_dt = [
        s_dt + timedelta(hours=float(sla))
        for s_dt, sla in zip(shipment_datetimes, promised_sla_hours)
    ]
    actual_delivery_dt = [
        s_dt + timedelta(hours=float(el))
        for s_dt, el in zip(shipment_datetimes, total_elapsed_hours)
    ]

    # Status: Delivered, In-Transit, Delayed
    on_time = np.array([act <= prom for act, prom in zip(actual_delivery_dt, promised_delivery_dt)])
    
    # Calculate baseline vs decline OTD to verify mechanics
    baseline_mask = ~is_decline_period
    decline_mask = is_decline_period
    baseline_otd = on_time[baseline_mask].mean() * 100
    decline_otd = on_time[decline_mask].mean() * 100
    print(f"Generated Ground Truth: Baseline OTD = {baseline_otd:.2f}%, Decline OTD = {decline_otd:.2f}% (Drop: {decline_otd - baseline_otd:.2f} pp)")

    # Prepare Clean Shipment Dataframe
    shipment_ids = [f"SHP_{i:07d}" for i in range(1, n_shipments + 1)]
    df_clean_shipments = pd.DataFrame({
        "shipment_id": shipment_ids,
        "customer_id": chosen_customers,
        "origin_hub_id": origins,
        "destination_hub_id": destinations,
        "route_id": chosen_routes,
        "vehicle_id": chosen_vehicles,
        "shipment_date": [dt.strftime("%Y-%m-%d") for dt in shipment_datetimes],
        "dispatch_timestamp": [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in shipment_datetimes],
        "promised_delivery_timestamp": [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in promised_delivery_dt],
        "actual_delivery_timestamp": [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in actual_delivery_dt],
        "shipment_status": ["Delivered" if ot else "Delayed" for ot in on_time],
        "product_category": chosen_categories,
        "service_type": service_types_arr,
        "shipment_weight_kg": weights,
        "shipping_cost_inr": shipping_costs,
        "on_time_flag": on_time.astype(int),
        "total_delay_hours": np.maximum(0.0, np.round((total_elapsed_hours - promised_sla_hours), 2)),
        "route_delay_hours": np.round(route_delay_hours, 2),
        "vehicle_delay_hours": np.round(vehicle_delay_hours, 2),
        "warehouse_delay_hours": np.round(warehouse_delay_hours, 2),
        "festive_delay_hours": np.round(festive_delay_hours, 2)
    })

    # Save Ground Truth for Verification & Drivers
    df_clean_shipments.to_csv(DATA_REF_DIR / "ground_truth_shipments.csv", index=False)

    # -------------------------------------------------------------
    # [3/5] Generate Warehouse Scans (~1.15 Million Scan Records)
    # -------------------------------------------------------------
    print("[3/5] Generating ~1,150,000 warehouse scan records across lifecycle stages...")
    scan_rows = []
    scan_id_counter = 1

    # To optimize memory during generation, iterate in chunks or vectorized lists
    # Each shipment gets 3-4 scans:
    # 1. ORIGIN_SORT_SCAN (at origin hub)
    # 2. DISPATCH_SCAN (at origin hub)
    # 3. DESTINATION_ARRIVAL_SCAN (at destination hub)
    # 4. DELIVERY_CONFIRMATION_SCAN (at destination/final)
    
    # Process scan generation vectorized
    n_scans_approx = n_shipments * 3.3
    scan_shp_ids = []
    scan_hubs = []
    scan_events = []
    scan_timestamps = []
    scan_statuses = []
    scan_durations = []

    for i in range(n_shipments):
        s_id = shipment_ids[i]
        orig = origins[i]
        dest = destinations[i]
        s_dt = shipment_datetimes[i]
        wh_delay = warehouse_delay_hours[i]
        act_dt = actual_delivery_dt[i]

        # 1. Origin Sort
        sort_duration = round(float(np.random.gamma(shape=3.0, scale=12.0) + wh_delay * 35.0), 1)
        sort_ts = s_dt - timedelta(minutes=int(sort_duration))
        scan_shp_ids.append(s_id)
        scan_hubs.append(orig)
        scan_events.append("ORIGIN_SORT_SCAN")
        scan_timestamps.append(sort_ts.strftime("%Y-%m-%d %H:%M:%S"))
        scan_statuses.append("Success" if wh_delay < 3.0 else "Backlog Exception")
        scan_durations.append(sort_duration)

        # 2. Dispatch
        scan_shp_ids.append(s_id)
        scan_hubs.append(orig)
        scan_events.append("DISPATCH_SCAN")
        scan_timestamps.append(s_dt.strftime("%Y-%m-%d %H:%M:%S"))
        scan_statuses.append("Success")
        scan_durations.append(15.0)

        # 3. Destination Arrival
        arr_ts = act_dt - timedelta(minutes=int(np.random.uniform(45, 180)))
        scan_shp_ids.append(s_id)
        scan_hubs.append(dest)
        scan_events.append("DESTINATION_ARRIVAL_SCAN")
        scan_timestamps.append(arr_ts.strftime("%Y-%m-%d %H:%M:%S"))
        scan_statuses.append("Success")
        scan_durations.append(round(float(np.random.uniform(25.0, 90.0)), 1))

        # 4. Delivery confirmation for 35% of records (additional scan)
        if i % 3 == 0:
            scan_shp_ids.append(s_id)
            scan_hubs.append(dest)
            scan_events.append("DELIVERY_CONFIRMATION_SCAN")
            scan_timestamps.append(act_dt.strftime("%Y-%m-%d %H:%M:%S"))
            scan_statuses.append("Delivered")
            scan_durations.append(10.0)

    scan_ids = [f"SCN_{k:08d}" for k in range(1, len(scan_shp_ids) + 1)]
    df_clean_scans = pd.DataFrame({
        "scan_id": scan_ids,
        "shipment_id": scan_shp_ids,
        "hub_id": scan_hubs,
        "scan_event": scan_events,
        "scan_timestamp": scan_timestamps,
        "scan_status": scan_statuses,
        "processing_duration_minutes": scan_durations
    })
    print(f"Generated {len(df_clean_scans):,} warehouse scan records.")

    # -------------------------------------------------------------
    # [4/5] Inject Controlled Data Quality Anomalies into Raw Data
    # -------------------------------------------------------------
    print("[4/5] Injecting controlled data quality issues into raw datasets...")
    
    # Copy for raw corruption
    df_raw_shipments = df_clean_shipments.copy()
    df_raw_scans = df_clean_scans.copy()

    # Drop ground truth helper columns from raw shipments
    df_raw_shipments = df_raw_shipments.drop(columns=[
        "on_time_flag", "total_delay_hours", "route_delay_hours", 
        "vehicle_delay_hours", "warehouse_delay_hours", "festive_delay_hours"
    ])

    # Issue 1: Duplicate Shipments (~1.5%)
    n_dup_ship = int(n_shipments * 0.015)
    dup_ship_idx = np.random.choice(len(df_raw_shipments), size=n_dup_ship, replace=False)
    df_dup_ship = df_raw_shipments.iloc[dup_ship_idx].copy()
    df_raw_shipments = pd.concat([df_raw_shipments, df_dup_ship], ignore_index=True)
    print(f"  - Injected {n_dup_ship:,} duplicate shipment records.")

    # Issue 2: Duplicate Scans (~2.0%)
    n_dup_scans = int(len(df_raw_scans) * 0.02)
    dup_scan_idx = np.random.choice(len(df_raw_scans), size=n_dup_scans, replace=False)
    df_dup_scans = df_raw_scans.iloc[dup_scan_idx].copy()
    df_raw_scans = pd.concat([df_raw_scans, df_dup_scans], ignore_index=True)
    print(f"  - Injected {n_dup_scans:,} duplicate scan records.")

    # Issue 3: Missing Delivery Timestamps (~1.8%)
    n_miss = int(n_shipments * 0.018)
    miss_idx = np.random.choice(len(df_raw_shipments), size=n_miss, replace=False)
    df_raw_shipments.loc[miss_idx, "actual_delivery_timestamp"] = np.nan
    df_raw_shipments.loc[miss_idx, "shipment_status"] = np.random.choice(["In Transit", "Lost / Investigating", None], size=n_miss)
    print(f"  - Injected {n_miss:,} missing delivery timestamps / lost shipments.")

    # Issue 4: Legacy Hub Mappings following network restructuring (~4.5%)
    # Use HUB_KNA instead of HUB_KEX, HUB_SLK instead of HUB_NWN, HUB_HLD_PORT
    legacy_mask = np.random.rand(len(df_raw_shipments)) < 0.045
    df_raw_shipments.loc[legacy_mask & (df_raw_shipments["origin_hub_id"] == "HUB_KNA"), "origin_hub_id"] = "HUB_KEX_OLD"
    df_raw_shipments.loc[legacy_mask & (df_raw_shipments["destination_hub_id"] == "HUB_SLK"), "destination_hub_id"] = "HUB_SLK_OLD"
    df_raw_shipments.loc[legacy_mask & (df_raw_shipments["origin_hub_id"] == "HUB_HLD"), "origin_hub_id"] = "HUB_HLD_PORT"
    print("  - Injected legacy unmapped hub codes (HUB_KEX_OLD, HUB_SLK_OLD, HUB_HLD_PORT).")

    # Issue 5: Out-of-order Warehouse Scan Events (~2.5%)
    n_ooo = int(len(df_raw_scans) * 0.025)
    ooo_idx = np.random.choice(len(df_raw_scans), size=n_ooo, replace=False)
    # Swap timestamps or add corrupted reversed timestamps
    df_raw_scans.loc[ooo_idx, "scan_timestamp"] = "2024-01-01 00:00:01"
    print(f"  - Injected {n_ooo:,} out-of-order scan timestamps.")

    # Issue 6: Mixed Timezones & Formats (~8.0%)
    tz_mask = np.random.rand(len(df_raw_shipments)) < 0.08
    def corrupt_tz(ts_str):
        if pd.isna(ts_str):
            return ts_str
        choice = random.choice([1, 2, 3])
        if choice == 1:
            return f"{ts_str}+05:30"  # IST explicitly appended
        elif choice == 2:
            return f"{ts_str}Z"       # Marked as UTC
        else:
            return ts_str.replace("-", "/") # Slash format
    df_raw_shipments.loc[tz_mask, "promised_delivery_timestamp"] = df_raw_shipments.loc[tz_mask, "promised_delivery_timestamp"].apply(corrupt_tz)
    print("  - Injected mixed time zones and slash datetime formats.")

    # Issue 7: Invalid Timestamps (~0.7%) (Delivery timestamp earlier than dispatch or future year)
    n_inv = int(n_shipments * 0.007)
    inv_idx = np.random.choice(len(df_raw_shipments), size=n_inv, replace=False)
    df_raw_shipments.loc[inv_idx[:n_inv//2], "actual_delivery_timestamp"] = "2023-11-15 10:00:00" # Delivered before dispatched!
    df_raw_shipments.loc[inv_idx[n_inv//2:], "actual_delivery_timestamp"] = "2099-12-31 23:59:59" # Far future!
    print(f"  - Injected {n_inv:,} invalid delivery timestamps.")

    # Issue 8: Inconsistent Category Labels (~5.0%)
    cat_mask = np.random.rand(len(df_raw_shipments)) < 0.05
    st_mapping = {
        "Standard Surface": "std surface",
        "Express Cargo": "EXP_CARGO",
        "Same Day Express": "same-day"
    }
    df_raw_shipments.loc[cat_mask, "service_type"] = df_raw_shipments.loc[cat_mask, "service_type"].map(st_mapping).fillna(df_raw_shipments.loc[cat_mask, "service_type"])
    print("  - Injected inconsistent casing and abbreviations in service_type.")

    # Issue 9: Referential Integrity Violations (~0.8%)
    n_orphans = int(n_shipments * 0.008)
    orphan_idx = np.random.choice(len(df_raw_shipments), size=n_orphans, replace=False)
    df_raw_shipments.loc[orphan_idx[:n_orphans//2], "vehicle_id"] = "VEH_9999"
    df_raw_shipments.loc[orphan_idx[n_orphans//2:], "route_id"] = "R_UNKNOWN_99"
    print(f"  - Injected {n_orphans:,} orphaned foreign keys (VEH_9999, R_UNKNOWN_99).")

    # Issue 10: Dirty Data Types (Weight as string with "kg", Cost as string with "INR ")
    dt_mask = np.random.rand(len(df_raw_shipments)) < 0.06
    df_raw_shipments["shipment_weight"] = df_raw_shipments["shipment_weight_kg"].astype(str)
    df_raw_shipments.loc[dt_mask, "shipment_weight"] = df_raw_shipments.loc[dt_mask, "shipment_weight"] + " kg"
    
    df_raw_shipments["shipping_cost"] = df_raw_shipments["shipping_cost_inr"].astype(str)
    df_raw_shipments.loc[dt_mask, "shipping_cost"] = "INR " + df_raw_shipments.loc[dt_mask, "shipping_cost"]
    
    df_raw_shipments = df_raw_shipments.drop(columns=["shipment_weight_kg", "shipping_cost_inr"])
    print("  - Injected string suffixes into numeric columns ('kg', 'INR').")

    # -------------------------------------------------------------
    # [5/5] Save Raw Datasets to data/raw/
    # -------------------------------------------------------------
    print("[5/5] Saving raw datasets to disk...")
    raw_shipments_path = DATA_RAW_DIR / "raw_shipments.csv"
    raw_scans_path = DATA_RAW_DIR / "raw_warehouse_scans.csv"

    # Save to CSV
    df_raw_shipments.to_csv(raw_shipments_path, index=False)
    df_raw_scans.to_csv(raw_scans_path, index=False)

    total_records = len(df_raw_shipments) + len(df_raw_scans) + len(df_routes) + len(df_vehicles)
    print(f"\n=======================================================")
    print(f"DATA GENERATION COMPLETE!")
    print(f"Raw Shipments:       {len(df_raw_shipments):,} records")
    print(f"Raw Warehouse Scans: {len(df_raw_scans):,} records")
    print(f"Routes:              {len(df_routes):,} records")
    print(f"Vehicles:            {len(df_vehicles):,} records")
    print(f"Customers:           {len(df_customers):,} records")
    print(f"TOTAL SYSTEM RECORDS: {total_records:,} (Target ~1.5M achieved)")
    print(f"=======================================================\n")

    return {
        "shipments_count": len(df_raw_shipments),
        "scans_count": len(df_raw_scans),
        "routes_count": len(df_routes),
        "vehicles_count": len(df_vehicles),
        "customers_count": len(df_customers),
        "total_records": total_records
    }


if __name__ == "__main__":
    generate_reference_data()
    generate_shipments_and_scans()
