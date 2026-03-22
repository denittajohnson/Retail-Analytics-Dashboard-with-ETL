import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Filters
selected_year = 2023
selected_month = 1
selected_category = None
selected_region = None

# Build WHERE clause
where_clauses = [f"d.year = {selected_year}", f"d.month = {selected_month}"]
if selected_category:
    where_clauses.append(f"p.category = '{selected_category}'")
if selected_region:
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

# Load Data
df_category = pd.read_sql(queries["Sales by Category"], engine)
df_region = pd.read_sql(queries["Sales by Region"], engine)
df_monthly = pd.read_sql(queries["Monthly Sales Trend"], engine)
df_customers = pd.read_sql(queries["Top Customers"], engine)
df_products = pd.read_sql(queries["Top Products"], engine)
df_heatmap = pd.read_sql(queries["Region vs Category Heatmap"], engine)

# Plotting
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10,6)

formatter = FuncFormatter(lambda x, _: f'{int(x):,}')  # Format y-axis numbers

# 1. Sales by Category
plt.figure()
sns.barplot(data=df_category, x="category", y="total_sales", palette="viridis")
plt.gca().yaxis.set_major_formatter(formatter)
plt.title("Total Sales by Category")
plt.ylabel("Sales")
plt.xlabel("Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Sales by Region
plt.figure()
sns.barplot(data=df_region, x="region", y="total_sales", palette="coolwarm")
plt.gca().yaxis.set_major_formatter(formatter)
plt.title("Sales by Region")
plt.ylabel("Sales")
plt.xlabel("Region")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Monthly Sales Trend
plt.figure()
sns.lineplot(data=df_monthly, x="month", y="monthly_sales", marker="o")
plt.gca().yaxis.set_major_formatter(formatter)
plt.title(f"Monthly Sales Trend - {selected_year}")
plt.ylabel("Sales")
plt.xlabel("Month")
plt.xticks(range(1,13))
plt.tight_layout()
plt.show()

# 4. Top Customers
plt.figure()
sns.barplot(data=df_customers, x="city", y="total_sales", palette="magma")
plt.gca().yaxis.set_major_formatter(formatter)
plt.title("Top 10 Customers by Revenue")
plt.ylabel("Sales")
plt.xlabel("City")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Top Products
plt.figure(figsize=(12,6))
sns.barplot(data=df_products, x="product_id", y="total_sales", hue="category", dodge=False, palette="Set2")
plt.gca().yaxis.set_major_formatter(formatter)
plt.title("Top 20 Products by Sales")
plt.ylabel("Sales")
plt.xlabel("Product ID")
plt.xticks(rotation=90)
plt.legend(title="Category")
plt.tight_layout()
plt.show()

# 6. Heatmap
heatmap_data = df_heatmap.pivot(index="region", columns="category", values="total_sales").fillna(0)
plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Region vs Category Sales Heatmap")
plt.ylabel("Region")
plt.xlabel("Category")
plt.tight_layout()
plt.show()