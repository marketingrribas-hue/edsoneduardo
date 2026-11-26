const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'cronograma', 'cronograma.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'Cronograma_30_dias_Clicia_Nascimento.pdf'), format: 'A4', printBackground: true });
  await b.close();
})();
