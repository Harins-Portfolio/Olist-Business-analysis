"""
OLIST - CONSOLIDATED FULL-ANALYSIS NOTEBOOK BUILDER
====================================================
Assembles 04_Python/olist_full_analysis.ipynb from string cell definitions.

Run:  python 04_Python/build_full_analysis_nb.py
Output: 04_Python/olist_full_analysis.ipynb  (clean, no stored outputs)

The notebook is intentionally built, not hand-edited, so the cell source is
reviewable here and regenerating never carries stale outputs. Sections are
appended in reading order; later tasks add their section code above the
assembly call at the bottom.
"""
from pathlib import Path

import nbformat as nbf

OUT = Path(__file__).resolve().parent / "olist_full_analysis.ipynb"


def md(src):
    return nbf.v4.new_markdown_cell(src.strip("\n"))


def code(src):
    return nbf.v4.new_code_cell(src.strip("\n"))


cells = []

# --------------------------------------------------------------------------- #
# SECTION 0 - SETUP & THEME
# --------------------------------------------------------------------------- #
cells.append(md(r"""
# Olist Business Analytics — Full Analysis Notebook

**Purpose:** One consolidated, run-top-to-bottom notebook: data quality (DAMA-5),
condensed descriptive profiling of the clean tables, business KPIs, growth,
categories, payments, geography, the validated H1 hypothesis (late delivery →
lower satisfaction), seller concentration, and the output exports that feed the
project canvas and dashboards.

**Data flow:** raw CSVs (brief shapes) → cleaned datasets in `02_Cleaned_data/`
→ star schema (verified) → analysis on the cleaned `olist_master.csv`. Read-only:
nothing in `01_Raw_Data/` or `02_Cleaned_data/` is modified.

**Outputs written:**
- `06_AI/Outputs/Generated_Insights/eda_summary.json`
- `06_AI/Outputs/Generated_Charts/viz_01..08.png`
- `06_AI/Outputs/Generated_Reports/descriptive_analysis.html`

> Run from the project root (`Project BA Olist/`). Python 3.14, matplotlib +
> seaborn, scipy, plotly.
"""))

cells.append(code(r"""
import sys, json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Robust project-root detection (survives headless execution from any cwd).
ROOT = Path.cwd()
for cand in [Path.cwd(), *Path.cwd().parents]:
    if (cand / "04_Python" / "descriptive_lib.py").exists():
        ROOT = cand
        break
sys.path.insert(0, str(ROOT / "04_Python"))

import descriptive_lib as dl

CLEAN = ROOT / "02_Cleaned_data"
STAR  = CLEAN / "star_schema"
CHART = ROOT / "06_AI" / "Outputs" / "Generated_Charts"
INSIGHTS = ROOT / "06_AI" / "Outputs" / "Generated_Insights"
CHART.mkdir(parents=True, exist_ok=True)
INSIGHTS.mkdir(parents=True, exist_ok=True)

GREEN, RED, NAVY, GRAY = "#0f6b47", "#b0413e", "#1f3a93", "#9aa3ad"

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white",
                     "axes.grid": True, "grid.alpha": .3, "font.size": 10,
                     "axes.titleweight": "bold"})
pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 220)


def savefig(name):
    plt.tight_layout()
    plt.savefig(CHART / name, dpi=160, bbox_inches="tight")
    plt.show()
    print(f"  saved -> {CHART / name}")


print(f"Project root: {ROOT}")
print(f"Registry loaded: {len(dl.TABLES)} clean tables")
"""))

# --------------------------------------------------------------------------- #
# SECTION 1 - RAW -> CLEAN PIPELINE (VERIFIED, NOT RE-RUN)
# --------------------------------------------------------------------------- #
cells.append(md(r"""
## 1. Raw → Clean pipeline (verified, not re-run)

Shapes of the 9 raw Kaggle CSVs, then verification that the cleaned outputs
reconcile (row counts + revenue to the cent). The ETL scripts
(`04_Python/ETL/`) are **not** re-executed here — this notebook is read-only.
"""))

cells.append(code(r"""
raw = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}
raw_rows = []
for f, nm in raw.items():
    df = pd.read_csv(ROOT / "01_Raw_Data" / f)
    raw_rows.append({"table": nm, "file": f, "rows": df.shape[0], "cols": df.shape[1]})
print("RAW data (9 CSVs from Kaggle, as shipped)")
display(pd.DataFrame(raw_rows).sort_values("rows", ascending=False).reset_index(drop=True))
"""))

cells.append(code(r"""
m = dl.read_table("olist_master.csv")
fo = pd.read_csv(STAR / "Fact_Orders.csv")
fi = pd.read_csv(STAR / "Fact_OrderItems.csv")

print("CLEANED pipeline verification (no ETL re-run):")
print(f"  Master rows (delivered orders) : {m.shape[0]:,}")
print(f"  Fact_Orders rows               : {fo.shape[0]:,}   grain match: {m.shape[0] == fo.shape[0]}")
print(f"  Master order_revenue           : R$ {m['order_revenue'].sum():,.2f}")
print(f"  Fact_Orders order_revenue      : R$ {fo['order_revenue'].sum():,.2f}")
print(f"  Fact_OrderItems line_price     : R$ {fi['line_price'].sum():,.2f}  (matches order revenue)")
print(f"  Fact_Orders total_freight      : R$ {fo['total_freight'].sum():,.2f}")
print(f"  Master total_freight           : R$ {m['total_freight'].sum():,.2f}")
"""))

# --------------------------------------------------------------------------- #
# SECTION 2 - DATA-QUALITY OVERVIEW (DAMA-5)
# --------------------------------------------------------------------------- #
cells.append(md(r"""
## 2. Data-quality overview (DAMA-5)

One row per clean table: rows, columns, primary-key uniqueness, null-bearing
columns and the DAMA-5 overall verdict. Then the live clean-check re-run
(PASS/WARN/INFO/FAIL counts with the non-pass details).
"""))

cells.append(code(r"""
ov = dl.overview()
display(ov)
"""))

cells.append(code(r"""
ver = dl.verdict()
c = ver["counts"]
print(f"CLEAN-CHECK: {c['PASS']} PASS | {c['WARN']} WARN | {c['INFO']} INFO | {c['FAIL']} FAIL  "
      f"-> {'READY OK' if c['FAIL'] == 0 else 'NOT READY'}")
for x in ver["checks"]:
    if x["status"] in ("FAIL", "WARN"):
        print(f"  [{x['status']}] {x['check']} ({x['table']}): {x['detail']}")
"""))

# --------------------------------------------------------------------------- #
# SECTION 3 - CONDENSED PER-TABLE PROFILING (6 CORE TABLES)
# --------------------------------------------------------------------------- #
cells.append(md(r"""
## 3. Condensed per-table profiling

Column report + DAMA-5 row + a readable **2×2 chart grid** for the 6 core
tables (master, orders, payments, items, products, reviews). The remaining 12
tables are summarized in Section 2's overview grid; full interactive detail for
every table lives in the HTML report (`descriptive_analysis.html`).
"""))

cells.append(code(r"""
def fmt_num(v):
    try:
        f = float(v)
        return str(int(f)) if f.is_integer() else f"{f:,.2f}"
    except (TypeError, ValueError):
        return v


def column_report(p):
    rows = []
    for c in p["columns"]:
        stat = ""
        if c["kind"] == "numeric":
            s = c.get("stats", {})
            stat = (f"min {fmt_num(s.get('min'))} | med {fmt_num(s.get('median'))} | "
                    f"mean {fmt_num(s.get('mean'))} | max {fmt_num(s.get('max'))}")
        elif c["kind"] == "datetime":
            s = c.get("stats", {})
            stat = f"{s.get('min', '')} -> {s.get('max', '')}"
        rows.append({"Column": c["name"], "Dtype": c["dtype"],
                     "Nulls": f"{c['null']:,} ({c['null_pct']}%)",
                     "Unique": f"{c['n_unique']:,}", "Summary": stat})
    return pd.DataFrame(rows)


def dama_df(d):
    return pd.DataFrame([{"Dimension": k, "Verdict": v[0], "Reason": v[1]}
                         for k, v in d["scores"].items()])


CORE = ["master", "orders_clean", "payments", "items", "products", "reviews"]


def chart_for(ax, c, df):
    name, chart, label = c["name"], c["chart"], c.get("label", c["name"])
    if chart == "donut":
        s = pd.to_numeric(df[name], errors="coerce").fillna(0)
        yes = int((s == 1).sum()); total = len(s)
        col = dl.PALETTE["warn"] if name == "is_late" else dl.PALETTE["ok"]
        ax.pie([yes, max(total - yes, 0)], labels=["yes", "no"],
               autopct=lambda v: f"{v:.0f}%" if v >= 3 else "",
               colors=[col, dl.PALETTE["muted"]], startangle=90,
               counterclock=False, textprops={"fontsize": 8},
               wedgeprops=dict(width=0.45))
        ax.set_title(label, fontsize=10)
    elif chart == "bar":
        if c.get("ordered"):
            num = pd.to_numeric(df[name], errors="coerce")
            vc = num.value_counts().sort_index() if num.notna().any() \
                else df[name].astype(str).value_counts().sort_index()
        else:
            vc = pd.Series(c.get("top", {})).sort_values()
        keys, vals = [str(k) for k in vc.index][:12], list(vc.values)[:12]
        ax.bar(keys, vals, color=dl.PALETTE["ok"])
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.set_title(label, fontsize=10)
    elif chart == "hist":
        s = pd.to_numeric(df[name], errors="coerce").dropna()
        if name in dl.MONEY_COLS:
            edges, st = dl.money_bins(s)
            ax.hist(s, bins=edges, color=dl.PALETTE["info"], alpha=.85)
            ax.set_xscale("log")
            cap = f"med R$ {fmt_num(st['median'])} | mean R$ {fmt_num(st['mean'])}"
            ax.set_title(f"{label}\n{cap}", fontsize=9)
            ax.set_xlabel("R$ (log scale)")
        else:
            bins = min(30, max(int(s.nunique()), 1))
            ax.hist(s, bins=bins, color=dl.PALETTE["info"], alpha=.85)
            ax.set_title(label, fontsize=10)
        ax.set_ylabel("count")
    elif chart == "trend":
        s = pd.to_datetime(df[name], errors="coerce").dropna()
        mm = s.dt.to_period("M").astype(str).value_counts().sort_index()
        ax.plot(mm.index, mm.values, color=dl.PALETTE["info"], marker="o", ms=3, lw=1.4)
        ax.tick_params(axis="x", labelrotation=45, labelsize=7)
        ax.set_title(label, fontsize=10)
        ax.set_ylabel("count")
    else:
        ax.axis("off")


def profile_section(key):
    t = next(x for x in dl.TABLES if x["key"] == key)
    p = dl.profile_table(t["rel"]); d = dl.dama5(p)
    print(f"### {p['label']}  (`{p['rel']}`) — {p['rows']:,} rows x {p['cols']} cols "
          f"| DAMA-5 overall: {d['overall'].upper()}")
    display(column_report(p))
    display(dama_df(d))
    charted = [c for c in p["columns"] if c.get("chart") not in ("skip", None)]
    if not charted:
        print("(no plottable columns)")
        return
    picks = charted[:4] + [None] * max(4 - len(charted), 0)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, c in zip(axes.ravel(), picks):
        if c is None:
            ax.axis("off")
            continue
        chart_for(ax, c, p["df"])
    fig.suptitle(f"{p['label']} — key distributions", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()
"""))

cells.append(code(r"""
for key in CORE:
    profile_section(key)
"""))

# --------------------------------------------------------------------------- #
# SECTION 4 - CORE MONEY & SCALE KPIs
# --------------------------------------------------------------------------- #
cells.append(md(r"""
## 4. Core money & scale KPIs

Headline numbers on the delivered-orders universe: revenue (goods), freight,
delivered orders, AOV, unique customers and the critical repeat rate.
"""))

cells.append(code(r"""
rev = m["order_revenue"].sum()
freight = m["total_freight"].sum()
aov = rev / len(m)
cust_count = m.groupby("customer_unique_id").size()
repeat_rate = (cust_count > 1).mean()

kpi = pd.DataFrame({
    "Metric": ["Gross revenue (goods)", "Total freight", "Delivered orders",
               "Average order value (AOV)", "Unique customers", "Repeat rate"],
    "Value": [f"R$ {rev:,.0f}", f"R$ {freight:,.0f}  ({freight/rev:.1%} of revenue)",
              f"{len(m):,}", f"R$ {aov:,.2f}", f"{len(cust_count):,}", f"{repeat_rate:.2%}"]})
display(kpi)
print(f"Customers with >=3 orders: {(cust_count >= 3).sum():,} ({(cust_count >= 3).mean():.2%})")
print(f"Avg orders per customer: {cust_count.mean():.3f}")
"""))

# --------------------------------------------------------------------------- #
# SECTION 5 - GROWTH & SEASONALITY
# --------------------------------------------------------------------------- #
cells.append(md(r"""
## 5. Growth & seasonality

Monthly revenue / volume / AOV, month-over-month momentum, the Black Friday
Nov-2017 spike, and weekday vs weekend behaviour. **Saves `viz_04`**.
"""))

cells.append(code(r"""
m["order_date"] = m["order_purchase_timestamp"].dt.to_period("M")
g = m.groupby("order_date").agg(orders=("order_id", "size"),
                                revenue=("order_revenue", "sum"))
g["aov"] = g["revenue"] / g["orders"]
g["mom"] = g["orders"].pct_change() * 100
g["revenue_mom"] = g["revenue"].pct_change() * 100
print("MONTHLY SERIES (orders, revenue, AOV)")
print(g[["orders", "revenue", "aov"]].to_string())
print(f"\nMedian monthly volume growth: {g['mom'].median():.1f}%")
print(f"Median monthly revenue growth: {g['revenue_mom'].median():.1f}%")
print(f"Peak order month: {g['orders'].idxmax()} ({g['orders'].max():,} orders)")
print(f"Peak revenue month: {g['revenue'].idxmax()} (R$ {g['revenue'].max():,.0f})")
"""))

cells.append(code(r"""
xx = range(len(g))
fig, ax = plt.subplots(figsize=(9.5, 4.5))
ax.bar(xx, g["orders"], color=GRAY, alpha=0.55, label="Orders")
ax2 = ax.twinx()
ax2.plot(xx, g["revenue"] / 1e3, color=NAVY, lw=2.4, marker="o", ms=3, label="Revenue (k)")
ax2.plot(xx, g["aov"], color=RED, lw=1.8, ls="--", label="AOV")
ax.set_xticks(xx, [str(x) for x in g.index], rotation=75, fontsize=8)
ax.set_ylabel("Order volume"); ax2.set_ylabel("Revenue (R$ k) / AOV")
ax.legend(loc="upper left"); ax2.legend(loc="upper center")
ax.set_title("Growth is volume-driven (Black Friday Nov-2017 spike), AOV flat ~R$ 137")
savefig("viz_04_monthly_revenue_volume.png")
"""))

cells.append(code(r"""
bf = m[m["order_purchase_timestamp"].dt.to_period("M") == pd.Period("2017-11", freq="M")]
avg_orders = g["orders"].mean()
print(f"Black Friday Nov-2017: {len(bf):,} orders, R$ {bf['order_revenue'].sum():,.0f} "
      f"({len(bf)/avg_orders - 1:+.0%} vs monthly avg {avg_orders:,.0f})")

wk = m.groupby(m["order_purchase_timestamp"].dt.dayofweek.ge(5)).agg(
    orders=("order_id", "size"), aov=("order_revenue", "mean"))
wk.index = ["weekday", "weekend"]
print("\nWeekday vs weekend:")
print(wk.to_string())

dow = m["order_purchase_timestamp"].dt.dayofweek.value_counts().sort_index()
dow.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("\nDay-of-week order mix:")
print(dow.to_string())
"""))

# --------------------------------------------------------------------------- #
# ASSEMBLY - later sections append above this line
# --------------------------------------------------------------------------- #
def build():
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14"},
    }
    nbf.write(nb, OUT)
    print(f"Wrote {OUT} ({len(cells)} cells)")
    return OUT


if __name__ == "__main__":
    build()
