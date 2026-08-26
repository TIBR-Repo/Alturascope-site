"""Put Alturascope's own photography on the service pages.

Audit finding: 50 of 83 pages pulled hero imagery from images.unsplash.com -
134 references to an external CDN with no preconnect - including the UK home
page, /work/ and /services/. A surveying firm illustrated with photographs of
buildings it has never been inside is a credibility problem before it is a
performance one, and roughly twenty real, unused survey images already sat in
the repo.

Service and UK pages get real work. Insight articles keep editorial variety
but are self-hosted (handled separately) so nothing leaves the origin.

Verified real before use. Deliberately NOT used: heritage-building-work.jpg
(AI-generated - the brickwork and mortar do not survive inspection),
report-image.jpg and presentation-1.jpg (lorem ipsum and invented figures).

Run once, then delete. Idempotent.
"""
import re
import sys

# page slug -> (image, alt, width, height)
HEROES = {
    "services/aba-autism-clinic-documentation": (
        "/pre-construction-survey.jpg",
        "Vacant clinic suite documented before an ABA therapy build-out, showing ceiling grid, partitions and existing services",
        1920, 1440),
    "services/aviation-facility-survey": (
        "/Images/site-interior-2.jpg",
        "Aerial orthographic survey of a large facility roof and rooftop plant captured by Alturascope",
        1920, 1080),
    "services/cannabis-facility-documentation": (
        "/Images/hvac.jpg",
        "Exposed mechanical services and structure in a controlled-environment facility documented by Alturascope",
        1920, 1440),
    "services/central-us-site-surveys": (
        "/Images/drone-shot-1.jpg",
        "Aerial orthographic view of a commercial building and its site, captured during an Alturascope survey",
        1600, 900),
    "services/commercial-kitchen-survey": (
        "/commercial-kitchen-work.jpg",
        "Commercial kitchen line documented by Alturascope, showing fryers, holding units and extract canopy",
        1280, 720),
    "services/construction-documentation": (
        "/Images/construction.jpg",
        "Commercial building interior during construction, documented by Alturascope for the as-built record",
        1600, 1245),
    "services/data-centre-documentation": (
        "/above-ceiling-survey.jpg",
        "Structural deck, containment and distribution above the ceiling line, documented by Alturascope",
        1920, 1451),
    "services/education-campus-documentation": (
        "/Images/site-interior-1.jpg",
        "Aerial orthographic survey of a campus building roof, showing plant, membrane condition and the surrounding site",
        1600, 1205),
    "services/film-tv-location-documentation": (
        "/Images/site-inside.jpg",
        "Interior of a commercial space documented by Alturascope as a navigable digital twin for location scouting",
        1600, 1200),
    "services/healthcare-facility-survey": (
        "/pre-construction-survey.jpg",
        "Clinical suite documented before fit-out, showing ceiling grid, partitions and existing service routes",
        1920, 1440),
    "services/industrial-facility-documentation": (
        "/Images/site-interior-2.jpg",
        "Aerial orthographic survey of an industrial facility roof, rooftop plant and loading yard",
        1920, 1080),
    "services/insurance-loss-documentation": (
        "/Images/attic.jpg",
        "Roof void documented by Alturascope, showing trusses, insulation and ductwork above the ceiling line",
        1920, 1440),
    "services/multi-site-rollout-documentation": (
        "/Images/drone-shot-1.jpg",
        "Aerial orthographic view of a retail unit and its car park, captured during a multi-site survey programme",
        1600, 900),
    "services/northeast-site-surveys": (
        "/Images/site-interior-1.jpg",
        "Aerial orthographic survey of a commercial roof captured by Alturascope in the northeastern United States",
        1600, 1205),
    "services/pre-construction-site-intelligence": (
        "/pre-construction-survey.jpg",
        "Vacant commercial unit documented before fit-out, showing ceiling grid, structure above and existing finishes",
        1920, 1440),
    "services/private-aircraft-documentation": (
        "/Images/site-interior-2.jpg",
        "Aerial orthographic survey of a hangar roof and apron captured by Alturascope",
        1920, 1080),
    "services/qsr-restaurant-survey": (
        "/commercial-kitchen-work.jpg",
        "Quick-service restaurant kitchen line documented by Alturascope ahead of a reimage programme",
        1280, 720),
    "services/retail-rollout-documentation": (
        "/pre-construction-survey.jpg",
        "Vacant retail unit documented by Alturascope before a rollout fit-out begins",
        1920, 1440),
    "services/self-storage-portfolio-documentation": (
        "/Images/site-interior-2.jpg",
        "Aerial orthographic survey of a storage facility roof and site captured by Alturascope",
        1920, 1080),
    "services/solar-farm-documentation": (
        "/Images/drone-shot-1.jpg",
        "Aerial orthographic capture of a site and its roof-mounted plant, documented by Alturascope",
        1600, 900),
    "services/southeast-site-surveys": (
        "/Images/construction.jpg",
        "Commercial interior under construction, documented by Alturascope in the southeastern United States",
        1600, 1245),
    "services/specialist-projects": (
        "/Images/attic.jpg",
        "Roof void and structural timbers documented by Alturascope on a specialist survey",
        1920, 1440),
    "services/west-coast-site-surveys": (
        "/Images/drone-shot-1.jpg",
        "Aerial orthographic survey of a commercial site captured by Alturascope on the west coast",
        1600, 900),
    "uk/above-ceiling-mep-survey": (
        "/above-ceiling-survey.jpg",
        "Ductwork, conduit and structural deck above the ceiling line, documented on a UK above-ceiling MEP survey",
        1920, 1451),
    "uk/measured-building-survey": (
        "/Images/site-inside.jpg",
        "Commercial interior captured as survey-grade point cloud data during a UK measured building survey",
        1600, 1200),
    "uk/multi-site-rollout-survey": (
        "/pre-construction-survey.jpg",
        "Vacant retail unit documented before fit-out during a UK multi-site rollout survey programme",
        1920, 1440),
    "uk/pre-construction-survey": (
        "/Images/hvac.jpg",
        "Exposed services and structure in a commercial floor plate stripped for fit-out, documented on a UK pre-construction survey",
        1920, 1440),
}

changed = 0
for slug, (img, alt, w, h) in HEROES.items():
    path = f"src/pages/{slug}.astro"
    src = open(path, encoding="utf-8").read()

    m = re.search(r'(?:src|heroImage)=("https://images\.unsplash\.com/[^"]+")', src)
    if not m:
        print(f"  {path}: no stock hero (already real?)")
        continue

    attr = "heroImage" if "heroImage=" in src[max(0, m.start() - 12):m.end()] else "src"
    if attr == "heroImage":
        src = src[: m.start(1)] + f'"{img}"' + src[m.end(1):]
        # SpecialtyPage takes the alt through its own prop
        src = re.sub(r'heroAlt="[^"]*"', f'heroAlt="{alt}"', src, count=1)
    else:
        src = src[: m.start(1)] + f'"{img}"\n          width="{w}"\n          height="{h}"' + src[m.end(1):]
        # replace the alt on the same <img>
        after = src[m.start():]
        alt_m = re.search(r'alt="[^"]*"', after)
        if alt_m:
            s0 = m.start() + alt_m.start()
            s1 = m.start() + alt_m.end()
            src = src[:s0] + f'alt="{alt}"' + src[s1:]

    open(path, "w", encoding="utf-8").write(src)
    changed += 1
    print(f"  {slug}: {img}")

print(f"\n  {changed} service and UK heroes now use Alturascope's own photography")
