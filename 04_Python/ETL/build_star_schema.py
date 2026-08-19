"""
OLIST - STAR SCHEMA BUILDER (Power BI ready)
====================================================
Run:  python build_star_schema.py
Reads : 02_Cleaned_data/*.csv   (Phase-2 cleaned outputs)
Writes: 02_Cleaned_data/star_schema/  (dimensions + facts)
Plus:   data_model.md (keys, relationships, measures)

Star schema produced:
  Dim_Date, Dim_Customer, Dim_Product, Dim_Seller, Dim_Geography
  Fact_Orders (grain: order) , Fact_OrderItems (grain: order line)

Rules (PROJECT_CANVAS §7 / §9):
  - Analysis universe = DELIVERED orders only (same as olist_master.csv)
  - Order revenue has two definitions: order_revenue (goods only, the KPI
    baseline) and order_revenue_gross (goods + freight).
  - Fact_OrderItems is filtered to the same delivered-order universe so
    referential integrity with Fact_Orders / Dim_Date holds.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[2]
CLEAN = PROJECT / "02_Cleaned_data"
STAR = CLEAN / "star_schema"
STAR.mkdir(parents=True, exist_ok=True)


def save(df: pd.DataFrame, name: str) -> None:
    df.to_csv(STAR / name, index=False)
    print(f"  {name:22s} {len(df):>9,} rows x {df.shape[1]:<2} cols  -> {name}")


def dim_customer():
    df = pd.read_csv(CLEAN / "olist_customers_dataset.csv",
                     dtype={"customer_zip_code_prefix": str})
    df = df.drop_duplicates("customer_id").reset_index(drop=True)
    save(df, "Dim_Customer.csv")
    return df


def dim_product():
    df = pd.read_csv(CLEAN / "products_clean.csv")
    df["category_english"] = df["category_english"].fillna("uncategorized")
    out = df[["product_id", "product_category_name", "category_english",
              "product_weight_g", "product_length_cm", "product_height_cm",
              "product_width_cm", "product_photos_qty"]].copy()
    save(out, "Dim_Product.csv")
    return out


def dim_seller():
    df = pd.read_csv(CLEAN / "olist_sellers_dataset.csv",
                     dtype={"seller_zip_code_prefix": str})
    save(df, "Dim_Seller.csv")
    return df


def dim_date(master: pd.DataFrame):
    start = master["order_purchase_timestamp"].min()
    hi = master[["order_purchase_timestamp", "order_delivered_customer_date"]].stack().max()
    # stack drops NaN; take max of delivered column as last day
    hi = master["order_delivered_customer_date"].max()
    dates = pd.date_range(start=start.normalize(), end=hi.normalize(), freq="D")
    df = pd.DataFrame({"date": dates})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["day_of_month"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek  # Mon=0..Sun=6
    df["weekday"] = df["date"].dt.strftime("%A")
    df["is_weekend"] = (df["date"].dt.dayofweek >= 5).astype(int)
    df["is_workday"] = 1 - df["is_weekend"]
    save(df, "Dim_Date.csv")
    return df


def dim_geography():
    df = pd.read_csv(CLEAN / "geolocation_clean.csv",
                     dtype={"geolocation_zip_code_prefix": str})
    out = df[["geolocation_zip_code_prefix", "latitude", "longitude",
              "geolocation_city", "geolocation_state"]].rename(columns={
                  "geolocation_zip_code_prefix": "zip_code_prefix",
                  "geolocation_city": "city",
                  "geolocation_state": "state"})
    save(out, "Dim_Geography.csv")
    return out


def fact_orders(master: pd.DataFrame):
    out = master[[
        "order_id", "customer_id", "order_purchase_timestamp",
        "order_revenue", "order_revenue_incl_freight", "total_freight",
        "total_payment_value", "payment_installments_max", "item_count",
        "payment_types_used", "delivery_days", "promised_delivery_days",
        "days_early_or_late", "is_late", "review_score", "has_review_comment",
        "order_month", "order_year", "is_weekend",
    ]].copy()
    out["order_date"] = out["order_purchase_timestamp"]
    out["date_key"] = out["order_date"].dt.strftime("%Y%m%d").astype(int)
    out["order_id"] = out["order_id"].astype(str)
    out = out.rename(columns={
        "order_revenue": "order_revenue",
        "order_revenue_incl_freight": "order_revenue_gross",
        "total_payment_value": "paid_amount",
    })
    out["is_ontime"] = 1 - out["is_late"]
    out["order_revenue"] = out["order_revenue"].round(2)
    out["order_revenue_gross"] = out["order_revenue_gross"].round(2)
    # integer-semantic columns stay integers (nullable Int64 keeps nulls intact)
    for c in ["payment_installments_max", "item_count", "review_score",
              "delivery_days", "promised_delivery_days", "days_early_or_late"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")
    out = out[["order_id", "customer_id", "order_date", "date_key",
               "order_revenue", "order_revenue_gross", "total_freight",
               "paid_amount", "payment_installments_max", "item_count",
               "payment_types_used", "delivery_days", "promised_delivery_days",
               "days_early_or_late", "is_late", "is_ontime", "review_score",
               "has_review_comment", "order_month", "order_year", "is_weekend"]]
    save(out, "Fact_Orders.csv")
    return out


def fact_order_items(items: pd.DataFrame, master: pd.DataFrame):
    kept = set(master["order_id"].astype(str))
    it = items.copy()
    it["order_id"] = it["order_id"].astype(str)
    it = it[it["order_id"].isin(kept)].copy()

    ctx = master[["order_id", "order_purchase_timestamp", "is_late"]].copy()
    ctx["order_id"] = ctx["order_id"].astype(str)
    it = it.merge(ctx, on="order_id", how="left")
    it["order_date"] = it["order_purchase_timestamp"]
    it["date_key"] = it["order_date"].dt.strftime("%Y%m%d").astype(int)
    it["line_price"] = it["price"]
    it["line_freight"] = it["freight_value"]
    # NOTE: the raw Olist items table has no quantity column, so no fabricated
    # constant-1 'quantity' is emitted here (it would be misleading).
    out = it[["order_item_id", "order_id", "product_id", "seller_id",
              "order_date", "date_key", "line_price",
              "line_freight", "is_late"]].reset_index(drop=True)
    save(out, "Fact_OrderItems.csv")
    return out


def main():
    print("=" * 60)
    print("OLIST STAR SCHEMA BUILDER")
    print("=" * 60)

    master = pd.read_csv(CLEAN / "olist_master.csv", parse_dates=[
        "order_purchase_timestamp", "order_delivered_customer_date",
        "order_estimated_delivery_date"])
    items = pd.read_csv(CLEAN / "items_clean.csv")

    print("\n-- Dimensions --")
    dim_customer()
    dim_product()
    dim_seller()
    ddate = dim_date(master)
    dim_geography()

    print("\n-- Facts --")
    fo = fact_orders(master)
    fi = fact_order_items(items, master)

    print("\n-- Integrity / consistency --")
    print(f"Fact_Orders rows           : {len(fo):,}  (distinct order_id {fo['order_id'].nunique():,})")
    print(f"Fact_OrderItems rows       : {len(fi):,}  (distinct order_id {fi['order_id'].nunique():,})")
    print(f"Item order_ids missing from Fact_Orders : {len(set(fi['order_id']) - set(fo['order_id']))}")
    print(f"Fact_Orders order_rev (goods)     : R$ {fo['order_revenue'].sum():,.2f}")
    print(f"Fact_Orders order_rev_gross (incl): R$ {fo['order_revenue_gross'].sum():,.2f}")
    print(f"Fact_Orders freight               : R$ {fo['total_freight'].sum():,.2f}")
    print(f"Fact_OrderItems line_price sum    : R$ {fi['line_price'].sum():,.2f}")
    print(f"Fact_OrderItems line_freight sum  : R$ {fi['line_freight'].sum():,.2f}")
    print(f"Dim_Date range                    : {ddate['date'].min().date()} -> {ddate['date'].max().date()} "
          f"({len(ddate):,} days)")
    print("\nDONE")


if __name__ == "__main__":
    main()