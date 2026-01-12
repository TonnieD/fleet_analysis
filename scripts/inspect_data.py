
import pandas as pd
import os

data_dir = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"

files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx')]

for f in files:
    path = os.path.join(data_dir, f)
    print(f"--- Analyzing {f} ---")
    try:
        xl = pd.ExcelFile(path)
        print(f"Sheets: {xl.sheet_names}")
        
        # Try to load the most relevant sheet (heuristically not 'Sheet1' if others exist, or just the first one)
        # The user's notebook used sheet_name=1. Let's try to see what's in both if possible, or just the 2nd one if it exists.
        
        for sheet in xl.sheet_names:
            print(f"  > Sheet: {sheet}")
            df = pd.read_excel(path, sheet_name=sheet, nrows=5)
            print(f"    Columns: {list(df.columns)}")
            print(f"    Shape (preview): {df.shape}")
            print(df.head(2).to_string())
            print("\n")
            
    except Exception as e:
        print(f"Error reading {f}: {e}")
    print("="*50 + "\n")
