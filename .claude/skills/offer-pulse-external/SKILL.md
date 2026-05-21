---
name: offer-pulse-external
description: Given a Jira offer ticket, a surface ITC, or a product name, audit all offers on that surface and produce the data needed for an ecomm engineering ticket (curated offer creation). External distribution version.
---

# /offer-pulse — Surface Offer Auditor

Sub-route determined from data — **NES Curated Offer** (surface has billing `package_id`s → catalog lookup) or **CES Package** (no `package_id`s → merchandising API chain). Output: Offer type (Standalone/Collection), Curated Offer ID or CES Package ID, and either: Offer ID + Plan (Standalone) or Offer Collection ID + all Component Offer IDs + per-component plans (Collection) — ready for ecomm engineering ticket.

After the clarifying questions gate resolves, execute immediately and silently — run all queries, then all catalog/merchandising calls, collect every result, then render the complete output once at the end. Never emit partial output, intermediate tables, or step narration mid-execution. The analyst sees only the final assembled output.

**HARD CONSTRAINTS:**
- Read-only. Never create, update, transition, or comment on any Jira ticket without explicit analyst instruction.
- Never read linked ecomm tickets. The champion is determined from data and the catalog MCP only.
- Never show only the top result when multiple exist. A surface can have many PFIDs, many package IDs, and many discount codes simultaneously. Show all of them.
- Every response ends with an explicit reminder that no ticket action has been taken.
- Every markdown table must have one row per unique combination of values. Never compress multiple values into a single cell (e.g., if a PFID appears on 3 ITCs, that is 3 rows — not one row with "itc1, itc2, itc3" in the ITC cell).
- In Step M1 (Modify mode) AND in Chain Step 2 (Create/Clone mode), never derive keyword seeds solely from the ITC string. Use the surface keyword seed table in both steps — `dpp_precheck` requires seeds for the wsb-vnext, i18n, m365, and solutionset families, not just "precheck" and "dpp". An incomplete keyword seed produces an incomplete Existing Packages or Candidate table and an incorrect ticket.

---

## Domain Vocabulary

| Technical Term | Business Label | Definition |
|---|---|---|
| PFID | Product ID | The underlying product SKU (e.g. `1320706`) |
| ITC | Surface | The page/journey where the customer saw the offer (e.g. `slp_wordpress`) |
| Package ID | Curated Offer ID | Named offer slug from billing/CLN data (e.g. `wordpress-o365-forever-ssl-basic`). NES only — CES has no package ID. |
| NES | Curated Offer | New eCommerce — catalog-backed offers with named bundles. Identified by a non-null `package_id`. |
| CES | Legacy Offer | Classic eCommerce — no named bundle. `package_id` is null. |
| Standalone Offer | Single-product curated offer | Curated offer with no bundled add-ons. `prePurchaseKeyMap` absent or empty. Output shows `Offer ID` + `Plan`. `Offer Collection ID` field is always shown; write `Not available` when none is present. |
| Offer Collection | Bundled curated offer | Curated offer with one or more add-ons wired via `prePurchaseKeyMap`. Output shows `Offer Collection ID` + one Component line per entry. No standalone Plan line. |
| CES Package | Legacy named bundle | A named CES offer configuration in the merchandising API (e.g. `wordpress-basic-1yr`). Not present in billing — used only for catalog resolution on fully-CES surfaces. |

---

## Catalog Concepts

These IDs appear in all Path A output. Use them consistently.

| Term | What it is | Where it comes from |
|------|-----------|---------------------|
| **Package ID = Curated Offer ID** | Same value, two names. The human-readable slug. | Billing data / Catalog MCP |
| **Offer ID** (standalone) | The `offerId` field from `get_curated_offer` when `prePurchaseKeyMap` is absent or empty. Points to the product definition. The plan from `get_offer_collection_definition` is authoritative. Output label: `Offer ID`. Always emit `Offer Collection ID : Not available` on standalones — never omit the field. | `get_curated_offer` response |
| **Offer Collection ID** (bundle) | The `offerId` field from `get_curated_offer` when `prePurchaseKeyMap` has one or more entries. Same UUID field — the label changes based on geometry. Points to the primary product definition in a bundle. Output label: `Offer Collection ID`. | `get_curated_offer` response |
| **Component Offer ID** | UUID from `prePurchaseKeyMap.offers[].offerId`. Each is a bundled add-on (e.g. M365, Titan Email). Only present on Offer Collections. Retrieved via `get_offer_definition_by_id`. | `catalog-offers` datasource |
| **CES Package ID** | Slug from the GoDaddy merchandising API (e.g. `wordpress-basic-ssl-1yr`). Used only on the CES fallback path — never present in billing data. | `https://merchandising.api.godaddy.com/v1/packages` |

**Critical rule — geometry determines which fields to emit:**
- `prePurchaseKeyMap` absent or empty → **Standalone**. Show `Offer ID` + `Plan`. Show `Offer Collection ID : Not available`. No component lines.
- `prePurchaseKeyMap.offers[]` has entries → **Offer Collection**. Show `Offer Collection ID` + one Component line per entry. No standalone `Plan` line.
- Neither geometry returns an `offerId` → BLOCKING. Do not emit any ID fields.
- Do not assume a Curated Offer ID always maps to a collection. Verify geometry from the response before emitting output.

---

## Resolution Confidence

The skill derives offer IDs via several methods in decreasing confidence order. When output is produced via an inferred path (not the direct billing-confirmed path), the Champion line and relevant fields carry an explicit disclosure label.

| Resolution Path | How it works | Confidence | Disclosure label |
|---|---|---|---|
| **Direct** | `package_id` present in billing → `get_curated_offer` lookup → geometry from `prePurchaseKeyMap` | Highest — billing-confirmed ground truth | *(none — no disclosure required)* |
| **Merchandising match** | No `package_id` in billing; WebFetch merchandising API matched surface PFIDs to a package slug | Medium-high — API match, not billing-confirmed | `INFERRED — merchandising API match` |
| **ID scan** | No `package_id` in billing; keyword search of all active curated offer IDs returned slug matches | Medium — keyword inference | `INFERRED — keyword scan` |
| **Tag search** | No `package_id`; tag-based catalog search; no existing curated offer slug found | Lower — no existing offer; net-new build required | `INFERRED — tag search; no existing offer` |
| **Pre-launch** | Zero billing rows; active catalog entry found by keyword match | Low-medium — product not yet receiving traffic | `INFERRED — pre-launch (zero billing rows; catalog match only)` |

**What this means for downstream tickets:** Output produced via the Direct path can be filed immediately — the champion is billing-confirmed. Output produced via any Inferred path should be validated with ecomm before filing — the suggested champion is a best-match candidate derived from keyword or API matching, not a billing-observed active offer.

These labels appear in the `Champion` line source annotation and in the Route Lock line. If you see an `INFERRED` label, treat the champion as a strong recommendation — not a confirmed fact.

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
| Fetch all CES packages with PFID arrays | WebFetch `https://merchandising.api.godaddy.com/v1/packages` — **call at most once per run; truncation is expected and acceptable** (see Step A2b WebFetch reliability rule) | External — public, no auth required |

Run all catalog lookups in parallel where possible. For N package IDs, fire all `get_curated_offer` calls at once. For M component offers within a package, fire all `get_offer_definition_by_id` calls at once.

---

## Architecture Reference

Key facts embedded here so no companion skill is required for catalog resolution.

### Known Reusable Component Offer UUIDs

These component offers appear across multiple curated offer bundles. Treat as known constants — no extra catalog lookup needed.

| Component | offerId UUID | Tags | Notes |
|---|---|---|---|
| M365 / Office 365 | `575a7d2a-d1ef-40f2-a7e5-dbcc09c20391` | `partneremail`, `m365` | Bundled email in cPanel-365, MWP, WSB, UK domain bundles |
| Titan Email | `927a9d45-7c5b-4652-ad68-d5cd9be75028` | `titanemail` | Bundled email in cPanel-OX, i18n builder, MENA domain bundles |
| Professional Email | `2468b30f-f448-4b21-a506-9c4103666f0d` | `partneremail`, `professional-email` | Standalone and CES ATMP packages only — not a child component inside NES bundles |
| SSL Certificate | `28e5b730-4e70-46b0-8672-6e18a17f81a1` | `sslcert` | Standalone offer AND child component in VPS4 and cPanel bundles |
| VPS4 Hosting | `d29f7b62-9766-43bc-b230-353579eaad9c` | `vps4` | Virtual Private Server v4 |
| cPanel Business Hosting | `05730877-89bd-49c0-8fff-c9880b743bf0` | `diablo` | cPanel hosting; `diablo` tag = machine-migrated from CES |
| WAM / Websites & Marketing | `d9e7bde4-7b28-49b3-b2fd-5dc528ab8062` | `wam`, `wsb` | US WAM |
| WAM International | `862a92dc-879f-4148-b43d-5c98898754c4` | `wsb`, `wam` | AU/CA/UK/international DPP domain bundles |
| NewDomain | `edf13c43-7d39-4f90-aa81-b40666d51f75` | `new-domain-offer` | Domain registration component in DPP bundles |
| Duda | `2c5e3bb2-e6dc-4b13-855e-36b148cc98fd` | `duda` | Website builder; MENA region bundles only |
| Smart Line | `89973c51-aacd-49a7-bcf8-876ff0e425b8` | — | Telephony; appears in US DPP tier-6 domain bundle |

**M365 (`575a7d2a`) and Titan Email (`927a9d45`) are the two universal email building blocks.** Same component UUID; context differs by bundle.

### Ghost-ID Prefix Patterns

Certain `package_id` prefixes are always NOT FOUND across all catalog datasources. Do not retry or block on these — classify immediately:

| Prefix | Example | Behavior |
|---|---|---|
| `nes-` | `nes-cpanel-set-1-economy-ssl-365-wss-xtra` | Page emits `nes-{slug}` as the pkgid field. Strip the `nes-` prefix and look up the clean slug in catalog. If the clean slug is also NOT FOUND, then classify as ghost. |
| `offer-` | `offer-airo-builder-professional` | Always NOT FOUND. May be experiment IDs or retired offers. |
| `_NNNmo` suffix | `wsb_vnext_tier2_060mo` | CES merch-package aliases. Suffix encodes a term override. Look up in `merch-packages` datasource, not `catalog-curated-offers`. |

When a `get_curated_offer` returns NOT FOUND: (1) if slug starts with `nes-`, strip prefix and retry with clean slug before classifying as ghost; (2) check `offer-` ghost prefix, (3) check if it is a `_NNNmo` term alias in `merch-packages`, (4) check if it is a retired offer still referenced in old event data.

### apiVersion 2 vs apiVersion 3

| | apiVersion 2 | apiVersion 3 |
|---|---|---|
| Component reference | `offersGrouping` + `prePurchaseKeyMap` with explicit UUIDs | `offerIds[]` array |
| Components resolvable? | Yes — via `get_offer_definition_by_id` | No — referenced UUIDs return NOT FOUND via V2 endpoint |
| Behavior for offer-pulse | Full decomposition possible | Treat as Standalone — curated offer slug is the only anchor |

### Known Free Add-on PFIDs

These appear as `purchaseType=Free` entries inside CES packages. Useful for PFID-matching on the CES path:

| PFID | Product | Notes |
|---|---|---|
| 3604 | Standard SSL 1yr free | Appears in virtually every hosting package |
| 464069 | M365 OfficeBusiness Ps free trial 1yr | WSB, cPanel-365, Business Hosting-365 packages |
| 1192198 | OX Professional Email Startup free 1yr | cPanel-ox variants |
| 965772 | GoDaddy Workspace email free tier | WordPress Workspace packages |

---

## Clarifying Questions Gate

Seven intake dimensions govern Path A query scope. Run this check before any queries or catalog lookups. If the request already answers a dimension, skip that question. Present all needed questions as a single numbered list — do not ask sequentially. Dimensions 3 (Market) and 5 (Term) are blocking — do not proceed past the gate until both are answered.

**Jira entry rule:** When the entry is a Jira ticket, fetch it first. Explicitly request these five structured fields — they are the primary sources for their respective dimensions and override prose in the title or description:

| Field ID | Dimension | What it resolves |
|---|---|---|
| `customfield_14809` | D2 — Segment | New Customer / Existing / Both |
| `customfield_20800` | D3 — Market | Regions affected |
| `customfield_34656` | D4 — Surface | Authoritative surface/ITC |
| `customfield_13603` | D6 — Offer Lever | Classification/lever |

If `customfield_34656` conflicts with the ticket title or description, flag the conflict explicitly before proceeding — do not silently resolve in favor of either. Then re-run all seven skip tests against the extracted ticket fields before asking any questions. A ticket that names the operation type, product, term, surface, market, ticket type, and offer lever resolves all seven dimensions — ask nothing.

**Maximum 4 questions.** If all seven dimensions are unclear, drop ITC Specificity and Offer Lever — infer "all surfaces matching the category" and "Offer Lever unknown" and state both assumptions. Priority order when questions must be dropped: Path > Offer Operation > Term > Market > Segment > Offer Lever > ITC Specificity. Never drop Term or Market to preserve ITC Specificity. Market is always required; it cannot be dropped in favor of any lower-priority dimension. Offer Lever is always optional — if unanswered, record "Not specified" and proceed.

**What offer geometry is and why it is NOT a gate dimension:**
Offer geometry (standalone vs bundle vs add-on vs upsell) is derived from data — not supplied by the analyst. Step A1 returns the active `package_id` values on the surface. Step A2a classifies each as Standalone or Offer Collection based on whether `prePurchaseKeyMap` is present in the catalog response. Asking the analyst for geometry before running Step A1 would require them to know something the data will tell us. Do not ask. If the discovered geometry conflicts with the analyst's stated intent (e.g. the surface's only active offer is a bundle but the analyst asked for a standalone), surface the conflict after Step A2 — not before. Similarly, net-new vs clone is resolved by the chain steps, not by a gate question.

**Skip test — this exact request must produce zero questions:**
> "80% discount on 1-year Basic Managed WordPress Hosting for Rest of World and India on the Sales Landing Page, new and existing customers — give me the full curated offer creation payload for ecommerce engineering"

*(Dimension 0 — Offer Operation = Create/Clone from "curated offer creation payload". Dimension 1 — Path = A from "curated offer creation payload". Dimension 2 — Segment = both from "new and existing". Dimension 3 — Market = ROW + India. Dimension 4 — ITC = SLP. Dimension 5 — Term = 1 Year from "1-year". Dimension 6 — Offer Lever = not specified, non-blocking, record as "Not specified". All seven resolved — zero questions.)*

---

### Dimension 0 — Offer Operation (Create/Clone vs Modify)

**This dimension is evaluated first.** It determines the entire execution mode.

**Skip if:** the request contains unambiguous language indicating the operation type:
- **Create/Clone signals:** "create new", "clone", "new offer", "offer creation", "net-new", "build a new bundle" → Offer Operation = Create/Clone
- **Modify signals:** "add to", "add [product] to existing", "add component to", "modify", "update the bundle", "wire [product] into", "add [product] as an add-on to existing bundles" → Offer Operation = Modify

**Pricing-framing inference layer (check before asking):**

Before presenting the Dimension 0 question, inspect the input for operation signals. Apply the first rule that yields an unambiguous result.

**Signals that resolve D0 WITHOUT asking (explicit and unambiguous — covered by Skip if above):**
These fire before any question is asked. If any apply, D0 is resolved — do not ask.
- Create/Clone: `new offer`, `clone`, `create offer`, `add to surface`, `net-new`, `build a new bundle`, `pricing change`, `pricing update`, `price update`, `upsell`
- Modify: `add to`, `add [product] to existing`, `add component to`, `modify`, `update the bundle`, `wire [product] into`

**Pricing-amount signals (direction-neutral — do NOT auto-proceed):**
- `$X.XX/mo`, `$X/month`, `per month`, `display price`, `annual price`, `annual display price`, `price at`, `price for`
- `DISC######`, `discount code`, `promo code`, `coupon`

These signals describe the artifact under discussion, not the operation type. Pricing language (e.g. "create a new offer at $6.99/mo") describes the override price, not whether the ticket is for a new offer or a pricing change. Auto-proceeding on pricing signals alone produces false positives on audit and pricing-review requests.

If pricing-amount signals are present AND no explicit Create/Clone or Modify tokens are present → ask the D0 question (see Ask if section below). Do NOT auto-infer Create/Clone. Do NOT proceed without asking.

If no signals of any kind are present → proceed to "Ask if" as normal.

**Ask if:** the operation is ambiguous (e.g. "TrustedSite on the precheck surface" with no verb specifying create vs add-to-existing), OR pricing-amount signals are present without explicit Create/Modify tokens.

**When the operation is ambiguous — use the D0 question:**

Question: "Are you **creating a new offer** (or cloning an existing one) or **modifying an existing offer** (e.g. adding a new product as a component to existing bundles)?"

**Resolve to one of three modes:**

| Mode | What it means | Trigger signals | Execution path |
|------|---------------|-----------------|----------------|
| **Create / Clone** | Build a new curated offer or clone an existing one. No existing bundle needs to change. | "create new", "clone", "new offer", "offer creation", "net-new", "build a new bundle" | Standard Path A chain: Steps A1 → A2 → A2a/A2b/A2c → Path A Output |
| **Modify — Add Component** | An existing bundle(s) on the surface needs a new product added as a component. The existing bundle structure is not being replaced. | "add to", "add [product] to existing", "add component to", "modify", "update the bundle", "wire [product] into" | Steps M1 → M2 → M3 → Modify Output (see below) |
| **Wire Existing Offer to New Surface** | A curated offer already exists in the catalog (at Rev > 1 or recently modified, meaning it is confirmed active) and needs to be made available on an additional surface ITC — no new offer creation or bundle modification required. | "wire to surface", "activate on [ITC]", "make available on", "surface [existing offer] on", or when Chain Step 2 / A2c returns a confirmed active offer that is NOT currently observed on the requested ITC | Steps A1 → A2a (catalog lookup only) → Wire Output (see below). Do not run A2b or A2c — the offer already exists. |

**Wire Output:** Emit a single Quick Reference block with the existing `Curated Offer ID`, `Offer ID` / `Offer Collection ID` (whichever geometry applies), all component IDs, and the target ITC(s). Add a BLOCKING line if the offer is not confirmed active in the catalog. Do not run the CES chain. Do not run Step B0.

If the request is ambiguous after asking, default to **Create/Clone** and note the assumption.

---

### Dimension 0b — Product Role (conditional — fires only when B0 add-on annotation triggered)

**Skip if:** B0 did not flag any known add-on PFID. Also skip if the analyst's request makes the role unambiguous:
- "Standalone M365 pricing", "M365 as a primary product", "M365-only offer" → role = Primary. Skip.
- "M365 in the wordpress bundle", "as an add-on", "component", "bundled with hosting" → role = Add-on. Skip.
- Entry is ITC-first or PFID-first with no add-on ambiguity → skip.

**Ask if:** B0 flagged one or more known add-on PFIDs AND the role was not made explicit in the entry.

Question: "Is **{product_name}** the **primary product** being sold on this surface (e.g. a standalone email or SSL subscription), or is it included as an **add-on component** within a hosting or website bundle? Answer 'unsure' if you're not certain — I'll show both paths."

**How the answer affects downstream routing:**

| Answer | Effect on A2b merchandising match |
|--------|----------------------------------|
| **Primary** | In A2b, when inspecting CES packages that contain the PFID, filter to packages where the PFID appears in `productPackage.products[].pfids[]` only — not in `addons[]`. This scopes champions to offers where the product is the main sellable item. |
| **Add-on** | In A2b, filter to packages where the PFID appears in `productPackage.addons[]`. Expect many matches. Add a flag to the output: "This product appears as a bundled add-on in {N} packages — the pricing ticket should target the host bundle's discount code, not a standalone offer for this PFID." |
| **Unsure** | Run A2b without role filtering. Present results in two labeled groups: "Packages where this is the primary product" and "Packages where this is a bundled add-on." The analyst selects the correct group. |

If the analyst answers "unsure" or does not answer, always use the Unsure branch — never silently default to Primary or Add-on.

---

---

### Dimension 2 — Customer Segment

**Source priority:**
1. **Jira `customfield_14809`** — when present and non-null, use it directly. Value mapping: `New Customer` → new customers only; `Existing Customer` → existing/renewals only; `Both` → both. If present, skip D2 entirely.
2. **Entry text** — if the request states "new customers", "existing customers", "renewals", "both", or "new and existing", skip D2.
3. **Ask** — if neither source resolves it. Exception: if the request is a pure surface audit with no pricing or offer scope, infer "both" and state the assumption rather than asking.

**How segment affects the query:**
- The Step A1 query always returns both `new_customer_orders` and `existing_customer_orders` as columns regardless of segment — you need full surface volume to identify champions. Segment is used for output labeling and for the Customer Segment field in the Quick Reference block, not for a WHERE clause filter.

Question: "Should this cover **new customers**, **existing / renewal customers**, or **both**?"

---

### Dimension 3 — Target Markets / Geo Scope

**Skip if:** specific markets or regions are named (e.g. "ROW and India", "US only", "all markets", "globally").

**Market inference layer (run before asking — attempt in this order):**

Before presenting the market question, attempt inference from four sources in priority order. Apply the first source that yields an unambiguous result.

**Source 0 — Jira `customfield_20800`** (only when entry is a Jira ticket):
If present and non-null, use it directly as the market/geo scope. This field overrides all inference sources below. Map the value to the appropriate billing filter and skip the question entirely. If the value is ambiguous (e.g. lists multiple regions without clear scope), fall through to Source 1.

**Source 1 — ITC prefix signals** (only if the ITC is already resolved):

| ITC prefix pattern | Confidence | Inferred market |
|-------------------|------------|-----------------|
| `dpp-intl-*`, `dpp-{market}-{ccTLD}-*` | Hard resolve | International / non-US (geo is explicit in slug — skip the question) |
| `mena-*` | Hard resolve | MENA region (geo is explicit in slug — skip the question) |
| `ssl-config` | Soft infer only | SSL products have unified global pricing — no geo-split PFID variants. Document as `Market (inferred: global — confirm if market-specific config needed)` and proceed. |
| `slp_*`, `dpp_precheck`, `dpp_config1`, `dlp_*`, `upp_*` with no geo qualifier | Soft infer only | Likely US domestic — document as `Market (inferred: likely US domestic — confirm)` and proceed, but flag in output that the analyst should confirm before filing the ticket |
| Mixed or ambiguous prefix | No inference | Proceed to Source 2 |

**Important:** Plain prefix surfaces (`slp_*`, `dpp_precheck`, `dpp_config1`, `dlp_*`, `upp_*`) process billing for multiple `bill_country_code` values. The ITC string alone is not authoritative for geo. A soft-inferred market skips the gate question but must include a visible confirmation flag in the output — it does NOT count as a hard-resolved skip that suppresses the flag entirely.

**Source 2 — Ticket body signals** (for Jira entry):
- Explicit geo scope in the ticket body: "Reseller customers", "US only", "India", "ROW", named countries → infer directly
- Product name with geo encoding: "India Titan Email", "UK hosting" → infer from the name

**Source 3 — Product geography profile** (last resort — apply only when no ITC or ticket signal is available):
- MWP (Managed WordPress) → US domestic inferred only when BOTH conditions are true: (1) ITC is a soft-inferred US-domestic surface (`slp_*`, `dlp_*`) AND (2) the ticket body contains no international scope signals. MWP product name alone is NOT sufficient — all confirmed NES champions embed M365 as the email component, so an incorrect market inference makes the M365 component recommendation architecturally wrong due to geo-availability.
- cPanel hosting, Business Hosting on `slp_*` or `dlp_*` surfaces without an intl variant → US domestic is a safe default
- WAM/WSB, Email (M365/Titan), domain products → do NOT infer from product alone; these have geo-split champion families

**Inference resolution rule:** If exactly one market is unambiguously supported by the inference sources above, skip the question and document the result as `Market (inferred): {value}` in the gate resolution summary. If inference is ambiguous or produces no result, market must be asked — it is a required input and cannot be assumed.

**Why market is especially load-bearing for Path A:** Market is required for the `catalog_query_get_offers` call in CES Chain Step 3 (`marketId` and `currency` parameters). It also determines the billing country filter applied in Step A1 and whether the M365 geo-availability flag fires in Step A2a. Without a market, Step A1 produces a miscounted PFID list, Chain Step 3 cannot run, and M365 risk cannot be assessed.

**Market → query filter mapping:**
- "US only" → `AND ope.bill_country_code = 'US' AND ope.trxn_currency_code = 'USD'`
- "ROW" (Rest of World) → `AND ope.bill_country_code NOT IN ('US', 'CA', 'IN')` — confirm the ROW definition with the analyst if the ticket specifies a non-standard boundary
- "India" → `AND ope.bill_country_code = 'IN'`
- Named country → `AND ope.bill_country_code = '{iso_code}'`
- "All markets" or "globally" → omit country filter; add `ope.bill_country_code` and `ope.trxn_currency_code` to the GROUP BY and display them as columns
- CES Chain Step 3: translate market to `marketId` (ISO country code, e.g. `US`, `IN`) and `currency` (ISO currency code, e.g. `USD`, `INR`)

Question: "Which markets should this cover? (e.g. US only, ROW, India, all markets, or a specific country list)"

---

### Dimension 4 — ITC / Surface

**Primary signal — Jira `customfield_34656`:** When the entry is a Jira ticket, read this field first. Its value is the authoritative surface and overrides the ticket title and description. If `customfield_34656` and the title/description disagree, flag the conflict explicitly before proceeding — do not silently resolve in favor of either.

**FOS / "Front of Site" requires clarification:** FOS is a broad term covering multiple sub-surfaces — it does NOT map exclusively to SLP. When a ticket or prompt uses "FOS" or "Front of Site" without specifying a sub-surface, and `customfield_34656` is also absent or generic, ask which sub-surface is intended before proceeding:

> "FOS covers multiple sub-surfaces. Which does this ticket target? (a) SLP — Sales Landing Page (`slp_*`), (b) Cart, (c) Precheck (`dpp_precheck`), or (d) Checkout?"

**SLP → DLP billing pattern:** When the resolved surface is `slp_*`, flag this in the output: SLP is the *referring* ITC — when customers click through from the SLP to purchase, the transaction may log under a `dlp_*` ITC in billing (e.g. `slp_wordpress` traffic often transacts as `dlp_wordpress_hosting`). Query both the SLP ITC and its associated DLP ITC when auditing SLP surfaces. State both in the output.

**Skip if:** an exact ITC string is given (e.g. `slp_wordpress`), `customfield_34656` resolves to a specific surface, or the entry is product-name-first or PFID-first with no surface reference.

**Ask if:** a surface category is named without an exact ITC (e.g. "the SLP", "DPP surfaces", "FOS") AND `customfield_34656` is absent or ambiguous AND the request has enough other specificity that narrowing would meaningfully reduce output. Do not ask if the analyst's stated purpose is a full surface audit.

Question: "The SLP maps to multiple ITCs (`slp_wordpress`, `slp_hosting_category`, etc.). Should I audit **all SLP surfaces** or a specific one? (Say 'all' to proceed with full coverage.)"

---

### Dimension 5 — Billing Term

**Why this matters:** A single product maps to different PFIDs by term length. PFID 1320706 is the 3-year variant of MWP Deluxe; there are separate PFIDs for 1-year and 2-year. The champion package ID and PFID list are meaningless without a term scope — mixing terms produces the wrong champion and the wrong PFID list for both engineering and pricing tickets.

**Data columns:** `product_term_num` (integer, e.g. `1`, `2`, `3`, `12`) and `product_term_unit_desc` (string — **stored lowercase** in billing data: `'year'`, `'month'`, `'quarter'`). Together they form the term label (e.g. "1 Year", "2 Year", "3 Year", "1 Month"). These columns are present in all queries — filter on both. **Always write `product_term_unit_desc = 'year'` not `'Year'` — the column stores lowercase only. Using Title Case returns zero rows.**

**Term pre-parse (mandatory — run before evaluating the skip test):**

Before asking Dimension 5, attempt to extract the term from the entry value using these signals:

| Signal | Examples | Inferred term |
|--------|---------|---------------|
| Explicit term word | "annual", "1-year", "one year", "yearly" | 1 Year |
| Explicit term word | "biennial", "2-year", "two year" | 2 Year |
| Explicit term word | "triennial", "3-year", "three year" | 3 Year |
| Explicit term word | "monthly", "1-month", "per month" | 1 Month |
| Pricing pattern | "$X/mo", "$X per month", "$X/month" | 1 Month |
| Pricing pattern | "$X/yr", "$X per year", "$X annually" | 1 Year |
| Entry phrase | "annual SKUs", "annual plan", "annual term", "1 Year" | 1 Year |

- If pre-parse finds one unambiguous signal: skip Dimension 5 entirely. Document the inference in the Term Scope header: `TERM SCOPE: 1 Year (inferred from entry — "annual SKUs")`.
- If pre-parse finds conflicting signals (e.g. entry mentions both monthly and annual): ask in confirmation form — "I inferred {term} from your entry — is that correct, or does this cover multiple terms?"
- If pre-parse finds nothing: ask Dimension 5 as normal.

**Skip if:** a specific term is named or parseable in the entry (see pre-parse table above).

**Ask if:** no term length is mentioned.

Question: "Which billing term(s) should this cover? (e.g. 1 Year, 2 Year, 3 Year, 1 Month — or 'all terms' to see the full cross-term breakdown)"

**Handling the answer:**
- **Specific term(s) given** (e.g. "1-year" or "1-year and 2-year"): add `AND product_term_num = {N} AND product_term_unit_desc = '{unit_lowercase}'` to **Step A1 only. Do NOT add this filter to Step B0 or Step M1** — those steps enumerate the complete PFID universe and must run without term restriction (see HARD CONSTRAINT in each). `{unit_lowercase}` is always lowercase: `'year'`, `'month'`, `'quarter'`. When multiple terms are specified, use `AND (product_term_num, product_term_unit_desc) IN (({N1}, 'year'), ({N2}, 'month'))` — lowercase values only.

  **HARD CONSTRAINT — no scoping filter (term, segment, or volume) EVER applies to Step B0 or Step M1.** These are PFID discovery steps — their job is to enumerate the complete product universe across all terms and segments. Applying a term filter, a `new_customer_orders > 0` filter, or a volume minimum at this stage produces an incomplete PFID list, which causes entire bundles to be silently missed downstream. These filters belong exclusively in the experiment query (Step A1).

  **1-year anchor query:** When a specific non-1-year term is identified, also run a parallel Step A1 query for 1-year (`product_term_num = 1 AND product_term_unit_desc = 'year'`). Reason: for NES curated offers, the base offer ID is term-agnostic — the 1-year row typically has the highest billing volume and most reliably confirms the correct base offer ID and plan. If the identified term is already 1-year, no extra query is needed. This supplemental run applies to Step A1 only — the HARD CONSTRAINT above is unchanged. Never use this rule to assume the term is 1-year; the term must still be identified from the ticket, inferred from signals, or asked as D5.

- **"All terms" or "unknown":** Do not filter. Run all queries without a term filter, but **group and display term as a first-class column** in every result table and every output block. Note clearly at the top of the output: "TERM SCOPE: All terms — output includes mixed-term results. Champion and PFID lists are not scoped to a single term; confirm the correct term with the analyst before filing the ticket."
- **Term stated in the Jira ticket:** extract it from the ticket body and skip the question. If the ticket body is ambiguous (e.g. "annual" could mean 1-year or 12-month), list both interpretations and ask for confirmation before running queries.

**Unit normalization:** analysts may say "annual" (= 1 Year), "biennial" or "2-year" (= 2 Year), "triennial" or "3-year" (= 3 Year), "monthly" (= 1 Month). Translate to `product_term_num` + `product_term_unit_desc` before filtering. **`product_term_unit_desc` values are always lowercase in the billing table: `'year'` not `'Year'`, `'month'` not `'Month'`, `'quarter'` not `'Quarter'`.** If the translation is ambiguous, state the assumption and confirm.

---

### Dimension 6 — Offer Lever

**Not blocking.** If unanswered after the gate, record `Not specified` and proceed.

**Source priority:**
1. **Jira `customfield_13603`** — read directly from the ticket when available. Overrides any inference from entry text.
2. **Entry text** — if the analyst names a lever explicitly (e.g. "soft bundle offer", "free trial", "sale price discount"), extract it.
3. **Ask (non-blocking, include as one of the up-to-4 gate questions)** — if `customfield_13603` is absent AND the entry text gives no clear signal AND fewer than 4 other gate questions are already needed.

**Skip if:** the lever is present in the Jira Classification field, or the analyst states it explicitly.

**Question:** "Which offer lever does this ticket use? (e.g. Soft Bundle, Sale Price Discount, Free Trial — or say 'unknown' to proceed without it)"

**Valid values (from AGIGROWTH Classification field):**

| Lever | Description |
|---|---|
| Sale Price Discount | Reduce 1st period price below list |
| Sale Price Increase | Increase 1st period price (stays below list) |
| Term-Based Pricing | Different pricing by term length |
| Free Trial - Credit Card Backed | Requires payment method upfront |
| Free Trial - BMAT | Bill Me After Trial — no card required |
| Free Trial - CMAT | Cancel Me After Trial — auto-converts unless canceled |
| Soft Bundle | Curated product combinations at combined discount |
| Lock on Create | Free trial followed by sale price for 1st term |
| ATMP | Annual Term Monthly Payment — annual commitment, monthly billing |
| Freemium | Free tier with paid upgrade path |
| Coupon Code | Promotional discount code |
| Other | Custom lever — define in Description |

**Routing note (informational — does not change data path):**

| Lever | Likely implication |
|---|---|
| Soft Bundle | Expect NES Offer Collection geometry; flag if surface shows standalone-only |
| Sale Price Discount / Sale Price Increase / Term-Based Pricing / ATMP / Coupon Code | Primarily a pricing/discount change — if the surface already has the right offer structure, `/pricing-ticket` may be the right skill rather than offer creation |
| Free Trial - BMAT / CMAT / Credit Card Backed | BPO / Cart Renewal Behavior fields in Quick Reference are critical — flag if absent in catalog response |
| Lock on Create | Two-phase pricing — confirm whether ecomm needs one offer or two |
| Freemium | Confirm whether free tier requires a separate PFID/offer |

Record the lever verbatim as provided (do not normalize casing). If `Other` is selected, note the custom description from the ticket body.

---

### Gate rendering rule

If one or more questions cannot be resolved (after skip tests and inference), collect ALL unresolved dimensions into a single numbered list and present them to the analyst in one block before running anything:

> "For the most accurate output, please answer all questions before I begin. I'll wait until I have all inputs — partial answers will result in a follow-up before any work starts.
>
> Before I run queries:
> 1. [question]
> 2. [question]"

**Do not run any queries, catalog MCP calls, or merchandising API fetches until all presented gate questions are answered.** If the analyst answers some but not all, re-present the remaining unanswered questions and continue to hold. Partial execution is not permitted — accuracy depends on the full input set being known before work begins.

If the analyst resolves all questions in a single reply, proceed immediately. If a reply answers some but leaves others open, acknowledge the answers received and re-present the remaining questions as a new numbered list using the same preamble.

---

## Entry

### Entry Option 1 — Jira Ticket
1. Fetch with `getJiraIssue` (`cloudId: godaddy.atlassian.net`). This uses the Atlassian MCP tool (`mcp__atlassian__getJiraIssue`). If the Atlassian MCP is not available, ask the analyst to paste the relevant ticket fields (surface/ITC, product or PFID, and ticket type) directly.
2. Extract from the ticket body only (ignore linked tickets):
   - **Surface / ITC** — map surface names using the Surface Map below
   - **Product / PFID** — if explicitly called out
   - **Ticket type** — curated offer creation or pricing/discount change
   - **Target price** — any explicit price point stated (e.g. "$3.99/mo", "80% off list price", "$16.99/$23.99 monthly"). Record as `Target Price (from ticket)`. This is the experiment target price, not billing history — it belongs in the Quick Reference alongside billing-derived pricing, clearly labeled as "(from ticket)".
   - **Offers being removed** — any language describing packages or products being replaced or retired (e.g. "Remove: Email Essentials w/ Security @ $2.99/mo", "replacing existing WAM packages"). Record verbatim. Populate the Status column in the CES Terminal Payload ("Being replaced") and emit an "Offers Being Replaced" note before the Quick Reference.
   - **Offer Lever / Classification** — the AGIGROWTH `Classification` field value, if populated (e.g. "Soft Bundle", "Sale Price Discount", "Free Trial - BMAT"). Record as `Offer Lever (from ticket)`. If absent or blank, record as `Not specified` — this field is non-blocking.
   - **New discount codes** — any explicitly named discount code not yet in billing (e.g. "DISCWAMBA", "use code 365AF1F1CB from PRICING-15500"). Record as `Discount (from ticket)`. Cross-reference the pricing ticket if linked. This is distinct from the billing-derived `Discount` field.
   - **Billing term** — scan the ticket body for term signals in this priority order: (1) a PFID or product table in the ticket body with a term or duration column (e.g. "1 Year", "12mo", "Annual"); (2) EP PackageID table rows whose slug encodes term (e.g. `-1yr`, `-3yr`, `-annual`, `-monthly`); (3) the product description or experiment scope field for phrases in the Dimension 5 pre-parse signal table ("annual", "1-year", "$X/yr"); (4) the ticket title. If any signal is unambiguous, record as `Term (from ticket): {value}` and skip Dimension 5 — do not ask the gate question. If multiple signals conflict (e.g. title says "annual" but PFID table has 3-year rows), record both and ask for confirmation in Dimension 5 using the confirmation form: "I see annual in the title but 3-year PFIDs in the table — which term scope should this cover?" Do not ask as a new open question — use this confirmation form only.
3. **Ticket type classifier (run before multi-arm detection and before the Clarifying Questions Gate):** Scan the ticket body for signals that indicate the ticket requires no EP offer ticket and no pricing ticket:

   | Signal type | Example signals | Early-exit label |
   |-------------|----------------|-----------------|
   | Rebate / cashback | "rebate", "cashback", "cash back", "reward", "post-purchase incentive" | rebate/cashback ticket |
   | Config toggle / feature flag | "config toggle", "feature flag", "enable/disable", "feature switch", "toggle on", "toggle off" | config/feature-flag ticket |
   | Reporting / analytics only | "reporting", "dashboard", "data pull", "analytics request", "metrics only" | reporting ticket |
   | Legal / compliance | "compliance", "legal requirement", "T&C update", "terms change" — with no pricing or offer scope | compliance ticket |

   If any signal is detected and the ticket contains NO language about offer creation, cloning, modifying an existing bundle, or changing a price or discount code, emit this block and stop:

   ```
   EARLY EXIT — {early-exit label} DETECTED
   This ticket appears to be a {type} ticket. No EP offer creation ticket or pricing ticket is required.
   Ticket signals found: "{verbatim signal text from ticket body}"
   
   Confirm this classification is correct. If the ticket does require an offer or pricing change (e.g. rebate paid via a discounted offer), respond and I will proceed with the standard offer-pulse workflow.
   ```

   Do not run the Clarifying Questions Gate or any queries until the analyst confirms the classification is wrong. If the analyst says the ticket does require offer/pricing work, proceed as normal.

4. **Multi-arm detection (run before Clarifying Questions Gate):** Scan the ticket body for multi-arm language: "Control:", "Treatment 1", "Treatment 2", "T1", "T2", "challenger", "arm", "variant A/B/C". If found, emit a **Ticket Decomposition block** before running any queries:

   ```
   MULTI-ARM EXPERIMENT DETECTED
   This ticket describes {N} experiment arms. Each arm that creates or modifies an offer requires a separate ticket type. Decompose before proceeding:
   
   | Arm | Description | Ticket Type |
   |-----|-------------|-------------|
   | Control | {description from ticket} | {no ticket — existing offer unchanged} |
   | Treatment 1 | {description from ticket} | {new offer (EP engineering) / pricing change (see /pricing-ticket) — based on description} |
   | Treatment 2 | {description from ticket} | {new offer (EP engineering) / pricing change (see /pricing-ticket) — based on description} |
   
   Confirm which arm(s) to produce output for before running queries.
   ```

   Wait for the analyst to confirm which arm(s) to run before proceeding. Run one complete path per confirmed arm.
5. Proceed to Path A below

### Entry Option 2 — Direct Input (ITC, Product Name, or PFID)

| Entry type | Example | Primary filter |
|---|---|---|
| ITC string | `dpp_precheck` | `WHERE item_tracking_code = '...'` |
| Surface category | "the SLP", "DPP surfaces" | `WHERE item_tracking_code LIKE 'slp_%'` |
| PFID (numeric) | `1320706` | `WHERE pf_id = '1320706'` |
| Product name (free text) | "professional email pro plus" | `WHERE LOWER(product_name) LIKE '%professional%email%pro%plus%'` — run Step B0 first, then Step A1 |
| Marketing shorthand / PNL subline | "MWP Basic", "WAM", "Pro Email" | `WHERE LOWER(product_pnl_subline_name) LIKE '%basic%'` — use when product_name LIKE yields zero or clearly wrong rows; run Step B0 first, then Step A1. **Exception: WAM Commerce tier uses subline `'Super Premium'`, not `'Commerce'` — see Step B0 gotcha.** |
| Product name + segment | "professional email pro plus, renewal only" | product name LIKE + `existing_customer_orders > 0` filter |

**If the entry is product-name-first:** run Step B0 first, then proceed to Step A1.
**If the entry is ITC-first or PFID-first:** skip B0 and proceed directly to Step A1.

---

## Surface Name → ITC Map

### Known Surfaces

Key surfaces for offer-pulse use cases. Volume figures as of 2026-05-15.

| ITC | Human label | NES/CES | Top packages / notes |
|---|---|---|---|
| `slp_wordpress` | WordPress Hosting Sales Page | NES | `wordpress-o365-forever-ssl-deluxe`, `wordpress-openexchange-forever-ssl-deluxe`, `wordpress-o365-forever-ssl-basic` — 100% package attachment |
| `slp_hosting_4gh` | cPanel Hosting Sales Page (4GH) | NES | `cpanel-o365-tier1/2/3`, `cpanel-set-1-economy-ssl-365-xtra` |
| `slp_pro_managed_wordpress_hosting` | Pro Managed WordPress Hosting Sales Page | NES | MWP Pro tier |
| `slp_hosting_category` | Hosting Category Sales Page (VPS/Server) | Mixed | NES: `vps4-self-managed-*` packages; CES: WordPress, M365, cPanel rows |
| `slp_ssl` | SSL Certificate Sales Page | NES | `ssl-001sites-tier1/2/managed/wildcard` all → offerId `28e5b730`; `ssl-001sites-tier3` → `bb0afea9` |
| `slp_365_category` | Email / M365 Category Sales Page | CES | Titan Email (70%) + M365 (30%) — no package IDs |
| `slp_365_category_config` | M365 Category — Seat Configuration Step | CES | M365 seat selector — no package IDs |
| `slp_airo` | Airo AI Website Builder Sales Page | NES | Domain-focused; champion: `domain` → `edf13c43` |
| `slp_rstdstore` | Standard / Shared Hosting Store | CES | No package IDs — confirmed CES |
| `dpp_precheck` | Domain Checkout Pre-Check (Add-on Step) | Mixed | NES for email essentials: champions `temp-email-essentials-99`, `temp-email-essentials-149` (live production — `temp-` slugs are not test artifacts). CES-dominant for non-email products. |
| `dpp_config1` | Domain Checkout — Add-on Configuration Step | CES | Email + DOP upsell at checkout — no package IDs |
| `dpp_absol1` / `dpp_absol1.*` | Domain Registration Checkout (all variants) | NES | All `dpp_absol1.*` experiment variants share the same champion: `domain` → `edf13c43` |
| `dlp_domain` | Domain Landing Page | NES | Champions: `domain` → `edf13c43`; `dbs` → `0ce223ed` |
| `dlp_wordpress_hosting` | WordPress Hosting Domain Landing Page | NES | MWP product |
| `dlp_usoybo` | US OYBO Domain + Email Bundle Landing Page | NES | Champion: `oybo-en-email` → `e328092f` — domain + M365 bundle |
| `mya_dom_srch` / `mya_dom_srch.*` | My Account Domain Search (all variants) | NES | All `mya_dom_srch.*` experiment variants share champion: `domain` → `edf13c43` |
| `single_product_renewal` | Single Product Renewal | CES | All products, all null packages — pure CES renewal surface |
| `notifications_bell` | Notification Bell Renewal / Upsell | CES | All null packages — pure CES |
| `upp_*` (all) | Upsell / Upgrade Path | CES | 100% CES across all upp_ surfaces — not on migration roadmap. Do not attempt curated offer resolution. |

**FOS requires clarification.** "Front of site" and "FOS" are broad terms covering SLP (`slp_*`), cart, precheck (`dpp_precheck`), and checkout — they do NOT map exclusively to `slp_*`. When a ticket uses "FOS" without a sub-surface qualifier, always check `customfield_34656` first. If that field is absent or ambiguous, ask which sub-surface is intended before querying. Never auto-route FOS to `slp_*`. See D4 for the full clarification flow.

If only a surface category is given (e.g. "the SLP"), query with `LIKE 'slp_%'` and show all matching ITCs ranked by total_orders — do not pick one and discard the rest.

---

### Prefix Fallback (for ITCs not in the table above)

| ITC prefix / pattern | Surface family | Expected NES/CES | Guidance |
|---|---|---|---|
| `slp_*` | Sales Landing Page (SLP) | Mixed — check CLN | Hosting (4GH, MWP, Pro MWP) and SSL are NES. M365, WAM, and most others are CES. Query CLN for package_id null-rate to confirm. |
| `slp-*` (hyphen), `hmc_*`, `lp_*`, `plp_*`, `mlp_*`, `_lp` suffix | SLP-family variants | Mixed — check CLN | Same routing logic as `slp_*`. Check CLN for package_id presence before assuming CES. |
| `dpp_*` with `.primary_*`, `.unavailable_*`, `.aftermarket_*`, `.smartdefault_*` suffix | Domain checkout experiment variant | NES | dpp_absol1 family — same `domain` champion (`edf13c43`). |
| `dpp_*` without experiment suffix | Domain checkout step | CES | `_config`, `_reoffer`, `_transfers` variants are CES add-on or re-offer steps. |
| `_dpp` suffix / contains, `bulk_search` exact | Domain Purchase Path non-prefix variants | Mixed — check CLN | These route to the DPP group per source of truth. Query CLN for package_id null-rate. |
| `dlp_*` | Domain Landing Page (DLP) | NES (typically) | Standard domain family. Confirm via CLN. |
| `upp_*` | Upsell / Upgrade Path (UPP) | CES | 100% CES. No NES migration planned. Skip curated offer resolution. |
| `mya_*` | My Account (MYA) | Mixed | `mya_dom_srch.*` variants are NES (domain). `mya_acctsettings_*` and renewal flows are CES. |
| `renewal` contains, `mui_*` | My Account — renewal / UI extension | CES | Covers `account_myrenewals_*`, `single_product_renewal`, `mui_*` — all MYA group, all CES. |
| `dcc` contains, `whois_serp*`, `whoisserp*` | Domain Control Center (DCC) | Mixed | `dcc` is a **contains** match. Domain search surfaces are NES; portfolio renewal and DOP flows are CES. **Do not confuse with `ddc_*`** (Domain Discount Club — separate group below). |
| `ddc_*` | Domain Discount Club (DDC) | CES | Distinct from DCC. `ddc_pro_01` = DDC; `dcc_portfolio_renewal` = DCC. All DDC surfaces are CES. |
| `cart_*`, `misc-purchase` contains, `xsell` contains | Cart (CART) | Mixed | NES for domain-search cart boxes (e.g. `cart_bottom_expresssearch`). CES for inline cross-sells (`cart_xsells_inline`, `misc-purchase`). |
| `vh_*`, `ai_onboarding_*`, `airohq*`, `dpp_bundling_is` exact | Venture Home (VH) | CES | AGI-managed. Not on NES migration path. Skip curated offer resolution. |
| `hp_*` | Homepage Quickbuy (HP) | Mixed — check CLN | Performance marketing. Query CLN for package_id presence. |
| `mgr_*`, `crm_*`, `shared_shopping_service` exact | C3 Sales Site / Reseller | CES | Internal sales tool surfaces — all CES. |
| `pro_*`, `wp_*` | GoDaddy Pro / Web Pro Microsite | CES | `wp_` = Web Pro microsite (NOT WordPress). All CES. For WordPress hosting surfaces use `slp_wordpress`, `dlp_wordpress_*`, etc. |
| `mui_*` | My Account UI extension | CES | Part of the MYA group. |
| `app_*` | In-app product surface (GDAPP) | CES | In-product upgrade / add-user flows — all CES. |
| `studio_*`, `android_*`, `ios_*`, `mob_*` | GDAPP — Mobile / Studio | CES | GoDaddy mobile apps and Studio. All CES. |
| `am_*`, `parked` contains, `tdfs` contains, `buynow` contains | Aftermarket (AM) | n/a | Cash-parking and marketplace surfaces. Not standard purchase surfaces. Do not attempt offer resolution. |
| `auction_*`, `gdc_*` | After Checkout Special (ACS) | CES | Post-checkout surfaces. Rarely the target for curated offer creation. |
| `gocentral` contains | P&C — Website Builder (GoCentral / vNext) | CES | Classic website builder surfaces. Distinct from current WAM product. |
| `netgdpipeline_*`, `dna_*` | Internal pipeline / aftermarket | n/a | Not customer-facing purchase surfaces. Do not attempt offer resolution. |

### Naming Pattern Hints

Use these to interpret an unfamiliar ITC before querying:

| Pattern in ITC slug | Meaning |
|---|---|
| `_f2p_` | Free-to-paid conversion → CES |
| `_p2p_` | Paid-to-paid plan change → CES |
| `_d2p_` | Domain-to-product in-app journey → CES |
| `_config` | Configuration step in a flow → usually CES |
| `_reoffer` | Re-offer / alternative suggestion step → CES |
| `.primary_exact`, `.primary_organicspin`, `.primary_tldcard`, `.primary_paidspin` | dpp_absol1 or mya_dom_srch experiment routing suffix → NES domain family |
| `.unavailable_*`, `.aftermarket_*`, `.smartdefault_*` | dpp_absol1 or mya_dom_srch experiment routing suffix → NES domain family |
| `_365`, `_o365` | M365 email surface → typically CES |
| `_wordpress`, `_mwp` | Managed WordPress surface → check CLN; may be NES |
| `temp-` prefix in a package_id | Live production champion — not a test artifact |

If an ITC is not matched by any of the above: query CLN directly for package_id null-rate to determine NES/CES routing. Never block execution on a vocab miss.

---

## SLP → Configure-Page Funnel Pairs

Some sales pages (SLP) act as entry surfaces only. The customer lands there, then clicks through
to a separate configure page that fires the add-to-cart event under its own ITC. Per the ITC
funnel spec, the event ITC belongs to the page that fires it — not the referrer. NES billing data
for these products appears under the configure-page ITC, not the SLP entry ITC.

**Confirmed funnel pairs:**

| Entry ITC (SLP) | Configure-Page ITC | Add-to-Cart Surface | Notes |
|---|---|---|---|
| `slp_hosting_4gh` | `dlp_hosting` | `/configure/traffic` NES configure page | Confirmed 2026-05-20 via direct traffic event query (6,018 nes-prefix slugs on `dlp_hosting`). `slp_hosting_4gh` has zero NES rows in `offer_pulse_experiment` because the add-to-cart ITC is attributed to the configure page. (GAP-042) |

**Expansion rule:** When the input ITC matches a row in the **Entry ITC** column, always query
BOTH the entry ITC and the configure-page ITC in every Step A1 and Step M1 query. This is
deterministic — no conditional judgment. The expansion fires whenever the input ITC is in the
left column of this table.

**Scope note — not all `dlp_*` surfaces are configure-page derivatives:**
- `dlp_domain` is a standalone domain landing page → does NOT expand
- `dlp_usoybo` is a standalone email bundle page → does NOT expand
- Only ITCs in the confirmed-pairs table above trigger the expansion

---

## Path A — Curated Offer

### Step A1 — Surface Audit

**Pre-flight: enumerate all package_ids on this surface (PFID-first or product-name-first entry only)**

When the entry is a PFID or a product name (not a bare ITC), run this query first against `pf_id_package_details_v1` to enumerate all `package_id` values the entry PFID participates in on this surface:

```sql
SELECT DISTINCT
    package_id
FROM pricing_experiment_dev.pf_id_package_details_v1
WHERE pf_id = '{entry_pfid}'               -- or IN ({pfid_list}) if multiple PFIDs from Step B0
  AND item_tracking_code = '{ITC}'         -- or LIKE / IN for surface category
  AND package_id IS NOT NULL;
```

Collect the returned `package_id` values into a set: `{active_package_ids}`. This becomes the IN-filter for the experiment query below.

If the pre-flight returns zero rows (no NES package_ids found for this PFID on this surface), skip the `package_id IN (...)` filter and run the experiment query with `pf_id = '{entry_pfid}'` and the ITC filter only — the surface is likely CES for this product.

If the entry is ITC-first (no specific PFID), skip this pre-flight entirely and run the experiment query with the ITC filter only.

**Funnel-pair expansion (check before writing queries)**

Before writing any Step A1 query, look up the input ITC in the SLP → Configure-Page Funnel
Pairs table above.

- If the input ITC appears in the **Entry ITC** column: replace the single-ITC filter with an
  IN-pair covering both the entry ITC and its configure-page ITC:
  `WHERE ope.item_tracking_code IN ('{entry_itc}', '{configure_page_itc}')`
  Apply this substitution in the experiment query, the pre-flight query, and the lean mapping
  check. Label the combined result rows by ITC in the output — do not collapse them.
- If the input ITC is NOT in the table: use the standard single-ITC filter.

When expansion fires, set a `SLP-DLP funnel expansion applied` flag for the Flags table.

**Experiment query**

When the pre-flight returned `package_id` values, use `package_id IN (...)` as the primary scope filter — not `pf_id = '...'`. This catches all component PFIDs in every bundle the entry PFID participates in (e.g. M365, SSL, Titan Email components that are part of the same bundle).

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
  AND ope.package_id IN ({active_package_ids})  -- from pre-flight; omit if pre-flight returned zero rows
  AND ope.bill_modified_mst_date >= DATEADD(day, -7, CURRENT_DATE)
  -- Term filter: add when a specific term was specified in the clarifying questions gate.
  -- Single term:   AND ope.product_term_num = {N} AND ope.product_term_unit_desc = '{unit}'
  -- Multiple terms: AND (ope.product_term_num, ope.product_term_unit_desc) IN (({N1},'{u1}'),({N2},'{u2}'))
  -- All terms:     omit the term filter; term is already in the GROUP BY and will appear as columns in output.
  -- NOTE: This is the FIRST step where the term filter is applied. It was not applied in B0. Apply it here.
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
ORDER BY total_orders DESC;
```

**Show all rows.** Never truncate. Flag explicitly if any rows are omitted. The result set will include PFIDs beyond the entry product — this is correct and expected when the bundle has multiple components.

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
  -- Term filter does NOT apply here — this table has no term column.
  -- Use it for historical mapping presence only; apply term scoping to the offer_pulse_experiment results above.
ORDER BY cln_update_utc_ts DESC;
```

**GAP-042 transparency (required when funnel-pair expansion fired AND the configure-page ITC returns zero NES rows in offer_pulse_experiment):**

When the expansion fired for a confirmed funnel pair and the configure-page ITC (e.g. `dlp_hosting`)
returns zero rows with a non-null `package_id` in `offer_pulse_experiment`, emit this note
immediately after the Step A1 results table — before any champion analysis:

> **GAP-042 pipeline note:** `{configure_page_itc}` shows 0 NES package rows in
> `offer_pulse_experiment`. This is a known pipeline gap: new NES add-to-cart events on this
> surface use UUID-format `productId` values that `pf_id_package_details_v1` cannot join on
> integer PFIDs. The offers exist in traffic event data but do not flow into this table until the
> pipeline is fixed. See the fallback query below for raw event data.

**Direct traffic event fallback (required when GAP-042 note fires):**

This fallback is NOT optional when the GAP-042 note fires — `offer_pulse_experiment` cannot
surface these NES events until the pipeline is fixed. Run this query to recover the actual
package slugs from the raw traffic event stream:

```sql
SELECT
    page_event_properties:trackingCode::STRING          AS itc,
    page_event_properties:packageId::STRING             AS package_id,
    COUNT(*)                                            AS event_count
FROM gd_traffic_mart.traffic_page_event
WHERE page_event_properties:trackingCode::STRING = '{configure_page_itc}'
  AND page_event_properties:packageId::STRING IS NOT NULL
  AND page_event_properties:packageId::STRING LIKE 'nes-%'
  AND event_ts >= DATEADD(day, -7, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY event_count DESC;
```

Label all results from this query as:
> `(source: direct traffic events — pipeline-bypassed; not in offer_pulse_experiment due to GAP-042)`

Use these slugs as NES package candidates for the downstream catalog resolution steps (Step A2a).
Strip the `nes-` prefix before calling `get_curated_offer` — the catalog stores the offer under
the clean slug.

---

### Step A2 — Identify Champions and Gaps

From the audit results:
- **NES coverage %** = `SUM(total_orders WHERE offer_type = 'NES') / SUM(total_orders) * 100`
- List all distinct non-null `package_id` values — these are all active curated offers on this surface
- Flag: multiple package_ids may indicate an A/B test already running
- Flag: multiple PFIDs under the same package_id means the bundle covers multiple products
- Flag: a package_id appearing with multiple discount codes means pricing variants exist
- Flag: if `item_discount_code` looks like a UUID, no real promo code is active (billing stored the offer ID); if it looks like a readable code (e.g. `DISCWAMBA`, `disc444888`), a real discount is applied
- **Component PFID note:** When the entry was PFID-first or product-name-first and the Step A1 pre-flight found NES `package_id` values, the Step A1 results will include PFIDs beyond the entry product — these are the bundled add-on components (e.g. M365, SSL, Titan Email) that participate in the same bundle. This is correct. All of these PFIDs are required for the ecomm payload. Do not treat component PFIDs as unexpected or filter them out.

**WAM dual-path detection (required when product PNL line = 'Websites and Marketing' or ticket mentions WAM/WSB):**

After computing the NES/CES split, check whether the PFIDs observed in Step A1 are active on BOTH a CES surface (ITC matches `slp_wsb_%`, `dpp_precheck`) AND a NES surface (ITC matches `slp_hosting_4gh`, `slp_wordpress`, or other NES-confirmed ITC) simultaneously.

If PFIDs are active on both surface types:
1. Emit a **DUAL-PATH EXPERIMENT** header immediately before any Quick Reference blocks:
   ```
   DUAL-PATH EXPERIMENT — Two EP tickets required
   This product is active on both CES and NES surfaces. Each requires a separate ticket filed to a different engineering owner.
     NES surfaces : {itc list where package_id IS NOT NULL}  →  Ticket to: catalog tools team
     CES surfaces : {itc list where package_id IS NULL}      →  Ticket to: @sparmar (CES engineering owner)
   ```
2. Generate two separate output sections: one NES Quick Reference block (from Step A2a) and one CES output section (from Steps A2b/A2c). Label each section with its surface type and engineering owner.
3. Do NOT merge the two output sections into a single Quick Reference.

If PFIDs are active on NES surfaces only, or CES surfaces only, proceed with the single-path routing as normal.
- **Discounted slug detection (mandatory):** Inspect every non-null `package_id` slug for discount-variant indicators: a `-disc` suffix, a `-discount-` substring, or an embedded discount-code pattern (8+ uppercase alphanumeric characters, e.g. `-365AF1F1CB`, `-disc444888`). If a slug matches any of these patterns, flag it as a discounted variant. Then: (a) emit a `Discounted variant` flag in the Flags table (see format below), (b) attempt `get_curated_offer` on the de-discounted slug (remove the `-disc` suffix or discount-code substring, e.g. `wsb-vnext-tier3-disc` → `wsb-vnext-tier3`) and record both the discounted and base versions, (c) in the Quick Reference, set the champion to the **base slug** (not the discounted variant) and note the discounted variant in the Champion line: `{base_slug} (base — use for new experiments; discounted variant {disc_slug} also active on surface)`. Engineering clones the base tier for new experiments; the discounted variant is the current live offer only. If the de-discounted lookup fails (slug not in catalog), keep the discounted slug as champion but add a BLOCKING note: "Base slug lookup failed — confirm clone source with ecomm."

**Branch decision after Step A2:**

| Condition | Next step |
|---|---|
| NES coverage > 0% | **Step A2a — NES Path** |
| NES coverage = 0% | **Pre-launch NES check (below), then Step A2b** |
| Zero rows returned | **Pre-launch NES check (below), then ask analyst to verify ITC or widen the date window** |

A mixed surface (NES > 0% but < 100%) follows the NES path (Step A2a). The CES portion is noted in the Flags table as "CES surface gap" but does **not** trigger Step A2b — the surface has a NES champion and the goal is to clone that.

**Route Lock (required immediately after the branch decision):** Once the NES/CES determination is made, commit to one sub-route and emit this single line before making any catalog or merchandising calls:

- NES path selected → `ROUTE: NES Curated Offer  —  {ITC}{if surface_label resolved: " (" + surface_label + ")"}`
- CES path selected → `ROUTE: CES Package  —  {ITC}{if surface_label resolved: " (" + surface_label + ")"}{if surface_nes_ces is CES or CES-dominant: " is a known CES-dominant surface"}  |  INFERRED PATH — no billing package_id; champion derived from merchandising API, ID scan, or tag search (see Resolution Confidence)`

Examples:
- `ROUTE: NES Curated Offer  —  slp_wordpress (WordPress Sales Landing Page)`
- `ROUTE: CES Package  —  dpp_precheck (Domain Purchase Path — Pre-Check) is a known CES-dominant surface`

This label must carry through all remaining steps and appear as the `Offer Route` field in every Quick Reference block. Do not switch routes mid-execution without a new disclosure line explaining why (e.g. pre-launch NES check changed the outcome).

**Vocab advisory (soft hint — fires only when NES coverage = 0% AND surface_nes_ces resolved):**

If `surface_nes_ces` resolved to `NES` or `Mixed`, emit this single line before the pre-launch NES check:

> `VOCAB NOTE: {ITC} is classified as {surface_nes_ces} in the surface vocabulary — running pre-launch NES check before entering the CES chain.`

This line is transparency only — it does not change routing. The pre-launch NES check always runs when NES=0%. If `surface_nes_ces` resolved to `CES` or `CES (NES in progress)`, or if the vocab lookup returned no result, omit this line entirely.

**Pre-launch NES check (required before concluding CES or zero-result):**

When NES coverage = 0% or zero billing rows are returned, run a catalog ID scan before entering the CES chain. Call:
```
get_curated_offers(datasource="catalog-curated-offers", active=true, limit=1200)
```

**Product-scope filter (required — applies to the keyword match):** Keyword-match the returned IDs against the **product name from the request only** — not against the surface ITC string. If the request named a specific product (from a Jira ticket description, ITC label, or analyst prompt), use that product name as the anchor. A match against the ITC string alone (e.g. `slp_ssl`) may return global catalog entries for products wired to OTHER surfaces — not this one. If no product name is discernible from the request, skip the pre-launch check and proceed to Step A2b.

If one or more active curated offer IDs match the product name AND no corresponding billing rows exist, the product is likely in a **pre-launch NES** state — it exists in the catalog but has not received purchase traffic yet.

**CES-only surface registry (check BEFORE routing any pre-launch NES match):**

Certain surfaces are confirmed CES-only — NES catalog entries may exist for the underlying product but are NOT wired to these surfaces. If the surface ITC matches any of the patterns below, skip the pre-launch NES route and proceed directly to Step A2b.

| Surface ITC pattern | Status | Notes |
|---|---|---|
| `ssl-config` | CES-only | SSL configuration surface; CES-only by design |
| `slp_wsb_*` | CES-only | WAM/WSB Sales Landing Pages; NES migration not yet live on these ITCs |
| `dpp_precheck` | Mixed | Email essentials NES offers ARE live (temp-email-essentials-99 and temp-email-essentials-149 confirmed active). CES-dominant for non-email products — for non-email product queries at this surface, skip pre-launch NES check. |
| `upp_*` | CES-only | Upsell Purchase Path; not on NES migration roadmap |

| Pre-launch check outcome | Action |
|---|---|
| Surface is in CES-only registry | Skip pre-launch NES check. Proceed directly to Step A2b. Emit **CES-ONLY SURFACE** disclosure (see below). |
| Surface not in registry AND one or more active catalog matches found for product name, zero billing rows | Emit **PRE-LAUNCH NES** disclosure (see below). Do NOT enter the CES chain (A2b/A2c). Route as NES via Step A2a using the catalog matches. |
| No catalog matches found, zero billing rows | Proceed to Step A2b (genuine CES or no offers configured) |
| No catalog matches found, NES = 0% but CES billing rows exist | Proceed to Step A2b as normal |

**CES-ONLY SURFACE disclosure (emit when surface is in the registry):**

```
CES-ONLY SURFACE — {ITC} is not on the NES migration path
  Surface              : {ITC}{if surface_label resolved: " (" + surface_label + ")"} | {surface_nes_ces if resolved, else "NES/CES: see surface vocab"}
  NES catalog entries  : {matched slugs, or "none found"}
  Status               : CES-only surface. Catalog entries for this product exist but are not wired to this surface.

  Routing as CES (Step A2b). To request NES wiring for this surface, file a catalog tools ticket.
```

**PRE-LAUNCH NES disclosure (emit when pre-launch check fires):**

```
PRE-LAUNCH NES — Zero billing rows, active catalog entry found
  Product : {product_name from request}
  Curated Offer ID(s) found : {matched slugs}
  Billing rows (last 7 days) : 0

  This product appears to be in a pre-launch state — configured in the NES catalog but not yet receiving purchase traffic.
  Routing as NES (Step A2a) using the catalog match. Confirm launch status with ecomm before filing the ticket.
  If the product is confirmed CES, respond and I will proceed via the CES chain instead.
```

Do not emit a "no results" or "zero billing rows" error when the pre-launch check fires. The catalog is the authoritative source when billing data is absent.

---

### Step A2a — NES Path (Catalog Lookup)

*Runs when NES coverage > 0%.*

**Pre-classification filter (required — runs before any `get_curated_offer` call):**

Before calling `get_curated_offer` on any `package_id` value from Step A2, classify each slug:

1. **CES term-alias IDs:** If the slug ends with `_NNNmo` or `_NNNyr` (underscore + digits + "mo"/"yr") — it is a CES merchandising alias. Exclude from `get_curated_offer` calls. Record as `CES term alias` in the Flags table. Do NOT count its order volume in NES% — recompute NES% after exclusion.

2. **Ghost IDs by prefix:**
   - If the slug starts with `nes-`:
     1. Call `get_curated_offer` with the raw slug (`nes-{slug}`) as-is. This confirms whether the prefixed form exists in catalog.
     2. If NOT FOUND: strip the prefix and call `get_curated_offer` again with the clean slug (`{slug}`). If the clean slug resolves, use it as the curated offer ID going forward.
     3. If the clean slug is also NOT FOUND: classify as Ghost ID.
     4. Record in the Flags table regardless of outcome (resolved or ghost) — see Flags row below.
   - If the slug starts with `offer-`: call `get_curated_offer` with the slug as-is. If NOT FOUND, classify as Ghost ID. Record as `Ghost ID` in the Flags table. Do NOT count its volume in NES% — recompute after exclusion.

3. **Known ghost list (treat identically to prefix-matched ghost IDs):** `nes-wss-tier0-nortonsmb-*`, `nes-wss-tier1-nortonsmb-*`, `nes-wss-tier2-nortonsmb-*`.

**NES% recalculation rule:** Recompute NES coverage % using only slugs that survived all three filters. If recalculated NES% drops to 0%, re-evaluate the branch decision and run the Vocab advisory + Pre-launch NES check before entering the CES chain.

**Flags table additions (append when applicable):**

| Flag | Detail |
|------|--------|
| nes- prefix detected | Raw slug from billing: `{nes-slug}`. Catalog called with raw slug → {NOT FOUND / FOUND}. {If NOT FOUND: Retried with clean slug `{clean-slug}` → {FOUND — using as curated offer ID / NOT FOUND — classified as ghost}.} |
| Ghost IDs found | `{list of ghost slugs}` — catalog lookup attempted and returned NOT FOUND; not countable as NES volume |
| CES term aliases found | `{list of alias slugs}` — excluded from NES volume; CES merchandising aliases encoding term overrides |

---

### Step A2a — Geometry Classification (Live Catalog Lookup)

*Runs for all slugs that survived the Pre-classification filter. Geometry is derived live from the catalog MCP response — no pre-classification file is used.*

**Free trial detection (slug-level pre-check — runs before any `get_curated_offer` call):**

Inspect each surviving slug before making catalog calls:
- Slug contains `FreeTrial` or `freetrial` (case-insensitive) → pre-flag as candidate free trial
- BPO fields (`trialDays`, `billingStartEvent`, `billingPeriod`) present in the subsequent `get_curated_offer` response → confirmed free trial

When confirmed: add a `Free Trial` row to the Flags table for that package_id. Both the slug-level and response-level signals are checked independently.

---

### Step A2a-SF — NES Slug Family Expansion

*Runs after Step A2a-PC (Package Catalog Pre-Check) and the Free trial detection pre-check, before the `get_curated_offer` calls. Applies only to the NES path (NES coverage > 0%, or GAP-042 trigger — see below). Does NOT run on the CES path.*

**Purpose:** Billing-confirmed champions (from `pf_id_package_details_v1`) are keyed on the exact PFID queried. Sibling bundles in the same product family — same base offer, same slug prefix, but serving a different term-length PFID — are invisible to the pre-flight unless they happen to share a PFID with the entry product. This step scans the full active catalog for the complete slug family and presents all variants to the analyst so the correct clone source can be selected based on desired component configuration, not just what appeared in billing.

**When this step runs:**

| Trigger condition | Action |
|---|---|
| One or more billing-confirmed slugs survived the Pre-classification filter | Run slug family expansion for each surviving slug. Standard path. |
| GAP-042 surface (NES% > 0% in surface vocab OR confirmed NES surface, but `pf_id_package_details_v1` returned zero rows for target PFID on this ITC) | Run slug family expansion as the **PRIMARY** discovery path. Billing pre-flight is structurally blind here. State: `GAP-042 ACTIVE: slug family expansion is primary — billing pipeline cannot surface NES rows for this ITC/PFID combination.` |
| Zero billing-confirmed slugs AND surface is not in GAP-042 condition | Skip this step. |

**GAP-042 detection rule (evaluate before running A2a-SF):**

All three conditions must be true:
1. The surface ITC appears in the SLP → Configure-Page Funnel Pairs table above.
2. `pf_id_package_details_v1` returned zero `package_id` rows for the target PFID on that ITC.
3. Either: (a) `surface_nes_ces` resolves to `NES` or `Mixed` in the surface vocabulary, OR (b) the direct traffic event fallback query (Step A1 above) returned one or more `nes-` prefixed slugs.

When GAP-042 fires, the slugs from the direct traffic event fallback query (with `nes-` prefix stripped) serve as the billing-confirmed anchor slugs for prefix extraction below.

---

**A. Prefix Extraction**

For each billing-confirmed anchor slug (or GAP-042 traffic-event slug, with `nes-` prefix stripped), extract the slug family prefix using this rule:

**Variant tokens that terminate the prefix** (stop extracting tokens when you hit one of these):
- `-ox` — OpenExchange / Titan email variant
- `-365` — Microsoft 365 email variant (including tokens matching `o365`, `365`, `i18no365`)
- `-ssl` — SSL component variant
- `-wss` — Website Security component variant
- `-xtra` — extended bundle variant
- `-atmp` — Annual Term Monthly Payment
- `-disc` / `-discount-` — discounted variant suffix
- `-norenew` — no-renewal variant
- `-freetrial` — free trial variant
- Any 8+ character uppercase-alphanumeric token (embedded discount code)

**Extraction procedure:**
1. Tokenize the slug on `-`.
2. Scan left to right. Stop at the first token that matches any variant token above.
3. The prefix is all tokens up to (but not including) the stop token, joined with `-`, plus a trailing `-`.

**Examples:**
- `cpanel-set-1-economy-ox` → stop at `-ox` → prefix = `cpanel-set-1-economy-`
- `cpanel-set-1-economy-ssl-365-wss-xtra` → stop at `-ssl` → prefix = `cpanel-set-1-economy-`
- `wordpress-o365-forever-ssl-deluxe` → stop at `-o365` (contains `365`) → prefix = `wordpress-`
- `wsb-vnext-tier3` → no variant tokens → prefix = `wsb-vnext-tier3-`

> **Note on `-365` detection:** Treat any token matching `o365`, `365`, or `i18no365` as a variant-token stop.

**Prefix floor:** The prefix must contain at least 3 characters before the trailing `-`. If extraction would produce a shorter prefix, skip expansion for that slug and note: `Slug {slug} — prefix too short for family scan; skipping expansion for this slug.`

---

**B. Catalog Family Scan**

```
get_curated_offers(datasource="catalog-curated-offers", active=true, limit=1200)
```

This call is idempotent within a run — if already made earlier in this execution, reuse the cached result. Do not make a second call.

For each extracted prefix, filter the returned slug list for all slugs that contain the prefix string. Collect the full set of family members across all anchor slugs. Deduplicate — if two anchor slugs produce the same prefix, merge their family member sets.

Record the family member count as `{F}`. All `{F}` members must be presented — never suppress.

---

**C. Component Structure Retrieval**

For each of the `{F}` family members, call in parallel:
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<family_member_slug>)
```

For each response, extract:
- `offerId` — the Offer Collection ID (if bundle geometry) or Offer ID (if standalone)
- Top-level `plan` field
- `prePurchaseKeyMap.offers[]` — component offer UUIDs (if bundle) — used for provisioning context only

Then, for each distinct `offerId`, call:
```
get_offer_collection_definition(datasource="catalog-offers", offerCollectionId=<offerId>)
```

**Component summary (sourced from `get_offer_collection_definition`.`offers[]` — NOT from `prePurchaseKeyMap`):**
From the `get_offer_collection_definition` response, use the `offers[]` array to determine ALL components in the collection (this includes components zero-priced via PRICE_OVERRIDE=0 policy and components with `configKeyValues` overrides, which do not appear in `prePurchaseKeyMap`). Map each UUID against the Known Reusable Component Offer UUIDs table. Format: `{N} components: {name1}, {name2}, ...`. Unlisted UUIDs → `unknown-{short_uuid}`. Standalone geometry (no `offers[]` entries): `Standalone — no components`.

**Term support check:** From `get_offer_collection_definition`, compare the analyst's target `product_term_num` against the `numberOfTerms` range in the collection schema:
- Range includes target → `Supports {N}-year via term parameter`
- Range excludes target → `Term-incompatible — collection does not support {N}-year`
- Field absent → `Term schema not found — confirm with ecomm`

**Billing confirmation status:** A family member is `Billing-confirmed` if its slug appeared as a non-null `package_id` in Step A1 billing results for the target PFID. Otherwise: `Catalog family — billing unconfirmed for PFID {target_pfid}`. When GAP-042 is active: `GAP-042 confirmed (traffic events)` for traffic-sourced slugs; `Catalog family — billing unconfirmed (GAP-042 active)` for all others.

---

**D. Family Table Output**

Render immediately before the `For every distinct non-null package_id` block. Part of default Quick Reference output — do not suppress.

```
CATALOG FAMILY — {prefix}* ({F} members found across {N_anchor} anchor slug(s))
```

| Slug | Offer Collection ID | Components | Term Support | Billing Status |
|------|---------------------|------------|--------------|----------------|
| `{slug}` | `{offerId}` | `{N} components: name1, name2, ...` | Supports {N}-year via term parameter | Billing-confirmed |

Column rules:
- **Slug** — full curated offer slug, inline code
- **Offer Collection ID** — `offerId` UUID from `get_curated_offer`. If NOT FOUND: `NOT FOUND — ghost or inactive` (exclude from active family count and note: `{slug} returned NOT FOUND — excluded from active family count.`)
- **Components** — compact summary sourced from `get_offer_collection_definition`.`offers[]`. Standalone: `Standalone — no components`. Zero components: `Bundle — 0 components (check offers[])`
- **Term Support** — derived from collection schema check
- **Billing Status** — per rules above

One row per family member. All `{F}` rows must appear. Never suppress a row.

---

**E. Analyst Selection Instruction**

Always emit after the Catalog Family table:

```
ANALYST ACTION REQUIRED — Select Clone Source
The table above shows all active members of the {prefix}* offer family.

To select the correct clone source:
  1. Identify the row whose Components column matches the desired bundle configuration
     (e.g. if the new offer should include SSL + M365 + Website Security, select the slug
     that shows those 3 components).
  2. Verify the Term Support column confirms the target term is supported by that collection.
     If the collection supports the target term as a runtime parameter (numberOfTerms schema),
     a separate clone for the target term may not be needed — ecomm can wire the existing
     collection with term={N}.
  3. Rows labeled "Catalog family — billing unconfirmed" are valid catalog offers but have not
     been confirmed as live for the target PFID in billing data. Ecomm should verify before
     finalizing.

Confirm your selection and I will proceed with the full catalog resolution using the selected slug.
```

**Execution pause rule:** After rendering the Catalog Family table and Analyst Action Required block, pause and wait for the analyst's selection before running `get_curated_offer` on the selected slug. Do not auto-select based on component count, billing volume, or slug naming convention.

**Exception — single billing-confirmed slug:** If the Catalog Family table contains exactly one `Billing-confirmed` row AND the analyst's request stated no specific component configuration preference, do not pause. Proceed with that slug and note: `Auto-selected: {slug} — sole billing-confirmed family member; no component preference stated. Confirm this is the intended clone source.`

---

**F. Execution After Selection**

Once the analyst confirms a slug (or the auto-selection rule fires), treat that slug as the billing-confirmed champion for all subsequent steps. Proceed to the `For every distinct non-null package_id` block as normal.

If the analyst selects a `Catalog family — billing unconfirmed` slug, annotate the Champion line in the Quick Reference:

```
Champion (clone from this)  :  {selected_slug}
                               (source: catalog family — billing unconfirmed for PFID {target_pfid}; analyst-selected from slug family expansion)
```

This label persists through the Quick Reference output and Ticket Preview.

---

**G. Flags Table Additions**

| Flag | Detail |
|------|--------|
| Slug family expanded | Prefix `{prefix}*` yielded `{F}` active catalog family members. Analyst selected `{selected_slug}` as clone source. {If billing-unconfirmed: "Note: selected slug is billing-unconfirmed for PFID {target_pfid} — analyst confirmed selection."} |
| GAP-042 slug family primary | Surface `{ITC}` has a known pipeline gap (GAP-042). Billing pre-flight returned zero NES rows. Slug family expansion ran as primary NES discovery path using slugs from direct traffic events. |
| Collection supports multi-term | Collection `{offerId}` supports `numberOfTerms: [{range}]`. A new clone for term `{N}` may be unnecessary — ecomm can wire the existing collection with `term: {termType: YEAR, numberOfTerms: {N}}`. Confirm with ecomm before requesting a net-new clone. |

---

For **every distinct non-null `package_id`** from Step A2, run all calls in parallel:

**Step 1 — get the curated offer definition:**
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<package_id>)
```

**Immediately record the top-level `plan` field from the response** (e.g. `deluxeSslOfficebusinessps`, `deluxeSslStartup`). Store it as `collection_plan` in the working state for this package. This field is present regardless of geometry. Do not discard it — it is the plan engineers use at the collection level for cloning operations.

**Immediately classify the offer type from the response:**
- `prePurchaseKeyMap` absent or `prePurchaseKeyMap.offers[]` empty → **Standalone Offer**
- `prePurchaseKeyMap.offers[]` has one or more entries → **Offer Collection**

State this classification explicitly in output before any other catalog detail.

**Unexpected Offer Collection ID rule:** If the response classifies as **Standalone** (no `prePurchaseKeyMap` entries) but the `offerId` field is present AND also appears as a key in an `offerCollections` or equivalent top-level structure in the response, OR if any downstream call (`get_offer_collection_definition`) returns a non-empty `offers[]` array for what the `get_curated_offer` response indicated was a standalone — do NOT silently ignore it. Surface it immediately with this block, inserted as the first item after the geometry classification line:

```
UNEXPECTED: Offer Collection ID found on what appears to be a standalone offer.
  Offer Collection ID : [value]
  This may indicate a structural gap in the NES offer configuration.
  Verify with ecomm engineering whether this collection is intentional.
```

Do not let this block suppress the rest of the output. Continue rendering the Quick Reference and Flags table as normal — the UNEXPECTED block is an additive annotation, not a halt condition.

---

**Step 2 — classify offer geometry from the Step 1 response, then look up the appropriate IDs:**

The `get_curated_offer` response determines geometry. Apply this rule before making any further calls:

| What the response contains | Geometry | What to look up next |
|---|---|---|
| `offerId` field present AND `prePurchaseKeyMap.offers[]` absent or empty | **Standalone Offer** | Call `get_offer_collection_definition` using `offerId`. Record `name`, `tags[]`, `plan` — the plan is authoritative for standalones. Always emit `Offer Collection ID : Not available` in output. If the `get_offer_collection_definition` response contains a non-empty `offers[]` array, emit the UNEXPECTED block (see above). |
| `offerId` field present AND `prePurchaseKeyMap.offers[]` has one or more entries | **Offer Collection** | The top-level `plan` field from `get_curated_offer` is the collection-level plan — already recorded as `collection_plan` in Step 1. It is authoritative for the collection wrapper and must appear in output. Call `get_offer_collection_definition` using `offerId` (this is the Base Offer / primary product). Then call `get_offer_definition_by_id` for each component in parallel (Step 3). |
| `offerId` field present AND response contains `offerIds[]` array instead of `prePurchaseKeyMap` | **Offer Collection (V3 API pattern)** | Component resolution is not possible via this response format. Record the raw `offerIds[]` values. Flag as `Bundle — components not resolvable (V3 API pattern)` in the Flags table. Do not attempt `get_offer_definition_by_id` calls for this slug. Surface the raw IDs to the analyst so ecomm can resolve component details manually. |
| Neither `offerId` nor `prePurchaseKeyMap` present | **Unresolvable** | Note as BLOCKING: "Catalog response contained no offerId — cannot identify Base Offer or components. Ecomm must resolve manually." |

State the geometry classification explicitly in output — "Standalone Offer" or "Offer Collection (N components)" — as the first line after the catalog block, before any field values.

```
get_offer_collection_definition(datasource="catalog-offers", offerCollectionId=<offerId from get_curated_offer>)
```

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

**Free component checkpoint (mandatory — runs after ALL component lookups above):**

After resolving every entry in `prePurchaseKeyMap.offers[]` AND every entry in `offers[]` from `get_offer_collection_definition`, inspect all resolved components for free-purchaseType entries. This step is mandatory because free components have zero billing revenue and will never appear in any billing query — they are invisible to billing-first discovery and must be identified via the catalog alone.

For each resolved component (from either `prePurchaseKeyMap.offers[]` or `offers[]`), check whether any of the following apply:
- `purchaseType = "Free"` or `purchaseType = "FREEACCOUNT"`
- `FREEACCOUNT = true` in `configKeyValues` or similar flag
- Price is zero across all markets in the catalog response

If any such entry is found:
1. Add its PFID(s) to the **PFIDs on Surface** list in the Quick Reference block with the label: `{pfid} ({product_name}) — Free addon (purchaseType=Free; zero billing revenue — not discoverable via billing data)`
2. Include it in the CES Package Request Payload PFID table with `purchaseType` and `autoRenewal` values from the catalog response
3. Do NOT omit it because billing data shows zero orders or zero revenue for it — that is expected for free addons

Failure to include a free-purchaseType PFID produces an incomplete ecomm ticket. This is a hard rule with no exceptions.

Do this for every distinct package_id, not just the highest-volume one. If 3 package_ids are active, make all catalog calls and present all 3 results side by side.

---

### Step A2b — CES Merchandising Lookup

*Runs only when NES coverage = 0%.*

The goal is to find CES package slugs from the merchandising API whose `pfids[]` match the surface PFIDs from Step A1.

**Catalog-era product routing — STOP check (must confirm negative before proceeding):**

Before issuing any WebFetch call, confirm that the target product is NOT a catalog-era category. Catalog-era products must never reach Step 1.

To confirm catalog-era status, inspect two sources:
1. The target product name from the original request.
2. The PFID label strings from Step A1 (e.g. `product_name` values from billing — strings containing "Microsoft 365", "Titan Email", "Professional Email", "Partner Email", "Email Essentials"). For PFID-first inputs where the product name is not resolved until Step A1 runs, this check must be deferred until after Step A1 completes — do not skip it.

**If either source indicates a catalog-era category** — defined as any product whose Chain Step 3 tag would be `["m365"]`, `["titanemail"]`, or `["professional-email", "partneremail"]` (i.e., M365, Email Essentials, Titan Email, Professional Email, Partner Email) — **STOP. Do not issue the Step 1 fetch.** Proceed directly to Chain Step 2 and record in the chain narrative:
> "Merchandising API skipped — catalog-era {product_category} product. Chain Step 2 is primary."

The `/v1/packages` endpoint does NOT contain entries for catalog-era products. Running it produces an expected no-match that would be misread as ambiguous, requiring a redundant chain step. Skipping avoids two wasted calls with no information gain.

For legacy products (pre-NES WAM/WSB, legacy hosting, SSL, domains): catalog-era status is confirmed negative — proceed to Step 1.

**Step 1 — Fetch all CES packages:**

> **HARD CONSTRAINT — pre-call checklist. All three conditions must be true before issuing the WebFetch call. If any condition fails, do not call.**
> 1. Catalog-era status confirmed negative (product is not M365, Titan Email, Professional Email, Partner Email, or Email Essentials — per both the request product name and Step A1 PFID label strings).
> 2. The URL `https://merchandising.api.godaddy.com/v1/packages` has NOT already been called in this run.
> 3. Understood: any result from this call — truncated, summary, or empty — means proceed immediately to Chain Step 2. There is no retry path.

```
WebFetch https://merchandising.api.godaddy.com/v1/packages
```
Returns a JSON array. Key fields per object:
- `id` — the CES package slug (e.g. `wordpress-basic-ssl-1yr`)
- `description` — human-readable label
- `packageType` — e.g. `Standard`, `Premium`
- `productPackage.products[].pfids[]` — PFIDs included in the primary products
- `productPackage.addons[]` — optional add-on groups (elective, not wired at checkout)

Truncation is expected: the `/v1/packages` endpoint returns 200+ packages and WebFetch will routinely truncate the response. Truncation is not an error. The unverified truncated portion cannot be confirmed, but this is acceptable — the merchandising API PFID match (direct catalog tool calls) is the authoritative source for package composition. WebFetch is a secondary check only.

**On a summary-style response** ("no matches found", "I searched the packages", "none of the packages contain"): treat as ambiguous — NOT a confirmed no-match. WebFetch may have summarized rather than parsed the JSON. Proceed immediately to Chain Step 2 and record in the chain narrative: "Merchandising API result was ambiguous — WebFetch may have summarized the response. Chain Step 2 run as primary. No-match cannot be confirmed from WebFetch alone."

**On a truncated response with no PFID match in the visible content:** treat as "no merchandising match found — expected for catalog-era products or incomplete response." Proceed immediately to Chain Step 2 and record: "Merchandising API — no PFID match in visible content; response truncated. Chain Step 2 run as fallback. Confirm no-match independently if champion identification is critical."

**On a clean response with one or more PFID matches:** proceed to the Step 2 match classification below.

If the API call fails (HTTP error or empty array), note this in the CES chain narrative and go directly to Step A2c Chain Step 2.

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

**CES free-trial component check (required after Step A2b merchandising match, when one or more matches were found):**

After identifying matched packages from the merchandising API, inspect the matched package's `pfids[]` array for any PFIDs that are NOT present in the Step A1 billing results. For any such PFID:
1. Attempt to look up the PFID in `get_offer_definition_by_id` or note it as a candidate free-trial component.
2. If the PFID resolves to `purchaseType=Free` or `purchaseType=FREEACCOUNT` in the catalog, OR if `receipt_price_usd_amt` = 0 in any billing rows for this PFID, add it to the PFID list with the annotation: `{pfid} ({product_name}) — Free addon (purchaseType=Free; zero billing revenue — not discoverable via billing data)`.
3. Include it in the CES Terminal Payload PFID table.
4. Do NOT omit it because billing data shows zero orders or zero revenue — that is expected for free addons.

This mirrors the NES free component checkpoint in Step A2a. A missing free-trial PFID produces an incomplete ecomm ticket on both the NES and CES paths.

**Branch decision after Step A2b:**

| Outcome | Action |
|---|---|
| One exact match | A2c Chain Step 1 — this package is the primary candidate |
| One or more superset matches (no exact) | A2c Chain Step 1 — smallest-superset as primary; flag extras |
| Only partial matches | A2c Chain Step 1 — best partial as primary; mark output BLOCKING — ecomm must confirm scope |
| No matches at all | Skip A2c Chain Step 1; go directly to A2c Chain Step 2 |

**slp_wsb_* Surface Champion Filter (required — evaluate before passing any slug to Chain Step 1):**

When the surface ITC matches `slp_wsb_*` AND the best-match package slug from Step A2b is `vnext-i18nox-*` — apply this filter before calling `get_curated_offer` in Chain Step 1:

1. **Check for a wsb-vnext-* sibling in the full match set.** Inspect ALL matched package slugs from the A2b Merchandising Match table (not just the best-match). If any slug in the match set begins with `wsb-vnext-`, select that slug as the primary candidate instead. Replace the `vnext-i18nox-*` slug as the input to Chain Step 1. Note in the Chain narrative: "slp_wsb_* surface — wsb-vnext-* candidate preferred over vnext-i18nox-* per surface champion filter."

2. **If no wsb-vnext-* candidate exists in the full match set.** Do NOT promote the `vnext-i18nox-*` slug to Chain Step 1. Instead, skip Chain Step 1 entirely for this slug and go directly to Chain Step 2. Add this disclosure to the CES header section before any candidate table:

   ```
   AMBIGUOUS CHAMPION — vnext-i18nox-* on slp_wsb_* surface
     Surface          : {ITC}
     Slug returned    : {vnext-i18nox-* slug}
     Issue            : vnext-i18nox-* is the Titan Email / international series. slp_wsb_* is a US/global FOS surface. The correct US champion is wsb-vnext-*, but no wsb-vnext-* match was found in the merchandising API for this PFID.
     Action           : Proceeding to Chain Step 2 (ID scan). If Chain Step 2 also returns only vnext-i18nox-* candidates, confirm with ecomm whether the US wsb-vnext-* series has been deprecated for this PFID or whether the merchandising API data is stale.
   ```

3. **DEM locale exception — this filter does NOT fire when the ITC is a DEM locale variant.** Evaluate the DEM exception before applying steps 1 and 2 above. The ITC is a DEM locale variant when it matches any of: `slp_wsb_ca_*`, `slp_wsb_au_*`, `slp_wsb_gb_*`, `slp_wsb_uk_*`. If the ITC matches a DEM locale pattern, `vnext-i18nox-*` is a valid candidate. Do NOT suppress it. Proceed to Chain Step 1 as normal. The filter applies only to non-locale `slp_wsb_*` ITCs (i.e., those that do NOT have a `_ca_`, `_au_`, `_gb_`, or `_uk_` token immediately following `slp_wsb_`).

This filter is narrowly scoped: it fires only when BOTH conditions are true simultaneously — (a) slug family is `vnext-i18nox-*` AND (b) surface prefix is `slp_wsb_` without a DEM locale token. It does not affect DPP, UPP, DLP, international ITCs, or any other slug family.

---

### Step A2c — CES Offer ID Resolution

*Runs when NES coverage = 0%. Execute in chain order — stop at the first step that returns a result.*

---

**Chain Step 1 — Merchandising slug → curated offer** *(only if A2b found a match)*

Take the best-match package slug from A2b. Attempt:
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<package_slug>)
```
- **Success:** Catalog recognizes this slug as a curated offer. Record the offer. Apply the same Standalone / Offer Collection classification as Step A2a.

  **NES-vs-CES validity check (required before treating Chain Step 1 as resolved — CES path only):** This check fires when the current route is CES (the surface is 100% CES — billing returned all-null `package_id` values for this ITC). When `get_curated_offer` returns active for the A2b merchandising match slug, confirm that the slug was present in the A2b Merchandising Match table as a PFID match for the target PFIDs on this surface. If the slug was NOT found in the A2b Merchandising Match table (i.e., the merchandising API did not associate this slug with the surface PFIDs), the slug is an NES-only offer — it exists in the NES catalog but has no merchandising presence for these PFIDs on this CES surface. In that case:

  1. Do NOT treat the chain as resolved. Do NOT populate `Existing CES Package: Confirmed — {slug}`.
  2. Emit a labeled NES reference block immediately in the CES header section (before the Candidate table):
     ```
     NES reference found       :  {slug}
     Offer ID                  :  {offerId from get_curated_offer}
     Plan                      :  {plan from get_curated_offer}
     Validity                  :  NOT a valid CES clone source — NES-only offer; absent from merchandising API for these PFIDs on this surface
     ```
  3. Set `Existing CES Package: Not found (NET-NEW BUILD required)` in the CES Terminal Payload.
  4. Proceed to Chain Step 2. If Chain Step 2 also returns no valid CES matches, proceed to the NET-NEW BUILD block.

  If the slug WAS present in the A2b Merchandising Match table for the target PFIDs, the NES-vs-CES check passes — proceed normally.

  This check does NOT apply on the NES path (surface has non-null `package_id` values in billing). On the NES path, `get_curated_offer` success in Chain Step 1 resolves the chain as normal.

  **Dual-series continuation check (required before stopping):** Before treating this as "chain resolved," inspect the matched package slug's prefix family. If the slug belongs to a known dual-series family — that is, the same PFID is known to appear in packages from at least two distinct slug-prefix families (e.g. `wsb-vnext-*` and `vnext-i18nox-*`) — do NOT stop here. Continue to Chain Step 2 to determine whether the sibling series also has a candidate for this PFID on this surface. Apply the Series Disambiguation rule (see "Series Disambiguation" block below). Only treat the chain as resolved once Chain Step 2 has confirmed whether a sibling series is present or absent.

  If the slug does not belong to a known dual-series family, the chain is resolved. Do not continue to Chain Step 2 unless a different failure condition applies.

- **Not found:** Proceed to Chain Step 2.

---

**Chain Step 2 — ID list scan + keyword match**

Pull all active curated offer IDs:
```
get_curated_offers(datasource="catalog-curated-offers", active=true, limit=1200)
```

Derive keywords from ALL of the following sources:
1. The target product name or SKU (e.g. "MWP Basic" → `mwp`, `basic`, `wordpress`)
2. The surface ITC string (e.g. `slp_wordpress` → `wordpress`)
3. PFID labels from Step A1 results (e.g. PFID 1320706 = "Deluxe Managed Hosting" → `deluxe`)
4. **Surface keyword seed table (mandatory — use ALL seeds for the surface pattern, not just the ITC tokens):**

   | Surface / ITC pattern | Required keyword seeds |
   |---|---|
   | `dpp_precheck` or `dpp_%` | `precheck`, `dpp`, `wsb`, `vnext`, `wam`, `i18n`, `m365`, `solutionset` |
   | `slp_wsb_%` or `slp_wordpress` | `wsb`, `vnext`, `wordpress`, `wam`, `i18n`, `i18nox` |
   | `slp_hosting_%` or `slp_rstdstore` | `hosting`, `mwp`, `wordpress`, `ssl`, `deluxe`, `basic` |
   | `upp_%` | `upp`, `upsell`, plus entry product name keywords |
   | `mgr_%` | `mgr`, plus entry product name keywords |
   | `slp_hosting_4gh` | `hosting`, `wordpress`, `ssl`, `mwp`, `o365`, `openexchange`, `deluxe`, `basic` |
   | Other surfaces | ITC slug tokens only — add product-family keywords if A1 billing revealed product families |

   This is the same seed table used in Step M1 (Modify mode). The seed requirement applies equally to Create/Clone mode. ITC-token seeds alone (e.g. "dpp", "precheck") are insufficient for surfaces that host multiple product families. An incomplete seed list produces a candidate table that misses live packages on the surface.

Score matches on ANY of the surface's required keywords. A surface like `dpp_precheck` requires all 8 keyword seeds to be tested — do not limit scoring to the highest-frequency token.

For each curated offer ID in the list, keyword-match against the ID slug string. Collect all matching IDs. **Before making any `get_curated_offer` calls: record the raw match count as `{M}`.** This count is committed at this point and cannot change. Call `get_curated_offer` for all `{M}` matched slugs in parallel.

**Merchandising validation check (required before declaring Chain Step 2 success):**

This check fires when: A2b ran AND A2b returned zero merchandising matches for the target PFIDs on this surface.

For each slug in the `{M}` matched candidates, check whether it appeared as a match in the Step A2b Merchandising Match table. If a slug was NOT present in the A2b Merchandising Match table, AND A2b returned zero matches for the target PFIDs on this surface, mark that slug:

> `DISQUALIFIED (NES-only) — absent from merchandising API for these PFIDs; not a valid CES clone source`

- The slug must still appear as a row in the Section 4 Candidate table, with `DISQUALIFIED (NES-only)` in the Selected column. Do not suppress it.
- Do not select a disqualified slug as the Chain Step 2 champion.
- Do not count a disqualified slug toward "Chain resolved."

If ALL `{M}` candidates are disqualified as NES-only: Chain Step 2 has no valid CES matches. Proceed to Chain Step 3. Do not emit a Quick Reference block using a disqualified slug.

This check does NOT fire when:
- A2b was skipped (catalog-era routing was taken instead)
- A2b did find matches for the target PFIDs (in that case, use the A2b match as primary; any additional Chain Step 2 slugs absent from A2b are listed as supplementary, not disqualified)

- **Success (one or more offers found whose PFID coverage matches the surface, and at least one candidate passes the merchandising validation check above):** Chain resolved. Apply Standalone / Offer Collection classification.

**Free PFID recovery (required when Chain Step 2 succeeds AND the champion slug was absent from the A2b Merchandising Match table):**

After `get_curated_offer` returns for the Chain Step 2 champion, attempt a targeted merchandising lookup for that specific slug:
```
WebFetch https://merchandising.api.godaddy.com/v1/packages/{champion_slug}
```
- **If the package exists:** extract its complete `pfids[]` and `addons[]` arrays. Apply the CES free-trial component check: for any PFID in `pfids[]` not present in the Step A1 billing results (or present with avg receipt price = 0), add it to the PFID list with the annotation: `{pfid} ({product_name}) — Free addon (purchaseType=Free; zero billing revenue — not discoverable via billing data)`.
- **If the slug is not in the merchandising API (404 or empty):** this is expected for catalog-era products (M365, Titan Email, Email Essentials). In this case, inspect the Step A1 billing results for any PFIDs with `avg_receipt_price = 0` or zero order rows and annotate those as candidate free addons. Add a BLOCKING note: "Catalog-era product — `/v1/packages` has no entry for `{champion_slug}`. Free add-on PFIDs cannot be confirmed from merchandising data. Verify the complete PFID list (including free components) with ecomm before filing."
- **Do not skip this step.** A CES payload without free addon PFIDs produces an incomplete engineering ticket.

- **No matches:** Proceed to Chain Step 3.

**All-M-shown rule (mandatory):** When Chain Step 2 runs, the number of rows in the Section 4 Candidate table must equal the number of keyword matches `{M}` reported in the Section 3 chain narrative. Every match must appear as a row — not just the "cleanest" or highest-confidence candidates. Many-to-1 relationships are common: multiple curated offer slugs (Norton bundles, AES variants, backup bundles, `temp-` variants, regional variants, ATMP contracts) can all be valid configurations for the same product. The analyst — not the skill — decides which slug is the correct champion.

**Series-split rule (mandatory — runs after all-M candidates are collected):** After collecting all `{M}` candidate slugs, inspect the set for entries from two or more distinct slug-prefix series families. Apply the Series Disambiguation rule (see "Series Disambiguation" block below) to determine whether multiple series are present and represent different product configurations. If they do:
- Do NOT emit a single Quick Reference champion block with all candidates. Instead, emit SEPARATE champion blocks — one per distinct series — each with its own `=== {series_label} ===` header and its own Champion line.
- Add a MULTI-SERIES SURFACE disclosure before the champion blocks:

  > "MULTI-SERIES SURFACE — `{N}` product-series families detected for this PFID on this surface: `{series-1 label}` ({N1} candidates) and `{series-2 label}` ({N2} candidates). These series represent different product configurations (see series labels below). A separate Quick Reference block is emitted for each series. Select the correct series based on market scope and email product before filing."

- Each series block uses its own champion (the highest-volume or best-matching slug within that series). The Candidate table (Section 4) still shows all `{M}` rows — grouped by series, with a `Series` column added.
- This rule fires only when multi-series presence is detected. Single-series runs are unaffected — no additional disclosure, no extra blocks.

Disclosure template for ID scan (add to CES header section):
> "Found `{M}` keyword matches by scanning `{N}` curated offer IDs from `get_curated_offers` for keywords `{keyword list}`. Showing all `{M}` candidates below — none suppressed at model discretion. If filtering was applied for any reason (hard lookup failure only), state the count and reason explicitly: 'Showing `{shown}` of `{M}` — `{omitted}` omitted due to: `{reason}`.'"

After any Chain Step 2 success, still run Chain Step 3 as a secondary validation to confirm no additional plan variants exist. Render the full candidate table from both steps.

**WebFetch / ID scan reconciliation (required whenever both A2b and Chain Step 2 ran):** After Chain Step 2 returns results, compare its candidates against the Step A2b Merchandising Match table. For every Chain Step 2 candidate whose slug was NOT present as a match in the A2b table, add a note to the Chain narrative (Section 3 of CES Output Disclosure) and to the Candidate table's Selected column:

> "Found via ID scan — absent from merchandising match table. WebFetch may have returned incomplete results. Confirm no-match independently."

Do not treat the A2b result as authoritative when Chain Step 2 finds offers not present there. The discrepancy is itself evidence that the WebFetch response may have been truncated or summarized. Surface it explicitly; do not resolve it by silently deferring to one source.

---

**Chain Step 3 — Tag-based search**

**Known-tag product mapping (check before running this step sequentially):**

The following product name → catalog tag mappings are stable and confirmed. When the request names one of these products, trigger Chain Step 3 IN PARALLEL with Chain Step 2 — do not wait for Chain Step 2 to exhaust first. This is the primary resolution path for these catalog-native products.

| Product name signals | Also recognized as | Catalog tags | Notes |
|---|---|---|---|
| "Microsoft 365", "M365", "o365", "Office 365" | "o365", "Microsoft email", "365 email", "o365 component", "m365 email essentials", "online essentials" | `["m365"]` | Returns 124+ plans; filter by plan name keywords |
| "Titan Email", "Titan", "i18n email", "i18nox" | "i18n email", "i18nox email", "international email", "OX email", "titan light", "titan pro" | `["titanemail"]` | International email product |
| "SSL", "SSL Certificate" | "secure site", "site seal", "DV SSL", "OV SSL", "EV SSL", "deluxe SSL", "dlxssl" | `["sslcert"]` | |
| "WAM", "Websites and Marketing", "WSB" | "wsb", "website builder", "vnext", "wsb-vnext", "design studio" | `["wam", "wsb"]` | |
| "Professional Email", "Partner Email" | "pro email", "partneremail" | `["professional-email", "partneremail"]` | |

When a product name matches a known-tag entry: run `catalog_query_get_offers` with those tags in parallel with Chain Step 2, regardless of whether Step 2 has returned results yet. Record both runs and reconcile the candidates in the Section 4 Candidate table.

**Plan-attribute keyword filtering (required when the tag search returns many plans):**

When `catalog_query_get_offers` returns a large plan set (e.g. 124 M365 plans), extract keyword attributes from the request (e.g. "Online Essentials w/o Teams" → keywords: `online`, `essentials`, `noteams`, `noteam`). Filter the returned `plans[]` by matching those keywords against the plan name string (case-insensitive). Show all plans that match at least one keyword. If no plan name matches any keyword, show the top 10 plans by volume (if available) and add a BLOCKING note: "Plan name filter returned zero matches — analyst must confirm the correct plan from the full list."

**Fallback (when no known-tag entry matches the product name):**

Derive product type tags from the surface PFIDs and product names (e.g. `hosting` from MWP, `m365` from Microsoft products, `ssl` from SSL PFIDs). Run:
```
catalog_query_get_offers(
    datasource="catalog-query",
    currency=<from request or default US/USD>,
    marketId=<from request or default US>,
    tags=[<derived product type tags>]
)
```

Filter the returned `plans[]` for keyword matches on the plan name field. For each matched plan, extract `offerId` from `instance.uri` (last path segment after `/offers/`) and call `get_offer_definition_by_id` in parallel.

- **Success:** Chain resolved via tag search. No curated offer slug is available from this path. The output must include a BLOCKING line: "Found via tag search only — no curated offer slug exists. Ecomm must create a new curated offer and wire this offer ID."
- **No matches:** Chain exhausted.

---

**If all chain steps fail:**

Do not emit a Quick Reference block with "Not found" values. Instead, emit a dedicated NET-NEW BUILD block:

```
=== NET-NEW BUILD REQUIRED ===
Champion (clone from this)  :  None — no existing offer found
                               (source: merchandising API, ID scan, and tag search all exhausted)

Action Required             :  Ecomm must build this offer from scratch — no clone source available
PFIDs to cover              :  {pfid_list from Step A1, with product_name for each}
Terms observed              :  {all distinct term_num + term_unit_desc from Step A1}
Volume (7d)                 :  {SUM(total_orders) from Step A1 — all CES}
BLOCKING                    :  No champion identified — ecomm must create a net-new curated offer. Provide PFID list and confirm scope before filing.
```

This replaces ambiguous "Not found" column values with an explicit state the engineer can act on.

---

### Series Disambiguation

*This rule is referenced from Chain Step 1 (dual-series continuation check), Chain Step 2 (series-split rule), and Step M1 (i18nox vs wsb-vnext check). Any change to this block applies to all three call sites.*

A **series** is a group of curated offer slugs sharing a common slug-prefix family (e.g. `wsb-vnext-*`, `vnext-i18nox-*`, `vnext-i18no365-*`). Two series require separate champion blocks when all three conditions hold:

1. **Shared PFID:** The same PFID appears in at least one package from each series (confirmed from merchandising API or billing data — not inferred from slug names alone).
2. **Different product configuration:** The series encode meaningfully different configurations — specifically: different email add-on product (M365 vs Titan Email vs none), or different geo-market scope (US/Global vs International/ROW), or different component UUIDs in `prePurchaseKeyMap`.
3. **Both active on the surface:** At least one package from each series is present in the candidate set for this surface.

When all three conditions hold, emit separate champion blocks and the MULTI-SERIES SURFACE disclosure (see Series-split rule in Chain Step 2). When fewer than three conditions hold — e.g. the PFID overlap is unconfirmed, or the series encode the same email product in the same geo — do not split; use the standard single-series output with an ambiguous-champion disclosure if needed.

**Known three-series family (confirmed 2026-05-14):**

| Series | Slug prefix | Geo scope | Email product | When to select |
|--------|-------------|-----------|---------------|----------------|
| US / M365 series | `wsb-vnext-tier{N}` | US / Global (English markets) | Microsoft 365 (`575a7d2a`) | US-only or English-market scope; or when market is global AND ticket specifies M365 |
| International M365 series | `vnext-i18no365-tier{N}` | International (non-English, M365-capable markets) | Microsoft 365 (`575a7d2a`) | International scope where M365 is available; `-365` suffix encodes M365 |
| International Titan series | `vnext-i18nox-tier{N}` | International (Titan Email markets — IN, developing markets) | Titan Email (`927a9d45`) | Non-English markets where M365 is unavailable; `-ox` suffix encodes Titan Email |

**Three-series BLOCKING rule:** When candidates from all three series are present for the same PFID (market scope = "all markets", "global", or unspecified), do NOT auto-select a champion. Emit three separate champion blocks (one per series) and add a BLOCKING line in each: "Three-series surface — confirm geo-split intent (US vs international-M365 vs international-Titan) with ecomm before filing." When market is US-only, select `wsb-vnext` and label the other two `market excluded: US scope`. When market is international-only, the analyst must confirm M365 vs Titan availability before selecting between `vnext-i18no365` and `vnext-i18nox`.

When the market scope is known, emit the matching series as the primary champion block and the others as secondary blocks labeled `{series label} — market excluded: {reason}`. When the market scope is unspecified or mixed, apply the Three-series BLOCKING rule above.

This table is extensible. When a new series sharing a PFID is confirmed, add a row here. Do not hardcode series names anywhere else in the skill — all series-specific logic routes through this block.

---

### Path A — Modify Mode (Add Component to Existing Offer)

*Runs when Offer Operation = Modify — Add Component. Does NOT run the standard Create/Clone chain (Steps A2a/A2b/A2c) for the existing packages. Replaces Steps A1 through A2c entirely.*

---

**Step M1 — Identify packages currently on the target surface**

Goal: find which `package_id` values are currently active on this surface. The new product being added is irrelevant here — you are discovering the existing bundles, not the entry product.

```sql
SELECT DISTINCT
    package_id,
    item_tracking_code  AS itc,
    SUM(total_orders)   AS total_orders_7d
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE item_tracking_code = '{ITC}'          -- or LIKE pattern for surface category
  AND package_id IS NOT NULL
  AND bill_modified_mst_date >= DATEADD(day, -7, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY total_orders_7d DESC;
```

**Thin-result checkpoint (required before the ID scan):** If the billing query returns fewer than 3 distinct package IDs for a surface category known to carry multiple product families (e.g. `dpp_precheck`, any surface with `wsb`, `vnext`, or `slp_` in its name), pause before running the ID scan and ask the analyst:

> "The billing query returned only {N} package(s) for {ITC} in the last 7 days. This surface is expected to carry multiple product families. Are there additional product families (e.g. WAM, WSB, M365, Titan Email, i18n variants) I should include in the ID scan?"

Wait for the analyst's answer before proceeding. If the analyst confirms additional families, add their keyword terms to the seed list below. If the analyst says the count is expected, proceed with the existing package IDs only.

If the billing query returns no results at all, also scan `get_curated_offers(datasource="catalog-curated-offers", active=true, limit=1200)` using the keyword seeds below.

**ID scan keyword seed table — use ALL keywords for the surface ITC pattern, not just the ITC string itself:**

| Surface / ITC pattern | Required keyword seeds |
|---|---|
| `dpp_precheck` or `dpp_%` | `precheck`, `dpp`, `wsb`, `vnext`, `wam`, `i18n`, `m365`, `solutionset` |
| `slp_wsb_%` or `slp_wordpress` | `wsb`, `vnext`, `wordpress`, `wam`, `i18n`, `i18nox` |
| `slp_hosting_%` or `slp_rstdstore` | `hosting`, `mwp`, `wordpress`, `ssl`, `deluxe`, `basic` |
| `upp_%` | `upp`, `upsell`, plus entry product name keywords |
| `mgr_%` | `mgr`, plus entry product name keywords |
| Other surfaces | ITC slug tokens only — add keywords if thin-result checkpoint fires |

**Multi-series disambiguation (required when candidates from more than one slug-prefix series family appear):**

Apply the Series Disambiguation rule (see "Series Disambiguation" block above). That block is the single source of truth for all series-specific logic — the known dual-series family table, the three conditions that trigger separate champion blocks, and the market-scope selection rules are all there. Do not apply ad-hoc series selection logic here.

When running the ID scan: score matches on ANY of the surface's required keywords, not just the single highest-frequency token. A surface like `dpp_precheck` requires all 8 keyword seeds to be tested.

Include any slug matches as additional candidates.

Collect all discovered `package_id` values into a set: `{existing_packages}`.

---

**Step M2 — Look up each existing package**

For every `package_id` in `{existing_packages}`, run in parallel:
```
get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<package_id>)
```

For each result, record:
- `package_id` (slug)
- `offerId` — the Base Offer ID (from the `get_curated_offer` response)
- Offer type: Standalone (no `prePurchaseKeyMap`) or Offer Collection (`prePurchaseKeyMap` present)

**Do NOT call `get_offer_collection_definition` or `get_offer_definition_by_id` for existing components.** The existing bundle contents are irrelevant to the modification — only the package slug and Base Offer ID are needed.

---

**Step M3 — Check whether the new product has an existing curated offer**

Run the standard CES lookup chain (Steps A2b + A2c) scoped to the **new product being added** — not to the existing packages. The goal is to determine whether a standalone curated offer for the new product already exists.

- **Merchandising fetch (A2b logic):** WebFetch `https://merchandising.api.godaddy.com/v1/packages`, match the new product's PFID against `pfids[]` in each package, identify the best-matching slug.
- **ID list scan (A2c Chain Step 2):** Scan `get_curated_offers` for keyword matches on the new product name/ITC.
- **Tag search (A2c Chain Step 3):** If chain steps 1–2 fail, run `catalog_query_get_offers` with derived product tags.

Classify the outcome:
- **Offer exists:** a standalone curated offer for the new product was found. Record its `offerId`. The ticket is a one-step operation: add this `offerId` to each existing package's `prePurchaseKeyMap`.
- **No offer found:** the new product has no standalone curated offer. The ticket is a two-step operation: Step 1 = create new curated offer for the new product; Step 2 = add the new `offerId` to each package's `prePurchaseKeyMap`.

---

### CES Output Disclosure Requirements

*Required whenever Steps A2b and A2c ran (NES coverage = 0%). Render all sections in this order, before the Quick Reference blocks.*

**Section 1 — Header (required)**

```
SURFACE IS 100% CES — Candidate Identification Path

No billing package_id is present on this surface. The goal of this
section is to identify which CES package(s) this product most likely
belongs to — using PFID matching against the merchandising API and
keyword scanning of the offer catalog. This produces a candidate list
for ecomm to review and confirm, not a billing-confirmed match.
Treat the champion as the strongest available candidate for cloning —
validate with ecomm before filing the ticket.
```

This must appear as a visible, prominent block. A Flags table row alone is not sufficient.

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
- **Row count must equal M.** The number of rows in this table must equal the `{M}` matches reported in the Section 3 chain narrative for Chain Step 2. If the table shows fewer rows than M, add an explicit line at the top: "Showing `{shown}` of `{M}` — `{omitted}` omitted due to: `{hard lookup failure — offerId not found in catalog / API error}`. All remaining rows shown." No other reason justifies omitting a row.
- Show every matched plan — never suppress candidates. A row may only be omitted if `get_curated_offer` returned a hard error (not-found or API failure) for that slug; document such omissions explicitly with the error.
- Never infer that a candidate is a test artifact, staging entry, duplicate, or lower-priority variant based on any characteristic of the slug string, offer ID, discount code, volume, or any other implicit signal. That judgment belongs to the analyst, not the skill. If you would have suppressed a row for any reason other than a hard lookup failure, include it and add a note in the Selected column instead.
- **`temp-` prefix is not evidence of a test artifact.** Slugs like `temp-email-essentials-99`, `temp-email-essentials-149`, and any other `temp-` prefixed ID must be included in the Candidate table as production candidates without cautionary notes about the naming convention. The `temp-` prefix is used for legitimate live production champions (confirmed at dpp_precheck). Only add a Selected-column note when concrete evidence of a problem exists from the API response (inactive status, hard lookup failure) — never from the slug name alone.
- If multiple plans resolve to the same offer ID, include every row and note "same offer ID" in the Selected column of each — this is an annotation, not a reason to collapse rows.
- If multiple plans resolve to different offer IDs, do not pick one — show all and mark plan selection as BLOCKING.
- Mark the best match with ✓ and a one-word reason (e.g. "best match", "AES variant", "same offer ID").

Omit this section if the chain was fully exhausted with no candidates found at any step.


---

### Path A Output — Modify Mode

*Render this section when Offer Operation = Modify — Add Component. Do not render the Create/Clone Quick Reference blocks.*

**Render only after all work is complete:** after all Step M2 `get_curated_offer` calls and all Step M3 chain steps have returned.

Open with a Term Scope header (same rule as Create/Clone — see below).

---

**Existing Packages on Surface**

One row per discovered package. This table confirms the scope of the modification — no component detail.

| Package Slug | Base Offer ID | Offer Type | Orders (7d) |
|---|---|---|---|
| `{package_id}` | `{offerId}` | Standalone / Offer Collection | `{total_orders_7d}` |

---

**New Component Status**

State whether the new product's curated offer exists, in a single labeled record block:

```
=== New Component — {new_product_name} ===
Curated Offer Exists    :  Yes — {offerId} (source: {merchandising match | ID scan | tag search only})
                           -- or --
                           No — net-new curated offer required (see Step-by-Step below)

Offer Operation         :  Add as component to {N} existing package(s) on {ITC}
```

---

**Step-by-Step Ticket Structure**

When offer exists (one-step):

```
Step 1 — Add new component to existing packages
  For each package listed above:
  Add to prePurchaseKeyMap:
    offerId : {new component offerId}
    plan    : {plan — if known from M3 chain result; write "NOT SPECIFIED — ecomm must confirm" if absent}
```

When offer does not exist (two-step):

```
Step 1 — Create new standalone curated offer for {new_product_name}
  PFIDs       : {pfid_list from Step M3 / analyst input}
  Plan        : NOT SPECIFIED — ecomm must define
  Market      : {from request}

Step 2 — Add new offer to existing packages
  For each package listed above:
  Add to prePurchaseKeyMap:
    offerId : {new offerId — from Step 1, not yet known}
    plan    : NOT SPECIFIED — ecomm must confirm after Step 1
  BLOCKING: Step 2 cannot be filed until Step 1 creates the offer and returns its offerId.
```

---

Append a Flags table for any applicable conditions. Use the same flag format as the Create/Clone path. Omit entirely if no flags apply.

After the Flags table, append the standard post-output ticket preview prompt (see Post-Output section). The ticket preview for the Modify path uses the Ticket Preview — Path A (Modify — Add Component) format below.

---

### Path A Output — Create / Clone

**Render only after all work is complete.** For the NES path: after all `get_curated_offer`, `get_offer_collection_definition`, and `get_offer_definition_by_id` calls have returned. For the CES path: after the merchandising fetch, all chain steps, and all catalog calls that chain steps triggered have returned. Do not render any section of the output until every call is done.

**Always open Path A output with a Term Scope header — one line, before any blocks or disclosure sections:**

- Specific term: `TERM SCOPE: {N} {unit} (e.g. 1 Year)`
- Multiple terms: `TERM SCOPE: {N1} {unit1}, {N2} {unit2} (e.g. 1 Year, 2 Year)`
- All terms / not filtered: `TERM SCOPE: All terms — champion and PFID list are cross-term. Confirm with analyst before filing.`

**Default output is the Quick Reference only.** Do not render supporting detail unless the analyst asks with a phrase like "show me the full audit", "give me the detail", or "expand".

| Tier | When rendered | Content |
|------|--------------|---------|
| **Quick Reference** | Always, by default | One block per bundle — the complete ecomm payload |
| **Supporting Detail** | Only on request | Surface volume table + per-bundle catalog deep-dive |

---

**Quick Reference (always rendered)**

**Offers Being Replaced (conditional — emit before champion selection when applicable):** When entry was a Jira ticket and removal language was extracted (see Entry Option 1, step 2), emit this block immediately before the Quick Reference blocks:

```
OFFERS BEING REPLACED (from ticket):
  {verbatim removal description from ticket body}
  These offers should be marked "Being replaced" in the CES Terminal Payload Status column.
```

Omit this block entirely if no removal language was found in the ticket body.

**Champion selection rule:** Before emitting Quick Reference blocks, evaluate whether a single champion can be identified. The champion is the existing live offer that ecomm will clone or base the new request from. It must appear as the first, visually separated line of every block — not buried in the middle of the record.

- If exactly one non-null `package_id` is active on the surface → it is the champion. Emit one block.
- If two or more `package_id` values are simultaneously active → ambiguous champion state. Emit a disclosure immediately before the Quick Reference blocks that includes the volume for each candidate:

  > "AMBIGUOUS CHAMPION — {N} bundles active simultaneously on `{itc}`: `{slug-1}` ({N1} orders/7d), `{slug-2}` ({N2} orders/7d). Confirm which is the intended champion with ecomm before cloning."

  Then emit one block per bundle. Do not attempt to pick one.
- If no single champion can be determined for any other reason (partial matches only, ID scan but no merchandising confirmation, etc.) → state the reason explicitly in one sentence before the blocks. Do not silently pick the best guess.

---

Emit one block per distinct `package_id` (or per resolved offer on the CES path). Open each block with `=== {bundle_slug} ===`, then emit a labeled record block. Labels left-aligned, padded to match the longest label in the block. Values on the right of the colon.

**The Champion line is always first. It is separated from all other fields by a blank line.** This is the only field an ecomm engineer needs to file the ticket — it must be findable in under 5 seconds.

Fields in this order:

```
=== {bundle_slug} ===
Champion (clone from this)  :  {champion value — see rules below}
                               (source: {billing data | merchandising match | ID scan | tag search only | none found})
Offer Route                 :  NES Curated Offer  —or—  CES Package  (locked at Step A2)

{Geometry-aware ID fields — use EXACTLY ONE of the three blocks below, depending on what Step A2a returned:}

[IF STANDALONE — prePurchaseKeyMap absent or empty:]
Offer ID                    :  {offerId} from get_curated_offer
Plan                        :  {plan from get_offer_collection_definition — authoritative for standalones}
Offer Collection ID         :  Not available
{If the UNEXPECTED block fired for this bundle, insert it here, before the remaining fields.}

[IF OFFER COLLECTION — prePurchaseKeyMap.offers[] has entries:]
Offer Collection ID         :  {offerId} from get_curated_offer (this is also the Base Offer ID for the primary product)
Collection Plan             :  {plan} from get_curated_offer top-level field (collection-level plan for cloning operations)
Component 1 — {Name}        :  {offerId} / plan: {plan from prePurchaseKeyMap entry — or "NOT SPECIFIED — component inherits collection plan (see Collection Plan above)"}
Component 2 — {Name}        :  {offerId} / plan: {plan from prePurchaseKeyMap entry — or "NOT SPECIFIED — component inherits collection plan (see Collection Plan above)"}
*(one line per component in prePurchaseKeyMap.offers[])*

[IF NEITHER ID PRESENT — catalog unresolvable:]
BLOCKING                    :  Catalog response contained no offerId — Offer ID and Offer Collection ID both unknown. Ecomm must resolve manually before filing.

{Continue with remaining fields, always present:}
PFIDs on Surface            :  {pfid1} ({product_name}), {pfid2} ({product_name}), ...
Product Name(s)             :  {product_name(s) from Step A1 for PFIDs on this surface, or from intake prompt — leave blank if unavailable}
Price                       :  {avg_catalog_list_price / avg_catalog_sale_price from Step A1 per PFID × term, or target price from intake prompt — leave blank if unavailable}
Target Price (from ticket)  :  {price target extracted from Jira ticket body, e.g. "$3.99/mo", "80% off list" — omit line if entry was not a Jira ticket or no price target was stated}
Surface(s)                  :  {all ITCs from Step A1 where this bundle is active — for the primary ITC, append surface label if resolved: e.g. "dpp_precheck (Domain Purchase Path — Pre-Check) | CES"}
Regions                     :  {bill_country_code / region_name from Step A1 billing data, or from intake prompt — leave blank if unavailable}
Term                        :  {product_term_num} {product_term_unit_desc} — list all observed values (e.g. "1 Year, 2 Year, 3 Year")
BPO / Trial                 :  {value from get_curated_offer response — omit line if not present in response}
Cart Renewal Behavior       :  {value from get_curated_offer response — omit line if not present in response}
Geo Scope                   :  {markets from request}
Discount                    :  {item_discount_code} from billing. UUID placeholder → "None (UUID placeholder)". Real code → write verbatim. Omit only if item_discount_code is null for every row for this bundle on this surface.
Discount (from ticket)      :  {discount code extracted from Jira ticket body or linked PRICING ticket — omit line if entry was not a Jira ticket or no code was stated; if a PRICING ticket was referenced, note it: "{code} (see {PRICING-XXXXX})"}
Customer Segment            :  New / existing / both
Offer Lever                 :  {value from Jira Classification field, analyst entry, or "Not specified"}
Volume                      :  {N} orders/7d on {itc} ({NES_pct}% NES)
BLOCKING                    :  One sentence. Omit this line entirely if nothing blocks ecomm from proceeding.
```

**Geometry-aware field rules:**

**HARD CONSTRAINT — Offer Collection ID must appear in every Quick Reference block, on every path, for every geometry:**
- Standalone geometry: emit `Offer Collection ID : Not available`. The field must be present and must say exactly "Not available" — not "N/A", not blank, not omitted. Its presence tells the analyst the field was checked and confirmed absent.
- Offer Collection geometry: emit `Offer Collection ID : {UUID from offerId field of get_curated_offer response}`. This UUID is the primary engineering ID for cloning and wiring operations. It is the same value as `offerId` — the label changes based on geometry, not the UUID. Never omit this field when geometry is Offer Collection.
- Ghost / unresolvable: emit `Offer Collection ID : Not resolvable — catalog returned no offerId`.

This constraint applies equally to NES Quick Reference blocks (Step A2a), CES Quick Reference blocks (Steps A2b/A2c), Modify output blocks (Step M output), and Supporting Detail blocks. No geometry or path is exempt.

- For a **Standalone Offer**: the label is `Offer ID` (not "Base Collection ID" or "Offer Collection ID"). Emit the `Plan` line immediately after it — the plan from `get_offer_collection_definition` is authoritative and must be shown. Do not emit any Component lines. Always emit `Offer Collection ID : Not available` — the field must appear so the analyst can see it was looked for and not found. Do not omit it entirely; do not write "N/A".
- For an **Offer Collection**: the label is `Offer Collection ID`. This is the same UUID as `offerId` from `get_curated_offer`, but the label signals to engineering that they are looking at a collection, not a standalone. Emit one Component line per `prePurchaseKeyMap.offers[]` entry. Do not emit a `Plan` line at the top level — plans are per-component.
- If **both an `offerId` and a `prePurchaseKeyMap` structure** are present (expected for all collections): show `Offer Collection ID` (same value as offerId) plus all component lines. No separate "Base Offer ID" label is needed unless the ticket context requires distinguishing the primary product offer from the collection wrapper — if that detail is needed, add a `Primary Product Offer ID` line immediately under `Offer Collection ID`.
- If **neither** is present: the BLOCKING line is the only ID field. Do not leave placeholder fields.

**Champion value by path:**
- NES path (A2a): `{package_id}` from Step A1 billing data — the currently-live curated offer on this surface. Source label: "billing data (Direct — billing-confirmed)". No INFERRED disclosure required.
- CES path, Chain Step 1 success: merchandising package slug confirmed as a curated offer. Source label: "INFERRED — merchandising API match".
- CES path, Chain Step 2 success: curated offer slug found via ID scan. Source label: "INFERRED — keyword scan (confirm with ecomm before cloning)".
- CES path, Chain Step 3 only: `Not found — no existing curated offer; new offer required`. Source label: "INFERRED — tag search only; no existing offer".
- CES path, chain exhausted: `None — net-new build required (see NET-NEW BUILD block below)`. Source label: "all paths exhausted".
- Ambiguous champion (multiple package_ids simultaneously active): list all active `package_id` values on one line, comma-separated. The AMBIGUOUS CHAMPION disclosure with volume still applies above the blocks.

**Clone Source field (Modify and Clone operations only):** When Offer Operation = Modify or Clone AND the discounted-variant flag fired, emit a separate `Source to Clone` field immediately after the `Champion` line. The champion shows the currently-live slug (which may be a discounted variant); the `Source to Clone` shows the base (non-discounted) slug that engineering should clone. When no discounted variant is detected, do NOT emit a separate `Source to Clone` line — the `Champion` line IS the clone source and the source label in parentheses is sufficient. Never duplicate the same slug value across both fields.

```
Champion (clone from this)  :  {disc_slug} (currently live — discounted variant)
Source to Clone             :  {base_slug} (base — use this as the clone source; see Discounted variant flag)
```

When Offer Operation = Create and no discounted variant was detected: **do not emit a separate "Clone Source" line.** The champion IS the clone source. Duplication of the same value across two fields creates ambiguity about which to use — remove it.

**Field rules:**
- **Product Name(s):** pull `product_name` values from Step A1 billing data for PFIDs observed on this surface. If the intake prompt names the product explicitly (e.g. "MWP Basic"), use that as the label. Leave blank (omit the line) only if Step A1 returned no rows and the intake prompt did not name the product.
- **Price:** pull `avg_catalog_list_price` and `avg_catalog_sale_price` from Step A1 per PFID × term combination. Format as "{PFID} → list ${list_price} / sale ${sale_price} per {term}". When entry was a Jira ticket and a `Target Price (from ticket)` was extracted, append it on its own line immediately after the billing-derived prices: `Target Price (from ticket) : {value}` — clearly distinguished from billing history. Leave blank (omit the line) if Step A1 returned no pricing data and no price was stated in the intake.
- **Surface(s):** list all distinct `item_tracking_code` values from Step A1 where this bundle (`package_id`) was observed. Never collapse multiple ITCs into one row.
- **Regions:** list distinct `bill_country_code` or `region_name` values from Step A1 for this bundle. If the intake prompt names markets explicitly, use those instead. Leave blank (omit the line) if Step A1 returned no country/region data and no market was stated in the intake.
- **PFIDs on Surface:** list all distinct `pf_id` values for this bundle, paired with their `product_name`. Always emit this line — even if only one PFID is present. **This list has two mandatory sources — both must be consulted before emitting:**
  1. **Billing source (NES path):** all distinct `pf_id` values returned by Step A1 for this `package_id`. **Billing source (CES path):** `package_id` is null on the CES path — key off the surface ITC and the analyst's product scope instead. List all distinct `pf_id` values returned by Step A1 for the target ITC (or the PFID from the intake entry if ITC-first). If PFIDs could not be determined from billing data, write: `PFID(s) : not identified in billing data — {reason: new surface (no 7-day billing traffic) | low-traffic surface (fewer than 3 distinct PFIDs found) | catalog-era product (PFIDs not tracked in billing for this category)} — verify complete PFID list with ecomm before filing`.
  2. **Free component source:** any PFIDs identified in the free component checkpoint (Step A2a) or CES free-trial component check (Step A2b) that have `purchaseType=Free` or zero billing revenue. These PFIDs will NOT appear in Step A1 results and must be added from the catalog resolution. Omitting them silently produces an incomplete PFID list and an incomplete engineering ticket.
  
  The final `PFIDs on Surface` line is the union of both sources. Never filter to only billing-visible PFIDs. Never filter to only the entry product or entry PFID. A bundle with N components (including free ones) must show N PFIDs here. A missing PFID means ecomm builds an incomplete offer.
  
  **Immediately after the PFIDs on Surface line, emit a completeness annotation:**
  ```
  PFID completeness  :  {N} of {expected_N} PFIDs resolved.
  ```
  Where `{expected_N}` = distinct components from `prePurchaseKeyMap.offers[]` + free component checkpoint + any CES addons. If `N = expected_N`: write "All {N} PFIDs resolved." If `N < expected_N`: write "{N} of {expected_N} resolved — {unresolved_count} unresolved: {list product names}. BLOCKING — incomplete PFID list. Resolve before filing." This annotation is mandatory on every run — never omit it even when the list appears complete. A BLOCKING annotation fires whenever N < expected_N regardless of how small the gap is.
- **Term:** always populated. If a specific term was requested, write exactly that value (e.g. "1 Year"). If all terms were requested or no filter was applied, list every distinct `product_term_num` + `product_term_unit_desc` combination observed for this bundle on this surface (e.g. "1 Year, 2 Year, 3 Year"). When multiple terms appear and no filter was applied, add a note: "All terms shown — confirm scope with analyst before filing." Do not aggregate or hide any observed term.
- **BPO / Trial:** sourced from the `get_curated_offer` response. Omit this line entirely if the field is absent in the response — do not write "N/A" or "None".
- **Cart Renewal Behavior:** sourced from the `get_curated_offer` response. Same rule — omit if not present.
- **Discount:** always reflects billing data, not what the request says. See format rules above. When entry was a Jira ticket and a `Discount (from ticket)` was extracted (e.g. "DISCWAMBA", "365AF1F1CB from PRICING-15500"), add a second `Discount (from ticket)` line immediately after the billing-derived `Discount` line. If a PRICING ticket was referenced in the Jira body, note it: `Discount (from ticket) : {code} (see {PRICING-XXXXX})`. These two Discount lines are separate — billing shows what exists today; ticket shows what is being applied by this experiment.
- One Component line per entry in `prePurchaseKeyMap.offers[]`. Use the component's `name` from `get_offer_definition_by_id` as the label. Never omit a component. **Exception: Modify — Add Component requests.** When Offer Operation = Modify, do not list existing unchanged components in any output block or ticket preview. The "never omit a component" rule applies to Create/Clone paths only. The Modify output shows only what is being added.
- For Standalone Offers: label the ID field `Offer ID` (not `Offer Collection ID`). Emit the `Plan` line immediately after, using the plan from `get_offer_collection_definition` — it is authoritative for standalones. Omit all Component lines. Always emit `Offer Collection ID : Not available` — the field must appear so the analyst can confirm it was looked for and not found.
- For Offer Collections: label the ID field `Offer Collection ID`. Emit a `Collection Plan` line immediately after it using the top-level `plan` from `get_curated_offer` — this is the collection-level plan engineers use for cloning operations. Do not omit this line. Do not emit a standalone `Plan` line — that label is reserved for Standalone geometry. Emit one Component line per `prePurchaseKeyMap.offers[]` entry.
- If a component's `plan` is absent from the `prePurchaseKeyMap` entry: write `NOT SPECIFIED — component inherits collection plan (see Collection Plan above)`. Do not add a BLOCKING line for this case — the absence of a per-component plan does not block ecomm when the collection-level plan is present. Only escalate to BLOCKING if the collection-level plan is also absent (i.e. `collection_plan` was not returned by `get_curated_offer`).
- If a component lookup failed: write `{raw offerId} — lookup failed, verify manually`.
- Never add placeholder lines for fields with no data. Omit the line.
- No prose before or after the Quick Reference blocks — except the champion ambiguity disclosure above and the required CES disclosure sections when the CES path ran.

When multiple bundles are stacked, separate each block with a blank line between the last field line and the next `=== {bundle_slug} ===` header.

After all Quick Reference blocks, append a Flags table. One row per condition that applies. Omit the table entirely if no flags apply.

| Flag | Detail |
|------|--------|
| A/B test likely | {N} bundles active on `{itc}` simultaneously — confirm champion with ecomm before cloning |
| nes- prefix detected | Billing data returned `{nes-slug}` (nes- prefix). Catalog called with raw slug → NOT FOUND. Retried with clean slug `{clean-slug}` → {FOUND — used as curated offer ID / NOT FOUND — classified as ghost}. |
| Discounted variant | `{disc_slug}` appears to be a discounted configuration (slug contains `-disc` / `-discount-` / embedded discount code). Base slug: `{base_slug}`. Clone the base slug for new experiments — do not clone the discounted variant unless the intent is to reproduce the existing discounted configuration. |
| M365 geo risk | Component `{name}` has `m365` tag — M365 is not available in all markets. Before cloning: (1) confirm M365 availability for `{market}` via the Microsoft partner portal or ecomm catalog team, (2) if M365 is unavailable, identify an alternative email component (Titan, open exchange) — the ticket is BLOCKED until a valid email component is confirmed for the target market. |
| CES surface gap | `{itc}` (`{N}` orders/7d) has no `package_id` — these orders are CES and not covered by the NES champion |
| Discount code conflict | `{itc}` has existing code `{code}` that would be overridden |
| Plan not specified | Component `{name}` has no plan in `prePurchaseKeyMap` — ecomm must confirm |
| Multiple terms (unfiltered) | Bundle `{slug}` observed with {N} distinct term lengths on this surface ({term_list}). No term filter was applied — output is cross-term. Analyst must confirm which term(s) the new offer should cover before filing. |
| SLP-DLP funnel expansion applied | NES events for `{entry_itc}` queried across both entry ITC and configure-page ITC (`{configure_page_itc}`). If `{configure_page_itc}` returns zero NES rows in `offer_pulse_experiment`, GAP-042 applies — NES package slugs recovered via direct traffic event fallback; labeled accordingly. |

*(Show only rows that apply. Do not show example rows. Omit the table entirely if nothing flags.)*

### M365 Geo Risk Handling

When the M365 geo risk flag fires, apply the decision table below before rendering the ticket payload. Market is resolved from the geo-routing step (B-pre / Step A pre-flight) or from explicit analyst input.

| Stated target market | Action | Output effect |
|---|---|---|
| Explicitly includes India | BLOCK | Add `BLOCKING: M365 component cannot be shown in India — bundle requires an alternative email component (Titan Email / open exchange) before this ticket can be filed.` Replace the M365 component row in the payload with `[BLOCKED — geo-restricted component]`. |
| "Global", "all markets", "ROW", or unspecified | WARN | Add `GEO WARNING: Target market includes or may include India and developing markets where M365 is unavailable. Confirm geo scope with ecomm before filing. If India is in scope, substitute Titan Email (offer ID: 927a9d45).` |
| Explicitly US / CA / AU / GB / developed-market-only | No action | Flag row still appears in the Flags table (for record) but no BLOCKING or WARN line is added to the payload. |

**Confirmed restricted markets (from billing data):** India (`IN`). Zero `IN`-market rows observed in billing for `wordpress-o365-forever-ssl-basic`, `wordpress-o365-forever-ssl-deluxe`, `dpp-ca-ca-solution-tier1`, or any `-o365-` slug. Treat any IN-market scope as a hard block.

**Standard flag language for the ticket comment** (copy verbatim into the curated offer creation ticket):

> "This offer includes an M365 email component. M365 Business plans are not available in India and select developing markets. If this offer is intended for global or ROW scope, the M365 component must be substituted with Titan Email (offer ID: 927a9d45) for IN-market traffic. Please confirm geo scope before wiring the component."

---

**CES Terminal Payload (rendered after all Quick Reference blocks and Flags, whenever the CES path ran)**

This block is the concluding artifact for the CES path — the complete handoff to engineering or pricing.

```
=== CES Package Request Payload ===
```

One row per PFID × Term combination. Pull all fields from the Step A1 surface audit results plus the A2b/A2c chain output. **Never omit a row because the volume is low.** Also include any PFIDs identified via the CES free-trial component check (Step A2b) or the Free PFID recovery step (Chain Step 2) that have zero or near-zero billing volume — annotate those rows with `purchaseType=Free; zero billing revenue` in the Product Name column. The row set here must match the `PFIDs on Surface` list in the Quick Reference block exactly — if they diverge, the Quick Reference list wins and the CES Terminal Payload must be updated to match.

**Champion ambiguity disclosure for CES:** If the Candidate table (Section 4 of the CES disclosure) showed multiple candidates without a single confirmed match — the "Selected" column has more than one finalist, or the chain ended at Step 3 only — add a one-line statement immediately before this table:

> "AMBIGUOUS CES CHAMPION — {reason: no exact merchandising match / multiple ID scan candidates / tag search only}. The 'Existing CES Package' column shows all candidates. Ecomm must confirm the correct slug before filing the package request."

| PFID | Product Name | Term | Tier | Discount Code | Existing CES Package | Orders (7d) | Status |
|------|-------------|------|------|--------------|---------------------|-------------|--------|

Column definitions:
- **PFID** — `pf_id` from billing
- **Product Name** — `product_name` from billing with term and quantity suffixes stripped. Remove trailing patterns such as " - 1 Year", " - 3 Years", " - Monthly", " - 1 Month", " - N users", "renews annually", etc. Use the base product name that is consistent across all term variants of the same SKU (e.g. "Microsoft 365 - Email Essentials - EE", not "Microsoft 365 - Email Essentials - EE - 1 Year").
- **Term** — `product_term_num` + `product_term_unit_desc` combined (e.g. "1 Year", "2 Year", "1 Month")
- **Tier** — `product_pnl_subline_name` from billing, normalized per the vocabulary table below. If null, use "Standalone". Do NOT fall back to `product_pnl_line_name` — it contains the product line name (e.g. "MS Office 365", "CnP Hosting"), not the tier.

  **Tier normalization vocabulary:**

  | Raw `product_pnl_subline_name` | Canonical Tier | Notes |
  |---|---|---|
  | `PMail` | Standalone | Accounting category for M365 personal mail — not a tier descriptor |
  | NULL | Standalone | No subline configured |
  | Any other non-null value | Use as-is | Real tier labels (Economy, Deluxe, Business Premium, Email Plus, Super Premium, etc.) |
- **Discount Code** — `item_discount_code` from billing. UUID placeholder → "None (UUID placeholder)". Real code → write verbatim.
- **Existing CES Package** — slug from Step A2b/A2c. Labels by chain outcome:
  - Chain Step 1 success: `Confirmed — {slug}`
  - Chain Step 2 success (ID scan): `Candidate — {slug} (confirm with ecomm)`
  - Chain Step 3 only: `Tag search only — no slug available`
  - Chain exhausted / no match: `Not found`
- **Orders (7d)** — `SUM(total_orders)` for this PFID × Term from Step A1
- **Status** — label per row:
  - Highest-volume PFID in the category that is not a removal target → `Entry champion (stays)`
  - PFIDs named in the ticket as being removed → `Being replaced`
  - Disposition unclear → `Legacy CES — confirm disposition with ecomm`
  - Multi-year or monthly variants where the ticket specifies annual only → `Scope unclear — confirm with ecomm`

**PFID matrix grouping (required when 4+ PFIDs share the same Tier column value):** When the PFID list contains multiple entries from the same product tier, insert a tier sub-header row before the first PFID in that group (using `*— {Tier} tier —*` as the PFID cell value, all other cells blank). This surfaces the full term matrix per tier and prevents analysts from conflating different term lengths as separate products. Example: a cPanel Economy group with 1-month through 5-year variants gets a `*— Economy tier —*` header, then one row per term. Apply this grouping whenever a CES package covers more than one product tier or when the same tier spans 4+ term variants.

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
Champion (clone from this)  :  {package_id} from billing — the curated offer currently live on this surface
                               (source: billing data)

{Geometry-aware ID fields — same rule as Quick Reference:}

[IF STANDALONE:]
Offer ID                    :  {offerId}
Plan                        :  {plan from get_offer_collection_definition}
Offer Collection ID         :  Not available
{If the UNEXPECTED block fired for this bundle, insert it here.}

[IF OFFER COLLECTION:]
Offer Collection ID         :  {offerId}

[IF NEITHER:]
BLOCKING                    :  Catalog response contained no offerId — Offer ID and Offer Collection ID both unknown.

{Remaining fields always present:}
Collection Name             :  {name} from get_offer_collection_definition
Status                      :  ACTIVE / INACTIVE
Supports overridePolicies   :  Yes / No
Tags                        :  All tags from API, comma-separated. Never inferred.
Orders (7d)                 :  {total_orders}
NES Share                   :  {nes_pct}%
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

## Step B0 — PFID Discovery (product-name-first entry only)

Run this step when the analyst names a product (not an ITC or PFID) to discover all relevant PFIDs before the full inventory. Skip if the entry is ITC-first or PFID-first.

**Multi-product entry handling (required when the request names more than one distinct product)**

Before running any query, parse the entry for distinct named products. A "distinct named product" is one that the analyst explicitly wants to price, discount, or scope — it is not a component mentioned only as part of a bundle description. Examples:

- "WAM Premium and Commerce annual with TrustedSite" → three named products: WAM Premium, WAM Commerce, TrustedSite. Run one B0 query per product.
- "add M365 to the existing wordpress bundle" → one named product for B0: M365. WordPress is the surface context, not a product to price separately.
- "1-year Basic and Deluxe MWP on SLP" → two named products: MWP Basic, MWP Deluxe. Run one B0 query per product.

**Execution rule:** For each distinct named product, run a separate B0 query using that product's keyword as the search term (against `product_name` LIKE and `product_pnl_subline_name` LIKE as normal). Run all B0 queries in parallel. Union the results into a single PFID list keyed by `pf_id` + `product_name` + `product_term_num` + `product_term_unit_desc`. Deduplicate on `pf_id` — if two product queries return the same PFID, keep one row and note the duplication in the B0 confirmation prompt.

**HARD CONSTRAINT on multi-product queries:** Each individual B0 query is subject to the full filter prohibition that applies to all B0 queries. No term filter, no segment filter, no volume minimum on any individual product query. The per-product scope rule changes how many queries run and how results are combined — it does not introduce filtering.

**Confirmation step (multi-product):** Present the combined PFID list grouped by product family, not as a flat table. One sub-table per named product. Label each sub-table with the product name. This lets the analyst verify that each product's PFIDs are complete before A1 runs:

> "I found {N1} PFIDs for {Product 1}, {N2} PFIDs for {Product 2}, and {N3} PFIDs for {Product 3} — {N_total} total. Does this look right? Flag any rows to exclude or add before I continue."

Do not auto-proceed until the analyst confirms all product groups.

**HARD CONSTRAINT — do not apply any scoping filter in this step.** Step B0 discovers the complete PFID universe for the named product. Applying any filter at this stage silently excludes PFIDs from all downstream steps, making entire bundles invisible with no error or warning. The following filter types are ALL prohibited at B0:

- **Term filter** — `product_term_num`, `product_term_unit_desc`, or any equivalent term restriction. A 1-year filter excludes 2-year and 3-year PFIDs. A product whose bundle includes a 3-year component (e.g. a WP hosting PFID in an o365 bundle) will be missed entirely if term is filtered here.
- **Customer segment filter** — `new_customer_orders > 0`, `existing_customer_orders > 0`, `new_customer = true`, or any equivalent new/existing restriction. Products with low new-customer billing history (base annual SKUs, legacy CES products) can have near-zero `new_customer_orders` while being the correct base PFID — this filter excludes them silently.
- **Volume minimum filter** — `HAVING SUM(total_orders) > {N}`, or any threshold that removes low-volume rows. Low volume does not mean wrong product — it means a less-common term, market, or segment combination that is still required for bundle completeness.
- **Any other WHERE or HAVING clause** that restricts to a subset of the product's PFID space — e.g. country filter, currency filter.

The ONLY filters permitted at B0 are product-identity filters: `LOWER(product_name) LIKE`, `LOWER(product_pnl_subline_name) LIKE`, `LOWER(product_pnl_line_name) LIKE`, or a direct PFID list. Apply term, segment, and volume filters in Step A1 only — never in B0.

**B0 PFID completeness check (required):** After B0 returns results, inspect the PFID list for term coverage. If a product is expected to have multiple term lengths (e.g. 1-year, 2-year, 3-year variants) but B0 only returned PFIDs for one term, flag it before the analyst confirmation step:

> "B0 returned PFIDs for {observed_terms} only. If this product has {other_expected_terms} variants, they were not found — verify the keyword or supply additional PFIDs before proceeding."

Do not auto-proceed past the B0 analyst confirmation step when term coverage looks incomplete.

**Two-column strategy — always search both `product_name` and `product_pnl_subline_name` in a single query.** Marketing shorthand (MWP, WAM, Pro Email) rarely appears in `product_name` — the actual column contains the full billing name (e.g. "Basic Managed WordPress Websites"). Using only `product_name` LIKE will silently return zero rows for shorthand entries.

**PRE-QUERY FILTER ASSERTION (required — complete before writing any SQL):**

Before constructing the B0 query, answer each of the following. If any answer is YES, remove that clause before proceeding.

1. Does the query contain `product_term_num` or `product_term_unit_desc`? → YES means a term filter leaked in. Remove it. Example failure: analyst asked for "1-year MWP Basic" → agent wrote `AND product_term_num = 1 AND product_term_unit_desc = 'year'` → PFID 1320704 (3-year MWP Hosting, required component of the o365 bundle) was excluded → wordpress-o365-forever-ssl-basic bundle was missed entirely. Term filter belongs in A1.
2. Does the query contain `new_customer_orders`, `existing_customer_orders`, or `new_customer = true`? → YES means a segment filter leaked in. Remove it. Example failure: analyst asked for "new customers only" → agent wrote `AND new_customer_orders > 0` → PFIDs 958797 and 958799 (WAM Premium and Commerce base PFIDs with low new-customer billing) were excluded → wsb-vnext-tier3 and wsb-vnext-tier4 bundles were missed entirely. Segment filter belongs in A1.
3. Does the query contain a HAVING or WHERE clause on `total_orders`, `bill_country_code`, `region_name`, or `trxn_currency_code`? → YES means a scoping filter leaked in. Remove it.

The only WHERE conditions permitted in the B0 SQL are: the product-identity LIKE clause, `bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)`, and any direct `pf_id IN (...)` clause when PFIDs were supplied directly by the analyst.

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
  -- HARD CONSTRAINT: Do NOT add any scoping filter here (no term, no segment, no volume minimum).
  -- B0 discovers all PFIDs across all terms and segments. Scoping filters belong in Step A1 only.
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_orders DESC;
```

Use the root keyword from the product name. For "MWP Basic" use `basic`; for "Websites and Marketing" use `websites and marketing` against `product_pnl_line_name`; for multi-word product names chain keywords: `LOWER(product_name) LIKE '%professional%email%pro%plus%'`.

> **WAM Commerce subline gotcha (CES surfaces only):** The "Websites + Marketing Commerce" tier (e.g. PFID 970473 "Websites + Marketing Commerce - renews annually", CES package `wsb-vnext-tier4-disc`) carries `product_pnl_subline_name = 'Super Premium'` in billing — NOT `'Commerce'` or `'eCommerce'`. Filtering on `LIKE '%commerce%'` will silently drop these PFIDs. A separate `'eCommerce'` subline exists but belongs to the old DIFM/DIFy bundle (`pwsdifm-gocentral-ols-websitecare`, PFID 1208799 "Websites + Marketing Ecommerce - with Build") — a different product that includes a build fee and marketing services. When the request is for "WAM Commerce": use `product_pnl_subline_name = 'Super Premium'` within the WAM PNL line, or filter by confirmed PFIDs directly. Do not use `'Commerce'` or `'eCommerce'` as a subline keyword.

If the combined query returns zero rows or only clearly wrong products, stop and ask: "I found no matches for '{keyword}' in product_name or product_pnl_subline_name. Please provide a PFID or the exact `product_pnl_subline_name` value."

If the analyst specified a customer segment, **do NOT add a segment HAVING clause here** — B0 discovers all PFIDs across all segments (see HARD CONSTRAINT above). Note the segment for use in Step A1 only. Carry `WHERE existing_customer_orders > 0` or `WHERE new_customer_orders > 0` into A1 — never into B0.

**HARD STOP — always present the B0 PFID list and wait for explicit analyst confirmation before proceeding to A1.** Do not auto-proceed even if the list looks clean. This confirmation catches wrong-product matches (unexpected tier inclusions, legacy renewal PFIDs elevated by billing volume, or keyword collisions with adjacent products) before they contaminate the downstream PFID inventory.

Present the B0 results as a collapsed PFID × Term table:

> "I found {N} PFIDs matching '{keyword}' across {M} term lengths. Does this look right before I proceed? Flag any rows to exclude or add."

If the analyst confirms (any affirmative), proceed to Step A1 with the validated PFID list.
If the analyst flags unexpected rows, remove them and re-confirm before proceeding.
If the analyst is unsure, offer to run the query again with a narrower keyword before proceeding.

The post-discovery term validation (below) runs as part of this confirmation step — not as a separate ask.

**Known add-on PFID detection (mandatory — run after B0 returns results, before presenting to analyst):**

After B0 returns its PFID list, check whether any returned `pf_id` values match the following known high-cardinality add-on PFIDs:

| PFID | Product | Add-on role |
|------|---------|-------------|
| 3604 | SSL certificate (standard) | Free bundled add-on in most MWP and WAM hosting packages |
| 464069 | Microsoft 365 (M365 email) | Bundled email component in NES wsb-vnext and wordpress-o365 packages |
| 1192198 | Open-Xchange / Titan email | Bundled email component in NES wordpress-openexchange packages |

If any of these PFIDs appear in B0 results, annotate that row in the B0 confirmation table:

```
{pfid} — {product_name} — NOTE: Known bundled add-on component. Appears in many packages as a free or included product, not as a primary sellable item. If your experiment targets a hosting or website bundle, this PFID is likely a component of that bundle. Confirm its role before proceeding to A2b — see Dimension 0b below.
```

Do NOT suppress the PFID or remove it from the list. The annotation is informational. The analyst may legitimately target this PFID as a primary product (e.g. standalone M365 pricing). The annotation ensures they are not surprised when A2b returns dozens of bundle matches.

If this annotation fires, also trigger **Dimension 0b** in the Clarifying Questions Gate (see below).

---

### Post-B0 Term Validation (runs whenever B0 is used)

*This check fires whenever Step B0 ran (product-name-first entry). Skip only if the entry was PFID-first or ITC-first and B0 was not executed.*

After B0 returns its PFID list, always run the term distribution query:

```sql
SELECT DISTINCT product_term_num, product_term_unit_desc, COUNT(*) AS pfid_count
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE pf_id IN ({pfid_list_from_B0})
  AND bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY pfid_count DESC;
```

**Branch A — No term stated at the gate (or "unknown" / "all terms"):**

Present the term distribution inline with the B0 PFID confirmation — this is one ask, not two:

> "I found {N} PFIDs matching '{keyword}'. Here are the billing terms present in the last 30 days:
>
> | Term | PFID Count | Total Orders |
> |------|-----------|--------------|
> | {term_1} | {n} | {vol} |
> | {term_2} | {n} | {vol} |
>
> Does this PFID list look right? And which term(s) should this offer cover? Flag any rows to exclude."

Wait for the analyst to confirm both the PFID list and the target term(s) before running A1. Do not assume the highest-volume term is correct.

**Branch B — Term was stated at the gate:**

If the stated term matches one or more rows, proceed to A1 with that term filter.

If ZERO rows match the stated term, surface the conflict before proceeding:

> "You specified {stated_term}, but the {N} PFIDs found for this product appear only with the following billing terms: {observed_term_list}. Should I proceed with {highest-volume observed term}, or would you like to adjust the term scope?"

Wait for confirmation before running A1. Do not silently proceed with the original stated term when data shows it is absent.

---

## Post-Output: Ticket Preview Prompt

After all output is rendered (Quick Reference blocks, Flags, CES Terminal Payload — whichever apply), always append this prompt as the final line of your response:

> "Would you like to see a draft of what the **ecomm engineering ticket request** would look like? I'll format it for copy-paste — no ticket will be created."

Wait for the analyst's response. If they say yes (any affirmative — "yes", "sure", "show me", "go ahead"), render the appropriate Ticket Preview block below. If they say no or ignore it, do not render the preview.

**HARD CONSTRAINT — READ ONLY:** The skill must never call `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, or any write-capable Atlassian tool as part of the ticket preview. This step is display-only. The analyst copies and files the ticket themselves. Violation of this constraint is a critical error.

Do not ask this question if:
- The analyst explicitly said they do not want a ticket (e.g. "just show me the data")
- The output ended in a BLOCKING state with no confirmed champion — the preview has no safe content to show
- All chain steps were exhausted with no result — the NET-NEW BUILD block already serves as the handoff

---

### Ticket Preview — Path A (Curated Offer Creation)

*Render when the analyst confirms they want a preview and Path A ran.*

Populate every field from the Quick Reference output already rendered. Do not re-query or call additional catalog tools. If a field was not resolved (e.g. BLOCKING component plan), write that status in the preview field verbatim so the analyst knows to complete it before filing.

```
=== Ticket Preview: Curated Offer Creation Request ===

  Summary line (copy into Jira Summary field):
  [Create Curated Offer] {surface label} — {product name}, {term} — {market(s)} — {new/existing/both}

  Description:

  **Champion (clone from):** {package_id or "not found — net-new build required"}
    Source: {billing data | merchandising match | ID scan | tag search only}

  {Geometry-aware ID section — use exactly one block:}

  [IF STANDALONE:]
  **Offer ID:** {offerId from get_curated_offer}
  **Plan:** {plan from get_offer_collection_definition — authoritative for standalones}
  Offer Collection ID: Not available
  *(Standalone offer — no component offer IDs)*

  [IF OFFER COLLECTION:]
  **Offer Collection ID:** {offerId from get_curated_offer}
  **Component Offer IDs (bundled at checkout):**
  {one line per prePurchaseKeyMap.offers[] entry}
  - {Component Name}: {offerId} / plan: {plan — or "NOT SPECIFIED — must confirm"}

  [IF NEITHER ID PRESENT:]
  **BLOCKING:** Catalog response contained no offerId — Offer ID and Offer Collection ID both unknown.
  Engineering cannot file this ticket until the ID is resolved.

  **PFIDs to include:**
  {one line per PFID}
  - {pfid}: {product_name} ({term})

  **Surface(s) / ITC(s):** {all ITCs from Quick Reference Surface(s) field}

  **Term scope:** {term from Term Scope header}

  **Market / Geo scope:** {markets from Quick Reference Geo Scope field}

  **Customer segment:** {new / existing / both}

  **Offer lever:** {value from Offer Lever field in Quick Reference — "Not specified" if absent}

  **Pricing reference:**
  {one line per PFID — from Quick Reference Price field}
  - {pfid} ({product_name}, {term}): list ${list} / sale ${sale}

  **Discount code (if any):** {item_discount_code from billing — or "None"}

  **Notes / flags for engineering:**
  {one line per row in the Flags table — omit section if no flags}
  - {flag}: {detail}

  Acceptance criteria:
  - [ ] Curated offer created and wired to the surfaces listed above
  - [ ] All component offer IDs confirmed active and available in target markets
  - [ ] Pricing validated against reference above
  {if BLOCKING rows exist in Flags:}
  - [ ] BLOCKING items resolved: {list them}
```

**Ticket-Ready Block (append after the Acceptance Criteria section above):**

After the standard ticket preview, append a second block formatted to match the column structure that EP engineering teams use when tracking offer creation work. This allows copy-paste directly into a tracking spreadsheet or Jira table without reformatting.

```
=== EP Engineering Ticket Table ===
(Column order matches EP ticket format — copy into Description table)

| Package | Product | PFID | One Time Fee | Discount Code | Free Product | Market |
|---------|---------|------|-------------|--------------|-------------|--------|
{one row per PFID × term from the Quick Reference PFIDs on Surface list}
{Package = package_id (champion slug) for NES; "TBD — net-new build" for chain-exhausted}
{Product = product_name from billing}
{PFID = pf_id}
{One Time Fee = "Yes" if purchaseType=Free or known trial; "No" otherwise — derive from catalog response or billing receipt_price_usd_amt = 0}
{Discount Code = item_discount_code from billing, or Discount (from ticket) if extracted from Jira body; "None" if absent}
{Free Product = "Yes" if purchaseType=Free; "No" otherwise}
{Market = bill_country_code / marketId from request scope}
```

Notes on this table:
- One row per distinct PFID in the offer — a bundle with 3 component PFIDs generates 3 rows, all with the same Package value.
- The `One Time Fee` and `Free Product` columns are derived from the free-component checkpoint and catalog `purchaseType` field. If uncertain, write "Confirm" rather than guessing.
- If `Discount (from ticket)` was extracted in the Jira entry step, use that value in the Discount Code column — not the billing-derived `item_discount_code` which will be null for new experiments.

**Format rule:** The summary line is designed for direct paste into the Jira Summary field. The description body is designed for the Jira Description field as plaintext or markdown. Do not add prose before or after the block.

---

### Ticket Preview — Path A (Modify — Add Component)

*Render when the analyst confirms they want a preview, Path A ran, and Offer Operation = Modify — Add Component.*

Populate every field from the Modify output already rendered. Do not re-query. Do not list existing unchanged components — this preview describes only the add operation.

**One-step preview (new product's curated offer already exists):**

```
=== Ticket Preview: Curated Offer Modification Request ===

  Summary line (copy into Jira Summary field):
  [Modify Curated Offer] Add {new_product_name} to {surface label} bundles — {market(s)}

  Description:

  **Operation:** Add new component to existing packages on {ITC}

  **New component to add:**
  - {new_product_name}: {new component offerId} / plan: {plan — or "NOT SPECIFIED — ecomm must confirm"}

  **Packages to be modified:**
  {one line per row in the Existing Packages on Surface table}
  - {package_slug}: Base Offer ID {offerId}

  **Surface(s) / ITC(s):** {all ITCs from Step M1}

  **Market / Geo scope:** {from request}

  **Notes / flags for engineering:**
  {one line per row in the Flags table — omit section if no flags}
  - {flag}: {detail}

  Acceptance criteria:
  - [ ] New component offer ID added to prePurchaseKeyMap of all packages listed above
  - [ ] Plan confirmed for new component
  - [ ] Existing bundle behavior unchanged (no other components added or removed)
  {if BLOCKING rows exist in Flags:}
  - [ ] BLOCKING items resolved: {list them}
```

**Two-step preview (new product's curated offer does not yet exist):**

```
=== Ticket Preview: Curated Offer Modification Request ===

  Summary line (copy into Jira Summary field):
  [Modify Curated Offer] Add {new_product_name} to {surface label} bundles — {market(s)}

  Description:

  **Operation:** Two-step — create new standalone offer, then add to existing packages

  **Step 1 — Create new standalone curated offer for {new_product_name}:**
  - PFIDs to cover: {pfid_list from analyst input or Step M3}
  - Plan: NOT SPECIFIED — ecomm must define
  - Market: {from request}
  - Note: offerId from Step 1 is required before Step 2 can be filed

  **Step 2 — Add new component to existing packages:**
  {one line per row in the Existing Packages on Surface table}
  - {package_slug}: Base Offer ID {offerId} — add new component offerId (from Step 1) to prePurchaseKeyMap

  **Surface(s) / ITC(s):** {all ITCs from Step M1}

  **Market / Geo scope:** {from request}

  **Notes / flags for engineering:**
  - BLOCKING: Step 2 cannot be filed until Step 1 creates the offer and returns its offerId
  {one line per additional row in the Flags table — omit if no other flags}
  - {flag}: {detail}

  Acceptance criteria:
  - [ ] Step 1: New standalone curated offer created for {new_product_name}
  - [ ] Step 1: offerId confirmed and returned to requester
  - [ ] Step 2: New component added to prePurchaseKeyMap of all packages listed above
  - [ ] Existing bundle behavior unchanged (no other components added or removed)
```

**Format rule:** Same as Create/Clone — summary line for Jira Summary field, description body for Jira Description field. Do not add prose before or after the block.

---

### Ticket Preview — CES Package Request (Path A, CES path)

*Render when the analyst confirms they want a preview, Path A ran, and the surface was 100% CES.*

This preview targets the **CES/Merchandising team** (not ecomm engineering) — the goal is a new CES package configuration, not a curated offer.

**Carry-forward rule:** When the Quick Reference block contains a resolved Offer ID or Offer Collection ID (whichever geometry applied), Plan, or catalog discount code for the champion, those exact values MUST be repeated verbatim in the Catalog Resolution section of the ticket preview — do not re-derive them or omit them. Use the same geometry-aware label that appeared in the Quick Reference (`Offer ID` for standalones, `Offer Collection ID` for bundles).

```
=== Ticket Preview: CES Package Request ===

  Summary line (copy into Jira Summary field):
  [CES Package] {surface label} — {product name}, {term} — {market(s)} — {new/existing/both}

  Description:

  **Existing CES package (clone from):** {slug from CES Terminal Payload "Existing CES Package" column, highest-volume entry}
    Source: {merchandising match | ID scan | "not found — net-new build required"}
    Confidence: {High | Medium | None — see CES disclosure in output above}

  **Catalog resolution** (from catalog MCP — distinct from billing data):
    Geometry: {Standalone Offer | Offer Collection ({N} components) | Unresolvable — see BLOCKING below}
    {If Standalone:}
    Offer ID: {offerId from get_curated_offer — or "Not resolved — confirm before filing" if confidence is None}
    Plan: {plan from get_offer_collection_definition — or "Not resolved — confirm before filing" if confidence is None}
    {If Offer Collection:}
    Offer Collection ID: {offerId from get_curated_offer — or "Not resolved — confirm before filing" if confidence is None}
    Components: {N component offer IDs — listed in Quick Reference above}
    {Both geometry types:}
    Catalog discount code: {discountCode field from get_curated_offer — or "None" if field absent, or "Not resolved — confirm before filing" if confidence is None}

  **PFIDs to include:**
  {one row per PFID × Term from the CES Terminal Payload table}
  - {pfid}: {product_name stripped of term suffix} ({term}) | Tier: {canonical tier per normalization table — PMail→Standalone, null→Standalone, else use as-is} — {orders}/7d

  **Surface(s) / ITC(s):** {all distinct ITCs from Step A1 results}

  **Term scope:** {from Term Scope header}

  **Market / Geo scope:** {markets from request}

  **Customer segment:** {new / existing / both}

  **Pricing reference:**
  {one line per PFID from CES Terminal Payload — use avg_catalog_list_price / avg_catalog_sale_price from billing}
  - {pfid} ({product_name}, {term}): list ${list} / sale ${sale}

  **Existing discount codes (from billing):** {item_discount_code from CES Terminal Payload — or "None"}

  **Notes / flags for merchandising team:**
  {one line per row in the Flags table — omit section if no flags}
  - {flag}: {detail}
  {if confidence is None or champion is ambiguous:}
  - UNCONFIRMED CHAMPION — clone source must be verified before filing

  Acceptance criteria:
  - [ ] CES package created or cloned from the source listed above
  - [ ] All PFIDs in scope confirmed with pricing team
  - [ ] Package wired to the surface ITC(s) listed above
  - [ ] Pricing validated against reference above
  {if catalog resolution was successful (confidence High or Medium):}
  - [ ] {Offer ID or Offer Collection ID} ({offerId}) and {Plan (standalone) or component offer IDs (collection)} confirmed with ecomm engineering before filing
  {if champion confidence is None:}
  - [ ] BLOCKING: clone source must be identified and confirmed before this ticket can proceed
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
| Standalone Offer | Domain or SSL sold without add-ons | `prePurchaseKeyMap` absent or empty. Output field: `Offer ID` (the `offerId` from `get_curated_offer`). One `get_offer_collection_definition` call. Plan from that response is authoritative and must be shown. State "Standalone Offer — single product, single plan" in output. Always show `Offer Collection ID : Not available` — the field must appear so the analyst can see it was looked for and not found. If `get_offer_collection_definition` returns a non-empty `offers[]`, emit the UNEXPECTED block. |
| Offer Collection (bundle) | WordPress hosting + M365 or Titan Email | `prePurchaseKeyMap` has one or more entries. Output field: `Offer Collection ID` (same UUID as `offerId` from `get_curated_offer` — label distinguishes it from a standalone). Never use the top-level plan. Iterate all `prePurchaseKeyMap.offers[]` entries — for each, call `get_offer_definition_by_id` and record `offerId`, `name`, `tags[]`, and the `plan` from the `prePurchaseKeyMap` entry. All Component Offer IDs are primary ecomm payload — a missing row means ecomm builds an incomplete offer. Also look up any `offers[]` entries from `get_offer_collection_definition` that are absent from `prePurchaseKeyMap` and list them in a separate table (not required for the clone, but must not be silently dropped). |

When in doubt, show more not less. It is always better to present a row and let the analyst exclude it than to silently omit it.

---

> **No ticket has been created or modified.** This is read-only output for your review. To create or update a ticket, tell me explicitly and I'll do it then.

