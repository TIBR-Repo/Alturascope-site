"""Prune articles Google crawled and declined to index (audit 2026-10-26).

Each pruned URL is deleted, gets an Astro redirect (plus a real nginx 301 -
see docs/deployment/redirects.md), drops out of the /insights/ listing, and
has its inbound links handled:
  - a "related" list item (an <a> ending in &rarr; on its own line) is removed,
    because repointing it would usually duplicate a sibling link;
  - an inline prose link is repointed at the redirect target, or unwrapped to
    plain text when the target is the page doing the linking.

Run once from the repo root: python scripts/migrations/prune-unindexed-2026-10.py
"""
import pathlib, re

PRUNE = {
    "/insights/aba-clinic-portfolio-renovation-documentation/": "/insights/aba-multi-location-growth-documentation-strategy/",
    "/insights/convenience-fuel-retail-site-survey-rollout/": "/services/retail-rollout-documentation/",
    "/insights/data-center-documentation-expansion-retrofit/": "/insights/documenting-controlled-environments-precision-facilities/",
    "/insights/franchise-expansion-shell-survey-new-locations/": "/insights/second-generation-space-what-to-verify-before-you-sign/",
    "/insights/healthcare-multi-site-facility-survey-documentation/": "/services/healthcare-facility-survey/",
    "/insights/managing-multi-site-survey-programmes-at-scale/": "/insights/standardising-site-surveys-multi-site-operators/",
    "/insights/multi-site-brand-standard-compliance-documentation/": "/insights/standardising-site-surveys-multi-site-operators/",
    "/insights/point-cloud-as-built-survey-architects-engineers/": "/services/construction-documentation/",
    "/insights/qsr-franchise-kitchen-equipment-documentation/": "/insights/grease-power-water-food-unit-fit-out/",
    "/insights/self-storage-portfolio-site-survey-documentation/": "/insights/due-diligence-documentation-portfolio-acquisitions/",
    "/services/self-storage-portfolio-documentation/": "/services/specialist-projects/",
    "/insights/site-documentation-heritage-complex-specialist-buildings/": "/services/specialist-projects/",
    "/insights/uk-retail-high-street-refurbishment-survey/": "/uk/multi-site-rollout-survey/",
    "/insights/vehicle-dealership-renovation-site-survey/": "/services/retail-rollout-documentation/",
    "/insights/why-poor-site-documentation-costs-construction-projects/": "/insights/what-should-a-professional-site-survey-include/",
}

root = pathlib.Path(".")
pages = root / "src" / "pages"

def page_url(p):
    rel = p.relative_to(pages).with_suffix("").as_posix()
    if rel.endswith("index"):
        rel = rel[: -len("index")]
    return "/" + (rel + "/" if rel and not rel.endswith("/") else rel)

for old in PRUNE:
    f = pages / (old.strip("/") + ".astro")
    if f.exists():
        f.unlink()
        print("deleted", f)

idx = pages / "insights" / "index.astro"
x = idx.read_text(encoding="utf-8")
for old in PRUNE:
    x, n = re.subn(r"\n\s*\{[^{}]*?href:\s*\"" + re.escape(old) + r"\"[^{}]*?\},?", "", x)
    if n:
        print("listing removed", old)
idx.write_text(x, encoding="utf-8")

for f in list(pages.rglob("*.astro")) + list((root / "src" / "components").rglob("*.astro")) + list((root / "src" / "data").rglob("*.json")):
    if f == idx:
        continue
    x = f.read_text(encoding="utf-8")
    orig = x
    me = page_url(f) if pages in f.parents else None
    for old, new in PRUNE.items():
        x = re.sub(r"\n[ \t]*<a href=\"" + re.escape(old) + r"\"[^>]*>[^<]*&rarr;</a>[ \t]*(?=\n)", "", x)
        def repl(m):
            if new == me:
                return m.group(2)
            return m.group(0).replace(old, new, 1)
        x = re.sub(r"(<a href=\"" + re.escape(old) + r"\"[^>]*>)(.*?)</a>", repl, x, flags=re.S)
        x = x.replace('"' + old + '"', '"' + new + '"')
    if x != orig:
        f.write_text(x, encoding="utf-8")
        print("relinked", f)
