"""Generates the theme's SVG illustrations and icons (wp-content/themes/seo-booster/assets/images).
Run: python3 tools/build_art.py   — pure SVG, original artwork, no external assets."""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'wp-content', 'themes', 'seo-booster', 'assets', 'images')
os.makedirs(OUT, exist_ok=True)
INK, INK2, BLUE, BLUE_D, LIME, LINE, SOFT, B50, WHITE, SLATE = '#0C1930', '#13254A', '#2563EB', '#1D4ED8', '#B9F24C', '#E2E8F0', '#F8FAFC', '#EFF4FF', '#FFFFFF', '#94A3B8'

def svg(w, h, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n'

def lines(x, y, widths, gap=14, color=LINE, h=7):
    return ''.join(f'<rect x="{x}" y="{y+i*gap}" width="{w}" height="{h}" rx="3.5" fill="{color}"/>' for i, w in enumerate(widths))

def window(x, y, w, h, inner='', dark=False):
    bg, bar, dot = (INK2, '#1B2F5A', '#2B416E') if dark else (WHITE, SOFT, LINE)
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{"#24396A" if dark else LINE}"/>'
            f'<path d="M{x} {y+16} a16 16 0 0 1 16 -16 h{w-32} a16 16 0 0 1 16 16 v14 h-{w} z" fill="{bar}"/>'
            f'<circle cx="{x+18}" cy="{y+15}" r="4" fill="{dot}"/><circle cx="{x+32}" cy="{y+15}" r="4" fill="{dot}"/><circle cx="{x+46}" cy="{y+15}" r="4" fill="{dot}"/>'
            f'{inner}</g>')

def bars(x, y, heights, w=22, gap=12, base=120, colors=None):
    out = ''
    for i, hgt in enumerate(heights):
        c = (colors or [BLUE] * len(heights))[i]
        out += f'<rect x="{x+i*(w+gap)}" y="{y+base-hgt}" width="{w}" height="{hgt}" rx="5" fill="{c}"/>'
    return out

def write(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)

# ---------- Home hero ----------
hero = ''
hero += '<defs><linearGradient id="g1" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="#1D4ED8"/></linearGradient></defs>'
hero += window(40, 40, 400, 290, dark=False, inner=(
    lines(64, 82, [140, 90]) +
    bars(70, 120, [38, 56, 50, 78, 96, 120], colors=[B50, B50, '#BFD3FE', '#93B4FB', BLUE, BLUE_D], w=34, gap=16) +
    f'<polyline points="87,224 137,200 187,206 237,170 287,146 337,112" fill="none" stroke="{LIME}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<circle cx="337" cy="112" r="7" fill="{LIME}" stroke="{INK}" stroke-width="3"/>'
    f'<rect x="64" y="262" width="352" height="1.5" fill="{LINE}"/>' + lines(64, 280, [120, 70], color=LINE)))
# link graph card
hero += window(300, 200, 240, 190, dark=True, inner=(
    f'<g stroke="{SLATE}" stroke-opacity=".45" stroke-width="2">'
    f'<line x1="420" y1="300" x2="350" y2="258"/><line x1="420" y1="300" x2="490" y2="250"/><line x1="420" y1="300" x2="360" y2="352"/><line x1="420" y1="300" x2="500" y2="350"/><line x1="490" y1="250" x2="510" y2="300"/></g>'
    f'<circle cx="420" cy="300" r="18" fill="{LIME}"/><path d="M412 300h16M420 292v16" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    f'<circle cx="350" cy="258" r="10" fill="{BLUE}"/><circle cx="490" cy="250" r="10" fill="{BLUE}"/><circle cx="360" cy="352" r="8" fill="#60A5FA"/><circle cx="500" cy="350" r="9" fill="#60A5FA"/><circle cx="510" cy="300" r="6" fill="#93C5FD"/>'))
# checklist card
hero += (f'<g><rect x="0" y="250" width="230" height="150" rx="16" fill="{WHITE}" stroke="{LINE}"/>' +
         ''.join(f'<circle cx="28" cy="{284+i*34}" r="10" fill="{LIME}"/><path d="M23 {284+i*34}l3.5 3.5 6.5-6.5" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>' + lines(48, 280+i*34, [w]) for i, w in enumerate([130, 100, 150])) +
         '</g>')
write('hero-growth.svg', svg(560, 410, hero, 'Illustration: growth chart, link network and completed checklist'))

# ---------- Service icons ----------
def icon(name, glyph, title):
    body = f'<rect width="56" height="56" rx="14" fill="{B50}"/>{glyph}'
    write(f'icon-{name}.svg', svg(56, 56, body, title))
S = f'fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
icon('offpage', f'<path d="M24 32l8-8" {S}/><path d="M21 28l-3 3a5.5 5.5 0 0 0 7.8 7.8l3-3" {S}/><path d="M35 28l3-3a5.5 5.5 0 0 0-7.8-7.8l-3 3" {S}/><circle cx="40" cy="40" r="5" fill="{LIME}"/>', 'Link building icon')
icon('audit', f'<rect x="15" y="13" width="20" height="26" rx="3" {S}/><path d="M20 21h10M20 27h6" {S}/><circle cx="35" cy="35" r="6" fill="{LIME}" stroke="{INK}" stroke-width="2.6"/><path d="M39.5 39.5l4 4" {S}/>', 'SEO audit icon')
icon('technical', f'<path d="M22 22l-6 6 6 6M34 22l6 6-6 6" {S}/><path d="M30 18l-4 20" {S}/><circle cx="41" cy="16" r="4" fill="{LIME}"/>', 'Technical SEO icon')
icon('webdev', f'<rect x="12" y="15" width="32" height="26" rx="4" {S}/><path d="M12 22h32" {S}/><rect x="17" y="27" width="10" height="9" rx="2" fill="{LIME}"/><path d="M31 28h8M31 33h5" {S}/>', 'Website development icon')
icon('maintenance', f'<path d="M33 15a7 7 0 0 0-8.5 9L15 33.5a3.5 3.5 0 0 0 5 5L29.5 29a7 7 0 0 0 9-8.5l-4.5 4.5-4-1-1-4z" {S}/><circle cx="40" cy="40" r="4.5" fill="{LIME}"/>', 'Website maintenance icon')
icon('content', f'<path d="M17 39l2-7 15-15 5 5-15 15z" {S}/><path d="M30 21l5 5" {S}/><path d="M17 43h22" stroke="{LIME}" stroke-width="3.5" stroke-linecap="round"/>', 'Content writing icon')
icon('design', f'<path d="M28 13a15 15 0 1 0 0 30c2.5 0 3-2 2-3.5s-.5-3.5 2-3.5h4a7 7 0 0 0 7-7c0-9-6.7-16-15-16z" {S}/><circle cx="21" cy="25" r="2.6" fill="{INK}"/><circle cx="28" cy="20" r="2.6" fill="{BLUE}"/><circle cx="35" cy="25" r="3.2" fill="{LIME}" stroke="{INK}" stroke-width="1.5"/>', 'Graphic design icon')
# value icons
icon('scope', f'<rect x="15" y="14" width="26" height="30" rx="4" {S}/><path d="M21 23h14M21 29h14M21 35h8" {S}/><circle cx="41" cy="16" r="5" fill="{LIME}"/>', 'Clear scope icon')
icon('report', f'<path d="M16 40V24M24 40V18M32 40v-9M40 40V14" {S}/><path d="M13 43h30" stroke="{LIME}" stroke-width="3.5" stroke-linecap="round"/>', 'Reporting icon')
icon('human', f'<circle cx="28" cy="21" r="6" {S}/><path d="M17 41c1.5-6 6-9 11-9s9.5 3 11 9" {S}/><circle cx="40" cy="16" r="4" fill="{LIME}"/>', 'Human review icon')
icon('shield', f'<path d="M28 13l12 5v9c0 8-5.5 13-12 16-6.5-3-12-8-12-16v-9z" {S}/><path d="M23 28l3.5 3.5 7-7" stroke="{BLUE}" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>', 'Safe methods icon')

# ---------- Service hero illustrations ----------
def service_art(name, inner, title):
    body = f'<rect x="0" y="0" width="520" height="380" rx="24" fill="{INK2}" opacity="0"/>' + inner
    write(f'art-{name}.svg', svg(520, 380, body, title))

service_art('offpage', window(30, 30, 300, 230, inner=lines(54, 72, [160, 110, 180, 140]) + f'<rect x="54" y="140" width="250" height="96" rx="10" fill="{B50}"/>' + lines(70, 156, [180, 140, 200], color='#BFD3FE')) +
    window(250, 140, 240, 210, dark=True, inner=(
        f'<g stroke="{SLATE}" stroke-opacity=".5" stroke-width="2"><line x1="370" y1="250" x2="300" y2="210"/><line x1="370" y1="250" x2="445" y2="205"/><line x1="370" y1="250" x2="300" y2="310"/><line x1="370" y1="250" x2="455" y2="310"/><line x1="370" y1="250" x2="375" y2="325"/></g>'
        f'<circle cx="370" cy="250" r="22" fill="{LIME}"/><path d="M362 252l6-6M359 250l-2.5 2.5a4.5 4.5 0 0 0 6.4 6.4L365 256.5M375 250l2.5-2.5a4.5 4.5 0 0 0-6.4-6.4L368.6 243.5" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        f'<circle cx="300" cy="210" r="11" fill="{BLUE}"/><circle cx="445" cy="205" r="11" fill="{BLUE}"/><circle cx="300" cy="310" r="9" fill="#60A5FA"/><circle cx="455" cy="310" r="10" fill="#60A5FA"/><circle cx="375" cy="325" r="7" fill="#93C5FD"/>')),
    'Illustration: a web page connected to a network of referring websites')
service_art('audit', window(40, 30, 330, 300, inner=lines(64, 72, [150, 100]) +
    ''.join(f'<rect x="64" y="{110+i*44}" width="282" height="34" rx="8" fill="{SOFT}" stroke="{LINE}"/><circle cx="84" cy="{127+i*44}" r="7" fill="{c}"/>' + lines(100, 124+i*44, [w]) for i, (c, w) in enumerate([('#EF4444', 170), ('#F59E0B', 140), ('#F59E0B', 190), (LIME, 120), (LIME, 160)]))) +
    f'<g><circle cx="400" cy="230" r="70" fill="{WHITE}" stroke="{INK}" stroke-width="10"/><circle cx="400" cy="230" r="52" fill="{B50}"/><path d="M372 238l18 18 34-40" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M450 282l40 40" stroke="{INK}" stroke-width="16" stroke-linecap="round"/></g>',
    'Illustration: a prioritised audit report under a magnifying glass')
service_art('technical', window(30, 30, 460, 300, dark=True, inner=(
    ''.join(f'<rect x="{60+ind*24}" y="{80+i*30}" width="{w}" height="10" rx="5" fill="{c}"/>' for i, (ind, w, c) in enumerate([(0, 120, '#60A5FA'), (1, 200, SLATE), (2, 150, LIME), (2, 90, SLATE), (1, 60, '#60A5FA'), (0, 170, SLATE), (1, 130, LIME)])) +
    f'<g transform="translate(330 120)"><circle cx="70" cy="80" r="74" fill="#1B2F5A"/><path d="M20 110a56 56 0 1 1 100 0" fill="none" stroke="#2B416E" stroke-width="14" stroke-linecap="round"/><path d="M20 110a56 56 0 0 1 86-62" fill="none" stroke="{LIME}" stroke-width="14" stroke-linecap="round"/><path d="M70 104l28-38" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/><circle cx="70" cy="104" r="9" fill="{WHITE}"/></g>')),
    'Illustration: site code alongside a page speed gauge')
service_art('webdev', window(20, 30, 380, 290, inner=(
    f'<rect x="44" y="70" width="332" height="96" rx="10" fill="{INK}"/>' + lines(64, 92, [170, 120], color='#2B416E', gap=18, h=10) + f'<rect x="64" y="134" width="80" height="18" rx="6" fill="{LIME}"/>' +
    ''.join(f'<rect x="{44+i*114}" y="182" width="104" height="110" rx="10" fill="{SOFT}" stroke="{LINE}"/><rect x="{56+i*114}" y="194" width="30" height="30" rx="8" fill="{B50}"/>' + lines(56+i*114, 236, [72, 50]) for i in range(3)))) +
    f'<g><rect x="380" y="110" width="120" height="230" rx="20" fill="{INK}"/><rect x="390" y="128" width="100" height="194" rx="10" fill="{WHITE}"/><rect x="398" y="138" width="84" height="46" rx="6" fill="{BLUE}"/>' + lines(398, 196, [70, 54, 64], gap=14) + f'<rect x="398" y="244" width="40" height="12" rx="5" fill="{LIME}"/><rect x="398" y="266" width="84" height="44" rx="6" fill="{SOFT}" stroke="{LINE}"/></g>',
    'Illustration: a responsive website on desktop and mobile')
service_art('maintenance', window(30, 40, 320, 250, inner=(
    lines(54, 82, [150, 100]) + ''.join(f'<rect x="54" y="{116+i*40}" width="272" height="30" rx="8" fill="{SOFT}" stroke="{LINE}"/><circle cx="72" cy="{131+i*40}" r="8" fill="{LIME}"/><path d="M68 {131+i*40}l3 3 5-5" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>' + lines(90, 128+i*40, [w]) for i, w in enumerate([150, 120, 170, 110])))) +
    f'<g transform="translate(300 150)"><circle cx="95" cy="95" r="90" fill="{BLUE}"/><path d="M128 52a30 30 0 0 0-36 38L50 132a14 14 0 0 0 20 20l42-42a30 30 0 0 0 38-36l-19 19-17-4-4-17z" fill="{WHITE}"/><circle cx="160" cy="40" r="16" fill="{LIME}"/></g>',
    'Illustration: completed maintenance checklist and a wrench')
service_art('content', window(40, 30, 300, 320, inner=(
    lines(64, 72, [200, 150], h=12, gap=20, color=INK) + lines(64, 124, [250, 230, 245, 200, 240, 180], gap=16) +
    f'<rect x="64" y="226" width="240" height="2" fill="{LINE}"/>' + lines(64, 244, [140], h=10, color=BLUE) + lines(64, 270, [250, 220, 235, 120], gap=16))) +
    f'<g transform="translate(330 70)"><rect x="0" y="0" width="160" height="200" rx="16" fill="{INK}"/>' + ''.join(f'<rect x="20" y="{28+i*36}" width="{w}" height="18" rx="9" fill="{c}"/>' for i, (w, c) in enumerate([(120, LIME), (90, '#2B416E'), (110, '#2B416E'), (70, '#2B416E'), (100, '#2B416E')])) +
    f'</g><path d="M300 330l20-60 120-120 40 40-120 120z" fill="{WHITE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M420 170l40 40" stroke="{INK}" stroke-width="6"/><path d="M300 330l20-60 40 40z" fill="{LIME}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>',
    'Illustration: a structured article with headings and an outline')
service_art('design', window(30, 30, 330, 300, inner=(
    f'<rect x="54" y="66" width="282" height="150" rx="12" fill="{B50}"/><circle cx="130" cy="140" r="44" fill="{BLUE}"/><rect x="190" y="104" width="110" height="72" rx="14" fill="{INK}"/><path d="M216 160l20-30 16 22 10-12 18 20z" fill="{LIME}"/>' +
    ''.join(f'<rect x="{54+i*58}" y="234" width="48" height="48" rx="10" fill="{c}"/>' for i, c in enumerate([INK, BLUE, LIME, '#60A5FA', LINE])) + lines(54, 296, [120]))) +
    f'<g transform="translate(330 120)"><rect x="0" y="0" width="170" height="220" rx="18" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/><text x="24" y="70" font-family="Manrope, Arial, sans-serif" font-size="54" font-weight="800" fill="{INK}">Aa</text>' + lines(24, 96, [120, 90, 110], gap=18, h=9) + f'<rect x="24" y="160" width="122" height="36" rx="10" fill="{BLUE}"/></g>',
    'Illustration: brand colours, logo and typography on an artboard')

# ---------- Inner-page heroes (3 Nov 2026) ----------
def chip(x, y, w, label_w, color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{color}"/>' + f'<rect x="{x+12}" y="{y+10}" width="{label_w}" height="6" rx="3" fill="{INK}" opacity=".55"/>'

def pkg_card(x, y, w, h, accent, featured=False):
    stroke = INK if featured else LINE
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHITE}" stroke="{stroke}" stroke-width="{3 if featured else 1.5}"/>'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{int(h*.32)}" rx="16" fill="{INK}"/><rect x="{x}" y="{y+int(h*.32)-16}" width="{w}" height="16" fill="{INK}"/>'
    out += f'<rect x="{x+18}" y="{y+22}" width="{int(w*.35)}" height="26" rx="6" fill="{accent}"/>'
    out += lines(x+18, y+int(h*.32)+20, [int(w*.6), int(w*.4)], color=INK, h=9, gap=18)
    out += ''.join(f'<circle cx="{x+26}" cy="{y+int(h*.32)+76+i*22}" r="6" fill="{LIME}"/>' + lines(x+40, y+int(h*.32)+73+i*22, [int(w*.5)]) for i in range(3))
    out += f'<rect x="{x+18}" y="{y+h-46}" width="{w-36}" height="30" rx="8" fill="{BLUE}"/>'
    if featured:
        out += f'<rect x="{x+w/2-44}" y="{y-12}" width="88" height="24" rx="12" fill="{LIME}"/>'
    return out

write('art-packages.svg', svg(520, 380, pkg_card(20, 70, 150, 270, '#60A5FA') + pkg_card(185, 40, 160, 300, LIME, True) + pkg_card(360, 70, 150, 270, '#60A5FA'), 'Illustration: three package cards with the middle one highlighted'))

proc = f'<path d="M70 190 C150 90, 210 290, 270 190 S390 90, 450 190" fill="none" stroke="#2B416E" stroke-width="6" stroke-dasharray="2 14" stroke-linecap="round"/>'
for i, (cx, cy, glyph) in enumerate([(70, 190, 'M60 190h20M70 180v20'), (200, 210, 'M190 210l7 7 13-14'), (330, 170, 'M320 165h20M320 175h14'), (450, 190, 'M440 195l8-14 8 8 8-12')]):
    col = LIME if i == 3 else (BLUE if i else WHITE)
    proc += f'<circle cx="{cx}" cy="{cy}" r="44" fill="{INK2}" stroke="#2B416E" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="30" fill="{col}"/><path d="{glyph}" fill="none" stroke="{INK if col != BLUE else WHITE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    proc += f'<rect x="{cx-36}" y="{cy+58}" width="72" height="10" rx="5" fill="#2B416E"/><rect x="{cx-24}" y="{cy+76}" width="48" height="8" rx="4" fill="#1B2F5A"/>'
write('art-process.svg', svg(520, 380, proc, 'Illustration: four connected steps from order to delivery'))

ab = window(30, 40, 300, 220, inner=lines(54, 82, [160, 110]) + bars(60, 108, [30, 46, 62, 84], w=40, gap=18, base=110, colors=[B50, '#BFD3FE', BLUE, BLUE_D]) + f'<polyline points="80,200 138,184 196,168 254,140" fill="none" stroke="{LIME}" stroke-width="4" stroke-linecap="round"/>')
ab += f'<g transform="translate(250 150)"><rect width="240" height="200" rx="18" fill="{INK}"/>' + ''.join(f'<circle cx="34" cy="{40+i*44}" r="13" fill="{LIME}"/><path d="M28 {40+i*44}l4 4 8-8" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>' + lines(58, 34+i*44, [w], color='#2B416E', h=10) for i, w in enumerate([140, 110, 150, 120])) + '</g>'
write('art-about.svg', svg(520, 380, ab, 'Illustration: a growth report beside a completed delivery checklist'))

ct = f'<g><rect x="40" y="60" width="290" height="200" rx="18" fill="{WHITE}" stroke="{LINE}"/><path d="M40 78 a18 18 0 0 1 18 -18 h254 a18 18 0 0 1 18 18 L185 170 Z" fill="{B50}" stroke="{LINE}"/><path d="M40 78 L185 175 L330 78" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/></g>'
ct += f'<g transform="translate(260 170)"><rect width="220" height="96" rx="22" fill="{INK}"/><path d="M40 96 l-10 26 34 -26z" fill="{INK}"/>' + lines(26, 28, [150, 110], color='#2B416E', h=12, gap=24) + f'<circle cx="190" cy="34" r="10" fill="{LIME}"/></g>'
ct += f'<g transform="translate(120 250)"><rect width="150" height="70" rx="20" fill="{BLUE}"/>' + lines(22, 22, [100, 70], color='#93C5FD', h=10, gap=20) + '</g>'
write('art-contact.svg', svg(520, 380, ct, 'Illustration: an envelope and chat messages'))

qt = window(40, 30, 300, 310, inner=lines(64, 72, [150, 90], color=INK, h=10, gap=18) + ''.join(f'<rect x="64" y="{118+i*52}" width="252" height="38" rx="9" fill="{SOFT}" stroke="{LINE}"/>' + lines(78, 132+i*52, [w]) for i, w in enumerate([140, 180, 110])) + f'<rect x="64" y="276" width="140" height="40" rx="10" fill="{BLUE}"/>')
qt += f'<g transform="translate(300 130) rotate(-8)"><rect width="190" height="120" rx="18" fill="{INK}"/><text x="24" y="70" font-family="Manrope, Arial, sans-serif" font-size="44" font-weight="800" fill="{LIME}">Quote</text>' + lines(24, 88, [120], color='#2B416E', h=9) + '</g>'
qt += f'<circle cx="455" cy="110" r="26" fill="{LIME}"/><path d="M444 110l8 8 15-16" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
write('art-quote.svg', svg(520, 380, qt, 'Illustration: a request form and a fixed quote'))

fq = ''
for i, (x, y, w, dark) in enumerate([(40, 50, 290, False), (190, 150, 290, True), (60, 250, 260, False)]):
    fill = INK if dark else WHITE; ln = '#2B416E' if dark else LINE
    fq += f'<rect x="{x}" y="{y}" width="{w}" height="84" rx="20" fill="{fill}" stroke="{ln}"/>' + f'<circle cx="{x+38}" cy="{y+42}" r="18" fill="{LIME if dark else B50}"/><text x="{x+31}" y="{y+50}" font-family="Manrope, Arial" font-size="22" font-weight="800" fill="{INK}">{"✓" if dark else "?"}</text>' + lines(x+70, y+30, [w-120, w-170], color=ln, h=10, gap=20)
write('art-faq.svg', svg(520, 380, fq, 'Illustration: questions and answers'))

sv = pkg_card(30, 120, 150, 240, '#60A5FA')
sv += window(150, 30, 340, 230, inner=lines(174, 72, [160, 100]) + ''.join(f'<rect x="{174+(i%3)*104}" y="{108+(i//3)*68}" width="92" height="56" rx="10" fill="{c}"/>' for i, c in enumerate([B50, INK, B50, B50, B50, LIME])))
sv += f'<g transform="translate(330 220)"><circle cx="70" cy="70" r="70" fill="{BLUE}"/><path d="M40 72l20 20 40-44" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'
write('art-services.svg', svg(520, 380, sv, 'Illustration: a service menu, a package card and a completed check'))

# ---------- Sample deliverables (labelled as illustrations on the page) ----------
rl = window(10, 10, 500, 340, inner=(f'<rect x="34" y="52" width="452" height="32" rx="6" fill="{INK}"/>' + ''.join(f'<rect x="{44+i*150}" y="64" width="{w}" height="8" rx="4" fill="#2B416E"/>' for i, w in enumerate([90, 60, 70])) +
    ''.join(f'<rect x="34" y="{92+i*40}" width="452" height="34" rx="6" fill="{SOFT if i % 2 else WHITE}" stroke="{LINE}"/>' + lines(46, 105+i*40, [110]) + f'<rect x="194" y="{105+i*40}" width="{60 + (i*17) % 50}" height="8" rx="4" fill="#BFD3FE"/>' + f'<rect x="344" y="{100+i*40}" width="62" height="18" rx="9" fill="{LIME}"/><rect x="354" y="{106+i*40}" width="42" height="6" rx="3" fill="{INK}" opacity=".6"/>' for i in range(6))))
write('report-links.svg', svg(520, 360, rl, 'Illustration of a link report: each placement with its live URL and status'))
ra = (f'<g transform="translate(40 40) rotate(-4)"><rect width="250" height="300" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/><rect x="20" y="22" width="120" height="14" rx="7" fill="{INK}"/>' + lines(20, 50, [200, 170]) + bars(30, 90, [40, 70, 55, 90], w=34, gap=16, base=100, colors=[B50, '#BFD3FE', BLUE, BLUE_D]) + lines(20, 214, [210, 190, 200, 150]) + '</g>' +
      f'<g transform="translate(230 70) rotate(4)"><rect width="250" height="290" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/><rect x="20" y="22" width="100" height="14" rx="7" fill="{INK}"/>' +
      ''.join(f'<rect x="20" y="{56+i*44}" width="210" height="34" rx="8" fill="{SOFT}"/><rect x="30" y="{65+i*44}" width="46" height="16" rx="8" fill="{c}"/>' + lines(88, 70+i*44, [w]) for i, (c, w) in enumerate([('#FCA5A5', 120), ('#FCD34D', 100), ('#FCD34D', 130), (LIME, 90), (LIME, 110)])) + '</g>')
write('report-audit.svg', svg(520, 380, ra, 'Illustration of an audit report: charts and a prioritised issue list'))
print('extra art written')

print('art written to', os.path.abspath(OUT))
