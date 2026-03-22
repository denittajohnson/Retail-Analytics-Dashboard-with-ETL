import pandas as pd


df = pd.read_csv("data/raw/orders.csv")
print(df.head())

df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns)

df['order_date'] = pd.to_datetime(df['order_date'])

df['sales'] = df['list_price'] * df['quantity']

df['discount'] = df['sales'] * df['discount_percent'] / 100

df['profit'] = df['sales'] - df['discount'] - (df['cost_price'] * df['quantity'])

# Create a unique customer_id by combining identifiable columns
df['customer_id'] = (
    df['segment'].str[:3] + "_" + 
    df['city'].str.replace(" ", "").str[:3] + "_" +
    df['state'].str.replace(" ", "").str[:3]
)

before = len(df)

df = df.drop_duplicates()
df['ship_mode'] = df['ship_mode'].fillna('Standard Class')

after = len(df)

print("\nDuplicates Removed:", before - after)

#Data Validation Checks

print("\nChecking Missing Values:")
print(df.isnull().sum())

print("\nChecking Duplicate Order IDs:")
print(df.duplicated(subset=["order_id"]).sum())

print("\nChecking Negative Values:")

print("Negative Quantity:", (df['quantity'] < 0).sum())
print("Negative Sales:", (df['sales'] < 0).sum())


print("\nData Types:")
print(df.dtypes)


print("\nTotal Rows After Cleaning:")
print(len(df))



df.to_csv("data/processed/orders_clean.csv", index=False)

print("\nTransformation Completed Successfully!")
print("Clean file saved to: data/processed/orders_clean.csv")

print("\nTransformed Data Preview:")
print(df.head())