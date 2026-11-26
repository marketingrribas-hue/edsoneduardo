// node render.js [dia...]  -> out/dia_XX/*.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const root = __dirname, build = path.join(root, 'build'), out = path.join(root, 'out');
  const only = process.argv.slice(2).map(Number);
  const files = fs.readdirSync(build).filter(f => /^dia_\d+\.html$/.test(f))
    .filter(f => !only.length || only.includes(+f.match(/\d+/)[0])).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const report = [];
  for (const f of files) {
    const d = f.match(/\d+/)[0];
    await page.goto('file://' + path.join(build, f));
    await page.waitForSelector('body[data-ready="1"]');
    await page.waitForTimeout(150);
    const dir = path.join(out, `dia_${d}`); fs.mkdirSync(dir, { recursive: true });
    for (const id of ['s1', 's2', 's3', 's4', 's5', 'card']) {
      const el = await page.$('#' + id);
      const name = id === 'card' ? `dia${d}_card.png` : `dia${d}_carrossel_${id[1]}.png`;
      await el.screenshot({ path: path.join(dir, name) });
    }
    const scales = await page.$$eval('.fitbox', b => b.map(x => x.dataset.scale));
    report.push(`${d}: ${scales.join(' ')}`);
  }
  await browser.close();
  console.log(report.join('\n'));
})();
