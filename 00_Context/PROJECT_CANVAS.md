# 📊 OLIST BUSINESS ANALYTICS — PROJECT CANVAS
> **THE MASTER FILE.** This document is the single source of truth for business understanding, evidence, and hypotheses for the Olist project. It is *living*: every agent/analyst session **must** run an EDA snapshot and update the relevant section of this file at the end of work. Never let this file go stale.

---

- **Last updated:** 2026-08-06
- **Owned by:** Nikhil Harins (Business Analyst) + AI Consultant
- **Project slug:** `olist`
- **Status:** Phase 1 complete → **Phase 2 (Data Cleaning) starting** · Post-logo
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
| KPI | Current baseline (AUG 2026 seed) | Target / Note |
|---|---|---|
| Total revenue | R$ 13,221,498 (delivered) | Recovering trend, not fixed target |
| Average order value (AOV) | R$ 137.04 | Rises over time |
| Monthly order volume | ~6k–7.3k (peak Nov-2017=7,289) | Should be growing |
| Repeat customer rate | **3.12%** ❌ (flagged problem) | Olist baseline ~3% → goal lift |
| Average review score | 4.16 (delivered) | Healthy >4.1 |

### LEADING KPIs (inputs / early-warning — what drives the outcomes)
| KPI leading (works across one) | Note |
|---|---|
| Delivery time (days) → measured 12.1 mean / 10 median | Leading indicator of satisfaction & retention |
| On-time delivery rate (delivered ≤ expected) | Leading indicator of review score |
| Payment installment levels (mean 2.85) | Leading indicator of AOV & credit risk |
| Category mix concentration (top=health_beauty) | Leading of revenue growth |
| Seller concentration (median seller revenue R$ 846) | Leading indicator of supply robustness |

**Rule:** Never compute lagging without its matching leading indicators, or we cannot act.

---

## 4. FULL EDA RESULTS (baseline snapshot — 2026-08-06)

> Method: all delivered orders (`order_status=delivered`), joined to items/payments/reviews; customers via `customer_unique_id`. Update each EDA step in Phase 3.

### 4.1 Scale & money
- Total gross revenue (delivered): **R$ 13,221,498**
- Delivered orders: **96,478**
- Average order value: **R$ 137.04**
- Repeat customer rate: **3.12%** (only 96,096 unique customers → retention is the core problem)
- Payment installments mean: **2.85**

### 4.2 Growth narrative
- Peak months: Nov-2017 (7,289), Jan-2018 (7,069), Mar-2018 (7,003)
- Stable high end: Jun–Aug 2018 (~6.1k–6.4k orders/mo, ~R$ 838k–868k rev/mo)
- Earliest history thin (Sep 2016 = 1 order, Oct 2016 = 265) → start of keep → growth is real but data trail short at the very start.

### 4.3 Delivery / operations
- Mean delivery days: **12.1** · median **10**
- Worst states for delivery time: **RR 29.0d, AP 26.7d, AM 26.0d, AL 24.0d, PA 23.3d** (all North/Northeast)
- Best states (not shown) are SP/MG/RS

### 4.4 Payments
| type | orders | value |
|---|---|---|
| credit_card | 74,304 | R$ 12,101,095 |
| boleto | 19,191 | R$ 2,769,933 |
| voucher | 3,679 | R$ 343,014 |
| debit_card | 1,485 | R$ 208,421 |

### 4.5 Reviews & satisfaction
- Mean review score: **4.16** (delivered orders)
- Distribution: 1★=9,406 · 2★=2,941 · 3★=7,961 · 4★=18,987 · 5★=57,066
- **KEY BUSINESS INSIGHT: On-time orders score 4.29 vs LATE orders score 2.57** → a 1.7-point satisfaction gap directly linked to delivery lateness.

### 4.6 Top categories (revenue)
| category | orders | revenue |
|---|---|---|
| health_beauty | 8,836 | R$ 1,258,681 |
| watches_gifts | 5,624 | R$ 1,205,006 |
| bed_bath_table | 9,417 | R$ 1,036,988 |
| sports_leisure | 7,720 | R$ 988,049 |
| computers_accessories | 6,689 | R$ 911,954 |
| *(uncategorized, labelled, kept)* | — | R$ 185,050 |

### 4.7 Sellers
- Active sellers (delivered): **2,970**
- Seller median revenue: **R$ 846** → very long tail, few big sellers
- Top states by customer revenue: **SP (R$ 5.2M), RJ (R$ 1.8M), MG (R$ 1.6M)**

> ⚠️ Full gap-trend month-over-month, top-10 category runs, and inter-state review breakdown are **Phase 3 scope** — update §5 here with deeper EDA.

---

## 5. DAMA-5 — DATA QUALITY ASSESSMENT (per dataset, baseline 2026-08-06)

Dimensions assessed: **Completeness, Consistency, Accuracy, Timeliness, Uniqueness.** Score scale: ✅ pass · ☑ partial · ❌ fail (to clean).

| Dataset | Rows | Completeness | Consistency | Accuracy | Timeliness | Uniqueness | Notes / action |
|---|---|---|---|---|---|---|---|
| olist_customers | 99,441 | ✅ no nulls | ✅ | ✅ `customer_unique_id` **must** use (not customer_id) | ✅ | ✅ 0 dups | clean |
| olist_geolocation | 1,000,163 | ✅ no nulls | ✅ | ☐ ~19k real zips inside 1M rows | ✅ | ❌ **261,831 dups** | dedup 1 GPS/zips; drop carrier |
| olist_order_items | 112,650 | ✅ | ✅ | ✅ | ✅ | ✅ | clean |
| olist_order_payments | 103,886 | ✅ | ☐ 3 rows `not_defined` | ✅ | ✅ | ✅ | drop 3 not_defined |
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
> *"Customers whose order is delivered LATE are measurably less satisfied than customers delivered ON TIME — and this gap (4.16 vs 2.57) drives the low review scores and contributes to the failing repeat rate."*

**Evidence so far (from 2026-08-06 baseline):** on-time score 4.16 vs late 2.57 (−1.6pts). Stat (t-test / effect size) to be validated in **Phase 3**.

**Null hypothesis:** late delivery has no meaningful effect on review score.

**Follow-on (Phase 3/4):** Segment effect by category & state (RR/AP/AM show worst delivery → test if they also show worst score).

---

## 7. DECISIONS LOG (tracked — do not rewrite history)
| Date | Decision | By | Rationale |
|---|---|---|---|
| 2026-08-06 | Analyse **delivered orders only** for revenue/satisfaction | Spec §decisions | align with CLAUDE_OLIST.md |
| 2026-08-06 | Label 610 products `uncategorized`, **do not drop** | Spec §decisions | keep data |
| 2026-08-06 | Use `customer_unique_id` for all customer counts | Spec §decisions | `customer_id` inflates |
| 2026-08-06 | Currency BRL, no conversions | Spec §decisions | — |
| 2026-08-06 | Geolocation dedup → 1 row/zip | baseline | dedup rule |

---

## 8. SESSION LOG — what was done this session
| Date | Step | Result |
|---|---|---|
| 2026-08-06 | EDA baseline snapshot | seeded §5; discovered lagging/core problem = repeat rate 3.12% + late-delivery score gap |
| 2026-08-06 | DAMA-5 baseline | §7; geolocation dedup is the only real fixing job |
| 2026-08-06 | PECO H1 | §6; will validate in Phase 3 |

---

## 9. SOURCE OF TRUTH & REGENERATION RULES
- **Any agent / OpenCode session must read this file first** before proceeding.
- **At the end of every session** (or after each phase step), touch each hot section: §3 (KPIs), §5 (EDA), §6 (hypotheses), §7 (decisions), §8 (session log).
- If §5 numbers change after cleaning, **update** them (do not stack unfixed numbers).
- Never erase a past decision from §7 — add a new row with the change.