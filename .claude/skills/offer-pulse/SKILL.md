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

After the clarifying questions gate resolves, execute immediately — run queries, then catalog MCP where needed, then present results. Do not narrate steps mid-execution.

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

---

## Catalog Concepts

These IDs appear in all Path A output. Use them consistently.

| Term | What it is | Where it comes from |
|------|-----------|---------------------|
| **Package ID = Curated Offer ID** | Same value, two names. The human-readable slug. | Billing data / Catalog MCP |
| **Base Offer ID** | UUID in the `offerId` field of `get_curated_offer`. Points to an Offer Collection definition (the primary product). | `get_curated_offer` response |
| **Offer Collection** | Product definition with plans, terms, and pricing schema. Always the primary product. Retrieved via `get_offer_collection_definition`. | `catalog-offers` datasource |
| **Component Offer ID** | UUID from `prePurchaseKeyMap.offers[].offerId`. Each is a bundled add-on (e.g. M365, Titan Email). Retrieved via `get_offer_definition_by_id`. | `catalog-offers` datasource |

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
| Search available plans by product type (CES fallback) | `catalog_query_get_offers(datasource, currency, marketId, tags)` | `catalog-query` |

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

### Step A2 — Identify Champions and Gaps

From the audit results:
- **NES coverage %** = `SUM(total_orders WHERE offer_type = 'NES') / SUM(total_orders) * 100`
- List all distinct non-null `package_id` values — these are all active curated offers on this surface
- Flag: multiple package_ids may indicate an A/B test already running
- Flag: multiple PFIDs under the same package_id means the bundle covers multiple products
- Flag: a package_id appearing with multiple discount codes means pricing variants exist
- Flag: if `item_discount_code` looks like a UUID, no real promo code is active (billing stored the offer ID); if it looks like a readable code (e.g. `DISCWAMBA`, `disc444888`), a real discount is applied

If NES coverage is 0%, the surface is fully CES — proceed to the CES Catalog Fallback section below. Never treat CES as terminal. A Flags table row labeled "CES surface gap" is **not sufficient** — a standalone `⚠ SURFACE IS 100% CES` header section must appear before the Quick Reference blocks, per the rendering rules in the CES Catalog Fallback section. A Flags row may appear in addition, but never instead of the header.

### Step A3 — Catalog Lookup

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

**Step 2 — look up the Base Offer (always an Offer Collection):**
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

For any `offerId` in `offers[]` that does NOT appear in `prePurchaseKeyMap.offers[]`: look it up with `get_offer_definition_by_id` in the same parallel batch and include it in a separate table labeled **"Additional Offers in Collection (not wired in prePurchaseKeyMap)"**. These are not required for ecomm to clone the bundle, but they must not be silently dropped — they tell ecomm what else is attached to the parent collection.

Never infer which `offers[]` entries are "unimportant" without looking them up. An entry that looks like a secondary add-on may turn out to be a required geo-variant component.

---

Do this for every distinct package_id, not just the highest-volume one. If 3 package_ids are active, make all catalog calls and present all 3 results side by side.

---

### CES Catalog Fallback (surface has no package_ids)

When the surface audit returns 0% NES coverage, there is no `package_id` to use as a lookup key. Use the catalog query API to find the offer definition for the proposed SKU directly.

**Step 1 — Query available plans for the product type:**
```
catalog_query_get_offers(
    datasource="catalog-query",
    currency=<currency from request, e.g. "USD">,
    marketId=<market from request, e.g. "US">,
    tags=[<product_type_tag, e.g. "m365", "hosting", "ssl">]
)
```
This returns a `plans[]` array of all purchasable plans for the given product type and market. Each entry contains a `plan` name field and an `instance.uri` shaped like `/customers/{id}/offers/{offerId}`.

**Step 2 — Filter plan names for the target SKU:**
Search `plan` names for keywords derived from the ticket's target SKU (e.g. for "Online Essentials w/o Teams": "online", "essentials", "no teams"). Track the total number of plans returned and the number that matched.

**Step 3 — Extract offer IDs from matched plans:**
For each matching plan, parse the `offerId` from `instance.uri` — it is the last path segment after `/offers/`.

**Step 4 — Look up the offer ID:**
Proceed with `get_offer_definition_by_id` and `get_offer_collection_definition` using the extracted offer ID. Apply the same Standalone / Offer Collection classification rules as the NES path above.

**Step 5 — Disclose the search in output (required):**

Before the Quick Reference block, include a CES path header and a candidate summary:

```
**SURFACE IS 100% CES — Catalog Fallback Path**

No package_id exists on this surface. catalog_query_get_offers returned {N} total plans
for {product_type} in {market}. {M} matched the target SKU keywords ({keyword list}).
```

Then render a candidate table showing all matched plans:

| Plan Name | Offer ID | subscriptionType | Selected |
|-----------|----------|-----------------|---------|
| `onlineEssentialsNoTeams` | `575a7d2a-...` | p1nt | ✓ best match |
| `m365OnlineEssentialsNoTeams` | `575a7d2a-...` | p1nt | same offer ID |
| `onlineBusinessEssentialsAesNoTeams` | `575a7d2a-...` | p1nt | AES variant |

Rules for the candidate table:
- Show every matched plan — never suppress candidates.
- If multiple plans resolve to the same offer ID, note "same offer ID" in the Selected column — this means they are variants of the same underlying offer, not separate offers.
- If multiple plans resolve to **different** offer IDs, do not silently pick one. Show all and flag plan selection as BLOCKING in the Quick Reference output.
- Mark the best match with ✓ and a one-word reason (e.g. "best match", "AES variant", "same offer ID").

**When a curated offer is found via `get_curated_offers` ID list scan (not via `catalog_query_get_offers`):**

If the curated offer is discovered by scanning the `get_curated_offers` ID list (e.g., searching 1,200 IDs for keyword matches on the target SKU name), use this disclosure template in the CES header section instead of the `catalog_query_get_offers` template:

> No package_id exists on this surface. Found `{package_id}` by scanning `{N}` curated offer IDs from `get_curated_offers` for keyword matches on `{keyword list}`. This offer was not found via billing data — confirm with ecomm that this is the correct curated offer before wiring the experiment.

After finding the curated offer via list scan, still run `catalog_query_get_offers` as a secondary validation step to enumerate all available plan variants for the target product type. Render the candidate table from those results, marking the already-found curated offer's plan with "found via ID scan" in the Selected column. This confirms there are no competing candidates and documents the search exhaustively. Never skip this secondary validation — a list-scan match is not sufficient evidence that no other plan variants exist.

**Step 6 — Legacy SKU context (required on CES path when a curated offer is found or created):**

From the Step A1 surface audit results, identify all PFIDs in the same product category as the new offer. Render this table before the Quick Reference blocks, immediately after the CES header and candidate table:

| PFID | Product Name | Term | Total Orders (7d) | New Orders (7d) | Avg Catalog Sale Price | Status |
|------|-------------|------|--------------------|-----------------|----------------------|--------|

Label each PFID:
- Highest-volume PFID in the category that is **not** named in the ticket as a removal target → `Entry champion (stays)`
- PFIDs explicitly named in the ticket as being removed → `Being replaced`
- PFIDs whose disposition is unclear from the ticket → `Legacy CES — confirm disposition with ecomm`
- Multi-year or monthly variants of a SKU where the ticket specifies annual only → `Scope unclear — confirm with ecomm`

Never omit a row because the volume seems low. A pricing engineer acting on incomplete scope will misconfigure the replacement.

### Path A Output

**Default output is the Quick Reference only.** Do not render supporting detail unless the analyst asks for it with a phrase like "show me the full audit", "give me the detail", or "expand".

The output has two tiers:

| Tier | When rendered | Content |
|------|--------------|---------|
| **Quick Reference** | Always, by default | One table per bundle — the complete ecomm payload, nothing else |
| **Supporting Detail** | Only on request | Surface volume table + per-bundle catalog deep-dive |

---

**Quick Reference (always rendered)**

Emit one block per distinct `package_id`. Open each block with a header line `=== {bundle_slug} ===`, then emit a labeled record block. Labels left-aligned, padded to match the longest label in the block. Values on the right of the colon. Fields in this order:

```
=== {bundle_slug} ===
Clone Source (Package ID)  :  {package_id}
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

When multiple bundles are stacked, separate each block with a blank line between the last field line and the next `=== {bundle_slug} ===` header.

Field rules:
- One Component line per entry in `prePurchaseKeyMap.offers[]`. Use the component's `name` from `get_offer_definition_by_id` as the label. Never omit a component.
- For Standalone Offers: omit all Component lines. Base Collection ID is the complete payload.
- If a component's `plan` is absent from its `prePurchaseKeyMap` entry: write `NOT SPECIFIED — ecomm must confirm` as the value and include a BLOCKING line.
- If a component lookup failed: write `{raw offerId} — lookup failed, verify manually`.
- Never add placeholder lines. Omit lines that do not apply.
- No prose before or after the Quick Reference blocks — except when the CES Catalog Fallback path ran, in which case the required CES header and candidate table precede the Quick Reference blocks.

After all Quick Reference blocks, append a Flags table. Include one row per condition that applies. Omit the table entirely if there are no flags.

| Flag | Detail |
|------|--------|
| A/B test likely | 2 bundles active on `{itc}` simultaneously — confirm champion with ecomm before cloning |
| M365 geo risk | Component `{name}` has `m365` tag — confirm availability for `{market}` before cloning |
| CES surface gap | `{itc}` (`{N}` orders/7d) is 100% CES — no package_id exists on this surface to clone |
| Discount code conflict | `{itc}` has existing code `{code}` that would be overridden |
| Plan not specified | Component `{name}` has no plan in `prePurchaseKeyMap` — ecomm must confirm |

*(Show only the rows that apply. Do not show example rows. Omit the table entirely if nothing flags.)*

---

**Supporting Detail (render only when the analyst asks)**

When the analyst requests detail, append the following after the Quick Reference. Do not render it by default.

**Surface Volume**

All rows, no truncation. One table.

| PFID | Product Name | Term | ITC | Package ID | Offer Type | Discount Code | Total Orders | New Orders | Existing Orders | Avg Receipt Price | Avg List Price |
|------|-------------|------|-----|-----------|------------|--------------|-------------|-----------|----------------|-----------------|---------------|

**Bundle Detail — {package_id}**

One block per bundle. Open with the bundle slug as a heading.

State the offer type first as a single bolded line: `Offer Collection — N bundled components.` or `Standalone Offer — single product, single plan.`

Then render the catalog details as a labeled record block. Labels left-aligned, padded to match the longest label in the block. Values on the right of the colon:

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

---

### Path B Output

Output format depends on the mode used in Step B1.

---

#### PFID Inventory Mode Output

Before the PFID table, render a Flags table for any of the following conditions that apply. Omit the table entirely if nothing flags.

| Flag | Detail |
|------|--------|
| Unexpected product match | PFID `{pfid}` — `{product_name}` does not appear to match the requested product |
| Zero US USD pricing | PFID `{pfid}` — no US USD transactions in the 30-day window; may not be sold in the US |
| Segment filter exclusions | `{N}` PFIDs excluded — zero `{existing/new}` orders in window |

**PFID Inventory Table (all rows, no truncation)**

| PFID | Product Name | Term | Existing Orders | New Orders | Avg US Receipt Price | Avg US Regular Price | Avg US List Price | Avg US Catalog Sale Price |
|------|-------------|------|----------------|-----------|---------------------|---------------------|------------------|--------------------------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

End with a one-line count: "N PFIDs across M term lengths."

This table is the ticket payload. If a term length is missing, a pricing engineer will configure the wrong PFID set. When in doubt, include the row and let the analyst exclude it.

---

#### Blast Radius Mode Output

Before the PFID × ITC table, render a Flags table for any of the following conditions that apply. Omit the table entirely if nothing flags.

| Flag | Detail |
|------|--------|
| Scope summary | `{N}` distinct PFIDs × `{M}` distinct ITCs in scope |
| CES-only surface | `{itc}` (`{N}` orders/7d) has no `package_id` — discount mechanism differs from NES |
| Blast radius exceeds ticket scope | PFID `{pfid}` also appears on `{itc}` which is not listed in the ticket — pricing team must decide whether to include |
| Existing discount code | PFID `{pfid}` on `{itc}` currently has code `{code}` — will be overridden |

**Complete PFID × ITC Inventory (all rows, no truncation)**

| PFID | Product Name | Term | ITC | Package ID | Offer Type | Current Discount Code | Total Orders (30d) | Avg Receipt Price | Avg List Price | Avg Catalog Sale Price |
|------|-------------|------|-----|-----------|------------|----------------------|-------------------|-----------------|---------------|----------------------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Discount Ticket Summary**

Render as a labeled record block. Labels left-aligned, padded to match the longest label. Values on the right of the colon. Populate every field from query results. Write "None" or "N/A" if a field genuinely does not apply.

```
=== Discount Ticket Summary ===
PFIDs to include          :  {pfid1}, {pfid2}, ...
Package IDs (NES)         :  {package_id1}, {package_id2}, ... (or "None — CES only")
ITCs in scope             :  {itc1}, {itc2}, ...
Price baseline            :  PFID {pfid} → avg receipt ${price} / avg list ${list} per term; ...
Existing codes to replace :  {code} on {itc} / PFID {pfid}; or "None"
```

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
