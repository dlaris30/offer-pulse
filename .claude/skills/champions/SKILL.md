---
name: champions
description: Given a surface (ITC prefix or specific ITC) and a product name or category, identifies the current champion curated offer on that surface+product combination, resolves it via the catalog MCP, and outputs a complete champion record with pricing.
---

# /champions — Surface Champion Identifier

**What this skill does:** Resolves the single dominant curated offer for a given surface + product combination. Produces a complete champion record — slug, geometry, component UUIDs, plan, term, intro/renewal pricing, free components, and discount codes.

**What this skill does NOT do:** Run any writes. Fetch Jira tickets. Produce ecomm engineering payloads or pricing ticket PFID lists. Those belong to `/offer-pulse`.

Arguments: $ARGUMENTS

---

## Input Requirements

Both arguments are required. Refuse to run if either is missing.

| Argument | Description | Examples |
|---|---|---|
| Surface | ITC prefix or specific ITC code | `slp_hosting_4gh`, `slp_wordpress`, `dpp_precheck` |
| Product | Product name or category in plain language | `cPanel Economy`, `MWP Deluxe`, `M365 Email Essentials`, `cPanel Economy with M365` |

**If either argument is missing:** do not proceed. Output exactly:

```
/champions requires two arguments:
  1. Surface — an ITC prefix or specific ITC (e.g. slp_hosting_4gh, slp_wordpress)
  2. Product — a product name or category (e.g. "cPanel Economy", "MWP Deluxe")

Example: /champions slp_hosting_4gh "cPanel Economy"
```

Stop. Do not run any queries or catalog calls.

---

## Execution Flow

Run silently from start to finish. Do not narrate steps, emit partial output, or surface intermediate query results. The analyst sees only the final champion record.

### Step 1 — CES Surface Pre-Check

Before any catalog calls, determine whether the target surface is a known CES-only surface.

Known CES-only signals:
- `dpp_precheck`, `dpp_config1` — 97–100% CES as of 2026-05-11
- `upp_*` prefixes (all 97 surfaces) — 100% CES, not on migration roadmap
- Any surface where a quick `package_id` null-rate check returns > 95% null

**If the surface is known-CES or confirms as CES via null-rate check:** skip all catalog calls and render the CES Surface block described in the "CES Surface Output" section below. Do not attempt `get_curated_offer`.

For surfaces that are mixed or unknown: proceed to Step 2.

---

### Step 2 — Identify the Champion Slug

Two paths. Take the higher-confidence path available.

#### Path S (Slug provided — highest confidence)

If the analyst provides a known `package_id` slug directly (e.g. `cpanel-o365-tier1`), use it as the champion slug. Set confidence basis to `Analyst-provided slug`.

Skip the behavioral query entirely.

#### Path B (Behavioral — surface + product category only)

Query `add_to_cart_package_event_cln` joined to `add_to_cart_product_event_cln` over the last 7 days. Use `connection='bi'`.

```sql
SELECT
    pkg.package_id,
    prod.product_id,
    prod.product_name,
    SUM(1) AS event_count
FROM signals_platform_clickstream_cln.add_to_cart_package_event_cln pkg
JOIN signals_platform_clickstream_cln.add_to_cart_product_event_cln prod
    ON pkg.add_to_cart_event_id = prod.add_to_cart_event_id
WHERE pkg.src_receive_utc_year_num  = EXTRACT(YEAR  FROM SYSDATE)
  AND pkg.src_receive_utc_month_num BETWEEN EXTRACT(MONTH FROM SYSDATE) - 1 AND EXTRACT(MONTH FROM SYSDATE)
  AND prod.src_receive_utc_year_num  = EXTRACT(YEAR  FROM SYSDATE)
  AND prod.src_receive_utc_month_num BETWEEN EXTRACT(MONTH FROM SYSDATE) - 1 AND EXTRACT(MONTH FROM SYSDATE)
  AND prod.product_item_tracking_code LIKE '<itc_pattern>%'
  AND pkg.package_id IS NOT NULL
  AND LOWER(prod.product_name) LIKE '%<product_keyword>%'
GROUP BY pkg.package_id, prod.product_id, prod.product_name
ORDER BY pkg.package_id, event_count DESC
```

After this query returns, group rows by `package_id` to identify the champion slug (highest total event_count per package_id), then collect all distinct `product_id` + `product_name` pairs associated with that slug. These are the PFIDs for the champion record. Multiple PFIDs per champion are expected and correct — one per component product in the bundle. Store them as `{champion_pfids}` for output rendering. Remove the LIMIT 10 — it can truncate component PFIDs for high-component bundles. Use `ORDER BY pkg.package_id, event_count DESC` and group in-memory instead.

**Partition rule:** Always filter `add_to_cart_package_event_cln` and `add_to_cart_product_event_cln` on `src_receive_utc_year_num` and `src_receive_utc_month_num`. Never use a date column. Extend the month window back by 1 to capture 7-day windows that straddle a month boundary.

**ITC pattern construction:** If the analyst provided an exact ITC (e.g. `slp_hosting_4gh`), filter on exact match (`product_item_tracking_code = 'slp_hosting_4gh'`). If a prefix was provided (e.g. `slp_wordpress`), use `LIKE 'slp_wordpress%'`.

**Product keyword construction:** Normalize the product name to one or two lowercase keywords. Examples: `cPanel Economy` → `economy`; `MWP Deluxe` → `deluxe`; `M365 Email Essentials` → `email essentials`. Do not filter on brand names (cPanel, MWP) — they rarely appear verbatim in `product_name` strings in CLN data. Use tier/descriptor words instead.

**Zero rows:** If the query returns zero rows with `package_id IS NOT NULL`, the surface is CES for this product. Render the CES Surface Output block.

**Champion selection — A/B experiment handling:**

- If the top result has > 20× the volume of the second result: single clear champion. Use the top slug.
- If 2–3 candidates are within 20% of each other by volume: A/B experiment likely in flight. Show **top 3 candidates** ranked by volume. Do not pick one — present all three and note the A/B flag. Proceed to catalog resolution for all three candidates.
- If only 1 non-null slug exists: use it.

Set confidence basis to `Behavioral proxy — 7-day add-to-cart volume on [ITC(s)]`. This is a behavioral signal, not a config fact. Note this explicitly in the output.

---

### Step 3 — Catalog Resolution

For each champion slug (1 slug on single champion, up to 3 on A/B flag):

#### 3a — Curated Offer Lookup

```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<slug>)
```

**NOT FOUND:** If the slug returns NOT FOUND, check ghost-ID patterns:
- `nes-` prefix → ghost, no catalog backing
- `offer-` prefix → ghost or retired
- `_NNNmo` suffix → CES merch-packages term alias, not NES

Record the ghost classification. Do not attempt further catalog calls for that slug. Note in the champion record.

**Active = false:** Note the offer is inactive. Proceed with resolution but flag it in the record.

Extract from the response:
- `offerId` — UUID pointing to the base offer or offer collection
- `plan` — the pinned plan name
- `active`
- `discountCodes[]` — if present
- `prePurchaseKeyMap` — presence/absence determines geometry
- `configKeyValues` — check for `billingPolicyOverride` (free trial, ATMP)
- `apiVersion` — if 3, component `offerIds[]` UUIDs are not publicly resolvable; note this

#### 3b — Geometry Classification

Evaluate `prePurchaseKeyMap` from the curated offer response:

- Absent or empty → **Standalone Offer**. `offerId` is the Offer ID. Call `get_offer_collection_definition(datasource="catalog-offers", offerCollectionId=<offerId>)` for plan schema. The `plan` from the curated offer is the selected plan. Output label for this UUID: `Offer ID`. Always emit `Offer Collection ID : Not available` on the next line — the field must appear in every champion record so the analyst can confirm it was looked for.
- Has one or more entries in `prePurchaseKeyMap.offers[]` → **Offer Collection**. `offerId` is the Offer Collection ID. Output label for this UUID: `Offer Collection ID`. This UUID must appear in the champion record. Do not omit it. Do not label it `Offer ID`. Proceed to 3c.
- `offersGrouping` present without `prePurchaseKeyMap` → **Offer Collection** (no provisioning overrides). `offerId` is the Offer Collection ID. Same label rule as above. Use `get_offer_collection_definition` `offers[]` array to resolve components.

Do not assume geometry. Always derive it from the response. The `offerId` UUID is the same value in all cases — only the label changes based on geometry. Mislabeling this field causes engineering to file tickets against the wrong ID.

#### 3c — Component Resolution (Offer Collections only)

For each entry in `prePurchaseKeyMap.offers[]`, call in parallel:
```
get_offer_definition_by_id(datasource="catalog-offers", offerId=<componentOfferId>)
```

From each component response, extract:
- Component name (from `name` field or tags)
- `offerId` UUID
- Whether it has `PRICE_OVERRIDE=0` or `FREEACCOUNT: "true"` baked in via `customData` → marks it as a free component

Known component UUIDs (use as fast-path labels — still call to confirm):

| UUID | Component |
|---|---|
| `575a7d2a-d1ef-40f2-a7e5-dbcc09c20391` | M365 / Office 365 |
| `927a9d45-7c5b-4652-ad68-d5cd9be75028` | Titan Email |
| `28e5b730-4e70-46b0-8672-6e18a17f81a1` | SSL Certificate |
| `d9e7bde4-7b28-49b3-b2fd-5dc528ab8062` | WAM / Websites and Marketing |
| `05730877-89bd-49c0-8fff-c9880b743bf0` | cPanel Business Hosting |
| `d29f7b62-9766-43bc-b230-353579eaad9c` | VPS4 Hosting |

#### 3d — Pricing Lookup

Call with `rateForDisplay=true`:
```
catalog_query_get_offers(
    datasource="catalog-query",
    currency="USD",
    marketId="en-US",
    curatedOfferId=<slug>,
    rateForDisplay=True
)
```

**Price extraction:** All price values are in micro-units. Divide by 1,000,000 for USD.

Fields to extract from the pricing response:
- `discountPrice` → intro price (USD)
- `renewalDiscountPrice` → renewal price (USD). If absent, note "renewal price not available."
- `term` object → `termType` (YEAR/MONTH) and `numberOfTerms`

**NOT FOUND on pricing call:** Some offers fail this call (e.g. `cpanel-set-1-economy-ssl-365-xtra` in test env). Handle gracefully:
- Do not error or block
- Report the plan name and term from the curated offer response
- Set `Intro price : Not available (pricing API returned NOT_FOUND)` and `Renewal price : Not available`
- Continue to render all other fields

---

## Output Format

### Single Champion Output

Render as labeled record blocks. Use `===` slug delimiter. No tables for the champion record itself. No padding. No step narration.

If a single clear champion was found:

```
=== champion: <slug> ===
Surface          : <ITC or ITC prefix>
Product          : <product description from analyst input>
Curated Offer    : <slug>
Geometry         : <Standalone Offer | Offer Collection>
Offer Collection ID : <UUID, or Not available if Standalone>
Plan             : <plan name from curated offer>
Term             : <termType> / <numberOfTerms> (e.g. YEAR / 1, MONTH / 1)
Intro price      : $<X.XX>/mo  (or $<X.XX>/yr — match the term)
Renewal price    : $<X.XX>/mo  (or Not available)
PFIDs            : <pfid1> (<product_name>), <pfid2> (<product_name>), ... — all distinct product_id values from behavioral query for this slug. Never omit a PFID row. If Path S was used (analyst-provided slug), write "Not available — behavioral query not run (analyst-provided slug)".
Free components  : <component name (UUID)> — FREEACCOUNT | <none>
Discount codes   : <code(s), or none>
Active           : <Yes | No — INACTIVE>
Confidence basis : <Analyst-provided slug | Behavioral proxy — 7-day add-to-cart volume on [ITC]>
```

**PFIDs field rules:**
- Source: `product_id` + `product_name` from `add_to_cart_product_event_cln`, collected from the same behavioral query run in Step 2 Path B.
- Multiple PFIDs per champion are expected and correct — one per component product in the bundle. A bundle with 3 components produces 3 PFID entries on this line.
- Format: `{pfid} ({product_name})` pairs, comma-separated on one line. If the line is long, wrap with each PFID on its own indented line.
- Never truncate. A missing PFID means pricing or engineering will build an incomplete ticket from this champion record.
- For Path S (analyst-provided slug): the behavioral query was not run, so PFIDs are not available from behavioral data. Write exactly: `Not available — behavioral query not run (analyst-provided slug)`. Do not attempt to guess or infer PFIDs.
- For A/B scenarios where multiple champions are shown: each champion record gets its own PFID list sourced from events associated with that specific slug.

**Component lines (Offer Collections only):** After the record block, add a component table:

```
Components
| Component | UUID | Free |
|---|---|---|
| M365 / Office 365 | 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391 | Yes — FREEACCOUNT |
| SSL Certificate   | 28e5b730-4e70-46b0-8672-6e18a17f81a1 | Yes — PRICE_OVERRIDE |
| cPanel Business Hosting | 05730877-89bd-49c0-8fff-c9880b743bf0 | No |
```

Never omit a component row. If a component UUID was NOT FOUND on lookup, include it as a row with `Name : NOT FOUND` and the UUID.

**"Free" column values:** `Yes — FREEACCOUNT` | `Yes — PRICE_OVERRIDE` | `No` | `Unknown (V3 offer — component not resolvable)`

---

### A/B Experiment Output

If 2–3 candidates are within 20% of each other by volume:

```
A/B Flag — multiple champions detected on <surface> for <product>

Top 3 candidates by 7-day add-to-cart volume:

| Rank | Slug | Event count | Share |
|------|------|-------------|-------|
| 1 | <slug-a> | N | X% |
| 2 | <slug-b> | N | Y% |
| 3 | <slug-c> | N | Z% |

Candidates are within 20% of each other — an A/B experiment is likely in flight.
Resolving all three via catalog. Champion records follow.
```

Then render a full `=== champion: <slug> ===` record block for each candidate, in rank order.

---

### CES Surface Output

When the surface is CES-only or the behavioral query returns zero non-null package_ids:

```
CES Surface — No Curated Offer Champion Available

Surface    : <ITC>
Product    : <product description from analyst input>
Path       : CES (Classic eCommerce)
Signal     : package_id is null for this surface+product combination

What this means: CES surfaces do not have named curated offers. There is no
package_id in billing or CLN data for this surface, so no catalog champion
can be resolved.

Next steps:
- To audit available CES packages for this product, use /offer-pulse (Path A, CES chain)
- To check if a NES migration is planned, consult the migration roadmap or ask /ces-nes
- To see all PFIDs active on this surface with pricing, use /offer-pulse (Path B)
```

Do not show a partial record with blank fields. The CES output block replaces the champion record entirely.

---

### Ghost Slug Output

When a slug from behavioral data returns NOT FOUND across all catalog systems:

```
=== champion: <slug> — UNRESOLVABLE ===
Surface          : <ITC>
Curated Offer    : <slug>
Catalog status   : NOT FOUND in catalog-curated-offers, catalog-offers, merch-packages
Ghost pattern    : <nes- prefix — likely deprecated mid-migration | offer- prefix — likely retired | _NNNmo suffix — CES term alias | Unknown>
PFIDs            : <pfid1> (<product_name>), <pfid2> (<product_name>), ... from behavioral query — or "Not available" if behavioral query returned no product_id rows for this slug
Confidence basis : Behavioral proxy — 7-day add-to-cart volume on [ITC]

Note: This slug appeared in CLN add-to-cart data but has no catalog backing.
It cannot be resolved to a plan, term, or price. If this is the highest-volume
slug on this surface, the surface may be running a deprecated or ghost offer.
Use /offer-pulse for a full surface audit including ghost ID patterns.
```

---

## Known Limitations

State these limitations in output only when relevant — do not add boilerplate to every champion record.

| Limitation | When to surface it |
|---|---|
| Behavioral proxy is not a config fact | Always — include in Confidence basis line |
| CES surfaces cannot be resolved to a champion | When output is the CES Surface block |
| `rateForDisplay=true` may fail for some offers | When pricing API returns NOT_FOUND — state in Intro/Renewal price fields |
| A/B experiments may produce 2–3 near-equal candidates | When detected — show A/B Flag block |
| V3 offers (`apiVersion=3`) have non-resolvable `offerIds[]` component UUIDs | When V3 detected — note in component table cells |
| Some CES slugs have dual catalog registration — they appear in NES catalog but the surface may still be running CES | When `get_curated_offer` succeeds but behavioral data shows it was on a known-CES surface prefix |

---

## Live Validation Anchors

These three champion resolutions were confirmed end-to-end on 2026-05-14. Use as calibration cases.

| Surface | Product | Expected slug | Intro price | Renewal price | Free component |
|---|---|---|---|---|---|
| `slp_hosting_4gh` | cPanel Economy + M365 | `cpanel-o365-tier1` | $14.99/mo | varies | M365 free |
| `slp_wordpress` | MWP Deluxe + M365 | `wordpress-o365-forever-ssl-deluxe` | $26.99/mo | varies | M365 free |
| standalone email | M365 Email Essentials | `office365-tier0` | $1.99/mo | $8.99/mo | none |

Prices are from `rateForDisplay=true`, micro-units ÷ 1,000,000. If a test run of `/champions` produces different prices for these slugs, the discrepancy is likely market/currency context — not a skill defect.

---

## Tool Usage Rules

| Tool | Use | Never use |
|---|---|---|
| `mcp__catalog-mcp-dev__get_curated_offer` | Slug → curated offer lookup | — |
| `mcp__catalog-mcp-dev__get_offer_collection_definition` | offerId → geometry + component list | — |
| `mcp__catalog-mcp-dev__get_offer_definition_by_id` | component UUID → name + free-flag | — |
| `mcp__catalog-mcp-dev__catalog_query_get_offers` | Pricing with `rateForDisplay=true` | — |
| `mcp__distillery__execute_query` | Behavioral champion query (Path B only) | Date column filtering on CLN tables |
| Jira MCP tools | — | Never in this skill |
| `mcp__atlassian__*` | — | Never in this skill |

Run all catalog calls in parallel where possible. For an A/B scenario with 3 candidates, fire all 3 `get_curated_offer` calls simultaneously. For component resolution within a single offer, fire all `get_offer_definition_by_id` calls simultaneously.

---

## Scope Constraints

- Read-only. No writes of any kind.
- No Jira ticket creation, transition, or commenting.
- No Confluence page creation or editing.
- Does not produce ecomm engineering payloads — use `/offer-pulse` Path A for that.
- Does not produce PFID blast-radius tables — use `/offer-pulse` Path B for that.
- Does not determine whether an offer should be replaced or cloned — that is analyst judgment.
- Does not validate whether a champion is the correct offer for a pricing change — that is analyst judgment.
