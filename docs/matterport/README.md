# Matterport covers — how the gallery gets its images

`models.json` holds every Alturascope Matterport scan: model id, project name, place.
As of 2026-08-25 there are 27.

## The key fact

Every Matterport model publishes its cover image at a public endpoint — no login, no API key:

```
https://my.matterport.com/api/v2/player/models/<MODEL_ID>/thumb/?width=1280
```

**Whatever view is set as the model's cover in Matterport is what this returns.** So the
website gallery never needs manual screenshots: set the opening view at source and the
image follows. Add `&cb=<timestamp>` to bypass caching after changing a cover.

Roughly 100–260 KB per image at 1280×720.

## Finding new scans

Model ids are stored on each ScopeWalk project's designer page (`/designer/projects/<id>`)
as the 3D-tour link. Sweeping ids 225–290 while logged in as owner finds them all:

```js
const h = await (await fetch('/designer/projects/' + id, {credentials:'same-origin'})).text();
const mp = [...h.matchAll(/matterport\.com\/show\/\?m=([A-Za-z0-9]+)/g)].map(x => x[1]);
```

**Watch the regex.** An earlier version captured a leading `3D` and produced a dead id
(`3DFkjRxRERuMc` instead of `FkjRxRERuMc`), which made a live scan look broken for weeks.

Scans not linked on their ScopeWalk project won't be found this way — Urgent Vets
(`rzzz3PB93UU`) had to be supplied by hand. Adding the link to the project fixes that.

## Selection notes (2026-08-25)

- Balance matters: a gallery of exteriors reads as a property brochure. Aim for a real
  share of interiors — mid-strip-out and shell units say "we survey buildings" loudest.
- The **dollhouse / mesh view** (currently 250 Apollo Suite 150) is the most
  differentiating image available — it says *digital twin* in a way no photograph can.
- Check every cover for identifiable faces before it goes public.
- A scan's cover is one image but the model holds hundreds; interior stills can be pulled
  from inside a scan and used alongside a different cover.
