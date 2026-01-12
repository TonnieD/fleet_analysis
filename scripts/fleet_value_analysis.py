
import pandas as pd
import numpy as np
import os
import sys
import logging

# --- CONFIGURATION ---
DATA_DIR = r"c:\Users\ngang\OneDrive\Desktop\Projects\Data Science\fleet_analysis\data"
LOG_FILE = os.path.join(DATA_DIR, "analysis_log.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "fleet_value_report.csv")

# Setup Logging
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

FILES = {
    "finance": "truck-finance.xlsx",
    "maintenance": "maintenancepo-truck.xlsx",
    "distance": "vehicle-distance-traveled.xlsx",
    "odometer": "truck-odometer-data-week-.xlsx",
    "stub": "stub-data.xlsx",
    "market": "truck-paper.xlsx"
}

def load_data(file_key, filename):
    path = os.path.join(DATA_DIR, filename)
    logging.info(f"Loading {file_key} from {filename}...")
    try:
        # Load Sheet 2 (Index 1)
        # Assuming header is row 0 of that sheet
        df = pd.read_excel(path, sheet_name=1)
        df.columns = df.columns.astype(str).str.strip()
        logging.info(f"  -> Loaded {len(df)} rows. Columns: {list(df.columns)}")
        return df
    except Exception as e:
        logging.error(f"  [ERROR] Failed to load {filename}: {e}")
        return None

def main():
    logging.info("--- Starting Fleet Value Analysis ---")
    
    # 1. Load Data
    finance_df = load_data("finance", FILES["finance"])
    maintenance_df = load_data("maintenance", FILES["maintenance"])
    distance_df = load_data("distance", FILES["distance"])
    # odometer_df = load_data("odometer", FILES["odometer"]) # Used for sanity check only
    stub_df = load_data("stub", FILES["stub"])
    market_df = load_data("market", FILES["market"])
    
    if finance_df is None:
        logging.critical("Finance data missing. Exiting.")
        return

    # 2. Operations (Distance & Revenue)
    logging.info("Processing Operations Data...")
    
    # Revenue
    revenue_agg = pd.DataFrame(columns=['Unit ID', 'Total_Revenue', 'Stub_Count'])
    if stub_df is not None:
        try:
            stub_df['Unit ID'] = stub_df['TRUCK'].astype(str).str.strip()
            stub_df['Revenue'] = pd.to_numeric(stub_df['TRUCK CHARGE'], errors='coerce').fillna(0)
            revenue_agg = stub_df.groupby('Unit ID').agg(
                Total_Revenue=('Revenue', 'sum'),
                Stub_Count=('Revenue', 'count')
            ).reset_index()
        except Exception as e:
            logging.error(f"Error processing stub data: {e}")

    # Distance
    usage_agg = pd.DataFrame(columns=['Unit ID', 'Total_Miles', 'Active_Days', 'Avg_Miles_Active_Day'])
    if distance_df is not None:
        try:
            distance_df['Unit ID'] = distance_df['unit_id'].astype(str).str.strip()
            distance_df['Date'] = pd.to_datetime(distance_df['date'], errors='coerce')
            distance_df['Distance'] = pd.to_numeric(distance_df['distance'], errors='coerce').fillna(0)
            
            # Last 10 weeks
            max_date = distance_df['Date'].max()
            if pd.notnull(max_date):
                cutoff = max_date - pd.Timedelta(days=70)
                recent = distance_df[distance_df['Date'] > cutoff]
                usage_agg = recent.groupby('Unit ID').agg(
                    Total_Miles=('Distance', 'sum'),
                    Active_Days=('Distance', lambda x: (x > 0).sum())
                ).reset_index()
                usage_agg['Avg_Miles_Active_Day'] = usage_agg['Total_Miles'] / usage_agg['Active_Days'].replace(0, 1)
        except Exception as e:
            logging.error(f"Error processing distance data: {e}")

    # 3. Finance & Maintenance
    logging.info("Processing Finance & Maintenance...")
    
    # Maintenance
    maint_agg = pd.DataFrame(columns=['Unit ID', 'Total_Repair_Cost', 'Repair_Count'])
    if maintenance_df is not None:
        try:
            maintenance_df['Unit ID'] = maintenance_df['unit_id'].astype(str).str.strip()
            maintenance_df['Cost'] = pd.to_numeric(maintenance_df['amount'], errors='coerce').fillna(0)
            maint_agg = maintenance_df.groupby('Unit ID').agg(
                Total_Repair_Cost=('Cost', 'sum'),
                Repair_Count=('Cost', 'count')
            ).reset_index()
        except Exception as e:
            logging.error(f"Error processing maintenance: {e}")

    # Finance (Base Table)
    finance_agg = finance_df[['unit_id', 'ownership_type', 'monthly_payment', 'balloon_payment', 'year', 'make', 'model']].copy()
    finance_agg.columns = ['Unit ID', 'Ownership', 'Monthly_Payment', 'Payoff_Balance', 'Year', 'Make', 'Model']
    for col in ['Monthly_Payment', 'Payoff_Balance']:
        finance_agg[col] = pd.to_numeric(finance_agg[col], errors='coerce').fillna(0)

    # 4. Market Value
    logging.info("Estimating Market Values...")
    finance_agg['Estimated_Market_Value'] = 0.0
    if market_df is not None:
        try:
            # Prepare Market Data
            market_df['Price'] = pd.to_numeric(market_df['truck_price'], errors='coerce')
            market_df['Year'] = pd.to_numeric(market_df['truck_year'], errors='coerce')
            market_df['Make_Norm'] = market_df['truck_brand'].astype(str).str.lower().str.strip()
            market_df['Model_Norm'] = market_df['truck_model'].astype(str).str.lower().str.strip().str.split(' ').str[0] # Aggressive Match
            
            market_stats = market_df.groupby(['Year', 'Make_Norm', 'Model_Norm'])['Price'].median().reset_index()
            
            # Prepare Finance Data for Join
            finance_agg['Year_Num'] = pd.to_numeric(finance_agg['Year'], errors='coerce')
            finance_agg['Make_Norm'] = finance_agg['Make'].astype(str).str.lower().str.strip()
            finance_agg['Model_Norm'] = finance_agg['Model'].astype(str).str.lower().str.strip().str.split(' ').str[0]
            
            # Merge
            temp = finance_agg.merge(market_stats, left_on=['Year_Num', 'Make_Norm', 'Model_Norm'], right_on=['Year', 'Make_Norm', 'Model_Norm'], how='left')
            finance_agg['Estimated_Market_Value'] = temp['Price'].fillna(0)
            
            # Fallback Averages if exact match fails
            avg_price = market_df['Price'].median()
            finance_agg['Estimated_Market_Value'] = finance_agg['Estimated_Market_Value'].replace(0, avg_price)
            
        except Exception as e:
            logging.error(f"Error processing market value: {e}")

    # 5. Merge
    logging.info("Merging Datasets...")
    master = finance_agg.merge(usage_agg, on='Unit ID', how='left')
    master = master.merge(revenue_agg, on='Unit ID', how='left')
    master = master.merge(maint_agg, on='Unit ID', how='left')
    
    # Fill NAs
    fill_cols = ['Total_Miles', 'Active_Days', 'Total_Revenue', 'Stub_Count', 'Total_Repair_Cost', 'Repair_Count', 'Avg_Miles_Active_Day', 'Estimated_Market_Value']
    for col in fill_cols:
        if col in master.columns:
             master[col] = master[col].fillna(0)
        else:
             master[col] = 0

    # 6. Derived Metrics & Logic
    logging.info("Applying Decision Logic...")
    
    # Metrics
    master['Repair_CPM'] = np.where(master['Total_Miles'] > 0, 
                                    master['Total_Repair_Cost'] / master['Total_Miles'], 
                                    0)
    master['Revenue_Per_Mile'] = np.where(master['Total_Miles'] > 0,
                                          master['Total_Revenue'] / master['Total_Miles'],
                                          0)
    master['Net_Exit_Gain'] = master['Estimated_Market_Value'] - master['Payoff_Balance']
    
    # Decision Rules (Example Logic)
    # KEEP: High Utilization (>1000 miles), Low CPM (<$0.50), Negative Exit (We'd lose money selling)
    # SELL: Low Utilization OR High CPM, Positive Exit
    # INSPECT: In between
    
    def recommend(row):
        # Inspect conditions
        if row['Total_Miles'] == 0 and row['Total_Repair_Cost'] > 0: return 'INSPECT (Cost No Miles)'
        
        # Sell conditions
        if row['Net_Exit_Gain'] > 5000:
            if row['Total_Miles'] < 2000: return 'SELL (Low Use, High Value)'
            if row['Repair_CPM'] > 0.80: return 'SELL (High Maint)'
            
        # Keep conditions
        if row['Total_Revenue'] > row['Monthly_Payment'] * 2: return 'KEEP (Profitable)'
        if row['Net_Exit_Gain'] < -5000: return 'KEEP (Underwater)'
        
        return 'INSPECT (Review)'

    master['Recommendation'] = master.apply(recommend, axis=1)
    
    # Projections (Next 10 weeks)
    master['Projected_Net_Value_10Wks'] = (
        (master['Total_Miles'] * master['Revenue_Per_Mile']) - 
        (master['Total_Repair_Cost']) - 
        (master['Monthly_Payment'] * 2.5) # 10 weeks approx 2.5 months
    )

    # Output
    cols = [
        'Unit ID', 'Recommendation', 'Make', 'Model', 'Year',
        'Total_Miles', 'Total_Revenue', 'Total_Repair_Cost', 
        'Repair_CPM', 'Revenue_Per_Mile', 'Net_Exit_Gain', 'Projected_Net_Value_10Wks',
        'Active_Days', 'Stub_Count',
        'Ownership', 'Monthly_Payment', 'Payoff_Balance', 'Estimated_Market_Value'
    ]
    
    final_df = master[cols]
    final_df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Analysis Complete. Written to {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
