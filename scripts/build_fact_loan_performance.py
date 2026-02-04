import csv

print("🔥🔥🔥 THIS IS THE ONLY FACT SCRIPT I AM RUNNING 🔥🔥🔥")

# =====================
# 路径配置
# =====================
APPLICATIONS_PATH = "data/raw/raw_loan_applications.csv"
OUTCOMES_PATH = "data/raw/raw_loan_outcomes.csv"
OUTPUT_PATH = "data/mart/fact_loan_performance.csv"

# =====================
# 读取 raw applications
# =====================
with open(APPLICATIONS_PATH, "r") as f:
    applications = list(csv.DictReader(f))

# =====================
# 读取 raw outcomes（做成 dict 方便 join）
# =====================
with open(OUTCOMES_PATH, "r") as f:
    outcomes = {
        row["application_id"]: row
        for row in csv.DictReader(f)
    }

fact_rows = []

# =====================
# join + 计算 fact
# =====================
for app in applications:
    application_id = app["application_id"]
    outcome = outcomes.get(application_id)

    if outcome is None:
        continue

    approved = int(outcome["approved_flag"])
    funded_amount = float(outcome["funded_amount"])
    interest_rate = float(app["interest_rate"])

    # -------- risk band 规则 --------
    if interest_rate <= 0.08:
        risk_band = "LOW"
    elif interest_rate <= 0.10:
        risk_band = "MEDIUM"
    else:
        risk_band = "HIGH"

    # -------- 金额计算 --------
    if approved:
        expected_total_payment = round(funded_amount * (1 + interest_rate), 2)
        expected_interest = round(expected_total_payment - funded_amount, 2)
    else:
        expected_total_payment = 0
        expected_interest = 0

    fact_rows.append({
        "application_id": application_id,
        "customer_id": app["customer_id"],
        "apply_date": app["apply_date"],
        "channel": app["channel"],
        "requested_amount": float(app["requested_amount"]),
        "term_months": int(app["term_months"]),
        "interest_rate": interest_rate,
        "risk_band": risk_band,
        "approved_flag": approved,
        "funded_amount": funded_amount,
        "default_flag": int(outcome["default_flag"]),
        "final_status": outcome["final_status"],
        "expected_total_payment": expected_total_payment,
        "expected_interest": expected_interest
    })

# =====================
# 写出 fact 表
# =====================
if not fact_rows:
    raise ValueError("❌ fact_rows is empty, no data generated")

with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fact_rows[0].keys())
    writer.writeheader()
    writer.writerows(fact_rows)

print(f"✅ SUCCESS: Built {len(fact_rows)} rows → {OUTPUT_PATH}")
