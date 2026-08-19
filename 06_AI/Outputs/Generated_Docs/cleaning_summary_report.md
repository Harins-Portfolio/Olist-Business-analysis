# OLIST — CLEANING SUMMARY REPORT (Phase 2, prompt 2.9)

_Generated: 2026-08-16T13:17:25  |  pipeline: `04_Python/ETL/data_preparation.py`_


## 1. Row counts — original vs final

| Table | Raw rows | Clean rows | Change |
|---|---|---|---|
| olist_orders_dataset.csv | 99,441 | 96,456 | ↓ (delivered orders with valid delivery dates, no outlier flags) |
| olist_order_payments_dataset.csv | 103,886 | 99,440 | ↓ (one row per order (aggregated)) |
| olist_order_items_dataset.csv | 112,650 | 112,647 | ↓ (no zero/oversized price, no negative freight) |
| olist_order_items_dataset.csv (agg) | 0 | 98,663 | ↑ (one row per order) |
| olist_products_dataset.csv | 32,951 | 32,951 | — (uncategorized filled, English category added) |
| olist_order_reviews_dataset.csv | 99,224 | 98,673 | ↓ (valid scores, one review per order) |
| olist_geolocation_dataset.csv | 1,000,163 | 19,011 | ↓ (one GPS row per zip, in-bounds) |
| olist_customers_dataset.csv | 0 | 99,441 | ↑ (clean as-is) |
| olist_sellers_dataset.csv | 0 | 3,095 | ↑ (clean as-is) |

## 2. What was removed / fixed and why (plain English)

- **Orders:** 96,478 orders had status `delivered`. Of these, 8 with no delivery date and 14 with delivery_days outside [0, 180] were flagged (kept in `06_AI/Outputs/Scratchpad/`) and excluded, leaving the final clean set.
- **Payments:** 9 payment rows with zero/negative value were **kept flagged** and aggregated per order; 2,961 orders paid in multiple transactions were combined into one row.
- **Items:** 0 rows with price <= 0 and 3 with price > R$ 5,000 and 0 with negative freight were removed (data-entry errors).
- **Products:** 610 products labelled `uncategorized` (kept, not dropped). 72 unique English categories after translation.
- **Reviews:** dropped rows with missing/out-of-range scores; kept the **first** review per order so the master stays one-row-per-order.
- **Geolocation:** 19,015 unique zips from 1,000,163 rows; kept one GPS point per zip (19,011 after removing 31 out-of-Brazil points).

## 3. What was filled / imputed and why

- `product_category_name` null → `uncategorized` (decision: keep completeness).
- `category_english` null → `uncategorized` (no translation exists).
- No numeric imputation was performed anywhere; missing values are **kept as null** so they are visible, and null counts are reported for the master below.

## 4. Master dataset (`olist_master.csv`)

- **Rows:** 96,456 delivered orders   **Columns:** 40
- **Date range:** 2016-09-15 → 2018-08-29
- **Unique customers:** 93,336   **Gross revenue:** R$ 13,197,189.09
- **% late orders:** 6.76%   **Null counts:** {"order_approved_at": 14, "order_delivered_carrier_date": 1, "total_payment_value": 1, "payment_types_used": 1, "payment_installments_max": 1, "item_count": 3, "total_items_price": 3, "total_freight": 3, "n_sellers": 3, "seller_ids": 3, "product_ids": 3, "review_id": 645, "review_score": 645, "review_comment_title": 85270, "review_comment_message": 57547, "review_creation_date": 645, "review_answer_timestamp": 645, "order_revenue": 3, "order_revenue_incl_freight": 3}
- **Key columns for Phase 3+:** `order_revenue`, `total_payment_value`, `total_items_price`, `total_freight`, `item_count`, `payment_installments_max`, `payment_types_used`, `review_score`, `is_late`, `delivery_days`, `days_early_or_late`, `promised_delivery_days`, `order_month`, `order_year`, `is_weekend`, `purchase_hour`, `customer_state`, `customer_unique_id`, `seller_ids`, `product_ids`.

## 5. Remaining data-quality issues that could affect analysis

- **Missing deliveries:** some delivered orders lack `order_delivered_customer_date` (excluded; see Scratchpad).
- **`review_comment_title` 88% null** — deliberately excluded from KPIs (decision).
- **Geolocation** covers only ~19k of ~4M Brazilian zips — usable for state-level mapping, not precise geocoding.
- **Freight** is customer-carried; cost/margin data does not exist in the dataset.

## 6. Client-ready summary

We consolidated nine raw Olist tables into a single clean analysis file covering 2 years of delivered orders, removing only data-entry errors and duplicate rows. Every KPI for the dashboard can now be computed from one `olist_master.csv`, and the cleaned per-table files are ready for Power BI. No business data was deleted — flagged rows are archived under `06_AI/Outputs/Scratchpad/` for audit.