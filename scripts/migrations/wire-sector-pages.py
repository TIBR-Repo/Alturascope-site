"""Wire the new sector pages in, and prune the ones we will never sell.

Five new sector pages exist but nothing links to them, which makes them
orphans. At the same time the site carries 28 service pages spanning
superyachts, private aircraft, solar farms and private art collections - most
with one inbound link and no prospect of a sale. They are not neutral: they
dilute what Google understands the site to be about and compete with the pages
that need to win.

The fantasy pages fold into /services/specialist-projects/, which already
exists for exactly this purpose, via 301s configured in astro.config.mjs. The
data centre service page goes too - the sector is dropped - but the data centre
*article* stays, because it is the single highest-impression page on the site.

Run once, then delete. Idempotent.
"""
import os
import re
import sys

HUB = "src/pages/services/index.astro"
LAYOUT = "src/layouts/Layout.astro"

NEW_CARDS = '''
          <a href="/services/veterinary-clinic-survey/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">VETERINARY</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Veterinary Practice Surveys</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Imaging shielding, kennel drainage, isolation ventilation and the electrical capacity to run it &mdash; across acquired practices nobody ever documented.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/dental-practice-survey/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">DENTAL &amp; DSO</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Dental Practice Surveys</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Chair services, compressed air and vacuum, panel capacity and what is really in the slab &mdash; before the operatory count is fixed.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/medical-aesthetics-clinic-survey/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">MED SPA &amp; AESTHETICS</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Med Spa &amp; Aesthetics Clinics</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Device power, treatment-room plumbing, plume extraction and laser-safe layout &mdash; tested against the unit before the lease is signed.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/behavioral-health-clinic-survey/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">BEHAVIORAL HEALTH</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Behavioral Health &amp; Treatment Clinics</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Ligature risk in the existing fabric, observation sightlines, acoustic confidentiality and separated circulation.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/fitness-studio-survey/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">FITNESS &amp; STUDIO</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Fitness &amp; Boutique Studios</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Floor loading, impact noise to the tenancy below, and clear height measured under the services rather than to the slab.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/cannabis-facility-documentation/" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">CANNABIS</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Dispensary &amp; Cultivation Surveys</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Electrical capacity, dehumidification, odour discharge and limited-access separation &mdash; before the licence clock starts.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>
'''

# --- 1. add the cards to the services hub --------------------------------
src = open(HUB, encoding="utf-8").read()
if "veterinary-clinic-survey" in src:
    print(f"  {HUB}: already wired")
else:
    anchor = '        </div>\n      </div>\n    </section>\n\n    <!-- Specialist Work -->'
    if anchor not in src:
        sys.exit("services hub sector-card block not found")
    src = src.replace(anchor, NEW_CARDS + anchor, 1)
    # the grid was built for four; let it wrap at three so ten cards read evenly
    src = src.replace(
        'class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"',
        'class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"', 1)
    open(HUB, "w", encoding="utf-8").write(src)
    print(f"  {HUB}: 6 sector cards added, grid set to 3 columns")

# --- 2. rebuild the footer Sectors column --------------------------------
src = open(LAYOUT, encoding="utf-8").read()
if "veterinary-clinic-survey" in src:
    print(f"  {LAYOUT}: already wired")
else:
    old = re.search(
        r'(<h4[^>]*>Sectors</h4>\s*<nav[^>]*>)([\s\S]*?)(</nav>)', src)
    if not old:
        sys.exit("footer Sectors column not found")
    links = [
        ("/services/qsr-restaurant-survey/", "QSR &amp; Restaurant"),
        ("/services/aba-autism-clinic-documentation/", "ABA &amp; Autism Therapy"),
        ("/services/veterinary-clinic-survey/", "Veterinary"),
        ("/services/dental-practice-survey/", "Dental &amp; DSO"),
        ("/services/medical-aesthetics-clinic-survey/", "Med Spa &amp; Aesthetics"),
        ("/services/behavioral-health-clinic-survey/", "Behavioral Health"),
        ("/services/fitness-studio-survey/", "Fitness &amp; Studio"),
        ("/services/cannabis-facility-documentation/", "Cannabis"),
        ("/services/retail-rollout-documentation/", "Retail &amp; Franchise"),
        ("/services/healthcare-facility-survey/", "Healthcare"),
        ("/services/commercial-kitchen-survey/", "Commercial Kitchens"),
    ]
    body = "\n" + "\n".join(
        f'                <a href="{h}" class="text-sm text-white/70 hover:text-white transition-colors">{t}</a>'
        for h, t in links) + "\n              "
    src = src[:old.start(2)] + body + src[old.end(2):]
    open(LAYOUT, "w", encoding="utf-8").write(src)
    print(f"  {LAYOUT}: footer Sectors column rebuilt around the target sectors")

# --- 3. prune, with 301s ---------------------------------------------------
PRUNE = [
    "superyacht-documentation", "private-aircraft-documentation",
    "private-collection-documentation", "private-estate-documentation",
    "film-tv-location-documentation", "solar-farm-documentation",
    "aviation-facility-survey", "resort-hotel-capex-survey",
    "data-centre-documentation",
]
removed = []
for slug in PRUNE:
    p = f"src/pages/services/{slug}.astro"
    if os.path.exists(p):
        os.remove(p)
        removed.append(slug)
print(f"\n  {len(removed)} service pages removed: {', '.join(removed) if removed else '(already gone)'}")

cfg = open("astro.config.mjs", encoding="utf-8").read()
if "superyacht-documentation" not in cfg:
    entries = "\n".join(
        f"    '/services/{s}/': '/services/specialist-projects/',"
        for s in PRUNE if s != "data-centre-documentation")
    entries += "\n    // The sector is dropped, but the data centre *article* stays - it is the\n"
    entries += "    // single highest-impression page on the site (233 impressions, position 20.9).\n"
    entries += "    '/services/data-centre-documentation/': '/services/industrial-facility-documentation/',"
    cfg = cfg.replace(
        "  redirects: {\n",
        "  redirects: {\n"
        "    // Pruned Aug 2026: 28 service pages spanning superyachts, private aircraft,\n"
        "    // solar farms and art collections diluted what the site is about and\n"
        "    // competed with the sectors we actually sell. Folded into the page that\n"
        "    // already exists for exactly this work.\n" + entries + "\n", 1)
    open("astro.config.mjs", "w", encoding="utf-8").write(cfg)
    print("  astro.config.mjs: 9 redirects added")
else:
    print("  astro.config.mjs: redirects already present")
