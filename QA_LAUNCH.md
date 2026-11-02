# QA & launch gates

## Functional
- [ ] WordPress/native admin or custom CMS can edit packages and their prices without code edits
- [ ] Two independent package groups on off-page SEO page, mobile selectors and accurate counts
- [ ] Website plans 1, 2, 5, 10 pages; writing word counts; brand graphics packages
- [ ] Package -> cart -> supported checkout -> confirmation -> order -> fulfillment tested end-to-end
- [ ] Sandbox paid, declined, cancelled and refunded payment tests recorded
- [ ] Tax, currency, variation and add-ons verified in order lines
- [ ] Brief fields are conditional, safely stored and attached to order, with admin access
- [ ] Virtual service items do not show shipping charges or delivery address unless required for billing/tax
- [ ] Contact, proposal, search, FAQ, blog, account, emails and password reset tested
- [ ] Broken links/buttons/menus and console errors fixed

## Trust and legal
- [ ] Approved business identity, return/refund/service rules, privacy and cookie terms
- [ ] No fake results, reviews, company logos, certificates, people or unverified guarantees
- [ ] Off-page offers reviewed for accurate publisher/placement claims and search-policy concerns
- [ ] Payment provider and business eligibility, webhook security and PCI scope validated
- [ ] Accessible consent and analytics configurations where required

## Design & quality
- [ ] Responsive 360, 390, 768, 1024, 1440 pixels, no layout overflow
- [ ] Header/footer/typography/spacing/cards consistent across service templates
- [ ] Accessible semantic hierarchy, focus/keyboard, adequate contrast, forms with error hints
- [ ] Content unique, actionable, specific, legally safe; no lorem ipsum or dummy CTA
- [ ] Real visuals or clearly generic branded diagrams with rights confirmed
- [ ] LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 targets; measured data differentiated from goals
- [ ] Metadata, robots, XML sitemap, redirects, canonical, structured data and internal links audited

## Security & operations
- [ ] HTTPS, MFA/least privilege, protected secrets and uploads, backups/restore tested
- [ ] WP updates / Woo compatibility / plugins documented; cache exemptions tested
- [ ] Webhook replay tested if applicable, no duplicate paid orders
- [ ] Staging noindexed, no test payment products or credentials on production
- [ ] Versioned deploy, rollback, monitored order emails, operating guides delivered
- [ ] Owner has approved domain launch, live payment activation and legal documents
