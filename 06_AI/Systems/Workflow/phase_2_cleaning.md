# TASKS — PHASE 2: DATA CLEANING
# ============================================================
# SLASH COMMAND: /ba.tasks phase_2
# ============================================================
# PURPOSE: Atomic task list for data cleaning.
# Generated FROM plan.md by /ba.tasks.
# Each task has: input → action → output → verification.
# Execute ONE task at a time. Confirm before moving to next.
# ============================================================
# OPENCODE INSTRUCTIONS:
# 1. Read constitution.md, spec.md, plan.md first
# 2. Find the first task where Status = To do
# 3. Execute only that task
# 4. Verify output matches the verification step
# 5. Mark Status = Done
# 6. Update plan.md P6 session log
# 7. Stop and wait for confirmation
# ============================================================

## PHASE GATE IN
**Prerequisite:** 01_Raw_Data/ contains all ⟨FILL: number⟩ source files
**Verify before starting:** List files in 01_Raw_Data/ and confirm all are present

## PHASE GATE OUT
**This phase is complete when:** ⟨FILL: project slug⟩_master.csv exists in 02_Cleaned_data/
and cleaning_summary_report.md exists in 06_AI/Outputs/Generated_Docs/

---

## T2.1 — Data quality audit

**Status:** To do
**Input:** All files in 01_Raw_Data/
**Action:**
For each file report:
- Row count and column count
- Null/missing values per column (count and %)
- Duplicate row count
- Data type per column
- Any values outside expected range (negatives in numeric fields, impossible dates, etc.)
**Output:** 06_AI/Outputs/Generated_Docs/cleaning_audit.md — formatted summary table
**Verification:** File exists. Contains one section per source table. No ⟨FILL⟩ placeholders remain.

---

## T2.2 — Clean ⟨FILL: central fact table name⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Count values in ⟨FILL: status column⟩ — show distribution
2. Filter to ⟨FILL: target records, e.g. status = 'delivered'⟩
3. Check ⟨FILL: key columns⟩ for nulls — show count per column
4. Flag rows where ⟨FILL: critical column⟩ is null — save flagged rows separately
5. Calculate ⟨FILL: derived column, e.g. delivery_days⟩
6. Flag outliers: ⟨FILL: derived column⟩ below ⟨FILL: min⟩ or above ⟨FILL: max⟩
7. Remove flagged rows from clean output
**Output:** 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
**Verification:** Row count is less than original. No nulls in ⟨FILL: critical columns⟩. ⟨FILL: derived column⟩ column exists.

---

## T2.3 — Clean ⟨FILL: transactions/payments table name⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Count values in ⟨FILL: type column⟩
2. Flag ⟨FILL: value column⟩ = 0 or negative
3. Check for nulls in all columns
4. Aggregate to one row per ⟨FILL: ID column⟩:
   - ⟨FILL: aggregated column 1⟩ = ⟨FILL: formula⟩
   - ⟨FILL: aggregated column 2⟩ = ⟨FILL: formula⟩
5. Verify aggregated row count = unique ⟨FILL: ID column⟩ count
**Output:** 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
**Verification:** One row per ⟨FILL: ID column⟩. No zero or negative ⟨FILL: value column⟩.

---

## T2.4 — Clean ⟨FILL: line items table name⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Check nulls in all columns
2. Flag ⟨FILL: numeric column⟩ = 0 or above ⟨FILL: max threshold⟩
3. Create full clean table (flagged rows removed)
4. Create aggregated table — one row per ⟨FILL: parent ID⟩:
   - ⟨FILL: aggregated columns⟩
**Output:**
- 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
- 02_Cleaned_data/⟨FILL: table name⟩_aggregated.csv
**Verification:** Both files exist. Aggregated row count = unique ⟨FILL: parent ID⟩ count.

---

## T2.5 — Clean ⟨FILL: reference/lookup table name⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Count nulls in ⟨FILL: key categorical column⟩
2. Fill nulls with '⟨FILL: default label⟩'
3. ⟨FILL: join to translation table if applicable — or delete this step⟩
4. Show top 20 values by count after cleaning
**Output:** 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
**Verification:** Zero nulls in ⟨FILL: key categorical column⟩. Translation column exists if applicable.

---

## T2.6 — Clean ⟨FILL: ratings/feedback table name⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Check nulls in ⟨FILL: score column⟩
2. Confirm valid range: ⟨FILL: min⟩ to ⟨FILL: max⟩ — flag outliers
3. Show distribution (count + % per score value)
4. Report % of records with written comment
**Output:** 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
**Verification:** All scores within valid range. Distribution table produced.

---

## T2.7 — Clean ⟨FILL: high-volume/geographic table name⟩
⟨FILL: delete this task entirely if no large reference table exists in the project⟩

**Status:** To do
**Input:** 01_Raw_Data/⟨FILL: filename⟩
**Action:**
1. Count unique ⟨FILL: key field⟩ values
2. Deduplicate — keep first row per ⟨FILL: key field⟩
3. Flag rows outside valid bounds: ⟨FILL: define bounds⟩
4. Remove flagged rows
**Output:** 02_Cleaned_data/⟨FILL: table name⟩_clean.csv
**Verification:** Row count = unique ⟨FILL: key field⟩ count. No values outside bounds.

---

## T2.8 — Build master dataset

**Status:** To do
**Input:** All files in 02_Cleaned_data/ (except kpi_tables/)
**Action:**
Join in this order (from plan.md P1):
1. Start with ⟨FILL: central table⟩_clean.csv
2. Join ⟨FILL: table 2⟩_clean.csv on ⟨FILL: key⟩ → add ⟨FILL: columns⟩
3. Join ⟨FILL: table 3⟩_clean.csv on ⟨FILL: key⟩ → add ⟨FILL: columns⟩
4. Join ⟨FILL: table 4⟩_clean.csv on ⟨FILL: key⟩ → add ⟨FILL: columns⟩
5. Join ⟨FILL: table 5⟩_clean.csv on ⟨FILL: key⟩ → add ⟨FILL: columns⟩
Add derived columns:
- ⟨FILL: derived column 1⟩
- ⟨FILL: derived column 2⟩
- ⟨FILL: derived column 3⟩
**Output:** 02_Cleaned_data/⟨FILL: project slug⟩_master.csv
**Verification:** Row count matches ⟨FILL: central table⟩_clean.csv. All expected columns present. Null count per column shown.

---

## T2.9 — Cleaning summary report

**Status:** To do
**Input:** All cleaned files + cleaning_audit.md
**Action:**
Produce a report containing:
1. Original vs final row counts per table
2. What was removed and why (plain English)
3. What was filled/imputed and why
4. Master dataset summary: rows, columns, date range
5. Remaining data quality issues
6. 3-sentence client-ready status summary
**Output:** 06_AI/Outputs/Generated_Docs/cleaning_summary_report.md
**Verification:** File exists. Contains all 6 sections. No ⟨FILL⟩ placeholders. Numbers match cleaned file row counts.

---
## PHASE COMPLETE CHECKLIST
- [ ] T2.1 — cleaning_audit.md saved
- [ ] T2.2 — ⟨FILL: central table⟩_clean.csv saved
- [ ] T2.3 — ⟨FILL: transactions table⟩_clean.csv saved
- [ ] T2.4 — ⟨FILL: line items table⟩_clean.csv + _aggregated.csv saved
- [ ] T2.5 — ⟨FILL: reference table⟩_clean.csv saved
- [ ] T2.6 — ⟨FILL: ratings table⟩_clean.csv saved
- [ ] T2.7 — ⟨FILL: geographic table⟩_clean.csv saved (if applicable)
- [ ] T2.8 — ⟨FILL: project slug⟩_master.csv saved
- [ ] T2.9 — cleaning_summary_report.md saved
- [ ] plan.md P5 Phase 2 status updated to Done
- [ ] plan.md P6 session log updated
