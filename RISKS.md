# RISKS & BLOCKERS

## A. Launch blockers (owner input required; the build continues around them)
| # | Blocker | Needed from owner | Blocks |
|---|---|---|---|
| B1 | Prices/scope for packages other than Off-Page group A (group A priced 2 Nov; Premium Links quote-only) | "From" prices for Premium Links; prices + scope for Web, Content, Design, Technical SEO, Audit | Publishing those packages |
| B2 | Legal trading entity, registered address, company number, jurisdiction | Exact details | Footer, Terms, Privacy, tax, payment accounts |
| B3 | Stripe and PayPal account eligibility for that entity and country | Confirmation that both accounts are active and in good standing | Live card/PayPal payments (sandbox can proceed) |
| B4 | Payoneer / bank transfer details for BACS | Account details, entered by the owner in wp-admin | BACS instructions |
| B5 | Tax/VAT position (UK VAT registration? international B2B reverse charge?) | Accountant's guidance | Tax settings, invoices |
| B6 | Terms, Refund, Privacy, Cookie and service-specific terms | Legal review of the drafts | Launch |
| B7 | Logo and brand assets (SVG logo, favicon) | Files | Design phase finalisation |
| B8 | Real proof: case studies, testimonials, client logos, credentials | Verified items with permission | `/work/` and trust sections (left out if none) |
| B9 | Contact/proposal form recipient email and auto-reply wording | Email address | Lead routing |
| B10 | SEO plugin choice (Rank Math vs Yoast) | Pick one | Phase 06 metadata |
| B11 | Guest-post/citation supply: who fulfils it, publisher criteria, replacement policy | Process description | Off-Page copy and terms |
| B12 | Analytics: GA4 property / GTM container, consent tool | IDs, choice | Consent and analytics |

## B. Technical risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Building directly on production (owner decision) breaks the live site | Med | Med (not launched) | Hostinger backup before each write phase, logged in PROGRESS.md; changes made in small steps; plugin can be deactivated instantly |
| WoodMart + Elementor page weight hurts Core Web Vitals | High | Med | Turn off unused WoodMart modules, wishlist and compare; optimise Elementor assets; LiteSpeed CSS/JS optimisation tested on checkout; measure, don't promise |
| LiteSpeed caching cart/checkout/session pages | Med | High | Exclude `/cart`, `/checkout`, `/my-account` and the Woo cookies; test with two browsers |
| Checkout Block vs gateway/add-on incompatibility | Med | High | Test Stripe and PayPal in the block checkout; fall back to the classic shortcode checkout if any incompatibility appears |
| Custom statuses break payment reporting | Low | High | Register them as paid statuses; never touch the transaction ID; test refunds |
| Uploads exposed publicly | Med | High | Deny-all directory + capability-checked download handler + MIME/size validation; test direct URL access |
| Credentials pasted into chat/git | Med (already happened once in this session) | High | Env-var only; **rotate the Application Password shared earlier in chat** |
| PHP 8.5 + plugin compatibility | Low–Med | Med | Check the Woo status report; keep plugins minimal |
| WoodMart MCP / Elementor MCP Composer are new tools | Med | Low | Fall back to the REST API and the Elementor editor; every change verified by reading it back |
| Container network blocks the site | Low (confirmed reachable) | Med | Hostinger connector as an alternative path |

## C. Content and compliance risks
| Risk | Mitigation |
|---|---|
| Link-building offers breaching Google's spam policies (paid links without `rel=sponsored`, ranking/dofollow/permanence guarantees) | Copy states editorial control, sponsored disclosure where applicable, and no ranking/dofollow/permanence guarantees; reviewed against https://developers.google.com/search/docs/essentials/spam-policies |
| Thin or near-duplicate service pages | MVP limited to 8 differentiated services; overlapping intents merged (e.g. WordPress fixes inside Maintenance) |
| Fabricated trust signals carried over from the WoodMart demo (stock testimonials, counters, logos) | Every demo widget is removed when its page is rebuilt; QA grep for demo text |
| Legal drafts mistaken for approved text | Visible "Draft – requires legal review" banner until the owner signs off |
