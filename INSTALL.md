# INSTALL — put the SEO Booster site live on seobooster.uk

These steps install two files: the **theme** (design and pages) and the **plugin** (packages, checkout workflow, forms and SEO). Allow about 10 minutes.

## 0. Backup
Take a backup first: Hostinger hPanel → Websites → seobooster.uk → Backups → **Create backup**. Every step below can be undone, but a backup makes rollback a one-click job.

## 1. Update the plugin (0.2.0)
Plugins → Add New → Upload Plugin → `seo-booster-core.zip` → **Replace current with uploaded**.

## 2. Re-run the catalogue import
Tools → **SEO Booster catalog** → untick "Dry run" → **Run import**.
- Every product page gets a full description: what's included, what isn't, requirements and delivery.
- Category parents are fixed.
- Re-running updates existing products, so you won't get duplicates.

## 3. Install and activate the theme
Appearance → Themes → Add New → Upload Theme → `seo-booster-theme.zip` → **Activate**.

WoodMart stays installed but inactive. To switch back, reactivate WoodMart.

## 4. Build the site (one click)
Appearance → **SEO Booster Setup** → leave all boxes ticked except "Overwrite" → **Build the site**.

This creates:
- **Pages:** Home, Services and 7 service pages, Packages, How it works, About, Contact, Get a quote, FAQ and Insights
- **Policy drafts:** Terms, Refunds, Privacy, Cookies and Accessibility
- **Articles:** 3 Insights articles
- **Branding:** the logo and site icon

It also:
- sets Home as the front page
- moves the old WoodMart demo pages to **Draft** (they are not deleted)
- makes WooCommerce require an account at checkout, so customers can fill in their brief

## 5. Check
1. Settings → Permalinks → **Save**. This refreshes the URLs.
2. **LiteSpeed Cache → Toolbox → Purge All.**
3. Open the site in a private window and check:
   - [ ] Home, `/services/off-page-seo/` and `/packages/` show package cards with prices.
   - [ ] The menu works on a phone.
   - [ ] The Contact form sends: the message appears in wp-admin → **Leads** and arrives at the admin email.
   - [ ] **Test order:** WooCommerce → Settings → Payments → enable **Direct bank transfer**. Add the $5 package to the cart, check out, then mark the order as Processing in wp-admin. It should move to **Paid – awaiting brief**, and My Account → order should show **Complete your brief**.

## Editing later
- **Page text and images:** Pages → edit with the block editor. Everything is ordinary blocks.
- **Header, footer and colours:** Appearance → **Editor**.
- **Prices and package details:** Products → (package). Cards update everywhere automatically.
- **Leads:** wp-admin → Leads.

## Before launch (owner)
- Policy pages are labelled "Draft under review". Have them reviewed, add company details, then remove the yellow notice block.
- Connect Stripe (test mode) and PayPal (sandbox), run test payments, then switch to live.
- Make sure the `hello@seobooster.uk` mailbox exists, or change the email in the footer, the Contact page and the policies.
