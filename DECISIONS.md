# Owner decisions (approval required before production)

## Locked — 2 Nov 2026 (Phase 01)
| Item | Decision |
|---|---|
| Build route | **`wordpress`**: keep the existing WoodMart + Elementor + WooCommerce on seobooster.uk, plus the custom `seo-booster-core` plugin (see ARCHITECTURE.md) |
| Visual builder | Elementor (existing), with WoodMart theme settings; no block theme |
| Environment | Build directly on seobooster.uk while pre-launch; Hostinger backup before each write phase; noindex until launch |
| Payment methods | Stripe, PayPal, BACS (Payoneer/bank transfer), **test/sandbox mode only** until owner approves going live |

## Original assumptions and open questions
| Item | Current assumption / question |
|---|---|
| Build route | A: WordPress + WooCommerce **preferred**; B: custom full-stack optional |
| Domain | seobooster.uk (verify authoritative live domain and staging URL) |
| Deployment | Hostinger Business shared hosting may be suitable for WordPress; verify actual plan and access; custom route needs supported server runtime |
| Visual builder | Select either block theme or Elementor MCP; existing WoodMart/Elementor work may be preserved if continuing current site |
| Business identity | Confirm actual legal trading entity, contact details and jurisdiction. Do not invent company number or address |
| Target customers | International B2B; initial site English (UK spelling), USD display prices unless changed |
| Brand | Professional blue / lime / navy / neutral palette proposed; finalise actual logo and brand assets |
| Fonts | Manrope headings, Inter body proposed; locally hosted where licensing permits |
| Prices | TBD. Never use invented market-rate pricing as live prices |
| Product lineup | Proposed in SERVICE_CATALOG.csv; approve packages, output counts, turnaround, revisions and guarantee language |
| Link building policy | No ranking guarantees, deceptive claims or hidden link schemes; spell out nature, qualification and editorial control of placements |
| Checkout | Confirm actual processor/gateway, supported country/entity/currency, tax and payout setup |
| Refund terms | Owner/legal review required: scope, work-started rules, digital/service delivery, cancellation and jurisdiction |
| Brief collection | Product-specific fields and optional uploads; privacy retention and security requirements apply |
| Evidence | Real testimonials, portfolios, certifications, logos only after verification or permission |
| Lead routing | Contact form destination, CRM/email integration, spam controls and auto-replies TBD |
| Language | English public copy; owner can brief Claude in Roman Urdu |
| Launch | Explicit approval after sandbox checkout, performance, security and content verification |

## Do not block discovery for noncritical unknowns
Use approval flags in structured data and placeholder labels in internal staging only; NEVER invent live prices, addresses, policies, testimonials, or client results. If launch-critical information remains unavailable, output a precise blocker list and continue independent development.
