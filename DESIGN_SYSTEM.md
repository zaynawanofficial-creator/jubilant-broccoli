# DESIGN_SYSTEM — SEO Booster

The look is a credible, precise B2B agency: navy ink, electric-blue actions, lime used sparingly for emphasis, and light neutral surfaces. No gradient blobs, cartoons or emoji cards.

## 1. Brand assets (`brand/`)
| File | Use |
|---|---|
| `logo.svg` | Header on light backgrounds (mark + wordmark) |
| `logo-light.svg` | Footer and dark sections |
| `logo-mark.svg` | Square mark (social avatar, app icon) |
| `favicon.svg` | Browser favicon (modern browsers) |
| `site-icon-512.png` | WordPress Site Icon (Settings → General). WordPress generates the smaller sizes from it |

The mark is three ascending bars with a growth arrow, standing for "boost". The wordmark is set as SVG text in Manrope 800. **To do before launch:** convert the text to outlines so the logo looks the same everywhere, or replace the whole logo with the owner's final version. The current one is a placeholder the owner has approved for now.

## 2. Tokens
### Colour
| Token | Hex | Use |
|---|---|---|
| `ink` | #0C1930 | Headings, dark sections, selected tab, featured card border |
| `primary` | #2563EB | Primary buttons, links |
| `primary-hover` | #1D4ED8 | Hover/active |
| `accent` | #B9F24C | Badges, tick bullets, highlights on ink. **Never use white text on lime** |
| `body` | #475569 | Body text |
| `muted` | #64748B | Labels and meta (≥ 14 px only) |
| `line` | #E2E8F0 | Borders and dividers |
| `bg` | #F8FAFC | Page background |
| `surface` | #FFFFFF | Cards |
| `success` / `warning` / `danger` | #15803D / #B45309 / #B91C1C | Form states (all ≥ 4.5:1 on white) |

### Contrast results (computed, WCAG 2.x)
| Pair | Ratio | Result |
|---|---|---|
| Ink on white | 17.54:1 | AAA |
| Body on white / bg | 7.58 / 7.24:1 | AAA |
| Muted on white | 4.76:1 | AA |
| White on primary | 5.17:1 | AA |
| White on primary-hover | 6.70:1 | AA |
| Primary link on white / bg | 5.17 / 4.94:1 | AA |
| Ink on lime (badges) | 13.25:1 | AAA |
| Lime on ink | 13.25:1 | AAA |
| Slate-300 #CBD5E1 on ink (body text in dark sections) | 11.81:1 | AAA |
| Primary on ink | 3.39:1 | Large text or UI only. Don't use for body links in dark sections; use lime or white instead |
| Body #475569 on ink | 2.31:1 | **Fail. Never use** |
| White on lime | 1.32:1 | **Fail. Never use** |

### Type
- Headings use Manrope (700/800); body uses Inter (400/500/600). Both are self-hosted woff2 with `font-display: swap`. Load only the weights we use.
- Scale (fluid): H1 `clamp(2.25rem, 5vw, 3.5rem)` · H2 `clamp(1.6rem, 4vw, 2.4rem)` · H3 1.25rem · body 1rem/1.6 · small 0.875rem.
- Line length is capped at 65–70ch for body copy.

### Spacing, radius, shadow
- Spacing uses a 4 px base: 4, 8, 12, 16, 20, 24, 32, 48, 64, 96. Section padding is 64 px on mobile and 96 px on desktop.
- Container max width is 1240 px, with 16 px gutters on mobile and 24 px on desktop.
- Radius: 10 px for buttons and inputs, 14 px for cards, 999 px for pills and tabs.
- Shadows: `0 1px 2px rgba(12,25,48,.05)` at rest and `0 8px 24px rgba(12,25,48,.08)` on hover.
- Touch targets: interactive controls are at least 44 px tall. Primary buttons are 48 px.

## 3. Mapping to WoodMart and Elementor
| Setting | Value |
|---|---|
| WoodMart → Theme Settings → Colors → Primary | #2563EB |
| WoodMart → Secondary | #0C1930 |
| WoodMart → Typography → Content / Title / Secondary | Inter / Manrope / Manrope |
| WoodMart → General → Site width | 1240 (custom) |
| WoodMart → Shop → Wishlist and Compare | **Disabled** (not useful for services) |
| Elementor → Site Settings → Global colours | Ink, Primary, Accent, Body, Line, Bg as named tokens |
| Elementor → Global fonts | Primary = Manrope 800, Secondary = Manrope 700, Text = Inter 400, Accent = Inter 600 |
| Elementor → Performance | Optimised DOM, improved asset loading, inline font icons on |

## 4. Components
| Component | Status | Notes |
|---|---|---|
| Package group tabs | **Built** (`seo-booster-core`) | WAI-ARIA tabs with arrow/Home/End keys and deep links (`#sbp-1-tab-1`) |
| Package card | **Built** | Name, ideal-for line, price (from WooCommerce), delivery, revisions, deliverables, collapsible exclusions, CTA |
| Featured card | **Built** | Ink border plus a lime "Most popular" badge, set by the `_sb_featured` meta |
| Quote card | **Built** | Shows "Priced per publisher" and a "Get a quote" button linking to `/get-a-quote/?package=SKU` |
| Mobile package row | **Built** | Below 600 px the cards become a horizontal swipe row (86% width, scroll-snap, next card peeks). No page-level horizontal overflow |
| Empty state | **Built** | Shown when a service has no published packages: message plus a proposal CTA |
| Brief form, brief banner, admin brief panel | **Built** | Uses WooCommerce account form styles |
| Header, mega-menu, footer | Phase 04 | WoodMart header builder |
| Hero, service tiles, process steps, FAQ accordion, CTA band, breadcrumbs, blog cards, trust panel | Phase 04 | Elementor templates saved as global widgets |

## 5. Evidence
Screenshots come from the static preview `docs/package-preview.html`, which uses the plugin's real CSS and JS and the same markup the shortcode outputs. They are in `docs/screens/`:
- `cards-1440.png`: four columns, two featured tiers
- `cards-premium-1440.png`: Premium Links tab after the ArrowRight key (`aria-selected=true`, panel 0 hidden)
- `cards-768.png`: tablet layout
- `cards-360.png`: mobile swipe row

Automated checks run with Playwright on the preview: no horizontal overflow at 360, 768 or 1440 px, and keyboard tab switching passed.

**Not yet verified:** rendering inside WoodMart and Elementor on the live site. Theme CSS can override some styles. This gets re-checked once the plugin is installed.

## 6. Page wireframes (structure for Phase 04)
**Home**
1. Header
2. Hero (H1, value proposition, CTA "Explore packages", secondary CTA "Get a proposal")
3. Service family tiles (4)
4. Problem → process → outcome strip
5. Featured packages (`[sb_packages service="off-page-seo" group="profiles-and-citations"]`)
6. Why us (transparent scope, manual work, reporting)
7. How it works (4 steps: choose, pay, brief, delivery)
8. FAQ
9. Final CTA
10. Footer

**Service page (Off-Page SEO)**
1. Breadcrumb
2. Hero (problem, offer, CTAs)
3. Who it's for / not for
4. `[sb_packages service="off-page-seo"]`
5. What's in a citation vs a profile link (comparison table)
6. Process
7. What we need from you
8. Sample report (labelled illustration)
9. FAQ
10. Related services
11. Proposal CTA

**Service hub:** hero, then category groups with service cards, then a CTA.

**Package detail (product):** title, price and CTA, deliverables, exclusions, requirements, turnaround, related packages, FAQ.

**Cart / Checkout:** WooCommerce blocks, no shipping, terms checkbox, then the "next step: your brief" note.

**About / Contact:** verified facts only; the CF7 form with consent.
