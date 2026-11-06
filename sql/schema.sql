-- ====================================================================
-- Logistics Root-Cause Analysis - Kolkata Freight Performance Intelligence
-- SQLite Relational Database Schema
-- ====================================================================

-- 1. DimHub: Logistics Hubs in Kolkata Metropolitan Area
DROP TABLE IF EXISTS dim_hubs;
CREATE TABLE dim_hubs (
    hub_id VARCHAR(20) PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    hub_type VARCHAR(50) NOT NULL,
    capacity_per_day INTEGER NOT NULL
);

-- 2. DimHubMapping: Network Restructuring Reference
DROP TABLE IF EXISTS dim_hub_mapping;
CREATE TABLE dim_hub_mapping (
    old_hub_id VARCHAR(20) NOT NULL,
    old_hub_name VARCHAR(100),
    new_hub_id VARCHAR(20) NOT NULL,
    new_hub_name VARCHAR(100),
    effective_date DATE NOT NULL,
    mapping_status VARCHAR(20) NOT NULL,
    PRIMARY KEY (old_hub_id, effective_date)
);

-- 3. DimRoute: Inter-Hub Transit Corridors
DROP TABLE IF EXISTS dim_routes;
CREATE TABLE dim_routes (
    route_id VARCHAR(30) PRIMARY KEY,
    origin_hub_id VARCHAR(20) NOT NULL,
    destination_hub_id VARCHAR(20) NOT NULL,
    distance_km REAL NOT NULL,
    planned_transit_hours REAL NOT NULL,
    route_category VARCHAR(50) NOT NULL,
    toll_plazas INTEGER DEFAULT 0,
    FOREIGN KEY (origin_hub_id) REFERENCES dim_hubs(hub_id),
    FOREIGN KEY (destination_hub_id) REFERENCES dim_hubs(hub_id)
);

-- 4. DimVehicle: Fleet Master & Maintenance Records
DROP TABLE IF EXISTS dim_vehicles;
CREATE TABLE dim_vehicles (
    vehicle_id VARCHAR(20) PRIMARY KEY,
    vehicle_type VARCHAR(50) NOT NULL,
    capacity_kg INTEGER NOT NULL,
    maintenance_date DATE NOT NULL,
    downtime_hours REAL NOT NULL,
    breakdown_count INTEGER NOT NULL,
    availability_status VARCHAR(30) NOT NULL,
    is_aging_fleet INTEGER DEFAULT 0
);

-- 5. DimCustomer: Business Clients & Service Contracts
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL,
    contract_tier VARCHAR(30) NOT NULL,
    credit_terms_days INTEGER NOT NULL
);

-- 6. FactShipments: Core Shipment Deliveries & SLAs
DROP TABLE IF EXISTS fact_shipments;
CREATE TABLE fact_shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    origin_hub_id VARCHAR(20) NOT NULL,
    destination_hub_id VARCHAR(20) NOT NULL,
    route_id VARCHAR(30) NOT NULL,
    vehicle_id VARCHAR(20) NOT NULL,
    shipment_date DATE NOT NULL,
    dispatch_timestamp DATETIME NOT NULL,
    promised_delivery_timestamp DATETIME NOT NULL,
    actual_delivery_timestamp DATETIME,
    shipment_status VARCHAR(30) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    shipment_weight_kg REAL NOT NULL,
    shipping_cost_inr REAL NOT NULL,
    on_time_flag INTEGER NOT NULL,
    is_delayed INTEGER NOT NULL,
    delay_hours REAL DEFAULT 0.0,
    quarter VARCHAR(5) NOT NULL,
    year_week INTEGER NOT NULL,
    is_decline_period INTEGER NOT NULL,
    is_festival_season INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (origin_hub_id) REFERENCES dim_hubs(hub_id),
    FOREIGN KEY (destination_hub_id) REFERENCES dim_hubs(hub_id),
    FOREIGN KEY (route_id) REFERENCES dim_routes(route_id),
    FOREIGN KEY (vehicle_id) REFERENCES dim_vehicles(vehicle_id)
);

-- 7. FactWarehouseScans: Granular Operational Tracking Events
DROP TABLE IF EXISTS fact_warehouse_scans;
CREATE TABLE fact_warehouse_scans (
    scan_id VARCHAR(30) PRIMARY KEY,
    shipment_id VARCHAR(30) NOT NULL,
    hub_id VARCHAR(20) NOT NULL,
    scan_event VARCHAR(50) NOT NULL,
    scan_timestamp DATETIME NOT NULL,
    scan_status VARCHAR(50) NOT NULL,
    processing_duration_minutes REAL NOT NULL,
    FOREIGN KEY (shipment_id) REFERENCES fact_shipments(shipment_id),
    FOREIGN KEY (hub_id) REFERENCES dim_hubs(hub_id)
);

-- Performance Indices
CREATE INDEX idx_shipments_date ON fact_shipments(shipment_date);
CREATE INDEX idx_shipments_week ON fact_shipments(year_week);
CREATE INDEX idx_shipments_origin ON fact_shipments(origin_hub_id);
CREATE INDEX idx_shipments_dest ON fact_shipments(destination_hub_id);
CREATE INDEX idx_shipments_route ON fact_shipments(route_id);
CREATE INDEX idx_shipments_vehicle ON fact_shipments(vehicle_id);
CREATE INDEX idx_shipments_status ON fact_shipments(shipment_status, on_time_flag);
CREATE INDEX idx_scans_shipment ON fact_warehouse_scans(shipment_id);
CREATE INDEX idx_scans_hub ON fact_warehouse_scans(hub_id);
CREATE INDEX idx_scans_event ON fact_warehouse_scans(scan_event);

