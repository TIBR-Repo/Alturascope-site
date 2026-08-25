#!/usr/bin/env python3
"""Static SEO / integrity audit over dist/. Run after `npm run build`.

Checks: title + description presence and length, canonical correctness,
duplicate titles/descriptions, H1 count, JSON-LD validity, image alt text,
internal link resolution + trailing slashes, hreflang reciprocity,
sitemap coverage.
"""
import json
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist")
SITE = "https://alturascope.com"

errors = []
warnings = []
info = []


def err(page, msg):
    errors.append("%-46s %s" % (page, msg))


def warn(page, msg):
    warnings.append("%-46s %s" % (page, msg))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.description = None
        self.canonical = None
        self.robots = None
        self.og = {}
        self.h1s = []
        self._in_h1 = False
        self._h1_buf = []
        self.images = []
        self.links = []
        self.hreflang = []
        self.jsonld_raw = []
        self._in_ld = False
        self._ld_buf = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            prop = (a.get("property") or "").lower()
            if name == "description":
                self.description = a.get("content", "")
            elif name == "robots":
                self.robots = a.get("content", "")
            elif prop.startswith("og:"):
                self.og[prop] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a.get("href", "")))
        elif tag == "h1":
            self._in_h1 = True
            self._h1_buf = []
        elif tag == "img":
            self.images.append(a)
        elif tag == "a":
            if a.get("href"):
                self.links.append(a["href"])
        elif tag == "script" and (a.get("type") or "") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            if self._in_h1:
                self.h1s.append("".join(self._h1_buf).strip())
            self._in_h1 = False
        elif tag == "script" and self._in_ld:
            self.jsonld_raw.append("".join(self._ld_buf))
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_h1:
            self._h1_buf.append(data)
        if self._in_ld:
            self._ld_buf.append(data)


def route_for(path):
    rel = os.path.relpath(path, DIST).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def main():
    if not os.path.isdir(DIST):
        print("dist/ not found — run `npm run build` first")
        return 1

    pages = {}
    for root, _dirs, files in os.walk(DIST):
        for f in files:
            if f.endswith(".html"):
                full = os.path.join(root, f)
                route = route_for(full)
                p = Page()
                with open(full, encoding="utf-8") as fh:
                    p.feed(fh.read())
                pages[route] = p

    routes = set(pages.keys())
    titles = defaultdict(list)
    descs = defaultdict(list)

    for route, p in sorted(pages.items()):
        is404 = route == "/404.html"

        # --- title ---
        t = (p.title or "").strip()
        if not t:
            err(route, "MISSING <title>")
        else:
            titles[t].append(route)
            if len(t) > 62 and not is404:
                warn(route, "title %d chars (>62): %s" % (len(t), t))

        # --- description ---
        d = (p.description or "").strip()
        if not d:
            err(route, "MISSING meta description")
        else:
            descs[d].append(route)
            if not is404:
                if len(d) > 160:
                    warn(route, "description %d chars (>160)" % len(d))
                elif len(d) < 70:
                    warn(route, "description %d chars (<70)" % len(d))

        # --- canonical ---
        if is404:
            pass
        elif not p.canonical:
            err(route, "MISSING canonical")
        else:
            expected = SITE + route
            if p.canonical.rstrip("/") + "/" != expected.rstrip("/") + "/":
                err(route, "canonical mismatch: %s != %s" % (p.canonical, expected))

        # --- h1 ---
        if not is404:
            if len(p.h1s) == 0:
                err(route, "NO <h1>")
            elif len(p.h1s) > 1:
                err(route, "%d <h1> tags: %s" % (len(p.h1s), " | ".join(x[:40] for x in p.h1s)))

        # --- og ---
        for k in ("og:title", "og:description", "og:image", "og:url"):
            if k not in p.og or not p.og[k]:
                warn(route, "missing %s" % k)

        # --- json-ld ---
        for i, raw in enumerate(p.jsonld_raw):
            try:
                obj = json.loads(raw)
            except Exception as e:
                err(route, "JSON-LD block %d invalid: %s" % (i, e))
                continue
            if "@context" not in obj:
                err(route, "JSON-LD block %d missing @context" % i)
            # A @graph node array is valid JSON-LD; each member carries its own @type.
            if "@graph" in obj:
                graph = obj["@graph"]
                if not isinstance(graph, list) or not graph:
                    err(route, "JSON-LD block %d has an empty or malformed @graph" % i)
                else:
                    for j, node in enumerate(graph):
                        if not isinstance(node, dict) or "@type" not in node:
                            err(route, "JSON-LD block %d @graph node %d missing @type" % (i, j))
            elif "@type" not in obj:
                err(route, "JSON-LD block %d missing @type" % i)

        # --- images ---
        for img in p.images:
            if "alt" not in img:
                err(route, "img without alt attr: %s" % img.get("src", "?"))
            elif not img["alt"].strip():
                warn(route, "img with empty alt: %s" % img.get("src", "?"))

        # --- links ---
        for href in p.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            if not href.startswith("/"):
                warn(route, "relative link (not root-absolute): %s" % href)
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if re.search(r"\.(jpg|jpeg|png|svg|webp|pdf|xml|txt|ico)$", target, re.I):
                if not os.path.exists(os.path.join(DIST, target.lstrip("/").replace("/", os.sep))):
                    err(route, "asset link 404: %s" % target)
                continue
            if not target.endswith("/"):
                err(route, "internal link missing trailing slash: %s" % href)
                target = target + "/"
            if target not in routes:
                err(route, "internal link 404: %s" % href)
            # fragment target check
            if "#" in href:
                frag = href.split("#", 1)[1]
                tp = pages.get(target)
                if tp is not None and frag:
                    with open(
                        os.path.join(DIST, target.strip("/").replace("/", os.sep), "index.html")
                        if target != "/"
                        else os.path.join(DIST, "index.html"),
                        encoding="utf-8",
                    ) as fh:
                        body = fh.read()
                    if ('id="%s"' % frag) not in body:
                        err(route, "fragment target missing: %s" % href)

        # --- hreflang reciprocity ---
        for lang, href in p.hreflang:
            if not href.startswith(SITE):
                warn(route, "hreflang href not absolute site URL: %s" % href)
                continue
            tgt = href[len(SITE):]
            if tgt not in routes:
                err(route, "hreflang points at missing page: %s (%s)" % (href, lang))
                continue
            if lang == "x-default":
                continue
            back = pages[tgt].hreflang
            if not any(h == SITE + route for _l, h in back):
                err(route, "hreflang NOT reciprocal: %s says %s, but %s doesn't link back" % (route, tgt, tgt))

    # --- duplicates ---
    for t, rs in titles.items():
        if len(rs) > 1:
            err("(duplicate title)", "%s -> %s" % (t[:50], ", ".join(rs)))
    for d, rs in descs.items():
        if len(rs) > 1:
            err("(duplicate description)", "%s… -> %s" % (d[:45], ", ".join(rs)))

    # --- sitemap ---
    sm_urls = set()
    for f in os.listdir(DIST):
        if f.startswith("sitemap") and f.endswith(".xml"):
            with open(os.path.join(DIST, f), encoding="utf-8") as fh:
                sm_urls.update(re.findall(r"<loc>([^<]+)</loc>", fh.read()))
    for route in sorted(routes):
        if route == "/404.html":
            continue
        p = pages[route]
        if p.robots and "noindex" in p.robots:
            continue
        if SITE + route not in sm_urls:
            err(route, "NOT in sitemap")

    info.append("pages audited: %d" % len(pages))
    info.append("sitemap URLs: %d" % len([u for u in sm_urls if not u.endswith(".xml")]))

    print("=" * 78)
    for line in info:
        print("  " + line)
    print("=" * 78)
    if errors:
        print("\nERRORS (%d)\n" % len(errors))
        for e in errors:
            print("  " + e)
    if warnings:
        print("\nWARNINGS (%d)\n" % len(warnings))
        for w in warnings:
            print("  " + w)
    if not errors and not warnings:
        print("\n  clean\n")
    print()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
