-- =============================================================================
-- OLIST - Starter analytical queries (normalized model)
-- Run AFTER loading with 00_create_schema.sql + 01_load_data.sql.
-- Business questions from PROJECT_CANVAS.md §2. All on DELIVERED orders.
-- =============================================================================

-- ---------------------------------------------------------------
-- 1. Total revenue by month (revenue = goods value, matches AOV baseline)
-- ---------------------------------------------------------------
SELECT to_char(o.order_purchase_timestamp, 'YYYY-MM') AS month,
       round(sum(it.price), 2)                        AS revenue,
       count(DISTINCT o.order_id)                     AS orders
FROM olist.orders o
JOIN olist.order_items it USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------
-- 2. Average order value (AOV) per month, goods vs incl-freight
-- ---------------------------------------------------------------
WITH rev AS (
    SELECT order_id,
           sum(price)                    AS revenue,
           sum(price + freight_value)    AS revenue_incl
    FROM olist.order_items
    GROUP BY order_id
)
SELECT to_char(o.order_purchase_timestamp, 'YYYY-MM') AS month,
       round(avg(rev.revenue), 2)                    AS aov_goods,
       round(avg(rev.revenue_incl), 2)               AS aov_incl_freight,
       count(*)                                      AS orders
FROM olist.orders o
JOIN rev USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------
-- 3. Product categories by revenue
-- ---------------------------------------------------------------
SELECT p.category_english,
       round(sum(it.price), 2) AS revenue,
       count(*)                AS line_items
FROM olist.order_items it
JOIN olist.products p USING (product_id)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 15;

-- ---------------------------------------------------------------
-- 4. Customers & spend by state
-- ---------------------------------------------------------------
SELECT c.customer_state,
       count(DISTINCT c.customer_id) AS customers,
       round(sum(it.price), 2)       AS revenue
FROM olist.orders o
JOIN olist.customers c USING (customer_id)
JOIN olist.order_items it USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- 5. Repeat purchase rate
-- ---------------------------------------------------------------
WITH cust_counts AS (
    SELECT c.customer_unique_id, count(DISTINCT o.order_id) AS n
    FROM olist.orders o
    JOIN olist.customers c USING (customer_id)
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT count(*)                                    AS unique_customers,
       count(*) FILTER (WHERE n >= 2)              AS repeat_customers,
       round(100.0 * count(*) FILTER (WHERE n >= 2) / count(*), 2) AS repeat_rate_pct
FROM cust_counts;

-- ---------------------------------------------------------------
-- 6. Delivery performance by state (on-time = delivered <= estimated window)
-- ---------------------------------------------------------------
SELECT c.customer_state,
       round(avg(o.delivery_days), 1)  AS avg_delivery_days,
       round(100.0 * count(*) FILTER (WHERE o.order_delivered_customer_date
                                          <= o.order_estimated_delivery_date)
              / count(*), 1)           AS on_time_pct
FROM olist.orders o
JOIN olist.customers c USING (customer_id)
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY on_time_pct;   -- worst on-time first

-- ---------------------------------------------------------------
-- 7. Satisfaction vs lateness
-- ---------------------------------------------------------------
SELECT CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
            THEN 'on-time' ELSE 'late' END AS delivery,
       round(avg(r.review_score), 2)       AS avg_score,
       count(*)                            AS orders
FROM olist.orders o
JOIN olist.reviews r USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY 1;

-- ---------------------------------------------------------------
-- 8. Freight burden (freight as % of goods revenue)
-- ---------------------------------------------------------------
SELECT round(100.0 * sum(it.freight_value) / nullif(sum(it.price), 0), 2) AS freight_pct
FROM olist.order_items it
JOIN olist.orders o USING (order_id)
WHERE o.order_status = 'delivered';

-- ---------------------------------------------------------------
-- 9. Highest-order months (seasonality / Black Friday)
-- ---------------------------------------------------------------
SELECT to_char(order_purchase_timestamp, 'YYYY-MM') AS month, count(*) AS orders
FROM olist.orders
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY count(*) DESC
LIMIT 6;