# PHASE 4 — KPI CALCULATION & DATA MODEL
# These prompts build the final KPI tables that feed your Power BI dashboard.
# All outputs go to 02_Cleaned_data/kpi_tables/ — Power BI connects to this folder.
# ============================================================

---

## PROMPT 4.0 — Create KPI output folder

```
Create the folder 02_Cleaned_data/kpi_tables/
This is where all KPI output files will be saved.
Confirm the folder exists and is empty.
```

---

## PROMPT 4.1 — KPI: Total revenue and order volume (monthly)

```
Using olist_master.csv, build the monthly revenue KPI table.

Create a table with one row per month containing:
- year_month (format: YYYY-MM, e.g. 2017-01)
- total_revenue (SUM of total_payment_value)
- order_count (COUNT of order_id)
- avg_order_value (total_revenue / order_count, rounded to 2 decimal places)
- mom_revenue_change (% change in total_revenue vs previous month)
   — null for the first month
- mom_order_change (% change in order_count vs previous month)
   — null for the first month

Also calculate these overall totals (put in a separate single-row summary table):
- grand_total_revenue
- grand_total_orders
- overall_avg_order_value
- best_revenue_month
- worst_revenue_month
- revenue_growth_rate (% change from first full month to last full month)

Save monthly table to 02_Cleaned_data/kpi_tables/kpi_revenue_monthly.csv
Save summary table to 02_Cleaned_data/kpi_tables/kpi_revenue_summary.csv

Tell me: is the business growing, flat, or declining? Give me one sentence.
```

---

## PROMPT 4.2 — KPI: On-time delivery rate

```
Using olist_master.csv, build the delivery performance KPI table.

Create a monthly delivery KPI table with one row per month:
- year_month
- total_orders
- on_time_orders (is_late = 0)
- late_orders (is_late = 1)
- on_time_rate (on_time_orders / total_orders, as %)
- avg_delivery_days
- avg_days_early_or_late (positive = delivered early, negative = late)

Create a state-level delivery KPI table with one row per customer_state:
- customer_state
- total_orders
- on_time_rate (%)
- avg_delivery_days
- delivery_performance_rank (1 = best, ranked by on_time_rate)

Calculate overall KPIs (single-row summary):
- overall_on_time_rate (%)
- overall_avg_delivery_days
- best_state_delivery (state with highest on_time_rate, min 100 orders)
- worst_state_delivery (state with lowest on_time_rate, min 100 orders)

Save to:
- kpi_tables/kpi_delivery_monthly.csv
- kpi_tables/kpi_delivery_by_state.csv
- kpi_tables/kpi_delivery_summary.csv

Benchmark check: is our overall on-time rate above or below 90%?
```

---

## PROMPT 4.3 — KPI: Customer satisfaction score

```
Using olist_master.csv, build the customer satisfaction KPI table.

Create a monthly satisfaction KPI table:
- year_month
- avg_review_score (rounded to 2 decimal places)
- count_reviews
- score_1_count and score_1_pct
- score_2_count and score_2_pct
- score_3_count and score_3_pct
- score_4_count and score_4_pct
- score_5_count and score_5_pct
- negative_review_rate (% of scores 1 or 2)

Create a category-level satisfaction table (join with products_clean.csv):
- category_english
- avg_review_score
- count_reviews
- negative_review_rate (%)
- rank (1 = best score)

Create a delivery-vs-satisfaction table:
- delivery_bucket (0-7d, 8-14d, 15-21d, 22-30d, 30+d)
- avg_review_score
- order_count
- negative_review_rate (%)

Overall summary:
- overall_avg_review_score
- overall_negative_review_rate
- score_if_all_on_time (average review score for is_late = 0 orders only)
- score_when_late (average review score for is_late = 1 orders only)
- lateness_score_penalty (difference between the two — how many stars late delivery costs)

Save to:
- kpi_tables/kpi_satisfaction_monthly.csv
- kpi_tables/kpi_satisfaction_by_category.csv
- kpi_tables/kpi_satisfaction_vs_delivery.csv
- kpi_tables/kpi_satisfaction_summary.csv
```

---

## PROMPT 4.4 — KPI: Customer retention and repeat rate

```
Using olist_master.csv, build the customer retention KPI table.

Step 1 — Classify all customers:
For each customer_unique_id:
- first_order_date (MIN of order_purchase_timestamp)
- last_order_date (MAX of order_purchase_timestamp)
- total_orders
- total_revenue (SUM of total_payment_value)
- customer_type: 'new' if total_orders = 1, 'returning' if total_orders >= 2

Step 2 — Monthly new customer acquisition:
- year_month (using first_order_date)
- new_customers_acquired

Step 3 — Overall retention KPIs (single-row summary):
- total_unique_customers
- new_customer_count and new_customer_pct
- returning_customer_count and returning_customer_pct
- repeat_purchase_rate (returning / total, as %)
- avg_revenue_per_new_customer
- avg_revenue_per_returning_customer
- revenue_uplift_from_retention (returning avg revenue minus new avg revenue)
- avg_days_between_orders (for returning customers only)

Step 4 — Projection scenario:
If repeat rate increased from current level to 10%:
- How many additional returning customers would that be?
- At the current avg revenue per returning customer, what would the additional revenue be?
Show this as a simple "what-if" table.

Save to:
- kpi_tables/kpi_customers_classified.csv
- kpi_tables/kpi_customer_acquisition_monthly.csv
- kpi_tables/kpi_retention_summary.csv
```

---

## PROMPT 4.5 — KPI: Revenue by category

```
Using order_items joined with products_clean.csv and olist_master.csv,
build the product category KPI table.

For each category_english calculate:
- total_revenue (SUM of price — not payment_value, this is item-level revenue)
- total_orders (COUNT of distinct order_id containing this category)
- total_items_sold (COUNT of item rows)
- avg_item_price (AVG of price)
- avg_review_score (joined from reviews)
- revenue_share_pct (this category's revenue / total revenue, as %)
- cumulative_revenue_pct (running total % — useful for Pareto analysis)

Also calculate:
- How many categories make up 80% of total revenue? (Pareto principle check)
- Top 5 categories by revenue (name them)
- Bottom 5 categories by revenue with more than 100 orders

Save to:
- kpi_tables/kpi_revenue_by_category.csv

Tell me: does the 80/20 rule apply here? What % of categories drive 80% of revenue?
```

---

## PROMPT 4.6 — Final KPI master dashboard table

```
Build the single master KPI table that Power BI will connect to.

This table has one row and contains every headline KPI in one place:

REVENUE
- total_revenue_brl
- avg_order_value_brl
- total_orders
- revenue_growth_rate_pct (first to last full month)
- best_revenue_month
- top_revenue_category

CUSTOMERS
- total_unique_customers
- repeat_purchase_rate_pct
- avg_revenue_per_customer_brl
- top_revenue_state

OPERATIONS
- overall_on_time_delivery_rate_pct
- avg_delivery_days
- worst_delivery_state
- lateness_rate_pct

SATISFACTION
- overall_avg_review_score
- negative_review_rate_pct
- lateness_score_penalty (stars lost due to late delivery)
- worst_satisfaction_category

Save to 02_Cleaned_data/kpi_tables/KPI_MASTER_DASHBOARD.csv

This file is the "single source of truth" for all headline numbers.
Any time a number appears on the dashboard, it traces back to this file.
```
