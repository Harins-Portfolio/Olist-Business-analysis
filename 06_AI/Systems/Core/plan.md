# PLAN.MD
# ============================================================
# SLASH COMMAND: /ba.plan
# ============================================================
# PURPOSE: Define HOW we are building it.
# This file is generated FROM spec.md.
# It contains the data model, tool decisions, folder structure,
# phase sequence, and decisions log.
# task/ files are generated FROM this file.
# ============================================================
# OPENCODE INSTRUCTIONS:
# When /ba.plan is run:
# 1. Read constitution.md
# 2. Read spec.md — this is your source of truth
# 3. Read CLAUDE.md Section 3 for the data model
# 4. Fill every ⟨FILL: ...⟩ — do not leave any placeholders
# 5. Confirm with the analyst before generating tasks/
# ============================================================

---

## P1 — DATA MODEL

### Source tables

⟨FILL: copy from CLAUDE.md Section 3 — full table inventory⟩

| Table | Rows | Key columns | Role in analysis |
|---|---|---|---|
| ⟨FILL⟩ | ⟨FILL⟩ | ⟨FILL⟩ | ⟨FILL: central fact / dimension / lookup⟩ |

### Join map

⟨FILL: describe every join relationship in plain English
e.g. "orders → customers via customer_id (many-to-one)"⟩

### Master table definition

**File name:** ⟨FILL: project slug⟩_master.csv
**Built from:** ⟨FILL: list every table that joins into the master⟩
**Row grain:** ⟨FILL: what does one row represent? e.g. "one delivered order"⟩
**Key derived columns:**
- ⟨FILL: derived column name⟩ = ⟨FILL: formula in plain English⟩
- ⟨FILL: derived column name⟩ = ⟨FILL: formula⟩

---

## P2 — TOOL DECISIONS

| Task | Tool | Reason |
|---|---|---|
| Data cleaning | ⟨FILL: Excel/Power Query or Python⟩ | ⟨FILL: why⟩ |
| Data joining | ⟨FILL: Python/SQL⟩ | ⟨FILL: why⟩ |
| KPI calculation | ⟨FILL: Python/SQL⟩ | ⟨FILL: why⟩ |
| Charts | ⟨FILL: Python — plotly/matplotlib⟩ | ⟨FILL: why⟩ |
| Dashboard | ⟨FILL: Power BI⟩ | ⟨FILL: why⟩ |
| Reports | ⟨FILL: Markdown → PDF or Word⟩ | ⟨FILL: why⟩ |

---

## P3 — FOLDER STRUCTURE & FILE MAP

Every output file is defined here before it exists.
OpenCode saves to these exact paths — no exceptions.

```
Project BA Olist/
│
├── 00_Context/
│   ├── CURRENT_STATUS.md
│   ├── NEXT_TASK.md
│   ├── PROJECT_MAP.md
│   ├── README.md
│   └── ROADMAP.md
│
├── 01_Raw_Data/
│   └── ⟨FILL: list every source file⟩
│
├── 02_Cleaned_data/
│   ├── ⟨FILL: list every cleaned file, e.g. orders_clean.csv⟩
│   └── kpi_tables/
│       ├── ⟨FILL: list every KPI table file⟩
│       └── KPI_MASTER_DASHBOARD.csv
│
├── 03_SQL/
│   └── ⟨FILL: list SQL files if applicable⟩
│
├── 04_Python/
│   ├── ⟨FILL: list Python scripts⟩
│   └── files/
│       └── ⟨FILL: list Python dependency files⟩
│
├── 05_Power_Bi/
│   └── ⟨FILL: dashboard filename⟩.pbix
│
├── 06_AI/
│   ├── Outputs/
│   │   ├── Generated_Charts/
│   │   │   └── ⟨FILL: list all chart files⟩
│   │   ├── Generated_DAX/
│   │   │   └── ⟨FILL: list DAX output files⟩
│   │   ├── Generated_Docs/
│   │   │   ├── cleaning_audit.md
│   │   │   ├── cleaning_summary_report.md
│   │   │   ├── storytelling_narrative_arc.md
│   │   │   ├── presentation_script.md
│   │   │   ├── qa_talking_points.md
│   │   │   └── project_completion_checklist.md
│   │   ├── Generated_Insights/
│   │   │   ├── eda_01_executive_snapshot.md
│   │   │   ├── ⟨FILL: list all eda_ output files⟩
│   │   │   └── eda_COMPLETE_SUMMARY.md
│   │   ├── Generated_Python/
│   │   │   └── ⟨FILL: list generated Python files⟩
│   │   ├── Generated_SQL/
│   │   │   └── ⟨FILL: list generated SQL files⟩
│   │   └── Scratchpad/
│   │       └── ⟨FILL: list intermediate/temp files⟩
│   └── Systems/
│       ├── Core/
│       │   ├── constitution.md
│       │   ├── spec.md
│       │   ├── plan.md
│       │   └── PROJECT_SPEC_OLIST.md
│       ├── Prompts/
│       │   ├── 00_INDEX.md
│       │   ├── 02_cleaning_prompts.md
│       │   ├── 03_eda_prompts.md
│       │   ├── 04_kpi_prompts.md
│       │   ├── 05_visualization_prompts.md
│       │   ├── 06_storytelling_prompts.md
│       │   ├── CLAUDE_OLIST.md
│       │   └── README.md
│       ├── Semantics/
│       │   └── ⟨FILL: list semantic files⟩
│       └── Workflow/
│           ├── phase_2_cleaning.md
│           ├── phase_3_eda.md
│           ├── phase_4_kpis.md
│           ├── phase_5_visualization.md
│           └── phase_6_storytelling.md
│
├── 07_Reports/
│   ├── ⟨FILL: project slug⟩_executive_summary.md
│   └── ⟨FILL: project slug⟩_recommendations_report.md
│
├── 08_Documentation/
│   ├── KPIs.md
│   └── business_questions.md
│
└── 09_Analysis/
    └── ⟨FILL: list analysis output files⟩
```

---

## P4 — DECISIONS LOG

Every analytical decision made during this project.
Read this before every session. Never re-question a logged decision.
To change a decision: update this log, then update affected task files.

| Date | Decision | Reason | Who |
|---|---|---|---|
| ⟨FILL⟩ | ⟨FILL: e.g. Filter to completed transactions only⟩ | ⟨FILL: reason⟩ | ⟨FILL: analyst/client⟩ |
| ⟨FILL⟩ | ⟨FILL⟩ | ⟨FILL⟩ | ⟨FILL⟩ |

---

## P5 — PHASE SEQUENCE

Phases run in order. A phase cannot start until the previous phase output is verified.

| Phase | Name | Input | Output | Task file | Status |
|---|---|---|---|---|---|
| 2 | Data Cleaning | 01_Raw_Data/ | 02_Cleaned_data/ + master.csv | tasks/phase_2_cleaning.md | ⟨FILL⟩ |
| 3 | EDA | master.csv | 06_AI/Outputs/Generated_Insights/eda_*.md+.csv | tasks/phase_3_eda.md | ⟨FILL⟩ |
| 4 | KPI Calculation | master.csv | kpi_tables/*.csv | tasks/phase_4_kpis.md | ⟨FILL⟩ |
| 5 | Visualization | kpi_tables/ | charts/ + .pbix | tasks/phase_5_visualization.md | ⟨FILL⟩ |
| 6 | Storytelling | eda_COMPLETE_SUMMARY.md + KPI_MASTER_DASHBOARD.csv | 07_Reports/ | tasks/phase_6_storytelling.md | ⟨FILL⟩ |

### Phase gate rules
- Phase 3 cannot start until: master.csv exists and cleaning_summary_report.md is saved
- Phase 4 cannot start until: eda_COMPLETE_SUMMARY.md is saved
- Phase 5 cannot start until: KPI_MASTER_DASHBOARD.csv is saved
- Phase 6 cannot start until: all charts in charts/ are saved and .pbix layout is planned

---

## P6 — SESSION LOG

One entry per work session. Keeps continuity between days and chat sessions.

| Date | Phase | Completed | Next task |
|---|---|---|---|
| ⟨FILL⟩ | ⟨FILL⟩ | ⟨FILL: what was done⟩ | ⟨FILL: exact next task ID, e.g. "T2.3"⟩ |

---
*Generated by /ba.plan from spec.md — update P4 and P6 during project*
*To change approach: update this file, then re-run /ba.tasks for affected phases*
