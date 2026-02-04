# Self-Serve Analytics Demo (SMB Lending)

## Project Overview
This project demonstrates an end-to-end analytics data pipeline for a small business lending use case.

Starting from raw loan application and outcome data, the pipeline builds:
- a loan-level fact table with derived performance metrics
- a risk-level analytics mart designed for self-serve analytics and business reporting

The project simulates real-world analytics engineering workflows, including schema design, metric definition, and reproducible ETL logic using Python.

---

## Business Context
Small business lending teams need to monitor portfolio performance across different risk segments, including approval rates, default rates, and loan sizes.

These insights are commonly consumed by risk, finance, and product stakeholders via dashboards or self-serve analytics tools.

---

## Data Pipeline & Model

### Raw Layer
- `raw_loan_applications.csv`
- `raw_loan_outcomes.csv`

### Fact Layer
- `fact_loan_performance.csv`
- Grain: one row per loan application
- Includes derived fields such as:
  - `risk_band`
  - `expected_total_payment`
  - `expected_interest`

### Mart Layer
- `mart_loan_metrics_by_risk.csv`
- Grain: one row per risk band
- Metrics include:
  - approval rate
  - default rate
  - average loan amount

Pipeline flow:
raw_loan_applications + raw_loan_outcomes
↓
fact_loan_performance
↓
mart_loan_metrics_by_risk

## Metric Definitions

- **Approval Rate** = number of approved loans / number of applications  
- **Default Rate** = number of defaulted loans / number of approved loans  
- **Average Loan Amount** = average funded amount per loan  

---

## Project Structure

data/
- raw/  
  - raw_loan_applications.csv  
  - raw_loan_outcomes.csv  
- mart/  
  - fact_loan_performance.csv  
  - mart_loan_metrics_by_risk.csv  

scripts/
- generate_raw_loan_applications.py  
- generate_raw_loan_outcomes.py  
- build_fact_loan_performance.py  
- build_mart_loan_metrics_by_risk.py  

---

## How to Run

1. Generate raw data:
python3 scripts/generate_raw_loan_applications.py
python3 scripts/generate_raw_loan_outcomes.py

2. Build fact table:
python3 scripts/build_fact_loan_performance.py

3. Build mart table:

3. Build mart table:
python3 scripts/build_mart_loan_metrics_by_risk.py

All output CSV files will be created under the `data/` directory.
