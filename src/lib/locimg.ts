// Cover image URL for a location card, with a short content hash as ?v=.
// The server tells browsers to cache images for 7 days, so without this a
// replaced cover (same file name) keeps showing the old picture to returning
// visitors. Computed at build time from the file in public/.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const cache = new Map<string, string>();
export function locImg(slug: string): string {
  if (!cache.has(slug)) {
    let v = "";
    try {
      const buf = readFileSync(join(process.cwd(), "public", "Images", "locations", `${slug}.webp`));
      v = "?v=" + createHash("md5").update(buf).digest("hex").slice(0, 8);
    } catch {}
    cache.set(slug, `/Images/locations/${slug}.webp${v}`);
  }
  return cache.get(slug)!;
}
