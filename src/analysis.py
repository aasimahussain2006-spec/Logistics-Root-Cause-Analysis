"""
Logistics Root-Cause Analysis - Exploratory Data Analysis & Aggregation Engine
Extracts aggregated performance views from SQLite database for visualization and modeling.
"""

import pandas as pd
from src.database import LogisticsDatabase


class LogisticsAnalysis:
    def __init__(self):
        self.db = LogisticsDatabase()

    def get_weekly_otd(self):
        """Weekly OTD trends and volume."""
        sql = """
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
        WHERE shipment_status != 'Lost / Exception'
        GROUP BY year_week, is_decline_period, is_festival_season
        ORDER BY year_week;
        """
        return self.db.run_query(sql)

    def get_quarterly_metrics(self):
        """Quarterly performance comparison."""
        sql = """
        SELECT
            quarter,
            CASE WHEN quarter IN ('Q1', 'Q2') THEN 'Baseline Period' ELSE 'Decline Period' END AS period_phase,
            COUNT(*) AS total_shipments,
            SUM(on_time_flag) AS on_time_shipments,
            ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
            ROUND(AVG(delay_hours), 2) AS avg_delay_hours,
            ROUND(SUM(shipping_cost_inr) / 1000000.0, 2) AS revenue_million_inr
        FROM fact_shipments
        WHERE shipment_status != 'Lost / Exception'
        GROUP BY quarter
        ORDER BY quarter;
        """
        return self.db.run_query(sql)

    def get_hub_performance(self):
        """Hub-level OTD ranking and baseline vs decline drop."""
        sql = """
        WITH hub_totals AS (
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
            WHERE s.shipment_status != 'Lost / Exception'
            GROUP BY h.hub_id, h.hub_name, h.zone
        )
        SELECT
            *,
            ROUND(decline_otd_pct - baseline_otd_pct, 2) AS otd_change_pp
        FROM hub_totals
        ORDER BY otd_change_pp ASC;
        """
        return self.db.run_query(sql)

    def get_route_delays(self):
        """Route-level delay metrics."""
        sql = """
        SELECT
            r.route_id,
            r.origin_hub_id,
            r.destination_hub_id,
            r.route_category,
            r.distance_km,
            r.planned_transit_hours,
            COUNT(s.shipment_id) AS trip_count,
            ROUND(AVG(s.on_time_flag) * 100.0, 2) AS otd_pct,
            ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours,
            ROUND(MAX(s.delay_hours), 2) AS max_delay_hours
        FROM dim_routes r
        JOIN fact_shipments s ON r.route_id = s.route_id
        WHERE s.shipment_status != 'Lost / Exception'
        GROUP BY r.route_id, r.origin_hub_id, r.destination_hub_id, r.route_category, r.distance_km, r.planned_transit_hours
        ORDER BY avg_delay_hours DESC;
        """
        return self.db.run_query(sql)

    def get_vehicle_performance(self):
        """Fleet vehicle performance, breakdowns, and downtime."""
        sql = """
        SELECT
            v.vehicle_type,
            v.availability_status,
            COUNT(DISTINCT v.vehicle_id) AS vehicle_count,
            ROUND(AVG(v.downtime_hours), 2) AS avg_downtime_hours,
            SUM(v.breakdown_count) AS total_breakdowns,
            ROUND(AVG(v.breakdown_count), 2) AS avg_breakdowns,
            COUNT(s.shipment_id) AS trips_completed,
            ROUND(AVG(s.on_time_flag) * 100.0, 2) AS otd_pct
        FROM dim_vehicles v
        LEFT JOIN fact_shipments s ON v.vehicle_id = s.vehicle_id
        WHERE s.shipment_status != 'Lost / Exception'
        GROUP BY v.vehicle_type, v.availability_status
        ORDER BY v.vehicle_type, avg_downtime_hours DESC;
        """
        return self.db.run_query(sql)

    def get_warehouse_processing(self):
        """Warehouse processing duration and scan volume by hub and event."""
        sql = """
        SELECT
            h.hub_id,
            h.hub_name,
            w.scan_event,
            COUNT(w.scan_id) AS scan_count,
            ROUND(AVG(w.processing_duration_minutes), 2) AS avg_duration_minutes,
            ROUND(MAX(w.processing_duration_minutes), 2) AS max_duration_minutes,
            SUM(CASE WHEN w.scan_status LIKE '%Exception%' OR w.scan_status LIKE '%Backlog%' THEN 1 ELSE 0 END) AS exception_count
        FROM fact_warehouse_scans w
        JOIN dim_hubs h ON w.hub_id = h.hub_id
        GROUP BY h.hub_id, h.hub_name, w.scan_event
        ORDER BY h.hub_id, avg_duration_minutes DESC;
        """
        return self.db.run_query(sql)

    def get_service_type_performance(self):
        """Service-type mix and OTD by operational phase."""
        sql = """
        SELECT
            service_type,
            CASE WHEN is_decline_period = 0 THEN 'Baseline (Q1-Q2)' ELSE 'Decline (Q3-Q4)' END AS period_phase,
            COUNT(*) AS volume,
            ROUND(AVG(on_time_flag) * 100.0, 2) AS otd_pct,
            ROUND(AVG(delay_hours), 2) AS avg_delay_hours
        FROM fact_shipments
        WHERE shipment_status != 'Lost / Exception'
        GROUP BY service_type, is_decline_period
        ORDER BY service_type, period_phase;
        """
        return self.db.run_query(sql)

    def get_customer_segment_performance(self):
        """Customer segment SLA compliance."""
        sql = """
        SELECT
            c.customer_segment,
            COUNT(s.shipment_id) AS total_shipments,
            ROUND(AVG(s.on_time_flag) * 100.0, 2) AS otd_pct,
            ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours,
            ROUND(SUM(s.shipping_cost_inr) / 1000000.0, 2) AS segment_revenue_million_inr
        FROM dim_customers c
        JOIN fact_shipments s ON c.customer_id = s.customer_id
        WHERE s.shipment_status != 'Lost / Exception'
        GROUP BY c.customer_segment
        ORDER BY total_shipments DESC;
        """
        return self.db.run_query(sql)

