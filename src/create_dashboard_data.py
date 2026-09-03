import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent

raw_file = PROJECT_DIR / "data" / "raw" / "fact_operations.csv"
processed_dir = PROJECT_DIR / "data" / "processed"

processed_dir.mkdir(exist_ok=True)

df = pd.read_csv(raw_file)

kpis = pd.DataFrame({
    "Total Operations": [len(df)],
    "Total Quantity": [df["quantity"].sum()],
    "SLA Compliance %": [(~df["sla_breached"]).mean() * 100],
    "SLA Breach Rate %": [df["sla_breached"].mean() * 100],
    "Average Processing Hours": [df["processing_time_hours"].mean()],
    "Average Delay Minutes": [df["delay_minutes"].mean()],
    "Total Cost": [df["cost"].sum()],
    "Average Quality Score": [df["quality_score"].mean()],
    "Cost per Operation": [df["cost"].mean()]
})

kpis.to_csv(
    processed_dir / "executive_kpis.csv",
    index=False
)

print("Created executive_kpis.csv")
print(kpis)