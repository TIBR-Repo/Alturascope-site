"""Second pass on the Estimating Desk pages.

Reshaping alone got them from 18.9 to 17.3 screens. The rest of the length is
genuine argument, and a considered B2B purchase earns it - but only if the
reader can skip to the part they came for. So:

  1. two real deletions, both of copy duplicated elsewhere on the site
  2. anchor ids on the sections a buyer actually looks for
  3. a sticky in-page sub-nav under the hero

Run once, then delete. Idempotent.
"""
import re
import sys

FILES = {
    "src/pages/estimating/index.astro": "us",
    "src/pages/uk/estimating.astro": "uk",
}

SECTION_IDS = {
    "<!-- What comes back -->": "what-you-get",
    "<!-- Machine audit -->": "the-audit",
    "<!-- How it works -->": "how-it-works",
    "<!-- Engagement -->": "pricing",
    "<!-- FAQ -->": "faq",
}

SUBNAV = """
    <!-- In-page navigation -->
    <nav class="sticky top-[64px] z-40 bg-white/95 backdrop-blur border-b border-border" aria-label="On this page">
      <div class="max-w-[1200px] mx-auto px-6">
        <ul class="flex items-center gap-6 md:gap-9 overflow-x-auto whitespace-nowrap py-3.5 -mb-px list-none m-0">
          <li><a href="#what-you-get" class="subnav-link text-[0.82rem] font-medium tracking-nav text-midgrey hover:text-navy transition-colors">What you get</a></li>
          <li><a href="#the-audit" class="subnav-link text-[0.82rem] font-medium tracking-nav text-midgrey hover:text-navy transition-colors">The audit</a></li>
          <li><a href="#how-it-works" class="subnav-link text-[0.82rem] font-medium tracking-nav text-midgrey hover:text-navy transition-colors">How it works</a></li>
          <li><a href="#pricing" class="subnav-link text-[0.82rem] font-medium tracking-nav text-midgrey hover:text-navy transition-colors">Pricing</a></li>
          <li><a href="#faq" class="subnav-link text-[0.82rem] font-medium tracking-nav text-midgrey hover:text-navy transition-colors">Questions</a></li>
          <li class="ml-auto pl-6 hidden md:block"><a href="#send-a-package" class="text-[0.82rem] font-medium tracking-nav text-navy border-b-2 border-gold pb-0.5">SEND_LABEL</a></li>
        </ul>
      </div>
    </nav>
"""


def take_section(src, comment):
    i = src.index(comment)
    start = src.rindex("\n", 0, i) + 1
    end_marker = "\n    </section>\n"
    j = src.index(end_marker, i) + len(end_marker)
    return src[start:j], start, j


def drop_responsibility_checklist(src):
    """The 'on every pack, without exception' box is the Basis of Estimate page
    reproduced inline. Link to it instead - the page needs the inbound link."""
    sec, start, end = take_section(src, "<!-- Responsibility -->")
    box = re.search(
        r'\n        <div class="mt-10 border border-border bg-offwhite p-8">[\s\S]*?\n        </div>\n',
        sec,
    )
    if not box:
        sys.exit("responsibility checklist box not found")
    replacement = (
        '\n        <div class="mt-10 border-l-2 border-gold bg-offwhite py-6 px-7">\n'
        '          <p class="text-midgrey leading-body">\n'
        '            <span class="text-navy font-medium">Every pack states its basis, carries its audit report, '
        'and waits for your sign-off.</span> Two revisions are included, we sign your non-disclosure agreement '
        'before the drawings arrive, we will not price the same package for two bidders, and the liability '
        'position is stated plainly in the engagement terms rather than buried in a footer.\n'
        '          </p>\n'
        '          <p class="mt-4">\n'
        '            <a href="/estimating/basis-of-estimate/" class="text-navy font-medium border-b border-gold pb-0.5 hover:opacity-80 transition-opacity">Read the Basis of Estimate standard &rarr;</a>\n'
        '          </p>\n'
        "        </div>\n"
    )
    sec = sec.replace(box.group(0), replacement)
    return src[:start] + sec + src[end:]


def trim_portal_cards(src):
    """Six cards, two of which restate the audit section and the FAQ."""
    sec, start, end = take_section(src, "<!-- The portal -->")
    before = sec.count('<div class="bg-white p-8">')
    for heading in ["Read the audit", "Or just ask us"]:
        card = re.search(
            r'\n          <div class="bg-white p-8">\n'
            r'            <h3 class="text-\[1\.05rem\] font-medium text-navy">' + re.escape(heading) +
            r'</h3>[\s\S]*?\n          </div>',
            sec,
        )
        if not card:
            sys.exit(f"portal card not found: {heading}")
        sec = sec.replace(card.group(0), "")
    after = sec.count('<div class="bg-white p-8">')
    print(f"      portal cards {before} -> {after}")
    return src[:start] + sec + src[end:]


for path, locale in FILES.items():
    src = open(path, encoding="utf-8").read()
    if "subnav-link" in src:
        print(f"  {path}: already has in-page nav, skipping")
        continue

    src = drop_responsibility_checklist(src)
    src = trim_portal_cards(src)

    # anchor ids
    for comment, anchor in SECTION_IDS.items():
        sec, start, end = take_section(src, comment)
        if 'id="' in sec.split("\n")[1]:
            continue
        sec = sec.replace("<section class=", f'<section id="{anchor}" class=', 1)
        sec = sec.replace('class="bg-', 'class="scroll-mt-32 bg-', 1)
        src = src[:start] + sec + src[end:]

    # sticky sub-nav, immediately after the hero
    _, _, hero_end = take_section(src, "<!-- Hero -->")
    label = "Send a tender package" if locale == "uk" else "Send a bid package"
    src = src[:hero_end] + SUBNAV.replace("SEND_LABEL", label) + src[hero_end:]

    open(path, "w", encoding="utf-8").write(src)
    print(f"  {path}: in-page nav added")
