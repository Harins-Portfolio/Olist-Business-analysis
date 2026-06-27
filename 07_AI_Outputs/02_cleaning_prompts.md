# PHASE 2 — DATA CLEANING & PREPARATION
# Copy-paste these prompts into OpenCode one at a time.
# Complete each prompt fully before moving to the next.
# ============================================================

---

## PROMPT 2.1 — Full data quality audit (run this first)

```
I have 9 CSV files in 01_Raw_Data for the Olist project.
Run a full data quality audit across all files.

For each file report:
1. Row count and column count
2. Count of null/missing values per column (show as number and %)
3. Count of duplicate rows
4. Data type of each column (date, number, text)
5. Any columns where values look wrong (negatives in price, future dates, etc.)

Format the output as a clean summary table.
Do not fix anything yet — just report what you find.
Save the report to 07_AI_Outputs/cleaning_audit.md
```

---

## PROMPT 2.2 — Orders table cleaning

```
Clean the olist_orders_dataset.csv file. Follow these steps exactly:

1. Show me the count of each value in order_status before we do anything
2. Filter to only orders where order_status = 'delivered' — save this as a separate file called orders_delivered.csv in 02_Cleaned_Data
3. Check the 4 date columns for nulls:
   - order_purchase_timestamp
   - order_approved_at
   - order_delivered_carrier_date
   - order_delivered_customer_date
   Show me the null count for each
4. For delivered orders: flag any row where order_delivered_customer_date is null — save flagged rows to 07_AI_Outputs/orders_delivery_date_missing.csv
5. Calculate delivery_days = order_delivered_customer_date minus order_purchase_timestamp (in days)
6. Flag any delivery_days values below 0 or above 180 as outliers
7. Show me a summary: total delivered orders, orders with complete dates, orders flagged

Save the cleaned delivered orders (no nulls in dates, no outlier flags) to 02_Cleaned_Data/orders_clean.csv
Tell me in plain English what was removed and why.
```

---

## PROMPT 2.3 — Payments table cleaning

```
Clean the olist_order_payments_dataset.csv file.

1. Show me the count of each payment_type value
2. Check for any payment_value that is 0 or negative — show me those rows
3. Check for nulls in all columns
4. Some orders have multiple payment rows (split payments) — show me the count of orders with more than one payment row
5. Create an aggregated payments table: one row per order_id, with:
   - total_payment_value = SUM of all payment_value rows for that order
   - payment_types_used = list of payment types used (e.g. "credit_card, voucher")
   - payment_installments_max = highest installments value for that order
6. Confirm the row count of the aggregated table matches the number of unique order_ids

Save to 02_Cleaned_Data/payments_clean.csv
Explain what aggregating payments means for the analysis.
```

---

## PROMPT 2.4 — Order items table cleaning

```
Clean the olist_order_items_dataset.csv file.

1. Check for nulls in all columns
2. Check price column: show min, max, average. Flag any price = 0 or price > 5000
3. Check freight_value column: show min, max, average. Flag any freight_value < 0
4. Some orders have multiple items — show me the count of orders with more than one item row
5. Create two outputs:
   a. items_clean.csv — the full cleaned items table with flagged rows removed
   b. orders_items_aggregated.csv — one row per order_id with:
      - item_count = number of items in the order
      - total_items_price = SUM of price for all items
      - total_freight = SUM of freight_value
      - seller_ids = list of unique seller_ids in the order
      - product_ids = list of product_ids in the order

Save both to 02_Cleaned_Data/
Tell me: what % of orders contain more than one item?
```

---

## PROMPT 2.5 — Products table cleaning

```
Clean the olist_products_dataset.csv file.

1. Show me the count of rows where product_category_name is null or empty
2. For those rows: fill product_category_name with the text 'uncategorized'
3. Join with product_category_name_translation.csv on product_category_name
4. Add a new column called category_english using the English translation
5. For rows where no translation exists (including 'uncategorized'), set category_english = 'uncategorized'
6. Show me the top 20 categories by product count after translation
7. Check for nulls in product dimensions (length, height, width, weight) — show counts

Save to 02_Cleaned_Data/products_clean.csv
Tell me: how many unique categories exist after translation?
```

---

## PROMPT 2.6 — Reviews table cleaning

```
Clean the olist_order_reviews_dataset.csv file.

1. Check for nulls in review_score — show count
2. Confirm review_score only contains values 1, 2, 3, 4, 5 — flag any outside this range
3. Show me the distribution: count of reviews at each score (1 through 5) and the % each represents
4. Check review_comment_message: what % of reviews have a written comment?
5. Create a clean reviews file with:
   - order_id
   - review_score
   - review_comment_message (keep even if null)
   - review_creation_date

Save to 02_Cleaned_Data/reviews_clean.csv
Tell me the overall average review score.
```

---

## PROMPT 2.7 — Geolocation table cleaning

```
Clean the olist_geolocation_dataset.csv file.

The problem: this file has 1,000,163 rows but only ~19,000 unique zip codes.
We need one GPS coordinate per zip code.

1. Show me the count of unique zip_code_prefix values
2. Deduplicate: keep only the first row per zip_code_prefix
3. Confirm the row count after deduplication
4. Check for any lat/lng values that fall outside Brazil's geographic bounds:
   - Latitude must be between -34 and 6
   - Longitude must be between -74 and -28
   Flag any rows outside these bounds
5. Remove flagged rows

Save to 02_Cleaned_Data/geolocation_clean.csv
Tell me how many zip codes we have after cleaning.
```

---

## PROMPT 2.8 — Master joined dataset

```
Now that all individual tables are clean, build the master analysis table.
Join the cleaned files to create one flat table for analysis.

Join order:
1. Start with orders_clean.csv (base — delivered orders only)
2. Join customers_dataset.csv on customer_id → add customer_unique_id, customer_city, customer_state
3. Join payments_clean.csv on order_id → add total_payment_value, payment_types_used
4. Join orders_items_aggregated.csv on order_id → add item_count, total_items_price, total_freight
5. Join reviews_clean.csv on order_id → add review_score, review_comment_message
6. Add calculated columns:
   - delivery_days = order_delivered_customer_date minus order_purchase_timestamp (days)
   - days_early_or_late = order_estimated_delivery_date minus order_delivered_customer_date (positive = early, negative = late)
   - is_late = 1 if days_early_or_late < 0, else 0
   - order_month = month and year extracted from order_purchase_timestamp

Show me:
- Final row count
- Final column list
- Count of nulls per column in the final table
- % of orders that are late

Save to 02_Cleaned_Data/olist_master.csv
This is the file we use for all analysis from Phase 3 onward.
```

---

## PROMPT 2.9 — Cleaning summary report

```
Generate a cleaning summary report for the Olist project.

The report should contain:
1. Original row counts vs final row counts for each table
2. What was removed from each table and why (in plain English)
3. What was filled or imputed and why
4. The final master dataset: row count, column count, date range covered
5. Any data quality issues that remain and could affect analysis
6. A 3-sentence plain English summary suitable for a client status update

Format it as a clean markdown document.
Save to 07_AI_Outputs/cleaning_summary_report.md
```
