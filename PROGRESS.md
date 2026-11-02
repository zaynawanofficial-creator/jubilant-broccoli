# PROGRESS

## Phase 02 + 03 (repo side) · 2 Nov 2026 · 🟡 built, not yet installed on the site
**Owner input received:** Off-Page tier structure and price anchors, placeholder business details, permission for Claude to design the logo and favicon. All recorded in DECISIONS.md.

**Built**
- `SERVICE_CATALOG.csv` has a new `pricing_model` column.
  - Off-Page rows are rewritten: group A has 8 priced tiers (approved, READY) and group B has 8 Premium Links tiers (quote-only).
  - The other services are unchanged and remain DRAFT.
- `wp-content/plugins/seo-booster-core/` v0.1.0. See the plugin's README.md.
  - Package meta box, the `sb_package_group` taxonomy, and a publishing gate (fixed price needs price > 0 plus both approvals).
  - The `[sb_packages]` shortcode: accessible group tabs, package cards, quote cards, and a swipe row on mobile.
  - A line-item snapshot of package terms, visible on the order, in emails and in the customer's account.
  - Service order statuses. Orders never auto-complete on payment, and the new statuses count as paid in reports.
  - The post-purchase brief:
    - My Account endpoint with conditional fields per package type (off-page, web, content, design, SEO, generic)
    - protected uploads with a MIME/size whitelist and a nonce- and capability-checked download
    - admin panel and orders column
    - reminders at 24 h and 72 h
  - Catalog importer (Tools → SEO Booster catalog, plus `wp sb import-catalog`) with dry run, upsert by SKU, and the approval rules.
  - Declares compatibility with HPOS and the cart/checkout blocks.
- `tools/build-plugin-zip.sh` creates `dist/seo-booster-core.zip` (git-ignored).
- `brand/`: logo.svg, logo-light.svg, logo-mark.svg, favicon.svg and site-icon-512.png.
- `DESIGN_SYSTEM.md`: tokens, computed contrast matrix, WoodMart/Elementor mapping, component inventory and wireframes.
- `docs/package-preview.html` and `docs/screens/*.png`: a static render using the plugin's real CSS and JS.

**Commands and results**
- `php -l` on every plugin file: no syntax errors (PHP 8.3).
- Playwright run on the preview: no horizontal overflow at 360, 768 or 1440 px. Keyboard ArrowRight switches tabs (`aria-selected=true`, previous panel hidden).
- Contrast computed for every palette pair. Two failing pairs are documented as "never use".

**NOT tested yet (be clear about this)**
- The plugin has **not run inside WordPress/WooCommerce**.
  - Running a local WordPress/WooCommerce in this container was blocked by the session's permission policy.
  - The live site rejected the supplied Application Password (`incorrect_password`, HTTP 401) on 2 Nov.
- So these are all untested end to end: cart, checkout, order statuses, brief and importer.

**Blockers**
1. **A working WordPress Application Password** for user `admin` on seobooster.uk. Alternatively, install `dist/seo-booster-core.zip` manually in wp-admin.
2. Premium Links "from" prices (optional; until then they stay quote-only).
3. Legal, tax and payment-account items from RISKS.md §A are unchanged.

**Next step:** once access works:
1. Take a Hostinger backup.
2. Install the plugin.
3. Run the importer as a dry run, then for real.
4. Apply the WoodMart/Elementor tokens.
5. Build `/services/off-page-seo/`.
6. Do a test checkout with BACS: cart → order → brief → status changes.
7. Record the results here.

---

## Phase 01 — Discovery · 2 Nov 2026 · ✅ complete
- Route locked as `wordpress` (WoodMart + Elementor + WooCommerce + `seo-booster-core`).
- Build on seobooster.uk while the site is pre-launch.
- Payments: Stripe, PayPal and BACS, in test mode only.
- Read-only audit: WordPress 7.1.4, WooCommerce 11.2.1, Elementor 4.3.5, WoodMart child, PHP 8.5, Hostinger + LiteSpeed. Demo pages only and 0 products.
- Docs written: ARCHITECTURE, DATA_MODEL, ROUTES, RISKS, BUILD_PLAN. No site changes.
