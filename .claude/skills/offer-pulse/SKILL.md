---
name: offer-pulse
description: Given a Jira offer ticket (e.g. AGIGROWTH-161), a surface ITC, or a product name, audit all offers on that surface and produce the data needed for an ecomm engineering ticket (curated offer creation) or a pricing ticket (discount code application).
---

# /offer-pulse — Surface Offer Auditor

**Two paths. Pick one at the start:**

| Path | Use when | Output |
|------|----------|--------|
| **A — Curated Offer** | Ticket is about a new/variant offer or bundle configuration | Offer type (Standalone/Collection), Curated Offer ID, Base Offer ID, Plan (Standalone) or all Component Offer IDs + per-component plans (Collection) — ready for ecomm engineering ticket |
| **B — Pricing / Discount** | Ticket is about applying or changing a discount code or price point | Complete PFID list with current discount codes and pricing — ready for pricing ticket |

After the clarifying questions gate resolves, execute immediately and silently — run all queries, then all catalog/merchandising calls, collect every result, then render the complete output once at the end. Never emit partial output, intermediate tables, or step narration mid-execution. The analyst sees only the final assembled output.

**HARD CONSTRAINTS:**
- Read-only. Never create, update, transition, or comment on any Jira ticket without explicit analyst instruction.
- Never read linked ecomm tickets. The champion is determined from data and the catalog MCP only.
- Never show only the top result when multiple exist. A surface can have many PFIDs, many package IDs, and many discount codes simultaneously. Show all of them.
- Every response ends with an explicit reminder that no ticket action has been taken.
- Every markdown table must have one row per unique combination of values. Never compress multiple values into a single cell (e.g., if a PFID appears on 3 ITCs, that is 3 rows — not one row with "itc1, itc2, itc3" in the ITC cell).

---

## Domain Vocabulary

| Technical Term | Business Label | Definition |
|---|---|---|
| PFID | Product ID | The underlying product SKU (e.g. `1320706`) |
| ITC | Surface | The page/journey where the customer saw the offer (e.g. `slp_wordpress`) |
| Package ID | Curated Offer ID | Named offer slug from billing/CLN data (e.g. `wordpress-o365-forever-ssl-basic`). NES only — CES has no package ID. |
| NES | Curated Offer | New eCommerce — catalog-backed offers with named bundles. Identified by a non-null `package_id`. |
| CES | Legacy Offer | Classic eCommerce — no named bundle. `package_id` is null. |
| Standalone Offer | Single-product curated offer | Curated offer with no bundled add-ons. One Base Offer ID, one plan. |
| Offer Collection | Bundled curated offer | Curated offer with one or more add-ons wired via `prePurchaseKeyMap`. Base Offer ID + Component Offer IDs. |
| CES Package | Legacy named bundle | A named CES offer configuration in the merchandising API (e.g. `wordpress-basic-1yr`). Not present in billing — used only for catalog resolution on fully-CES surfaces. |

---

## Catalog Concepts

These IDs appear in all Path A output. Use them consistently.

| Term | What it is | Where it comes from |
|------|-----------|---------------------|
| **Package ID = Curated Offer ID** | Same value, two names. The human-readable slug. | Billing data / Catalog MCP |
| **Base Offer ID** | UUID in the `offerId` field of `get_curated_offer`. Points to an Offer Collection definition (the primary product). | `get_curated_offer` response |
| **Offer Collection** | Product definition with plans, terms, and pricing schema. Always the primary product. Retrieved via `get_offer_collection_definition`. | `catalog-offers` datasource |
| **Component Offer ID** | UUID from `prePurchaseKeyMap.offers[].offerId`. Each is a bundled add-on (e.g. M365, Titan Email). Retrieved via `get_offer_definition_by_id`. | `catalog-offers` datasource |
| **CES Package ID** | Slug from the GoDaddy merchandising API (e.g. `wordpress-basic-ssl-1yr`). Used only on the CES fallback path — never present in billing data. | `https://merchandising.api.godaddy.com/v1/packages` |

**Critical rule (from catalog team):** Do not assume a Curated Offer ID maps to a single product or plan. If `prePurchaseKeyMap` is present and non-empty, it is an Offer Collection — iterate all components and resolve each individually. Never use the top-level plan as authoritative for collections.

---

## Data Foundation

All queries use `connection='bi'`.

### `pricing_experiment_dev.offer_pulse_experiment`
Pre-joined billing + CLN table. Use for volume, pricing, and NES/CES breakdown.

Key columns: `pf_id`, `product_name`, `product_term_num`, `product_term_unit_desc`, `item_tracking_code` (ITC), `package_id`, `item_discount_code`, `purchase_path_name`, `bill_isc_source_code`, `bill_country_code`, `region_name`, `product_pnl_line_name`, `product_pnl_subline_name`, `trxn_currency_code`, `total_orders`, `new_customer_orders`, `existing_customer_orders`, `path_tracking_total_orders`, `pfid_pnl_total_orders`, `order_ratio_pct`, `total_revenue_usd`, `total_units_sold`, `receipt_price_usd_amt`, `receipt_regular_price_usd_amt`, `catalog_list_price_usd`, `catalog_sale_price_usd`, `bill_modified_mst_date`, `cln_create_utc_ts`, `cln_update_utc_ts`

### `pricing_experiment_dev.pf_id_package_details_v1`
Lean mapping table: `pf_id`, `item_tracking_code`, `package_id`, `cln_create_utc_ts`, `cln_update_utc_ts`. Use for a quick ITC → package_id lookup without volume data, or to check historical mappings via timestamps.

> **Aggregation note:** `total_orders` and related metrics are pre-aggregated at the grain of pf_id × ITC × package_id × discount_code × country × date. Always use `SUM(total_orders)` when aggregating across a date range.

---

## Catalog MCP Reference

These calls use the `catalog-mcp-dev` MCP server (`mcp__catalog-mcp-dev__*` tools), which provides access to the GoDaddy ecommerce catalog. The server must be configured before running Path A. If unavailable, note it in output and provide the raw `package_id` values only — do not block on catalog lookups.

| Action | Tool | Datasource |
|--------|------|------------|
| Look up a curated offer by package ID | `get_curated_offer(curatedOfferId=<package_id>)` | `catalog-curated-offers` |
| Look up a Base Offer (Offer Collection) | `get_offer_collection_definition(offerCollectionId=<offerId>)` | `catalog-offers` |
| Look up a Component Offer (add-on) | `get_offer_definition_by_id(offerId=<componentOfferId>)` | `catalog-offers` |
| List all active curated offer IDs | `get_curated_offers(active=true, limit=1200)` | `catalog-curated-offers` |
| Search available plans by product type (CES tag search) | `catalog_query_get_offers(datasource, currency, marketId, tags)` | `catalog-query` |
| Fetch all CES packages with PFID arrays | WebFetch `https://merchandising.api.godaddy.com/v1/packages` | External — public, no auth required |

Run all catalog lookups in parallel where possible. For N package IDs, fire all `get_curated_offer` calls at once. For M component offers within a package, fire all `get_offer_definition_by_id` calls at once.

---

## Clarifying Questions Gate

Run this check before any queries or catalog lookups. If the request already answers a dimension, skip that question. Present all needed questions as a single numbered list — do not ask sequentially. Maximum 3 questions. If more than 3 dimensions are unclear, ask about Path, segment, and markets; infer ITC specificity as "all surfaces matching the category" and state the assumption.

**Skip test — this exact request must produce zero questions:**
> "80% discount on Basic Managed WordPress Hosting for Rest of World and India on the Sales Landing Page, new and existing customers — give me the full curated offer creation payload for ecommerce engineering"

---

### Dimension 1 — Path (A vs B)

**Skip if:** the request contains any of: "curated offer", "clone", "new offer", "offer creation", "bundle", "ecomm ticket", "engineering ticket" → Path A. Or: "discount code", "promo code", "pricing change", "price point", "PFID list", "pricing ticket" → Path B. Note: the word "discount" as a percentage modifier (e.g. "80% discount") does not imply Path B — it describes the override price, not the ticket type.

**Ask if:** the request describes an offer or price change without making the goal explicit (e.g. "look at MWP Basic on SLP" with no stated purpose).

Question: "Are you building a **new curated offer** (Path A — ecomm engineering) or applying a **discount / price change** to an existing offer (Path B — pricing ticket)?"

---

### Dimension 2 — Customer Segment

**Skip if:** the request states "new customers", "existing customers", "renewals", "both", or "new and existing".

**Ask if:** segment is not mentioned. Exception: if the request is a pure surface audit with no pricing or offer scope, infer "both" and state the assumption rather than asking.

Question: "Should this cover **new customers**, **existing / renewal customers**, or **both**?"

---

### Dimension 3 — Target Markets / Geo Scope

**Skip if:** specific markets or regions are named (e.g. "ROW and India", "US only", "all markets", "globally").

**Ask if:** no market is mentioned.

Question: "Which markets should this cover? (e.g. US only, ROW, India, all markets, or a specific country list)"

---

### Dimension 4 — ITC Specificity

**Skip if:** an exact ITC string is given (e.g. `slp_wordpress`), or the entry is product-name-first or PFID-first with no surface reference.

**Ask if:** a surface category is named without an exact ITC (e.g. "the SLP", "DPP surfaces") AND the request has enough other specificity that narrowing would meaningfully reduce output. Do not ask if the analyst's stated purpose is a full surface audit.

Question: "The SLP maps to multiple ITCs (`slp_wordpress`, `slp_hosting_category`, etc.). Should I audit **all SLP surfaces** or a specific one? (Say 'all' to proceed with full coverage.)"

---

### Gate rendering rule

If one or more questions are needed, present them all in a single numbered list before running anything:

> "Before I run queries, a couple of quick questions:
> 1. [question]
> 2. [question]"

Wait for all answers before proceeding.

---

## Entry

### Entry Option 1 — Jira Ticket
1. Fetch with `getJiraIssue` (`cloudId: godaddy.atlassian.net`). This uses the Atlassian MCP tool (`mcp__atlassian__getJiraIssue`). If the Atlassian MCP is not available, ask the analyst to paste the relevant ticket fields (surface/ITC, product or PFID, and ticket type) directly.
2. Extract from the ticket body only (ignore linked tickets):
   - **Surface / ITC** — map surface names using the Surface Map below
   - **Product / PFID** — if explicitly called out
   - **Ticket type** — curated offer creation or pricing/discount change
3. Proceed to Path A or Path B below

### Entry Option 2 — Direct Input (ITC, Product Name, or PFID)

| Entry type | Example | Primary filter |
|---|---|---|
| ITC string | `dpp_precheck` | `WHERE item_tracking_code = '...'` |
| Surface category | "the SLP", "DPP surfaces" | `WHERE item_tracking_code LIKE 'slp_%'` |
| PFID (numeric) | `1320706` | `WHERE pf_id = '1320706'` |
| Product name (free text) | "professional email pro plus" | `WHERE LOWER(product_name) LIKE '%professional%email%pro%plus%'` — run Step B0 first |
| Marketing shorthand / PNL subline | "MWP Basic", "WAM", "Pro Email" | `WHERE LOWER(product_pnl_subline_name) LIKE '%basic%'` — use when product_name LIKE yields zero or clearly wrong rows; run Step B0 first |
| Product name + segment | "professional email pro plus, renewal only" | product name LIKE + `existing_customer_orders > 0` filter |

**If the entry is product-name-first:** go to Step B0 before B1.
**If the entry is ITC-first or PFID-first:** skip B0, go directly to B1 in the appropriate mode.

---

## Surface Name → ITC Map

| Ticket language | Exact ITC | LIKE filter |
|---|---|---|
| Pre-Check, PreCheck, DPP | `dpp_precheck` | `LIKE 'dpp_%'` |
| Sales Landing Page, SLP | varies | `LIKE 'slp_%'` |
| Domain Landing Page, DLP | varies | `LIKE 'dlp_%'` |
| Upgrade Path, UPP | varies | `LIKE 'upp_%'` |
| Dashboard, Manage, MGR | varies | `LIKE 'mgr_%'` |
| Cart | varies | `LIKE 'cart_%'` |

If only a surface category is given (e.g. "the SLP"), use the LIKE pattern. Show all matching ITCs ranked by total_orders — do not pick one and discard the rest.

---

## Path A — Curated Offer

### Step A1 — Surface Audit

```sql
SELECT
    ope.pf_id,
    ope.product_name,
    ope.product_term_num,
    ope.product_term_unit_desc          AS term_unit,
    ope.item_tracking_code              AS itc,
    ope.package_id,
    CASE WHEN ope.package_id IS NULL THEN 'CES (Legacy)' ELSE 'NES (Curated)' END AS offer_type,
    ope.item_discount_code,
    ope.purchase_path_name,
    ope.bill_country_code,
    ope.product_pnl_line_name,
    ope.product_pnl_subline_name,
    SUM(ope.total_orders)               AS total_orders,
    SUM(ope.new_customer_orders)        AS new_orders,
    SUM(ope.existing_customer_orders)   AS existing_orders,
    SUM(ope.total_revenue_usd)          AS total_revenue_usd,
    AVG(ope.receipt_price_usd_amt)      AS avg_receipt_price,
    AVG(ope.receipt_regular_price_usd_amt) AS avg_regular_price,
    AVG(ope.catalog_list_price_usd)     AS avg_catalog_list_price,
    AVG(ope.catalog_sale_price_usd)     AS avg_catalog_sale_price
FROM pricing_experiment_dev.offer_pulse_experiment ope
WHERE ope.item_tracking_code = '{ITC}'       -- or LIKE 'slp_%' for surface category
  AND ope.bill_modified_mst_date >= DATEADD(day, -7, CURRENT_DATE)
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
ORDER BY total_orders DESC;
```

**Show all rows.** Never truncate. Flag explicitly if any rows are omitted.

Also run the lean mapping check to catch ITC → package_id combinations that may exist outside the 7-day window:

```sql
SELECT
    pf_id,
    item_tracking_code  AS itc,
    package_id,
    cln_create_utc_ts,
    cln_update_utc_ts
FROM pricing_experiment_dev.pf_id_package_details_v1
WHERE item_tracking_code = '{ITC}'
ORDER BY cln_update_utc_ts DESC;
```

---

### Step A2 — Identify Champions and Gaps

From the audit results:
- **NES coverage %** = `SUM(total_orders WHERE offer_type = 'NES') / SUM(total_orders) * 100`
- List all distinct non-null `package_id` values — these are all active curated offers on this surface
- Flag: multiple package_ids may indicate an A/B test already running
- Flag: multiple PFIDs under the same package_id means the bundle covers multiple products
- Flag: a package_id appearing with multiple discount codes means pricing variants exist
- Flag: if `item_discount_code` looks like a UUID, no real promo code is active (billing stored the offer ID); if it looks like a readable code (e.g. `DISCWAMBA`, `disc444888`), a real discount is applied

**Branch decision after Step A2:**

| Condition | Next step |
|---|---|
| NES coverage > 0% | **Step A2a — NES Path** |
| NES coverage = 0% | **Step A2b — CES Merchandising Lookup** |
| Zero rows returned | Stop — ask analyst to verify the ITC or widen the date window |

A mixed surface (NES > 0% but < 100%) follows the NES path (Step A2a). The CES portion is noted in the Flags table as "CES surface gap" but does **not** trigger Step A2b — the surface has a NES champion and the goal is to clone that.

---

### Step A2a — NES Path (Catalog Lookup)

*Runs when NES coverage > 0%.*

For **every distinct non-null `package_id`** from Step A2, run all calls in parallel:

**Step 1 — get the curated offer definition:**
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<package_id>)
```

**Immediately classify the offer type from the response:**
- `prePurchaseKeyMap` absent or `prePurchaseKeyMap.offers[]` empty → **Standalone Offer**
- `prePurchaseKeyMap.offers[]` has one or more entries → **Offer Collection**

State this classification explicitly in output before any other catalog detail.

---

**Step 2 — look up the Base Offer:**
```
get_offer_collection_definition(datasource="catalog-offers", offerCollectionId=<offerId>)
```
Record: `name`, `tags[]`. For Standalone Offers, also record `plan` — it is authoritative. For Offer Collections, do not surface the top-level plan.

---

**Step 3 — for Offer Collections, look up every Component Offer in parallel:**
```
get_offer_definition_by_id(datasource="catalog-offers", offerId=<prePurchaseKeyMap.offers[i].offerId>)
```

For each component, record:
- `offerId` — from the `prePurchaseKeyMap` entry
- `name` — from `get_offer_definition_by_id`
- `tags[]` — from `get_offer_definition_by_id` (all tags returned; never infer)
- `plan` — from the `prePurchaseKeyMap` entry itself, **not** from `get_offer_definition_by_id`

Never omit a component. If `prePurchaseKeyMap.offers[]` has 3 entries, make 3 calls. If a lookup fails, include the row with the raw `offerId` and note "lookup failed — verify manually."

> **M365 geo-availability:** If any component offer's `tags[]` includes `m365`, flag it. M365 Business plans are not available in all markets. If the request targets ROW or India, confirm M365 availability for those markets before recommending a clone that includes an M365 component.

---

**Handling `offers[]` entries in `get_offer_collection_definition` that are not in `prePurchaseKeyMap`:**

`get_offer_collection_definition` returns a top-level `offers[]` array that contains ALL offers attached to the collection — including the primary product itself and any optional/non-bundled offers. This is broader than `prePurchaseKeyMap`.

- **`prePurchaseKeyMap.offers[]`** (from `get_curated_offer`) — the bundled add-on components wired at purchase time. This is the authoritative source for all Component Offer IDs (M365, Titan Email will always be here if they are part of the bundle). Every entry here is required for the ecomm payload.
- **`offers[]`** (from `get_offer_collection_definition`) — all offers in the collection, including the primary product (labeled `parentOffer` in `offersGrouping`) and any optional add-ons not bundled at checkout (e.g. Norton, upsell seats).

For any `offerId` in `offers[]` that does NOT appear in `prePurchaseKeyMap.offers[]`: look it up with `get_offer_definition_by_id` in the same parallel batch and include it in a separate table labeled **"Additional Offers in Collection (not wired in prePurchaseKeyMap)"**. These are not required for ecomm to clone the bundle, but they must not be silently dropped.

Never infer which `offers[]` entries are "unimportant" without looking them up.

Do this for every distinct package_id, not just the highest-volume one. If 3 package_ids are active, make all catalog calls and present all 3 results side by side.

---

### Step A2b — CES Merchandising Lookup

*Runs only when NES coverage = 0%.*

The goal is to find CES package slugs from the merchandising API whose `pfids[]` match the surface PFIDs from Step A1 — establishing which named offer configuration was shown on this surface, even though no `package_id` appears in billing.

**Step 1 — Fetch all CES packages:**
```
WebFetch https://merchandising.api.godaddy.com/v1/packages
```
Returns a JSON array. Key fields per object:
- `id` — the CES package slug (e.g. `wordpress-basic-ssl-1yr`)
- `description` — human-readable label
- `packageType` — e.g. `Standard`, `Premium`
- `productPackage.products[].pfids[]` — PFIDs included in the primary products
- `productPackage.addons[]` — optional add-on groups (elective, not wired at checkout)

If the API call fails or returns an empty array, note this in the CES header and go directly to Step A2c Chain Step 2.

**Step 2 — Match surface PFIDs against package pfids[]:**

From the Step A1 surface audit, collect all distinct PFIDs observed on this surface. For each merchandising package, compute the intersection of `productPackage.products[].pfids[]` (from all products in the package) against the surface PFID set.

**Classify each match:**

| Match Type | Definition | Confidence |
|---|---|---|
| **Exact** | Package PFIDs == surface PFIDs exactly (same set, no extras, no gaps) | High |
| **Superset** | Package PFIDs ⊇ surface PFIDs (covers all surface PFIDs plus additional products) | High — flag extras |
| **Partial** | Overlap but neither is a full subset | Medium — ecomm must confirm scope |
| **No match** | Intersection is empty | Discard |

**Always render the CES Merchandising Match table** — even if no matches are found (table will be empty):

| Package Slug | Description | Package Type | Package PFIDs | Surface PFIDs Matched | Surface PFIDs Unmatched | Match Type | Surface Orders (7d) |
|---|---|---|---|---|---|---|---|

Include the "Surface Orders (7d)" column for matched PFIDs from Step A1 results so the analyst can see whether matched packages reflect live traffic.

**Branch decision after Step A2b:**

| Outcome | Action |
|---|---|
| One exact match | A2c Chain Step 1 — this package is the primary candidate |
| One or more superset matches (no exact) | A2c Chain Step 1 — smallest-superset as primary; flag extras |
| Only partial matches | A2c Chain Step 1 — best partial as primary; mark output BLOCKING — ecomm must confirm scope |
| No matches at all | Skip A2c Chain Step 1; go directly to A2c Chain Step 2 |

---

### Step A2c — CES Offer ID Resolution

*Runs when NES coverage = 0%. Execute in chain order — stop at the first step that returns a result.*

---

**Chain Step 1 — Merchandising slug → curated offer** *(only if A2b found a match)*

Take the best-match package slug from A2b. Attempt:
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<package_slug>)
```
- **Success:** Catalog recognizes this slug as a curated offer. Record the offer. Apply the same Standalone / Offer Collection classification as Step A2a. Chain resolved.
- **Not found:** Proceed to Chain Step 2.

---

**Chain Step 2 — ID list scan + keyword match**

Pull all active curated offer IDs:
```
get_curated_offers(datasource="catalog-curated-offers", active=true, limit=1200)
```

Derive keywords from:
1. The target product name or SKU (e.g. "MWP Basic" → `mwp`, `basic`, `wordpress`)
2. The surface ITC string (e.g. `slp_wordpress` → `wordpress`)
3. PFID labels from Step A1 results (e.g. PFID 1320706 = "Deluxe Managed Hosting" → `deluxe`)

For each curated offer ID in the list, keyword-match against the ID slug string. Collect all matching IDs and call `get_curated_offer` for each in parallel.

- **Success (one or more offers found whose PFID coverage matches the surface):** Chain resolved. Apply Standalone / Offer Collection classification.
- **No matches:** Proceed to Chain Step 3.

Disclosure template for ID scan (add to CES header section):
> "Found `{package_id}` by scanning `{N}` curated offer IDs from `get_curated_offers` for keyword matches on `{keyword list}`. This offer was not found via billing data — confirm with ecomm that this is the correct curated offer before wiring the experiment."

After any Chain Step 2 success, still run Chain Step 3 as a secondary validation to confirm no additional plan variants exist. Render the full candidate table from both steps.

---

**Chain Step 3 — Tag-based search**

Derive product type tags from the surface PFIDs and product names (e.g. `hosting` from MWP, `m365` from Microsoft products, `ssl` from SSL PFIDs). Run:
```
catalog_query_get_offers(
    datasource="catalog-query",
    currency=<from request>,
    marketId=<from request>,
    tags=[<derived product type tags>]
)
```

Filter the returned `plans[]` for keyword matches on the plan name field. For each matched plan, extract `offerId` from `instance.uri` (last path segment after `/offers/`) and call `get_offer_definition_by_id` in parallel.

- **Success:** Chain resolved via tag search. No curated offer slug is available from this path. The output must include a BLOCKING line: "Found via tag search only — no curated offer slug exists. Ecomm must create a new curated offer and wire this offer ID."
- **No matches:** Chain exhausted.

---

**If all chain steps fail:**

BLOCKING line in the Quick Reference: "No curated offer found via merchandising match, ID scan, or tag search — ecomm must create a new curated offer from scratch. Provide PFID list to ecomm and request offer creation."

---

### CES Output Disclosure Requirements

*Required whenever Steps A2b and A2c ran (NES coverage = 0%). Render all sections in this order, before the Quick Reference blocks.*

**Section 1 — Header (required)**

```
SURFACE IS 100% CES — Catalog Fallback Path
```

This must appear as a visible, prominent line. A Flags table row alone is not sufficient.

**Section 2 — Merchandising Match table** (from Step A2b — always rendered, even if empty)

Use the table format defined in Step A2b.

**Section 3 — Chain narrative** (one sentence per chain step attempted)

State which steps were attempted and what each returned:
- "Chain Step 1: `{package_slug}` matched as a curated offer." or "Chain Step 1: `{package_slug}` not found in catalog."
- "Chain Step 2: Scanned `{N}` curated offer IDs; `{M}` keyword matches found." or "Chain Step 2: No keyword matches in `{N}` IDs."
- "Chain Step 3: Tag search on `{tags}` in `{market}` returned `{N}` plans; `{M}` matched SKU keywords." or "Chain Step 3: No matching plans found."

**Section 4 — Candidate table** (from whichever chain step(s) succeeded)

| Plan Name | Offer ID | subscriptionType | Selected |
|-----------|----------|-----------------|---------|

Rules:
- Show every matched plan — never suppress candidates.
- If multiple plans resolve to the same offer ID, note "same offer ID" in the Selected column.
- If multiple plans resolve to different offer IDs, do not pick one — show all and mark plan selection as BLOCKING.
- Mark the best match with ✓ and a one-word reason (e.g. "best match", "AES variant", "same offer ID").

Omit this section if the chain was fully exhausted with no candidates found at any step.

**Section 5 — CES Package Request Payload** (required whenever any chain step ran)

This table gives the requester everything needed to file or review a CES package request. One row per PFID × Term combination observed on the surface. Pull all fields from the Step A1 surface audit results plus the A2b/A2c chain output.

| PFID | Product Name | Term | Tier | Discount Code | Existing CES Package | Orders (7d) | Status |
|------|-------------|------|------|--------------|---------------------|-------------|--------|

Column definitions:
- **PFID** — `pf_id` from billing
- **Product Name** — `product_name` from billing (full billing label, not marketing shorthand)
- **Term** — `product_term_num` + `product_term_unit_desc` combined (e.g. "1 Year", "2 Year", "1 Month")
- **Tier** — `product_pnl_subline_name` from billing (e.g. "Basic", "Deluxe", "Ultimate"). If null, fall back to `product_pnl_line_name`.
- **Discount Code** — `item_discount_code` from billing. If it looks like a UUID, write "None (UUID placeholder)". If it looks like a real code (e.g. `DISCWAMBA`), write the code verbatim.
- **Existing CES Package** — CES package slug from Step A2b/A2c. Use these labels by chain outcome:
  - Chain Step 1 success: `Confirmed — {slug}`
  - Chain Step 2 success (ID scan): `Candidate — {slug} (confirm with ecomm)`
  - Chain Step 3 only: `Tag search only — no slug available`
  - Chain exhausted / no match: `Not found`
- **Orders (7d)** — `SUM(total_orders)` for this PFID × Term from Step A1

Label each row in the Status column:
- Highest-volume PFID in the category that is not a removal target → `Entry champion (stays)`
- PFIDs explicitly named in the ticket as being removed → `Being replaced`
- PFIDs whose disposition is unclear → `Legacy CES — confirm disposition with ecomm`
- Multi-year or monthly variants where the ticket specifies annual only → `Scope unclear — confirm with ecomm`

Never omit a row because the volume is low. A pricing or ecomm engineer acting on incomplete scope will misconfigure the request.

---

### Path A Output

**Render only after all work is complete.** For the NES path: after all `get_curated_offer`, `get_offer_collection_definition`, and `get_offer_definition_by_id` calls have returned. For the CES path: after the merchandising fetch, all chain steps, and all catalog calls that chain steps triggered have returned. Do not render any section of the output until every call is done.

**Default output is the Quick Reference only.** Do not render supporting detail unless the analyst asks with a phrase like "show me the full audit", "give me the detail", or "expand".

| Tier | When rendered | Content |
|------|--------------|---------|
| **Quick Reference** | Always, by default | One block per bundle — the complete ecomm payload |
| **Supporting Detail** | Only on request | Surface volume table + per-bundle catalog deep-dive |

---

**Quick Reference (always rendered)**

Emit one block per distinct `package_id` (or per resolved offer on the CES path). Open each block with a header line `=== {bundle_slug} ===`, then emit a labeled record block. Labels left-aligned, padded to match the longest label in the block. Values on the right of the colon. Fields in this order:

```
=== {bundle_slug} ===
Clone Source (Package ID)  :  {see Clone Source rules below}
Base Collection ID         :  {offerId} from get_curated_offer
Component 1 — {Name}      :  {offerId} / plan: {plan}
Component 2 — {Name}      :  {offerId} / plan: {plan}
*(one line per component in prePurchaseKeyMap.offers[])*
Geo Scope                  :  {markets from request}
Discount                   :  {pct}% off {list or sale} price. Omit this line if no discount in request.
Customer Segment           :  New / existing / both
Volume                     :  {N} orders/7d on {itc} ({NES_pct}% NES)
BLOCKING                   :  One sentence. Omit this line entirely if nothing blocks ecomm from proceeding.
```

**Clone Source rules by path:**
- NES path (A2a): `{package_id}` from billing data — authoritative slug
- CES path, Chain Step 1 success: merchandising package slug confirmed as a curated offer
- CES path, Chain Step 2 success: curated offer slug found via ID scan
- CES path, Chain Step 3 only: `N/A — found via tag search only; ecomm must create curated offer`
- CES path, chain exhausted: `N/A — new offer required`

**Field rules:**
- One Component line per entry in `prePurchaseKeyMap.offers[]`. Use the component's `name` from `get_offer_definition_by_id` as the label. Never omit a component.
- For Standalone Offers: omit all Component lines. Base Collection ID is the complete payload.
- If a component's `plan` is absent: write `NOT SPECIFIED — ecomm must confirm` and include a BLOCKING line.
- If a component lookup failed: write `{raw offerId} — lookup failed, verify manually`.
- Never add placeholder lines. Omit lines that do not apply.
- No prose before or after the Quick Reference blocks — except the required CES disclosure sections when the CES path ran.

When multiple bundles are stacked, separate each block with a blank line between the last field line and the next `=== {bundle_slug} ===` header.

After all Quick Reference blocks, append a Flags table. One row per condition that applies. Omit the table entirely if no flags apply.

| Flag | Detail |
|------|--------|
| A/B test likely | 2 bundles active on `{itc}` simultaneously — confirm champion with ecomm before cloning |
| M365 geo risk | Component `{name}` has `m365` tag — confirm availability for `{market}` before cloning |
| CES surface gap | `{itc}` (`{N}` orders/7d) has no `package_id` — these orders are CES and not covered by the NES champion |
| Discount code conflict | `{itc}` has existing code `{code}` that would be overridden |
| Plan not specified | Component `{name}` has no plan in `prePurchaseKeyMap` — ecomm must confirm |

*(Show only rows that apply. Do not show example rows. Omit the table entirely if nothing flags.)*

---

**Supporting Detail (render only when the analyst asks)**

When the analyst requests detail, append after the Quick Reference. Do not render by default.

**Surface Volume**

All rows, no truncation. One table.

| PFID | Product Name | Term | ITC | Package ID | Offer Type | Discount Code | Total Orders | New Orders | Existing Orders | Avg Receipt Price | Avg List Price |
|------|-------------|------|-----|-----------|------------|--------------|-------------|-----------|----------------|-----------------|---------------|

**Bundle Detail — {package_id}**

One block per bundle. Open with the bundle slug as a heading.

State the offer type first as a single bolded line: `Offer Collection — N bundled components.` or `Standalone Offer — single product, single plan.`

Then render catalog details as a labeled record block:

```
=== {bundle_slug} ===
Curated Offer ID          :  {package_id}
Base Collection ID        :  {offerId}
Collection Name           :  {name} from get_offer_collection_definition
Status                    :  ACTIVE / INACTIVE
Supports overridePolicies :  Yes / No
Tags                      :  All tags from API, comma-separated. Never inferred.
Orders (7d)               :  {total_orders}
NES Share                 :  {nes_pct}%
```

Then, for Offer Collections only, the component table:

| Component Offer ID | Name | Plan Wired in Bundle | Tags | Notes |
|---|---|---|---|---|
| `{offerId}` from `prePurchaseKeyMap` entry | `{name}` from `get_offer_definition_by_id` | `{plan}` from `prePurchaseKeyMap` entry — never from `get_offer_definition_by_id`. If absent: **NOT SPECIFIED** | All tags from API | geo flags; autoRenew if present |

One row per `prePurchaseKeyMap.offers[]` entry. Never omit.

If `offers[]` from `get_offer_collection_definition` contains entries not present in `prePurchaseKeyMap`, append a second table labeled "Also in Collection (not wired at checkout)":

| Offer ID | Name | Tags | Role |
|---|---|---|---|

Omit this table entirely if no such entries exist.

---

## Path B — Pricing / Discount Ticket

Use this path when the ticket is about applying a discount code or changing price points — the goal is to produce a complete, verified PFID list for the pricing team.

### Step B0 — PFID Discovery (product-name-first entry only)

Run this step when the analyst names a product (not an ITC or PFID) to discover all relevant PFIDs before the full inventory. Skip if the entry is ITC-first or PFID-first.

**Two-column strategy — always search both `product_name` and `product_pnl_subline_name` in a single query.** Marketing shorthand (MWP, WAM, Pro Email) rarely appears in `product_name` — the actual column contains the full billing name (e.g. "Basic Managed WordPress Websites"). Using only `product_name` LIKE will silently return zero rows for shorthand entries.

```sql
SELECT
    ope.pf_id,
    ope.product_name,
    ope.product_term_num,
    ope.product_term_unit_desc          AS term_unit,
    ope.product_pnl_line_name,
    ope.product_pnl_subline_name,
    SUM(ope.total_orders)               AS total_orders,
    SUM(ope.existing_customer_orders)   AS existing_orders,
    SUM(ope.new_customer_orders)        AS new_orders
FROM pricing_experiment_dev.offer_pulse_experiment ope
WHERE (
    LOWER(ope.product_name) LIKE '%{keyword}%'
    OR LOWER(ope.product_pnl_subline_name) LIKE '%{keyword}%'
    OR LOWER(ope.product_pnl_line_name) LIKE '%{keyword}%'
)
  AND ope.bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_orders DESC;
```

Use the root keyword from the product name. For "MWP Basic" use `basic`; for "Websites and Marketing" use `websites and marketing` against `product_pnl_line_name`; for multi-word product names chain keywords: `LOWER(product_name) LIKE '%professional%email%pro%plus%'`.

If the combined query returns zero rows or only clearly wrong products, stop and ask: "I found no matches for '{keyword}' in product_name or product_pnl_subline_name. Please provide a PFID or the exact `product_pnl_subline_name` value."

If the analyst specified a customer segment:
- **Renewal / existing only:** add `HAVING SUM(existing_customer_orders) > 0`; carry `WHERE existing_customer_orders > 0` into B1
- **New only:** `HAVING SUM(new_customer_orders) > 0`

Present the collapsed PFID × Term table and confirm with the analyst before continuing. If the list looks wrong (unexpected products, missing term lengths), stop and ask. After confirmation, proceed to Step B1 in **PFID Inventory Mode**.

---

### Step B1 — PFID Inventory

Declare the mode before running the query:

| Mode | When to use | Grain | Key columns |
|---|---|---|---|
| **PFID Inventory** | Product-name-first entry, or "give me the PFID list" ask | PFID × Term | PFID, Term, Segment, Orders, US pricing |
| **Blast Radius** | ITC-first entry, or "what surfaces / discount codes are affected" ask | PFID × ITC × Package ID × Country × Currency | Full width — ITC, package_id, discount code, revenue |

---

#### PFID Inventory Mode

Use when the goal is a clean PFID list for a pricing ticket — not surface attribution.

```sql
SELECT
    ope.pf_id,
    ope.product_name,
    ope.product_term_num,
    ope.product_term_unit_desc                                    AS term_unit,
    SUM(ope.total_orders)                                         AS total_orders,
    SUM(ope.existing_customer_orders)                             AS existing_orders,
    SUM(ope.new_customer_orders)                                  AS new_orders,
    AVG(CASE WHEN ope.bill_country_code = 'US'
             AND ope.trxn_currency_code = 'USD'
             THEN ope.receipt_price_usd_amt END)                  AS avg_us_receipt_price,
    AVG(CASE WHEN ope.bill_country_code = 'US'
             AND ope.trxn_currency_code = 'USD'
             THEN ope.receipt_regular_price_usd_amt END)          AS avg_us_regular_price,
    AVG(CASE WHEN ope.bill_country_code = 'US'
             AND ope.trxn_currency_code = 'USD'
             THEN ope.catalog_list_price_usd END)                 AS avg_us_list_price,
    AVG(CASE WHEN ope.bill_country_code = 'US'
             AND ope.trxn_currency_code = 'USD'
             THEN ope.catalog_sale_price_usd END)                 AS avg_us_catalog_sale_price
FROM pricing_experiment_dev.offer_pulse_experiment ope
WHERE ope.pf_id IN ({pfid_list})           -- from Step B0, or supplied directly
  AND ope.bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2, 3, 4
ORDER BY ope.pf_id, ope.product_term_num;
```

If the analyst specified renewal/existing only, add: `AND ope.existing_customer_orders > 0` to the WHERE clause (row-level filter, not HAVING, to preserve accurate order counts).

US-only pricing columns are intentional — pricing tickets are typically scoped to US USD. If international pricing is needed, request it explicitly.

---

#### Blast Radius Mode

Use when the goal is to understand surface spread, package_id coverage, or existing discount codes — typically ITC-first or multi-surface tickets.

```sql
SELECT
    ope.pf_id,
    ope.product_name,
    ope.product_term_num,
    ope.product_term_unit_desc          AS term_unit,
    ope.item_tracking_code              AS itc,
    ope.package_id,
    CASE WHEN ope.package_id IS NULL THEN 'CES (Legacy)' ELSE 'NES (Curated)' END AS offer_type,
    ope.item_discount_code,
    ope.product_pnl_line_name,
    ope.product_pnl_subline_name,
    ope.bill_country_code,
    ope.trxn_currency_code,
    SUM(ope.total_orders)               AS total_orders,
    SUM(ope.total_revenue_usd)          AS total_revenue_usd,
    AVG(ope.receipt_price_usd_amt)      AS avg_receipt_price,
    AVG(ope.receipt_regular_price_usd_amt) AS avg_regular_price,
    AVG(ope.catalog_list_price_usd)     AS avg_catalog_list_price,
    AVG(ope.catalog_sale_price_usd)     AS avg_catalog_sale_price
FROM pricing_experiment_dev.offer_pulse_experiment ope
WHERE ope.item_tracking_code = '{ITC}'       -- or LIKE / IN for multi-surface
  AND ope.bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
ORDER BY total_orders DESC;
```

If the ticket is product-first but blast-radius mode is needed, filter on `pf_id` instead of ITC and keep the full group-by.

> **Row count warning:** Blast Radius Mode groups on 12 columns. On a product with many surfaces, currencies, and discount codes, this query can exceed 500 rows. If it does, add `HAVING SUM(total_orders) > 10` to suppress noise rows, or switch to PFID Inventory Mode and drill blast radius as a follow-up.

---

### Step B2 — Discount Scope Assessment

From the results, identify:
- **All distinct PFIDs** that would be affected
- **All distinct ITCs** those PFIDs appear on (the blast radius)
- **All distinct package_ids** — each may need its own discount code configuration
- **Existing active discount codes** per PFID × ITC × package_id combination — flag any that look like real codes vs UUID placeholders
- **Current pricing** (receipt vs list vs catalog sale price) — anchor for the new discount target
- **NES vs CES split** per PFID — affects how the discount is applied

> **Call out explicitly:** If a discount code is meant to apply to a specific package_id and that package_id appears on more ITCs than the ticket specifies, surface those additional ITCs. Pricing team needs to decide whether to widen scope or restrict via ITC filtering.

**CES ITC handling (Blast Radius Mode only):**

For each distinct ITC that has CES-only rows (all `package_id` values null), run a lightweight CES slug lookup to give the pricing team a reference for discount code configuration:

1. **Merchandising match (Step A2b logic):** Fetch `https://merchandising.api.godaddy.com/v1/packages`. Match the ITC's PFID set against `pfids[]` in each package. Classify as Exact, Superset, or Partial.
2. **ID list scan (Step A2c Chain Step 2 only):** If no merchandising match, scan `get_curated_offers` ID list for keyword matches. Do **not** run Chain Step 3 (tag search) for Path B — pricing tickets do not require full offer classification.

Assign a confidence level per ITC:
- **High** — exact PFID match from merchandising API
- **Medium** — superset/partial merchandising match, or ID list scan keyword match
- **None** — all steps failed

The goal is a slug reference for discount configuration, not a full offer classification. Document findings in the CES Offer Candidates table in the output.

---

### Path B Output

**Render only after all work is complete.** After the Step B0/B1 queries have returned and, if CES ITCs are present, after the Step B2 merchandising fetch and ID scan have returned. Do not render any section of the output until every call is done.

Output format depends on the mode used in Step B1.

---

#### PFID Inventory Mode Output

Before the PFID table, render a Flags table for any of the following conditions. Omit entirely if nothing flags.

| Flag | Detail |
|------|--------|
| Unexpected product match | PFID `{pfid}` — `{product_name}` does not appear to match the requested product |
| Zero US USD pricing | PFID `{pfid}` — no US USD transactions in the 30-day window; may not be sold in the US |
| Segment filter exclusions | `{N}` PFIDs excluded — zero `{existing/new}` orders in window |

**PFID Inventory Table (all rows, no truncation)**

| PFID | Product Name | Term | Existing Orders | New Orders | Avg US Receipt Price | Avg US Regular Price | Avg US List Price | Avg US Catalog Sale Price |
|------|-------------|------|----------------|-----------|---------------------|---------------------|------------------|--------------------------|

End with a one-line count: "N PFIDs across M term lengths."

This table is the ticket payload. When in doubt, include the row and let the analyst exclude it.

---

#### Blast Radius Mode Output

Before the PFID × ITC table, render a Flags table for any of the following conditions. Omit entirely if nothing flags.

| Flag | Detail |
|------|--------|
| Scope summary | `{N}` distinct PFIDs × `{M}` distinct ITCs in scope |
| CES-only surface | `{itc}` (`{N}` orders/7d) has no `package_id` — discount mechanism differs from NES |
| Blast radius exceeds ticket scope | PFID `{pfid}` also appears on `{itc}` which is not listed in the ticket — pricing team must decide whether to include |
| Existing discount code | PFID `{pfid}` on `{itc}` currently has code `{code}` — will be overridden |

**Complete PFID × ITC Inventory (all rows, no truncation)**

| PFID | Product Name | Term | ITC | Package ID | Offer Type | Current Discount Code | Total Orders (30d) | Avg Receipt Price | Avg List Price | Avg Catalog Sale Price |
|------|-------------|------|-----|-----------|------------|----------------------|-------------------|-----------------|---------------|----------------------|

**CES Offer Candidates** *(rendered only when one or more ITCs are CES-only and the Step B2 CES lookup ran)*

| ITC | PFID | Product Name | Term | Tier | Discount Code | Existing CES Package | Found Via | Confidence |
|---|---|---|---|---|---|---|---|---|

One row per **PFID × Term** combination within each CES ITC — not one row per ITC. A surface with multiple PFIDs or term lengths produces multiple rows. If no CES ITCs exist, omit this table entirely.

Column definitions:
- **Term** — `product_term_num` + `product_term_unit_desc` combined (e.g. "1 Year", "2 Year")
- **Tier** — `product_pnl_subline_name` from Step B1 results. If null, use `product_pnl_line_name`.
- **Discount Code** — `item_discount_code` from Step B1 results. UUID placeholder → write "None".
- **Existing CES Package** — slug from merchandising match or ID scan. Write "Not found" if both steps failed.
- **Found Via** values: `Merchandising — exact`, `Merchandising — superset`, `Merchandising — partial`, `ID scan`, `—` (none found)
- **Confidence**: `High` (exact merchandising match), `Medium` (superset/partial match or ID scan), `None` (all steps failed)

**Discount Ticket Summary**

Labeled record block. Labels left-aligned, padded to match the longest label. Every field populated from query results. Write "None" or "N/A" if a field genuinely does not apply.

```
=== Discount Ticket Summary ===
PFIDs to include          :  {pfid1}, {pfid2}, ...
Package IDs (NES)         :  {package_id1}, {package_id2}, ... (or "None — CES only")
CES Slug Candidates       :  {slug} on {itc} (unconfirmed — see CES Offer Candidates table above); or "None found"
ITCs in scope             :  {itc1}, {itc2}, ...
Price baseline            :  PFID {pfid} → avg receipt ${price} / avg list ${list} per term; ...
Existing codes to replace :  {code} on {itc} / PFID {pfid}; or "None"
```

The `CES Slug Candidates` line is **omitted entirely** if the surface is 100% NES or if Path B ran in PFID Inventory Mode.

---

## Multi-Surface Tickets

If the ticket mentions multiple surfaces (e.g. "DPP and SLP"), run the audit query once per surface and produce one output block per surface. Do not merge them unless the analyst requests a combined view.

---

## Known Relationship Patterns

| Pattern | Example | What to do |
|---------|---------|------------|
| One ITC → many PFIDs | SLP selling hosting + email | Show all; don't assume the highest-volume PFID is the only relevant one |
| One PFID → many ITCs | PFID 1320706 on 6 different surfaces | Show all surfaces; flag cross-surface blast radius |
| One ITC → many package_ids | SLP with A/B test running | Show all; ask analyst which is intended champion |
| One package_id → many PFIDs | Bundle includes hosting + SSL + email | Show all PFIDs; all need to be in the pricing ticket |
| One PFID → many discount codes | Same PFID with different codes per ITC | Show all; don't pick the most common one |
| Standalone Offer | Domain or SSL sold without add-ons | `prePurchaseKeyMap` absent or empty. One `get_offer_collection_definition` call. Plan from that response is authoritative. State "Standalone Offer — single product, single plan" in output. |
| Offer Collection (bundle) | WordPress hosting + M365 or Titan Email | `prePurchaseKeyMap` has one or more entries. Never use the top-level plan. Iterate all `prePurchaseKeyMap.offers[]` entries — for each, call `get_offer_definition_by_id` and record `offerId`, `name`, `tags[]`, and the `plan` from the `prePurchaseKeyMap` entry. All Component Offer IDs are primary ecomm payload — a missing row means ecomm builds an incomplete offer. Also look up any `offers[]` entries from `get_offer_collection_definition` that are absent from `prePurchaseKeyMap` and list them in a separate table (not required for the clone, but must not be silently dropped). |

When in doubt, show more not less. It is always better to present a row and let the analyst exclude it than to silently omit it.

---

> **No ticket has been created or modified.** This is read-only output for your review. To create or update a ticket, tell me explicitly and I'll do it then.
