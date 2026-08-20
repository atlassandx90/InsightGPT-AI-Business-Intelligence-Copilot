SELECT
    SUM(payment_value) AS total_sales
FROM payments;

-- 1. Total Revenue
SELECT SUM(payment_value) AS total_revenue
FROM payments;

-- 2. Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 3. Average Order Value
SELECT
ROUND(
    (SUM(payment_value)/COUNT(DISTINCT order_id))::numeric,
    2
) AS average_order_value
FROM payments;

-- 4. Order Status Distribution
SELECT
order_status,
COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;