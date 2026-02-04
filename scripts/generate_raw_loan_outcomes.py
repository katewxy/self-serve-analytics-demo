import csv
import random

# ===== 输入 & 输出路径 =====
INPUT_PATH = "data/raw/raw_loan_applications.csv"
OUTPUT_PATH = "data/raw/raw_loan_outcomes.csv"

rows = []

# 读取 applications，保证一一对应
with open(INPUT_PATH, "r") as f:
    reader = csv.DictReader(f)
    applications = list(reader)

for app in applications:
    approved = random.random() < 0.7  # 70% 通过率

    rows.append({
        "application_id": app["application_id"],
        "approved_flag": int(approved),
        "funded_amount": int(app["requested_amount"]) if approved else 0,
        "default_flag": int(approved and random.random() < 0.08),
        "final_status": (
            "funded" if approved else random.choice(["declined", "withdrawn"])
        )
    })

# 写入 CSV
with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Generated {len(rows)} rows → {OUTPUT_PATH}")
