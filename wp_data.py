#!/usr/bin/env python3
"""
Builds wordpress/data/site.json (+ media) for the RankRight Site plugin importer.

    python3 wp_data.py

Page sections are rendered with the same components as build.py, then adapted for WordPress:
asset paths -> {{ASSETS}}, absolute site URL -> {{HOME}}, pricing grids -> [rrm_pricing] (live WooCommerce
products), contact form -> [rrm_contact_form]. Bump nothing by hand: the version is a content hash.
"""
import copy
import glob
import hashlib
import html
import json
import os
import re
import shutil

import build as B
import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "wordpress", "data")
MEDIA = os.path.join(DATA, "media")
S = C.SITE
LABEL = {"seo": "SEO", "link-building": "Link Building", "website-development": "Website Development",
         "content-writing": "Content Writing", "ppc": "PPC Management", "social-media-marketing": "Social Media Marketing"}
MENU_NAME = {"ppc": "PPC (Pay-Per-Click)", "seo": "SEO", "social-media-marketing": "Social Media Marketing"}
SLUG_FIX = {"/faqs/": "/faq/", "/refund-policy/": "/refund-returns/"}
REDIRECTS = {"website-development-2": "/website-development/", "faqs": "/faq/", "refund-policy": "/refund-returns/",
             "about": "/about-us/", "contact": "/contact-us/", "shop": "/shop/", "ppc": "/ppc-pay-per-click/",
             "pay-per-click": "/ppc-pay-per-click/", "seo": "/search-engine-optimization/", "link-building": "/link-building-services/"}
AUDIENCE = {
    "seo": ["Local businesses and start-ups targeting a handful of core keywords", "Growing SMEs ready to compete for 20+ keywords",
            "Competitive and multi-location brands", "Large sites targeting national visibility", "Online stores with 70+ product pages",
            "International, enterprise or complex SEO projects"],
    "link-building": ["Testing link building on a small budget", "New sites building their first niche-relevant links",
                      "Sites ready for guest posts and a diverse link profile", "Established sites that need premium guest posts",
                      "Competitive niches that need DA 40+ authority", "Brands chasing top positions in tough niches"],
    "website-development": ["Sole traders and new businesses that need a simple, professional site", "Service businesses that need 5–7 SEO-ready pages",
                            "Brands that want a fully custom, content-rich website", "Shops launching their first online store",
                            "Retailers with larger catalogues and custom needs", "Complex builds, integrations and custom functionality"],
    "content-writing": ["A single page, blog post or product page", "Two pages with proper keyword targeting", "Rewriting your core website pages",
                        "A full website rewrite with competitor research", "Ecommerce stores that need product and category copy",
                        "Ongoing content programmes and blogs"],
    "ppc": ["Advertisers who want to find and fix wasted spend", "Businesses launching their first Google Ads campaign",
            "Brands combining Google search with Meta ads", "Multi-channel advertisers ready for retargeting",
            "Online stores focused on Shopping campaigns and ROAS", "High-spend, multi-market advertisers"],
    "social-media-marketing": ["Small brands focusing on one platform", "Businesses active on Facebook and Instagram",
                               "B2B and B2C brands adding LinkedIn", "Brands growing across four platforms",
                               "Brands adding TikTok to the mix", "Large brands that need always-on social"],
}
DEFAULT_DELIVERY = {"seo": "Ongoing — monthly", "ppc": "Ongoing — monthly", "social-media-marketing": "Ongoing — monthly",
                    "website-development": "Agreed at kick-off", "content-writing": "Agreed at kick-off", "link-building": "7–12 days"}

captured = {}


def fix_html(h):
    h = h.replace('"/assets/', '"{{ASSETS}}/').replace("url(\"/assets/", "url(\"{{ASSETS}}/")
    for a, b in SLUG_FIX.items():
        h = h.replace(a, b)
    return h


def fix_schema(nodes):
    txt = json.dumps(nodes, ensure_ascii=False)
    txt = txt.replace(B.DOMAIN, "{{HOME}}")
    for a, b in SLUG_FIX.items():
        txt = txt.replace(a, b)
    return json.loads(txt)


def fake_render(path, *, title, description, body, schema=None, **kw):
    captured[path] = {"title": title, "description": description, "body": body, "schema": schema or []}


def pricing_wp(key, svc):
    pk = svc["packages"]
    return f"""<section class="section" id="pricing" aria-labelledby="pricing-h"><div class="container">
<div class="section-head center"><span class="eyebrow">Pricing</span><h2 id="pricing-h">{html.escape(pk['heading'])}</h2>
<p class="lead">Fixed prices, every deliverable listed. Hit <strong>Order now</strong>, share a 2-minute brief and check out securely — or <a href="/contact-us/?package={key}#enquiry">get a free recommendation</a>.</p></div>
[rrm_pricing service="{key}"]
</div></section>"""


def product_name(key, p):
    lab = LABEL[key]
    if lab.split()[0].lower() in p["name"].lower():
        return f"{p['name']} Package"
    return f"{p['name']} — {lab} Package"


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("—", " ")).strip("-")


def price_phrase(p, unit):
    if p is None:
        return "custom-priced"
    return f"{B.money(p)} {'per month' if unit == '/month' else 'one-off'}"


SUFFIX = {"seo": "", "link-building": " Link Building", "website-development": " Website", "content-writing": " Content Writing",
          "ppc": "", "social-media-marketing": " Social Media"}


def product_title(key, p, unit):
    base = p["name"] + ("" if SUFFIX[key].strip().split(" ")[0].lower() in p["name"].lower() else SUFFIX[key])
    if p["price"] is None:
        return f"{base} Package – Custom Quote | RankRight Media"
    price = B.money(p["price"]) + ("/mo" if unit == "/month" else "")
    for tail in (" | Order Online", " | RankRight", ""):
        t = f"{base} Package – {price}{tail}"
        if len(t) <= 60:
            return t
    return t


def product_desc(p, unit):
    price = ("Custom pricing" if p["price"] is None else
             f"Just {B.money(p['price'])}{'/month' if unit == '/month' else ''}")
    end = (" Request your quote today." if p["price"] is None else " 2-minute brief, secure checkout — start today.")
    feats = [("up to" + f[5:]) if f.startswith("Up to") else f for f in p["features"] if not f.lower().startswith("delivery")]
    for n in (3, 2, 1):
        d = f"{p['tagline']}: {', '.join(feats[:n])}. {price}.{end}"
        if len(d) <= 158:
            return d
    return d[:157] + "…"


def products():
    out = []
    for key in C.SERVICE_ORDER:
        svc = C.SERVICES[key]
        items = svc["packages"]["items"]
        for i, p in enumerate(items):
            unit = p.get("unit", svc["packages"]["unit"])
            name = product_name(key, p)
            feats = p["features"]
            delivery = next((f.split(":", 1)[-1].replace("Delivery in", "").strip() for f in feats if f.lower().startswith("delivery")), DEFAULT_DELIVERY[key])
            pp = price_phrase(p["price"], unit)
            nxt = items[i + 1] if i + 1 < len(items) else None
            audience = AUDIENCE[key][i]
            flist = ", ".join(f.lower() if not f[:2].isupper() else f for f in feats[:-1]) + " and " + feats[-1].lower()
            buy = ("Request a quote and we’ll reply within one working day with a tailored proposal, timeline and fixed price."
                   if p["price"] is None else
                   "Check out securely, then complete a short brief about your business, goals and preferences. Our team starts work straight away and keeps you updated until every deliverable is complete.")
            desc = f"""<h2>What’s included in the {html.escape(p['name'])} package?</h2>
<p>The <strong>{html.escape(name)}</strong> is a {pp} {html.escape(svc['service_type'].lower())} package from RankRight Media — {html.escape(p['tagline'][0].lower() + p['tagline'][1:])}. It includes {html.escape(flist)}.</p>
<h2>Who is this package for?</h2>
<p>{html.escape(audience)}.{(' Need more? Compare it with the ' + html.escape(nxt['name']) + ' package below.') if nxt else ''}</p>
<h2>What you’ll receive</h2>
<ul>{''.join('<li>' + html.escape(f) + '</li>' for f in feats)}</ul>
<h2>How ordering works</h2>
<p>{buy}</p>
<p>Prefer to talk it through first? Call <a href="tel:{S['phone_e164']}">{S['phone_display']}</a> or <a href="/contact-us/?package={p['id']}#enquiry">send us a question</a>.</p>"""
            short = f"{p['tagline']}. {feats[0]}, {feats[1][0].lower() + feats[1][1:]} and more — {pp}."
            rm_title = f"{p['name']} {LABEL[key] if LABEL[key].split()[0].lower() not in p['name'].lower() else ''} Package – {B.money(p['price']) if p['price'] is not None else 'Custom Quote'}".replace("  ", " ")
            out.append({
                "sku": p["id"], "name": name, "slug": slugify(name), "short": p["name"], "tagline": p["tagline"],
                "price": p["price"], "unit": unit if p["price"] is not None else "", "features": feats,
                "featured": bool(p.get("featured")), "order": i, "service": key, "delivery": delivery, "tier": i + 1,
                "audience": audience, "short_desc": short, "description": desc, "image": f"products/{p['id']}.webp",
                "cat_slug": svc["slug"].replace("-services", "") + "-packages", "cat_name": f"{LABEL[key]} Packages",
                "cat_desc": svc["description"], "cat_image": f"services/{key}.webp",
                "rm_title": product_title(key, p, unit),
                "rm_desc": product_desc(p, unit),
                "rm_focus": f"{p['name'].lower()} {LABEL[key].lower()} package" if LABEL[key].split()[0].lower() not in p["name"].lower() else f"{p['name'].lower()} package",
            })
    return out


def service_schema(key, prods):
    svc = C.SERVICES[key]
    offers = []
    for p in prods:
        if p["service"] != key:
            continue
        o = {"@type": "Offer", "name": p["name"], "url": "{{HOME}}/package/" + p["slug"] + "/", "availability": "https://schema.org/InStock",
             "seller": {"@id": "{{HOME}}/#organization"}, "description": "; ".join(p["features"])}
        if p["price"] is not None:
            o["price"] = f"{p['price']:.2f}"
            o["priceCurrency"] = "USD"
        offers.append(o)
    priced = [p["price"] for p in prods if p["service"] == key and p["price"] is not None]
    return {"@type": "Service", "@id": "{{HOME}}/" + svc["slug"] + "/#service", "name": svc["name"], "serviceType": svc["service_type"],
            "description": svc["description"], "url": "{{HOME}}/" + svc["slug"] + "/", "provider": {"@id": "{{HOME}}/#organization"},
            "areaServed": [{"@type": "Country", "name": "United Kingdom"}, {"@type": "Place", "name": "Worldwide"}],
            "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": f"{min(priced):.2f}", "highPrice": f"{max(priced):.2f}", "offerCount": len(offers)},
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": svc["packages"]["heading"], "itemListElement": offers}}


LEGAL_PAGES = {
    "privacy-policy": ("Privacy Policy", "How RankRight Media Ltd collects, uses and protects your personal data under the UK GDPR, and how to exercise your data protection rights.", """
<p><strong>Effective Date:</strong> 10 April 2025</p>
<p>RankRight Media Ltd (“we,” “us,” or “our”) is committed to protecting your privacy. This Privacy Policy outlines how we collect, use, and safeguard your personal information when you visit our website.</p>
<h2>1. Information We Collect</h2><p>We may collect and process the following data:</p>
<ul><li><strong>Personal Identification Information:</strong> Name, email address, phone number, etc.</li><li><strong>Technical Data:</strong> IP address, browser type, operating system, etc.</li><li><strong>Usage Data:</strong> Information on how you use our website.</li><li><strong>Marketing and Communications Data:</strong> Your preferences in receiving marketing from us.</li></ul>
<h2>2. How We Use Your Information</h2><p>We use your information to:</p><ul><li>Provide and manage our services.</li><li>Improve our website and services.</li><li>Communicate with you, including sending promotional materials.</li><li>Comply with legal obligations.</li></ul>
<h2>3. Sharing Your Information</h2><p>We do not sell your personal data. We may share your information with:</p><ul><li><strong>Service Providers:</strong> Who assist in operating our website and conducting our business (for example, hosting, email and payment providers).</li><li><strong>Legal Obligations:</strong> When required by law or to protect our rights.</li></ul>
<h2>4. Data Security</h2><p>We implement appropriate security measures to protect your personal data. However, no method of transmission over the Internet is 100% secure.</p>
<h2>5. Your Data Protection Rights</h2><p>Under the UK GDPR, you have rights including:</p><ul><li>Access to your personal data.</li><li>Correction of inaccurate data.</li><li>Erasure of your data.</li><li>Objection to processing.</li><li>Data portability.</li></ul><p>To exercise these rights, contact us at <a href="mailto:support@rankrightmedia.uk">support@rankrightmedia.uk</a>. You also have the right to complain to the Information Commissioner’s Office (ico.org.uk).</p>
<h2>6. Cookies</h2><p>Our website uses essential cookies to run the shopping cart and checkout, and may use analytics cookies to improve user experience. You can set your browser to refuse cookies.</p>
<h2>7. Changes to This Policy</h2><p>We may update this Privacy Policy periodically. Changes will be posted on this page with an updated revision date.</p>
<h2>8. Contact Us</h2><p>For questions about this Privacy Policy, contact us at:</p><ul><li><strong>Email:</strong> <a href="mailto:support@rankrightmedia.uk">support@rankrightmedia.uk</a></li><li><strong>Phone:</strong> <a href="tel:+447446254421">+44 7446 254421</a></li><li><strong>Address:</strong> 68 Trelawney Road, Ilford, England, IG6 2NJ</li></ul>"""),
    "refund-returns": ("Refund Policy", "RankRight Media Ltd refund policy: when refunds apply, non-refundable services and how to request a refund for our digital marketing services.", """
<p><strong>Effective Date:</strong> 10 April 2025</p>
<h2>1. Overview</h2><p>At RankRight Media Ltd, we strive to provide high-quality digital marketing services. If you are not satisfied with our services, please review our refund policy below.</p>
<h2>2. Eligibility for Refunds</h2><p>Refunds may be considered under the following conditions:</p><ul><li>The service delivered does not match the agreed-upon specifications.</li><li>A written request for a refund is submitted within 14 days of service delivery.</li></ul>
<h2>3. Non-Refundable Services</h2><p>The following services are non-refundable:</p><ul><li>Services that have been fully rendered.</li><li>Third-party costs incurred on your behalf.</li></ul>
<h2>4. Process for Requesting a Refund</h2><p>To request a refund:</p><ol><li>Contact us at <a href="mailto:support@rankrightmedia.uk">support@rankrightmedia.uk</a> with your service details.</li><li>Provide a detailed explanation of your concerns.</li><li>Allow us 7 business days to review your request.</li></ol>
<h2>5. Contact Information</h2><p>For any questions or concerns regarding our Refund Policy, please contact us at:</p><ul><li><strong>Email:</strong> <a href="mailto:support@rankrightmedia.uk">support@rankrightmedia.uk</a></li><li><strong>Phone:</strong> <a href="tel:+447446254421">+44 7446 254421</a></li><li><strong>Address:</strong> 68 Trelawney Road, Ilford, England, IG6 2NJ</li></ul>"""),
    "terms-and-conditions": ("Terms & Conditions", "The terms and conditions that govern your use of the RankRight Media website and the digital marketing services provided by RankRight Media Ltd.", """
<p><strong>Effective Date:</strong> 10 April 2025</p>
<h2>1. Introduction</h2><p>These Terms &amp; Conditions govern your use of our website and our services. By accessing our website, you agree to these terms.</p>
<h2>2. Services</h2><p>RankRight Media Ltd provides digital marketing services, including SEO, link building, content writing, PPC advertising, social media management, website development, local SEO, and social media ads.</p>
<h2>3. User Obligations</h2><p>You agree to:</p><ul><li>Provide accurate information.</li><li>Use our services lawfully.</li><li>Not infringe on our intellectual property rights.</li></ul>
<h2>4. Payment Terms</h2><p>Package prices are shown on our website and payable at checkout. Any other payment terms will be outlined in individual service agreements. Late payments may incur interest charges.</p>
<h2>5. Limitation of Liability</h2><p>We are not liable for any indirect or consequential losses arising from the use of our services.</p>
<h2>6. Termination</h2><p>We reserve the right to terminate services if these terms are violated.</p>
<h2>7. Governing Law</h2><p>These terms are governed by the laws of England and Wales.</p>
<h2>8. Contact Us</h2><p>For questions about these Terms &amp; Conditions, contact us at:</p><ul><li><strong>Email:</strong> <a href="mailto:support@rankrightmedia.uk">support@rankrightmedia.uk</a></li><li><strong>Phone:</strong> <a href="tel:+447446254421">+44 7446 254421</a></li><li><strong>Address:</strong> 68 Trelawney Road, Ilford, England, IG6 2NJ</li></ul>"""),
}


def contact_body():
    a = S["address"]
    maps = "https://www.google.com/maps/search/?api=1&query=" + "68+Trelawney+Road+Ilford+IG6+2NJ"
    i = B.icon
    return f"""
<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div><div class="container rel narrow center">
<nav aria-label="Breadcrumb"><ol class="crumbs crumbs-center"><li><a href="/">Home</a></li><li aria-current="page">Contact Us</li></ol></nav>
<span class="eyebrow">Contact us</span><h1>Contact RankRight Media</h1>
<p class="lead">Start the conversation to establish a great relationship and grow your business. We reply within one working day.</p></div></section>
<section class="section" id="enquiry"><div class="container split split-60">
<div>[rrm_contact_form]</div>
<aside class="contact-side reveal d1">
  <span class="eyebrow">Get in touch</span><h2 class="h3">Seamless Communication, Global Impact.</h2>
  <p>Have a question or ready to grow your business with digital marketing? We’re here to help! Whether you need SEO, content writing, PPC, or social media management — just drop us a message.</p>
  <div class="contact-cards">
    <a href="tel:{S['phone_e164']}"><span class="ico">{i('i-phone')}</span><span><b>Let’s talk</b><span>{S['phone_display']}</span></span></a>
    <a href="mailto:{S['email']}"><span class="ico">{i('i-mail')}</span><span><b>Email support</b><span>{S['email']}</span></span></a>
    <a href="{maps}" target="_blank" rel="noopener"><span class="ico">{i('i-pin')}</span><span><b>Head office</b><span>{a['street']}, {a['locality']}, {a['region']}, {a['postcode']}</span></span></a>
    <div><span class="ico">{i('i-clock')}</span><span><b>Working hours</b><span>Monday – Friday · UK &amp; international clients</span></span></div>
  </div>
</aside></div></section>
{B.faq_section(C.GENERAL_FAQS[:4], heading="Before you get in touch")}"""


def main():
    os.makedirs(MEDIA, exist_ok=True)
    B.render = fake_render
    B.pricing_section = pricing_wp
    B.WARNINGS.clear()
    B.page_home()
    for k in C.SERVICE_ORDER:
        B.page_service(k)
    B.page_about()
    home_faqs = C.HOME_FAQS
    C.HOME_FAQS = C.GENERAL_FAQS + [f for f in home_faqs if f[0] not in ("Do you work with small businesses?",)]
    B.page_faqs()
    C.HOME_FAQS = home_faqs
    prods = products()

    page_meta = {
        "/": ("home", "Home", "RankRight Media"),
        "/about-us/": ("about-us", "About Us", None),
        "/faqs/": ("faq", "FAQ", None),
    }
    for k in C.SERVICE_ORDER:
        page_meta[B.svc_url(k)] = (C.SERVICES[k]["slug"], C.SERVICES[k]["name"], None)

    pages = []
    for path, cap in captured.items():
        slug, title, _ = page_meta[path]
        body = fix_html(cap["body"])
        schema = fix_schema(cap["schema"])
        if slug in [C.SERVICES[k]["slug"] for k in C.SERVICE_ORDER]:
            key = [k for k in C.SERVICE_ORDER if C.SERVICES[k]["slug"] == slug][0]
            schema = [n for n in schema if n.get("@type") != "Service"] + [service_schema(key, prods)]
        pages.append({"slug": slug, "title": title, "content": "<!-- wp:html -->\n" + body + "\n<!-- /wp:html -->", "raw": True,
                      "schema": schema, "rm_title": cap["title"], "rm_desc": cap["description"],
                      "rm_focus": {"home": "digital marketing agency", "about-us": "rankright media"}.get(slug, C.SERVICES.get(next((k for k in C.SERVICE_ORDER if C.SERVICES[k]['slug'] == slug), ''), {}).get('service_type', 'digital marketing').lower() + " services")})
    # FAQ page: add the WordPress FAQ questions to the general group
    for p in pages:
        if p["slug"] == "faq":
            p["rm_title"] = "FAQ | SEO, Web, PPC & Social Media Questions | RankRight Media"
    pages.append({"slug": "contact-us", "title": "Contact Us", "raw": True, "content": "<!-- wp:html -->\n" + fix_html(contact_body()) + "\n<!-- /wp:html -->",
                  "schema": fix_schema([B.faq_node("/contact-us/", C.GENERAL_FAQS[:4])]), "rm_title": "Contact RankRight Media | Get a Free Quote",
                  "rm_desc": "Contact RankRight Media for SEO, link building, websites, content, PPC and social media. Call +44 7446 254421 or email support@rankrightmedia.uk.", "rm_focus": "contact rankright media"})
    pages.append({"slug": "blog", "title": "Blog", "content": "", "raw": False, "rm_title": "Digital Marketing Blog: SEO, PPC & Web Guides | RankRight Media",
                  "rm_desc": "Practical guides on SEO, link building, website development, content writing, PPC and social media marketing from the RankRight Media team.", "rm_focus": "digital marketing blog"})
    pages.append({"slug": "thank-you", "title": "Thank You", "raw": True, "noindex": True, "content": "<!-- wp:html -->\n" + fix_html(
        f"""<section class="section nf"><div class="container narrow center"><span class="ico ico-solid">{B.icon('i-check')}</span><h1>Thank you — we’ve got your message</h1>
<p class="lead">A member of our team will reply within one working day. Need us sooner? Call <a href="tel:{S['phone_e164']}">{S['phone_display']}</a>.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Back to home</a><a class="btn btn-ghost" href="/blog/">Read our guides</a></div></div></section>""") + "\n<!-- /wp:html -->",
                  "rm_title": "Thank You | RankRight Media", "rm_desc": "Thanks for contacting RankRight Media. Our team will reply within one working day."})
    for slug, (title, desc, body) in LEGAL_PAGES.items():
        pages.append({"slug": slug, "title": title, "content": body.strip(), "raw": False, "rm_title": f"{title} | RankRight Media", "rm_desc": desc,
                      "hero": {"eyebrow": "Legal", "sub": "RankRight Media Ltd · 68 Trelawney Road, Ilford, England, IG6 2NJ"}})

    # CTR-focused titles & descriptions (titles <= 60 chars, descriptions <= 158)
    META = {
        "home": ("SEO, Web Design & PPC Agency | RankRight Media (UK)",
                 "Grow faster with fixed-price SEO from $299/mo, websites from $199 and content from $49. 1K+ projects, 500+ clients. Get your free quote today."),
        "search-engine-optimization": ("SEO Services That Drive Leads | Plans from $299/mo",
                 "Rank higher with white-hat SEO: keyword research, technical fixes, content and links. 6 fixed-price plans from $299/month with monthly reports."),
        "link-building-services": ("Link Building Services | Manual Backlinks from $3.49",
                 "Niche-relevant dofollow backlinks via 100% manual outreach on DA 10–50+ sites. Live-URL reports, delivery in 3–12 days. Order in 2 minutes."),
        "website-development": ("Website Development Services | Sites from $199",
                 "Fast, mobile-first websites and online stores on WordPress, WooCommerce or Shopify that rank and convert. Fixed prices from $199. Live in days."),
        "content-writing": ("SEO Content Writing Services | Pages from $49",
                 "Human-written, SEO-optimised web pages, blogs and product descriptions that rank and convert. Packages from $49, delivered in 3–7 days."),
        "ppc-pay-per-click": ("PPC Management Services | Google & Meta Ads from $249",
                 "Profitable Google, Meta and TikTok ad campaigns with proper conversion tracking. Management from $249/month or a $99 PPC audit to cut wasted spend."),
        "social-media-marketing": ("Social Media Marketing Services | Plans from $199/mo",
                 "Done-for-you social media: posts, campaigns, targeting and community management on Instagram, Facebook, LinkedIn and TikTok. From $199/month."),
        "about-us": ("About RankRight Media | Founder-Led Digital Agency",
                 "Meet the founder-led team behind RankRight Media: 10+ years in SEO, web and eCommerce, 1K+ projects and 500+ happy clients across the UK and beyond."),
        "contact-us": ("Contact RankRight Media | Free Quote in 1 Working Day",
                 "Talk to us about SEO, websites, content, PPC or social media. Call +44 7446 254421 or send a message — we reply within one working day."),
        "faq": ("Digital Marketing FAQs: Prices, Timelines & Process",
                "Straight answers on SEO, link building, web design, content, PPC and social media: what it costs, how long it takes and how ordering works."),
        "blog": ("Digital Marketing Blog: SEO, PPC & Web Design Guides",
                 "Practical, no-fluff guides on SEO costs, local SEO, link building, website pricing, content, Google Ads and AI search from the RankRight team."),
        "privacy-policy": ("Privacy Policy | RankRight Media Ltd", "How RankRight Media Ltd collects, uses and protects your personal data under the UK GDPR, and how to exercise your data protection rights."),
        "refund-returns": ("Refund Policy | RankRight Media Ltd", "When refunds apply to RankRight Media services, which services are non-refundable, and how to request a refund within 14 days of delivery."),
        "terms-and-conditions": ("Terms & Conditions | RankRight Media Ltd", "The terms that govern use of the RankRight Media website and the SEO, web, content, PPC and social media services provided by RankRight Media Ltd."),
    }
    for p in pages:
        if p["slug"] in META:
            p["rm_title"], p["rm_desc"] = META[p["slug"]]
        if p["slug"] == "home":
            feat = """<section class="section spot" id="packages" aria-labelledby="pk-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">Popular packages</span><h2 id="pk-h">Start Today With a Fixed-Price Package</h2>
<p class="lead">No proposals, no waiting. Pick a package, share a 2-minute brief and our team starts work. <a href="/shop/">Compare all 36 packages →</a></p></div>
[rrm_featured_packages]</div></section>
"""
            marker = '<section class="section-tight"><div class="container"><div class="magic'
            assert marker in p["content"]
            p["content"] = p["content"].replace(marker, feat + marker, 1)
    pages.append({"slug": "order", "title": "Order", "raw": True, "noindex": True, "content": "<!-- wp:shortcode -->\n[rrm_order_form]\n<!-- /wp:shortcode -->",
                  "rm_title": "Complete Your Order | RankRight Media", "rm_desc": "Share a quick project brief and continue to secure checkout."})
    for p in pages:
        assert len(p["rm_title"]) <= 65, (p["slug"], len(p["rm_title"]))

    # Service data used by product pages, header/footer, llms.txt
    services = {}
    for k in C.SERVICE_ORDER:
        s = C.SERVICES[k]
        services[k] = {"slug": s["slug"], "name": s["name"], "short_name": s["short_name"], "menu_name": MENU_NAME.get(k, s["short_name"]),
                       "icon": s["icon"], "menu_blurb": s["menu_blurb"], "card": s["card"], "description": s["description"],
                       "service_type": s["service_type"], "heading": s["packages"]["heading"], "note": s["packages"]["note"],
                       "cat_slug": s["slug"].replace("-services", "") + "-packages", "process": [list(x) for x in s["process"]],
                       "faqs": [[q, fix_html(a)] for q, a in s["faqs"]],
                       "testimonials_html": fix_html(B.testimonials_section(s["testimonials"]))}

    partials = {"cta": fix_html(B.cta_band()), "stats": fix_html(B.stats_band())}

    # Media manifest
    media = []
    for f in sorted(glob.glob(os.path.join(MEDIA, "**", "*.webp"), recursive=True)):
        rel = os.path.relpath(f, MEDIA).replace(os.sep, "/")
        base = os.path.splitext(os.path.basename(rel))[0]
        title = base.replace("-", " ").title()
        alt = title
        prod = next((p for p in prods if p["image"] == rel), None)
        if prod:
            title, alt = prod["name"], f"{prod['name']} — RankRight Media {LABEL[prod['service']]} package illustration"
        if rel.startswith("services/"):
            k = base
            title = alt = f"{LABEL.get(k, k)} services by RankRight Media"
        media.append({"file": rel, "title": title, "alt": alt})

    posts = load_posts()
    for p in posts:
        mp = next((m for m in media if m["file"] == p["image"]), None)
        if mp:
            mp["title"], mp["alt"] = p["title"], p["image_alt"]

    data = {
        "settings": {"name": S["name"], "legal_name": S["legal_name"], "tagline": "SEO, Websites, Content & Ads That Grow Your Business",
                     "phone_display": S["phone_display"], "phone_e164": S["phone_e164"], "email": S["email"], "address": S["address"],
                     "currency_code": "USD", "indexable": False,
                     "llms_summary": "RankRight Media Ltd is a UK-based digital marketing agency (Ilford, England) serving clients in the UK and worldwide. It sells fixed-price packages for SEO, link building, website development, SEO content writing, PPC management and social media marketing, with clear deliverables and reporting."},
        "service_order": C.SERVICE_ORDER, "services": services, "pages": pages, "products": prods, "posts": posts,
        "media": media, "media_reset": "2", "importer_rev": 4, "partials": partials, "redirects": REDIRECTS,
        "author": {"name": "Zain Ul Abdeen", "first": "Zain", "last": "Ul Abdeen", "bio": C.TEAM[0]["bio"]},
    }
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True)
    mh = hashlib.sha1("".join(open(f, "rb").read().hex()[:64] + f for f in sorted(glob.glob(os.path.join(MEDIA, "**", "*.webp"), recursive=True))).encode()).hexdigest()
    data["version"] = hashlib.sha1((blob + mh).encode()).hexdigest()[:12]
    with open(os.path.join(DATA, "site.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"site.json v{data['version']}: {len(pages)} pages, {len(prods)} products, {len(posts)} posts, {len(media)} media")


def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "wordpress", "content", "posts", "*.html"))):
        raw = open(f, encoding="utf-8").read()
        meta_txt, body = raw.split("-->", 1)
        meta = json.loads(meta_txt.replace("<!--", "", 1))
        meta["content"] = body.strip()
        meta["image"] = f"blog/{meta['slug']}.webp"
        posts.append(meta)
    return posts


if __name__ == "__main__":
    main()
