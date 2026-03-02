-- Scrappy Market Agentic AI System
-- Example investigation queries (for demos + agent test cases)

USE scrappy_ai;

-- Q1: Total sales revenue for e-bikes at Atlanta, Athens, Savannah over last 90 days (relative to max date in calendar)
WITH maxd AS (
  SELECT MAX(full_date) AS max_date FROM calendar_dim
),
range90 AS (
  SELECT c.date_id
  FROM calendar_dim c, maxd
  WHERE c.full_date >= DATE_SUB(maxd.max_date, INTERVAL 90 DAY)
)
SELECT
  s.store_name,
  SUM(sf.revenue) AS total_revenue,
  SUM(sf.quantity_sold) AS total_units
FROM sales_fact sf
JOIN stores s ON s.store_id = sf.store_id
JOIN products p ON p.product_id = sf.product_id
WHERE p.category = 'E-Bike'
  AND s.city IN ('Atlanta','Athens','Savannah')
  AND sf.date_id IN (SELECT date_id FROM range90)
GROUP BY s.store_name
ORDER BY total_revenue DESC;

-- Q2: Compare top 3 e-bike models in Atlanta vs Athens for last quarter (relative to max date)
WITH maxd AS (
  SELECT MAX(full_date) AS max_date FROM calendar_dim
),
last_q AS (
  SELECT quarter AS q, year AS y
  FROM calendar_dim c, maxd
  WHERE c.full_date = maxd.max_date
),
quarter_dates AS (
  SELECT date_id
  FROM calendar_dim c
  JOIN last_q q ON c.quarter = q.q AND c.year = q.y
)
SELECT
  s.city,
  p.product_name,
  SUM(sf.revenue) AS revenue
FROM sales_fact sf
JOIN stores s ON s.store_id = sf.store_id
JOIN products p ON p.product_id = sf.product_id
WHERE p.category = 'E-Bike'
  AND s.city IN ('Atlanta','Athens')
  AND sf.date_id IN (SELECT date_id FROM quarter_dates)
GROUP BY s.city, p.product_name
ORDER BY revenue DESC
LIMIT 6;

-- Q3: Week-over-week sales trend for e-bikes in Savannah during May (year inferred from max date)
WITH maxy AS (
  SELECT year AS y FROM calendar_dim ORDER BY full_date DESC LIMIT 1
)
SELECT
  c.year,
  c.month,
  FLOOR((DAYOFMONTH(c.full_date)-1)/7)+1 AS week_of_month,
  SUM(sf.revenue) AS weekly_revenue
FROM sales_fact sf
JOIN stores s ON s.store_id = sf.store_id
JOIN products p ON p.product_id = sf.product_id
JOIN calendar_dim c ON c.date_id = sf.date_id
JOIN maxy ON c.year = maxy.y
WHERE s.city = 'Savannah'
  AND p.category = 'E-Bike'
  AND c.month = 5
GROUP BY c.year, c.month, week_of_month
ORDER BY week_of_month;

-- Investigation: Promotion impact on sales (join on product_id + date range overlap)
SELECT
  pr.campaign_name,
  pr.discount_pct,
  SUM(sf.revenue) AS revenue_during_promo,
  SUM(sf.quantity_sold) AS units_during_promo
FROM promotions pr
JOIN sales_fact sf ON sf.product_id = pr.product_id
JOIN calendar_dim c ON c.date_id = sf.date_id
WHERE c.date_id BETWEEN pr.start_date_id AND pr.end_date_id
GROUP BY pr.campaign_name, pr.discount_pct
ORDER BY revenue_during_promo DESC;

-- Inventory check: count stockout days (inventory_level = 0) by store + category
SELECT
  s.store_name,
  p.category,
  COUNT(*) AS zero_inventory_days
FROM inventory_snapshots i
JOIN stores s ON s.store_id = i.store_id
JOIN products p ON p.product_id = i.product_id
WHERE i.inventory_level = 0
GROUP BY s.store_name, p.category
ORDER BY zero_inventory_days DESC;
