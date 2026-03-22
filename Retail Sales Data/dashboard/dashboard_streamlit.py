import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
from matplotlib.ticker import FuncFormatter

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Streamlit Config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("📊 Retail Sales Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

years = pd.read_sql("SELECT DISTINCT year FROM dim_date ORDER BY year;", engine)["year"].tolist()
selected_year = st.sidebar.selectbox("Select Year", years)

months = pd.read_sql(f"SELECT DISTINCT month FROM dim_date WHERE year={selected_year} ORDER BY month;", engine)["month"].tolist()
selected_month = st.sidebar.selectbox("Select Month", months)

categories = pd.read_sql("SELECT DISTINCT category FROM dim_products ORDER BY category;", engine)["category"].tolist()
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

regions = pd.read_sql("SELECT DISTINCT region FROM dim_customers ORDER BY region;", engine)["region"].tolist()
selected_region = st.sidebar.selectbox("Select Region", ["All"] + regions)

# Build WHERE Clause
where_clauses = [f"d.year = {selected_year}", f"d.month = {selected_month}"]
if selected_category != "All":
    where_clauses.append(f"p.category = '{selected_category}'")
if selected_region != "All":
    where_clauses.append(f"c.region = '{selected_region}'")
where_sql = " AND ".join(where_clauses)

# Queries
queries = {
    "Sales by Category": f"""
        SELECT p.category, SUM(f.sales) AS total_sales, SUM(f.profit) AS total_profit
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_customers c ON f.customer_id = c.customer_id
        WHERE {where_sql}
        GROUP BY p.category
        ORDER BY total_sales DESC;
    """,
    "Sales by Region": f"""
        SELECT c.region, SUM(f.sales) AS total_sales, SUM(f.profit) AS total_profit
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_customers c ON f.customer_id = c.customer_id
        WHERE {where_sql}
        GROUP BY c.region
        ORDER BY total_sales DESC;
    """,
    "Monthly Sales Trend": f"""
        SELECT d.year, d.month, SUM(f.sales) AS monthly_sales, SUM(f.profit) AS monthly_profit
        FROM fact_sales f
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_products p ON f.product_id = p.product_id
        JOIN dim_customers c ON f.customer_id = c.customer_id
        WHERE d.year = {selected_year}
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    """,
    "Top Customers": f"""
        SELECT c.city, c.state, SUM(f.sales) AS total_sales, SUM(f.profit) AS total_profit
        FROM fact_sales f
        JOIN dim_customers c ON f.customer_id = c.customer_id
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_products p ON f.product_id = p.product_id
        WHERE {where_sql}
        GROUP BY c.city, c.state
        ORDER BY total_sales DESC
        LIMIT 10;
    """,
    "Top Products": f"""
        SELECT f.product_id, p.category, p.sub_category, SUM(f.sales) AS total_sales, SUM(f.profit) AS total_profit
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_customers c ON f.customer_id = c.customer_id
        WHERE {where_sql}
        GROUP BY f.product_id, p.category, p.sub_category
        ORDER BY total_sales DESC
        LIMIT 20;
    """,
    "Region vs Category Heatmap": f"""
        SELECT c.region, p.category, SUM(f.sales) AS total_sales
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        JOIN dim_date d ON f.order_date = d.date
        JOIN dim_customers c ON f.customer_id = c.customer_id
        WHERE {where_sql}
        GROUP BY c.region, p.category
        ORDER BY c.region, p.category;
    """
}

# Function to run query
@st.cache_data
def run_query(query):
    return pd.read_sql(query, engine)

sns.set_style("whitegrid")
formatter = FuncFormatter(lambda x, _: f'{int(x):,}')

# 1. Sales by Category
st.subheader("💰 Total Sales by Category")
df_category = run_query(queries["Sales by Category"])
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df_category, x="category", y="total_sales", palette="viridis", ax=ax)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel("Sales")
ax.set_xlabel("Category")
st.pyplot(fig)

# 2. Sales by Region
st.subheader("🌎 Sales by Region")
df_region = run_query(queries["Sales by Region"])
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df_region, x="region", y="total_sales", palette="coolwarm", ax=ax)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel("Sales")
ax.set_xlabel("Region")
st.pyplot(fig)

# 3. Monthly Sales Trend
st.subheader("📈 Monthly Sales Trend")
df_monthly = run_query(queries["Monthly Sales Trend"])
fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(data=df_monthly, x="month", y="monthly_sales", marker="o", ax=ax)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel("Sales")
ax.set_xlabel("Month")
st.pyplot(fig)

# 4. Top Customers
st.subheader("🏆 Top 10 Customers by Revenue")
df_customers = run_query(queries["Top Customers"])
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df_customers, x="city", y="total_sales", palette="magma", ax=ax)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel("Sales")
ax.set_xlabel("City")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# 5. Top Products
st.subheader("🛍️ Top 20 Products by Sales")
df_products = run_query(queries["Top Products"])
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(data=df_products, x="product_id", y="total_sales", hue="category", dodge=False, ax=ax)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel("Sales")
ax.set_xlabel("Product ID")
ax.tick_params(axis='x', rotation=90)
ax.legend(title="Category")
st.pyplot(fig)

# 6. Heatmap: Region vs Category
st.subheader("📊 Region vs Category Sales Heatmap")
df_heatmap = run_query(queries["Region vs Category Heatmap"])
heatmap_data = df_heatmap.pivot(index="region", columns="category", values="total_sales").fillna(0)
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_ylabel("Region")
ax.set_xlabel("Category")
st.pyplot(fig)