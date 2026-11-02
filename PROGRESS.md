# PROGRESS

## Phase 01 — Discovery · 2 Nov 2026 · ✅ complete
**Decisions locked (owner):**
- Route: `wordpress` (keep WoodMart + Elementor + WooCommerce, with custom `seo-booster-core` plugin)
- Environment: build on seobooster.uk while pre-launch
- Payments: Stripe, PayPal, BACS (Payoneer/bank), all in test mode until approved

**Work done**
- Build kit committed to the repo root (`91b9e72`).
- Read-only audit of seobooster.uk:
  - Stack: WP 7.1.4, Woo 11.2.1, Elementor 4.3.5, WoodMart child, PHP 8.5, Hostinger + LiteSpeed.
  - Content: demo pages only, 0 products.
  - MCP endpoint reachable (401 without auth).
  - Details in ARCHITECTURE.md §1.
- Wrote ARCHITECTURE.md, DATA_MODEL.md, ROUTES.md, RISKS.md and BUILD_PLAN.md.
- Updated DECISIONS.md with the locked decisions.

**Commands run (all read-only):** `curl` against `/`, `/wp-json/`, `wp/v2/pages`, `wc/store/v1/products`, `wc/store/v1/products/categories`, `/wp-json/mcp/...` and the common routes.

**Site changes:** none.

**Tests:** none applicable (docs-only phase).

**Open items**
- Owner input: the blocker list in RISKS.md §A, starting with **B1 (Off-Page SEO prices/scope)**, B2, B3 and B7.
- Security: the WordPress Application Password was pasted into chat earlier in this session. Revoke it and issue a new one, stored only as the `WP_API_PASSWORD` environment secret.
- The WoodMart MCP needs a session restart (and the env secret) before it loads.

**Next step:** Phase 02 (Design system). Before any write, take a Hostinger backup of seobooster.uk.
