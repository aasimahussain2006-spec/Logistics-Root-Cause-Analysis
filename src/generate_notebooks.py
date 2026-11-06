"""
Logistics Root-Cause Analysis - Jupyter Notebook Programmatic Generator
Generates all 7 production-grade, executable Jupyter Notebooks in notebooks/.
"""

import json
from pathlib import Path
from src.config import PROJECT_ROOT

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_notebook(cells):
    """Creates a standard Jupyter Notebook dictionary."""
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.4"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }


def generate_all_notebooks():
    print("Generating 7 Jupyter Notebooks in notebooks/...")

    # -------------------------------------------------------------
    # Notebook 1: Business Understanding
    # -------------------------------------------------------------
    nb1_cells = [
        markdown_cell("""# 01. Business Understanding & Problem Formulation
## Kolkata Freight & Logistics Performance Intelligence

> **Important Notice:** This notebook uses synthetic operational records modeled for demonstration.

### Executive Problem Context
Kolkata Freight & Logistics (KFL) operates a freight trucking network across 12 major hubs in the Greater Kolkata metropolitan region.
Over the past two quarters (Q3–Q4), headline performance suffered a severe collapse.

### Headline Metric: On-Time Delivery Rate (OTD)
$$\\text{OTD} = \\left( \\frac{\\text{Eligible shipments delivered on or before promised delivery time}}{\\text{Total eligible delivered shipments}} \\right) \\times 100$$
- Corporate Target SLA: $\\ge 85.0\\%$
- Baseline Period (Q1–Q2): $\\approx 90.1\\%$
- Decline Period (Q3–Q4): $\\approx 64.3\\%$"""),
        code_cell("""import sys
sys.path.append("..")
import pandas as pd
from src.config import HUBS, HUB_RENAMING_MAPPING, HEADLINE_METRIC, OTD_TARGET_PERCENT

print(f"Headline Metric: {HEADLINE_METRIC}")
print(f"Target SLA: {OTD_TARGET_PERCENT}%")
print(f"Monitored Kolkata Hubs: {len(HUBS)}")"""),
        markdown_cell("""### The 12 Monitored Logistics Hubs
Reviewing facility locations, geocoordinates, and designed daily throughput capacities:"""),
        code_cell("""df_hubs = pd.DataFrame.from_dict(HUBS, orient="index")
df_hubs[["name", "zone", "type", "capacity_per_day"]]""")
    ]
    with open(NOTEBOOKS_DIR / "01_business_understanding.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb1_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 2: Data Quality Checks
    # -------------------------------------------------------------
    nb2_cells = [
        markdown_cell("""# 02. Automated Data Quality Inspection & Profiling
Auditing ~1.55 million raw records across Shipments, Warehouse Scans, Routes, and Vehicles to detect controlled anomalies."""),
        code_cell("""import sys
sys.path.append("..")
from src.data_validation import validate_raw_datasets

report = validate_raw_datasets()"""),
        markdown_cell("""### Summary of Audited Data Quality Anomalies
Inspecting detected duplicates, missing delivery timestamps, dirty string units, and timezone anomalies:"""),
        code_cell("""for category, details in report.items():
    print(f"\\n--- {category.upper()} ---")
    for k, v in details.items():
        print(f"  {k}: {v:,}")""")
    ]
    with open(NOTEBOOKS_DIR / "02_data_quality_checks.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb2_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 3: Data Cleaning
    # -------------------------------------------------------------
    nb3_cells = [
        markdown_cell("""# 03. Deterministic Data Cleaning & Preprocessing Pipeline
Standardizing schemas, reconciling entity IDs, normalizing timezones to UTC, and logging an auditable cleaning trail."""),
        code_cell("""import sys
sys.path.append("..")
import pandas as pd
from src.data_cleaning import run_cleaning_pipeline

df_audit = run_cleaning_pipeline()"""),
        markdown_cell("""### Data Cleaning Audit Trail Review
Inspecting the audit log of every transformation performed:"""),
        code_cell("""pd.set_option("display.max_colwidth", None)
df_audit[["step", "table_name", "records_affected", "records_retained", "records_excluded", "reason_for_exclusion"]]""")
    ]
    with open(NOTEBOOKS_DIR / "03_data_cleaning.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb3_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 4: Exploratory Data Analysis
    # -------------------------------------------------------------
    nb4_cells = [
        markdown_cell("""# 04. Exploratory Data Analysis & Diagnostic Intelligence
Connecting to the SQLite analytical data warehouse and generating diagnostic charts."""),
        code_cell("""import sys
sys.path.append("..")
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from src.database import LogisticsDatabase

db = LogisticsDatabase()"""),
        markdown_cell("""### Weekly OTD Performance & Volume Trajectory"""),
        code_cell("""sql_wk = \"\"\"
SELECT year_week, COUNT(*) AS volume, AVG(on_time_flag)*100.0 AS otd_pct
FROM fact_shipments WHERE shipment_status != 'Lost / Exception'
GROUP BY year_week ORDER BY year_week;
\"\"\"
df_wk = db.run_query(sql_wk)
df_wk.head(10)"""),
        markdown_cell("""### Hub-Level Deterioration Analysis"""),
        code_cell("""sql_hubs = \"\"\"
SELECT 
    origin_hub_id,
    AVG(CASE WHEN is_decline_period = 0 THEN on_time_flag END)*100.0 AS baseline_otd,
    AVG(CASE WHEN is_decline_period = 1 THEN on_time_flag END)*100.0 AS decline_otd
FROM fact_shipments WHERE shipment_status != 'Lost / Exception'
GROUP BY origin_hub_id;
\"\"\"
df_hubs = db.run_query(sql_hubs)
df_hubs["decline_pp"] = df_hubs["decline_otd"] - df_hubs["baseline_otd"]
df_hubs.sort_values(by="decline_pp")""")
    ]
    with open(NOTEBOOKS_DIR / "04_exploratory_data_analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb4_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 5: Hypothesis Testing
    # -------------------------------------------------------------
    nb5_cells = [
        markdown_cell("""# 05. Inferential Statistical Hypothesis Testing
Rigorous scientific testing of Hypotheses H1 through H6 using Welch t-tests, Chi-square tests, and Logistic Regression."""),
        code_cell("""import sys
sys.path.append("..")
import pandas as pd
from src.hypothesis_testing import run_all_hypothesis_tests

df_hyp = run_all_hypothesis_tests()"""),
        markdown_cell("""### Formal Hypothesis Decisions & Evidence"""),
        code_cell("""df_hyp[["hypothesis_id", "business_question", "statistical_method", "test_statistic", "p_value", "decision"]]""")
    ]
    with open(NOTEBOOKS_DIR / "05_hypothesis_testing.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb5_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 6: Driver Tree Analysis
    # -------------------------------------------------------------
    nb6_cells = [
        markdown_cell("""# 06. Operational Driver Tree & Counterfactual Decomposition
Decomposing the headline OTD decline from 90.1% to 64.3% into distinct, non-overlapping operational drivers."""),
        code_cell("""import sys
sys.path.append("..")
import pandas as pd
from src.driver_tree import run_driver_tree_analysis

df_decomp = run_driver_tree_analysis()"""),
        markdown_cell("""### Decomposition Table & Attribution Percentages"""),
        code_cell("""df_decomp""")
    ]
    with open(NOTEBOOKS_DIR / "06_driver_tree_analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb6_cells), f, indent=2)

    # -------------------------------------------------------------
    # Notebook 7: Early-Warning System
    # -------------------------------------------------------------
    nb7_cells = [
        markdown_cell("""# 07. Weekly Early-Warning Monitoring & Backtesting Audit
Constructing a composite operational risk index and backtesting leading indicators against historical observations."""),
        code_cell("""import sys
sys.path.append("..")
from src.early_warning import run_early_warning_pipeline

results = run_early_warning_pipeline()"""),
        markdown_cell("""### Backtest Evaluation Metrics"""),
        code_cell("""print(f"Target Deterioration: Week {results['target_crisis_week']}")
print(f"Earliest Alert Detection: Week {results['detected_week']}")
print(f"Warning Lead Time: {results['lead_time_weeks']} Weeks Ahead")
print(f"Baseline False Alarms: {results['false_alarms']}")
print(f"System Recall: {results['recall_pct']}%")
print(f"Alert Precision: {results['precision_pct']}%")""")
    ]
    with open(NOTEBOOKS_DIR / "07_early_warning_analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb7_cells), f, indent=2)

    print("All 7 Jupyter Notebooks successfully generated!")


if __name__ == "__main__":
    generate_all_notebooks()

