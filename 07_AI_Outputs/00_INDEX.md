# OLIST PROJECT — PROMPT LIBRARY INDEX
# ============================================================
# This folder contains all AI prompts for the Olist BA project.
# Copy prompts one at a time into OpenCode. Never run two at once.
# Save every output before running the next prompt.
# ============================================================

## HOW TO USE THIS LIBRARY

1. Know which phase you are in (check CLAUDE.md Section 6)
2. Open the matching prompt file below
3. Copy ONE prompt at a time into OpenCode
4. Wait for the full output before copying the next
5. If an output looks wrong, run the prompt again with a correction note appended
6. Never skip a numbered prompt — they build on each other

---

## FILE MAP

| File | Phase | Prompts | What it produces |
|---|---|---|---|
| 02_cleaning_prompts.md | Phase 2 | 2.1 – 2.9 | Cleaned tables + master dataset |
| 03_eda_prompts.md | Phase 3 | 3.1 – 3.9 | Analysis outputs + EDA summary |
| 04_kpi_prompts.md | Phase 4 | 4.0 – 4.6 | KPI tables for Power BI |
| 05_visualization_prompts.md | Phase 5 | 5.1 – 5.9 | Charts (Python) + PBI dashboard |
| 06_storytelling_prompts.md | Phase 6 | 6.1 – 6.6 | Reports + presentation script |

---

## CURRENT STATUS

- [ ] Phase 2 — Data Cleaning (IN PROGRESS)
- [ ] Phase 3 — EDA
- [ ] Phase 4 — KPI Calculation
- [ ] Phase 5 — Visualization
- [ ] Phase 6 — Storytelling

Update the checkboxes above as you complete each phase.

---

## QUICK REFERENCE — WHERE TO START

Just finished data cleaning in Power Query?
→ Open 02_cleaning_prompts.md, start at PROMPT 2.8 (master join)

Starting EDA for the first time?
→ Open 03_eda_prompts.md, start at PROMPT 3.1

Ready to build Power BI?
→ Complete all of Phase 4 first (kpi_tables/ must exist)
→ Then open 05_visualization_prompts.md at PROMPT 5.7

---

## REUSE NOTE

These prompts are Olist-specific in their table names and column references.
To reuse for a future project:
1. Copy this entire prompts/ folder to your new project
2. Replace table names and column names with your new project's names
3. Update the business questions and KPI definitions
4. The structure, flow, and output format stay exactly the same
