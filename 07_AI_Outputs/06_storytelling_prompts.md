# PHASE 6 — STORYTELLING & RECOMMENDATIONS
# This phase turns your analysis into a client deliverable.
# Input: 07_AI_Outputs/eda_COMPLETE_SUMMARY.md + all kpi_tables/
# Output: executive presentation narrative + written recommendations report
# ============================================================

---

## PROMPT 6.1 — Build the narrative arc

```
Read 07_AI_Outputs/eda_COMPLETE_SUMMARY.md and the KPI master dashboard file
at 02_Cleaned_Data/kpi_tables/KPI_MASTER_DASHBOARD.csv

I need to present this analysis to a business executive.
The presentation has 10 minutes. Build the narrative arc.

A good business story has 3 parts:
1. WHERE WE ARE — the current situation (facts)
2. WHAT WE FOUND — the key insight that changes how we see the situation
3. WHAT TO DO — the recommended action and expected outcome

Using the Olist data, write the narrative arc:

PART 1 — WHERE WE ARE (2–3 sentences)
Describe the business snapshot: revenue, scale, growth trend.
Use real numbers from KPI_MASTER_DASHBOARD.

PART 2 — WHAT WE FOUND (3–4 sentences, one per major finding)
Lead with the most important finding. Each sentence = one insight + its implication.
Do not say "we found that..." — state the insight directly as fact.
Example format: "One in four orders arrives after the promised date, directly costing
the business 0.8 stars on average review score — a gap that compounds into lost repeat purchases."

PART 3 — WHAT TO DO (3–4 bullet points)
Each bullet: action → expected result → time to see impact
Be specific. Not "improve delivery" — "partner with regional carriers in the 5 worst-performing
states to reduce average delivery time by 20%, targeting a 5pp improvement in on-time rate
within 2 quarters."

Write this in clean, confident business English.
No jargon. No hedging. No "it appears that."
Save to 07_AI_Outputs/storytelling_narrative_arc.md
```

---

## PROMPT 6.2 — Executive summary (1 page)

```
Using 07_AI_Outputs/eda_COMPLETE_SUMMARY.md and KPI_MASTER_DASHBOARD.csv,
write a one-page executive summary for the Olist analysis.

Format:
- PROJECT: Olist E-Commerce Performance Analysis
- PERIOD: [date range from data]
- PREPARED BY: [leave blank — I will fill in]
- DATE: [today's date]

BUSINESS SNAPSHOT (5 KPI callouts in one line each):
→ Total Revenue: [value]
→ Total Orders: [value]
→ On-Time Delivery: [value]%
→ Avg Review Score: [value] / 5
→ Repeat Customer Rate: [value]%

KEY FINDINGS (4 bullet points, max 2 lines each):
• [Finding 1 — most important]
• [Finding 2]
• [Finding 3]
• [Finding 4]

STRATEGIC RECOMMENDATIONS (3 bullet points):
• Priority 1: [action] → [expected outcome]
• Priority 2: [action] → [expected outcome]
• Priority 3: [action] → [expected outcome]

RISK FLAGS (2 bullet points):
• [Something that could get worse if not addressed]
• [A data limitation the client should know about]

Write this in formal business English. Every sentence must be backed by a number from the data.
Save to 06_Reports/olist_executive_summary.md
```

---

## PROMPT 6.3 — Slide-by-slide presentation script

```
I need to present this analysis in a 10-minute executive meeting.
Using the narrative arc from storytelling_narrative_arc.md,
write the speaker script for a 7-slide presentation.

SLIDE 1 — Title slide (30 seconds)
What to say when opening. How to frame the context in one sentence.

SLIDE 2 — Business snapshot (60 seconds)
Script for presenting the 5 headline KPIs.
How to frame growth or decline without alarming the room.

SLIDE 3 — The revenue story (90 seconds)
Script for the revenue trend chart.
What to point to, what the trend means, where the turning points are.

SLIDE 4 — The delivery problem (90 seconds)
Script for the delivery by state chart.
Lead with the most shocking number. Explain the root cause.

SLIDE 5 — The satisfaction connection (90 seconds)
Script for the delivery vs satisfaction chart.
Connect late delivery directly to lost revenue — make it financial, not just operational.

SLIDE 6 — The customer loyalty gap (60 seconds)
Script for the repeat rate finding.
Frame it as an opportunity, not just a problem.
Include the "what if we doubled the repeat rate" projection.

SLIDE 7 — Recommendations (90 seconds)
Script for the 3 recommendations.
Close with a clear call to action — what decision does the executive need to make today?

For each slide: write exact words to say, not bullet points.
This is the script — it should sound natural spoken aloud, not read like a report.
Save to 07_AI_Outputs/presentation_script.md
```

---

## PROMPT 6.4 — Full written recommendations report

```
Write the full strategic recommendations report for the Olist project.
This is the formal written deliverable — not a presentation, a document.

Structure:

1. INTRODUCTION (1 paragraph)
   Context: who Olist is, what data was analysed, what the objective was.

2. METHODOLOGY (1 paragraph)
   What we did: data cleaned, tables joined, KPIs defined, analysis performed.
   Keep it simple — one sentence per step.

3. KEY FINDINGS (one section per theme — 4 themes total)

   Each theme section contains:
   - Theme headline (e.g. "Delivery Performance Is the Primary Risk")
   - 2–3 paragraphs of findings with data
   - A callout box: "What this means for the business" (2–3 sentences)

   Theme 1: Revenue & Growth
   Theme 2: Delivery & Operations
   Theme 3: Customer Satisfaction
   Theme 4: Customer Retention

4. STRATEGIC RECOMMENDATIONS (3 recommendations, one per page equivalent)

   Each recommendation:
   - Recommendation title (action-oriented, e.g. "Prioritise Logistics in the 5 Worst-Performing States")
   - The problem it solves (data evidence)
   - The recommended action (specific and practical)
   - Expected outcome (quantified where possible)
   - How to measure success (what KPI improves, by how much, in what timeframe)
   - Effort vs impact rating: Low/Medium/High for both

5. LIMITATIONS & NEXT STEPS (1 short section)
   What the data cannot tell us. What additional data would improve the analysis.
   Suggested next project phase (e.g. churn prediction model, CLV analysis).

6. APPENDIX — KPI DEFINITIONS
   Table listing every KPI: name, formula, source tables.

Use formal but clear business English.
No statistics jargon. Every claim must cite a specific number.
Save to 06_Reports/olist_recommendations_report.md
This is the client deliverable.
```

---

## PROMPT 6.5 — Talking points for Q&A

```
After an executive presentation, there is always a Q&A.
Based on the Olist analysis findings, prepare talking points for the 10 most likely questions.

For each question:
- The question an executive might ask
- The ideal answer (2–4 sentences, backed by data)
- The number to cite (exact KPI value)
- What NOT to say (common mistake or overreach to avoid)

Questions to prepare for:
1. "How confident are you in these numbers?"
2. "Why is the repeat customer rate so low — is that normal for this industry?"
3. "Which state should we fix first?"
4. "How much would it cost to fix the delivery problem?"
5. "What's the ROI if we improve on-time delivery by 10 percentage points?"
6. "Can you predict which customers are about to churn?"
7. "Why do some categories have such low review scores?"
8. "What's the single most important thing we should do first?"
9. "How does this compare to our competitors?"
10. "What would you need to do a deeper analysis?"

Save to 07_AI_Outputs/qa_talking_points.md
```

---

## PROMPT 6.6 — Final deliverables checklist

```
Generate a final project deliverables checklist for the Olist project.

List every file that should exist in the project at completion.
Check each folder:
- 02_Cleaned_Data/ — list expected files
- 02_Cleaned_Data/kpi_tables/ — list expected files
- 07_AI_Outputs/ — list expected files
- 07_AI_Outputs/charts/ — list expected charts
- 06_Reports/ — list expected reports

For each file: file name, what it contains, which phase produced it, status (exists / missing).

Then generate a project completion scorecard:
- Phase 2 Cleaning: X of Y files complete
- Phase 3 EDA: X of Y analyses complete
- Phase 4 KPIs: X of Y KPI tables complete
- Phase 5 Visualization: X of Y charts complete
- Phase 6 Storytelling: X of Y documents complete
- Overall: X% complete

If any files are missing, tell me which prompts to re-run to generate them.
Save to 07_AI_Outputs/project_completion_checklist.md
```
