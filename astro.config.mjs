// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

const BUILD_DATE = new Date().toISOString();

export default defineConfig({
  site: 'https://alturascope.com',
  trailingSlash: 'always',
  // /uk/heritage-building-documentation/ duplicated /uk/heritage-building-survey/
  // and had no inbound links at all - two UK pages competing for the same query.
  // Astro emits a meta-refresh page with a canonical for static builds; the
  // nginx config also carries a real 301 (see docs/deployment/redirects.md).
  redirects: {
    // Pruned Aug 2026: 28 service pages spanning superyachts, private aircraft,
    // solar farms and art collections diluted what the site is about and
    // competed with the sectors we actually sell. Folded into the page that
    // already exists for exactly this work.
    '/services/superyacht-documentation/': '/services/specialist-projects/',
    '/services/private-aircraft-documentation/': '/services/specialist-projects/',
    '/services/private-collection-documentation/': '/services/specialist-projects/',
    '/services/private-estate-documentation/': '/services/specialist-projects/',
    '/services/film-tv-location-documentation/': '/services/specialist-projects/',
    '/services/solar-farm-documentation/': '/services/specialist-projects/',
    '/services/aviation-facility-survey/': '/services/specialist-projects/',
    '/services/resort-hotel-capex-survey/': '/services/specialist-projects/',
    // The sector is dropped, but the data centre *article* stays - it is the
    // single highest-impression page on the site (233 impressions, position 20.9).
    '/services/data-centre-documentation/': '/services/industrial-facility-documentation/',
    '/uk/heritage-building-documentation/': '/uk/heritage-building-survey/',
  },
  build: {
    // Inline the stylesheet into every page instead of linking a content-hashed
    // file. A deploy changes that hash, so any browser holding cached HTML from
    // before the deploy requests a stylesheet that no longer exists and renders
    // the page completely unstyled. Inlining removes the request, and therefore
    // the failure: stale HTML still paints correctly using its own styles.
    inlineStylesheets: 'always',
  },
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => !page.includes('/thank-you/'),
      // Give crawlers a change signal. Without lastmod, a recrawl of an updated
      // page can lag by weeks - which is why new services were slow to surface.
      serialize(item) {
        const url = item.url;
        item.lastmod = BUILD_DATE;
        if (url === 'https://alturascope.com/') {
          item.changefreq = 'weekly';
          item.priority = 1.0;
        } else if (/\/(estimating|services|work|uk)\/?$/.test(url)) {
          item.changefreq = 'weekly';
          item.priority = 0.9;
        } else if (url.includes('/estimating/') || url.includes('/work/')) {
          item.changefreq = 'monthly';
          item.priority = 0.8;
        } else if (url.includes('/insights/')) {
          item.changefreq = 'monthly';
          item.priority = 0.6;
        } else {
          item.changefreq = 'monthly';
          item.priority = 0.7;
        }
        return item;
      },
    }),
  ],
});
