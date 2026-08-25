# -*- coding: utf-8 -*-
"""Render a take-off overlay onto a real drawing: area polygons, linear runs,
count markers and a legend. Specimen measurements, clearly labelled."""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = r"C:\Users\andre\alturascope-site\public\Images\plan-1.jpg"
OUT = "takeoff-overlay.jpg"

AREA = (58, 130, 246)      # blue   - area take-off
LINEAR = (232, 108, 60)    # orange - linear runs
COUNT = (34, 168, 120)     # green  - counts
GOLD = (201, 168, 76)


def font(sz, bold=False):
    for n in (("arialbd.ttf" if bold else "arial.ttf"), "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            continue
    return ImageFont.load_default()


im = Image.open(SRC).convert("RGB")
W, H = im.size

# lift the drawing slightly so the overlay reads on top of it
im = Image.blend(im, Image.new("RGB", (W, H), (255, 255, 255)), 0.28)

ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov, "RGBA")

# ---- area take-offs (rooms), roughly following the plan's room block ----
areas = [
    ([(455, 240), (900, 240), (900, 400), (455, 400)], "A1  Treatment 1-4", "58.4 m²"),
    ([(455, 405), (900, 405), (900, 545), (455, 545)], "A2  Corridor / circulation", "31.2 m²"),
    ([(360, 560), (760, 560), (760, 830), (360, 830)], "A3  Consult 2-5", "72.8 m²"),
    ([(770, 560), (1010, 560), (1010, 830), (770, 830)], "A4  Lab / sterile", "43.6 m²"),
    ([(140, 700), (350, 700), (350, 980), (140, 980)], "A5  WC block", "24.1 m²"),
]
LABEL_NUDGE = {"A1  Treatment 1-4": 46}   # keep clear of the count markers on the run
for pts, code, val in areas:
    d.polygon(pts, fill=AREA + (54,), outline=AREA + (235,), width=4)
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts) + LABEL_NUDGE.get(code, 0)
    lab = "%s\n%s" % (code, val)
    bb = d.multiline_textbbox((cx, cy), lab, font=font(21, True), anchor="mm", align="center")
    d.rounded_rectangle([bb[0] - 12, bb[1] - 8, bb[2] + 12, bb[3] + 8], 6, fill=(255, 255, 255, 232), outline=AREA + (255,), width=2)
    d.multiline_text((cx, cy), lab, font=font(21, True), fill=(20, 32, 52), anchor="mm", align="center")

# ---- linear runs (services / partitions) ----
lines = [
    ([(455, 300), (1180, 300), (1180, 520)], "L1  Sanitary drainage", "41.8 m"),
    ([(360, 860), (1010, 860)], "L2  Partition head track", "28.4 m"),
]
for pts, code, val in lines:
    d.line(pts, fill=LINEAR + (245,), width=9, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8], fill=LINEAR + (255,))
    mx, my = pts[len(pts) // 2]
    lab = "%s   %s" % (code, val)
    bb = d.textbbox((mx, my - 30), lab, font=font(20, True), anchor="mm")
    d.rounded_rectangle([bb[0] - 12, bb[1] - 7, bb[2] + 12, bb[3] + 7], 6, fill=LINEAR + (250,))
    d.text((mx, my - 30), lab, font=font(20, True), fill=(255, 255, 255), anchor="mm")

# ---- count markers ----
counts = [(505, 300), (640, 300), (775, 300), (905, 300), (1130, 640), (1230, 560), (1310, 505)]
for i, (x, y) in enumerate(counts, 1):
    d.ellipse([x - 19, y - 19, x + 19, y + 19], fill=COUNT + (240,), outline=(255, 255, 255, 255), width=3)
    d.text((x, y), str(i), font=font(19, True), fill=(255, 255, 255), anchor="mm")
lab = "C1  Sanitary fittings   7 nr"
bb = d.textbbox((1140, 700), lab, font=font(20, True), anchor="mm")
d.rounded_rectangle([bb[0] - 12, bb[1] - 7, bb[2] + 12, bb[3] + 7], 6, fill=COUNT + (250,))
d.text((1140, 700), lab, font=font(20, True), fill=(255, 255, 255), anchor="mm")

# ---- header bar ----
d.rectangle([0, 0, W, 78], fill=(11, 31, 58, 238))
d.text((26, 24), "TAKE-OFF OVERLAY", font=font(24, True), fill=(255, 255, 255))
d.text((286, 28), "Sheet P-200  Rev C  ·  Trenching & Sanitary Plan  ·  scale 1:100",
       font=font(19), fill=(210, 220, 232))
d.text((W - 26, 28), "SPECIMEN", font=font(21, True), fill=GOLD, anchor="ra")

# ---- legend ----
lx, ly = 26, H - 168
d.rounded_rectangle([lx, ly, lx + 470, ly + 142], 8, fill=(255, 255, 255, 242), outline=(11, 31, 58, 220), width=2)
d.text((lx + 18, ly + 14), "MEASURED ON THIS SHEET", font=font(16, True), fill=(90, 100, 115))
rows = [(AREA, "Area", "5 groups   ·   230.1 m²"),
        (LINEAR, "Linear", "2 runs   ·   70.2 m"),
        (COUNT, "Count", "1 group   ·   7 nr")]
for i, (col, k, v) in enumerate(rows):
    y = ly + 46 + i * 30
    d.rectangle([lx + 18, y, lx + 44, y + 18], fill=col + (255,))
    d.text((lx + 56, y + 1), k, font=font(19, True), fill=(20, 32, 52))
    d.text((lx + 150, y + 1), v, font=font(19), fill=(60, 72, 90))

out = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
out.save(OUT, quality=88, optimize=True)
print("wrote", OUT, out.size, round(os.path.getsize(OUT) / 1024), "KB")
