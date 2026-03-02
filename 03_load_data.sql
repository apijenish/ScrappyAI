-- Scrappy Market Agentic AI System
-- Bulk load CSVs into MySQL.
-- Replace file paths with your local paths.
-- If LOAD DATA fails due to secure_file_priv, use MySQL Workbench's "Table Data Import Wizard".

USE scrappy_ai;

-- Optional (if you use LOAD DATA LOCAL INFILE):
-- SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'C:/path/to/stores.csv'
INTO TABLE stores
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(store_id, store_name, city, state, region);

LOAD DATA LOCAL INFILE 'C:/path/to/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, brand, price);

LOAD DATA LOCAL INFILE 'C:/path/to/calendar_dim.csv'
INTO TABLE calendar_dim
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date_id, full_date, day_of_week, month, quarter, year);

LOAD DATA LOCAL INFILE 'C:/path/to/sales_fact.csv'
INTO TABLE sales_fact
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(sale_id, store_id, product_id, date_id, quantity_sold, revenue, cost, profit);

LOAD DATA LOCAL INFILE 'C:/path/to/promotions.csv'
INTO TABLE promotions
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(promo_id, product_id, start_date_id, end_date_id, discount_pct, campaign_name);

LOAD DATA LOCAL INFILE 'C:/path/to/inventory_snapshots.csv'
INTO TABLE inventory_snapshots
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(snapshot_id, store_id, product_id, date_id, inventory_level);

-- Sanity checks:
SELECT COUNT(*) AS stores_rows FROM stores;
SELECT COUNT(*) AS products_rows FROM products;
SELECT COUNT(*) AS calendar_rows FROM calendar_dim;
SELECT COUNT(*) AS sales_rows FROM sales_fact;
SELECT COUNT(*) AS promotions_rows FROM promotions;
SELECT COUNT(*) AS inventory_rows FROM inventory_snapshots;
