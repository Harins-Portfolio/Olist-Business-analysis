"""
OLIST - CONSOLIDATED FULL-ANALYSIS NOTEBOOK BUILDER
====================================================
Assembles 04_Python/olist_full_analysis.ipynb from string cell definitions.

Run:  python 04_Python/build_full_analysis_nb.py
Output: 04_Python/olist_full_analysis.ipynb  (clean, no stored outputs)

The notebook is intentionally built, not hand-edited, so the cell source is
reviewable here and regenerating never carries stale outputs. Sections are
appended in reading order; later tasks add their section code above the
assembly call at the bottom.
"""
from pathlib import Path

import nbformat as nbf

OUT = Path(__file__).resolve().parent / "olist_full_analysis.ipynb"


def md(src):
    return nbf.v4.new_markdown_cell(src.strip("\n"))


def code(src):
    return nbf.v4.new_code_cell(src.strip("\n"))


cells = []

# --------------------------------------------------------------------------- #
# SECTION 0 - SETUP & THEME
# --------------------------------------------------------------------------- #
cells.append(md(r"""
# Olist Business Analytics — Full Analysis Notebook

**Purpose:** One consolidated, run-top-to-bottom notebook: data quality (DAMA-5),
condensed descriptive profiling of the clean tables, business KPIs, growth,
categories, payments, geography, the validated H1 hypothesis (late delivery →
lower satisfaction), seller concentration, and the output exports that feed the
project canvas and dashboards.

**Data flow:** raw CSVs (brief shapes) → cleaned datasets in `02_Cleaned_data/`
→ star schema (verified) → analysis on the cleaned `olist_master.csv`. Read-only:
nothing in `01_Raw_Data/` or `02_Cleaned_data/` is modified.

**Outputs written:**
- `06_AI/Outputs/Generated_Insights/eda_summary.json`
- `06_AI/Outputs/Generated_Charts/viz_01..08.png`
- `06_AI/Outputs/Generated_Reports/descriptive_analysis.html`

> Run from the project root (`Project BA Olist/`). Python 3.14, matplotlib +
> seaborn, scipy, plotly.
"""))

cells.append(code(r"""
import sys, json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Robust project-root detection (survives headless execution from any cwd).
ROOT = Path.cwd()
for cand in [Path.cwd(), *Path.cwd().parents]:
    if (cand / "04_Python" / "descriptive_lib.py").exists():
        ROOT = cand
        break
sys.path.insert(0, str(ROOT / "04_Python"))

import descriptive_lib as dl

CLEAN = ROOT / "02_Cleaned_data"
STAR  = CLEAN / "star_schema"
CHART = ROOT / "06_AI" / "Outputs" / "Generated_Charts"
INSIGHTS = ROOT / "06_AI" / "Outputs" / "Generated_Insights"
CHART.mkdir(parents=True, exist_ok=True)
INSIGHTS.mkdir(parents=True, exist_ok=True)

GREEN, RED, NAVY, GRAY = "#0f6b47", "#b0413e", "#1f3a93", "#9aa3ad"

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white",
                     "axes.grid": True, "grid.alpha": .3, "font.size": 10,
                     "axes.titleweight": "bold"})
pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 220)


def savefig(name):
    plt.tight_layout()
    plt.savefig(CHART / name, dpi=160, bbox_inches="tight")
    plt.show()
    print(f"  saved -> {CHART / name}")


print(f"Project root: {ROOT}")
print(f"Registry loaded: {len(dl.TABLES)} clean tables")
"""))

# --------------------------------------------------------------------------- #
# ASSEMBLY - later sections append above this line
# --------------------------------------------------------------------------- #
def build():
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14"},
    }
    nbf.write(nb, OUT)
    print(f"Wrote {OUT} ({len(cells)} cells)")
    return OUT


if __name__ == "__main__":
    build()
