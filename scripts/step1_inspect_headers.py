
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"
files = ["truck-finance.xlsx", "maintenancepo-truck.xlsx"]

for f in files:
    path = os.path.join(data_dir, f)
    print(f"--- {f} Head (header=None) ---")
    try:
        df = pd.read_excel(path, header=None, nrows=5)
        print(df.to_string())
    except Exception as e:
        print(e)
    print("\n")
