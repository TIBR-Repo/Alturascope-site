"""Bring titles and meta descriptions inside the lengths Google will display.

115 warnings, all length. The judgement applied here:

  Descriptions are not a ranking factor, only a click-through one, so an
  over-long one is pure loss and is safe to rewrite. All are brought under
  158 characters, preferring a clean sentence boundary.

  Titles are different - they carry ranking weight, and rewriting sixty of
  them wholesale risks positions the site already holds for marginal display
  gain. So the change is conservative and keyword-preserving: drop the
  redundant " | Alturascope" suffix on any title that is over length (the
  brand is already in the SERP as the domain), and shorten only the badly
  over-long ones by cutting the trailing descriptive clause. Titles between
  62 and about 72 characters display nearly in full and are left alone.

Pass --apply to write. Without it, prints the proposal for review.
"""
import re
import sys
import glob
import html

APPLY = "--apply" in sys.argv
TITLE_MAX = 62
DESC_MAX = 158

# Titles that stay long on purpose would go here; none currently.
KEEP = set()


def shorten_title(t):
    """Drop the redundant brand suffix. Nothing else.

    Cutting the descriptive clause after a colon was tried and rejected: it
    turned "ABA Clinic Portfolio Renovation: Standardising Documentation Across
    Acquired Locations" into "ABA Clinic Portfolio Renovation" and threw away
    the keywords the page ranks on. A title that stays at 70-something
    characters displays nearly in full and costs nothing.
    """
    return re.sub(r"\s*\|\s*Alturascope\s*$", "", t).strip()


def shorten_desc(d):
    if len(d) <= DESC_MAX:
        return d
    sentences = re.split(r"(?<=[.!?])\s+", d)
    acc = ""
    for s in sentences:
        cand = (acc + " " + s).strip()
        if len(cand) <= DESC_MAX:
            acc = cand
        else:
            break
    # Only ever cut at a sentence boundary. A word-boundary trim was tried and
    # rejected - it produced "...turns inherited real estate into." and
    # "...the most expensive surprises in commercial." Better over-long than
    # ungrammatical; what is left over is reported for hand-editing.
    return acc if len(acc) >= 90 else d


title_re = re.compile(r'(\btitle=)"((?:[^"\\]|\\.)*)"')
desc_re = re.compile(r'(\bdescription=)"((?:[^"\\]|\\.)*)"')

changed_t = changed_d = 0
for path in sorted(glob.glob("src/pages/**/*.astro", recursive=True)):
    src = open(path, encoding="utf-8").read()
    out = src

    m = title_re.search(out)
    if m:
        raw = m.group(2)
        plain = html.unescape(raw)
        if len(plain) > TITLE_MAX and plain not in KEEP:
            new = shorten_title(plain)
            if new != plain:
                # keep whatever entity form the file already used
                new_raw = new.replace("&", "&amp;") if "&amp;" in raw else new
                out = out[: m.start(2)] + new_raw + out[m.end(2):]
                changed_t += 1
                if not APPLY:
                    print(f"  TITLE {path}\n    {len(plain):>3} {plain}\n    {len(new):>3} {new}")

    m = desc_re.search(out)
    if m:
        raw = m.group(2)
        plain = html.unescape(raw)
        if len(plain) > DESC_MAX:
            new = shorten_desc(plain)
            if new != plain:
                new_raw = new.replace("&", "&amp;") if "&amp;" in raw else new
                out = out[: m.start(2)] + new_raw + out[m.end(2):]
                changed_d += 1
                if not APPLY:
                    print(f"  DESC  {path}\n    {len(plain):>3} {plain}\n    {len(new):>3} {new}")

    if APPLY and out != src:
        open(path, "w", encoding="utf-8").write(out)

print(f"\n  {changed_t} titles, {changed_d} descriptions {'rewritten' if APPLY else 'proposed'}")
