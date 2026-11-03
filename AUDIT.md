# RankRight Media: Site Audit, Rebuild Notes & Launch Checklist

**Scope:** visual and content audit of rankrightmedia.uk (Home, SEO and Link Building pages, from full-page captures dated 4 Nov 2026) plus a backend check of the Hostinger account. The live site, `urbantier.uk/sitemap_index.xml` and the WP dashboard could not be reached from the build environment because its network policy blocks those hosts.

---

## 0. 🚨 Urgent, separate from the redesign: compromised site on your hosting account

`rankrightmedia.online` (same Hostinger user `u655401359` as seobooster.uk, shopvious.com, iamfamous.uk and buyfollowerssingapore.com) has been **hacked with UK casino spam**:

- `/uk/mobile-casinos/` holds 119+ injected pages ("non-GamStop casinos", "free spins no deposit"…)
- `post-sitemap.xml`, `sitemap23.xml` and `sitemap24.xml` are spam sitemaps; robots.txt points Google at them
- robots.txt **blocks Ahrefs, Semrush, Majestic and others** so the spam stays hidden from SEO tools
- Unexpected root files: `wp-slgnup.gz` (a look-alike of `wp-signup`), `ok.txt`, `.htaccess.bk`, and three different Google verification files

**Why it matters:** all five sites share one hosting user, so a backdoor on one can usually write to the others. Google can also tie the spam to your brand name.

**Do now:** take `rankrightmedia.online` offline (or wipe and reinstall it), rotate the hPanel, FTP, database and WP admin passwords for every site, remove any Search Console properties you don't recognise, scan the other four sites for unknown files and admin users, and request removal of the spam URLs in Search Console. Nothing was deleted or changed by me; every check was read-only.

---

## 1. Audit of the current WordPress site

### Trust and conversion (highest revenue impact)

| Issue | Where | Impact | Fix in rebuild |
|---|---|---|---|
| **Three contradictory stat sets**: 8K+/5K+/**0.7**/5+ (Home), 56K+/38K+/4.7/35+ (SEO), 7K+/5K+/**0.6**/4+ (LB) | Stat bands | Instantly reads as fake. "0.7 client rating" is a broken counter | One set in `content.py → STATS`, used everywhere. **You must confirm these are true** (see §3) |
| "Join 2,000+ businesses" vs "5K+ happy clients" vs "Join dozens of happy clients" | Home | Same credibility problem | Removed the conflicting claims |
| Client logo wall (CrowdZero, GoatStreetVibe, Global Sol, Drophaus…) | Home | These are stock template logos. Under the UK DMCC Act 2024, implying clients you don't have is a misleading commercial practice | Replaced with a "tools we use" strip. Add **real** client logos only, with permission |
| Prices in **€** on a UK brand whose case studies are in £ | Pricing tables | Currency friction costs conversions; buyers wonder whether you're really UK-based | Kept € (your prices); switch with one line, `SITE["currency_code"]` |
| Testimonials with no company, role or location | Everywhere | Low credibility | Labelled by service. Add company names and Google/Trustpilot links when you have them |
| "Experience the Magic" skill bars showing **3%, 3%, 0%, 0%** | Home | Looks broken | Replaced with service links |
| Hero mock-up shows "Engaging you with Creative Design / 3D NFT / 3D Animation" lorem text | SEO and LB heroes | Theme demo content left in | Replaced with a custom on-brand SEO dashboard graphic |
| Project budgets "£20,00" and "£25,00" | Featured projects | Typos on money figures | Shown as £20,000 / £25,000. **Confirm** |
| Four of six featured projects had no image | Featured projects | Empty black boxes | Branded artwork until you add real screenshots |
| "How it works" steps 2 and 3 are missing titles | Home | Broken section | Completed (Secure Checkout / Share Your Brief) |
| Gradient buttons with white text (≈2.5:1 contrast) | Site-wide | Fails WCAG AA and is harder to read | Dark text on gradient (≈9:1) |
| Typos: "Link Buliding", "Manegement", "Website Developer" | Footer and bars | Sloppy signal | Fixed |
| "Powered by WordPress", Copyright 2025 | Footer | Dated | Removed; year updates automatically |

### On-page SEO and AI visibility

- One H1 per page wasn't reliable on Elementor, and emoji in H2s (💰, 🚀, ⭐) add no value. Rebuilt with a clean H1→H2→H3 hierarchy.
- There were no answer-first definitions ("What is link building?"), no FAQs, no pricing tables in machine-readable form and no "key facts" blocks. Those are exactly what AI Overviews, ChatGPT and Perplexity quote. All of them are now added.
- Schema was generic at best. Every page now has a connected `@graph`: Organization + ProfessionalService, WebSite, WebPage/AboutPage/ContactPage, BreadcrumbList, Service with OfferCatalog (every package and price), AggregateOffer, FAQPage and ItemList.
- Thin service pages for Web Dev, Content, PPC and Social. Rebuilt as full pages targeting keywords from your Ahrefs exports (see §2).

### Technical, performance and security

- Elementor and WordPress weigh heavily (multi-MB pages, render-blocking CSS and JS). The new homepage's critical path is ~210 KB uncompressed, with self-hosted fonts, zero third-party requests and zero cookies.
- The new site is static HTML, so there's no database, no plugins, no wp-login and nothing to hack. A strict Content-Security-Policy, HSTS, X-Frame-Options, nosniff, Referrer-Policy and Permissions-Policy ship in `.htaccess` and `_headers`.
- There are no analytics or advertising cookies, so **no cookie banner is required** as things stand. If you add GA4, add consent mode and a banner.

---

## 2. Keyword targeting (from your Ahrefs GB exports)

| Page | Primary target (UK vol / KD) | Secondary |
|---|---|---|
| `/` | brand + "digital marketing agency UK" | SEO agency UK |
| `/search-engine-optimization/` | seo service (2,000 / KD7), seo service uk (700 / 45) | professional seo service (700 / 8), local seo service (900 / 2), seo audit service (1,300 / 5), technical seo service (800 / 3) |
| `/link-building-services/` | link building services | dofollow backlinks, guest post outreach |
| `/website-development/` | **website development services (2,000 / KD2)** | website design and development services (600 / 4), ecommerce website development services (500 / 7), wordpress website development services (400 / 0) |
| `/content-writing/` | **seo content writing service (450 / KD0)** | seo friendly content writing service (150) |
| `/ppc-pay-per-click/` | **ppc management service (600 / KD1)** | ppc service (500 / 9), ppc audit service (300 / 0), facebook ads management service (200 / 15) |
| `/social-media-marketing/` | social media marketing services | social media growth services (90), organic social media growth services (80) |

**Quick wins to build next as their own pages:** `seo audit service` (1,300 / KD5), `technical seo audit service` (900 / KD10), `local seo service` (900 / KD2) + `local seo service uk / london / manchester`, `website maintenance services` (1,100 / KD2) and `website maintenance services uk` (400 / KD7). All are low difficulty with commercial intent, and each one lifts the parent service page through internal links.

---

## 3. What I need from you before launch (everything is in `content.py`)

1. **Founders and team**: names, roles, photos, short bios and LinkedIn links from the WP About page → `TEAM`. The section and Person schema appear automatically.
2. **Packages for Web Dev, Content, PPC and Social** if the WP pages list prices. These pages currently use "request a quote".
3. **Email inbox** → `SITE["email"]`, plus `MAIL_TO` / `MAIL_FROM` in `src/root/contact.php`.
4. **Company number, address and founding year** → strong E-E-A-T and local signals (shown in the footer and schema).
5. **Social and review profiles** (Google Business Profile, LinkedIn, Facebook, Trustpilot) → `SITE["same_as"]`. This is the #1 signal AI engines use to confirm an entity.
6. **Confirm the stats** (8K+ projects, 5K+ clients, 4.7 rating, 5+ awards). Only publish numbers you can evidence; name the awards if you keep "5+ awards".
7. **Legal pages**: the Privacy, Refund and Terms pages are drafts and set to `noindex`. Paste in your reviewed WP text.
8. **Exact WP URL slugs** for every page and blog post, so the 301 map in `.htaccess` is complete. The Web Dev, Content, PPC and Social slugs are my best guesses.
9. **Blog posts**: export them from WP (Tools → Export) so no ranking content is lost. The Blog link is held back until posts are migrated.
10. **Payments**: the "Buy now" buttons pre-fill the enquiry form with the chosen package. If you want instant checkout, create Stripe Payment Links and I'll wire each button to its link.
11. Copy marked **NEW** on the four service pages without screenshots (Web Dev, Content, PPC, Social) describes how you work: human-written content, ad-account ownership, no bought followers. Check it matches reality.

## 4. Launch checklist

- [ ] Fill in §3, then run `python3 build.py --check` (fails on broken links, missing anchors, duplicate IDs, multiple H1s, images without alt text, or inline styles)
- [ ] Crawl the old site (Screaming Frog or the WP sitemap) → add every changed URL to the 301 block in `.htaccess`
- [ ] Back up WordPress, then upload `public/` to the web root (Hostinger: File Manager or Git deploy)
- [ ] Test the contact form end to end (check spam folder; MAIL_FROM must be a real mailbox on the domain)
- [ ] Search Console: submit `/sitemap.xml`, inspect the homepage and service pages, watch Coverage for 404s for 2–4 weeks
- [ ] Bing Webmaster Tools: import from GSC (Bing powers ChatGPT search results)
- [ ] Validate with Google's Rich Results Test and the Schema.org validator
