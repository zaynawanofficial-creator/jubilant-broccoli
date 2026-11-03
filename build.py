#!/usr/bin/env python3
"""
RankRight Media static site builder — Python 3 standard library only.

    python3 build.py            # builds ./public
    python3 build.py --check    # builds, then fails on broken links / SEO issues

Output in ./public is plain HTML/CSS/JS: upload it to any static host (Hostinger, Cloudflare Pages, Netlify).
"""
import datetime as _dt
import hashlib
import html
import json
import os
import re
import shutil
import sys
from html.parser import HTMLParser

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
S = C.SITE
DOMAIN = S["domain"].rstrip("/")
TODAY = _dt.date.today().isoformat()
YEAR = _dt.date.today().year
WARNINGS = []
PAGES = []  # (path, robots_index, priority)

esc = lambda s: html.escape(str(s), quote=True)


def asset_ver(rel):
    with open(os.path.join(SRC, "assets", rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="/assets/img/icons.svg#{name}"></use></svg>'


def money(p):
    if p is None:
        return "Custom"
    s = f"{p:,.2f}" if isinstance(p, float) and not float(p).is_integer() else f"{int(p):,}"
    return S["currency_symbol"] + s


def svc_url(key):
    return f"/{C.SERVICES[key]['slug']}/"


def abs_url(path):
    return DOMAIN + path


# ------------------------------------------------------------------------------------------------
# Schema helpers
# ------------------------------------------------------------------------------------------------
ORG_ID = DOMAIN + "/#organization"
SITE_ID = DOMAIN + "/#website"


def org_node():
    n = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": S["name"],
        "legalName": S["legal_name"],
        "url": DOMAIN + "/",
        "logo": {"@type": "ImageObject", "url": abs_url("/assets/img/logo-rankright-media.png"), "width": 464, "height": 146},
        "image": abs_url("/assets/img/og-default.png"),
        "description": S["tagline"],
        "telephone": S["phone_e164"],
        "areaServed": [{"@type": "Country", "name": c} for c in S["area_served"]],
        "priceRange": S["currency_symbol"] + "–" + S["currency_symbol"] * 3,
        "currenciesAccepted": S["currency_code"],
        "knowsAbout": ["Search engine optimisation", "Local SEO", "Technical SEO", "Link building", "Website development",
                       "SEO content writing", "Pay-per-click advertising", "Google Ads", "Social media marketing"],
        "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support", "telephone": S["phone_e164"],
                          "areaServed": "GB", "availableLanguage": ["English"]}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Digital marketing services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@id": abs_url(svc_url(k)) + "#service"}} for k in C.SERVICE_ORDER]},
    }
    if S["email"]:
        n["email"] = S["email"]
        n["contactPoint"][0]["email"] = S["email"]
    if S["address"]:
        a = S["address"]
        n["address"] = {"@type": "PostalAddress", "streetAddress": a.get("street", ""), "addressLocality": a.get("locality", ""),
                        "postalCode": a.get("postcode", ""), "addressRegion": a.get("region", ""), "addressCountry": "GB"}
    if S["same_as"]:
        n["sameAs"] = S["same_as"]
    if S["founded"]:
        n["foundingDate"] = S["founded"]
    if S["company_number"]:
        n["identifier"] = {"@type": "PropertyValue", "propertyID": "Companies House", "value": S["company_number"]}
    if C.TEAM:
        n["employee"] = [{"@type": "Person", "name": m["name"], "jobTitle": m["role"],
                          **({"sameAs": [m["linkedin"]]} if m.get("linkedin") else {})} for m in C.TEAM]
    return n


def website_node():
    return {"@type": "WebSite", "@id": SITE_ID, "url": DOMAIN + "/", "name": S["name"], "inLanguage": "en-GB",
            "publisher": {"@id": ORG_ID}}


def breadcrumb_node(path, crumbs):
    return {"@type": "BreadcrumbList", "@id": abs_url(path) + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(u)} for i, (n, u) in enumerate(crumbs)]}


def faq_node(path, faqs):
    strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
    return {"@type": "FAQPage", "@id": abs_url(path) + "#faq",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}


def jsonld(nodes):
    data = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>"


# ------------------------------------------------------------------------------------------------
# Layout
# ------------------------------------------------------------------------------------------------
def header(active):
    items = "".join(
        f'<li><a href="{svc_url(k)}"><span class="mi">{icon(C.SERVICES[k]["icon"])}</span>'
        f'<span><strong>{esc(C.SERVICES[k]["short_name"] if k != "ppc" else "PPC (Pay-Per-Click)")}</strong>'
        f'<small>{esc(C.SERVICES[k]["menu_blurb"])}</small></span></a></li>' for k in C.SERVICE_ORDER)
    cur = lambda k: ' aria-current="page"' if active == k else ""
    svc_active = ' aria-current="true"' if active in C.SERVICES else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="/" aria-label="{esc(S['name'])} home"><img src="/assets/img/logo-rankright-media.webp" alt="{esc(S['name'])}" width="232" height="73"></a>
    <nav aria-label="Main">
      <ul class="nav-links" id="nav-links">
        <li><a href="/"{cur('home')}>Home</a></li>
        <li class="has-menu"><button type="button" aria-expanded="false" aria-controls="svc-menu"{svc_active}>Services {icon('i-chevron')}</button>
          <ul class="menu" id="svc-menu">{items}</ul></li>
        <li><a href="/about-us/"{cur('about')}>About Us</a></li>
        <li><a href="/faqs/"{cur('faqs')}>FAQs</a></li>
        <li><a href="/contact-us/"{cur('contact')}>Contact Us</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:{S['phone_e164']}">{icon('i-phone')}{esc(S['phone_display'])}</a>
      <a class="btn btn-primary btn-sm" href="/contact-us/">Get started {icon('i-arrow')}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">{icon('i-menu','i-open')}{icon('i-close','i-close')}</button>
    </div>
  </div>
</header>"""


def footer():
    svc = "".join(f'<li><a href="{svc_url(k)}">{esc(C.SERVICES[k]["name"])}</a></li>' for k in C.SERVICE_ORDER)
    email = f'<a href="mailto:{esc(S["email"])}">{icon("i-mail")}{esc(S["email"])}</a>' if S["email"] else ""
    reg = f' Registered in England &amp; Wales No. {esc(S["company_number"])}.' if S["company_number"] else ""
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/img/logo-rankright-media.webp" alt="{esc(S['name'])}" width="232" height="73" loading="lazy">
        <p>RankRight Media UK is your trusted digital partner, offering SEO, web development, content writing &amp; more — all under one roof.</p>
        <div class="foot-contact"><a href="tel:{S['phone_e164']}">{icon('i-phone')}{esc(S['phone_display'])}</a>{email}</div>
      </div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div><h2>Support</h2><ul><li><a href="/faqs/">FAQs</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/refund-policy/">Refund Policy</a></li><li><a href="/terms-and-conditions/">Terms &amp; Conditions</a></li></ul></div>
      <div><h2>Company</h2><ul><li><a href="/contact-us/">Contact us</a></li><li><a href="/about-us/">About us</a></li><li><a href="/llms.txt">AI summary (llms.txt)</a></li></ul></div>
    </div>
    <div class="foot-bottom"><p>Copyright © {YEAR} {esc(S['legal_name'])}. All rights reserved.{reg}</p><p>UK-based digital marketing agency</p></div>
  </div>
</footer>
<div class="mobile-cta"><a class="btn btn-ghost" href="tel:{S['phone_e164']}">{icon('i-phone')}Call</a><a class="btn btn-primary" href="/contact-us/">Get a quote</a></div>"""


def render(path, *, title, description, body, active="", schema=None, crumbs=None, robots="index", og_type="website",
           page_type="WebPage", priority="0.7", image="/assets/img/og-default.png"):
    if len(title) > 65:
        WARNINGS.append(f"{path}: title is {len(title)} chars (aim ≤ 60–65): {title}")
    if not 70 <= len(description) <= 165:
        WARNINGS.append(f"{path}: meta description is {len(description)} chars (aim 120–160)")
    url = abs_url(path)
    nodes = [org_node(), website_node()]
    wp = {"@type": page_type, "@id": url + "#webpage", "url": url, "name": title, "description": description,
          "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID}, "inLanguage": "en-GB", "dateModified": TODAY,
          "primaryImageOfPage": {"@type": "ImageObject", "url": abs_url(image)}}
    if crumbs:
        wp["breadcrumb"] = {"@id": url + "#breadcrumb"}
        nodes.append(breadcrumb_node(path, crumbs))
    nodes.insert(2, wp)
    nodes += schema or []
    robots_meta = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" if robots == "index" else "noindex, follow"
    css_v, js_v = asset_ver("css/main.css"), asset_ver("js/main.js")
    doc = f"""<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots_meta}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-GB" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#07010f">
<meta name="author" content="{esc(S['name'])}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(S['name'])}">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{abs_url(image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(S['name'])} — UK digital marketing agency">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{abs_url(image)}">
<link rel="preload" href="/assets/fonts/outfit-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css?v={css_v}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
{jsonld(nodes)}
<script src="/assets/js/main.js?v={js_v}" defer></script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    out = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    if path.endswith("/"):
        PAGES.append((path, robots == "index", priority))


# ------------------------------------------------------------------------------------------------
# Components
# ------------------------------------------------------------------------------------------------
def crumbs_html(crumbs):
    li = []
    for i, (n, u) in enumerate(crumbs):
        li.append(f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{esc(n)}</li>')
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{"".join(li)}</ol></nav>'


def stars(n=5):
    return '<span class="stars" aria-hidden="true">' + icon("i-star") * n + "</span>"


def stats_band():
    cells = []
    for s in C.STATS:
        v = s["value"]
        shown = (f"{v}" if isinstance(v, float) else f"{v}") + s["suffix"]
        cells.append(f'<div class="stat"><b data-count="{v}" data-suffix="{esc(s["suffix"])}">{esc(shown)}</b><span>{esc(s["label"])}</span></div>')
    return f'<section class="stats" aria-label="RankRight Media in numbers"><div class="container stats-grid">{"".join(cells)}</div></section>'


def testimonials_section(ids, eyebrow="Testimonials", heading="Client Feedback &amp; Reviews", anchor="reviews"):
    cards = []
    for i, tid in enumerate(ids):
        t = C.TESTIMONIALS[tid]
        if t["photo"]:
            av = f'<img src="/assets/img/{t["photo"]}" alt="{esc(t["name"])}" width="54" height="54" loading="lazy">'
        else:
            av = f'<span class="ini" aria-hidden="true">{esc("".join(w[0] for w in t["name"].split()[:2]))}</span>'
        cards.append(f"""<figure class="tcard reveal d{i % 3}">{icon('i-quote','q')}
<blockquote><p>“{esc(t['quote'])}”</p></blockquote>
<figcaption class="who">{av}<span><b>{esc(t['name'])}</b><span>{esc(t['context'])}</span></span></figcaption></figure>""")
    return f"""<section class="section" id="{anchor}" aria-labelledby="{anchor}-h"><div class="container">
<div class="section-head center"><span class="eyebrow">{eyebrow}</span><h2 id="{anchor}-h">{heading}</h2>
<p class="lead">Real words from businesses we’ve helped grow online.</p></div>
<div class="tgrid">{''.join(cards)}</div></div></section>"""


def faq_section(faqs, heading="Frequently Asked Questions", sub="", anchor="faq"):
    items = "".join(f"""<details{' open' if i == 0 else ''}><summary>{esc(q)}<span class="pm">{icon('i-chevron')}</span></summary><div class="a">{a}</div></details>""" for i, (q, a) in enumerate(faqs))
    subp = f'<p class="lead">{sub}</p>' if sub else ""
    return f"""<section class="section" id="{anchor}" aria-labelledby="{anchor}-h"><div class="container narrow">
<div class="section-head center"><span class="eyebrow">FAQ</span><h2 id="{anchor}-h">{heading}</h2>{subp}</div>
<div class="faq">{items}</div></div></section>"""


def steps_section(steps, heading, eyebrow="How it works", anchor="process"):
    li = "".join(f'<li class="step reveal d{i % 4}"><span class="ico">{icon(ic)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for i, (ic, t, d) in enumerate(steps))
    return f"""<section class="section spot" id="{anchor}" aria-labelledby="{anchor}-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">{eyebrow}</span><h2 id="{anchor}-h">{heading}</h2></div>
<ol class="steps" role="list">{li}</ol></div></section>"""


def cta_band(h="Ready to grow your business online?", p="Tell us about your goals and we’ll recommend the right package — no pressure, no jargon.", primary=("Get a free quote", "/contact-us/")):
    return f"""<section class="section-tight"><div class="container"><div class="cta reveal">
<h2>{h}</h2><p class="lead">{p}</p>
<div class="btn-row"><a class="btn btn-primary" href="{primary[1]}">{primary[0]} {icon('i-arrow')}</a>
<a class="btn btn-ghost" href="tel:{S['phone_e164']}">{icon('i-phone')}Call {esc(S['phone_display'])}</a></div></div></div></section>"""


def related_section(keys):
    li = "".join(f'<a href="{svc_url(k)}"><span class="ico">{icon(C.SERVICES[k]["icon"])}</span>{esc(C.SERVICES[k]["name"])}{icon("i-arrow","go")}</a>' for k in keys)
    return f"""<section class="section-tight" aria-labelledby="rel-h"><div class="container">
<div class="section-head"><span class="eyebrow">Keep exploring</span><h2 id="rel-h">Related services</h2></div>
<div class="related">{li}</div></div></section>"""


def visual(v):
    if v["kind"] == "dash":
        return f"""<div class="dash" role="img" aria-label="Illustration of an SEO dashboard with organic traffic trending upwards">
<span class="float-chip">{icon('i-trend')}{esc(v['chip'])}</span>
<div class="dash-top"><span class="dash-dots"><i></i><i></i><i></i></span><span class="dash-label">{esc(v['label'])}</span></div>
<div class="dash-chart"><div class="row"><span class="k">Organic clicks</span><span class="up">{icon('i-trend')}Trending up</span></div>
<svg class="line" viewBox="0 0 400 150" aria-hidden="true"><defs>
<linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#b57bff"/><stop offset=".6" stop-color="#ff7ac6"/><stop offset="1" stop-color="#ffb48c"/></linearGradient>
<linearGradient id="ag" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ff7ac6" stop-opacity=".35"/><stop offset="1" stop-color="#ff7ac6" stop-opacity="0"/></linearGradient></defs>
<g stroke="rgba(255,255,255,.07)"><path d="M0 30h400M0 70h400M0 110h400"/></g>
<path d="M0 132 C40 128 60 120 90 116 S140 112 170 96 S220 90 250 70 S300 58 330 38 S380 20 400 12 L400 150 L0 150Z" fill="url(#ag)"/>
<path class="draw" d="M0 132 C40 128 60 120 90 116 S140 112 170 96 S220 90 250 70 S300 58 330 38 S380 20 400 12" fill="none" stroke="url(#lg)" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="400" cy="12" r="5" fill="#ffb48c"/></svg></div>
<div class="dash-kpis"><div class="kpi"><span>Rankings</span><b>{icon('i-trend')}Top 10</b></div><div class="kpi"><span>Traffic</span><b>{icon('i-trend')}Growing</b></div><div class="kpi"><span>Leads</span><b>{icon('i-trend')}More</b></div></div>
<div class="serp"><span class="rank">#1</span><small><i></i>yourbusiness.co.uk</small><strong>Your Business — Trusted Local Experts</strong><p>Found first by customers searching for what you sell.</p></div>
</div>"""
    if v["kind"] == "kpis":
        k = "".join(f'<div class="kpi"><span>{esc(a)}</span><b>{icon("i-trend")}{esc(b)}</b></div>' for a, b in v["kpis"])
        return f"""<div class="dash" role="img" aria-label="Illustration of a PPC campaign dashboard">
<span class="float-chip">{icon('i-target')}{esc(v['chip'])}</span>
<div class="dash-top"><span class="dash-dots"><i></i><i></i><i></i></span><span class="dash-label">{esc(v['label'])}</span></div>
<div class="dash-chart"><div class="row"><span class="k">Conversions</span><span class="up">{icon('i-trend')}Optimising weekly</span></div>
<svg class="line" viewBox="0 0 400 150" aria-hidden="true"><defs><linearGradient id="bg1" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ff7ac6"/><stop offset="1" stop-color="#b57bff"/></linearGradient></defs>
<g fill="url(#bg1)"><rect x="12" y="104" width="34" height="46" rx="6"/><rect x="62" y="92" width="34" height="58" rx="6"/><rect x="112" y="96" width="34" height="54" rx="6"/><rect x="162" y="76" width="34" height="74" rx="6"/><rect x="212" y="64" width="34" height="86" rx="6"/><rect x="262" y="52" width="34" height="98" rx="6"/><rect x="312" y="34" width="34" height="116" rx="6"/><rect x="362" y="18" width="34" height="132" rx="6"/></g></svg></div>
<div class="dash-kpis">{k}</div></div>"""
    bars = "".join(f'<div class="bar"><div class="lbl"><span>{esc(l)}</span></div><div class="track"><div class="fill {w}"></div></div></div>' for l, w in v["bars"])
    return f"""<div class="dash" role="img" aria-label="Illustration: {esc(v['label'])}">
<span class="float-chip">{icon('i-sparkle')}{esc(v['chip'])}</span>
<div class="dash-top"><span class="dash-dots"><i></i><i></i><i></i></span><span class="dash-label">{esc(v['label'])}</span></div>
<div class="dash-chart"><div class="bars">{bars}</div></div></div>"""


def pricing_section(key, svc):
    pk = svc["packages"]
    unit = pk["unit"]
    cards, rows = [], []
    for i, p in enumerate(pk["items"]):
        feat = " featured" if p.get("featured") else ""
        rib = '<span class="ribbon">Recommended</span>' if p.get("featured") else ""
        unit_html = f"<span>{esc(unit)}</span>" if p["price"] is not None else "<span>quote</span>"
        lis = "".join(f"<li>{icon('i-check')}{esc(f)}</li>" for f in p["features"])
        label = "Buy now" if p["price"] is not None else "Request a quote"
        cards.append(f"""<article class="price reveal d{i % 3}{feat}" aria-labelledby="{p['id']}-h">{rib}
<span class="ico ico-solid">{icon('i-card')}</span><h3 id="{p['id']}-h">{esc(p['name'])}</h3><p class="tagline">{esc(p['tagline'])}</p>
<p class="amount"><b>{money(p['price'])}</b>{unit_html}</p><ul>{lis}</ul>
<a class="btn {'btn-primary' if feat else 'btn-ghost'} btn-block" href="/contact-us/?package={p['id']}#enquiry">{label} {icon('i-arrow')}</a></article>""")
        rows.append(f"<tr><th scope=\"row\">{esc(p['name'])}</th><td>{money(p['price'])}{'' if p['price'] is None else ' ' + esc(unit)}</td><td>{esc('; '.join(p['features']))}</td></tr>")
    return f"""<section class="section" id="pricing" aria-labelledby="pricing-h"><div class="container">
<div class="section-head center"><span class="eyebrow">Pricing</span><h2 id="pricing-h">{esc(pk['heading'])}</h2>
<p class="lead">Clear, fixed prices with every deliverable listed — so you know exactly what you’re getting.</p></div>
<div class="pricing">{''.join(cards)}</div><p class="price-note">{esc(pk['note'])} Prices shown in {esc(S['currency_code'])}.</p>
<details class="compare"><summary>Compare all {esc(svc['short_name'])} packages side by side{icon('i-chevron')}</summary>
<div class="table-wrap"><table><caption class="sr-only">{esc(pk['heading'])} compared</caption><thead><tr><th scope="col">Package</th><th scope="col">Price</th><th scope="col">What’s included</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>
</div></section>"""


def service_schema(key, svc, path):
    n = {"@type": "Service", "@id": abs_url(path) + "#service", "name": svc["name"], "serviceType": svc["service_type"],
         "description": svc["description"], "url": abs_url(path), "provider": {"@id": ORG_ID},
         "areaServed": [{"@type": "Country", "name": c} for c in S["area_served"]]}
    if svc["packages"]:
        offers = []
        for p in svc["packages"]["items"]:
            o = {"@type": "Offer", "name": p["name"], "description": "; ".join(p["features"]),
                 "url": abs_url(f"/contact-us/?package={p['id']}"), "availability": "https://schema.org/InStock", "seller": {"@id": ORG_ID}}
            if p["price"] is not None:
                o["price"] = f"{p['price']:.2f}"
                o["priceCurrency"] = S["currency_code"]
                if svc["packages"]["unit"] == "/month":
                    o["priceSpecification"] = {"@type": "UnitPriceSpecification", "price": f"{p['price']:.2f}", "priceCurrency": S["currency_code"],
                                               "unitText": "MONTH", "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MON"}}
            offers.append(o)
        n["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": svc["packages"]["heading"], "itemListElement": offers}
        priced = [p["price"] for p in svc["packages"]["items"] if p["price"] is not None]
        n["offers"] = {"@type": "AggregateOffer", "lowPrice": f"{min(priced):.2f}", "highPrice": f"{max(priced):.2f}",
                       "priceCurrency": S["currency_code"], "offerCount": len(svc["packages"]["items"])}
    return n


# ------------------------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------------------------
def page_service(key):
    svc = C.SERVICES[key]
    path = svc_url(key)
    crumbs = [("Home", "/"), ("Services", "/#services"), (svc["short_name"] if key != "ppc" else "PPC", path)]
    side = "".join(f'<li><a href="{a}">{icon(ic)}{esc(t)}</a></li>' for ic, t, a in svc["features"])
    checks = "".join(f"<li>{icon('i-check')}{esc(c)}</li>" for c in svc["checklist"])
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in svc["facts"])
    pkg = svc["packages"]
    if pkg:
        hero_cta = f'<a class="btn btn-primary" href="#pricing">View packages {icon("i-arrow")}</a>'
        pricing = pricing_section(key, svc)
    else:
        hero_cta = f'<a class="btn btn-primary" href="/contact-us/?package={key}#enquiry">Get a free quote {icon("i-arrow")}</a>'
        pricing = f"""<section class="section-tight" id="pricing" aria-labelledby="pricing-h"><div class="container"><div class="cta reveal">
<span class="eyebrow">Pricing</span><h2 id="pricing-h">A fixed quote, tailored to your project</h2>
<p class="lead">Every {esc(svc['short_name'].lower())} project is different, so we quote after a free 20-minute discovery call. You’ll get an itemised proposal with clear deliverables and timelines — no hidden costs.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact-us/?package={key}#enquiry">Request your quote {icon('i-arrow')}</a><a class="btn btn-ghost" href="tel:{S['phone_e164']}">{icon('i-phone')}{esc(S['phone_display'])}</a></div></div></div></section>"""
        WARNINGS.append(f"{path}: no packages/prices in content.py (copy them from the live WP page if it has any)")
    panel = svc["panel"]
    ticks = ""
    if panel.get("ticks"):
        ticks = '<ul class="ticks">' + "".join(f"<li>{icon('i-check')}<span><strong>{esc(a)}</strong><br>{esc(b)}</span></li>" for a, b in panel["ticks"]) + "</ul>"
    includes = "".join(f"""<article class="card card-flex svc-card reveal d{i % 3}"><span class="ico">{icon(ic)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p>
<a class="text-link" href="/contact-us/?package={key}#enquiry">{esc(svc['includes_cta'])} {icon('i-arrow')}</a></article>""" for i, (ic, t, d) in enumerate(svc["includes"]))
    body = f"""
<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div>
<div class="container rel hero-grid">
  <div>{crumbs_html(crumbs)}
    <span class="eyebrow">{esc(svc['eyebrow'])}</span>
    <h1>{esc(svc['h1'])}</h1>
    <p class="lead">{esc(svc['lead'])}</p>
    <div class="btn-row">{hero_cta}<a class="btn btn-ghost" href="/contact-us/">Talk to an expert</a></div>
    <p class="updated">{icon('i-clock')}Last updated <time datetime="{TODAY}">{_dt.date.today().strftime('%-d %B %Y')}</time></p>
  </div>
  <div class="hero-visual">{visual(svc['visual'])}</div>
</div></section>

<section class="section"><div class="container split split-60">
  <div class="prose reveal">{svc['intro']}
    <ul class="check-cols">{checks}</ul>
    <aside class="facts" aria-labelledby="facts-h"><h2 id="facts-h">{icon('i-clipboard')}Key facts</h2><dl>{facts}</dl></aside>
  </div>
  <aside class="sidebar" aria-label="{esc(svc['short_name'])} features">
    <div class="side-card"><h2>Features</h2><ul class="side-list">{side}</ul></div>
    <div class="side-card side-cta"><h2>Free consultation</h2><p>Not sure which plan is right? We’ll review your website and recommend the best fit.</p><a class="btn btn-dark btn-block" href="/contact-us/?package={key}#enquiry">Book a call {icon('i-arrow')}</a></div>
  </aside>
</div></section>

{pricing}
{steps_section(svc['process'], esc(svc['process_heading']))}

<section class="panel-photo" id="{panel.get('anchor','potential')}"><div class="bgimg"><img src="/assets/img/{panel['img']}" alt="{esc(panel['alt'])}" width="945" height="700" loading="lazy"></div>
<div class="container"><div class="glass reveal"><h2>{esc(panel['h2'])}</h2>{panel['body']}{ticks}
<a class="btn btn-primary" href="/contact-us/?package={key}#enquiry">Get started {icon('i-arrow')}</a></div></div></section>

<section class="section spot" id="includes" aria-labelledby="inc-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">Why choose us</span><h2 id="inc-h">{esc(svc['includes_heading'])}</h2></div>
<div class="grid-3">{includes}</div></div></section>

{stats_band()}
{testimonials_section(svc['testimonials'])}
{faq_section(svc['faqs'], heading=f"{esc(svc['short_name'])} questions, answered")}
{related_section(svc['related'])}
{cta_band()}
"""
    schema = [service_schema(key, svc, path), faq_node(path, svc["faqs"])]
    render(path, title=svc["title"], description=svc["description"], body=body, active=key, schema=schema, crumbs=crumbs, priority="0.9")


def page_home():
    path = "/"
    svc_cards = "".join(f"""<article class="card card-flex svc-card reveal d{i % 3}"><span class="ico">{icon(C.SERVICES[k]['icon'])}</span>
<h3><a class="card-link" href="{svc_url(k)}">{esc(C.SERVICES[k]['name'])}</a></h3><p>{esc(C.SERVICES[k]['card'])}</p>
<ul>{''.join(f"<li>{icon('i-check')}{esc(x)}</li>" for x in C.SERVICES[k]['card_points'])}</ul>
<span class="text-link">Learn more {icon('i-arrow')}</span></article>""" for i, k in enumerate(C.SERVICE_ORDER))
    caps = "".join(f'<li><a href="{svc_url(k)}">{esc(C.SERVICES[k]["short_name"])}{icon("i-arrow")}</a></li>' for k in ["seo", "website-development", "content-writing", "social-media-marketing"])
    projects = []
    for i, p in enumerate(C.PROJECTS):
        media = (f'<div class="proj-media"><img src="/assets/img/{p["img"]}" alt="{esc(p["name"])} — {esc(p["tag"])} project" width="502" height="415" loading="lazy"></div>'
                 if p["img"] else f'<div class="proj-media art art-{p["art"]}" aria-hidden="true">{icon(p["icon"])}</div>')
        projects.append(f"""<article class="proj reveal d{i % 3}"><div class="proj-head"><span class="tag">{esc(p['tag'])}</span><h3>{esc(p['name'])}</h3></div>{media}
<dl><div><dt>Client</dt><dd>{esc(p['client'])}</dd></div><div><dt>Date</dt><dd>{esc(p['date'])}</dd></div><div><dt>Location</dt><dd>{esc(p['location'])}</dd></div><div><dt>Budget</dt><dd>{esc(p['budget'])}</dd></div></dl></article>""")
    tools = ["Google Search Console", "Google Analytics 4", "Google Ads", "Google Business Profile", "Ahrefs", "Semrush", "Meta Ads", "WordPress", "Shopify", "TikTok Ads"]
    tool_li = "".join(f"<li>{icon('i-check')}{esc(t)}</li>" for t in tools)
    stamp = """<svg viewBox="0 0 132 132" aria-hidden="true"><defs><path id="circ" d="M66 66 m-48 0 a48 48 0 1 1 96 0 a48 48 0 1 1 -96 0"/></defs>
<text font-family="Outfit, sans-serif" font-size="11.5" font-weight="700" fill="#16051f"><textPath href="#circ" textLength="298" lengthAdjust="spacing">PREMIUM SERVICES &amp; SUPPORT • PREMIUM SERVICES &amp; SUPPORT • </textPath></text></svg>"""
    item_list = {"@type": "ItemList", "@id": DOMAIN + "/#services", "name": "RankRight Media services",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url(svc_url(k)), "name": C.SERVICES[k]["name"]} for i, k in enumerate(C.SERVICE_ORDER)]}
    hc = C.STATS[1]
    body = f"""
<section class="hero"><div class="aurora"></div><div class="gridlines"></div>
<div class="container rel hero-grid">
  <div>
    <span class="pill"><span class="dot"></span>Welcome to RankRight Media</span>
    <h1>Grow Your Business with <span class="grad-text">SEO, Websites &amp; Ads</span> That Convert</h1>
    <p class="lead">Looking for a trusted team to grow your business online? At RankRight Media, we turn your digital dreams into real results. Whether you’re just starting out or want to take your business to the next level, our UK-based experts are here to help.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/contact-us/">Get started {icon('i-arrow')}</a><a class="btn btn-ghost" href="/search-engine-optimization/#pricing">View SEO packages</a></div>
    <ul class="trust-row">
      <li>{stars()}<span><strong>{esc(S['rating_display'])}/5</strong> client rating</span></li>
      <li>{icon('i-shield')}White-hat, Google-safe</li>
      <li>{icon('i-pin')}UK-based support</li>
    </ul>
  </div>
  <div class="hero-visual">{visual({'kind': 'dash', 'label': 'Your growth dashboard', 'chip': 'Page 1 on Google'})}</div>
</div></section>

<section class="section-tight"><div class="container"><div class="tools reveal"><div class="aurora"></div>
<h2 class="rel">Trusted by UK businesses. Powered by the tools the pros use.</h2>
<ul class="tool-list rel" aria-label="Platforms and tools we work with">{tool_li}</ul></div></div></section>

<section class="section" id="about" aria-labelledby="who-h"><div class="container split">
  <div class="media-frame reveal"><img src="/assets/img/team-collaboration.webp" alt="RankRight Media team members reviewing a client strategy on a tablet" width="619" height="562" loading="lazy">
    <span class="stamp">{stamp}<span class="core">{icon('i-star')}</span></span>
    <span class="exp-badge"><b>{hc['value']}{esc(hc['suffix'])}</b><span>happy clients<br>across the UK</span></span></div>
  <div class="reveal d1"><span class="eyebrow">Who we are</span><h2 id="who-h">Your Digital Future, Our Expertise</h2>
    <p>RankRight Media is a UK-based digital marketing agency built with a passion for helping businesses grow online. Our mission is simple: to provide honest, effective, and smart marketing solutions that get real results. We understand that every business is different, which is why we create custom strategies tailored to your goals. From small startups to growing brands, we work with clients who want to grow fast and smart — without all the confusion.</p>
    <p>Our team includes SEO specialists, content writers, ad experts, and web developers, all working together to deliver high-quality work that speaks for itself.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/about-us/">More about us {icon('i-arrow')}</a><a class="btn btn-ghost" href="/contact-us/">Contact us</a></div></div>
</div></section>

<section class="section-tight"><div class="container vvm">
  <div class="value-card reveal"><span class="eyebrow">Our value</span><h2>Smart Designs, Sharp Results</h2>
    <p>At RankRight Media, we believe in values that matter. We focus on:</p>
    <ul class="value-list">
      <li>{icon('i-eye')}<span><strong>Transparency</strong> – We keep things clear, simple, and honest. No hidden costs or fake promises.</span></li>
      <li>{icon('i-sparkle')}<span><strong>Creativity</strong> – Our ideas are fresh, unique, and tailored to your brand.</span></li>
      <li>{icon('i-trend')}<span><strong>Results</strong> – We care about performance. Everything we do is backed by data and focused on growth.</span></li>
      <li>{icon('i-heart')}<span><strong>Support</strong> – We treat our clients like partners. You’re never alone — we’re here at every step.</span></li>
    </ul>
    <p>When you work with us, you get a team that truly cares about your success.</p>
    <a class="btn btn-primary" href="#services">Get service {icon('i-arrow')}</a></div>
  <div class="vvm-stack">
    <div class="tone tone-violet reveal d1"><span class="eyebrow">Our vision</span><h3>Elevate Your Digital Presence with RankRight Media Expertise.</h3>
      <p>Our vision is to become the go-to digital marketing agency for UK businesses who want to grow with confidence. We aim to make marketing simple, effective, and stress-free for all kinds of businesses — whether online or local. By staying updated with the latest trends and tools, we make sure your brand always stays ahead in the digital world.</p></div>
    <div class="tone tone-pink reveal d2"><span class="eyebrow">Our mission</span><h3>Unleash Your Potential in the Digital Realm with Us.</h3>
      <p>Our mission is to help businesses grow through powerful and affordable digital marketing services. We’re here to support you at every stage of your journey — whether it’s building your first website, running paid ads, or ranking on Google.</p></div>
  </div>
</div></section>

{stats_band()}

<section class="section spot" id="services" aria-labelledby="svc-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">What we offer</span><h2 id="svc-h">Expert Digital Marketing Services</h2>
<p class="lead">Everything you need to get found, look credible and convert — delivered by one accountable UK team.</p></div>
<div class="grid-3">{svc_cards}</div></div></section>

<section class="section-tight"><div class="container"><div class="magic reveal">
  <div class="magic-copy"><span class="eyebrow">Why it works</span><h2>Experience the Magic of RankRight Media</h2>
    <p>When your business is ready to grow, we’re ready to help. Let us handle the technical stuff — so you can focus on running your business. From the first consultation to the final results, we work with full dedication, honesty, and a touch of creativity. Your success is our priority.</p>
    <p><strong>Ready to get started?</strong> Reach out now and let’s discuss your project!</p>
    <ul class="cap-list" aria-label="Popular services">{caps}</ul></div>
  <div class="magic-media"><img src="/assets/img/strategy-session.webp" alt="RankRight Media strategist and client planning a digital marketing campaign" width="960" height="928" loading="lazy"></div>
</div></div></section>

{steps_section([('i-message', 'Choose a Package', 'Browse our pricing and select the package that best fits your needs. Each plan clearly explains what’s included, so you know exactly what you’re getting.'),
                ('i-card', 'Secure Checkout', 'Once you’ve selected a package, proceed to checkout and make your payment through our secure system. It’s fast, safe, and hassle-free.'),
                ('i-clipboard', 'Share Your Brief', 'After payment, you’ll be directed to a short form where you can share your business details, goals, and preferences. This helps us understand exactly what you need.'),
                ('i-rocket', 'We Start Working!', 'That’s it! Our team will begin working on your project right away. You’ll receive updates as we make progress and deliver results on time.')],
               'How to Get Started – Just 4 Easy Steps')}

<section class="section" aria-labelledby="grow-h"><div class="container">
  <div class="bento-head"><h2 id="grow-h">We Drive Digital Growth with RankRight Media</h2><p class="lead">From websites to complete digital strategies, RankRight Media is your partner in building a strong, lasting online presence.</p></div>
  <div class="bento">
    <div class="b b-comm reveal"><div class="mock" aria-hidden="true">
      <div class="msg"><i></i><span>This month: 12 pages optimised, 20 backlinks live, report attached.</span></div>
      <div class="msg me"><i></i><span>Brilliant — enquiries are up already!</span></div>
      <div class="msg"><i></i><span>Next: local SEO push for your service areas.</span></div></div>
      <h3>Clear Communication, Always</h3><p>At RankRight Media, we keep you in the loop — every step, every update. Your success is our shared mission.</p>
      <a class="text-link" href="/about-us/">Learn more {icon('i-arrow')}</a></div>
    <div class="b b-traffic reveal d1"><span class="ico">{icon('i-rocket')}</span><h3>Boost Traffic &amp; Sales</h3><p>We use result-driven strategies to increase your website traffic and convert visitors into loyal buyers.</p>
      <svg class="spark" viewBox="0 0 200 60" aria-hidden="true"><path d="M0 52 C30 50 40 44 60 40 S100 34 120 24 S170 10 200 4" fill="none" stroke="#ff7ac6" stroke-width="3" stroke-linecap="round"/></svg></div>
    <div class="b b-support reveal d2"><span class="ring">{icon('i-phone')}</span><h3>Premium Support</h3><a class="phone" href="tel:{S['phone_e164']}">{esc(S['phone_display'])}</a>
      <p>Get fast, priority assistance from our expert team whenever you need it. We’re here to solve your queries quickly and keep your projects running smoothly.</p>
      <a class="btn btn-dark btn-sm" href="tel:{S['phone_e164']}">Call now</a></div>
    <div class="b b-rating reveal"><div class="score"><b>{esc(S['rating_display'])}+</b>{stars()}</div><div><h3>Client Ratings</h3><p>With a {esc(S['rating_display'])}+ rating, our clients consistently applaud our reliability, creativity, and transparent approach.</p><a class="text-link" href="#reviews">Read client reviews {icon('i-arrow')}</a></div></div>
    <div class="b b-grow reveal d1"><h3>Designed to Grow With You</h3><p>Whether you’re just starting or scaling fast, our web solutions are responsive, flexible, and future-ready.</p>
      <a class="btn btn-dark btn-sm" href="/website-development/">Learn more {icon('i-arrow')}</a></div>
  </div>
</div></section>

<section class="section spot" id="work" aria-labelledby="work-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">Featured projects</span><h2 id="work-h">What We’ve Done for Our Clients</h2>
<p class="lead">A snapshot of recent projects across branding, SEO, content, PPC and web development.</p></div>
<div class="grid-3">{''.join(projects)}</div></div></section>

<section class="panel-photo" aria-labelledby="why-h"><div class="bgimg"><img src="/assets/img/outreach-team.webp" alt="RankRight Media team collaborating at their desks" width="945" height="992" loading="lazy"></div>
<div class="container"><div class="glass reveal"><span class="eyebrow">Why choose us</span><h2 id="why-h">Why Businesses Choose RankRight Media</h2>
<p>There are many agencies out there — but here’s why our clients choose us:</p>
<ul class="ticks">
<li>{icon('i-check')}<span><strong>Real Results</strong> – We focus on ROI, not just traffic.</span></li>
<li>{icon('i-check')}<span><strong>Clear Communication</strong> – No technical jargon — just simple updates.</span></li>
<li>{icon('i-check')}<span><strong>Affordable Plans</strong> – Flexible pricing that fits your budget.</span></li>
<li>{icon('i-check')}<span><strong>Dedicated Team</strong> – Experts who care about your business.</span></li>
<li>{icon('i-check')}<span><strong>UK-Based Support</strong> – Easy to reach, always available.</span></li></ul>
<p>Join the UK businesses who trust RankRight Media for their digital growth.</p>
<a class="btn btn-primary" href="/about-us/">Discover more {icon('i-arrow')}</a></div></div></section>

{testimonials_section(['thomas-graham', 'emma-clarke', 'sophie-bennett', 'daniel-reid', 'nathan-clarke', 'olivia-mason'])}
{faq_section(C.HOME_FAQS, heading="Questions businesses ask us", sub="Straight answers about our services, pricing and process.")}
{cta_band()}
"""
    render(path, title="RankRight Media | UK SEO & Digital Marketing Agency",
           description="UK digital marketing agency for SEO, link building, websites, content writing, PPC and social media. Clear packages, white-hat methods, monthly reports.",
           body=body, active="home", schema=[item_list, faq_node(path, C.HOME_FAQS)], priority="1.0")


def page_about():
    path = "/about-us/"
    crumbs = [("Home", "/"), ("About Us", path)]
    team_html, team_schema = "", []
    if C.TEAM:
        cards = []
        for m in C.TEAM:
            av = f'<img src="/assets/img/{m["photo"]}" alt="{esc(m["name"])}, {esc(m["role"])} at RankRight Media" width="120" height="120" loading="lazy">' if m.get("photo") else esc("".join(w[0] for w in m["name"].split()[:2]))
            li = f'<a class="text-link" href="{esc(m["linkedin"])}" rel="noopener" target="_blank">LinkedIn {icon("i-arrow")}</a>' if m.get("linkedin") else ""
            cards.append(f'<article class="member reveal"><div class="avatar">{av}</div><h3>{esc(m["name"])}</h3><p class="role">{esc(m["role"])}</p><p>{esc(m.get("bio",""))}</p>{li}</article>')
            team_schema.append({"@type": "Person", "name": m["name"], "jobTitle": m["role"], "worksFor": {"@id": ORG_ID},
                                **({"image": abs_url("/assets/img/" + m["photo"])} if m.get("photo") else {}),
                                **({"sameAs": [m["linkedin"]]} if m.get("linkedin") else {})})
        team_html = f"""<section class="section" id="team" aria-labelledby="team-h"><div class="container">
<div class="section-head center"><span class="eyebrow">Meet the team</span><h2 id="team-h">The People Behind RankRight Media</h2></div>
<div class="team">{''.join(cards)}</div></div></section>"""
    else:
        WARNINGS.append("/about-us/: TEAM is empty in content.py — founders/team section (and Person schema) is hidden until added")
    body = f"""
<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div><div class="container rel narrow">
{crumbs_html(crumbs)}<span class="eyebrow">About RankRight Media</span>
<h1>A UK Digital Marketing Agency Built on Honest Results</h1>
<p class="lead">RankRight Media helps businesses grow online with SEO, link building, websites, content, PPC and social media — all under one roof, with clear pricing and no jargon.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact-us/">Work with us {icon('i-arrow')}</a><a class="btn btn-ghost" href="/#services">Our services</a></div></div></section>

<section class="section" aria-labelledby="who-h"><div class="container split">
  <div class="media-frame reveal"><img src="/assets/img/team-collaboration.webp" alt="RankRight Media team members reviewing a client strategy on a tablet" width="619" height="562"></div>
  <div class="reveal d1"><span class="eyebrow">Who we are</span><h2 id="who-h">Your Digital Future, Our Expertise</h2>
  <p>RankRight Media is a UK-based digital marketing agency built with a passion for helping businesses grow online. Our mission is simple: to provide honest, effective, and smart marketing solutions that get real results. We understand that every business is different, which is why we create custom strategies tailored to your goals. From small startups to growing brands, we work with clients who want to grow fast and smart — without all the confusion.</p>
  <p>Our team includes SEO specialists, content writers, ad experts, and web developers, all working together to deliver high-quality work that speaks for itself.</p></div>
</div></section>

{team_html}

<section class="section-tight"><div class="container grid-2">
  <div class="tone tone-violet reveal"><span class="eyebrow">Our vision</span><h2 class="h3">Elevate Your Digital Presence with RankRight Media Expertise.</h2>
  <p>Our vision is to become the go-to digital marketing agency for UK businesses who want to grow with confidence. We aim to make marketing simple, effective, and stress-free for all kinds of businesses — whether online or local. By staying updated with the latest trends and tools, we make sure your brand always stays ahead in the digital world.</p></div>
  <div class="tone tone-pink reveal d1"><span class="eyebrow">Our mission</span><h2 class="h3">Unleash Your Potential in the Digital Realm with Us.</h2>
  <p>Our mission is to help businesses grow through powerful and affordable digital marketing services. We’re here to support you at every stage of your journey — whether it’s building your first website, running paid ads, or ranking on Google.</p></div>
</div></section>

<section class="section spot" aria-labelledby="val-h"><div class="container rel">
<div class="section-head center"><span class="eyebrow">Our values</span><h2 id="val-h">Smart Designs, Sharp Results</h2></div>
<div class="grid-4">
<article class="card reveal"><span class="ico">{icon('i-eye')}</span><h3>Transparency</h3><p>We keep things clear, simple, and honest. No hidden costs or fake promises.</p></article>
<article class="card reveal d1"><span class="ico">{icon('i-sparkle')}</span><h3>Creativity</h3><p>Our ideas are fresh, unique, and tailored to your brand.</p></article>
<article class="card reveal d2"><span class="ico">{icon('i-trend')}</span><h3>Results</h3><p>Everything we do is backed by data and focused on growth.</p></article>
<article class="card reveal d3"><span class="ico">{icon('i-heart')}</span><h3>Support</h3><p>We treat our clients like partners. You’re never alone — we’re here at every step.</p></article>
</div></div></section>

{stats_band()}

<section class="panel-photo" aria-labelledby="why-h"><div class="bgimg"><img src="/assets/img/outreach-team.webp" alt="RankRight Media team collaborating at their desks" width="945" height="992" loading="lazy"></div>
<div class="container"><div class="glass reveal"><span class="eyebrow">Why choose us</span><h2 id="why-h">Why Clients Choose RankRight Media</h2>
<ul class="ticks">
<li>{icon('i-check')}<span><strong>Real Results</strong> – We focus on ROI, not just traffic.</span></li>
<li>{icon('i-check')}<span><strong>Clear Communication</strong> – No technical jargon — just simple updates.</span></li>
<li>{icon('i-check')}<span><strong>Affordable Plans</strong> – Flexible pricing that fits your budget.</span></li>
<li>{icon('i-check')}<span><strong>Dedicated Team</strong> – Experts who care about your business.</span></li>
<li>{icon('i-check')}<span><strong>UK-Based Support</strong> – Easy to reach, always available.</span></li></ul>
<a class="btn btn-primary" href="/contact-us/">Start your project {icon('i-arrow')}</a></div></div></section>

{testimonials_section(['daniel-reid', 'emma-clarke', 'nathan-clarke'])}
{cta_band()}
"""
    render(path, title="About RankRight Media | UK Digital Marketing Agency",
           description="Meet RankRight Media: a UK digital marketing agency of SEO specialists, writers, ad experts and web developers helping businesses grow online.",
           body=body, active="about", schema=team_schema, crumbs=crumbs, page_type="AboutPage", priority="0.8")


def package_options():
    opts = ['<option value="">Not sure yet — please advise</option>']
    for k in C.SERVICE_ORDER:
        s = C.SERVICES[k]
        grp = [f'<option value="{k}">{esc(s["name"])} — general enquiry</option>']
        if s["packages"]:
            for p in s["packages"]["items"]:
                unit = s["packages"]["unit"] if p["price"] is not None else ""
                grp.append(f'<option value="{p["id"]}">{esc(p["name"])} — {money(p["price"])}{(" " + esc(unit)) if unit else ""}</option>')
        opts.append(f'<optgroup label="{esc(s["name"])}">{"".join(grp)}</optgroup>')
    return "".join(opts)


def page_contact():
    path = "/contact-us/"
    crumbs = [("Home", "/"), ("Contact Us", path)]
    email_card = f'<a href="mailto:{esc(S["email"])}"><span class="ico">{icon("i-mail")}</span><span><b>Email us</b><span>{esc(S["email"])}</span></span></a>' if S["email"] else ""
    faqs = [C.HOME_FAQS[2], C.HOME_FAQS[3], C.HOME_FAQS[5]]
    body = f"""
<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div><div class="container rel narrow">
{crumbs_html(crumbs)}<span class="eyebrow">Contact us</span>
<h1>Let’s Grow Your Business Together</h1>
<p class="lead">Tell us about your goals and we’ll recommend the right package. Prefer to talk? Call our UK team on <a href="tel:{S['phone_e164']}">{esc(S['phone_display'])}</a>.</p></div></section>

<section class="section" id="enquiry" aria-labelledby="form-h"><div class="container split split-60">
<form class="form reveal" action="/contact.php" method="post" accept-charset="UTF-8">
  <h2 id="form-h" class="h3">Send us an enquiry</h2>
  <p class="notice" id="form-error" role="alert" hidden>Sorry — your message didn’t send. Please check the required fields and try again, or call us on {esc(S['phone_display'])}.</p>
  <div class="form-row">
    <div class="field"><label for="f-name">Your name <span aria-hidden="true">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required maxlength="100"></div>
    <div class="field"><label for="f-email">Email <span aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
  </div>
  <div class="form-row">
    <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40"></div>
    <div class="field"><label for="f-website">Website</label><input id="f-website" name="website" type="url" inputmode="url" placeholder="https://" maxlength="200"></div>
  </div>
  <div class="field"><label for="f-package">Service or package</label><select id="f-package" name="package">{package_options()}</select></div>
  <div class="field"><label for="f-message">How can we help? <span aria-hidden="true">*</span></label><textarea id="f-message" name="message" required maxlength="5000" placeholder="Your goals, timeline and anything else we should know"></textarea></div>
  <div class="hp" aria-hidden="true"><label for="f-company">Leave this field empty</label><input id="f-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
  <input id="f-ts" name="ts" type="hidden" value="0">
  <label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I agree to RankRight Media contacting me about this enquiry, as described in the <a href="/privacy-policy/">Privacy Policy</a>.</span></label>
  <button class="btn btn-primary" type="submit">Send enquiry {icon('i-arrow')}</button>
  <small>We reply within one working day. Your details are never shared or sold.</small>
</form>
<aside class="contact-cards" aria-label="Other ways to reach us">
  <a href="tel:{S['phone_e164']}"><span class="ico">{icon('i-phone')}</span><span><b>Call our team</b><span>{esc(S['phone_display'])}</span></span></a>
  {email_card}
  <div><span class="ico">{icon('i-pin')}</span><span><b>UK-based agency</b><span>Working with businesses across the United Kingdom</span></span></div>
  <div><span class="ico">{icon('i-clock')}</span><span><b>Fast replies</b><span>Enquiries answered within one working day</span></span></div>
</aside>
</div></section>
{faq_section(faqs, heading="Before you get in touch")}
"""
    render(path, title="Contact RankRight Media | Get a Free Quote",
           description="Contact RankRight Media for SEO, link building, websites, content, PPC and social media. Call +44 7446 254421 or request a free quote online.",
           body=body, active="contact", schema=[faq_node(path, faqs)], crumbs=crumbs, page_type="ContactPage", priority="0.8")


def page_faqs():
    path = "/faqs/"
    crumbs = [("Home", "/"), ("FAQs", path)]
    groups, all_faqs = [], list(C.HOME_FAQS)
    groups.append(("General", C.HOME_FAQS, "/"))
    for k in C.SERVICE_ORDER:
        s = C.SERVICES[k]
        groups.append((s["name"], s["faqs"], svc_url(k)))
        all_faqs += s["faqs"]
    blocks = []
    for gi, (name, faqs, url) in enumerate(groups):
        items = "".join(f"<details><summary>{esc(q)}<span class=\"pm\">{icon('i-chevron')}</span></summary><div class=\"a\">{a}</div></details>" for q, a in faqs)
        more = f'<p><a class="text-link" href="{url}">Explore {esc(name)} {icon("i-arrow")}</a></p>' if url != "/" else ""
        blocks.append(f'<section class="section-tight" aria-labelledby="g{gi}"><h2 id="g{gi}">{esc(name)}</h2><div class="faq">{items}</div>{more}</section>')
    body = f"""
<section class="page-hero"><div class="aurora"></div><div class="gridlines"></div><div class="container rel narrow">
{crumbs_html(crumbs)}<span class="eyebrow">Help centre</span><h1>Frequently Asked Questions</h1>
<p class="lead">Straight answers about our SEO, link building, website, content, PPC and social media services — including pricing and timelines.</p></div></section>
<div class="container narrow">{''.join(blocks)}</div>
{cta_band(h="Still have a question?", p="Our UK team is happy to help — get in touch and we’ll reply within one working day.", primary=("Contact us", "/contact-us/"))}
"""
    render(path, title="FAQs | SEO, Link Building, Web & PPC Questions | RankRight Media",
           description="Answers to common questions about RankRight Media’s SEO, link building, website development, content writing, PPC and social media services, pricing and timelines.",
           body=body, active="faqs", schema=[faq_node(path, all_faqs)], crumbs=crumbs, priority="0.7")


LEGAL = {
    "privacy-policy": ("Privacy Policy", "How RankRight Media collects, uses and protects personal data under UK GDPR, including enquiries, cookies and your data protection rights.", f"""
<p>This policy explains how {S['name']} (“we”, “us”) collects and uses personal data when you visit this website or contact us. We are the data controller for this information under the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018.</p>
<h2>What we collect</h2><ul><li><strong>Enquiries:</strong> your name, email address, phone number, website and message when you use our contact form, call or email us.</li><li><strong>Client information:</strong> business details and account access you provide so we can deliver our services.</li><li><strong>Technical data:</strong> standard server logs (IP address, browser type, pages requested) kept by our hosting provider for security.</li></ul>
<h2>Cookies</h2><p>This website does not use advertising or analytics cookies. If we introduce analytics in future, we will ask for your consent first and update this policy.</p>
<h2>How we use your data</h2><ul><li>To reply to your enquiry and provide quotes (legitimate interests / steps before entering a contract).</li><li>To deliver the services you buy and manage your account (contract).</li><li>To meet legal, tax and accounting obligations (legal obligation).</li></ul><p>We never sell your data or use it for unrelated marketing without your consent.</p>
<h2>Sharing</h2><p>We share data only with trusted providers who help us run our business — such as our website host, email provider and payment processor — under appropriate data processing terms.</p>
<h2>How long we keep it</h2><p>Enquiries that don’t lead to work are deleted within 12 months. Client records are kept for as long as required for legal and accounting purposes (normally six years).</p>
<h2>Your rights</h2><p>You can ask to access, correct, delete or restrict use of your personal data, object to processing, or request a copy in a portable format. Contact us using the details on our <a href="/contact-us/">contact page</a>. You also have the right to complain to the Information Commissioner’s Office (ico.org.uk).</p>
"""),
    "refund-policy": ("Refund Policy", "RankRight Media refund and cancellation policy for SEO, link building, website, content, PPC and social media services.", """
<p>We want you to be confident buying from us. This policy explains when refunds and cancellations apply.</p>
<h2>Before work starts</h2><p>If you cancel an order before we have started work, we will refund your payment in full.</p>
<h2>Consumers’ 14-day cancellation right</h2><p>If you buy as a consumer (not for business purposes), you have 14 days to cancel under the Consumer Contracts Regulations 2013. If you ask us to start work within that period, we may deduct a fair amount for work already carried out.</p>
<h2>Work in progress and completed work</h2><p>Because our services involve time, outreach and third-party placements, payments for work already completed or delivered (for example, published backlinks or written content) are not refundable. Where work has been partly completed, we will refund the unused portion.</p>
<h2>Monthly plans</h2><p>Monthly plans can be cancelled before your next billing date. Work already paid for in the current month will be completed and reported.</p>
<h2>If something isn’t right</h2><p>If a deliverable doesn’t match what your package describes, tell us within 14 days of delivery and we will fix it, replace it or refund that item.</p>
<h2>How to request a refund</h2><p>Contact us via our <a href="/contact-us/">contact page</a> with your order details. Approved refunds are returned to your original payment method within 14 days.</p>
"""),
    "terms-and-conditions": ("Terms & Conditions", "The terms and conditions that apply when you use the RankRight Media website or buy our digital marketing services.", """
<p>These terms apply to your use of this website and to any services you buy from RankRight Media. Please read them carefully.</p>
<h2>Our services</h2><p>We provide the deliverables described in the package or proposal you accept. Timelines are estimates and depend on you providing information, content and access promptly.</p>
<h2>Results</h2><p>Search engines, ad platforms and social networks are controlled by third parties. We do not guarantee specific rankings, traffic or sales, but we will always carry out the agreed work with reasonable skill and care.</p>
<h2>Payment</h2><p>Prices are shown on our website or in your proposal. One-off packages are paid in advance. Monthly plans are billed in advance each month. Advertising spend is paid directly to the advertising platform and is not included in our fees unless stated.</p>
<h2>Your responsibilities</h2><p>You confirm that you have the right to the content, trademarks and accounts you give us, and that your website and products comply with the law and platform policies.</p>
<h2>Intellectual property</h2><p>Once paid for in full, content and designs we create for you belong to you. We may reference the work in our portfolio unless you ask us not to.</p>
<h2>Liability</h2><p>Nothing in these terms limits liability that cannot be limited by law. Otherwise, our total liability is limited to the amount you paid for the service in question.</p>
<h2>Cancellations and refunds</h2><p>See our <a href="/refund-policy/">Refund Policy</a>.</p>
<h2>Law</h2><p>These terms are governed by the laws of England and Wales.</p>
"""),
}


def page_legal(slug):
    title, desc, html_body = LEGAL[slug]
    path = f"/{slug}/"
    crumbs = [("Home", "/"), (title, path)]
    body = f"""
<section class="page-hero"><div class="container rel narrow">{crumbs_html(crumbs)}<h1>{esc(title)}</h1>
<p class="updated">{icon('i-clock')}Last updated <time datetime="{TODAY}">{_dt.date.today().strftime('%-d %B %Y')}</time></p></div></section>
<section class="section"><div class="container narrow legal prose">{html_body}</div></section>"""
    # noindex until the business has reviewed/replaced the draft legal text
    render(path, title=f"{title} | RankRight Media", description=desc, body=body, crumbs=crumbs, robots="noindex", priority="0.3")
    WARNINGS.append(f"{path}: DRAFT legal text — replace with your reviewed policy, then set robots to index")


def page_thanks():
    body = f"""<section class="section nf"><div class="container narrow center"><span class="ico ico-solid">{icon('i-check')}</span>
<h1>Thank you — we’ve got your enquiry</h1><p class="lead">A member of our UK team will reply within one working day. Need us sooner? Call <a href="tel:{S['phone_e164']}">{esc(S['phone_display'])}</a>.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Back to home</a><a class="btn btn-ghost" href="/#services">Explore services</a></div></div></section>"""
    render("/thank-you/", title="Thank You | RankRight Media", description="Thanks for contacting RankRight Media. Our UK team will reply to your enquiry within one working day.", body=body, robots="noindex")


def page_404():
    body = f"""<section class="section nf"><div class="container narrow center"><b class="grad-text">404</b>
<h1>This page has moved or doesn’t exist</h1><p class="lead">Try one of our services below, or head back to the homepage.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Back to home</a><a class="btn btn-ghost" href="/contact-us/">Contact us</a></div></div></section>
{related_section(['seo', 'link-building', 'website-development'])}"""
    render("/404.html", title="Page Not Found | RankRight Media", description="Sorry, we couldn’t find that page. Explore RankRight Media’s SEO, link building, website, content, PPC and social media services.", body=body, robots="noindex")


# ------------------------------------------------------------------------------------------------
# Non-HTML files
# ------------------------------------------------------------------------------------------------
def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def extra_files():
    urls = "".join(f"<url><loc>{abs_url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, idx, pr in PAGES if idx)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    # robots.txt — explicitly welcome search and AI answer engines
    bots = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "DuckDuckBot", "Amazonbot", "meta-externalagent", "CCBot"]
    rb = "\n".join(f"User-agent: {b}\nAllow: /\n" for b in bots)
    write("robots.txt", f"# {S['name']} — search engines and AI assistants are welcome to read and cite this site.\n{rb}\nUser-agent: *\nAllow: /\nDisallow: /contact.php\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    # llms.txt — concise, factual brief for LLMs / AI answer engines
    lines = [f"# {S['name']}", "", f"> {S['name']} is a UK-based digital marketing agency offering SEO, link building, website development, SEO content writing, PPC (pay-per-click) management and social media marketing, with clear packages and monthly reporting.", "",
             f"- Website: {DOMAIN}/", f"- Phone: {S['phone_display']}", f"- Area served: {', '.join(S['area_served'])}", f"- Prices shown in: {S['currency_code']}"]
    if S["email"]:
        lines.append(f"- Email: {S['email']}")
    lines += ["", "## Services", ""]
    for k in C.SERVICE_ORDER:
        s = C.SERVICES[k]
        lines.append(f"- [{s['name']}]({abs_url(svc_url(k))}): {s['description']}")
    for k in C.SERVICE_ORDER:
        s = C.SERVICES[k]
        if s["packages"]:
            lines += ["", f"## {s['packages']['heading']} ({s['packages']['unit']})", ""]
            for p in s["packages"]["items"]:
                lines.append(f"- {p['name']} — {money(p['price'])}: {'; '.join(p['features'])}")
    lines += ["", "## Key pages", "", f"- [About us]({DOMAIN}/about-us/)", f"- [FAQs]({DOMAIN}/faqs/)", f"- [Contact / quote]({DOMAIN}/contact-us/)", ""]
    write("llms.txt", "\n".join(lines))
    write("site.webmanifest", json.dumps({"name": S["name"], "short_name": "RankRight", "start_url": "/", "display": "browser", "background_color": "#07010f",
                                          "theme_color": "#07010f", "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                                                                              {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    csp = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; "
           "form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests")
    host = DOMAIN.split("://")[1]
    write(".htaccess", f"""# RankRight Media — Apache / LiteSpeed (Hostinger) configuration
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# One canonical origin: https + non-www
RewriteCond %{{HTTPS}} !=on [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://{host}%{{REQUEST_URI}} [L,R=301]
# Old WordPress endpoints: stop bot noise
RewriteRule ^(xmlrpc\\.php|wp-login\\.php|wp-admin/?.*)$ - [G,L]
# --- 301s from old WordPress URLs (fill in from the live sitemap before launch) ---
# RewriteRule ^old-slug/?$ /new-slug/ [R=301,L]
RewriteRule ^about/?$ /about-us/ [R=301,L]
RewriteRule ^contact/?$ /contact-us/ [R=301,L]
RewriteRule ^faq/?$ /faqs/ [R=301,L]
RewriteRule ^terms/?$ /terms-and-conditions/ [R=301,L]
</IfModule>

<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"
Header always set Cross-Origin-Opener-Policy "same-origin"
Header always set Content-Security-Policy "{csp}"
Header unset X-Powered-By
<FilesMatch "\\.(css|js|woff2|webp|png|svg|ico)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\\.(html|xml|txt|webmanifest)$">
Header set Cache-Control "public, max-age=300, must-revalidate"
</FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript text/plain application/xml image/svg+xml application/manifest+json
</IfModule>
AddType application/manifest+json .webmanifest
AddType text/plain .txt
AddDefaultCharset UTF-8
""")
    write("_headers", f"""/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Cross-Origin-Opener-Policy: same-origin
  Content-Security-Policy: {csp}
/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")


def copy_static():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(SRC, "root")):
        shutil.copy2(os.path.join(SRC, "root", f), os.path.join(OUT, f))


# ------------------------------------------------------------------------------------------------
# Checks: links, anchors, ids, headings, images
# ------------------------------------------------------------------------------------------------
class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1, self.imgs_no_alt, self.inline_style = [], [], 0, 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if "style" in a:
            self.inline_style += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and not a.get("alt"):
            self.imgs_no_alt += 1
        for k in ("href", "src"):
            v = a.get(k)
            if v and tag != "use":
                self.links.append(v)
        if tag == "use" and a.get("href"):
            self.links.append(a["href"])


def check():
    errors = []
    files = {}
    for dp, _, fs in os.walk(OUT):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(dp, f)
                sc = Scan()
                sc.feed(open(p, encoding="utf-8").read())
                files[p] = sc
    for p, sc in files.items():
        rel = os.path.relpath(p, OUT)
        dup = {i for i in sc.ids if sc.ids.count(i) > 1}
        if dup:
            errors.append(f"{rel}: duplicate ids {sorted(dup)}")
        if sc.h1 != 1:
            errors.append(f"{rel}: has {sc.h1} <h1> elements")
        if sc.imgs_no_alt:
            errors.append(f"{rel}: {sc.imgs_no_alt} <img> without alt")
        if sc.inline_style:
            errors.append(f"{rel}: {sc.inline_style} inline style attributes (blocked by CSP)")
        for link in sc.links:
            if link.startswith(("http", "mailto:", "tel:", "data:")):
                continue
            target, _, frag = link.partition("#")
            target = target.split("?")[0]
            if target == "":
                if frag and frag not in sc.ids:
                    errors.append(f"{rel}: missing anchor #{frag}")
                continue
            fp = os.path.join(OUT, target.lstrip("/"))
            if target.endswith("/"):
                fp = os.path.join(fp, "index.html")
            if target == "/contact.php":
                continue
            if not os.path.exists(fp):
                errors.append(f"{rel}: broken link {link}")
                continue
            if frag and fp.endswith(".html") and fp in files and frag not in files[fp].ids:
                errors.append(f"{rel}: link {link} — anchor not found")
            if frag and fp.endswith(".svg"):
                if f'id="{frag}"' not in open(fp, encoding="utf-8").read():
                    errors.append(f"{rel}: icon #{frag} missing from sprite")
    return errors


def main():
    copy_static()
    page_home()
    for k in C.SERVICE_ORDER:
        page_service(k)
    page_about()
    page_contact()
    page_faqs()
    for slug in LEGAL:
        page_legal(slug)
    page_thanks()
    page_404()
    extra_files()
    print(f"Built {len(PAGES)} pages into {os.path.relpath(OUT, ROOT)}/")
    for w in WARNINGS:
        print("  WARN", w)
    errs = check()
    for e in errs:
        print("  ERROR", e)
    if errs and "--check" in sys.argv:
        sys.exit(1)
    print("Checks:", "OK" if not errs else f"{len(errs)} error(s)")


if __name__ == "__main__":
    main()
