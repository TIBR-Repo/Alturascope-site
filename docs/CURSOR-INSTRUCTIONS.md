# Cursor Instructions: Deploy 6 New Insights Blog Posts

## Overview
This folder contains 6 complete .astro blog post files ready to be placed into the AlturaScope website. Each file is fully written with content, structured data (Article schema, BreadcrumbList schema, FAQPage schema), internal links, and CTAs matching the existing blog post pattern.

## Step 1: Copy Files to the Correct Location

Copy each file from this folder into `/src/pages/insights/`:

1. `qsr-reimage-pre-construction-survey-timelines.astro`
2. `self-storage-portfolio-site-survey-documentation.astro`
3. `data-center-documentation-expansion-retrofit.astro`
4. `managing-multi-site-survey-programmes-at-scale.astro`
5. `multi-site-survey-programmes-uk.astro`
6. `data-centre-survey-uk-expansion-compliance.astro`

## Step 2: Update the Insights Index Page

In `/src/pages/insights/index.astro`, add links to all 6 new posts. Follow the existing pattern for how posts are listed on that page. Add them in publication date order (newest first):

- Data Centre Survey UK (April 14, 2026)
- Multi-Site Survey Programmes UK (April 7, 2026)
- Managing Multi-Site Surveys at Scale (April 1, 2026)
- Data Center Documentation (March 24, 2026)
- Self-Storage Portfolio Documentation (March 17, 2026)
- QSR Reimage Timelines (March 10, 2026)

## Step 3: Add Cross-Links FROM Existing Service Pages TO New Posts

Add a natural in-body text link from each of these existing pages to the corresponding new post. Find an appropriate sentence in the page body where the link fits naturally — don't just append it at the bottom.

| Existing Page | Link To | Suggested Anchor Text |
|---|---|---|
| `/services/qsr-restaurant-survey` | `/insights/qsr-reimage-pre-construction-survey-timelines/` | "how pre-construction surveys cut reimage timelines" |
| `/services/self-storage-portfolio-documentation` | `/insights/self-storage-portfolio-site-survey-documentation/` | "what portfolio operators need from site documentation" |
| `/services/data-centre-documentation` | `/insights/data-center-documentation-expansion-retrofit/` | "what facilities teams need before expansion" |
| `/services/data-centre-documentation` | `/insights/data-centre-survey-uk-expansion-compliance/` | "UK-specific data centre survey requirements" |
| `/uk/multi-site-rollout-survey` | `/insights/multi-site-survey-programmes-uk/` | "why single-source survey programmes work better" |
| `/services/multi-site-rollout-documentation` | `/insights/managing-multi-site-survey-programmes-at-scale/` | "lessons from surveying 500+ commercial locations" |

## Step 4: Add Cross-Links FROM Existing Blog Posts TO New Posts

Add links within the body text of these existing Insights posts:

| Existing Post | Link To | Context |
|---|---|---|
| `/insights/standardising-site-surveys-multi-site-operators` | `/insights/qsr-reimage-pre-construction-survey-timelines/` | Where QSR or restaurant surveys are mentioned |
| `/insights/standardising-site-surveys-multi-site-operators` | `/insights/managing-multi-site-survey-programmes-at-scale/` | Where programme scale is discussed |
| `/insights/standardising-site-surveys-multi-site-operators` | `/insights/multi-site-survey-programmes-uk/` | Where UK is mentioned |
| `/insights/due-diligence-documentation-portfolio-acquisitions` | `/insights/self-storage-portfolio-site-survey-documentation/` | Where portfolio assets are discussed |
| `/insights/documenting-controlled-environments-precision-facilities` | `/insights/data-center-documentation-expansion-retrofit/` | Where data centres are mentioned |
| `/insights/documenting-controlled-environments-precision-facilities` | `/insights/data-centre-survey-uk-expansion-compliance/` | Where UK is mentioned |

## Step 5: Verify Build

Run `npm run build` and verify:
- All 6 new pages build without errors
- All internal links resolve (no 404s)
- The sitemap includes the new URLs
- Structured data is valid (check any new page's source for correct JSON-LD)

## Notes
- All posts use the same Layout import and page structure as existing Insights posts
- All posts include `data-hero-page` attribute for the scroll-aware header
- UK posts (5 and 6) include `lang="en-GB"` and `hreflang` arrays
- Publication dates are staggered: March 10, March 17, March 24, April 1, April 7, April 14
- FAQ sections use expandable `<details>` elements matching the existing pattern
