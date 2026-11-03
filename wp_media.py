#!/usr/bin/env python3
"""
Renders on-brand illustrations (HTML/CSS/SVG -> Chromium -> WebP) into wordpress/data/media/:
  products/<sku>.webp  (1200x900)   services/<key>.webp (1200x900)   blog/<slug>.webp (1200x675)

    python3 wp_media.py            # needs Playwright + Chromium (preinstalled in the build env)
"""
import html
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "src", "assets")
OUT = os.path.join(ROOT, "wordpress", "data", "media")
SPRITE = open(os.path.join(ASSETS, "img", "icons.svg"), encoding="utf-8").read().replace('<svg xmlns="http://www.w3.org/2000/svg">', '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">')
LABEL = {"seo": "SEO", "link-building": "Link Building", "website-development": "Website Development",
         "content-writing": "Content Writing", "ppc": "PPC Management", "social-media-marketing": "Social Media"}
e = html.escape

CSS = f"""
@font-face{{font-family:Outfit;src:url('file://{ASSETS}/fonts/outfit-var.woff2');font-weight:100 900}}
@font-face{{font-family:Inter;src:url('file://{ASSETS}/fonts/inter-var.woff2');font-weight:100 900}}
*{{box-sizing:border-box;margin:0}}
body{{background:#07010f;font-family:Inter,sans-serif;color:#f6f3fb}}
.c{{position:relative;overflow:hidden;background:radial-gradient(900px 600px at -10% -20%,rgba(123,60,255,.55),transparent 60%),radial-gradient(800px 600px at 115% -10%,rgba(255,79,174,.38),transparent 60%),radial-gradient(700px 500px at 80% 120%,rgba(255,180,140,.18),transparent 60%),#0a0218}}
.c::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:radial-gradient(ellipse 80% 70% at 40% 40%,#000 30%,transparent 80%)}}
.logo{{position:absolute;left:64px;bottom:52px;width:170px}}
.pill{{display:inline-flex;align-items:center;gap:10px;padding:10px 18px;border-radius:999px;border:1.5px solid rgba(255,122,198,.55);background:rgba(255,122,198,.08);font:700 19px Outfit;letter-spacing:.14em;text-transform:uppercase;color:#ff9fd6}}
.pill svg{{width:22px;height:22px;color:#ff7ac6}}
h1{{font:700 76px/1.02 Outfit;letter-spacing:-.03em;margin:26px 0 18px}}
h1 .g{{background:linear-gradient(100deg,#b57bff,#ff7ac6 55%,#ffb48c);-webkit-background-clip:text;color:transparent}}
.tag{{font:500 26px/1.4 Inter;color:#cbc2dc;max-width:520px}}
.tiers{{display:flex;gap:8px;margin-top:30px}}.tiers i{{width:44px;height:8px;border-radius:9px;background:rgba(255,255,255,.12)}}.tiers i.on{{background:linear-gradient(90deg,#b57bff,#ff7ac6)}}
.copy{{position:absolute;left:64px;top:64px;width:560px;z-index:2}}
.vis{{position:absolute;right:56px;top:50%;transform:translateY(-50%);width:500px;z-index:1}}
.panel{{border-radius:24px;background:linear-gradient(160deg,rgba(255,255,255,.1),rgba(255,255,255,.03));border:1.5px solid rgba(255,255,255,.16);box-shadow:0 40px 90px -30px rgba(181,123,255,.6);padding:22px;backdrop-filter:blur(8px)}}
.dots{{display:flex;gap:7px;margin-bottom:16px}}.dots i{{width:11px;height:11px;border-radius:50%;background:#ff6b8b}}.dots i:nth-child(2){{background:#ffc35a}}.dots i:nth-child(3){{background:#5ee6b8}}
.inner{{border-radius:16px;background:rgba(7,1,15,.6);border:1px solid rgba(255,255,255,.09);padding:18px}}
.lbl{{font:600 15px Outfit;color:#a99fc0;letter-spacing:.06em;text-transform:uppercase}}
.kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}}
.kpi{{border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);padding:12px}}
.kpi span{{display:block;font:600 12px Outfit;color:#8c82a3;letter-spacing:.08em;text-transform:uppercase}}.kpi b{{font:700 22px Outfit;color:#5ee6b8}}
.serp{{position:absolute;left:-60px;bottom:-56px;width:330px;background:#fff;color:#1d1530;border-radius:16px;padding:16px 18px;transform:rotate(-3deg);box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}}
.serp small{{font-size:13px;color:#5b5370}}.serp b{{display:block;font:600 18px Outfit;color:#3b1fa8;margin:4px 0}}.serp p{{font-size:13px;color:#5b5370}}
.serp .r{{position:absolute;top:-16px;right:-14px;background:linear-gradient(100deg,#b57bff,#ff7ac6);color:#16051f;font:800 17px Outfit;padding:9px 12px;border-radius:999px}}
.line{{height:12px;border-radius:9px;background:rgba(255,255,255,.12);margin:12px 0}}
.kw{{display:inline-block;padding:6px 12px;border-radius:999px;font:600 14px Outfit;margin:4px 6px 0 0;background:rgba(255,122,198,.16);color:#ffb3df;border:1px solid rgba(255,122,198,.35)}}
.phone{{width:300px;margin-left:auto;margin-right:60px;border-radius:44px;padding:14px;background:#120827;border:2px solid rgba(255,255,255,.18);box-shadow:0 40px 90px -30px rgba(255,122,198,.6)}}
.post{{border-radius:28px;overflow:hidden;background:#1a0f33}}
.post .img{{height:250px;background:radial-gradient(circle at 30% 30%,#ff7ac6,transparent 60%),radial-gradient(circle at 70% 70%,#b57bff,transparent 60%),#2a1452}}
.post .row{{display:flex;gap:16px;padding:14px 16px;font:600 16px Outfit;color:#ffb3df}}
.bubble{{position:absolute;padding:12px 16px;border-radius:16px;background:#fff;color:#2a1452;font:700 18px Outfit;box-shadow:0 20px 40px -15px rgba(0,0,0,.6)}}
.ad{{background:#fff;color:#1d1530;border-radius:16px;padding:16px 18px;margin-bottom:14px}}
.ad small{{font:700 13px Inter;color:#1d1530}}.ad b{{display:block;font:600 20px Outfit;color:#1a0dab;margin:6px 0}}.ad p{{font-size:14px;color:#4d5156}}
.blog .copy{{width:640px}}.blog h1{{font-size:58px;line-height:1.08}}.blog .vis{{width:430px;right:44px}}
"""


def icon(n):
    return f'<svg><use href="#{n}"/></svg>'


def visual(key):
    if key == "seo":
        return """<div class="panel"><div class="dots"><i></i><i></i><i></i></div><div class="inner"><div class="lbl">Organic clicks</div>
<svg viewBox="0 0 400 170" width="100%"><defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#b57bff"/><stop offset=".6" stop-color="#ff7ac6"/><stop offset="1" stop-color="#ffb48c"/></linearGradient><linearGradient id="a" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ff7ac6" stop-opacity=".4"/><stop offset="1" stop-color="#ff7ac6" stop-opacity="0"/></linearGradient></defs>
<g stroke="rgba(255,255,255,.08)"><path d="M0 40h400M0 85h400M0 130h400"/></g><path d="M0 150 C50 146 70 136 110 130 S170 120 200 100 S260 92 290 70 S350 40 400 14 L400 170 L0 170Z" fill="url(#a)"/>
<path d="M0 150 C50 146 70 136 110 130 S170 120 200 100 S260 92 290 70 S350 40 400 14" fill="none" stroke="url(#l)" stroke-width="5" stroke-linecap="round"/><circle cx="400" cy="14" r="7" fill="#ffb48c"/></svg>
<div class="kpis"><div class="kpi"><span>Rank</span><b>Top 3</b></div><div class="kpi"><span>Traffic</span><b>↑</b></div><div class="kpi"><span>Leads</span><b>↑</b></div></div></div>
<div class="serp"><span class="r">#1</span><small>● yourbusiness.com</small><b>Your Business — Trusted Experts</b><p>Found first by the customers searching for you.</p></div></div>"""
    if key == "link-building":
        nodes = [(250, 70, "DA 50+"), (430, 150, "DA 40+"), (440, 330, "Niche blog"), (260, 420, "DA 30+"), (70, 330, "Guest post"), (60, 150, "Citation")]
        lines = "".join(f'<line x1="250" y1="245" x2="{x}" y2="{y}" stroke="url(#lk)" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>' for x, y, _ in nodes)
        circ = "".join(f'<g><circle cx="{x}" cy="{y}" r="44" fill="#1a0f33" stroke="rgba(255,255,255,.25)" stroke-width="2"/><text x="{x}" y="{y + 6}" text-anchor="middle" font-family="Outfit" font-weight="700" font-size="17" fill="#ffb3df">{t}</text></g>' for x, y, t in nodes)
        return f"""<svg viewBox="0 0 500 490" width="100%"><defs><linearGradient id="lk" x1="0" x2="1"><stop offset="0" stop-color="#b57bff"/><stop offset="1" stop-color="#ff7ac6"/></linearGradient>
<radialGradient id="cg"><stop offset="0" stop-color="#ff7ac6"/><stop offset="1" stop-color="#b57bff"/></radialGradient></defs>{lines}{circ}
<circle cx="250" cy="245" r="78" fill="url(#cg)"/><text x="250" y="238" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="24" fill="#16051f">Your</text><text x="250" y="266" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="24" fill="#16051f">website</text></svg>"""
    if key == "website-development":
        return """<div class="panel"><div class="dots"><i></i><i></i><i></i></div><div class="inner">
<div style="height:150px;border-radius:12px;background:linear-gradient(120deg,#b57bff,#ff7ac6 60%,#ffb48c);padding:22px"><div style="width:62%;height:16px;border-radius:9px;background:rgba(22,5,31,.55)"></div><div style="width:44%;height:12px;border-radius:9px;background:rgba(22,5,31,.35);margin-top:12px"></div><div style="width:120px;height:34px;border-radius:99px;background:#16051f;margin-top:22px"></div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px">""" + "".join('<div style="height:110px;border-radius:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);padding:12px"><div style="width:30px;height:30px;border-radius:9px;background:rgba(255,122,198,.35)"></div><div class="line" style="margin:14px 0 8px"></div><div class="line" style="width:60%;margin:0"></div></div>' for _ in range(3)) + """</div>
<div class="kpis"><div class="kpi"><span>Speed</span><b>98</b></div><div class="kpi"><span>SEO</span><b>100</b></div><div class="kpi"><span>Mobile</span><b>✓</b></div></div></div></div>"""
    if key == "content-writing":
        return """<div class="panel"><div class="dots"><i></i><i></i><i></i></div><div class="inner">
<div class="lbl">Blog post · Draft</div><div style="font:700 26px/1.25 Outfit;margin:12px 0 6px">How to choose the right SEO package</div>
<div class="line" style="width:95%"></div><div class="line" style="width:88%"></div><div class="line" style="width:92%"></div><div class="line" style="width:60%"></div>
<div style="margin-top:14px"><span class="kw">search intent</span><span class="kw">E-E-A-T</span><span class="kw">internal links</span><span class="kw">meta ✓</span></div>
<div class="kpis"><div class="kpi"><span>Readability</span><b>A+</b></div><div class="kpi"><span>SEO score</span><b>96</b></div><div class="kpi"><span>Original</span><b>100%</b></div></div></div></div>"""
    if key == "ppc":
        return """<div class="panel"><div class="dots"><i></i><i></i><i></i></div>
<div class="ad"><small>Sponsored · yourbusiness.com</small><b>Get More Customers Today | Free Quote</b><p>Trusted experts. Fast response. Book online in 60 seconds.</p></div>
<div class="inner"><div class="lbl">Conversions this month</div><svg viewBox="0 0 400 140" width="100%"><defs><linearGradient id="b" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ff7ac6"/><stop offset="1" stop-color="#b57bff"/></linearGradient></defs><g fill="url(#b)">""" + "".join(f'<rect x="{12 + i * 49}" y="{130 - h}" width="34" height="{h}" rx="7"/>' for i, h in enumerate([34, 46, 42, 62, 74, 86, 104, 124])) + """</g></svg>
<div class="kpis"><div class="kpi"><span>CPA</span><b>↓</b></div><div class="kpi"><span>ROAS</span><b>↑</b></div><div class="kpi"><span>CTR</span><b>↑</b></div></div></div></div>"""
    return """<div style="position:relative"><div class="phone"><div class="post"><div style="display:flex;align-items:center;gap:10px;padding:14px 16px"><i style="width:36px;height:36px;border-radius:50%;background:linear-gradient(120deg,#b57bff,#ff7ac6);display:block"></i><b style="font:700 16px Outfit">yourbrand</b></div>
<div class="img"></div><div class="row"><span>♥ 2,481</span><span>💬 186</span><span>↗ 92</span></div><div style="padding:0 16px 18px"><div class="line"></div><div class="line" style="width:70%"></div></div></div></div>
<span class="bubble" style="left:0;top:70px">+ Followers</span><span class="bubble" style="left:20px;bottom:90px">♥ Engagement</span><span class="bubble" style="right:0;bottom:30px">↗ Leads</span></div>"""


def card(key, title_html, tagline, pill, tier=None, blog=False):
    tiers = "" if tier is None else '<div class="tiers">' + "".join(f'<i class="{"on" if i < tier else ""}"></i>' for i in range(6)) + "</div>"
    w, h = (1200, 675) if blog else (1200, 900)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{SPRITE}
<div class="c {'blog' if blog else ''}" style="width:{w}px;height:{h}px">
<div class="copy"><span class="pill">{icon(C.SERVICES[key]['icon'])}{e(pill)}</span><h1>{title_html}</h1><p class="tag">{e(tagline)}</p>{tiers}</div>
<div class="vis">{visual(key)}</div>
<img class="logo" src="file://{ASSETS}/img/logo-rankright-media.png" alt=""></div></body></html>"""


def jobs():
    out = []
    for key in C.SERVICE_ORDER:
        s = C.SERVICES[key]
        out.append((f"services/{key}.webp", card(key, f'<span class="g">{e(LABEL[key])}</span><br>Services', s["menu_blurb"], "RankRight Media"), (1200, 900)))
        for i, p in enumerate(s["packages"]["items"]):
            name = p["name"]
            out.append((f"products/{p['id']}.webp", card(key, f'<span class="g">{e(name)}</span>', p["tagline"], f"{LABEL[key]} package", tier=i + 1), (1200, 900)))
    posts_dir = os.path.join(ROOT, "wordpress", "content", "posts")
    if os.path.isdir(posts_dir):
        for f in sorted(os.listdir(posts_dir)):
            raw = open(os.path.join(posts_dir, f), encoding="utf-8").read()
            meta = json.loads(raw.split("-->", 1)[0].replace("<!--", "", 1))
            out.append((f"blog/{meta['slug']}.webp", card(meta["service"], e(meta["image_title"]), meta["image_sub"], meta["category"], blog=True), (1200, 675)))
    return out


NODE = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  for (const j of jobs) {
    await p.setViewportSize({ width: j.w, height: j.h });
    await p.goto('file://' + j.html);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(120);
    await p.screenshot({ path: j.png, clip: { x: 0, y: 0, width: j.w, height: j.h } });
  }
  await b.close();
})();
"""


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    tmp = tempfile.mkdtemp()
    js = []
    todo = [j for j in jobs() if j[0].startswith(only)]
    for rel, doc, (w, h) in todo:
        hp = os.path.join(tmp, rel.replace("/", "_") + ".html")
        open(hp, "w", encoding="utf-8").write(doc)
        js.append({"html": hp, "png": hp + ".png", "w": w, "h": h, "rel": rel})
    jf = os.path.join(tmp, "jobs.json")
    json.dump(js, open(jf, "w"))
    nf = os.path.join(tmp, "render.js")
    open(nf, "w").write(NODE)
    env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"], text=True).strip())
    subprocess.check_call(["node", nf, jf], env=env)
    for j in js:
        dst = os.path.join(OUT, j["rel"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        Image.open(j["png"]).convert("RGB").save(dst, "WEBP", quality=82, method=6)
    print(f"rendered {len(js)} images")


if __name__ == "__main__":
    main()
