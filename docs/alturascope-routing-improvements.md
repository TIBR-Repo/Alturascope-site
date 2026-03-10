# AlturaScope — Site-Wide Routing and Discovery Improvements

## Instructions for Cursor

These are targeted edits to existing pages. The goal is to ensure that visitors who arrive on the homepage or the Services page can easily discover the key sector specialisms (ABA/autism therapy, QSR/restaurant, retail, healthcare) and the multi-site rollout offering — without adding clutter to the top navigation.

The top nav stays exactly as it is: The Standard, Services, About, Contact. These changes make the Services page and the homepage do the heavy routing work.

---

## CHANGE 1: Services Index Page (`src/pages/services/index.astro`)

The current Services page has three sections: Core Service, Rollout Programmes, and Specialist Work. The Rollout Programmes section is where the key sectors should be surfaced prominently. Currently it has four text links at the bottom. This needs to become a proper visual section that makes the sector specialisms obvious and clickable.

### Replace the entire "Rollout Programmes" section (the `<section class="bg-offwhite section-padding">` block, approximately lines 63-84) with the following:

```html
    <!-- Rollout & Multi-Site Programmes -->
    <section class="bg-offwhite section-padding">
      <div class="max-w-[1200px] mx-auto px-6">
        <p class="label text-gold mb-4">Rollout Programmes</p>
        <h2 class="text-[2rem] font-light text-navy leading-tight">
          The same standard. Across every site in your programme.
        </h2>
        <div class="mt-6 space-y-4 text-midgrey leading-body max-w-[900px]">
          <p>
            For operators running rollout programmes — retail rebrand, QSR reimage, healthcare expansion, franchise build-out — consistency is the deliverable. Every site produces the same structured package through ScopeWalk, in the same format, accessible in the same place. Your design team briefs from the same information on site one as they do on site fifty.
          </p>
          <p>
            We coordinate access and travel nationally, with programme pricing that includes travel costs rather than adding them per visit.
          </p>
        </div>
        <a href="/services/multi-site-rollout-documentation" class="inline-block mt-6 text-navy font-medium hover:opacity-80 transition-opacity">
          How multi-site programmes work &rarr;
        </a>

        <!-- Sector Cards -->
        <div class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <a href="/services/qsr-restaurant-survey" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">QSR &amp; RESTAURANT</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Restaurant Remodel &amp; Reimage Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Kitchen equipment schedules, above-ceiling MEP documentation, and conditions reports — consistent across every location in the programme.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/aba-autism-clinic-documentation" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">ABA &amp; AUTISM THERAPY</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">ABA Clinic Documentation</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Hundreds of clinics documented. Sensory rooms, acoustic separation, elopement prevention, ceiling heights, and everything PE-backed platforms need.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/retail-rollout-documentation" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">RETAIL &amp; FRANCHISE</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Retail Rebrand &amp; Refresh Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Prototype adaptation across dozens of locations. Equipment schedules, storefront conditions, and above-ceiling documentation at every site.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/healthcare-facility-survey" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">HEALTHCARE</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Healthcare Network Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Dental, urgent care, veterinary, and medical office documentation. Clinical equipment, MEP density, and compliance-relevant conditions.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>
        </div>
      </div>
    </section>
```

### Also update the "Internal Links" section at the bottom of the Services page (approximately lines 147-155) to include sector links:

Replace the existing internal links section with:

```html
    <!-- Internal Links -->
    <section class="bg-white py-12">
      <div class="max-w-[900px] mx-auto px-6 flex flex-wrap justify-center gap-6 text-sm">
        <a href="/" class="text-navy font-medium hover:opacity-80 transition-opacity">Home &rarr;</a>
        <a href="/work" class="text-navy font-medium hover:opacity-80 transition-opacity">The Standard &rarr;</a>
        <a href="/services/multi-site-rollout-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">Multi-site rollout programmes &rarr;</a>
        <a href="/services/qsr-restaurant-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">QSR restaurant surveys &rarr;</a>
        <a href="/services/aba-autism-clinic-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">ABA clinic documentation &rarr;</a>
        <a href="/services/retail-rollout-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">Retail rollout documentation &rarr;</a>
        <a href="/services/healthcare-facility-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">Healthcare facility surveys &rarr;</a>
        <a href="/services/pre-construction-site-intelligence" class="text-navy font-medium hover:opacity-80 transition-opacity">Pre-construction intelligence &rarr;</a>
        <a href="/about" class="text-navy font-medium hover:opacity-80 transition-opacity">About Alturascope &rarr;</a>
        <a href="/contact" class="text-navy font-medium hover:opacity-80 transition-opacity">Start a project &rarr;</a>
      </div>
    </section>
```

---

## CHANGE 2: Homepage — Rework "Who We Work With" Section (`src/pages/index.astro`)

The current "Who We Work With" section has four generic categories in a 4-column grid. It needs to do more work routing visitors to the key sectors. The approach is to keep the four categories but make the "Rollout & Multi-Site Programmes" card more prominent with explicit sector links, and add a subtle sector discovery line below the grid.

### Replace the entire "Who We Work With" section (approximately lines 219-254) with:

```html
    <!-- SECTION 6: Who We Work With -->
    <section class="bg-offwhite section-padding">
      <div class="max-w-[1200px] mx-auto px-6">
        <p class="label text-gold text-center mb-4">Who We Work With</p>
        <h2 class="text-[2rem] font-light text-navy text-center">
          Built for teams making decisions on space.
        </h2>

        <div class="mt-16 grid grid-cols-1 md:grid-cols-2 gap-10">
          <!-- Multi-Site — larger, top row, full width on mobile -->
          <div class="md:col-span-2 bg-white rounded border border-border p-10">
            <h3 class="text-navy font-medium text-[1.2rem] mb-4">
              <a href="/services/multi-site-rollout-documentation" class="hover:opacity-80 transition-opacity">Rollout &amp; Multi-Site Programmes</a>
            </h3>
            <p class="text-midgrey text-[0.95rem] leading-relaxed max-w-[700px]">
              PE-backed operators, franchise groups, healthcare networks, and national brands running programmes across dozens or hundreds of locations. One brief, one standard, every site &mdash; managed centrally through ScopeWalk.
            </p>
            <div class="mt-6 flex flex-wrap gap-x-8 gap-y-3">
              <a href="/services/qsr-restaurant-survey" class="text-navy text-sm font-medium hover:opacity-80 transition-opacity">QSR &amp; Restaurant &rarr;</a>
              <a href="/services/aba-autism-clinic-documentation" class="text-navy text-sm font-medium hover:opacity-80 transition-opacity">ABA &amp; Autism Therapy &rarr;</a>
              <a href="/services/retail-rollout-documentation" class="text-navy text-sm font-medium hover:opacity-80 transition-opacity">Retail &amp; Franchise &rarr;</a>
              <a href="/services/healthcare-facility-survey" class="text-navy text-sm font-medium hover:opacity-80 transition-opacity">Healthcare &rarr;</a>
            </div>
          </div>

          <!-- GCs -->
          <div>
            <h3 class="text-navy font-medium mb-3">General Contractors &amp; Design-Build</h3>
            <p class="text-midgrey text-[0.9rem] leading-relaxed">
              <a href="/services/pre-construction-site-intelligence" class="text-navy underline underline-offset-2 hover:opacity-80">Pre-construction site intelligence</a>, above-ceiling capture, and conditions surveys that get your team off site faster and into design sooner.
            </p>
          </div>

          <!-- Developers -->
          <div>
            <h3 class="text-navy font-medium mb-3">Developers &amp; Asset Managers</h3>
            <p class="text-midgrey text-[0.9rem] leading-relaxed">
              <a href="/services/construction-documentation" class="text-navy underline underline-offset-2 hover:opacity-80">Pre-lease diligence</a>, renew-versus-relocate analysis, and <a href="/services/multi-site-rollout-documentation" class="text-navy underline underline-offset-2 hover:opacity-80">multi-site capex programmes</a>. One vendor, consistent deliverables, nationwide coverage.
            </p>
          </div>
        </div>

        <!-- Specialist note -->
        <div class="mt-10 text-center">
          <p class="text-midgrey text-[0.9rem]">
            Some projects require a different kind of attention &mdash; heritage buildings, aviation, marine, resorts, private estates. <a href="/services/specialist-projects" class="text-navy font-medium hover:opacity-80 transition-opacity">Tell us about yours &rarr;</a>
          </p>
        </div>
      </div>
    </section>
```

This does several things:
- Makes "Rollout & Multi-Site Programmes" the dominant card — spanning full width at the top of the section, with explicit sector links (QSR, ABA, Retail, Healthcare) right there
- Keeps GCs and Developers as secondary cards below
- Moves the Specialist mention to a subtle one-liner below the grid — it's still accessible but doesn't compete for attention with the multi-site sectors
- The visual hierarchy now clearly says: "multi-site rollout work is our main thing, and here are the sectors we do it in"

---

## CHANGE 3: Multi-Site Rollout Documentation Page (`src/pages/services/multi-site-rollout-documentation.astro`)

This page is the hub for all rollout work. It needs to route visitors clearly to the sector-specific pages. Currently it has some sector links but they could be more prominent.

### Find the section where sectors or programme types are listed and ensure it includes prominent cards or links to:
- `/services/qsr-restaurant-survey` — QSR & Restaurant
- `/services/aba-autism-clinic-documentation` — ABA & Autism Therapy
- `/services/retail-rollout-documentation` — Retail & Franchise
- `/services/healthcare-facility-survey` — Healthcare

If there is not already a dedicated "Sectors We Serve" section on this page, add one after the main content sections but before the FAQ. Use the same card pattern as the Services index page update above:

```html
    <!-- Sector Specialisms -->
    <section class="bg-offwhite section-padding">
      <div class="max-w-[1200px] mx-auto px-6">
        <p class="label text-gold mb-4">Sector Specialisms</p>
        <h2 class="text-[2rem] font-light text-navy leading-tight">
          Multi-site documentation across the sectors that matter.
        </h2>
        <div class="mt-6 space-y-4 text-midgrey leading-body max-w-[900px]">
          <p>
            Every sector has its own documentation requirements. A QSR restaurant survey captures kitchen equipment and above-ceiling exhaust routing. An ABA clinic survey documents ceiling heights, acoustic separation, and elopement prevention. A retail rebrand survey records storefront conditions and fixture infrastructure. The methodology is consistent. The sector knowledge runs deep.
          </p>
        </div>

        <div class="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <a href="/services/qsr-restaurant-survey" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">QSR &amp; RESTAURANT</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Restaurant Remodel Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Kitchen equipment, above-ceiling MEP, conditions reports. Consistent across every location.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/aba-autism-clinic-documentation" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">ABA &amp; AUTISM THERAPY</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">ABA Clinic Documentation</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Hundreds of clinics documented. Sensory rooms, acoustics, elopement prevention, and programme-scale delivery.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/retail-rollout-documentation" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">RETAIL &amp; FRANCHISE</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Retail Rebrand Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Prototype adaptation, storefront conditions, equipment schedules. National coverage.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>

          <a href="/services/healthcare-facility-survey" class="group block bg-white rounded p-8 border border-border transition-all duration-300 hover:border-gold hover:shadow-md">
            <p class="label text-gold text-[0.65rem] mb-3">HEALTHCARE</p>
            <h3 class="text-[1.1rem] font-medium text-navy leading-snug group-hover:opacity-80 transition-opacity">Healthcare Network Programmes</h3>
            <p class="mt-3 text-midgrey text-[0.85rem] leading-relaxed">Dental, urgent care, veterinary, medical office. Clinical MEP and compliance documentation.</p>
            <span class="inline-block mt-4 text-navy text-sm font-medium">Learn more &rarr;</span>
          </a>
        </div>
      </div>
    </section>
```

If sector links already exist elsewhere on this page in a simpler format, keep those too — more internal links is better for SEO. But this dedicated section should be the primary visual routing mechanism.

---

## CHANGE 4: Footer — Reorder Sectors Column (`src/layouts/Layout.astro`)

The Sectors column in the footer currently lists: QSR & Restaurant, Retail & Franchise, Healthcare, Commercial Kitchens, Aviation, Heritage. With the ABA page being added (from the previous instruction set), the order should reflect priority — the sectors you want to be found for most prominently should be listed first.

### Reorder the Sectors column to:

```html
<h4 class="text-xs font-medium uppercase tracking-label text-white/50 mb-6">Sectors</h4>
<nav class="flex flex-col gap-3">
  <a href="/services/aba-autism-clinic-documentation" class="text-sm text-white/70 hover:text-white transition-colors">ABA &amp; Autism Therapy</a>
  <a href="/services/qsr-restaurant-survey" class="text-sm text-white/70 hover:text-white transition-colors">QSR &amp; Restaurant</a>
  <a href="/services/retail-rollout-documentation" class="text-sm text-white/70 hover:text-white transition-colors">Retail &amp; Franchise</a>
  <a href="/services/healthcare-facility-survey" class="text-sm text-white/70 hover:text-white transition-colors">Healthcare</a>
  <a href="/services/commercial-kitchen-survey" class="text-sm text-white/70 hover:text-white transition-colors">Commercial Kitchens</a>
  <a href="/services/aviation-facility-survey" class="text-sm text-white/70 hover:text-white transition-colors">Aviation</a>
  <a href="/services/heritage-building-documentation" class="text-sm text-white/70 hover:text-white transition-colors">Heritage</a>
</nav>
```

ABA moves to the top because it's the deepest specialism. QSR and Retail follow as the other core multi-site sectors. Healthcare is fourth. Commercial Kitchens, Aviation, and Heritage remain at the bottom as specialist niches.

---

## CHANGE 5: Multi-Site Rollout Page — Update Intro Copy

The introductory copy on `/services/multi-site-rollout-documentation.astro` currently mentions "retail, healthcare, hospitality, franchise" in the first paragraph. Update this to explicitly name the key sectors and link to them.

Find the paragraph that reads something like:
```
For operators running rollout programmes — retail, healthcare, hospitality, franchise — consistency is the deliverable.
```

And replace with:
```html
For operators running rollout programmes — <a href="/services/qsr-restaurant-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">QSR and restaurant remodel</a>, <a href="/services/aba-autism-clinic-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">ABA therapy clinic expansion</a>, <a href="/services/retail-rollout-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">retail rebrand and refresh</a>, <a href="/services/healthcare-facility-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">healthcare network renovation</a> — consistency is the deliverable.
```

---

## CHANGE 6: Construction Documentation Page — Add Sector Cross-Links

On `/services/construction-documentation.astro`, find the bottom links section and ensure it includes links to the multi-site rollout page and at least two sector pages. If these don't already exist, add:

```html
<a href="/services/multi-site-rollout-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">Multi-site rollout programmes &rarr;</a>
<a href="/services/qsr-restaurant-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">QSR restaurant surveys &rarr;</a>
<a href="/services/aba-autism-clinic-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">ABA clinic documentation &rarr;</a>
```

---

## CHANGE 7: Pre-Construction Site Intelligence Page — Add Sector Cross-Links

On `/services/pre-construction-site-intelligence.astro`, find the bottom links section and add:

```html
<a href="/services/aba-autism-clinic-documentation" class="text-navy font-medium hover:opacity-80 transition-opacity">ABA clinic documentation &rarr;</a>
<a href="/services/qsr-restaurant-survey" class="text-navy font-medium hover:opacity-80 transition-opacity">QSR restaurant surveys &rarr;</a>
```

---

## DEPLOYMENT CHECKLIST

- [ ] Services index page updated with sector cards in Rollout section
- [ ] Services index page internal links updated
- [ ] Homepage "Who We Work With" section reworked with multi-site prominence
- [ ] Multi-site rollout page has Sector Specialisms section with cards
- [ ] Multi-site rollout page intro copy updated with sector links
- [ ] Footer Sectors column reordered (ABA first)
- [ ] Construction documentation page cross-linked to sectors
- [ ] Pre-construction intelligence page cross-linked to sectors
- [ ] All links resolve correctly
- [ ] Visual hierarchy looks correct on both desktop and mobile
- [ ] Sector cards are properly responsive (stack on mobile, 2-col on tablet, 4-col on desktop)
- [ ] Build passes with 0 errors
- [ ] git commit and push to origin and forge
