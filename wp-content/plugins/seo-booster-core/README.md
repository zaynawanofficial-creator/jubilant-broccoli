# SEO Booster Core (WordPress plugin)

This plugin turns WooCommerce products into **service packages**. It adds package groups (shown as tabs), package cards, a post-purchase project brief, and service order statuses. It works with any theme and is designed to run alongside WoodMart and Elementor.

## Install
1. Run `tools/build-plugin-zip.sh` from the repo root. It creates `dist/seo-booster-core.zip`.
2. In wp-admin, go to Plugins → Add New → Upload Plugin, choose the zip, then click Activate. WooCommerce must already be active.
3. Go to Settings → Permalinks → Save once. This registers the `/my-account/sb-brief/` endpoint.

## Load the catalogue
Go to **Tools → SEO Booster catalog**. Run it once as a dry run, then untick "Dry run" and run it again. The importer reads `data/SERVICE_CATALOG.csv`:
- Products are matched by SKU (`package_code`), so re-running updates them rather than creating duplicates.
- A **fixed-price** row is published only if it has a price, both approvals are `YES`, and `publish` is `READY`.
- A **quote** row is published when scope is approved and `publish` is `QUOTE`. It shows a "Get a quote" button instead of Add to cart.
- Every other row is imported as a **draft**.

The group intro text, deliverables, exclusions and requirements come from `data/group-content.php`. You can edit them per product afterwards.

## Show packages on a page
Add a Shortcode widget in Elementor:
```
[sb_packages service="off-page-seo"]                         ← all groups as tabs
[sb_packages service="off-page-seo" group="premium-links"]   ← one group only
```
`service` is the product category slug and `group` is the package-group slug. Prices are always read live from WooCommerce, so changing a price in wp-admin updates every card immediately.

## Edit a package
Go to Products → (package). Change the price in **Product data**. Everything else (deliverables, turnaround, approvals and so on) is in the **Service package** box.

There is a publishing gate: a fixed-price package stays a draft until it has a price above zero and both "Price approved" and "Scope approved" are ticked.

## Order workflow
| Step | Status | What happens |
|---|---|---|
| 1 | Payment received | Status becomes **Paid – awaiting brief**. Service orders never jump to Completed automatically. |
| 2 | Brief reminders | Sent at 24 h and 72 h if the brief is still incomplete. Uses Action Scheduler. |
| 3 | Customer submits brief | Status becomes **Brief received**. The admin gets an email. |
| 4 | Admin starts work | Admin sets **In progress**. This is the renamed Processing status. |
| 5 | Ready for review | Order action "Service: move to Client review" emails the customer. |
| 6 | Delivered | Order action "Service: mark Delivered" emails the customer. Admin then sets Completed. |

- All of these service statuses are registered as **paid**, so revenue reports and refunds behave normally.
- The brief is stored on the order. It shows in the order screen's "Project brief" box and the "Brief" column of the orders list.
- Uploaded brief files go to `uploads/sb-briefs/{order}/`. Direct access to that folder is blocked. Files can only be downloaded through a nonce-checked link by the customer or a shop manager.

## Recommended WooCommerce settings
- **Accounts & Privacy:** turn off guest checkout and turn on "create account during checkout". The brief form needs an account.
- **Tax:** set this up after the owner's tax advice is in. See RISKS.md B5.
- **Payments:** BACS, Stripe (test mode) and PayPal Payments (sandbox) until live payments are approved.
