#!/usr/bin/env python
"""Write a dated Search Console report, and flag anything that changed.

Run by a Windows scheduled task (see install-schedule.ps1). Every run writes a
markdown file to Documents/Alturascope-SEO/ and refreshes latest.md. It also
keeps state.json, so each report can say what moved since last time rather
than just restating the current numbers.

    python scripts/gsc/report.py            # full report
    python scripts/gsc/report.py --quick    # index status only, for daily runs
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsc  # noqa: E402

OUT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Alturascope-SEO")
STATE = os.path.join(OUT_DIR, "state.json")
PIVOT = "2026-08-26"


def load_state() -> dict:
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {}


def save_state(d: dict) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(d, open(STATE, "w", encoding="utf-8"), indent=2)


def capture(fn, *a, **kw) -> str:
    """Run one of gsc.py's command functions and grab what it printed."""
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        fn(*a, **kw)
    finally:
        sys.stdout = real
    return buf.getvalue().rstrip()


class Args:
    def __init__(self, **kw):
        self.paths, self.site, self.days = [], None, 28
        self.pivot, self.contains, self.url = PIVOT, None, None
        self.__dict__.update(kw)


def index_snapshot(svc, site) -> dict:
    out = {}
    for p in gsc.WATCHED:
        try:
            r = svc.urlInspection().index().inspect(body={
                "inspectionUrl": gsc.page_url(site, p),
                "siteUrl": site, "languageCode": "en-GB",
            }).execute()
            idx = r.get("inspectionResult", {}).get("indexStatusResult", {})
            out[p] = {
                "verdict": idx.get("verdict", "?"),
                "coverage": idx.get("coverageState", "?"),
                "crawl": (idx.get("lastCrawlTime") or "")[:10],
            }
        except Exception as e:
            out[p] = {"verdict": "ERROR", "coverage": str(e)[:60], "crawl": ""}
    return out


def totals(svc, site, days=28) -> dict:
    start, end = gsc.daterange(days)
    rows = gsc.query(svc, site, start, end, [], row_limit=1)
    t = rows[0] if rows else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}
    return {"clicks": t["clicks"], "impressions": t["impressions"],
            "ctr": t["ctr"], "position": t["position"], "start": start, "end": end}


def theme_totals(svc, site, days=28) -> dict:
    start, end = gsc.daterange(days)
    rows = gsc.query(svc, site, start, end, ["query"], row_limit=1000)
    out = {t: {"clicks": 0, "impr": 0, "terms": 0} for t in list(gsc.THEMES) + ["other"]}
    for r in rows:
        q = r["keys"][0].lower()
        theme = next((t for t, w in gsc.THEMES.items() if any(x in q for x in w)), "other")
        out[theme]["clicks"] += r["clicks"]
        out[theme]["impr"] += r["impressions"]
        out[theme]["terms"] += 1
    return out


def delta(now, was, key, better_when_lower=False):
    if was is None:
        return ""
    d = now - was
    if abs(d) < 0.005:
        return "  (no change)"
    arrow = "improved" if (d < 0) == better_when_lower else "down"
    return f"  ({d:+,.1f} {arrow})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="index status only")
    args = ap.parse_args()

    svc = gsc.service()
    site = gsc.resolve_site(svc)
    state = load_state()
    today = dt.date.today().isoformat()

    idx = index_snapshot(svc, site)
    prev_idx = state.get("index", {})
    newly_indexed = [p for p, v in idx.items()
                     if v["verdict"] == "PASS" and prev_idx.get(p, {}).get("verdict") not in (None, "PASS")]
    still_unknown = [p for p, v in idx.items() if v["verdict"] != "PASS"]

    L = []
    L.append(f"# Alturascope search report - {today}\n")

    if newly_indexed:
        L.append("## Newly indexed since the last run\n")
        for p in newly_indexed:
            L.append(f"- **{p}** - {idx[p]['coverage']}")
        L.append("")

    indexed = sum(1 for v in idx.values() if v["verdict"] == "PASS")
    L.append(f"## Indexing: {indexed} of {len(idx)} watched pages\n")
    L.append("| page | verdict | coverage | last crawl |")
    L.append("| --- | --- | --- | --- |")
    for p, v in idx.items():
        L.append(f"| `{p}` | {v['verdict']} | {v['coverage']} | {v['crawl'] or 'never'} |")
    L.append("")

    if still_unknown:
        L.append(f"**{len(still_unknown)} page(s) still not indexed.** Request Indexing is the "
                 "only lever that skips the crawl queue, and it is UI-only - Search Console > "
                 "paste the URL in the top bar > Request Indexing.\n")

    if not args.quick:
        t = totals(svc, site)
        was = state.get("totals", {})
        L.append(f"## Performance, 28 days to {t['end']}\n")
        L.append("| metric | value | vs last run |")
        L.append("| --- | --- | --- |")
        L.append(f"| clicks | {t['clicks']:.0f} |{delta(t['clicks'], was.get('clicks'), 'clicks') or ' -'} |")
        L.append(f"| impressions | {t['impressions']:.0f} |{delta(t['impressions'], was.get('impressions'), 'impressions') or ' -'} |")
        L.append(f"| CTR | {t['ctr']*100:.2f}% |{delta(t['ctr']*100, (was.get('ctr') or 0)*100 if was.get('ctr') is not None else None, 'ctr') or ' -'} |")
        L.append(f"| avg position | {t['position']:.1f} |{delta(t['position'], was.get('position'), 'pos', better_when_lower=True) or ' -'} |")
        L.append("")

        th = theme_totals(svc, site)
        prev_th = state.get("themes", {})
        L.append("## Queries by theme\n")
        L.append("| theme | clicks | impressions | terms | impressions vs last run |")
        L.append("| --- | --- | --- | --- | --- |")
        for name in ("estimating", "survey", "uk", "other"):
            v = th.get(name, {"clicks": 0, "impr": 0, "terms": 0})
            pv = prev_th.get(name, {}).get("impr")
            L.append(f"| {name} | {v['clicks']:.0f} | {v['impr']:.0f} | {v['terms']} |"
                     f"{delta(v['impr'], pv, 'impr') or ' -'} |")
        L.append("")
        est = th.get("estimating", {}).get("impr", 0)
        L.append(f"**Estimating impressions: {est:.0f}.** This was zero before the "
                 f"August 2026 overhaul - it is the number that says whether the "
                 f"estimating work is landing.\n")

        # Build the comparison before writing any markdown around it: it exits
        # early when there is not yet enough post-deploy data, and a code fence
        # opened before a failed call leaves the rest of the report inside it.
        comparison, reason = None, ""
        try:
            comparison = capture(gsc.cmd_compare, svc, site, Args(pivot=PIVOT))
        except SystemExit as e:
            reason = " ".join(str(e).split())
        L.append("## Before and after the overhaul\n")
        if comparison:
            L.append("```")
            L.append(comparison)
            L.append("```\n")
        else:
            L.append(f"_Not available yet: {reason}_\n")

        state["totals"] = {k: t[k] for k in ("clicks", "impressions", "ctr", "position")}
        state["themes"] = th

    state["index"] = idx
    state["last_run"] = today
    save_state(state)

    os.makedirs(OUT_DIR, exist_ok=True)
    body = "\n".join(L)
    dated = os.path.join(OUT_DIR, f"report-{today}.md")
    open(dated, "w", encoding="utf-8").write(body)
    open(os.path.join(OUT_DIR, "latest.md"), "w", encoding="utf-8").write(body)

    print(body)
    print(f"\n  written to {dated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
