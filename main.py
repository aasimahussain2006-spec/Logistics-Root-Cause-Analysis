"""
Logistics Root-Cause Analysis - Master Pipeline Orchestrator
Executes the end-to-end analytics workflow from synthetic data generation through
data quality auditing, cleaning, SQLite modeling, hypothesis testing, driver tree decomposition,
early-warning backtesting, Power BI export, PDF memo generation, and test validation.
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_generation import generate_reference_data, generate_shipments_and_scans
from src.data_validation import validate_raw_datasets
from src.data_cleaning import run_cleaning_pipeline
from src.database import build_database
from src.visualization import generate_all_visualizations
from src.hypothesis_testing import run_all_hypothesis_tests
from src.driver_tree import run_driver_tree_analysis
from src.early_warning import run_early_warning_pipeline
from src.export_power_bi import export_star_schema_tables
from src.report_generation import build_management_memo_pdf, export_management_memo_markdown
from src.generate_notebooks import generate_all_notebooks


def run_full_pipeline():
    start_time = time.time()
    print("\n" + "="*70)
    print("KOLKATA FREIGHT & LOGISTICS - PERFORMANCE INTELLIGENCE PIPELINE")
    print("Master End-to-End Execution")
    print("="*70 + "\n")

    # Step 1: Reference & Synthetic Data Generation
    print("[PHASE 1/11] Generating Reference Datasets & Synthetic Operational Feeds...")
    generate_reference_data()
    generate_shipments_and_scans()

    # Step 2: Data Quality Auditing
    print("\n[PHASE 2/11] Auditing Raw Data Quality & Controlled Anomalies...")
    validate_raw_datasets()

    # Step 3: Cleaning & Preprocessing
    print("\n[PHASE 3/11] Executing Deterministic Data Cleaning Pipeline...")
    run_cleaning_pipeline()

    # Step 4: Database Integration
    print("\n[PHASE 4/11] Initializing SQLite Data Warehouse & Ingesting Relational Facts...")
    build_database()

    # Step 5: Visualizations & EDA
    print("\n[PHASE 5/11] Generating 12 Publication-Grade EDA Visualizations...")
    generate_all_visualizations()

    # Step 6: Inferential Hypothesis Testing
    print("\n[PHASE 6/11] Executing Inferential Hypothesis Testing Suite (H1-H6)...")
    run_all_hypothesis_tests()

    # Step 7: Driver Tree Decomposition
    print("\n[PHASE 7/11] Executing Operational Driver Tree & Counterfactual Attribution...")
    run_driver_tree_analysis()

    # Step 8: Early-Warning Monitoring & Backtesting
    print("\n[PHASE 8/11] Backtesting Weekly Early-Warning Risk System...")
    run_early_warning_pipeline()

    # Step 9: Power BI Star Schema Export
    print("\n[PHASE 9/11] Exporting Power BI Star Schema CSVs...")
    export_star_schema_tables()

    # Step 10: Executive Management Memo
    print("\n[PHASE 10/11] Generating Executive Management Memo PDF & Markdown...")
    build_management_memo_pdf()
    export_management_memo_markdown()

    # Step 11: Jupyter Notebooks
    print("\n[PHASE 11/11] Generating 7 Documented Jupyter Notebooks...")
    generate_all_notebooks()

    elapsed = time.time() - start_time
    print("\n" + "="*70)
    print(f"PIPELINE EXECUTION COMPLETE IN {elapsed:.1f} SECONDS")
    print("All datasets, database, reports, charts, and documentation generated successfully.")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_full_pipeline()

