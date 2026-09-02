# -*- coding: utf-8 -*-
"""Mobile image pass.

Two problems, one script.

1. Thirteen service pages carry a malformed one-entry `srcset` left behind when
   the August work swapped the heroes to real Alturascope photography. A
   single-candidate srcset with no width descriptor always beats `src`, so those
   pages have been serving the old stock image ever since - including
   /services/qsr-restaurant-survey/ and /services/pre-construction-site-intelligence/.

2. Every hero is a ~1600px image sent whole to a 390px phone, eager, as the LCP
   element. No page has a real srcset.

So: strip the bad srcsets, generate 640w/1024w variants of every hero, and emit
a proper width-descriptor srcset everywhere a hero is rendered.
"""
import io, os, re, glob, sys
from PIL import Image

ROOT = r"C:\Users\andre\alturascope-site"
PUB = os.path.join(ROOT, "public")
WIDTHS = [640, 1024]

# ---------------------------------------------------------------- variants ---
def public_path(url):
    return os.path.join(PUB, url.lstrip("/").replace("/", os.sep))

def variants_for(url):
    """Generate -640/-1024 next to the original. Returns [(url, width), ...]."""
    src = public_path(url)
    if not os.path.exists(src):
        return None
    with Image.open(src) as im:
        ow, oh = im.size
        out = []
        for w in WIDTHS:
            if w >= ow:
                continue
            vurl = re.sub(r"\.webp$", "-%dw.webp" % w, url)
            vpath = public_path(vurl)
            if not os.path.exists(vpath):
                im.copy().resize((w, max(1, round(oh * w / ow))), Image.LANCZOS).save(
                    vpath, "WEBP", quality=72, method=6)
            out.append((vurl, w))
        out.append((url, ow))
    return out

def srcset_str(url):
    v = variants_for(url)
    if not v or len(v) < 2:
        return None
    return ", ".join("%s %dw" % (u, w) for u, w in v)

# ------------------------------------------------------- collect hero urls ---
heroes = set()
for p in glob.glob(os.path.join(ROOT, "dist", "**", "index.html"), recursive=True):
    h = io.open(p, encoding="utf-8").read()
    for tag in re.findall(r"<img\b[^>]*?>", h):
        if 'loading="eager"' not in tag:
            continue
        m = re.search(r'src="([^"]+\.webp)"', tag)
        if m:
            heroes.add(m.group(1))

made = {}
for u in sorted(heroes):
    ss = srcset_str(u)
    if ss:
        made[u] = ss
print("hero images with variants: %d" % len(made))
for u in sorted(made):
    print("   " + u)

# ------------------------------------------------- 1. strip stale srcsets ----
stripped = 0
for p in glob.glob(os.path.join(ROOT, "src", "pages", "**", "*.astro"), recursive=True):
    s = io.open(p, encoding="utf-8").read()
    # srcset="<newline+spaces>/one/file.webp"  followed by an optional sizes line
    new = re.sub(r'\n\s*srcset="\s*\n?\s*/[^"]+?"(\n\s*sizes="[^"]*")?', "", s)
    if new != s:
        io.open(p, "w", encoding="utf-8", newline="").write(new)
        stripped += 1
print("\nstripped stale srcset from %d files" % stripped)

# --------------------------------------- 2. add real srcset to hero <img> ----
def add_srcset(match):
    tag = match.group(0)
    if "srcset" in tag or 'loading="eager"' not in tag:
        return tag
    m = re.search(r'src="([^"]+\.webp)"', tag)
    if not m or m.group(1) not in made:
        return tag
    ss = made[m.group(1)]
    return tag.replace(
        'src="%s"' % m.group(1),
        'src="%s"\n          srcset="%s"\n          sizes="100vw"' % (m.group(1), ss),
        1)

patched = 0
for p in glob.glob(os.path.join(ROOT, "src", "pages", "**", "*.astro"), recursive=True):
    s = io.open(p, encoding="utf-8").read()
    new = re.sub(r"<img\b[^>]*?>", add_srcset, s, flags=re.S)
    if new != s:
        io.open(p, "w", encoding="utf-8", newline="").write(new)
        patched += 1
print("added srcset to %d static hero pages" % patched)
