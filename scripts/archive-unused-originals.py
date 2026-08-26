"""Keep the JPEG/PNG originals in the repo but out of the deploy.

Everything referenced by a page is now WebP, so shipping both formats doubled
the image payload for no benefit. The originals move to assets-source/, which
Astro does not publish - they stay in version control as the masters, and the
deploy carries one format.

Protected regardless of what the reference scan says:
  - og/, logo.png, apple-touch-icon.png, favicon - referenced by absolute URL
    or by crawlers rather than by a page
  - Images/pack/uk-*.jpg - the UK sample pack, about to be used
"""
import os
import re
import glob
import shutil

PROTECT = re.compile(r'^/(og/|logo\.png|apple-touch-icon\.png|favicon|Images/pack/uk-)')

referenced = set()
for f in glob.glob("dist/**/*.html", recursive=True) + glob.glob("dist/**/*.xml", recursive=True):
    text = open(f, encoding="utf-8", errors="ignore").read()
    # relative and absolute forms both count
    for m in re.findall(r'["\'(](?:https://alturascope\.com)?(/[A-Za-z0-9._/\-]+\.(?:jpg|jpeg|png|webp|mp4|pdf))', text):
        referenced.add(m)

moved, freed = 0, 0
for path in sorted(glob.glob("public/**/*.jpg", recursive=True) + glob.glob("public/**/*.png", recursive=True)):
    rel = "/" + os.path.relpath(path, "public").replace(os.sep, "/")
    if rel in referenced or PROTECT.match(rel):
        continue
    # only archive an original whose WebP replacement actually exists
    webp = os.path.splitext(path)[0] + ".webp"
    if not os.path.exists(webp):
        print(f"    keeping {rel} - no WebP replacement")
        continue
    dest = os.path.join("assets-source", os.path.relpath(path, "public"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    freed += os.path.getsize(path)
    shutil.move(path, dest)
    moved += 1

print(f"  {moved} originals archived to assets-source/, {freed/1048576:.1f} MB out of the deploy")
