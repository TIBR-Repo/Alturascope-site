"""Rewrite the money pages in the buyer's language, not ours.

Search Console showed the problem in one line: "compare fit-out firms for qsr
rollouts" put us at position 3.6 - page one, someone actively shortlisting
vendors - with zero clicks. What they saw was a result titled "Multi-Site
Rollout Site Documentation", which does not read as a firm you can hire to
survey a fit-out.

The Joe & The Juice deliverable settled what the product actually is: a
pre-fit-out due diligence report for a property director deciding whether a
second-generation space is worth signing. Nobody in that role searches for
"reality capture", "site intelligence" or "documentation". They search for
existing conditions surveys, as-built surveys, and second-generation space.

Titles stay inside 62 characters. Every replacement keeps the page's primary
keyword and adds the term the buyer actually uses.

Run once, then delete. Idempotent.
"""
import html
import os
import re
import sys

# path -> (title, meta description, h1 replacement or None)
CHANGES = {
    "index.astro": (
        "Existing Conditions Surveys & Construction Estimating",
        "Existing conditions and as-built surveys for multi-site fit-out programmes, plus construction estimating. US, Canada and UK. One brief, one standard, every site.",
        "Know the building before you price the work.",
    ),
    "services/index.astro": (
        "Existing Conditions & As-Built Surveys | Alturascope",
        "Existing conditions surveys, as-built records and pre-lease due diligence for multi-site operators - and construction estimating from the same record.",
        "Surveys that answer what the building will cost you.",
    ),
    "services/multi-site-rollout-documentation.astro": (
        "Site Surveys for Multi-Site Rollout Programmes",
        "Existing conditions surveys across retail, QSR and franchise rollout programmes. One brief, one format, every location - so each site can be priced and designed.",
        "Site surveys for rollout programmes.",
    ),
    "services/pre-construction-site-intelligence.astro": (
        "Pre-Lease & Pre-Construction Due Diligence Surveys",
        "Know what you are signing for. Existing conditions, capacity and reuse assessed before the lease or the fit-out budget is committed.",
        "Pre-lease due diligence, before you commit the budget.",
    ),
    "services/construction-documentation.astro": (
        "As-Built Surveys & Existing Conditions Records",
        "As-built surveys and existing conditions records for commercial buildings - measured, photographed and structured so design and pricing start from fact.",
        "As-built surveys and existing conditions records.",
    ),
    "services/qsr-restaurant-survey.astro": (
        "Restaurant & QSR Existing Conditions Surveys",
        "Existing conditions surveys for QSR and restaurant remodel programmes. Kitchen equipment, grease interception, MEP capacity and reuse - site by site.",
        "Existing conditions surveys for restaurant remodels.",
    ),
    "services/retail-rollout-documentation.astro": (
        "Retail Fit-Out & Remodel Existing Conditions Surveys",
        "Existing conditions surveys for retail remodel, rebrand and expansion programmes - the same record at every location, ready to design and price from.",
        "Existing conditions surveys for retail fit-out.",
    ),
    "services/aba-autism-clinic-documentation.astro": (
        "ABA Clinic Existing Conditions & Fit-Out Surveys",
        "Existing conditions surveys for ABA and autism therapy clinics - acoustic separation, sensory-room provision, HVAC and MEP capacity, checked before design.",
        None,
    ),
    "work.astro": (
        "What an Alturascope Survey Actually Delivers",
        "What arrives after a survey: a navigable record, a written conditions report, equipment and capacity schedules, and the drawings your team can design from.",
        "This is what you receive.",
    ),
}

TITLE = re.compile(r'(\btitle=)"((?:[^"\\]|\\.)*)"')
DESC = re.compile(r'(\bdescription=)"((?:[^"\\]|\\.)*)"')
H1 = re.compile(r'(<h1[^>]*>)([\s\S]*?)(</h1>)')

over = [(p, len(t)) for p, (t, _, _) in CHANGES.items() if len(t) > 62]
if over:
    sys.exit("titles too long: " + repr(over))

changed = 0
for rel, (title, desc, h1) in CHANGES.items():
    path = os.path.join("src", "pages", *rel.split("/"))
    src = open(path, encoding="utf-8").read()
    before = src

    def enc(text, existing):
        return text.replace("&", "&amp;") if "&" in text else text

    m = TITLE.search(src)
    if m:
        src = src[: m.start(2)] + enc(title, m.group(2)) + src[m.end(2):]
    m = DESC.search(src)
    if m:
        src = src[: m.start(2)] + enc(desc, m.group(2)) + src[m.end(2):]
    if h1:
        m = H1.search(src)
        if m:
            src = src[: m.start(2)] + enc(h1, m.group(2)) + src[m.end(2):]

    if src != before:
        open(path, "w", encoding="utf-8").write(src)
        changed += 1
        print(f"  {rel}")
        print(f"     title ({len(title)}): {title}")
        if h1:
            print(f"     h1          : {h1}")

print(f"\n  {changed} pages rewritten in buyer language")
