# PROJECT SPEC — Olist E-Commerce Analysis
# ============================================================
# OPENCODE INSTRUCTIONS:
# - Read this file at the start of every session before doing any work
# - This file defines the complete scope, constraints, and execution rules
# - If something is not defined here, ask before proceeding — never assume
# ============================================================

---

## SPEC HEADER

**Project:** Olist E-Commerce Performance Analysis
**Client:** Olist (internal / portfolio project)
**Analyst:** Nikhil Harins
**Version:** 1.0
**Status:** Active
**Last updated:** 2026-06-28

---

## SECTION 1 — PROBLEM STATEMENT

Olist operates a Brazilian e-commerce marketplace connecting small sellers to major online platforms. Leadership lacks visibility into what is driving revenue growth, which operational bottlenecks are hurting customer satisfaction, and why repeat purchase rates are critically low. Without this analysis, the business cannot prioritise where to invest to improve performance.

**Success looks like:** An executive dashboard and written recommendations report that tells leadership exactly which 3 actions will have the highest impact on revenue and customer satisfaction, backed by 2 years of transaction data.

---

## SECTION 2 — SCOPE

### In scope
- Analysis of 9 Olist CSV files covering September 2016 to October 2018
- Revenue, customer retention, delivery performance, and satisfaction KPIs
- Geographic breakdown by Brazilian state
- Seller performance analysis
- Power BI executive dashboard (3 pages)
- Python charts for analysis validation
- Written executive summary and strategic recommendations report
- Presentation script for a 10-minute executive meeting

### Out of scope
- Predictive or machine learning models (Phase 7 — not in this engagement)
- Real-time data or live database connection
- Competitor benchmarking (no external data available)
- Cost or margin analysis (cost data not in dataset)
- Marketing attribution or campaign analysis

### Constraints
- Dataset covers 2016–2018 only — findings reflect that period, not current state
- No access to seller cost data — revenue analysis is gross revenue only
- Geolocation table has 1M+ rows of duplicates — must be deduplicated before use
- 610 products have no category — labelled 'uncategorized', not dropped
- customer_id inflates customer counts — must use customer_unique_id throughout

---

## SECTION 3 — DELIVERABLES

| Deliverable | Format | Saved to | Due |
|---|---|---|---|
| Cleaned master dataset | .csv | 02_Cleaned_data/olist_master.csv | End of Phase 2 |
| KPI tables (8 tables) | .csv | 02_Cleaned_data/kpi_tables/ | End of Phase 4 |
| KPI master dashboard file | .csv | 02_Cleaned_data/kpi_tables/KPI_MASTER_DASHBOARD.csv | End of Phase 4 |
| Python analysis charts (6) | .html or .ipynb if you are capable of creating a clean jupyter notebook for analysis no need for code yet just the structure with steps | 06_AI/Outputs/Generated_Charts/ | End of Phase 5 |
| Power BI dashboard | .pbix | 05_Power_Bi/ | End of Phase 5 |
| Executive summary (1 page) | .md | 07_Reports/ | End of Phase 6 |
| Recommendations report | .md | 07_Reports/ | End of Phase 6 |
| Presentation script | .md | 06_AI/Outputs/Generated_Docs/ | End of Phase 6 |
| Q&A talking points | .md | 06_AI/Outputs/Generated_Docs/ | End of Phase 6 |

---

## SECTION 4 — DATA SOURCES

| Table / file | Format | Location | Refresh cadence |
|---|---|---|---|
| olist_orders_dataset | CSV | 01_Raw_Data/ | Static — historical only |
| olist_order_items_dataset | CSV | 01_Raw_Data/ | Static |
| olist_order_payments_dataset | CSV | 01_Raw_Data/ | Static |
| olist_order_reviews_dataset | CSV | 01_Raw_Data/ | Static |
| olist_customers_dataset | CSV | 01_Raw_Data/ | Static |
| olist_sellers_dataset | CSV | 01_Raw_Data/ | Static |
| olist_products_dataset | CSV | 01_Raw_Data/ | Static |
| product_category_name_translation | CSV | 01_Raw_Data/ | Static |
| olist_geolocation_dataset | CSV | 01_Raw_Data/ | Static |

**Primary analysis table:** 02_Cleaned_data/olist_master.csv
**Source of truth for KPIs:** 02_Cleaned_data/kpi_tables/KPI_MASTER_DASHBOARD.csv

---

## SECTION 5 — ANALYSIS PLAN

| Step | Description | Input | Output | Prompt file | Status |
|---|---|---|---|---|---|
| 2.1 | Data quality audit | 01_Raw_Data/ | cleaning_audit.md | 02_cleaning_prompts.md | To do |
| 2.2 | Clean orders table | orders_dataset.csv | orders_clean.csv | 02_cleaning_prompts.md | To do |
| 2.3 | Clean payments table | payments_dataset.csv | payments_clean.csv | 02_cleaning_prompts.md | To do |
| 2.4 | Clean order items | order_items_dataset.csv | items_clean.csv + aggregated.csv | 02_cleaning_prompts.md | To do |
| 2.5 | Clean products table | products_dataset.csv | products_clean.csv | 02_cleaning_prompts.md | To do |
| 2.6 | Clean reviews table | reviews_dataset.csv | reviews_clean.csv | 02_cleaning_prompts.md | To do |
| 2.7 | Clean geolocation | geolocation_dataset.csv | geolocation_clean.csv | 02_cleaning_prompts.md | To do |
| 2.8 | Build master dataset | All clean tables | olist_master.csv | 02_cleaning_prompts.md | To do |
| 2.9 | Cleaning summary report | All cleaned files | cleaning_summary_report.md | 02_cleaning_prompts.md | To do |
| 3.1 | Executive snapshot | olist_master.csv | eda_01_executive_snapshot.md | 03_eda_prompts.md | To do |
| 3.2 | Revenue over time | olist_master.csv | eda_02_revenue_*.csv+.md | 03_eda_prompts.md | To do |
| 3.3 | Revenue by category | olist_master.csv | eda_03_by_category.csv+.md | 03_eda_prompts.md | To do |
| 3.4 | Geographic analysis | olist_master.csv | eda_04_geography.csv+.md | 03_eda_prompts.md | To do |
| 3.5 | Customer behaviour | olist_master.csv | eda_05_customer_*.csv+.md | 03_eda_prompts.md | To do |
| 3.6 | Delivery performance | olist_master.csv | eda_06_delivery_*.csv+.md | 03_eda_prompts.md | To do |
| 3.7 | Satisfaction analysis | olist_master.csv | eda_07_satisfaction_*.csv+.md | 03_eda_prompts.md | To do |
| 3.8 | Seller performance | olist_master.csv | eda_08_seller_*.csv+.md | 03_eda_prompts.md | To do |
| 3.9 | EDA complete summary | 06_AI/Outputs/Generated_Insights/eda_* | eda_COMPLETE_SUMMARY.md | 03_eda_prompts.md | To do |
| 4.0 | Create kpi_tables folder | — | 02_Cleaned_data/kpi_tables/ | 04_kpi_prompts.md | To do |
| 4.1 | Revenue KPI table | olist_master.csv | kpi_revenue_*.csv | 04_kpi_prompts.md | To do |
| 4.2 | Delivery KPI table | olist_master.csv | kpi_delivery_*.csv | 04_kpi_prompts.md | To do |
| 4.3 | Satisfaction KPI table | olist_master.csv | kpi_satisfaction_*.csv | 04_kpi_prompts.md | To do |
| 4.4 | Retention KPI table | olist_master.csv | kpi_retention_*.csv | 04_kpi_prompts.md | To do |
| 4.5 | Category KPI table | olist_master.csv | kpi_revenue_by_category.csv | 04_kpi_prompts.md | To do |
| 4.7 | KPI master dashboard | kpi_tables/ | KPI_MASTER_DASHBOARD.csv | 04_kpi_prompts.md | To do |
| 5.1 | Revenue trend chart | kpi_revenue_monthly.csv | chart_01_revenue_trend.html | 05_visualization_prompts.md | To do |
| 5.2 | Category bar chart | kpi_revenue_by_category.csv | chart_02_by_category.html | 05_visualization_prompts.md | To do |
| 5.3 | Delivery by state chart | kpi_delivery_by_state.csv | chart_03_delivery_by_state.html | 05_visualization_prompts.md | To do |
| 5.4 | Delivery vs satisfaction | olist_master.csv | chart_04_delivery_vs_satisfaction.html | 05_visualization_prompts.md | To do |
| 5.5 | Brazil heatmap | kpi_delivery_by_state.csv | chart_05_brazil_heatmap.html | 05_visualization_prompts.md | To do |
| 5.6 | Review score overview | kpi_satisfaction_monthly.csv | chart_06_satisfaction_overview.html | 05_visualization_prompts.md | To do |
| 5.7 | Power BI data model | kpi_tables/ | — (instructions only) | 05_visualization_prompts.md | To do |
| 5.8 | Power BI DAX measures | kpi_tables/ | — (DAX code) | 05_visualization_prompts.md | To do |
| 5.9 | Power BI layout plan | kpi_tables/ | — (layout spec) | 05_visualization_prompts.md | To do |
| 6.1 | Narrative arc | eda_COMPLETE_SUMMARY.md | storytelling_narrative_arc.md | 06_storytelling_prompts.md | To do |
| 6.2 | Executive summary | KPI_MASTER_DASHBOARD.csv | olist_executive_summary.md | 06_storytelling_prompts.md | To do |
| 6.3 | Presentation script | narrative_arc.md | presentation_script.md | 06_storytelling_prompts.md | To do |
| 6.4 | Recommendations report | All outputs | olist_recommendations_report.md | 06_storytelling_prompts.md | To do |
| 6.5 | Q&A talking points | eda_COMPLETE_SUMMARY.md | qa_talking_points.md | 06_storytelling_prompts.md | To do |
| 6.6 | Completion checklist | All folders | project_completion_checklist.md | 06_storytelling_prompts.md | To do |

---

## SECTION 6 — QUALITY RULES

### Data rules
- [ ] No analysis uses raw files from 01_Raw_Data/ — only cleaned files from 02_Cleaned_data/
- [ ] All revenue figures use payment_value (from payments table) not price (item-level only)
- [ ] All customer counts use customer_unique_id — never customer_id
- [ ] Only delivered orders (order_status = 'delivered') used for revenue and satisfaction analysis
- [ ] Geolocation: one row per zip_code_prefix only

### Output rules
- [ ] Every number in a report traces back to a file in kpi_tables/ or 06_AI/Outputs/
- [ ] No invented figures — if data doesn't support a claim, flag it explicitly
- [ ] Every chart has a title, axis labels, and a plain English subtitle
- [ ] Every analysis output ends with a "What this means for the business" paragraph

### Language rules
- [ ] No statistics jargon without a plain English translation
- [ ] No hedging language: "appears to", "seems like", "it could be"
- [ ] All recommendations use action verbs: "implement", "reduce", "target", "prioritise"
- [ ] Executive summary language: confident, specific, number-backed

---

## SECTION 7 — DECISIONS LOG

| Date | Decision | Reason | Made by |
|---|---|---|---|
| 2026-06-28 | Analyse delivered orders only | Cancelled/processing orders distort revenue and satisfaction KPIs | Niki |
| 2026-06-28 | Label missing product categories as 'uncategorized' — do not drop | 610 products still have valid sales data worth keeping | Niki |
| 2026-06-28 | Use customer_unique_id for all customer counts | customer_id inflates count — one person can have multiple IDs | Niki |
| 2026-06-28 | Geolocation: keep first row per zip_code_prefix | 1M+ rows reduced to ~19K unique zips — duplicates add no value | Niki |
| 2026-06-28 | Currency stays in BRL — no conversion | Dataset is domestic Brazil — conversion adds no analytical value | Niki |
| 2026-06-28 | No churn prediction model in this engagement | Out of scope for Phase 7 — flag as future opportunity only | Niki |

---

## SECTION 8 — OPEN QUESTIONS

| # | Question | Blocking what? | Status |
|---|---|---|---|
| 1 | Should freight_value be included in total revenue or kept separate? | Step 4.1 — Revenue KPI | Open |
| 2 | Is the data from a single seller's account or the full marketplace? | Context for all analysis | Open |

---

## SECTION 9 — SESSION LOG

| Date | What was completed | What comes next |
|---|---|---|
| 2026-06-28 | Project spec created. CLAUDE.md complete. Prompt library built. | Run Phase 2 Prompt 2.1 — data quality audit |

---
*Spec version controlled manually — update version number and date on every significant change.*
