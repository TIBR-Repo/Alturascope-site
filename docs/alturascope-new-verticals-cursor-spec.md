# AlturaScope — New Vertical Landing Pages
# Complete Cursor Implementation Spec

---

## Overview

This document is a complete implementation brief. It contains **seven new hidden service pages** for AlturaScope. These pages follow the exact same pattern as the existing specialist/hidden pages (aviation, superyacht, heritage, film/TV, etc.):

- **Not in the main navigation** — discovered via organic search, direct links, or referral
- **Included in sitemap.xml** so Google indexes them
- **Same layout, components, header/footer, and design language** as all existing service pages
- **Same tone:** confident, professional, specific — not salesy or generic

Each section below contains: URL slug, meta title, meta description, Open Graph tags, JSON-LD schema, full page content (H1, body sections, FAQ, CTA), internal cross-links, and SEO notes.

---

## Global Notes (Apply to All Seven Pages)

### Tone & Voice
- Authoritative but not arrogant. Speak from experience, not credentials
- Specific and technical where it matters — these pages target people who know their industry
- Never claim to provide professional interpretation, assessment, compliance certification, or engineering opinion. AlturaScope provides **documentation, structured data, and intelligence** — others make the formal calls
- Use "documentation" and "intelligence" liberally. Avoid "inspection" or "assessment" unless clearly framed as data gathering
- Emphasise that this is deeper than standard Matterport walk-throughs — mention LiDAR point clouds, millimetre-accurate scanning, thermal imaging, structured reporting, and the ScopeWalk platform where appropriate
- Geographic scope: mention North America (US and Canada) and the United Kingdom on every page EXCEPT the cannabis page (North America only)

### Technical SEO
- Each page needs `<title>`, `<meta name="description">`, `og:title`, `og:description`, `og:type` (website), `og:url` in `<head>`
- Each page needs a `<link rel="canonical" href="..." />` tag
- Each page needs JSON-LD `ProfessionalService` schema (provided per page)
- All pages must be added to `sitemap.xml` after creation
- All pages should be submitted to Google Search Console for indexing after deployment
- Do NOT add these pages to the main navigation — they remain discoverable via search only

### Internal Linking
- Every new page links back to `/services/` or the most relevant core service page
- Every new page links to at least one other specialist/hidden page where there's a natural connection
- Every new page links to `/contact` via the CTA section
- Cross-link to existing pages where relevant (e.g., data centre page can link to construction-documentation)

### Content Structure (Same for All Pages)
1. **Hero Section** — H1, subtitle/tagline, primary CTA
2. **The Problem** — 2-3 paragraphs explaining what this sector struggles with regarding site documentation
3. **What We Capture** — Specific deliverables and data points, presented as a structured list or grid (NOT bullet points in the traditional sense — use the same card/grid component as existing specialist pages)
4. **How It Works** — Brief process overview (3-4 steps)
5. **FAQ Section** — 3-4 questions with answers (critical for featured snippets and People Also Ask)
6. **CTA Section** — Clear call to action with link to `/contact`

---

---

# PAGE 1: Data Centre Documentation

## URL
`/services/data-centre-documentation`

## Meta
**Title:** `Data Centre Documentation & Reality Capture | Alturascope`
**Description:** `Millimetre-accurate LiDAR scanning, thermal imaging, and structured asset documentation for data centres. Rack layouts, power distribution, cooling systems, and capacity mapping across North America and the UK.`

## Open Graph
```
og:title: Data Centre Documentation & Reality Capture | Alturascope
og:description: Millimetre-accurate LiDAR scanning, thermal imaging, and structured asset documentation for data centres. Rack layouts, power distribution, cooling systems, and capacity mapping across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/data-centre-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Data Centre Documentation",
  "description": "Reality capture, LiDAR scanning, thermal imaging, and structured documentation services for data centres across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/data-centre-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Data Centre Documentation", "Reality Capture", "LiDAR Scanning", "Thermal Imaging", "Digital Twin"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Data Centre Documentation

### Subtitle
Millimetre-accurate reality capture for the infrastructure that can't afford ambiguity.

### The Problem

Data centre operators make expansion, retrofit, and capacity planning decisions worth tens of millions of dollars. Those decisions depend on knowing — precisely — what exists today: every rack position, every power run, every cooling path, every square metre of available white space.

Most facilities rely on outdated CAD drawings that stopped being accurate the week after commissioning. As-built documentation drifts further from reality with every cabinet move, every power rebalancing, every cooling modification. When it comes time to plan the next phase, engineering teams are working from assumptions, not data.

The cost of getting it wrong in a live data centre environment is measured in downtime — and downtime is measured in hundreds of thousands per hour.

### What We Capture

**Spatial Documentation**
Complete LiDAR point cloud of the facility — millimetre-accurate, survey-grade. Every aisle, every row, every overhead cable pathway, every underfloor void. This isn't a Matterport walkthrough. This is a measurable, georeferenced 3D dataset your engineers can extract dimensions from, plan against, and trust.

**Rack and Cabinet Inventory**
Structured documentation of rack positions, U-space allocation, and cabinet configurations. Photographed, tagged, and spatially located within the point cloud so your planning team can see exactly what's where without entering the white space.

**Power Distribution Mapping**
Documentation of the power chain from utility intake through UPS, switchgear, PDUs, and busway to the rack level. Nameplate data, visible condition, and spatial location — everything an electrical engineer needs to model existing capacity and plan additional load.

**Cooling Infrastructure**
CRAH and CRAC unit locations, capacities, and nameplate data. Hot aisle / cold aisle configurations. Containment systems. Raised floor tile layouts — perforated versus solid — mapped spatially so airflow modelling can begin from real geometry, not guesswork.

**Thermal Imaging**
Calibrated thermal capture across the facility: hotspot identification in electrical distribution, temperature differential mapping across cooling zones, and thermal documentation of cabinet faces to identify uneven heat loads. All thermal observations are georeferenced within the 3D model — not standalone JPEGs with vague location descriptions.

**Structured Reporting via ScopeWalk**
Every data point captured feeds into ScopeWalk, our proprietary reporting platform. Your team receives structured, searchable, spatially-referenced documentation — not a folder of files. Engineers, planners, and operations staff can access what they need without sifting through raw scan data.

### How It Works

**1. Scope and Protocol**
We work with your facilities team to define what needs capturing and any access constraints — particularly around live environments, restricted zones, and scheduling windows.

**2. On-Site Capture**
A single site visit with LiDAR, thermal, and photographic capture. We work around live operations. No disruption to running systems. Typical facility capture is completed within one to two days depending on scale.

**3. Processing and Structuring**
Raw capture is processed into deliverables: registered point cloud, thermal overlay, structured asset inventory, and spatial documentation — all assembled within ScopeWalk.

**4. Delivery**
Your team receives access to the complete dataset via ScopeWalk. Point cloud data is also available for export in standard formats (E57, LAS, RCP) for integration with your existing CAD, BIM, or DCIM platforms.

### FAQ

**Q: Can you work in a live data centre environment without disruption?**
A: Yes. Our capture methodology is non-contact and non-invasive. We use LiDAR and thermal imaging — no physical interaction with any equipment, no power shutdowns, no access panel removal required. We coordinate with your operations team on scheduling and access protocols.

**Q: How accurate is the LiDAR data?**
A: We deliver millimetre-accurate point clouds using survey-grade LiDAR equipment. This is significantly more precise than camera-based systems like Matterport and is suitable for engineering planning, capacity modelling, and design coordination.

**Q: Do you provide engineering analysis or capacity recommendations?**
A: We provide comprehensive, structured documentation — the raw intelligence your engineering team or consultants need to make informed decisions. We do not provide engineering opinions, capacity assessments, or compliance certifications. Our role is to ensure the data is complete, accurate, and accessible.

**Q: Can the data integrate with our existing DCIM or BIM platforms?**
A: Yes. Point cloud data is delivered in industry-standard formats. Structured asset data from ScopeWalk can be exported for integration with DCIM platforms, BIM environments, or your own internal systems.

### CTA
**H2:** Tell Us About Your Facility
**Body:** Share your facility details, scope requirements, and timeline. We respond within one business day with a scope recommendation and all-in pricing — travel included.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Construction Documentation →](/services/construction-documentation)
- [Multi-Site Rollout Surveys →](/services/multi-site-rollout-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`data centre documentation`, `data center LiDAR scan`, `data centre reality capture`, `data center as-built survey`, `data centre thermal imaging`, `data center facility documentation`, `DCIM as-built`, `data centre point cloud`

---

---

# PAGE 2: Insurance & Catastrophe Documentation

## URL
`/services/insurance-loss-documentation`

## Meta
**Title:** `Insurance Loss & Catastrophe Documentation | Alturascope`
**Description:** `Rapid-response reality capture for insurance claims, property losses, and catastrophe events. LiDAR scanning, thermal imaging, and structured damage documentation across North America and the UK.`

## Open Graph
```
og:title: Insurance Loss & Catastrophe Documentation | Alturascope
og:description: Rapid-response reality capture for insurance claims, property losses, and catastrophe events. LiDAR scanning, thermal imaging, and structured damage documentation across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/insurance-loss-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Insurance Loss & Catastrophe Documentation",
  "description": "Rapid-response reality capture, LiDAR scanning, thermal imaging, and structured damage documentation for insurance claims and catastrophe events across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/insurance-loss-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Insurance Documentation", "Catastrophe Documentation", "Reality Capture", "LiDAR Scanning", "Thermal Imaging", "Damage Documentation"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Insurance Loss & Catastrophe Documentation

### Subtitle
Comprehensive damage documentation when accuracy matters and time doesn't wait.

### The Problem

After a fire, flood, storm, or structural event, the quality of documentation determines everything: the speed of the claim, the accuracy of the settlement, the defensibility of the outcome. And yet, most loss documentation is still done with a clipboard, a phone camera, and a PDF report written from memory days later.

The result is disputed claims, missed damage, contested scopes, and restoration invoices that can't be verified against independent evidence. Adjusters, carriers, policyholders, and restoration contractors all suffer from the same root cause — incomplete, unstructured, spatially disconnected documentation.

The first 48 to 72 hours after a loss event are the most critical for evidence capture. Conditions change. Moisture migrates. Temporary repairs obscure original damage. What isn't documented comprehensively and promptly becomes a matter of opinion rather than evidence.

### What We Capture

**Complete Spatial Record**
LiDAR point cloud of the affected property — every room, every elevation, every affected area. A permanent, millimetre-accurate, measurable 3D record of conditions as they existed at the time of capture. This isn't a photo gallery. This is a dimensionally accurate environment your adjusters, engineers, and legal teams can revisit as many times as needed.

**Damage Documentation**
Systematic, room-by-room, system-by-system photographic documentation of all visible damage. Every observation is spatially tagged — pinned to a precise location in the 3D model so there is no ambiguity about where damage was found or how extensive it is.

**Thermal Imaging**
Calibrated thermal capture to identify moisture migration invisible to the naked eye. Water damage extends far beyond what's visually apparent — thermal imaging reveals evaporative cooling patterns in walls, ceilings, and floors that indicate concealed moisture. All thermal observations are georeferenced within the 3D model, giving remediation teams precise locations rather than vague descriptions.

**Structured Reporting**
All documentation is delivered through ScopeWalk as a structured, searchable dataset. Damage observations are categorised by building system — structural, envelope, mechanical, electrical, plumbing, interior finishes, contents. Each observation includes location, photographs, thermal data where relevant, and descriptive notes. The format is designed for use by adjusters, engineers, restoration contractors, and legal teams without requiring interpretation of raw scan data.

**Pre-Loss Baseline Comparison**
Where pre-loss documentation exists — prior surveys, Matterport models, or point clouds — we can provide comparative analysis showing exactly what changed. This eliminates ambiguity about pre-existing conditions versus event damage.

### How It Works

**1. Rapid Mobilisation**
Contact us and we mobilise. Our national travel model across the US, Canada, and the UK means we can reach most locations within 24 to 48 hours. Loss documentation is time-sensitive and we treat it accordingly.

**2. Comprehensive On-Site Capture**
LiDAR scanning, thermal imaging, and systematic photographic documentation of the entire affected area. A single visit captures everything — no return trips, no missed areas, no gaps in the record.

**3. Processing and Delivery**
Structured deliverables are typically available within 48 to 72 hours of capture. Your team receives the complete dataset via ScopeWalk — spatially referenced, categorised, and ready for use in claims processing, scope development, or litigation support.

### FAQ

**Q: How quickly can you mobilise after a loss event?**
A: We operate a national travel model across the United States, Canada, and the United Kingdom. In most cases we can be on site within 24 to 48 hours of first contact. For large-scale catastrophe events we can coordinate multi-site deployment.

**Q: Is this an inspection or a professional loss assessment?**
A: We provide comprehensive documentation — a complete, structured, spatially-referenced record of conditions at the time of capture. We do not provide loss adjustment opinions, engineering assessments, or cause-and-origin determinations. Our documentation is designed to give the professionals making those determinations the best possible evidence base to work from.

**Q: Can this documentation be used in legal proceedings?**
A: Our deliverables provide a factual, dimensionally accurate, timestamped record of conditions. The data has been used to support claims processes and dispute resolution. We capture what exists — the interpretation and application of that data is for your professional advisors.

**Q: Do you work with restoration contractors?**
A: Yes. Restoration companies use our documentation for scope development, progress tracking, and invoice substantiation. Pre-remediation and post-remediation capture provides a clear before-and-after record.

**Q: Can thermal imaging detect moisture behind walls?**
A: Thermal imaging detects temperature differentials caused by evaporative cooling — a reliable indicator of concealed moisture in walls, ceilings, and floors. It identifies affected areas that are invisible to visual inspection, allowing remediation teams to target their response accurately. The thermal data we capture is georeferenced within the 3D model, so moisture locations are spatially precise rather than described in approximate terms.

### CTA
**H2:** Need Rapid Documentation?
**Body:** Contact us with your location, the nature of the event, and your timeline. We'll confirm availability and mobilisation schedule within hours.
**Button:** Contact Us Now → /contact

### Internal Cross-Links
- [Construction Documentation →](/services/construction-documentation)
- [Commercial Kitchen Surveys →](/services/commercial-kitchen-survey)
- [All Services →](/services/)

### SEO Target Keywords
`insurance loss documentation`, `catastrophe documentation`, `property damage LiDAR scan`, `insurance claim reality capture`, `fire damage documentation`, `flood damage survey`, `loss adjuster documentation`, `CAT response documentation`, `property loss evidence capture`, `thermal imaging moisture detection insurance`

---

---

# PAGE 3: Industrial & Manufacturing Facility Documentation

## URL
`/services/industrial-facility-documentation`

## Meta
**Title:** `Industrial & Manufacturing Facility Documentation | Alturascope`
**Description:** `LiDAR scanning, thermal imaging, and structured as-built documentation for factories, processing plants, and industrial facilities. Equipment inventories, power mapping, and spatial intelligence across North America and the UK.`

## Open Graph
```
og:title: Industrial & Manufacturing Facility Documentation | Alturascope
og:description: LiDAR scanning, thermal imaging, and structured as-built documentation for factories, processing plants, and industrial facilities across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/industrial-facility-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Industrial & Manufacturing Facility Documentation",
  "description": "LiDAR scanning, thermal imaging, and structured as-built documentation for factories, processing plants, and industrial facilities across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/industrial-facility-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Industrial Documentation", "Factory Survey", "Manufacturing Facility Documentation", "Reality Capture", "LiDAR Scanning"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Industrial & Manufacturing Facility Documentation

### Subtitle
Accurate as-built intelligence for facilities that never stop changing.

### The Problem

Manufacturing and industrial facilities evolve constantly — production lines move, equipment gets replaced, utilities get rerouted, mezzanines go up, walls come down. The original construction drawings, if they ever existed, stopped reflecting reality within months of the facility opening.

When it's time to plan an expansion, reconfigure a production line, install automation, or bring in a new tenant, engineering teams face the same problem: nobody actually knows what's there. The result is expensive site visits by multiple disciplines, design clashes discovered during construction, and project timelines that slip because the existing conditions weren't properly understood at the outset.

The facilities that run most efficiently are the ones that know themselves best. Accurate, current, structured documentation of what exists is the foundation that every capital decision should be built on.

### What We Capture

**Complete Spatial Record**
Full LiDAR point cloud of the facility — production floor, mezzanines, offices, loading docks, service areas, roof level. Millimetre-accurate and survey-grade. Your engineering team gets a measurable 3D environment they can extract dimensions from, design within, and coordinate against.

**Equipment and Asset Inventory**
Structured documentation of major equipment: manufacturer, model, serial number, nameplate data, and spatial location within the facility. Each asset is photographed, tagged, and positioned in the point cloud. This isn't a spreadsheet assembled from memory — it's a verified, spatially-referenced inventory.

**Overhead Systems**
Crane and hoist systems — span, capacity, hook height, runway positions. Overhead utilities — compressed air, process piping, electrical distribution, exhaust and ventilation ductwork. Documented and spatially located within the 3D model so design teams know what's above the production floor, not just on it.

**Power Distribution**
Electrical infrastructure from main switchgear through distribution panels to major loads. Nameplate data, visible condition, and spatial location — the information an electrical engineer needs to evaluate available capacity and plan additional supply.

**Thermal Imaging**
Calibrated thermal capture of electrical distribution equipment, motor drives, bearings, and process equipment. Temperature anomalies in electrical and mechanical systems are identified and georeferenced within the 3D model — giving maintenance and engineering teams precise locations rather than vague observations.

**Floor Loading and Clear Heights**
Critical dimensional data: floor-to-structure heights at multiple points, column grids, dock door dimensions, turning radii, aisle widths. The spatial data that drives layout planning, equipment specification, and logistics design.

**Structured Reporting via ScopeWalk**
All documentation is delivered through ScopeWalk as a structured, searchable, spatially-referenced dataset. Filter by system type, area, or asset category. Export for integration with your CMMS, ERP, or CAD platforms.

### How It Works

**1. Scope Definition**
We work with your plant or facilities team to define the capture scope — full facility or targeted areas. We coordinate scheduling around production operations and any access or safety requirements.

**2. On-Site Capture**
LiDAR, thermal, and photographic capture executed systematically. We work around live production. No disruption to operations. Typical industrial facility capture is completed within one to three days depending on scale and complexity.

**3. Processing and Structuring**
Raw data is processed into deliverables: registered point cloud, thermal overlay, structured asset inventory, dimensional data, and spatial documentation within ScopeWalk.

**4. Delivery**
Complete dataset accessible via ScopeWalk. Point cloud data available in standard formats (E57, LAS, RCP) for CAD and BIM integration.

### FAQ

**Q: Can you capture a facility while production is running?**
A: Yes. Our equipment is non-contact and doesn't interfere with operations. We coordinate with your team on scheduling, safety protocols, and access to ensure capture happens without disrupting production.

**Q: What's the difference between this and a standard Matterport survey?**
A: Matterport produces a visual walkthrough — useful for orientation but not dimensionally reliable for engineering work. We deliver survey-grade LiDAR point clouds with millimetre accuracy, supplemented by thermal imaging, structured asset inventories, and dimensional data. The output is designed for engineers and planners, not viewers.

**Q: Do you provide engineering recommendations?**
A: We provide structured documentation and spatial intelligence. Engineering analysis, capacity assessments, and design recommendations are for your engineering team or consultants to determine based on the data we provide. Our role is to ensure they have the most complete and accurate evidence base possible.

**Q: Can you document racking systems?**
A: Yes. We have specific experience documenting warehouse racking — beam levels, bay dimensions, load ratings, column positions, aisle widths, and clear heights. This data supports layout optimisation, code compliance review, and reconfiguration planning.

### CTA
**H2:** Tell Us About Your Facility
**Body:** Share your facility details, the scope of documentation needed, and your timeline. We respond within one business day with a scope recommendation and all-in pricing — travel included.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Construction Documentation →](/services/construction-documentation)
- [Data Centre Documentation →](/services/data-centre-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`industrial facility documentation`, `factory as-built survey`, `manufacturing facility LiDAR scan`, `industrial reality capture`, `factory point cloud`, `plant documentation`, `manufacturing as-built`, `industrial thermal imaging`, `warehouse documentation`

---

---

# PAGE 4: Self-Storage & Warehousing Portfolio Documentation

## URL
`/services/self-storage-portfolio-documentation`

## Meta
**Title:** `Self-Storage & Warehousing Portfolio Documentation | Alturascope`
**Description:** `Standardised condition surveys and structured documentation for self-storage and warehousing portfolios. Due diligence capture, capital planning data, and portfolio-wide intelligence across North America and the UK.`

## Open Graph
```
og:title: Self-Storage & Warehousing Portfolio Documentation | Alturascope
og:description: Standardised condition surveys and structured documentation for self-storage and warehousing portfolios across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/self-storage-portfolio-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Self-Storage & Warehousing Portfolio Documentation",
  "description": "Standardised condition surveys and structured documentation for self-storage and warehousing portfolios across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/self-storage-portfolio-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Self-Storage Documentation", "Portfolio Documentation", "Condition Survey", "Reality Capture", "Due Diligence Documentation"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Self-Storage & Warehousing Portfolio Documentation

### Subtitle
One standard. Every location. The intelligence your capital planning actually needs.

### The Problem

The self-storage and warehousing sector is consolidating rapidly. Private equity firms and REITs are acquiring portfolios of dozens — sometimes hundreds — of facilities, often across multiple states, provinces, or regions. Each acquisition decision depends on understanding the physical condition of every asset in the portfolio.

The typical due diligence process sends different people to different sites with different approaches, producing inconsistent data that's almost impossible to compare across locations. Which facilities need immediate capital investment? Which roofs are approaching end of life? Which climate control systems are undersized? Which sites have deferred maintenance that wasn't disclosed? Without standardised documentation, these questions get answered with gut feel and rough estimates.

Post-acquisition, the same problem persists: capital planning across a portfolio requires condition data that's comparable site-to-site. If every location was surveyed differently, the data is noise, not intelligence.

### What We Capture

**Standardised Site Survey**
Every location in the portfolio is documented using the same capture protocol, the same equipment, and the same structured reporting format. This is the foundation that makes portfolio-level comparison meaningful. What gets measured at location one gets measured at location two hundred.

**Building Envelope**
Roof condition, wall cladding, door and loading systems, foundation and slab condition, drainage infrastructure, parking and hardscape. Documented visually and, where applicable, with thermal imaging to identify moisture intrusion and insulation failures invisible to visual inspection.

**Climate Control Systems**
HVAC units, dehumidification systems, and climate management infrastructure — manufacturer, model, age, capacity, visible condition. For climate-controlled storage, this is the critical infrastructure that determines unit viability and customer satisfaction.

**Security and Access Infrastructure**
Gate systems, camera positions, lighting, access control hardware, perimeter fencing. Documented and spatially located within the site model.

**Unit Mix and Configuration**
Unit types, sizes, and count verified against reported inventory. Drive-up versus interior, climate-controlled versus standard, specialty units. Dimensional verification where discrepancies exist between reported and actual configurations.

**Fire Protection**
Sprinkler systems, fire alarm panels, extinguisher locations, and suppression infrastructure documented by location and visible condition. Tag and inspection dates photographed where accessible.

**Spatial Documentation**
LiDAR point cloud or structured dimensional capture providing accurate site dimensions, building footprints, clear heights, column positions, and circulation paths. The measurable spatial data that supports layout optimisation and conversion planning.

**Portfolio-Level Reporting**
All site data flows into ScopeWalk, structured identically across every location. Your acquisitions, operations, and capital planning teams can compare facilities side-by-side on any data point — equipment age, envelope condition, unit mix, system capacity — across the entire portfolio.

### How It Works

**1. Portfolio Scope and Protocol**
We work with your acquisitions or operations team to define the capture protocol for the portfolio. One brief, one standard, every location. We establish the data points, the condition scoring methodology, and the reporting format before the first site is visited.

**2. Scheduled Rollout**
We deploy across the portfolio on a coordinated schedule — regional clusters to maximise efficiency. Our national travel model across the US, Canada, and the UK means geographic spread isn't a constraint. Travel is included in project pricing.

**3. Consistent Delivery**
Every site is delivered in the same format through ScopeWalk. As sites are completed, data becomes available progressively — your team doesn't wait for the entire portfolio to finish before accessing intelligence on completed locations.

**4. Portfolio Dashboard**
Once the programme is complete, your team has a single platform containing standardised condition data for every location. Sort by condition score, filter by system, prioritise by urgency. The capital planning decisions that used to take weeks of argument now take an afternoon with data.

### FAQ

**Q: How many locations can you cover and how quickly?**
A: We routinely run multi-site documentation programmes across North America and the UK. Portfolio programmes of 50 to 200+ locations are executed on coordinated schedules, typically completing 2 to 4 sites per day per technician depending on facility size. We scale capacity to meet your programme timeline.

**Q: Is this suitable for acquisition due diligence?**
A: Yes. Standardised condition documentation across a portfolio is exactly what due diligence teams need — consistent data that supports comparison, identifies risk, and informs capital reserve estimates. The structured format through ScopeWalk makes the data immediately useful for financial modelling and investment committee presentation.

**Q: Do you provide condition ratings or valuations?**
A: We provide structured observations and documented evidence using a standardised methodology. We do not provide formal condition ratings, property valuations, or engineering assessments. Our documentation is designed to give the professionals making those determinations — engineers, appraisers, capital planners — the most complete and consistent data set possible.

**Q: Can we use this data in our existing asset management platform?**
A: Yes. Structured data from ScopeWalk can be exported in standard formats for integration with your asset management, CMMS, or capital planning platforms. We work with your team to ensure the data structure aligns with your existing systems.

### CTA
**H2:** Tell Us About Your Portfolio
**Body:** Share the number of locations, geographic spread, your timeline, and what you need to know. We respond within one business day with a programme recommendation and portfolio pricing — all travel included.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Multi-Site Rollout Surveys →](/services/multi-site-rollout-documentation)
- [Industrial Facility Documentation →](/services/industrial-facility-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`self-storage portfolio documentation`, `self-storage due diligence survey`, `warehousing condition survey`, `self-storage acquisition documentation`, `portfolio condition assessment`, `self-storage capital planning`, `multi-site storage survey`, `REIT property documentation`

---

---

# PAGE 5: Cannabis Facility Documentation

## URL
`/services/cannabis-facility-documentation`

## Meta
**Title:** `Cannabis Facility Documentation & Reality Capture | Alturascope`
**Description:** `Structured documentation and reality capture for licensed cannabis cultivation, processing, and dispensary facilities. Security mapping, environmental systems, and compliance-ready reporting across North America.`

## Open Graph
```
og:title: Cannabis Facility Documentation & Reality Capture | Alturascope
og:description: Structured documentation and reality capture for licensed cannabis cultivation, processing, and dispensary facilities. Security mapping, environmental systems, and compliance-ready reporting across North America.
og:type: website
og:url: https://alturascope.com/services/cannabis-facility-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Cannabis Facility Documentation",
  "description": "Structured documentation and reality capture for licensed cannabis facilities across North America.",
  "url": "https://alturascope.com/services/cannabis-facility-documentation",
  "areaServed": ["US", "CA"],
  "serviceType": ["Cannabis Facility Documentation", "Reality Capture", "Compliance Documentation", "Security Documentation"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

### IMPORTANT: Geographic Note
This page mentions **North America only** — do NOT reference the United Kingdom.

## Page Content

### H1
Cannabis Facility Documentation

### Subtitle
Structured, compliance-ready documentation for licensed cultivation, processing, and retail operations.

### The Problem

Licensed cannabis operations face documentation requirements that most industries don't: security camera coverage maps, environmental control specifications, access zone delineation, spatial layouts that must match regulatory submissions exactly. Regulators expect precision. Investors require verified facility data. And the gap between what was submitted for licensing and what actually exists on the ground can create significant compliance exposure.

Most operators don't have accurate, current documentation of their facilities. Buildouts happen fast, modifications are made on the fly, and the as-built reality drifts from the approved plans. When an audit arrives — or an investor conducts due diligence — the scramble to produce accurate facility documentation is expensive, stressful, and often incomplete.

Proactive operators document their facilities accurately and keep that documentation current. It's cheaper, faster, and far less painful than the alternative.

### What We Capture

**Complete Spatial Documentation**
LiDAR point cloud of the entire facility — grow rooms, processing areas, vault and storage, retail floor, back of house, loading areas. Millimetre-accurate, measurable, and suitable for regulatory submission support, design coordination, and operational planning.

**Security Infrastructure Mapping**
Camera positions, fields of view, access control hardware, alarm panel locations, perimeter security, and vault/secure storage documentation. Spatially mapped within the 3D model so your security plan reflects what actually exists, not what was drawn on a plan two years ago.

**Environmental Control Systems**
HVAC, dehumidification, CO2 supplementation, lighting systems (type, wattage, PAR ratings where accessible), irrigation infrastructure, and air filtration. Documented with manufacturer, model, and nameplate data — the information your mechanical engineers and grow consultants need to evaluate performance and plan upgrades.

**Zoning and Access Control Documentation**
Clear spatial documentation of regulated zones: limited access areas, restricted areas, vault rooms, quarantine zones. Dimensions, access points, and security hardware documented and mapped to support regulatory compliance verification.

**Utility Infrastructure**
Electrical distribution — panels, capacity, circuit allocation. Water supply and drainage. Gas lines where present. The baseline utility data that supports capacity planning as operations scale.

**Structured Reporting via ScopeWalk**
All documentation is delivered through ScopeWalk in a structured, searchable format. Your compliance team, facility managers, and consultants can access exactly the data they need without wading through raw scan files.

### How It Works

**1. Scope and Coordination**
We work with your operations and compliance teams to define capture scope and coordinate access — particularly for restricted and limited-access areas. We understand the sensitivity around facility documentation in this industry and operate with discretion.

**2. On-Site Capture**
Comprehensive LiDAR, photographic, and environmental system documentation. Executed efficiently and systematically. We work around cultivation schedules and operational requirements.

**3. Processing and Delivery**
Structured deliverables through ScopeWalk, typically available within 5 business days of capture. Point cloud data available in standard formats for integration with architectural and engineering platforms.

### FAQ

**Q: Do you work with licensed facilities only?**
A: Yes. We provide documentation services to licensed cannabis cultivation, processing, and retail facilities operating in compliance with their jurisdictional regulations.

**Q: Is the documentation suitable for regulatory submission?**
A: Our documentation provides accurate, structured, spatially-referenced data about your facility as it exists. It supports regulatory submissions, licence applications, and compliance reviews by giving your compliance team and consultants a verified factual basis to work from. We do not provide regulatory compliance opinions or certifications.

**Q: How do you handle facility security and confidentiality?**
A: We understand the sensitivity of cannabis facility documentation. All data is handled under strict confidentiality. Access to ScopeWalk deliverables is controlled by your team. We coordinate all site access through your designated contacts and follow your security protocols.

**Q: Can you document multiple facilities for a multi-state operator?**
A: Yes. Our national travel model covers the United States and Canada. Multi-site programmes are coordinated on a schedule that works with your operations across all locations.

### CTA
**H2:** Tell Us About Your Facility
**Body:** Share your facility type, location, and documentation needs. We respond within one business day with a scope recommendation and all-in pricing.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Construction Documentation →](/services/construction-documentation)
- [Industrial Facility Documentation →](/services/industrial-facility-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`cannabis facility documentation`, `cannabis grow facility survey`, `cannabis compliance documentation`, `dispensary as-built survey`, `cannabis facility LiDAR scan`, `licensed cannabis facility documentation`, `cannabis security camera mapping`, `cannabis facility reality capture`

---

---

# PAGE 6: Education Campus Documentation

## URL
`/services/education-campus-documentation`

## Meta
**Title:** `Education Campus Documentation & Condition Surveys | Alturascope`
**Description:** `Standardised condition surveys, LiDAR scanning, and structured documentation for K-12 schools, colleges, and university campuses. Capital planning intelligence and portfolio-wide reporting across North America and the UK.`

## Open Graph
```
og:title: Education Campus Documentation & Condition Surveys | Alturascope
og:description: Standardised condition surveys, LiDAR scanning, and structured documentation for K-12 schools, colleges, and university campuses across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/education-campus-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Education Campus Documentation",
  "description": "Standardised condition surveys, LiDAR scanning, and structured documentation for K-12 schools, colleges, and university campuses across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/education-campus-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Education Facility Documentation", "School Condition Survey", "Campus Documentation", "Reality Capture", "Capital Planning Documentation"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Education Campus Documentation

### Subtitle
Structured condition intelligence for the buildings where deferred maintenance is measured in decades.

### The Problem

School boards, colleges, and universities manage enormous facility portfolios — often dozens or hundreds of buildings spanning multiple decades of construction. Deferred maintenance backlogs run into the billions across North America and the UK. The buildings that educate the next generation are frequently the least well-documented assets in any public portfolio.

Capital allocation decisions are made every year: which roofs get replaced, which mechanical systems get upgraded, which buildings get renovated, which get decommissioned. Those decisions should be driven by consistent, objective condition data. In practice, they're driven by emergency failures, squeaky wheels, and the political influence of individual administrators.

The institutions that manage their facilities best are the ones that have comprehensive, standardised, current documentation of every building in the portfolio — so capital priorities are set by evidence, not anecdote.

### What We Capture

**Building-by-Building Condition Documentation**
Every building in the portfolio is surveyed using the same capture protocol. Structural systems, building envelope, mechanical, electrical, plumbing, fire protection, interior finishes, accessibility features, and site conditions — all documented to the same standard so comparison across buildings is meaningful.

**Building Systems Inventory**
Major building systems documented with age, type, visible condition, and spatial location. HVAC units, boilers, chillers, electrical panels, fire alarm panels, roof-top equipment, elevators. The asset data that drives lifecycle planning and replacement scheduling.

**Accessibility Documentation**
Entrance conditions, corridor widths, ramp slopes, restroom configurations, signage, door hardware heights, elevator presence and condition. Structured documentation that supports accessibility compliance review by qualified consultants — captured with the dimensional accuracy to be useful, not approximate.

**Envelope and Weatherproofing**
Roof condition, window systems, exterior wall condition, foundation and below-grade waterproofing indicators. Supplemented with thermal imaging where appropriate to identify moisture intrusion and insulation failures not visible to the eye.

**Hazardous Material Indicators**
Documentation of material ages and types consistent with potential asbestos-containing materials, lead paint vintage indicators, and other hazardous material concerns. We do not test or certify — we document the visual and age-based indicators that inform where professional testing should be directed.

**Spatial Documentation**
LiDAR point cloud or structured dimensional capture of every building, providing accurate floor plans, ceiling heights, and room dimensions. Particularly valuable where original construction drawings no longer exist or no longer reflect reality.

**Portfolio-Level Reporting**
All building data flows into ScopeWalk in a standardised format. Sort and compare across the portfolio by any data point: building system age, condition score, envelope status, accessibility readiness. The structured intelligence that turns a maintenance backlog into a prioritised capital plan.

### How It Works

**1. Portfolio Scope and Protocol**
We work with your facilities or capital planning team to establish the capture protocol, condition scoring methodology, and reporting requirements across the portfolio. One standard for every building.

**2. Coordinated Campus Capture**
We deploy on a schedule coordinated with campus operations — working around academic calendars, events, and occupied spaces. Capture is non-invasive and non-disruptive to building use.

**3. Progressive Delivery**
Completed buildings are delivered progressively through ScopeWalk as they're processed. Your team starts working with data immediately — you don't wait for the entire portfolio to be finished.

**4. Portfolio Intelligence**
Once complete, the portfolio dataset enables evidence-based capital planning: which buildings need attention first, which systems are approaching end of life, where the highest-risk conditions exist.

### FAQ

**Q: Can you work in occupied school buildings?**
A: Yes. Our capture methodology is non-contact and non-disruptive. We can work in occupied buildings during school hours or during breaks and holidays — whichever your administration prefers. We coordinate scheduling with your facilities team.

**Q: Does this replace a formal Facility Condition Assessment (FCA)?**
A: We provide comprehensive, structured documentation — the field data that feeds into a formal FCA process. Many FCA consultants lack efficient tools for gathering the field data they need. Our documentation provides them with a complete, standardised evidence base that accelerates their assessment work significantly. We do not provide the engineering opinions or condition ratings that constitute a formal FCA.

**Q: Can you cover an entire school district or university system?**
A: Yes. Multi-site portfolio programmes are our core capability. We routinely run documentation programmes across dozens to hundreds of locations using a standardised protocol with consistent deliverables. Our national coverage model across the US, Canada, and the UK means geographic spread is not a constraint.

**Q: What about buildings with no existing drawings?**
A: This is common, particularly with older school buildings. Our LiDAR capture produces accurate spatial data regardless of whether drawings exist. For buildings with no documentation at all, our survey effectively creates the first accurate record of the building's geometry and systems.

### CTA
**H2:** Tell Us About Your Campus or Portfolio
**Body:** Share the number of buildings, your geographic scope, and what you're trying to accomplish — whether it's capital planning, a bond programme, or portfolio-wide condition baselining. We respond within one business day.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Multi-Site Rollout Surveys →](/services/multi-site-rollout-documentation)
- [Self-Storage Portfolio Documentation →](/services/self-storage-portfolio-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`school condition survey`, `education campus documentation`, `school facility condition assessment`, `university building documentation`, `K-12 facility survey`, `campus LiDAR scan`, `school district capital planning`, `education facility reality capture`, `school building as-built`, `university campus condition survey`

---

---

# PAGE 7: Solar Farm & Renewable Energy Documentation

## URL
`/services/solar-farm-documentation`

## Meta
**Title:** `Solar Farm & Renewable Energy Site Documentation | Alturascope`
**Description:** `LiDAR scanning, thermal imaging, and structured documentation for solar farms, battery storage facilities, and renewable energy infrastructure. Pre-construction surveys, as-built verification, and operational monitoring across North America and the UK.`

## Open Graph
```
og:title: Solar Farm & Renewable Energy Site Documentation | Alturascope
og:description: LiDAR scanning, thermal imaging, and structured documentation for solar farms, battery storage facilities, and renewable energy infrastructure across North America and the UK.
og:type: website
og:url: https://alturascope.com/services/solar-farm-documentation
```

## JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "AlturaScope — Solar Farm & Renewable Energy Documentation",
  "description": "LiDAR scanning, thermal imaging, drone capture, and structured documentation for solar farms, battery storage, and renewable energy infrastructure across North America and the United Kingdom.",
  "url": "https://alturascope.com/services/solar-farm-documentation",
  "areaServed": ["US", "CA", "GB"],
  "serviceType": ["Solar Farm Documentation", "Renewable Energy Documentation", "Drone Survey", "Thermal Imaging", "LiDAR Scanning", "Reality Capture"],
  "parentOrganization": {
    "@type": "Organization",
    "name": "AlturaScope",
    "url": "https://alturascope.com"
  }
}
```

## Page Content

### H1
Solar Farm & Renewable Energy Site Documentation

### Subtitle
Structured intelligence for the assets powering the grid — from pre-construction through operations.

### The Problem

Renewable energy development moves fast. Solar farms, battery energy storage systems, and associated infrastructure are being deployed at unprecedented scale across North America and the UK. Every phase of the lifecycle — site evaluation, design, construction, commissioning, operations, and maintenance — depends on accurate documentation of what exists on and around the site.

Pre-construction, developers need precise topographic and spatial data to inform panel layout, grading design, and interconnection planning. During construction, owners and lenders need verified as-built documentation confirming what was actually installed matches what was designed. In operations, performance issues — underperforming panels, hotspots, inverter anomalies, vegetation encroachment — need to be identified and located precisely across sites that can span hundreds of acres.

The scale of these sites makes traditional documentation approaches impractical. Walking a 500-acre solar farm with a clipboard doesn't work. Drone-based LiDAR and thermal capture does.

### What We Capture

**Pre-Construction Site Documentation**
LiDAR-based topographic capture of the development site — existing terrain, vegetation, structures, access routes, and utility infrastructure. Georeferenced spatial data that supports site design, grading calculations, environmental review, and permitting.

**As-Built Verification**
Post-construction documentation confirming installed infrastructure matches design intent. Panel array positions, racking systems, inverter locations, combiner boxes, electrical infrastructure, fencing, access roads, and drainage — all captured and spatially referenced for owner's acceptance and lender verification.

**Aerial Thermal Imaging**
Drone-based thermal capture across the array identifying underperforming panels, hotspot cells, bypass diode failures, string-level anomalies, and connection issues. Every thermal observation is georeferenced — your O&M team receives precise panel locations for each anomaly, not a thermal image of a generic field of panels.

**Inverter and Electrical Infrastructure**
Ground-level documentation of inverter stations, transformers, switchgear, combiner boxes, and cable routing. Manufacturer data, nameplate specifications, and visible condition — structured and spatially located within the site model.

**Battery Energy Storage Systems (BESS)**
For co-located or standalone battery storage: container positions, HVAC and fire suppression systems, electrical connections, and thermal documentation of operating temperatures. The documentation that supports both operational monitoring and regulatory compliance.

**Vegetation and Encroachment Monitoring**
Aerial and ground-level documentation of vegetation conditions affecting panel performance, access, or structural loading. Repeat capture cycles provide comparative data showing progression over time.

**Structured Reporting via ScopeWalk**
All site data is delivered through ScopeWalk in a structured, searchable, spatially-referenced format. Filter by system, zone, or anomaly type. Export for integration with SCADA, CMMS, or asset management platforms.

### How It Works

**1. Scope and Coordination**
We work with your development, construction, or O&M team to define capture scope, access requirements, and scheduling. For operational sites, we coordinate around maintenance windows and grid commitments.

**2. Site Capture**
Drone-based LiDAR and thermal capture for large-area coverage, supplemented by ground-level documentation of electrical infrastructure and equipment. Site capture timelines depend on scale — from a single day for smaller arrays to multiple days for utility-scale installations.

**3. Processing and Delivery**
Georeferenced deliverables through ScopeWalk: point clouds, orthomosaics, thermal maps, structured anomaly reporting, and asset inventories. Data is delivered in formats compatible with GIS, CAD, and SCADA platforms.

### FAQ

**Q: What size solar installations can you document?**
A: We document installations ranging from commercial rooftop arrays to utility-scale ground-mounted farms spanning hundreds of acres. Our drone-based capture methodology scales efficiently — larger sites require more flight time but the approach is the same.

**Q: Can thermal imaging identify individual failing panels?**
A: Drone-based thermal imaging can identify panel-level and cell-level thermal anomalies — including hotspot cells, bypass diode failures, and string-level underperformance. Each anomaly is georeferenced so your maintenance team knows the exact panel location, row, and position within the array.

**Q: Do you provide performance analysis or engineering recommendations?**
A: We provide structured documentation: thermal anomaly maps, asset inventories, and spatial data. Performance analysis, root cause determination, and engineering recommendations are for your O&M engineers or specialist consultants. Our documentation gives them the field data they need to work efficiently and accurately.

**Q: Can you provide repeat capture for ongoing monitoring?**
A: Yes. Scheduled capture cycles — annually, semi-annually, or aligned with your maintenance programme — provide comparative data over time. This enables trend analysis on panel degradation, vegetation encroachment, and infrastructure condition, all through the same structured reporting framework.

**Q: Do you cover battery storage facilities as well?**
A: Yes. Battery energy storage systems are documented with the same rigour — spatial positioning, thermal monitoring, electrical infrastructure, and environmental systems. For co-located solar-plus-storage sites, everything is captured in a single deployment.

### CTA
**H2:** Tell Us About Your Site
**Body:** Share your site location, phase (pre-construction, construction, or operational), approximate scale, and what you need documented. We respond within one business day with a scope recommendation and all-in pricing — travel included.
**Button:** Start a Project → /contact

### Internal Cross-Links
- [Construction Documentation →](/services/construction-documentation)
- [Industrial Facility Documentation →](/services/industrial-facility-documentation)
- [All Services →](/services/)

### SEO Target Keywords
`solar farm documentation`, `solar farm thermal imaging`, `solar panel drone inspection`, `solar farm LiDAR survey`, `solar farm as-built`, `PV array thermal scan`, `renewable energy site documentation`, `solar farm reality capture`, `BESS documentation`, `battery storage facility survey`, `solar farm drone survey UK`

---

---

# Implementation Checklist for Cursor

## File Creation
Create seven new `.astro` page files matching the existing specialist page pattern:
1. `/services/data-centre-documentation`
2. `/services/insurance-loss-documentation`
3. `/services/industrial-facility-documentation`
4. `/services/self-storage-portfolio-documentation`
5. `/services/cannabis-facility-documentation`
6. `/services/education-campus-documentation`
7. `/services/solar-farm-documentation`

## Design & Layout
- Use the **exact same layout, component structure, typography, and design language** as the existing specialist/hidden pages (aviation, superyacht, heritage, film/TV, etc.)
- Same header, footer, navigation pattern
- Same CTA button style and placement
- Same section spacing and content structure
- These pages should be visually indistinguishable in style from the existing specialist pages

## Navigation
- Do **NOT** add these pages to the main site navigation
- They remain hidden/discoverable via search only — same as existing specialist pages

## Head Tags (All Seven Pages)
Each page must include in `<head>`:
```html
<title>[Meta Title from spec above]</title>
<meta name="description" content="[Meta Description from spec above]" />
<meta property="og:title" content="[OG Title from spec above]" />
<meta property="og:description" content="[OG Description from spec above]" />
<meta property="og:type" content="website" />
<meta property="og:url" content="[Canonical URL from spec above]" />
<link rel="canonical" href="[Canonical URL from spec above]" />
<meta name="robots" content="index, follow" />
```

## Schema Markup
Inject the JSON-LD schema block for each page inside a `<script type="application/ld+json">` tag in the page `<head>`.

## Sitemap
Add all seven new URLs to `sitemap.xml` after creation.

## Post-Deployment (Manual — Outside Cursor)
1. Submit all seven new URLs to Google Search Console for indexing
2. Verify sitemap update is reflected in Search Console
3. Test all pages render correctly on mobile and desktop
4. Verify all internal cross-links function correctly
5. Verify all meta tags and schema are rendering correctly (use Google's Rich Results Test)
