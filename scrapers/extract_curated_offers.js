#!/usr/bin/env node

const puppeteer = require('puppeteer');

async function extractCuratedOffers(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36');

    console.error(`Navigating to: ${url}`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    await new Promise(resolve => setTimeout(resolve, 5000));

    const offers = await page.evaluate(() => {
      const results = [];

      const pkgidInputs = document.querySelectorAll('input[name="pkgid"]');
      pkgidInputs.forEach(input => {
        const value = input.value;
        if (value && value.startsWith('nes-')) {
          results.push({
            type: 'pkgid',
            element: 'input[name="pkgid"]',
            value: value,
            curatedOfferId: value.replace(/^nes-/, '')
          });
        }
      });

      const dataElements = document.querySelectorAll('[data-package-id], [data-offer-id], [data-curated-offer]');
      dataElements.forEach(el => {
        ['data-package-id', 'data-offer-id', 'data-curated-offer'].forEach(attr => {
          const value = el.getAttribute(attr);
          if (value && value.startsWith('nes-')) {
            results.push({
              type: attr,
              element: el.tagName.toLowerCase(),
              value: value,
              curatedOfferId: value.replace(/^nes-/, '')
            });
          }
        });
      });

      const allInputs = document.querySelectorAll('input[type="hidden"]');
      allInputs.forEach(input => {
        const value = input.value;
        if (value && value.startsWith('nes-')) {
          const exists = results.some(r => r.value === value);
          if (!exists) {
            results.push({
              type: 'hidden-input',
              element: `input[name="${input.name}"]`,
              value: value,
              curatedOfferId: value.replace(/^nes-/, '')
            });
          }
        }
      });

      // Build metadata map from the page source JSON
      // planType, flag, priceTag, oldPrice, salePrice precede productPackage; termLengthMonths follows it
      const html = document.documentElement.innerHTML;
      const metaMap = {};
      const ppRegex = /productPackage["']:\s*["']([^"']+)["']/g;
      let ppM;
      while ((ppM = ppRegex.exec(html)) !== null) {
        const pkg = ppM[1].replace(/^nes-/, '');
        if (metaMap[pkg]) continue;
        const before = html.slice(Math.max(0, ppM.index - 3000), ppM.index);
        const after  = html.slice(ppM.index, Math.min(html.length, ppM.index + 1000));

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
        metaMap[pkg] = {
          planType:       ptM  ? ptM[ptM.length - 1].replace(/.*"planType"\s*:\s*"/, '').replace(/"$/, '')   : null,
          recommended,
          recommendedLabel: recommended && ftM ? ftM[ftM.length - 1].replace(/.*"flagText"\s*:\s*"/, '').replace(/"$/, '') : null,
          priceTag:       ptgM ? ptgM[ptgM.length - 1].replace(/.*"priceTag"\s*:\s*"/, '').replace(/"$/, '') : null,
          oldPrice:       opM  ? opM[opM.length - 1].replace(/.*"oldPrice"\s*:\s*"/, '').replace(/"$/, '')   : null,
          salePrice:      spM  ? spM[spM.length - 1].replace(/.*"price"\s*:\s*"/, '').replace(/"$/, '')      : null,
          termLengthMonths: tmM ? parseInt(tmM[1]) : null,
          itc:            itcM ? itcM[1] : null,
          destination:    dstM ? dstM[1] : null,
        };
      }
      results.forEach(r => {
        const m = metaMap[r.curatedOfferId] || {};
        r.planType         = m.planType         || null;
        r.recommended      = m.recommended      || false;
        r.recommendedLabel = m.recommendedLabel || null;
        r.termLengthMonths = m.termLengthMonths || null;
        r.salePrice        = m.salePrice        || null;
        r.oldPrice         = m.oldPrice         || null;
        r.priceTag         = m.priceTag         || null;
        r.itc              = m.itc              || null;
        r.destination      = m.destination      || null;
      });

      return results;
    });

    console.log(JSON.stringify(offers, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

const url = process.argv[2];
if (!url) {
  console.error('Usage: node extract_curated_offers.js <URL>');
  process.exit(1);
}

extractCuratedOffers(url);
