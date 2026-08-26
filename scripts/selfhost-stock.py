"""Bring the remaining stock imagery onto our own origin.

The service and UK pages now carry Alturascope's own photography. What is left
is editorial imagery inside insight articles and a few body images, where
variety matters more than provenance. Those stay, but they stop being requests
to images.unsplash.com: 134 references to a third-party CDN with no preconnect
is a render-blocking dependency on somebody else's infrastructure, and it hands
every reader's IP to a third party.

Downloads each unique photo once into public/Images/stock/ and rewrites every
reference to the local path.

Run once, then delete. Idempotent - already-local references are left alone.
"""
import os
import re
import glob
import hashlib
import urllib.request

OUT = "public/Images/stock"
os.makedirs(OUT, exist_ok=True)

pattern = re.compile(r'https://images\.unsplash\.com/photo-([0-9a-f]+-[0-9a-f]+)(\?[^"\']*)?')

# collect every reference across the source tree
files = glob.glob("src/**/*.astro", recursive=True)
ids = {}
for f in files:
    for m in pattern.finditer(open(f, encoding="utf-8").read()):
        ids.setdefault(m.group(1), set()).add(f)

print(f"  {len(ids)} unique photos across {len(set().union(*ids.values())) if ids else 0} files")

for photo_id in sorted(ids):
    dest = f"{OUT}/{photo_id}.jpg"
    if os.path.exists(dest):
        continue
    url = f"https://images.unsplash.com/photo-{photo_id}?w=1600&q=72&fm=jpg&fit=max"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as r, open(dest, "wb") as out:
            out.write(r.read())
        print(f"    downloaded {photo_id}.jpg ({os.path.getsize(dest)//1024} KB)")
    except Exception as e:
        print(f"    FAILED {photo_id}: {e}")

# rewrite references
rewritten = 0
for f in files:
    src = open(f, encoding="utf-8").read()
    new = pattern.sub(lambda m: f"/Images/stock/{m.group(1)}.jpg", src)
    if new != src:
        open(f, "w", encoding="utf-8").write(new)
        rewritten += 1

print(f"\n  {rewritten} files rewritten to local paths")
