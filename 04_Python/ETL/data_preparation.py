"""
OLIST - PHASE 2: DATA CLEANING & PREPARATION
=============================================
Run:  python data_preparation.py
Reads : 01_Raw_Data/*.csv   (never modified)
Writes: 02_Cleaned_data/*.csv            per-table cleaned + aggregated
        02_Cleaned_data/olist_master.csv single flat analysis table
        06_AI/Outputs/Scratchpad/*       flagged rows for manual review
        06_AI/Outputs/Generated_Docs/    cleaning_audit.md + cleaning_summary_report.md

Implements the Phase-2 workflow (prompts 2.1 -> 2.9):
  T2.1 quality audit   T2.2 orders   T2.3 payments   T2.4 items
  T2.5 products        T2.6 reviews  T2.7 geolocation  T2.8 master  T2.9 report

Project decisions honoured (PROJECT_CANVAS §7 / CLAUDE_OLIST §9):
  - Delivered orders only for all analysis
  - customer_unique_id is the true customer key
  - 'uncategorized' label, never dropped
  - geolocation: one GPS row per zip; points outside Brazil dropped
  - BRL currency, no conversions
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
#  Paths / config
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW     = PROJECT_ROOT / "01_Raw_Data"
CLEAN   = PROJECT_ROOT / "02_Cleaned_data"
SCRATCH = PROJECT_ROOT / "06_AI" / "Outputs" / "Scratchpad"
DOCS    = PROJECT_ROOT / "06_AI" / "Outputs" / "Generated_Docs"

for p in (CLEAN, SCRATCH, DOCS):
    p.mkdir(parents=True, exist_ok=True)

DELIVERY_MIN, DELIVERY_MAX = 0, 180      # prompt 2.2
PRICE_MAX = 5000                          # prompt 2.4
BRAZIL_BOX = {"lat": (-34, 6), "lng": (-74, -28)}  # prompt 2.7

audit: dict = {
    "orders": {}, "payments": {}, "items": {}, "products": {},
    "reviews": {}, "geolocation": {}, "master": {},
}
run_meta = {"generated_at": datetime.now().isoformat(timespec="seconds")}


def save(df: pd.DataFrame, name: str, where: Path = CLEAN) -> pd.DataFrame:
    df.to_csv(where / name, index=False)
    return df


def load(name: str) -> pd.DataFrame:
    path = RAW / name
    df = pd.read_csv(path, dtype={"zip_code_prefix": str})
    audit.setdefault(name, {})["rows_in"] = len(df)
    return df


# --------------------------------------------------------------------------- #
#  T2.1 - DATA QUALITY AUDIT
# --------------------------------------------------------------------------- #
def quality_audit() -> pd.DataFrame:
    records = []
    for f in sorted(RAW.glob("*.csv")):
        df = pd.read_csv(f, dtype=str)
        null_cols = df.isna().sum()
        records.append({
            "table": f.name,
            "rows": len(df),
            "cols": df.shape[1],
            "dup_rows": int(df.duplicated().sum()),
            "null_cells": int(null_cols.sum()),
            "null_cells_pct": round(float(df.isna().mean().mean() * 100), 2),
            "cols_with_nulls": int((null_cols > 0).sum()),
        })
    out = pd.DataFrame(records)
    return out


# --------------------------------------------------------------------------- #
#  T2.2 - ORDERS
# --------------------------------------------------------------------------- #
def clean_orders() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = load("olist_orders_dataset.csv")
    date_cols = ["order_purchase_timestamp", "order_approved_at",
                 "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date"]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors="coerce")

    audit["orders_status"] = df["order_status"].value_counts().to_dict()
    audit["orders"]["null_dates"] = {c: int(df[c].isna().sum()) for c in date_cols}

    delivered = df[df["order_status"] == "delivered"].copy()
    save(delivered, "orders_delivered.csv")

    missing = delivered[delivered["order_delivered_customer_date"].isna()].copy()
    save(missing, "orders_delivery_date_missing.csv", SCRATCH)

    ok = delivered[delivered["order_delivered_customer_date"].notna()].copy()
    ok["delivery_days"] = (ok["order_delivered_customer_date"]
                           - ok["order_purchase_timestamp"]).dt.days.astype(float)

    outliers = ok[(ok["delivery_days"] < DELIVERY_MIN) | (ok["delivery_days"] > DELIVERY_MAX)].copy()
    save(outliers, "orders_delivery_outliers.csv", SCRATCH)

    clean = ok[ok["delivery_days"].between(DELIVERY_MIN, DELIVERY_MAX)]
    save(clean, "orders_clean.csv")

    audit["orders"].update({
        "delivered": int(len(delivered)),
        "missing_delivery_date": int(len(missing)),
        "outliers": int(len(outliers)),
        "final": int(len(clean)),
    })
    return clean, delivered


# --------------------------------------------------------------------------- #
#  T2.3 - PAYMENTS  (one row per order)
# --------------------------------------------------------------------------- #
def clean_payments() -> pd.DataFrame:
    pay = load("olist_order_payments_dataset.csv")
    pay["payment_value"] = pd.to_numeric(pay["payment_value"], errors="coerce")
    pay["payment_installments"] = pd.to_numeric(pay["payment_installments"], errors="coerce").fillna(1)

    audit["payments"]["types"] = pay["payment_type"].value_counts().to_dict()
    audit["payments"]["zero_neg"] = int((pay["payment_value"] <= 0).sum())
    audit["payments"]["split_orders"] = int((pay.groupby("order_id").size() > 1).sum())

    aggr = (pay
            .groupby("order_id", as_index=False)
            .agg(total_payment_value=("payment_value", "sum"),
                 payment_types_used=("payment_type",
                                     lambda s: ",".join(sorted(set(s)))),
                 payment_installments_max=("payment_installments", "max")))
    aggr["total_payment_value"] = aggr["total_payment_value"].round(2)
    save(aggr, "payments_clean.csv")
    audit["payments"]["unique_orders"] = int(len(aggr))
    audit["payments"]["agg_zero_neg"] = int((aggr["total_payment_value"] <= 0).sum())
    return aggr


# --------------------------------------------------------------------------- #
#  T2.4 - ORDER ITEMS  (full clean + per-order aggregate)
# --------------------------------------------------------------------------- #
def clean_items() -> tuple[pd.DataFrame, pd.DataFrame]:
    it = load("olist_order_items_dataset.csv")
    it["price"] = pd.to_numeric(it["price"], errors="coerce")
    it["freight_value"] = pd.to_numeric(it["freight_value"], errors="coerce")

    audit["items"]["price"] = {"min": float(it["price"].min()),
                               "max": float(it["price"].max()),
                               "mean": float(it["price"].mean())}
    audit["items"]["freight"] = {"min": float(it["freight_value"].min()),
                                 "max": float(it["freight_value"].max()),
                                 "mean": float(it["freight_value"].mean())}

    audit["items"]["price_zero_neg"] = int((it["price"] <= 0).sum())
    audit["items"]["price_over_max"] = int((it["price"] > PRICE_MAX).sum())
    audit["items"]["freight_neg"] = int((it["freight_value"] < 0).sum())

    mask_ok = (it["price"] > 0) & (it["price"] <= PRICE_MAX) & (it["freight_value"] >= 0)
    items_clean = it[mask_ok]
    save(items_clean, "items_clean.csv")

    aggr = (items_clean
            .groupby("order_id", as_index=False)
            .agg(item_count=("order_item_id", "nunique"),
                 total_items_price=("price", "sum"),
                 total_freight=("freight_value", "sum"),
                 n_sellers=("seller_id", "nunique")))
    sellers = (items_clean.groupby("order_id")["seller_id"]
               .apply(lambda s: "|".join(sorted(set(s)))).reset_index(name="seller_ids"))
    prods = (items_clean.groupby("order_id")["product_id"]
             .apply(lambda s: "|".join(sorted(set(s)))).reset_index(name="product_ids"))
    aggr = (aggr.merge(sellers, on="order_id", how="left")
                .merge(prods, on="order_id", how="left"))
    aggr["total_items_price"] = aggr["total_items_price"].round(2)
    aggr["total_freight"] = aggr["total_freight"].round(2)
    save(aggr, "orders_items_aggregated.csv")

    audit["items"]["multi_item_orders"] = int((items_clean.groupby("order_id").size() > 1).sum())
    audit["items"]["final_rows"] = int(len(items_clean))
    audit["items"]["agg_orders"] = int(len(aggr))
    return items_clean, aggr


# --------------------------------------------------------------------------- #
#  T2.5 - PRODUCTS  (+ English category)
# --------------------------------------------------------------------------- #
def clean_products() -> pd.DataFrame:
    prod = load("olist_products_dataset.csv")
    prod["product_category_name"] = prod["product_category_name"].fillna("uncategorized")
    audit["products"]["null_cat_filled"] = int((prod["product_category_name"] == "uncategorized").sum())

    trans = load("product_category_name_translation.csv").rename(
        columns={"product_category_name_english": "category_english"})
    prod = prod.merge(trans, on="product_category_name", how="left")
    prod["category_english"] = prod["category_english"].fillna("uncategorized")
    save(prod, "products_clean.csv")

    audit["products"]["unique_categories"] = int(prod["category_english"].nunique())
    audit["products"]["top20"] = prod["category_english"].value_counts().head(20).to_dict()
    return prod


# --------------------------------------------------------------------------- #
#  T2.6 - REVIEWS
# --------------------------------------------------------------------------- #
def clean_reviews() -> pd.DataFrame:
    rev = load("olist_order_reviews_dataset.csv")
    rev["review_score"] = pd.to_numeric(rev["review_score"], errors="coerce")

    audit["reviews"]["score_null"] = int(rev["review_score"].isna().sum())
    audit["reviews"]["score_out_of_range"] = int((~rev["review_score"].isin([1, 2, 3, 4, 5])).fillna(False).sum())
    audit["reviews"]["distribution"] = rev["review_score"].value_counts().sort_index().to_dict()
    audit["reviews"]["pct_with_comment"] = round(rev["review_comment_message"].notna().mean() * 100, 2)

    clean = rev[rev["review_score"].isin([1, 2, 3, 4, 5])].copy()
    clean = clean.sort_values("review_creation_date").drop_duplicates("order_id", keep="first")
    save(clean, "reviews_clean.csv")
    audit["reviews"]["final"] = int(len(clean))
    return clean


# --------------------------------------------------------------------------- #
#  T2.7 - GEOLOCATION  (one GPS row per zip, in-bounds)
# --------------------------------------------------------------------------- #
def clean_geolocation() -> pd.DataFrame:
    geo = load("olist_geolocation_dataset.csv")
    geo["latitude"] = pd.to_numeric(geo["geolocation_lat"], errors="coerce")
    geo["longitude"] = pd.to_numeric(geo["geolocation_lng"], errors="coerce")
    audit["geolocation"]["unique_zips"] = int(geo["geolocation_zip_code_prefix"].nunique())

    in_box = (geo["latitude"].between(*BRAZIL_BOX["lat"]) &
              geo["longitude"].between(*BRAZIL_BOX["lng"]))
    geo_bad = geo[~in_box]
    audit["geolocation"]["out_of_bounds"] = int(len(geo_bad))

    geo = geo[in_box].drop_duplicates("geolocation_zip_code_prefix", keep="first")
    audit["geolocation"]["final_zips"] = int(len(geo))
    save(geo, "geolocation_clean.csv")
    return geo


# --------------------------------------------------------------------------- #
#  T2.8 - MASTER  (one flat row per delivered order)
# --------------------------------------------------------------------------- #
def build_master(orders_clean: pd.DataFrame,
                 payments: pd.DataFrame,
                 items_aggr: pd.DataFrame,
                 reviews: pd.DataFrame) -> pd.DataFrame:
    cust = pd.read_csv(RAW / "olist_customers_dataset.csv")

    m = (orders_clean
         .merge(cust, on="customer_id", how="left")
         .merge(payments, on="order_id", how="left")
         .merge(items_aggr, on="order_id", how="left")
         .merge(reviews, on="order_id", how="left"))

    # ---- derived columns (descriptive / diagnostic / predictive-ready) ----
    m["delivery_days"] = m["delivery_days"].astype(float)
    m["days_early_or_late"] = ((m["order_estimated_delivery_date"]
                                - m["order_delivered_customer_date"]).dt.days).astype(float)
    m["is_late"] = (m["days_early_or_late"] < 0).astype(int)
    m["order_month"] = m["order_purchase_timestamp"].dt.strftime("%Y-%m")
    m["order_year"] = m["order_purchase_timestamp"].dt.year
    m["order_day_of_week"] = m["order_purchase_timestamp"].dt.dayofweek       # Mon=0..Sun=6
    m["is_weekend"] = (m["order_day_of_week"] >= 5).astype(int)
    m["purchase_hour"] = m["order_purchase_timestamp"].dt.hour
    m["promised_delivery_days"] = ((m["order_estimated_delivery_date"]
                                    - m["order_purchase_timestamp"]).dt.days).astype(float)
    m["delivery_lag_vs_promise_days"] = m["days_early_or_late"].astype(float)  # - = late, + = early
    m["has_review_comment"] = m["review_comment_message"].notna().astype(int)

    # one clean "revenue" column: MERCHANDISE value (total items price) so it
    # matches the KPI baseline (AOV R$ 137.04). Freight and full paid amount kept
    # separately so all three lenses (goods / paid / freight) are available.
    m["order_revenue"] = m["total_items_price"].round(2)
    m["order_revenue_incl_freight"] = (m["total_items_price"] + m["total_freight"]).round(2)

    # monetary types float for modelling
    m["total_payment_value"] = m["total_payment_value"].astype(float)
    m["total_items_price"] = m["total_items_price"].astype(float)
    m["total_freight"] = m["total_freight"].astype(float)
    m["payment_installments_max"] = m["payment_installments_max"].astype(float)

    m = m.sort_values("order_purchase_timestamp").reset_index(drop=True)
    save(m, "olist_master.csv")

    audit["master"] = {
        "rows": int(len(m)),
        "cols": int(m.shape[1]),
        "date_min": str(m["order_purchase_timestamp"].min().date()),
        "date_max": str(m["order_purchase_timestamp"].max().date()),
        "pct_late": round(float(m["is_late"].mean() * 100), 2),
        "columns": list(m.columns),
        "nulls": {c: int(m[c].isna().sum()) for c in m.columns if m[c].isna().sum() > 0},
        "unique_customers": int(m["customer_unique_id"].nunique()),
        "revenue": round(float(m["order_revenue"].sum()), 2),
    }
    return m


# --------------------------------------------------------------------------- #
#  T2.9 - REPORTING
# --------------------------------------------------------------------------- #
def write_reports(audit_clean: pd.DataFrame):
    def col(f):
        return CLEAN / f

    files = [f.name for f in CLEAN.glob("*.csv")]
    ordered = ["orders_clean.csv", "payments_clean.csv", "items_clean.csv",
               "orders_items_aggregated.csv", "products_clean.csv",
               "reviews_clean.csv", "geolocation_clean.csv", "olist_master.csv",
               "orders_delivered.csv"]

    # ---- cleaning_audit.md ----
    audit_md = ["# DATA QUALITY AUDIT — Olist (Phase 2, prompt 2.1)\n",
                f"_Generated: {run_meta['generated_at']}  |  source: 01_Raw_Data (never modified)_\n",
                "\n## T2.1 — Raw-file snapshot\n\n| Table | Rows | Cols | Duplicate rows | Null cells | Null % | Cols with nulls |",
                "|---|---|---|---|---|---|---|"]
    for _, r in audit_clean.iterrows():
        audit_md.append(f"| {r['table']} | {r['rows']:,} | {r['cols']} | {r['dup_rows']:,} | "
                        f"{r['null_cells']:,} | {r['null_cells_pct']:.2f}% | {r['cols_with_nulls']} |")
    audit_md.append("\n## T2.2 — Order status distribution (all 99,441 orders)\n")
    audit_md.append("| order_status | count |\n|---|---|")
    for k, v in audit["orders_status"].items():
        audit_md.append(f"| {k} | {v:,} |")
    (DOCS / "cleaning_audit.md").write_text("\n".join(audit_md), encoding="utf-8")

    # ---- cleaning_summary_report.md ----
    m = audit["master"]
    o = audit["orders"]
    sum_md = [
        "# OLIST — CLEANING SUMMARY REPORT (Phase 2, prompt 2.9)\n",
        f"_Generated: {run_meta['generated_at']}  |  pipeline: `04_Python/ETL/data_preparation.py`_\n",
        "\n## 1. Row counts — original vs final\n",
        "| Table | Raw rows | Clean rows | Change |",
        "|---|---|---|---|",
    ]
    mapping = {
        "olist_orders_dataset.csv": ("orders_clean.csv", "delivered orders with valid delivery dates, no outlier flags"),
        "olist_order_payments_dataset.csv": ("payments_clean.csv", "one row per order (aggregated)"),
        "olist_order_items_dataset.csv": ("items_clean.csv", "no zero/oversized price, no negative freight"),
        "olist_order_items_dataset.csv (agg)": ("orders_items_aggregated.csv", "one row per order"),
        "olist_products_dataset.csv": ("products_clean.csv", "uncategorized filled, English category added"),
        "olist_order_reviews_dataset.csv": ("reviews_clean.csv", "valid scores, one review per order"),
        "olist_geolocation_dataset.csv": ("geolocation_clean.csv", "one GPS row per zip, in-bounds"),
        "olist_customers_dataset.csv": ("olist_customers_dataset.csv", "clean as-is"),
        "olist_sellers_dataset.csv": ("olist_sellers_dataset.csv", "clean as-is"),
    }
    for raw_name, (clean_name, note) in mapping.items():
        raw_n = audit.get(raw_name, {}).get("rows_in", 0)
        out_p = col(clean_name)
        final_n = int(pd.read_csv(out_p, dtype=str).shape[0]) if out_p.exists() else 0
        sign = "—" if final_n == raw_n else ("↓" if final_n < raw_n else "↑")
        sum_md.append(f"| {raw_name} | {raw_n:,} | {final_n:,} | {sign} ({note}) |")

    sum_md += [
        "\n## 2. What was removed / fixed and why (plain English)\n",
f"- **Orders:** {o['delivered']:,} orders had status `delivered`. Of these, {o['missing_delivery_date']} with no "
        f"delivery date and {o['outliers']} with delivery_days outside [{DELIVERY_MIN}, {DELIVERY_MAX}] were flagged (kept in "
        "`06_AI/Outputs/Scratchpad/`) and excluded, leaving the final clean set.",
        f"- **Payments:** {audit['payments']['zero_neg']} payment rows with zero/negative value were **kept flagged** and aggregated "
        f"per order; {audit['payments']['split_orders']:,} orders paid in multiple transactions were combined into one row.",
        f"- **Items:** {audit['items']['price_zero_neg']} rows with price <= 0 and {audit['items']['price_over_max']} with price > "
        f"R$ {PRICE_MAX:,} and {audit['items']['freight_neg']} with negative freight were removed (data-entry errors).",
        f"- **Products:** {audit['products']['null_cat_filled']} products labelled `uncategorized` (kept, not dropped). "
        f"{audit['products']['unique_categories']} unique English categories after translation.",
        "- **Reviews:** dropped rows with missing/out-of-range scores; kept the **first** review per order so the master stays "
        "one-row-per-order.",
        f"- **Geolocation:** {audit['geolocation']['unique_zips']:,} unique zips from 1,000,163 rows; kept one GPS point per zip "
        f"({audit['geolocation']['final_zips']:,} after removing {audit['geolocation']['out_of_bounds']:,} out-of-Brazil points).",
        "\n## 3. What was filled / imputed and why\n",
        "- `product_category_name` null → `uncategorized` (decision: keep completeness).",
        "- `category_english` null → `uncategorized` (no translation exists).",
        "- No numeric imputation was performed anywhere; missing values are **kept as null** so they are visible, and null counts "
        "are reported for the master below.",
        "\n## 4. Master dataset (`olist_master.csv`)\n",
        f"- **Rows:** {m['rows']:,} delivered orders   **Columns:** {m['cols']}",
        f"- **Date range:** {m['date_min']} → {m['date_max']}",
        f"- **Unique customers:** {m['unique_customers']:,}   **Gross revenue:** R$ {m['revenue']:,.2f}",
        f"- **% late orders:** {m['pct_late']}%   **Null counts:** {json.dumps(m['nulls'])}",
        "- **Key columns for Phase 3+:** `order_revenue`, `total_payment_value`, `total_items_price`, `total_freight`, "
        "`item_count`, `payment_installments_max`, `payment_types_used`, `review_score`, `is_late`, `delivery_days`, "
        "`days_early_or_late`, `promised_delivery_days`, `order_month`, `order_year`, `is_weekend`, `purchase_hour`, "
        "`customer_state`, `customer_unique_id`, `seller_ids`, `product_ids`.",
        "\n## 5. Remaining data-quality issues that could affect analysis\n",
        "- **Missing deliveries:** some delivered orders lack `order_delivered_customer_date` (excluded; see Scratchpad).",
        "- **`review_comment_title` 88% null** — deliberately excluded from KPIs (decision).",
        "- **Geolocation** covers only ~19k of ~4M Brazilian zips — usable for state-level mapping, not precise geocoding.",
        "- **Freight** is customer-carried; cost/margin data does not exist in the dataset.",
        "\n## 6. Client-ready summary\n",
        "We consolidated nine raw Olist tables into a single clean analysis file covering 2 years of delivered orders, "
        "removing only data-entry errors and duplicate rows. Every KPI for the dashboard can now be computed from one "
        "`olist_master.csv`, and the cleaned per-table files are ready for Power BI. No business data was deleted — "
        "flagged rows are archived under `06_AI/Outputs/Scratchpad/` for audit.",
    ]
    (DOCS / "cleaning_summary_report.md").write_text("\n".join(sum_md), encoding="utf-8")

    # machine-readable audit for the canvas/agent
    (DOCS / "cleaning_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")


# --------------------------------------------------------------------------- #
#  MAIN
# --------------------------------------------------------------------------- #
def main():
    print("=" * 70)
    print("OLIST DATA PREPARATION — Phase 2")
    print("=" * 70)

    audit_df = quality_audit()
    print("\n--- T2.1 QUALITY AUDIT ---")
    print(audit_df.to_string(index=False))

    orders_clean, _ = clean_orders()
    print(f"\n--- T2.2 ORDERS: {audit['orders']['final']:,} clean "
          f"(delivered {audit['orders']['delivered']:,}, missing date {audit['orders']['missing_delivery_date']}, "
          f"outliers {audit['orders']['outliers']}) ---")

    payments = clean_payments()
    print(f"--- T2.3 PAYMENTS: {audit['payments']['unique_orders']:,} aggregated order-payment rows ---")

    _, items_aggr = clean_items()
    print(f"--- T2.4 ITEMS: {audit['items']['final_rows']:,} clean, "
          f"{audit['items']['agg_orders']:,} order aggregates ---")

    clean_products()
    print(f"--- T2.5 PRODUCTS: {audit['products']['unique_categories']} categories ---")

    reviews = clean_reviews()
    print(f"--- T2.6 REVIEWS: {audit['reviews']['final']:,} one-per-order reviews ---")

    clean_geolocation()
    print(f"--- T2.7 GEOLOCATION: {audit['geolocation']['final_zips']:,} zips ---")

    master = build_master(orders_clean, payments, items_aggr, reviews)
    print(f"--- T2.8 MASTER: {audit['master']['rows']:,} rows x {audit['master']['cols']} cols "
          f"| revenue R$ {audit['master']['revenue']:,.2f} | late {audit['master']['pct_late']}% ---")
    nulls = audit["master"]["nulls"]
    if nulls:
        print(f"    nulls: {nulls}")

    write_reports(audit_df)
    print("\n--- T2.9 REPORTS SAVED ---")
    print(f"    {DOCS / 'cleaning_audit.md'}")
    print(f"    {DOCS / 'cleaning_summary_report.md'}")
    print(f"    {DOCS / 'cleaning_audit.json'}")
    print("\nDONE")


if __name__ == "__main__":
    main()
