import pandas as pd

try:
    df = pd.read_excel("inflation_rates.xlsx")
    print("Columns:", df.columns.tolist())
    print("\nHead:\n", df.head())
    print("\nInfo:")
    print(df.info())
except Exception as e:
    print(f"Error: {e}")
