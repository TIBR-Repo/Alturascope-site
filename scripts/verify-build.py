#!/usr/bin/env python
"""Everything that should be true about dist/ before a push.

seo-audit.py covers meta, canonicals, schema and hreflang. This covers the
things that broke during the August 2026 overhaul and would have shipped
silently: links to pages that no longer exist, anchors that point at nothing,
images referenced but not built, and pages that lazy-load their own hero.

    python scripts/verify-build.py

Exits non-zero on any failure, so it can gate a deploy.
"""
import os
import re
import sys
import glob
from collections import defaultdict

DIST = "dist"
failures = []
notes = []


def route_of(path):
    u = "/" + os.path.relpath(path, DIST).replace(os.sep, "/").replace("index.html", "")
    return u[:-5] if u.endswith(".html") else u


def main():
    if not os.path.isdir(DIST):
        sys.exit("dist/ not found - run `npm run build` first")

    pages = {}
    for f in glob.glob(f"{DIST}/**/*.html", recursive=True):
        pages[route_of(f)] = open(f, encoding="utf-8", errors="ignore").read()

    routes = set(pages)
    # A redirect stub exists at its old path, so a link to one technically
    # resolves - which is exactly why it slipped past this check the first
    # time. Internal links should point at the destination: a hop wastes crawl
    # budget and dilutes the signal the link was meant to pass.
    redirects = {r for r, h in pages.items() if 'http-equiv="refresh"' in h}
    ids = {r: set(re.findall(r'\bid="([^"]+)"', h)) for r, h in pages.items()}

    # --- internal links, trailing slashes, fragments -----------------------
    bad_link, bad_frag, no_slash, to_redirect = [], [], [], []
    asset_re = re.compile(r"\.(jpg|jpeg|png|webp|svg|pdf|mp4|xml|txt|ico|json)$", re.I)
    for r, html in pages.items():
        if 'http-equiv="refresh"' in html:
            continue
        # Both site-absolute links and bare same-page fragments. The bare "#id"
        # form was missed originally because this pattern required a leading
        # slash - which let a sub-nav link at a non-existent anchor ship.
        for href in set(re.findall(r'href="((?:/|#)[^"]*)"', html)):
            path, _, frag = href.partition("#")
            path = path or r
            if asset_re.search(path):
                continue
            if not path.endswith("/") and path != "/404.html":
                no_slash.append((r, href))
            elif path not in routes:
                bad_link.append((r, href))
            elif path in redirects:
                to_redirect.append((r, href))
            elif frag and frag not in ids.get(path, set()):
                bad_frag.append((r, href))

    # --- referenced assets exist ------------------------------------------
    missing = defaultdict(set)
    for r, html in pages.items():
        for a in re.findall(
            r'(?:src|href|content|poster|srcset)="(?:https://alturascope\.com)?(/[^"\s]+\.(?:jpg|jpeg|png|webp|mp4|pdf))',
            html,
        ):
            if not os.path.exists(DIST + a):
                missing[a].add(r)

    # --- LCP: a page should not lazy-load its own first image -------------
    lazy_hero = []
    for r, html in pages.items():
        body = html.split("<body", 1)[-1]
        body = re.sub(r"<header[\s\S]*?</header>", "", body)
        # Only the first section counts. A page with a text-only hero has its
        # first image far below the fold, where lazy loading is correct - the
        # original check flagged those as failures.
        first_section = body.split("</section>", 1)[0]
        m = re.search(r"<img[^>]*>", first_section)
        if m and 'loading="lazy"' in m.group(0):
            lazy_hero.append(r)

    # --- orphans: indexable pages nothing links to ------------------------
    inbound = defaultdict(set)
    for r, html in pages.items():
        b = re.sub(r"<footer[\s\S]*?</footer>", "", html.split("<body", 1)[-1])
        b = re.sub(r"<header[\s\S]*?</header>", "", b)
        b = re.sub(r'<div id="mobile-overlay"[\s\S]*?</nav>', "", b)
        for href in set(re.findall(r'href="(/[^"#?]*)"', b)):
            inbound[href].add(r)
    orphans = []
    for r, html in pages.items():
        if r in ("/404.html", "/") or "noindex" in html or 'http-equiv="refresh"' in html:
            continue
        chrome = f'href="{r}"' in "".join(
            re.findall(r"<footer[\s\S]*?</footer>|<header[\s\S]*?</header>", pages["/"])
        )
        if not inbound.get(r) and not chrome:
            orphans.append(r)

    # --- report -----------------------------------------------------------
    print(f"\n  {len(pages)} pages in dist/\n")

    def check(label, items, fmt=lambda x: str(x), fatal=True, limit=10):
        if items:
            print(f"  FAIL  {label}: {len(items)}")
            for it in list(items)[:limit]:
                print(f"          {fmt(it)}")
            if len(items) > limit:
                print(f"          ... and {len(items) - limit} more")
            (failures if fatal else notes).append(label)
        else:
            print(f"  ok    {label}")

    pair = lambda t: f"{t[0]} -> {t[1]}"
    check("no broken internal links", bad_link, pair)
    check("no links missing a trailing slash", no_slash, pair)
    check("no dead fragments", bad_frag, pair)
    check("no missing image or media assets", sorted(missing),
          lambda a: f"{a}  (from {len(missing[a])} page(s))")
    check("no page lazy-loads its own hero image", lazy_hero)
    check("no internal links pointing at a redirect", to_redirect, pair)
    check("no orphan pages", orphans, fatal=False)

    total_img = sum(
        os.path.getsize(f)
        for e in ("jpg", "jpeg", "png", "webp")
        for f in glob.glob(f"{DIST}/**/*.{e}", recursive=True)
    )
    print(f"\n  image payload: {total_img/1048576:.2f} MB")

    if failures:
        print(f"\n  {len(failures)} check(s) failed\n")
        return 1
    if notes:
        print(f"\n  passed, with {len(notes)} advisory note(s)\n")
    else:
        print("\n  all checks passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
