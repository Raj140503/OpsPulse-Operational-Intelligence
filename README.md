# OpsPulse – Operational Intelligence Platform

## Overview

**OpsPulse** is an end-to-end Operational & Performance Intelligence Platform designed to analyze business operations, identify bottlenecks, diagnose root causes of delays, and support data-driven resource allocation.

The project combines **Python, PostgreSQL, SQL, and Power BI** to transform synthetic operational data into management-ready insights.

## 🚀 Live Dashboard

**Streamlit App:** https://opspulse-operational-intelligence.streamlit.app/

**GitHub Repository:**  
https://github.com/Raj140503/OpsPulse-Operational-Intelligence

---


### Business Questions

- How efficiently is the business operating?
- Where are the major operational bottlenecks?
- Which stages contribute most to delays?
- How does employee experience affect performance?
- How does workload pressure influence delays?
- Which experience × workload combinations have the highest risk?
- How do operational delays relate to quality and cost?
- Where should management prioritize improvement efforts?

---

## Project Architecture

```text
OpsPulse Operational Intelligence/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   ├── generate_data.py
│   ├── generate_stage_data.py
│   ├── validation.py
│   └── validate_stage_data.py
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_load_data.sql
│   ├── 03_operational_kpis.sql
│   └── 04_powerbi_views.sql
├── dashboard/
│   └── OpsPulse_Operational_Intelligence.pbix
├── documents/
│   └── quality_check_bottleneck.png
└── README.md
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Data Generation | Faker |
| Visualization | Matplotlib |
| Database | PostgreSQL |
| Analytics | SQL, CTEs, aggregations |
| BI | Power BI |
| BI Modeling | DAX, Power Query |
| Version Control | Git / GitHub |

---

## Data Model

### Dimension Tables

- **dim_date** – calendar attributes for time analysis
- **dim_customer** – customer information
- **dim_product** – product information
- **dim_employee** – department, team, and experience information
- **dim_location** – operational location information

### Fact Tables

- **fact_operations** – operational transaction-level data
- **fact_operation_stages** – stage-level execution data

Each operation contains four stages:

1. Processing
2. Quality Check
3. Packaging
4. Dispatch

The project contains **150,000 operations** and **600,000 stage records**.

---

## Data Validation

The dataset was validated before analysis.

Validation includes:

- Missing-value checks
- Duplicate checks
- Primary-key validation
- Foreign-key validation
- Numeric range validation
- Date validation
- Timestamp sequence validation
- SLA logic validation
- Stage-to-operation relationship validation
- Four-stage completeness validation

All core validation checks passed.

---

## Python & EDA

`notebooks/01_eda.ipynb` performs:

- Operational KPI analysis
- Monthly trends
- Department performance
- Employee experience analysis
- Location analysis
- Workload analysis
- Stage-level performance
- Bottleneck identification
- Workload × bottleneck analysis
- Quality Check RCA
- Experience × workload RCA
- Correlation analysis
- Management RCA prioritization

Processed analytical datasets are stored in `data/processed/`.

---

## PostgreSQL & SQL Analytics

The PostgreSQL layer contains the dimensional model and analytical queries.

The SQL layer covers:

- Operational KPI calculations
- Monthly performance
- Department performance
- Bottleneck analysis
- Employee experience analysis
- Workload analysis
- Experience × workload RCA

Power BI uses these PostgreSQL views:

- `vw_operations_overview`
- `vw_stage_performance`
- `vw_experience_workload_rca`

---

# Power BI Dashboards

The Power BI report contains **five dashboard pages**.

## 1. Executive Overview

Provides a high-level operational view with:

- Total Operations
- SLA Compliance %
- Average Processing Hours
- Average Delay Minutes
- Total Cost
- Average Quality Score
- Monthly Operations Trend
- Monthly SLA Compliance Trend
- Average Processing Time by Department
- SLA Compliance by Department
- Year filtering

---

## 2. Bottleneck & Root Cause Analysis

Focuses on identifying where delays originate and what factors are associated with them.

Includes:

- Stage Duration vs Target
- Stage Delay Rate
- Experience × Workload Delay Rate Matrix
- Delay Rate by Workload Level
- Average Operational Delay
- Cost per Operation
- Average Quality Score

The analysis identifies **Quality Check** as the primary process bottleneck.

---

## 3. Workforce & Productivity

Analyzes workforce performance and operational productivity.

Includes:

- Total Operations
- Average Processing Time by Experience Level
- SLA Compliance by Experience Level
- Operations by Workload Level
- Delay Rate by Workload Level
- Average Processing Time
- Cost per Operation

---

## 4. Quality & Cost Analysis

Examines relationships between quality and operational cost.

Includes:

- Average Quality Score
- Total Operational Cost
- Quality Score vs Operational Cost
- Cost per Operation
- Average Quality Score by Department
- Total Operational Cost by Department

---

## 5. Management Insights

Provides management-oriented KPIs and decision support.

Includes:

- SLA Breach Rate
- Cost per Operation
- High-Risk Experience & Workload Combinations
- Average Operational Delay
- Average Quality Score
- Management recommendations

### Key Management Priorities

- Optimize the **Quality Check** stage.
- Reduce delays during **Very High and Extreme workload** periods.
- Provide additional support and training for **Junior employees**.
- Prioritize **Junior + Extreme workload** operations.
- Balance operational speed with quality and cost performance.

---

# Key KPIs

Baseline results from the generated operational dataset:

| KPI | Result |
|---|---:|
| Total Operations | 150,000 |
| Total Quantity | 1,179,390 |
| SLA Compliance | 78.16% |
| SLA Breach Rate | 21.84% |
| Average Processing Time | 4.54 hours |
| Average Delay | 17.61 minutes |
| Average Quality Score | 90.07 |
| Total Cost | 36.89M |
| Cost per Operation | 245.94 |
| Cost per Unit | 31.28 |
| Average Workload | 8.65 |

---

# Bottleneck Analysis

The **Quality Check** stage is the primary operational bottleneck.

| Stage | Avg Duration (min) | Target (min) | Variance (min) | Delay Rate |
|---|---:|---:|---:|---:|
| Quality Check | 110.47 | 75 | +35.47 | 59.00% |
| Packaging | 48.54 | 45 | +3.54 | 41.77% |
| Processing | 80.79 | 90 | -9.21 | 31.88% |
| Dispatch | 32.36 | 40 | -7.64 | 26.65% |

Quality Check averages approximately **47% above its target duration**.

---

# Root Cause Analysis

## Employee Experience

| Experience | Delay Rate | Avg QC Duration |
|---|---:|---:|
| Junior | 69.07% | 131.61 min |
| Mid | 56.84% | 104.69 min |
| Senior | 47.76% | 89.79 min |

## Workload Pressure

Quality Check delay rates increase across workload bands:

| Workload Band | Delay Rate |
|---|---:|
| Low | 51.61% |
| Moderate | 57.36% |
| High | 63.97% |
| Very High | 70.47% |
| Extreme | 76.24% |

The Low → Extreme increase is approximately **24.6 percentage points**.

## Experience × Workload

The highest-risk combination observed was:

**Junior + Extreme workload → 83.82% delay rate**

This supports targeted workload balancing, experienced-resource allocation, and additional support for less-experienced employees during high-pressure periods.

---

# Correlation Findings

| Relationship | Correlation |
|---|---:|
| Quality Check Duration ↔ Quality Score | -0.80 |
| Quality Check Duration ↔ Cost | +0.88 |
| Workload ↔ Quantity | +0.92 |
| Workload ↔ Quality Check Duration | +0.14 |

These values indicate **association, not causation**.

The results suggest that Quality Check duration is strongly associated with both quality and cost, while workload alone is not a strong linear predictor of individual Quality Check duration.

---

# Recommended Management Actions

### 1. Optimize Quality Check

- Review QC process steps and queues.
- Reduce avoidable waiting time.
- Monitor stage-level performance.

### 2. Improve Resource Allocation

- Allocate experienced employees during high-pressure periods.
- Balance workload across teams.

### 3. Support Junior Employees

- Provide targeted training.
- Improve SOP and process guidance.
- Add support during high-workload periods.

### 4. Monitor Workload Thresholds

- Track Very High and Extreme workload conditions.
- Investigate high-risk operations.

### 5. Balance Quality, Cost & Speed

- Monitor Quality Check duration alongside quality score and cost.
- Avoid reducing processing time at the expense of quality.

---

# How to Run

## 1. Generate Data

From the project root:

```bash
python src/generate_data.py
python src/generate_stage_data.py
```

## 2. Validate Data

```bash
python src/validation.py
python src/validate_stage_data.py
```

## 3. Run EDA

```bash
jupyter notebook
```

Open:

```text
notebooks/01_eda.ipynb
```

## 4. PostgreSQL

Run:

```text
sql/01_create_schema.sql
sql/03_operational_kpis.sql
sql/04_powerbi_views.sql
```

Load the generated CSV files into the corresponding PostgreSQL tables.

## 5. Power BI

Open:

```text
dashboard/OpsPulse_Operational_Intelligence.pbix
```

Update the PostgreSQL connection if required and refresh the model.

---

# Portfolio Value

This project demonstrates practical experience with:

- Python data analysis
- Data generation and validation
- Pandas and NumPy
- PostgreSQL
- Advanced SQL
- Dimensional data modeling
- KPI development
- Root Cause Analysis
- Statistical correlation
- Power BI
- DAX
- Power Query
- Interactive dashboard development
- Operational decision support
- Git/GitHub

It demonstrates an end-to-end workflow from **raw operational data → validated datasets → SQL analytics → RCA → Power BI dashboards → management recommendations**.

---

## Disclaimer

This project uses **synthetically generated data** for educational and portfolio purposes. The operational patterns, KPIs, correlations, and recommendations are simulated and should not be interpreted as real-world business results.
