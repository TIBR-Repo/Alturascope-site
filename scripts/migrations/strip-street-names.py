"""One-off (Nov 2026, Andrew): project labels show town + state only, never a street.
Named centres, landmarks and neighbourhoods stay - they are public places, not addresses.
Slugs (URLs) are left alone so no page moves."""
import json, pathlib

KEEP_FIRST = {  # first label part is a named centre / landmark / neighbourhood
    "Galleria", "Town & Country", "Clearfork", "SanTan Village", "Scottsdale Fashion Square",
    "Kierland Commons", "Queen Anne", "Bellevue Square", "Brea Mall", "The Gardens Mall",
    "Old Orchard", "Spectrum Center", "Lincoln Road", "Inwood Village", "Fifth Avenue",
    "Westfield Topanga", "Los Gatos Village Square", "La Centerra", "Tacoma Mall",
    "Victoria Gardens", "Union Market", "The Gardens on El Paseo", "Broadway Plaza",
    "Village Walk", "Grand Central Terminal", "Mission Viejo", "Corte Madera",
}
NEIGHBOURHOOD = {  # "Broadway, Upper West Side, New York" -> "Upper West Side, New York"
    "Manhattan Avenue": True, "Broadway": True,
}

p = pathlib.Path(__file__).resolve().parents[2] / "src/data/locations.json"
locs = json.loads(p.read_text(encoding="utf-8"))
changed = 0
for l in locs:
    parts = [x.strip() for x in l["label"].split(",")]
    if len(parts) < 2 or parts[0] in KEEP_FIRST:
        continue
    if len(parts) == 2 and parts[1] in {"New York", "Arizona"}:
        continue  # e.g. "Fifth Avenue, New York" handled above; "Scottsdale Fashion Square, Arizona"
    first = parts[0]
    looks_street = any(w in first for w in (
        "Road", "Street", "Avenue", "Boulevard", "Drive", "Lane", "Parkway", "Turnpike", "Way",
        "Route", "Broadway", "Business Center", "Commons", "Basin", "114th", "Calle", "Plaza"))
    if looks_street and len(parts) >= 3:
        new = ", ".join(parts[1:])
        if new != l["label"]:
            l["label"] = new; changed += 1
p.write_text(json.dumps(locs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("relabelled", changed)
for l in locs:
    print(l["slug"], "|", l["label"])
