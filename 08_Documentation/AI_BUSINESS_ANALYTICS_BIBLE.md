# THE AI BUSINESS ANALYTICS BIBLE
## Your Step-by-Step Operating Manual — Zero to Executive Deliverable

---

> **What this document is:** the single file you open at the start of every new project. It tells you exactly what to do, in what order, using which file from your existing system. It does not teach you statistics or analytics theory — it orchestrates the AI tools, prompts, and agent you have already built.
>
> **What this document is not:** a new set of prompts. Every prompt, template, and script referenced here already exists in your `BA_Projects` system. This file is the map that tells you which door to open and when.
>
> **How to use it:** read top to bottom the first time to understand the full arc. After that, treat it as a checklist — find your current phase, follow the steps, check the boxes, move on.

---

## YOUR SYSTEM AT A GLANCE

Before Phase 0, understand the four layers you've already built. Every step in this bible points back to one of these.

| Layer | What it is | Where it lives |
|---|---|---|
| **CLAUDE.md** | Your project's identity — who the client is, what the data is, your rules, your KPIs | Project root |
| **Systems/** | Your SpecKit-style execution plan — constitution, spec, plan, prompts, and workflow tasks | `06_AI/Systems/` |
| **Prompts** | Copy-paste prompts for every phase of analysis | `06_AI/Systems/Prompts/` |
| **Python Agent** | One script that runs EDA, outlier detection, and KPI calculation automatically | `04_Python/` |

These four layers talk to each other in one direction:

```
CLAUDE.md  →  spec.md  →  plan.md  →  Workflow/phase_*.md  →  Prompts/*.md  →  Python Agent  →  Deliverables
(who/what)    (why)        (how)       (atomic steps)         (exact wording)   (automation)    (client files)
```

You never skip a layer. You never improvise outside it. That discipline is what makes this a system instead of a series of one-off conversations with AI.

---
# PHASE 0 — BUSINESS UNDERSTANDING & PROJECT DEFINITION

## Goal

Turn a vague client request into a structured business problem and an AI-readable project definition before touching a single dataset.

## Why this matters

This is the highest ROI phase in the project. Every dashboard, KPI, SQL query, Python analysis, and recommendation depends on correctly understanding the business problem first.

AI is extremely good at analysing data, but it cannot determine whether it is solving the right problem unless you provide the business context.

Every hour invested here prevents days of unnecessary analysis later.

This phase separates an analyst who produces charts from a consultant who solves business problems.

---

## Steps

### 1. Have the business conversation before opening any tools.

Ask questions such as:

- What decision are we trying to support?
- Why is this analysis needed now?
- Who will use the results?
- What does success look like?
- What are the biggest business concerns?
- What assumptions already exist?
- What would make this project a success?

Write everything in plain language before touching any data.

---

### 2. Create the project folder using your standard project structure.

```
Project_Name/

01_Raw_Data/
02_Cleaned_Data/
03_SQL/
04_Python/
05_Power_BI/
06_AI/
07_Reports/
08_Documentation/
09_Specify/
README.md
```

---

### 3. Build the business context.

Complete:

- business_questions.md
- KPIs.md
- PROJECT_SPEC.md
- semantic_layer.json
- CLAUDE.md
- constitution.md
- spec.md
- plan.md

These documents become the project's memory and provide context to every AI tool throughout the project.

---

### 4. Define the semantic layer.

Document:

- Business entities
- KPIs
- Metrics
- Dimensions
- Business terminology
- Relationships
- Calculation rules

The semantic layer allows AI to understand the business rather than simply the database.

---

### 5. Validate the project scope.

Confirm:

- Business objective
- Deliverables
- Timeline
- Assumptions
- Constraints
- Success criteria
- Out-of-scope items

Nothing else should begin until these are approved.

---

## Validation checklist

☐ Business problem is clearly defined

☐ Success criteria are measurable

☐ KPIs are documented

☐ Business questions are complete

☐ Semantic layer exists

☐ CLAUDE.md contains no placeholders

☐ Project specification is approved

☐ AI has enough context to understand the project

---

## Common mistakes

Beginning analysis before understanding the business problem.

Creating dashboards without defining KPIs first.

Skipping the semantic layer and expecting AI to understand company terminology.

Allowing project scope to change without updating the documentation.

Confusing business questions with technical questions.

---

## You're ready for Phase 1 when:

The business problem is completely understood, the documentation is finished, and every AI tool has enough context to understand both the company and the project before any data is analysed.

---

## PHASE 1 — PROJECT INTAKE

### Goal
Turn a vague client request into a structured, AI-readable project definition before touching any data.

### Why this matters
Every hour spent here saves ten hours later. An AI that doesn't know the business problem will analyze the wrong things confidently. This phase is what separates a freelancer who "does data stuff" from a consultant who solves business problems.

### Steps

**1. Have the client conversation first — outside any tool.**
Ask: what decision are you trying to make? What happens if you don't get this analysis? What does success look like? Write down their answers in plain language before opening anything.

**2. Create the project folder using your standard structure.**
```
ProjectName/
├── 01_Raw_Data/
├── 02_Cleaned_data/
│   └── kpi_tables/
├── 04_Python/
├── 05_Power_Bi/
├── 06_AI/
│   ├── Outputs/
│   │   ├── Generated_Charts/
│   │   ├── Generated_DAX/
│   │   ├── Generated_Docs/
│   │   ├── Generated_Insights/
│   │   ├── Generated_Python/
│   │   ├── Generated_SQL/
│   │   └── Scratchpad/
│   └── Systems/
│       ├── Core/
│       ├── Prompts/
│       ├── Semantics/
│       └── Workflow/
├── 07_Reports/
├── 08_Documentation/
└── 09_Analysis/
```

**3. Copy `CLAUDE_TEMPLATE.md` into the project root. Rename to `CLAUDE.md`.**
Fill it using your `NEW_PROJECT_CHECKLIST.md` — this takes 20–30 minutes. You are answering: who is the client, what's the business model, what data do you have, what are the 12–15 business questions, what are the 8 KPIs.

**4. Copy the `06_AI/Systems/` folder (Core/ with constitution.md, spec.md template, plan.md template; Workflow/ with task templates) into the project.**
Run `/ba.specify` in OpenCode — it reads your fresh CLAUDE.md and fills `spec.md` with the problem statement, scope, user stories, and success criteria.

**5. Approve spec.md, then run `/ba.plan`.**
This fills `plan.md` with the data model, tool decisions, full file map, and phase sequence — generated from spec.md.

**6. Approve plan.md, then run `/ba.tasks`.**
This generates the five atomic task files in `06_AI/Systems/Workflow/` — your execution checklist for the entire project.

### Validation checklist before moving on
- [ ] CLAUDE.md has zero `⟨FILL: ...⟩` placeholders remaining
- [ ] spec.md Section 2 (scope) clearly states what is OUT of scope, not just in
- [ ] plan.md P3 (file map) names every output file before it exists
- [ ] 06_AI/Systems/Workflow/phase_2_cleaning.md exists and references your actual source file names

### Common mistakes
- Skipping straight to data cleaning because "the client is in a hurry" — this guarantees rework
- Leaving business questions vague ("understand the customers better" instead of "what % of customers return within 90 days")
- Not writing down what's out of scope — this is how scope creep eats your margin on a fixed-price project

### You're ready for Phase 1 when:
CLAUDE.md, spec.md, plan.md all exist with no placeholders, and you've read them once start to finish without confusion.

---
## PHASE 2 — POSTGRESQL FOUNDATION & DATA PLATFORM

## Goal

Create a single, trusted source of truth by loading all raw datasets into PostgreSQL before any cleaning, transformation or analysis begins.

## Why this matters

CSV files are excellent for storing data, but they are not a database.

Without a central database, every tool reads data independently, leading to duplicated work, inconsistent calculations and multiple versions of the truth.

PostgreSQL becomes the centre of the analytics workflow.

Every tool — SQL, Python, Power BI and AI — works from exactly the same data source.

This makes the project reproducible, scalable and much easier to maintain.

---

## Steps

### 1. Preserve the raw data.

Copy every source file into:

```
01_Raw_Data/
```

These files should never be modified.

They are the permanent evidence trail for the project.

---

### 2. Create the PostgreSQL database.

Create the project database.

Example:

```
olist
```

Create the initial database schema using:

```
03_SQL/

00_create_schema.sql
```

This defines the database structure before any data is imported.

---

### 3. Load the raw data using Python.

Run the ETL scripts inside:

```
04_Python/

etl/
```

Python is responsible for:

- Reading CSV files
- Importing data into PostgreSQL
- Validating row counts
- Reporting import errors

Python does **not** perform business transformations during this phase.

---

### 4. Validate the imported data.

Confirm:

- Row counts match the source files
- Every table loaded successfully
- Primary keys are present
- Data types imported correctly
- No tables failed during import

Record any issues before moving forward.

---

### 5. Prepare the database for analysis.

The PostgreSQL database now becomes the project's single source of truth.

Every subsequent phase should read data directly from PostgreSQL rather than the original CSV files.

The workflow now becomes:

```
Raw CSV

↓

PostgreSQL

↓

SQL Cleaning

↓

Python Analysis

↓

Power BI

↓

Executive Reports
```

---

## Validation checklist

☐ Every CSV imported successfully

☐ Database schema created

☐ Row counts match the source data

☐ No failed imports

☐ Python ETL completed successfully

☐ PostgreSQL is ready for SQL transformations

---

## Common mistakes

Cleaning CSV files before importing them.

Using multiple copies of the same dataset.

Connecting Power BI directly to raw CSV files.

Importing data without validating row counts.

Using Python to redesign the database instead of simply loading the data.

---

## You're ready for Phase 3 when:

Every raw dataset has been successfully loaded into PostgreSQL, the database accurately reflects the source files, and PostgreSQL is ready to become the single source of truth for all SQL transformations, Python analysis, Power BI dashboards and AI-assisted business analysis.

---


## PHASE 3 — DATA ACQUISITION & VALIDATION

### Goal
Get the raw data into the project and confirm it is what the client said it was — before you trust a single number in it.

### Steps

**1. Drop every raw file into `01_Raw_Data/`. Never modify these files. Ever.**
This folder is your evidence trail. If a client questions a number eight weeks later, you trace it back to an untouched source file.

**2. Open `06_AI/Systems/Workflow/phase_2_cleaning.md`, run Task T2.1 (data quality audit).**
This is the first prompt from your `06_AI/Systems/Prompts/02_cleaning_prompts.md` library. It reports row counts, null percentages, duplicate counts, and data types for every file — before any cleaning happens.

**3. Read the audit output against what the client told you in Phase 0.**
Does the row count match what they said? Are the date ranges what you expected? Flag anything that contradicts the intake conversation — this is often where you discover the client doesn't fully understand their own data.

### Validation checklist
- [ ] `cleaning_audit.md` exists in `06_AI/Outputs/`
- [ ] Every file the client mentioned in Phase 0 is present in `01_Raw_Data/`
- [ ] No surprises between what the client said and what the audit shows — or surprises are documented in plan.md's decisions log

### Common mistakes
- Cleaning data before auditing it — you fix problems you haven't fully identified yet
- Not flagging client expectation mismatches early, when they're cheap to resolve

### You're ready for Phase 2 when:
The audit is complete and any data surprises have been discussed with the client or logged as a decision.

---

## PHASE 4 — DATA CLEANING & PREPARATION

### Goal
Transform raw, messy source files into one trustworthy master dataset that every later phase builds on.

### Why this is the highest-leverage phase
Every KPI, every chart, every recommendation traces back to this master file. An error here propagates silently through your entire deliverable. This is where consulting-grade work is actually won or lost — not in the visualization.

### Steps

**1. Open `06_AI/Systems/Prompts/02_cleaning_prompts.md`. Work through Tasks 2.2 through 2.7 in order — one table at a time.**
Each prompt cleans one source table: handles nulls, flags outliers, fixes data types, deduplicates. Copy one prompt into OpenCode, review the output, confirm it before moving to the next.

**2. Run Task 2.8 — the master join.**
This is the single most important prompt in your entire library. It joins every cleaned table into one flat file using the data model you defined in `plan.md P1`. This master file is what every subsequent phase reads from.

**3. Run Task 2.9 — the cleaning summary report.**
This produces a plain-English document explaining what was removed, what was filled, and why — your audit trail and your first piece of client-facing communication.

**4. Update `06_AI/Systems/Core/plan.md` Section P4 (decisions log) with every cleaning decision you made.**
Which records were excluded? Why? This prevents you — or anyone picking up the project later — from re-litigating settled decisions.

### Validation checklist
- [ ] Every file in `02_Cleaned_data/` has zero unexplained nulls in key columns
- [ ] The master dataset row count makes sense given what was filtered out
- [ ] `cleaning_summary_report.md` exists and you could hand it to the client as-is
- [ ] Every cleaning decision is logged in plan.md

### Common mistakes
- Deleting outliers instead of flagging them — sometimes the outlier is the most interesting finding in the dataset
- Joining tables before checking for duplicate keys — this silently inflates your row counts and every KPI built on them
- Not running the agent's outlier detection step (covered below) as a second check on manual cleaning

### You're ready for Phase 3 when:
Your master dataset exists, passes the validation checklist, and you trust every number in it enough to put your name on it.

---

## PHASE 5 — EXPLORATORY DATA ANALYSIS (EDA)

### Goal
Understand what the data is actually saying before you calculate a single official KPI — this is where you find the story.

### Two ways to do this phase — use both

**Path A — Automated (fast, comprehensive baseline)**
Run your Python Analysis Agent now. One command (`python [project]_analysis_agent.py`) produces:
- Full numeric summary across every column
- Primary metric trend over time, with chart
- Performance by segment, with chart
- Geographic breakdown
- Entity (customer/user) behaviour classification
- Outlier detection report with flagged rows
- All KPI tables, pre-calculated
- A plain-English executive summary printed to console and saved to file

This gives you a complete first draft of the entire analysis in minutes, not days.

**Path B — Manual / guided (deeper, business-specific)**
Open `06_AI/Systems/Prompts/03_eda_prompts.md` and work through Tasks 3.1 through 3.9 in OpenCode. These prompts go deeper than the agent on the specific business questions from your CLAUDE.md — correlation analysis, satisfaction drivers, seller/partner performance, the "what if" projections.

### Recommended sequence
Run the agent first (Path A) to get oriented fast. Then use the manual prompts (Path B) to dig into whatever the agent's output makes you curious about. The agent gives you breadth; the manual prompts give you depth on the questions that matter most to this specific client.

**Run Task 3.9 last — the EDA complete summary.**
This compiles every finding into one document with 5–7 headline insights, organized by business theme, ending in your top 5 strategic recommendations. This single file becomes the foundation for everything in Phase 6.

### Validation checklist
- [ ] Agent has run successfully and all outputs exist in `06_AI/Outputs/` and `kpi_tables/`
- [ ] `eda_COMPLETE_SUMMARY.md` exists and contains real numbers, not placeholders
- [ ] Every finding could survive the question "how do you know that?" with a specific number as the answer
- [ ] You personally understand and could explain every finding without re-reading it

### Common mistakes
- Trusting the agent's output without reading it — automation accelerates analysis, it doesn't replace your judgment
- Stopping at the first interesting finding instead of working through all 9 prompts — the most valuable insight is often the 7th thing you check, not the 1st
- Writing findings in statistics language instead of business language — "the p-value was 0.03" tells a CEO nothing; "this difference is real, not random chance" does

### You're ready for Phase 4 when:
`eda_COMPLETE_SUMMARY.md` is complete and you could walk into a client meeting right now and talk through the findings confidently.

---

## PHASE 6 — KPI CALCULATION

### Goal
Convert your EDA findings into the official, single-source-of-truth numbers that will appear on every dashboard, report, and slide for the rest of the project.

### Why this is a separate phase from EDA
EDA is exploration — you're allowed to be messy and follow curiosity. KPIs are commitments — once a number is in `KPI_MASTER_DASHBOARD.csv`, every other deliverable references it. This phase is where you lock in the numbers that matter.

### Steps

**1. If you haven't already, your Python Agent already calculated all of this in Phase 3 (Path A).**
Check `02_Cleaned_data/kpi_tables/` — if `KPI_MASTER_DASHBOARD.csv` exists with values for every KPI from CLAUDE.md Section 5, this phase is largely done already.

**2. If any KPI is missing or needs manual refinement, open `06_AI/Systems/Prompts/04_kpi_prompts.md`.**
Work through the relevant prompt for that specific KPI — each one builds a periodic table, a segment breakdown, and a single-row summary, with an explicit benchmark check against the target you defined in CLAUDE.md.

**3. Confirm `KPI_MASTER_DASHBOARD.csv` has one row, one column per KPI, zero nulls.**
This file is the spine of your entire dashboard and report. Every number anyone sees from here forward traces to this one file.

### Validation checklist
- [ ] Every KPI from CLAUDE.md Section 5 has a value in `KPI_MASTER_DASHBOARD.csv`
- [ ] Every KPI has a documented formula — you could explain to a client exactly how each number was calculated
- [ ] Benchmark comparisons are explicit (above/below target, by how much)
- [ ] No KPI value was hand-typed or estimated — every value traces to a calculation against the master dataset

### Common mistakes
- Letting two different files disagree on the same KPI (e.g. revenue calculated slightly differently in two places) — this is the fastest way to lose client trust
- Defining a KPI without a benchmark — a number with no target tells the client nothing about whether it's good or bad

### You're ready for Phase 5 when:
`KPI_MASTER_DASHBOARD.csv` is complete, consistent, and you'd stake your reputation on every number in it.

---

## PHASE 7 — VISUALIZATION

### Goal
Turn validated KPIs and findings into visuals an executive can understand in under 5 seconds per chart.

### Two tracks — run both

**Track A — Python charts (for the written report and presentation)**
Open `06_AI/Systems/Prompts/05_visualization_prompts.md`. Work through Tasks 5.1–5.6 — each produces one interactive Plotly chart saved as `.html`, covering: primary metric trend, segment performance, geography, correlation analysis, and a distribution overview. Then run the KPI scorecard prompt (`kpi_scorecard_prompt.md`) for a styled executive summary table using Great Tables — this is your dashboard-quality scorecard outside of Power BI.

**Track B — Power BI dashboard (for the interactive client deliverable)**
Run Tasks 5.7–5.9. These don't produce files directly — they give you step-by-step instructions for: connecting Power BI to your `kpi_tables/` folder, the exact DAX measures to write for every KPI, and a full page-by-page layout plan mapped to your business questions from CLAUDE.md Section 4.

**Connection note:** connect Power BI directly to the `kpi_tables/` CSV folder via Get Data → Folder, not via the Python script connector. Your agent already does the heavy computation outside Power BI — routing through Python inside Power BI adds fragility and a 30-minute timeout risk for zero benefit.

### Client deliverable note
If the client needs an Excel file rather than (or in addition to) Power BI, use `excel_export_prompt.md` — it builds a polished workbook with Excel formulas (not hardcoded Python values), conditional formatting on KPI status, and native charts, then forces a recalculation check for zero formula errors before delivery.

### Validation checklist
- [ ] Every chart has a clear title, axis labels, and a one-sentence plain-English subtitle
- [ ] Power BI dashboard answers every business question from CLAUDE.md Section 4 — walk through each question against the dashboard to confirm
- [ ] KPI scorecard shows status (met/close/missed) for every KPI, not just the raw value
- [ ] If an Excel deliverable was built, `scripts/recalc.py` shows zero formula errors

### Common mistakes
- Building beautiful charts that don't answer any of the defined business questions — decoration instead of insight
- Using a chart type that requires explanation — if you have to explain how to read it, use a simpler chart
- Forgetting to label units (BRL vs USD, %, days) — ambiguous numbers undermine trust instantly

### You're ready for Phase 6 when:
Every business question from CLAUDE.md has a corresponding visual, and the Power BI dashboard or Excel file could be handed to the client today without further explanation.

---

## PHASE 8 — STORYTELLING & RECOMMENDATIONS

### Goal
Convert analysis into a narrative an executive can act on — this is the phase that justifies your consulting fee.

### Why this phase exists separately from visualization
A chart shows what happened. A story explains why it matters and what to do about it. Executives don't pay for charts — they pay for the judgment that turns a chart into a decision.

### Steps, in order

**1. Run Task 6.1 — the narrative arc.**
Produces the 3-part story structure: where we are, what we found, what to do. This is the spine every other deliverable in this phase builds from.

**2. Run Task 6.2 — the one-page executive summary.**
Your highest-leverage single document. If a CEO only reads one page from the entire project, this is it.

**3. Run Task 6.3 — the presentation script.**
Exact words to say, slide by slide, for your live client meeting. Not bullet points — a real spoken script, timed to your meeting length.

**4. Run Task 6.4 — the full written recommendations report.**
The formal deliverable: introduction, methodology, findings by theme, numbered recommendations with effort/impact ratings, limitations, and a KPI appendix.

**5. If a PDF version is needed, run the PDF executive summary prompt (`pdf_executive_summary_prompt.md`).**
Produces a polished, client-ready PDF using reportlab — cover page, KPI scorecard table, key findings, embedded charts, and recommendations, separate from the longer markdown report.

**6. Run Task 6.5 — Q&A talking points.**
Prepares you for the 10 hardest questions an executive is likely to ask, each with the exact number to cite and what not to overreach into saying.

**7. Run Task 6.6 — the final deliverables checklist.**
A completion scorecard across every phase, flagging any missing file and which task to re-run to produce it.

### Validation checklist
- [ ] Every claim in every document cites a specific number from `KPI_MASTER_DASHBOARD.csv` or `eda_COMPLETE_SUMMARY.md`
- [ ] No hedging language anywhere ("appears to," "seems like," "it could be")
- [ ] Every recommendation has a specific action, an expected outcome, and a way to measure success
- [ ] The Q&A prep includes at least one question that challenges your methodology — be ready to defend it
- [ ] Task 6.6's completion checklist shows 100% across all phases

### Common mistakes
- Burying the most important finding instead of leading with it
- Recommendations that are vague ("improve delivery") instead of specific ("partner with regional carriers in the 5 worst states to cut average delivery time by 20% within 2 quarters")
- Not rehearsing the presentation script out loud before the actual client meeting

### You're ready to deliver when:
Task 6.6's checklist is complete, you've read through every document once as if you were the client seeing it cold, and nothing makes you wince.

---

## THE FULL PROJECT AT A GLANCE

```
PHASE 0   Business Understanding & Project Definition
            → CLAUDE.md + Business Questions + KPIs + Semantic Layer + Project Specification

PHASE 1   Project Intake
            → Project Folder Setup + Requirements Gathering + Scope Definition + Project Plan

PHASE 2   Data Acquisition & Validation
            → 01_Raw_Data/ + Data Quality Audit + Source Validation

PHASE 3   PostgreSQL Foundation & Data Platform
            → Database Schema + Python ETL + PostgreSQL + Import Validation

PHASE 4   Data Cleaning & Preparation
            → SQL Transformations + Clean Tables

PHASE 5   Exploratory Data Analysis (EDA)
            → Python Agent + SQL + AI Insights

PHASE 6   KPI Calculation
            → KPI Tables + KPI_MASTER_DASHBOARD

PHASE 7   Visualization
            → Power BI + Python Charts + Executive Dashboard

PHASE 8   Storytelling & Recommendations
            → Executive Summary + Report + Presentation + AI Documentation
```

Every arrow above is a file your AI system already knows how to produce. Your job across all six phases is judgment, not execution — deciding what matters, validating what the AI produces, and adding the business context only you have from talking to the client.

---

## YOUR GROWTH PATH — FREELANCE TO CONSULTANT

This system handles **descriptive and diagnostic analytics** end to end — what happened, and why. As you grow, two capabilities sit outside this current system and represent your next learning frontier:

**Statistical rigor** — hypothesis testing, confidence intervals, knowing whether a finding is real or just noise. This is what separates "the data shows X" from "we can say with confidence that X is true, not coincidence." Build this skill deliberately, project by project, even before you formalize it into prompts.

**Predictive analytics** — regression, classification, clustering, forecasting. This is what moves you from "here's what happened" to "here's what will happen, and here's how to change it." This is the highest-value skill on your path to solving million-dollar problems, and it's worth dedicated focus once this descriptive/diagnostic system feels automatic.

Everything in this bible is your foundation. Run it enough times that Phases 0–6 become muscle memory — that's what frees up your attention to learn the two skills above without dropping the operational quality you've already built.

---
*This document orchestrates your existing CLAUDE.md, 06_AI/Systems/ framework, prompt library, and Python agent. It does not replace them — it tells you which one to open and when. Read it once fully, then use it as your phase-by-phase checklist for every future project.*
