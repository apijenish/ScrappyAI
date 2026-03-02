-- Optional: Helpful view to simplify agent-generated SQL
USE scrappy_ai;

CREATE OR REPLACE VIEW v_sales_enriched AS
SELECT
  sf.sale_id,
  s.store_id, s.store_name, s.city, s.state, s.region,
  p.product_id, p.product_name, p.category, p.brand, p.price,
  c.date_id, c.full_date, c.day_of_week, c.month, c.quarter, c.year,
  sf.quantity_sold, sf.revenue, sf.cost, sf.profit
FROM sales_fact sf
JOIN stores s ON s.store_id = sf.store_id
JOIN products p ON p.product_id = sf.product_id
JOIN calendar_dim c ON c.date_id = sf.date_id;
