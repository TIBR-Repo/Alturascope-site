# Redirects

## Why there are two mechanisms

Astro's `redirects` config (in `astro.config.mjs`) is the in-repo source of
truth. For a static build it emits an HTML stub carrying a `meta refresh`, a
`noindex` and a canonical pointing at the destination. That works, survives
every deploy, and needs nobody to touch the server — but it is a client-side
redirect, and Google treats it as weaker than a real 301.

So each entry should also exist as an nginx `return 301`. The nginx rule is the
one that passes link equity properly; the Astro stub is the safety net if the
server config is ever reset by Forge.

## Current redirects

| From | To | Reason |
|---|---|---|
| `/uk/heritage-building-documentation/` | `/uk/heritage-building-survey/` | Duplicate page with zero inbound links, competing with the survey page for the same query. Consolidated 2026-08-26. |

## Adding the nginx rule

SSH as `forge@206.189.228.174`. The site config is
`/etc/nginx/forge-conf/2978903/site.conf`, and `forge` can edit it directly and
has NOPASSWD sudo for `service nginx configtest` and `nginx -s reload` only.

Prefer a separate include so a Forge UI edit to `site.conf` cannot silently
drop it — the same pattern the Cache-Control headers use (see `caching.md`):

```nginx
# /etc/nginx/forge-conf/2978903/server/redirects.conf
location = /uk/heritage-building-documentation/ {
    return 301 https://alturascope.com/uk/heritage-building-survey/;
}
```

Then:

```bash
sudo service nginx configtest && sudo nginx -s reload
```

Verify from a machine that has never visited the URL:

```bash
curl -sI https://alturascope.com/uk/heritage-building-documentation/ | head -3
# expect: HTTP/2 301 and the Location header
```

## Note on `public/_redirects`

`public/_redirects` is Netlify format and does nothing on nginx. It is still in
the tree; do not add rules there expecting them to work.
