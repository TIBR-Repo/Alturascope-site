# Caching headers (needs Forge)

## The bug this documents

On 2026-08-25 pages across the site rendered completely unstyled: Times New Roman,
blue underlined links, no layout. It looked like a UK-side fault but could hit any page.

Cause, in order:

1. The server sends **no `Cache-Control` header at all** - not on HTML, not on assets.
2. With no directive, browsers apply *heuristic* caching, roughly 10% of the age of the
   document. The previous build had been live for days, so returning visitors were being
   served HTML cached from well before the deploy.
3. Astro emits the Tailwind bundle with a content hash in its filename. New pages added
   new utilities, the bundle changed, the hash changed, and the previous filename stopped
   existing on the server.
4. Stale HTML therefore requested a stylesheet that had been deleted -> 404 -> unstyled page.

A hard refresh fixed it, which is why it appeared to affect only some pages.

## What was done in the repo

`astro.config.mjs` sets `build.inlineStylesheets: 'always'`. There is now no stylesheet
request to fail: every page carries its own CSS. Cached HTML paints correctly using the
styles it was built with. Page weight goes from roughly 29 KB to 82 KB raw, but about
**13.8 KB gzipped**, and it removes a render-blocking round trip.

The only remaining external stylesheet is Google Fonts, which is unaffected by deploys.

## Server side - DONE 2026-08-25

Applied to the live server. Two files, both owned by `forge` (no root needed):

| File | Included at | Purpose |
| --- | --- | --- |
| `/etc/nginx/forge-conf/2978903/before/cache-control-map.conf` | http context, above the server blocks | a `map $uri` choosing the policy |
| `/etc/nginx/forge-conf/2978903/server/cache-control.conf` | inside the HTTPS `server` block | one `add_header Cache-Control $alturascope_cache_control always;` |

Policy, keyed on the URL rather than content type, because pages use
`trailingSlash: 'always'` and so have **no file extension**:

| URL | Cache-Control |
| --- | --- |
| anything without a known extension (every page) | `no-cache` |
| `/_astro/*` (content-hashed build assets) | `public, max-age=31536000, immutable` |
| images, video, PDF | `public, max-age=604800` |
| fonts | `public, max-age=31536000, immutable` |
| `.html`, `.xml`, `.txt`, `.json` (robots, sitemap) | `no-cache` |

`no-cache` does not mean "do not store" - it means "store, but revalidate before
use". The ETag is already sent, so revalidation costs a 304 and no body.

### Two things worth knowing before editing this again

**Where to put custom nginx.** This build of Forge has no per-site nginx editor
in the UI. The site config is just `include forge-conf/2978903/site.conf;`, and
that file carries includes for `before/*` (http context) and `server/*` (inside
the server block). Those directories are owned by `forge`, are writable without
sudo, and survive Forge regenerating `site.conf`. The site's **Commands** runner
is enough to write them - it runs as `forge` from the site root.

**`add_header` inheritance.** nginx only inherits `add_header` from an outer
level if the inner level declares *none of its own*. The security headers
(`X-Frame-Options`, `X-XSS-Protection`, `X-Content-Type-Options`) are declared at
server level, and `server/cache-control.conf` is included at that same level, so
they coexist. Had the `add_header` gone inside a `location` block instead, that
location would silently have lost all three. Verified after applying: all three
still present.

**Reloading.** `forge` has NOPASSWD sudo for `nginx -s reload`, `systemctl
reload|restart nginx` and `service nginx *` - nothing else. A reload with a
broken config is refused and the old config keeps serving, so reloading is safe;
a `restart` with a broken config is not.

### Verified live

```
/uk/                          Cache-Control: no-cache
/Images/aph-image.jpg         Cache-Control: public, max-age=604800
/video/...mp4                 Cache-Control: public, max-age=604800
/downloads/...pdf             Cache-Control: public, max-age=604800
/robots.txt, /sitemap-0.xml   Cache-Control: no-cache
X-Frame-Options / X-XSS-Protection / X-Content-Type-Options   all still present
http->https 301, www->apex 301, 404 page 404, all pages 200
```

### Re-checking it

```bash
curl -sI https://alturascope.com/uk/ | grep -i cache-control                  # no-cache
curl -sI https://alturascope.com/Images/aph-image.jpg | grep -i cache-control # max-age=604800
```

### Rolling it back

```bash
rm /etc/nginx/forge-conf/2978903/before/cache-control-map.conf    /etc/nginx/forge-conf/2978903/server/cache-control.conf
sudo -n /usr/sbin/nginx -s reload
```

Remove **both** files together - the `add_header` references a variable the map
defines, so deleting only the map leaves nginx unable to load.
