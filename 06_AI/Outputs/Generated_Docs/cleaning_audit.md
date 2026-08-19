# DATA QUALITY AUDIT — Olist (Phase 2, prompt 2.1)

_Generated: 2026-08-16T13:17:25  |  source: 01_Raw_Data (never modified)_


## T2.1 — Raw-file snapshot

| Table | Rows | Cols | Duplicate rows | Null cells | Null % | Cols with nulls |
|---|---|---|---|---|---|---|
| olist_customers_dataset.csv | 99,441 | 5 | 0 | 0 | 0.00% | 0 |
| olist_geolocation_dataset.csv | 1,000,163 | 5 | 261,831 | 0 | 0.00% | 0 |
| olist_order_items_dataset.csv | 112,650 | 7 | 0 | 0 | 0.00% | 0 |
| olist_order_payments_dataset.csv | 103,886 | 5 | 0 | 0 | 0.00% | 0 |
| olist_order_reviews_dataset.csv | 99,224 | 7 | 0 | 145,903 | 21.01% | 2 |
| olist_orders_dataset.csv | 99,441 | 8 | 0 | 4,908 | 0.62% | 3 |
| olist_products_dataset.csv | 32,951 | 9 | 0 | 2,448 | 0.83% | 8 |
| olist_sellers_dataset.csv | 3,095 | 4 | 0 | 0 | 0.00% | 0 |
| product_category_name_translation.csv | 71 | 2 | 0 | 0 | 0.00% | 0 |

## T2.2 — Order status distribution (all 99,441 orders)

| order_status | count |
|---|---|
| delivered | 96,478 |
| shipped | 1,107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |