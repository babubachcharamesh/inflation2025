import pandas as pd
df = pd.read_excel("inflation_rates.xlsx")
print(df.head(10).to_string())
print(df.info())
