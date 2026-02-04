import csv
import random
from datetime import date, timedelta

# ===== 配置输出路径 =====
OUTPUT_PATH = "data/raw/raw_loan_applications.csv"

# ===== 一些基础参数 =====
NUM_ROWS = 50

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

rows = []

for i in range(NUM_ROWS):
    rows.append({
        "application_id": f"APP_{i+1}",
        "customer_id": f"CUST_{random.randint(1, 20)}",
        "apply_date": random_date(
            date(2023, 1, 1),
            date(2023, 12, 31)
        ).isoformat(),
        "requested_amount": random.choice([5000, 10000, 20000, 50000]),
        "term_months": random.choice([12, 24, 36]),
        "interest_rate": random.choice([0.08, 0.1, 0.12]),
        "channel": random.choice(["web", "partner", "sales"])
    })

# ===== 写入 CSV =====
with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Generated {len(rows)} rows → {OUTPUT_PATH}")
