---
name: live-surface
description: Given an ITC, surface alias (e.g. "FOS wordpress"), or prod URL, scrapes the corresponding prod page to find all live NES curated offer IDs, then looks each one up in the catalog MCP. Announces the resolved ITC and URL before scraping. Returns the active curated offers ready for clone targeting. Used standalone or invoked by /offer-pulse when a base offer ID resolves to multiple curated offer variants.
---

# /live-surface — Live Curated Offers on a Surface

Answers: "Which curated offer variants are currently live on this surface, and what are their catalog details?"

Use this when offer-pulse identifies a base offer ID connected to multiple curated offers and you need to know which specific variant to clone.

---

## Invocation

```
/live-surface <surface>
/live-surface <surface> <tier>   ← optional tier filter (basic, deluxe, ultimate, etc.)
```

`<surface>` can be an ITC, a human surface alias (see table below), or a full prod URL.

Examples:
- `/live-surface slp_wordpress`
- `/live-surface slp_wordpress deluxe`
- `/live-surface "front of site wordpress"`
- `/live-surface "FOS hosting"`
- `/live-surface https://www.godaddy.com/hosting/wordpress-hosting`

---

## Alias → ITC Lookup

Analysts often name surfaces informally. Match the input (case-insensitive) against these aliases before looking up the URL. Partial matches are fine (e.g. "FOS wordpress" → `slp_wordpress`).

| Analyst says | Resolves to ITC |
|---|---|
| FOS wordpress, MWP SLP, wordpress SLP, wordpress hosting SLP | slp_wordpress |
| FOS web hosting, web hosting SLP, hosting SLP, 4GH SLP | slp_hosting_4GH |
| FOS email, email SLP, M365 hub, M365 email hub, 365 hub | slp_365_category |
| professional email SLP, business email SLP, M365 email SLP, M365 EE SLP, email essentials SLP | slp_365_email |
| M365 business SLP, office365 SLP, M365 365 SLP, M365 SLP | slp_365 |
| WSB SLP, website builder SLP, website builder | slp_wsb_ft_getstarted_plans_nocc |
| airo wordpress SLP, airo WP SLP | slp_airo_wordpress |
| airo AI builder SLP, AI website builder SLP | slp_airoaibuilder |
| airo plus SLP | slp_airo_plus |
| VPS SLP, VPS hosting SLP | Slp_vps4_linux |
| SSL SLP, SSL certificate SLP | slp_ssl |
| security SLP, website security SLP | slp_website_security_suites |
| DM SLP, digital marketing SLP | digital_marketing_suite_reach |
| DDC, discount domain club SLP | ddc_starter_01 |
| domain auctions SLP, auctions SLP | auctionscart |
| domain value appraisal SLP, GoValue SLP | offer-govalue-api-offer-basic |
| wordpress support SLP, WP support SLP | slp_wordpress_support |
| hosting solutions SLP, hosting category SLP | slp_hosting_category |

If the analyst says **"FOS"** with no product qualifier, output:
```
"FOS" is ambiguous — which product surface?
Known FOS surfaces: wordpress, web hosting, email, website builder, VPS, SSL, website security, digital marketing, airo.
```
Do not proceed until the analyst specifies.

If no alias match and the input is not a known ITC or URL, output:
```
Surface "{input}" not recognised.
Known ITCs and aliases are listed in .claude/skills/live-surface/SKILL.md.
```
Do not proceed further.

---

## ITC → Prod URL Mapping

The scraper is the authoritative source for what offers are live. What the page returns is what is deployed — do not cross-reference against any static list, migration doc, or prior session output. The catalog MCP lookup adds metadata; it does not validate whether an offer should be there.

| ITC | Prod URL | Scrape Pattern |
|-----|----------|---------------|
| slp_wordpress | https://www.godaddy.com/hosting/wordpress-hosting | nes-prefix |
| slp_airo_wordpress | https://www.godaddy.com/airo/airo-for-wordpress | nes-prefix |
| slp_hosting_4GH | https://www.godaddy.com/hosting/web-hosting | productPackage |
| slp_365_category | https://www.godaddy.com/email | productPackage |
| slp_wsb_ft_getstarted_plans_nocc | https://www.godaddy.com/websites/website-builder | productPackage |
| slp_wordpress_support | https://www.godaddy.com/wordpress/premium-support | nes-prefix |
| slp_hosting_category | https://www.godaddy.com/hosting-solutions | nes-prefix |
| Slp_vps4_linux | https://www.godaddy.com/hosting/vps-hosting | productPackage |
| slp_ssl | https://www.godaddy.com/web-security/ssl-certificate | productPackage |
| slp_website_security_suites | https://www.godaddy.com/web-security/website-security | productPackage |
| slp_365_email | https://www.godaddy.com/email/professional-business-email | productPackage |
| slp_365 | https://www.godaddy.com/business/office-365 | productPackage |
| digital_marketing_suite_reach | https://www.godaddy.com/online-marketing/digital-marketing | productPackage |
| slp_airoaibuilder | https://www.godaddy.com/websites/ai-website-builder | productPackage |
| ddc_starter_01 | https://www.godaddy.com/domains/discount-domain-club | productPackage |
| offer-govalue-api-offer-basic | https://www.godaddy.com/domain-value-appraisal | productPackage |
| auctionscart | https://www.godaddy.com/auctions/domain-auctions | productPackage |
| slp_airo_plus | https://www.godaddy.com/airo/airo-plus | productPackage |

**Notes:**
- **M365 email hub and sub-pages:** `slp_365_category` (`/email`) is a hub page that hosts multiple product sections, each embedding its own section ITC. `slp_365_email` (`/email/professional-business-email`) and `slp_365` (`/business/office-365`) are dedicated sub-pages where all packages carry the sub-page ITC. When the analyst names a specific product (e.g., "Email Essentials", "M365 business"), route to the relevant sub-page — do not scrape the hub. When returning results from a sub-page, include a hub disclosure line in the output (see Step 5). The `slp_365_category` hub is only queried when the analyst explicitly asks for the hub or the category page.
- **`office365-tier0` ITC quirk:** On the hub (`/email`) and business page (`/business/office-365`), `office365-tier0` carries ITC `slp_powerbi` — not the page ITC. On `/email/professional-business-email` it carries `slp_365_email`. This is not a scraper error; it reflects the embedded ITC in each page's configuration.
- `https://www.godaddy.com/hosting/web-hosting` and `/selectplan` are the same ITC (`slp_hosting_4GH`). The non-selectplan URL now returns all 8 offers via the productPackage pattern — use it as the canonical URL.
- `https://www.godaddy.com/hosting/wordpress-hosting/selectplan` uses ITC `slp_wordpress` — same surface as the main URL, not a separate entry.
- `slp_wordpress_support` routes to `destination=cart` (not precheck). All others route to `destination=precheck`.
- `/web-security/ssl-certificate` and `/web-security/website-security` require the full 5-second render wait — their plan boxes load asynchronously. Earlier tests that showed NO NES used shorter wait times.
- **Geo:** Curated offer IDs are the same globally (US, UK, India confirmed identical). Displayed prices (`salePrice`, `oldPrice`) are US prices. For other markets, substitute the market-specific URL prefix (e.g., `https://www.godaddy.com/en-uk/hosting/wordpress-hosting` for UK) — the scraper will return local currency prices.
- **Pages confirmed NES-free from the 27-URL audit** (probe checked `productPackage` regex + hidden inputs, 5s render wait): `/domains`, `/domains/domain-name-generator`, `/domains/domain-broker`, `/domains/domain-protection`, `/domains/domain-investing`, `/domains/bulk-domain-search`, `/websites/online-store`, `/websites/best-ecommerce-website-builder`, `/websites/best-website-builder`, `/online-marketing/digital-marketing-services`, `/payments`, `/airo`, `/airo/airoallaccess`. These are informational/tool/lead-gen pages with no purchasable plan box.

If the ITC is not in this table, output:
```
No URL mapped for ITC "{ITC}".
Add the URL to the mapping table in .claude/skills/live-surface/SKILL.md to enable scraping.
```
Do not proceed further.

---

## Step 0 — Resolve Input and Announce

Before scraping, resolve the analyst's input to a canonical ITC + URL using the alias table and mapping table above. Then output a one-line confirmation so the analyst can catch misrouting early:

```
Resolving: "{analyst input}" → ITC: {itc} | URL: {url}
```

If the input was already an exact ITC, write `(exact match)` instead of the alias. If the input was a URL, write `(URL match)`.

Example outputs:
```
Resolving: "FOS wordpress" → ITC: slp_wordpress | URL: https://www.godaddy.com/hosting/wordpress-hosting (alias match)
Resolving: "slp_ssl" → ITC: slp_ssl | URL: https://www.godaddy.com/web-security/ssl-certificate (exact match)
Resolving: "https://www.godaddy.com/hosting/vps-hosting" → ITC: Slp_vps4_linux | URL: https://www.godaddy.com/hosting/vps-hosting (URL match)
```

---

## Step 1 — Scrape the Page

Look up the test URL and Scrape Pattern for the ITC.

**For `nes-prefix` pattern** (wordpress/hosting pages — Sitecore hidden inputs):
```bash
node scrapers/extract_curated_offers.js {URL} 2>/dev/null
```
Parse the JSON array returned. Each item has these fields — collect all:
- `curatedOfferId` — the offer slug (nes- prefix already stripped)
- `planType` — canonical product name from Sitecore (e.g., `"Hosting for WordPress Basic"`)
- `recommended` — true/false; whether this tier is the featured/recommended plan
- `recommendedLabel` — label text when recommended=true (e.g., `"RECOMMENDED"`), else null
- `termLengthMonths` — default term configured on the surface (e.g., 12), else null
- `salePrice` — displayed sale price (e.g., `"$6.99"`), else null
- `oldPrice` — displayed list price (e.g., `"$14.99"`), else null
- `priceTag` — displayed discount badge (e.g., `"SAVE 53%"`), else null
- `itc` — itemTrackingCode from the CTA (confirms the surface ITC, e.g., `"slp_wordpress"`)
- `destination` — cart destination from the CTA (`"precheck"` or `"cart"`)

**For `productPackage` pattern** (email/WAM pages — JSON embedded in page source):
```bash
node scrapers/debug_email.js {URL} 2>/dev/null
```
Parse the JSON returned. Each item in `productPackages` is an object with the same fields as above (`productPackage`, `planType`, `recommended`, `recommendedLabel`, `termLengthMonths`, `salePrice`, `oldPrice`, `priceTag`, `itc`, `destination`). Extract `productPackage` as the raw value. If it starts with `nes-`, strip that prefix. The result is the curated offer ID. Fields are null when the Sitecore component for that surface doesn't embed them (e.g., `slp_hosting_4gh` does not include pricing or term metadata).

If the result is empty (empty array or `productPackages: []`), output:
```
No NES curated offers found on {URL}.
Possible reasons: page is CES-only or URL has changed.
```
Do not proceed further.

**ITC mismatch check:** After parsing the scraper output, collect the distinct `itc` values returned. Compare against the expected ITC from the mapping table (case-insensitive). If they differ, flag it before proceeding:
```
⚠️ ITC mismatch: expected {table_itc}, page returned {scraped_itc}.
The mapping table may be stale. Proceeding with scraped data — update SKILL.md if confirmed.
```
If the scraped `itc` is null for all offers (field not present in the page JSON), skip this check silently.

---

## Step 2 — Catalog MCP Lookup

For each `curatedOfferId` returned by the scraper, call:

```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId="{id}")
```

Run all calls in parallel.

If a call returns `NOT_FOUND`:
1. Check whether the ID being looked up still contains a `nes-` prefix (this can happen if the parsing step above missed a value). If so, strip the prefix and retry `get_curated_offer` with the clean slug before classifying as not found.
2. If the clean-slug retry also returns `NOT_FOUND` (or no prefix was present), include the offer in the output with:
```
Plan             : —
Base Offer ID    : —
Active           : Not in catalog (verify in prod catalog API before cloning)
Revision         : —
```

Extract these fields from each successful response:
- `curatedOfferId` — the ID to clone (carry forward all scraper fields: `planType`, `recommended`, `recommendedLabel`, `termLengthMonths`, `salePrice`, `oldPrice`, `priceTag`)
- `plan` — full plan name slug
- `offerId` — base offer ID
- `active` — true/false
- `revisionNumber`
- Free trial: present if `configKeyValues.offers[].configKeyValuesData.billingPolicyOverride.planType == "FREE_TRIAL"`. Extract `trialInfo.term` (e.g. 1 MONTH) and `freeTrialOutcome` (e.g. BILL).

---

## Step 3 — Extract Tier Label

From the `plan` field, extract the tier label for display:
- If plan contains "basic" → **Basic**
- If plan contains "deluxe" → **Deluxe**
- If plan contains "ultimate" → **Ultimate**
- If plan contains "economy" → **Economy**
- If plan contains "premier" or "pro" → **Pro**
- Otherwise → use the full plan slug

---

## Step 4 — Apply Tier Filter (if provided)

If a tier argument was passed, return only the offer(s) whose tier label matches (case-insensitive). If no match, list the available tiers and ask the analyst to confirm.

---

## Step 5 — Render Output

```
=== Live Surface: {ITC} ===
Source    : {prod URL}
Scraped   : {today's date}
Offers    : {N} found
Hub       : {only if ITC is slp_365_email or slp_365 → "https://www.godaddy.com/email (slp_365_category) — offers here may also appear on the hub with different embedded ITCs"; otherwise omit this line entirely}

--- {Tier Label} ---
Product Name     : {planType, or — if null}
Recommended      : {Yes — {recommendedLabel} | No}
Curated Offer ID : {curatedOfferId}
ITC              : {itc, or — if null}
Destination      : {destination, or — if null}
Plan             : {plan}
Base Offer ID    : {offerId}
Active           : {Yes | No}
Revision         : {revisionNumber}
Free Trial       : {Yes — {N} {MONTH|YEAR} → {outcome} | No}
Default Term     : {termLengthMonths} months (or — if null)
Displayed Price  : {salePrice} (was {oldPrice}, {priceTag}) — or — if null

--- {Tier Label} ---
...
```

If only one offer was found, omit the tier header separator and render a single block.

---

## Output Constraints

- Do not show raw JSON from the scraper or MCP responses.
- Do not show offer keys, product IDs, or `quantityByOfferKey` — these are internal catalog details not needed for clone targeting.
- If `active: false` on any offer, flag it clearly: `Active : No ⚠️ — confirm before cloning`.
- Do not write any files.
- Do not auto-log this run.
