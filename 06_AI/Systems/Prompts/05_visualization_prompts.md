# PHASE 5 — DATA VISUALIZATION
# Two tracks: Python charts (for analysis and reports) + Power BI (for the client dashboard).
# Run Python track first to validate the story. Then build Power BI using the kpi_tables/ folder.
# ============================================================

---

## PYTHON VISUALIZATION TRACK
## Use these to explore and validate before building the Power BI dashboard.

---

## PROMPT 5.1 — Revenue trend chart (Python)

```
Using 02_Cleaned_data/kpi_tables/kpi_revenue_monthly.csv,
create a professional revenue trend chart in Python.

Chart type: Line chart with bar chart overlay
- Bars: monthly order_count (left Y axis, light color)
- Line: total_revenue (right Y axis, strong color)
- X axis: year_month labels, rotated 45 degrees
- Add a trend line (linear regression line) over the revenue line
- Mark the best month with an annotation label
- Title: "Monthly Revenue and Order Volume — Olist 2016–2018"
- Clean professional style: no gridlines on Y, light horizontal gridlines only

Use matplotlib or plotly. Use plotly if possible — it's interactive.
Generate complete runnable code.
Save the chart to 06_AI/Outputs/Generated_Charts/chart_01_revenue_trend.html (if plotly)
or chart_01_revenue_trend.png (if matplotlib)
```

---

## PROMPT 5.2 — Category revenue bar chart (Python)

```
Using 02_Cleaned_data/kpi_tables/kpi_revenue_by_category.csv,
create a horizontal bar chart of revenue by category.

- Show top 15 categories only
- Bars sorted from highest to lowest revenue (highest at top)
- Color: gradient from strong color (top) to light (bottom) — same color family
- Add revenue value labels at the end of each bar
- Add a vertical line showing the average category revenue
- Add a secondary label showing revenue_share_pct next to the value
- Title: "Revenue by Product Category — Top 15"
- Keep it clean: no chart border, minimal axes

Generate complete runnable code.
Save to 06_AI/Outputs/Generated_Charts/chart_02_revenue_by_category.html
```

---

## PROMPT 5.3 — Delivery performance by state (Python)

```
Using 02_Cleaned_data/kpi_tables/kpi_delivery_by_state.csv,
create two side-by-side charts:

Chart A — Horizontal bar chart:
- Top 15 states by average delivery days (worst to best, worst at top)
- Color bars red if avg_delivery_days > 20, amber if 10–20, green if < 10
- Add the number label on each bar
- Title: "Average Delivery Days by State"

Chart B — Horizontal bar chart:
- Same 15 states, showing on_time_rate (%)
- Color bars red if on_time_rate < 80%, amber if 80–90%, green if > 90%
- Add the % label on each bar
- Title: "On-Time Delivery Rate by State"

Place both charts side by side in one figure.
Add a shared subtitle: "States ranked by delivery performance — Olist 2016–2018"

Generate complete runnable code.
Save to 06_AI/Outputs/Generated_Charts/chart_03_delivery_by_state.html
```

---

## PROMPT 5.4 — Delivery vs satisfaction scatter plot (Python)

```
Using olist_master.csv, create a scatter plot showing the relationship
between delivery time and review score.

- X axis: delivery_days (0 to 60 — exclude extreme outliers above 60)
- Y axis: review_score (1 to 5)
- Plot individual orders as semi-transparent dots (opacity 0.1 — there are 90k points)
- Overlay a LOWESS smoothing curve or binned average line in a strong color
- Add annotations at key delivery day milestones:
  "7 days: avg score X.X" / "14 days: avg score X.X" / "30 days: avg score X.X"
- Add a vertical dashed line at the average delivery time
- Title: "Delivery Speed vs Customer Satisfaction"
- Subtitle: "Each dot = one order. Line shows the average trend."

Generate complete runnable code.
Save to 06_AI/Outputs/Generated_Charts/chart_04_delivery_vs_satisfaction.html
```

---

## PROMPT 5.5 — Customer geography heatmap (Python)

```
Using 02_Cleaned_data/kpi_tables/kpi_delivery_by_state.csv and
the revenue by state data from the EDA, create a Brazil state heatmap.

Use plotly choropleth with Brazil state boundaries (geojson).
The geojson for Brazilian states is available at:
https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson

Create two maps side by side (or as tabs):
Map 1 — Revenue by state: color intensity = total_revenue
Map 2 — Delivery performance by state: color intensity = avg_delivery_days

For each map:
- Use a sequential color scale (light = low, dark = high)
- Add state abbreviation labels
- Add a hover tooltip showing: state name, value, rank
- Title each map clearly

Generate complete runnable code.
Save to 06_AI/Outputs/Generated_Charts/chart_05_brazil_heatmap.html
```

---

## PROMPT 5.6 — Review score distribution (Python)

```
Using 02_Cleaned_data/kpi_tables/kpi_satisfaction_monthly.csv
and the overall satisfaction summary, create two charts:

Chart A — Donut chart:
- Slices: 5 segments (one per score 1–5)
- Color: score 5 = strong green, 4 = light green, 3 = amber, 2 = light red, 1 = strong red
- Label each slice with: score number + count + %
- Center label: overall average score (large, bold)
- Title: "Review Score Distribution"

Chart B — Line chart (monthly trend):
- X axis: year_month
- Y axis: avg_review_score (scale 3.5 to 5.0 — zoom in to show variation)
- Add reference lines at 4.0 (good) and 3.5 (concerning)
- Shade the area below 4.0 in light red
- Title: "Average Review Score Over Time"

Place both charts in one layout.
Generate complete runnable code.
Save to 06_AI/Outputs/Generated_Charts/chart_06_satisfaction_overview.html
```

---

## POWER BI TRACK
## Use these prompts to get AI help building the Power BI dashboard.
## You will paste these into OpenCode while your Power BI file is open
## (requires Power BI MCP or manual copy-paste of DAX/M code).

---

## PROMPT 5.7 — Power BI data model setup instructions

```
I am building a Power BI dashboard for the Olist project.
My data files are all in 02_Cleaned_data/kpi_tables/

Guide me through connecting Power BI to these files:
1. How to connect Power BI to a folder of CSV files
2. Which files to load and which to skip
3. How to set up the relationships between tables in the model view:
   - KPI_MASTER_DASHBOARD (summary — no relationships needed)
   - kpi_revenue_monthly (connect on year_month)
   - kpi_delivery_monthly (connect on year_month)
   - kpi_satisfaction_monthly (connect on year_month)
   - kpi_delivery_by_state (no date connection — state dimension)
   - kpi_revenue_by_category (no date connection — category dimension)
   - kpi_retention_summary (single-row summary — no relationships needed)

Give me step-by-step instructions with screenshots described in text.
Do not write DAX yet — just the connection and model setup.
```

---

## PROMPT 5.8 — Power BI DAX measures

```
I have connected the kpi_tables/ files to Power BI.
Now write the DAX measures I need for the dashboard.

Write complete DAX for each of these measures:

1. Total Revenue = SUM of total_payment_value from kpi_revenue_monthly
2. Total Orders = SUM of order_count from kpi_revenue_monthly
3. Avg Order Value = [Total Revenue] / [Total Orders]
4. On-Time Rate = SUM of on_time_orders / SUM of total_orders from kpi_delivery_monthly (as %)
5. Avg Delivery Days = AVERAGE of avg_delivery_days from kpi_delivery_monthly
6. Avg Review Score = AVERAGE of avg_review_score from kpi_satisfaction_monthly
7. Negative Review Rate = SUM of score_1+score_2 counts / SUM of count_reviews (as %)
8. Repeat Customer Rate = value from kpi_retention_summary[repeat_purchase_rate_pct]
9. Revenue MoM Change % = month-over-month % change in Total Revenue
10. Late Delivery Rate % = 100 minus On-Time Rate

For each measure: write the DAX, explain what it does in one sentence,
and tell me which visual to use it on.
```

---

## PROMPT 5.9 — Power BI dashboard layout plan

```
I am designing the Olist executive dashboard in Power BI.
The dashboard has 3 pages. Give me the layout plan for each page.

PAGE 1 — Executive Overview
- What KPI cards to show (top row)
- What charts to show (main area)
- What slicers/filters to add
- Exact visual types for each element

PAGE 2 — Operations & Delivery
- Focus: delivery performance, state breakdown, bottleneck analysis
- Layout of visuals
- Slicers needed

PAGE 3 — Customer & Satisfaction
- Focus: review scores, delivery vs satisfaction, customer retention
- Layout of visuals
- Slicers needed

For each visual on each page tell me:
- Visual type (card, bar, line, map, table, scatter, donut)
- Data fields to use (exact column names from my kpi_tables files)
- Any conditional formatting to apply (e.g. red if below benchmark)
- Title text

Format this as a clear layout specification I can follow step by step.
```
