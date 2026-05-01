-- Scrappy Market Agentic AI System (MySQL)
-- DDL: tables + keys (aligned with ERD)

USE scrappy_data;

DROP TABLE IF EXISTS inventory_snapshots;
DROP TABLE IF EXISTS promotions;
DROP TABLE IF EXISTS sales_fact;
DROP TABLE IF EXISTS calendar_dim;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;

CREATE TABLE stores (
  store_id INT PRIMARY KEY,
  store_name VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL,
  state VARCHAR(50) NOT NULL,
  region VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(50) NOT NULL,
  brand VARCHAR(50) NOT NULL,
  price DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE calendar_dim (
  date_id INT PRIMARY KEY,
  full_date DATE NOT NULL,
  day_of_week VARCHAR(20) NOT NULL,
  month INT NOT NULL,
  quarter INT NOT NULL,
  year INT NOT NULL,
  UNIQUE KEY uq_calendar_full_date (full_date)
) ENGINE=InnoDB;

CREATE TABLE sales_fact (
  sale_id INT PRIMARY KEY,
  store_id INT NOT NULL,
  product_id INT NOT NULL,
  date_id INT NOT NULL,
  quantity_sold INT NOT NULL,
  revenue DECIMAL(10,2) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  profit DECIMAL(10,2) NOT NULL,
  KEY idx_sales_store (store_id),
  KEY idx_sales_product (product_id),
  KEY idx_sales_date (date_id),
  CONSTRAINT fk_sales_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
  CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(product_id),
  CONSTRAINT fk_sales_date FOREIGN KEY (date_id) REFERENCES calendar_dim(date_id)
) ENGINE=InnoDB;

CREATE TABLE promotions (
  promo_id INT PRIMARY KEY,
  product_id INT NOT NULL,
  start_date_id INT NOT NULL,
  end_date_id INT NOT NULL,
  discount_pct DECIMAL(5,2) NOT NULL,
  campaign_name VARCHAR(100) NOT NULL,
  KEY idx_promo_product (product_id),
  KEY idx_promo_dates (start_date_id, end_date_id),
  CONSTRAINT fk_promo_product FOREIGN KEY (product_id) REFERENCES products(product_id),
  CONSTRAINT fk_promo_start FOREIGN KEY (start_date_id) REFERENCES calendar_dim(date_id),
  CONSTRAINT fk_promo_end FOREIGN KEY (end_date_id) REFERENCES calendar_dim(date_id),
  CONSTRAINT chk_promo_date_range CHECK (end_date_id >= start_date_id)
) ENGINE=InnoDB;

CREATE TABLE inventory_snapshots (
  snapshot_id INT PRIMARY KEY,
  store_id INT NOT NULL,
  product_id INT NOT NULL,
  date_id INT NOT NULL,
  inventory_level INT NOT NULL,
  KEY idx_inv_store (store_id),
  KEY idx_inv_product (product_id),
  KEY idx_inv_date (date_id),
  CONSTRAINT fk_inv_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
  CONSTRAINT fk_inv_product FOREIGN KEY (product_id) REFERENCES products(product_id),
  CONSTRAINT fk_inv_date FOREIGN KEY (date_id) REFERENCES calendar_dim(date_id)
) ENGINE=InnoDB;
