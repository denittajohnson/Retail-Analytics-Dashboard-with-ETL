import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load cleaned CSV
df = pd.read_csv("data/processed/orders_clean.csv")

# Load dim_products
dim_products = df[['product_id','category','sub_category']].drop_duplicates()
dim_products.to_sql('dim_products', engine, if_exists='append', index=False)
print("dim_products loaded")

# Load dim_customers
dim_customers = df[['customer_id','segment','country','city','state','postal_code','region']].drop_duplicates()
dim_customers.to_sql('dim_customers', engine, if_exists='append', index=False)
print("dim_customers loaded")

# Load dim_date
df['order_date'] = pd.to_datetime(df['order_date'])
dim_date = pd.DataFrame()
dim_date['date'] = df['order_date']
dim_date['year'] = df['order_date'].dt.year
dim_date['month'] = df['order_date'].dt.month
dim_date['day'] = df['order_date'].dt.day
dim_date = dim_date.drop_duplicates()
dim_date.to_sql('dim_date', engine, if_exists='append', index=False)
print("dim_date loaded")

# Load fact_sales
fact_sales = df[['order_id','customer_id','product_id','order_date','quantity','sales','discount','profit']]
fact_sales.to_sql('fact_sales', engine, if_exists='append', index=False)
print("fact_sales loaded")

print("ETL Load Completed Successfully")