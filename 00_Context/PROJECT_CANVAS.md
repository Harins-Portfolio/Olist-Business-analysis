# 📊 OLIST BUSINESS ANALYTICS — PROJECT CANVAS
> **THE MASTER FILE.** This document is the single source of truth for business understanding, evidence, and hypotheses for the Olist project. It is *living*: every agent/analyst session **must** run an EDA snapshot and update the relevant section of this file at the end of work. Never let this file go stale.

---

- **Last updated:** 2026-08-07
- **Owned by:** Nikhil Harins (Business Analyst) + AI Consultant
- **Project slug:** `olist`
- **Status:** Phase 1 complete → **Phase 2/3 — Full EDA complete** (delivered-order view) → cleaning + KPI formalisation next
- **Evidence source:** `04_Python/olist_full_analysis.ipynb` (consolidated step-by-step; old notebooks archived in `04_Python/archive/`) → `06_AI/Outputs/Generated_Insights/eda_summary.json`
- **Source of truth that generates this:** `06_AI/Systems/Core/CLAUDE_OLIST.md` + `spec.md`

---

## 1. THE BUSINESS PROBLEM — WHAT WE ARE SOLVING

**Client:** Olist — Brazilian e-commerce marketplace that connects small/medium sellers to major online platforms and handles logistics end-to-end.

**The problem (business language):**
Olist leadership lacks visibility into what actually drives revenue, which operational bottlenecks are hurting satisfaction, and why repeat purchase is critically low. Decisions on where to invest are being made without data.

**What success looks like (the "so what"):**
An executive dashboard + written recommendations that tell leadership **exactly which 3 actions will have the highest impact** on revenue and customer satisfaction — backed by 2 years (Sep 2016 – Oct 2018) of transaction data.

**Scope guardrails (what we are NOT doing):**
- No ML/predictive modeling (Phase 7 excluded from this engagement)
- No cost/margin analysis (cost data not in dataset) — gross revenue only
- No marketing attribution; results reflect 2016–18 only, in BRL

---

## 2. THE KEY BUSINESS QUESTIONS (from CLAUDE_OLIST.md §4)

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
10. What % of orders are delivered on time vs late?
11. Which states have the worst delivery times?

**THEME 4 — Customer Satisfaction**
12. What is the average review score overall and by month?
13. Which product categories get the worst reviews?
14. Is there a measurable link between late delivery and low review scores?
15. Which states have the lowest satisfaction?

---

## 3. KPIs — LAGGING & LEADING

### LAGGING KPIs (outcome / past results — what we are improving)
| KPI | Current baseline (**EDA 2026-08-06**) | Trend read | Target / Note |
|---|---|---|---|
| Total revenue | R$ 13,221,498 (delivered) | Growing, ~R$ 850–990k/mo mature | Track trend, no fixed target |
| Average order value (AOV) | **R$ 137.04** (median R$ 86.6) | **Flat–slightly declining** (2017: 138.95 → 2018: 136.80) | AOV is NOT rising — challenge |
| Monthly order volume | ~6.1k–7.3k/mo (peak Nov-2017 7,289) | +5%/mo median volume growth | Should keep growing |
| Repeat customer rate | **3.12%** ❌ (2,997 of 96,096 repeat) | **Critical failure — flat & tiny** | ~0.26% buy ≥3×; goal lift |
| Average review score | **4.16** (delivered) | Stable | Healthy >4.1 |

### LEADING KPIs (inputs / early-warning — what drives the outcomes)
| Leading KPI | Measured value | Why it matters |
|---|---|---|
| On-time delivery rate | **91.9%** (8,644 on-time of 96,470) | Strongest lever on satisfaction (r = −0.30) |
| Delivery time (days) | mean 12.1 / median 10 | 95.7% within 30d; drives score drop >22d |
| Freight burden | R$ 2.20M = **16.6% of revenue** | Hits satisfaction (score −0.13 w/ freight) |
| Payment instalments | 63.1% of revenue via >1 instalment (mean 2.85) | Credit-heavy mix; AOV & bad-debt signal |
| Category concentration | top 5 = 39.7% of revenue | Revenue growth depends on few categories |
| Seller concentration | top 1% = 25.5% of revenue; top 20% = 82.3% | **Single-point supply risk** |

**Rule:** Never compute lagging without its matching leading indicators, or we cannot act. **Biggest gap to close = repeat rate (3.12%).**

---

## 4. FULL EDA RESULTS (deep EDA executed `04_Python/olist_eda.ipynb`, 2026-08-06)

> Method: all analysis on **delivered orders only** (96,478 of 99,441), joined across orders/items/payments/reviews/customers/sellers/products. Numbers from "my merchant file" totals exclude non-delivered orders. Reproducible in `olist_eda.ipynb`.

### 4.0 THE ONE-LINE SUMMARY
> *"Olist is growing and healthy-satisfying, with two deep problems: it can't get customers to buy a second time (3.12% repeat), and delivery lateness destroys satisfaction (score 2.57 late vs 4.29 on-time) — likely one shared root cause."*

### 4.1 Scale & money
- Gross revenue (delivered): **R$ 13,221,498**
- Delivered orders: **96,478** · AOV **R$ 137.04** (median **R$ 86.58**)
- Freight revenue: **R$ 2,198,276 = 16.6% of total revenue**
- Unique customers: **96,596** · repeat rate **3.12%** (2,997 repeat; **only 252 buy ≥3× = 0.26%**)

### 4.2 Growth & seasonality
- **Market is growing**: volume median +5.0%/mo, revenue median +8.1%/mo; mature months R$ 838k–988k.
- **AOV is FLAT, not rising**: 2017 avg R$ 138.95 → 2018 R$ 136.80. Growth = volume, not value.
- **Black Friday spike**: Nov-2017 = 7,289 orders (**+81% vs monthly avg**), R$ 987,765 — biggest single revenue month. Dec-2017 Christmas (5,513 orders).
- Weekday vs weekend: 74,288 wkday vs 22,190 weekend orders; AOV near-equal (R$ 137 vs R$ 140).

### 4.3 Delivery, payments & freight (the operational drag)
- Mean delivery **12.1 days**, median 10 (25th=6, 75th=15, 90th=23, 95th=29, 99th=46).
- **On-time rate 91.9%** → 7,826 late orders (8.1%).
- Speed windows: **34.9% ≤7d · 72.7% ≤14d · 95.7% ≤30d** → the tail 15–30d is the squeeze.
- Payments (delivered): credit_card **R$ 12.1M (78.5%)**, boleto R$ 2.77M (17.9%), debit R$ 0.21M, voucher R$ 0.34M. **63.1% of revenue pays in >1 instalment** (mean 2.85).
- **Freight = 16.6% of revenue** (the customer-carried logistics cost).

### 4.4 Satisfaction (the quality picture)
- Average review score **4.16** (delivered); **78.9% rate 4–5★**, **12.8% rate 1–2★** (a thick dissatisfaction tail).
- Score mix: 1★=9,406 · 2★=2,941 · 3★=7,961 · 4★=18,987 · 5★=57,066.

### 4.5 THE DELIVERY→SATISFACTION EFFECT (validated by EDA)
- **On-time orders score 4.29 vs LATE orders 2.57 → 1.73-point gap** (t=89.6, p<0.001, significant).
- Score decays with wait: **≤7d 4.41 → 8–14d 4.29 → 15–21d 4.10 → 22–30d 3.49 → 31–60d 2.18 → 60d+ 2.18**. Satisfaction collapses at ~3 weeks.
- **delivery_days vs score r = −0.30** (the dominant driver); freight vs score −0.13.

### 4.6 Geography — Southeast dependence, North/Northeast problems
- Customer revenue: **SP 38.3%** → RJ 13.8% → MG 12.0% (**top3 = 63.4%**).
- **Sellers are even more concentrated: SP = 64.6% of seller revenue.**
- Slowest states (avg days): RR 28.0, AM 26.0, AL 24.0, PA 23.3, MA 21.2 — all North/Northeast.
- Worst on-time %: AL 76%, MA 80%, SE 84%, CE 84%, PI 85%.
- **Lowest review states**: MA 3.77, AL 3.82, PA 3.84, BA 3.86, CE 3.87 — *the states with worst delivery are the states with worst satisfaction — the two problems compound.*
- Fastest/impact state SP: **8.26 days, score 4.18**, 44,441 delivered orders.

> ⚠️ gap-hour-to-month trend, top-10 category runs, seller-review interaction, and inter-state deep review breakdown = **Phase 3 scope**.

---

## 5. DAMA-5 — DATA QUALITY ASSESSMENT (per dataset, baseline 2026-08-06)

Dimensions assessed: **Completeness, Consistency, Accuracy, Timeliness, Uniqueness.** Score scale: ✅ pass · ☑ partial · ❌ fail (to clean).

| Dataset | Rows | Completeness | Consistency | Accuracy | Timeliness | Uniqueness | Notes / action |
|---|---|---|---|---|---|---|---|
| olist_customers | 99,441 | ✅ no nulls | ✅ | ✅ `customer_unique_id` **must** use (not customer_id) | ✅ | ✅ 0 dups | clean |
| olist_geolocation | 1,000,163 | ✅ no nulls | ✅ | ☐ ~19k real zips inside 1M rows | ✅ | ❌ **261,831 dups** | dedup 1 GPS/zips; drop carrier |
| olist_order_items | 112,650 | ✅ | ✅ | ✅ | ✅ | ✅ | clean |
| olist_order_payments | 103,886 | ✅ | ☐ 3 rows `not_defined` | ✅ | ✅ | ✅ | 3 `not_defined` kept+aggregated (negligible) |
| olist_order_reviews | 99,224 | ❌ `review_comment_title` 88% null; message 59% null | ✅ | ✅ | ✅ | ✅ | exclude title column from KPIs |
| olist_orders | 99,441 | ☐ approval nil 160·carrier 1,783·delivery 2,965 | ✅ | ☐ status spread (approved/created/… 5–325 rows) | ✅ | ✅ | filter `delivered`; flag null dates |
| olist_products | 32,951 | ☐ 610 uncategorized + 2 null dimension rows | ✅ | ✅ | ✅ | ✅ | label `uncategorized`; drop 2 null dims |
| olist_sellers | 3,095 | ✅ | ✅ | ✅ | ✅ | ✅ | clean |
| product_category_translation | 71 | ✅ | ✅ | ✅ | ✅ | ✅ | lookup |

**DAMA-5 summary:** 3 tables fail on a dimension (geolocation↦dups, reviews↦completeness, payments↦consistency). Two are benign-in-enhance (reviews title, 3 payment rows). **One structural fixing needed = geolocation dedup.** Orders/completeness handled by filtering to `delivered`.

---

## 6. PECO — FIRST HYPOTHESIS (Population · Exposure · Comparison · Outcome)

- **Population (P):** Olist customers in Brazil who placed a delivered order Sep-2016 → Oct-2018.
- **Exposure (E):** An order whose delivery exceeded the estimated delivery window (**late delivery**).
- **Comparison (C):** On-time delivered orders (delivered ≤ estimated) within the same population & period.
- **Outcome (O):** Customer satisfaction as measured by **review score (1–5)**.

**HYPOTHESIS H1 (business language):**
> *"Customers whose order is delivered LATE are measurably less satisfied than customers delivered ON TIME — and this gap (2.57 vs 4.29) drives low review scores and contributes to the failing repeat rate."*

**Evidence — EDA 2026-08-06 (VALIDATED ✅):**
- On-time avg score **4.29** vs late **2.57** → **1.73-point gap**, statistically significant (**t=89.6, p<0.001**).
- Dose–response: score 4.41 at ≤7d → 3.49 at 22–30d → **2.18 at 31–60d** (collapse at ~3 weeks).
- Correlation delivery_days vs score = **r −0.30** (dominant driver in the data).

**Null hypothesis:** REJECTED — late delivery has a large, significant negative effect on review score.

**PECO follow-on (Phase 3/4):**
1. Category × late-delivery interaction on score (do high-value cats suffer more?).
2. State-level test: NE states (worst delivery) should show worst scores — confirmed directionally in EDA (MA 3.77, AL 3.82).
3. Link test: does repeat purchase drop *after* a late delivery? (retention ↔ satisfaction link).

---

## 7. DECISIONS LOG (tracked — do not rewrite history)
| Date | Decision | By | Rationale |
|---|---|---|---|
| 2026-08-06 | Analyse **delivered orders only** for revenue/satisfaction | Spec §decisions | align with CLAUDE, excludes cancelled/other statuses |
| 2026-08-06 | Label 610 products `uncategorized`, **do not drop** | Spec §decisions | keep data complete |
| 2026-08-06 | Use `customer_unique_id` for all customer counts | Spec §decisions | `customer_id` inflates |
| 2026-08-06 | Currency BRL, no conversions | Spec §decisions | — |
| 2026-08-06 | Geolocation dedup → 1 row/zip | EDA §5 | dedup rule |
| 2026-08-06 | Untranslated PT categories keep their name; only truly null → `uncategorized` | EDA (found 2 PT-missing cats: `pc_gamer`, `portateis_…`) | don't lump real cats in uncategorized |
| 2026-08-06 | **EDA to `olist_eda.ipynb` + `eda_summary.json` as canonical statistical source** | EDA | reproducible deep-dive |
| 2026-08-06 | **Phase 2 cleaning executed via `04_Python/ETL/data_preparation.py`** | Cleaning | implements prompts 2.1–2.9; auditable pipeline |
| 2026-08-06 | **Master `order_revenue` = merchandise value (total_items_price), NOT payment_value** | Cleaning | AOV baseline R$ 137.04 is goods-only; freight (R$ 2.20M) tracked separately in `total_freight`; `total_payment_value` kept as "customer paid" |
| 2026-08-06 | **Delivered orders with missing/outlier delivery dates excluded from analysis** (8 missing + 14 outliers) | Cleaning | `delivery_days` must be valid for delivery KPIs; flagged rows archived in `06_AI/Outputs/Scratchpad/` |
| 2026-08-06 | **Reviews deduped to one per order (keep first)** | Cleaning | keeps master at one-row-per-delivered-order grain |
| 2026-08-06 | **Geolocation: one GPS per zip; 31 out-of-Brazil points removed** | Cleaning | 19,011 zips final; matches EDA §5 |
| 2026-08-06 | **BOTH revenue columns kept in master** — `order_revenue` (goods, ~R$ 13.2M) AND `order_revenue_incl_freight` (goods+freight, ~R$ 15.4M) | Visualization prep | dashboard headline uses `order_revenue` (matches EDA/AOV R$ 137); incl-freight available for freight-burden story |
| 2026-08-06 | **Star schema exported for Power BI** → `02_Cleaned_data/star_schema/` (`build_star_schema.py`) | Power BI prep | 7 tables: Dim_Date/Customer/Product/Seller/Geography + Fact_Orders (order grain) + Fact_OrderItems (line grain, enables category/seller). Both revenue definitions in Fact_Orders. Line `line_price` sums exactly to order revenue (R$ 13.2M) — no double count if one grain per visual. `data_model.md` documents keys/relationships/DAX |
| 2026-08-07 | **Zip codes must be TEXT, never integer** (CEP leading-zero significant `04106` ≠ `4106`) | Validation | fixed actual data loss this session (§8); DDL/import forces TEXT |
| 2026-08-07 | **`not_defined` payments (3) kept aggregated** (do not re-drop) | Validation | negligible impact; canvas §5 wording corrected from "drop 3" → "3 aggregated" |
| 2026-08-07 | **Unknown SQL analyzer:** load PostgreSQL only; Power BI star optional in `olist` schema | SQL prep | `03_SQL/00_create_schema.sql` normal schema; zips TEXT |
| 2026-08-07 | **Local Postgres conn resolved** — superuser `postgres` password = `postgres`, target DB = existing `Olist` | Build | .env.txt corrected (gitignored); no temp `trust` reset needed |
| 2026-08-07 | **Load scope = normalized core only** (9 tables) into DB `Olist`. Flat `olist.master` + Power-BI star **not** loaded | Build | diverges from earlier "normalized + star" scope; star DDL kept as optional `03_SQL/00b_create_star_schema.sql` |
| 2026-08-07 | **Product dims hold counts as NUMERIC, not INTEGER** (`product_name_lenght/_description_lenght/photos_qty`) | Build | cleaned CSV stores these as decimals (`40.0`); INTEGER rejected the COPY |
| 2026-08-07 | **`reviews` keyed by `order_id`, NOT `review_id`** | Build | per `clean_check.json` order_id is the unique key (98,673); review_id repeats across orders in the cleaned export. Column order matches the CSV (COPY maps by position, not name) |
| 2026-08-07 | **Star DDL split to `03_SQL/00b_create_star_schema.sql`** (optional, not run) | Build | keeps `00_create_schema.sql` = normalized default |
| 2026-08-16 | **Consolidated the three EDA/analysis notebooks into a single `04_Python/olist_full_analysis.ipynb`** (step-by-step, from-scratch, clean outputs) | Build | built via `04_Python/build_full_analysis_nb.py` + verified headless via `04_Python/verify_notebook.py`; old notebooks moved to `04_Python/archive/`; all outputs regenerated (eda_summary.json 20 keys, 8 viz PNGs, descriptive_analysis.html) |

---

## 8. SESSION LOG — what was done this session
| Date | Step | Result |
|---|---|---|
| 2026-08-06 | EDA baseline snapshot | seeded §4; discovered lagging/core problem = repeat rate 3.12% + late-delivery score gap |
| 2026-08-06 | DAMA-5 baseline | §5; geolocation dedup is the real cleaning fix |
| 2026-08-06 | **Full EDA executed** (`olist_eda.ipynb`) | Deep stats → §4; validated PECO H1 (gap 1.73, p<0.001); growth is volume/not-value; NE delivery↔satisfaction compounding |
| 2026-08-06 | PECO H1 | **VALIDATED ✅** — null rejected; late delivery significant negative effect |
| 2026-08-06 | **Phase 2 cleaning & preparation executed** | `data_preparation.py` → 11 files in `02_Cleaned_data/` + `olist_master.csv` (96,456 delivered orders × 40 cols). Master matches EDA baselines (score 4.16, 12.1d delivery, 8.1% late, AOV R$ 136.83, revenue R$ 13.20M). Audit + summary → `06_AI/Outputs/Generated_Docs/` |
| 2026-08-06 | **High-impact visualizations built** (`04_Python/visualization_insights.ipynb`) | 8 Matplotlib PNGs → `06_AI/Outputs/Generated_Charts/`: correlation heatmap `viz_01`, H1 dose-response `viz_02`, on-vs-late gap `viz_03`, volume-vs-AOV `viz_04`, repeat rate `viz_05`, state delivery↔score `viz_06`, freight burden `viz_07`, category/state concentration `viz_08`. Master-backed figures: repeat rate **3.0%** (2,801/93,336), H1 gap **1.72★** (4.29 vs 2.57), freight **16.6%**, late **8.1%**. |
| 2026-08-06 | **Star schema exported for Power BI** → `02_Cleaned_data/star_schema/` | 7 tables (5 dims + 2 facts) + `data_model.md`. Integrity: line `line_price` R$ 13.20M == Fact_Orders `order_revenue`, line freight == `total_freight`, 0 orphan item rows, 96,456 order-level rows. Ready for Power BI import in Phase 5 |
| 2026-08-07 | **Complete clean-check** (`04_Python/ETL/validate_clean_data.py`) | Independent verification → `clean_check.json` + `clean_check_report.md`: 110 PASS / 0 FAIL / 1 WARN (`not_defined`) / 2 INFO. Inputs: per-table quality, PK/composite keys, RI, sum reconciliation. |
| 2026-08-07 | **CRITICAL: zip leading-zero data loss fixed** | Review (reviewer subagent) flagged CEP zero-stripping. Root cause `data_preparation.py`: `load()` dtype key (`zip_code_prefix`) didn't match geolocation column (`geolocation_zip_code_prefix`) so zips coerced to int; customers read by default dtype. Fixed + regenerated all `02_Cleaned_data/` outputs. |
| 2026-08-07 | **PostgreSQL prep** (`03_SQL/`) | Created `00_create_schema.sql` (normal model + optional star), `01_load_data.sql` (`\copy`, UTF8), `02_analysis_queries.sql` (starter queries for business questions). |
| 2026-08-07 | **Load executed & verified → db `Olist`** | Created schema + loaded **9 normalized tables** via `psql \copy`. All counts == `clean_check.json`: customers 99,441 · geography 19,011 · order_items 112,647 · orders 96,456 · orders_items_aggregated 98,663 · payments 99,440 · products 32,951 · reviews 98,673 · sellers 3,095. Numbers reconcile to the cent (delivered): items R$ 13,197,189.09 ✓ freight R$ 2,197,044.12 ✓. **Zip leading-zero intact**: customers 23,995 leading-zero CEPs, zips 5-char TEXT ✓. |
| 2026-08-07 | **Model caveat documented** | `reviews` (98,673) and `orders_items_aggregated` (98,663) contain rows beyond the 96,456 delivered orders — join to `olist.orders` (or filter `order_status='delivered'`) for the delivered-universe analysis. DB `Olist` collation = `Spanish_Spain.1252` (accents fine). |
| 2026-08-16 | **Built + verified the consolidated notebook** (`04_Python/olist_full_analysis.ipynb`) | 12 sections, 51 cells, all range assertions **PASS**; H1 confirmed (late-vs-ontime gap **1.73**); repeat rate **3.0%**; SP **38%** of revenue |

---

## 9. SOURCE OF TRUTH & REGENERATION RULES
- **Any agent / OpenCode session must read this file first** before proceeding.
- **At the end of every session** (or after each phase step), touch each hot section: §3 (KPIs), §4 (EDA), §5 (DAMA-5), §6 (hypotheses), §7 (decisions), §8 (session log).
- If §4 numbers change after cleaning, **update** them (do not stack unfixed numbers).
- Statistical evidence lives in `04_Python/olist_eda.ipynb`; re-run it before major updates.
- Never erase a past decision from §7 — add a new row with the change.