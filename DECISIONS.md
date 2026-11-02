# Owner decisions (approval required before production)

## Locked — 2 Nov 2026 (Phase 01)
| Item | Decision |
|---|---|
| Build route | **`wordpress`**: keep the existing WoodMart + Elementor + WooCommerce on seobooster.uk, plus the custom `seo-booster-core` plugin (see ARCHITECTURE.md) |
| Visual builder | Elementor (existing), with WoodMart theme settings; no block theme |
| Environment | Build directly on seobooster.uk while pre-launch; Hostinger backup before each write phase; noindex until launch |
| Payment methods | Stripe, PayPal, BACS (Payoneer/bank transfer), **test/sandbox mode only** until owner approves going live |
| Off-Page group A (2 Nov) | "Profiles and Citations": 8 tiers of 5 / 10 / 15 / 20 / 30 / 50 / 75 / 100 links. A mix of business listings, directory submissions, local citations and profile links. Owner's price anchors: 5 links = $5, 10 = $10, 20 = $15–18. Claude filled in the other tiers on the same volume-discount curve: 15 = $14, 20 = $17, 30 = $24, 50 = $37, 75 = $52, 100 = $65. **Owner can change any price in wp-admin.** |
| Off-Page group B (2 Nov) | "Premium Links": 8 tiers. Guest posts at DR 20+, 30+, 40+, 50+, 60+ and 70+, plus press release Standard and Premium. Price depends on publisher metrics, so these are **quote-only** until the owner sets "from" prices |
| Business details (2 Nov) | Owner said to use placeholders for now and will replace them later. Public brand is "SEO Booster". Contact email placeholder is `hello@seobooster.uk`, and that mailbox must exist. **No invented address, company number or legal name is published.** Those fields are left out of the site until the owner supplies them |
| Logo / favicon (2 Nov) | Claude designed placeholder versions in `brand/`, approved by the owner for use now |
| App password rotation | Owner declined rotation. Note: the password supplied is **rejected by the site** (`incorrect_password`), so a working one is needed |

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
