"""Fetch Pexels stock photos for the ScopeWalk sample-project demo page.

Reads PEXELS_API_KEY from .env in the worktree root.
Writes JPEGs to public/images/demo/<folder>/<n>.jpg
Skips files that already exist (idempotent).
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
PUBLIC_DEMO = ROOT / "public" / "images" / "demo"


def load_env(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


ENV = load_env(ENV_FILE)
API_KEY = ENV.get("PEXELS_API_KEY") or os.environ.get("PEXELS_API_KEY")
if not API_KEY:
    print("ERROR: PEXELS_API_KEY not set in .env or environment", file=sys.stderr)
    sys.exit(1)


# folder -> (query string, count needed)
JOBS = [
    ("plumbing",        "commercial kitchen plumbing pipes",   8),
    ("restrooms",       "modern restroom interior",            7),
    ("electrical",      "electrical panel breaker box",       12),
    ("hvac",            "rooftop hvac air conditioning unit",  9),
    ("lifesafety",      "fire extinguisher exit sign",         6),
    ("hvacschedule",    "industrial hvac equipment",          12),
    ("exterior",        "commercial storefront facade",       14),
    ("walkin",          "walk in cooler refrigerator",        10),
    ("foodservice",     "commercial kitchen equipment",       14),
    ("drone",           "aerial drone shopping plaza",         6),
    ("site",            "empty commercial space interior",    12),
]


def http_get_json(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def fetch_pexels(query: str, count: int) -> list:
    """Return up to `count` photo URLs (large size) for `query`. Pexels max per_page=80."""
    per_page = max(15, min(80, count * 2))  # request more than we need to allow for skipping
    qs = urllib.parse.urlencode({"query": query, "per_page": per_page, "orientation": "landscape"})
    url = f"https://api.pexels.com/v1/search?{qs}"
    data = http_get_json(url, headers={"Authorization": API_KEY, "User-Agent": "Mozilla/5.0"})
    photos = data.get("photos", [])
    return [(p.get("src", {}).get("large"), p.get("photographer"), p.get("url")) for p in photos if p.get("src", {}).get("large")]


def main() -> int:
    PUBLIC_DEMO.mkdir(parents=True, exist_ok=True)
    print(f"Output base: {PUBLIC_DEMO}")
    total_downloaded = 0
    total_skipped = 0
    for folder, query, count in JOBS:
        out_dir = PUBLIC_DEMO / folder
        out_dir.mkdir(parents=True, exist_ok=True)

        # Determine which files are missing
        missing = [i for i in range(1, count + 1) if not (out_dir / f"{i}.jpg").exists()]
        if not missing:
            print(f"  [skip] {folder}: all {count} files already exist")
            total_skipped += count
            continue

        print(f"  [fetch] {folder}: query='{query}', need {len(missing)}/{count}")
        try:
            photos = fetch_pexels(query, count)
        except Exception as e:
            print(f"    !! API error for {folder}: {e}", file=sys.stderr)
            continue

        if not photos:
            print(f"    !! no photos returned for {folder}")
            continue

        idx_in_query = 0
        for n in missing:
            if idx_in_query >= len(photos):
                print(f"    !! ran out of unique photos for {folder} at file {n}")
                break
            src_url, _, _ = photos[idx_in_query]
            idx_in_query += 1
            dest = out_dir / f"{n}.jpg"
            try:
                http_download(src_url, dest)
                size_kb = dest.stat().st_size // 1024
                print(f"    -> {dest.name}  ({size_kb} KB)")
                total_downloaded += 1
            except Exception as e:
                print(f"    !! download failed for {dest.name}: {e}", file=sys.stderr)
            time.sleep(0.15)  # be polite to Pexels

    print(f"\nDone. Downloaded {total_downloaded}, skipped {total_skipped} pre-existing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
