const puppeteer = require('puppeteer');
const url = process.argv[2];
const marketCookie = process.argv[3];

(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36');

  if (marketCookie) {
    await page.setCookie({
      name: 'market',
      value: marketCookie,
      domain: '.godaddy.com',
      path: '/',
    });
  }

  const response = await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 60000});
  await new Promise(r => setTimeout(r, 12000));
  const finalUrl = page.url();

  const result = await page.evaluate(() => {
    const html = document.documentElement.outerHTML;
    const seen = new Set();
    const packages = [];
    const ppRegex = /productPackage["']:\s*["']([^"']+)["']/g;
    let m;
    while ((m = ppRegex.exec(html)) !== null) {
      const pkg = m[1];
      if (seen.has(pkg)) continue;
      seen.add(pkg);
      const before = html.slice(Math.max(0, m.index - 3000), m.index);
      const after  = html.slice(m.index, Math.min(html.length, m.index + 1000));

      const ptM  = before.match(/"planType"\s*:\s*"([^"]+)"/g);
      const flM  = before.match(/"flag"\s*:\s*(true|false)/g);
      const ftM  = before.match(/"flagText"\s*:\s*"([^"]+)"/g);
      const ptgM = before.match(/"priceTag"\s*:\s*"([^"]+)"/g);
      const opM  = before.match(/"oldPrice"\s*:\s*"([^"]+)"/g);
      const spM  = before.match(/"price"\s*:\s*"([^"]+)"/g);
      const tmM  = after.match(/"productPackageTermLengthInMonths"\s*:\s*(\d+)/);
      const itcM = after.match(/itemTrackingCode["']:\s*["']([^"']+)["']/);
      const dstM = after.match(/["']destination["']:\s*["']([^"']+)["']/);

      const recommended = flM ? flM[flM.length - 1].includes('true') : false;
      packages.push({
        productPackage: pkg,
        planType:       ptM  ? ptM[ptM.length - 1].replace(/.*"planType"\s*:\s*"/, '').replace(/"$/, '')   : null,
        recommended,
        recommendedLabel: recommended && ftM ? ftM[ftM.length - 1].replace(/.*"flagText"\s*:\s*"/, '').replace(/"$/, '') : null,
        priceTag:       ptgM ? ptgM[ptgM.length - 1].replace(/.*"priceTag"\s*:\s*"/, '').replace(/"$/, '') : null,
        oldPrice:       opM  ? opM[opM.length - 1].replace(/.*"oldPrice"\s*:\s*"/, '').replace(/"$/, '')   : null,
        salePrice:      spM  ? spM[spM.length - 1].replace(/.*"price"\s*:\s*"/, '').replace(/"$/, '')      : null,
        termLengthMonths: tmM ? parseInt(tmM[1]) : null,
        itc:            itcM ? itcM[1] : null,
        destination:    dstM ? dstM[1] : null,
      });
    }
    return {productPackages: packages};
  });

  console.log(JSON.stringify({
    cookie: marketCookie || null,
    inputUrl: url,
    finalUrl,
    status: response ? response.status() : null,
    ...result,
  }, null, 2));
  await browser.close();
})();
