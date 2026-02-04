import csv
from collections import defaultdict

print("🔥 RUNNING MART LOAN METRICS BY RISK 🔥")

INPUT_PATH = "data/mart/fact_loan_performance.csv"
OUTPUT_PATH = "data/mart/mart_loan_metrics_by_risk.csv"

# ===== 容器 =====
metrics = defaultdict(lambda: {
    "applications": 0,
    "approvals": 0,
    "defaults": 0,
    "loan_amount_sum": 0.0
})

# ===== 读取 fact 表 =====
with open(INPUT_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        risk = row["risk_band"]
        approved = int(row["approved_flag"])
        defaulted = int(row["default_flag"])
        loan_amount = float(row["requested_amount"])

        metrics[risk]["applications"] += 1

        if approved:
            metrics[risk]["approvals"] += 1
            metrics[risk]["loan_amount_sum"] += loan_amount

            if defaulted:
                metrics[risk]["defaults"] += 1

# ===== 写出 mart 表 =====
with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "risk_band",
        "applications",
        "approvals",
        "approval_rate",
        "defaults",
        "default_rate",
        "avg_loan_amount"
    ])

    for risk, m in metrics.items():
        applications = m["applications"]
        approvals = m["approvals"]
        defaults = m["defaults"]

        approval_rate = approvals / applications if applications > 0 else 0
        default_rate = defaults / approvals if approvals > 0 else 0
        avg_loan_amount = (
            m["loan_amount_sum"] / approvals if approvals > 0 else 0
        )

        writer.writerow([
            risk,
            applications,
            approvals,
            round(approval_rate, 2),
            defaults,
            round(default_rate, 2),
            round(avg_loan_amount, 2)
        ])

print("✅ mart_loan_metrics_by_risk.csv generated")
