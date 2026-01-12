
import pandas as pd
import os

data_dir = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"

def inspect_file(filename):
    path = os.path.join(data_dir, filename)
    print(f"--- Top 5 rows of {filename} ---")
    try:
        # Load all sheets to be sure
        xl = pd.ExcelFile(path)
        for sheet in xl.sheet_names:
            print(f"Sheet: {sheet}")
            df = pd.read_excel(path, sheet_name=sheet, nrows=5)
            print(f"Columns: {list(df.columns)}")
            print(df.to_string())
            print("\n")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

print("Comparing files for Unit ID discovery...\n")
inspect_file("truck-finance.xlsx")
inspect_file("truck-paper.xlsx")
