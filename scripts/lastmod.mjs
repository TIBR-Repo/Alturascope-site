// Writes src/data/lastmod.json: URL path -> date the page's source last changed.
//
// The sitemap used to stamp every URL with the build time, so every deploy told
// Google that all pages had changed. Google learns to ignore a lastmod that is
// always "now". This gives it real dates instead.
//
// Needs full git history. The Forge deploy is a shallow clone, so there it does
// nothing and the committed lastmod.json is used as-is - run `npm run lastmod`
// locally before committing content changes.
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const sh = (c) => execSync(c, { encoding: 'utf8' });
if (sh('git rev-parse --is-shallow-repository').trim() === 'true') {
  console.log('lastmod: shallow clone, keeping committed src/data/lastmod.json');
  process.exit(0);
}

// One pass over history: first time we see a file is its latest change.
const latest = {};
let date = null;
for (const line of sh('git log --format=@%cs --name-only -- src/pages src/data').split('\n')) {
  if (line.startsWith('@')) date = line.slice(1);
  else if (line && !(line in latest)) latest[line] = date;
}
// Uncommitted edits count as today.
const today = new Date().toISOString().slice(0, 10);
for (const line of sh('git status --porcelain -- src/pages src/data').split('\n')) {
  const f = line.slice(3).trim();
  if (f) latest[f] = today;
}

const out = {};
for (const [file, d] of Object.entries(latest)) {
  const m = file.match(/^src\/pages\/(.+)\.astro$/);
  if (!m || m[1].includes('[')) continue;
  const path = '/' + m[1].replace(/(^|\/)index$/, '').replace(/\/?$/, '/');
  out[path === '//' ? '/' : path] = d;
}

// Location stories come from one template plus one data file; date each story
// by whichever of the two changed last.
const storyDate = [latest['src/pages/work/locations/[slug].astro'], latest['src/data/location-stories.json']]
  .filter(Boolean).sort().pop();
const stories = JSON.parse(readFileSync('src/data/location-stories.json', 'utf8'));
for (const s of Array.isArray(stories) ? stories : Object.values(stories)) {
  if (s.slug) out[`/work/locations/${s.slug}/`] = storyDate;
}

writeFileSync('src/data/lastmod.json', JSON.stringify(out, null, 1) + '\n');
console.log(`lastmod: ${Object.keys(out).length} paths`);
