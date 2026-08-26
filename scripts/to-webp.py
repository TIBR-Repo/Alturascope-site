"""Convert site imagery to WebP and repoint every reference.

The site shipped 22.6MB of JPEG and PNG and not one WebP or AVIF file. The
gallery alone was 4MB across 26 images, on the page we most want people to
reach.

Converts in place (keeping the original file, so anything we miss still
resolves) and rewrites src/srcset references in the source tree.

Deliberately left as-is:
  - /og/default.jpg and /logo.png - some social scrapers still refuse WebP
  - /apple-touch-icon.png - iOS wants PNG
  - favicon.svg - already vector

Run once, then delete. Idempotent.
"""
import os
import re
import glob
from PIL import Image

SKIP = {"og/default.jpg", "logo.png", "apple-touch-icon.png"}
QUALITY = 80

converted, saved_before, saved_after = 0, 0, 0
mapping = {}

for path in glob.glob("public/**/*.jpg", recursive=True) + glob.glob("public/**/*.png", recursive=True):
    rel = os.path.relpath(path, "public").replace(os.sep, "/")
    if rel in SKIP:
        continue
    dest = os.path.splitext(path)[0] + ".webp"
    web_src = "/" + rel
    web_dest = "/" + os.path.splitext(rel)[0] + ".webp"

    if not os.path.exists(dest):
        try:
            with Image.open(path) as im:
                if im.mode in ("P", "LA"):
                    im = im.convert("RGBA")
                elif im.mode == "CMYK":
                    im = im.convert("RGB")
                im.save(dest, "WEBP", quality=QUALITY, method=6)
        except Exception as e:
            print(f"    FAILED {rel}: {e}")
            continue

    before, after = os.path.getsize(path), os.path.getsize(dest)
    # Only adopt the WebP where it is actually smaller.
    if after >= before:
        os.remove(dest)
        continue
    converted += 1
    saved_before += before
    saved_after += after
    mapping[web_src] = web_dest

print(f"  {converted} images converted")
print(f"  {saved_before/1048576:.1f} MB -> {saved_after/1048576:.1f} MB "
      f"({100 - 100*saved_after//saved_before}% smaller)")

# rewrite references
files = glob.glob("src/**/*.astro", recursive=True) + glob.glob("src/**/*.json", recursive=True)
touched = 0
for f in files:
    src = open(f, encoding="utf-8").read()
    new = src
    for old, dest in mapping.items():
        new = new.replace(f'"{old}"', f'"{dest}"')
        new = new.replace(f"'{old}'", f"'{dest}'")
    if new != src:
        open(f, "w", encoding="utf-8").write(new)
        touched += 1

# the gallery and pack pages build their paths from a slug, so patch the templates
for f, old, new in [
    ("src/pages/work/locations.astro", "/Images/locations/${loc.slug}.jpg", "/Images/locations/${loc.slug}.webp"),
    ("src/components/GalleryBand.astro", "/Images/locations/${loc.slug}.jpg", "/Images/locations/${loc.slug}.webp"),
]:
    if not os.path.exists(f):
        continue
    src = open(f, encoding="utf-8").read()
    if old in src:
        open(f, "w", encoding="utf-8").write(src.replace(old, new))
        touched += 1
        print(f"  templated path patched in {f}")

print(f"  {touched} source files rewritten")
