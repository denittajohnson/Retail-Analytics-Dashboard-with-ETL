import pandas as pd

df = pd.read_csv("data/raw/orders.csv")
print(df.head())
print(df.columns)
print(df.info())