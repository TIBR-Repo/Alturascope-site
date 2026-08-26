# One-off migrations

These ran once, in August 2026, as part of the site overhaul that followed a
full structural and SEO audit. They are kept because each one records *why* a
change was made and, in a couple of cases, which approach was tried and
rejected — which is the part that stops somebody undoing the work later.

They are all idempotent: re-running detects that the work is done and skips.
None of them is part of the routine build. The only script you need day to day
is `../seo-audit.py`, which should be run after `npm run build` and before any
push.

Run in this order if they ever have to be replayed against an older tree:

| Script | What it did |
|---|---|
| `restructure-estimating.py` | Moved the free sample-pack offer from 38% down the estimating pages to screen two; made the six deliverables and nine audit checks two-column; folded "we don't build it" into the moat section. |
| `estimating-navigation.py` | Added the sticky in-page sub-nav and section anchors; dropped the inline Basis of Estimate checklist in favour of a link to the page that already says it. |
| `estimating-merge.py` | Merged the accountability section into "a desk, not a person"; slimmed the Vyntworks card grid. |
| `add-estimating-links.py` | Put an `EstimatingBand` on seventeen survey pages, each with a lead sentence written for that page's subject. |
| `replace-stock-heroes.py` | Swapped 27 service and UK heroes from Unsplash to Alturascope's own photography. Records which repo images are AI-generated or carry lorem ipsum and must never be published. |
| `selfhost-stock.py` | Downloaded the remaining editorial stock imagery to `public/Images/stock/` so nothing is requested from a third-party CDN. |
| `to-webp.py` | Converted imagery to WebP and repointed every reference. |
| `archive-unused-originals.py` | Moved the superseded JPEG/PNG masters to `assets-source/`, which Astro does not publish. |
| `fix-schema-types.py` | Gave the hub pages real schema types instead of five copies of `ProfessionalService`; added the gallery's `ItemList` of `ImageObject`s. |
| `tighten-meta.py` | Conservative meta pass: dropped the redundant brand suffix from over-long titles, trimmed descriptions at sentence boundaries only. |
| `rewrite-long-meta.py` | Hand-written replacements for the 31 descriptions and 10 titles the automated pass could not fix safely. |

## The two approaches that were tried and rejected

Both are documented in the scripts themselves, but they are worth repeating
because they look reasonable until you read the output:

1. **Cutting a title at its colon.** Turns *"ABA Clinic Portfolio Renovation:
   Standardising Documentation Across Acquired Locations"* into *"ABA Clinic
   Portfolio Renovation"* — inside the length limit, and stripped of the
   keywords the page ranks on.
2. **Trimming a meta description on a word boundary.** Produces
   *"...turns inherited real estate into."* Better over-length than
   ungrammatical.
