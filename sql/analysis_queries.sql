-- ====================================================================
-- Logistics Root-Cause Analysis - Kolkata Freight Performance Intelligence
-- Analytical SQL Queries (Advanced CTEs, Window Functions, Grouping)
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Weekly On-Time Delivery Rate (OTD) Trend & Week-over-Week Change
-- --------------------------------------------------------------------
WITH weekly_metrics AS (
    SELECT
        year_week,
        is_decline_period,
        is_festival_season,
        COUNT(*) AS total_shipments,
        SUM(on_time_flag) AS on_time_shipments,
        SUM(is_delayed) AS delayed_shipments,
        ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
        ROUND(AVG(delay_hours), 2) AS avg_delay_hours
    FROM fact_shipments
    GROUP BY year_week, is_decline_period, is_festival_season
)
SELECT
    year_week,
    is_decline_period,
    is_festival_season,
    total_shipments,
    on_time_shipments,
    delayed_shipments,
    otd_pct,
    avg_delay_hours,
    ROUND(otd_pct - LAG(otd_pct, 1) OVER (ORDER BY year_week), 2) AS wow_otd_change_pp,
    ROUND(AVG(otd_pct) OVER (ORDER BY year_week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 2) AS rolling_4wk_otd_pct
FROM weekly_metrics
ORDER BY year_week;


-- --------------------------------------------------------------------
-- QUERY 2: Monthly OTD & Baseline vs Decline Comparison
-- --------------------------------------------------------------------
SELECT
    strftime('%Y-%m', shipment_date) AS shipment_month,
    quarter,
    CASE WHEN strftime('%m', shipment_date) <= '06' THEN 'Baseline (H1)' ELSE 'Decline (H2)' END AS period_phase,
    COUNT(*) AS total_delivered,
    SUM(on_time_flag) AS on_time_count,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
    ROUND(AVG(delay_hours), 2) AS avg_delay_hours,
    ROUND(SUM(shipping_cost_inr), 2) AS total_freight_revenue_inr
FROM fact_shipments
GROUP BY strftime('%Y-%m', shipment_date), quarter
ORDER BY shipment_month;


-- --------------------------------------------------------------------
-- QUERY 3: Hub-wise OTD Ranking and Performance Deterioration
-- --------------------------------------------------------------------
WITH hub_performance AS (
    SELECT
        h.hub_id,
        h.hub_name,
        h.zone,
        COUNT(s.shipment_id) AS total_volume,
        ROUND(AVG(s.on_time_flag) * 100.0, 2) AS overall_otd_pct,
        ROUND(AVG(CASE WHEN s.is_decline_period = 0 THEN s.on_time_flag END) * 100.0, 2) AS baseline_otd_pct,
        ROUND(AVG(CASE WHEN s.is_decline_period = 1 THEN s.on_time_flag END) * 100.0, 2) AS decline_otd_pct,
        ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours
    FROM dim_hubs h
    JOIN fact_shipments s ON (h.hub_id = s.origin_hub_id OR h.hub_id = s.destination_hub_id)
    GROUP BY h.hub_id, h.hub_name, h.zone
)
SELECT
    hub_id,
    hub_name,
    zone,
    total_volume,
    overall_otd_pct,
    baseline_otd_pct,
    decline_otd_pct,
    ROUND(decline_otd_pct - baseline_otd_pct, 2) AS otd_deterioration_pp,
    avg_delay_hours,
    RANK() OVER (ORDER BY (decline_otd_pct - baseline_otd_pct) ASC) AS worst_deterioration_rank
FROM hub_performance
ORDER BY worst_deterioration_rank;


-- --------------------------------------------------------------------
-- QUERY 4: Route-wise Delays and Congestion Corridor Analysis
-- --------------------------------------------------------------------
SELECT
    r.route_id,
    r.origin_hub_id,
    r.destination_hub_id,
    r.route_category,
    r.distance_km,
    r.planned_transit_hours,
    COUNT(s.shipment_id) AS total_trips,
    ROUND(AVG(s.on_time_flag) * 100.0, 2) AS route_otd_pct,
    ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours,
    ROUND(MAX(s.delay_hours), 2) AS max_delay_hours,
    ROUND(SUM(CASE WHEN s.delay_hours > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(s.shipment_id), 2) AS delayed_trip_pct
FROM dim_routes r
JOIN fact_shipments s ON r.route_id = s.route_id
GROUP BY r.route_id, r.origin_hub_id, r.destination_hub_id, r.route_category, r.distance_km, r.planned_transit_hours
HAVING COUNT(s.shipment_id) >= 100
ORDER BY avg_delay_hours DESC
LIMIT 20;


-- --------------------------------------------------------------------
-- QUERY 5: Fleet Vehicle Downtime, Breakdowns and Availability
-- --------------------------------------------------------------------
SELECT
    v.vehicle_type,
    v.availability_status,
    COUNT(DISTINCT v.vehicle_id) AS total_vehicles,
    ROUND(AVG(v.downtime_hours), 2) AS avg_downtime_hours,
    SUM(v.breakdown_count) AS total_breakdowns,
    ROUND(AVG(v.breakdown_count), 2) AS avg_breakdowns_per_vehicle,
    COUNT(s.shipment_id) AS total_shipments_hauled,
    ROUND(AVG(s.on_time_flag) * 100.0, 2) AS fleet_otd_pct
FROM dim_vehicles v
LEFT JOIN fact_shipments s ON v.vehicle_id = s.vehicle_id
GROUP BY v.vehicle_type, v.availability_status
ORDER BY v.vehicle_type, avg_downtime_hours DESC;


-- --------------------------------------------------------------------
-- QUERY 6: Warehouse Processing Duration & Scan Backlogs by Hub
-- --------------------------------------------------------------------
SELECT
    h.hub_id,
    h.hub_name,
    w.scan_event,
    COUNT(w.scan_id) AS total_scans,
    ROUND(AVG(w.processing_duration_minutes), 2) AS avg_processing_minutes,
    ROUND(MAX(w.processing_duration_minutes), 2) AS max_processing_minutes,
    SUM(CASE WHEN w.scan_status LIKE '%Exception%' OR w.scan_status LIKE '%Backlog%' THEN 1 ELSE 0 END) AS exception_scans,
    ROUND(SUM(CASE WHEN w.scan_status LIKE '%Exception%' OR w.scan_status LIKE '%Backlog%' THEN 1 ELSE 0 END) * 100.0 / COUNT(w.scan_id), 2) AS exception_rate_pct
FROM fact_warehouse_scans w
JOIN dim_hubs h ON w.hub_id = h.hub_id
GROUP BY h.hub_id, h.hub_name, w.scan_event
ORDER BY h.hub_id, avg_processing_minutes DESC;


-- --------------------------------------------------------------------
-- QUERY 7: Customer Segment Performance & SLA Compliance
-- --------------------------------------------------------------------
SELECT
    c.customer_segment,
    c.contract_tier,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(s.shipment_id) AS total_shipments,
    ROUND(AVG(s.on_time_flag) * 100.0, 2) AS otd_pct,
    ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours,
    ROUND(SUM(s.shipping_cost_inr), 2) AS segment_revenue_inr,
    ROUND(AVG(s.shipping_cost_inr), 2) AS avg_ticket_size_inr
FROM dim_customers c
JOIN fact_shipments s ON c.customer_id = s.customer_id
GROUP BY c.customer_segment, c.contract_tier
ORDER BY total_shipments DESC;


-- --------------------------------------------------------------------
-- QUERY 8: Service-Type Mix Shift & Performance Impact
-- --------------------------------------------------------------------
WITH service_quarterly AS (
    SELECT
        service_type,
        CASE WHEN is_decline_period = 0 THEN 'Baseline (H1)' ELSE 'Decline (H2)' END AS period,
        COUNT(*) AS shipment_volume,
        ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
        ROUND(AVG(delay_hours), 2) AS avg_delay_hours
    FROM fact_shipments
    GROUP BY service_type, is_decline_period
)
SELECT
    service_type,
    period,
    shipment_volume,
    otd_pct,
    avg_delay_hours
FROM service_quarterly
ORDER BY service_type, period;


-- --------------------------------------------------------------------
-- QUERY 9: Product Category Performance & Fragility Profile
-- --------------------------------------------------------------------
SELECT
    product_category,
    COUNT(shipment_id) AS shipment_count,
    ROUND(AVG(shipment_weight_kg), 1) AS avg_weight_kg,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
    ROUND(AVG(delay_hours), 2) AS avg_delay_hours,
    ROUND(SUM(shipping_cost_inr), 2) AS total_freight_inr
FROM fact_shipments
GROUP BY product_category
ORDER BY shipment_count DESC;


-- --------------------------------------------------------------------
-- QUERY 10: Weekly Volume vs OTD Correlation Aggregation
-- --------------------------------------------------------------------
SELECT
    year_week,
    COUNT(shipment_id) AS weekly_volume,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS weekly_otd_pct,
    ROUND(AVG(delay_hours), 2) AS weekly_avg_delay_hours,
    is_festival_season,
    CASE 
        WHEN is_festival_season = 1 THEN 'Festive Surge (Durga Puja)'
        WHEN is_decline_period = 1 THEN 'Decline Period'
        ELSE 'Baseline Period'
    END AS operational_context
FROM fact_shipments
GROUP BY year_week, is_festival_season, is_decline_period
ORDER BY year_week;

