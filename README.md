# RankRight Media: website

A fast, secure, static rebuild of rankrightmedia.uk. It uses plain HTML, CSS and a little vanilla JS, with no WordPress, plugins, database or third-party requests.

- **`public/`**: the finished website. Upload the contents of this folder to your web root.
- **`content.py`**: every word, price, testimonial and business fact. Edit this file.
- **`build.py`**: generates `public/` (layout, SEO meta, JSON-LD schema, sitemap, robots.txt, llms.txt, security headers) and checks it.
- **`src/assets/`**: CSS, JS, fonts and images. **`src/root/`**: favicon and the `contact.php` form handler.
- **`AUDIT.md`**: audit of the old site, keyword map, what's still needed, and the launch checklist.

## Edit and rebuild

```bash
python3 build.py --check
```

This needs Python 3.8+ and nothing else. `--check` fails the build on broken internal links, missing anchors, duplicate IDs, more than one H1, images without alt text, and inline styles (which the Content-Security-Policy would block).

Preview locally:

```bash
cd public && python3 -m http.server 8000
```

## Deploy (Hostinger or any Apache/LiteSpeed host)

1. Back up the current WordPress site.
2. Upload the **contents** of `public/` to `public_html/` (including `.htaccess`).
3. Set `MAIL_TO` / `MAIL_FROM` in `contact.php` and send a test enquiry.
4. Submit `https://rankrightmedia.uk/sitemap.xml` in Google Search Console and Bing Webmaster Tools.

On Cloudflare Pages or Netlify, deploy `public/`. The `_headers` file there applies the same security headers. The PHP form handler needs PHP, so on those hosts point the form at a form service instead.

## What's built in

- **SEO:** unique titles and descriptions, canonical, hreflang en-GB, Open Graph and Twitter cards, breadcrumbs, XML sitemap, clean heading hierarchy, internal linking between related services.
- **Schema:** Organization + ProfessionalService, WebSite, WebPage/AboutPage/ContactPage, BreadcrumbList, Service with OfferCatalog (every package and price), AggregateOffer, FAQPage, ItemList. There's deliberately no self-serving Review markup: Google ignores it, and it carries legal risk under the UK DMCC Act.
- **AI visibility:** answer-first definitions, question-led H2s, FAQs, "Key facts" blocks and HTML pricing tables on every service page, plus `/llms.txt` and a robots.txt that explicitly welcomes GPTBot, ClaudeBot, PerplexityBot, Google-Extended and others.
- **Performance:** self-hosted variable fonts, WebP images with fixed dimensions (no layout shift), lazy loading, about 4 KB of JS, cache-busted assets with 1-year caching.
- **Security:** strict CSP (no inline scripts or styles), HSTS, X-Frame-Options DENY, nosniff, Referrer-Policy, Permissions-Policy; a form handler with honeypot, time-trap, same-origin check, rate limit and header-injection protection.
- **Accessibility:** skip link, keyboard-operable menu (Esc closes), visible focus, `prefers-reduced-motion` support, WCAG AA contrast on buttons.
