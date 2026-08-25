# -*- coding: utf-8 -*-
"""Rank a photo archive for website suitability so only a shortlist needs human review.

Scores each image on sharpness, spatial distribution of detail (a scene rather than a
flat close-up), tonal range, colour interest and orientation. Writes scores.json.
"""
import os, sys, glob, json, math
import numpy as np
from PIL import Image, ImageOps

EXT = ('.jpg', '.jpeg', '.png')
WORK = 360  # analysis size


def laplacian_var(g):
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    h, w = g.shape
    out = np.zeros((h - 2, w - 2), dtype=np.float32)
    for dy in range(3):
        for dx in range(3):
            if k[dy, dx]:
                out += k[dy, dx] * g[dy:h - 2 + dy, dx:w - 2 + dx]
    return float(out.var())


def score_image(path):
    if '\\Dropbox\\' in path or '/Dropbox/' in path:
        raise RuntimeError('refusing to read a Dropbox path - may trigger a download: ' + path)
    try:
        im = Image.open(path)
        im.draft('RGB', (WORK * 2, WORK * 2))   # decode at reduced size: far faster on 25MB JPEGs
        im = ImageOps.exif_transpose(im).convert('RGB')
    except Exception:
        return None
    W0, H0 = im.size
    im.thumbnail((WORK, WORK))
    a = np.asarray(im, dtype=np.float32) / 255.0
    if a.ndim != 3 or a.shape[0] < 40 or a.shape[1] < 40:
        return None
    g = a.mean(axis=2)

    # 1. sharpness
    sharp = laplacian_var(g)
    s_sharp = min(sharp / 0.006, 1.0)

    # 2. detail spread — is detail spread across the frame (a scene) or
    #    concentrated / absent (a flat wall, a close-up of a label)?
    gy, gx = np.gradient(g)
    edge = np.hypot(gx, gy)
    H, W = edge.shape
    cells = []
    for r in range(4):
        for c in range(4):
            cells.append(edge[r * H // 4:(r + 1) * H // 4, c * W // 4:(c + 1) * W // 4].mean())
    cells = np.array(cells)
    occupancy = float((cells > cells.max() * 0.25).sum()) / 16.0   # fraction of frame with real detail
    s_spread = occupancy

    # 3. tonal range without clipping
    p2, p98 = np.percentile(g, 2), np.percentile(g, 98)
    s_range = min(float(p98 - p2) / 0.75, 1.0)
    blown = float((g > 0.97).mean())
    crushed = float((g < 0.03).mean())
    s_clip = max(0.0, 1.0 - (blown + crushed) * 6.0)

    # 4. colour interest
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    s_colour = min(float(sat.mean()) / 0.30, 1.0)

    # 5. orientation — landscape works for web bands
    ar = W0 / float(H0)
    s_orient = 1.0 if ar >= 1.25 else (0.55 if ar >= 0.95 else 0.3)

    # 6. resolution floor
    s_res = 1.0 if min(W0, H0) >= 1200 else 0.5

    total = (s_sharp * 0.22 + s_spread * 0.28 + s_range * 0.14 +
             s_clip * 0.10 + s_colour * 0.10 + s_orient * 0.11 + s_res * 0.05)

    return {
        'path': path, 'score': round(total, 4), 'sharp': round(s_sharp, 3),
        'spread': round(s_spread, 3), 'range': round(s_range, 3), 'clip': round(s_clip, 3),
        'colour': round(s_colour, 3), 'ar': round(ar, 2), 'px': '%dx%d' % (W0, H0),
    }


FOLDERS = [
    ('C:\\Users\\andre\\Downloads\\Lowell Massachusetts', 'Lowell MA'),
    ('C:\\Users\\andre\\Downloads\\Peachtree', 'Peachtree'),
    ('C:\\Users\\andre\\Downloads\\65 GENERAL WARRAN MALVERN PA PICS', 'Malvern PA'),
    ('C:\\Users\\andre\\Downloads\\clearfork', 'Clearfork TX'),
    ('C:\\Users\\andre\\Downloads\\2200 Pennsylvania photos (1)', '2200 Penn DC'),
    ('C:\\Users\\andre\\Downloads\\Slidell', 'Slidell LA'),
    ('C:\\Users\\andre\\Documents\\JatJ\\Bellevue', 'Bellevue WA'),
    ('C:\\Users\\andre\\Documents\\JatJ\\Berkeley', 'Berkeley CA'),
    ('C:\\Users\\andre\\Documents\\JatJ\\Miami\\photos_upright', 'Miami FL'),
]

if __name__ == '__main__':
    results = []
    for folder, label in FOLDERS:
        if not os.path.isdir(folder):
            print('skip (missing):', label); continue
        files = [f for f in glob.glob(os.path.join(folder, '**', '*'), recursive=True)
                 if f.lower().endswith(EXT)]
        done = 0
        for f in files:
            r = score_image(f)
            if r:
                r['project'] = label
                results.append(r); done += 1
        print('%-14s %4d scored' % (label, done))
        sys.stdout.flush()

    results.sort(key=lambda r: -r['score'])
    json.dump(results, open('scores.json', 'w'))
    print('\nTOTAL %d images scored' % len(results))
    print('\ntop 15:')
    for r in results[:15]:
        print('  %.3f  %-12s sp=%.2f sh=%.2f  %s' % (r['score'], r['project'], r['spread'], r['sharp'], os.path.basename(r['path'])[:34]))
