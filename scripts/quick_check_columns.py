
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"
files = {
    "finance": "truck-finance.xlsx",
    "maintenance": "maintenancepo-truck.xlsx",
    "distance": "vehicle-distance-traveled.xlsx",
    "odometer": "truck-odometer-data-week-.xlsx",
    "stub": "stub-data.xlsx",
    "market": "truck-paper.xlsx"
}

for k, f in files.items():
    print(f"Checking {k}...")
    try:
        df = pd.read_excel(os.path.join(data_dir, f), sheet_name=1, nrows=0)
        print(f"COLUMNS {k}: {list(df.columns)}")
    except Exception as e:
        print(f"Error {k}: {e}")
