# TASKS — PHASE 6: STORYTELLING & RECOMMENDATIONS
# ============================================================
# SLASH COMMAND: /ba.tasks phase_6
# Execute ONE task at a time. Verify output. Confirm. Then next.
# ============================================================

## PHASE GATE IN
**Prerequisites:**
- eda_COMPLETE_SUMMARY.md exists in 06_AI/Outputs/Generated_Insights/
- KPI_MASTER_DASHBOARD.csv exists in 02_Cleaned_data/kpi_tables/
- All charts saved in 06_AI/Outputs/Generated_Charts/
**Verify before starting:** Read eda_COMPLETE_SUMMARY.md and KPI_MASTER_DASHBOARD.csv before any task.

## PHASE GATE OUT
**This phase is complete when:** All files in the Phase Complete Checklist below exist.

---

## T6.1 — Narrative arc

**Status:** To do
**Input:** 06_AI/Outputs/Generated_Insights/eda_COMPLETE_SUMMARY.md + 02_Cleaned_data/kpi_tables/KPI_MASTER_DASHBOARD.csv
**Action:**
Build 3-part narrative:
PART 1 — WHERE WE ARE (2–3 sentences):
Describe ⟨FILL: client/company⟩ snapshot using real numbers. Scale, trend, context.
PART 2 — WHAT WE FOUND (3–4 sentences — one per major finding):
Lead with highest-impact finding. State as fact not discovery.
Format: [insight] — [financial or operational implication].
PART 3 — WHAT TO DO (3 bullets):
Format: [specific action] → [expected result] → [timeframe].
Language rules from constitution.md apply. No hedging. No jargon.
**Output:** 06_AI/Outputs/Generated_Docs/storytelling_narrative_arc.md
**Verification:** File exists. Contains 3 clearly labelled parts. Every claim cites a number.

---

## T6.2 — Executive summary

**Status:** To do
**Input:** eda_COMPLETE_SUMMARY.md + KPI_MASTER_DASHBOARD.csv
**Action:**
One-page document with:
- Header: project name, period, analyst, date
- Business snapshot: ⟨FILL: number⟩ KPI callouts, one line each
- Key findings: 4 bullets, max 2 lines each, number-backed
- Strategic recommendations: 3 bullets, action → outcome format
- Risk flags: 2 bullets
**Output:** 07_Reports/⟨FILL: project slug⟩_executive_summary.md
**Verification:** File in 07_Reports/ (not 06_AI/Outputs/Generated_Docs/). Fits one page when printed. Every finding has a number.

---

## T6.3 — Presentation script

**Status:** To do
**Input:** 06_AI/Outputs/Generated_Docs/storytelling_narrative_arc.md
**Action:**
Write speaker script for ⟨FILL: number⟩-slide, ⟨FILL: total minutes⟩-minute presentation.
One section per slide with: slide name, time allocation, exact words to speak.
Slide structure:
- Slide 1 — Title: ⟨FILL: seconds⟩s — opening framing sentence
- Slide 2 — Snapshot: ⟨FILL: seconds⟩s — headline KPIs, tone guidance
- Slide 3 — ⟨FILL: finding theme 1⟩: ⟨FILL: seconds⟩s — what to point to, what it means
- Slide 4 — ⟨FILL: finding theme 2⟩: ⟨FILL: seconds⟩s — lead with strongest number
- Slide 5 — ⟨FILL: finding theme 3⟩: ⟨FILL: seconds⟩s — connect to financial impact
- Slide ⟨FILL: last⟩ — Recommendations: ⟨FILL: seconds⟩s — close with call to action
Words to say — not bullet points. Must sound natural spoken aloud.
**Output:** 06_AI/Outputs/Generated_Docs/presentation_script.md
**Verification:** File exists. One section per slide. Time allocations add up to ⟨FILL: total minutes⟩ minutes.

---

## T6.4 — Full recommendations report

**Status:** To do
**Input:** All 06_AI/Outputs/Generated_Insights/eda_*.md files + KPI_MASTER_DASHBOARD.csv
**Action:**
Formal written report with:
1. Introduction (1 paragraph): who the client is, what was analysed, objective
2. Methodology (1 paragraph): what was done, one sentence per step
3. Key findings — one section per theme from spec.md S4:
   Each section: headline + 2–3 paragraphs with data + callout box "What this means for the business"
4. Strategic recommendations — ⟨FILL: number⟩ recommendations:
   Each: title + problem (with data) + action + expected outcome + success KPI + effort/impact rating
5. Limitations & next steps: what data cannot tell us, suggested next phase
6. Appendix: KPI definitions table
**Output:** 07_Reports/⟨FILL: project slug⟩_recommendations_report.md
**Verification:** File in 07_Reports/. Contains all 6 sections. Every claim cites a number. No hedging language.

---

## T6.5 — Q&A talking points

**Status:** To do
**Input:** eda_COMPLETE_SUMMARY.md + KPI_MASTER_DASHBOARD.csv
**Action:**
Prepare talking points for the ⟨FILL: number, e.g. 10⟩ most likely executive questions.
For each question:
- The question (executive voice)
- Ideal answer: 2–4 sentences, number-backed
- The number to cite: exact value from KPI_MASTER_DASHBOARD.csv
- What NOT to say: overreach or claim the data doesn't support
Must include at minimum:
- One question challenging data quality or methodology
- One question asking for ROI or financial projection
- One question about what to prioritise first
- One question about missing analysis
- One question about competitive comparison
**Output:** 06_AI/Outputs/Generated_Docs/qa_talking_points.md
**Verification:** File exists. ⟨FILL: number⟩ questions covered. Every answer cites a KPI value.

---

## T6.6 — Project completion checklist

**Status:** To do
**Input:** All project folders
**Action:**
List every expected file per folder. For each: name + contents + phase + status (exists/missing).
Generate completion scorecard: X of Y files per phase, overall %.
For missing files: identify which task ID to re-run.
**Output:** 06_AI/Outputs/Generated_Docs/project_completion_checklist.md
**Verification:** File exists. Scorecard present. Missing files (if any) linked to task IDs.

---

## PHASE COMPLETE CHECKLIST
- [ ] T6.1 — storytelling_narrative_arc.md saved to 06_AI/Outputs/Generated_Docs/
- [ ] T6.2 — ⟨FILL: slug⟩_executive_summary.md saved to 07_Reports/
- [ ] T6.3 — presentation_script.md saved to 06_AI/Outputs/Generated_Docs/
- [ ] T6.4 — ⟨FILL: slug⟩_recommendations_report.md saved to 07_Reports/
- [ ] T6.5 — qa_talking_points.md saved to 06_AI/Outputs/Generated_Docs/
- [ ] T6.6 — project_completion_checklist.md saved to 06_AI/Outputs/Generated_Docs/
- [ ] plan.md P5 Phase 6 status updated to Done
- [ ] plan.md P6 session log updated
- [ ] Project status in spec.md S1 updated to Complete
