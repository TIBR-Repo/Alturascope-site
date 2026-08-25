# Photo tools

Written 2026-08-25 while selecting imagery for the site. All three read local files only
and refuse any path containing `\Dropbox\` — the Dropbox copies are online-only
placeholders, and reading them makes Dropbox download them (~1.5 GB the first time).

## score_photos.py
Ranks a survey archive for website suitability: sharpness, how far detail is spread across
the frame, tonal range, colour, orientation. Writes `scores.json`.

Scored 2,425 photos in ~100 seconds and cut them to ~70 worth reviewing by eye. It ranks
*technical* quality — a sharp nameplate scores as highly as a finished interior — so treat
it as a pre-filter, never a judge.

## find_plates.py
Finds equipment rating plates and panel schedules: fine text detail that collapses when the
image is downsampled, concentrated centrally. Writes `plates.json`.

Its false-positive mode is textured walls. **The trick that worked:** take one confirmed hit
and pull the frames either side of it — surveyors photograph plates in bursts, so a single
hit surfaces the whole equipment sequence.

## make_takeoff.py
Renders a take-off overlay (area polygons, linear runs, count markers, legend, title block)
onto a drawing photograph. Superseded for marketing use by Selwyn's real Vyntworks pack,
but kept — it is the only way to produce one of these without the platform.

## Requirements
`pillow`, `numpy`. Both already installed. PDF work uses `pymupdf` (poppler is not
available on this machine, so the Read tool cannot open PDFs directly).
