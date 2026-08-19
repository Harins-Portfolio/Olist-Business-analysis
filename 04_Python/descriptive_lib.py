"""
OLIST - DESCRIPTIVE ANALYSIS LIBRARY (shared by notebook + HTML report)
=======================================================================
Read-only profiling of every clean dataset (11 flat + 7 star-schema tables).

- Produces, per table: column profile (dtype, nulls, uniques, samples),
  numeric describe + histogram, categorical top-N, date range, DAMA-5 scoring.
- Runs the existing clean-check (validate_clean_data.py) and surfaces a
  PASS / WARN / FAIL verdict per table so you can verify the cleaning yourself.
- Never modifies 02_Cleaned_data/.

Usage:
    import descriptive_lib as dl
    dl.TABLES                      # registry of all 18 tables
    prof = dl.profile_table(rel)   # full profile dict for one table
    dama = dl.dama5(prof)          # DAMA-5 scores for that table
    dl.verdict()                   # runs clean-check, returns grouped results
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN = PROJECT_ROOT / "02_Cleaned_data"
STAR = CLEAN / "star_schema"
REPORTS = PROJECT_ROOT / "06_AI" / "Outputs" / "Generated_Reports"

# Reuse the authoritative manifests from the validator so numbers always match.
sys.path.insert(0, str(PROJECT_ROOT / "04_Python" / "ETL"))
import validate_clean_data as vcd  # noqa: E402

# --------------------------------------------------------------------------- #
#  TABLE REGISTRY - every clean data product, in a sensible reading order
# --------------------------------------------------------------------------- #
# (key, relative path, human label, group)
TABLES: list[dict] = [
    {"key": "master",        "rel": "olist_master.csv",                "label": "Master (denormalized)", "group": "Flat files"},
    {"key": "orders_clean",  "rel": "orders_clean.csv",                "label": "Orders clean",          "group": "Flat files"},
    {"key": "orders_deliv",  "rel": "orders_delivered.csv",            "label": "Orders delivered",      "group": "Flat files"},
    {"key": "payments",      "rel": "payments_clean.csv",              "label": "Payments clean",        "group": "Flat files"},
    {"key": "items",         "rel": "items_clean.csv",                 "label": "Items clean (line)",    "group": "Flat files"},
    {"key": "items_agg",     "rel": "orders_items_aggregated.csv",     "label": "Orders items aggregated", "group": "Flat files"},
    {"key": "products",      "rel": "products_clean.csv",              "label": "Products clean",        "group": "Flat files"},
    {"key": "reviews",       "rel": "reviews_clean.csv",               "label": "Reviews clean",         "group": "Flat files"},
    {"key": "geolocation",   "rel": "geolocation_clean.csv",           "label": "Geolocation clean",     "group": "Flat files"},
    {"key": "customers",     "rel": "olist_customers_dataset.csv",     "label": "Customers (as-is)",     "group": "Flat files"},
    {"key": "sellers",       "rel": "olist_sellers_dataset.csv",       "label": "Sellers (as-is)",       "group": "Flat files"},
    {"key": "fact_orders",   "rel": "star_schema/Fact_Orders.csv",     "label": "Star: Fact_Orders",     "group": "Star schema"},
    {"key": "fact_items",    "rel": "star_schema/Fact_OrderItems.csv", "label": "Star: Fact_OrderItems", "group": "Star schema"},
    {"key": "dim_customer",  "rel": "star_schema/Dim_Customer.csv",    "label": "Star: Dim_Customer",    "group": "Star schema"},
    {"key": "dim_product",   "rel": "star_schema/Dim_Product.csv",     "label": "Star: Dim_Product",     "group": "Star schema"},
    {"key": "dim_seller",    "rel": "star_schema/Dim_Seller.csv",      "label": "Star: Dim_Seller",      "group": "Star schema"},
    {"key": "dim_geo",       "rel": "star_schema/Dim_Geography.csv",   "label": "Star: Dim_Geography",   "group": "Star schema"},
    {"key": "dim_date",      "rel": "star_schema/Dim_Date.csv",        "label": "Star: Dim_Date",        "group": "Star schema"},
]

_TABLES_BY_REL = {t["rel"]: t for t in TABLES}

# Columns that must be read as strings (leading-zero-safe ids / zips).
STR_COLS = {
    "olist_master.csv": ["order_id", "customer_id", "customer_unique_id",
                         "customer_zip_code_prefix", "customer_city", "customer_state",
                         "payment_types_used", "seller_ids", "product_ids", "review_id"],
    "orders_clean.csv": ["order_id", "customer_id", "order_status"],
    "orders_delivered.csv": ["order_id", "customer_id", "order_status"],
    "payments_clean.csv": ["order_id", "payment_types_used"],
    "items_clean.csv": ["order_id", "order_item_id", "product_id", "seller_id"],
    "orders_items_aggregated.csv": ["order_id", "seller_ids", "product_ids"],
    "products_clean.csv": ["product_id", "product_category_name", "category_english"],
    "reviews_clean.csv": ["review_id", "order_id", "review_comment_title",
                          "review_comment_message"],
    "geolocation_clean.csv": ["geolocation_zip_code_prefix", "geolocation_city",
                              "geolocation_state"],
    "olist_customers_dataset.csv": ["customer_id", "customer_unique_id",
                                    "customer_zip_code_prefix", "customer_city",
                                    "customer_state"],
    "olist_sellers_dataset.csv": ["seller_id", "seller_zip_code_prefix",
                                  "seller_city", "seller_state"],
    "star_schema/Fact_Orders.csv": ["order_id", "customer_id", "payment_types_used"],
    "star_schema/Fact_OrderItems.csv": ["order_item_id", "order_id", "product_id",
                                        "seller_id"],
    "star_schema/Dim_Customer.csv": ["customer_id", "customer_unique_id",
                                     "customer_zip_code_prefix", "customer_city",
                                     "customer_state"],
    "star_schema/Dim_Product.csv": ["product_id", "product_category_name",
                                    "category_english"],
    "star_schema/Dim_Seller.csv": ["seller_id", "seller_zip_code_prefix",
                                   "seller_city", "seller_state"],
    "star_schema/Dim_Geography.csv": ["zip_code_prefix", "city", "state"],
    "star_schema/Dim_Date.csv": ["date", "month_name", "weekday"],
}

# Date/time columns to parse.
DATE_COLS = {
    "olist_master.csv": ["order_purchase_timestamp", "order_approved_at",
                         "order_delivered_carrier_date", "order_delivered_customer_date",
                         "order_estimated_delivery_date", "review_creation_date",
                         "review_answer_timestamp"],
    "orders_clean.csv": ["order_purchase_timestamp", "order_approved_at",
                         "order_delivered_carrier_date", "order_delivered_customer_date",
                         "order_estimated_delivery_date"],
    "orders_delivered.csv": ["order_purchase_timestamp", "order_approved_at",
                             "order_delivered_carrier_date",
                             "order_delivered_customer_date",
                             "order_estimated_delivery_date"],
    "items_clean.csv": ["shipping_limit_date"],
    "reviews_clean.csv": ["review_creation_date", "review_answer_timestamp"],
    "star_schema/Fact_Orders.csv": ["order_date"],
    "star_schema/Fact_OrderItems.csv": ["order_date"],
    "star_schema/Dim_Date.csv": ["date"],
}

# Integer-semantic columns that the CSVs round-trip as float when they contain
# nulls (pandas writes nullable Int64 NA as an empty cell). Cast back on read so
# they display and profile as integers while keeping nulls.
INT_COLS = {
    "olist_master.csv": ["payment_installments_max", "item_count", "n_sellers",
                         "review_score", "delivery_days", "promised_delivery_days",
                         "days_early_or_late", "delivery_lag_vs_promise_days"],
    "orders_clean.csv": ["delivery_days"],
    "products_clean.csv": ["product_photos_qty", "product_name_lenght",
                           "product_description_lenght"],
    "star_schema/Fact_Orders.csv": ["payment_installments_max", "item_count",
                                    "review_score", "delivery_days",
                                    "promised_delivery_days", "days_early_or_late"],
    "star_schema/Dim_Product.csv": ["product_photos_qty"],
}

MONEY_COLS = set(vcd.MONEY_COLS)
BOOL_COLS = {"is_late", "is_weekend", "has_review_comment", "is_ontime",
             "is_workday"}

# --------------------------------------------------------------------------- #
#  SEMANTIC CHART TYPING - overrides the dtype-based kind with the chart that
#  best tells the story for each column (used by the notebook AND the report).
# --------------------------------------------------------------------------- #
# Binary 0/1 flags -> donut (share of "yes").
BINARY_COLS = BOOL_COLS
# Ordinal / small-count discrete -> ordered bar chart (natural order).
ORDINAL_COLS = {
    "review_score", "order_year", "order_day_of_week", "purchase_hour",
    "year", "quarter", "month", "day_of_month", "day_of_week",
    "payment_installments_max", "item_count", "n_sellers",
    "product_photos_qty", "order_item_id", "order_month",
}
# Nominal categories -> horizontal top-10 bar, even when high cardinality
# (e.g. product categories have 74 unique values, still worth showing).
NOMINAL_COLS = {
    "order_status", "customer_state", "seller_state", "geolocation_state",
    "state", "payment_types_used", "category_english", "product_category_name",
    "month_name", "weekday", "customer_city", "seller_city", "geolocation_city",
    "city",
}
# Surrogate keys with no analytical meaning -> never plotted.
SKIP_COLS = {"date_key"}
# Coordinate columns -> plotted as ONE scatter (longitude vs latitude).
COORD_COLS = {"latitude", "longitude", "geolocation_lat", "geolocation_lng"}
# Same underlying timestamp rendered several ways -> chart only one of them.
DATE_FAMILY = {"order_purchase_timestamp", "order_date", "date",
               "order_month", "order_year", "order_day_of_week"}
# Monetary columns -> amount-band bar chart + median/mean caption (they are
# heavily right-skewed, so a plain linear histogram collapses 95%+ into one
# giant bar; fixed bands read like price bands instead of a log scale).
MONEY_COLS = set(vcd.MONEY_COLS)


def money_bins(s, nb=30):
    """Geometric bin edges (leading zero bucket) + stats for money histograms.

    A linear histogram of e.g. order revenue puts ~96% of rows in the first
    bar (0..449), which reads as '80k orders at price 0'.  Log-spaced bins show
    the real shape.  Returns (edges, stats) with stats None if nothing to plot.
    """
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return None, None
    pos = s[s > 0]
    if pos.empty:
        return np.linspace(0, max(s.max(), 1), nb + 1), None
    lo = max(float(pos.min()), 1e-6)
    hi = max(float(s.max()), lo * 2)
    edges = np.concatenate([[0.0], np.geomspace(lo, hi, nb)])
    stats = {"median": float(s.median()), "mean": float(s.mean()),
             "min": float(s.min()), "max": float(s.max()),
             "zeros": int((s == 0).sum())}
    return edges, stats


# Fixed, business-friendly amount bands. (lo <= x < hi) and labels read like
# price bands, so the chart needs no log-scale notation.
MONEY_BANDS = [
    (0.0, 1.0, "R$ 0"),
    (1.0, 50.0, "R$ 1–50"),
    (50.0, 100.0, "R$ 50–100"),
    (100.0, 200.0, "R$ 100–200"),
    (200.0, 500.0, "R$ 200–500"),
    (500.0, 1000.0, "R$ 500–1k"),
    (1000.0, float("inf"), "R$ 1k+"),
]


def money_bands(s):
    """Bucket amounts into human-readable R$ bands + stats for money charts.

    Returns (labels, counts, stats); stats is None if there is nothing to plot.
    Every non-null value falls in exactly one band, so sum(counts) == len(s).
    """
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return [], [], None
    labels, counts = [], []
    for lo, hi, lab in MONEY_BANDS:
        labels.append(lab)
        counts.append(int(((s >= lo) & (s < hi)).sum()))
    stats = {"median": float(s.median()), "mean": float(s.mean()),
             "min": float(s.min()), "max": float(s.max()),
             "zeros": int((s == 0).sum())}
    return labels, counts, stats

# Human-readable chart titles (units included where it helps).
LABELS = {
    "is_late": "Late delivery", "is_ontime": "On-time delivery",
    "is_weekend": "Weekend order", "is_workday": "Workday",
    "has_review_comment": "Has review comment",
    "review_score": "Review score (1-5)", "order_year": "Order year",
    "year": "Year", "month": "Month", "quarter": "Quarter",
    "day_of_week": "Day of week (Mon=0)", "order_day_of_week": "Day of week (Mon=0)",
    "day_of_month": "Day of month", "purchase_hour": "Purchase hour (0-23)",
    "payment_installments_max": "Max installments", "item_count": "Items per order",
    "n_sellers": "Sellers per order", "product_photos_qty": "Product photos",
    "product_name_lenght": "Name length (chars)",
    "product_description_lenght": "Description length (chars)",
    "order_item_id": "Item position in order",
    "payment_types_used": "Payment types", "customer_state": "Customer state",
    "seller_state": "Seller state", "geolocation_state": "State", "state": "State",
    "category_english": "Product category",
    "product_category_name": "Product category (PT)", "month_name": "Month name",
    "weekday": "Weekday",
    "delivery_days": "Delivery days", "promised_delivery_days": "Promised delivery days",
    "days_early_or_late": "Days early (+) / late (-)",
    "delivery_lag_vs_promise_days": "Delivery lag vs promise",
    "order_revenue": "Revenue (goods)", "order_revenue_incl_freight": "Revenue + freight",
    "order_revenue_gross": "Revenue + freight", "total_payment_value": "Total paid",
    "paid_amount": "Total paid", "total_items_price": "Items subtotal",
    "total_freight": "Freight", "freight_value": "Freight per item",
    "line_price": "Line price", "line_freight": "Line freight",
    "price": "Item price", "latitude": "Latitude", "longitude": "Longitude",
    "product_weight_g": "Weight (g)", "product_length_cm": "Length (cm)",
    "product_height_cm": "Height (cm)", "product_width_cm": "Width (cm)",
    "order_month": "Order month", "order_purchase_timestamp": "Purchase date",
    "order_approved_at": "Approved at", "order_delivered_carrier_date": "Delivered to carrier",
    "order_delivered_customer_date": "Delivered to customer",
    "order_estimated_delivery_date": "Estimated delivery",
    "review_creation_date": "Review created", "review_answer_timestamp": "Review answered",
    "shipping_limit_date": "Shipping limit", "order_date": "Order date", "date": "Date",
    "order_status": "Order status",
    "geolocation_city": "City", "customer_city": "City", "seller_city": "City",
    "city": "City", "customer_unique_id": "Customer", "customer_id": "Customer id",
    "order_id": "Order id", "product_id": "Product id", "seller_id": "Seller id",
    "review_id": "Review id", "customer_zip_code_prefix": "Customer zip prefix",
    "seller_zip_code_prefix": "Seller zip prefix",
    "geolocation_zip_code_prefix": "Zip prefix", "zip_code_prefix": "Zip prefix",
    "seller_ids": "Seller ids", "product_ids": "Product ids",
    "review_comment_title": "Review comment title",
    "review_comment_message": "Review comment message",
}

PALETTE = {"ok": "#0f6b47", "warn": "#b7791f", "bad": "#b0413e",
           "info": "#1f3a93", "muted": "#9aa3ad"}


def rel_path(rel: str) -> Path:
    return (STAR if rel.startswith("star_schema/") else CLEAN) / rel.split("/")[-1]


def read_table(rel: str) -> pd.DataFrame:
    """Read one cleaned CSV with the right dtypes (zip/id stay text, dates parsed)."""
    str_cols = [c for c in STR_COLS.get(rel, [])]
    date_cols = [c for c in DATE_COLS.get(rel, [])]
    int_cols = [c for c in INT_COLS.get(rel, [])]
    dtype = {c: str for c in str_cols}
    path = rel_path(rel)
    df = pd.read_csv(path, dtype=dtype, keep_default_na=False,
                     na_values=["", "NULL", "nan"])
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in int_cols:
        if c in df.columns:
            df[c] = (pd.to_numeric(df[c].replace("", np.nan), errors="coerce")
                     .astype("Int64"))
    return df


def _sample(vals: pd.Series) -> list:
    uniq = vals.dropna().unique()
    return [str(v) for v in uniq[:6]]


def profile_table(rel: str) -> dict:
    """Full descriptive profile of one table."""
    df = read_table(rel)
    meta = _TABLES_BY_REL[rel]

    pk = vcd.PRIMARY_KEYS.get(rel)
    comp = vcd.COMPOSITE_KEYS.get(rel, [])
    key_cols = comp or ([pk] if pk else [])
    n_unique_keys = df.drop_duplicates(key_cols).shape[0] if key_cols and all(
        c in df.columns for c in key_cols) else None

    columns = []
    for col in df.columns:
        s = df[col]
        name = col
        n_null = int(s.isna().sum())
        n_uniq = int(s.nunique(dropna=True))
        col_prof = {
            "name": col,
            "dtype": str(s.dtype),
            "null": n_null,
            "null_pct": round(100.0 * n_null / len(df), 2) if len(df) else 0.0,
            "n_unique": n_uniq,
            "samples": _sample(s),
        }
        if pd.api.types.is_numeric_dtype(s) and n_uniq > 1:
            desc = s.describe()
            col_prof["kind"] = "numeric"
            col_prof["stats"] = {
                "min": None if pd.isna(desc.get("min")) else round(float(desc["min"]), 2),
                "q25": None if pd.isna(desc.get("25%")) else round(float(desc["25%"]), 2),
                "median": None if pd.isna(desc.get("50%")) else round(float(desc["50%"]), 2),
                "mean": None if pd.isna(desc.get("mean")) else round(float(desc["mean"]), 2),
                "q75": None if pd.isna(desc.get("75%")) else round(float(desc["75%"]), 2),
                "max": None if pd.isna(desc.get("max")) else round(float(desc["max"]), 2),
                "std": None if pd.isna(desc.get("std")) else round(float(desc["std"]), 2),
            }
        elif pd.api.types.is_datetime64_any_dtype(s.dtype) \
                or (s.dtype == object and col in DATE_COLS.get(rel, [])):
            col_prof["kind"] = "datetime"
            valid = pd.to_datetime(s, errors="coerce").dropna()
            if len(valid):
                col_prof["stats"] = {"min": str(valid.min()), "max": str(valid.max())}
            else:
                col_prof["stats"] = {}
        elif n_uniq <= 60:
            col_prof["kind"] = "categorical"
            col_prof["top"] = s.value_counts(dropna=False).head(10).to_dict()
        else:
            col_prof["kind"] = "text"

        # nominal categories are always worth a chart, whatever their cardinality
        if name in NOMINAL_COLS:
            col_prof["kind"] = "categorical"
            col_prof["top"] = s.value_counts(dropna=False).head(10).to_dict()

        # semantic chart type (overrides the dtype-based kind)
        if name in SKIP_COLS:
            col_prof["chart"] = "skip"
        elif name in COORD_COLS:
            col_prof["chart"] = "scatter"
        elif name in BINARY_COLS:
            col_prof["chart"] = "donut"
        elif name in ORDINAL_COLS:
            col_prof["chart"] = "bar"
            col_prof["ordered"] = True
        elif col_prof["kind"] == "numeric":
            col_prof["chart"] = "hist"
        elif col_prof["kind"] == "categorical":
            col_prof["chart"] = "bar"
            col_prof["ordered"] = False
        elif col_prof["kind"] == "datetime":
            col_prof["chart"] = "trend"
        else:
            col_prof["chart"] = "skip"
        col_prof["label"] = LABELS.get(name, name)
        columns.append(col_prof)

    return {
        "rel": rel,
        "key": meta["key"],
        "label": meta["label"],
        "group": meta["group"],
        "rows": len(df),
        "cols": df.shape[1],
        "key_cols": key_cols,
        "key_unique": n_unique_keys,
        "columns": columns,
        "df": df,
    }


def dama5(prof: dict) -> dict:
    """DAMA-5 scoring: Completeness / Consistency / Accuracy / Timeliness / Uniqueness."""
    rel = prof["rel"]
    df = prof["df"]

    allowed = set(vcd.NULL_ALLOWED.get(rel, []))
    real_nulls = {c["name"]: c["null"] for c in prof["columns"]
                  if c["null"] > 0 and c["name"] not in allowed}

    # Completeness
    if not real_nulls:
        comp = ("pass", "no unexpected nulls")
    else:
        comp = ("warn", f"{len(real_nulls)} col(s) with nulls outside allowlist")

    # Consistency
    issues = []
    if "review_score" in df.columns:
        bad = df["review_score"].dropna()
        bad = bad[~bad.isin([1, 2, 3, 4, 5])]
        if len(bad):
            issues.append(f"review_score out of 1..5 ({len(bad)})")
    for bc in BOOL_COLS & set(df.columns):
        vals = set(df[bc].dropna().unique())
        if not vals <= {0, 1}:
            issues.append(f"{bc} not in {{0,1}}")
    for mc in MONEY_COLS & set(df.columns):
        try:
            if (pd.to_numeric(df[mc], errors="coerce") < 0).any():
                issues.append(f"{mc} negative")
        except Exception:
            pass
    cons = ("pass", "domains OK") if not issues else ("warn", "; ".join(issues[:3]))

    # Accuracy (text-key hygiene + money parseability)
    bad_text = 0
    for c in vcd.TEXT_KEYS:
        if c in df.columns:
            bad_text += int(df[c].str.contains(r'["\s]', na=False).sum())
    acc = ("pass", "no key/whitespace issues") if bad_text == 0 else \
        ("warn", f"{bad_text} text-key cells contain quotes/whitespace")

    # Timeliness (dates parse + order sanity on master)
    n_bad_dates = 0
    for c in DATE_COLS.get(rel, []):
        if c in df.columns:
            s = df[c].dropna()
            n_bad_dates += int(pd.to_datetime(s, errors="coerce").isna().sum())
    if rel == "olist_master.csv" and "order_purchase_timestamp" in df.columns \
            and "order_delivered_customer_date" in df.columns:
        a = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
        b = pd.to_datetime(df["order_delivered_customer_date"], errors="coerce")
        both = a.notna() & b.notna()
        n_bad_dates += int((b[both] < a[both]).sum())
    time = ("pass", "all dates parse & ordered") if n_bad_dates == 0 else \
        ("warn", f"{n_bad_dates} unparseable / misordered dates")

    # Uniqueness
    if prof["key_unique"] is None:
        uni = ("info", "no key column defined")
    elif prof["key_unique"] == prof["rows"]:
        uni = ("pass", f"{'+'.join(prof['key_cols'])} unique ({prof['rows']:,})")
    else:
        uni = ("fail", f"key not unique: {prof['key_unique']:,}/{prof['rows']:,}")

    scores = {"Completeness": comp, "Consistency": cons, "Accuracy": acc,
              "Timeliness": time, "Uniqueness": uni}
    statuses = [v[0] for v in scores.values()]
    overall = "fail" if "fail" in statuses else ("warn" if "warn" in statuses else "pass")
    return {"rel": rel, "scores": scores, "overall": overall}


def overview() -> pd.DataFrame:
    """One-row-per-table summary grid."""
    rows = []
    for t in TABLES:
        p = profile_table(t["rel"])
        d = dama5(p)
        rows.append({
            "Table": t["label"],
            "File": t["rel"],
            "Group": t["group"],
            "Rows": f"{p['rows']:,}",
            "Cols": p["cols"],
            "PK unique": "✅" if p["key_unique"] == p["rows"] else (
                "—" if p["key_unique"] is None else f"❌ {p['key_unique']:,}"),
            "Null cols": sum(1 for c in p["columns"] if c["null"] > 0),
            "DAMA-5": {"pass": "✅", "warn": "☑", "fail": "❌"}[d["overall"]],
        })
    return pd.DataFrame(rows)


def verdict() -> dict:
    """Re-run the full clean-check and split results per table + global summary."""
    vcd.CHECKS.clear()
    vcd.check_tables()
    vcd.check_domains()
    vcd.check_zips()
    vcd.check_dates()
    vcd.check_star()
    vcd.check_sums()
    vcd.check_doc_gaps()
    checks = list(vcd.CHECKS)
    by_table: dict[str, list[dict]] = {}
    for c in checks:
        by_table.setdefault(c.get("table", ""), []).append(c)
    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "INFO": 0, "SKIP": 0}
    for c in checks:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    return {"checks": checks, "by_table": by_table, "counts": counts,
            "generated_at": datetime.now().isoformat(timespec="seconds")}


if __name__ == "__main__":
    print(f"Registry: {len(TABLES)} tables")
    for t in TABLES:
        p = profile_table(t["rel"])
        d = dama5(p)
        print(f"  [{d['overall']:4s}] {p['label']:<28s} {p['rows']:>8,} rows x {p['cols']} cols")
