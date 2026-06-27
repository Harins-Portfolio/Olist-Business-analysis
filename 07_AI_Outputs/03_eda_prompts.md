# PHASE 3 — EXPLORATORY DATA ANALYSIS (EDA)
# All prompts use olist_master.csv from 02_Cleaned_Data
# Run prompts in order. Save every output before moving on.
# ============================================================

---

## PROMPT 3.1 — First look at the master dataset

```
Load 02_Cleaned_Data/olist_master.csv

Give me a complete first-look summary:
1. Total number of orders, total revenue, date range of the data
2. Average order value (total_payment_value / order count)
3. Average delivery time in days
4. Average review score
5. % of orders delivered late
6. Number of unique customers (customer_unique_id)
7. Number of unique sellers
8. Number of unique product categories

Present this as an executive snapshot — 8 numbers, clean labels, no code.
This is the first slide of the dashboard.
Save to 07_AI_Outputs/eda_01_executive_snapshot.md
```

---

## PROMPT 3.2 — Revenue and order volume over time

```
Using olist_master.csv, analyse revenue and order volume over time.

1. Group by order_month. For each month calculate:
   - total revenue (SUM of total_payment_value)
   - order count (COUNT of order_id)
   - average order value (revenue / order count)

2. Show the results as a table sorted by date

3. Identify:
   - The best revenue month and worst revenue month
   - The month with the highest order volume
   - Whether overall trend is growing, flat, or declining
   - Any months that look like outliers (unusually high or low)

4. Explain in plain English what the trend tells us about the business

Save the table to 07_AI_Outputs/eda_02_revenue_over_time.csv
Save the written analysis to 07_AI_Outputs/eda_02_revenue_analysis.md
```

---

## PROMPT 3.3 — Revenue by product category

```
Using olist_master.csv, analyse revenue by product category.

For this we need to join with 02_Cleaned_Data/orders_items_aggregated.csv
and 02_Cleaned_Data/products_clean.csv to get category_english.

1. Calculate total revenue per category_english (SUM of price from order_items)
2. Calculate order count per category
3. Calculate average item price per category
4. Rank categories from highest to lowest revenue
5. Show the top 15 categories in a table
6. Calculate what % of total revenue the top 5 categories represent

Tell me:
- Which 3 categories should the business protect at all costs?
- Which categories have high order volume but low revenue (potential pricing issue)?
- Which categories have low volume but high average price (niche opportunities)?

Save to 07_AI_Outputs/eda_03_revenue_by_category.csv and eda_03_category_analysis.md
```

---

## PROMPT 3.4 — Customer geography analysis

```
Using olist_master.csv, analyse customers by geography.

1. Group by customer_state. For each state calculate:
   - customer count (unique customer_unique_id)
   - order count
   - total revenue
   - average order value
   - % of total revenue this state represents

2. Rank states by total revenue — show top 10

3. Calculate the revenue concentration:
   - What % of total revenue comes from SP (São Paulo)?
   - What % comes from the top 3 states combined?

4. Identify states with high customer count but low average order value
   (these may be price-sensitive markets)

5. Flag any states with fewer than 100 orders — these are underserved markets

Tell me in plain English:
- Where is the business strongest?
- Where are the growth opportunities?
- What is the geographic risk if São Paulo has a logistics disruption?

Save to 07_AI_Outputs/eda_04_customer_geography.csv and eda_04_geography_analysis.md
```

---

## PROMPT 3.5 — Customer behaviour: new vs returning

```
Using olist_master.csv, analyse new vs returning customer behaviour.

1. For each customer_unique_id, find their first order date and total order count
2. Classify each customer:
   - New = only 1 order in the dataset
   - Returning = 2 or more orders

3. Calculate:
   - Total unique customers
   - % who are new (only 1 order)
   - % who are returning (2+ orders)
   - Average orders per returning customer
   - Average revenue per new customer vs returning customer

4. Show new customer acquisition by month (first order date grouped by month)
   — is the business acquiring more new customers over time or plateauing?

5. For returning customers: what is the average gap in days between their first and second order?

Tell me:
- What does the repeat rate tell us about customer loyalty?
- What would revenue look like if the repeat rate doubled from current level?

Save to 07_AI_Outputs/eda_05_customer_behaviour.csv and eda_05_customer_analysis.md
```

---

## PROMPT 3.6 — Delivery performance analysis

```
Using olist_master.csv, analyse delivery performance.

1. Calculate overall:
   - Average delivery_days across all orders
   - Median delivery_days
   - Min and max delivery_days (flag extremes)
   - % of orders where is_late = 1

2. Group by customer_state. For each state:
   - Average delivery_days
   - % of orders late
   - Rank from worst to best delivery performance

3. Break down delivery time into stages (requires joining orders_clean.csv):
   - Approval time: order_approved_at minus order_purchase_timestamp
   - Carrier pickup time: order_delivered_carrier_date minus order_approved_at
   - Last mile time: order_delivered_customer_date minus order_delivered_carrier_date
   Show the average for each stage across all orders

4. Identify:
   - The 5 states with the worst on-time delivery rate
   - The 5 states with the longest average delivery time
   - Which stage (approval / pickup / last mile) is the biggest bottleneck

Tell me in plain English where the logistics problem is and who it affects most.

Save to 07_AI_Outputs/eda_06_delivery_performance.csv and eda_06_delivery_analysis.md
```

---

## PROMPT 3.7 — Customer satisfaction analysis

```
Using olist_master.csv, analyse customer satisfaction.

1. Overall review score distribution:
   - Count and % of reviews at each score (1 through 5)
   - Overall average score
   - % of reviews that are negative (score 1 or 2)

2. Review score by month — is satisfaction improving or declining over time?

3. Review score by customer_state — which states are least satisfied?

4. Delivery vs satisfaction correlation:
   - Create delivery time buckets: 0–7 days, 8–14 days, 15–21 days, 22–30 days, 30+ days
   - Calculate average review score for each bucket
   - Show as a table: delivery bucket → average score

5. Late delivery impact:
   - Average review score for on-time orders (is_late = 0)
   - Average review score for late orders (is_late = 1)
   - The difference between these two numbers is the "cost of lateness" in stars

Tell me:
- What is the single biggest driver of low review scores?
- What score improvement could we expect if the on-time rate reached 95%?

Save to 07_AI_Outputs/eda_07_satisfaction_analysis.csv and eda_07_satisfaction_analysis.md
```

---

## PROMPT 3.8 — Seller performance analysis

```
Using 02_Cleaned_Data/orders_items_aggregated.csv joined with sellers_dataset.csv
and olist_master.csv, analyse seller performance.

1. For each seller_id calculate:
   - Total revenue (SUM of price across their items)
   - Total orders fulfilled
   - Average order value
   - Average review score (join through order_id to reviews)
   - Average delivery_days for their orders
   - % of their orders that are late

2. Rank sellers by total revenue — show top 20

3. Identify problem sellers:
   - Sellers with more than 50 orders AND average review score below 3.0
   - Sellers with more than 50 orders AND late delivery rate above 30%

4. Identify star sellers:
   - Top 10 by revenue with review score above 4.0 AND late rate below 10%

Tell me:
- What % of total revenue comes from the top 10% of sellers?
- How many sellers should be flagged for review based on quality metrics?

Save to 07_AI_Outputs/eda_08_seller_performance.csv and eda_08_seller_analysis.md
```

---

## PROMPT 3.9 — EDA complete summary

```
Generate a complete EDA summary for the Olist project.

Read all files in 07_AI_Outputs/ that start with eda_

Compile a single summary document that contains:

1. EXECUTIVE SUMMARY (5–7 bullet points, each a headline finding)
   — write these as if presenting to a CEO in 60 seconds

2. KEY FINDINGS BY THEME
   - Revenue & Growth: top 3 findings
   - Customers: top 3 findings
   - Delivery & Operations: top 3 findings
   - Customer Satisfaction: top 3 findings
   - Sellers: top 2 findings

3. TOP 5 STRATEGIC RECOMMENDATIONS
   Each recommendation must follow this format:
   - Finding: [the data insight]
   - Business impact: [what this costs or risks in plain English]
   - Recommended action: [what the business should do]
   - Priority: High / Medium / Low

4. WHAT WE STILL DON'T KNOW
   List 2–3 questions the data raises but cannot fully answer

Save to 07_AI_Outputs/eda_COMPLETE_SUMMARY.md
This document becomes the foundation for the storytelling phase.
```
