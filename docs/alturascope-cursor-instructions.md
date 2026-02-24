# AlturaScope — New Page Build Instructions for Cursor

## READ THIS FIRST — Context and Objectives

You are building new pages for alturascope.com, an Astro-based static site. These pages are a critical SEO initiative. The site currently has 11 indexed pages in Google, zero search visibility, and zero backlinks. The technical SEO foundation is solid (schema, meta, sitemap, canonical URLs all in place). What's missing is content that targets the search terms our actual buyers use.

**Who is AlturaScope?**
AlturaScope is NOT a Matterport scanning company. We are NOT competing with technicians who show up, press a button, and deliver a 3D link. AlturaScope is a site intelligence company. The scan is the capture method — the value is the structured deliverable package: conditions reports, equipment and asset schedules, MEP documentation, above-ceiling investigation, thermal imaging analysis, narrated walkthroughs, and a permanent project platform (ScopeWalk). A general contractor or programme manager can brief their entire consultant team from our deliverable without returning to site. That is the differentiator. Every page must communicate this.

**Who is the buyer?**
The buyer is NOT an architect looking for floor plans. The buyer is:
- A VP of Construction at a 200-unit QSR chain told to remodel 80 locations this year
- A programme director at a PE-backed retail group running a national rebrand
- A facilities director at a healthcare network planning multi-site capex
- A development manager at a franchise group expanding into new markets

These people do not search for "Matterport scan" or "as-built drawings." They search for things like "multi-site restaurant survey programme," "pre-construction site survey QSR," "how to manage a nationwide restaurant remodel," or "rollout programme site documentation." Write for them.

**What makes AlturaScope different from competitors (especially PPM, THE FUTURE 3D, PM Design)?**
1. **Depth of capture** — We don't just measure walls. We document conditions, services, equipment, access constraints, MEP routing, above-ceiling infrastructure, and thermal anomalies. One visit produces the full picture.
2. **Structured deliverables** — Every visit produces the same deliverable architecture: digital twin, conditions report (P1/P2/P3 prioritised), equipment and asset schedule, narrated video walkthrough, labelled photo storyboard. Not a folder of files — a decision-ready package.
3. **ScopeWalk platform** — All deliverables live in a permanent, structured portal. Programme managers can compare sites side by side, brief consultants directly from the portal, and track rollout progress. This is not Dropbox. It's a project record.
4. **Specialist capabilities** — FLIR thermal imaging for MEP documentation and moisture/insulation analysis. Pole-mounted 360° above-ceiling capture. Borescope inspection for hidden services. LiDAR point clouds for survey-grade accuracy. These aren't add-ons — they're integrated into the methodology.
5. **Single-vendor national model** — One brief, one standard, consistent deliverables across every location. Travel included in pricing. No surprise line items. No local subcontractor lottery.
6. **18 years of construction experience** — The person on site understands construction, not just cameras. The conditions report is written by someone who knows what they're looking at and what it means for the project.

**Competitor context for positioning:**
- PPM (asbuiltdrawings.com) — Market leader for multi-site as-built surveys. 26,000+ projects, 75+ surveyors. But their deliverable is CAD plans and Revit models. They measure and draft. They don't deliver structured intelligence.
- PM Design Group — Offers as-built surveys plus equipment documentation and 360° walkthroughs. Larger firm with architecture and MEP engineering services. Closer to us but part of a bigger practice, not a focused offering.
- Larson Design Group — Has a "Reality Capture" product similar to ScopeWalk. Architecture firm that does surveys as part of larger engagements.
- THE FUTURE 3D — Scanning company with city pages. Primarily scan-and-deliver. Not in our league on deliverable depth.

We are not competing with these companies directly. We are positioning in the space between them — deeper than a scanning company, more focused than a full architecture practice, and specifically built for programme-scale rollouts where consistency and deliverable structure matter more than individual scan quality.

---

## Design and Aesthetic Requirements

**Match the existing site exactly.** Study the existing pages — homepage, /services, /services/construction-documentation, /services/multi-site-rollout-documentation, /services/specialist-projects, and the UK pages — for:
- Typography, spacing, colour palette
- Section structure (eyebrow text above H2s, hero layout, CTA button styling)
- Component patterns (feature grids, stat counters, testimonial blocks if any)
- Dark/light section alternation
- The tone: confident, precise, understated. No exclamation marks. No hype. No "cutting-edge" or "state-of-the-art" or "revolutionary." The copy should read like a senior construction professional explaining what they do — direct, specific, assured.

**Image approach:** Use the same Unsplash approach as existing pages for now. Choose images that suggest commercial interiors, construction environments, restaurant/retail spaces, warehouses, healthcare corridors — whatever fits the page vertical. Alt text must be descriptive and keyword-rich (e.g., "Pre-construction site survey of a quick service restaurant interior showing equipment and MEP services" not "restaurant photo").

---

## Technical SEO Requirements — Apply to EVERY New Page

### Meta Tags
Every page must have:
```html
<title>[Keyword-rich title] | Alturascope</title>
<meta name="description" content="[155-160 chars, includes primary keyword, compelling reason to click]" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="https://alturascope.com/[page-path]/" />
```

### Open Graph Tags
```html
<meta property="og:title" content="[Same as title tag]" />
<meta property="og:description" content="[Same as meta description]" />
<meta property="og:url" content="https://alturascope.com/[page-path]/" />
<meta property="og:type" content="website" />
<meta property="og:image" content="[Hero image URL]" />
<meta property="og:site_name" content="Alturascope" />
```

### JSON-LD Schema
Every new page must include Service schema:
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[Service Name]",
  "description": "[Service description incorporating primary keyword]",
  "provider": {
    "@type": "ProfessionalService",
    "name": "Alturascope",
    "url": "https://alturascope.com",
    "areaServed": [
      { "@type": "Country", "name": "United States" },
      { "@type": "Country", "name": "Canada" },
      { "@type": "Country", "name": "United Kingdom" }
    ]
  },
  "serviceType": "[Primary keyword phrase]",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Site Documentation Services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Navigable Digital Twin" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Conditions Report" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Equipment & Asset Schedule" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "ScopeWalk Platform Access" } }
    ]
  }
}
```

### FAQ Schema (on every page — add 3-5 relevant FAQs per page)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text]"
      }
    }
  ]
}
```

### Internal Linking Rules
Every new page MUST link to:
- At least 2 other service pages (use contextual anchor text, not "click here")
- The /contact page (via CTA buttons)
- At least 1 relevant Insights blog post (if one exists on a related topic)
- The /services page or /work page where appropriate

Additionally, AFTER building the new pages, go back and add links TO the new pages FROM:
- The homepage (in relevant sections — e.g., the "Who We Work With" section should link to rollout vertical pages)
- /services/multi-site-rollout-documentation (this is the parent page — it should link to each vertical)
- /services/construction-documentation (cross-link where relevant)
- Any Insights blog posts that discuss related topics
- The footer navigation (add a new "Industries" or "Sectors" section if appropriate)

Use keyword-rich anchor text for internal links. Not "learn more" — instead use "QSR restaurant survey programmes" or "multi-site retail rollout documentation."

### Heading Structure
- One H1 per page (keyword-optimised, not a tagline)
- H2s for major sections (include secondary keywords)
- H3s for subsections and deliverable items
- Never skip heading levels

### URL Structure
All new pages go under `/services/` to maintain the existing hierarchy:
- `/services/qsr-restaurant-survey/`
- `/services/retail-rollout-documentation/`
- `/services/healthcare-facility-survey/`
- `/services/pre-construction-site-intelligence/`
- `/services/northeast-site-surveys/`
- `/services/southeast-site-surveys/`
- `/services/central-us-site-surveys/`
- `/services/west-coast-site-surveys/`

### Sitemap
Ensure all new pages are included in the auto-generated sitemap-index.xml. These pages should NOT be added to the main navigation — they are discovery pages found through search or direct link, same as the existing specialist pages (aviation, marine, heritage, etc.).

---

## PAGES TO BUILD

---

### PAGE 1: QSR Restaurant Survey Programme

**URL:** `/services/qsr-restaurant-survey/`

**Meta Title:** `QSR Restaurant Site Surveys — Multi-Site Remodel Documentation | Alturascope`

**Meta Description:** `Pre-construction site surveys for QSR and restaurant remodel programmes. Equipment schedules, conditions reports, above-ceiling MEP documentation, and Matterport digital twins — consistent deliverables across every location.`

**H1:** `QSR Restaurant Site Surveys — Complete Documentation for Multi-Site Remodel Programmes`

**Target Keywords (weave naturally throughout):**
- QSR site survey
- restaurant pre-construction survey
- quick service restaurant remodel documentation
- multi-site restaurant survey programme
- restaurant equipment schedule
- restaurant conditions survey
- QSR rollout documentation
- restaurant renovation site survey
- commercial kitchen documentation
- franchise remodel survey

**Page Structure and Content Direction:**

**Hero Section:**
- Eyebrow: `Multi-Site Programmes · QSR & Restaurant`
- H1 as above
- Subheading (2-3 sentences): Address the buyer directly. Something along the lines of: When you're managing a remodel programme across dozens or hundreds of restaurant locations, every site is different — but your documentation shouldn't be. AlturaScope delivers the same structured intelligence package at every location, so your design team works from consistent, complete information and your programme stays on track.
- CTAs: [Tell Us About Your Programme](/contact) and [See How It Works](/services)

**Section: The Problem (H2: What Slows Down a Multi-Site Restaurant Remodel)**
Write 3-4 paragraphs from the buyer's perspective. The VP of Construction or programme director running 80+ locations doesn't have time to deal with inconsistent site information. Address these pain points specifically:
- Every location is slightly different — equipment varies, previous tenants made modifications, MEP routing differs, above-ceiling conditions are unknown
- Traditional as-built surveys produce floor plans but miss the operational detail that drives the scope — equipment makes and models, services connections, actual ceiling plenum conditions, fire suppression routing
- Inconsistent deliverables from different local surveyors mean the design team has to re-learn a new format every time, and gaps are only discovered when the contractor is on site
- Return site visits to capture missed information cost time and money and disrupt restaurant operations
- The result: change orders, programme delays, and scope creep that could have been prevented with complete documentation upfront

**Section: What We Deliver at Every Location (H2: The Same Deliverable Architecture. Every Restaurant. Every Time.)**
This is where we differentiate from PPM and every other as-built company. Describe each deliverable component as an H3:

- **H3: Navigable Digital Twin** — Describe how the 3D model lets the entire team (architect, MEP engineer, kitchen consultant, franchise owner) explore the space remotely. Measurements taken in the model. No return visits to verify a dimension.

- **H3: Conditions Report (P1 / P2 / P3 Prioritised)** — Written assessment of existing conditions structured by priority. P1: immediate action required before remodel proceeds. P2: address during remodel. P3: noted for awareness. Covers structural observations, services condition, finishes, ceiling condition, floor condition, ADA compliance observations, fire suppression status. Not a narrative — a structured, scannable document formatted consistently across every location.

- **H3: Equipment & Asset Schedule** — This is a major differentiator. Full inventory of installed kitchen equipment, HVAC units, electrical panels, POS infrastructure, signage, lighting types and quantities, fire suppression components, plumbing fixtures — with makes, models, locations, and services connections where visible. Formatted for procurement and fitout teams. The same format at every location so your team can compare, plan, and order across the entire programme.

- **H3: Above-Ceiling MEP Documentation** — In a restaurant environment, what's above the ceiling drives the scope. HVAC supply and return routing, grease duct runs, electrical conduit, fire suppression mains, exhaust fans. We document above-ceiling conditions using FLIR thermal imaging (non-invasive identification of active services), pole-mounted 360° capture through access points, and targeted borescope inspection. Integrated into the conditions report and the digital twin.

- **H3: Commercial Kitchen Documentation** — Beyond the equipment schedule: gas line routing, hood and exhaust configuration, grease trap location and condition, walk-in cooler/freezer condition and services, ice machine drainage, three-compartment sink plumbing. The detail that kitchen consultants and equipment suppliers need to spec accurately for the remodel.

- **H3: Narrated Video Walkthrough** — Spoken commentary tour of the space. What was found, what it means for the remodel scope, what requires specialist input. Allows the design team and franchise owner to understand conditions without a site visit.

- **H3: ScopeWalk Platform Access** — All deliverables for every location in the programme, structured and permanently accessible through a single portal. Not a file transfer link — a programme management tool. Compare locations side by side. Brief consultants directly from the platform. Track programme progress. Filter by status, priority, or location.

**Section: How We Work in Operating Restaurants (H2: Minimal Disruption. Maximum Capture.)**
Address the operational reality of surveying operating QSR locations:
- Early morning and off-peak scheduling to avoid disrupting service
- Single-visit methodology — we arrive once and capture everything. Equipment, conditions, above-ceiling, thermal, walkthrough — all in one visit.
- Typical survey time for a standard QSR location: 2-4 hours depending on size and scope
- All deliverables returned within [appropriate turnaround] of the site visit
- Scheduling managed centrally by AlturaScope — your team briefs us once and we coordinate directly with each location

**Section: Programme Scale (H2: From Pilot to Full Rollout)**
Describe the programme onboarding process:
- Pilot phase: we survey 3-5 locations to calibrate the deliverable to your team's specific requirements. Format, level of detail, reporting structure — all refined before the full rollout begins.
- Full rollout: consistent execution across every location. Same surveyor methodology. Same deliverable format. Same ScopeWalk structure. Whether it's 20 locations or 500.
- National coverage: we operate across all 50 US states and every Canadian province under a travel model. Travel costs included in project pricing. No local subcontractor variability.
- UK coverage available for brands with transatlantic programmes.

**Section: FAQ (H2: Common Questions About QSR Site Survey Programmes)**
Write 4-5 FAQs with proper FAQ schema. Examples:
- How long does a typical QSR site survey take?
- What equipment documentation is included in the survey?
- Can you survey restaurants during operating hours?
- How does ScopeWalk work for multi-site programmes?
- What's the difference between an as-built survey and a conditions survey?

**Section: CTA (H2: Ready to Brief Your Programme?)**
Short closing section with CTA. Same format as existing pages.

**Internal Links to Include:**
- Link to /services/multi-site-rollout-documentation (parent service page)
- Link to /services/construction-documentation (for single-site work)
- Link to /services/commercial-kitchen-survey (if it exists as specialist page)
- Link to /services (how it works)
- Link to at least one relevant Insights post if available
- Link to /contact

---

### PAGE 2: Retail Rollout Documentation

**URL:** `/services/retail-rollout-documentation/`

**Meta Title:** `Retail Rollout Site Documentation — Multi-Site Survey Programme | Alturascope`

**Meta Description:** `Site documentation for retail remodel, rebrand, and expansion programmes. Conditions surveys, equipment schedules, and Matterport digital twins delivered consistently across every location — nationwide.`

**H1:** `Retail Rollout Site Documentation — Consistent Intelligence Across Every Location`

**Target Keywords:**
- retail rollout site survey
- multi-site retail documentation
- retail remodel survey programme
- store rebrand site documentation
- retail expansion site survey
- PE-backed retail rollout
- franchise site survey
- retail conditions survey nationwide
- retail fit-out pre-construction survey
- multi-location retail documentation

**Page Structure and Content Direction:**

**Hero Section:**
- Eyebrow: `Multi-Site Programmes · Retail & Franchise`
- H1 as above
- Subheading: Address the programme director or PE-backed operator. When you're running a rebrand, refresh, or expansion across dozens of retail locations, the site survey is the first decision point — and it shapes every decision that follows. AlturaScope delivers the same structured documentation package at every store, so your design team, contractors, and consultants all work from the same baseline.
- CTAs: [Tell Us About Your Programme](/contact) and [How It Works](/services)

**Section: The Problem (H2: The Hidden Cost of Inconsistent Site Information)**
Write from the perspective of a PE-backed operator or franchise group running a national programme:
- When every location is documented differently — different surveyors, different formats, different levels of detail — the design team spends as much time interpreting the information as using it
- Floor plans alone don't capture the conditions that drive scope changes: ceiling condition, MEP routing, structural constraints, equipment that's been added or modified since the last survey, accessibility issues
- At programme scale, a 5% change order rate across 100 locations isn't a rounding error — it's a budget line item that was preventable
- The traditional approach — send a local surveyor to each location and hope for consistency — doesn't scale

**Section: What We Deliver (H2: Every Store. The Same Standard. The Same Platform.)**
Same deliverable structure as the QSR page but framed for retail:

- **H3: Navigable Digital Twin** — Adapt for retail context (store layout, fixture positions, ceiling heights, structural grid, column locations)
- **H3: Conditions Report** — Adapted for retail: flooring condition, ceiling type and condition, storefront and glazing, loading dock access, back-of-house vs front-of-house separation, existing fixture infrastructure
- **H3: Equipment & Asset Schedule** — Retail-specific: HVAC units, electrical panels and capacity, lighting types and fixtures, fire suppression, security systems, POS infrastructure, signage (interior and exterior), stockroom racking
- **H3: Thermal Imaging & MEP Documentation** — FLIR thermal capture to identify hidden services, active electrical loads, HVAC performance, moisture intrusion behind walls. Above-ceiling documentation for ceiling plenum conditions.
- **H3: Narrated Walkthrough** — Spoken assessment tailored to retail remodel scope
- **H3: ScopeWalk Programme Dashboard** — Emphasise the programme management angle: compare stores, filter by region or priority, brief consultants, track progress across the rollout

**Section: Who This Is For (H2: Built for Operators Running Programmes at Scale)**
- PE-backed retail operators running portfolio-wide upgrades
- Franchise groups executing national rebrands
- Developers managing multi-tenant retail fitouts
- Construction managers coordinating multi-site contractor deployment

Each should be an H3 with 2-3 sentences explaining the specific value for that buyer.

**Section: National Coverage (H2: One Vendor. One Standard. Nationwide.)**
- All 50 US states, all Canadian provinces, United Kingdom
- Travel included in project pricing
- No local subcontractor variability — AlturaScope methodology, AlturaScope deliverables, every time
- Programme scheduling managed centrally

**Section: FAQ (H2)**
4-5 retail-specific FAQs. Wrap in FAQ schema.

**Section: CTA**

**Internal Links:**
- /services/multi-site-rollout-documentation
- /services/qsr-restaurant-survey (cross-link)
- /services/construction-documentation
- /services (how it works)
- Relevant Insights posts
- /contact

---

### PAGE 3: Healthcare Facility Survey

**URL:** `/services/healthcare-facility-survey/`

**Meta Title:** `Healthcare Facility Surveys — Site Documentation for Medical & Clinical Spaces | Alturascope`

**Meta Description:** `Conditions surveys and site documentation for hospitals, clinics, and healthcare networks. MEP documentation, equipment schedules, thermal imaging, and Matterport digital twins for capital planning and renovation programmes.`

**H1:** `Healthcare Facility Surveys — Structured Documentation for Capital Planning and Renovation`

**Target Keywords:**
- healthcare facility survey
- hospital site documentation
- medical facility conditions survey
- healthcare capital planning survey
- clinic pre-construction survey
- healthcare MEP documentation
- hospital renovation site survey
- healthcare facility assessment
- medical equipment documentation
- healthcare multi-site survey

**Page Structure and Content Direction:**

**Hero Section:**
- Eyebrow: `Specialist Sectors · Healthcare`
- H1 as above
- Subheading: Healthcare facilities are among the most complex environments to document — and among the most consequential to get wrong. Sensitive operations, complex MEP infrastructure, infection control requirements, and regulatory compliance all demand documentation that goes deeper than a floor plan. AlturaScope delivers the structured site intelligence your capital planning and renovation teams need.
- CTAs: [Tell Us About Your Project](/contact) and [See Our Methodology](/services)

**Section: Why Healthcare Documentation Is Different (H2)**
- MEP density and complexity far exceeds typical commercial spaces — medical gas, vacuum systems, nurse call, redundant power, specialised HVAC with air handling requirements
- Operational sensitivity — surveys must work around active clinical operations, patient areas, restricted zones
- Equipment documentation requirements are more extensive — medical equipment, imaging equipment, lab equipment, sterilisation, pharmacy infrastructure
- Compliance documentation — surveys often inform regulatory submissions, JC/AAAHC compliance evidence, or CMS condition assessments
- Multi-building campus complexity — main hospital, satellite clinics, medical office buildings, each with different systems and conditions

**Section: What We Deliver (H2: Documentation That Serves Your Entire Capital Planning Team)**
Same deliverable architecture, adapted for healthcare:

- **H3: Digital Twin** — Navigate patient rooms, corridors, operating suites, mechanical rooms, rooftops. Dimensional accuracy for design teams. Remote access for consultants and administrators who don't need to enter clinical spaces.
- **H3: Conditions Report** — Healthcare-specific: building envelope, roofing, structural observations, MEP system condition, interior finishes (clinical vs administrative), code compliance observations, ADA/accessibility, fire and life safety systems
- **H3: Equipment & Infrastructure Schedule** — Medical equipment, HVAC (including air handling units, exhaust systems, isolation room infrastructure), electrical (including generator, UPS, transfer switches), plumbing (including medical gas, vacuum, waste), fire suppression, nurse call and communication, security and access control
- **H3: Thermal Imaging** — FLIR capture for identifying active services behind walls and above ceilings, HVAC performance assessment, moisture intrusion detection, electrical load identification. Non-invasive. No disruption to clinical operations.
- **H3: Above-Ceiling Documentation** — Healthcare plenum spaces are among the most densely serviced in commercial construction. Document routing, identify conflicts, inform the design team before renovation begins.
- **H3: ScopeWalk Platform** — For healthcare networks running multi-facility capex programmes: all facilities documented in a single platform, comparable and accessible.

**Section: Healthcare Network Programmes (H2: Multi-Facility Capital Planning)**
For healthcare networks running capital programmes across multiple facilities — standardised documentation allows apples-to-apples comparison of facility condition, informs capital allocation decisions, and gives every project team the same quality of baseline information.

**Section: How We Work in Healthcare Environments (H2)**
- Surveys scheduled around clinical operations
- PPE compliance and infection control protocols observed
- Sensitive areas documented with appropriate discretion
- Single-visit methodology minimises operational disruption
- All survey personnel background-checked and compliant with facility access requirements

**Section: FAQ (H2)**
4-5 healthcare-specific FAQs with schema.

**Section: CTA**

**Internal Links:**
- /services/construction-documentation
- /services/multi-site-rollout-documentation (for healthcare networks)
- /services/specialist-projects
- Relevant Insights posts
- /contact

---

### PAGE 4: Pre-Construction Site Intelligence (Positioning Page)

**URL:** `/services/pre-construction-site-intelligence/`

**Meta Title:** `Pre-Construction Site Intelligence — Beyond As-Built Surveys | Alturascope`

**Meta Description:** `A site survey should tell you more than dimensions. AlturaScope delivers structured pre-construction intelligence — conditions, equipment, services, thermal analysis — so your team makes decisions from complete information.`

**H1:** `Pre-Construction Site Intelligence — The Documentation Your Project Decisions Depend On`

**Target Keywords:**
- pre-construction site survey
- pre-construction documentation
- existing conditions survey
- site intelligence for construction
- pre-construction site assessment
- building conditions report
- site survey beyond as-built
- construction site documentation
- existing building documentation
- pre-construction planning survey

**Page Structure and Content Direction:**

This page is the POSITIONING page. It explains what AlturaScope does differently and why it matters. It's the page that converts someone who searched "pre-construction site survey" and expected to find as-built drawing companies — and instead finds something deeper.

**Hero Section:**
- Eyebrow: `The AlturaScope Methodology`
- H1 as above
- Subheading: Most pre-construction surveys produce a floor plan. Ours produces a decision. The difference between knowing a room's dimensions and knowing its conditions, its services, its equipment, its constraints, and its implications for your scope — that's the difference between a survey and site intelligence.
- CTAs: [Start a Project](/contact) and [See the Full Service](/services)

**Section: The Problem with Traditional Site Surveys (H2: A Floor Plan Is Not a Decision)**
This is where we draw the line between AlturaScope and the as-built survey industry:
- Traditional as-built surveys measure walls and produce drawings. They answer the question "what shape is the space?" They do not answer "what condition is it in?", "what equipment is installed?", "what's above the ceiling?", "what are the MEP constraints?", or "what will this cost to deal with?"
- The questions that drive scope, budget, and programme decisions — conditions, services, equipment, access, compliance — are typically discovered on site during construction. By then, the design is committed and the change order is inevitable.
- A pre-construction site survey should prevent surprises, not create a baseline for them.

**Section: What Site Intelligence Means (H2: What You Receive From Every AlturaScope Visit)**
Full deliverable breakdown — this is the definitive description of the AlturaScope methodology. Every deliverable component as H3, described in full:

- **H3: Navigable Digital Twin (Matterport)** — Full description
- **H3: Written Conditions Report** — P1/P2/P3 structure, what it covers, how it's formatted
- **H3: Equipment & Asset Schedule** — Full inventory, makes/models, services connections, formatted for procurement
- **H3: Thermal Imaging (FLIR)** — What it reveals, how it's used, what it prevents
- **H3: Above-Ceiling MEP Documentation** — Thermal, pole-mounted 360°, borescope, integrated into conditions report
- **H3: Narrated Video Walkthrough** — Spoken assessment of conditions and implications
- **H3: Labelled Photo Storyboard** — Consistent, navigable, structured
- **H3: ScopeWalk Platform Access** — Permanent, structured, accessible

**Section: Who Needs This (H2: Built for Teams Making Decisions on Space)**
- General contractors and design-build firms
- Developers and asset managers
- Multi-site programme operators
- Facilities and capital planning teams

**Section: How This Is Different (H2: Survey vs Intelligence)**
A clean comparison — not a competitor-bashing table, but a clear articulation of what traditional as-built surveys deliver vs what AlturaScope delivers. Frame it as "if all you need is a floor plan, there are excellent companies that do that. If you need the full picture before you commit to a design, a programme, or a budget — that's what we do."

**Section: FAQ (H2)**
5-6 FAQs. Include "What's the difference between an as-built survey and a conditions survey?" — this is a high-value search query.

**Section: CTA**

**Internal Links:**
- /services/construction-documentation
- /services/multi-site-rollout-documentation
- /services/qsr-restaurant-survey
- /services/retail-rollout-documentation
- /services/healthcare-facility-survey
- /services/specialist-projects
- Relevant Insights posts
- /contact

---

### PAGES 5-8: Regional Hub Pages

Build four regional pages. These are NOT city pages with swapped names — each must reference the construction market, project types, and operational context specific to that region.

#### PAGE 5: Northeast
**URL:** `/services/northeast-site-surveys/`
**Meta Title:** `Site Surveys & Documentation — Northeast US | Alturascope`
**Meta Description:** `Pre-construction site documentation across the Northeast — New York, Boston, Philadelphia, Washington DC, and the I-95 corridor. Matterport digital twins, conditions reports, and equipment schedules for renovation and rollout programmes.`
**H1:** `Site Surveys & Pre-Construction Documentation — Northeast United States`
**Target Keywords:** site survey New York, pre-construction survey Boston, site documentation Philadelphia, building survey Washington DC, commercial site survey Northeast US, Matterport survey NYC
**Regional Context to Reference:**
- Dense urban construction environments: tight access, occupied buildings, high-rise interiors
- Aging building stock — pre-war structures with undocumented modifications across decades of tenancy
- Strict permitting environments (NYC DOB, Boston ISD) that demand accurate existing conditions documentation
- Major retail, QSR, and healthcare markets concentrated along the I-95 corridor
- Reference specific project types: office-to-residential conversions, retail refreshes in dense urban cores, healthcare campus renovations

#### PAGE 6: Southeast
**URL:** `/services/southeast-site-surveys/`
**Meta Title:** `Site Surveys & Documentation — Southeast US | Alturascope`
**Meta Description:** `Site documentation for construction and renovation projects across the Southeast — Atlanta, Miami, Charlotte, Nashville, Tampa. Conditions surveys, thermal imaging, and digital twins.`
**H1:** `Site Surveys & Pre-Construction Documentation — Southeast United States`
**Target Keywords:** site survey Atlanta, pre-construction survey Miami, site documentation Charlotte, building survey Nashville, commercial site survey Southeast US, Matterport survey Florida
**Regional Context:**
- Rapid commercial growth markets — high volume of new-build and renovation activity
- Hurricane and moisture damage documentation (thermal imaging for moisture intrusion is particularly relevant here)
- QSR and franchise expansion concentrated in high-growth metros (Atlanta, Nashville, Charlotte, Tampa, Orlando)
- Healthcare network expansion — major health systems running multi-facility capital programmes
- Climate considerations for MEP documentation — HVAC loads, moisture management, building envelope assessment

#### PAGE 7: Central US
**URL:** `/services/central-us-site-surveys/`
**Meta Title:** `Site Surveys & Documentation — Central US | Alturascope`
**Meta Description:** `Pre-construction site documentation across the Central US — Chicago, Dallas, Houston, Denver, Minneapolis. Equipment schedules, MEP documentation, and Matterport digital twins for renovation and rollout programmes.`
**H1:** `Site Surveys & Pre-Construction Documentation — Central United States`
**Target Keywords:** site survey Chicago, pre-construction survey Dallas, site documentation Houston, building survey Denver, commercial site survey Texas, Matterport survey Midwest
**Regional Context:**
- Major QSR and franchise headquarters concentrated in Chicago and Dallas — these are the decision-making cities for national programmes
- Industrial and warehouse conversion projects across the Midwest
- Large-format retail and big-box renovation programmes in Texas and the Sun Belt
- Energy sector facility documentation (Houston)
- Extreme climate range demands thorough HVAC and building envelope assessment

#### PAGE 8: West Coast
**URL:** `/services/west-coast-site-surveys/`
**Meta Title:** `Site Surveys & Documentation — West Coast US | Alturascope`
**Meta Description:** `Site documentation for construction and renovation projects across the West Coast — Los Angeles, San Francisco, Seattle, Portland. Seismic assessment documentation, conditions surveys, and Matterport digital twins.`
**H1:** `Site Surveys & Pre-Construction Documentation — West Coast United States`
**Target Keywords:** site survey Los Angeles, pre-construction survey San Francisco, site documentation Seattle, building survey Portland, commercial site survey California, Matterport survey West Coast
**Regional Context:**
- Seismic assessment considerations — existing conditions documentation critical for renovation in seismic zones
- Stringent energy and sustainability code requirements (Title 24 in California)
- Tech sector office renovation and conversion projects
- High construction costs make thorough pre-construction documentation especially valuable — every prevented change order matters more when labour rates are $150+/hr
- Dense urban environments similar to Northeast but with different building types and codes

**Common Structure for All Regional Pages:**
Each regional page should follow this structure:
1. Hero with regional H1 and subheading referencing the specific market
2. Section: Why documentation matters in this region (2-3 paragraphs referencing regional specifics)
3. Section: What we deliver (abbreviated version of the full deliverable list — link to /services/pre-construction-site-intelligence for full detail)
4. Section: Markets we serve in the region (QSR, retail, healthcare, commercial — with links to the vertical pages)
5. Section: Coverage and logistics (travel model, no local subcontractor variability, scheduling)
6. Section: CTA
7. Internal links to vertical pages, services page, and contact

---

## AFTER BUILDING ALL PAGES — Backlink Updates

Go back to existing pages and add internal links to the new pages:

### Homepage
In the "Who We Work With" section, add contextual links:
- "Rollout & Multi-Site Programmes" subsection should link to /services/qsr-restaurant-survey and /services/retail-rollout-documentation
- "General Contractors & Design-Build" should link to /services/pre-construction-site-intelligence

### /services/multi-site-rollout-documentation
This is the parent page for rollout work. Add a section or paragraph that links to:
- /services/qsr-restaurant-survey
- /services/retail-rollout-documentation
- /services/healthcare-facility-survey

### /services/construction-documentation
Add cross-links to:
- /services/pre-construction-site-intelligence
- /services/healthcare-facility-survey

### /services page (main services hub)
If there's a section listing service types or industries, add links to the new vertical pages.

### Footer
Consider adding a "Sectors" or "Industries" column to the footer with links to:
- QSR & Restaurant
- Retail & Franchise
- Healthcare
- And the existing specialist pages (aviation, marine, heritage, etc.)

### Insights Blog Posts
Review each existing blog post. Where a post discusses topics related to the new pages (pre-construction surveys, equipment documentation, rollout programmes, etc.), add a contextual link to the relevant new page.

---

## FINAL CHECKLIST

Before deploying, verify:
- [ ] Every new page has unique meta title and description
- [ ] Every new page has canonical URL
- [ ] Every new page has Open Graph tags
- [ ] Every new page has JSON-LD Service schema
- [ ] Every new page has FAQ schema with 3-5 questions
- [ ] Every new page has at least 3 internal links to other pages
- [ ] Every new page has a CTA linking to /contact
- [ ] Every new page has keyword-rich alt text on all images
- [ ] Every new page uses proper heading hierarchy (one H1, H2s, H3s)
- [ ] All new pages appear in sitemap-index.xml
- [ ] Backlinks from existing pages to new pages have been added
- [ ] Footer updated with new sector links
- [ ] No duplicate content between pages — each page has genuinely distinct content
- [ ] Copy tone matches existing site: confident, precise, understated, no hype
- [ ] All pages render correctly on mobile
