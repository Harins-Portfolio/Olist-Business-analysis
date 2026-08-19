-- =============================================================================
-- OLIST BUSINESS ANALYTICS - PostgreSQL schema (DDL) - NORMALIZED CORE
-- Generated for Project BA Olist TFM. Load target: PostgreSQL (db "Olist").
-- Analysis universe: DELIVERED orders only (per PROJECT_CANVAS decisions).
--
-- Design notes:
--  * Every ID and zip/CEP column is TEXT/VARCHAR -- CEP codes are leading-zero
--    significant ("04106") and must NEVER be an integer (see clean_check_report
--    §4 / data loss found this session).
--  * Money is NUMERIC(14,2). Dates/timestamps are real TIMESTAMP types.
--  * We load the NORMALIZED core tables (orders/payments/items/reviews/products/
--    customers/sellers/geolocation). Joins happen through these keys. The flat
--    olist_master and the Power-BI star (00b_create_star_schema.sql) are
--    optional convenience artifacts - prefer the normalized model for SQL.
--
-- Run order:
--   1) psql -d <db> -f 03_SQL/00_create_schema.sql
--   2) psql -d <db> -f 03_SQL/01_load_data.sql     (COPY loads, adjust the CSV PATH)
-- =============================================================================

BEGIN;

DROP SCHEMA IF EXISTS olist CASCADE;
CREATE SCHEMA olist;

-- ---------------------------------------------------------------------------
--  GEOGRAPHY  (1 row per zip prefix)
-- ---------------------------------------------------------------------------
CREATE TABLE olist.geography (
    geolocation_zip_code_prefix  TEXT PRIMARY KEY,   -- CEP (leading zeros kept)
    geolocation_city             TEXT,
    geolocation_state            TEXT,
    latitude                     NUMERIC(10,6),
    longitude                    NUMERIC(10,6)
);

-- ---------------------------------------------------------------------------
--  CUSTOMERS
-- ---------------------------------------------------------------------------
CREATE TABLE olist.customers (
    customer_id                  TEXT PRIMARY KEY,
    customer_unique_id           TEXT NOT NULL,
    customer_zip_code_prefix     TEXT,
    customer_city                TEXT,
    customer_state               TEXT
);
CREATE INDEX ON olist.customers (customer_unique_id);

-- ---------------------------------------------------------------------------
--  SELLERS
-- ---------------------------------------------------------------------------
CREATE TABLE olist.sellers (
    seller_id                    TEXT PRIMARY KEY,
    seller_zip_code_prefix       TEXT,
    seller_city                  TEXT,
    seller_state                 TEXT
);

-- ---------------------------------------------------------------------------
--  PRODUCTS
-- ---------------------------------------------------------------------------
CREATE TABLE olist.products (
    product_id                   TEXT PRIMARY KEY,
    product_category_name        TEXT,
    product_name_lenght          NUMERIC(10,2),
    product_description_lenght   NUMERIC(10,2),
    product_photos_qty           NUMERIC(10,2),
    product_weight_g             NUMERIC(10,2),
    product_length_cm            NUMERIC(10,2),
    product_height_cm            NUMERIC(10,2),
    product_width_cm             NUMERIC(10,2),
    category_english             TEXT
);

-- ---------------------------------------------------------------------------
--  ORDERS  (delivered orders with valid delivery dates)
-- ---------------------------------------------------------------------------
CREATE TABLE olist.orders (
    order_id                         TEXT PRIMARY KEY,
    customer_id                      TEXT,
    order_status                     TEXT,
    order_purchase_timestamp         TIMESTAMP,
    order_approved_at                TIMESTAMP,
    order_delivered_carrier_date     TIMESTAMP,
    order_delivered_customer_date    TIMESTAMP,
    order_estimated_delivery_date    TIMESTAMP,
    delivery_days                    INTEGER
);
CREATE INDEX ON olist.orders (customer_id);
CREATE INDEX ON olist.orders (order_purchase_timestamp);

-- ---------------------------------------------------------------------------
--  ORDER ITEMS  (line grain; composite key order_id + order_item_id)
-- ---------------------------------------------------------------------------
CREATE TABLE olist.order_items (
    order_id                   TEXT,
    order_item_id              INTEGER,
    product_id                 TEXT,
    seller_id                  TEXT,
    shipping_limit_date        TIMESTAMP,
    price                      NUMERIC(14,2),
    freight_value              NUMERIC(14,2),
    PRIMARY KEY (order_id, order_item_id)
);
CREATE INDEX ON olist.order_items (product_id);
CREATE INDEX ON olist.order_items (seller_id);

-- ---------------------------------------------------------------------------
--  PAYMENTS  (one row per order, aggregated)
-- ---------------------------------------------------------------------------
CREATE TABLE olist.payments (
    order_id                     TEXT PRIMARY KEY,
    total_payment_value          NUMERIC(14,2),
    payment_types_used           TEXT,           -- e.g. "credit_card" or "boleto,credit_card"
    payment_installments_max     INTEGER
);

-- ---------------------------------------------------------------------------
--  REVIEWS  (one review row per order; keyed by order_id per clean_check)
--  NOTE: key is order_id (unique in reviews_clean.csv). review_id is NOT unique
--  in the cleaned export (some review_ids repeat across orders), so it is a
--  plain column here - do NOT add a UNIQUE index on it.
-- ---------------------------------------------------------------------------
CREATE TABLE olist.reviews (
    review_id                    TEXT,
    order_id                     TEXT PRIMARY KEY,
    review_score                 INTEGER CHECK (review_score BETWEEN 1 AND 5),
    review_comment_title         TEXT,
    review_comment_message       TEXT,
    review_creation_date         TIMESTAMP,
    review_answer_timestamp      TIMESTAMP
);

-- ---------------------------------------------------------------------------
--  ORDERS ITEMS AGGREGATED (per-order summary; exported by the pipeline)
-- ---------------------------------------------------------------------------
CREATE TABLE olist.orders_items_aggregated (
    order_id             TEXT PRIMARY KEY,
    item_count           INTEGER,
    total_items_price    NUMERIC(14,2),
    total_freight        NUMERIC(14,2),
    n_sellers            INTEGER,
    seller_ids           TEXT,     -- pipe-delimited list
    product_ids          TEXT      -- pipe-delimited list
);

COMMIT;

-- =========================================================================
--  (OPTIONAL) FLAT ANALYTICAL MASTER + POWER BI STAR SCHEMA
--  See 00b_create_star_schema.sql for the star model (Dim_*/Fact_*).
--  The normalized model above is the recommended target for SQL analysis.
-- =========================================================================
