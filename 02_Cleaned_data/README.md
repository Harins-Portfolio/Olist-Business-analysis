# 02_Cleaned_data — Cleaned & Prepared Datasets

> **This folder holds the cleaned data products of the Olist project.**
> The CSVs themselves are **not committed to Git** (they are reproducible and excluded via `.gitignore`). This README explains what each file is, why there are more files than the 9 raw sources, and exactly how to regenerate everything from `01_Raw_Data/`.

---

## 1. Why are there more files than the raw data?

The raw data (`01_Raw_Data/`) contains **9 source CSVs**. Cleaning produces **11 files here** because the Phase-2 workflow (prompts 2.1–2.9) generates:

- **Cleaned versions** of each source table,
- **Aggregated** tables (payments & items condensed to one row per order),
- A **denormalized master** table (everything joined together),
- A **star schema** folder for Power BI (7 conformed tables).

All of them are derived from the same 9 sources. **No source file is ever modified.**

---

## 2. File inventory

| File | What it is | Grain (1 row =) | Needed for Power BI? |
|---|---|---|---|
| `olist_master.csv` | Master, denormalized analysis table (40 cols: revenue, freight, delivery, satisfaction, geo, derived flags) | 1 delivered order | Optional (flat alternative to the star) |
| `orders_clean.csv` | Orders with valid delivery dates, outliers removed, `delivery_days` added | 1 delivered order | No (intermediate) |
| `orders_delivered.csv` | All orders with status `delivered` (may lack a delivery date) | 1 delivered order | No (audit) |
| `payments_clean.csv` | Payments aggregated per order (total, types, max instalments) | 1 order | Building block |
| `items_clean.csv` | Full order-line detail (price, freight, product, seller) | 1 order line | Yes (line-level) |
| `orders_items_aggregated.csv` | Items summarized per order (counts, totals, seller/product lists) | 1 order | No (intermediate) |
| `products_clean.csv` | Product catalogue + English category (`category_english`) | 1 product | Yes (dimension) |
| `reviews_clean.csv` | Review scores + comments, one per order | 1 order | Building block |
| `geolocation_clean.csv` | One GPS point per zip code prefix | 1 zip code | Yes (maps) |
| `olist_customers_dataset.csv` | Customer dimension (copied as-is) | 1 customer | Yes (dimension) |
| `olist_sellers_dataset.csv` | Seller dimension (copied as-is) | 1 seller | Yes (dimension) |

### Key cleaning decisions (documented in `06_AI/Outputs/Generated_Docs/cleaning_summary_report.md`)
- **Delivered orders only** — the analysis universe is 96,456 orders (of 99,441).
- 8 delivered orders missing a delivery date and 14 with delivery days outside [0, 180] were **flagged** to `06_AI/Outputs/Scratchpad/` and excluded.
- 610 products without a category were labelled `uncategorized` (**kept, not dropped**).
- Geolocation deduplicated to 19,011 unique zips; 31 out-of-Brazil points removed.
- Reviews deduplicated to one per order so the master keeps a one-row-per-order grain.
- **Revenue is defined as merchandise (goods) value** — `order_revenue` ≈ R$ 13.2M (AOV R$ 137). Goods + freight (`order_revenue_incl_freight`) ≈ R$ 15.4M is also kept.

---

## 3. Regenerating the cleaned data (exact commands)

Requirements: Python 3.10+, `pandas`, `numpy`, `matplotlib`.

```bash
# 1. Reproduce all cleaned CSVs + master + audit/summary docs
python 04_Python/ETL/data_preparation.py

# 2. Reproduce the Power BI star schema (reads the cleaned CSVs)
python 04_Python/ETL/build_star_schema.py

# 3. Reproduce the insight charts (reads the master)
#    Run the notebook in Jupyter: 04_Python/visualization_insights.ipynb
```

Outputs land in:
- `02_Cleaned_data/` — cleaned tables + `olist_master.csv`
- `02_Cleaned_data/star_schema/` — Power BI model (see §4)
- `06_AI/Outputs/Generated_Docs/` — `cleaning_audit.md`, `cleaning_summary_report.md`
- `06_AI/Outputs/Generated_Charts/` — the 8 insight PNGs

> Because everything is reproducible, the data files are intentionally **not** in Git. Run the two scripts after cloning to obtain identical datasets.

---

## 4. Star schema for Power BI — `02_Cleaned_data/star_schema/`

The recommended way to consume the data in Power BI:

| Table | Grain | Rows |
|---|---|---|
| `Dim_Date` | 1 calendar day | 763 |
| `Dim_Customer` | 1 customer | 99,441 |
| `Dim_Product` | 1 product | 32,951 |
| `Dim_Seller` | 1 seller | 3,095 |
| `Dim_Geography` | 1 zip prefix (lat/lng) | 19,011 |
| `Fact_Orders` | 1 delivered order | 96,456 |
| `Fact_OrderItems` | 1 order line | 110,170 |

Relationships, DAX measures and the revenue double-count rule are documented in **`star_schema/data_model.md`**.

---

## 5. Data quality notes / remaining caveats

- `paid_amount` (customer-paid total) has 1 missing value — use `order_revenue_gross` instead.
- `review_score` is null for 645 orders (orders without a review) — keep null, do not impute.
- `review_comment_title` is ~88% null — deliberately excluded from KPIs.
- Geolocation covers ~19k of Brazil's ~4M zips — fine for state-level mapping, not precise geocoding.
- No cost/margin data exists in the dataset; revenue figures are gross (no returns/refunds adjustment).

---

_Generated 2026-08-06 · Source of truth: `00_Context/PROJECT_CANVAS.md` · Pipeline: `04_Python/ETL/data_preparation.py` + `build_star_schema.py`_
