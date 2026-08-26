"""Wire the survey side of the site to the Estimating Desk.

Audit finding: zero of 33 insight articles and zero of 28 service pages linked
to /estimating/ in body copy. The estimating pages therefore inherited none of
the site's internal authority, and a reader on a survey page was never offered
the obvious next thought.

This inserts the EstimatingBand component immediately before each page's
closing CTA, with a lead sentence written for that page's own subject.

Run once, then delete. Idempotent.
"""
import re
import sys

# page -> (locale, lead sentence)
TARGETS = {
    "src/pages/services/pre-construction-site-intelligence.astro": ("us",
        "Once you know what is actually there, the next question is what it costs to change."),
    "src/pages/services/construction-documentation.astro": ("us",
        "An as-built record answers what is there; a priced schedule answers what it costs to alter."),
    "src/pages/services/multi-site-rollout-documentation.astro": ("us",
        "A rollout is priced dozens of times, and the estimating capacity for that is usually the bottleneck, not the surveying."),
    "src/pages/services/retail-rollout-documentation.astro": ("us",
        "Store programmes are won and lost on how quickly a landlord package can be priced."),
    "src/pages/services/qsr-restaurant-survey.astro": ("us",
        "A reimage programme needs each unit priced as well as measured, usually against the same deadline."),
    "src/pages/services/commercial-kitchen-survey.astro": ("us",
        "Kitchen fit-outs carry the most equipment cost per square foot of anything we document."),
    "src/pages/services/healthcare-facility-survey.astro": ("us",
        "Clinical build-outs are priced against phasing and infection-control constraints that a drawing alone will not show."),
    "src/pages/services/aba-autism-clinic-documentation.astro": ("us",
        "Clinic operators opening several locations a year price the same build-out repeatedly."),
    "src/pages/services/industrial-facility-documentation.astro": ("us",
        "Industrial alterations are priced around plant that has to keep running."),
    "src/pages/services/self-storage-portfolio-documentation.astro": ("us",
        "Portfolio capex is a pricing exercise as much as a survey one."),
    "src/pages/services/heritage-building-documentation.astro": ("us",
        "Heritage work is priced on access, fabric and constraint rather than area."),
    "src/pages/services/specialist-projects.astro": ("us",
        "Specialist work rarely fits a price book, which is exactly when a traceable build-up matters."),
    "src/pages/uk/pre-construction-survey.astro": ("uk",
        "Once the existing conditions are recorded, the next question is what the works will cost."),
    "src/pages/uk/measured-building-survey.astro": ("uk",
        "A measured survey gives you the quantities; someone still has to price them."),
    "src/pages/uk/multi-site-rollout-survey.astro": ("uk",
        "A rollout means pricing the same shop fit repeatedly, to the same deadlines."),
    "src/pages/uk/heritage-building-survey.astro": ("uk",
        "Listed building work is priced on access, fabric and constraint rather than floor area."),
    "src/pages/uk/above-ceiling-mep-survey.astro": ("uk",
        "What is above the ceiling is usually what moves the mechanical and electrical price."),
}

BAND = '    <EstimatingBand locale="{locale}" lead="{lead}" />\n\n'


def import_line_for(path):
    depth = path.count("/") - 1  # src/pages/... -> how far up to src/
    prefix = "../" * depth
    return f'import EstimatingBand from "{prefix}components/EstimatingBand.astro";\n'


count = 0
for path, (locale, lead) in TARGETS.items():
    src = open(path, encoding="utf-8").read()
    if "EstimatingBand" in src:
        print(f"  {path}: already linked, skipping")
        continue

    if "SpecialtyPage" in src:
        # These render through the shared component, which carries the band itself.
        print(f"  {path}: uses SpecialtyPage, handled in the component")
        continue

    # add the import directly after the Layout import
    m = re.search(r'^import Layout from "[^"]+";\n', src, re.M)
    if not m:
        sys.exit(f"no Layout import in {path}")
    src = src[: m.end()] + import_line_for(path) + src[m.end():]

    band = BAND.format(locale=locale, lead=lead.replace('"', "&quot;"))

    # insert before the closing CTA where there is one, otherwise before </Layout>
    anchor = re.search(r'\n(    <!-- CTA[^\n]*-->\n)', src)
    if anchor:
        src = src[: anchor.start() + 1] + band + src[anchor.start() + 1:]
    else:
        close = src.rindex("  </div>\n</Layout>")
        src = src[:close] + band + src[close:]

    open(path, "w", encoding="utf-8").write(src)
    count += 1
    print(f"  {path}: band added ({locale})")

print(f"\n  {count} pages now link to the Estimating Desk in body copy")
