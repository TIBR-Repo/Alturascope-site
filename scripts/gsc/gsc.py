#!/usr/bin/env python
"""Search Console for alturascope.com, without a browser.

Authenticates as a service account that has been added as a user on the
property, so there is no OAuth consent screen, no refresh token to expire and
nothing to click. Setup is in README.md in this directory.

    python scripts/gsc/gsc.py status
    python scripts/gsc/gsc.py submit-sitemap
    python scripts/gsc/gsc.py index-status            # the pages we changed
    python scripts/gsc/gsc.py report --days 28
    python scripts/gsc/gsc.py compare --pivot 2026-08-26
    python scripts/gsc/gsc.py queries --contains estimating

What this CANNOT do: request indexing. Google's Indexing API is sanctioned
only for JobPosting and BroadcastEvent markup, so for ordinary pages that
button still lives in the UI. `index-status` is the next best thing - it tells
you whether Google has actually picked a page up, so you know whether asking
would even help.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from collections import defaultdict

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    sys.exit("pip install --user google-api-python-client google-auth")

KEY_PATH = os.environ.get(
    "GSC_KEY", r"C:\Users\andre\.credentials\gsc-service-account.json"
)
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
SITE_HINT = "alturascope.com"

# The pages this overhaul created or materially changed, in the order they
# matter commercially. Used by `index-status` and `compare`.
WATCHED = [
    "/uk/estimating/",
    "/estimating/",
    "/uk/",
    "/work/locations/",
    "/estimating/sample-quote-pack/",
    "/estimating/basis-of-estimate/",
    "/insights/what-is-a-basis-of-estimate/",
    "/insights/nrm2-bill-of-quantities-explained/",
    "/insights/how-to-check-a-construction-estimate/",
    "/insights/estimating-capacity-limits-contractor-growth/",
]

# Terms the overhaul was aimed at. `queries` groups against these.
THEMES = {
    "estimating": ["estimat", "bid ", "tender", "quantity", "take-off", "takeoff",
                   "bill of quantities", "nrm2", "nrm ", "bcis", "basis of estimate",
                   "provisional sum", "preliminaries"],
    "survey": ["survey", "matterport", "digital twin", "point cloud", "as-built",
               "as built", "lidar", "measured building", "documentation"],
    "uk": ["uk", "london", "british", "england", "scotland", "wales"],
}


def die(msg: str) -> None:
    sys.exit(f"\n  {msg}\n")


def service():
    if not os.path.exists(KEY_PATH):
        die(
            f"No service-account key at {KEY_PATH}\n"
            f"  Set GSC_KEY, or follow scripts/gsc/README.md to create one."
        )
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def resolve_site(svc, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    try:
        entries = svc.sites().list().execute().get("siteEntry", [])
    except HttpError as e:
        die(f"Could not list properties: {e}")
    if not entries:
        die(
            "The service account can see no properties.\n"
            "  Add its email as a user in Search Console:\n"
            "  Settings > Users and permissions > Add user > paste the\n"
            "  client_email from the key file > permission 'Full'."
        )
    matches = [e for e in entries if SITE_HINT in e["siteUrl"]]
    if not matches:
        listing = "\n".join(f"    {e['siteUrl']}  ({e['permissionLevel']})" for e in entries)
        die(f"No property matching '{SITE_HINT}'. Visible to this account:\n{listing}")
    # a Domain property (sc-domain:) covers more than a URL-prefix one
    matches.sort(key=lambda e: (not e["siteUrl"].startswith("sc-domain:"), e["siteUrl"]))
    return matches[0]["siteUrl"]


def page_url(site: str, path: str) -> str:
    if site.startswith("sc-domain:"):
        return f"https://{site.split(':', 1)[1]}{path}"
    return site.rstrip("/") + path


def daterange(days: int, end_offset: int = 3) -> tuple[str, str]:
    """Search Analytics lags roughly three days; don't ask for data that isn't there."""
    end = dt.date.today() - dt.timedelta(days=end_offset)
    return (end - dt.timedelta(days=days - 1)).isoformat(), end.isoformat()


def query(svc, site: str, start: str, end: str, dimensions: list[str],
          row_limit: int = 500, filters: list | None = None) -> list[dict]:
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
        "dataState": "final",
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    try:
        return svc.searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])
    except HttpError as e:
        die(f"Search Analytics query failed: {e}")


# ---------------------------------------------------------------- commands


def cmd_status(svc, site, args):
    entries = svc.sites().list().execute().get("siteEntry", [])
    print(f"\n  key:      {KEY_PATH}")
    print(f"  identity: {json.load(open(KEY_PATH))['client_email']}")
    print(f"  using:    {site}\n")
    print("  properties visible to this account:")
    for e in entries:
        mark = "*" if e["siteUrl"] == site else " "
        print(f"   {mark} {e['siteUrl']:<45} {e['permissionLevel']}")
    sm = svc.sitemaps().list(siteUrl=site).execute().get("sitemap", [])
    print(f"\n  sitemaps ({len(sm)}):")
    for s in sm:
        warn = s.get("warnings", 0)
        errs = s.get("errors", 0)
        last = (s.get("lastSubmitted") or "")[:10]
        print(f"    {s['path']}")
        print(f"      submitted {last}  errors {errs}  warnings {warn}  "
              f"indexed-state {'pending' if s.get('isPending') else 'processed'}")
    print()


def cmd_submit_sitemap(svc, site, args):
    target = args.url or page_url(site, "/sitemap-index.xml")
    try:
        svc.sitemaps().submit(siteUrl=site, feedpath=target).execute()
    except HttpError as e:
        die(f"Submit failed: {e}\n  (sitemap submission needs 'Full' or 'Owner' permission)")
    print(f"\n  submitted {target}\n")
    cmd_status(svc, site, args)


def cmd_index_status(svc, site, args):
    paths = args.paths or WATCHED
    print(f"\n  {'verdict':<12} {'coverage':<34} {'last crawl':<12} page")
    print(f"  {'-'*12} {'-'*34} {'-'*12} {'-'*40}")
    for p in paths:
        url = p if p.startswith("http") else page_url(site, p)
        try:
            r = svc.urlInspection().index().inspect(body={
                "inspectionUrl": url, "siteUrl": site, "languageCode": "en-GB",
            }).execute()
        except HttpError as e:
            print(f"  {'ERROR':<12} {str(e)[:34]:<34} {'':<12} {p}")
            continue
        idx = r.get("inspectionResult", {}).get("indexStatusResult", {})
        verdict = idx.get("verdict", "?")
        coverage = (idx.get("coverageState") or "?")[:34]
        crawl = (idx.get("lastCrawlTime") or "never")[:10]
        print(f"  {verdict:<12} {coverage:<34} {crawl:<12} {p}")
    print("\n  PASS = indexed. NEUTRAL/'Discovered - currently not indexed' means")
    print("  Google knows about it but has not indexed it yet.\n")


def cmd_report(svc, site, args):
    start, end = daterange(args.days)
    print(f"\n  {site}   {start} to {end}\n")

    totals = query(svc, site, start, end, [], row_limit=1)
    if totals:
        t = totals[0]
        print(f"  clicks {int(t['clicks']):>6}   impressions {int(t['impressions']):>8}   "
              f"CTR {t['ctr']*100:>5.2f}%   avg position {t['position']:>5.1f}\n")

    for dim, title, n in (("page", "Top pages", 15), ("query", "Top queries", 20)):
        rows = query(svc, site, start, end, [dim], row_limit=n)
        print(f"  {title}")
        print(f"    {'clicks':>6} {'impr':>8} {'pos':>6}  {dim}")
        for r in rows:
            key = r["keys"][0]
            if dim == "page":
                key = key.replace("https://alturascope.com", "") or "/"
            print(f"    {int(r['clicks']):>6} {int(r['impressions']):>8} "
                  f"{r['position']:>6.1f}  {key[:66]}")
        print()


def cmd_queries(svc, site, args):
    start, end = daterange(args.days)
    rows = query(svc, site, start, end, ["query"], row_limit=1000)
    if args.contains:
        rows = [r for r in rows if args.contains.lower() in r["keys"][0].lower()]
        print(f"\n  queries containing '{args.contains}'   {start} to {end}\n")
        print(f"    {'clicks':>6} {'impr':>8} {'pos':>6}  query")
        for r in sorted(rows, key=lambda r: -r["impressions"])[:40]:
            print(f"    {int(r['clicks']):>6} {int(r['impressions']):>8} "
                  f"{r['position']:>6.1f}  {r['keys'][0][:66]}")
        print()
        return

    buckets = defaultdict(lambda: [0, 0, []])
    for r in rows:
        q = r["keys"][0].lower()
        theme = next((t for t, words in THEMES.items() if any(w in q for w in words)), "other")
        buckets[theme][0] += r["clicks"]
        buckets[theme][1] += r["impressions"]
        buckets[theme][2].append(r)
    print(f"\n  queries by theme   {start} to {end}\n")
    print(f"    {'clicks':>6} {'impr':>8} {'terms':>6}  theme")
    for theme in ("estimating", "survey", "uk", "other"):
        if theme not in buckets:
            continue
        c, i, rs = buckets[theme]
        print(f"    {int(c):>6} {int(i):>8} {len(rs):>6}  {theme}")
    print("\n  'estimating' is the number to watch - it was near zero before")
    print("  the August 2026 overhaul added estimating content.\n")


def cmd_compare(svc, site, args):
    pivot = dt.date.fromisoformat(args.pivot)
    span = args.days
    lag = dt.date.today() - dt.timedelta(days=3)

    after_end = min(pivot + dt.timedelta(days=span - 1), lag)
    after_days = (after_end - pivot).days + 1
    if after_days < 3:
        die(f"Only {max(after_days,0)} day(s) of data since {pivot}. "
            f"Search Console lags ~3 days - come back in a week.")

    before_end = pivot - dt.timedelta(days=1)
    before_start = before_end - dt.timedelta(days=after_days - 1)

    def totals_for(s, e):
        r = query(svc, site, s.isoformat(), e.isoformat(), [], row_limit=1)
        return r[0] if r else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}

    b = totals_for(before_start, before_end)
    a = totals_for(pivot, after_end)

    print(f"\n  {site}")
    print(f"  before  {before_start} to {before_end}   ({after_days} days)")
    print(f"  after   {pivot} to {after_end}   ({after_days} days)\n")
    print(f"    {'':<14}{'before':>10}{'after':>10}{'change':>12}")
    for label, key, fmt in (("clicks", "clicks", "{:.0f}"),
                            ("impressions", "impressions", "{:.0f}"),
                            ("CTR %", "ctr", "{:.2f}"),
                            ("avg position", "position", "{:.1f}")):
        bv = b[key] * (100 if key == "ctr" else 1)
        av = a[key] * (100 if key == "ctr" else 1)
        if key == "position":
            delta = f"{bv - av:+.1f}" + (" better" if av < bv else " worse")
        else:
            delta = f"{av - bv:+,.0f}" if key != "ctr" else f"{av - bv:+.2f}"
        print(f"    {label:<14}{fmt.format(bv):>10}{fmt.format(av):>10}{delta:>12}")

    print(f"\n  Watched pages, impressions\n")
    print(f"    {'before':>8}{'after':>8}{'change':>10}  page")
    for p in WATCHED:
        full = page_url(site, p)
        f = [{"dimension": "page", "operator": "equals", "expression": full}]
        rb = query(svc, site, before_start.isoformat(), before_end.isoformat(), ["page"], 1, f)
        ra = query(svc, site, pivot.isoformat(), after_end.isoformat(), ["page"], 1, f)
        ib = int(rb[0]["impressions"]) if rb else 0
        ia = int(ra[0]["impressions"]) if ra else 0
        print(f"    {ib:>8}{ia:>8}{ia - ib:>+10}  {p}")
    print()


COMMANDS = {
    "status": cmd_status,
    "submit-sitemap": cmd_submit_sitemap,
    "index-status": cmd_index_status,
    "report": cmd_report,
    "queries": cmd_queries,
    "compare": cmd_compare,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=sorted(COMMANDS))
    ap.add_argument("paths", nargs="*", help="paths for index-status")
    ap.add_argument("--site", help="override the property (e.g. sc-domain:alturascope.com)")
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--pivot", default="2026-08-26", help="compare: the deploy date")
    ap.add_argument("--contains", help="queries: filter to terms containing this")
    ap.add_argument("--url", help="submit-sitemap: a different sitemap URL")
    args = ap.parse_args()

    svc = service()
    site = resolve_site(svc, args.site)
    COMMANDS[args.command](svc, site, args)


if __name__ == "__main__":
    main()
