"""Third and final pass on the Estimating Desk pages.

Two merges of arguments that were being made twice:

  1. "Someone is accountable for the number" (Andrew's portrait and bio) is the
     same claim as "A desk, not a person" - who prices it and who signs it.
     The portrait moves into that section, the standalone section goes.
  2. The Vyntworks section carried a two-card grid restating what the section's
     own prose already said. It becomes one inset.

Run once, then delete. Idempotent.
"""
import re
import sys

FILES = ["src/pages/estimating/index.astro", "src/pages/uk/estimating.astro"]


def take_section(src, comment):
    i = src.index(comment)
    start = src.rindex("\n", 0, i) + 1
    end_marker = "\n    </section>\n"
    j = src.index(end_marker, i) + len(end_marker)
    return src[start:j], start, j


def merge_portrait_into_desk(src):
    sec, start, end = take_section(src, "<!-- Who signs it -->")
    paras = re.findall(r'<p>\s*([\s\S]*?)\s*</p>', sec)
    if len(paras) < 2:
        sys.exit("could not read the accountability copy")
    src = src[:start] + src[end:]

    block = (
        '\n        <div class="mt-12 border border-border bg-offwhite">\n'
        '          <div class="grid md:grid-cols-[minmax(0,220px)_1fr] gap-8 md:gap-11 items-center p-8 md:p-10">\n'
        '            <figure class="m-0">\n'
        '              <img\n'
        '                src="/Images/aph-image.jpg"\n'
        '                alt="Andrew Harris, founder of Alturascope"\n'
        '                width="1150"\n'
        '                height="1533"\n'
        '                loading="lazy"\n'
        '                decoding="async"\n'
        '                class="w-full h-auto"\n'
        '              />\n'
        '            </figure>\n'
        '            <div>\n'
        '              <p class="label text-gold mb-3">The Name On It</p>\n'
        '              <h3 class="text-[1.3rem] font-medium text-navy leading-snug">Someone is accountable for the number.</h3>\n'
        f'              <p class="mt-4 text-midgrey leading-body text-[0.95rem]">{paras[0]}</p>\n'
        f'              <p class="mt-3 text-midgrey leading-body text-[0.95rem]">{paras[1]}</p>\n'
        '              <p class="mt-4 text-midgrey/70 text-[0.88rem]">&mdash; Andrew Harris, Founder</p>\n'
        '            </div>\n'
        '          </div>\n'
        "        </div>\n"
    )
    desk, d_start, d_end = take_section(src, "<!-- The desk -->")
    tail = "      </div>\n    </section>\n"
    desk = desk.replace(tail, block + tail)
    return src[:d_start] + desk + src[d_end:]


def slim_vyntworks(src):
    sec, start, end = take_section(src, "<!-- Vyntworks -->")
    grid = re.search(
        r'\n        <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-7">[\s\S]*?\n        </div>\n',
        sec,
    )
    if not grid:
        sys.exit("vyntworks card grid not found")
    replacement = (
        '\n        <div class="mt-10 border border-gold/40 bg-white/[0.03] p-8 max-w-[68ch]">\n'
        '          <p class="text-offwhite/80 leading-body">\n'
        '            <span class="text-gold font-medium">You already have an account.</span> Every client gets one, '
        'set up by us, at no cost and with no licence attached &mdash; it is simply where your estimate is waiting. '
        'Licensed properly, the same system carries the job on through purchase orders, subcontract packages, cost '
        'control and the final account, and the quote you won becomes the budget without anything being re-keyed.\n'
        '          </p>\n'
        '          <p class="mt-5">\n'
        '            <a href="https://vyntworks.com" target="_blank" rel="noopener" class="text-offwhite font-medium border-b border-gold pb-0.5 hover:opacity-80 transition-opacity text-[0.95rem]">vyntworks.com &rarr;</a>\n'
        '          </p>\n'
        "        </div>\n"
    )
    sec = sec.replace(grid.group(0), replacement)
    return src[:start] + sec + src[end:]


for path in FILES:
    src = open(path, encoding="utf-8").read()
    if "<!-- Who signs it -->" not in src:
        print(f"  {path}: already merged, skipping")
        continue
    src = merge_portrait_into_desk(src)
    src = slim_vyntworks(src)
    open(path, "w", encoding="utf-8").write(src)
    print(f"  {path}: portrait merged into the desk, Vyntworks slimmed -> {src.count('<section')} sections")
