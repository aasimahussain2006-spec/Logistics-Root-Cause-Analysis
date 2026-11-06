# Logistics Root-Cause Analysis – Kolkata Freight & Logistics Performance Intelligence
### End-to-End Advanced Analytics Engineering, Statistical Attribution & Operational Intelligence System

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%203%20%7C%20DuckDB-orange.svg)](https://sqlite.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![BI](https://img.shields.io/badge/Power%20BI-Star%20Schema%20Compatible-yellow.svg)](https://powerbi.microsoft.com/)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed%20%7C%20100%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

> **IMPORTANT DISCLAIMER:**  
> This project is based on a fictional freight trucking company operating across Kolkata and West Bengal, India. Actual company datasets have not been supplied. All 1,546,782 records across shipments, routes, vehicles, and scans were synthetically generated with fixed random seeds for complete reproducibility. All findings, causal drivers, and recommendations represent modeled analytical scenarios and must never be cited as real-world company records.

---

## 1. Executive Summary & Business Problem

**Kolkata Freight & Logistics (KFL)** operates an arterial freight haulage and multi-modal distribution network across 12 strategic logistics hubs in Greater Kolkata and the NH16 / Kona Expressway industrial freight corridor.

During the second half of FY 2024 (Q3–Q4 / Weeks 27–52), executive leadership observed an alarming collapse in headline business performance:
- **Headline Operational Metric:** **On-Time Delivery Rate (OTD)**
  $$\text{OTD} = \left( \frac{\text{Eligible shipments delivered on or before promised delivery time}}{\text{Total eligible delivered shipments}} \right) \times 100$$
- **Corporate SLA Commitment:** $\ge 85.00\%$
- **Baseline Performance (Q1–Q2):** **90.10%** (SLA Met)
- **Current Performance (Q3–Q4):** **64.33%** (Severe Crisis)
- **Observed Collapse:** **-25.77 percentage points (-28.6% relative decline)**

Management initially held conflicting hypotheses attributing the collapse to either local highway roadworks, fleet mechanical breakdowns, warehouse conveyor bottlenecks, service-tier mix shifts, or the annual Durga Puja festive demand surge. This project was commissioned to conduct an objective, empirical, data-driven root-cause investigation across ~1.55 million operational records.

---

## 2. Key Empirical Findings & Driver Attribution

Our counterfactual decomposition and inferential statistical suite successfully accounted for **92.9% of the observed decline** without double-counting:

```
[Baseline OTD: 90.10%]
       │
       ├──► 1. Warehouse Sorting Bottlenecks (Dhulagarh & Taratala)  : -4.73 pp (18.4% of drop)
       ├──► 2. Highway Corridor Congestion (NH16 / Kona Bypass)      : -4.13 pp (16.0% of drop)
       ├──► 3. Fleet Mechanical Breakdowns & Downtime (Aging Fleet)   : -3.96 pp (15.4% of drop)
       ├──► 4. Commercial Service Mix Shift (Tight-SLA Growth)       : -7.71 pp (29.9% of drop)
       ├──► 5. Seasonal Festive Demand Shock (Durga Puja Peak)       : -3.42 pp (13.3% of drop)
       └──► 6. Unexplained Residual & Stochastic Transit Noise        : -1.82 pp ( 7.1% of drop)
       │
       ▼
[Current OTD: 64.33%]  ──► Total Decline: -25.77 pp (92.9% Mathematically Explained)
```

### The Seasonality Myth (Hypothesis H6 Refuted):
Executive management initially assumed the annual Durga Puja / Diwali festival surge was the primary cause of poor OTD. **Statistical phase testing decisively refutes this**:
- OTD had already collapsed to **65.4% during Weeks 27–38**, a full 12 weeks before the festival surge began in Week 39.
- In Weeks 45–52, after shipment volume normalized back to baseline, OTD failed to recover (remaining at **63.8%**).
- **Conclusion:** While the festival volume shock exacerbated temporary delays, the underlying crisis was driven by structural sorting equipment failures at Dhulagarh/Taratala and deferred fleet maintenance.

---

## 3. Technology Stack & Enterprise Architecture

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Language & Core** | Python 3.12, NumPy, Pandas | Vectorized generation, data transformation, business logic |
| **Database & SQL** | SQLite 3.45, SQL (CTEs, Window Functions) | Relational modeling, indexing, high-performance analytical views |
| **Statistical Analysis** | SciPy, Statsmodels, Scikit-learn | Welch's t-test, Chi-Square, Logistic Regression, FDR adjustment |
| **Visual Analytics** | Matplotlib, Seaborn, Plotly | 12 publication-grade EDA visualizations & waterfall charts |
| **Interactive BI** | Streamlit | 6-page interactive corporate intelligence dashboard |
| **Enterprise BI** | Power BI Star Schema CSV Exports | Conformed Dimensions, Fact Tables, DAX measures |
| **Executive Reporting**| ReportLab, Markdown | 2-page C-suite PDF memorandum and audit documentation |
| **Quality & CI/CD** | Pytest | 13 automated unit tests verifying schema, OTD, and attribution |

---

## 4. Repository Structure

```
Logistics_Root_Cause_Analysis/
├── data/
│   ├── raw/                       # Raw synthetic CSVs with controlled quality anomalies (~1.55M rows)
│   ├── processed/                 # Sanitized datasets and kolkata_logistics.db (SQLite)
│   ├── reference/                 # Canonical reference tables (hubs, routes, vehicles, customers)
│   └── power_bi_exports/          # Star-schema CSV exports for Power BI Desktop
├── notebooks/                     # 7 fully documented, runnable Jupyter Notebooks
│   ├── 01_business_understanding.ipynb
│   ├── 02_data_quality_checks.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_hypothesis_testing.ipynb
│   ├── 06_driver_tree_analysis.ipynb
│   └── 07_early_warning_analysis.ipynb
├── src/                           # Reusable production Python modules
│   ├── config.py                  # System paths, constants, hub metadata, random seeds
│   ├── data_generation.py         # Vectorized ~1.55M synthetic generator with controlled flaws
│   ├── data_validation.py         # Automated data quality profiler and flaw detector
│   ├── data_cleaning.py           # Deterministic data cleaning pipeline & audit logger
│   ├── database.py                # SQLite warehouse manager, schema migration, analytical queries
│   ├── analysis.py                # Analytical aggregations and metrics engine
│   ├── visualization.py           # 12 publication-grade EDA visualization generators
│   ├── hypothesis_testing.py      # Statistical testing engine for H1-H6 with effect sizes
│   ├── driver_tree.py             # Counterfactual driver tree decomposition engine
│   ├── early_warning.py           # Weekly composite risk index & backtesting engine
│   ├── report_generation.py       # Two-page executive memo PDF builder (ReportLab)
│   └── export_power_bi.py         # Power BI Star Schema generator
├── sql/
│   ├── schema.sql                 # DDL for Facts, Dimensions, Foreign Keys, and Indices
│   └── analysis_queries.sql       # 10 production SQL queries with CTEs and Window Functions
├── dashboard/                     # Multi-page interactive Streamlit dashboard
│   ├── app.py                     # Main application entry point
│   ├── components/                # Modular KPI cards, charts, and sidebar filters
│   └── assets/                    # Corporate styling CSS
├── reports/
│   ├── driver_tree/               # driver_tree.png and driver_tree_decomposition.csv
│   ├── management_memo/           # management_memo.pdf (2 pages) and management_memo.md
│   └── visualizations/            # 12 publication-grade charts (PNG)
├── documentation/
│   ├── problem_statement.md       # Comprehensive business background and SLA definition
│   ├── data_dictionary.md         # Full column-level dictionary across 7 tables
│   ├── methodology.md             # End-to-end analytical framework and testing methods
│   ├── hypothesis_log.csv         # Audit log of H1-H6 statistical decisions and evidence
│   ├── cleaning_audit.csv         # Audit log of every data cleaning transformation
│   ├── early_warning_audit.csv    # 52-week risk scores and alert audit trail
│   └── star_schema_and_dax.md     # Power BI data model and production DAX formulas
├── tests/                         # Automated unit tests (Pytest)
│   ├── test_data_generation.py
│   ├── test_data_cleaning.py
│   └── test_analysis.py
├── main.py                        # Master pipeline orchestrator
├── requirements.txt               # Pinned dependencies
└── README.md                      # Comprehensive portfolio documentation
```

---

## 5. Controlled Data Quality Engineering & Cleaning Audit

To simulate real-world enterprise data challenges, 9 controlled data quality flaws were intentionally injected into the raw feeds:

| Flaw Category | Injected Volume | Impact & Detection Mechanism | Cleaning & Reconciliation Action |
| :--- | :--- | :--- | :--- |
| **Duplicate Consignments** | 3,247 Shipments | Double-counted volumes and artificially inflated costs | Deduplicated using composite primary key `(shipment_id)` |
| **Corrupted Scan Events** | 22,111 Scans | Repeated RFID pulse bounces at sorting gates | Deduplicated on `(scan_id)` |
| **Missing Delivery Timestamps**| 6,299 Records | Unconfirmed shipments skewing OTD denominator | Tagged as `"Lost / Exception"` and segregated from SLA pool |
| **Dirty String Units** | 21,269 Records | Ingestion failures due to `" kg"` and `"INR "` strings | Regex extraction and standardized casting to IEEE 754 float |
| **Timezone Inconsistencies** | 18,675 Records | Mixed UTC `Z`, IST `+05:30`, and `/` date formats | Normalized deterministically to standard UTC `YYYY-MM-DD HH:MM:SS` |
| **Chronological Violations** | 2,450 Records | Deliveries timestamped before dispatch or year 2099 | Quarantined and excluded from downstream analytical facts |
| **Legacy Hub Mappings** | 3,986 Records | Pre-merger codes (`HUB_KEX_OLD`, `HUB_SLK_OLD`) | Entity reconciliation using `dim_hub_mapping` reference table |
| **Inconsistent Taxonomy** | 17,749 Records | Mixed casing (`"std surface"`, `"EXP_CARGO"`) | Standardized to canonical 3 service categories |
| **Referential Integrity Orphans**| 2,800 Records | Missing foreign keys (`VEH_9999`, `R_UNKNOWN`) | Deterministically resolved using hub coordinates and fleet pool |

*Complete transformation records are preserved in [documentation/cleaning_audit.csv](file:///c:/yuva%20intern/Logistics_Root_Cause_Analysis/documentation/cleaning_audit.csv).*

---

## 6. Formal Statistical Hypothesis Testing Results

| ID | Business Question | Statistical Method | Test Statistic | p-Value | Effect Size | Decision | Empirical Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **H1** | Did corridor transit friction drive delays? | Welch's Independent t-test | $t = 31.42$ | $5.25 \times 10^{-162}$ | Cohen's $d = 0.48$ | **Supported** | Arterial highway routes (NH16/Kona) averaged 2.45h delay vs 0.65h on suburban corridors. |
| **H2** | Did vehicle downtime increase delay probability? | Binomial Logistic Regression | $z = 18.24$ | $< 10^{-15}$ | Odds Ratio = 3.42 | **Supported** | Vehicles with >40h downtime increased consignment delay probability by 3.4x (95% CI [3.12, 3.75]). |
| **H3** | Did warehouse dwell time increase turnaround? | Welch's t-test & Pearson $r$ | $t = 48.20$ | $< 10^{-15}$ | $r = 0.64$ | **Supported** | Origin sort duration jumped from 36.4 to 118.5 min in decline period; strongly correlated with total delay. |
| **H4** | Was deterioration concentrated in specific hubs? | Pearson's $\chi^2$ Independence | $\chi^2 = 3,412.5$ | $< 10^{-15}$ | Cramer's $V = 0.28$ | **Supported** | Dhulagarh (-33.2 pp) and Taratala (-29.8 pp) collapsed, while Salt Lake maintained >82% OTD. |
| **H5** | Did service mix shifts impact headline OTD? | Chi-Square & Standardization | $\chi^2 = 824.1$ | $< 10^{-15}$ | Mix share: +8.0 pp | **Supported** | Tight-SLA Express and Same-Day volume expanded from 8% to 16% of shipments, compressing SLA buffer. |
| **H6** | Did seasonal festive demand cause the decline? | Interrupted Phase t-test | $t = 28.60$ | $< 10^{-15}$ | Recovery = 0.0 pp | **Not Supported** | OTD collapsed in Weeks 27-38 prior to festival, and failed to recover post-festival (63.8%). Refuted as primary cause. |

---

## 7. Weekly Early-Warning Monitoring & Backtest Results

To prevent future operational blind spots, we engineered a Weekly Early-Warning System combining rolling Z-scores of leading operational indicators (warehouse dwell time creep, corridor transit latency, fleet maintenance deferral) into a **Composite Operational Risk Index**.

### Historical Backtesting Against FY 2024:
- **Actual Structural Collapse:** **Week 27** (Beginning of Q3)
- **Earliest Warning Detection:** **Week 23** (Orange Alert triggered on sort dwell and corridor latency creep)
- **Warning Lead Time:** **4 Weeks in Advance** (Target $\ge 4$ weeks met)
- **Baseline False Alarms (Weeks 1–20):** **0 (Zero)**
- **System Recall:** **100.0%** (Zero missed deterioration events)
- **Alert Precision:** **86.7%**

---

## 8. Interactive Streamlit Dashboard Walkthrough

The platform features a corporate interactive dashboard with 6 specialized analytical views:

```powershell
# Launch the Streamlit Intelligence Platform
streamlit run dashboard/app.py
```

### Dashboard Pages:
1. **Executive Overview:** Headline KPI cards (Total shipments, On-time count, Delay count, Overall OTD, Decline pp), weekly volume vs OTD trend, quarterly scorecard.
2. **Hub Performance:** Interactive comparison across all 12 hubs, baseline vs decline performance ranking, throughput capacity vs volume utilization.
3. **Route & Vehicle Analysis:** Highway corridor delay distributions, transit distance vs planned hours scatter, vehicle downtime vs breakdown frequency.
4. **Warehouse Operations:** RFID scan event mix pie chart, hub-wise sorting dwell time box plots, terminal backlog exception rates.
5. **Root-Cause Analysis:** Interactive Plotly Waterfall driver tree diagram, tabular attribution percentages, formal hypothesis testing log.
6. **Early-Warning System:** Real-time composite operational risk index gauge, 4-week lead alert trajectory, weekly operational risk audit trail.

---

## 9. Power BI Star Schema Integration & DAX Measures

The project prepares production-ready CSV exports in `data/power_bi_exports/` following an optimized dimensional star schema:
- **Fact Tables:** `FactShipments.csv` (347,621 rows), `FactWarehouseScans.csv` (1,138,153 rows)
- **Dimension Tables:** `DimDate.csv`, `DimHub.csv`, `DimRoute.csv`, `DimVehicle.csv`, `DimCustomer.csv`, `DimService.csv`

### Core DAX Measures Included:
```dax
-- On-Time Delivery Rate Percentage
OTD Percentage = 
DIVIDE(
    CALCULATE(SUM(FactShipments[on_time_flag]), FactShipments[shipment_status] <> "Lost / Exception"),
    CALCULATE(COUNTROWS(FactShipments), FactShipments[shipment_status] <> "Lost / Exception"),
    BLANK()
)

-- Quarter-over-Quarter Percentage-Point Change
OTD Percentage-Point Change = 
VAR PrevOTD = CALCULATE([OTD Percentage], PREVIOUSQUARTER(DimDate[FullDate]))
RETURN IF(NOT ISBLANK(PrevOTD), ([OTD Percentage] - PrevOTD) * 100, BLANK())
```

---

## 10. Targeted Operational Action Matrix

| Focus Area | Operational Intervention | Responsible Owner | Measurable SLA Target | Implementation Timeline | Review Cadence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Warehouse Automation** | Overhaul sorting lines at Dhulagarh & Taratala; deploy manual sorting bypass | VP Warehouse Operations | Origin sort dwell < 45 min | 6 Weeks | Weekly |
| **Dynamic Highway Routing** | GPS geofenced rerouting avoiding Kona Expressway during 08:00–12:00 peak | Head of Fleet Dispatch | Arterial transit delay < 40 min | 3 Weeks | Bi-Weekly |
| **Fleet Preventative Care** | 10,000 km mandatory overhaul on aging multi-axles; retire 50 highest-downtime LCVs | Fleet Maintenance Director | Fleet breakdown rate < 1.0% | 8 Weeks | Monthly |
| **Express SLA Pricing** | Calibrate Same-Day delivery window from 6h to 8h in congested zones | Chief Commercial Officer | Same Day OTD $\ge 85.0\%$ | 4 Weeks | Monthly |
| **Early-Warning Deployment**| Operationalize weekly composite risk scoring index with 4-week lead alert | Head of Data & BI | Zero unflagged bottleneck crises | 2 Weeks | Weekly |

---

## 11. Installation & Execution Guide

### Prerequisites
- Python 3.12 64-bit
- Windows, macOS, or Linux

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/Logistics_Root_Cause_Analysis.git
cd Logistics_Root_Cause_Analysis
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run Master End-to-End Pipeline
```bash
python main.py
```
*This executes data generation, quality auditing, cleaning, SQLite modeling, hypothesis testing, driver tree decomposition, early-warning backtesting, Power BI export, PDF memo generation, and notebook creation in ~45 seconds.*

### 3. Run Automated Unit Tests
```bash
pytest tests/ -v
```

### 4. Launch Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 12. Deliverable Verification Checklist

- [x] **4 Synthetic Datasets:** Shipments (347,621), Scans (1,138,153), Routes (132), Vehicles (1,400) totaling ~1.55M records.
- [x] **Hub Mapping Reference Dataset:** `hub_mapping.csv` reconciling network restructuring.
- [x] **Data Dictionary:** Detailed documentation in `documentation/data_dictionary.md`.
- [x] **Data Cleaning Audit:** Auditable trail of transformations in `documentation/cleaning_audit.csv`.
- [x] **SQL Database & Queries:** `kolkata_logistics.db` with relational schema and 10 advanced CTE queries.
- [x] **7 Jupyter Notebooks:** `01_` through `07_` fully structured and executable in `notebooks/`.
- [x] **Reusable Python Modules:** 11 modular scripts in `src/`.
- [x] **Six-Hypothesis Analysis:** Documented in `documentation/hypothesis_log.csv`.
- [x] **12 Publication EDA Visualizations:** High-resolution PNGs in `reports/visualizations/`.
- [x] **Driver Tree Diagram:** Waterfall chart in `reports/driver_tree/driver_tree.png` explaining 92.9% of decline.
- [x] **Weekly Early-Warning System:** Composite risk index backtested with 4-week lead time in `documentation/early_warning_audit.csv`.
- [x] **Streamlit Dashboard:** 6 interactive corporate pages in `dashboard/app.py`.
- [x] **Power BI Exports:** 8 Star-Schema CSVs in `data/power_bi_exports/` with DAX documentation.
- [x] **Two-Page Management Memo:** Executive ReportLab PDF in `reports/management_memo/management_memo.pdf`.
- [x] **Unit Tests:** 13 passed unit tests in `tests/`.
- [x] **Master Orchestrator:** `main.py` executing the entire pipeline seamlessly.

