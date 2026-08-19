-- =============================================================================
-- OLIST - (OPTIONAL) POWER BI STAR SCHEMA
-- Only needed if you want the exact star model (Dim_*/Fact_*) in Postgres for
-- dashboards; otherwise skip this file and just use the normalized tables in
-- 00_create_schema.sql. Column names below match the CSVs in
-- 02_Cleaned_data/star_schema/ 1:1.
--
-- Run order (optional):
--   1) psql -d <db> -f 03_SQL/00_create_schema.sql
--   2) psql -d <db> -f 03_SQL/00b_create_star_schema.sql   (optional)
--   3) load the star CSVs with \copy (optional)
-- =============================================================================

BEGIN;

CREATE TABLE olist.dim_date (
    date           DATE PRIMARY KEY,
    date_key       INTEGER NOT NULL UNIQUE,
    year           INTEGER,
    quarter        INTEGER,
    month          INTEGER,
    month_name     TEXT,
    day_of_month   INTEGER,
    day_of_week    INTEGER,
    weekday        TEXT,
    is_weekend     SMALLINT,
    is_workday     SMALLINT
);

CREATE TABLE olist.dim_product (
    product_id        TEXT PRIMARY KEY,
    product_category_name TEXT,
    category_english  TEXT,
    product_weight_g  NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm  NUMERIC,
    product_photos_qty INTEGER
);

CREATE TABLE olist.dim_seller (
    seller_id              TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city            TEXT,
    seller_state           TEXT
);

CREATE TABLE olist.dim_geography (
    zip_code_prefix TEXT PRIMARY KEY,
    latitude    NUMERIC(10,6),
    longitude   NUMERIC(10,6),
    city        TEXT,
    state       TEXT
);

CREATE TABLE olist.dim_customer (
    customer_id              TEXT PRIMARY KEY,
    customer_unique_id       TEXT NOT NULL,
    customer_zip_code_prefix TEXT,
    customer_city            TEXT,
    customer_state           TEXT
);

CREATE TABLE olist.fact_orders (
    order_id                  TEXT PRIMARY KEY,
    customer_id               TEXT,
    order_date                TIMESTAMP,
    date_key                  INTEGER,
    order_revenue             NUMERIC(14,2),
    order_revenue_gross       NUMERIC(14,2),
    total_freight             NUMERIC(14,2),
    paid_amount               NUMERIC(14,2),
    payment_installments_max  INTEGER,
    item_count                INTEGER,
    payment_types_used        TEXT,
    delivery_days             INTEGER,
    promised_delivery_days    INTEGER,
    days_early_or_late        INTEGER,
    is_late                   SMALLINT,
    is_ontime                 SMALLINT,
    review_score              INTEGER,
    has_review_comment        SMALLINT,
    order_month               TEXT,
    order_year                INTEGER,
    is_weekend                SMALLINT
);

CREATE TABLE olist.fact_order_items (
    order_item_id    INTEGER,
    order_id         TEXT,
    product_id       TEXT,
    seller_id        TEXT,
    order_date       TIMESTAMP,
    date_key         INTEGER,
    line_price       NUMERIC(14,2),
    line_freight     NUMERIC(14,2),
    is_late          SMALLINT,
    PRIMARY KEY (order_id, order_item_id)
);

-- Optional referential integrity (only if all tables loaded).
ALTER TABLE olist.fact_orders     ADD CONSTRAINT fk_orders_cust  FOREIGN KEY (customer_id) REFERENCES olist.dim_customer(customer_id);
ALTER TABLE olist.fact_order_items ADD CONSTRAINT fk_items_order   FOREIGN KEY (order_id)   REFERENCES olist.fact_orders(order_id);
ALTER TABLE olist.fact_order_items ADD CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES olist.dim_product(product_id);
ALTER TABLE olist.fact_order_items ADD CONSTRAINT fk_items_seller  FOREIGN KEY (seller_id)  REFERENCES olist.dim_seller(seller_id);

COMMIT;