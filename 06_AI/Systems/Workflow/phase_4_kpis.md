# TASKS — PHASE 4: KPI CALCULATION
# ============================================================
# SLASH COMMAND: /ba.tasks phase_4
# Execute ONE task at a time. Verify output. Confirm. Then next.
# ============================================================

## PHASE GATE IN
**Prerequisite:** eda_COMPLETE_SUMMARY.md exists in 06_AI/Outputs/Generated_Insights/
**Verify before starting:** Confirm 02_Cleaned_data/kpi_tables/ folder exists (run T4.0 first)

## PHASE GATE OUT
**This phase is complete when:** KPI_MASTER_DASHBOARD.csv exists in 02_Cleaned_data/kpi_tables/

---

## T4.0 — Create kpi_tables folder

**Status:** To do
**Input:** None
**Action:** Create folder 02_Cleaned_data/kpi_tables/ if it does not exist.
**Output:** Empty folder at 02_Cleaned_data/kpi_tables/
**Verification:** Folder exists.

---

## T4.1 — KPI table: ⟨FILL: KPI 1 name from spec.md S4⟩

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Create periodic table (one row per ⟨FILL: time period⟩):
- ⟨FILL: time period column⟩
- ⟨FILL: KPI 1⟩ = ⟨FILL: formula⟩
- ⟨FILL: supporting metric⟩ = ⟨FILL: formula⟩
- period_over_period_change (%)
Create single-row summary: grand total, best period, worst period, overall growth rate.
**Output:**
- 02_Cleaned_data/kpi_tables/kpi_⟨FILL: KPI 1 slug⟩_by_period.csv
- 02_Cleaned_data/kpi_tables/kpi_⟨FILL: KPI 1 slug⟩_summary.csv
**Verification:** Both files exist. One row per period in periodic table. Summary has one row.

---

## T4.2 — KPI table: ⟨FILL: KPI 2 name⟩

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Create periodic table + ⟨FILL: dimension⟩-level table + single-row summary.
Benchmark check: is ⟨FILL: KPI 2⟩ above or below ⟨FILL: target from spec.md S5⟩?
**Output:**
- kpi_tables/kpi_⟨FILL: KPI 2 slug⟩_by_period.csv
- kpi_tables/kpi_⟨FILL: KPI 2 slug⟩_by_⟨FILL: dimension⟩.csv
- kpi_tables/kpi_⟨FILL: KPI 2 slug⟩_summary.csv
**Verification:** All 3 files exist. Benchmark check result stated explicitly.

---

## T4.3 — KPI table: ⟨FILL: KPI 3 name⟩
⟨FILL: same structure as T4.2 — adapt for KPI 3⟩

**Status:** To do
**Input / Action / Output / Verification:** ⟨FILL⟩

---

## T4.4 — KPI table: ⟨FILL: KPI 4 name⟩ + what-if projection

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Build KPI table per T4.2 structure.
Add what-if projection:
  If ⟨FILL: KPI 4⟩ improved from ⟨FILL: current level⟩ to ⟨FILL: target⟩:
  - Additional ⟨FILL: entities⟩ = ⟨FILL: calculation⟩
  - Additional ⟨FILL: revenue/impact⟩ = ⟨FILL: calculation⟩
Label projection clearly as PROJECTION — not from source data.
**Output:** kpi_tables/kpi_⟨FILL: KPI 4 slug⟩_*.csv
**Verification:** Files exist. Projection is labelled. Numbers are rounded.

---

## T4.5 — T4.6 — KPI tables: ⟨FILL: KPI 5–8 names⟩
⟨FILL: duplicate T4.2 structure for each remaining KPI. Delete unused blocks.⟩

---

## T4.7 — KPI master dashboard file

**Status:** To do
**Input:** All files in 02_Cleaned_data/kpi_tables/
**Action:**
Build one-row summary pulling the headline value for each KPI from its summary file.
Group columns by theme (from spec.md S4):
- ⟨FILL: THEME 1⟩: ⟨FILL: KPI column names⟩
- ⟨FILL: THEME 2⟩: ⟨FILL: KPI column names⟩
- ⟨FILL: THEME 3⟩: ⟨FILL: KPI column names⟩
- ⟨FILL: THEME 4⟩: ⟨FILL: KPI column names⟩
**Output:** 02_Cleaned_data/kpi_tables/KPI_MASTER_DASHBOARD.csv
**Verification:** File exists. One row. ⟨FILL: number⟩ columns — one per KPI. No nulls.

---

## PHASE COMPLETE CHECKLIST
- [ ] T4.0 — kpi_tables/ folder exists
- [ ] T4.1 — kpi_⟨FILL: KPI 1 slug⟩_*.csv files saved
- [ ] T4.2 — kpi_⟨FILL: KPI 2 slug⟩_*.csv files saved
- [ ] T4.3 — kpi_⟨FILL: KPI 3 slug⟩_*.csv files saved
- [ ] T4.4 — kpi_⟨FILL: KPI 4 slug⟩_*.csv files saved (with projection)
- [ ] T4.5 — remaining KPI files saved
- [ ] T4.7 — KPI_MASTER_DASHBOARD.csv saved
- [ ] plan.md P5 Phase 4 status updated to Done
- [ ] plan.md P6 session log updated
