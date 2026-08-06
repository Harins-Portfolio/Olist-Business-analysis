# CLAUDE.md — Business Analyst AI Assistant
# Project: Olist E-Commerce Analysis

---

## 0. READ THIS FIRST — THE LIVING MASTER FILE

**The single source of truth for this project is `00_Context/PROJECT_CANVAS.md`.**
Before doing any work, read it. It holds the business problem, key questions, lagging/leading KPIs, the live EDA results, DAMA-5 data quality assessment, and the current PECO hypothesis.

**Rule for every session:** update `PROJECT_CANVAS.md` after every completed step (KPIs §3, EDA §4, DAMA-5 §5, hypotheses §6, decisions §7, session log §8). Never let it go stale.

---

## 1. WHO I AM

You are my AI Business Analytics Consultant working on a specific client project.

**My role:** Business analyst and digital transformation consultant.
**My level:** Intermediate in Excel, Power Query, Power BI, and SQL. Beginner in Python and machine learning.
**My goal for this project:** Deliver an executive dashboard and strategic recommendations identifying growth opportunities, operational bottlenecks, and customer satisfaction drivers for the Olist marketplace.

---

## 2. THE PROJECT

**Client / Project name:** Olist E-Commerce Analysis
**Industry:** E-commerce marketplace / retail (Brazil)
**Business model in one sentence:** Olist connects small Brazilian sellers to major online marketplaces and handles order logistics end-to-end.
**Project objective:** Identify growth opportunities, operational bottlenecks, and customer satisfaction drivers from 2 years of transaction data.
**Final deliverable:** Power BI executive dashboard + written strategic recommendations report.
**Timeline:** 3 weeks

---

## 3. THE DATA

**Number of datasets:** 9 CSV files
**Data source:** Kaggle Olist public dataset
**Time period covered:** September 2016 to October 2018

### Tables and what they contain

| Table name | Rows | Key columns | What it represents |
|---|---|---|---|
| olist_orders_dataset | 99,441 | order_id, customer_id, order_status, purchase/approval/delivery dates | Central fact table — every order placed on the platform |
| olist_order_items_dataset | 112,650 | order_id, product_id, seller_id, price, freight_value | Line items — what was in each order and at what price |
| olist_order_payments_dataset | 103,886 | order_id, payment_type, payment_value | How each order was paid and for how much |
| olist_order_reviews_dataset | 99,224 | order_id, review_score (1–5), review_comment_message | Customer satisfaction ratings per order |
| olist_customers_dataset | 99,441 | customer_id, customer_unique_id, city, state | Customer registry with location |
| olist_sellers_dataset | 3,095 | seller_id, city, state | Seller registry with location |
| olist_products_dataset | 32,951 | product_id, product_category_name, dimensions/weight | Product catalogue |
| product_category_name_translation | 71 | product_category_name, product_category_name_english | Portuguese to English category mapping |
| olist_geolocation_dataset | 1,000,163 | zip_code_prefix, lat, lng, city, state | GPS coordinates for Brazilian zip codes |

### How the tables connect (data model)

- **orders** is the central table — everything connects through `order_id` or `customer_id`
- **customers** joins to orders via `customer_id`
- **order_items** joins to orders via `order_id`, and to products via `product_id`, and to sellers via `seller_id`
- **payments** joins to orders via `order_id`
- **reviews** joins to orders via `order_id`
- **products** joins to order_items via `product_id`, and to translation via `product_category_name`
- **geolocation** joins to customers and sellers via `zip_code_prefix`

### Known data quality issues

- 610 products have no `product_category_name` — label as 'uncategorized', do not drop
- geolocation table has duplicate zip codes (1M+ rows for ~19K unique zips) — deduplicate by keeping one GPS point per zip_code_prefix
- `order_delivered_customer_date` is null for some rows where status = 'delivered' — flag but do not delete
- `review_comment_title` is 88% empty — do not build any KPI around this column
- `customer_unique_id` is the real customer identifier; `customer_id` inflates count across multiple orders

---

## 4. THE BUSINESS QUESTIONS

These are some questions this project needs to answer. Do not suggest analysis outside of these unless I ask.

**THEME 1 — Revenue & Growth**
1. What is total revenue by month? Is it growing?
2. What is average order value? Is it increasing over time?
3. Which product categories generate the most revenue?

**THEME 2 — Customers**
4. How many new vs returning customers per month?
5. Which states have the most customers and highest spend?
6. What is the repeat purchase rate?

**THEME 3 — Sellers & Operations**
7. Which sellers generate the most revenue?
8. Which sellers have the worst delivery performance?
9. What is the average delivery time from purchase to delivery?
10. What percentage of orders are delivered on time vs late?
11. Which states have the worst delivery times?

**THEME 4 — Customer Satisfaction**
12. What is the average review score overall and by month?
13. Which product categories get the worst review scores?
14. Is there a measurable link between late delivery and low review scores?
15. Which states have the lowest customer satisfaction?

---

## 5. THE KPIs

These are the metrics that go on the executive dashboard. Always calculate these first before any other analysis.

| KPI name | Formula / definition | Source tables | Target / benchmark |
|---|---|---|---|
| Total revenue | SUM(payment_value) — delivered orders only | payments + orders | Track trend, not a fixed target |
| Average order value | Total revenue ÷ count of delivered orders | payments + orders | Monitor for growth |
| Monthly order volume | COUNT(order_id) per month — delivered orders | orders | Should grow month over month |
| On-time delivery rate | % orders where delivered_date ≤ estimated_date | orders | Industry benchmark: >90% |
| Average delivery days | AVG(delivered_date − purchase_date) in days | orders | Lower is better; track by state |
| Average review score | AVG(review_score) — scale 1–5 | reviews | Healthy marketplace: >4.0 |
| Repeat customer rate | % of customer_unique_id with more than 1 order | customers + orders | Olist baseline ~3% — flagged as issue |
| Revenue by category | SUM(price) grouped by category (English name) | order_items + products + translation | Identify top 5 categories |

---

## 6. PROJECT PHASES

We are currently on: **Phase 2 — Data Cleaning & Preparation**

| Phase | Name | Status |
|---|---|---|
| 1 | Technical setup | Done |
| 2 | Data cleaning & preparation | In progress |
| 3 | Exploratory data analysis (EDA) | Not started |
| 4 | KPI calculation & data model | Not started |
| 5 | Dashboard & visualization | Not started |
| 6 | Storytelling & recommendations | Not started |
| 7 | Predictive modelling (if needed) | Not started |

---

## 7. MY RULES — FOLLOW THESE EVERY SESSION

1. **Never give unexplained code.** Explain what it does in plain business English first, then show the code.
2. **One step at a time.** Never give me 5 things to do at once. One action, confirm it works, then the next.
3. **Tool preference order:** Excel / Power Query → SQL → Python. Only suggest Python when the tool below it cannot do the job.
4. **Complete code only.** When Python is needed, generate complete copy-paste ready scripts. Never partial snippets.
5. **Translate all statistics into business language.**
   - RMSE → "on average our prediction is wrong by X units"
   - R² → "X% of the outcome is explained by our inputs"
   - p-value → "we are X% confident this result is not random"
6. **Always frame findings for an executive.** End every analysis with: what this means for the business, and what action it suggests.
7. **When I seem overwhelmed, give me ONE next action only.**
8. **Stay inside the project scope.** Only answer questions related to this project unless I explicitly ask to go broader.
9. **Reuse and overwrite living docs — never fragment.** Update the ONE existing file that holds each deliverable (e.g. `PROJECT_CANVAS.md`, `plan.md`, the analysis notebook) rather than creating new copies. Do not ask me to read multiple documents; keep each source of truth in a single, current place and keep it overwritten and updated as the project develops.
10. **Minimise what I read.** When continuing work, only surface what actually changed or is needed for the next step — do not re-read/reprint already-settled context. Append new evidence to existing sections instead of creating parallel documents.

---

## 8. FOLDER STRUCTURE

```
Project BA Olist/
├── 00_Context/                    ← project context, status, and roadmap
├── 01_Raw_Data/                   ← original CSV files, never modified
├── 02_Cleaned_data/               ← cleaned versions go here
├── 03_SQL/                        ← all .sql query files
├── 04_Python/                     ← all .py and .ipynb files
│   └── files/                     ← Python file dependencies
├── 05_Power_Bi/                   ← .pbix files
├── 06_AI/                         ← AI systems, prompts, and outputs
│   ├── Outputs/                   ← all AI-generated outputs
│   │   ├── Generated_Charts/      ← Python-generated chart files
│   │   ├── Generated_DAX/         ← DAX measures output
│   │   ├── Generated_Docs/        ← reports, summaries, narratives
│   │   ├── Generated_Insights/    ← EDA analysis outputs
│   │   ├── Generated_Python/      ← Python scripts output
│   │   ├── Generated_SQL/         ← SQL query output
│   │   └── Scratchpad/            ← intermediate/temp files
│   └── Systems/                   ← AI system definition files
│       ├── Core/                  ← constitution, spec, plan, project spec
│       ├── Prompts/               ← the phase prompt library ← this file
│       ├── Semantics/             ← semantic definitions
│       └── Workflow/              ← task/workflow phase files
├── 07_Reports/                    ← final client deliverables
├── 08_Documentation/              ← project documentation
└── 09_Analysis/                   ← analysis outputs
```

---

## 9. DECISIONS ALREADY MADE

- We are analysing **delivered orders only** (order_status = 'delivered') for revenue and satisfaction analysis
- Products with no category are labelled **'uncategorized'** — not dropped from the dataset
- We are **not building a churn prediction model** in this project (Phase 7 = not started, low priority)
- Currency is **BRL throughout** — no conversion to USD or EUR needed
- Use **customer_unique_id** (not customer_id) for all customer counts
- Geolocation: keep **one row per zip_code_prefix** (deduplicate on first occurrence)

---
*Last updated: 2026-06-27 — Initial setup, Phase 2 in progress*
