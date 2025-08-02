import pandas as pd
import sys

def examine_excel_file(file_path, file_name):
    print(f"\n=== Examining {file_name} ===")
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
        print("\nBasic info:")
        print(df.info())
        
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

if __name__ == "__main__":
    examine_excel_file("customer_data.xlsx", "Customer Data")
    examine_excel_file("loan_data.xlsx", "Loan Data")
