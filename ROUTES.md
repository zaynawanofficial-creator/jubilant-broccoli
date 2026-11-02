# ROUTES — URL map

> **Built 2 Nov 2026 (block theme).** The setup screen creates the URLs below. Changes from the original plan:
> - **No `/services/seo/` hub.** `/services/` groups everything.
> - **No `/work/` page** until verified case studies exist.
> - **`/insights/` is the posts page.**
>
> Pages created: `/`, `/services/`, `/services/{off-page-seo, seo-audit, technical-seo, website-development, website-maintenance, content-writing, graphic-design}/`, `/packages/`, `/how-it-works/`, `/about/`, `/contact/`, `/get-a-quote/`, `/faq/`, `/insights/`, `/terms/`, `/refund-policy/`, `/privacy-policy/`, `/cookie-policy/`, `/accessibility/`.
>
> Articles: `/citations-vs-profile-backlinks/`, `/choose-guest-post-dr-tier/`, `/wordpress-speed-checklist/`.

Status legend:
- **MVP**: built in phases 02–06.
- **Draft**: created but kept unpublished.
- **Planned**: not built until the owner approves the content and capacity.
- **System**: a WooCommerce or WordPress endpoint.

Indexing is noindex while the site is pre-launch. After launch, indexing follows the column below.

## Public
| Route | Type | Status | Index | Notes |
|---|---|---|---|---|
| `/` | Elementor page (replaces demo `home-corporate-2`) | MVP | yes | Set as front page |
| `/services/` | Elementor hub | MVP | yes | Category families, then service cards |
| `/services/seo/` | Elementor category hub | MVP | yes | |
| `/services/off-page-seo/` | service page, 2 groups | **MVP – first vertical slice** | yes | `[sb_packages service="off-page-seo"]` |
| `/services/seo-audit/` | service page | MVP | yes | |
| `/services/technical-seo/` | service page | MVP | yes | |
| `/services/website-development/` | service page (1/2/5/10 pages) | MVP | yes | |
| `/services/website-maintenance/` | service page (fixes + care plans) | MVP | yes | Covers "WordPress fixes" intent to avoid a thin duplicate |
| `/services/content-writing/` | service page (2 groups: articles, batches) | MVP | yes | |
| `/services/graphic-design/` | service page (2 groups: social creatives, branding) | MVP | yes | |
| `/services/ppc-management/`, `/services/analytics-tracking/`, `/services/email-marketing/`, `/services/marketing-automation/` | service pages | Draft | — | Catalog rows exist; publish only once approved |
| Remaining brief URLs (local, ecommerce, AI search, managed SEO, WordPress dev, speed, landing pages, copywriting, blog writing, product descriptions, brand identity, social graphics, Google Ads, social media, CRO) | — | Planned | — | Checked for keyword and intent overlap before any build |
| `/packages/` | Elementor page with filterable `[sb_packages]` | MVP (after 3+ services are live) | yes | |
| `/product/{slug}/` | Woo single product (package detail) | MVP | **noindex** | Keeps the service page as the canonical ranking URL; the product URL is reached from cards |
| `/how-it-works/` | page | MVP | yes | |
| `/about/` | page (replaces demo `about-us-3`) | MVP | yes | Verified facts only |
| `/contact/` | page (replaces demo `contact-us`) | MVP | yes | CF7 form |
| `/get-a-quote/` | page + CF7 proposal form | MVP | yes | Accepts `?package=SKU` |
| `/faq/` | page | MVP | yes | |
| `/insights/` | posts archive (rename demo `blog`) | MVP template | yes | Published only with real articles |
| `/work/` | case-study archive | Draft | — | Unpublished until verified evidence exists |
| `/terms/`, `/refund-policy/`, `/privacy-policy/`, `/cookie-policy/`, `/accessibility/` | pages | MVP drafts | yes | Banner reads "Draft – requires legal review"; launch blocker |

## System / account
| Route | Index | Notes |
|---|---|---|
| `/cart/` | noindex | cache-excluded |
| `/checkout/`, `/checkout/order-received/{id}/` | noindex | cache-excluded |
| `/my-account/`, `/my-account/orders/`, `/my-account/view-order/{id}/` | noindex | Includes the "Complete your brief" panel |
| `/my-account/sb-brief/{order_id}/` | noindex | New endpoint for the brief form |
| 404 template | noindex | Links to services, search and contact |

## To remove or redirect (demo leftovers)
| Route | Action |
|---|---|
| `/home-corporate-2/` | 301 → `/` after the new home is built |
| `/about-us-3/` | rename slug to `/about/` |
| `/contact-us/` | rename slug to `/contact/` |
| `/blog/` | rename to `/insights/` |
| `/portfolio/` | rename to `/work/` (kept draft) |
| `/shop/` | keep as the Woo shop base, noindex, and remove from the menu (services are the browsing UI) |
| `/wishlist/`, `/compare/` | disable the WoodMart features and remove the pages (not useful for services) |

## Navigation
- **Header:** Services (grouped dropdown: SEO & Visibility · Web & Ecommerce · Content & Creative · Growth) · Packages · How it works · About · Insights · Contact · [Explore packages] CTA · cart · account.
- **Footer:** service links, company, policies, contact.
- Only published routes appear in the menus, so there are no dead links.
