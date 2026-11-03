// Article cover images (1200x675) for the starter Insights posts -> theme assets/images/covers/{slug}.png
// Run: NODE_PATH=$(npm root -g) node tools/build_covers.js && python3 tools/build_package_images.py --covers
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..'); const T = ROOT + '/wp-content/themes/seo-booster';
const posts = [
  ['citations-vs-profile-backlinks', 'Link building', 'Citations vs profile backlinks', 'art-offpage'],
  ['choose-guest-post-dr-tier', 'Link building', 'Choosing a guest post DR tier', 'report-links'],
  ['wordpress-speed-checklist', 'Websites', 'WordPress speed checklist', 'art-technical'],
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 675 } });
  for (const [slug, cat, title, art] of posts) {
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>@font-face{font-family:M;src:url(file://${T}/assets/fonts/manrope-latin-wght.woff2)}@font-face{font-family:I;src:url(file://${T}/assets/fonts/inter-latin-wght.woff2)}
    body{margin:0}.c{position:relative;width:1200px;height:675px;overflow:hidden;background:radial-gradient(800px 420px at 85% 0%,#1E3A8A 0%,rgba(12,25,48,0) 60%),#0C1930}
    .g{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:56px 56px}
    .e{position:absolute;left:72px;top:72px;font:700 24px I;letter-spacing:.12em;text-transform:uppercase;color:#B9F24C}
    h1{position:absolute;left:72px;top:120px;width:520px;margin:0;font:800 64px/1.05 M;letter-spacing:-.03em;color:#fff}
    .l{position:absolute;left:72px;bottom:64px;font:800 26px M;color:#fff}.l b{color:#B9F24C}
    img{position:absolute;right:-20px;top:90px;width:600px;background:#fff;border-radius:24px;padding:16px;box-sizing:border-box;filter:drop-shadow(0 30px 60px rgba(0,0,0,.45))}</style></head>
    <body><div class="c"><div class="g"></div><div class="e">${cat}</div><h1>${title}</h1><img src="file://${T}/assets/images/${art}.svg"><div class="l">SEO <b>Booster</b> · Insights</div></div></body></html>`;
    const tmp = path.join(T, 'assets/images/covers/_t.html'); fs.writeFileSync(tmp, html);
    await p.goto('file://' + tmp); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(T, 'assets/images/covers', slug + '.png') }); fs.unlinkSync(tmp);
  }
  await b.close(); console.log('covers done');
})();
