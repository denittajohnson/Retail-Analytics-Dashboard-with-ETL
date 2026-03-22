-- Total Sales by Category
SELECT 
    p.category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;

--Sales by Region
SELECT 
    c.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_sales DESC;

--Monthly Sales Trend
SELECT 
    d.year,
    d.month,
    SUM(f.sales) AS monthly_sales,
    SUM(f.profit) AS monthly_profit
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

--Top Customers by Revenue
SELECT 
    c.city,
    c.state,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.city, c.state
ORDER BY total_sales DESC
LIMIT 10;

--Product Performance
SELECT 
    p.category,
    p.sub_category,
    f.product_id,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category, p.sub_category, f.product_id
ORDER BY total_sales DESC
LIMIT 20;