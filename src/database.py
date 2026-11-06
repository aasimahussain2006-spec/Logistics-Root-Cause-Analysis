"""
Logistics Root-Cause Analysis - Database Management & Analytical Data Integration
Builds SQLite relational data warehouse, creates schema, indices, views, and executes analytical queries.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from src.config import (
    DB_PATH,
    DATA_PROCESSED_DIR,
    DATA_REF_DIR,
    PROJECT_ROOT
)


class LogisticsDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.schema_path = PROJECT_ROOT / "sql" / "schema.sql"
        self.queries_path = PROJECT_ROOT / "sql" / "analysis_queries.sql"

    def get_connection(self):
        """Create and return a SQLite database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def init_schema(self):
        """Execute schema.sql to initialize tables and performance indices."""
        print("[Database 1/3] Initializing SQLite schema and tables...")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)
        print("Schema and indices successfully applied.")

    def load_data(self):
        """Load cleaned and reference tables into the SQLite database."""
        print("[Database 2/3] Ingesting relational tables into SQLite database...")
        conn = self.get_connection()

        # 1. DimHubs
        df_hubs = pd.read_csv(DATA_REF_DIR / "hubs.csv")
        df_hubs.to_sql("dim_hubs", conn, if_exists="replace", index=False)
        print(f"  - dim_hubs: {len(df_hubs):,} rows")

        # 2. DimHubMapping
        df_mapping = pd.read_csv(DATA_REF_DIR / "hub_mapping.csv")
        df_mapping.to_sql("dim_hub_mapping", conn, if_exists="replace", index=False)
        print(f"  - dim_hub_mapping: {len(df_mapping):,} rows")

        # 3. DimRoutes
        df_routes = pd.read_csv(DATA_REF_DIR / "routes.csv")
        df_routes.to_sql("dim_routes", conn, if_exists="replace", index=False)
        print(f"  - dim_routes: {len(df_routes):,} rows")

        # 4. DimVehicles
        df_vehicles = pd.read_csv(DATA_REF_DIR / "vehicles.csv")
        df_vehicles.to_sql("dim_vehicles", conn, if_exists="replace", index=False)
        print(f"  - dim_vehicles: {len(df_vehicles):,} rows")

        # 5. DimCustomers
        df_customers = pd.read_csv(DATA_REF_DIR / "customers.csv")
        df_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
        print(f"  - dim_customers: {len(df_customers):,} rows")

        # 6. FactShipments (Chunked ingestion for high throughput)
        print("  - Ingesting fact_shipments...")
        clean_ship_path = DATA_PROCESSED_DIR / "cleaned_shipments.csv"
        chunk_size = 50_000
        for i, chunk in enumerate(pd.read_csv(clean_ship_path, chunksize=chunk_size, low_memory=False)):
            chunk.to_sql("fact_shipments", conn, if_exists="append" if i > 0 else "replace", index=False)
        ship_count = conn.execute("SELECT COUNT(*) FROM fact_shipments").fetchone()[0]
        print(f"  - fact_shipments: {ship_count:,} rows loaded.")

        # 7. FactWarehouseScans (Chunked ingestion)
        print("  - Ingesting fact_warehouse_scans...")
        clean_scans_path = DATA_PROCESSED_DIR / "cleaned_warehouse_scans.csv"
        for i, chunk in enumerate(pd.read_csv(clean_scans_path, chunksize=chunk_size, low_memory=False)):
            chunk.to_sql("fact_warehouse_scans", conn, if_exists="append" if i > 0 else "replace", index=False)
        scans_count = conn.execute("SELECT COUNT(*) FROM fact_warehouse_scans").fetchone()[0]
        print(f"  - fact_warehouse_scans: {scans_count:,} rows loaded.")

        # Re-create indices for fast analytical queries
        print("[Database 3/3] Creating analytical indices...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_shipments_id ON fact_shipments(shipment_id)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_date ON fact_shipments(shipment_date)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_week ON fact_shipments(year_week)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_origin ON fact_shipments(origin_hub_id)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_dest ON fact_shipments(destination_hub_id)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_route ON fact_shipments(route_id)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_vehicle ON fact_shipments(vehicle_id)",
            "CREATE INDEX IF NOT EXISTS idx_shipments_status ON fact_shipments(shipment_status, on_time_flag)",
            "CREATE INDEX IF NOT EXISTS idx_scans_shipment ON fact_warehouse_scans(shipment_id)",
            "CREATE INDEX IF NOT EXISTS idx_scans_hub ON fact_warehouse_scans(hub_id)",
            "CREATE INDEX IF NOT EXISTS idx_scans_event ON fact_warehouse_scans(scan_event)"
        ]
        for idx in indices:
            conn.execute(idx)
        conn.commit()
        conn.close()
        print("Database load completed successfully.")

    def run_query(self, query_sql):
        """Execute a SQL query and return a pandas DataFrame."""
        with self.get_connection() as conn:
            df = pd.read_sql_query(query_sql, conn)
        return df


def build_database():
    db = LogisticsDatabase()
    db.init_schema()
    db.load_data()
    return db


if __name__ == "__main__":
    build_database()
