"""Give the hub pages schema types that describe what they actually are.

ProfessionalService was duplicated across /about/, /contact/, /insights/,
/services/ and /work/. Five pages all claiming to be the same service entity
muddies the entity picture; the Organization node in the layout is already the
canonical business record, so each page should say what the *page* is and
point back at that node.

The gallery declared CollectionPage but listed nothing - 26 captioned images
with real alt text and no ItemList telling a crawler what they were.

Run once, then delete. Idempotent.
"""
import json
import re
import sys

ORG = {"@id": "https://alturascope.com/#organization"}

PAGES = {
    "src/pages/about.astro": {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "About Alturascope",
        "description": "Who runs Alturascope, how the survey and estimating sides fit together, and the standard both are held to.",
        "url": "https://alturascope.com/about/",
        "isPartOf": ORG,
        "about": ORG,
    },
    "src/pages/contact.astro": {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Alturascope",
        "description": "Start a site documentation project or send a bid package to the Estimating Desk.",
        "url": "https://alturascope.com/contact/",
        "isPartOf": ORG,
    },
    "src/pages/insights/index.astro": {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Alturascope Insights",
        "description": "Writing on site documentation, reality capture and construction estimating for teams making decisions on existing buildings.",
        "url": "https://alturascope.com/insights/",
        "publisher": ORG,
    },
    "src/pages/services/index.astro": {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Site Documentation Services",
        "description": "Reality capture, as-built documentation, conditions surveys and multi-site programmes across the US, Canada and the UK.",
        "url": "https://alturascope.com/services/",
        "isPartOf": ORG,
    },
    "src/pages/work.astro": {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "The Standard",
        "description": "How an Alturascope survey runs, what instruments are used, and exactly what is delivered afterwards.",
        "url": "https://alturascope.com/work/",
        "isPartOf": ORG,
    },
}

block = re.compile(r'const schema = JSON\.stringify\(\{[\s\S]*?\n\}\);\n')

for path, obj in PAGES.items():
    src = open(path, encoding="utf-8").read()
    if not block.search(src):
        sys.exit(f"schema block not found in {path}")
    body = json.dumps(obj, indent=2)
    src = block.sub(f"const schema = JSON.stringify({body});\n", src, count=1)
    open(path, "w", encoding="utf-8").write(src)
    print(f"  {path}: @type -> {obj['@type']}")

# --- gallery: list what is actually in the collection -----------------------
path = "src/pages/work/locations.astro"
src = open(path, encoding="utf-8").read()
if "mainEntity" in src:
    print(f"  {path}: already has an ItemList")
else:
    addition = """
// Tell crawlers what the collection actually contains. Each entry is a real
// surveyed building, named by centre or street - never by occupier.
const itemListSchema = JSON.stringify({
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Commercial sites documented by Alturascope",
  "numberOfItems": locations.length,
  "itemListElement": locations.map((loc, i) => ({
    "@type": "ListItem",
    "position": i + 1,
    "item": {
      "@type": "ImageObject",
      "name": loc.label,
      "description": `${loc.kind} - commercial site documented by Alturascope as a Matterport digital twin`,
      "contentUrl": `https://alturascope.com/Images/locations/${loc.slug}.jpg`,
      "width": loc.w,
      "height": loc.h,
      "creator": { "@id": "https://alturascope.com/#organization" },
      "creditText": "Alturascope",
    },
  })),
});
"""
    src = src.replace("const breadcrumbSchema", addition.lstrip("\n") + "\nconst breadcrumbSchema", 1)
    src = src.replace('"isPartOf": { "@id": "https://alturascope.com/#organization" },',
                      '"isPartOf": { "@id": "https://alturascope.com/#organization" },\n  "mainEntity": { "@id": "https://alturascope.com/work/locations/#itemlist" },', 1)
    # render through the layout's extraSchema slot
    src = src.replace("  breadcrumbSchema={breadcrumbSchema}",
                      "  breadcrumbSchema={breadcrumbSchema}\n  extraSchema={itemListSchema}", 1)
    open(path, "w", encoding="utf-8").write(src)
    print(f"  {path}: ItemList of {'25'} ImageObjects added")
