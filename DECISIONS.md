# Owner decisions (approval required before production)

## Locked — 2 Nov 2026 (Phase 01)
| Item | Decision |
|---|---|
| Build route | **`wordpress`** with WooCommerce and the custom `seo-booster-core` plugin. **Changed 2 Nov (owner): custom block theme `seo-booster` (theme.json + templates/index.html) replaces WoodMart/Elementor**, "build the complete website in one go" |
| Visual builder | WordPress block editor / Site Editor (native). WoodMart and Elementor stay installed but inactive, so you can roll back |
| Environment | Build directly on seobooster.uk while pre-launch; Hostinger backup before each write phase; noindex until launch |
| Payment methods | Stripe, PayPal, BACS (Payoneer/bank transfer), **test/sandbox mode only** until owner approves going live |
| Off-Page group A (2 Nov) | "Profiles and Citations": 8 tiers of 5 / 10 / 15 / 20 / 30 / 50 / 75 / 100 links. A mix of business listings, directory submissions, local citations and profile links. Owner's price anchors: 5 links = $5, 10 = $10, 20 = $15–18. Claude filled in the other tiers on the same volume-discount curve: 15 = $14, 20 = $17, 30 = $24, 50 = $37, 75 = $52, 100 = $65. **Owner can change any price in wp-admin.** |
| Off-Page group B (2 Nov, updated) | "Premium Links": 7 guest-post tiers plus press release. Owner prices: DR10+ $10, DR20+ $25, DR30+ $49, DR50+ $89. Claude extended the curve: DR40+ $69, DR60+ $139, DR70+ $199, Press Release writing + distribution $99. Fixed price, no longer quote-only |
| All other prices (2 Nov) | Owner told Claude to research and set prices. Set in the budget-marketplace band; see PRICING_RESEARCH.md. PPC, Analytics, Email and Automation stay DRAFT until their service pages are written |
| Business details (2 Nov) | Owner said to use placeholders for now and will replace them later. Public brand is "SEO Booster". Contact email placeholder is `hello@seobooster.uk`, and that mailbox must exist. **No invented address, company number or legal name is published.** Those fields are left out of the site until the owner supplies them |
| Logo / favicon (2 Nov) | Claude designed placeholder versions in `brand/`, approved by the owner for use now |
| App password | Three passwords supplied (2 Nov). All got `incorrect_password` **from inside this cloud container only**. Cause found: requests through the container's egress proxy get `401 incorrect_password` from `/wp-json/` even with **no** credentials, while a direct request returns 200. So the proxy path alters the Authorization header, and the passwords are probably valid. Not worked around (proxy must not be bypassed). Owner installs the plugin zip manually; MCP should work from the owner's own machine. Passwords stored only in the local user config, never in git |

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
