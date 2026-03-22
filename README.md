#  Retail Sales Analytics Dashboard with ETL

## About
This project is a **Retail Sales Analytics Dashboard** built with Python, PostgreSQL, Pandas, Matplotlib, Seaborn, and Streamlit. It demonstrates a **full ETL pipeline**: extracting raw data, transforming it for analysis, and loading it into a PostgreSQL database. The dashboard provides interactive visualizations to help analyze sales performance by category, region, customer, and product.

This project is ideal for **Data Engineering and Analytics practice**, showcasing data cleaning, transformation, database modeling, and dashboard creation.

---

## ⭐ Star Schema

The project uses a **star schema** in PostgreSQL for organizing the data warehouse:


### **Fact Table**
- **fact_sales**: Contains all sales transactions.
  - `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `sales`, `discount`, `profit`

### **Dimension Tables**
1. **dim_products**
   - `product_id`, `category`, `sub_category`
2. **dim_customers**
   - `customer_id`, `segment`, `country`, `city`, `state`, `postal_code`, `region`
3. **dim_date**
   - `date`, `year`, `month`, `day`

---

## Folder Structure

Retail Sales Data/
│
├─ data/
│ ├─ raw/  (orders.csv)
│ └─ processed/ # Cleaned CSV files (orders_clean.csv)
│
├─ etl/
│ ├─ extract.py 
│ ├─ transform.py 
│ └─ load.py
│
├─ dashboard/
│ ├─ dashboard_mat_seaborn.py # Matplotlib + Seaborn dashboard
│ └─ dashboard_streamlit.py # Streamlit interactive dashboard
│
├─ sql/
│ └─ queries.sql # Example SQL queries for analysis
│
├─ .env # Environment variables (not uploaded to GitHub)
├─ .gitignore # Ignore sensitive and unnecessary files


---

## Technologies Used
- **Python** – ETL, data manipulation, dashboard  
- **Pandas / NumPy** – Data cleaning & transformation  
- **Matplotlib / Seaborn** – Static visualizations  
- **Streamlit** – Interactive dashboard  
- **PostgreSQL** – Data warehouse and star schema  
- **SQLAlchemy** – Database connection and loading  

---

## ETL Process

### 1️⃣ Extract
- Load raw CSV (`orders.csv`) using `extract.py`.
- Preview data, check columns and types.

### 2️⃣ Transform
- Clean and preprocess data in `transform.py`:
  - Standardize column names  
  - Convert `order_date` to datetime  
  - Calculate `sales`, `discount`, and `profit`  
  - Remove duplicates and fill missing values  
  - Validate data for negative values and missing values  

### 3️⃣ Load
- Use `load.py` to load data into PostgreSQL:  
  - `dim_products`  
  - `dim_customers`  
  - `dim_date`  
  - `fact_sales`  
- Database connection uses **SQLAlchemy** and `.env` for credentials.

---

## Dashboard

### **Matplotlib + Seaborn (`dashboard_mat_seaborn.py`)**
- Static charts for:  
  - Total Sales by Category  
  - Sales by Region  
  - Monthly Sales Trend  
  - Top 10 Customers  
  - Top 20 Products  
  - Heatmap: Region vs Category  

### **Streamlit Interactive Dashboard (`dashboard_streamlit.py`)**
- Filters in sidebar:  
  - Year / Month  
  - Product Category  
  - Region  
- Interactive plots update dynamically based on selected filters.

---

## How to Run

### **1. Clone the repo**
```bash
git clone https://github.com/denittajohnson/Retail-Analytics-Dashboard-with-ETL.git
cd Retail-Analytics-Dashboard-with-ETL
2. Install dependencies
pip install -r requirements.txt

Dependencies: pandas, sqlalchemy, matplotlib, seaborn, streamlit, psycopg2-binary

3. Setup .env

Create a .env file in the root folder with your PostgreSQL credentials:

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=retail_db

**Important: .env is ignored by Git to keep credentials safe.**

4. Run ETL
python etl/extract.py
python etl/transform.py
python etl/load.py
5. Run Streamlit Dashboard
python -m streamlit run dashboard/dashboard_streamlit.py


The project uses a star schema to optimize analytical queries.

Denitta Johnson – Data Engineering & Analytics Enthusiast

GitHub: https://github.com/denittajohnson
Contact: denittajohnson@gmail.com

