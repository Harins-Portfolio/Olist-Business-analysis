-- =============================================================================
-- OLIST - PostgreSQL LOAD (COPY) script - NORMALIZED CORE
-- Run AFTER 00_create_schema.sql. Use psql:
--    psql -U <user> -d <db> -f 03_SQL/01_load_data.sql
--
-- Uses \copy (psql client-side COPY): reads files from THIS machine (the one
-- running psql). Edit the BASE path below if your checkout lives elsewhere.
-- =============================================================================

\set ON_ERROR_STOP on

-- ---------------------------------------------------------------------------
-- NORMALIZED CORE TABLES (recommended for SQL analysis)
-- ---------------------------------------------------------------------------
\copy olist.geography (geolocation_zip_code_prefix, geolocation_city, geolocation_state, latitude, longitude) FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/geolocation_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.customers FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/olist_customers_dataset.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.sellers FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/olist_sellers_dataset.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.products FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/products_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.orders FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/orders_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.order_items FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/items_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.payments FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/payments_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.reviews FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/reviews_clean.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy olist.orders_items_aggregated FROM 'C:/Users/Nikhil Harins/OneDrive/Documentos/UNIE - Analiticas de Negocio/TFM/Project BA Olist/02_Cleaned_data/orders_items_aggregated.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ---------------------------------------------------------------------------
-- Sanity: row counts after load (compare against clean_check_report §2)
-- ---------------------------------------------------------------------------
SELECT 'geography' AS tbl, count(*) FROM olist.geography
UNION ALL SELECT 'customers', count(*) FROM olist.customers
UNION ALL SELECT 'sellers', count(*) FROM olist.sellers
UNION ALL SELECT 'products', count(*) FROM olist.products
UNION ALL SELECT 'orders', count(*) FROM olist.orders
UNION ALL SELECT 'order_items', count(*) FROM olist.order_items
UNION ALL SELECT 'payments', count(*) FROM olist.payments
UNION ALL SELECT 'reviews', count(*) FROM olist.reviews
UNION ALL SELECT 'orders_items_aggregated', count(*) FROM olist.orders_items_aggregated
ORDER BY tbl;