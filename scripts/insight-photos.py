# -*- coding: utf-8 -*-
"""Prepare survey photographs for publication in Insights articles.

The articles make specific claims - "a 42-way panel with three spare ways", "a
meter above the ceiling, outside the demise". Those read as assertions until
there is a photograph of the thing. This takes selected frames out of the local
survey libraries and turns them into web assets.

Rules baked in, because they are the client-confidentiality boundary Andrew set:

  * ALL metadata stripped. These are phone photographs; even where GPS is absent
    the camera body, serial and timestamps have no business being published.
  * Nothing here may show branding or a storefront. That is enforced by the
    selection below, not by the code - every entry was chosen by eye, and four
    candidates were dropped after review for being too blurry or too cluttered
    to carry the point they were meant to illustrate.
  * Longest edge capped at 1400px, plus a 640w variant for phones.

Run:  python scripts/insight-photos.py
"""
import io, os, sys
from PIL import Image

JATJ = r"C:\Users\andre\Documents\JatJ"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "public", "Images", "insights")
STAGE = os.path.join(JATJ, "1100NewYorkAve", "upload_staging")

# slug -> source file. Back-of-house services and plant only.
PHOTOS = {
    # above the ceiling
    "void-service-congestion":  (STAGE, "Above ceiling - Service congestion in void - 101543.jpg"),
    "void-services":            (STAGE, "Above ceiling - Void services - 090718.jpg"),
    "ceiling-access-point":     (STAGE, "Above ceiling - access - Ceiling access point - 090616.jpg"),
    "base-building-fire-alarm": (STAGE, "Above ceiling - fire alarm - Base-building FA distribution in tenant void - 090016.jpg"),
    "duct-insulation-damaged":  (STAGE, "Above ceiling - HVAC - Duct insulation damaged - 090058.jpg"),
    # electrical
    "panel-schedule":           (STAGE, "Electrical room - Panel schedule - 102131.jpg"),
    "panel-l-schedule":         (STAGE, "Electrical room - Panel L schedule - 102155.jpg"),
    "panel-l-enclosure":        (STAGE, "Electrical room - Panel L - 102140.jpg"),
    "transformer-approach":     (STAGE, "Electrical room - Transformer approach - 102203.jpg"),
    # water
    "water-meter-outside-demise": (STAGE, "DOMESTIC WATER METER (adjacent tenant plen - WATER METER - located OUTSIDE the demise - 101628.jpg"),
    "backflow-nameplate":       (STAGE, "BACKFLOW - NAMEPLATE - PLATE Zurn Wilkins 375 RPZ, 175 psi - 100434.jpg"),
    # plant
    "chiller-nameplate":        (STAGE, "CHILLER NAMEPLATE - KEY base building runs a CENTRAL CHILLED WATER PLANT - 100826.jpg"),
    # kitchen / grease
    "grease-receptor":          (STAGE, "GREASE RECEPTOR - CONFIRMED grease receptor - above floor, NOT in-slab - 083922.jpg"),
    "hood-underside-filters":   (STAGE, "HOOD - Hood underside - filters - 084230.jpg"),
}

WIDTHS = [640, 1400]


def main():
    os.makedirs(OUT, exist_ok=True)
    missing, made = [], []
    for slug, (folder, name) in PHOTOS.items():
        src = os.path.join(folder, name)
        if not os.path.exists(src):
            missing.append(name)
            continue
        with Image.open(src) as im:
            im = im.convert("RGB")           # drops the alpha and, with it, nothing useful
            ow, oh = im.size
            for w in WIDTHS:
                if w > ow:
                    w = ow
                target = im.resize((w, max(1, round(oh * w / ow))), Image.LANCZOS)
                suffix = "" if w == WIDTHS[-1] else "-%dw" % w
                out = os.path.join(OUT, "%s%s.webp" % (slug, suffix))
                # No exif= argument: Pillow writes none, so every tag is gone.
                target.save(out, "WEBP", quality=78, method=6)
            made.append(slug)

    print("wrote %d photographs to public/Images/insights/" % len(made))
    for s in sorted(made):
        p = os.path.join(OUT, s + ".webp")
        print("   %-30s %6d KB" % (s, os.path.getsize(p) // 1024))
    if missing:
        print("\nMISSING (%d):" % len(missing))
        for m in missing:
            print("   " + m)
        sys.exit(1)

    # prove the metadata is gone
    from PIL import Image as I
    bad = []
    for s in made:
        with I.open(os.path.join(OUT, s + ".webp")) as im:
            if im.getexif():
                bad.append(s)
    print("\nmetadata check: %s" % ("STRIPPED on all files" if not bad else "STILL PRESENT on " + ", ".join(bad)))


if __name__ == "__main__":
    main()
