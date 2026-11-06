# Methodology & Analytical Framework: Kolkata Freight Performance Intelligence

> **Classification:** Technical & Methodological Documentation  
> **Authors:** Senior Analytics Engineering & Statistical Intelligence Team

---

## 1. End-to-End Analytical Architecture

The project implements a rigorous seven-stage data intelligence workflow:

```
[Raw Disparate Feeds (~1.55M Records)]
       │
       ▼
[Stage 1: Automated Data Quality Auditing] ──► Flagging 10 Controlled Flaws
       │
       ▼
[Stage 2: Deterministic Cleaning & Reconciliation] ──► Audit Log (cleaning_audit.csv)
       │
       ▼
[Stage 3: SQLite Relational Analytical Warehouse] ──► Star Schema & CTE Queries
       │
       ▼
[Stage 4: Exploratory Data Analysis & Visualizations] ──► 12 Domain Charts
       │
       ▼
[Stage 5: Inferential Statistical Hypothesis Testing] ──► H1 to H6 (t-test, Chi², OLS, Logit)
       │
       ▼
[Stage 6: Counterfactual Driver Tree Decomposition] ──► Explaining >= 80% Decline
       │
       ▼
[Stage 7: Early-Warning Monitoring & BI Dashboard] ──► Streamlit, Power BI, PDF Memo
```

---

## 2. Controlled Data Quality Auditing Methodology

In accordance with enterprise data engineering standards, incoming operational data is never ingested directly into reporting. Ten specific data quality flaws are audited and quarantined:

1. **Entity Duplication:** Exact and composite duplicate detection on `(shipment_id, dispatch_timestamp)` and `(scan_id)`.
2. **Missing Delivery Outcomes:** Shipments missing physical delivery timestamps are segregated and categorized as "In-Transit" or "Investigating Exception".
3. **Legacy Entity Resolution:** Tracking facility ID changes via `hub_mapping.csv` to ensure historical continuity (e.g. mapping `HUB_KNA` / `HUB_KEX_OLD` to `HUB_KEX`).
4. **Out-of-Order Lifecycle Scans:** Chronological sequence verification ensuring `ORIGIN_SORT` < `DISPATCH` < `DESTINATION_ARRIVAL` < `DELIVERY`.
5. **Timezone Discrepancy & Standardization:** Parsing heterogeneous timestamp formats (ISO 8601 with `+05:30` IST offset, Zulu `Z`, local strings) and converting deterministically to UTC.
6. **Chronological Invalidation:** Quarantining records where delivery timestamp precedes dispatch timestamp, or dates exist in invalid future epochs.
7. **Categorical Normalization:** Fuzzy and dictionary mapping of dirty strings (`"std surface"` $\to$ `"Standard Surface"`, `"EXP_CARGO"` $\to$ `"Express Cargo"`).
8. **Referential Integrity Validation:** Cross-table foreign key validation between `fact_shipments` and dimension tables (`dim_vehicles`, `dim_routes`, `dim_customers`).
9. **String-to-Numeric Sanitization:** Stripping currency symbols (`"INR "`) and unit markers (`" kg"`) using regex before casting to IEEE 754 floating point numbers.
10. **Audit Logging:** Every transformation is logged with `original_records`, `records_affected`, `records_retained`, `records_excluded`, and `reason` in `cleaning_audit.csv`.

---

## 3. Statistical Testing Framework (Hypotheses H1–H6)

We define a formal null ($H_0$) and alternative ($H_1$) hypothesis for each potential driver:

### H1: Route Inefficiencies
- **Question:** Did transit delays on major arterial corridors (e.g., NH16, Kona Expressway) drive the increase in delivery delays?
- **Methods:** Two-sample Welch's t-test comparing transit delays on affected vs unaffected corridors; Multiple linear regression with route-fixed effects.
- **Significance Level:** $\alpha = 0.05$.

### H2: Vehicle Downtime & Breakdowns
- **Question:** Did fleet mechanical downtime and roadside breakdowns significantly lower on-time delivery likelihood?
- **Methods:** Binomial Logistic Regression predicting $P(\text{Delayed})$ from `downtime_hours` and `breakdown_count`; Odds Ratio estimation with 95% CI.

### H3: Warehouse Processing Delays
- **Question:** Did sorting duration and scanning bottlenecks at mega-hubs increase consignment turnaround time?
- **Methods:** Independent sample t-test and Wilcoxon rank-sum test of processing durations between baseline and decline periods; Pearson/Spearman correlation between warehouse dwell time and total delay.

### H4: Disproportionate Hub-Level Deterioration
- **Question:** Was performance degradation concentrated in specific hubs (Dhulagarh, Taratala) rather than uniform across all 12 facilities?
- **Methods:** One-Way ANOVA across 12 hubs followed by Tukey's HSD post-hoc test; Chi-square test of independence for delivery outcome by hub.

### H5: Customer & Service-Type Mix Shifts
- **Question:** Did an increased proportion of high-speed, tight-SLA services (Same Day Express, Express Cargo) account for the drop in overall OTD?
- **Methods:** Chi-square test of service-type distributions across quarters; Counterfactual standardization isolating mix-shift vs within-service rate changes.

### H6: Seasonal Demand Surge
- **Question:** Did the Durga Puja / Diwali festival volume surge account for the headline performance decline?
- **Methods:** Interrupted time series and pre/peak/post festival segment comparison. Testing whether OTD rebounded to baseline post-festival (rejection of pure seasonality if performance remains depressed).

---

## 4. Driver Tree & Counterfactual Decomposition Methodology

To break down the decline in OTD from Baseline ($OTD_{\text{base}}$) to Current ($OTD_{\text{curr}}$):
$$\Delta OTD = OTD_{\text{curr}} - OTD_{\text{base}}$$

We employ a **Counterfactual Standardization & Attribution Model**:
1. **Mix-Shift Effect (Service & Customer Mix):**
   $$\Delta_{\text{mix}} = \sum_s (w_{s,\text{curr}} - w_{s,\text{base}}) \times OTD_{s,\text{base}}$$
   Where $w_s$ is the volume share of service category $s$.
2. **Within-Category Operational Shift (Rate Effect):**
   $$\Delta_{\text{rate}} = \sum_s w_{s,\text{curr}} \times (OTD_{s,\text{curr}} - OTD_{s,\text{base}})$$
3. **Factor Attribution Decomposition:**
   Within $\Delta_{\text{rate}}$, we compute marginal contribution of:
   - Warehouse sorting bottleneck ($\Delta_{\text{wh}}$)
   - Highway corridor congestion ($\Delta_{\text{route}}$)
   - Vehicle mechanical breakdowns ($\Delta_{\text{veh}}$)
   - Festive surge strain ($\Delta_{\text{festive}}$)
   - Unexplained residual ($\epsilon$)

**Decomposition Constraint:**
$$\sum \text{Explained Drivers} + \epsilon = \Delta OTD$$
Targeting $\ge 80\%$ explained variance without double counting.

---

## 5. Early-Warning & Backtesting Methodology

The Weekly Early-Warning System monitors five leading and concurrent operational metrics:
1. Hub-level Warehouse Sorting Duration (Z-score vs 4-week rolling mean)
2. Corridor Transit Delay Deviation
3. Fleet Breakdown Incident Rate per 1,000 km
4. Volume-to-Design-Capacity Ratio
5. Rolling 3-Week OTD Slope

### Alert Thresholds:
- **Normal (Green):** Composite Risk Score $< 1.0$
- **Watch (Yellow):** $1.0 \le \text{Score} < 2.0$ (Leading indicators elevated, OTD intact)
- **Warning (Orange):** $2.0 \le \text{Score} < 3.0$ (Significant localized bottlenecks)
- **Critical (Red):** $\text{Score} \ge 3.0$ (Systemic operational failure)

### Backtesting Protocol:
- Historical simulation over Weeks 1–52.
- Evaluate alert trigger dates against the structural deterioration date (Week 27).
- Quantify Warning Lead Time (Target $\ge 4$ weeks), False Alert Rate, Precision, and Recall.

