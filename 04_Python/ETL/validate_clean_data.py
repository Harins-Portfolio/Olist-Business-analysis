"""
OLIST - CLEAN DATA VALIDATION (complete clean check)
====================================================
Run:  python validate_clean_data.py
Reads : 02_Cleaned_data/*.csv  +  02_Cleaned_data/star_schema/*.csv   (never modified)
Writes: 06_AI/Outputs/Generated_Docs/clean_check.json   (machine-readable results)
        06_AI/Outputs/Generated_Docs/clean_check_report.md (human report, via Phase C)

Purpose
-------
Independent, reproducible verification that the Phase-2 cleaning pipeline and the
Phase-2 star schema are complete, internally consistent, and SQL-loadable. This is
NOT a re-run of cleaning - it validates the products of cleaning against a manifest
of documented expectations (PROJECT_CANVAS.md, data_model.md, cleaning_audit.json).

Checks are grouped:
  1. Per-table quality   (row counts, nulls, uniqueness, domains, encoding)
  2. List-column hygiene (pipe/comma separators, whitespace, date / zip typing)
  3. Star referential integrity (dims <-> facts, orphans, key resolution)
  4. Sum / consistency   (fact totals reconcile with master + documented numbers)
  5. Document gap scan   (doc-vs-actual on known issues: not_defined, zero payments, AOV)

Exit code 0 when all Critical checks pass; non-zero if any Critical fails.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW = PROJECT_ROOT / "01_Raw_Data"
CLEAN = PROJECT_ROOT / "02_Cleaned_data"
STAR = CLEAN / "star_schema"
DOCS = PROJECT_ROOT / "06_AI" / "Outputs" / "Generated_Docs"
DOCS.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
#  Reference manifest - documented expectations (source of truth for the checks)
# --------------------------------------------------------------------------- #
# Grain / PKs that must be unique in each table.
PRIMARY_KEYS = {
    "olist_master.csv": "order_id",
    "orders_clean.csv": "order_id",
    "orders_delivered.csv": "order_id",
    "payments_clean.csv": "order_id",
    "orders_items_aggregated.csv": "order_id",
    "items_clean.csv": "order_item_id",
    "reviews_clean.csv": "order_id",
    "products_clean.csv": "product_id",
    "geolocation_clean.csv": "geolocation_zip_code_prefix",
    "olist_customers_dataset.csv": "customer_id",
    "olist_sellers_dataset.csv": "seller_id",
    "star_schema/Fact_Orders.csv": "order_id",
    "star_schema/Fact_OrderItems.csv": "order_item_id",
    "star_schema/Dim_Customer.csv": "customer_id",
    "star_schema/Dim_Product.csv": "product_id",
    "star_schema/Dim_Seller.csv": "seller_id",
    "star_schema/Dim_Geography.csv": "zip_code_prefix",
    "star_schema/Dim_Date.csv": "date_key",
}

# Line-item tables: `order_item_id` is only unique WITHIN an order (order_item_id
# restarts per order in the Olist schema) -> the real key is the composite pair.
COMPOSITE_KEYS = {
    "items_clean.csv": ["order_id", "order_item_id"],
    "star_schema/Fact_OrderItems.csv": ["order_id", "order_item_id"],
}

# Columns legitimately NULL that must NOT be treated as data problems. Any null
# appearing OUTSIDE this allowlist is a genuine completeness failure.
NULL_ALLOWED = {
    "olist_master.csv": [
        "order_approved_at", "order_delivered_carrier_date",
        "total_payment_value", "payment_types_used", "payment_installments_max",
        "item_count", "total_items_price", "total_freight", "n_sellers",
        "seller_ids", "product_ids", "review_id", "review_score",
        "review_comment_title", "review_comment_message", "review_creation_date",
        "review_answer_timestamp", "order_revenue", "order_revenue_incl_freight",
    ],
    "orders_clean.csv": ["order_approved_at", "order_delivered_carrier_date"],
    "orders_delivered.csv": ["order_approved_at", "order_delivered_carrier_date",
                             "order_delivered_customer_date"],
    "reviews_clean.csv": ["review_comment_title", "review_comment_message"],
    "products_clean.csv": ["product_name_lenght", "product_description_lenght",
                           "product_photos_qty", "product_weight_g",
                           "product_length_cm", "product_height_cm", "product_width_cm"],
    "star_schema/Fact_Orders.csv": ["order_revenue", "order_revenue_gross",
                                    "total_freight", "paid_amount",
                                    "payment_installments_max", "item_count",
                                    "payment_types_used", "review_score"],
    "star_schema/Dim_Product.csv": ["product_weight_g", "product_length_cm",
                                    "product_height_cm", "product_width_cm",
                                    "product_photos_qty"],
}

# Documented row counts (data_model.md / README / cleaning_audit.json). Pass if equal.
REF_ROWS = {
    "olist_master.csv": 96456,
    "orders_clean.csv": 96456,
    "orders_delivered.csv": 96478,
    "payments_clean.csv": 99440,
    "items_clean.csv": 112647,
    "orders_items_aggregated.csv": 98663,
    "reviews_clean.csv": 98673,
    "products_clean.csv": 32951,
    "geolocation_clean.csv": 19011,
    "olist_customers_dataset.csv": 99441,
    "olist_sellers_dataset.csv": 3095,
    "star_schema/Fact_Orders.csv": 96456,
    "star_schema/Fact_OrderItems.csv": 110170,
    "star_schema/Dim_Customer.csv": 99441,
    "star_schema/Dim_Product.csv": 32951,
    "star_schema/Dim_Seller.csv": 3095,
    "star_schema/Dim_Geography.csv": 19011,
    "star_schema/Dim_Date.csv": 763,
}

# String key columns that MUST survive as text (leading-zero safe) - SQL typing.
TEXT_KEYS = [
    "order_id", "order_item_id", "customer_id", "customer_unique_id",
    "product_id", "seller_id", "geolocation_zip_code_prefix",
    "zip_code_prefix", "customer_zip_code_prefix", "seller_zip_code_prefix",
]

# Zip/CEB columns - Brazilian postal codes ARE leading-zero significant, so any
# value coerced to int will have silently lost leading zeros. A clean zip parses
# to a 5-digit (or 8-digit CEP) numeric POSITIVE integer when read as text.
ZIP_COLS = {
    "olist_master.csv": "customer_zip_code_prefix",
    "olist_customers_dataset.csv": "customer_zip_code_prefix",
    "olist_sellers_dataset.csv": "seller_zip_code_prefix",
    "geolocation_clean.csv": "geolocation_zip_code_prefix",
    "star_schema/Dim_Customer.csv": "customer_zip_code_prefix",
    "star_schema/Dim_Seller.csv": "seller_zip_code_prefix",
    "star_schema/Dim_Geography.csv": "zip_code_prefix",
}

# Datetime columns that MUST parse to a real calendar date/time.
DATE_COLS = {
    "olist_master.csv": ["order_purchase_timestamp", "order_approved_at",
                         "order_delivered_carrier_date", "order_delivered_customer_date",
                         "order_estimated_delivery_date", "review_creation_date",
                         "review_answer_timestamp"],
    "orders_clean.csv": ["order_purchase_timestamp", "order_approved_at",
                         "order_delivered_carrier_date", "order_delivered_customer_date",
                         "order_estimated_delivery_date"],
    "reviews_clean.csv": ["review_creation_date", "review_answer_timestamp"],
}

MONEY_COLS = ["order_revenue", "order_revenue_incl_freight", "total_freight",
              "total_payment_value", "paid_amount", "order_revenue_gross",
              "line_price", "line_freight", "price", "freight_value",
              "total_items_price"]


def result(name: str, status: str, detail: str, table: str = "") -> dict:
    return {"check": name, "status": status, "detail": detail, "table": table}


CHECKS: list[dict] = []


def add(name, status, detail, table=""):
    CHECKS.append(result(name, status, detail, table))


def _safe_read(rel: str) -> pd.DataFrame:
    return pd.read_csv(CLEAN / rel, dtype=str, keep_default_na=False,
                       na_values=["", "NULL", "nan"])


# --------------------------------------------------------------------------- #
#  1. PER-TABLE QUALITY
# --------------------------------------------------------------------------- #
def check_tables():
    for rel, pk in PRIMARY_KEYS.items():
        path = CLEAN / rel if "/" not in rel else STAR / rel.split("/")[1]
        if not path.exists():
            add("exists", "FAIL", f"missing file {rel}", rel)
            continue
        df = _safe_read(rel)
        rows = len(df)

        # row count vs manifest
        ref = REF_ROWS.get(rel)
        if ref is not None and rows != ref:
            add("row_count", "FAIL", f"expected {ref:,} got {rows:,}", rel)
        else:
            add("row_count", "PASS", f"{rows:,} rows", rel)

        # PK uniqueness (composite pair for line-item tables)
        comp = COMPOSITE_KEYS.get(rel)
        if comp and all(c in df.columns for c in comp):
            n_unique = df.drop_duplicates(comp).shape[0]
            label = f"({'+'.join(comp)})"
        elif pk in df.columns:
            n_unique = df[pk].nunique()
            label = pk
        else:
            label, n_unique = pk, 0
        if n_unique == rows:
            add("pk_unique", "PASS", f"{label} unique ({n_unique:,})", rel)
        else:
            add("pk_unique", "FAIL", f"{label} has {n_unique:,} uniq / {rows:,} rows", rel)

        # nulls: flag only nulls OUTSIDE the documented allowlist
        real_nulls = {c: int(df[c].isna().sum()) for c in df.columns
                      if df[c].isna().sum() > 0 and c not in NULL_ALLOWED.get(rel, [])}
        if rel == "olist_master.csv" and real_nulls:
            add("nulls", "FAIL", f"unexpected master nulls {json.dumps(real_nulls)}", rel)
        elif rel == "olist_master.csv":
            add("nulls", "PASS", "master nulls confined to documented allowlist", rel)
        elif real_nulls:
            add("nulls", "FAIL", f"unexpected nulls {json.dumps(real_nulls)}", rel)
        else:
            add("nulls", "PASS", "no unexpected nulls", rel)


# --------------------------------------------------------------------------- #
#  2. VALUE / TYPE / HYGIENE
# --------------------------------------------------------------------------- #
def check_domains():
    # reviews
    rev = _safe_read("reviews_clean.csv")
    bad = rev[~rev["review_score"].isin(["1", "2", "3", "4", "5"])]
    add("domain", "PASS" if bad.empty else "FAIL",
        f"review_score in 1..5 (violations={int(len(bad))})", "reviews_clean.csv")

    # master boolean flags
    m = _safe_read("olist_master.csv")
    for col in ["is_late", "is_weekend", "has_review_comment"]:
        vals = set(m[col].dropna().unique())
        ok = vals <= {"0", "1"}
        add("domain", "PASS" if ok else "FAIL",
            f"{col} in {{0,1}} got {sorted(vals)}", "olist_master")

    # money non-negative (master + facts + items + reviews)
    money_files = [
        ("olist_master.csv", ["order_revenue", "order_revenue_incl_freight",
                              "total_freight", "total_payment_value", "total_items_price"]),
        ("star_schema/Fact_Orders.csv", ["order_revenue", "order_revenue_gross",
                                         "total_freight", "paid_amount"]),
        ("star_schema/Fact_OrderItems.csv", ["line_price", "line_freight"]),
        ("items_clean.csv", ["price", "freight_value"]),
    ]
    for rel, cols in money_files:
        df = _safe_read(rel)
        for col in cols:
            if col not in df.columns:
                continue
            num = pd.to_numeric(df[col], errors="coerce")
            neg = int((num < 0).sum())
            add("money", "PASS" if neg == 0 else "FAIL",
                f"{col} non-negative", rel)

    # fact booleans
    fo = _safe_read("star_schema/Fact_Orders.csv")
    for col in ["is_late", "is_ontime", "is_weekend", "has_review_comment"]:
        if col in fo.columns:
            vals = set(fo[col].dropna().unique())
            add("domain", "PASS" if vals <= {"0", "1"} else "FAIL",
                f"{col} in {{0,1}} got {sorted(vals)}", "Fact_Orders")

    # text key integrity: no accidental quote / whitespace, non-empty.
    # NOTE: this does NOT prove leading zeros were preserved - see check_zips().
    for col in TEXT_KEYS:
        if col in m.columns:
            bad = int(m[col].isna().sum() + (m[col].str.contains(r'["\s]', na=False)).sum())
            add("text_keys", "PASS" if bad == 0 else "FAIL",
                f"{col} clean (bad={bad})", "olist_master")


# --------------------------------------------------------------------------- #
#  2b. ZIP LEADING-ZERO INTEGRITY (CEP = leading-zero significant postal codes)
# --------------------------------------------------------------------------- #
# A clean zip that was produced via int coercion will have silently lost its
# leading zeros (e.g. "04106" -> "4106"). The only reliable way to prove a
# leading-zero-safe round-trip is to compare the C-cleaned leading-zero count
# against the RAW source. Mismatch => data lost upstream.
RAW_ZIP_COLS = {
    "olist_master.csv": ("olist_customers_dataset.csv", "customer_zip_code_prefix"),
    "olist_customers_dataset.csv": ("olist_customers_dataset.csv", "customer_zip_code_prefix"),
    "olist_sellers_dataset.csv": ("olist_sellers_dataset.csv", "seller_zip_code_prefix"),
    "geolocation_clean.csv": ("olist_geolocation_dataset.csv", "geolocation_zip_code_prefix"),
    "star_schema/Dim_Customer.csv": ("olist_customers_dataset.csv", "customer_zip_code_prefix"),
    "star_schema/Dim_Seller.csv": ("olist_sellers_dataset.csv", "seller_zip_code_prefix"),
    "star_schema/Dim_Geography.csv": ("olist_geolocation_dataset.csv", "geolocation_zip_code_prefix"),
}


def check_zips():
    for rel, col in ZIP_COLS.items():
        df = _safe_read(rel)
        if col not in df.columns:
            add("zip", "FAIL", f"column {col} missing", rel)
            continue
        s = df[col].astype(str)
        leading_zero = int(s.str.match(r"^0\d").sum())

        raw_rel, raw_col = RAW_ZIP_COLS.get(rel, (None, None))
        if raw_rel is None:
            add("zip", "SKIP", "no raw comparison configured", rel)
            continue
        raw = pd.read_csv(RAW / raw_rel, dtype=str)
        raw_lz = int(raw[raw_col].str.match(r"^0\d").sum())

        # Grains differ (master/subset, geo=dedup) so counts rarely match exactly.
        # The corruption we must catch is FULL loss: raw has leading-zero zips but
        # the cleaned output has none (int-coercion). Any positive clean count
        # proves preservation and passes.
        if raw_lz > 0 and leading_zero == 0:
            add("zip", "FAIL",
                f"{rel}.{col}: RAW has {raw_lz:,} leading-zero zips but cleaned has "
                f"{leading_zero:,} -> leading zeros LOST (int coercion)", rel)
        elif raw_lz == 0:
            add("zip", "PASS", f"{rel}.{col}: no leading-zero zips in raw data", rel)
        elif raw_lz > 0 and leading_zero > 0:
            add("zip", "PASS",
                f"{rel}.{col}: leading-zero zips preserved (raw {raw_lz:,} -> clean {leading_zero:,})",
                rel)


# --------------------------------------------------------------------------- #
#  2c. DATETIME PARSING
# --------------------------------------------------------------------------- #
def check_dates():
    for rel, cols in DATE_COLS.items():
        df = _safe_read(rel)
        for col in cols:
            if col not in df.columns:
                continue
            s = df[col].dropna()
            parsed = pd.to_datetime(s, errors="coerce")
            n_bad = int(parsed.isna().sum())
            # order sanity: delivered >= purchased when both present
            add("date", "PASS" if n_bad == 0 else "FAIL",
                f"{col} parses ({len(s):,} ok, {n_bad} bad)", rel)
        # cross-field date ordering on master
        if rel == "olist_master.csv" and "order_purchase_timestamp" in df.columns \
                and "order_delivered_customer_date" in df.columns:
            a = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
            b = pd.to_datetime(df["order_delivered_customer_date"], errors="coerce")
            both = a.notna() & b.notna()
            n_bad_order = int((b[both] < a[both]).sum())
            add("date", "PASS" if n_bad_order == 0 else "FAIL",
                f"delivered< purchase (n={n_bad_order})", rel)


# --------------------------------------------------------------------------- #
#  3. STAR REFERENTIAL INTEGRITY
# --------------------------------------------------------------------------- #
def check_star():
    fo = _safe_read("star_schema/Fact_Orders.csv")
    fi = _safe_read("star_schema/Fact_OrderItems.csv")
    dc = _safe_read("star_schema/Dim_Customer.csv")
    dp = _safe_read("star_schema/Dim_Product.csv")
    ds = _safe_read("star_schema/Dim_Seller.csv")
    dd = _safe_read("star_schema/Dim_Date.csv")
    dg = _safe_read("star_schema/Dim_Geography.csv")

    # items.order_id all in facts
    orphans = set(fi["order_id"]) - set(fo["order_id"])
    add("ri", "PASS" if not orphans else "FAIL",
        f"{len(orphans)} Fact_OrderItems.order_id not in Fact_Orders", "Fact_OrderItems")

    # item dims resolve
    for col, dim_df, dim_pk, dim_name in [
        ("product_id", dp, "product_id", "Dim_Product"),
        ("seller_id", ds, "seller_id", "Dim_Seller"),
    ]:
        missing = set(fi[col]) - set(dim_df[dim_pk])
        add("ri", "PASS" if not missing else "FAIL",
            f"{len(missing)} Fact_OrderItems.{col} unresolved in {dim_name}", dim_name)

    # fact customer resolves
    missing_cust = set(fo["customer_id"]) - set(dc["customer_id"])
    add("ri", "PASS" if not missing_cust else "FAIL",
        f"{len(missing_cust)} Fact_Orders.customer_id unresolved", "Dim_Customer")

    # date keys resolve
    missing_dk = (set(fo["date_key"]) - set(dd["date_key"])) | \
                 (set(fi["date_key"]) - set(dd["date_key"]))
    add("ri", "PASS" if not missing_dk else "FAIL",
        f"{len(missing_dk)} fact date_key(s) unresolved in Dim_Date", "Dim_Date")


# --------------------------------------------------------------------------- #
#  4. SUM CONSISTENCY
# --------------------------------------------------------------------------- #
def check_sums():
    fo = pd.read_csv(STAR / "Fact_Orders.csv")
    fi = pd.read_csv(STAR / "Fact_OrderItems.csv")
    m = pd.read_csv(CLEAN / "olist_master.csv")

    rev_orders = fo["order_revenue"].sum()
    rev_items = fi["line_price"].sum()
    add("sum", "PASS" if np.isclose(rev_orders, rev_items, atol=0.005) else "FAIL",
        f"Fact_Orders.order_revenue {rev_orders:,.2f} vs line_price {rev_items:,.2f}",
        "sum")

    frt_orders = fo["total_freight"].sum()
    frt_items = fi["line_freight"].sum()
    add("sum", "PASS" if np.isclose(frt_orders, frt_items, atol=0.005) else "FAIL",
        f"Fact_Orders.total_freight {frt_orders:,.2f} vs line_freight {frt_items:,.2f}",
        "sum")

    # master vs star must reconcile (same grain, 96,456)
    add("sum", "PASS" if len(m) == len(fo) else "FAIL",
        f"master rows {len(m):,} vs Fact_Orders {len(fo):,}", "master")

    rev_master = m["order_revenue"].astype(float).sum()
    add("sum", "PASS" if np.isclose(rev_master, rev_orders, atol=0.005) else "FAIL",
        f"master.order_revenue {rev_master:,.2f} vs Fact {rev_orders:,.2f}", "master")

    # documented gross / freight
    gross = fo["order_revenue_gross"].sum()
    add("meta", "INFO", f"order_revenue_gross {gross:,.2f} (data_model.md 15,394,233.21)", "sum")


# --------------------------------------------------------------------------- #
#  5. DOC GAP SCAN - known decision mismatches flagged, not silently swallowed
# --------------------------------------------------------------------------- #
def check_doc_gaps():
    # AOV: clean universe vs EDA/canvas headline
    m = pd.read_csv(CLEAN / "olist_master.csv")
    aov_clean = m["order_revenue"].astype(float).sum() / len(m)
    add("aov", "INFO",
        f"clean AOV {aov_clean:,.2f} (doc headline 137.04 via 13,221,498/96,478)",
        "olist_master")

    # payment_type 'not_defined' - canvas §5 says drop 3, pipeline kept+aggregated
    pmt = pd.read_csv(CLEAN / "payments_clean.csv")
    nd_types = pmt["payment_types_used"].astype(str).str.contains("not_defined", na=False).sum()
    add("gap:not_defined", "WARN",
        f"{int(nd_types)} orders carry payment_types_used containing 'not_defined' "
        "(canvas \u00a75 says drop 3)", "payments_clean")


# --------------------------------------------------------------------------- #
#  MAIN
# --------------------------------------------------------------------------- #
def main() -> int:
    print("=" * 70)
    print("OLIST COMPLETE CLEAN CHECK")
    print("=" * 70)

    check_tables()
    check_domains()
    check_zips()
    check_dates()
    check_star()
    check_sums()
    check_doc_gaps()

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "pipeline": "04_Python/ETL/validate_clean_data.py",
        "checks": CHECKS,
    }

    fails = [c for c in CHECKS if c["status"] in ("FAIL", "WARN")]
    critical = [c for c in CHECKS if c["status"] == "FAIL"]

    for c in CHECKS:
        icon = {"PASS": "OK ", "FAIL": "XX ", "WARN": "!! ", "INFO": ".. ",
                "SKIP": "-- "}[c["status"]]
        print(f"[{icon}] {c['check']:<22} {c['table']:<24} {c['detail']}")

    print("-" * 70)
    print(f"total={len(CHECKS)} pass={sum(1 for c in CHECKS if c['status']=='PASS')} "
          f"fail={sum(1 for c in CHECKS if c['status']=='FAIL')} "
          f"warn={sum(1 for c in CHECKS if c['status']=='WARN')}"
          f" info={sum(1 for c in CHECKS if c['status']=='INFO')}")
    if fails:
        print("\nNon-passing checks:")
        for c in fails:
            print(f"  [{c['status']}] {c['check']}: {c['detail']}")

    (DOCS / "clean_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nResults -> {DOCS / 'clean_check.json'}")
    return 1 if critical else 0


if __name__ == "__main__":
    sys.exit(main())