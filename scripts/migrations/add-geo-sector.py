"""One-off (Nov 2026): add lat/lng, state and sector tags to locations.json for the Projects map + filters."""
import json, pathlib
p = pathlib.Path(__file__).resolve().parents[2] / "src/data/locations.json"
d = json.loads(p.read_text(encoding="utf-8"))
G = {  # slug: (lat, lng, state, sectors)
 "apollo-drive-chelmsford": (42.60,-71.37,"MA",["healthcare","office"]),
 "pavilions-lane-sacramento": (38.58,-121.43,"CA",["retail"]),
 "galleria-roseville": (38.77,-121.27,"CA",["retail"]),
 "corte-madera": (37.93,-122.51,"CA",["retail"]),
 "town-and-country-houston": (29.78,-95.56,"TX",["shell","retail"]),
 "pennsylvania-avenue-washington-dc": (38.90,-77.05,"DC",["office"]),
 "henderson-avenue-dallas": (32.81,-96.79,"TX",["retail"]),
 "clearfork-fort-worth": (32.70,-97.40,"TX",["retail"]),
 "santan-village-gilbert": (33.30,-111.74,"AZ",["retail"]),
 "scottsdale-fashion-square": (33.50,-111.93,"AZ",["retail"]),
 "kierland-commons-scottsdale": (33.62,-111.93,"AZ",["retail"]),
 "grand-central-terminal-new-york": (40.753,-73.977,"NY",["landmark","retail"]),
 "queen-anne-seattle": (47.64,-122.36,"WA",["retail"]),
 "bellevue-square": (47.62,-122.20,"WA",["retail"]),
 "brea-mall": (33.92,-117.89,"CA",["retail"]),
 "mission-viejo": (33.56,-117.67,"CA",["retail"]),
 "j-street-sacramento": (38.58,-121.49,"CA",["shell","retail"]),
 "the-gardens-mall-palm-beach": (26.85,-80.08,"FL",["retail"]),
 "old-orchard-skokie": (42.06,-87.75,"IL",["retail"]),
 "spectrum-center-irvine": (33.65,-117.74,"CA",["retail"]),
 "berkeley-way": (37.87,-122.27,"CA",["office","retail"]),
 "lincoln-road-miami-beach": (25.79,-80.14,"FL",["retail","landmark"]),
 "culebra-road-san-antonio": (29.47,-98.62,"TX",["shell","retail"]),
 "inwood-village-dallas": (32.84,-96.82,"TX",["retail"]),
 "mckinney-avenue-dallas": (32.80,-96.80,"TX",["shell","retail"]),
 "fifth-avenue-new-york": (40.76,-73.977,"NY",["shell","landmark","retail"]),
 "westfield-topanga-canoga-park": (34.19,-118.60,"CA",["retail"]),
 "grand-avenue-san-marcos": (33.14,-117.17,"CA",["retail"]),
 "new-york-avenue-washington-dc": (38.90,-77.03,"DC",["office"]),
 "los-gatos-village-square": (37.24,-121.96,"CA",["shell","retail"]),
 "jericho-turnpike-commack": (40.84,-73.29,"NY",["retail"]),
 "west-diversey-parkway-chicago": (41.93,-87.64,"IL",["shell","retail"]),
 "manhattan-avenue-greenpoint-brooklyn": (40.73,-73.95,"NY",["shell","retail"]),
 "broadway-upper-west-side-new-york": (40.80,-73.97,"NY",["retail"]),
 "cactus-road-phoenix": (33.60,-111.98,"AZ",["shell","retail"]),
 "la-centerra-katy": (29.78,-95.82,"TX",["retail"]),
 "route-59-naperville": (41.75,-88.20,"IL",["office"]),
 "peachtree-road-atlanta": (33.85,-84.36,"GA",["office","healthcare"]),
 "industrial-avenue-lowell": (42.62,-71.32,"MA",["healthcare","office"]),
 "gateway-oaks-drive-sacramento": (38.60,-121.52,"CA",["healthcare","office"]),
 "ohio-street-commons-joliet": (41.53,-88.08,"IL",["healthcare","shell"]),
 "thousand-oaks-boulevard-thousand-oaks": (34.18,-118.88,"CA",["healthcare","office"]),
 "madera-road-simi-valley": (34.28,-118.75,"CA",["healthcare","office"]),
 "matley-lane-reno": (39.52,-119.79,"NV",["office"]),
 "south-willow-avenue-cookeville": (36.14,-85.50,"TN",["healthcare"]),
 "maryland-avenue-hagerstown": (39.64,-77.72,"MD",["office"]),
 "northeastern-boulevard-salem": (42.77,-71.22,"NH",["healthcare","office"]),
 "broadway-lincoln-square-new-york": (40.77,-73.98,"NY",["shell","retail"]),
 "crossroads-park-drive-houston": (29.83,-95.62,"TX",["healthcare"]),
}
for x in d:
    if x["slug"] in G:
        lat,lng,st,sec = G[x["slug"]]
        x.update(lat=lat, lng=lng, state=st, sectors=sec)
missing=[x["slug"] for x in d if "lat" not in x]
print("missing", missing)
p.write_text(json.dumps(d, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
