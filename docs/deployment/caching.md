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

## What still wants doing on the server

Inlining removes the *breakage*. It does not stop a browser serving stale HTML, so a
visitor can still see yesterday's copy. Add this to the site's nginx config in Forge
(Sites -> alturascope.com -> Edit Files -> Nginx Configuration), inside `server { }`:

```nginx
# HTML: always revalidate, so a deploy is picked up immediately.
location / {
    try_files $uri $uri/ $uri/index.html =404;
    add_header Cache-Control "no-cache";
}

# Build assets carry a content hash in the filename, so they can be cached hard.
location /_astro/ {
    add_header Cache-Control "public, max-age=31536000, immutable";
}

# Images, video and PDFs: a week, revalidated after that.
location ~* \.(jpg|jpeg|png|webp|svg|mp4|pdf)$ {
    add_header Cache-Control "public, max-age=604800";
}
```

`no-cache` does not mean "do not store" - it means "store, but revalidate before use".
The ETag is already being sent, so revalidation costs a 304 and no body.

## Checking it

```bash
curl -sI https://alturascope.com/uk/ | grep -i cache-control      # expect: no-cache
curl -sI https://alturascope.com/_astro/<file>.js | grep -i cache-control  # expect: immutable
```
