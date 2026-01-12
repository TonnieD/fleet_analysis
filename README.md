# Fleet Value Analysis

Automated system for analyzing fleet performance to determine whether a truck unit should be **KEPT**, **SOLD**, or **INSPECTED**.

## Overview
This project processes disparate data sources (Finance, Maintenance, Operations, Market Listings) to generate a "Master Decision Table". It values each truck based on its profitability, maintenance costs, and estimated market exit value.

## Project Structure
```
fleet_analysis/
├── data/                   # Input Excel files and Output CSVs
│   ├── truck-finance.xlsx
│   ├── vehicle-distance-traveled.xlsx
│   ├── ...
│   └── fleet_value_report.csv  <-- Final Output
├── notebooks/              # Jupyter Notebooks for presentation
│   └── Fleet_Value_Analysis_Presentation.ipynb
├── scripts/                # Python scripts for automation
│   ├── fleet_value_analysis.py <-- Main Analysis Engine
│   └── generate_notebook.py    <-- Utility to regen notebook
└── README.md
```

## Setup
1.  **Environment**: Ensure you have the `fleet_analysis` Conda environment activated.
    ```bash
    conda activate fleet_analysis
    ```
2.  **Dependencies**: Project relies on `pandas`, `numpy`, and `openpyxl`.

## Usage

### 1. Run the Full Analysis
To process all data and generate the decision table:
```bash
python scripts/fleet_value_analysis.py
```
**Output**: `data/fleet_value_report.csv`

### 2. View the Presentation
A Jupyter Notebook is available to walk stakeholders through the logic step-by-step:
- Open `notebooks/Fleet_Value_Analysis_Presentation.ipynb` in VS Code or Jupyter Lab.

## Decision Logic
The system evaluates each truck against the following rules:

| Recommendation | Condition | Rationale |
| :--- | :--- | :--- |
| **KEEP (Profitable)** | Revenue > 2x Payment | Truck is covering its costs and generating profit. |
| **KEEP (Underwater)** | Net Exit Gain < -$5,000 | Selling now would result in a loss; better to run it. |
| **SELL (High Maint)** | Repair CPM > $0.80 | Maintenance costs are eating margins. |
| **SELL (Low Use)** | Net Exit > $5k & Miles < 2k | Asset has value but isn't being used. |
| **INSPECT** | All other cases | Requires manual review or has conflicting signals. |

## Key Metrics
- **Repair CPM**: Total Repair Cost / Total Miles.
- **Net Exit Gain**: Estimated Market Value - Payoff Balance.
- **Revenue Per Mile**: Total Revenue / Total Miles.
- **Projected Net Value**: Estimated profit over the next 10 weeks.
