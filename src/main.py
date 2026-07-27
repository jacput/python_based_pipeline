import pandas as pd
import sys

# Load the CSV file into a DataFrame
try:
    file_path = r'C:\Users\jputhiamada3\OneDrive - DXC Production\Desktop\SalesPipeline\data\incoming\DailySales_07272026.csv'
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error loading file: {e}")
    sys.exit(1)
else:
    required_columns = [
    "OrderID",
    "OrderDate",
    "CustomerID",
    "Product",
    "Qty",
    "UnitPrice",
    "State"
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        sys.exit(1)

    # View the first 5 rows
    print(df.head())
    row_count = len(df)
    print(f"Number of rows: {len(df)}")
    sys.exit(0)  # Graceful success exit