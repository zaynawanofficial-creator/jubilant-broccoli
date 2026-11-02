# ARCHITECTURE — SEO Booster

**Status:** Decided 2 Nov 2026 (Phase 01). **Route:** `wordpress`.

## 1. Environment audit (read-only, 2 Nov 2026)
| Item | Finding | Evidence |
|---|---|---|
| Host | Hostinger, hcdn edge + LiteSpeed cache | `platform: hostinger`, `server: hcdn`, `x-litespeed-cache` headers |
| PHP | 8.5.12 | `x-powered-by` header |
| WordPress | 7.1.4 | generator meta |
| WooCommerce | 11.2.1 | generator meta |
| Builder / theme | Elementor 4.3.5, WoodMart + `woodmart-child` | generator meta, asset paths |
| Other plugins seen | Contact Form 7, Safe SVG, Jetpack, LiteSpeed Cache, MCP Adapter, Elementor MCP Composer (`elementor-mcp-composer/v1.0.19`) | `/wp-json/` namespaces |
| AI/MCP access | `/wp-json/mcp/mcp-adapter-default-server` returns 401 without auth (reachable from this container) | curl |
| Content | 11 pages, all WoodMart demo imports or Woo system pages; **0 products, 0 posts, 0 product categories** | `wp/v2/pages`, `wc/store/v1/products` |
| Missing routes | `/services/`, `/packages/`, `/terms/`, `/privacy-policy/` → 404 | curl |
| Sitemap / robots | Both redirect (301), so a core or plugin sitemap exists; robots.txt has the standard Woo disallows | curl |

The site has not launched. Nothing there needs preserving apart from the theme, plugin stack and licences.

## 2. Options compared
| Criterion | A. Block theme + Woo | **B. WoodMart + Elementor + Woo (chosen)** | C. Custom full-stack |
|---|---|---|---|
| Already installed and licensed | No (would replace the theme) | **Yes** | No |
| Admin can edit pages visually | Site Editor | **Elementor (owner's existing tool) + WoodMart MCP** | Custom CMS needed |
| Cart, checkout, orders, coupons, tax | Woo native | **Woo native** | Must be built and secured |
| Runs on the current Hostinger plan | Yes | **Yes** | Needs a Node/VPS runtime |
| Performance ceiling | Best | Good with tuning (WoodMart asset toggles, LiteSpeed) | Best |
| Time to the first paid order | Medium | **Shortest** | Longest |
| Lock-in risk | Low | Medium (WoodMart/Elementor licences) | Low, but full maintenance burden |

**Decision:** B. The owner chose it, and it is the shortest path to a working paid-order flow on the hosting and licences already in place. Option A stays open as a later performance rebuild, because every piece of business logic lives in a theme-independent plugin.

## 3. System design
```
Visitor ─► Elementor page (service page / hub / home)
             └─ [sb_packages] shortcode/widget ─► reads WooCommerce products (+ sb meta)
                    └─ Add to cart ─► Woo Cart ─► Woo Checkout (Stripe / PayPal / BACS)
                                                     └─ Order (HPOS) + line-item sb meta
                                                          └─ status: awaiting-brief
Buyer ─► My Account › Orders › "Complete your brief" (seo-booster-core form)
                                                          └─ order meta + protected uploads
Admin ─► Woo Orders screen + SB metabox (brief, files, milestones) ─► custom statuses ─► emails
```

### Components
1. **WooCommerce (core):** products, cart, checkout, orders, coupons, tax, refunds and emails. No forks and no direct database writes.
2. **`seo-booster-core` plugin (this repo, `wp-content/plugins/seo-booster-core/`):** theme-independent. It provides:
   - the package meta schema, the `sb_package_group` taxonomy and the approval gate on publishing
   - the `[sb_packages]` shortcode and Elementor widget (group tabs, cards, and a comparison view that switches to an accordion on mobile)
   - quote-only packages, which link to the proposal form instead of the cart
   - the post-purchase brief (conditional fields per service type, secure uploads)
   - the custom service order statuses and emails, and the rule that service orders never auto-complete
   - the admin order metabox and the CSV catalog importer (WP-CLI command)
3. **WoodMart child theme:** design tokens, header and footer, and template overrides only where needed. No business logic.
4. **Elementor:** page layouts for home, hubs, service pages, about and contact. Global colours and fonts map to the design tokens.
5. **Payments:** WooCommerce Stripe Gateway, WooCommerce PayPal Payments and core BACS (used for Payoneer/bank transfer). Test mode until the owner approves going live. Keys are entered in wp-admin by the owner, never via chat or git.
6. **Forms:** Contact Form 7 (already installed) for contact and proposal requests, with a honeypot/Turnstile and a consent checkbox.
7. **SEO:** one SEO plugin, to be decided in Phase 06. Cart, checkout and account pages are noindexed, and the site is noindexed until launch.
8. **Cache:** LiteSpeed Cache, with cart, checkout and my-account excluded and Woo session cookies respected.

### Why the brief is collected after payment
Checkout stays short, which helps conversion. Long briefs and file uploads happen in an authenticated area tied to the order, which keeps PII and uploads under capability checks.

## 4. Access and deployment
- **Content and config:** the WoodMart MCP (`.mcp.json`, password read from `${WP_API_PASSWORD}`) or the WP/Woo REST API using an Application Password.
- **Plugin code:** built in this repo, zipped, and uploaded via wp-admin or Hostinger file deploy. Each deploy gets a git tag.
- **Backups:** a Hostinger backup or snapshot is taken before every phase that writes to the site, and recorded in PROGRESS.md.
- **Environment:** build directly on production while the site is pre-launch (owner decision). Search-engine visibility stays off until launch is approved.

## 5. Non-goals (for now)
- Subscriptions and retainers that need WooCommerce Subscriptions. These are sold as quote-only until that licence is approved.
- Multi-currency. Prices are in USD until the owner decides otherwise.
- A full client ticketing system. Phase 05 uses order notes plus the brief and delivery files.
