# Comprehensive Data Dictionary: Kolkata Freight Logistics System

> **Data Classification:** Synthetic Operational Freight Records  
> **Total Records Documented:** ~1.5 Million Records across 7 Interconnected Tables

---

## 1. Dataset A: Shipments (`fact_shipments` / `raw_shipments.csv`)

Primary transactional entity capturing freight consignments, promised delivery SLAs, actual fulfillment outcomes, and pricing.

| Column Name | Raw Type | Clean Type | Constraints / Keys | Description & Business Rules | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `shipment_id` | `VARCHAR` | `VARCHAR(30)` | PRIMARY KEY | Unique alphanumeric consignment identifier | `SHP_0001425` |
| `customer_id` | `VARCHAR` | `VARCHAR(20)` | FOREIGN KEY | Client account initiating the freight movement | `CUST_00450` |
| `origin_hub_id` | `VARCHAR` | `VARCHAR(20)` | FOREIGN KEY | Origin dispatch hub in Kolkata metropolitan region | `HUB_DKN` |
| `destination_hub_id` | `VARCHAR` | `VARCHAR(20)` | FOREIGN KEY | Destination receiving hub | `HUB_TRT` |
| `route_id` | `VARCHAR` | `VARCHAR(30)` | FOREIGN KEY | Primary highway transit corridor code | `R_DKN_TRT` |
| `vehicle_id` | `VARCHAR` | `VARCHAR(20)` | FOREIGN KEY | Haulage vehicle assigned to shipment dispatch | `VEH_0214` |
| `shipment_date` | `VARCHAR` | `DATE` | NOT NULL | Calendar date of initial shipment consignment | `2024-03-15` |
| `dispatch_timestamp` | `VARCHAR` | `DATETIME` | NOT NULL (UTC) | Timestamp when truck departed origin hub gate | `2024-03-15 08:30:00` |
| `promised_delivery_timestamp` | `VARCHAR` | `DATETIME` | NOT NULL (UTC) | Contractual customer SLA delivery target time | `2024-03-15 15:45:00` |
| `actual_delivery_timestamp` | `VARCHAR` | `DATETIME` | NULLABLE (UTC) | Physical delivery timestamp confirmed at recipient destination | `2024-03-15 15:10:00` |
| `shipment_status` | `VARCHAR` | `VARCHAR(30)` | Categorical | Final lifecycle status (`Delivered`, `Delayed`, `In Transit`, `Lost`) | `Delivered` |
| `product_category` | `VARCHAR` | `VARCHAR(50)` | Categorical | Freight commodity classification | `FMCG & Packaged Goods` |
| `service_type` | `VARCHAR` | `VARCHAR(50)` | Categorical | Service level tier (`Standard Surface`, `Express Cargo`, `Same Day Express`) | `Standard Surface` |
| `shipment_weight` / `shipment_weight_kg` | `VARCHAR` / `FLOAT` | `REAL` | Value > 0 | Total consignment gross weight in kilograms | `450.5` |
| `shipping_cost` / `shipping_cost_inr` | `VARCHAR` / `FLOAT` | `REAL` | Value > 0 | Freight invoice amount in Indian Rupees (INR) | `3250.00` |
| `on_time_flag` | N/A (Derived) | `INTEGER` | `0` or `1` | 1 if delivered on or before promised timestamp, 0 if delayed | `1` |
| `is_delayed` | N/A (Derived) | `INTEGER` | `0` or `1` | 1 if actual delivery timestamp > promised timestamp | `0` |
| `delay_hours` | N/A (Derived) | `REAL` | $\ge 0.0$ | Number of delayed hours beyond contractual SLA | `0.0` |
| `quarter` | N/A (Derived) | `VARCHAR(5)` | `Q1`, `Q2`, `Q3`, `Q4` | Operating calendar quarter | `Q1` |
| `year_week` | N/A (Derived) | `INTEGER` | 1 to 52 | ISO calendar week number | `11` |
| `is_decline_period` | N/A (Derived) | `INTEGER` | `0` or `1` | 1 if shipment occurred in Q3-Q4 (Weeks 27-52) | `0` |
| `is_festival_season`| N/A (Derived) | `INTEGER` | `0` or `1` | 1 if shipment occurred in Durga Puja peak (Weeks 39-44) | `0` |

---

## 2. Dataset B: Routes (`dim_routes` / `raw_routes.csv`)

Master catalog of 132 directed transit corridors connecting all pairs of the 12 logistics hubs.

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `route_id` | `VARCHAR(30)` | Unique corridor identifier (`R_<ORIGIN>_<DEST>`) | `R_DKN_HWH` |
| `origin_hub_id` | `VARCHAR(20)` | Origin hub foreign key | `HUB_DKN` |
| `destination_hub_id` | `VARCHAR(20)` | Destination hub foreign key | `HUB_HWH` |
| `distance_km` | `REAL` | Road transit distance in kilometers | `28.4` |
| `planned_transit_hours` | `REAL` | Standard benchmark transit duration under normal conditions | `1.15` |
| `route_category` | `VARCHAR(50)` | Corridor classification (`Arterial Highway`, `Urban Core`, `Port Link`) | `Arterial Highway (NH16/Kona)` |
| `toll_plazas` | `INTEGER` | Number of automated toll plazas on corridor | `1` |

---

## 3. Dataset C: Vehicles (`dim_vehicles` / `raw_vehicles.csv`)

Fleet asset registry tracking vehicle specifications, maintenance logs, downtime, and operational availability.

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `vehicle_id` | `VARCHAR(20)` | Unique commercial vehicle registration code | `VEH_0045` |
| `vehicle_type` | `VARCHAR(50)` | Vehicle class (`32ft Multi-Axle`, `20ft Container`, `14ft LCV`, `Tata Ace`) | `32ft Multi-Axle Truck` |
| `capacity_kg` | `INTEGER` | Maximum gross payload capacity in kilograms | `18000` |
| `maintenance_date` | `DATE` | Most recent scheduled depot maintenance date | `2024-05-18` |
| `downtime_hours` | `REAL` | Cumulative mechanical downtime logged in hours | `18.5` |
| `breakdown_count` | `INTEGER` | Total number of unscheduled roadside mechanical breakdowns | `2` |
| `availability_status` | `VARCHAR(30)` | Current fleet state (`Active`, `Maintenance`, `Breakdown`) | `Active` |
| `is_aging_fleet` | `INTEGER` | Indicator flag (1 if vehicle is in >5-year aging subset) | `0` |

---

## 4. Dataset D: Warehouse Scans (`fact_warehouse_scans` / `raw_warehouse_scans.csv`)

Granular item-level barcode and RFID scan events tracking consignments across terminal sorting lines.

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `scan_id` | `VARCHAR(30)` | Unique barcode scan transaction identifier | `SCN_00125489` |
| `shipment_id` | `VARCHAR(30)` | Associated consignment foreign key | `SHP_0001425` |
| `hub_id` | `VARCHAR(20)` | Logistics facility where scan was recorded | `HUB_DKN` |
| `scan_event` | `VARCHAR(50)` | Scan stage (`ORIGIN_SORT`, `DISPATCH`, `DESTINATION_ARRIVAL`, etc.) | `ORIGIN_SORT_SCAN` |
| `scan_timestamp` | `DATETIME` | Normalized timestamp of scan execution (UTC) | `2024-03-15 07:15:20` |
| `scan_status` | `VARCHAR(50)` | Scan condition (`Success`, `Backlog Exception`, `Manual Override`) | `Success` |
| `processing_duration_minutes` | `REAL` | Handling dwell time inside facility for this stage in minutes | `34.5` |

---

## 5. Reference Dataset: Hub Mapping (`dim_hub_mapping` / `hub_mapping.csv`)

Audit reference table used to reconcile corporate facility re-namings and ID migrations.

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `old_hub_id` | `VARCHAR(20)` | Historical legacy hub code in raw records | `HUB_KNA` |
| `old_hub_name` | `VARCHAR(100)` | Historical depot name | `Kona Expressway Transit Hub` |
| `new_hub_id` | `VARCHAR(20)` | Standardized modern hub code | `HUB_KEX` |
| `new_hub_name` | `VARCHAR(100)` | Modern corporate facility title | `Kona Express Highway Logistics Center` |
| `effective_date` | `DATE` | Date network restructuring took legal effect | `2024-07-01` |
| `mapping_status` | `VARCHAR(20)` | Migration status (`Active`, `Unchanged`, `Deprecated`) | `Active` |

---

## 6. Reference Dataset: Customers (`dim_customers` / `customers.csv`)

Corporate customer accounts contracting freight services.

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(20)` | Unique account code | `CUST_00120` |
| `customer_name` | `VARCHAR(100)` | Client business trading name | `Kolkata Freight Client 0120` |
| `customer_segment` | `VARCHAR(50)` | Commercial segment (`Enterprise B2B`, `SME Industrial`, `E-Commerce`) | `Enterprise B2B` |
| `contract_tier` | `VARCHAR(30)` | SLA commitment tier (`Gold`, `Silver`, `Bronze`, `Standard`) | `Gold` |
| `credit_terms_days` | `INTEGER` | Invoicing payment terms in calendar days | `30` |

