# SEO BOOSTER — COMPLETE PRODUCTION WEBSITE SPECIFICATION
**Project:** SEO Booster digital growth, web and creative services agency
**Audience:** SMEs, ecommerce brands, agencies, founders and B2B teams in international markets
**Commercial model:** transparent fixed-scope services/packages purchased online + bespoke consultation/quote services + optional retainers.
**North-star:** turn qualified organic/referral visitors into inquiries and paid orders with clear scope, trustworthy content and easy post-payment onboarding.

## 1. Hard requirements
1. The result must be a real business-ready website, not a landing page only. Native admin editability and a functional checkout/order workflow are mandatory.
2. All pages and packages are data-driven and independently maintainable. No hand-coded prices buried in JSX/HTML/PHP.
3. Buyers can select package, review deliverables/exclusions/turnaround/revisions, customize eligible options, place order, submit required URLs/files/instructions and receive confirmation. Fulfillment team sees all fields in one order record.
4. Each service can include *multiple groups of packages* (e.g. 8 citations/profile links and 8 editorial outreach/guest posting); per-group comparisons must remain understandable on mobile.
5. Checkout supports applicable taxes and compliant payment methods; no shipping for virtual services; issue payment confirmations and retain transaction IDs via provider integration.
6. Realistic professional graphics, rights-cleared and optimized. No fake testimonials, invented customer logos, results, counters or unsupported claims.
7. About, Contact, Terms, Refunds, Privacy, Cookies, Accessibility and service-specific terms must exist and be legally reviewed before go-live.
8. Provide complete responsive layouts, SEO architecture, performance, security, anti-spam, backups, accessibility and measurable conversion events.

## 2. Information architecture
### Public top navigation
- Home `/`
- Services `/services/` with mega-menu or accessible grouped dropdown
- Packages `/packages/` (optional central comparison/filters)
- Work / Case Studies `/work/` (verified cases only)
- About `/about/`
- Insights `/insights/`
- Contact `/contact/`
- Primary CTA `Explore Packages` or `Get a Proposal`
- Utilities: search, cart, account

### Service categories + recommended URLs (review content differentiation)
**SEO & visibility**
- SEO Services `/services/seo/` (category hub)
- SEO Audit `/services/seo-audit/`
- On-page SEO `/services/on-page-seo/`
- Technical SEO `/services/technical-seo/`
- Off-page SEO & Link Acquisition `/services/off-page-seo/`
- Local SEO `/services/local-seo/`
- Ecommerce SEO `/services/ecommerce-seo/`
- Content SEO `/services/content-seo/`
- AI Search / AEO / GEO Consulting `/services/ai-search-optimization/`
- SEO Strategy / Monthly Retainers `/services/managed-seo/`

**Web & ecommerce**
- Website Design & Development `/services/website-development/`
- WordPress Development `/services/wordpress-development/`
- Ecommerce Development `/services/ecommerce-development/`
- Website Maintenance `/services/website-maintenance/`
- WordPress Fixes & Troubleshooting `/services/wordpress-fixes/`
- Website Speed & Core Web Vitals `/services/website-speed-optimization/`
- Landing Page Design `/services/landing-page-design/`

**Content & creative**
- Content Writing `/services/content-writing/`
- Website Copywriting `/services/website-copywriting/`
- Blog & Article Writing `/services/blog-writing/`
- Product Descriptions `/services/product-descriptions/`
- Graphic Design `/services/graphic-design/`
- Brand Identity & Brand Kits `/services/brand-identity/`
- Social Graphics & Ad Creatives `/services/social-media-graphics/`

**Digital growth / operations**
- PPC / Paid Media Management `/services/ppc-management/`
- Google Ads `/services/google-ads/`
- Social Media Marketing `/services/social-media-marketing/`
- Email Marketing `/services/email-marketing/`
- Conversion Rate Optimization `/services/conversion-rate-optimization/`
- Analytics & Tracking `/services/analytics-tracking/`
- Marketing Automation & AI Workflows `/services/marketing-automation/`

Do not automatically publish all of these: run keyword-intent and differentiation research to avoid overlap and thin pages. Start with well-scoped categories and build more pages only when content and operational capacity exist.

### Business/support pages
`/about/`, `/contact/`, `/work/`, `/insights/`, `/faq/`, `/how-it-works/`, `/get-a-quote/`, `/my-account/`, `/cart/`, `/checkout/`, `/order-received/` (system endpoint), `/terms/`, `/refund-policy/`, `/privacy-policy/`, `/cookie-policy/`, `/accessibility/`, `/disclaimer/` (if needed), `/404/` template. Header/footer accessible, no dead links.

## 3. Homepage blueprint
1. Minimal sticky header: responsive logo, well-grouped services, CTA, cart/account.
2. Strong first screen: audience-specific H1, value proposition, 2 conversion paths (browse packages / request custom proposal), trust language backed by verified experience.
3. Service family cards with meaningful differentiated copy and icons/visual motifs.
4. Problem -> process -> business outcome narrative; no fabricated numerical results.
5. Featured package selectors linking to service detail, with starting prices **only if approved**.
6. Why work with us: transparent scope, human review, reporting, accountable delivery.
7. How it works: choose scope, complete brief, payment/onboarding, delivery/review.
8. Real work / examples; if not approved, use labelled illustrations of deliverables instead of fabricated cases.
9. Featured useful insights; 1–2 documented frameworks / methods.
10. FAQ accordion with valid, useful policies.
11. Final CTA and contact / sales inquiry.
12. Detailed footer: services, business info where verified, policies, channels, socials.

## 4. Canonical service page template
- Hero with service-specific customer problem, offer and relevant CTA.
- Who it's for / not for, outcomes and realistic limitations.
- Optional group navigation (e.g. `Citations & Profiles` / `Editorial Outreach & Guest Posts`).
- 4–16 data-driven, filterable or tabbed package cards with clear quantities, deliverables, price, turnaround, revisions, exclusions, currency, CTA and ideal customer.
- A mobile-friendly comparison table / accordion; no horizontally broken pricing table.
- Process and deliverables, sample report/reporting format, what buyer must provide.
- FAQ with actual policies and links to terms.
- Related services and custom quote CTA.
- Unique metadata, breadcrumb, meaningful internal links, structured data only if eligible and factual.

## 5. Package model (schema)
Represent offers with `service_category`, `service_slug`, `group_slug`, `package_slug`, `title`, `pricing_model` (fixed/range/quote/subscription), `currency`, `price`, `billing_period`, `quantity_unit`, `quantity`, `deliverables`, `exclusions`, `turnaround_range`, `revisions`, `requirements`, `optional_addons`, `visibility`, `approved`, `product_id`, `sort_order`, `related_offer_ids` and `terms_version`.
Use **approved** values for live prices and scope; require `approved=true` for publish. Quote-only products must route to lead forms, not zero-value checkout.

### Off-page SEO examples
Group A: directory / business listing / profile citations. Illustrative counts `5, 10, 15, 20, 25, 30, 40, 50` placements *where appropriate*; distinguish profile URLs from validated business citations. Specify manual/automated submission, account ownership, NAP consistency, site categories, indexing disclaimers and report proof.
Group B: editorial outreach / guest-post coordination, e.g. `1, 2, 3, 4, 5, 6, 8, 10` placements pending supply. Define editorial quality criteria and publisher acceptance, sponsored disclosures where applicable, content cost, replacement terms and whether placement can legitimately be guaranteed. Do not guarantee ranking improvements, `dofollow` status or permanent links without a verified contractual basis. Review offerings against search engine spam policies and applicable disclosures.

### Website development examples
One-page landing site, 2-page starter, 5-page business, 10-page business; optional extra-page fee, revision allowance, accessibility/performance scope, responsive templates, analytics, content entry, CMS training, hosting and theme/plugin license exclusions. Separate ecommerce/WordPress plans if complexity warrants.

### Maintenance/fixes examples
Single issue diagnostic, simple fix, multi-issue bundle, malware cleanup assessment (quote if needed), monthly basic care, monthly growth care. Clarify hours, supported platforms, SLA response target vs fix commitment, backups, updates, exclusions and incident escalation.

### Writing examples
500, 1,000, 1,500, 2,000, 3,000-word original articles, batches of 5 or 10 articles, landing-page copy, product-description quantities. Include research level, subject expertise, editorial reviews, revisions, plagiarism checks, citation handling and AI usage disclosure policy. Word counts are scopes, not promises of SEO results.

### Graphics examples
Single banner/ad creative; 3-pack/5-pack; social post template set; campaign ad suite; logo refinement; mini brand kit; full identity system (logo variants, palette, typography, brand book, templates); custom branding project. Clearly define source files, formats, licensing, stock assets, rounds of revision and turnaround.

### Additional categories
PPC: audit, account setup, campaign builds, monthly management; ad spend billed separately with approved minimums.
Social: editorial calendar, creative batch, channel management; clarify organic vs paid and platform approvals.
Analytics: GA4/GTM tracking audit, setup, dashboard, measurement plan, conversion events; consent and access requirements.
Automation: workflow discovery, single automation, multi-stage implementation, managed maintenance; data processing and credentials handling.
SEO subscriptions: monthly packages with precise deliverables, contract duration, billing/cancellation terms, reporting and implementation boundaries.

## 6. Ecommerce & post-purchase system
### Choose a package
- All public packages have unique SKU/ID, fixed or legitimately variable price, sale validity controls and clear ordering restrictions.
- Data-backed package cards: `View Details`, `Add to Cart`, optionally `Buy Now`.
- Variations only for a meaningful axis (e.g. page count) and manageable variation counts; distinct products when scope differs fundamentally.
- Optional add-ons: expedited delivery (if service permits), extra revisions, copywriting, additional pages, keyword research, or creative source files. No hidden forced upsells.

### Checkout
- Service products virtual (skip shipping), tax configuration based on entity and customers and legal advice; USD default until confirmed.
- Guest checkout or account creation (owner decision); clear billing, coupon, accepted payment methods, VAT/tax where applicable, terms checkbox and confirmation.
- Do not collect payment data directly; use provider-hosted checkout or supported payment integration.
- Test both supported checkout block/classic checkout and addons/gateways together; fall back to compatible layout if necessary.

### Project brief
- Capture required URLs, domain, target pages, target geography, brand files, writing brief, preferred tone, competitor examples, platform details, logo files etc. **Conditional by package type**.
- Prefer minimal secure fields at purchase and a post-payment authenticated `Complete your brief` step for longer information; reminders for incomplete briefs.
- Validation, size limits, MIME checking, malware scanning if supported, retention and access restrictions on uploaded assets.
- Store fields against the order line items and/or order with scoped permissions. Show buyer confirmation and admin actionable view.
- Never ask for plain-text passwords; use delegated access, secure transfer or temporary credentials with documented rotation.

### Fulfillment lifecycle
`Awaiting payment` -> `Paid / Awaiting brief` -> `Brief received` -> `In progress` -> `Client review` -> `Delivered` -> `Completed` / `Refunded` / `Cancelled`; map custom workflow to provider/Woo order statuses without breaking payment semantics. Admin note, internal assignment, milestones, deliverable files, email events and optional customer portal. Beware service orders should NOT auto-complete just because payment succeeded.

## 7. Design system
- Tone: credible, confident, precise, no inflated claims.
- Palette proposal: ink/navy #0C1930, primary blue #2563EB, accent lime #B9F24C, body slate #475569, background #F8FAFC; contrast-test all combinations. Neutral light surfaces with selective dark sections.
- Typography proposal: Manrope headings, Inter body with performance-aware font loading.
- Layout: 1200–1280px content max width, fluid gutters, systematic spacing, consistent radii, 44px+ target size for key controls where feasible.
- Components: button system, content cards, service tiles, package cards, compare lists, tabs, FAQ, breadcrumbs, blog cards, forms, trust panels, empty/error/success states, navigation, footer.
- Visuals: custom brand diagrams, service illustrations, technical process snapshots, genuine deliverable previews with private details removed; no stock people masquerading as actual team; responsive images with descriptive alt text when informative.
- Motion: subtle and reduced-motion compliant, never slowing content interaction.

## 8. Content + SEO/AEO
- Each service page should match a distinct intent and state who, what, how, deliverables, price/scope, limitations and next action.
- Create editorial standards and source-linked service research. Verify claims and avoid copied/rephrased competitors.
- Technical: canonical, meta title/description, XML sitemap, robots, breadcrumbs, Open Graph, schema as applicable (Organization, BreadcrumbList, Service when valid, FAQ visible content but no promise of FAQ rich snippets), properly managed redirects, search-friendly navigation, indexability and 404 behavior.
- AI discoverability: clear semantic headings, accessible HTML, concise descriptive answers, visible authorship/business credentials where verified, crawlable content, consistent factual business information. No fabricated AI SEO tricks.
- Core Web Vitals field targets at 75th percentile: LCP <=2.5s, INP <=200ms, CLS <=0.1; measure actual tests, don't promise scores without evidence.
- Blog: topic clusters and articles that support real services; author/date/update, sources, unique expertise and editorial workflow.

## 9. Trust and legal
- No fabricated logos, stats, reviews, memberships, office photos, team members or case studies.
- Explain fulfillment, access requirements, reporting cadence, revisions, cancellation, refund conditions and how approved link placements are handled.
- Terms, refund, privacy, cookies and any processor-required disclosures must be reviewed against relevant jurisdiction and service type. Flag incomplete legal copy, don't pretend to provide legal approval.
- Tracking/cookies and consent implementation must respect applicable laws; use category-aware consent management if required.

## 10. Performance & security
- HTTPS, reliable backups, staging, least-privilege accounts, 2FA where possible, role-limited upload access, CSRF/XSS/SQLi mitigation, input validation and secure secrets.
- WP route: compatible PHP/WP versions, Woo HPOS-aware extensions, updates, caching exclusions for cart/checkout/account, object cache only if supported and configured, emails with SPF/DKIM/DMARC, logged errors without PII, restore test.
- Custom route: auth and authorization, CSRF, webhook signature verification, idempotent order events, rate limits, secure file storage, database migrations and backups, error logging and security headers.
- Image optimization and caching, minimal JS, zero unused builder libraries, accessibility checks and mobile regression tests.

## 11. Acceptance criteria
- Every launched route loads, has accurate unique copy and works at 360px+, on Chrome/Safari/Firefox as practical.
- At least one service with two package groups and a fully tested purchase journey is complete before adding all remaining categories.
- Approved product changes in admin reflect correctly on service cards and checkout, without code changes.
- Real or sandbox payment end-to-end successfully records paid order with exact package, variant, amount, taxes, addons and submitted brief; refund and failed payment paths tested.
- Lead form delivers and records consent appropriately; admin receives actionable order alerts.
- No fabricated proof, missing pages, lorem ipsum, dead buttons, broken forms, console errors, placeholder payments or unsupported performance statements.
- Document deployment, rollback, backup restore, ownership of plugins/themes/licenses, admin training, operational handover.
