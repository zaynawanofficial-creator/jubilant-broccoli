# DATA_MODEL — service packages, briefs, orders

Everything below lives in native WooCommerce and WordPress storage. Meta keys are prefixed `_sb_`. Order data is written only through the `WC_Order` CRUD methods, which keeps it compatible with HPOS.

## 1. Taxonomies
| Taxonomy | Object | Purpose | Example terms |
|---|---|---|---|
| `product_cat` (Woo core) | product | Service, nested under a category family | `seo` › `off-page-seo`, `web` › `website-development` |
| `sb_package_group` (custom, hierarchical) | product | A package group within one service, rendered as the tabs | `off-page-seo-profiles-citations`, `off-page-seo-guest-posts` |

Term meta on `sb_package_group`: `_sb_group_label`, `_sb_group_intro`, `_sb_group_sort`.

## 2. Package = WooCommerce product
- **Type:** `simple` by default. Use `variable` only when the scope differs along one axis (for example, page count with an identical deliverable spec).
- **Virtual:** yes. **Downloadable:** no.
- **Price fields:** native `_regular_price` and `_sale_price` are the only source of price. Nothing is hardcoded.
- **SKU:** `package_code` from `SERVICE_CATALOG.csv` (stable ID).

| Meta key | Type | Brief §5 field | Notes |
|---|---|---|---|
| `_sb_pricing_model` | enum `fixed\|range\|quote\|subscription` | pricing_model | `quote` hides add-to-cart and routes to `/get-a-quote/?package=SKU` |
| `_sb_billing_period` | enum `one-off\|month` | billing_period | `month` is quote-only until a subscriptions licence is approved |
| `_sb_quantity` | int | quantity | |
| `_sb_unit` | string | quantity_unit | submissions, placements, pages, words, graphics |
| `_sb_deliverables` | list (one item per line) | deliverables | rendered as a ✓ list |
| `_sb_exclusions` | list | exclusions | rendered as a "Not included" list |
| `_sb_turnaround` | string | turnaround_range | e.g. "7–10 working days" |
| `_sb_revisions` | string | revisions | |
| `_sb_requirements` | list | requirements | shown before purchase, and drives the brief fields |
| `_sb_brief_profile` | enum `offpage\|web\|content\|design\|seo\|generic` | — | selects the brief form |
| `_sb_ideal_for` | string | — | one-line ideal customer |
| `_sb_addons` | list of product IDs | optional_addons | add-ons are separate virtual products, so nothing is forced |
| `_sb_related` | list of product IDs | related_offer_ids | |
| `_sb_terms_version` | string | terms_version | snapshotted onto the order line |
| `_sb_price_approved` | bool | approved | |
| `_sb_scope_approved` | bool | approved | |
| `_sb_sort` | int | sort_order | |

`service_category`, `service_slug` and `group_slug` are derived from the taxonomies. `currency` is the store currency (USD). `visibility` is the native catalog visibility. `product_id` is the native ID.

### Publishing gate (enforced in the plugin)
A product can move to `publish` only when both `_sb_price_approved` and `_sb_scope_approved` are true, **or** when `_sb_pricing_model = quote`. If neither holds, the save is forced back to `draft` and an admin notice is shown. The catalog importer always creates `draft` products.

## 3. Order data
### At checkout (minimal)
Order meta: `_sb_primary_url` (required for offpage/seo/web profiles) and `_sb_terms_accepted_version`.

### Order line item meta (snapshot at purchase)
Fields: `_sb_package_sku`, `_sb_group`, `_sb_quantity`, `_sb_unit`, `_sb_turnaround`, `_sb_revisions`, `_sb_terms_version`, `_sb_brief_profile`.

This keeps the order an accurate record even if the product changes later.

### Brief (post-payment, per order)
| Key | Content |
|---|---|
| `_sb_brief_status` | `pending\|partial\|complete` |
| `_sb_brief_data` | JSON keyed by line-item ID → field → value (sanitised per field type) |
| `_sb_brief_files` | list of attachment IDs in the protected upload dir |
| `_sb_brief_submitted_at` | ISO datetime |
| `_sb_brief_reminders` | count + last sent |

### Brief profiles (conditional fields)
| Profile | Fields |
|---|---|
| `offpage` | target URLs (1–N), anchor/keyword themes, business name/address/phone (NAP, for citations), niche, geography, existing profiles to avoid |
| `web` | page list, features, reference sites, content readiness, platform/hosting, access method (delegated invite only) |
| `content` | topic(s), audience, word count (pre-filled from line), tone, keywords, sources to cite, AI-use preference |
| `design` | formats/sizes, brand assets upload, references, copy, deadline |
| `seo` | site URL, GSC/GA access via user invite, priority pages, competitors |
| `generic` | free-text goals + files |

**Hard rule:** no field accepts passwords. Access to client systems is handled only through delegated invites, which the help text explains.

### Uploads
- Location: `wp-content/uploads/sb-briefs/{order_id}/`. The directory gets a deny-all `.htaccess` and files are served through a capability-checked handler.
- Allowed types: pdf, png, jpg, webp, svg (sanitised), docx, xlsx, zip.
- Limits: ≤ 20 MB per file, ≤ 10 files per order.

## 4. Order statuses (service lifecycle)
| Woo status | Label | Paid? | Entered when |
|---|---|---|---|
| `pending` | Awaiting payment | no | core |
| `on-hold` | Awaiting bank transfer | no | BACS (core) |
| `wc-sb-awaiting-brief` | Paid – awaiting brief | **yes** (`is_paid`) | payment complete and brief not complete |
| `wc-sb-brief-received` | Brief received | yes | brief submitted |
| `processing` | In progress | yes | admin starts work |
| `wc-sb-client-review` | Client review | yes | admin uploads deliverable for review |
| `wc-sb-delivered` | Delivered | yes | final delivery sent |
| `completed` | Completed | yes | admin or auto after N days post-delivery |
| `refunded` / `cancelled` / `failed` | core | — | core |

- Custom statuses are added to `wc_order_is_paid_statuses` so reports and payment semantics stay correct.
- `woocommerce_payment_complete_order_status` returns `sb-awaiting-brief` for orders containing SB packages, so service orders never jump to `completed`.

## 5. Catalog source
`SERVICE_CATALOG.csv` is the seed. A WP-CLI command, `wp sb import-catalog SERVICE_CATALOG.csv`, upserts products by SKU and keeps rows with `publish=DRAFT` as drafts. The CSV holds no prices (`TBD`), so imported products stay draft until the owner fills in and approves the prices.
