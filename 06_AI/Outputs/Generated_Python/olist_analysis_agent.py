"""
OLIST ANALYSIS AGENT
====================
Drop this file into BA_Projects/04_Python/
Run with: python olist_analysis_agent.py

What it does automatically:
  1. Loads and validates all cleaned source files
  2. Runs full EDA on the master dataset
  3. Detects outliers across all numeric columns
  4. Calculates all 8 KPIs
  5. Saves every output to the correct folder
  6. Prints a plain-English executive summary at the end

Requirements:
  pip install pandas numpy scipy plotly openpyxl

Before running:
  - Phase 2 cleaning must be complete
  - olist_master.csv must exist in 02_Cleaned_Data/
"""

import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PATHS = {
    "master":      os.path.join(PROJECT_ROOT, "02_Cleaned_Data", "olist_master.csv"),
    "items":       os.path.join(PROJECT_ROOT, "02_Cleaned_Data", "order_items_aggregated.csv"),
    "products":    os.path.join(PROJECT_ROOT, "02_Cleaned_Data", "products_clean.csv"),
    "sellers":     os.path.join(PROJECT_ROOT, "02_Cleaned_Data", "olist_sellers_dataset.csv"),
    "kpi_out":     os.path.join(PROJECT_ROOT, "02_Cleaned_Data", "kpi_tables"),
    "eda_out":     os.path.join(PROJECT_ROOT, "07_AI_Outputs"),
    "charts_out":  os.path.join(PROJECT_ROOT, "07_AI_Outputs", "charts"),
}

# KPI benchmarks — change these if client targets differ
BENCHMARKS = {
    "on_time_rate_pct":     90.0,   # % orders delivered on time — industry standard
    "avg_review_score":      4.0,   # out of 5 — healthy marketplace threshold
    "repeat_customer_rate":  3.0,   # % baseline for Olist (flagged as problem)
    "late_delivery_max_days": 30,   # orders beyond this are severe outliers
}

# Outlier detection method: "iqr" or "zscore"
OUTLIER_METHOD = "iqr"
OUTLIER_IQR_MULTIPLIER = 1.5   # standard = 1.5, strict = 3.0
OUTLIER_ZSCORE_THRESHOLD = 3.0

# ── SETUP ────────────────────────────────────────────────────────────────────

for path in [PATHS["kpi_out"], PATHS["eda_out"], PATHS["charts_out"]]:
    os.makedirs(path, exist_ok=True)

log_lines = []

def log(msg, section=False):
    if section:
        line = f"\n{'='*60}\n{msg}\n{'='*60}"
    else:
        line = f"  {msg}"
    print(line)
    log_lines.append(line)

def save_csv(df, filename, subfolder="kpi_out"):
    path = os.path.join(PATHS[subfolder], filename)
    df.to_csv(path, index=False)
    log(f"Saved: {filename} ({len(df)} rows)")
    return path

def save_chart(fig, filename):
    path = os.path.join(PATHS["charts_out"], filename)
    fig.write_html(path)
    log(f"Chart saved: {filename}")

# ── STEP 1: LOAD & VALIDATE ──────────────────────────────────────────────────

log("STEP 1 — LOADING DATA", section=True)

master = pd.read_csv(PATHS["master"], parse_dates=[
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
])

log(f"Master dataset: {len(master):,} rows × {master.shape[1]} columns")
log(f"Date range: {master['order_purchase_timestamp'].min().date()} → {master['order_purchase_timestamp'].max().date()}")

# Validate required columns
REQUIRED_COLS = [
    "order_id", "customer_unique_id", "order_purchase_timestamp",
    "order_delivered_customer_date", "order_estimated_delivery_date",
    "total_payment_value", "review_score", "customer_state",
    "delivery_days", "is_late", "order_month",
]
missing_cols = [c for c in REQUIRED_COLS if c not in master.columns]
if missing_cols:
    raise ValueError(f"Master dataset is missing required columns: {missing_cols}")
log(f"All required columns present ✓")

# Load supporting tables if available
items = pd.read_csv(PATHS["items"]) if os.path.exists(PATHS["items"]) else None
products = pd.read_csv(PATHS["products"]) if os.path.exists(PATHS["products"]) else None
sellers = pd.read_csv(PATHS["sellers"]) if os.path.exists(PATHS["sellers"]) else None

# ── STEP 2: EDA ──────────────────────────────────────────────────────────────

log("STEP 2 — EXPLORATORY DATA ANALYSIS", section=True)

eda_results = {}

# 2a. Numeric summary
numeric_cols = ["total_payment_value", "delivery_days", "review_score",
                "item_count", "total_items_price", "total_freight"]
numeric_cols = [c for c in numeric_cols if c in master.columns]

numeric_summary = master[numeric_cols].describe().T.round(2)
numeric_summary["null_count"] = master[numeric_cols].isnull().sum()
numeric_summary["null_pct"] = (master[numeric_cols].isnull().mean() * 100).round(2)
save_csv(numeric_summary.reset_index().rename(columns={"index": "column"}),
         "eda_numeric_summary.csv", "eda_out")
eda_results["numeric_summary"] = numeric_summary

# 2b. Revenue by month
master["order_month_dt"] = pd.to_datetime(master["order_month"], format="%Y-%m", errors="coerce")
monthly = (
    master.groupby("order_month")
    .agg(
        total_revenue=("total_payment_value", "sum"),
        order_count=("order_id", "count"),
    )
    .reset_index()
    .sort_values("order_month")
)
monthly["avg_order_value"] = (monthly["total_revenue"] / monthly["order_count"]).round(2)
monthly["revenue_mom_pct"] = monthly["total_revenue"].pct_change().mul(100).round(2)
monthly["total_revenue"] = monthly["total_revenue"].round(2)
save_csv(monthly, "eda_revenue_monthly.csv", "eda_out")
eda_results["monthly"] = monthly

# Revenue trend chart
fig_rev = make_subplots(specs=[[{"secondary_y": True}]])
fig_rev.add_trace(go.Bar(x=monthly["order_month"], y=monthly["order_count"],
                          name="Order Count", opacity=0.4, marker_color="#94a3b8"), secondary_y=False)
fig_rev.add_trace(go.Scatter(x=monthly["order_month"], y=monthly["total_revenue"],
                              name="Total Revenue (BRL)", mode="lines+markers",
                              line=dict(color="#0f172a", width=2.5)), secondary_y=True)
fig_rev.update_layout(title="Monthly Revenue and Order Volume — Olist 2016–2018",
                       xaxis_tickangle=45, plot_bgcolor="white",
                       yaxis=dict(showgrid=False), yaxis2=dict(showgrid=True, gridcolor="#f1f5f9"))
save_chart(fig_rev, "eda_revenue_trend.html")

# 2c. Revenue by category
if items is not None and products is not None:
    items_prod = items.merge(products[["product_id", "category_english"]], on="product_id", how="left")
    items_prod["category_english"] = items_prod["category_english"].fillna("uncategorized")
    category_rev = (
        items_prod.groupby("category_english")
        .agg(total_revenue=("total_items_price", "sum"), order_count=("order_id", "nunique"))
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    category_rev["revenue_share_pct"] = (category_rev["total_revenue"] / category_rev["total_revenue"].sum() * 100).round(2)
    category_rev["cumulative_pct"] = category_rev["revenue_share_pct"].cumsum().round(2)
    category_rev["total_revenue"] = category_rev["total_revenue"].round(2)
    save_csv(category_rev, "eda_revenue_by_category.csv", "eda_out")
    eda_results["category_rev"] = category_rev

    top15_cat = category_rev.head(15)
    fig_cat = px.bar(top15_cat, x="total_revenue", y="category_english",
                     orientation="h", title="Revenue by Product Category — Top 15",
                     labels={"total_revenue": "Revenue (BRL)", "category_english": ""},
                     color="revenue_share_pct", color_continuous_scale="Blues",
                     text=top15_cat["revenue_share_pct"].map(lambda x: f"{x:.1f}%"))
    fig_cat.update_layout(yaxis=dict(autorange="reversed"), plot_bgcolor="white",
                           coloraxis_showscale=False)
    save_chart(fig_cat, "eda_revenue_by_category.html")

# 2d. Geography
geo = (
    master.groupby("customer_state")
    .agg(
        customer_count=("customer_unique_id", "nunique"),
        order_count=("order_id", "count"),
        total_revenue=("total_payment_value", "sum"),
        avg_order_value=("total_payment_value", "mean"),
        on_time_rate=("is_late", lambda x: (1 - x.mean()) * 100),
        avg_delivery_days=("delivery_days", "mean"),
        avg_review_score=("review_score", "mean"),
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)
geo["revenue_share_pct"] = (geo["total_revenue"] / geo["total_revenue"].sum() * 100).round(2)
geo = geo.round(2)
save_csv(geo, "eda_geography.csv", "eda_out")
eda_results["geo"] = geo

# 2e. Customer behaviour
customer_orders = (
    master.groupby("customer_unique_id")
    .agg(
        order_count=("order_id", "count"),
        total_spend=("total_payment_value", "sum"),
        first_order=("order_purchase_timestamp", "min"),
    )
    .reset_index()
)
customer_orders["customer_type"] = np.where(customer_orders["order_count"] > 1, "returning", "new")
save_csv(customer_orders, "eda_customer_behaviour.csv", "eda_out")
eda_results["customer_orders"] = customer_orders

# 2f. Delivery performance by state
delivery_state = (
    master.groupby("customer_state")
    .agg(
        total_orders=("order_id", "count"),
        on_time_orders=("is_late", lambda x: (x == 0).sum()),
        avg_delivery_days=("delivery_days", "mean"),
        avg_days_variance=("days_early_or_late", "mean") if "days_early_or_late" in master.columns else ("delivery_days", "mean"),
    )
    .reset_index()
)
delivery_state["on_time_rate_pct"] = (delivery_state["on_time_orders"] / delivery_state["total_orders"] * 100).round(2)
delivery_state["avg_delivery_days"] = delivery_state["avg_delivery_days"].round(1)
delivery_state["delivery_rank"] = delivery_state["on_time_rate_pct"].rank(ascending=False).astype(int)
save_csv(delivery_state, "eda_delivery_by_state.csv", "eda_out")
eda_results["delivery_state"] = delivery_state

# 2g. Delivery vs satisfaction
bins = [0, 7, 14, 21, 30, float("inf")]
labels = ["0–7 days", "8–14 days", "15–21 days", "22–30 days", "30+ days"]
master["delivery_bucket"] = pd.cut(master["delivery_days"], bins=bins, labels=labels)
delivery_sat = (
    master.groupby("delivery_bucket", observed=True)
    .agg(
        avg_review_score=("review_score", "mean"),
        order_count=("order_id", "count"),
        negative_review_rate=("review_score", lambda x: (x <= 2).mean() * 100),
    )
    .reset_index()
    .round(2)
)
save_csv(delivery_sat, "eda_delivery_vs_satisfaction.csv", "eda_out")
eda_results["delivery_sat"] = delivery_sat

# Delivery vs satisfaction chart
fig_delsat = px.bar(delivery_sat, x="delivery_bucket", y="avg_review_score",
                    color="avg_review_score", color_continuous_scale="RdYlGn",
                    range_color=[1, 5], text="avg_review_score",
                    title="Delivery Speed vs Average Review Score")
fig_delsat.add_hline(y=BENCHMARKS["avg_review_score"], line_dash="dash",
                      annotation_text=f"Target: {BENCHMARKS['avg_review_score']}")
fig_delsat.update_layout(plot_bgcolor="white", coloraxis_showscale=False)
save_chart(fig_delsat, "eda_delivery_vs_satisfaction.html")

# ── STEP 3: OUTLIER DETECTION ────────────────────────────────────────────────

log("STEP 3 — OUTLIER DETECTION", section=True)

outlier_numeric_cols = [c for c in [
    "total_payment_value", "delivery_days", "review_score",
    "item_count", "total_items_price", "total_freight"
] if c in master.columns]

outlier_report = []
all_outlier_flags = pd.DataFrame(index=master.index)

for col in outlier_numeric_cols:
    series = master[col].dropna()

    if OUTLIER_METHOD == "iqr":
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - OUTLIER_IQR_MULTIPLIER * IQR
        upper = Q3 + OUTLIER_IQR_MULTIPLIER * IQR
        method_label = f"IQR ×{OUTLIER_IQR_MULTIPLIER}"
    else:
        z = np.abs(stats.zscore(series))
        lower = series.mean() - OUTLIER_ZSCORE_THRESHOLD * series.std()
        upper = series.mean() + OUTLIER_ZSCORE_THRESHOLD * series.std()
        method_label = f"Z-score >{OUTLIER_ZSCORE_THRESHOLD}"

    flag_col = f"outlier_{col}"
    all_outlier_flags[flag_col] = (
        (master[col] < lower) | (master[col] > upper)
    ).astype(int)

    n_outliers = all_outlier_flags[flag_col].sum()
    pct_outliers = n_outliers / len(master) * 100

    outlier_report.append({
        "column": col,
        "method": method_label,
        "lower_bound": round(lower, 2),
        "upper_bound": round(upper, 2),
        "outlier_count": int(n_outliers),
        "outlier_pct": round(pct_outliers, 2),
        "min_value": round(series.min(), 2),
        "max_value": round(series.max(), 2),
        "plain_english": (
            f"{n_outliers:,} orders ({pct_outliers:.1f}%) have {col.replace('_', ' ')} "
            f"outside the normal range of {round(lower,1)} to {round(upper,1)}"
        )
    })
    log(f"{col}: {n_outliers:,} outliers ({pct_outliers:.1f}%) — range [{round(lower,1)}, {round(upper,1)}]")

outlier_df = pd.DataFrame(outlier_report)
save_csv(outlier_df, "outlier_report.csv", "eda_out")

# Save flagged outlier rows for analyst review
outlier_flags_joined = master.join(all_outlier_flags)
any_outlier = all_outlier_flags.any(axis=1)
flagged_rows = outlier_flags_joined[any_outlier]
save_csv(flagged_rows, "outlier_flagged_rows.csv", "eda_out")
log(f"Total rows flagged as outlier on at least one column: {len(flagged_rows):,}")

# Outlier visualisation — box plots
fig_box = make_subplots(rows=2, cols=3,
    subplot_titles=[c.replace("_", " ").title() for c in outlier_numeric_cols[:6]])
for i, col in enumerate(outlier_numeric_cols[:6]):
    row, col_pos = divmod(i, 3)
    fig_box.add_trace(
        go.Box(y=master[col].dropna(), name=col.replace("_", " "),
               boxpoints="outliers", marker_color="#0f172a"),
        row=row+1, col=col_pos+1
    )
fig_box.update_layout(title="Outlier Distribution — All Numeric Columns",
                       showlegend=False, plot_bgcolor="white")
save_chart(fig_box, "outlier_boxplots.html")

# ── STEP 4: KPI CALCULATION ──────────────────────────────────────────────────

log("STEP 4 — KPI CALCULATION", section=True)

os.makedirs(PATHS["kpi_out"], exist_ok=True)

# KPI 1 — Revenue monthly
kpi_revenue = monthly.copy()
kpi_revenue.columns = ["year_month", "total_revenue_brl", "order_count",
                        "avg_order_value_brl", "revenue_mom_pct"]
save_csv(kpi_revenue, "kpi_revenue_monthly.csv")

kpi_revenue_summary = pd.DataFrame([{
    "grand_total_revenue_brl":  round(master["total_payment_value"].sum(), 2),
    "grand_total_orders":       len(master),
    "overall_avg_order_value":  round(master["total_payment_value"].mean(), 2),
    "best_revenue_month":       monthly.loc[monthly["total_revenue"].idxmax(), "order_month"],
    "worst_revenue_month":      monthly.loc[monthly["total_revenue"].idxmin(), "order_month"],
    "revenue_growth_rate_pct":  round(
        (monthly["total_revenue"].iloc[-1] - monthly["total_revenue"].iloc[0])
        / monthly["total_revenue"].iloc[0] * 100, 2
    ),
}])
save_csv(kpi_revenue_summary, "kpi_revenue_summary.csv")
log(f"Total revenue: BRL {kpi_revenue_summary['grand_total_revenue_brl'].iloc[0]:,.2f}")

# KPI 2 — Delivery performance monthly
kpi_delivery_monthly = (
    master.groupby("order_month")
    .agg(
        total_orders=("order_id", "count"),
        on_time_orders=("is_late", lambda x: (x == 0).sum()),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
    )
    .reset_index()
    .sort_values("order_month")
)
kpi_delivery_monthly["on_time_rate_pct"] = (
    kpi_delivery_monthly["on_time_orders"] / kpi_delivery_monthly["total_orders"] * 100
).round(2)
kpi_delivery_monthly["avg_delivery_days"] = kpi_delivery_monthly["avg_delivery_days"].round(1)
save_csv(kpi_delivery_monthly, "kpi_delivery_monthly.csv")
save_csv(delivery_state.rename(columns={"customer_state": "state"}),
         "kpi_delivery_by_state.csv")

overall_on_time = round((master["is_late"] == 0).mean() * 100, 2)
overall_avg_delivery = round(master["delivery_days"].mean(), 1)
kpi_delivery_summary = pd.DataFrame([{
    "overall_on_time_rate_pct":  overall_on_time,
    "overall_avg_delivery_days": overall_avg_delivery,
    "benchmark_on_time_pct":     BENCHMARKS["on_time_rate_pct"],
    "vs_benchmark":              round(overall_on_time - BENCHMARKS["on_time_rate_pct"], 2),
    "best_state":                delivery_state.loc[delivery_state["on_time_rate_pct"].idxmax(), "customer_state"],
    "worst_state":               delivery_state.loc[delivery_state["on_time_rate_pct"].idxmin(), "customer_state"],
}])
save_csv(kpi_delivery_summary, "kpi_delivery_summary.csv")
log(f"On-time delivery rate: {overall_on_time}% (benchmark: {BENCHMARKS['on_time_rate_pct']}%)")

# KPI 3 — Satisfaction monthly
kpi_satisfaction_monthly = (
    master.groupby("order_month")
    .agg(
        avg_review_score=("review_score", "mean"),
        count_reviews=("review_score", "count"),
        negative_review_rate=("review_score", lambda x: (x <= 2).mean() * 100),
    )
    .reset_index()
    .sort_values("order_month")
    .round(2)
)
save_csv(kpi_satisfaction_monthly, "kpi_satisfaction_monthly.csv")

on_time_score  = round(master[master["is_late"] == 0]["review_score"].mean(), 2)
late_score     = round(master[master["is_late"] == 1]["review_score"].mean(), 2)
kpi_satisfaction_summary = pd.DataFrame([{
    "overall_avg_review_score":  round(master["review_score"].mean(), 2),
    "overall_negative_rate_pct": round((master["review_score"] <= 2).mean() * 100, 2),
    "score_when_on_time":        on_time_score,
    "score_when_late":           late_score,
    "lateness_score_penalty":    round(on_time_score - late_score, 2),
    "benchmark_review_score":    BENCHMARKS["avg_review_score"],
}])
save_csv(kpi_satisfaction_summary, "kpi_satisfaction_summary.csv")
log(f"Avg review score: {kpi_satisfaction_summary['overall_avg_review_score'].iloc[0]} "
    f"(penalty from late delivery: -{kpi_satisfaction_summary['lateness_score_penalty'].iloc[0]} stars)")

# KPI 4 — Customer retention
new_customers       = (customer_orders["customer_type"] == "new").sum()
returning_customers = (customer_orders["customer_type"] == "returning").sum()
total_customers     = len(customer_orders)
repeat_rate         = round(returning_customers / total_customers * 100, 2)

avg_rev_new       = round(customer_orders[customer_orders["customer_type"] == "new"]["total_spend"].mean(), 2)
avg_rev_returning = round(customer_orders[customer_orders["customer_type"] == "returning"]["total_spend"].mean(), 2)

# What-if: if repeat rate reached 10%
target_repeat_rate    = 10.0
additional_returning  = int((target_repeat_rate / 100 * total_customers) - returning_customers)
projected_revenue_uplift = round(additional_returning * avg_rev_returning, 2)

kpi_retention_summary = pd.DataFrame([{
    "total_unique_customers":       total_customers,
    "new_customers":                int(new_customers),
    "returning_customers":          int(returning_customers),
    "repeat_purchase_rate_pct":     repeat_rate,
    "avg_revenue_new_customer":     avg_rev_new,
    "avg_revenue_returning_customer": avg_rev_returning,
    "revenue_uplift_per_returning": round(avg_rev_returning - avg_rev_new, 2),
    "whatif_target_repeat_rate_pct": target_repeat_rate,
    "whatif_additional_returning":  additional_returning,
    "whatif_revenue_uplift_brl":    projected_revenue_uplift,
    "note": "PROJECTION — not from source data",
}])
save_csv(kpi_retention_summary, "kpi_retention_summary.csv")
log(f"Repeat customer rate: {repeat_rate}% "
    f"(if 10%: +BRL {projected_revenue_uplift:,.0f} projected revenue — PROJECTION)")

# KPI 5 — Revenue by category (if items available)
if "category_rev" in eda_results:
    save_csv(eda_results["category_rev"], "kpi_revenue_by_category.csv")

# KPI Master Dashboard — one row, all headline KPIs
kpi_master = pd.DataFrame([{
    # Revenue
    "total_revenue_brl":            kpi_revenue_summary["grand_total_revenue_brl"].iloc[0],
    "total_orders":                 kpi_revenue_summary["grand_total_orders"].iloc[0],
    "avg_order_value_brl":          kpi_revenue_summary["overall_avg_order_value"].iloc[0],
    "revenue_growth_rate_pct":      kpi_revenue_summary["revenue_growth_rate_pct"].iloc[0],
    "best_revenue_month":           kpi_revenue_summary["best_revenue_month"].iloc[0],
    # Customers
    "total_unique_customers":       kpi_retention_summary["total_unique_customers"].iloc[0],
    "repeat_purchase_rate_pct":     kpi_retention_summary["repeat_purchase_rate_pct"].iloc[0],
    "avg_revenue_per_customer":     round(master["total_payment_value"].sum() / total_customers, 2),
    # Operations
    "on_time_delivery_rate_pct":    kpi_delivery_summary["overall_on_time_rate_pct"].iloc[0],
    "avg_delivery_days":            kpi_delivery_summary["overall_avg_delivery_days"].iloc[0],
    "worst_delivery_state":         kpi_delivery_summary["worst_state"].iloc[0],
    "late_delivery_rate_pct":       round(100 - kpi_delivery_summary["overall_on_time_rate_pct"].iloc[0], 2),
    # Satisfaction
    "overall_avg_review_score":     kpi_satisfaction_summary["overall_avg_review_score"].iloc[0],
    "negative_review_rate_pct":     kpi_satisfaction_summary["overall_negative_rate_pct"].iloc[0],
    "lateness_score_penalty_stars": kpi_satisfaction_summary["lateness_score_penalty"].iloc[0],
}])
save_csv(kpi_master, "KPI_MASTER_DASHBOARD.csv")

# ── STEP 5: EXECUTIVE SUMMARY ─────────────────────────────────────────────────

log("STEP 5 — EXECUTIVE SUMMARY", section=True)

top_cat   = eda_results["category_rev"].iloc[0]["category_english"] if "category_rev" in eda_results else "N/A"
top_state = eda_results["geo"].iloc[0]["customer_state"]
top3_rev_share = eda_results["geo"].head(3)["revenue_share_pct"].sum()

summary = f"""
OLIST E-COMMERCE — ANALYSIS AGENT SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*60}

DATASET
  Records analysed:  {len(master):,} delivered orders
  Date range:        {master['order_purchase_timestamp'].min().date()} → {master['order_purchase_timestamp'].max().date()}
  Unique customers:  {total_customers:,}

HEADLINE KPIs
  Total revenue:          BRL {kpi_master['total_revenue_brl'].iloc[0]:>12,.2f}
  Avg order value:        BRL {kpi_master['avg_order_value_brl'].iloc[0]:>12,.2f}
  Total orders:               {kpi_master['total_orders'].iloc[0]:>12,}
  On-time delivery rate:      {kpi_master['on_time_delivery_rate_pct'].iloc[0]:>11.1f}%
  Avg delivery days:          {kpi_master['avg_delivery_days'].iloc[0]:>12.1f}
  Avg review score:           {kpi_master['overall_avg_review_score'].iloc[0]:>12.2f} / 5
  Repeat customer rate:       {kpi_master['repeat_purchase_rate_pct'].iloc[0]:>11.1f}%

KEY FINDINGS
  1. Revenue growth rate of {kpi_master['revenue_growth_rate_pct'].iloc[0]:.1f}% from first to last full month.
     Best month: {kpi_master['best_revenue_month'].iloc[0]}.

  2. On-time delivery rate is {kpi_master['on_time_delivery_rate_pct'].iloc[0]:.1f}% vs {BENCHMARKS['on_time_rate_pct']}% benchmark
     ({'+' if kpi_delivery_summary['vs_benchmark'].iloc[0] >= 0 else ''}{kpi_delivery_summary['vs_benchmark'].iloc[0]:.1f} pp).
     Worst performing state: {kpi_master['worst_delivery_state'].iloc[0]}.

  3. Late delivery costs {kpi_master['lateness_score_penalty_stars'].iloc[0]:.2f} stars on average review score.
     On-time orders score {on_time_score} vs {late_score} for late orders.

  4. Repeat customer rate is {kpi_master['repeat_purchase_rate_pct'].iloc[0]:.1f}% — critically low.
     If raised to 10%: projected +BRL {projected_revenue_uplift:,.0f} additional revenue (PROJECTION).

  5. Top revenue state: {top_state}. Top 3 states = {top3_rev_share:.1f}% of total revenue
     (concentration risk).

OUTLIER FLAGS
"""
for _, row in outlier_df.iterrows():
    if row["outlier_count"] > 0:
        summary += f"  {row['plain_english']}\n"

summary += f"""
OUTPUTS SAVED
  KPI tables:    02_Cleaned_Data/kpi_tables/ ({len(os.listdir(PATHS['kpi_out']))} files)
  EDA outputs:   07_AI_Outputs/ 
  Charts:        07_AI_Outputs/charts/ ({len(os.listdir(PATHS['charts_out']))} files)
{'='*60}
"""

print(summary)

summary_path = os.path.join(PATHS["eda_out"], "agent_executive_summary.md")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)
log(f"Summary saved: agent_executive_summary.md")

log("\nAGENT COMPLETE — All outputs saved.", section=True)
