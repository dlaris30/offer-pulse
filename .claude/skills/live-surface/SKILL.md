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
/live-surface <surface> [market]                        ← market token, country code, or country name
/live-surface <surface> <tier>                          ← optional tier filter (basic, deluxe, ultimate, etc.)
/live-surface <surface> [market] <tier>
/live-surface <surface> scrape-only                     ← scrape + tier-filter only; no catalog MCP calls
/live-surface <surface> [market] scrape-only
/live-surface <surface> [market] <tier> scrape-only
```

`<surface>` can be an ITC, a human surface alias (see table below), or a full prod URL.

`[market]` is optional. Accepts a market token (e.g., `en-in`), a country code (e.g., `IN`), a country name (e.g., `India`), or a market group shorthand (e.g., `DEM`). See the Market Resolution section below. When omitted, defaults to US (existing behavior).

Examples:
- `/live-surface slp_wordpress`
- `/live-surface slp_hosting_4GH en-in`
- `/live-surface "FOS web hosting" IN`
- `/live-surface slp_wordpress en-au basic`
- `/live-surface slp_hosting_4GH DEM`
- `/live-surface slp_wordpress deluxe`
- `/live-surface slp_wordpress basic scrape-only`
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

## Market Resolution

When a `[market]` argument is provided, resolve it to a market token and construct the final URL before scraping. When omitted, use the US default (no prefix).

### Step M1 — Resolve Market Token

Match the input against this lookup (case-insensitive):

**Country name / code aliases:**

| Analyst says | Resolves to |
|---|---|
| US, United States, en-US, (none) | *(US default — no prefix)* |
| AU, Australia | `en-au` |
| CA, Canada | `en-ca` (English primary; use `fr-ca` for French) |
| CA-FR, Canada French | `fr-ca` |
| UK, GB, United Kingdom | `en-uk` |
| IN, India, India English | `en-in` |
| IN-HI, India Hindi, hi-IN | `hi-in` |
| JP, Japan | `ja-JP` |
| KR, Korea, South Korea | `ko-KR` |
| DE, Germany | `de` |
| FR, France | `fr` |
| ES, Spain | `es-es` |
| MX, Mexico | `es` |
| BR, Brazil | `pt-br` |
| PT, Portugal | `pt-pt` |
| IT, Italy | `it` |
| NL, Netherlands | `nl` |
| NO, Norway | `nb-NO` |
| SE, Sweden | `sv-SE` |
| DK, Denmark | `da-DK` |
| PH, Philippines | `en-ph` |
| SG, Singapore | `en` |
| AE, UAE | `en` |
| IR, Ireland | `en` |
| NZ, New Zealand | `en` |

If the input already matches a token in the lookup table below (e.g., `en-in`, `fr`, `ko-KR`), use it directly.

If the input does not match any alias or token, output:
```
Market "{input}" not recognised. Valid tokens: en-au, en-ca, fr-ca, en-uk, en-in, hi-in, en, en-ph, zh-sg, zh, id-id, th-th, vi-vn, es-es, es, pt-br, pt-pt, fr, de, it, nl, pl-pl, tr-tr, uk-ua, ko-KR, ja-JP, nb-NO, sv-SE, da-DK.
```

**Multi-locale countries:** India and Canada have two locales each. The alias table maps to the primary (English) locale by default. Announce the resolution: `Market: IN → en-in (India English; specify hi-in for Hindi locale)`.

**Market group shorthands** (fires parallel scraper calls for each token):

| Group | Tokens scraped | Coverage |
|---|---|---|
| `DEM` | `en-au`, `en-ca`, `en-uk` | Exhaustive — all 3 DEM markets |
| `ROW` | `en-in`, `en-ph`, `es`, `fr`, `de`, `en` | Representative sample (~6 of ~22 ROW bases) |
| `LATAM` | `es`, `pt-br` | Latin America |
| `EU` | `en`, `fr`, `de`, `it`, `es-es` | European Union representative |
| `EM-EN` | `en-in`, `en-ph` | Emerging markets English |

ROW is a representative sample covering the major known offer-family archetypes. It does not enumerate all ~22 non-US/non-DEM URL bases. The 6 tokens were chosen to detect the M365 vs Titan Email / -ox family split. Additional markets can be added per-run on request.

### Step M2 — Construct the Final URL

Look up the token in this table to determine URL type and base path derivation:

| Token | URL type | URL base |
|---|---|---|
| *(none / us / default)* | path | `www.godaddy.com` |
| `en-au` | path | `www.godaddy.com/en-au` |
| `en-ca` | path | `www.godaddy.com/en-ca` |
| `fr-ca` | path | `www.godaddy.com/fr-ca` |
| `en-uk` | path | `www.godaddy.com/en-uk` |
| `en-in` | path | `www.godaddy.com/en-in` |
| `hi-in` | path | `www.godaddy.com/hi-in` |
| `en` | path | `www.godaddy.com/en` |
| `en-ph` | path | `www.godaddy.com/en-ph` |
| `zh-sg` | path | `www.godaddy.com/zh-sg` |
| `zh` | path | `www.godaddy.com/zh` |
| `id-id` | path | `www.godaddy.com/id-id` |
| `th-th` | path | `www.godaddy.com/th-th` |
| `vi-vn` | path | `www.godaddy.com/vi-vn` |
| `es-es` | path | `www.godaddy.com/es-es` |
| `es` | path | `www.godaddy.com/es` |
| `pt-br` | path | `www.godaddy.com/pt-br` |
| `pt-pt` | path | `www.godaddy.com/pt-pt` |
| `fr` | path | `www.godaddy.com/fr` |
| `de` | path | `www.godaddy.com/de` |
| `it` | path | `www.godaddy.com/it` |
| `nl` | path | `www.godaddy.com/nl` |
| `pl-pl` | path | `www.godaddy.com/pl-pl` |
| `tr-tr` | path | `www.godaddy.com/tr-tr` |
| `uk-ua` | path | `www.godaddy.com/uk-ua` |
| `ko-KR` | subdomain | `kr.godaddy.com` |
| `ja-JP` | subdomain | `jp.godaddy.com` |
| `nb-NO` | subdomain | `no.godaddy.com` |
| `sv-SE` | subdomain | `se.godaddy.com` |
| `da-DK` | subdomain | `dk.godaddy.com` |

**URL construction rules:**

Derive `base_path` by stripping `https://www.godaddy.com` from the ITC → Prod URL mapping table entry (e.g., `https://www.godaddy.com/hosting/web-hosting` → `/hosting/web-hosting`).

```
US default (no market):
  final_url = https://www.godaddy.com{base_path}

Path-prefix market:
  final_url = https://www.godaddy.com/{market-token}{base_path}
  e.g., en-in + /hosting/web-hosting → https://www.godaddy.com/en-in/hosting/web-hosting

Subdomain market (ko-KR, ja-JP, nb-NO, sv-SE, da-DK):
  final_url = https://{subdomain}.godaddy.com{base_path}
  e.g., ko-KR (subdomain: kr) + /hosting/web-hosting → https://kr.godaddy.com/hosting/web-hosting
```

For group scrapes, construct one URL per token and fire all scraper calls in parallel. Announce all URLs before scraping.

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
- **Geo:** Expect different curated offer IDs per market — do not assume global uniformity. Probe results (2026-06) confirmed `slp_hosting_4GH` returns a distinct `-ox`/Titan Email offer family for `en-in` (India) vs the `-365-`/M365 family served to US/UK/ES. UK and ES matched the US set in that test but this is surface-specific and not guaranteed to be stable across surfaces or time. Always scrape the target market explicitly when the ticket has a geo scope — use `/live-surface <surface> [market]` with the appropriate token.
- **Pages confirmed NES-free from the 27-URL audit** (probe checked `productPackage` regex + hidden inputs, 5s render wait): `/domains`, `/domains/domain-name-generator`, `/domains/domain-broker`, `/domains/domain-protection`, `/domains/domain-investing`, `/domains/bulk-domain-search`, `/websites/online-store`, `/websites/best-ecommerce-website-builder`, `/websites/best-website-builder`, `/online-marketing/digital-marketing-services`, `/payments`, `/airo`, `/airo/airoallaccess`. These are informational/tool/lead-gen pages with no purchasable plan box.

If the ITC is not in this table, output:
```
No URL mapped for ITC "{ITC}".
Add the URL to the mapping table in .claude/skills/live-surface/SKILL.md to enable scraping.
```
Do not proceed further.

---

## Step 0 — Resolve Input and Announce

Before scraping, resolve the analyst's input to a canonical ITC + market token + final URL using the alias table, Market Resolution section, and ITC mapping table above.

**Resolution order:**
1. Resolve `<surface>` → ITC (alias table or exact/URL match)
2. Resolve `[market]` → market token (alias table or direct token; default to US if absent)
3. Derive `base_path` from the ITC → Prod URL table (strip `https://www.godaddy.com`)
4. Construct `final_url` per the URL construction rules in Market Resolution

Then output a one-line confirmation so the analyst can catch misrouting early:

```
Resolving: "{analyst input}" → ITC: {itc} | Market: {token} ({description}) | URL: {final_url}
```

If no market was specified, write `Market: US (default)`. If the surface input was an exact ITC, write `(exact match)`. If it was a URL, write `(URL match)`.

Example outputs:
```
Resolving: "FOS wordpress" → ITC: slp_wordpress | Market: US (default) | URL: https://www.godaddy.com/hosting/wordpress-hosting (alias match)
Resolving: "FOS web hosting" / India → ITC: slp_hosting_4GH | Market: en-in (India English) | URL: https://www.godaddy.com/en-in/hosting/web-hosting
Resolving: "slp_ssl" → ITC: slp_ssl | Market: US (default) | URL: https://www.godaddy.com/web-security/ssl-certificate (exact match)
Resolving: "FOS web hosting" / ko-KR → ITC: slp_hosting_4GH | Market: ko-KR (South Korea) | URL: https://kr.godaddy.com/hosting/web-hosting
```

For group scrapes (DEM, ROW, LATAM, EU, EM-EN), announce all tokens and URLs before firing any scraper call.

For exhaustive groups (DEM):
```
Resolving: "FOS web hosting" / DEM → ITC: slp_hosting_4GH | Markets: en-au, en-ca, en-uk (all 3 DEM markets)
  en-au → https://www.godaddy.com/en-au/hosting/web-hosting
  en-ca → https://www.godaddy.com/en-ca/hosting/web-hosting
  en-uk → https://www.godaddy.com/en-uk/hosting/web-hosting
Scraping 3 markets in parallel.
```

For representative groups (ROW):
```
Resolving: "FOS web hosting" / ROW → ITC: slp_hosting_4GH | Markets: en-in, en-ph, es, fr, de, en (ROW representative: 6 of ~22)
  en-in → https://www.godaddy.com/en-in/hosting/web-hosting
  en-ph → https://www.godaddy.com/en-ph/hosting/web-hosting
  es → https://www.godaddy.com/es/hosting/web-hosting
  fr → https://www.godaddy.com/fr/hosting/web-hosting
  de → https://www.godaddy.com/de/hosting/web-hosting
  en → https://www.godaddy.com/en/hosting/web-hosting
Scraping 6 markets in parallel.
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
This market may be CES-only for this surface. To confirm, run in Helix:
  SELECT package_id, COUNT(*) AS events
  FROM signals_platform_clickstream_cln.add_to_cart_package_event_cln
  WHERE product_item_tracking_code = '{ITC}'
    AND event_date >= CURRENT_DATE - 30
  GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
A NULL-only package_id result confirms CES. Non-null values confirm NES is active.
```
Do not proceed further.

**ITC mismatch check:** After parsing the scraper output, collect the distinct `itc` values returned. Compare against the expected ITC from the mapping table (case-insensitive). If they differ, flag it before proceeding:
```
⚠️ ITC mismatch: expected {table_itc}, page returned {scraped_itc}.
The mapping table may be stale. Proceeding with scraped data — update SKILL.md if confirmed.
```
If the scraped `itc` is null for all offers (field not present in the page JSON), skip this check silently.

---

## Step 1B — Group Synthesis (group scrapes only)

This step fires only when 2 or more markets were scraped (any group shorthand: DEM, ROW, LATAM, EU, EM-EN, or a manually-specified list of tokens). Skip for single-market scrapes.

After all market scrapes complete, synthesize results into offer families:

**1. Fingerprint each market**
- Take the set of curatedOfferIds returned for that market
- Sort alphabetically
- Join with `|` to form a fingerprint string

**2. Group by fingerprint**
- Markets with identical fingerprint strings share the same offer family
- Markets with no results (empty scrape) → bucket: `empty_markets` — "No NES offers detected (likely CES surface)"
- Markets where the scrape failed (timeout / connection error) → bucket: `failed_markets` — "Scrape failed — excluded from synthesis"

**3. Name each family**
Apply in order — first match wins:
- Any curatedOfferId in the set contains `-365-`, `-o365-`, or `m365` → name: "M365 series"
- Any curatedOfferId in the set contains `-ox-`, `-openexchange-`, or `titan` → name: "Titan Email / -ox series"
- Multiple families each matching different rules above → name: "Mixed series"
- No pattern match → name: "Family A", "Family B", ... (sequential letters, one per unique fingerprint)

**4. Record synthesis result**
Carry forward into Step 5:
- `families` — array of `{ name, markets: [...tokens], offers: [...curatedOfferIds] }`
- `empty_markets` — tokens with empty scrape result
- `failed_markets` — tokens where scraper returned an error

After Step 1B completes, skip Steps 2, 3, and 4. Proceed directly to Step 5 using the group rendering path.

---

## Step 1b — Pre-filter by Tier (runs only when a tier argument was supplied)

If a tier argument was passed, apply the tier filter NOW — before any catalog MCP calls.

Using the `planType` field from each scraped item, keep only items whose `planType` contains the supplied tier string (case-insensitive, substring match):
- "basic"    → keep items where planType contains "basic"
- "deluxe"   → keep items where planType contains "deluxe"
- "ultimate" → keep items where planType contains "ultimate"
- "economy"  → keep items where planType contains "economy"

If exactly one item survives: proceed with that item only. Step 2 fires one catalog call.
If zero items survive: list the `planType` values that were present and ask the analyst to confirm the tier name before proceeding. Do not call Step 2.
If `planType` is null for all scraped items: skip Step 1b entirely; all items proceed to Step 2 (fallback to Step 4 filter as normal).
If no tier argument was supplied: skip Step 1b entirely.

---

## Scrape-only Mode

When `scrape-only` is in the invocation arguments, stop after Step 1b. Do not run Steps 2, 3, 4, or 5.

Return the filtered scraper array as the raw result — one JSON object per item, with all fields collected in Step 1: `curatedOfferId`, `planType`, `recommended`, `recommendedLabel`, `termLengthMonths`, `salePrice`, `oldPrice`, `priceTag`, `itc`, `destination`. Do not render any formatted output block. Do not call any catalog MCP tools.

This mode is used by `/offer-pulse` on the FOS NES fast path, where catalog resolution is handled downstream by `catalog_chain.py`. The caller owns all catalog work.

Scrape-only takes precedence over all other output formatting rules in this skill.

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

If Step 1b already fired (tier argument was passed AND `planType` was non-null for at least one scraped item), Step 4 is a no-op — filtering was already applied pre-catalog.

If Step 1b did not fire (no tier argument, or all `planType` values were null), apply the tier filter now: return only the offer(s) whose tier label matches (case-insensitive). If no match, list the available tiers and ask the analyst to confirm.

---

## Step 5 — Render Output

```
=== Live Surface: {ITC} ===
Source    : {final URL}
Market    : {token} ({country/description}) — or "US (default)"
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

**Group scrapes (Step 1B ran):** render one block per unique offer family — not one block per market. Use the synthesis result from Step 1B.

```
=== Live Surface: {ITC} | {group label} ===

{N} offer famil{y/ies} found.

Family: {family name}
Seen in : {comma-separated market tokens}
Offers  : {curatedOfferIds — one per line if more than 3}

[repeat for each family]

[if empty_markets non-empty:]
No NES offers : {tokens} — CES surface or no active packages

[if failed_markets non-empty:]
Scrape failed : {tokens} — excluded from synthesis
```

Group label in the header:
- DEM → "DEM (all 3 markets)"
- ROW → "ROW (representative: 6 markets)"
- Other groups → group shorthand only

For DEM where all 3 markets share one family, append below the family block: "Offer family is uniform across all 3 DEM markets."

For ROW, append a footer after the last family block:
```
---
ROW sample: en-in, en-ph, es, fr, de, en.
To extend: name additional markets (e.g. "add pt-br, tr-tr") or request full catalog chain for either family.
```

---

## Output Constraints

- Do not show raw JSON from the scraper or MCP responses.
- Do not show offer keys, product IDs, or `quantityByOfferKey` — these are internal catalog details not needed for clone targeting.
- If `active: false` on any offer, flag it clearly: `Active : No ⚠️ — confirm before cloning`.
- Do not write any files.
- Do not auto-log this run.
- Group scrapes render one block per unique offer family, not one block per market. Synthesis is by curatedOfferId fingerprint (Step 1B).
- ROW renders a "To extend" footer. DEM does not (it is exhaustive).
- Empty scrape (no NES offers) and scrape failures are surfaced separately in group output — never silently dropped.
