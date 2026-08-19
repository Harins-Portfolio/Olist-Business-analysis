"""
OLIST - DESCRIPTIVE ANALYSIS HTML REPORT
========================================
Read-only, self-contained SINGLE-FILE report with ONE PAGE PER TABLE.

Layout:
  - Sidebar navigation groups tables exactly as descriptive_lib.TABLES does
    (currently "Flat files" and "Star schema").
  - Each table is its own page (hidden until selected); deep-linkable via
    #<key> (e.g. #fact_orders) and browser back/forward work via hashchange.
  - Charts are lazy: each page ships with an inert <template> holding its
    figures; the JS clones it into the page the first time the page is opened,
    so Plotly.js is loaded once and the initial page stays light.

Future-enhancement measures:
  - Everything is registry-driven from descriptive_lib.TABLES: adding a table
    (or re-labelling a group) automatically produces its page, nav link and
    chart template - no template edits needed.
  - Page layout, nav builder and navigation JS live here in module-level
    functions/constants, so styling or navigation changes are one place.
  - Chart typing (hist / bar / donut / trend / scatter) is centralized in
    descriptive_lib.

Run:  python 04_Python/descriptive_report.py
Reads:  02_Cleaned_data/*.csv  +  star_schema/*.csv   (never modified)
Writes: 06_AI/Outputs/Generated_Reports/descriptive_analysis.html
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import descriptive_lib as dl

REPORTS_DIR = dl.REPORTS
OUT = REPORTS_DIR / "descriptive_analysis.html"

GREEN, RED, NAVY, GRAY, AMBER = "#0f6b47", "#b0413e", "#1f3a93", "#9aa3ad", "#b7791f"


def _fmt(v):
    """Print 24.0 as '24' but keep 24.95 as '24.95' - kills the '.0' noise."""
    try:
        f = float(v)
        return str(int(f)) if f.is_integer() else f"{f:,.2f}"
    except (TypeError, ValueError):
        return v


def fig_hist(col_prof: dict) -> str:
    """Continuous column -> histogram. Money is right-skewed, so plot it as
    human-readable R$ amount bands (fixed labels, no log-scale notation) and
    caption median/mean."""
    import plotly.graph_objects as go

    df = col_prof["_frame"]
    name = col_prof["name"]
    cap = ""
    if name in dl.MONEY_COLS:
        labels, counts, stats = dl.money_bands(df[name])
        if stats is None:
            return ""
        fig = go.Figure(go.Bar(x=labels, y=counts, marker_color=NAVY,
                               marker_line_width=0))
        xlab = "R$"
        if stats:
            cap = f"median <b>R$ {_fmt(stats['median'])}</b> · mean R$ {_fmt(stats['mean'])} · " \
                  f"min R$ {_fmt(stats['min'])}"
            if stats["zeros"]:
                cap += f" · {stats['zeros']:,} rows = R$ 0"
            else:
                cap += " · no R$ 0 rows"
    else:
        s = pd.to_numeric(df[name], errors="coerce").dropna()
        if s.empty:
            return ""
        nb = min(30, max(int(s.nunique()), 1))
        fig = go.Figure(go.Histogram(x=s, nbinsx=nb, marker_color=NAVY,
                                     marker_line_width=0))
        xlab = name
    fig.update_layout(height=180, margin=dict(l=8, r=8, t=26, b=8),
                      title=dict(text=col_prof["label"], font=dict(size=12)),
                      xaxis_title=xlab, yaxis_title="count",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb",
                      showlegend=False)
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    return html + (f"<p class='caption'>{cap}</p>" if cap else "")


def fig_bar(col_prof: dict) -> str:
    """Ordinal (ordered) -> vertical bar in natural order; nominal -> top-10 h-bar."""
    import plotly.graph_objects as go

    df = col_prof["_frame"]
    name = col_prof["name"]
    if col_prof.get("ordered"):
        num = pd.to_numeric(df[name], errors="coerce")
        if num.notna().any():
            vc = num.value_counts().sort_index()
        else:
            vc = df[name].astype(str).value_counts().sort_index()
        keys = [str(k) for k in vc.index]
        vals = list(vc.values)
        fig = go.Figure(go.Bar(x=keys, y=vals, marker_color=NAVY))
        fig.update_layout(height=180, margin=dict(l=8, r=8, t=26, b=8),
                          title=dict(text=col_prof["label"], font=dict(size=12)),
                          xaxis_title=name, yaxis_title="count",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb",
                          showlegend=False)
    else:
        vc = pd.Series(col_prof.get("top", {}))
        keys = [str(k) for k in vc.index]
        vals = list(vc.values)
        fig = go.Figure(go.Bar(x=vals, y=keys, orientation="h",
                               marker_color=GREEN))
        fig.update_layout(height=150 + 22 * len(keys), margin=dict(l=8, r=8, t=26, b=8),
                          title=dict(text=col_prof["label"], font=dict(size=12)),
                          xaxis_title="count", yaxis_title="",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb",
                          showlegend=False)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def fig_donut(col_prof: dict) -> str:
    """Binary flag -> donut showing the share of 'yes'."""
    import plotly.graph_objects as go

    df = col_prof["_frame"]
    s = pd.to_numeric(df[col_prof["name"]], errors="coerce").fillna(0)
    yes = int((s == 1).sum())
    total = len(s)
    colors = [AMBER if col_prof["name"] == "is_late" else GREEN, GRAY]
    fig = go.Figure(go.Pie(labels=["yes", "no"],
                           values=[yes, max(total - yes, 0)],
                           hole=.5, marker=dict(colors=colors),
                           textinfo="label+percent", textfont=dict(size=10)))
    fig.update_layout(height=190, margin=dict(l=8, r=8, t=26, b=8),
                      title=dict(text=col_prof["label"], font=dict(size=12)),
                      showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb")
    return fig.to_html(full_html=False, include_plotlyjs=False)


def fig_trend(col_prof: dict) -> str:
    """Datetime -> monthly time-series (growth + seasonality)."""
    import plotly.graph_objects as go

    df = col_prof["_frame"]
    s = pd.to_datetime(df[col_prof["name"]], errors="coerce").dropna()
    if s.empty:
        return ""
    months = s.dt.to_period("M").astype(str).value_counts().sort_index()
    fig = go.Figure(go.Scatter(x=months.index, y=months.values,
                               mode="lines+markers",
                               line=dict(color=NAVY, width=1.6),
                               marker=dict(size=4)))
    fig.update_layout(height=180, margin=dict(l=8, r=8, t=26, b=8),
                      title=dict(text=col_prof["label"], font=dict(size=12)),
                      xaxis_title="month", yaxis_title="count",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb",
                      showlegend=False)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def fig_scatter(df: pd.DataFrame, coord_cols: list) -> str:
    """Density heatmap of zip-centroid coordinates (longitude vs latitude)."""
    import plotly.graph_objects as go

    lat_c = next((c["name"] for c in coord_cols
                  if c["name"] in ("latitude", "geolocation_lat")), None)
    lng_c = next((c["name"] for c in coord_cols
                  if c["name"] not in ("latitude", "geolocation_lat")), None)
    fig = go.Figure(go.Histogram2d(
        x=pd.to_numeric(df[lng_c], errors="coerce"),
        y=pd.to_numeric(df[lat_c], errors="coerce"),
        nbinsx=60, nbinsy=60, colorscale="Viridis", showscale=True,
        colorbar=dict(title="zip<br>prefixes", thickness=12)))
    fig.update_layout(height=300, margin=dict(l=8, r=8, t=26, b=8),
                      title=dict(text="Zip-centroid density (coverage)", font=dict(size=12)),
                      xaxis=dict(title="longitude", range=[-74, -34]),
                      yaxis=dict(title="latitude", range=[-34, 6],
                                 scaleanchor="x", scaleratio=1.035),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfbfb")
    return fig.to_html(full_html=False, include_plotlyjs=False)


def fig_for(col_prof: dict) -> str:
    chart = col_prof.get("chart")
    if chart == "hist":
        return fig_hist(col_prof)
    if chart == "bar":
        return fig_bar(col_prof)
    if chart == "donut":
        return fig_donut(col_prof)
    if chart == "trend":
        return fig_trend(col_prof)
    return ""


def _badge(status: str) -> str:
    st = status.lower()
    color = {"pass": GREEN, "warn": AMBER, "fail": RED, "info": GRAY}.get(st, GRAY)
    return f'<span class="badge" style="background:{color}">{status.upper()}</span>'


def column_table_html(col_prof: dict) -> str:
    rows = []
    for c in col_prof:
        s = c.get("stats")
        stat_txt = ""
        if s:
            if c["kind"] == "numeric":
                stat_txt = (f"min <b>{_fmt(s['min'])}</b> · med <b>{_fmt(s['median'])}</b> · "
                            f"mean <b>{_fmt(s['mean'])}</b> · max <b>{_fmt(s['max'])}</b>")
            elif c["kind"] == "datetime":
                stat_txt = f"{s.get('min', '')} → {s.get('max', '')}"
        null_badge = (f'<span style="color:{RED}">{c["null"]:,} ({c["null_pct"]}%)</span>'
                      if c["null"] else f'<span style="color:{GREEN}">0</span>')
        rows.append(
            "<tr>"
            f"<td><code>{c['name']}</code></td>"
            f"<td>{c['dtype']}</td>"
            f"<td class='tiny'>{c.get('chart', '')}</td>"
            f"<td>{null_badge}</td>"
            f"<td>{c['n_unique']:,}</td>"
            f"<td class='stat'>{stat_txt}</td>"
            "</tr>"
        )
    return "<table class='cols'><thead><tr><th>Column</th><th>Type</th><th>Chart</th>" \
           "<th>Nulls</th><th>Unique</th><th>Summary</th></tr></thead><tbody>" + \
           "".join(rows) + "</tbody></table>"


def charts_html(prof: dict) -> str:
    """All distribution figures for a table as HTML.  Kept inert in a
    <template> until the page is opened, so the initial load stays light."""
    charts = []
    scats = [c for c in prof["columns"] if c.get("chart") == "scatter"]
    scat_names = {c["name"] for c in scats}
    seen_family = False
    for c in prof["columns"]:
        if c.get("chart") in (None, "skip") or c["name"] in scat_names:
            continue
        if c["name"] in dl.DATE_FAMILY:
            if seen_family:
                continue  # same timestamp shown once (e.g. keep trend, skip month/year/day)
            seen_family = True
        c["_frame"] = prof["df"]
        html = fig_for(c)
        if html:
            charts.append(f"<div class='chart'>{html}</div>")
    if scats:
        charts.append(f"<div class='chart'>{fig_scatter(prof['df'], scats)}</div>")
    return "".join(charts)


def page_html(prof: dict, dama: dict, checks: list[dict]) -> str:
    """One table = one page (hidden until selected from the sidebar).  Figures
    are deferred: the page ships with an empty #chart-slot and an inert
    <template>; the first time the page is shown the JS clones the template
    into the slot, which renders the Plotly charts exactly once."""
    score_row = "".join(
        f"<td><b>{k}</b><br>{_badge(v[0])}<div class='tiny'>{v[1]}</div></td>"
        for k, v in dama["scores"].items()
    )

    # Verification block for this table
    verdict_block = ""
    if checks:
        v = checks[0]["status"] if len(checks) == 1 else None
        if len(checks) == 1:
            verdict_block = (f"<div class='verdict'><b>Clean-check:</b> "
                             f"{_badge(v)} {checks[0]['detail']}</div>")
        else:
            badges = "".join(_badge(c["status"]) + " " + c["detail"] + "<br>"
                             for c in checks)
            verdict_block = f"<div class='verdict'><b>Clean-check ({len(checks)} checks):</b><br>{badges}</div>"

    chart_html = charts_html(prof)
    n_charts = chart_html.count("class='chart'")

    key_ok = prof["key_unique"] == prof["rows"] if prof["key_unique"] is not None else None
    key_html = "—" if key_ok is None else (
        f'<span style="color:{GREEN}">unique ✅ ({prof["key_unique"]:,})</span>'
        if key_ok else f'<span style="color:{RED}">DUPLICATES ❌ ({prof["key_unique"]:,}/{prof["rows"]:,})</span>')

    return f"""
<section class="page card" id="page-{prof['key']}" hidden>
  <h2>{prof['label']} <span class="file">({prof['rel']})</span></h2>
  <div class="meta">
    <span><b>{prof['rows']:,}</b> rows</span>
    <span><b>{prof['cols']}</b> columns</span>
    <span>Key: <code>{'+'.join(prof['key_cols'])}</code> → {key_html}</span>
    <span>Overall: {_badge(dama['overall'])}</span>
  </div>
  {verdict_block}
  <div class="dama"><table class="cols"><thead><tr>
     <th>Completeness</th><th>Consistency</th><th>Accuracy</th><th>Timeliness</th><th>Uniqueness</th>
  </tr></thead><tbody><tr>{score_row}</tr></tbody></table></div>
  {column_table_html(prof['columns'])}
  <details open><summary>Distribution charts ({n_charts})</summary>
    <div class="charts" id="chart-slot-{prof['key']}"></div>
  </details>
</section>
<template id="tmpl-{prof['key']}">
  <div class="charts">{chart_html}</div>
</template>
"""


def build_html() -> None:
    print("Profiling all 18 tables ...")
    overview = dl.overview()
    print("Running clean-check ...")
    v = dl.verdict()

    print("Building sections ...")
    sections = []
    nav_flat = []
    nav_star = []
    for t in dl.TABLES:
        p = dl.profile_table(t["rel"])
        d = dl.dama5(p)
        checks = v["by_table"].get(t["rel"], [])
        sections.append(page_html(p, d, checks))
        icon = {"pass": "✅", "warn": "☑", "fail": "❌"}[d["overall"]]
        link = f'<li>{icon} <a href="#{t["key"]}" data-page="{t["key"]}">{t["label"]}</a></li>'
        (nav_flat if t["group"] == "Flat files" else nav_star).append(link)

    counts = v["counts"]
    summary_badges = "".join(_badge(s) + f" {counts.get(s, 0)} "
                             for s in ["PASS", "FAIL", "WARN", "INFO"])

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Olist — Descriptive Analysis of Cleaned Data</title>
<style>
* {{ box-sizing:border-box; }}
body {{ font-family:'Segoe UI',system-ui,sans-serif; margin:0; color:#222; background:#f4f6f8; }}
a {{ color:{NAVY}; text-decoration:none; }}
header {{ background:#102a43; color:#fff; padding:22px 32px; }}
header h1 {{ margin:0 0 6px; font-size:22px; }}
header .sub {{ opacity:.85; font-size:13px; }}
main {{ display:grid; grid-template-columns:260px 1fr; gap:0; }}
nav {{ background:#1d3a5f; padding:14px 10px; position:sticky; top:0; height:100vh; overflow:auto; }}
nav ul {{ list-style:none; margin:0; padding:0; }}
nav a {{ color:#d7e3f1; font-size:13px; }}
nav .grp {{ color:#8fb3d9; font-size:11px; text-transform:uppercase; margin:12px 0 4px; letter-spacing:.06em; }}
.content {{ padding:24px 32px; max-width:1150px; }}
.card {{ background:#fff; border:1px solid #e3e8ee; border-radius:10px; padding:18px 22px; margin-bottom:22px; }}
.card h2 {{ margin:0 0 10px; font-size:18px; }}
.card .file {{ color:#7b8794; font-size:12px; font-weight:normal; }}
.meta {{ display:flex; flex-wrap:wrap; gap:18px; font-size:13px; margin-bottom:12px; }}
.badge {{ color:#fff; padding:2px 9px; border-radius:10px; font-size:11px; font-weight:600; }}
.dama {{ margin:8px 0 14px; }}
.dama td {{ width:20%; vertical-align:top; font-size:12px; text-align:center; }}
.dama .tiny {{ color:#6b7684; font-size:11px; font-weight:normal; margin-top:4px; }}
table.cols {{ border-collapse:collapse; width:100%; font-size:12.5px; margin:10px 0; }}
table.cols th {{ background:#eef2f6; text-align:left; padding:6px 8px; border:1px solid #dde4ec; }}
table.cols td {{ padding:6px 8px; border:1px solid #e7ecf2; vertical-align:top; }}
table.cols td.stat {{ color:#445; }}
code {{ background:#eef2f6; padding:1px 5px; border-radius:4px; font-size:12px; }}
.verdict {{ background:#f2f7f3; border-left:4px solid {GREEN}; padding:8px 12px; font-size:13px; margin:6px 0 10px; }}
details summary {{ cursor:pointer; font-weight:600; color:{NAVY}; margin-top:6px; }}
.charts {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:14px; margin-top:10px; }}
.charts > div {{ min-width:0; }}
.chart .caption {{ font-size:11px; color:#6b7684; margin:3px 2px 0; }} 
.ov {{ background:#fff; border:1px solid #e3e8ee; border-radius:10px; padding:18px 22px; margin-bottom:22px; }}
.ov .kpis {{ display:flex; gap:16px; flex-wrap:wrap; margin:12px 0; }}
.kpi {{ background:#eef6f1; border-left:4px solid {GREEN}; padding:10px 16px; border-radius:6px; }}
.kpi b {{ font-size:20px; display:block; }}
.page[hidden] {{ display:none; }}
.nav a.active {{ color:#fff; background:#2d5a8f; border-radius:6px; padding:2px 10px; font-weight:600; }}
</style></head>
<body>
<header>
  <h1>📊 Olist — Descriptive Analysis of All Cleaned Datasets</h1>
  <div class="sub">18 tables · one page per table · DAMA-5 scored · clean-check re-run · generated {v['generated_at'].replace('T', ' ')}</div>
</header>
<main>
<nav><ul>
  <li><a href="#overview" data-page="overview">— Overview —</a></li>
  <li class="grp">Flat files</li>
  {''.join(nav_flat)}
  <li class="grp">Star schema</li>
  {''.join(nav_star)}
</ul></nav>
<div class="content">
  <div class="ov" id="overview">
    <h2>✅ Everything-at-a-glance</h2>
    <div class="kpis">
      <div class="kpi"><b>{len(dl.TABLES)}</b> tables profiled</div>
      <div class="kpi"><b>{counts['PASS']}</b> checks passed</div>
      <div class="kpi"><b style="color:{RED}">{counts['FAIL']}</b> checks failed</div>
      <div class="kpi"><b>{counts['WARN']}</b> warnings</div>
      <div class="kpi"><b>{sum(p['rows'] for p in [dl.profile_table(t['rel']) for t in dl.TABLES])}</b> total rows</div>
    </div>
    <p>Clean-check verdict: {summary_badges} — status <b>{'READY ✅' if counts['FAIL'] == 0 else 'NOT READY ❌'}</b>.</p>
    <h3>Overview grid</h3>
    {overview.to_html(index=False, escape=False, border=0, classes='cols')}
  </div>
  {''.join(sections)}
</div>
</main>
<script>
/* Single-file page navigation: one page per table. Pages stay hidden until
   selected; charts are lazy (cloned from each table's <template> on first
   visit). Deep-linkable via #<key>; browser back/forward via hashchange. */
(function () {{
  var visited = {{}};
  function showPage(id) {{
    var pages = document.querySelectorAll('.page');
    for (var i = 0; i < pages.length; i++) pages[i].hidden = true;
    var page = document.getElementById('page-' + id);
    if (page) {{
      page.hidden = false;
      if (!visited[id]) {{
        visited[id] = true;
        var tmpl = document.getElementById('tmpl-' + id);
        var slot = document.getElementById('chart-slot-' + id);
        if (tmpl && slot) slot.appendChild(tmpl.content.cloneNode(true));
      }}
    }}
    var links = document.querySelectorAll('.nav a[data-page]');
    for (var j = 0; j < links.length; j++) {{
      links[j].classList.toggle('active', links[j].getAttribute('data-page') === id);
    }}
  }}
  function pageFromHash() {{
    var h = (location.hash || '').replace(/^#/, '');
    return document.getElementById('page-' + h) ? h : 'overview';
  }}
  window.addEventListener('hashchange', function () {{ showPage(pageFromHash()); }});
  var navLinks = document.querySelectorAll('.nav a[data-page]');
  for (var k = 0; k < navLinks.length; k++) {{
    navLinks[k].addEventListener('click', function (e) {{
      e.preventDefault();
      var id = this.getAttribute('data-page');
      if (location.hash !== '#' + id) location.hash = id;
      showPage(id);
    }});
  }}
  showPage(pageFromHash());
}})();
</script>
</body></html>"""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")


def inject_plotly(html: str) -> str:
    import plotly.offline as pyo

    plotly_js = pyo.get_plotlyjs()  # ~3.5 MB inline javascript
    script = f"<script type='text/javascript'>{plotly_js}</script>"
    return html.replace("<style>", script + "<style>", 1)


def main() -> None:
    build_html()
    text = OUT.read_text(encoding="utf-8")
    injected = inject_plotly(text)
    OUT.write_text(injected, encoding="utf-8")
    print(f"[OK] Report -> {OUT}  ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
