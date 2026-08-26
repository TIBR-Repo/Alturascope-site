# Search Console automation

`gsc.py` talks to Search Console with no browser, no OAuth consent screen and
no token that expires. It authenticates as a **service account** that you add
as a user on the property — the same way you'd add a colleague's email.

Setup is one-time and takes about eight minutes. After that everything below
runs headlessly, forever, including from a scheduled job.

---

## Status: live since 26 August 2026

Set up and working. Property is a **Domain property** (`sc-domain:alturascope.com`),
which covers http/https and every subdomain. The service account
`gsc-reader@claude-gsc-alturascope.iam.gserviceaccount.com` holds `siteFullUser`,
which is enough for everything here including sitemap submission.

The setup below is kept for reference, or for standing it up again elsewhere.

---

## One-time setup

### 1. Create the service account (Google Cloud, ~5 min)

1. Go to **console.cloud.google.com** and sign in with the Google account that
   **owns the alturascope.com Search Console property**.
2. Create a project (top-left picker → *New Project*). Call it `alturascope-seo`.
   If you already have a project, reuse it.
3. **APIs & Services → Library** → search **"Google Search Console API"** →
   **Enable**.
4. **APIs & Services → Credentials → Create Credentials → Service account**.
   - Name: `gsc-reader`
   - Skip the optional role and access steps — the permission that matters is
     granted in Search Console, not here. Click **Done**.
5. Click the new service account → **Keys** tab → **Add key → Create new key →
   JSON**. A file downloads.
6. Move that file to:

   ```
   C:\Users\andre\.credentials\gsc-service-account.json
   ```

   It is a secret. It must not go anywhere near the site repo.

### 2. Grant it access to the property (Search Console, ~1 min)

1. Open the JSON file and copy the `client_email` value. It looks like
   `gsc-reader@alturascope-seo.iam.gserviceaccount.com`.
2. In **Search Console** → select the alturascope.com property →
   **Settings → Users and permissions → Add user**.
3. Paste that email. Set permission to **Full**.

   *Full* is required — sitemap submission needs it. *Restricted* is enough for
   reading performance data only, if you'd rather start there.

### 3. Check it worked

```bash
python scripts/gsc/gsc.py status
```

You should see the property listed with a `*` beside it, plus the sitemaps
Google currently has on file.

---

## What you can then run

```bash
# submit the sitemap (replaces the 5 clicks)
python scripts/gsc/gsc.py submit-sitemap

# has Google actually indexed the pages the overhaul created?
python scripts/gsc/gsc.py index-status

# performance overview
python scripts/gsc/gsc.py report --days 28

# how estimating terms are doing, which is the whole point of the August work
python scripts/gsc/gsc.py queries
python scripts/gsc/gsc.py queries --contains nrm2

# before/after around the deploy — the number that says whether it worked
python scripts/gsc/gsc.py compare --pivot 2026-08-26
```

`compare` needs at least a few days of data after the pivot date, and Search
Console runs about three days behind, so it's worth running from roughly
**2 September 2026** onward. It compares an equal-length window either side, so
it stays fair as the window grows.

---

## What is *not* automatable, and why

**Request Indexing cannot be scripted.** Google's Indexing API is officially
sanctioned only for `JobPosting` and `BroadcastEvent` structured data. There is
no supported endpoint for asking Google to crawl an ordinary page, so that
button genuinely only exists in the UI.

Two things reduce how much that matters:

- The **sitemap now carries `lastmod`** (added August 2026 — its absence was why
  the estimating launch was slow to surface). A resubmitted sitemap with fresh
  `lastmod` values is the supported way to signal change, and `submit-sitemap`
  does it.
- `index-status` uses the **URL Inspection API**, which is read-only but tells
  you what you actually wanted to know: whether a page is indexed, what
  coverage state it's in, and when it was last crawled. So you can see whether
  asking would even have helped.

If you want Request Indexing driven anyway, it has to be Playwright against a
logged-in session. That's possible but it's the fragile part of the stack —
Google changes the UI, and a browser session has to be refreshed periodically.
Worth doing only if the sitemap route proves too slow in practice.

---

## Scheduled reporting (live since 26 August 2026)

Two **Windows scheduled tasks** — real ones, not a Claude session cron, so they
survive reboots and run whether or not anything else is open:

| Task | When | What |
| --- | --- | --- |
| `Alturascope SEO - daily index check` | daily 08:12 | `report.py --quick` — index status only, ~40s |
| `Alturascope SEO - weekly report` | Mondays 08:23 | `report.py` — performance, themes, before/after, ~2min |

Reports land in **`Documents\Alturascope-SEO\`**: a dated `report-YYYY-MM-DD.md`
plus `latest.md`, which is always the most recent. `state.json` holds the previous
run so each report can say what *moved* rather than just restating totals — it
calls out any page that became indexed since last time. `run.log` captures stdout
and stderr, because a scheduled task otherwise swallows both and a failure is
invisible.

Re-register or change the times with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\gsc\install-schedule.ps1
```

Run one immediately:

```powershell
Start-ScheduledTask -TaskName "Alturascope SEO - weekly report"
```

Remove them:

```powershell
Get-ScheduledTask -TaskName "Alturascope SEO*" | Unregister-ScheduledTask -Confirm:$false
```
