
import pandas as pd
import numpy as np
import os
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
DATA_DIR = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

FILES = {
    "finance": "truck-finance.xlsx",
    "maintenance": "maintenancepo-truck.xlsx",
    "distance": "vehicle-distance-traveled.xlsx",
    "odometer": "truck-odometer-data-week-.xlsx",
    "stub": "stub-data.xlsx",
    "market": "truck-paper.xlsx"
}

def load_data(file_key, filename):
    """
    Loads the second sheet (index 1) of the Excel file.
    Assumes first sheet is descriptive text.
    """
    path = os.path.join(DATA_DIR, filename)
    print(f"Loading {file_key} from {filename}...")
    try:
        # User specified: Data is in the second sheet (index 1)
        df = pd.read_excel(path, sheet_name=1)
        
        # Basic cleanup: Strip whitespace from column names
        df.columns = df.columns.astype(str).str.strip()
        
        print(f"  -> Loaded {len(df)} rows. Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"  [ERROR] Failed to load {filename}: {e}")
        return None

def main():
    print("--- Starting Fleet Value Analysis ---")
    
    # 1. Load Data
    finance_df = load_data("finance", FILES["finance"])
    maintenance_df = load_data("maintenance", FILES["maintenance"])
    distance_df = load_data("distance", FILES["distance"])
    odometer_df = load_data("odometer", FILES["odometer"])
    stub_df = load_data("stub", FILES["stub"])
    market_df = load_data("market", FILES["market"])
    
    # Validation
    if finance_df is None:
        print("[CRITICAL] Finance data missing. Exiting.")
        return

    print("\n--- Step 1 Complete: Data Loaded ---")

if __name__ == "__main__":
    main()
