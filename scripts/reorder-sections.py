"""Reorder the SECTIONS array in sample-project.astro.

Operates on the literal text of each section object (delimited by the leading
'  {' and matching '  },' at two-space indentation inside the SECTIONS array)
and rewrites them in the requested order. Content of each section is preserved
byte-for-byte.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "src" / "pages" / "work" / "sample-project.astro"

NEW_ORDER = [
    "siteoverview",
    "narrative",
    "generalcondition",
    "recommendations",
    "exterior",
    "electrical",
    "hvac",
    "plumbing",
    "lifesafety",
    "aboveceiling",
    "hvacschedule",
    "equipmentreuse",
    "walkin",
    "foodservice",
    "thermal",
    "restrooms",
]


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")

    start_marker = "const SECTIONS = [\n"
    end_marker = "\n];\n"
    start_idx = text.find(start_marker)
    if start_idx < 0:
        print("ERROR: SECTIONS array start not found")
        return 1
    body_start = start_idx + len(start_marker)
    end_idx = text.find(end_marker, body_start)
    if end_idx < 0:
        print("ERROR: SECTIONS array end not found")
        return 1
    body = text[body_start:end_idx]

    # Split into individual section blocks. Each block begins at a line that is
    # exactly "  {" and ends at the line "  }," that closes it. We walk the body
    # line by line and group by brace depth at the section level.
    lines = body.split("\n")
    blocks = []
    current = []
    depth = 0
    in_block = False
    for line in lines:
        if not in_block:
            if line == "  {":
                in_block = True
                depth = 1
                current = [line]
            # otherwise ignore inter-block whitespace
            continue
        current.append(line)
        # track brace depth for this section block (count { and } per line)
        depth += line.count("{") - line.count("}")
        if depth == 0:
            # line should be "  },"
            blocks.append("\n".join(current))
            current = []
            in_block = False

    print(f"Parsed {len(blocks)} section blocks")

    # Map id -> block
    by_id = {}
    for blk in blocks:
        m = re.search(r'id:\s*"([^"]+)"', blk)
        if not m:
            print(f"WARN: block has no id, skipping:\n{blk[:80]}")
            continue
        by_id[m.group(1)] = blk

    missing = [sid for sid in NEW_ORDER if sid not in by_id]
    extra = [sid for sid in by_id if sid not in NEW_ORDER]
    if missing:
        print(f"ERROR: NEW_ORDER references missing ids: {missing}")
        return 1
    if extra:
        print(f"ERROR: file contains ids not in NEW_ORDER: {extra}")
        return 1
    if len(by_id) != len(NEW_ORDER):
        print(f"ERROR: count mismatch ({len(by_id)} vs {len(NEW_ORDER)})")
        return 1

    new_body = "\n".join(by_id[sid] for sid in NEW_ORDER)

    new_text = text[:body_start] + new_body + text[end_idx:]
    PAGE.write_text(new_text, encoding="utf-8")
    print(f"Rewrote {PAGE} with sections in new order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
