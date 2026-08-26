"""One-off restructure of the two Estimating Desk pages.

The pages measured 18.9 desktop screens / 33.1 mobile screens: 19 stacked
full-bleed sections, each carrying 240px of vertical padding before a word of
copy. The copy itself is good and carries the page's search weight, so this
does not delete argument - it changes the *shape*:

  1. the free sample-pack offer moves from 38% down the page to screen two
  2. the six "what comes back" blocks become a two-column grid
  3. the nine audit checks become a two-column grid
  4. "Independence" folds into "The moat" - both are the same point
  5. lower sections drop to section-padding-tight

Run once, then delete. Idempotent: re-running detects the work is done.
"""
import re
import sys

FILES = [
    "src/pages/estimating/index.astro",
    "src/pages/uk/estimating.astro",
]


def take_section(src, comment):
    """Return (block, start, end) for the section introduced by `comment`."""
    i = src.index(comment)
    # rewind to the start of the comment's own line
    start = src.rindex("\n", 0, i) + 1
    end_marker = "\n    </section>\n"
    j = src.index(end_marker, i) + len(end_marker)
    return src[start:j], start, j


def move_sample_pack_up(src):
    """Move 'See the pack' to sit directly after the stats bar."""
    block, start, end = take_section(src, "<!-- See the pack -->")
    src = src[:start] + src[end:]
    _, _, stats_end = take_section(src, "<!-- Stats -->")
    return src[:stats_end] + "\n" + block + src[stats_end:]


def two_column_deliverables(src):
    """The six 'what comes back' blocks become a 2-up grid."""
    block_re = re.compile(
        r'        <div class="mt-1[26]">\n'
        r'          <h3 class="text-\[1\.35rem\] font-medium text-navy">[\s\S]*?\n'
        r'        </div>\n'
    )
    sec, start, end = take_section(src, "<!-- What comes back -->")
    blocks = block_re.findall(sec)
    if len(blocks) != 6:
        sys.exit(f"expected 6 deliverable blocks, found {len(blocks)}")

    stripped = block_re.sub("", sec)
    # normalise each block's own top margin - the grid owns the spacing now
    cells = [b.replace('<div class="mt-16">', "<div>", 1)
              .replace('<div class="mt-12">', "<div>", 1) for b in blocks]
    grid = (
        '        <div class="mt-14 grid grid-cols-1 md:grid-cols-2 gap-x-14 gap-y-12">\n'
        + "".join(cells)
        + "        </div>\n"
    )
    # re-insert the grid just before the section's closing markup
    tail = "      </div>\n    </section>\n"
    stripped = stripped.replace(tail, grid + tail)
    stripped = stripped.replace("max-w-[900px] mx-auto px-6", "max-w-[1180px] mx-auto px-6", 1)
    return src[:start] + stripped + src[end:]


def two_column_audit(src):
    """The nine deterministic checks become a 2-up grid of stacked rows."""
    sec, start, end = take_section(src, "<!-- Machine audit -->")
    sec = sec.replace(
        '<div class="mt-14 space-y-0">',
        '<div class="mt-14 grid grid-cols-1 lg:grid-cols-2 lg:gap-x-14">',
        1,
    )
    sec = sec.replace(
        'class="grid grid-cols-1 md:grid-cols-[190px_1fr] gap-2 md:gap-8 border-t border-white/15 py-6"',
        'class="border-t border-white/15 py-5"',
    )
    sec = sec.replace(
        'class="grid grid-cols-1 md:grid-cols-[190px_1fr] gap-2 md:gap-8 border-t border-b border-white/15 py-6"',
        'class="border-t border-white/15 py-5"',
    )
    sec = sec.replace('<p class="label text-gold">', '<p class="label text-gold mb-2">')
    return src[:start] + sec + src[end:]


def fold_independence_into_moat(src):
    """'We don't build it' is the same argument as the moat. One section, not two."""
    ind, ind_start, ind_end = take_section(src, "<!-- Independence -->")
    heading = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', ind).group(1).strip()
    body = re.search(r'<p class="mt-6 text-midgrey leading-body[^"]*">([\s\S]*?)</p>', ind).group(1).strip()
    src = src[:ind_start] + src[ind_end:]

    inset = (
        '\n        <div class="mt-10 border-l-2 border-gold bg-offwhite py-6 px-7">\n'
        f'          <p class="text-navy font-medium leading-snug text-[1.05rem]">{heading}</p>\n'
        f'          <p class="mt-3 text-midgrey leading-body">{body}</p>\n'
        "        </div>\n"
    )
    moat, m_start, m_end = take_section(src, "<!-- The moat -->")
    tail = "      </div>\n    </section>\n"
    moat = moat.replace(tail, inset + tail)
    moat = moat.replace("max-w-[900px] mx-auto px-6", "max-w-[1000px] mx-auto px-6", 1)
    return src[:m_start] + moat + src[m_end:]


def tighten_lower_padding(src):
    """Sections past the process step no longer need 120px of air."""
    for comment in ["<!-- The portal -->", "<!-- Responsibility -->", "<!-- Vyntworks -->",
                    "<!-- The moat -->", "<!-- Supply chain -->", "<!-- Engagement -->",
                    "<!-- FAQ -->"]:
        sec, start, end = take_section(src, comment)
        sec = sec.replace(' section-padding"', ' section-padding-tight"', 1)
        sec = sec.replace(' section-padding scroll-mt-24"', ' section-padding-tight scroll-mt-24"', 1)
        src = src[:start] + sec + src[end:]
    return src


for path in FILES:
    original = open(path, encoding="utf-8").read()
    if "section-padding-tight" in original:
        print(f"  {path}: already restructured, skipping")
        continue

    src = original.replace("    <!-- How it works -->\n    <!-- Who signs it -->",
                           "    <!-- Who signs it -->")  # stray comment in the UK file
    src = move_sample_pack_up(src)
    src = two_column_deliverables(src)
    src = two_column_audit(src)
    src = fold_independence_into_moat(src)
    src = tighten_lower_padding(src)

    open(path, "w", encoding="utf-8").write(src)
    before = original.count("<section")
    after = src.count("<section")
    print(f"  {path}: {before} -> {after} sections")
