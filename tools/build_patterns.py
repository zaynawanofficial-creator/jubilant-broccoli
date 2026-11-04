"""Builds every page of the SEO Booster site as block patterns + a site manifest.

Output:
  wp-content/themes/seo-booster/patterns/page-*.php   (one editable block pattern per page/post)
  wp-content/themes/seo-booster/inc/site-manifest.php (pages/posts the setup screen creates)
Run: python3 tools/build_patterns.py

Content rules (CLAUDE.md): no invented clients, results, reviews, credentials or guarantees.
Prices are never hard-coded: cards use [sb_from service="…"] and [sb_packages …], which read WooCommerce.
"""
import os
from blocks import (group, heading, para, eyebrow, lead, ul, buttons, image, columns, column, details,
                    table, shortcode, query_posts, join)

ROOT = os.path.join(os.path.dirname(__file__), '..', 'wp-content', 'themes', 'seo-booster')
PAT = os.path.join(ROOT, 'patterns')
os.makedirs(PAT, exist_ok=True)

# ---------------------------------------------------------------- shared data
SERVICES = [
    # slug, product_cat slug, name, icon, art, short
    ('off-page-seo', 'off-page-seo', 'Off-Page SEO &amp; Link Building', 'offpage', 'offpage',
     'Business citations, profile links, guest posts and press releases, built by hand and reported with live URLs.'),
    ('seo-audit', 'seo-audit', 'SEO Audit', 'audit', 'audit',
     'A prioritised, plain-English list of what is holding your site back in search, with the fix for each issue.'),
    ('technical-seo', 'technical-seo', 'Technical SEO', 'technical', 'technical',
     'Hands-on fixes for indexing, redirects, structured data and Core Web Vitals, with a before/after report.'),
    ('website-development', 'website-development', 'Website Development', 'webdev', 'webdev',
     'Fast, mobile-friendly WordPress sites from a 1-page landing page to a 10-page business website.'),
    ('website-maintenance', 'website-maintenance', 'Website Maintenance &amp; Fixes', 'maintenance', 'maintenance',
     'One-off WordPress fixes and simple monthly care: updates, backups, monitoring and small changes.'),
    ('content-writing', 'content-writing', 'Content Writing', 'content', 'content',
     'Original, researched articles from 500 to 3,000 words, or a month of content planned as a topic cluster.'),
    ('graphic-design', 'graphic-design', 'Graphic Design &amp; Branding', 'design', 'design',
     'Social media graphics, ad creatives and brand kits in your colours, delivered ready to use.'),
]
from services_new import NEW as NEW_SERVICES
SERVICES += [(n['slug'], n['slug'], n['name'].replace('&', '&amp;'), n['icon'], n['art'], n['short']) for n in NEW_SERVICES]
SVC = {s[0]: s for s in SERVICES}


def art_file(s):
    a = s[4]
    return f'{a}.svg' if a.startswith(('art-', 'hero-', 'report-')) else f'art-{a}.svg'


def svc_card(slug, dark=False):
    s = SVC[slug]
    return group(
        image(art_file(s), '', 'sb-card__art'),
        heading(f'<a href="/services/{s[0]}/">{s[2]}</a>', 3),
        para(s[5]),
        para(f'From <strong>[sb_from service="{s[1]}"]</strong>', 'sb-price-from'),
        para('View packages →', 'sb-card__more'),
        cls='sb-card sb-card--svc sb-card--dark' if dark else 'sb-card sb-card--svc', layout='flow')


def card(title, text, icon=None, cls='sb-card'):
    parts = [image(f'icon-{icon}.svg', '', 'sb-card__icon')] if icon else []
    return group(*parts, heading(title, 3), para(text) if isinstance(text, str) else text, cls=cls, layout='flow')


def section(*children, cls='', anchor='', tag='section'):
    return group(*children, align='full', cls=('sb-section ' + cls).strip(), anchor=anchor, tag=tag)


def head(eb, title, sub=None, center=False):
    parts = [eyebrow(eb) if eb else '', heading(title), lead(sub) if sub else '']
    return group(*parts, cls='sb-section-head' + (' sb-center' if center else ''), layout='flow', align='wide')


def grid(*children, n=4, cls=''):
    """Fixed-column responsive grid (4/3/2 on desktop, 2 on tablet, 1 on phones). CSS: .sb-grid--N."""
    return group(*children, align='wide', cls=f'sb-grid sb-grid--{n} {cls}'.strip(), layout='flow')


STEP_ICONS = ['scope', 'shield', 'human', 'report']


def steps(items):
    return grid(*[group(group(para(f'{i + 1:02d}', 'sb-step__n'), image(f'icon-{STEP_ICONS[i % 4]}.svg', '', 'sb-step__icon'), cls='sb-step__top', layout='flex'),
                        heading(t, 3), para(d), cls='sb-card sb-step', layout='flow') for i, (t, d) in enumerate(items)], n=4, cls='sb-steps')


def faq(items):
    return group(*[details(q, a) for q, a in items], cls='sb-faq', layout='constrained')


def cta(title='Not sure which package fits?', text='Tell us about your site and goals. We will recommend the right package, or send a fixed quote for anything custom.',
        btns=(('Get a free quote', '/get-a-quote/'), ('Browse packages', '/packages/', 'outline')), art='art-quote.svg'):
    return section(group(columns(column(heading(title), para(text), buttons(*btns), width='60%'),
                                 column(image(art, '', 'sb-cta__art'), width='40%', cls='sb-hide-mobile'), align='', center=True, cls='sb-cta__cols'),
                         align='wide', cls='sb-cta', layout='flow'), cls='sb-section--tight')


def page_hero(art, alt, *blocks):
    """Inner-page hero: breadcrumbs + copy on the left, illustration on the right."""
    left = column(shortcode('[sb_breadcrumbs]'), *blocks, width='58%')
    right = column(image(art, alt, 'sb-hero__art'), width='42%')
    return group(columns(left, right, cls='sb-hero__cols', center=True), align='full', cls='sb-hero sb-hero--page', tag='section')


def proof(art, alt, eb, title, text, bullets, note='Illustrative example. Your report shows your own URLs and data.', cls=''):
    """Split section: deliverable visual + what you receive."""
    return section(columns(column(image(art, alt, 'sb-proof__art'), width='50%'),
                           column(eyebrow(eb), heading(title), para(text), ul(bullets, 'sb-ticks'), para(note, 'sb-muted'), width='50%'),
                           cls='sb-split', center=True), cls=cls)


def hero(eb, title, sub, btns, checks, art, alt, crumbs=False):
    left = column(*( [shortcode('[sb_breadcrumbs]')] if crumbs else []), eyebrow(eb), heading(title, 1), lead(sub), buttons(*btns), ul(checks, 'sb-checks'), width='56%')
    right = column(image(art, alt, 'sb-hero__art'), width='44%')
    return group(columns(left, right, cls='sb-hero__cols', center=True), align='full', cls='sb-hero', tag='section')


WHATIS = {
    'off-page-seo': ('What is off-page SEO?', [
        'Off-page SEO is everything that happens away from your own website to show search engines your business is real, relevant and trusted. The biggest part is links: other websites pointing to yours. Business listings and citations (your name, address and phone number on trusted directories) matter most for local searches.',
        'Not all links are equal. A handful of relevant, editorial links usually beats hundreds of spammy ones, and Google ignores or penalises links that exist only to manipulate rankings. That is why we build links by hand on real platforms, keep sponsored labels where publishers require them, and give you every URL so you can check the work yourself.']),
    'seo-audit': ('What is an SEO audit?', [
        'An SEO audit is a health check of your website from a search engine\'s point of view. It looks at whether Google can crawl and index your pages, how fast they load, whether titles and content match what people search for, and what your link profile looks like compared with competitors.',
        'A good audit is not a 90-page export from a tool. It tells you which problems actually cost you traffic, in what order to fix them, and how. Ours does exactly that, in plain English, so you can spend your budget on the fixes that matter.']),
    'technical-seo': ('What is technical SEO?', [
        'Technical SEO is the foundation under your content: making sure search engines can crawl, render and understand your pages, and that visitors get a fast, stable experience. It covers redirects, canonical tags, sitemaps, structured data, duplicate pages and Core Web Vitals.',
        'When the foundation is broken, great content and links underperform. A single misplaced noindex tag or a chain of redirects can hide pages from Google entirely. We find and fix these issues safely, after a full backup, and show you the before and after.']),
    'website-development': ('What does a small business website need?', [
        'A good small business website does three jobs: it explains what you do in the first few seconds, it convinces visitors you are trustworthy, and it makes it easy to get in touch or buy. Everything else, from colours to animations, should support those three jobs.',
        'We build on WordPress because it is fast to edit, widely supported and yours to keep. Every site is mobile-friendly, set up with SEO basics from day one, and handed over with a video so you can update pages without paying a developer each time.']),
    'website-maintenance': ('Why does a WordPress site need maintenance?', [
        'WordPress, your theme and your plugins all release updates for security fixes and compatibility. Skip them and the risk of a hack or a broken page grows every month. Install them carelessly and a plugin conflict can take the site down.',
        'Maintenance means doing updates safely: a backup first, updates in the right order, checks afterwards, and someone watching uptime. When something does break, you want a developer who finds the real cause, not a quick patch that fails again next week.']),
    'content-writing': ('What makes content rank and convert?', [
        'Content ranks when it answers the question behind a search better than the pages already there: clearer, more specific, more useful. It converts when it speaks to a real reader, shows expertise and makes the next step obvious.',
        'Word count alone does neither. We plan every article around search intent, structure it with clear headings and direct answers, check the facts, and write it for people first. The SEO details, such as keywords, meta descriptions and internal links, are built in without making it read like it was written for a robot.']),
    'graphic-design': ('Why does consistent branding matter?', [
        'People decide whether to trust a business in seconds, and design is a big part of that first impression. A consistent logo, colours and typography across your website, social media and adverts makes you look established and makes you easier to remember.',
        'You do not need an expensive agency to get there. A clear brand kit and a steady supply of on-brand graphics give most small businesses everything they need to look professional everywhere they show up.']),
}

FEATURE_ICONS = ['human', 'scope', 'report', 'shield', 'technical']

DELIVER = {
    'off-page-seo': ('report-links.svg', 'Illustration of a link report listing each live URL', 'Proof of work', 'A live-URL report for every order',
                     'You get a spreadsheet listing every placement: the platform or publisher, the live URL and its status on delivery day, so you can check each one yourself.',
                     ['Every live URL, ready to click and verify', 'Platform or publisher and its category', 'Domain Rating at publication for guest posts', 'Replacement terms stated on every package']),
    'seo-audit': ('report-audit.svg', 'Illustration of an audit report with charts and a prioritised issue list', 'Your report', 'A prioritised plan, not a 90-page data dump',
                  'Each issue is rated high, medium or low, explained in plain English and paired with the fix, so you or your developer know exactly what to do first.',
                  ['Executive summary on one page', 'Issues grouped by impact', 'Screenshots and affected URLs', 'Clear fix for every finding']),
    'technical-seo': ('report-audit.svg', 'Illustration of a technical change log with before and after charts', 'Your report', 'Every change logged, with before and after',
                      'We back up first, make the fixes, then hand you a change log with the before/after measurements for each one.',
                      ['Backup taken before any change', 'Change log you can share with your team', 'Lab speed results before and after', 'Search Console checks after fixes']),
    'website-development': ('hero-growth.svg', 'Illustration of a website dashboard and growth chart', 'Handover', 'A site you can run yourself',
                            'Your site is built in WordPress with a standard editor. At launch you get a recorded walkthrough so you can update pages without calling a developer.',
                            ['Responsive pages tested on phones and desktops', 'Contact form connected to your inbox', 'SEO basics set: titles, descriptions, sitemap', 'Recorded handover video']),
    'website-maintenance': ('art-about.svg', 'Illustration of a maintenance report and completed checklist', 'Every fix documented', 'Know exactly what was wrong and what changed',
                            'After every fix or care month you receive a plain-English summary: the cause, what we changed and anything to watch.',
                            ['Backup before every change', 'Root cause, not just the symptom', 'Updates and checks logged for care plans', 'Same issue back within 14 days? Fixed free']),
    'content-writing': ('art-faq.svg', 'Illustration of a structured article with questions answered', 'Built to answer', 'Articles that answer real questions',
                        'Every article is structured around what your readers search for, with clear headings, direct answers and natural keyword use.',
                        ['Topic and keyword agreed before writing', 'Meta title and description included', 'Plagiarism-checked and fact-checked', 'Delivered as a Google Doc or Word file']),
    'graphic-design': ('art-services.svg', 'Illustration of design files and a brand board', 'Ready-to-use files', 'Files that work everywhere you need them',
                       'You receive correctly sized exports for each platform, plus vector source files for branding, organised so your team can find them.',
                       ['Exports sized for each platform', 'Vector files for logos and brand kits', 'Colour and font references', 'Licensed assets only']),
}

HOW_STEPS = [
    ('Choose a package', 'Every package lists exactly what is included, what is not, the turnaround and the revisions. Pick one, or ask for a quote.'),
    ('Add your project details', 'Right after choosing a package, a short form collects what we need: URLs, keywords and preferences. Files can follow later.'),
    ('Pay securely', 'Check out in one step. You get an order number and receipt by email straight away.'),
    ('Receive your delivery', 'We deliver within the stated turnaround, with a report or files you can check. Revisions are included where listed.'),
]

PAGES = []   # dicts for the manifest
POSTS = []


SEO_TITLES = {
    'home': 'SEO Services UK | Fixed-Price SEO, Link Building & Websites',
    'services': 'SEO, Web Design & Content Services with Fixed Prices | SEO Booster',
    'off-page-seo': 'Link Building Services | Off-Page SEO, Citations & Guest Posts',
    'seo-audit': 'SEO Audit Service | Technical SEO Audit with Prioritised Fixes',
    'technical-seo': 'Technical SEO Services | Core Web Vitals, Schema & Fixes',
    'website-development': 'Website Development Services | Design & Build at a Fixed Price',
    'website-maintenance': 'Website Maintenance Services | WordPress Care Plans & Fixes',
    'content-writing': 'SEO Content Writing Services | Articles from 500 to 3,000 Words',
    'graphic-design': 'Graphic Design & Branding Packages | Logos, Brand Kits, Social',
    'packages': 'SEO & Website Packages and Prices | SEO Booster',
    'how-it-works': 'How Ordering Works | Scope, Payment, Delivery | SEO Booster',
    'about': 'About SEO Booster | Transparent SEO & Web Services',
    'contact': 'Contact SEO Booster | Questions, Orders & Custom Projects',
    'get-a-quote': 'Get a Free Fixed Quote for SEO or Web Work | SEO Booster',
    'faq': 'FAQ | Ordering, Payments, Delivery & Link Building | SEO Booster',
}


def page(slug, title, content, excerpt, parent='', template='landing', menu_order=0):
    PAGES.append(dict(slug=slug, title=title, parent=parent, template=template, excerpt=excerpt, pattern=f'seo-booster/page-{slug}', order=menu_order, seo_title=SEO_TITLES.get(slug, '')))
    write_pattern(f'page-{slug}', f'Page: {title}', content)


def post(slug, title, content, excerpt, category='Guides'):
    POSTS.append(dict(slug=slug, title=title, excerpt=excerpt, category=category, pattern=f'seo-booster/post-{slug}'))
    write_pattern(f'post-{slug}', f'Article: {title}', content, cat='seo-booster-sections', post_types='post', inserter='no')


def write_pattern(name, title, content, cat='seo-booster-pages', post_types='page', inserter='yes'):
    hdr = (f"<?php\n/**\n * Title: {title.replace('&amp;', '&')}\n * Slug: seo-booster/{name}\n * Categories: {cat}\n"
           f" * Post Types: {post_types}\n * Inserter: {inserter}\n * Description: Generated by tools/build_patterns.py\n */\n?>\n")
    with open(os.path.join(PAT, f'{name}.php'), 'w') as f:
        f.write(hdr + content + '\n')


# ================================================================ HOME
home = join(
    hero('SEO · Websites · Content · Design',
         'SEO services, link building and websites at <span class="sb-hl">fixed prices</span>',
         'Choose a package, tell us about your site and pay securely. You get a written scope, a delivery date and proof of the work: live links, audit reports or ready-to-use files. No retainers, no lock-in, no vague monthly summaries.',
         [('Explore packages', '/packages/'), ('Get a free quote', '/get-a-quote/', 'outline')],
         ['Packages from [sb_from]', 'Scope agreed before you pay', 'Live-URL and before/after reports'],
         'hero-growth.svg', 'Illustration of a growth chart, a network of links and a completed checklist'),
    group(group(
        group(image('icon-scope.svg', ''), para('<strong>Clear scope</strong>Deliverables, exclusions and turnaround on every package.'), layout='flow'),
        group(image('icon-human.svg', ''), para('<strong>Done by people</strong>Manual work, checked before it reaches you.'), layout='flow'),
        group(image('icon-report.svg', ''), para('<strong>Proof of work</strong>Live URLs, before/after data or source files.'), layout='flow'),
        group(image('icon-shield.svg', ''), para('<strong>Safe methods</strong>No PBNs, no ranking guarantees, no password requests.'), layout='flow'),
        align='wide', cls='sb-trust', layout='flow'), align='full', cls='sb-section--dark sb-trustbar', layout='constrained', tag='section'),
    section(head('Services', 'Everything a growing website needs, priced up front',
                 'Start with one service or combine several. Each one has its own packages, so you only pay for what you need.'),
            group(*[svc_card(x) for x in ['monthly-seo', 'local-seo', 'off-page-seo', 'seo-audit', 'website-development', 'ecommerce-website-development', 'ppc-management', 'content-writing']],
                  align='wide', layout='flow', cls='sb-grid sb-grid--4'),
            para('<a href="/services/">See all 20 services →</a>', 'sb-center sb-card__more')),
    proof('report-links.svg', 'Illustration of a delivery report listing live URLs', 'Proof of work', 'Every order ends with something you can check',
          'No vague monthly summaries. You receive the actual output: live URLs, an audit PDF, a change log or your design files, with what was done and when.',
          ['Live-URL reports for every link order', 'Prioritised audit reports in plain English', 'Before/after measurements for technical work', 'Source files for websites and design'], cls='sb-section--blue'),
    section(head('Most popular', 'Off-page SEO packages', 'Two package groups: foundational citations and profile links, and premium guest posts by Domain Rating. Switch between them below.', center=True),
            group(shortcode('[sb_packages service="off-page-seo"]'), align='wide', layout='flow'),
            para('<a href="/services/off-page-seo/">How our link building works →</a>', 'sb-center sb-card__more'),
            cls='sb-section--soft'),
    section(head('How it works', 'From order to delivery in four steps', None, center=True), steps(HOW_STEPS),
            para('<a href="/how-it-works/">Read the full process, including revisions and refunds →</a>', 'sb-center sb-card__more')),
    section(columns(
        column(eyebrow('Why SEO Booster'), heading('Transparent work you can check'),
               lead('Most SEO and web work is sold on promises. We sell defined deliverables instead, so you always know what you paid for and can verify it yourself.'),
               ul(['<strong>Fixed prices</strong> shown on every package.',
                   '<strong>Written scope</strong>: what is included, what is not, and what we need from you.',
                   '<strong>Reports you can check</strong>: live link URLs, audit findings, before/after measurements.',
                   '<strong>Revisions included</strong> where listed, and replacements for links that are not live at delivery.'], 'sb-ticks'),
               width='55%'),
        column(group(heading('What we will never do', 3),
                     ul(['Promise rankings or traffic. No one controls Google.',
                         'Use private blog networks (PBNs) or hacked sites.',
                         'Ask for your passwords. We use user invites.',
                         'Lock you into long contracts or hidden renewals.'], 'sb-crosses'),
                     cls='sb-panel', layout='flow'), width='45%'),
        cls='sb-split', center=True), cls='sb-section--blue'),
    section(head('Insights', 'Guides to help you spend wisely'), query_posts(3),
            para('<a href="/insights/">All insights →</a>', 'sb-card__more')),
    section(head('FAQ', 'Common questions', None, center=True), faq([
        ('How quickly will I see results from SEO?', 'Deliverables arrive within the turnaround on each package. Search results take longer and depend on your site, competition and Google. Most sites see movement over weeks to months, which is why we never promise rankings.'),
        ('What happens after I pay?', 'You receive an order confirmation, then complete a short brief in your account. Work starts once the brief is complete, and the turnaround clock starts then.'),
        ('Can I get something custom?', 'Yes. Use the <a href="/get-a-quote/">quote form</a> and we will reply with a fixed scope and price before you commit.'),
        ('Do you need access to my website?', 'Only for services that change your site. We ask you to invite us as a user, and you can remove the access when we are done. Never send passwords.'),
        ('What is your refund policy?', 'If we have not started, you get a full refund. Once work has started, refunds depend on what has been delivered. See the <a href="/refund-policy/">refund policy</a>.'),
    ]), para('<a href="/faq/">More answers →</a>', 'sb-center sb-card__more')),
    cta('Ready to boost your site?', 'Choose a fixed-price package now, or tell us what you need and get a clear quote.'),
)
page('home', 'Home', home, 'Fixed-price SEO, link building, website, content and design services with clear deliverables, stated turnaround and reports you can check.')

# ================================================================ SERVICES HUB
hub_groups = [
    ('SEO services', 'Get found on Google, in Maps and in AI answers, with work you can check.', ['monthly-seo', 'local-seo', 'off-page-seo', 'seo-audit', 'technical-seo', 'on-page-seo', 'ecommerce-seo', 'ai-seo', 'white-label-seo', 'seo-consultancy']),
    ('Websites &amp; ecommerce', 'Build it properly, move it safely, then keep it fast and secure.', ['website-development', 'ecommerce-website-development', 'website-maintenance', 'website-migration']),
    ('Paid ads &amp; social media', 'Reach buyers now with ads, and stay visible with consistent social content.', ['ppc-management', 'facebook-ads', 'tiktok-ads', 'social-media-management']),
    ('Content &amp; creative', 'Words and visuals that explain what you do and why it matters.', ['content-writing', 'graphic-design']),
]
hub = join(
    page_hero('art-services.svg', 'Illustration of a service menu and package card', eyebrow('Services'), heading('Services with clear scope and fixed prices', 1),
          lead('Choose a service to see its packages, what is included and how we work. Not sure where to start? An <a href="/services/seo-audit/">SEO audit</a> tells you what will make the biggest difference.'),
          buttons(('See all packages', '/packages/'), ('Get a quote', '/get-a-quote/', 'outline'))),
    *[section(head(eb, title, sub), group(*[svc_card(s) for s in slugs], align='wide', layout='flow', cls='sb-grid sb-grid--4' if len(slugs) % 4 == 0 else 'sb-grid sb-grid--3'),
              cls='sb-section--soft' if i % 2 else '') for i, (title, sub, slugs) in enumerate(hub_groups) for eb in ['']],
    section(head('Custom projects', 'Quoted services', 'Available as custom projects. Tell us what you need and we will send a fixed quote.'),
            group(card('Analytics &amp; tracking', 'GA4 and Google Tag Manager audits, setup and conversion tracking, with consent built in.'),
                  card('Email marketing', 'Templates, automations and campaign management on your existing email platform.'),
                  card('Marketing automation', 'Workflow audits and builds that connect your forms, CRM and email.'),
                  align='wide', layout='flow', cls='sb-grid sb-grid--3'),
            buttons(('Request a quote', '/get-a-quote/')), cls='sb-section--blue'),
    cta(),
)
page('services', 'Services', hub, 'SEO services, local SEO, link building, website development, ecommerce, PPC, social media, content and design, all with fixed-price packages you can order online.', menu_order=1)

# ================================================================ SERVICE PAGES
def service_page(slug, eb, h1, sub, checks, for_list, not_for, pk_title, pk_sub, features, process, needs, faqs, related, extra=None, title=None, excerpt=''):
    s = SVC[slug]
    content = join(
        hero(eb, h1, sub, [('See packages', '#packages'), ('Get a quote', f'/get-a-quote/?service={slug}', 'outline')], checks,
             art_file(s), f'Illustration for {s[2].replace("&amp;", "and")}', crumbs=True),
        section(columns(
            column(group(heading('Who it is for', 3), ul(for_list, 'sb-ticks'), cls='sb-card', layout='flow')),
            column(group(heading('Not the right fit if…', 3), ul(not_for, 'sb-crosses'), cls='sb-card', layout='flow')),
        ), cls='sb-section--tight'),
        section(head('Packages', pk_title, pk_sub, center=True),
                group(shortcode(f'[sb_packages service="{s[1]}"]'), align='wide', layout='flow'),
                para('Need a bigger or custom order? <a href="/get-a-quote/">Ask for a quote</a>.', 'sb-center sb-muted'),
                cls='sb-section--soft', anchor='packages'),
        section(columns(column(eyebrow('The basics'), heading(WHATIS[slug][0]), width='40%'),
                        column(*[para(x) for x in WHATIS[slug][1]], width='60%'), cls='sb-split sb-whatis')),
        proof(*DELIVER[slug]),
        section(head('What you get', 'Included in every order', None),
                group(*[card(t, d, FEATURE_ICONS[i % len(FEATURE_ICONS)] if i else s[3]) for i, (t, d) in enumerate(features)], align='wide', layout='flow', cls='sb-grid sb-grid--3'), cls='sb-section--soft'),
        extra or '',
        section(head('Process', 'How we deliver', None, center=True), steps(process)),
        section(columns(
            column(eyebrow('Before we start'), heading('What we need from you'),
                   para('When you choose a package you add these on the order page, before checkout, so we can start straight after payment. Never include passwords. We will ask for a user invite if access is needed.'),
                   width='45%'),
            column(group(ul(needs, 'sb-ticks'), cls='sb-panel', layout='flow'), width='55%'),
            cls='sb-split', center=True)),
        section(head('FAQ', f'{(title or s[2])}: questions', None, center=True), faq(faqs), cls='sb-section--blue'),
        section(head('Related', 'Often ordered together', None),
                group(*[svc_card(r) for r in related], align='wide', layout='flow', cls='sb-grid sb-grid--3')),
        cta(),
    )
    page(slug, (title or s[2]).replace('&amp;', '&'), content, excerpt, parent='services', menu_order=SERVICES.index(s) + 1)


service_page('off-page-seo', 'Off-page SEO',
    'Link building services and off-page SEO, done by hand and proven with live URLs',
    'Build the authority signals search engines and customers look for: consistent business listings, quality profile links, and guest posts on real websites grouped by Domain Rating.',
    ['From [sb_from service="off-page-seo"]', 'Manual submissions, no bots', 'Spreadsheet report of every live URL'],
    ['New websites that need a foundation of trusted links and listings', 'Local businesses that need consistent name, address and phone data', 'Established sites ready for editorial links on stronger domains', 'Agencies that need reliable white-label fulfilment'],
    ['You want guaranteed rankings or a set number of "dofollow" links', 'Your site has unresolved technical problems (start with an <a href="/services/seo-audit/">audit</a>)', 'You need links from one specific named website', 'Your niche is gambling, adult or other restricted topics'],
    'Two groups. Choose your level.',
    '<strong>Profiles &amp; Citations</strong> build a broad, consistent foundation. <strong>Premium Links</strong> are guest posts on established sites by Domain Rating (DR), plus press releases.',
    [('Manual creation', 'Every listing, profile and outreach email is done by a person, never by submission software.'),
     ('Relevant categories', 'We choose directories and profiles that fit your industry and country where they exist.'),
     ('Consistent NAP data', 'Your business name, address and phone are entered identically everywhere, which is what citation sources check.'),
     ('Live-URL report', 'A spreadsheet with every placement URL, so you can check each one yourself.'),
     ('Free replacements', 'Profile links not live at delivery are replaced. Guest posts removed within 90 days are replaced.'),
     ('Disclosure where required', 'Publishers that label sponsored content keep doing so. We do not hide paid placements.')],
    [('Brief', 'You send your URL, business details, keywords and niche.'), ('Plan', 'We match platforms or publishers to your niche and DR tier.'),
     ('Build', 'Listings, profiles and articles are created and checked by hand.'), ('Report', 'You receive a spreadsheet of live URLs within the turnaround.')],
    ['Website URL and the pages to link to', 'Business name, address and phone (or "online only")', 'Main keywords or topics for anchor text', 'A short business description and category', 'An email address you control, for listing verification'],
    [('What is the difference between citations, profile links and guest posts?', 'Citations are business listings with your name, address and phone, mainly a local SEO trust signal. Profile links come from accounts on established platforms. Guest posts are articles on other websites with a contextual link to you. Our guide <a href="/citations-vs-profile-backlinks/">explains when each one helps</a>.'),
     ('Are the links dofollow?', 'Some are and some are not. Each platform and publisher decides. A natural link profile contains both, so we never sell "dofollow only" packages.'),
     ('What does DR mean?', 'Domain Rating is an Ahrefs score from 0 to 100 estimating a site\'s link strength. Your guest post is placed on a site at or above the DR tier you order, measured on the day of publishing.'),
     ('Will this improve my rankings?', 'Links are one of many ranking factors, and results depend on your site, content and competition. We guarantee the deliverables, not rankings.'),
     ('Is this safe? I have heard links can cause penalties.', 'Google penalises manipulative link schemes such as PBNs, automated spam and hidden paid links. We use real platforms and real publishers, and keep sponsored labels where publishers require them.'),
     ('Can I choose the anchor text?', 'Yes. Add your preferences to the brief. We mix branded, natural and partial-match anchors to keep your profile natural.')],
    ['seo-audit', 'technical-seo', 'content-writing'],
    extra=section(head('Compare', 'Which link type do you need?', None),
                  table(['', 'Citations &amp; profiles', 'Guest posts (DR tiers)', 'Press release'],
                        [['Best for', 'Foundations, local SEO, new sites', 'Authority for competitive pages', 'Launches and company news'],
                         ['Link type', 'Listing or profile page', 'Contextual link inside an article', 'Links in distributed news'],
                         ['Price range', 'From [sb_from service="off-page-seo" group="profiles-and-citations"]', 'From [sb_from service="off-page-seo" group="premium-links"]', 'See packages'],
                         ['Delivery', '3 to 14 working days', '7 to 14 working days', '5 to 7 working days'],
                         ['Report', 'All live URLs', 'Live URL plus DR when published', 'Distribution report']]),
                  cls='sb-section--tight'),
    title='Off-Page SEO', excerpt='Manual link building: business citations, profile backlinks, guest posts by Domain Rating and press releases, with a live-URL report.')

service_page('seo-audit', 'SEO audit',
    'SEO audit service: find out exactly what is holding your site back',
    'A clear, prioritised audit of your site\'s technical health, on-page SEO and content, written in plain English with the fix for every issue, so you or your developer can act on it.',
    ['From [sb_from service="seo-audit"]', 'Prioritised by impact', 'Plain-English PDF report'],
    ['Site owners who are not sure why traffic is flat or falling', 'Businesses about to invest in content or links', 'Anyone redesigning or migrating a website', 'Agencies needing a second opinion'],
    ['You want us to implement the fixes in the same order (see <a href="/services/technical-seo/">Technical SEO</a>)', 'Your site has more than 500 pages (ask for an enterprise quote)', 'You need a guarantee of rankings after fixing'],
    'Pick the depth you need',
    'The quick review covers technical basics. The full audit adds content, keywords, internal links, backlinks and competitors.',
    [('Full crawl', 'We crawl your site like a search engine to find errors, redirects, duplicates and orphan pages.'),
     ('Indexing check', 'What Google can and cannot index, sitemaps, robots rules and canonical tags.'),
     ('Speed &amp; mobile', 'Core Web Vitals lab tests and mobile usability, with the causes of slow pages.'),
     ('On-page review', 'Titles, descriptions, headings and structured data on your key pages.'),
     ('Priority list', 'Every issue rated high, medium or low, so you fix what matters first.'),
     ('Walkthrough', 'The full audit includes a 30-minute call to go through the findings.')],
    [('Brief', 'You share your URL, goals and competitors.'), ('Crawl &amp; review', 'We run the crawl and review the findings manually.'),
     ('Write-up', 'Each issue is explained with its impact and the fix.'), ('Deliver', 'You get the PDF and can ask questions about any point.')],
    ['Website URL', 'Google Search Console access via a user invite (recommended)', 'Your main goals and target market', 'Two or three competitors you watch'],
    [('How long does an audit take?', 'The quick review is delivered in 2 to 3 working days and the full audit in 4 to 6, after we receive your brief.'),
     ('Do I need to give you access?', 'Search Console access makes the audit more accurate but is optional. We never need your passwords.'),
     ('Will you fix the issues?', 'The audit tells you what to fix and how. If you want us to do it, our <a href="/services/technical-seo/">Technical SEO</a> packages cover implementation.'),
     ('Is this an automated report?', 'We use crawling tools to collect data, but every finding is reviewed and written up by a person.')],
    ['technical-seo', 'off-page-seo', 'content-writing'],
    excerpt='Prioritised SEO audits in plain English: technical health, indexing, speed, on-page SEO and a fix for every issue.')

service_page('technical-seo', 'Technical SEO',
    'Technical SEO services that fix what search engines trip over',
    'We fix the issues that quietly hold sites back, including broken links, redirect chains, indexing errors, missing structured data and slow pages, and show you the before and after.',
    ['From [sb_from service="technical-seo"]', 'Backup before every change', 'Before/after report'],
    ['Sites with an audit and a list of fixes to implement', 'WordPress, WooCommerce and Shopify sites that load slowly', 'Sites with indexing or duplicate-content problems', 'Owners who want ongoing technical upkeep'],
    ['You need a full redesign or new features', 'You want a guaranteed PageSpeed score (real-user data depends on your visitors)', 'Your hosting cannot be changed and is the main bottleneck'],
    'Fix it once, or keep it healthy',
    'A one-off fix bundle, a Core Web Vitals optimisation, or a month of ongoing technical SEO.',
    [('Indexing &amp; crawl fixes', 'Robots rules, sitemaps, canonicals, noindex mistakes and orphan pages.'),
     ('Redirects &amp; broken links', 'Redirect chains collapsed, 404s fixed or redirected properly.'),
     ('Structured data', 'Accurate schema for your business, products and articles where it is eligible.'),
     ('Speed optimisation', 'Image compression, caching and script loading tuned for Core Web Vitals.'),
     ('Safe changes', 'Full backup before work, and changes tested on key pages.'),
     ('Change log', 'A written list of every change, with before/after measurements.')],
    [('Review', 'We confirm the issues to fix from your audit or our own check.'), ('Backup', 'A full backup is taken before any change.'),
     ('Fix &amp; test', 'Changes are made and tested on key templates.'), ('Report', 'You get the change log and before/after results.')],
    ['Website URL and platform', 'Admin access via a user invite', 'Search Console access (recommended)', 'Your audit, if you already have one'],
    [('Can you guarantee a 100 PageSpeed score?', 'No. Lab scores depend on your theme, plugins and hosting, and Google uses real-user data. We report honest before/after lab measurements.'),
     ('Which platforms do you work on?', 'Mainly WordPress and WooCommerce. We also handle common fixes on Shopify and other platforms. Ask if you are unsure.'),
     ('What if something breaks?', 'We back up before working and fix anything our changes cause at no cost.'),
     ('Is the monthly plan a subscription?', 'No. It covers one month. Order again whenever you need another month, with no automatic renewals.')],
    ['seo-audit', 'website-maintenance', 'off-page-seo'],
    excerpt='Technical SEO fixes for indexing, redirects, structured data and Core Web Vitals, with backups and a before/after report.')

service_page('website-development', 'Website development',
    'Website design and development services at a fixed price',
    'From a single landing page to a 10-page business site, built on WordPress so you can edit it yourself, with your content added and SEO basics set up from day one.',
    ['From [sb_from service="website-development"]', 'Mobile-friendly and fast', 'Edit it yourself after handover'],
    ['New businesses that need a credible website quickly', 'Owners replacing an outdated or slow site', 'Campaigns that need a focused landing page', 'Service businesses with 2 to 10 core pages'],
    ['You need a complex web app, booking system or custom integrations (ask for a quote)', 'You want an online shop with many products (ask about ecommerce)', 'You have no content and no time to provide it (add copywriting)'],
    'Choose your number of pages',
    'Every plan includes responsive design, your content added, a contact form, basic SEO and a handover video.',
    [('Responsive design', 'Looks right on phones, tablets and desktops, and is tested at common screen sizes.'),
     ('Your content added', 'We add your text, logo and images, formatted properly.'),
     ('Contact form', 'Connected to your email with spam protection.'),
     ('SEO basics', 'Titles, meta descriptions, headings, sitemap and clean URLs.'),
     ('Speed basics', 'Optimised images and caching for fast loading.'),
     ('Handover video', 'A recorded walkthrough showing how to edit your pages.')],
    [('Brief', 'You share pages, content and websites you like.'), ('Design', 'We build the homepage first for your feedback.'),
     ('Build', 'Remaining pages are built and content added.'), ('Launch', 'We go live, test everything and hand over.')],
    ['Logo and brand colours', 'Text for each page (or order <a href="/services/content-writing/">copywriting</a>)', 'Hosting and domain access via a user invite', 'Two or three websites you like'],
    [('Is hosting included?', 'No. You keep ownership of your hosting and domain. We can recommend options and set them up.'),
     ('Can I update the site myself?', 'Yes. Sites are built in WordPress with a standard editor, and you get a handover video.'),
     ('How many revisions do I get?', 'Two rounds of design revisions are included. Extra changes can be quoted.'),
     ('Do you write the content?', 'You supply the text, or add our content writing service for professionally written pages.'),
     ('What about an online shop?', 'Small WooCommerce shops can be quoted. <a href="/get-a-quote/">Tell us what you sell</a>.')],
    ['website-maintenance', 'content-writing', 'graphic-design'],
    excerpt='WordPress website design and development packages: 1, 2, 5 and 10 pages with responsive design, SEO basics and handover.')

service_page('website-maintenance', 'Website maintenance',
    'Website maintenance services and WordPress fixes, handled by a developer',
    'Something broken? Get a one-off fix. Want it to stay working? Choose a month of care with updates, backups, monitoring and small changes included.',
    ['From [sb_from service="website-maintenance"]', 'Backup before every fix', 'Written summary of what changed'],
    ['WordPress sites showing errors, white screens or broken layouts', 'Owners who do not have time for updates and backups', 'Sites that need small content or design changes regularly', 'Anyone worried about plugin conflicts after updates'],
    ['Your site needs a full rebuild (see <a href="/services/website-development/">Website Development</a>)', 'The problem is caused by your hosting company and they will not fix it', 'You need 24/7 emergency cover'],
    'Fix it now, or keep it maintained',
    'Diagnosis, single fixes and bundles for problems today, plus Basic and Growth care for ongoing peace of mind.',
    [('Developer diagnosis', 'A WordPress developer finds the real cause, not just the symptom.'),
     ('Backup first', 'A full backup is taken before any change.'),
     ('Updates done safely', 'Plugins, theme and core updated with checks afterwards (care plans).'),
     ('Uptime monitoring', 'We are alerted if your site goes down (care plans).'),
     ('Small changes', 'Care plans include time for content and layout tweaks.'),
     ('Clear summary', 'A plain-English note of what was wrong and what we changed.')],
    [('Report', 'You describe the problem or your needs in the brief.'), ('Access', 'You invite us as a user, never sharing passwords.'),
     ('Fix', 'We back up, fix and test.'), ('Summary', 'You get a written summary and we check it stays fixed.')],
    ['Website URL', 'Description and screenshots of the problem', 'Admin access via a user invite', 'Hosting details, if the issue might be server-side'],
    [('How fast can you fix my site?', 'Single fixes are usually completed within 24 to 48 hours after we receive access, depending on the issue.'),
     ('What if the problem is bigger than one fix?', 'We will tell you before doing extra work, and suggest the bundle or a quote.'),
     ('Do care plans renew automatically?', 'No. Each plan covers one month. Order again when you want another month.'),
     ('Can you remove malware?', 'We assess hacked sites first, because the clean-up effort varies a lot. Order a diagnosis and we will quote the clean-up.')],
    ['technical-seo', 'website-development', 'seo-audit'],
    excerpt='WordPress fixes and monthly website care: diagnosis, single and multi-fix bundles, updates, backups and monitoring.')

service_page('content-writing', 'Content writing',
    'SEO content writing services that people actually want to read',
    'Researched blog posts and guides from 500 to 3,000 words, or a batch of articles planned as a topic cluster that supports your main service pages.',
    ['From [sb_from service="content-writing"]', 'Plagiarism-checked', 'Meta title and description included'],
    ['Businesses that need regular blog content', 'Sites building topical authority around their services', 'Agencies that need dependable writers', 'Owners who know their subject but lack time to write'],
    ['You need regulated advice written by a licensed professional (medical, legal, financial)', 'You want hundreds of near-identical pages for keyword variations', 'You expect rankings purely from word count'],
    'Single articles or batches',
    'Choose a word count for one article, or a batch of 1,000-word articles planned around one topic.',
    [('Original writing', 'Every article is written from scratch and plagiarism-checked.'),
     ('Search-aware structure', 'Clear headings, direct answers and natural keyword use.'),
     ('Meta data', 'SEO title and meta description for each article.'),
     ('Fact-checking', 'Claims are checked and sources linked where useful.'),
     ('One revision', 'A free revision round to match your voice.'),
     ('Ready to publish', 'Delivered as a Google Doc or Word file. Publishing is available on request.')],
    [('Brief', 'Topic, audience, keywords and tone.'), ('Outline', 'For batches, we plan and agree the topic list first.'),
     ('Write', 'Research, writing and an editorial check.'), ('Deliver', 'You review and request a revision if needed.')],
    ['Topic or working title', 'Target audience and main keyword', 'Tone of voice and any examples', 'Any sources or points that must be included'],
    [('Do you use AI to write?', 'Our writers may use tools for research and outlines, but every article is written, edited and fact-checked by a person. Tell us in your brief if you need a no-AI process.'),
     ('Will the content rank?', 'Good content is necessary but not sufficient. Rankings also depend on your site authority and competition. We write to match search intent and answer real questions.'),
     ('Can you write in my brand voice?', 'Yes. Share examples and we will match them. The free revision helps fine-tune it.'),
     ('Who owns the content?', 'You do, once the order is paid. Publish it wherever you like.')],
    ['off-page-seo', 'seo-audit', 'graphic-design'],
    excerpt='SEO content writing: original, researched 500 to 3,000-word articles and topic-cluster batches with meta data included.')

service_page('graphic-design', 'Graphic design',
    'Graphic design and branding packages, ready to use',
    'Social media graphics and ad creatives sized for each platform, plus mini brand kits and full identities with the files and guidelines you need to stay consistent.',
    ['From [sb_from service="graphic-design"]', 'Your colours and fonts', 'Source files available'],
    ['Businesses posting on social media every week', 'New brands that need a logo and visual identity', 'Brands with a dated logo that needs a refresh', 'Advertisers that need fresh ad creatives'],
    ['You need video, animation or 3D work', 'You want unlimited concepts and revisions', 'You need trademark searches or registration'],
    'Social creatives and branding',
    'Packs of 1 to 10 social graphics, or a brand kit, refresh or full identity.',
    [('Custom design', 'Made for your brand, not a recoloured template.'),
     ('Platform sizes', 'Sized correctly for Instagram, Facebook, LinkedIn and X.'),
     ('Brand consistency', 'Your colours, fonts and logo used correctly every time.'),
     ('Revisions included', 'Two rounds on graphics and three on branding.'),
     ('Usable files', 'PNG/JPG for posting, and vector files for branding.'),
     ('Licensed assets', 'Only images you supply or that are licensed for commercial use.')],
    [('Brief', 'Formats, text, brand assets and references.'), ('Concepts', 'First designs for your feedback.'),
     ('Refine', 'Revisions within your allowance.'), ('Deliver', 'Final files in the formats you need.')],
    ['Logo and brand colours (if you have them)', 'Text for each graphic', 'Platforms and sizes', 'Styles you like and dislike'],
    [('Do I own the designs?', 'Yes. Once paid, you own the final designs. Stock elements remain under their own licences.'),
     ('Can I get the editable source file?', 'Branding packages include vector files. For social graphics, ask in your brief.'),
     ('Do you write the captions?', 'Captions are not included, but our <a href="/services/content-writing/">content writers</a> can help.'),
     ('How many logo concepts do I get?', 'Two with the Mini Brand Kit and three with Full Brand Identity.')],
    ['website-development', 'content-writing', 'off-page-seo'],
    excerpt='Graphic design packages: social media graphics, ad creatives, mini brand kits, brand refreshes and full brand identities.')

# ---------------------------------------------------------------- new services (tools/services_new.py)
for n in NEW_SERVICES:
    pg = n['page']
    WHATIS[n['slug']] = pg['whatis']
    DELIVER[n['slug']] = pg['deliver']
    SEO_TITLES[n['slug']] = pg['seo_title']
    service_page(n['slug'], pg['eb'], pg['h1'], pg['sub'], pg['checks'], pg['for_'], pg['not_for'], pg['pk_title'], pg['pk_sub'],
                 pg['features'], pg['process'], pg['needs'], pg['faqs'], pg['related'], title=n['name'], excerpt=pg['excerpt'])

# ================================================================ PACKAGES
packages = join(
    page_hero('art-packages.svg', 'Illustration of three package cards', eyebrow('Packages'), heading('All packages and prices', 1),
          lead('Every package in one place, with what is included, the turnaround and the revisions. Pick a package, add your project details and check out in minutes.'),
          ul([f'<a href="#{s[0]}">{s[2]}</a>' for s in SERVICES], 'sb-jump')),
    *[section(head('', s[2], s[5]), group(shortcode(f'[sb_packages service="{s[1]}"]'), align='wide', layout='flow'),
              para(f'<a href="/services/{s[0]}/">More about {s[2]} →</a>', 'sb-card__more'),
              cls='sb-section--soft' if i % 2 else '', anchor=s[0]) for i, s in enumerate(SERVICES)],
    cta('Need a custom package?', 'Larger volumes, combined services or something not listed. Tell us what you need.'),
)
page('packages', 'Packages', packages, 'All SEO Booster packages and prices in one place: link building, audits, technical SEO, websites, maintenance, content and design.', menu_order=2)

# ================================================================ HOW IT WORKS
how = join(
    page_hero('art-process.svg', 'Illustration of four connected steps', eyebrow('How it works'), heading('A simple, transparent process', 1),
          lead('Buying a service should be as clear as buying a product. Here is exactly what happens from order to delivery.')),
    section(steps(HOW_STEPS)),
    section(columns(
        column(eyebrow('After you pay'), heading('Your order, step by step'),
               para('You can follow your order in <a href="/my-account/">your account</a>. These are the stages you will see:'), width='45%'),
        column(table(['Status', 'What it means'], [
            ['Paid – awaiting brief', 'Payment received. Please complete your brief so we can start.'],
            ['Brief received', 'We have everything we need and your order is queued.'],
            ['In progress', 'Work has started. The turnaround clock is running.'],
            ['Client review', 'Your delivery is ready to check. Request revisions if included.'],
            ['Delivered', 'Final delivery sent: report, files or live URLs.'],
            ['Completed', 'Order closed.']]), width='55%'),
        cls='sb-split'), cls='sb-section--soft'),
    section(head('Good to know', 'Turnaround, revisions and payments'),
            group(card('Turnaround', 'Shown on every package in working days. The clock starts when your brief is complete, not at payment.', 'scope'),
                  card('Revisions', 'Included where listed on the package. Revisions refine the agreed scope and do not add new deliverables.', 'human'),
                  card('Reports', 'Every order ends with proof: live URLs, an audit PDF, a change log or source files.', 'report'),
                  card('Payments', 'Secure checkout with card, PayPal or bank transfer, depending on the options shown at checkout.', 'shield'),
                  align='wide', layout='flow', cls='sb-grid sb-grid--4')),
    section(head('FAQ', 'Process questions', None, center=True), faq([
        ('Do I need an account?', 'Yes. An account is created at checkout so you can complete your brief, follow your order and download files securely.'),
        ('What if I do not complete my brief?', 'We send reminders. Work cannot start without it, and the turnaround starts when the brief is complete.'),
        ('Can I change my order after paying?', 'Contact us before work starts and we will adjust it or refund the difference.'),
        ('How do refunds work?', 'Full refund before work starts, partial after. See the <a href="/refund-policy/">refund policy</a>.')]), cls='sb-section--blue'),
    cta(),
)
page('how-it-works', 'How It Works', how, 'How ordering works at SEO Booster: choose a package, pay securely, send your brief and receive your delivery with a report.', menu_order=3)

# ================================================================ ABOUT
about = join(
    page_hero('art-about.svg', 'Illustration of a growth report and delivery checklist', eyebrow('About'), heading('SEO and web services, sold the honest way', 1),
          lead('SEO Booster sells clearly defined SEO, website, content and design services at fixed prices, so small businesses and agencies can buy expert help without guesswork.')),
    section(columns(
        column(eyebrow('Why we exist'), heading('Most buyers cannot see what they are paying for'),
               para('SEO and web services are often sold as monthly retainers with vague deliverables and big promises. It is hard to know what was done, whether it was worth it, or what to ask for next.'),
               para('We take the opposite approach: small, fixed-scope packages with the deliverables written down, a stated turnaround and a report you can check. If something is not listed, it is not included, and if you need something different, we quote it first.'),
               width='55%'),
        column(image('hero-growth.svg', 'Illustration of a growth chart and link network'), width='45%'),
        cls='sb-split', center=True)),
    section(columns(
        column(image('team/zain-malik.webp', 'Zain Malik, founder of SEO Booster', 'sb-founder__photo'), width='38%'),
        column(eyebrow('Meet the founder'), heading('Zain Malik'), para('Founder — SEO, Web &amp; eCommerce Expert', 'sb-founder__role'),
               para('Zain is the founder of SEO Booster UK, with more than 10 years of experience in SEO, website development and eCommerce strategy. He helps businesses grow online with data-driven, results-focused solutions.'),
               para('He started SEO Booster with a simple idea: buying SEO, website and design work should feel as clear as buying anything else online. You should know what you are getting, what it costs, when it arrives and how to check it was done.'),
               para('That idea shapes everything here, from fixed-price packages with written deliverables to live-URL reports and plain-English audits. Zain also writes our <a href="/insights/">Insights</a> guides, so business owners can make better decisions about search and marketing, whether or not they buy from us.'),
               buttons(('Read Zain\'s guides', '/insights/'), ('Talk to us', '/contact/', 'outline')), width='62%'),
        cls='sb-split sb-founder', center=True), anchor='founder', cls='sb-section--blue'),
    section(head('Principles', 'How we work', None, center=True),
            group(card('Clarity over promises', 'We describe what we will deliver, not what Google will do. No ranking guarantees, ever.', 'scope'),
                  card('Proof of work', 'Every order ends with something you can verify: URLs, reports, files or a change log.', 'report'),
                  card('People, not bots', 'Submissions, outreach, writing and fixes are done and checked by people.', 'human'),
                  card('Safe by default', 'Search-engine-safe methods, backups before changes, and no password sharing.', 'shield'),
                  align='wide', layout='flow', cls='sb-grid sb-grid--4'), cls='sb-section--soft'),
    section(columns(
        column(eyebrow('Who we help'), heading('Built for small teams and agencies'), width='45%'),
        column(ul(['<strong>Small and local businesses</strong> that need visibility without a long contract.',
                   '<strong>Ecommerce stores</strong> that need technical fixes, content and links.',
                   '<strong>Agencies and freelancers</strong> that need reliable fulfilment they can resell.',
                   '<strong>Founders</strong> launching a new site who need the foundations done right.'], 'sb-ticks'), width='55%'),
        cls='sb-split', center=True)),
    cta('Let us talk about your website', 'Ask a question, request a quote or go straight to the packages.', (('Contact us', '/contact/'), ('Browse packages', '/packages/', 'outline'))),
)
page('about', 'About', about, 'About SEO Booster: fixed-scope SEO, website, content and design services with clear deliverables and honest reporting.', menu_order=4)

# ================================================================ CONTACT + QUOTE
contact = join(
    page_hero('art-contact.svg', 'Illustration of an envelope and chat messages', eyebrow('Contact'), heading('Get in touch', 1),
          lead('Questions about a package, an order or a custom project? Send a message and we will reply by email.')),
    section(columns(
        column(shortcode('[sb_lead_form type="contact"]'), width='60%'),
        column(group(heading('Other ways to reach us', 3),
                     ul(['Email: <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>',
                         'Existing order? Reply from <a href="/my-account/">your account</a> or quote your order number.',
                         'Want a price for a custom project? Use the <a href="/get-a-quote/">quote form</a>.'], 'sb-ticks'),
                     cls='sb-panel', layout='flow'),
               group(heading('Before you write', 3), para('Never send passwords by email or form. If we need access to a website or account, we will ask you to invite us as a user.'),
                     cls='sb-panel', layout='flow'), width='40%'),
        cls='sb-split')),
)
page('contact', 'Contact', contact, 'Contact SEO Booster about packages, orders or custom SEO, website, content and design projects.', menu_order=6)

quote = join(
    page_hero('art-quote.svg', 'Illustration of a request form and a quote', eyebrow('Free quote'), heading('Get a fixed quote', 1),
          lead('Tell us what you need. We will reply with a clear scope, turnaround and price, and you decide whether to go ahead. No obligation.')),
    section(columns(
        column(shortcode('[sb_lead_form type="quote"]'), width='60%'),
        column(group(heading('What happens next', 3),
                     ul(['We review your request and website.', 'You receive a written scope and fixed price by email.', 'If you accept, we send a secure payment link.', 'Work starts once your brief is complete.'], 'sb-ticks'),
                     cls='sb-panel', layout='flow'),
               group(heading('Prefer to buy now?', 3), para('Most services have fixed-price packages you can order straight away.'), buttons(('Browse packages', '/packages/')),
                     cls='sb-panel', layout='flow'), width='40%'),
        cls='sb-split')),
)
page('get-a-quote', 'Get a Quote', quote, 'Request a free, fixed quote for SEO, link building, websites, maintenance, content or design work.', menu_order=7)

# ================================================================ FAQ
faq_page = join(
    page_hero('art-faq.svg', 'Illustration of questions and answers', eyebrow('FAQ'), heading('Frequently asked questions', 1),
          lead('Answers about ordering, payments, delivery and our methods. Cannot find yours? <a href="/contact/">Ask us</a>.')),
    section(heading('Ordering &amp; payment'), faq([
        ('Which currency are prices in?', 'Prices are shown in [sb_currency]. Your bank or payment provider may convert the amount to your own currency.'),
        ('How do I pay?', 'At checkout, using the payment options shown there. We never see or store your card details.'),
        ('Do I get an invoice?', 'Yes. Your order confirmation email works as a receipt, and you can view all orders in your account.'),
        ('Can I order several packages at once?', 'Yes. Add them to your cart and check out once. You complete one brief per order.')]),
        heading('Delivery &amp; revisions'), faq([
        ('When does the turnaround start?', 'When your brief is complete. Turnaround is in working days (Monday to Friday).'),
        ('What if I need changes?', 'Revisions are included where listed on the package. Ask for them from your order page or by replying to our delivery email.'),
        ('How will I receive my delivery?', 'By email and in your account: a report, files or a list of live URLs, depending on the service.')]),
        heading('Methods &amp; safety'), faq([
        ('Do you guarantee rankings?', 'No. No honest provider can, because rankings depend on Google and your competitors. We guarantee the deliverables listed on each package.'),
        ('Are your link building methods safe?', 'We use real platforms and real publishers, not PBNs or automated spam, and we keep sponsored labels where publishers require them.'),
        ('Will you need my passwords?', 'Never. For website work, invite us as a user and remove the access when we are done.'),
        ('Is my data safe?', 'We only collect what we need to deliver your order. See our <a href="/privacy-policy/">privacy policy</a>.')]),
        heading('Refunds'), faq([
        ('Can I get a refund?', 'Yes, in full before work starts. After that, refunds depend on what has been delivered. See the <a href="/refund-policy/">refund policy</a>.'),
        ('What if a link disappears?', 'Profile links not live at delivery are replaced, and guest posts removed within 90 days are replaced free of charge.')]),
        tag='section', cls='sb-faq-page'),
    cta(),
)
page('faq', 'FAQ', faq_page, 'Answers about ordering, payments, delivery, revisions, refunds and link building safety at SEO Booster.', menu_order=8)

# ================================================================ LEGAL (drafts for owner / legal review)
UPDATED = '3 November 2026'


def legal(slug, title, summary, glance, sections, excerpt, art='art-faq.svg'):
    """Legal page: hero, at-a-glance box, sticky contents, numbered sections, contact card."""
    toc = ul([f'<a href="#{a}">{i + 1}. {h}</a>' for i, (a, h, _) in enumerate(sections)], 'sb-toc')
    body = []
    for i, (a, h, blocks) in enumerate(sections):
        body.append(heading(f'<span>{i + 1:02d}</span> {h}', 2, 'sb-legal__h', anchor=a))
        body.extend(blocks)
    content = join(
        page_hero(art, '', eyebrow('Legal'), heading(title, 1), lead(summary),
                  ul([f'Last updated: {UPDATED}', 'Applies to orders on seobooster.uk', 'Plain-English summary first'], 'sb-checks')),
        section(columns(
            column(group(heading('On this page', 3), toc, cls='sb-legal__toc', layout='flow'), width='30%', cls='sb-legal__aside'),
            column(group(para('<strong>Draft under review.</strong> This document is being checked by a legal adviser before launch, and our company registration details will be added. If anything is unclear, email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>.'), cls='sb-notice', layout='flow'),
                   group(heading('At a glance', 3), ul(glance, 'sb-ticks'), cls='sb-panel sb-legal__glance', layout='flow'),
                   group(*body, cls='sb-legal__body', layout='flow'),
                   group(heading('Questions about this policy?', 3), para('Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> with your question and, if it is about an order, your order number. A real person will reply.'),
                         buttons(('Contact us', '/contact/'), ('Read our FAQ', '/faq/', 'outline')), cls='sb-card sb-legal__contact', layout='flow'),
                   width='70%'),
            cls='sb-legal')),
    )
    page(slug, title, content, excerpt, template='landing', menu_order=20)


legal('terms', 'Terms of Service',
      'The agreement between you and SEO Booster when you buy one of our services. We have kept it as short and plain as we can.',
      ['You buy a fixed package with a written scope. Anything not listed is not included.',
       'Delivery times start once we have your project details.',
       'We never guarantee rankings, traffic or "dofollow" links. We do guarantee the listed deliverables.',
       'You can cancel for a full refund before work starts.',
       'You own the final work once it is paid for.'],
      [('about', 'About these terms', [para('These terms apply when you order a service from SEO Booster ("we", "us", "our") through seobooster.uk or by accepting a written quote from us. By placing an order you confirm that you have read and accepted them. If you buy for a business, you confirm you are authorised to accept them on its behalf.')]),
       ('services', 'Our services and scope', [para('Each package page lists its deliverables, what is not included, the turnaround and the revisions. That description is the scope of your order. Custom work is defined in a written quote. If you need something outside the scope, we will tell you and quote it before doing any extra work.')]),
       ('ordering', 'Placing an order', [para('When you choose a package you add your project details, then pay at checkout. Your order is accepted when payment is confirmed and you receive an order confirmation email. We may decline or refund an order if the request is unlawful, breaches search engine guidelines, or falls outside what we can deliver, for example restricted niches for link building.')]),
       ('payment', 'Prices and payment', [para('Prices are shown in [sb_currency] and include any taxes shown at checkout. Payment is taken in full when you order, unless we agree otherwise in writing. Payments are processed by our payment providers, and we never see or store your full card details. For bank transfers, work begins once the funds have arrived.')]),
       ('details', 'Your project details and access', [para('You agree to give us accurate information and anything we reasonably need to do the work. The turnaround starts when your project details are complete. Where we need access to your website or tools, you grant it by inviting us as a user. Please never send passwords by email or form. You can remove our access at any time once the work is finished.')]),
       ('delivery', 'Delivery and communication', [para('Turnaround times are in working days (Monday to Friday, excluding UK bank holidays). We will tell you promptly if something outside our control, such as a publisher delay, affects the timeline. We deliver by email and through your account, with the report, files or live URLs described in your package.')]),
       ('revisions', 'Revisions and approval', [para('Revisions are included where listed on the package. They refine the agreed work and do not add new deliverables. Please request revisions within 14 days of delivery. After that, or once you have approved the work, the order is treated as complete.')]),
       ('platforms', 'Third-party platforms and link placements', [para('Business listings, profiles, guest posts and press releases are hosted by independent third parties. They control their own sites and may edit, re-label, de-index or remove content. We choose reputable platforms and follow their rules, including sponsored labels where a publisher requires them. Replacement terms for links that disappear are stated on each package.')]),
       ('results', 'No guarantee of search results', [para('Search rankings, traffic and indexing depend on search engine algorithms, your website and your competitors, none of which we control. We do not guarantee rankings, traffic, revenue, indexing or link attributes such as "dofollow". We guarantee that we will deliver what your package describes, with reasonable skill and care.')]),
       ('content', 'Your content and responsibilities', [para('You are responsible for the information and materials you send us, and confirm you have the right to use them. You must not ask us to publish anything unlawful, misleading, defamatory or that infringes another person\'s rights. We may pause work on content that we reasonably believe breaks these rules.')]),
       ('ip', 'Ownership of the work', [para('Once your order is paid in full, you own the final deliverables we create for you, such as articles, designs and reports. Third-party elements, for example licensed fonts, stock images or plugins, remain under their own licences. We may show non-confidential work in our portfolio only with your permission.')]),
       ('cancel', 'Cancellations and refunds', [para('If you are a consumer in the UK, you normally have 14 days to cancel a service contract. If you ask us to start within that period, you agree to pay for the work done up to the point you cancel. Full details, including business orders, are in our <a href="/refund-policy/">Refund Policy</a>.')]),
       ('confidential', 'Confidentiality', [para('We keep your project details, data and unpublished material confidential and use them only to deliver your order. Our <a href="/privacy-policy/">Privacy Policy</a> explains how we handle personal data.')]),
       ('liability', 'Our liability', [para('We are responsible for losses that are a foreseeable result of us breaking these terms or failing to use reasonable care. For business customers, our total liability for any order is limited to the amount paid for that order, and we are not liable for loss of profit, revenue or business opportunity. Nothing in these terms limits liability that cannot be limited by law, or your statutory rights as a consumer.')]),
       ('changes', 'Changes, law and contact', [para('We may update these terms from time to time. The version published when you place an order applies to that order. The governing law and our registered company details will be added here before launch. Questions? Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>.')])],
      'SEO Booster terms of service: scope, ordering, payment, delivery, revisions, link placements, ownership and liability, explained in plain English.', art='art-quote.svg')

legal('refund-policy', 'Refund Policy',
      'When you can cancel, what you get back, and how to ask. Fair to you, and fair to the people doing the work.',
      ['Cancel before work starts: full refund.',
       'Cancel after work starts: refund for the work not yet done.',
       'Missing or wrong deliverables are fixed first, then refunded if we cannot fix them.',
       'Profile links not live at delivery, and guest posts removed within 90 days, are replaced free.',
       'Refunds go back to your original payment method.'],
      [('before', 'Before work starts', [para('If you cancel before we have started, you receive a full refund. Work usually starts once your project details are complete and we have confirmed the plan with you.')]),
       ('consumer', 'Your 14-day cancellation right (UK consumers)', [para('If you buy as a consumer, you can cancel within 14 days of your order. If you asked us to begin during those 14 days, we will refund the price minus the value of the work already done. If the service has been fully delivered within the 14 days at your request, the right to cancel no longer applies.')]),
       ('after-start', 'After work has started', [para('We refund the value of the work not yet done. Where deliverables are partly complete, for example 10 of 20 links placed, you keep what has been delivered and receive a refund for the rest.')]),
       ('after-delivery', 'After delivery', [para('Delivered work is not refundable simply because you changed your mind. If what we delivered does not match the package description, tell us within 14 days. We will fix or complete it first. If we cannot, we will refund the affected part.')]),
       ('replacements', 'Link replacements', [para('Profile and citation links that are not live on the day we deliver your report are replaced. Guest posts that are removed within 90 days of publication are replaced with a placement of the same tier or better. Replacements are the remedy for removed links, rather than refunds.')]),
       ('results', 'Rankings and traffic', [para('We do not guarantee rankings or traffic (see our <a href="/terms/">Terms</a>), so refunds are not available because search results did not change.')]),
       ('how', 'How to request a refund', [para('Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> with your order number and a short reason. We reply within two working days. Approved refunds are sent to your original payment method within 5 working days. Your bank may take a few more days to show it.')]),
       ('disputes', 'Before opening a dispute', [para('Please contact us first. Most problems are solved quickly by email, and a bank chargeback can take weeks for both sides.')])],
      'SEO Booster refund policy: full refund before work starts, pro-rata after, free link replacements and the UK 14-day cancellation right.', art='art-quote.svg')

legal('privacy-policy', 'Privacy Policy',
      'What personal data we collect, why, who sees it and how long we keep it, plus how to use your rights.',
      ['We only collect what we need to deliver your order and reply to you.',
       'We never sell your data or use it for third-party advertising.',
       'Card details are handled by the payment provider, not by us.',
       'You can ask to see, correct or delete your data at any time.',
       'We do not use analytics or advertising cookies at the moment.'],
      [('who', 'Who we are', [para('SEO Booster ("we") runs seobooster.uk and is the controller of the personal data described here. Our registered company details will be added before launch. Contact: <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>.')]),
       ('collect', 'What we collect', [ul(['<strong>Account and order data:</strong> name, email address, billing address, order history and payment status.',
                                          '<strong>Project details:</strong> website URLs, business name and contact details for listings, keywords, briefs and any files you upload.',
                                          '<strong>Messages:</strong> what you send through our contact and quote forms, or by email.',
                                          '<strong>Technical data:</strong> IP address and browser information in server logs, kept for security.'])]),
       ('use', 'How and why we use it', [para('We use your data to take payment and deliver your order (to perform our contract with you), to answer enquiries and keep records (our legitimate interests), to meet tax and accounting rules (legal obligation), and, only if you agree, to send occasional updates.')]),
       ('share', 'Who we share it with', [para('We share data only with the services that help us run the site and deliver your order: our payment providers, our hosting provider and our email provider. Where a service requires it, we submit your business details to third-party platforms, for example your name, address and phone number to business directories for a citations order. These are the details you asked us to publish.')]),
       ('transfers', 'International transfers', [para('Some of our providers may process data outside the UK. When they do, we rely on safeguards recognised under UK data protection law, such as adequacy regulations or standard contractual clauses.')]),
       ('retention', 'How long we keep it', [para('We keep order and invoice records for six years to meet UK tax rules. Project files and briefs are deleted or archived within 12 months of order completion, unless you ask us to keep them for future work. Contact-form messages that do not lead to an order are deleted after 24 months.')]),
       ('security', 'How we protect it', [para('The site uses HTTPS, access to customer data is limited to the people who need it, uploaded files are stored in a protected folder that cannot be opened directly from the web, and we never ask for your passwords.')]),
       ('rights', 'Your rights', [para('Under UK data protection law you can ask to access, correct, delete or receive a copy of your data, and to restrict or object to how we use it. Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> and we will reply within one month. If you are unhappy with our answer, you can complain to the Information Commissioner\'s Office (ICO) at ico.org.uk.')]),
       ('cookies', 'Cookies', [para('See our <a href="/cookie-policy/">Cookie Policy</a> for the cookies this site uses.')]),
       ('changes', 'Changes to this policy', [para('We will update this page when our practices change and show the date at the top. Significant changes will also be emailed to customers with active orders.')])],
      'SEO Booster privacy policy: what personal data we collect, why, who it is shared with, how long it is kept and your UK GDPR rights.', art='art-about.svg')

legal('cookie-policy', 'Cookie Policy',
      'The small files this website stores in your browser, what each one does, and how to control them.',
      ['We only use cookies the website needs to work, such as your cart and login.',
       'There are no analytics, advertising or tracking cookies at the moment.',
       'If we add any, we will ask for your consent first.',
       'You can delete cookies in your browser at any time.'],
      [('what', 'What cookies are', [para('Cookies are small text files that a website stores in your browser. They let the site remember things between pages, such as what is in your cart or that you are logged in.')]),
       ('essential', 'Cookies we use', [para('These are strictly necessary for the shop and your account to work, so they do not need consent:'),
                                          table(['Cookie', 'Purpose', 'Duration'], [
                                              ['woocommerce_cart_hash', 'Remembers changes to your cart', 'Session'],
                                              ['woocommerce_items_in_cart', 'Tells the site your cart has items', 'Session'],
                                              ['wp_woocommerce_session_*', 'Keeps your cart and checkout details', 'Up to 2 days'],
                                              ['wordpress_logged_in_*', 'Keeps you logged in to your account', 'Session or 14 days if you choose "remember me"'],
                                              ['wordpress_sec_*', 'Secures your login', 'Session or 14 days'],
                                              ['wordpress_test_cookie', 'Checks that your browser accepts cookies', 'Session']])]),
       ('analytics', 'Analytics and advertising', [para('We do not currently use analytics, advertising or social media tracking cookies. If we add them, we will show a consent banner first, they will stay off until you accept, and this page will be updated.')]),
       ('control', 'How to control cookies', [para('You can view and delete cookies in your browser settings. Blocking the cookies listed above will stop the cart, checkout and account from working.')])],
      'The cookies used on seobooster.uk: only essential cookies for the cart, checkout and login. No analytics or advertising tracking.', art='art-faq.svg')

legal('accessibility', 'Accessibility Statement',
      'We want everyone to be able to find a service, place an order and get help on this website.',
      ['We aim to meet WCAG 2.2 level AA.',
       'The site works with a keyboard and screen readers.',
       'Colours meet WCAG contrast ratios.',
       'Tell us about any barrier and we will fix it or help another way.'],
      [('commitment', 'Our commitment', [para('We design and build this website to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA, and we check new pages against them before they go live.')]),
       ('measures', 'What we have done', [ul(['Text and interface colours meet WCAG contrast ratios.', 'Every function works with a keyboard, with visible focus outlines.', 'Images that carry meaning have text alternatives. Decorative images are hidden from screen readers.', 'Pages use proper headings, landmarks and labelled form fields.', 'Animation is reduced when your device asks for reduced motion.', 'Text can be zoomed to 200% without losing content.'])]),
       ('limits', 'Known limitations', [para('Some parts of the site are provided by third parties, such as payment forms. We choose providers that take accessibility seriously, but we cannot fully control their components.')]),
       ('feedback', 'Feedback and help', [para('If something is hard to use, email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> with the page address and the problem. We reply within two working days and will either fix the issue or give you the information or service in another way.')]),
       ('review', 'Review', [para(f'This statement was last reviewed on {UPDATED}.')])],
      'Accessibility statement for seobooster.uk: WCAG 2.2 AA approach, measures taken, known limitations and how to get help.', art='art-contact.svg')

# ================================================================ INSIGHTS (articles, by Zain Malik)
def ext(url, label):
    return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'


def takeaways(items):
    return group(heading('Key takeaways', 3), ul(items, 'sb-ticks'), cls='sb-panel sb-takeaways', layout='flow')


def inline_cta(title, text, label, url):
    return group(heading(title, 3), para(text), buttons((label, url)), cls='sb-inline-cta', layout='flow')


def post_faq(items):
    return join(heading('Frequently asked questions'), faq(items))


POST_EXTRA = {
'citations-vs-profile-backlinks': [
  heading('A quick citation audit you can do yourself'),
  para('Search Google for your business name with your old phone number, then with your old address if you have moved. Every result that shows outdated details is a listing worth fixing. Then search for your name plus your town and check the first two pages for directories where you are missing entirely. Write the results in a simple spreadsheet. That list is the starting point any good local SEO provider would use.'),
  post_faq([('How many citations does a local business need?', 'There is no magic number. Most small local businesses benefit from accurate listings on the major platforms, the main directories in their country and the key sites in their industry. Accuracy and relevance matter far more than a specific count.'),
            ('Are nofollow citations worthless?', 'No. Citations are mainly about confirming your business details, not passing link authority, so a nofollow link on a trusted directory still does its job.'),
            ('How long do citations take to have an effect?', 'Search engines need to recrawl the listings, which can take a few weeks. Fixing inconsistent details on major platforms usually has the quickest impact.'),
            ('Should I remove old or duplicate listings?', 'Yes, where you can. Duplicates and outdated addresses confuse search engines and customers. Claim and correct them, or ask the platform to merge or remove them.')])],
'choose-guest-post-dr-tier': [
  heading('How to spot a link farm'),
  para('Open the site\'s recent posts. If every article is on a different, unrelated topic, each one links out to a business, and nobody seems to read or comment, you are probably looking at a site that exists to sell links. Check whether it ranks for anything in Google, and whether its traffic comes from a real audience. A smaller, genuine site in your niche is almost always the better buy.'),
  post_faq([('Is a higher DR always better?', 'Not on its own. Relevance, real traffic and editorial standards often matter more than a few extra DR points.'),
            ('Should guest post links be dofollow?', 'Publishers decide. Paid placements should be qualified, for example with rel="sponsored". A natural link profile includes a mix.'),
            ('How many guest posts do I need?', 'It depends on your competitors. Compare the number and quality of sites linking to the pages that outrank you, and close the gap gradually.'),
            ('Where should guest posts link to?', 'To the page that best answers the topic of the article, often a service or guide page, using natural anchor text.')])],
'wordpress-speed-checklist': [
  heading('A simple before-and-after routine'),
  para('Before changing anything, take a full backup and record the PageSpeed results for three key pages. Make one change at a time, clear your cache and test again. Keeping a short log of what you changed and what happened means you can undo anything that breaks the site, and you will learn which fixes actually made a difference on your setup.'),
  post_faq([('What is a good PageSpeed score for WordPress?', 'Aim for "good" Core Web Vitals for real users rather than a perfect lab score. Many fast, successful sites score in the 70s or 80s in the lab.'),
            ('Do caching plugins conflict with each other?', 'Yes. Run one caching solution, either your host\'s or a single plugin, never several at once.'),
            ('Will a new theme make my site faster?', 'Sometimes, but test first. A lightweight theme helps most when your current theme or page builder loads a lot of unused code.'),
            ('How often should I check site speed?', 'After every major update, new plugin or design change, and at least monthly for important pages.')])],
'canva-brand-kit-guide': [
  heading('Turning your brand kit into templates'),
  para('The kit only saves time when your team has templates to start from. Begin with the five formats you use most often, for example a square social post, a story, a quote card, a one-page flyer and a presentation cover. Build each with locked logo positions and your brand fonts, then share them with the team. From then on, new designs take minutes instead of starting from a blank page.'),
  post_faq([('Is Canva Brand Kit free?', 'Brand Kits are part of Canva\'s paid plans, such as Pro and Teams. Free accounts have limited brand options, so check Canva\'s current plan details.'),
            ('Can I have more than one brand kit?', 'On team plans you can create several kits, which is useful for agencies or businesses with sub-brands.'),
            ('Can I upload my own fonts to Canva?', 'On supported plans, yes, as long as your font licence allows it.'),
            ('What is the difference between a brand kit and brand guidelines?', 'The brand kit stores the assets. Guidelines explain how to use them: spacing, logo do\'s and don\'ts, tone of voice and examples.')])],
'local-seo-checklist': [
  heading('7. Make your website match your profile'),
  para('Your website should confirm everything your Google Business Profile says. Put your business name, address and phone number in the footer, add a clear contact page with a map, and make sure your main service pages mention the areas you serve in natural sentences. Link from your profile to the most relevant page, not always the homepage. Every match between your profile and your website is another reason for Google to trust both.'),
  heading('8. Keep it going'),
  para('Local SEO is not a one-off job. New competitors open, platforms change and reviews keep arriving. Set a monthly routine: one or two profile posts, replies to every review, a check that your details are still correct, and one improvement to your website. Small, steady actions beat a burst of work followed by months of silence.'),
  post_faq([('How long does local SEO take?', 'Profile and citation fixes are often reflected within weeks. Competitive areas and new businesses usually need several months of consistent work.'),
            ('Do I need a physical address for local SEO?', 'No. Service-area businesses can hide their address on Google and list the areas they cover instead.'),
            ('Should I create a page for every town?', 'Only where you genuinely serve the area and can say something specific about it. Thin copies with the town name swapped can hurt more than help.'),
            ('How do I get more Google reviews?', 'Ask at the right moment, send a direct review link, and reply to every review. Never pay for or incentivise reviews.')])],
'ppc-management-cost': [
  heading('Questions to ask before hiring anyone'),
  ul(['Will the ads run in my own account, and will I have admin access?', 'Exactly what work happens each week, and how will I see it?', 'Is conversion tracking included, and who checks it is accurate?', 'What is the notice period, and what happens to my account if I leave?', 'Do you charge a percentage of spend, and if so, is it capped?']),
  para('A good provider answers all five without hesitation. If the answers are vague, keep looking.'),
  post_faq([('What is a reasonable PPC management fee?', 'It depends on account size and complexity. For small accounts, flat monthly fees are usually clearer and better value than a percentage of spend.'),
            ('How much should I spend on Google Ads?', 'Enough to get meaningful data, typically enough for at least 20 to 30 clicks a day in your main campaign. Start small, measure, then scale what converts.'),
            ('Should I own my Google Ads account?', 'Always. Your account holds your data and history. Agencies should work in your account as users, not run ads from theirs.'),
            ('How long before PPC campaigns perform well?', 'Expect a learning period of two to four weeks, then gradual improvement as search terms, bids and ads are optimised.')])],
'ai-seo-guide': [
  heading('Write pages AI tools can quote'),
  para('Look at your most important service or guide page and ask: if someone asked an AI tool the main question this page answers, is there a clear two-sentence answer near the top? Is the price range, location or process stated plainly? Are facts like opening hours and services identical to your Google profile? Pages that answer directly, with specific details and consistent facts, are much easier for any system, human or machine, to rely on.'),
  heading('AI SEO and normal SEO work together'),
  para('Everything that helps AI tools understand you also helps Google: technical health, clear structure, authority and genuinely useful content. That is why we treat AI visibility as part of a broader <a href="/services/monthly-seo/">SEO plan</a> rather than a separate trick. Start with the foundations, then measure how AI answers change over time.'),
  post_faq([('What is generative engine optimisation (GEO)?', 'GEO is the practice of making your content easy for generative AI tools to understand, trust and cite. It builds on classic SEO rather than replacing it.'),
            ('Does schema markup help with AI search?', 'Structured data helps machines understand your pages and business details, which supports accurate AI answers. It is not a guarantee of being cited.'),
            ('Should I block AI crawlers?', 'That is a business decision. Blocking them may protect content, but it also reduces the chance that AI tools mention or cite you.'),
            ('Is AI-written content bad for SEO?', 'Not automatically. What matters is whether content is helpful, accurate and original. Low-value content at scale is a problem however it is written.')])],
}

post('citations-vs-profile-backlinks', 'Business citations vs profile backlinks: what is the difference and which do you need?', join(
    para('"Citations" and "profile backlinks" are often sold together, and plenty of sellers use the two words as if they mean the same thing. They do not. They do different jobs, they are judged differently by search engines, and buying the wrong one is one of the most common ways small businesses waste their first SEO budget.'),
    takeaways(['Citations confirm who and where your business is. They matter most for local search.', 'Profile backlinks build brand presence and help new sites get discovered.', 'Consistency beats volume: one wrong address can undo the value of ten correct listings.', 'Neither replaces strong pages and editorial links for competitive keywords.']),
    heading('What is a business citation?'),
    para('A citation is any online mention of your business name, address and phone number, often shortened to NAP. You find them on business directories, map apps, industry associations, local chambers of commerce and review platforms. Many include a link to your website, but the link is not the point. The point is the data.'),
    para('Search engines cross-check those details across the web to confirm that your business is real, where it is and how to contact it. Google lists relevance, distance and prominence as the main factors in local results, and consistent information across trusted sites feeds into prominence (see ' + ext('https://support.google.com/business/answer/7091', 'Google\'s guide to local ranking') + '). That is why citations are a core part of <a href="/services/local-seo/">local SEO</a>.'),
    heading('What is a profile backlink?'),
    para('A profile backlink is a link from an account or profile page you create on an established platform: a professional community, a design portfolio site, a developer platform, a podcast directory or a business network. The profile describes your brand and links to your website.'),
    para('On their own, individual profile links carry modest weight. Their value comes from breadth and legitimacy: a real brand tends to have a footprint across many platforms, and search engines notice when a site has none. For a brand-new website, a set of well-made profiles also helps crawlers discover your pages sooner.'),
    heading('Citations vs profile backlinks, side by side'),
    table(['', 'Citations', 'Profile backlinks'], [
        ['Main purpose', 'Confirm business identity and location', 'Brand presence and link discovery'],
        ['Most useful for', 'Local businesses and service areas', 'New sites, online-only brands'],
        ['What matters most', 'Identical name, address and phone', 'Complete, genuine-looking profiles'],
        ['Link attribute', 'Often nofollow, which is fine', 'Mixed dofollow and nofollow'],
        ['Typical mistake', 'Inconsistent or outdated details', 'Thousands of empty, automated profiles']]),
    heading('Which one does your business need?'),
    ul(['<strong>A local business</strong> such as a plumber, clinic, salon or office-based agency: start with citations and your Google Business Profile, then add profile links.',
        '<strong>An online-only business</strong>: focus on profile links first, then move to editorial links such as guest posts as your site matures. Our guide to <a href="/choose-guest-post-dr-tier/">choosing a guest post tier</a> explains how.',
        '<strong>A brand-new website</strong>: a small mix of both gives search engines the signals to discover and trust you sooner.',
        '<strong>A business that has moved or rebranded</strong>: fix existing citations before building new ones. Old addresses are actively harmful.']),
    heading('Four mistakes that waste money'),
    ul(['<strong>Inconsistent details.</strong> "Ltd" in one place, "Limited" in another, and an old phone number elsewhere all weaken citations. Decide on one exact format before anything is submitted.',
        '<strong>Buying thousands of automated links.</strong> Mass-submission software creates low-quality profiles on abandoned sites. Google\'s ' + ext('https://developers.google.com/search/docs/essentials/spam-policies', 'spam policies') + ' are clear that links made to manipulate rankings can be ignored or penalised.',
        '<strong>Ignoring the reports.</strong> If a provider cannot give you a list of live URLs, you have no way to check what you paid for.',
        '<strong>Expecting rankings from these alone.</strong> Citations and profiles are foundations. Competitive keywords also need strong pages, content and editorial links.']),
    heading('How to check the work you buy'),
    para('Ask for a spreadsheet of every live URL, open a sample of them, and check that the business details match yours exactly. Good providers welcome this. It is the standard we hold ourselves to, and every <a href="/services/off-page-seo/">link building package</a> we sell ends with that report.'),
    *POST_EXTRA['citations-vs-profile-backlinks'],
    inline_cta('Want this done properly?', 'Our citation and profile packages are built by hand with consistent details, and you get a report of every live URL.', 'See link building packages', '/services/off-page-seo/#packages'),
), 'Citations and profile backlinks do different jobs. What each one is, which your business needs, the mistakes that waste money and how to check the work.', 'Link building')

post('choose-guest-post-dr-tier', 'How to choose a guest post tier by Domain Rating (without wasting money)', join(
    para('Guest posts are usually sold by Domain Rating, or DR, an Ahrefs score from 0 to 100 that estimates how strong a website\'s backlink profile is (' + ext('https://ahrefs.com/blog/domain-rating/', 'Ahrefs explains how DR is calculated') + '). Higher DR generally means a stronger link and a higher price. DR is a useful shortcut, but buying on DR alone is how people end up paying premium prices for links that do very little.'),
    takeaways(['DR measures a site\'s links, not its traffic, relevance or quality.', 'Match the tier to your own site. A natural profile has a range of strengths.', 'Check real traffic, relevance and editorial standards before you buy.', 'Paid links should be labelled. Avoid "guaranteed dofollow, permanent" offers.']),
    heading('What DR tells you, and what it does not'),
    para('DR looks only at links pointing to a site. It says nothing about whether real people read the site, whether it covers your topic, or whether it sells links to anyone who pays. A DR 60 blog with no search traffic and twenty sponsored posts a day is far less valuable than a DR 35 industry site with a real audience.'),
    heading('Match the tier to your site'),
    table(['Your situation', 'Sensible starting tier'], [
        ['New site with few or no links', 'DR 10+ to DR 20+, alongside citations and profile links'],
        ['Established local or niche site', 'DR 30+ to DR 40+'],
        ['Competitive national keywords', 'DR 50+ and above, mixed with lower tiers'],
        ['Product launch or company news', 'A press release plus one or two strong posts']]),
    para('Jumping straight to only high-DR links on a brand-new site looks unusual and is rarely the best use of budget. Build foundations first, then add strength.'),
    heading('Five quality checks beyond DR'),
    ul(['<strong>Real organic traffic.</strong> The site should get visitors from search, not just have a high score.',
        '<strong>Topical relevance.</strong> A link from a site in your field is worth more than a random general blog.',
        '<strong>Editorial standards.</strong> Real articles with real authors, not pages of "write for us" posts.',
        '<strong>Outbound link volume.</strong> Sites linking to dozens of unrelated businesses every day pass less value.',
        '<strong>Disclosure.</strong> Reputable publishers label sponsored content, which keeps everyone inside search engine guidelines.']),
    heading('Paid links and Google\'s rules'),
    para('Google asks that links which are paid for are qualified, for example with <code>rel="sponsored"</code> (' + ext('https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links', 'Google: qualify your outbound links') + '). Many publishers handle this themselves. Be wary of anyone selling "guaranteed dofollow, permanent, undisclosed" links. That combination is exactly what Google\'s ' + ext('https://developers.google.com/search/docs/essentials/spam-policies', 'link spam policy') + ' is designed to catch.'),
    heading('A simple buying plan'),
    ul(['Start with foundations: <a href="/citations-vs-profile-backlinks/">citations and profile links</a>.', 'Add one or two posts at a tier that matches your site.', 'Point links at your most useful pages, not only the homepage.', 'Review progress after two or three months before buying more.', 'If you are unsure where to start, an <a href="/services/seo-audit/">SEO audit</a> will show whether links are even your biggest problem.']),
    *POST_EXTRA['choose-guest-post-dr-tier'],
    inline_cta('Ready to add premium links?', 'Our guest posts run from DR 10+ to DR 70+, on real sites, with a live-URL report on publication.', 'See guest post tiers', '/services/off-page-seo/#packages'),
), 'DR is useful but not the whole story. How to pick a guest post tier that fits your site, five quality checks beyond the number and how to stay within Google\'s rules.', 'Link building')

post('wordpress-speed-checklist', 'Is your WordPress site slow? A 12-point speed checklist before you pay anyone', join(
    para('A slow site loses visitors before they read a word, and page experience is one of the signals Google uses. The good news: most WordPress sites get noticeably faster from a handful of simple fixes. Work through this checklist before paying for optimisation. You may not need to.'),
    takeaways(['Measure first with PageSpeed Insights and note LCP, INP and CLS.', 'Images, caching and unused plugins cause most slow WordPress sites.', 'Real-user data matters more than a perfect lab score.', 'If a cached page is still slow, hosting may be the bottleneck.']),
    heading('Measure first'),
    para('Test your homepage and one important page in ' + ext('https://pagespeed.web.dev/', 'PageSpeed Insights') + '. Note the three Core Web Vitals: Largest Contentful Paint (LCP), Interaction to Next Paint (INP) and Cumulative Layout Shift (CLS). Google\'s "good" thresholds are an LCP of 2.5 seconds or less, INP of 200 milliseconds or less and CLS of 0.1 or less (' + ext('https://web.dev/articles/vitals', 'web.dev: Web Vitals') + ').'),
    heading('The 12-point checklist'),
    ul(['<strong>Compress images.</strong> Serve WebP or AVIF, and resize images to the size they are actually displayed.',
        '<strong>Lazy-load images below the fold</strong>, but never the main hero image. That one should load first.',
        '<strong>Turn on page caching.</strong> Most good hosts include it. Otherwise use one reputable caching plugin, not three.',
        '<strong>Delete unused plugins.</strong> Deactivated plugins are a security risk too.',
        '<strong>Check your theme and page builder.</strong> Heavy builders can add large amounts of CSS and JavaScript to every page.',
        '<strong>Limit third-party scripts.</strong> Chat widgets, trackers and embedded feeds each add load time.',
        '<strong>Host fonts locally</strong> and load only the weights you use.',
        '<strong>Reserve space for images and embeds</strong> so the layout does not jump while loading, which is the main cause of poor CLS.',
        '<strong>Update PHP</strong> to a version WordPress currently recommends (' + ext('https://wordpress.org/about/requirements/', 'WordPress requirements') + '). It is often free speed.',
        '<strong>Clean the database</strong> of old revisions, spam comments and expired transients.',
        '<strong>Use a CDN</strong> if your visitors are spread across countries.',
        '<strong>Review your hosting.</strong> If server response time stays slow on a cached page, the host is likely the bottleneck.']),
    heading('Lab scores vs real users'),
    para('PageSpeed lab scores are useful for testing changes, but Google uses data from real visitors where it has enough of it. A perfect 100 in the lab is not required. What matters is that real users experience "good" Core Web Vitals on your important pages.'),
    heading('When to get help'),
    para('If you have worked through the list and pages are still slow, the cause is usually deeper: a heavy theme, a plugin conflict, unoptimised database queries or underpowered hosting. That is where our <a href="/services/technical-seo/">Core Web Vitals optimisation</a> comes in, with a backup first and an honest before/after report. To keep a site fast after updates, see our <a href="/services/website-maintenance/">website maintenance plans</a>.'),
    *POST_EXTRA['wordpress-speed-checklist'],
    inline_cta('Want it fixed for you?', 'We optimise images, caching, scripts and fonts, then show you the before and after.', 'See Core Web Vitals packages', '/services/technical-seo/#packages'),
), 'Twelve practical checks to speed up a WordPress site, from images and caching to plugins and fonts, plus how to read Core Web Vitals properly.', 'Websites')

post('canva-brand-kit-guide', 'How to create a brand kit in Canva (and what to put in it)', join(
    para('Canva\'s Brand Kit is one of the most useful features for small teams: it keeps your logos, colours and fonts one click away, so every social post, flyer and presentation looks like it came from the same business. Here is how to set one up properly, and what a good brand kit actually contains.'),
    takeaways(['A Brand Kit stores your logos, colour palettes and fonts inside Canva.', 'Prepare your assets first: logo files, exact hex codes and font names.', 'Brand Kits are part of Canva\'s paid plans. Check your plan if the option is missing.', 'Branded templates are what make the kit save real time.']),
    heading('What is a Canva brand kit?'),
    para('A brand kit in Canva is a saved set of your brand assets: logos, colour palettes, fonts and, on some plans, guidelines and brand templates. Once it is set up, everyone on your team picks from the same approved assets instead of guessing colours or downloading old logos. Canva documents the feature in its help centre (' + ext('https://www.canva.com/help/brand-kit/', 'Canva: Set up Brand Kits') + ').'),
    heading('Before you start: prepare your assets'),
    ul(['<strong>Logo files</strong> in PNG with a transparent background, plus SVG if you have it. Include light and dark versions.',
        '<strong>Exact colour codes</strong> in hex format, for example #0C1930. Do not pick colours by eye from a screenshot.',
        '<strong>Font names</strong> for headings and body text. If your brand uses a licensed font, check that you are allowed to upload it.',
        '<strong>A short tone-of-voice note</strong>, such as "friendly, plain English, no jargon", if your plan supports guidelines.']),
    heading('How to set up a brand kit in Canva, step by step'),
    ul(['Open Canva and select <strong>Brand</strong> from the side panel on the homepage.', 'Choose to create a new Brand Kit and give it a clear name, such as your business name.', 'Upload your <strong>logos</strong>: main, icon-only and light versions.', 'Add your <strong>colour palette</strong> using the exact hex codes.', 'Set your <strong>fonts</strong> for headings, subheadings and body text.', 'Add guidelines and brand templates if your plan includes them.']),
    para('On some plans, Canva can also build a kit automatically from your website or a brand guidelines PDF (' + ext('https://www.canva.com/help/brand-kit-builder/', 'Canva: Brand Kit Builder') + '). It is a helpful start, but always review what it extracts. Logos and colours are not always picked up correctly.'),
    heading('What a good brand kit includes'),
    table(['Asset', 'Why it matters'], [
        ['Logo variations', 'A wide logo, an icon and a light version cover almost every layout.'],
        ['Primary and accent colours', 'Two or three main colours plus neutrals keep designs consistent.'],
        ['Two fonts, maximum', 'One for headings and one for body text is easier to keep consistent.'],
        ['Branded templates', 'Ready-made social posts and documents are what save your team real time.'],
        ['Simple guidelines', 'Do\'s and don\'ts stop well-meaning team members from stretching the logo.']]),
    heading('Common brand kit mistakes'),
    ul(['Uploading a blurry logo screenshot instead of the original file.', 'Adding ten colours "just in case". Fewer colours make stronger branding.', 'Mixing fonts that look too similar, which reads as a mistake rather than a choice.', 'Never building templates, so everyone still starts from a blank page.']),
    heading('Do you need a designer?'),
    para('If you already have a professional logo and colours, setting up the kit yourself takes under an hour with this guide. If your logo is outdated, or you want ready-made templates your team can use straight away, our <a href="/services/graphic-design/">graphic design and branding packages</a> include a <a href="/services/graphic-design/#packages">Canva Brand Kit Setup</a> with five branded templates.'),
    *POST_EXTRA['canva-brand-kit-guide'],
    inline_cta('Want your Canva brand kit set up for you?', 'We add your logos, colours and fonts to Canva and design five branded templates for your team.', 'See branding packages', '/services/graphic-design/#packages'),
), 'Step-by-step guide to creating a brand kit in Canva: what to prepare, how to set it up, what a good brand kit includes and the mistakes to avoid.', 'Design')

post('local-seo-checklist', 'Local SEO for small businesses: a practical checklist', join(
    para('When someone searches "electrician near me" or "accountant in Leeds", Google shows a map with three businesses before any normal results. Getting into that map pack is local SEO. This checklist covers what actually moves the needle for a small business, in the order we would tackle it.'),
    takeaways(['Your Google Business Profile is the single most important local SEO asset.', 'Consistent name, address and phone number everywhere builds trust.', 'Reviews matter, but must be genuine. Fake reviews break Google policy.', 'Location pages help when you serve several areas.']),
    heading('What is a local SEO service?'),
    para('A local SEO service optimises the signals Google uses for local results. Google says it ranks local results on relevance, distance and prominence (' + ext('https://support.google.com/business/answer/7091', 'Google: improve your local ranking') + '). You cannot change distance, but you can improve relevance and prominence through your profile, your website, your citations and your reviews.'),
    heading('1. Claim and complete your Google Business Profile'),
    ul(['Choose the most accurate primary category, then add relevant secondary categories.', 'List every service you offer, with short descriptions.', 'Add opening hours, including holiday hours.', 'Upload real photos of your work, team and premises.', 'Post updates and offers regularly. It shows the business is active.']),
    heading('2. Make your business details consistent everywhere'),
    para('Your name, address and phone number should be identical on your website, your profile and every directory. Small differences, such as "Street" and "St" or an old phone number, create doubt. Fix existing listings before building new ones. Our guide to <a href="/citations-vs-profile-backlinks/">citations vs profile backlinks</a> explains why.'),
    heading('3. Earn genuine reviews, and reply to them'),
    para('Ask happy customers at the right moment, make it easy with a direct link, and reply to every review, good or bad. Never buy reviews or offer incentives. Fake reviews break Google\'s policies and can lead to your profile being restricted.'),
    heading('4. Build local pages on your website'),
    para('If you serve several towns, create a genuinely useful page for each: the services you offer there, local examples of your work and how to get in touch. Avoid copying the same text with the town name swapped. Search engines treat that as thin, duplicate content.'),
    heading('5. Add LocalBusiness structured data'),
    para('Structured data helps search engines read your business details accurately. Google documents the LocalBusiness type and its properties (' + ext('https://developers.google.com/search/docs/appearance/structured-data/local-business', 'Google: LocalBusiness structured data') + '). Test it with the ' + ext('https://search.google.com/test/rich-results', 'Rich Results Test') + '.'),
    heading('6. Track what matters'),
    para('Watch calls, direction requests and website clicks in your profile insights, and track a handful of local keywords monthly. Rankings vary by searcher location, so use a tool that checks from your area.'),
    *POST_EXTRA['local-seo-checklist'],
    inline_cta('Prefer to have it done for you?', 'Our local SEO packages cover your Google Business Profile, citations, location pages and schema, from a fixed price.', 'See local SEO packages', '/services/local-seo/#packages'),
), 'A practical local SEO checklist for small businesses: Google Business Profile, consistent citations, genuine reviews, location pages, LocalBusiness schema and tracking.', 'SEO')

post('ppc-management-cost', 'PPC management costs: what you should pay and what you should get', join(
    para('PPC management pricing is confusing on purpose. Some agencies charge a percentage of your ad spend, some a flat monthly fee, some both, and many hide setup costs. Here is how the main models work, what a fair service should include, and how to tell if your account is being managed at all.'),
    takeaways(['Ad spend and management fees are separate. You pay the ad platform directly.', 'Flat fees are easier to budget. Percentage fees grow with your spend.', 'A good manager works on search terms, ads and tracking every week.', 'Conversion tracking must be set up before any optimisation means anything.']),
    heading('Ad spend vs management fee'),
    para('Your ad spend is what you pay Google or Meta for clicks. The management fee is what you pay someone to run the account. Keep them separate: ads should be billed to your own card, in your own account, so you always keep the data and the history.'),
    heading('Common pricing models'),
    table(['Model', 'How it works', 'Watch out for'], [
        ['Percentage of spend', 'A share of your monthly ad budget', 'Fees rise even when results do not'],
        ['Flat monthly fee', 'A fixed price per month', 'Check how many campaigns are included'],
        ['Hybrid', 'Flat fee plus a smaller percentage', 'Complexity, and harder to compare'],
        ['One-off audit or setup', 'Fixed price for a defined job', 'Make sure you get the account, not just a report']]),
    heading('What good PPC management includes'),
    ul(['<strong>Conversion tracking that works.</strong> Without it, optimisation is guesswork (' + ext('https://support.google.com/google-ads/answer/6308', 'Google Ads: about conversion tracking') + ').',
        '<strong>Search term reviews.</strong> Irrelevant searches added as negative keywords every week.',
        '<strong>Ad testing.</strong> New ad copy tested against the current best performer.',
        '<strong>Budget and bid management</strong> moved towards campaigns that convert.',
        '<strong>Clear reporting</strong> showing spend, conversions and cost per result, not just clicks and impressions.']),
    heading('Signs your account is not being managed'),
    ul(['The change history shows almost no activity for weeks.', 'Search terms include obviously irrelevant phrases.', 'Every campaign uses broad match with no negative keywords.', 'Reports show clicks and impressions but never conversions.', 'You do not have admin access to your own ad account.']),
    heading('Start with an audit'),
    para('If you already run ads, a <a href="/services/ppc-management/#packages">Google Ads audit</a> is the cheapest way to find wasted spend before paying for ongoing management. If you advertise on Facebook and Instagram too, see our <a href="/services/facebook-ads/">Facebook ads management</a>.'),
    *POST_EXTRA['ppc-management-cost'],
    inline_cta('Want a second pair of eyes on your ads?', 'Our fixed-price Google Ads audit shows wasted spend, tracking gaps and the fixes in priority order.', 'See PPC packages', '/services/ppc-management/#packages'),
), 'How PPC management is priced, what a fair service includes, signs your account is not being managed and why ad spend should always stay in your own account.', 'Paid ads')

post('ai-seo-guide', 'AI SEO explained: how to get your business cited in AI answers', join(
    para('More people now ask AI tools questions they used to type into Google: "Which local SEO companies offer fixed prices?" or "What should a website maintenance plan include?" Those tools summarise the web and sometimes cite sources. AI SEO, also called generative engine optimisation (GEO), is about becoming one of those sources.'),
    takeaways(['AI search builds on the same foundations as normal SEO.', 'Clear, direct answers are easier for AI tools to quote.', 'Consistent brand facts across the web reduce mistakes in AI answers.', 'No one can guarantee a mention. Ignore anyone who claims otherwise.']),
    heading('How AI search tools choose sources'),
    para('Google says its AI features, such as AI Overviews, rely on the same systems and quality signals as regular search, and that the usual SEO best practices still apply (' + ext('https://developers.google.com/search/docs/appearance/ai-features', 'Google: AI features and your website') + '). Other assistants vary, but they tend to favour sources that are clear, specific, consistent and trusted.'),
    heading('Five practical steps'),
    ul(['<strong>Answer questions directly.</strong> Put a clear, one- or two-sentence answer near the top of the page, then add detail.',
        '<strong>Structure pages well.</strong> Descriptive headings, short paragraphs, lists and tables make information easy to extract.',
        '<strong>Keep brand facts consistent.</strong> Your name, services, location and prices should match across your site, profiles and directories.',
        '<strong>Use structured data.</strong> Organization, service and FAQ markup help machines understand your pages (test them with the ' + ext('https://search.google.com/test/rich-results', 'Rich Results Test') + ').',
        '<strong>Earn mentions on trusted sites.</strong> AI tools learn from the wider web, so reputable mentions matter.']),
    heading('What to avoid'),
    ul(['Hidden text or prompts aimed at AI crawlers. They break search guidelines and can backfire.', 'Mass-produced AI content with nothing new to say. Google\'s ' + ext('https://developers.google.com/search/docs/fundamentals/creating-helpful-content', 'helpful content guidance') + ' applies to AI-written pages too.', 'Paying for "guaranteed ChatGPT placement". It does not exist.']),
    heading('How to measure AI visibility'),
    para('Make a list of 20 to 30 questions your customers ask, run them through AI tools monthly, and record which brands are mentioned and which pages are cited. It is manual, but it shows whether your changes are working. Our <a href="/services/ai-seo/">AI SEO service</a> does this for you, alongside the fixes.'),
    *POST_EXTRA['ai-seo-guide'],
    inline_cta('See how AI tools describe your business', 'Our AI Search Visibility Check tests real customer questions and shows where you are missing.', 'See AI SEO packages', '/services/ai-seo/#packages'),
), 'What AI SEO and generative engine optimisation (GEO) are, how AI tools choose sources, five practical steps to get cited and what to avoid.', 'SEO')

# ================================================================ template heroes
write_pattern('hero-insights', 'Hero: Insights', page_hero('art-content.svg', 'Illustration of a structured article with an outline',
              eyebrow('Insights'), heading('SEO, link building and website guides that save you money', 1),
              lead('Straight answers from the work we do every day: what moves rankings, what wastes budget, and how to choose the right service for your site.'),
              ul(['Practical checklists', 'No jargon', 'Written by the people doing the work'], 'sb-checks')),
              cat='seo-booster-sections', post_types='', inserter='no')

# ================================================================ manifest
def php_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


lines = ["<?php", "/**", " * Generated by tools/build_patterns.py — pages and posts created by the setup screen.", " *", " * @package SEOBoosterTheme", " */", "", "defined( 'ABSPATH' ) || exit;", "", "return array(", "\t'pages' => array("]
for p in PAGES:
    lines.append("\t\tarray( " + ', '.join(f"'{k}' => {php_str(str(v)) if not isinstance(v, int) else v}" for k, v in p.items()) + " ),")
lines.append("\t),")
lines.append("\t'posts' => array(")
for p in POSTS:
    lines.append("\t\tarray( " + ', '.join(f"'{k}' => {php_str(v)}" for k, v in p.items()) + " ),")
lines += ["\t),", ");", ""]
with open(os.path.join(ROOT, 'inc', 'site-manifest.php'), 'w') as f:
    f.write('\n'.join(lines))
print(f'{len(PAGES)} pages, {len(POSTS)} posts written to {os.path.abspath(PAT)}')
