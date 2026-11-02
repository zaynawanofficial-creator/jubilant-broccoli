# BUILD_PLAN — phases, steps, acceptance gates

**Rules for every phase:**
- Take a Hostinger backup before the first write to the site.
- Work in small steps and read every change back.
- End the phase by updating PROGRESS.md (files, commands, evidence, bugs, next step), then commit and push.
- Stop for owner review whenever an approval is needed.

## Phase 01 — Discovery ✅ (this commit)
Deliverables: ARCHITECTURE, DATA_MODEL, ROUTES, RISKS, BUILD_PLAN, PROGRESS.
**Gate:** owner reviews the decisions and the blocker list.

## Phase 02 — Design system
1. Write `DESIGN_SYSTEM.md`:
   - tokens: colour (#0C1930 ink, #2563EB primary, #B9F24C accent, #475569 body, #F8FAFC bg, plus neutrals and states), type (Manrope/Inter, self-hosted, with a scale), spacing (4-pt), radii, shadows
   - the contrast matrix (computed)
   - the component inventory
2. Wireframes (markdown/ASCII + annotated) for home, service hub, a two-group service page, package detail, cart, checkout, insights, case study, about and contact.
3. Backup → set WoodMart Theme Settings (colours, typography, header/footer builder) and Elementor global colours/fonts → turn off wishlist, compare and unused modules.
4. Package card and group-tab component spec (desktop grid / mobile accordion; accessible tabs: `role=tablist`, arrow keys).

**Gate:** screenshots at 360/390/768/1024/1440 with zero clipping, contrast AA reported, keyboard nav reported, no lorem ipsum.

## Phase 03 — Commerce engine (`seo-booster-core`)
1. Plugin scaffold:
   - package meta box + taxonomy `sb_package_group` + publishing gate
   - `[sb_packages]` shortcode + Elementor widget
   - quote routing
   - line-item snapshot
   - payment-complete → `sb-awaiting-brief`
2. `wp sb import-catalog` → DRAFT products for all CSV rows.
3. Woo settings: USD, virtual products, guest checkout on (account optional), terms checkbox.
4. Gateways in **test mode**: BACS (configured, owner enters the details), Stripe test keys, PayPal sandbox. Install only Woo's official gateway plugins.
5. Temporarily give one Off-Page package a **test-only** price in a private/draft state to run the flow: card → cart → checkout → paid order → admin view. Revert afterwards.

**Gate:** card, cart and order prices match; an admin price edit updates the card without a code change; failed, cancelled and refunded sandbox payments are tested; the order doesn't auto-complete.

## Phase 04 — Service pages (MVP)
1. Build `/services/off-page-seo/` first: hero, who it's for / not for, the two group tabs, comparison, process, buyer inputs, FAQ, related services, proposal CTA.
2. Then Website Development, Website Maintenance, Content Writing, Graphic Design, Technical SEO, SEO Audit, the `/services/` and `/services/seo/` hubs, and the header mega-menu.
3. Unapproved packages display as "Request a quote" (quote mode) rather than a fake price.

**Gate:** distinct copy per page, working links, mobile tabs/accordion verified, no hardcoded prices.

## Phase 05 — Checkout, brief and client portal
1. Minimal checkout field (`_sb_primary_url`) for the relevant profiles.
2. My Account brief endpoint with conditional profiles, uploads (protected), and status badges.
3. Custom statuses, admin metabox (brief, files, milestones, internal notes, deliverable upload), and emails (brief reminder at 24h/72h, status changes).
4. Sandbox tests: success, decline, cancel, refund, BACS on-hold → paid.

**Gate:** brief linked to the order; a direct upload URL returns 403 to a logged-out user; emails received; payment status correct.

## Phase 06 — SEO, content, trust, legal drafts
1. SEO plugin (owner's choice): titles/meta, canonical, sitemap (exclude system pages), breadcrumbs, OG, Organization schema (verified fields only), BreadcrumbList.
2. About, How it works, FAQ, Contact, Get a quote (CF7 + spam protection + consent), the Insights template, and `/work/` as a draft.
3. Legal drafts with the review banner.
4. 301s for demo slugs.
5. Consent banner (category-aware) before GA4/GTM.

**Gate:** crawl report (no 4xx in navigation), unique titles, noindex on system pages, QA list of missing approvals.

## Phase 07 — Test & optimise
1. Playwright suite in `tests/e2e`: navigation, mobile menu, group tabs, add to cart, checkout valid/invalid, brief, account, contact form, 404, broken links/images, console errors; all widths.
2. Accessibility checks (axe), Lighthouse lab runs (labelled as lab data, not field data), and a LiteSpeed cache-exclusion test.
3. Write `TEST_REPORT.md` + `FIX_LOG.md`, fix the blockers, re-run.

## Phase 08 — Launch & handover
1. `PACKAGE_ADMIN_GUIDE.md`, `ORDER_FULFILLMENT_SOP.md`, `CONTENT_EDITOR_GUIDE.md`, `LAUNCH_CHECKLIST.md`.
2. Backup/restore test, git tag, rollback procedure.
3. SPF/DKIM/DMARC check, live-payment checklist, owner approvals.
4. Final status: **READY** or **BLOCKED** with reasons. Indexing and live payments are switched on only with explicit owner approval.
