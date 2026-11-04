// Renders one 1200x900 visual per package from SERVICE_CATALOG.csv into
// wp-content/plugins/seo-booster-core/data/images/{sku}.png (converted to WebP by build_package_images.py).
// Run: node tools/build_package_images.js   (uses the preinstalled Playwright)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const ART = ROOT + '/wp-content/themes/seo-booster/assets/images';
const OUT = ROOT + '/wp-content/plugins/seo-booster-core/data/images';
const csv = fs.readFileSync(ROOT + '/SERVICE_CATALOG.csv', 'utf8').trim().split('\n');
const head = csv.shift().split(',');
const parse = l => { const o = []; let cur = '', q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === ',' && !q) { o.push(cur); cur = ''; } else cur += ch; } o.push(cur); return Object.fromEntries(head.map((h, i) => [h, o[i]])); };
const ART_FOR = { 'Off-Page SEO': 'art-offpage', 'SEO Audit': 'art-audit', 'Technical SEO': 'art-technical', 'Website Development': 'art-webdev', 'Website Maintenance': 'art-maintenance', 'Content Writing': 'art-content', 'Graphic Design': 'art-design',
  'Analytics and Tracking': 'art-audit', 'Email Marketing': 'art-content', 'Marketing Automation': 'art-maintenance', 'Local SEO': 'art-local', 'Monthly SEO': 'hero-growth', 'SEO Consultancy': 'art-contact', 'Ecommerce SEO': 'art-store',
  'On-Page SEO': 'art-content', 'White Label SEO': 'art-packages', 'AI SEO': 'art-ai', 'Website Migration': 'art-migration', 'Ecommerce Website Development': 'art-store', 'PPC Management': 'art-ads', 'Facebook Ads': 'art-adcreative', 'TikTok Ads': 'art-adcreative', 'Social Media Management': 'art-social' };
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const tmp = path.join(OUT, '_tpl.html'); let n = 0;
  for (const line of csv) {
    const r = parse(line); const art = ART_FOR[r.service] || 'art-offpage';
    const qty = r.quantity && r.unit && !['service', 'project', 'scope', 'site', 'month', 'report', 'call', 'plan'].includes(r.unit) ? `${Number(r.quantity).toLocaleString('en-GB')}` : '';
    const unit = qty ? r.unit.replace('guest post', 'guest post').replace('press release', 'press release') : '';
    const dr = (r.package_title.match(/DR \d+\+/) || [])[0];
    const long = r.package_title.length > 16;
    let big, sub;
    if (dr) { big = `<div class="qty">${dr.replace(' ', '&nbsp;')}<span>Guest post</span></div>`; sub = 'Premium editorial link'; }
    else if (qty && r.unit !== 'guest post' && r.unit !== 'press release') { big = `<div class="qty">${qty}<span>${esc(unit)}</span></div>`; sub = esc(r.package_title); }
    else { big = `<div class="name${long ? ' long' : ''}">${esc(r.package_title)}</div>`; sub = esc(r.group); }
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
      @font-face{font-family:M;src:url(file://${ROOT}/wp-content/themes/seo-booster/assets/fonts/manrope-latin-wght.woff2)}
      @font-face{font-family:I;src:url(file://${ROOT}/wp-content/themes/seo-booster/assets/fonts/inter-latin-wght.woff2)}
      body{margin:0;width:1200px;height:900px;overflow:hidden;font-family:I}
      .c{position:relative;width:1200px;height:900px;background:radial-gradient(900px 520px at 90% 0%,#1E3A8A 0%,rgba(12,25,48,0) 60%),#0C1930;color:#fff}
      .grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:linear-gradient(180deg,#000,transparent 90%)}
      .eb{position:absolute;left:80px;top:80px;font:700 26px I;letter-spacing:.12em;text-transform:uppercase;color:#B9F24C}
      .qty{position:absolute;left:76px;top:140px;font:800 200px/1 M;letter-spacing:-.04em;white-space:nowrap}
      .qty span{display:block;font:700 46px M;letter-spacing:-.01em;color:#CBD5E1;margin-top:10px}
      .name{position:absolute;left:80px;top:150px;width:560px;font:800 92px/1.02 M;letter-spacing:-.03em}.name.long{font-size:70px;width:540px}
      .sub{position:absolute;left:80px;bottom:80px;font:600 30px I;color:#CBD5E1;width:560px}
      .art{position:absolute;right:-40px;bottom:30px;width:600px;background:#fff;border-radius:22px;padding:10px;box-sizing:border-box;filter:drop-shadow(0 30px 60px rgba(0,0,0,.45))}
      .logo{position:absolute;right:70px;top:70px;font:800 30px M}.logo b{color:#B9F24C}
    </style></head><body><div class="c"><div class="grid"></div><div class="eb">${esc(r.service)}</div>${big}
      <div class="sub">${sub}</div><img class="art" src="file://${ART}/${art}.svg"><div class="logo">SEO <b>Booster</b></div></div></body></html>`;
    fs.writeFileSync(tmp, html); await p.goto('file://' + tmp); await p.waitForTimeout(80);
    await p.screenshot({ path: path.join(OUT, r.package_code + '.png') }); n++;
  }
  fs.unlinkSync(tmp); await b.close(); console.log(n + ' package images');
})();
