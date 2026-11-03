"""Informative illustrations (v2, 3 Nov 2026): every picture carries real, relevant labels
(statuses, issue names, page sections) instead of empty placeholder bars.
Overwrites the hero/service/report SVGs written by build_art.py. Run after build_art.py:
    python3 tools/build_art.py && python3 tools/build_art_v2.py
All content is illustrative (no client data, no performance claims)."""
import os
from html import escape
OUT = os.path.join(os.path.dirname(__file__), '..', 'wp-content', 'themes', 'seo-booster', 'assets', 'images')
INK, INK2, NAVY3, BLUE, BLUE_D, LIME, LINE, SOFT, B50, WHITE, SLATE, BODY = '#0C1930', '#13254A', '#1B2F5A', '#2563EB', '#1D4ED8', '#B9F24C', '#E2E8F0', '#F8FAFC', '#EFF4FF', '#FFFFFF', '#94A3B8', '#475569'
RED, AMBER, GREEN = '#DC2626', '#D97706', '#15803D'
FONT = "Inter, 'Segoe UI', Arial, Helvetica, sans-serif"
HEAD = "Manrope, 'Segoe UI', Arial, Helvetica, sans-serif"


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t"><title id="t">{escape(title)}</title>'
            f'<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0C1930" flood-opacity=".18"/></filter></defs>{body}</svg>\n')


def t(x, y, s, size=12, weight=500, fill=INK, anchor='start', head=False):
    return f'<text x="{x}" y="{y}" font-family="{HEAD if head else FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'


def card(x, y, w, h, title='', dark=False, shadow=True, dots=True):
    bg, bar, tc, ln = (INK2, NAVY3, WHITE, '#24396A') if dark else (WHITE, SOFT, INK, LINE)
    out = f'<g{" filter=\"url(#sh)\"" if shadow else ""}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{ln}"/></g>'
    out += f'<path d="M{x} {y+14} a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v20 h-{w} z" fill="{bar}"/>'
    if dots:
        out += ''.join(f'<circle cx="{x+16+i*12}" cy="{y+17}" r="3.5" fill="{"#2B416E" if dark else LINE}"/>' for i in range(3))
    if title:
        out += t(x + (54 if dots else 16), y + 21, title, 11.5, 700, tc)
    return out


def pill(x, y, label, bg, fg, w=None, size=10):
    w = w or (len(label) * size * 0.62 + 16)
    return f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="{bg}"/>' + t(x + w / 2, y + 14, label, size, 700, fg, 'middle')


def check(cx, cy, r=8, bg=LIME, fg=INK):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/><path d="M{cx-r*.45} {cy}l{r*.3} {r*.32} {r*.55} -{r*.62}" fill="none" stroke="{fg}" stroke-width="{max(1.6, r*.24):.1f}" stroke-linecap="round" stroke-linejoin="round"/>'


def write(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)


LIVE = (B50, BLUE_D)
OK = ('#DCFCE7', GREEN)

# ------------------------------------------------------------------ home hero
b = card(30, 24, 400, 270, 'Order #1042 · Off-Page SEO')
steps = ['Package', 'Details', 'In progress', 'Report']
for i, s in enumerate(steps):
    x = 56 + i * 92
    done = i < 2
    cur = i == 2
    b += f'<circle cx="{x}" cy="86" r="11" fill="{LIME if done else (BLUE if cur else LINE)}"/>'
    b += check(x, 86, 11) if done else t(x, 90, str(i + 1), 10, 800, WHITE if cur else BODY, 'middle')
    if i < 3:
        b += f'<rect x="{x+15}" y="85" width="62" height="2.5" rx="1" fill="{LIME if done else LINE}"/>'
    b += t(x, 112, s, 10, 600, INK if (done or cur) else SLATE, 'middle')
rows = [('Business directory', 'Citation'), ('Local listing', 'Citation'), ('Industry profile', 'Profile'), ('Startup directory', 'Profile')]
for i, (n, k) in enumerate(rows):
    y = 132 + i * 36
    b += f'<rect x="48" y="{y}" width="364" height="28" rx="8" fill="{SOFT}" stroke="{LINE}"/>' + t(62, y + 18, n, 11, 600) + t(210, y + 18, k, 10.5, 500, BODY)
    b += pill(340, y + 4, 'Live', *OK, w=56)
b += card(330, 210, 210, 150, 'Delivery report', dark=True)
b += t(350, 278, '20 / 20', 34, 800, WHITE, head=True) + t(350, 300, 'links live on delivery', 11, 500, '#CBD5E1')
b += f'<rect x="350" y="316" width="168" height="8" rx="4" fill="#2B416E"/><rect x="350" y="316" width="168" height="8" rx="4" fill="{LIME}"/>'
b += t(350, 342, 'Spreadsheet · every URL', 10, 600, LIME)
b += f'<g filter="url(#sh)"><rect x="0" y="300" width="250" height="64" rx="14" fill="{WHITE}" stroke="{LINE}"/></g>' + check(30, 332, 13) + t(52, 328, 'Project details received', 12, 700) + t(52, 345, 'Work starts right after payment', 10.5, 500, BODY)
write('hero-growth.svg', svg(560, 380, b, 'Example order: progress steps, live link list and a delivery report'))

# ------------------------------------------------------------------ off-page: link network around your site
b = card(20, 20, 480, 340, 'Your link profile', shadow=False)
cx, cy = 260, 200
nodes = [(110, 110, 'Business directory'), (410, 110, 'Local citation'), (90, 290, 'Industry profile'), (420, 290, 'Guest post · DR 30+'), (260, 330, 'Press release'), (260, 80, 'Brand profile')]
for x, y, _ in nodes:
    b += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{SLATE}" stroke-width="1.6" stroke-dasharray="4 5"/>'
b += f'<g filter="url(#sh)"><rect x="{cx-80}" y="{cy-26}" width="160" height="52" rx="14" fill="{INK}"/></g>' + t(cx, cy - 4, 'yoursite.com', 14, 800, WHITE, 'middle', True) + t(cx, cy + 14, 'target page', 10, 500, LIME, 'middle')
for x, y, label in nodes:
    w = len(label) * 6.4 + 34
    b += f'<g filter="url(#sh)"><rect x="{x-w/2:.0f}" y="{y-15}" width="{w:.0f}" height="30" rx="15" fill="{WHITE}" stroke="{LINE}"/></g>' + check(x - w / 2 + 15, y, 7) + t(x - w / 2 + 27, y + 4, label, 10.5, 600)
write('art-offpage.svg', svg(520, 380, b, 'Illustration: your site linked from directories, citations, profiles, guest posts and press releases'))

# ------------------------------------------------------------------ audit: prioritised issues
b = card(20, 24, 400, 330, 'SEO audit · priority fixes')
issues = [('Broken internal links', 'High', ('#FEE2E2', RED)), ('Slow LCP on mobile', 'High', ('#FEE2E2', RED)), ('Missing meta descriptions', 'Medium', ('#FEF3C7', AMBER)),
          ('Duplicate page titles', 'Medium', ('#FEF3C7', AMBER)), ('No schema markup', 'Low', ('#DCFCE7', GREEN)), ('Images without alt text', 'Low', ('#DCFCE7', GREEN))]
b += t(40, 78, 'Issue', 10, 700, SLATE) + t(310, 78, 'Priority', 10, 700, SLATE)
for i, (n, pr, c) in enumerate(issues):
    y = 88 + i * 42
    b += f'<rect x="36" y="{y}" width="368" height="34" rx="8" fill="{SOFT}" stroke="{LINE}"/>' + t(50, y + 21, n, 11.5, 600) + pill(306, y + 7, pr, *c, w=70)
b += f'<g filter="url(#sh)"><circle cx="430" cy="270" r="62" fill="{WHITE}" stroke="{INK}" stroke-width="9"/></g><circle cx="430" cy="270" r="46" fill="{B50}"/>' + t(430, 266, 'Fix', 13, 800, BLUE, 'middle', True) + t(430, 284, 'first', 13, 800, BLUE, 'middle', True)
b += f'<path d="M474 316l30 30" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
write('art-audit.svg', svg(520, 380, b, 'Illustration: an SEO audit listing issues by priority'))

# ------------------------------------------------------------------ technical: checklist + vitals gauge
b = card(20, 24, 300, 330, 'Technical fixes · change log', dark=True)
fixes = ['301 redirect chains fixed', 'Canonical tags corrected', 'XML sitemap regenerated', 'Broken links repaired', 'Schema markup added', 'Images converted to WebP']
for i, f_ in enumerate(fixes):
    y = 84 + i * 42
    b += check(48, y, 9) + t(66, y + 4, f_, 11.5, 600, WHITE)
b += card(280, 120, 220, 230, 'Core Web Vitals')
b += f'<path d="M318 270a72 72 0 0 1 144 0" fill="none" stroke="{LINE}" stroke-width="14" stroke-linecap="round"/><path d="M318 270a72 72 0 0 1 120 -54" fill="none" stroke="{GREEN}" stroke-width="14" stroke-linecap="round"/>'
b += t(390, 262, 'Good', 18, 800, GREEN, 'middle', True) + t(390, 298, 'LCP · INP · CLS', 10.5, 600, BODY, 'middle') + pill(330, 312, 'Before / after report', B50, BLUE_D, w=120)
write('art-technical.svg', svg(520, 380, b, 'Illustration: a technical SEO change log and a Core Web Vitals gauge'))

# ------------------------------------------------------------------ web dev: real page wireframe + phone
b = card(14, 24, 380, 320, 'yourbusiness.com')
b += t(34, 76, 'LOGO', 11, 800, INK, head=True) + ''.join(t(200 + i * 46, 76, s, 10, 600, BODY) for i, s in enumerate(['Home', 'Services', 'About', 'Contact']))
b += f'<rect x="30" y="90" width="348" height="104" rx="10" fill="{INK}"/>' + t(48, 124, 'Clear headline that says', 15, 800, WHITE, head=True) + t(48, 144, 'what you do and for whom', 15, 800, WHITE, head=True)
b += pill(48, 160, 'Get a quote', LIME, INK, w=88)
for i, s in enumerate(['Service one', 'Service two', 'Service three']):
    x = 30 + i * 118
    b += f'<rect x="{x}" y="208" width="108" height="78" rx="10" fill="{SOFT}" stroke="{LINE}"/><rect x="{x+12}" y="220" width="22" height="22" rx="6" fill="{B50}"/>' + t(x + 12, 260, s, 10, 700) + t(x + 12, 275, 'Short benefit', 9, 500, BODY)
b += f'<rect x="30" y="298" width="348" height="30" rx="8" fill="{B50}"/>' + t(44, 317, 'Contact form → your inbox', 10.5, 700, BLUE_D)
b += f'<g filter="url(#sh)"><rect x="380" y="86" width="126" height="262" rx="22" fill="{INK}"/></g><rect x="390" y="104" width="106" height="226" rx="12" fill="{WHITE}"/>'
b += f'<rect x="398" y="114" width="90" height="70" rx="8" fill="{INK}"/>' + t(406, 140, 'Headline', 11, 800, WHITE, head=True) + pill(406, 156, 'Call now', LIME, INK, w=58, size=9)
b += ''.join(f'<rect x="398" y="{194+i*40}" width="90" height="32" rx="7" fill="{SOFT}" stroke="{LINE}"/>' + t(406, 214 + i * 40, s, 9, 600) for i, s in enumerate(['Service one', 'Service two', 'Reviews']))
b += pill(398, 312, 'Mobile-ready', OK[0], OK[1], w=90, size=9)
write('art-webdev.svg', svg(520, 380, b, 'Illustration: a business website wireframe on desktop and mobile'))

# ------------------------------------------------------------------ maintenance: monthly care checklist
b = card(20, 30, 320, 310, 'Monthly care · this month')
care = [('Backup completed', 'Daily'), ('WordPress core updated', 'Done'), ('Plugins updated (12)', 'Done'), ('Uptime monitored', '24/7'), ('Security scan', 'Clean'), ('Small changes', '1 h left')]
for i, (n, st) in enumerate(care):
    y = 74 + i * 42
    b += f'<rect x="36" y="{y}" width="288" height="34" rx="8" fill="{SOFT}" stroke="{LINE}"/>' + check(54, y + 17, 8) + t(70, y + 21, n, 11.5, 600) + pill(250, y + 7, st, *OK, w=64)
b += f'<g filter="url(#sh)"><circle cx="420" cy="210" r="86" fill="{BLUE}"/></g><path d="M452 168a30 30 0 0 0-36 38L374 248a14 14 0 0 0 20 20l42-42a30 30 0 0 0 38-36l-19 19-17-4-4-17z" fill="{WHITE}"/>'
b += pill(360, 312, 'Fixed in 24–48 h', LIME, INK, w=118)
write('art-maintenance.svg', svg(520, 380, b, 'Illustration: a monthly website care checklist and a wrench'))

# ------------------------------------------------------------------ content: article structure
b = card(20, 20, 330, 340, 'Article draft · 1,500 words')
lines_ = [('H1', 'How to choose a local SEO agency', 13, 800), ('', 'Short intro that answers the question first.', 10.5, 500), ('H2', 'What a good agency should offer', 11.5, 700),
          ('', 'Clear deliverables, reporting, fair contracts…', 10.5, 500), ('H2', 'Questions to ask before you buy', 11.5, 700), ('', 'Checklist, examples and red flags.', 10.5, 500), ('H2', 'FAQ', 11.5, 700)]
y = 72
for tag, text, size, w in lines_:
    if tag:
        b += pill(36, y - 13, tag, INK if tag == 'H1' else B50, WHITE if tag == 'H1' else BLUE_D, w=30, size=9) + t(74, y + 1, text, size, w, INK, head=(tag == 'H1'))
        y += 30
    else:
        b += t(74, y - 6, text, size, w, BODY)
        y += 22
b += f'<rect x="36" y="{y}" width="298" height="54" rx="10" fill="{B50}"/>' + t(48, y + 20, 'Meta description', 10, 700, BLUE_D) + t(48, y + 38, 'A clear 150-character summary for Google.', 10, 500, BODY)
b += card(312, 110, 190, 190, 'Checks', dark=True)
b += ''.join(check(334, 158 + i * 34, 8) + t(350, 162 + i * 34, s, 11, 600, WHITE) for i, s in enumerate(['Keyword in title', 'Plagiarism-free', 'Facts checked', 'Internal links']))
write('art-content.svg', svg(520, 380, b, 'Illustration: an article outline with headings, meta description and quality checks'))

# ------------------------------------------------------------------ design: brand board
b = card(16, 24, 340, 320, 'Brand kit · v1')
b += f'<rect x="32" y="62" width="150" height="120" rx="12" fill="{INK}"/><rect x="74" y="86" width="22" height="50" rx="5" fill="{BLUE}"/><rect x="102" y="70" width="22" height="66" rx="5" fill="{LIME}"/>' + t(107, 166, 'Primary logo', 10, 700, WHITE, 'middle')
b += f'<rect x="192" y="62" width="148" height="56" rx="12" fill="{WHITE}" stroke="{LINE}"/>' + t(266, 96, 'Logo · light', 10.5, 700, INK, 'middle')
b += f'<rect x="192" y="126" width="148" height="56" rx="12" fill="{BLUE}"/>' + t(266, 160, 'Logo · icon', 10.5, 700, WHITE, 'middle')
sw = [(INK, '#0C1930'), (BLUE, '#2563EB'), (LIME, '#B9F24C'), ('#60A5FA', '#60A5FA'), (SOFT, '#F8FAFC')]
for i, (c, h) in enumerate(sw):
    x = 32 + i * 63
    b += f'<rect x="{x}" y="196" width="55" height="46" rx="9" fill="{c}" stroke="{LINE}"/>' + t(x + 2, 258, h, 8.5, 600, BODY)
b += t(32, 290, 'Headings: Manrope ExtraBold', 11, 700) + t(32, 310, 'Body text: Inter Regular', 11, 500, BODY) + pill(32, 318, 'SVG · PDF · PNG', B50, BLUE_D, w=110)
b += f'<g filter="url(#sh)"><rect x="330" y="120" width="174" height="230" rx="16" fill="{WHITE}" stroke="{LINE}"/></g>' + t(350, 186, 'Aa', 56, 800, INK, head=True) + t(350, 214, 'Manrope', 13, 800, INK, head=True) + t(350, 234, 'Inter', 13, 500, BODY)
b += f'<rect x="350" y="252" width="134" height="34" rx="9" fill="{BLUE}"/>' + t(417, 274, 'Button style', 11, 700, WHITE, 'middle') + pill(350, 300, 'Social kit', LIME, INK, w=74)
write('art-design.svg', svg(520, 380, b, 'Illustration: a brand kit with logo versions, colour palette and typography'))

# ------------------------------------------------------------------ services menu
b = card(20, 24, 300, 330, 'Choose a service')
svcs = [('Off-Page SEO', 'Links & citations'), ('SEO Audit', 'Priority fixes'), ('Technical SEO', 'Speed & indexing'), ('Website Development', '1–10 pages'), ('Maintenance & Fixes', 'Care plans'), ('Content Writing', 'Articles & batches'), ('Graphic Design', 'Social & branding')]
for i, (n, d) in enumerate(svcs):
    y = 66 + i * 40
    sel = i == 0
    b += f'<rect x="34" y="{y}" width="272" height="32" rx="8" fill="{B50 if sel else SOFT}" stroke="{BLUE if sel else LINE}"/>' + t(48, y + 20, n, 11.5, 700) + t(292, y + 20, d, 9.5, 500, BODY, 'end')
b += card(300, 110, 200, 210, 'Your package', dark=True)
b += t(320, 176, '20 links', 22, 800, WHITE, head=True) + t(320, 198, 'Profiles & citations', 11, 500, '#CBD5E1')
b += ''.join(check(328, 224 + i * 26, 7) + t(342, 228 + i * 26, s, 10.5, 600, WHITE) for i, s in enumerate(['Done by hand', 'Live-URL report', '5–7 working days']))
b += pill(320, 290, 'Choose package →', LIME, INK, w=120)
write('art-services.svg', svg(520, 380, b, 'Illustration: a service menu with a selected package'))

# ------------------------------------------------------------------ packages: 3 tiers
def tier(x, y, w, h, name, qty, feats, featured=False):
    o = f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHITE}" stroke="{INK if featured else LINE}" stroke-width="{2.5 if featured else 1}"/></g>'
    o += f'<path d="M{x} {y+16} a16 16 0 0 1 16 -16 h{w-32} a16 16 0 0 1 16 16 v70 h-{w} z" fill="{INK}"/>'
    o += t(x + 16, y + 30, name, 10.5, 700, LIME) + t(x + 16, y + 66, qty, 22, 800, WHITE, head=True)
    o += ''.join(check(x + 22, y + 110 + i * 26, 7) + t(x + 36, y + 114 + i * 26, f_, 10, 600) for i, f_ in enumerate(feats))
    o += f'<rect x="{x+14}" y="{y+h-46}" width="{w-28}" height="30" rx="8" fill="{BLUE}"/>' + t(x + w / 2, y + h - 26, 'Choose', 11, 700, WHITE, 'middle')
    if featured:
        o += pill(x + w / 2 - 40, y - 10, 'Most popular', LIME, INK, w=80, size=9)
    return o
b = tier(14, 70, 156, 280, 'STARTER', '5 links', ['Citations', 'Profiles', 'URL report']) + tier(182, 40, 160, 310, 'POPULAR', '20 links', ['Citations', 'Profiles', 'URL report', 'NAP checked'], True) + tier(354, 70, 156, 280, 'GROWTH', '50 links', ['Citations', 'Profiles', 'URL report'])
write('art-packages.svg', svg(520, 380, b, 'Illustration: three package tiers with the popular option highlighted'))

# ------------------------------------------------------------------ process (on dark)
b = f'<path d="M78 170 C150 80, 200 260, 260 170 S380 80, 442 170" fill="none" stroke="#2B416E" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>'
labels = [('1', 'Choose', 'a package'), ('2', 'Add', 'project details'), ('3', 'Pay', 'securely'), ('4', 'Receive', 'your report')]
for i, (n, a1, a2) in enumerate(labels):
    x = 78 + i * 121
    y = 170 if i % 2 == 0 else 190
    col = LIME if i == 3 else (BLUE if i else WHITE)
    b += f'<circle cx="{x}" cy="{y}" r="42" fill="{INK2}" stroke="#2B416E" stroke-width="2"/><circle cx="{x}" cy="{y}" r="28" fill="{col}"/>' + t(x, y + 7, n, 20, 800, INK if col != BLUE else WHITE, 'middle', True)
    b += t(x, y + 70, a1, 14, 800, WHITE, 'middle', True) + t(x, y + 88, a2, 11, 500, '#CBD5E1', 'middle')
write('art-process.svg', svg(520, 330, b, 'Illustration: four steps from choosing a package to receiving your report'))

# ------------------------------------------------------------------ about: proof checklist + chart
b = card(20, 40, 300, 230, 'How every order runs')
b += ''.join(check(48, 92 + i * 40, 10) + t(68, 96 + i * 40, s, 12, 600) for i, s in enumerate(['Scope agreed before you pay', 'Work done by hand', 'Checked before delivery', 'Report you can verify']))
b += card(250, 170, 250, 190, 'What you receive', dark=True)
items = [('Live-URL report', 'Links'), ('Audit PDF', 'SEO'), ('Change log', 'Technical'), ('Source files', 'Design')]
b += ''.join(t(270, 226 + i * 32, a, 12, 700, WHITE) + pill(400, 212 + i * 32, k, NAVY3, LIME, w=84) for i, (a, k) in enumerate(items))
write('art-about.svg', svg(520, 380, b, 'Illustration: how every order runs and what you receive'))

# ------------------------------------------------------------------ contact: real conversation
b = f'<g filter="url(#sh)"><rect x="20" y="30" width="300" height="190" rx="16" fill="{WHITE}" stroke="{LINE}"/></g><path d="M20 48 a18 18 0 0 1 18 -18 h264 a18 18 0 0 1 18 18 L170 140 Z" fill="{B50}" stroke="{LINE}"/><path d="M20 48 L170 145 L320 48" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round"/>'
b += t(40, 190, 'hello@seobooster.uk', 13, 800, INK, head=True) + t(40, 208, 'A real person replies by email', 10.5, 500, BODY)
b += f'<g filter="url(#sh)"><rect x="210" y="160" width="290" height="70" rx="18" fill="{SOFT}" stroke="{LINE}"/></g>' + t(230, 190, 'Can you help with links for', 12, 600) + t(230, 208, 'my plumbing business?', 12, 600)
b += f'<g filter="url(#sh)"><rect x="150" y="250" width="330" height="88" rx="18" fill="{INK}"/></g>' + t(172, 280, 'Yes. 20 citations fits a local', 12, 600, WHITE) + t(172, 298, 'business. Here is the scope and price.', 12, 600, WHITE) + pill(172, 308, 'Fixed quote', LIME, INK, w=80, size=9)
write('art-contact.svg', svg(520, 360, b, 'Illustration: an email conversation about a link building package'))

# ------------------------------------------------------------------ quote: request form → fixed quote
b = card(20, 24, 290, 330, 'Request a quote')
fields = [('Website', 'https://yourbusiness.com'), ('Service', 'Website Development'), ('Pages', 'Home, Services, About, Contact'), ('Budget', 'Select a range')]
for i, (lab, val) in enumerate(fields):
    y = 70 + i * 60
    b += t(38, y, lab, 10.5, 700) + f'<rect x="36" y="{y+8}" width="256" height="32" rx="8" fill="{SOFT}" stroke="{LINE}"/>' + t(48, y + 29, val, 10.5, 500, BODY)
b += f'<rect x="36" y="310" width="140" height="32" rx="8" fill="{BLUE}"/>' + t(106, 331, 'Request quote', 11, 700, WHITE, 'middle')
b += f'<g transform="rotate(-5 410 200)"><g filter="url(#sh)"><rect x="320" y="110" width="190" height="200" rx="16" fill="{INK}"/></g>' + t(340, 146, 'FIXED QUOTE', 10.5, 800, LIME) + t(340, 178, '5-page website', 15, 800, WHITE, head=True)
b += ''.join(t(340, 208 + i * 24, a, 10.5, 600, '#CBD5E1') + t(490, 208 + i * 24, v, 10.5, 700, WHITE, 'end') for i, (a, v) in enumerate([('Scope', 'Written'), ('Timeline', '10–14 days'), ('Revisions', '2 rounds'), ('Price', 'Agreed')]))
b += '</g>' + check(480, 104, 16)
write('art-quote.svg', svg(520, 380, b, 'Illustration: a quote request form and a fixed quote with scope and timeline'))

# ------------------------------------------------------------------ FAQ: real questions and answers
qa = [(30, 30, 300, 'Do you guarantee rankings?', False), (170, 100, 330, 'No. We guarantee the deliverables.', True), (30, 180, 290, 'When does work start?', False), (180, 250, 320, 'As soon as your details are in.', True)]
b = ''
for x, y, w, q, ans in qa:
    b += f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="58" rx="18" fill="{INK if ans else WHITE}" stroke="{"#24396A" if ans else LINE}"/></g>'
    b += f'<circle cx="{x+30}" cy="{y+29}" r="15" fill="{LIME if ans else B50}"/>' + (check(x + 30, y + 29, 15) if ans else t(x + 30, y + 35, '?', 16, 800, BLUE, 'middle', True))
    b += t(x + 56, y + 34, q, 12.5, 700, WHITE if ans else INK)
write('art-faq.svg', svg(520, 330, b, 'Illustration: common questions with clear answers'))

# ------------------------------------------------------------------ sample deliverables
b = card(10, 10, 500, 340, 'Link report · example')
cols = [('Platform', 34), ('Type', 190), ('Live URL', 270), ('Status', 430)]
b += f'<rect x="24" y="52" width="472" height="28" rx="6" fill="{INK}"/>' + ''.join(t(x, 70, c, 10, 700, WHITE) for c, x in cols)
rows = [('Business directory', 'Citation', '…/listing/your-business'), ('Local chamber listing', 'Citation', '…/members/your-business'), ('Industry profile', 'Profile', '…/company/your-business'),
        ('Startup directory', 'Profile', '…/startups/your-business'), ('Niche blog · DR 34', 'Guest post', '…/blog/how-to-choose…'), ('Press network', 'Press release', '…/news/your-launch')]
for i, (pl, ty, url) in enumerate(rows):
    y = 86 + i * 40
    b += f'<rect x="24" y="{y}" width="472" height="34" rx="6" fill="{SOFT if i % 2 else WHITE}" stroke="{LINE}"/>' + t(34, y + 21, pl, 10.5, 600) + t(190, y + 21, ty, 10, 500, BODY) + t(270, y + 21, url, 10, 500, BLUE_D) + pill(426, y + 7, 'Live', *OK, w=52)
write('report-links.svg', svg(520, 360, b, 'Example link report listing each placement, its type, live URL and status'))

b = (f'<g transform="rotate(-4 160 200)"><g filter="url(#sh)"><rect x="30" y="40" width="250" height="300" rx="14" fill="{WHITE}" stroke="{LINE}"/></g>' + t(50, 74, 'Executive summary', 13, 800, INK, head=True) + t(50, 94, 'Health by area', 10.5, 600, BODY))
for i, (lab, w, c) in enumerate([('Technical', 70, AMBER), ('On-page', 55, AMBER), ('Content', 82, GREEN), ('Links', 40, RED), ('Speed', 60, AMBER)]):
    y = 116 + i * 38
    b += t(50, y + 4, lab, 10.5, 600) + f'<rect x="120" y="{y-6}" width="140" height="12" rx="6" fill="{SOFT}"/><rect x="120" y="{y-6}" width="{w*1.4:.0f}" height="12" rx="6" fill="{c}"/>'
b += t(50, 318, 'Top 3 fixes on page 2 →', 10.5, 700, BLUE) + '</g>'
b += f'<g transform="rotate(3 380 210)"><g filter="url(#sh)"><rect x="250" y="60" width="250" height="300" rx="14" fill="{WHITE}" stroke="{LINE}"/></g>' + t(270, 94, 'Priority fixes', 13, 800, INK, head=True)
for i, (iss, pr, c) in enumerate([('Fix broken internal links', 'High', ('#FEE2E2', RED)), ('Compress hero images', 'High', ('#FEE2E2', RED)), ('Write meta descriptions', 'Med', ('#FEF3C7', AMBER)), ('Add FAQ schema', 'Low', ('#DCFCE7', GREEN)), ('Merge thin pages', 'Med', ('#FEF3C7', AMBER))]):
    y = 112 + i * 46
    b += f'<rect x="266" y="{y}" width="218" height="38" rx="8" fill="{SOFT}"/>' + pill(274, y + 9, pr, *c, w=42, size=9) + t(324, y + 23, iss, 10.5, 600)
b += '</g>'
write('report-audit.svg', svg(520, 400, b, 'Example audit report: executive summary and prioritised fixes'))
print('v2 art written')
