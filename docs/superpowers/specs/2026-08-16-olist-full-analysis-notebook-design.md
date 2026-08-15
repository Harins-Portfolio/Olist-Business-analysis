# Design: Consolidated Olist Analysis Notebook

- **Date:** 2026-08-16
- **Project:** Olist Business Analytics (TFM)
- **Status:** Approved by user (2026-08-16)

## 1. Problem

The project has three overlapping Python notebooks in `04_Python/` that analyze the same Olist data in inconsistent ways:

1. **`olist_eda.ipynb`** — Full EDA from the 9 **raw** CSVs (money/scale, growth, categories, payments, geography, delivery, satisfaction + H1 t-test, sellers, correlations, seasonality). Exports `eda_summary.json`.
2. **`visualization_insights.ipynb`** — 8 publication-quality decision charts from the **cleaned** `olist_master.csv`, saved to `06_AI/Outputs/Generated_Charts/`.
3. **`descriptive_analysis.ipynb`** — Profiles all **18 cleaned tables** via `descriptive_lib.py` (column report + DAMA-5 + charts), clean-check verification, cross-table sanity. Charts are unreadable: up to 8 tiny charts crammed in one row at ~2.8" tall with rotated 7pt labels and log-scale money histograms.

Problems: overlapping analysis, different data sources (raw vs cleaned), inconsistent chart style, unreadable charts in the descriptive notebook, and stale/divergent numbers.

## 2. Goal

Produce **one consolidated, step-by-step, runnable-from-top-to-bottom notebook** that replaces all three, is perfectly readable, and keeps every downstream output contract working.

## 3. Decisions (user-approved)

| Topic | Decision |
|---|---|
| Data foundation | **Both** — show raw briefly, then analyze on cleaned data (raw → clean pipeline) |
| Raw→clean step | **Verify, don't re-run** — display raw shapes, verify cleaned outputs match; do NOT execute ETL scripts |
| Chart style | **Matplotlib + Seaborn mix** — seaborn for statistical charts (heatmap, distplots), matplotlib for the rest, one consistent palette |
| Old notebooks | **Move to `04_Python/archive/`** |
| Outputs | **Regenerate all** — `eda_summary.json`, the 8 decision PNGs, and the HTML report |
| Profiling depth | **Condense table profiling** — readable tables + 2×2 grids for the 6 core tables only; detail lives in `descriptive_report.py`/HTML |

## 4. Deliverable

`04_Python/olist_full_analysis.ipynb`

Notebook convention: English; markdown cells for narrative, code cells for computation; **one chart per cell** for business analysis; 2×2 readable grids (~10×8") only in the condensed profiling section; figure facecolor white, font.size >= 10, no rotated 7pt labels.

## 5. Notebook structure (12 sections)

### 0. Setup & theme
- Imports: `pathlib`, `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy.stats`, `json`, `IPython.display`.
- Project-root detection (`Path.cwd()`), add `04_Python/` to `sys.path` for `descriptive_lib`.
- One shared theme: colors `GREEN #0f6b47`, `RED #b0413e`, `NAVY #1f3a93`, `GRAY #9aa3ad` (from existing notebooks); `sns.set_theme(style='whitegrid')`; readable `font.size >= 10`.
- Helper `savefig(name)` writing PNGs to `06_AI/Outputs/Generated_Charts/` at dpi 160.
- dtype-aware loaders (zips/ids as `str`, dates parsed).

### 1. Raw → clean pipeline (verify, don't re-run)
- Load the 9 raw CSVs; print shapes (compact table).
- Verify cleaned outputs: row counts, revenue reconciliation (~R$13.2M delivered), star-fact grain match. No ETL execution.

### 2. Data-quality overview
- `descriptive_lib.overview()` grid (18 tables, one row each) + DAMA-5 verdict.
- `descriptive_lib.verdict()` clean-check counts (PASS/WARN/INFO/FAIL) with non-pass details.

### 3. Per-table profiling (condensed)
- For each of the 18 tables: `column_report` DataFrame + `dama_df` DAMA-5 scores (compact, readable).
- Charts ONLY for the 6 core tables (`master`, `orders_clean`, `payments`, `items`, `products`, `reviews`) as **2×2 grids (~10×8")** choosing the most informative columns (money log-hist, review-score bar, payment-mix donut, top category bar, order trend, geo scatter).
- A note markdown cell: full per-table detail lives in `descriptive_report.py` → HTML.

### 4. Core money & scale KPIs
- From cleaned `olist_master.csv`: gross revenue (goods), delivered orders, AOV (R$137.04), freight total + share (16.6%), unique customers, repeat rate (3.12%). Table + one chart per KPI (where chart adds value).

### 5. Growth & seasonality
- Monthly orders/revenue/AOV chart (viz_04 style, dual-axis), momentum table (MoM), Black Friday (Nov-2017 spike) and Christmas callout, weekday vs weekend.

### 6. Categories & products
- Top-15 categories by revenue (join master → items → products), top-10 horizontal bar, category × satisfaction view.

### 7. Payments
- Payment-mix donut (credit/boleto/debit/voucher), installments distribution, credit-heavy note (63.1% of revenue in >1 instalment).

### 8. Geography
- State revenue concentration bar (top states), SP share (38.3%), delivery-vs-score bubble (viz_06 style), slowest / worst-on-time states.

### 9. Delivery & satisfaction (H1 — validated)
- Delivery-days distribution (hist + KDE, quantile annotations).
- On-time rate (91.9%), late orders count.
- Dose–response chart: score by delivery-time bucket (viz_02 style).
- On-time vs late score gap (viz_03 style, 1.73-star penalty).
- **t-test** (`scipy.stats.ttest_ind`, Welch) with effect size.
- Correlation heatmap (seaborn, viz_01 style) among revenue, freight, delivery_days, review_score.

### 10. Sellers, repeat, freight, concentration
- Seller long-tail: top 1% / top 20% share (25.5% / 82.3%).
- Repeat-purchase chart (viz_05 style).
- Freight burden (viz_07 style).
- Category & state revenue concentration (viz_08 style).

### 11. Verification & cross-table sanity
- Star-schema referential integrity checks (FK orphans = 0).
- Zip leading-zero integrity (from `descriptive_lib.verdict()`).
- Master ↔ Fact_Orders grain match.

### 12. Export + conclusions
- Write `eda_summary.json` (same keys as `olist_eda.ipynb` §13) to `06_AI/Outputs/Generated_Insights/`.
- Save the 8 decision PNGs with the **same filenames** as today (`viz_01_correlation_heatmap.png` … `viz_08_concentration.png`).
- Regenerate HTML report by importing/running `descriptive_report.py`.
- Closing narrative markdown ("Done") with next steps.

## 6. Output contracts (must keep working)

| Consumer | File | Contract |
|---|---|---|
| `00_Context/PROJECT_CANVAS.md` | `06_AI/Outputs/Generated_Insights/eda_summary.json` | Same 20 keys, same semantics |
| Reports / thesis | `06_AI/Outputs/Generated_Charts/viz_01…viz_08.png` | Same 8 filenames |
| Report consumers | `06_AI/Outputs/Generated_Reports/descriptive_analysis.html` | Regenerated by `descriptive_report.py` |

## 7. Non-goals

- No ML / predictive modeling (project scope excludes it).
- No re-running the ETL pipeline inside the notebook (destructive, slow).
- No new shared module beyond keeping `descriptive_lib.py`; plotting helpers stay inline in the notebook.
- Do not modify `02_Cleaned_data/` or `01_Raw_Data/`.

## 8. Verification & success criteria

1. Execute the notebook headless (nbconvert) from project root; runs clean top-to-bottom with no errors.
2. `eda_summary.json` values match canvas baselines: revenue ≈ R$13.22M, AOV ≈ 137, repeat rate ≈ 3.12%, avg delivery ≈ 12.1d, mean score ≈ 4.16, satisfaction gap ≈ 1.73.
3. All 8 `viz_*.png` files written to `Generated_Charts/`.
4. HTML report regenerated without error.
5. Old notebooks moved to `04_Python/archive/`; new notebook is the only top-level analysis notebook.

## 9. Migration

- After the new notebook is verified, move `olist_eda.ipynb`, `visualization_insights.ipynb`, `descriptive_analysis.ipynb` to `04_Python/archive/` (git mv).
- Update `PROJECT_CANVAS.md` evidence-source lines pointing at the old notebooks (decision logged in §7 decisions log).
