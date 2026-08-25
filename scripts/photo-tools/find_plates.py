# -*- coding: utf-8 -*-
"""Find equipment nameplate / rating-plate photographs in a survey archive.

Signature: a lot of fine-scale detail (small text) that collapses when the image is
heavily downsampled, concentrated in the middle of the frame, and sharp.
"""
import os, sys, glob, json
import numpy as np
from PIL import Image, ImageOps

EXT = ('.jpg', '.jpeg', '.png')
DROPBOX = os.sep + 'Dropbox' + os.sep


def lap_var(g):
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    h, w = g.shape
    out = np.zeros((h - 2, w - 2), dtype=np.float32)
    for dy in range(3):
        for dx in range(3):
            if k[dy, dx]:
                out += k[dy, dx] * g[dy:h - 2 + dy, dx:w - 2 + dx]
    return float(out.var())


def plate_score(path):
    assert DROPBOX not in path, path
    try:
        im = Image.open(path)
        im.draft('RGB', (1400, 1400))
        im = ImageOps.exif_transpose(im).convert('RGB')
    except Exception:
        return None

    big = im.copy(); big.thumbnail((700, 700))
    small = im.copy(); small.thumbnail((170, 170))
    gb = np.asarray(big, dtype=np.float32).mean(axis=2) / 255.0
    gs = np.asarray(small, dtype=np.float32).mean(axis=2) / 255.0
    if gb.shape[0] < 60 or gs.shape[0] < 30:
        return None

    fine = lap_var(gb)
    coarse = lap_var(gs)
    # text-like: fine detail that disappears on heavy downsample
    ratio = fine / (coarse + 1e-6)

    # detail concentrated centrally (a plate fills the middle of the frame)
    H, W = gb.shape
    gy, gx = np.gradient(gb)
    e = np.hypot(gx, gy)
    cen = e[H // 4:3 * H // 4, W // 4:3 * W // 4].mean()
    out = (e.sum() - e[H // 4:3 * H // 4, W // 4:3 * W // 4].sum()) / max(e.size - (H // 2) * (W // 2), 1)
    centrality = cen / (out + 1e-6)

    a = np.asarray(big, dtype=np.float32) / 255.0
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0).mean())

    score = (min(ratio / 3.5, 1.0) * 0.50
             + min(fine / 0.010, 1.0) * 0.30
             + min(centrality / 1.6, 1.0) * 0.20)
    # plates are metal/paper: heavily saturated frames are usually something else
    if sat > 0.42:
        score *= 0.75
    return {'path': path, 'plate': round(float(score), 4), 'ratio': round(float(ratio), 2),
            'fine': round(float(fine), 5), 'centrality': round(float(centrality), 2),
            'sat': round(float(sat), 3)}


FOLDERS = [
    (r'C:\Users\andre\Downloads\Lowell Massachusetts', 'Lowell MA'),
    (r'C:\Users\andre\Downloads\Peachtree', 'Peachtree'),
    (r'C:\Users\andre\Downloads\65 GENERAL WARRAN MALVERN PA PICS', 'Malvern PA'),
    (r'C:\Users\andre\Downloads\clearfork', 'Clearfork TX'),
    (r'C:\Users\andre\Downloads\2200 Pennsylvania photos (1)', '2200 Penn DC'),
    (r'C:\Users\andre\Documents\JatJ\Bellevue', 'Bellevue WA'),
    (r'C:\Users\andre\Documents\JatJ\Berkeley', 'Berkeley CA'),
    (r'C:\Users\andre\Documents\JatJ\Miami\photos_upright', 'Miami FL'),
]

if __name__ == '__main__':
    res = []
    for folder, label in FOLDERS:
        if not os.path.isdir(folder):
            print('skip', label); continue
        files = [f for f in glob.glob(os.path.join(folder, '**', '*'), recursive=True)
                 if f.lower().endswith(EXT)]
        n = 0
        for f in files:
            r = plate_score(f)
            if r:
                r['project'] = label
                res.append(r); n += 1
        print('%-14s %4d' % (label, n)); sys.stdout.flush()
    res.sort(key=lambda r: -r['plate'])
    json.dump(res, open('plates.json', 'w'))
    print('\nscored %d; top 12:' % len(res))
    for r in res[:12]:
        print('  %.3f ratio=%5.1f  %-12s %s' % (r['plate'], r['ratio'], r['project'], os.path.basename(r['path'])[:32]))
