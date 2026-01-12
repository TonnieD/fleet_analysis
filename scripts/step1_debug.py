
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data\truck-finance.xlsx"
print(f"Reading {path}...")
try:
    df = pd.read_excel(path, nrows=2)
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"Error: {e}")
