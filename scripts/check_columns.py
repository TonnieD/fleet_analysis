
import pandas as pd
import os

data_dir = r'c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data'
files = [
    "truck-finance.xlsx",
    "maintenancepo-truck.xlsx",
    "vehicle-distance-traveled.xlsx",
    "truck-odometer-data-week-.xlsx",
    "stub-data.xlsx",
    "truck-paper.xlsx"
]

for f in files:
    path = os.path.join(data_dir, f)
    try:
        df = pd.read_excel(path, nrows=0)
        print(f"--- {f} ---")
        print(list(df.columns))
        print("\n")
    except Exception as e:
        print(f"Error reading {f}: {e}")
