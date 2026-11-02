# SEO Booster — Claude Code Website Build Kit
**Prepared:** 31 October 2026 | **Purpose:** production-grade agency website with purchasable service packages, not a static mockup.

## Start here
1. Read `PROJECT_BRIEF.md`, `CLAUDE.md`, `DECISIONS.md`, `SERVICE_CATALOG.csv`, and `QA_LAUNCH.md`.
2. Pick exactly one deployment route: **A WordPress + WooCommerce** (recommended) or **B custom full-stack**. Don't build both unless explicitly authorized.
3. Open Claude Code in a NEW Git repository/project folder, copy `CLAUDE.md` to the repository root, then paste `phase-prompts/01-discovery.md` into Claude Code. Use Plan Mode first.
4. Progress through prompts `02` to `08` in order. Each phase has acceptance gates and must leave working artifacts in the repo. Don't attempt all phases in one gigantic agent instruction.
5. Use `SERVICE_CATALOG.csv` as *proposed information architecture*, NOT approved prices/deliverables. Pricing, payment account, jurisdictions, company statements, timelines, credentials, testimonials and guarantees all require explicit owner confirmation.
6. For WordPress: build with a native block theme + a standalone functionality plugin OR Elementor MCP and native editable Elementor layouts if visual editing is a priority. Do not accidentally combine two mutually conflicting page-builder frameworks.
7. For custom route: build actual application + CMS + backend checkout/order handling. A single `index.html` is not the finished site.

## Practical recommendation
WordPress + WooCommerce is the default because it already supplies an admin panel, product variations, coupons, order records and fulfillment statuses. Set professional-service products as **virtual** to remove shipping; **do not mark as downloadable** unless immediate downloadable deliverables exist. Begin with a curated subset of approved packages; allow subsequent expansion to 16+ per service through data, not hand-coded pages.

## Deliverables expected from Claude Code
- Version-controlled code and setup documentation
- Editable service pages and reusable package cards
- Working cart, supported payment gateway checkout, post-purchase brief collection, order emails and admin order view
- Responsive design, real or clearly marked unverified business proof, search-ready technical baseline and analytics consent configuration
- Automated checks and a tested launch checklist; a real test checkout before launch

## Current references
- Anthropic Claude Code `CLAUDE.md` and Plan Mode: https://support.claude.com/en/articles/14553413-claude-code-cheatsheet
- Elementor native MCP setup: https://elementor.com/help/how-to-connect-elementor-to-an-ai-tool-using-mcp/
- WordPress block theme: https://developer.wordpress.org/themes/core-concepts/theme-structure/
- WordPress `theme.json`: https://developer.wordpress.org/themes/global-settings-and-styles/introduction-to-theme-json/
- WooCommerce variable products: https://woocommerce.com/document/variable-product/
- WooCommerce virtual services: https://woocommerce.com/document/managing-products/virtual-downloadable/
- WooCommerce Add-Ons / brief fields: https://woocommerce.com/document/product-add-ons/
- WooCommerce checkout block: https://woocommerce.com/document/woocommerce-store-editing/customizing-cart-and-checkout/checkout-block/
- Google Search quality: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search spam: https://developers.google.com/search/docs/essentials/spam-policies

**Licensing and payment note:** Elementor Pro, WooCommerce extensions, and payment gateways may require paid plans; compatibility and legal eligibility must be verified for the *actual* company and processor account. No assumptions that Stripe is available to the operating entity.
