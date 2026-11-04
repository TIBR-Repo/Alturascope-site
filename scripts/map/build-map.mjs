// Builds the static US + Puerto Rico outline for the Projects map and projects every
// location's lat/lng to map x/y (written back into src/data/locations.json as mx/my).
// Run after adding locations:  cd scripts/map && npm i && node build-map.mjs
// Kept out of the site's own package.json so the 1 GB deploy box never installs it.
import fs from "node:fs";
import { feature, mesh } from "topojson-client";
import { geoAlbersUsa, geoMercator, geoPath } from "d3-geo";
import { presimplify, simplify } from "topojson-simplify";
import usRaw from "us-atlas/states-10m.json" with { type: "json" };
const us = simplify(presimplify(usRaw), 0.015);
import world from "world-atlas/countries-10m.json" with { type: "json" };

const W = 960, H = 600;
const root = new URL("../../", import.meta.url);
const states = feature(us, us.objects.states);
const lower = { type: "FeatureCollection", features: states.features.filter((f) => !["02", "15", "72"].includes(f.id)) };
const proj = geoAlbersUsa().fitExtent([[10, 10], [W - 10, H - 70]], lower);
const path = geoPath(proj).digits(1);
const statesPath = path(states);
const borders = path(mesh(us, us.objects.states, (a, b) => a !== b));

// Puerto Rico inset, bottom right.
const pr = feature(world, world.objects.countries).features.find((f) => f.properties.name === "Puerto Rico");
const prBox = [[W - 190, H - 70], [W - 40, H - 20]];
const prProj = geoMercator().fitExtent(prBox, pr);
const prPath = geoPath(prProj).digits(1)(pr);

const locFile = new URL("src/data/locations.json", root);
const locs = JSON.parse(fs.readFileSync(locFile, "utf8"));
let miss = 0;
for (const l of locs) {
  if (l.lat == null) continue;
  let p = l.state === "PR" ? prProj([l.lng, l.lat]) : proj([l.lng, l.lat]);
  if (!p) { miss++; console.warn("unprojectable", l.slug); continue; }
  l.mx = Math.round(p[0] * 10) / 10; l.my = Math.round(p[1] * 10) / 10;
}
fs.writeFileSync(locFile, JSON.stringify(locs, null, 1) + "\n");
fs.writeFileSync(new URL("src/data/us-map.json", root), JSON.stringify({ width: W, height: H, states: statesPath, borders, pr: prPath, prLabel: [W - 115, H - 8] }));
console.log("ok", locs.length, "locations,", miss, "unprojected");
