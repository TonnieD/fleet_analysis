
import pandas as pd
import os
import sys

# Set up output to handle encoding usually
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

def load_and_inspect():
    print("--- Data Inspection ---")
    for key, filename in files.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            print(f"[MISSING] {filename}")
            continue
            
        try:
            # Read first few rows to get columns
            df = pd.read_excel(path, nrows=2)
            print(f"\n[{key.upper()}] {filename}")
            print(f"Columns: {list(df.columns)}")
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")

if __name__ == "__main__":
    load_and_inspect()
