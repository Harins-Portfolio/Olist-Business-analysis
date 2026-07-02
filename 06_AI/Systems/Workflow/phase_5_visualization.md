# TASKS — PHASE 5: VISUALIZATION
# ============================================================
# SLASH COMMAND: /ba.tasks phase_5
# Execute ONE task at a time. Verify output. Confirm. Then next.
# Python track first. Power BI track second.
# ============================================================

## PHASE GATE IN
**Prerequisite:** KPI_MASTER_DASHBOARD.csv exists in 02_Cleaned_data/kpi_tables/
**Verify before starting:** List all files in kpi_tables/ and confirm all expected files are present.

## PHASE GATE OUT
**This phase is complete when:** All charts in charts/ are saved AND Power BI layout plan is documented.

---

## PYTHON TRACK

## T5.1 — ⟨FILL: primary metric⟩ trend chart

**Status:** To do
**Input:** 02_Cleaned_data/kpi_tables/kpi_⟨FILL: KPI 1 slug⟩_by_period.csv
**Action:**
Chart type: ⟨FILL: combo bar + line / line only / bar only⟩
- Primary element: ⟨FILL: what is plotted, which column, which axis⟩
- Secondary element: ⟨FILL: what is overlaid, or delete if single series⟩
- X axis: ⟨FILL: time period column⟩, labels rotated 45°
- Add linear trend line over ⟨FILL: primary series⟩
- Annotate best and worst period
- Title: "⟨FILL: chart title⟩"
- Style: no chart border, light horizontal gridlines only
Use plotly (preferred) or matplotlib. Generate complete runnable Python code.
**Output:** 06_AI/Outputs/Generated_Charts/chart_01_⟨FILL: metric slug⟩_trend.html
**Verification:** File exists and opens in browser. Title visible. Best/worst annotations present.

---

## T5.2 — ⟨FILL: segment⟩ ranked bar chart

**Status:** To do
**Input:** 02_Cleaned_data/kpi_tables/kpi_⟨FILL: KPI slug⟩_by_⟨FILL: segment⟩.csv
**Action:**
Orientation: ⟨FILL: horizontal or vertical⟩. Top ⟨FILL: 10 or 15⟩ only.
Sort: highest to lowest.
Color: ⟨FILL: single gradient OR conditional — define thresholds⟩
Add value labels on bars. ⟨FILL: add reference line at average/benchmark or delete⟩
Title: "⟨FILL: chart title⟩"
Generate complete runnable Python code.
**Output:** 06_AI/Outputs/Generated_Charts/chart_02_by_⟨FILL: segment slug⟩.html
**Verification:** File exists. Bars sorted. Labels visible. Conditional colors correct if applicable.

---

## T5.3 — Geographic performance chart

**Status:** To do
**Input:** 02_Cleaned_data/kpi_tables/kpi_⟨FILL: geographic KPI slug⟩_by_⟨FILL: geo level⟩.csv
**Action:**
⟨FILL: OPTION A — choropleth map if GeoJSON available:⟩
Use plotly choropleth. GeoJSON: ⟨FILL: URL or file path⟩
Color = ⟨FILL: KPI column⟩. Hover: ⟨FILL: geographic name, value, rank⟩.
⟨FILL: OPTION B — ranked bar chart if GeoJSON not available:⟩
Horizontal bar, sorted by ⟨FILL: KPI column⟩. Conditional colors: ⟨FILL: thresholds⟩.
Title: "⟨FILL: chart title⟩"
Generate complete runnable Python code.
**Output:** 06_AI/Outputs/Generated_Charts/chart_03_geographic.html
**Verification:** File exists. Geographic areas labelled. Hover or bar labels present.

---

## T5.4 — ⟨FILL: variable A⟩ vs ⟨FILL: variable B⟩ correlation chart

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
⟨FILL: OPTION A — scatter plot for large datasets:⟩
X: ⟨FILL: variable A⟩ limited to ⟨FILL: range⟩. Y: ⟨FILL: variable B⟩.
Semi-transparent dots (opacity ⟨FILL: 0.05–0.2⟩). Smoothing curve overlaid.
Annotate ⟨FILL: 2–3 reference points⟩. Reference line at avg ⟨FILL: variable A⟩.
⟨FILL: OPTION B — binned average chart for cleaner exec output:⟩
Buckets: ⟨FILL: bucket definitions⟩. Avg ⟨FILL: variable B⟩ per bucket.
Bar or line chart. Bucket labels on X axis.
Title: "⟨FILL: variable A⟩ vs ⟨FILL: variable B⟩"
Subtitle: "⟨FILL: plain English description of what the chart shows⟩"
Generate complete runnable Python code.
**Output:** 06_AI/Outputs/Generated_Charts/chart_04_⟨FILL: var A slug⟩_vs_⟨FILL: var B slug⟩.html
**Verification:** File exists. Trend visible. Reference points or bucket labels present.

---

## T5.5 — ⟨FILL: satisfaction / quality metric⟩ overview chart

**Status:** To do
**Input:** 02_Cleaned_data/kpi_tables/kpi_⟨FILL: satisfaction KPI slug⟩_by_period.csv
**Action:**
Chart A — distribution: ⟨FILL: donut or stacked bar⟩
Segments: ⟨FILL: define segments and colors⟩. Labels: value + count + %.
⟨FILL: center label showing overall average⟩
Chart B — trend: line chart over time.
Y axis zoomed to show variation. Reference lines at ⟨FILL: good⟩ and ⟨FILL: concerning⟩ thresholds.
⟨FILL: shade area below concerning threshold in light red⟩
Place A and B side by side in one layout.
Generate complete runnable Python code.
**Output:** 06_AI/Outputs/Generated_Charts/chart_05_⟨FILL: metric slug⟩_overview.html
**Verification:** File exists. Both charts visible. Reference lines present.

---

## T5.6 — Additional chart (if applicable)
⟨FILL: describe additional chart or delete this task entirely⟩

**Status:** To do
**Output:** 06_AI/Outputs/Generated_Charts/chart_06_⟨FILL: slug⟩.html

---

## POWER BI TRACK

## T5.7 — Power BI data model setup

**Status:** To do
**Input:** 02_Cleaned_data/kpi_tables/ (all files)
**Action:**
Produce step-by-step instructions for:
1. Connecting Power BI to the kpi_tables/ folder
2. Which files to load and which to skip
3. Relationship setup in model view — every join defined:
   ⟨FILL: table A joins table B on column X — specify each relationship⟩
   ⟨FILL: note tables with no relationships⟩
**Output:** Instructions shown in chat — no file saved (manual Power BI steps)
**Verification:** Analyst confirms connections and relationships are set up in Power BI before T5.8.

---

## T5.8 — Power BI DAX measures

**Status:** To do
**Input:** spec.md S4 (KPI list) + kpi_tables/ column names
**Action:**
Write complete DAX for each KPI:
- ⟨FILL: KPI 1⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 2⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 3⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 4⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 5⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 6⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 7⟩ = ⟨FILL: DAX formula hint⟩
- ⟨FILL: KPI 8⟩ = ⟨FILL: DAX formula hint⟩
- Period-over-period % change for ⟨FILL: primary KPI⟩
For each: DAX formula + plain English explanation + recommended visual type.
**Output:** Instructions shown in chat — analyst pastes into Power BI
**Verification:** Analyst confirms all measures return correct values vs KPI_MASTER_DASHBOARD.csv.

---

## T5.9 — Power BI dashboard layout plan

**Status:** To do
**Input:** spec.md S3 (user stories) + spec.md S4 (business questions)
**Action:**
Define layout for ⟨FILL: number⟩ dashboard pages.
For each page:
- Page name and purpose
- Which business questions (from spec.md S4) it answers
- KPI cards (top row): which KPIs, which measure
- Main visuals: visual type + data fields + title
- Conditional formatting rules
- Slicer/filter options
**Output:** 06_AI/Outputs/Generated_Docs/⟨FILL: project slug⟩_powerbi_layout_plan.md
**Verification:** File exists. Every business question from spec.md S4 is covered by at least one visual.

---

## PHASE COMPLETE CHECKLIST
- [ ] T5.1 — chart_01_*.html saved
- [ ] T5.2 — chart_02_*.html saved
- [ ] T5.3 — chart_03_geographic.html saved
- [ ] T5.4 — chart_04_*.html saved
- [ ] T5.5 — chart_05_*.html saved
- [ ] T5.6 — chart_06_*.html saved (if applicable)
- [ ] T5.7 — Power BI connections confirmed by analyst
- [ ] T5.8 — DAX measures confirmed by analyst
- [ ] T5.9 — powerbi_layout_plan.md saved
- [ ] plan.md P5 Phase 5 status updated to Done
- [ ] plan.md P6 session log updated
