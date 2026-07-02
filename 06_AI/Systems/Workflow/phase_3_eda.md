# TASKS — PHASE 3: EXPLORATORY DATA ANALYSIS
# ============================================================
# SLASH COMMAND: /ba.tasks phase_3
# ============================================================
# Execute ONE task at a time. Verify output. Confirm. Then next.
# ============================================================

## PHASE GATE IN
**Prerequisite:** ⟨FILL: project slug⟩_master.csv exists in 02_Cleaned_data/
**Verify before starting:** Load master.csv and show row count, column count, date range.

## PHASE GATE OUT
**This phase is complete when:** eda_COMPLETE_SUMMARY.md exists in 06_AI/Outputs/Generated_Insights/

---

## T3.1 — Executive snapshot

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:** Calculate every KPI defined in spec.md S4 as a single summary row.
Show: ⟨FILL: KPI 1⟩, ⟨FILL: KPI 2⟩, ⟨FILL: KPI 3⟩, ⟨FILL: KPI 4⟩, ⟨FILL: KPI 5⟩
One number per KPI. Clean labels. No code shown.
**Output:** 06_AI/Outputs/Generated_Insights/eda_01_executive_snapshot.md
**Verification:** All ⟨FILL: number⟩ KPIs present. Numbers are rounded and labelled. No nulls.

---

## T3.2 — ⟨FILL: primary metric⟩ over time

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Group by ⟨FILL: time period column⟩. Calculate per period:
- ⟨FILL: primary metric⟩ total
- ⟨FILL: count metric⟩
- ⟨FILL: ratio or average metric⟩
- Period-over-period % change
Identify: best period, worst period, overall trend direction, outlier periods.
End with: plain English trend summary (1 sentence) + business implication (1 sentence).
**Output:** 06_AI/Outputs/Generated_Insights/eda_02_⟨FILL: metric slug⟩_over_time.csv + eda_02_⟨FILL: metric slug⟩_analysis.md
**Verification:** Both files saved. CSV has one row per period. MD ends with business implication.

---

## T3.3 — Performance by ⟨FILL: segment, e.g. category / product type / department⟩

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv ⟨FILL: + any join tables needed⟩
**Action:**
Group by ⟨FILL: segment column⟩. Calculate: total ⟨FILL: metric⟩, count, average, % of total.
Rank top ⟨FILL: 10 or 15⟩. Calculate: % of total from top ⟨FILL: 3 or 5⟩.
Identify high-volume/low-value and low-volume/high-value segments.
End with: 3 bullet business implications.
**Output:** 06_AI/Outputs/Generated_Insights/eda_03_by_⟨FILL: segment slug⟩.csv + eda_03_⟨FILL: segment slug⟩_analysis.md
**Verification:** Both files saved. MD contains 3 business implication bullets.

---

## T3.4 — Geographic analysis

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Group by ⟨FILL: geographic column⟩. Calculate: entity count, transaction count, total ⟨FILL: metric⟩, average ⟨FILL: metric⟩, % of total.
Rank top ⟨FILL: 10⟩. Calculate concentration: % of total from top ⟨FILL: 1 or 3⟩ areas.
Flag areas below ⟨FILL: minimum threshold⟩ records.
Answer: where strongest, where opportunity, what is concentration risk.
**Output:** 06_AI/Outputs/Generated_Insights/eda_04_geography.csv + eda_04_geography_analysis.md
**Verification:** Both files saved. MD answers all 3 strategic questions explicitly.

---

## T3.5 — ⟨FILL: entity, e.g. customer / user / client⟩ behaviour

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
For each unique ⟨FILL: entity ID⟩: first activity date, total activity count, total ⟨FILL: value⟩.
Classify: ⟨FILL: one-time label⟩ (1 transaction) vs ⟨FILL: repeat label⟩ (2+).
Calculate: total unique entities, % per class, avg ⟨FILL: value⟩ per class.
Show ⟨FILL: new entity⟩ acquisition by ⟨FILL: time period⟩.
Project: what would ⟨FILL: metric⟩ look like if repeat rate doubled?
**Output:** 06_AI/Outputs/Generated_Insights/eda_05_⟨FILL: entity slug⟩_behaviour.csv + eda_05_⟨FILL: entity slug⟩_analysis.md
**Verification:** Both files saved. Projection clearly labelled as PROJECTION.

---

## T3.6 — Operational performance

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Calculate overall: avg ⟨FILL: operational metric⟩, median, min, max, % meeting benchmark.
Group by ⟨FILL: dimension⟩: avg ⟨FILL: metric⟩, % meeting benchmark, rank.
⟨FILL: if stages exist — break down into Stage 1 / Stage 2 / Stage 3 with avg per stage⟩
Identify: worst 5 ⟨FILL: dimension values⟩, biggest bottleneck.
End with: root cause plain English + who it affects most.
**Output:** 06_AI/Outputs/Generated_Insights/eda_06_operational_performance.csv + eda_06_operational_analysis.md
**Verification:** Both files saved. Bottleneck identified explicitly by name.

---

## T3.7 — ⟨FILL: satisfaction / quality metric⟩ analysis

**Status:** To do
**Input:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Action:**
Overall distribution: count + % per score value, overall average, % negative.
Trend over time: average by ⟨FILL: time period⟩.
By ⟨FILL: segment⟩: average by group — which are worst?
Correlation with ⟨FILL: operational metric from T3.6⟩:
  - Create buckets: ⟨FILL: bucket definitions⟩
  - Avg ⟨FILL: satisfaction metric⟩ per bucket
Impact: avg score when benchmark met vs missed. Difference = cost of poor performance.
**Output:** 06_AI/Outputs/Generated_Insights/eda_07_⟨FILL: metric slug⟩_analysis.csv + eda_07_⟨FILL: metric slug⟩_analysis.md
**Verification:** Both files saved. Correlation table present. Cost of poor performance number stated.

---

## T3.8 — ⟨FILL: partner / seller / supplier⟩ performance
⟨FILL: delete this task entirely if no partner/seller dimension exists⟩

**Status:** To do
**Input:** ⟨FILL: master table + relevant joined tables⟩
**Action:**
Per ⟨FILL: partner ID⟩: total ⟨FILL: revenue/volume⟩, transaction count, avg ⟨FILL: satisfaction⟩, avg ⟨FILL: operational metric⟩, % meeting benchmark.
Rank top ⟨FILL: 20⟩ by ⟨FILL: revenue/volume⟩.
Flag problem ⟨FILL: partners⟩: high volume + low quality.
Flag star ⟨FILL: partners⟩: high revenue + high quality.
**Output:** 06_AI/Outputs/Generated_Insights/eda_08_⟨FILL: partner slug⟩_performance.csv + eda_08_⟨FILL: partner slug⟩_analysis.md
**Verification:** Both files saved. Problem and star lists explicitly named.

---

## T3.9 — EDA complete summary

**Status:** To do
**Input:** All files in 06_AI/Outputs/Generated_Insights/ starting with eda_
**Action:**
Compile into one document:
1. Executive summary: 5–7 headline findings as bullets — CEO-ready, real numbers, 60-second read
2. Key findings by theme (read themes from spec.md S4)
3. Top 5 strategic recommendations — each with: finding + impact + action + priority
4. What we still don't know: 2–3 unanswered questions raised by the data
**Output:** 06_AI/Outputs/Generated_Insights/eda_COMPLETE_SUMMARY.md
**Verification:** File exists. Contains all 4 sections. Every finding cites a number. No ⟨FILL⟩ placeholders.

---

## PHASE COMPLETE CHECKLIST
- [ ] T3.1 — eda_01_executive_snapshot.md saved
- [ ] T3.2 — eda_02_*.csv + .md saved
- [ ] T3.3 — eda_03_*.csv + .md saved
- [ ] T3.4 — eda_04_*.csv + .md saved
- [ ] T3.5 — eda_05_*.csv + .md saved
- [ ] T3.6 — eda_06_*.csv + .md saved
- [ ] T3.7 — eda_07_*.csv + .md saved
- [ ] T3.8 — eda_08_*.csv + .md saved (if applicable)
- [ ] T3.9 — eda_COMPLETE_SUMMARY.md saved
- [ ] plan.md P5 Phase 3 status updated to Done
- [ ] plan.md P6 session log updated
