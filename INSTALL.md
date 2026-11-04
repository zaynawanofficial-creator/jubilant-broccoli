# INSTALL — put the SEO Booster site live on seobooster.uk

## Updating to theme 1.3.0 + plugin 0.5.0 (4 Nov 2026)
1. **Backup** in Hostinger.
2. **Plugin:** upload `seo-booster-core.zip` → **Replace current with uploaded**.
3. **Import:** Tools → **SEO Booster catalog** → untick Dry run. Tick **Refresh package images** to get the new visuals. Click **Run import**. This adds 13 new services with 53 packages, plus the Canva Brand Kit package; 116 packages in total.
4. **Theme:** upload `seo-booster-theme.zip` → **Replace current with uploaded**.
5. Appearance → **SEO Booster Setup** → tick **Overwrite** → **Build the site**. This creates the 13 new service pages, rebuilds the existing pages, updates the 3 existing articles and adds 4 new ones with covers.
6. **Clear every cache:** LiteSpeed Cache → Toolbox → **Purge All**. Also purge **CSS/JS optimised files** and **UCSS** if those are enabled. On your phone, clear the browser cache or test in a private tab.
   - Your phone screenshots showed an old stylesheet on product, cart and checkout pages. The theme now versions its CSS by file date and inlines the critical mobile-header rules, but purging is still needed once.
7. **If the header or footer doesn't change:** Appearance → Editor → Patterns → Template parts → Header/Footer → ⋮ → **Reset**.


## Updating to theme 1.2.0 + plugin 0.4.0 (3 Nov 2026)
1. **Backup** in Hostinger.
2. **Plugin:** upload `seo-booster-core.zip` → **Replace current with uploaded**. Brings the compact package picker and SEO title tags.
3. **Theme:** upload `seo-booster-theme.zip` → **Replace current with uploaded**. Brings the new footer, mobile header, legal pages, blog hero and illustrations.
4. Appearance → **SEO Booster Setup** → tick **Overwrite** → **Build the site**. This rebuilds the pages with the new copy and legal layout, adds cover images to the 3 articles and drafts the "Hello world!" post.
5. **If the header or footer doesn't change:** they were probably edited in the Site Editor, and a saved copy overrides the theme file. Go to Appearance → Editor → Patterns → Template parts → Header/Footer → ⋮ → **Reset**.
6. LiteSpeed Cache → **Purge All**, then check on a phone: logo, cart and menu icon only; the menu starts with Home.


## Updating to theme 1.1.0 + plugin 0.3.0 (3 Nov 2026)
1. **Backup** in Hostinger.
2. **Plugin:** Plugins → Add New → Upload → `seo-booster-core.zip` → **Replace current with uploaded**.
3. **Import:** Tools → **SEO Booster catalog** → untick Dry run → **Run import**. This:
   - adds the new packages, so every group now has at least 4
   - attaches a package image to every product that doesn't have one yet
   - switches maintenance packages to the new "Fix" project-details form
4. **Theme:** Appearance → Themes → Add New → Upload → `seo-booster-theme.zip` → **Replace current with uploaded**.
5. **Rebuild the pages with the new design:** Appearance → **SEO Booster Setup**:
   - tick **Overwrite**
   - if you want test orders to work right away, also tick **Enable Direct bank transfer**
   - click **Build the site**
6. **Clear the cache:** LiteSpeed Cache → **Purge All**.
7. **Test the new flow in a private window:**
   - [ ] Services → Off-Page SEO → **Choose package**. The service details page opens with the project-details form.
   - [ ] Fill in the form → **Continue to checkout**. The branded checkout opens with your details listed under the package.
   - [ ] Place the order with bank transfer → the thank-you page shows the next steps.
   - [ ] In wp-admin, open the order: the **Project brief** box is already filled in.

Earlier first-time install steps follow.

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
