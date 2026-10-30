-- Q1: WHERE and HAVING
-- Customers with completed orders above INR 500
-- whose qualifying order total exceeds INR 8,000.
-- Q1
SELECT
   customer_id,
   SUM(order_amount) AS total_qualifying_spend
FROM orders
WHERE status = 'completed'
 AND order_amount > 500
GROUP BY customer_id
HAVING SUM(order_amount) > 8000
ORDER BY total_qualifying_spend DESC;

-- Q2: Three-table JOIN
-- Revenue by customer city and product category.
-- Q2
SELECT
   c.city,
   p.category,
   ROUND(SUM(o.order_amount), 2) AS revenue
FROM orders AS o
JOIN customers AS c
   ON o.customer_id = c.customer_id
JOIN products AS p
   ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.city, p.category
ORDER BY c.city, p.category;

-- Q3: Scalar subquery
-- Products priced above the average catalogue price.
-- Q3
SELECT
   product_id,
   product_name,
   price_inr
FROM products
WHERE price_inr > (
   SELECT AVG(price_inr)
   FROM products
)
ORDER BY price_inr DESC;

-- Q4: LEFT JOIN
-- Customers who have no completed orders.
-- Q4
SELECT
   c.customer_id,
   c.city
FROM customers AS c
LEFT JOIN orders AS o
   ON c.customer_id = o.customer_id
  AND o.status = 'completed'
WHERE o.order_id IS NULL
ORDER BY c.customer_id;

-- Q5: Common Table Expressions (CTEs)
-- Customers whose completed spending exceeds the average
-- completed spending of customers with completed orders.
-- Q5
WITH customer_spend AS (
   SELECT
       customer_id,
       SUM(order_amount) AS total_spend
   FROM orders
   WHERE status = 'completed'
   GROUP BY customer_id
),
average_spend AS (
   SELECT AVG(total_spend) AS avg_spend
   FROM customer_spend
)
SELECT
   cs.customer_id,
   ROUND(cs.total_spend, 2) AS total_spend,
   ROUND(a.avg_spend, 2) AS average_spend
FROM customer_spend AS cs
CROSS JOIN average_spend AS a
WHERE cs.total_spend > a.avg_spend
ORDER BY cs.total_spend DESC;

-- Q6: Ranking window functions
-- Rank customers by completed spending within each city.
-- Q6
WITH customer_spend AS (
   SELECT
       c.customer_id,
       c.city,
       SUM(o.order_amount) AS total_spend
   FROM customers AS c
   JOIN orders AS o
       ON c.customer_id = o.customer_id
   WHERE o.status = 'completed'
   GROUP BY c.customer_id, c.city
)
SELECT
   customer_id,
   city,
   ROUND(total_spend, 2) AS total_spend,
   RANK() OVER (
       PARTITION BY city
       ORDER BY total_spend DESC
   ) AS spend_rank,
   DENSE_RANK() OVER (
       PARTITION BY city
       ORDER BY total_spend DESC
   ) AS dense_spend_rank,
   ROW_NUMBER() OVER (
       PARTITION BY city
       ORDER BY total_spend DESC
   ) AS spend_row_number
FROM customer_spend
ORDER BY city, spend_rank, customer_id;

-- Q7: Daily revenue and cumulative running total
-- The day is extracted from the first ten characters of order_ts.
-- Q7
WITH daily_revenue AS (
   SELECT
       SUBSTR(order_ts, 1, 10) AS day,
       ROUND(SUM(order_amount), 2) AS revenue
   FROM orders
   WHERE status = 'completed'
   GROUP BY SUBSTR(order_ts, 1, 10)
)
SELECT
   day,
   revenue,
   ROUND(
       SUM(revenue) OVER (
           ORDER BY day
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ),
       2
   ) AS cumulative_revenue
FROM daily_revenue
ORDER BY day;