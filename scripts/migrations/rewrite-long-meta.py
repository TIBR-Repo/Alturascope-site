"""Hand-written replacements for the meta the automated pass could not fix.

The conservative pass in tighten-meta.py cleared everything with a usable
sentence boundary. What remained were single long sentences, which cannot be
trimmed without breaking grammar, and article titles that were long even after
the brand suffix came off.

Each replacement below keeps the page's primary keyword in the opening clause.
Titles are only shortened where they ran past ~78 characters; anything in the
60s displays nearly in full and is left as it is.
"""
import html
import re
import sys
import glob
import os

DESCRIPTIONS = {
    "contact.astro":
        "Share the address, the size and what you need to decide. We reply within one business day with a scope recommendation and an all-in quote, travel included.",
    "insights/aba-clinic-portfolio-renovation-documentation.astro":
        "PE-backed ABA platforms acquire clinics faster than they can standardise them. Consistent documentation turns inherited property into a renovation programme.",
    "insights/aba-clinic-sensory-room-design-documentation.astro":
        "Sensory rooms are the most design-sensitive spaces in an ABA clinic. What to document before fit-out, to avoid rework and meet licensing requirements.",
    "insights/above-ceiling-mep-survey-fit-out.astro":
        "Hidden ductwork, undocumented pipework and uncharted electrical runs cause the most expensive surprises in fit-out. How to find out what is up there first.",
    "insights/data-centre-survey-uk-expansion-compliance.astro":
        "What UK facilities directors and design consultants need from a site survey before a data centre expansion, retrofit or compliance exercise begins.",
    "insights/documenting-controlled-environments-precision-facilities.astro":
        "Cannabis grow rooms, data centres and cleanrooms need documentation that captures environmental systems and compliance infrastructure, not just the space.",
    "insights/estimating-capacity-limits-contractor-growth.astro":
        "The bids you declined for lack of hours never reach the accounts. How to put a number on them, and the four ways contractors fix the constraint.",
    "insights/healthcare-multi-site-facility-survey-documentation.astro":
        "Dental, urgent care, veterinary and medical office programmes face documentation problems a standard survey cannot solve. What multi-site operators need.",
    "insights/how-to-check-a-construction-estimate.astro":
        "Estimates fail through omission, not arithmetic. Six checks in under an hour, ordered by how much money each one tends to save.",
    "insights/point-cloud-as-built-survey-architects-engineers.astro":
        "The difference between a navigable digital twin and a survey-grade point cloud, and when a design team actually needs each one.",
    "insights/qsr-franchise-kitchen-equipment-documentation.astro":
        "QSR remodel programmes depend on accurate kitchen equipment data from every site. What thorough documentation captures that a walk-through misses.",
    "insights/qsr-reimage-pre-construction-survey-timelines.astro":
        "Restaurant reimage programmes lose days to undocumented conditions. How pre-construction survey data removes the surprises that extend dark time.",
    "insights/site-documentation-heritage-complex-specialist-buildings.astro":
        "Heritage properties, listed buildings and complex industrial spaces do not fit the standard survey template. What a different approach looks like.",
    "insights/uk-retail-high-street-refurbishment-survey.astro":
        "UK retailers running refurbishment and rebrand programmes across high street, retail park and shopping centre sites need consistent measured survey data.",
    "insights/what-is-a-basis-of-estimate.astro":
        "A basis of estimate states what a price was built from and what it assumes. What belongs in one, why it protects margin, and how to hold an estimate to it.",
    "insights/what-should-a-professional-site-survey-include.astro":
        "Before you commission a survey, here is what a professional package should deliver and the questions worth asking any provider.",
    "services/aviation-facility-survey.astro":
        "Site documentation for hangars, terminals, MRO facilities and airside infrastructure, where dimensional precision is non-negotiable.",
    "services/commercial-kitchen-survey.astro":
        "Conditions documentation and equipment schedules for commercial kitchens. MEP records, fixture inventories and Matterport capture for fit-out and remodel.",
    "services/film-tv-location-documentation.astro":
        "Matterport digital twins and measured documentation for film and television locations, so production can plan and prep without repeated site visits.",
    "services/heritage-building-documentation.astro":
        "Millimetre-accurate LiDAR and Matterport documentation for listed buildings, historic structures and conservation projects across the US, Canada and UK.",
    "services/index.astro":
        "Matterport digital twins, MEP documentation and LiDAR point clouds - the deliverables your team needs to decide before setting foot on site.",
    "services/multi-site-rollout-documentation.astro":
        "One brief, one standard, every location. Survey programmes for QSR operators, franchise groups and PE-backed retail rollouts across North America and the UK.",
    "services/pre-construction-site-intelligence.astro":
        "A survey should tell you more than dimensions. Conditions, equipment, services and thermal analysis, so your team decides from complete information.",
    "services/private-aircraft-documentation.astro":
        "Structured 3D documentation, thermal imaging and condition records for private aircraft - pre-purchase surveys and asset records for owners and buyers.",
    "services/private-collection-documentation.astro":
        "Discreet, precise documentation of private collections and high-value assets. Matterport capture and structured inventories for insurance and estate work.",
    "services/qsr-restaurant-survey.astro":
        "Pre-construction surveys for QSR and restaurant remodel programmes: equipment schedules, conditions reports, above-ceiling MEP and Matterport twins.",
    "services/retail-rollout-documentation.astro":
        "Conditions surveys, equipment schedules and Matterport digital twins for retail remodel, rebrand and expansion programmes - consistent at every location.",
    "services/specialist-projects.astro":
        "Complex environments and sensitive briefs. Heritage buildings, aviation facilities, superyachts and resorts - where the standard approach will not do.",
    "services/superyacht-documentation.astro":
        "LiDAR scanning and reality capture for superyachts, vessels and marine facilities. As-built documentation for refit planning and interior design.",
    "uk/above-ceiling-mep-survey.astro":
        "Non-invasive above-ceiling MEP documentation for UK fit-out: thermal imaging, pole-mounted 360 capture and borescope inspection, before design is committed.",
    "work/locations.astro":
        "A sample of commercial sites documented by Alturascope - retail, office, mall and transport locations, each captured as a navigable digital twin.",
}

TITLES = {
    "insights/aba-clinic-portfolio-renovation-documentation.astro":
        "ABA Clinic Portfolio Renovation: Standardising Documentation",
    "insights/documenting-controlled-environments-precision-facilities.astro":
        "Documenting Cannabis Facilities, Data Centres & Cleanrooms",
    "insights/due-diligence-documentation-portfolio-acquisitions.astro":
        "Due Diligence Documentation for Portfolio Acquisitions",
    "insights/fashion-retail-store-refit-survey-documentation.astro":
        "Fashion Retail Store Surveys Before a Brand-Wide Refit",
    "insights/franchise-expansion-shell-survey-new-locations.astro":
        "Franchise Expansion Shell Surveys: Pre-Lease Documentation",
    "insights/healthcare-multi-site-facility-survey-documentation.astro":
        "Healthcare Multi-Site Surveys: Dental, Urgent Care & Medical",
    "insights/point-cloud-as-built-survey-architects-engineers.astro":
        "Point Cloud Surveys & As-Built Documentation for Design Teams",
    "insights/site-documentation-heritage-complex-specialist-buildings.astro":
        "Site Documentation for Heritage & Specialist Buildings",
    "insights/standardising-site-surveys-multi-site-operators.astro":
        "How Multi-Site Operators Standardise Site Surveys",
    "services/aba-autism-clinic-documentation.astro":
        "ABA & Autism Therapy Clinic Documentation & Site Surveys",
}

# sanity-check the copy before touching a file
bad = [(k, len(v)) for k, v in DESCRIPTIONS.items() if len(v) > 158]
bad += [(k, len(v)) for k, v in TITLES.items() if len(v) > 62]
if bad:
    for k, n in bad:
        print(f"  TOO LONG ({n}): {k}")
    sys.exit("fix the copy above before running")


def swap(path, attr, new):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'\b' + attr + r'="((?:[^"\\]|\\.)*)"', src)
    if not m:
        return False, "attribute not found"
    old_raw = m.group(1)
    # preserve the entity style already in the file
    new_raw = new.replace("&", "&amp;") if "&amp;" in old_raw or "&" in new else new
    if new_raw == old_raw:
        return False, "unchanged"
    out = src[: m.start(1)] + new_raw + src[m.end(1):]
    open(path, "w", encoding="utf-8").write(out)
    return True, html.unescape(old_raw)


nd = nt = 0
for rel, new in DESCRIPTIONS.items():
    p = os.path.join("src", "pages", *rel.split("/"))
    ok, note = swap(p, "description", new)
    if ok:
        nd += 1
    else:
        print(f"  description skipped ({note}): {rel}")

for rel, new in TITLES.items():
    p = os.path.join("src", "pages", *rel.split("/"))
    ok, note = swap(p, "title", new)
    if ok:
        nt += 1
    else:
        print(f"  title skipped ({note}): {rel}")

print(f"\n  {nd} descriptions and {nt} titles rewritten by hand")
