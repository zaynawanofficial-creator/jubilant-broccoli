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
SVC = {s[0]: s for s in SERVICES}


def svc_card(slug, dark=False):
    s = SVC[slug]
    return group(
        image(f'art-{s[4]}.svg', '', 'sb-card__art'),
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


def page(slug, title, content, excerpt, parent='', template='landing', menu_order=0):
    PAGES.append(dict(slug=slug, title=title, parent=parent, template=template, excerpt=excerpt, pattern=f'seo-booster/page-{slug}', order=menu_order))
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
         'Fixed-price SEO and web services that show you <span class="sb-hl">exactly</span> what you get',
         'Pick a package, pay securely and send your brief. Every order has a clear scope, a stated turnaround and a report or files you can check, without retainers or vague promises.',
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
            group(*[svc_card(s[0]) for s in SERVICES],
                  card('Something else?', join(para('PPC, analytics, email and automation projects are quoted individually.'), para('<a href="/get-a-quote/">Request a quote →</a>', 'sb-card__more')), cls='sb-card sb-card--outline'),
                  align='wide', layout='flow', cls='sb-grid sb-grid--4')),
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
    ('SEO &amp; visibility', 'Get found: authority, technical health and a clear plan.', ['off-page-seo', 'seo-audit', 'technical-seo']),
    ('Websites', 'Build it properly, then keep it fast, secure and working.', ['website-development', 'website-maintenance']),
    ('Content &amp; creative', 'Words and visuals that explain what you do and why it matters.', ['content-writing', 'graphic-design']),
]
hub = join(
    page_hero('art-services.svg', 'Illustration of a service menu and package card', eyebrow('Services'), heading('Services with clear scope and fixed prices', 1),
          lead('Choose a service to see its packages, what is included and how we work. Not sure where to start? An <a href="/services/seo-audit/">SEO audit</a> tells you what will make the biggest difference.'),
          buttons(('See all packages', '/packages/'), ('Get a quote', '/get-a-quote/', 'outline'))),
    *[section(head(eb, title, sub), group(*[svc_card(s) for s in slugs], align='wide', layout='flow', cls='sb-grid sb-grid--3'),
              cls='sb-section--soft' if i % 2 else '') for i, (title, sub, slugs) in enumerate(hub_groups) for eb in ['']],
    section(head('Coming soon', 'Quoted services', 'These are available as custom projects while we finalise fixed packages.'),
            group(card('PPC &amp; paid ads', 'Account audits, campaign setup and management for Google and Meta ads. Ad spend is always billed separately.'),
                  card('Analytics &amp; tracking', 'GA4 and Google Tag Manager audits, setup and conversion tracking, with consent built in.'),
                  card('Email marketing', 'Templates, automations and campaign management on your existing email platform.'),
                  card('Marketing automation', 'Workflow audits and builds that connect your forms, CRM and email.'),
                  align='wide', layout='flow', cls='sb-grid sb-grid--4'),
            buttons(('Request a quote', '/get-a-quote/')), cls='sb-section--blue'),
    cta(),
)
page('services', 'Services', hub, 'SEO, link building, website development, maintenance, content writing and graphic design services with fixed-price packages.', menu_order=1)

# ================================================================ SERVICE PAGES
def service_page(slug, eb, h1, sub, checks, for_list, not_for, pk_title, pk_sub, features, process, needs, faqs, related, extra=None, title=None, excerpt=''):
    s = SVC[slug]
    content = join(
        hero(eb, h1, sub, [('See packages', '#packages'), ('Get a quote', f'/get-a-quote/?service={slug}', 'outline')], checks,
             f'art-{s[4]}.svg', f'Illustration for {s[2].replace("&amp;", "and")}', crumbs=True),
        section(columns(
            column(group(heading('Who it is for', 3), ul(for_list, 'sb-ticks'), cls='sb-card', layout='flow')),
            column(group(heading('Not the right fit if…', 3), ul(not_for, 'sb-crosses'), cls='sb-card', layout='flow')),
        ), cls='sb-section--tight'),
        section(head('Packages', pk_title, pk_sub, center=True),
                group(shortcode(f'[sb_packages service="{s[1]}"]'), align='wide', layout='flow'),
                para('Prices in [sb_currency]. Need a bigger or custom order? <a href="/get-a-quote/">Ask for a quote</a>.', 'sb-center sb-muted'),
                cls='sb-section--soft', anchor='packages'),
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
    'Link building and citations, done by hand and reported with live URLs',
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
    [('What is the difference between citations, profile links and guest posts?', 'Citations are business listings with your name, address and phone, mainly a local SEO trust signal. Profile links come from accounts on established platforms. Guest posts are articles on other websites with a contextual link to you. Our guide <a href="/insights/citations-vs-profile-backlinks/">explains when each one helps</a>.'),
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
    'Find out exactly what is holding your website back',
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
    'Technical fixes that help search engines crawl, understand and rank your pages',
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
    'A fast, professional WordPress website without the agency price tag',
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
    'WordPress fixes and care, handled by a developer',
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
    'Original articles written for people first, structured for search',
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
    'On-brand graphics and brand kits, ready to use',
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

# ================================================================ PACKAGES
packages = join(
    page_hero('art-packages.svg', 'Illustration of three package cards', eyebrow('Packages'), heading('All packages and prices', 1),
          lead('Every package in one place. Prices are in [sb_currency] and every card shows what is included, the turnaround and the revisions.'),
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
                  card('Payments', 'Secure checkout with the payment options shown at checkout. Prices are in [sb_currency].', 'shield'),
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

# ================================================================ LEGAL (drafts)
DRAFT = group(para('<strong>Draft under review.</strong> This policy is being reviewed before launch, and company registration details will be added. Questions? Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>.'), cls='sb-notice', layout='flow')


def legal(slug, title, blocks, excerpt):
    page(slug, title, join(DRAFT, *blocks), excerpt, template='', menu_order=20)


legal('terms', 'Terms of Service', [
    para('These terms apply when you buy services from SEO Booster ("we", "us") through seobooster.uk. By placing an order you agree to them.'),
    heading('1. Services and scope'), para('Each package describes its deliverables, exclusions, turnaround and revisions. Anything not listed is not included. Custom work is defined in a written quote.'),
    heading('2. Orders and payment'), para('Prices are shown in [sb_currency] and payable in full at checkout unless agreed otherwise in writing. An order is accepted when payment is confirmed.'),
    heading('3. Your brief and access'), para('You must provide accurate information and any materials needed. Turnaround starts when your brief is complete. You are responsible for the content and materials you supply and for having the rights to use them. Never send us passwords. Grant access through user invitations.'),
    heading('4. Delivery and revisions'), para('We deliver within the stated turnaround in working days. Revisions refine the agreed deliverables and do not extend the scope.'),
    heading('5. No guarantee of search results'), para('Search rankings and traffic depend on factors outside our control, including search engine algorithms and competitors. We do not guarantee rankings, traffic, indexing or link attributes (such as "dofollow"). We guarantee the deliverables described in your package.'),
    heading('6. Third-party platforms'), para('Listings, profiles and publications are hosted by third parties who may edit or remove content. Replacement terms are stated on each package.'),
    heading('7. Ownership'), para('When your order is paid in full, you own the final deliverables we create for you, except third-party assets (such as licensed stock images or fonts), which remain under their own licences.'),
    heading('8. Refunds and cancellation'), para('See our <a href="/refund-policy/">Refund Policy</a>.'),
    heading('9. Liability'), para('Our total liability for any order is limited to the amount you paid for that order, to the extent permitted by law. Nothing in these terms limits liability that cannot be limited by law.'),
    heading('10. Changes and contact'), para('We may update these terms. The version published when you order applies to that order. Contact: <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>.'),
], 'Terms of service for buying SEO, website, content and design services from SEO Booster.')

legal('refund-policy', 'Refund Policy', [
    para('We want you to be happy with what you buy. This policy explains when refunds apply.'),
    heading('Before work starts'), para('If you cancel before we start work, which is usually before your brief is complete, you receive a full refund.'),
    heading('After work starts'), para('If you cancel after work has started, we refund the value of the work not yet done. Where deliverables are partly complete (for example, some links already placed), you receive those deliverables and a refund for the remainder.'),
    heading('After delivery'), para('Delivered work is not refundable, except where we did not deliver what the package describes. In that case we will first fix or complete the delivery, and refund if we cannot.'),
    heading('Replacements'), para('Profile and citation links not live at delivery are replaced. Guest posts removed within 90 days of publication are replaced free of charge.'),
    heading('Search results'), para('Refunds are not available because rankings or traffic did not change, as these are not guaranteed (see our <a href="/terms/">Terms</a>).'),
    heading('How to request a refund'), para('Email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> with your order number. Approved refunds go back to the original payment method.'),
], 'When and how refunds apply to SEO Booster orders.')

legal('privacy-policy', 'Privacy Policy', [
    para('This policy explains how SEO Booster collects and uses personal data when you use seobooster.uk or buy our services.'),
    heading('What we collect'), ul(['<strong>Account and order data</strong>: name, email, billing address, order history.',
                                     '<strong>Project brief data</strong>: website URLs, business details and files you upload to deliver your order.',
                                     '<strong>Messages</strong>: what you send through our contact and quote forms.',
                                     '<strong>Technical data</strong>: IP address and browser data in server logs, and the cookies described in our <a href="/cookie-policy/">Cookie Policy</a>.']),
    heading('How we use it'), para('To process payments, deliver and support your orders, answer enquiries, keep the site secure and meet legal obligations. We do not sell your data.'),
    heading('Payment data'), para('Payments are handled by our payment providers. We never receive or store your full card details.'),
    heading('Who we share it with'), para('Only service providers that help us run the site and deliver orders, such as hosting, payment and email providers. Where a service requires it, we share brief details with third-party platforms (for example, your business details for citations).'),
    heading('How long we keep it'), para('Order records are kept as long as required for accounting and tax. Brief files are deleted or archived after the order is completed, unless you ask us to keep them for future work.'),
    heading('Your rights'), para('You can ask to access, correct, delete or export your personal data, or object to its use, by emailing <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a>. You may also complain to your data protection authority.'),
], 'How SEO Booster collects, uses and protects personal data.')

legal('cookie-policy', 'Cookie Policy', [
    para('Cookies are small files stored by your browser. This page explains the cookies seobooster.uk uses.'),
    heading('Essential cookies'), para('Our store uses essential cookies to keep your cart, log you in and protect checkout. The site cannot work without them, so they do not require consent.'),
    heading('Analytics and marketing'), para('We do not currently use analytics or advertising cookies. If we add them, we will ask for your consent first and update this page.'),
    heading('Managing cookies'), para('You can block or delete cookies in your browser settings. Blocking essential cookies will stop the cart and account from working.'),
], 'The cookies used on seobooster.uk and how to control them.')

legal('accessibility', 'Accessibility', [
    para('We want seobooster.uk to be usable by everyone. We aim to meet WCAG 2.2 level AA.'),
    heading('What we do'), ul(['Text and interface colours are checked against WCAG contrast ratios.', 'All functions work with a keyboard, with visible focus outlines.', 'Images that carry meaning have text alternatives.', 'Pages use proper headings and landmarks for screen readers.', 'Motion is reduced when your device asks for it.']),
    heading('Known limitations'), para('Some third-party components, such as payment forms, are provided by external services and may not fully meet the same standard.'),
    heading('Feedback'), para('If something is hard to use, email <a href="mailto:hello@seobooster.uk">hello@seobooster.uk</a> and tell us the page and the problem. We will fix it or provide the information another way.'),
], 'Accessibility statement for seobooster.uk.')

# ================================================================ INSIGHTS (articles)
post('citations-vs-profile-backlinks', 'Business citations vs profile backlinks: what is the difference and which do you need?', join(
    para('"Citations" and "profile backlinks" are often sold together, and many sellers use the words interchangeably. They do different jobs, though. Knowing the difference helps you buy the right thing and avoid paying for links that do nothing.'),
    heading('What is a business citation?'),
    para('A citation is any online mention of your business name, address and phone number (often shortened to NAP). Typical sources are business directories, map apps, industry listings and local chamber or association sites.'),
    para('Citations matter most for <strong>local SEO</strong>. Search engines cross-check your business details across the web. Consistent details build confidence that your business is real and where you say it is, while conflicting addresses or old phone numbers do the opposite.'),
    heading('What is a profile backlink?'),
    para('A profile backlink is a link from an account or profile page you create on an established platform: a community, a design portfolio site, a developer platform or a social bookmarking site. The profile usually describes your brand and links to your website.'),
    para('Profile links help a new site get discovered and add brand mentions. Individually they carry little weight. Their value is in breadth and in looking like a real, active brand across the web.'),
    heading('Side by side'),
    table(['', 'Citations', 'Profile backlinks'], [
        ['Main purpose', 'Confirm business identity and location', 'Brand presence and link discovery'],
        ['Most useful for', 'Local businesses, service areas', 'New sites, any niche'],
        ['Key requirement', 'Identical name, address and phone', 'A complete, genuine-looking profile'],
        ['Link attribute', 'Often nofollow, which is fine', 'Mixed dofollow and nofollow']]),
    heading('Which do you need?'),
    ul(['<strong>A local business</strong> (plumber, clinic, salon, agency with an office): start with citations, then add profile links.',
        '<strong>An online-only business</strong>: focus on profile links and, as your site matures, editorial links such as guest posts.',
        '<strong>A brand-new website</strong>: a small mix of both gives search engines signals to find and trust you sooner.']),
    heading('Three mistakes to avoid'),
    ul(['<strong>Inconsistent details.</strong> "Ltd" in one place, "Limited" in another, and an old phone number elsewhere all weaken citations. Decide on one exact format first.',
        '<strong>Buying thousands of automated links.</strong> Mass-submission software creates low-quality, spammy profiles that can do more harm than good.',
        '<strong>Expecting rankings from these alone.</strong> Citations and profiles are foundations. Competitive keywords also need strong content and editorial links.']),
    para('Our <a href="/services/off-page-seo/">off-page SEO packages</a> mix citations and profile links, created by hand with consistent business details and a report of every live URL.'),
), 'Citations and profile backlinks do different jobs. Learn what each one is, when it helps, and the mistakes that waste money.', 'Link building')

post('choose-guest-post-dr-tier', 'How to choose a guest post tier by Domain Rating (without wasting money)', join(
    para('Guest posts are usually sold by Domain Rating (DR), a 0 to 100 score from Ahrefs that estimates the strength of a website\'s backlink profile. A higher DR often means a stronger link and a higher price. DR is useful, but it is not the whole story.'),
    heading('What DR does and does not tell you'),
    para('DR measures links pointing to a site, not its traffic, relevance or editorial standards. A site can have a high DR and almost no real readers, especially if it sells many links. That is why we look at more than one metric.'),
    heading('Match the tier to your site'),
    table(['Your situation', 'Sensible starting tier'], [
        ['New site, few or no links', 'DR 10+ to DR 20+, plus citations and profile links'],
        ['Established local or niche site', 'DR 30+ to DR 40+'],
        ['Competitive national keywords', 'DR 50+ and above, mixed with lower tiers'],
        ['Launch or news story', 'Press release plus one or two strong posts']]),
    para('A natural link profile has a range of strengths. Jumping straight to only high-DR links on a brand-new site looks unusual and is a poor use of budget.'),
    heading('Five quality checks beyond DR'),
    ul(['<strong>Real organic traffic</strong>: the site should receive visitors from search, not just have a high score.',
        '<strong>Topical relevance</strong>: a link from a site in your field is worth more than a random general blog.',
        '<strong>Editorial standards</strong>: real articles with real authors, not pages stuffed with "write for us" posts.',
        '<strong>Outbound link volume</strong>: sites linking out to dozens of unrelated businesses every day pass less value.',
        '<strong>Disclosure</strong>: reputable publishers label sponsored content. That is normal and keeps everyone within search engine guidelines.']),
    heading('Paid links and Google\'s rules'),
    para('Google\'s spam policies say links that are paid for should be qualified, for example with <code>rel="sponsored"</code>. Many publishers handle this themselves. Avoid anyone selling "guaranteed dofollow, permanent, undisclosed" links, because that is exactly the pattern Google looks for.'),
    heading('A simple buying plan'),
    ul(['Start with foundations: citations and profile links.', 'Add one or two posts at a tier that matches your site.', 'Point links at your most useful pages, not only the homepage.', 'Review progress after a few months before buying more.']),
    para('See our <a href="/services/off-page-seo/#packages">Premium Links packages</a>, with guest posts from DR 10+ to DR 70+ and a live-URL report on publication.'),
), 'DR is useful but not the whole story. How to pick a guest post tier that fits your site, and five quality checks beyond the number.', 'Link building')

post('wordpress-speed-checklist', 'Is your WordPress site slow? A 12-point speed checklist before you pay anyone', join(
    para('A slow site loses visitors and sales, and Core Web Vitals are part of how Google assesses page experience. Before paying for optimisation, work through this checklist. Many sites get much faster from the first few items alone.'),
    heading('Measure first'),
    para('Test your homepage and one key page in Google PageSpeed Insights. Note the Largest Contentful Paint (LCP), Interaction to Next Paint (INP) and Cumulative Layout Shift (CLS). Google\'s "good" thresholds are LCP up to 2.5 seconds, INP up to 200 milliseconds and CLS up to 0.1.'),
    heading('The checklist'),
    ul(['<strong>Compress images.</strong> Serve WebP or AVIF and resize images to the size they are displayed at.',
        '<strong>Lazy-load below-the-fold images</strong>, but never the main hero image, which should load first.',
        '<strong>Use page caching.</strong> Most hosts offer it, or use a reputable caching plugin.',
        '<strong>Remove unused plugins.</strong> Deactivate and delete anything you do not need.',
        '<strong>Check your theme and builder.</strong> Heavy page builders can add a lot of CSS and JavaScript to every page.',
        '<strong>Limit third-party scripts</strong> such as chat widgets, trackers and embedded feeds. Each one adds load time.',
        '<strong>Host fonts locally</strong> and load only the weights you use.',
        '<strong>Reserve space for images and embeds</strong> so the layout does not jump as the page loads (CLS).',
        '<strong>Update PHP</strong> to a currently supported version. It is free speed.',
        '<strong>Clean the database</strong> of old revisions, spam comments and expired transients.',
        '<strong>Use a CDN</strong> if your visitors are spread across countries.',
        '<strong>Review hosting.</strong> If the server response time (TTFB) is slow on a cached page, the host may be the bottleneck.']),
    heading('Lab scores vs real users'),
    para('PageSpeed lab scores are useful for testing, but Google uses data from real visitors (the Chrome UX Report) where available. A perfect lab score is not required. Aim for real users to experience "good" vitals.'),
    para('Need help? Our <a href="/services/technical-seo/">Core Web Vitals optimisation</a> includes a backup, the fixes and an honest before/after report, and our <a href="/services/website-maintenance/">maintenance plans</a> keep a site fast after updates.'),
), 'Twelve practical checks to speed up a WordPress site, including images, caching, plugins and fonts, and how to read Core Web Vitals properly.', 'Websites')

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
