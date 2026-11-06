# Business Problem Statement: Kolkata Freight & Logistics Performance Intelligence

> **IMPORTANT NOTICE:**  
> This project is based on a fictional freight trucking company operating in Kolkata, West Bengal, India. Actual company datasets have not been supplied. All generated datasets, operational observations, statistical findings, driver trees, and recommendations are entirely **synthetic**. They are designed exclusively for educational, demonstration, and analytical evaluation purposes and must never be interpreted as real-world company findings.

---

## 1. Executive Context & Background

**Kolkata Freight & Logistics (KFL)** is a regional freight trucking and multi-modal logistics enterprise operating across 12 critical logistics hubs in the Greater Kolkata Metropolitan Area, Howrah freight corridor, and key West Bengal arterial highways. The network handles high-volume containerized, palletized, and express cargo for over 3,000 corporate clients, ranging from heavy industrial machinery and chemicals to fast-moving consumer goods (FMCG) and e-commerce parcels.

Over the past two quarters (Q3 and Q4 / second half of the operating year), executive leadership observed a steep and alarming deterioration in headline business performance. Customer churn increased by 18%, contract penalties for missed Service Level Agreements (SLAs) surged by 140%, and customer satisfaction scores dropped precipitously.

---

## 2. Headline Performance Metric: On-Time Delivery Rate (OTD)

To establish an objective, auditable operational north-star metric, the business selected **On-Time Delivery Rate (OTD)** as its provisional headline metric.

### 2.1 Metric Formulation
$$\text{OTD} = \left( \frac{\text{Eligible shipments delivered on or before promised delivery time}}{\text{Total eligible delivered shipments}} \right) \times 100$$

Where:
- $\text{Eligible Delivered Shipments}$ are completed shipments with valid dispatch and delivery confirmation timestamps.
- A shipment is classified as **On-Time** if:
  $$\text{actual\_delivery\_timestamp} \le \text{promised\_delivery\_timestamp}$$
- A shipment is classified as **Delayed** if:
  $$\text{actual\_delivery\_timestamp} > \text{promised\_delivery\_timestamp}$$
- $\text{Delay Duration (Hours)} = \max\left(0, \frac{\text{actual\_delivery\_timestamp} - \text{promised\_delivery\_timestamp}}{3600 \text{ seconds}}\right)$

### 2.2 Operational Benchmark & Observed Decline
- **Internal Target SLA:** $\ge 85.00\%$
- **Baseline Performance (Q1 & Q2):** $\approx 86.40\%$
- **Current Performance (Q3 & Q4):** $\approx 73.60\%$
- **Headline Deterioration:** $-12.80\text{ percentage points (-14.8\% relative decline)}$

### 2.3 Exclusions and Assumptions
1. **Shipments Cancelled Prior to Dispatch:** Excluded from the OTD denominator because no transit SLA was engaged.
2. **Lost / Unresolved Shipments:** Shipments undergoing active insurance or police investigation without a delivery attempt are recorded as "Lost/In-Transit Exception" and analyzed in secondary freight-shrinkage metrics rather than delivery timeliness.
3. **Severe Force Majeure (Red Weather Alerts):** Days with official cyclonic warnings from IMD (India Meteorological Department) or severe flood alerts are tagged, but included in raw baseline audit logs for operational transparency.
4. **Timezone Normalization:** All warehouse scan timestamps and GPS dispatch/delivery events are recorded locally in Indian Standard Time (IST / UTC+05:30) and normalized to UTC for database storage.

---

## 3. Conflicting Management Hypotheses

Executive leadership held divergent views regarding what caused the 12.8 percentage point collapse in OTD:

| Hypothesis ID | Proposed Driver | Management Assertion |
| :--- | :--- | :--- |
| **H1** | **Route Inefficiencies** | Infrastructure construction on NH16, Dankuni bypass, and the Kona Expressway caused severe transit congestion. |
| **H2** | **Vehicle Downtime & Breakdowns** | Fleet maintenance deferrals led to a spike in on-road mechanical breakdowns among aging heavy multi-axle trucks and 14ft LCVs. |
| **H3** | **Warehouse Processing Delays** | Inbound sorting bottlenecks and material-handling conveyor breakdowns at mega-hubs increased dwell times. |
| **H4** | **Disproportionate Hub Deterioration** | Operational breakdowns were not systemic across all 12 hubs, but heavily concentrated in specific problematic facilities (e.g., Dhulagarh, Taratala). |
| **H5** | **Customer & Service Mix Shifts** | A rapid commercial shift toward tight-SLA services ("Same Day Express" and "Express Cargo") strained fulfillment capacity. |
| **H6** | **Seasonal Shipment Demand Fluctuations** | The annual Durga Puja / Diwali festival volume surge in Q3 overwhelmed network handling capacity. |

---

## 4. Analytical Objectives & Scope

1. **End-to-End Data Pipeline:** Ingest, inspect, reconcile, and clean over 1.5 million records across shipments, routes, vehicles, and warehouse scans.
2. **Database Integration:** Model relational data into a high-performance SQLite analytical data warehouse with star schema export capability.
3. **Exploratory Data Analysis:** Visualize temporal, geographic, fleet, and operational distributions across all 12 hubs.
4. **Rigorous Hypothesis Testing:** Apply two-sample t-tests, Chi-square tests, correlation analysis, and regression modeling to test each hypothesis against data.
5. **Driver Tree Decomposition:** Attribute the headline drop across operational drivers, aiming to explain $\ge 80\%$ of the observed decline.
6. **Early-Warning & Monitoring System:** Build a weekly alerting mechanism to detect leading indicators of operational distress $\ge 4$ weeks before headline OTD deteriorates.
7. **Interactive Intelligence Platform:** Deploy a corporate Streamlit dashboard and generate a two-page executive management memo.

