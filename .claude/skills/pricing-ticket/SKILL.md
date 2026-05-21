---
name: pricing-ticket
description: Given a Jira offer ticket, product name, ITC, or PFID, produce a complete PFID list with current discount codes and pricing — ready for a pricing or discount ticket.
---

# /pricing-ticket — Pricing & Discount Ticket Builder

Given a Jira ticket, product name, ITC, or PFID, produce everything the pricing team needs: a verified PFID list, current discount codes, existing price points, and a ready-to-paste ticket summary.

After the clarifying questions gate resolves, execute immediately and silently — run all queries, collect every result, then render the complete output once at the end. Never emit partial output, intermediate tables, or step narration mid-execution.

**HARD CONSTRAINTS:**
- Read-only. Never create, update, transition, or comment on any Jira ticket without explicit analyst instruction.
- Never show only the top result when multiple exist. A surface can have many PFIDs and many discount codes simultaneously. Show all of them.
- Every response ends with an explicit reminder that no ticket action has been taken.
- Every markdown table must have one row per unique combination of values. Never compress multiple values into a single cell.
- In Step B0, never apply term, segment, or volume filters. Those belong in Step B1 only.

---

## Domain Vocabulary

| Technical Term | Business Label | Definition |
|---|---|---|
| PFID | Product ID | The underlying product SKU (e.g. `1320706`) |
| ITC | Surface | The page/journey where the customer saw the offer (e.g. `slp_wordpress`) |
| Package ID | Curated Offer ID | Named offer slug from billing/CLN data (e.g. `wordpress-o365-forever-ssl-basic`). NES only — CES has no package ID. |
| NES | Curated Offer | New eCommerce — catalog-backed offers with named bundles. Identified by a non-null `package_id`. |
| CES | Legacy Offer | Classic eCommerce — no named bundle. `package_id` is null. |

---

## Data Foundation

All queries use `connection='bi'`.

### `pricing_experiment_dev.offer_pulse_experiment`
Pre-joined billing + CLN table.

Key columns: `pf_id`, `product_name`, `product_term_num`, `product_term_unit_desc`, `item_tracking_code` (ITC), `package_id`, `item_discount_code`, `purchase_path_name`, `bill_country_code`, `trxn_currency_code`, `product_pnl_line_name`, `product_pnl_subline_name`, `total_orders`, `new_customer_orders`, `existing_customer_orders`, `receipt_price_usd_amt`, `receipt_regular_price_usd_amt`, `catalog_list_price_usd`, `catalog_sale_price_usd`, `bill_modified_mst_date`

> **Aggregation note:** `total_orders` is pre-aggregated at the grain of pf_id × ITC × package_id × discount_code × country × date. Always use `SUM(total_orders)` when aggregating across a date range.

### `pricing_experiment_dev.pf_id_package_details_v1`
Lean mapping table: `pf_id`, `item_tracking_code`, `package_id`, `cln_create_utc_ts`, `cln_update_utc_ts`. Use for ITC → package_id lookup outside the 7-day window.

---

## Surface Name → ITC Map

| Ticket language | Exact ITC | LIKE filter |
|---|---|---|
| Pre-Check, PreCheck, DPP | `dpp_precheck` | `LIKE 'dpp_%'` |
| Sales Landing Page, SLP, FOS, Front of Site | varies | `LIKE 'slp_%'` — FOS means Sales Landing Pages, not Domain Purchase Path. Do not map FOS to `dpp_*`. |
| Domain Landing Page, DLP | varies | `LIKE 'dlp_%'` |
| Upgrade Path, UPP | varies | `LIKE 'upp_%'` |
| Dashboard, Manage, MGR | varies | `LIKE 'mgr_%'` |

---

## Clarifying Questions Gate

Three dimensions govern query scope. Run this check before any queries. If the request already answers a dimension, skip that question. Present all needed questions as a single numbered list — do not ask sequentially.

**Jira entry rule:** When the entry is a Jira ticket, fetch it first. Then re-run all skip tests against the extracted ticket fields before asking any questions.

**Maximum 3 questions.** If all dimensions are unclear, ask all three. Priority if dropping becomes necessary: Term > Market > Segment. Never drop Term or Market.

---

### Dimension 1 — Customer Segment

**Skip if:** the request states "new customers", "existing customers", "renewals", "both", or "new and existing".

**Ask if:** segment is not mentioned. Exception: if the request is a pure surface audit, infer "both" and state the assumption.

**How segment affects queries:**
- For renewal-only scope, add `AND ope.existing_customer_orders > 0` to the Step B1 WHERE clause. For new-only scope, add `AND ope.new_customer_orders > 0`. Use a row-level WHERE filter — not HAVING — to preserve accurate order counts. Never apply in Step B0.

Question: "Should this cover **new customers**, **existing / renewal customers**, or **both**?"

---

### Dimension 2 — Target Markets / Geo Scope

**Skip if:** specific markets or regions are named.

**Market inference layer (run before asking — attempt in this order):**

**Source 1 — ITC prefix signals** (only if ITC already resolved):

| ITC prefix pattern | Confidence | Inferred market |
|---|---|---|
| `dpp-intl-*`, `dpp-{market}-{ccTLD}-*` | Hard resolve | International / non-US (geo is explicit in slug — skip the question) |
| `mena-*` | Hard resolve | MENA region (geo is explicit in slug — skip the question) |
| `slp_*`, `dpp_precheck`, `dpp_config1`, `dlp_*`, `upp_*` with no geo qualifier | Soft infer only | Likely US domestic — document as `Market (inferred: likely US domestic — confirm)` and proceed, but flag in output that the analyst should confirm before filing the ticket |
| Mixed or ambiguous prefix | No inference | Proceed to Source 2 |

**Important:** Plain prefix surfaces (`slp_*`, `dpp_precheck`, `dpp_config1`, `dlp_*`, `upp_*`) process billing for multiple `bill_country_code` values. The ITC string alone is not authoritative for geo. A soft-inferred market skips the gate question but must include a visible confirmation flag in the output — it does NOT count as a hard-resolved skip that suppresses the flag entirely.

**Source 2 — Ticket body signals** (for Jira entry):
- Explicit geo scope in the ticket body: "Reseller customers", "US only", "India", "ROW", named countries → infer directly
- Product name with geo encoding: "India Titan Email", "UK hosting" → infer from the name

**Source 3 — Product geography profile** (last resort — apply only when no ITC or ticket signal is available):
- MWP (Managed WordPress) → US domestic inferred only when BOTH conditions are true: (1) ITC is a soft-inferred US-domestic surface (`slp_*`, `dlp_*`) AND (2) the ticket body contains no international scope signals. MWP product name alone is NOT sufficient.
- cPanel hosting, Business Hosting on `slp_*` or `dlp_*` without an intl variant → US domestic is a safe default
- WAM/WSB, Email (M365/Titan), domain products → do NOT infer from product alone; these have geo-split pricing families

**Inference resolution rule:** If exactly one market is unambiguously supported by the inference sources above, skip the question and document the result as `Market (inferred): {value}` in the gate resolution summary. If inference is ambiguous or produces no result, market must be asked — it is a required input and cannot be assumed.

**Market → query filter mapping:**
- "US only" → `AND ope.bill_country_code = 'US' AND ope.trxn_currency_code = 'USD'`
- "ROW" → `AND ope.bill_country_code NOT IN ('US', 'CA', 'IN')` — confirm the ROW definition with the analyst if the ticket specifies a non-standard boundary
- "India" → `AND ope.bill_country_code = 'IN'`
- Named country → `AND ope.bill_country_code = '{iso_code}'`
- "All markets" or "globally" → omit country filter; add `ope.bill_country_code` and `ope.trxn_currency_code` to GROUP BY

Question: "Which markets should this cover? (e.g. US only, ROW, India, all markets, or a specific country list)"

---

### Dimension 3 — Billing Term

**Term pre-parse (mandatory — run before evaluating the skip test):**

| Signal | Examples | Inferred term |
|---|---|---|
| Explicit term word | "annual", "1-year", "one year", "yearly" | 1 Year |
| Explicit term word | "biennial", "2-year", "two year" | 2 Year |
| Explicit term word | "triennial", "3-year", "three year" | 3 Year |
| Explicit term word | "monthly", "1-month", "per month" | 1 Month |
| Pricing pattern | "$X/mo", "$X per month", "$X/month" | 1 Month |
| Pricing pattern | "$X/yr", "$X per year", "$X annually" | 1 Year |
| Entry phrase | "annual SKUs", "annual plan", "annual term", "1 Year" | 1 Year |

- If pre-parse finds one unambiguous signal: skip Dimension 3 entirely. Document the inference in the Term Scope header: `TERM SCOPE: 1 Year (inferred from entry — "annual SKUs")`.
- If pre-parse finds conflicting signals (e.g. entry mentions both monthly and annual): ask in confirmation form — "I inferred {term} from your entry — is that correct, or does this cover multiple terms?"
- If pre-parse finds nothing: ask Dimension 3 as normal.

**Skip if:** a specific term is parseable from the entry (see pre-parse table above).

**Ask if:** no term length is mentioned.

Question: "Which billing term(s) should this cover? (e.g. 1 Year, 2 Year, 3 Year, 1 Month — or 'all terms')"

**Handling the answer:**
- **Specific term(s):** add `AND product_term_num = {N} AND product_term_unit_desc = '{unit_lowercase}'` to Step B1 only. When multiple terms are specified, use `AND (product_term_num, product_term_unit_desc) IN (({N1}, '{u1}'), ({N2}, '{u2}'))` — lowercase values only. **`product_term_unit_desc` is always lowercase: `'year'`, `'month'`, `'quarter'`. Using Title Case returns zero rows.**
- **"All terms":** omit term filter; group and display term as a first-class column. Note at top of output: "TERM SCOPE: All terms — confirm scope with analyst before filing."
- **Term stated in the Jira ticket:** extract it from the ticket body and skip the question. If the ticket body is ambiguous (e.g. "annual" could mean 1-year or 12-month), list both interpretations and ask for confirmation before running queries.
- **HARD CONSTRAINT:** Term filter never applies to Step B0. B0 discovers the complete PFID universe across all terms.

**Unit normalization:** analysts may say "annual" (= 1 Year), "biennial" or "2-year" (= 2 Year), "triennial" or "3-year" (= 3 Year), "monthly" (= 1 Month). Translate to `product_term_num` + `product_term_unit_desc` before filtering. If the translation is ambiguous, state the assumption and confirm.

---

### Gate rendering rule

If one or more questions cannot be resolved, collect all into a single numbered list before running anything:

> "For the most accurate output, please answer all questions before I begin. I'll wait until I have all inputs.
>
> Before I run queries:
> 1. [question]
> 2. [question]"

**Do not run any queries until all gate questions are answered.** If the analyst answers some but not all, acknowledge the answers received and re-present the remaining unanswered questions as a new numbered list using the same preamble. Partial execution is not permitted.

---

## Entry

### Entry Option 1 — Jira Ticket

1. Fetch with `mcp__atlassian__getJiraIssue` (`cloudId: godaddy.atlassian.net`). If Atlassian MCP is unavailable, ask the analyst to paste the relevant fields (surface/ITC, product or PFID, term).
2. Extract from ticket body only (ignore linked tickets):
   - **Surface / ITC** — map using Surface Name → ITC Map above
   - **Product / PFID** — if explicitly called out
   - **Target price** — any explicit price point stated. Record as `Target Price (from ticket)`.
   - **New discount codes** — any explicitly named code not yet in billing. Record as `Discount (from ticket)`.
   - **Billing term** — scan for term signals in priority order: (1) PFID/product table with a term or duration column (e.g. "1 Year", "12mo", "Annual"); (2) package slug encoding (`-1yr`, `-3yr`, `-annual`, `-monthly`); (3) experiment scope field for phrases in the Dimension 3 pre-parse signal table; (4) ticket title. If any signal is unambiguous, record as `Term (from ticket): {value}` and skip Dimension 3. If multiple signals conflict (e.g. title says "annual" but PFID table has 3-year rows), record both and ask for confirmation using the confirmation form: "I see annual in the title but 3-year PFIDs in the table — which term scope should this cover?"
   - **Offers being removed** — any language describing packages or products being replaced. Record verbatim.
3. **Ticket type classifier (run before gate):** Scan for signals indicating no pricing ticket is needed:

   | Signal type | Example signals | Early-exit label |
   |---|---|---|
   | Rebate / cashback | "rebate", "cashback", "cash back", "reward", "post-purchase incentive" | rebate/cashback ticket |
   | Config toggle / feature flag | "config toggle", "feature flag", "enable/disable", "feature switch", "toggle on", "toggle off" | config/feature-flag ticket |
   | Reporting / analytics only | "reporting", "dashboard", "data pull", "analytics request", "metrics only" | reporting ticket |
   | Legal / compliance | "compliance", "legal requirement", "T&C update", "terms change" — with no pricing or offer scope | compliance ticket |

   If any signal is detected and the ticket contains NO language about changing a price or discount code, emit:

   ```
   EARLY EXIT — {early-exit label} DETECTED
   This ticket appears to be a {type} ticket. No pricing ticket is required.
   Ticket signals found: "{verbatim signal text from ticket body}"

   Confirm this classification is correct. If the ticket does require a price or discount change (e.g. rebate paid via a discounted offer), respond and I will proceed.
   ```

   Do not run the gate or any queries until the analyst confirms.

4. **Multi-arm detection (run before gate):** Scan for "Control:", "Treatment 1", "Treatment 2", "T1", "T2", "challenger", "arm", "variant A/B/C". If found, emit a **Ticket Decomposition block**:

   ```
   MULTI-ARM EXPERIMENT DETECTED
   This ticket describes {N} experiment arms. Each arm that changes pricing or applies a discount requires a separate pricing ticket.

   | Arm | Description | Ticket Type |
   |-----|-------------|-------------|
   | Control | {description} | {no ticket — unchanged} |
   | Treatment 1 | {description} | {pricing ticket / not applicable} |

   Confirm which arm(s) to produce output for before running queries.
   ```

   Wait for arm confirmation before proceeding.

5. Proceed to Step B0 (if product-name-first) or Step B1 (if ITC-first or PFID-first).

### Entry Option 2 — Direct Input (ITC, Product Name, or PFID)

| Entry type | Example | Primary filter |
|---|---|---|
| ITC string | `dpp_precheck` | `WHERE item_tracking_code = '...'` |
| Surface category | "the SLP", "DPP surfaces" | `WHERE item_tracking_code LIKE 'slp_%'` |
| PFID (numeric) | `1320706` | `WHERE pf_id = '1320706'` |
| Product name (free text) | "professional email pro plus" | `WHERE LOWER(product_name) LIKE '%professional%email%pro%plus%'` — run Step B0 first |
| Marketing shorthand / PNL subline | "MWP Basic", "WAM", "Pro Email" | `WHERE LOWER(product_pnl_subline_name) LIKE '%basic%'` — use when product_name LIKE yields zero or clearly wrong rows; run Step B0 first. **Exception: WAM Commerce tier uses subline `'Super Premium'`, not `'Commerce'` — see Step B0 gotcha.** |
| Product name + segment | "professional email pro plus, renewal only" | product name LIKE + `existing_customer_orders > 0` filter |

**If the entry is product-name-first:** go to Step B0 before B1.
**If the entry is ITC-first or PFID-first:** skip B0, go directly to B1.

---

## Step B0 — PFID Discovery (product-name-first entry only)

Run this step when the analyst names a product to discover all relevant PFIDs before the full inventory. Skip if entry is ITC-first or PFID-first.

**Multi-product entry handling:**

Parse the entry for distinct named products. A "distinct named product" is one the analyst explicitly wants to price or discount — not a component mentioned only as surface context.

Examples:
- "WAM Premium and Commerce annual with TrustedSite" → three products: WAM Premium, WAM Commerce, TrustedSite. One B0 query per product.
- "1-year Basic and Deluxe MWP on SLP" → two products: MWP Basic, MWP Deluxe. One B0 query per product.

Run all B0 queries in parallel. Union results into a single PFID list. Deduplicate on `pf_id`.

**HARD CONSTRAINT — no scoping filter in this step.** Prohibited at B0:
- Term filter (`product_term_num`, `product_term_unit_desc`)
- Segment filter (`new_customer_orders > 0`, `existing_customer_orders > 0`)
- Volume minimum (`HAVING SUM(total_orders) > {N}`)
- Any country, currency, or other WHERE/HAVING restriction

Only product-identity filters are permitted: `LOWER(product_name) LIKE`, `LOWER(product_pnl_subline_name) LIKE`, `LOWER(product_pnl_line_name) LIKE`, or a direct PFID list.

**Two-column strategy — always search both `product_name` and `product_pnl_subline_name`:**

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
  -- HARD CONSTRAINT: No term, segment, or volume filter here. Scoping filters belong in Step B1 only.
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_orders DESC;
```

> **WAM Commerce subline gotcha:** The "Websites + Marketing Commerce" tier carries `product_pnl_subline_name = 'Super Premium'` — NOT `'Commerce'`. Filtering on `LIKE '%commerce%'` silently drops these PFIDs. When the request is for "WAM Commerce": use `product_pnl_subline_name = 'Super Premium'` within the WAM PNL line, or filter by confirmed PFIDs directly.

If zero rows return, stop and ask: "I found no matches for '{keyword}'. Please provide a PFID or the exact `product_pnl_subline_name` value."

**Known add-on PFID detection (run after B0 returns, before presenting to analyst):**

| PFID | Product | Add-on role |
|---|---|---|
| 3604 | SSL certificate (standard) | Free bundled add-on in most MWP and WAM packages |
| 464069 | Microsoft 365 (M365 email) | Bundled email in NES wordpress-o365 packages |
| 1192198 | Open-Xchange / Titan email | Bundled email in NES wordpress-openexchange packages |

If any appear in B0 results, annotate that row:

```
{pfid} — {product_name} — NOTE: Known bundled add-on. Appears in many packages as a free/included product, not as a primary sellable item. Confirm its role before proceeding — pricing the bundle's host offer may be more appropriate than targeting this PFID directly.
```

Do NOT suppress the PFID. The annotation is informational.

**B0 term coverage check (required):** After B0 returns, run:

```sql
SELECT DISTINCT product_term_num, product_term_unit_desc, COUNT(*) AS pfid_count
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE pf_id IN ({pfid_list_from_B0})
  AND bill_modified_mst_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY pfid_count DESC;
```

- **No term stated at gate:** present term distribution inline with the B0 confirmation. Ask for both PFID list confirmation and target term(s) in one block.
- **Term stated at gate, zero matching rows:** surface the conflict before proceeding. Do not silently proceed with the stated term.

**HARD STOP — always present the B0 PFID list and wait for explicit analyst confirmation before running B1.** Present as a table grouped by product family. Prompt:

> "I found {N} PFIDs matching '{keyword}' across {M} term lengths. Does this look right before I proceed? Flag any rows to exclude or add."

---

## Step B1 — PFID Inventory

Declare the mode before running:

| Mode | When to use |
|---|---|
| **PFID Inventory** | Product-name-first entry, or "give me the PFID list" ask — goal is a clean PFID list for a pricing ticket |
| **Blast Radius** | ITC-first entry, or "what surfaces / discount codes are affected" ask — goal is surface spread and existing discount codes |

---

### PFID Inventory Mode

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
  -- Term filter: apply when specified in gate.
  -- Single:    AND ope.product_term_num = {N} AND ope.product_term_unit_desc = '{unit}'
  -- Multiple:  AND (ope.product_term_num, ope.product_term_unit_desc) IN (({N1},'{u1}'),({N2},'{u2}'))
  -- All terms: omit filter; term columns are in GROUP BY.
GROUP BY 1, 2, 3, 4
ORDER BY ope.pf_id, ope.product_term_num;
```

If the analyst specified renewal/existing only, add: `AND ope.existing_customer_orders > 0`.

---

### Blast Radius Mode

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
  -- Term filter: apply when specified in gate.
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
ORDER BY total_orders DESC;
```

> **Row count warning:** Blast Radius Mode groups on 12 columns. If result exceeds 500 rows, add `HAVING SUM(total_orders) > 10` to suppress noise, or switch to PFID Inventory Mode and drill blast radius as a follow-up.

---

## Step B2 — Discount Scope Assessment

From the B1 results, identify:
- **All distinct PFIDs** in scope
- **All distinct ITCs** (the blast radius)
- **All distinct package_ids** — each may need its own discount code configuration
- **Existing active discount codes** per PFID × ITC × package_id — flag real codes vs UUID placeholders
- **Current pricing** (receipt vs list vs catalog sale) — anchor for the new discount target
- **NES vs CES split** per PFID — affects how the discount is applied

> **Call out explicitly:** If a discount code targets a specific package_id that appears on more ITCs than the ticket specifies, surface those additional ITCs. The pricing team decides whether to widen scope or restrict via ITC filtering.

**CES ITC handling (Blast Radius Mode only):**

**FOS Price-Up Experiment Exception:** When ALL of the following are true — (1) ITC matches
`LIKE 'slp_%'` (FOS surface), (2) surface is CES (package_id null), AND (3) context signals a
treatment price HIGHER than the current catalog sale price (e.g. "+$2/mo", "premium → $16.99",
"price increase") — emit this block before any other CES output:

```
⚠️ CES FOS PRICE-UP EXPERIMENT DETECTED
Implementation path differs from a standard discount ticket.

FOS prices come from CES package tokens at render time — FOS can only show prices ≤ the
catalog sale price. To test a higher price, the pattern is:

1. Raise the PFID sale price to the treatment price (affects ALL customers immediately)
2. Create a discount code that nets back to the current (control) price
3. Create a new CONTROL CES package = PFID + discount code
4. Treatment CES packages = PFID only (renders raised price)

⚠️ ATOMIC DEPLOYMENT REQUIRED: pricing change + discount code + CES package + FoS publish
   must all deploy in a single coordinated window. Any step alone = site-wide pricing exposure.

Canonical playbook: https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4271539132/FOS+Experiments

Producing the PFID list and price baseline below. The Discount Ticket Summary will note
that TWO tickets are required: (1) sale price increase + (2) discount code for control.
```

**UPP exception:** For any ITC matching `LIKE 'upp_%'`, skip the merchandising API lookup entirely — UPP discount configuration goes through Hivemind, not the merchandising API. Still identify the PFID set for use in the Hivemind cohort JSON (see UPP Hivemind Configuration section below).

For all other CES-only ITCs (all `package_id` null), run a lightweight lookup to provide a slug reference for discount code configuration:

1. **Merchandising match:** Fetch `https://merchandising.api.godaddy.com/v1/packages`. Match the ITC's PFID set against `pfids[]` in each package. Classify as Exact, Superset, or Partial.
2. **ID list scan (fallback):** If no merchandising match, scan `get_curated_offers(active=true)` for keyword matches against the ITC or product name. Do not run tag search — that level of resolution is not needed for a pricing ticket.

Confidence levels:
- **High** — exact PFID match from merchandising API
- **Medium** — superset/partial merchandising match, or ID list keyword match
- **None** — all steps failed

---

## Output

**Render only after all work is complete.** Never render partial output.

**Always open with a Term Scope header:**

- Specific term: `TERM SCOPE: {N} {unit} (e.g. 1 Year)`
- Multiple terms: `TERM SCOPE: {N1} {unit1}, {N2} {unit2}`
- All terms: `TERM SCOPE: All terms — PFID list is cross-term. Confirm scope before filing.`

---

### PFID Inventory Mode Output

Before the PFID table, render a Flags table for any of these conditions. Omit entirely if nothing flags.

| Flag | Detail |
|---|---|
| Unexpected product match | PFID `{pfid}` — `{product_name}` does not appear to match the requested product |
| Zero US USD pricing | PFID `{pfid}` — no US USD transactions in the 30-day window |
| Segment filter exclusions | `{N}` PFIDs excluded — zero `{existing/new}` orders in window |

**PFID Inventory Table (all rows, no truncation)**

| PFID | Product Name | Term | Existing Orders | New Orders | Avg US Receipt Price | Avg US Regular Price | Avg US List Price | Avg US Catalog Sale Price |
|---|---|---|---|---|---|---|---|---|

End with: "N PFIDs across M term lengths."

---

### Blast Radius Mode Output

Before the PFID × ITC table, render a Flags table for any of these conditions. Omit entirely if nothing flags.

| Flag | Detail |
|---|---|
| Scope summary | `{N}` distinct PFIDs × `{M}` distinct ITCs in scope |
| UPP surface detected | One or more `upp_*` ITCs in scope — implementation path is Hivemind, not merchandising API. Path exclusions apply (BMAT, d2p). See UPP Hivemind Configuration section. |
| CES-only surface | `{itc}` (`{N}` orders/30d) has no `package_id` — discount mechanism differs from NES |
| Blast radius exceeds ticket scope | PFID `{pfid}` also appears on `{itc}` not listed in the ticket |
| Existing discount code | PFID `{pfid}` on `{itc}` currently has code `{code}` — will be overridden |

**Complete PFID × ITC Inventory (all rows, no truncation)**

| PFID | Product Name | Term | ITC | Package ID | Offer Type | Current Discount Code | Total Orders (30d) | Avg Receipt Price | Avg List Price | Avg Catalog Sale Price |
|---|---|---|---|---|---|---|---|---|---|---|

**CES Offer Candidates** *(rendered only when one or more non-UPP ITCs are CES-only and Step B2 CES lookup ran. UPP surfaces are excluded from this table — their discount path is Hivemind, not the merchandising API.)*

| ITC | PFID | Product Name | Term | Tier | Discount Code | Existing CES Package | Found Via | Confidence |
|---|---|---|---|---|---|---|---|---|

One row per PFID × Term within each CES ITC. Omit this table entirely if no CES ITCs exist.

Column definitions:
- **Term** — `product_term_num` + `product_term_unit_desc` combined (e.g. "1 Year")
- **Tier** — `product_pnl_subline_name`; if null, use `product_pnl_line_name`
- **Discount Code** — `item_discount_code` from B1; UUID placeholder → write "None"
- **Existing CES Package** — slug from merchandising match or ID scan; "Not found" if both failed
- **Found Via**: `Merchandising — exact`, `Merchandising — superset`, `Merchandising — partial`, `ID scan`, `—`
- **Confidence**: `High`, `Medium`, `None`

---

### Discount Ticket Summary

Labeled record block. Every field populated from query results. Write "None" or "N/A" if a field genuinely does not apply.

```
=== Discount Ticket Summary ===
PFIDs to include          :  {pfid1}, {pfid2}, ...
Package IDs (NES)         :  {package_id1}, {package_id2}, ... (or "None — CES only")
CES Slug Candidates       :  {slug} on {itc} (unconfirmed — see CES Offer Candidates above); or "None found"
ITCs in scope             :  {itc1}, {itc2}, ...
Price baseline            :  PFID {pfid} → avg receipt ${price} / avg list ${list} per term; ...
Existing codes to replace :  {code} on {itc} / PFID {pfid}; or "None"
```

The `CES Slug Candidates` line is omitted if the surface is 100% NES or if PFID Inventory Mode was used.

---

### UPP Hivemind Configuration

*Render only when one or more `upp_*` ITCs are present in B1 results. Render after the Discount Ticket Summary, before the Ticket Preview Prompt.*

> ⚠️ **UPP SURFACE — IMPLEMENTATION PATH IS HIVEMIND, NOT MERCHANDISING API**
>
> Discount experiments on `upp_*` surfaces are configured in Hivemind using a cohort JSON
> payload. The merchandising API and NES catalog are not in the UPP serving path.

**Path exclusions (silent — no error is returned):**
- **`d2p` conversion type** — direct-to-paid (new purchase) is not supported by UPP discount logic. ITCs containing `_d2p_` in the conversion_type segment are affected.
- **BMAT customers** (Bill Me After Trial) — excluded by ecom billing agent limitation.

**Hivemind configuration template:**

```
=== Hivemind Experiment Config ===
Experiment name suffix  :  {name}UPPDCX       ← "UPPDCX" suffix required
Label                   :  UPLIB               ← required; BOTH suffix AND label mandatory
Cohort JSON             :  { "WAM product": ["{DISC-CODE-1}"] }
                             key   = product type (e.g. "WAM product")
                             value = discount code strings from pricing team (DISC-##### format)
Propagation delay       :  ~25 min after saving before live
Max simultaneous codes  :  2 per UPP session (cart checkout limited to 1)
Bucketing               :  Shopper-level (logged-in users only)
```

**Test → Prod workflow:**
1. Build in test → add yourself to variant approved list → verify (allow ~25 min propagation)
2. "Copy to prod" creates a **separate copy** — does NOT promote the test experiment
3. In prod: open duration calculator → coordinate with BA team (not self-served for in-product)
4. Toggle traffic on → goes **live immediately** on toggle — be deliberate

**Concurrent experiment warning:** UPP applies the best (lowest) price across all active experiments for a shopper. Never run two concurrent pricing experiments on the same cohort — run sequentially or use separate variants.

---

## Multi-Surface Tickets

If the ticket mentions multiple surfaces (e.g. "DPP and SLP"), run the B1 query once per surface and produce one output block per surface. Do not merge them unless the analyst requests a combined view.

---

## Post-Output: Ticket Preview Prompt

After all output is rendered, append:

> "Would you like to see a draft of the **pricing or discount team ticket request**? I'll format it for copy-paste — no ticket will be created."

If yes, render the appropriate preview based on which B1 mode was used.

**HARD CONSTRAINT — READ ONLY:** Never call `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, or any write-capable Atlassian tool as part of this preview. Display only.

Do not show the preview if the analyst said they do not want a ticket, or if the output ended with no results.

---

### Ticket Preview — PFID Inventory Mode

*Render when PFID Inventory Mode was used in Step B1.*

```
=== Ticket Preview: Pricing / Discount Ticket Request ===

  Summary line (copy into Jira Summary field):
  [Pricing] {product name} — {term} — {market(s)} — {new/existing/both} — {discount target or price change description}

  Description:

  **PFIDs to apply discount / price change:**
  {one line per row in the PFID Inventory Table}
  - {pfid}: {product_name}, {term} — existing orders: {existing_orders}, new orders: {new_orders}
    Current avg US receipt: ${avg_us_receipt_price} | list: ${avg_us_list_price} | catalog sale: ${avg_us_catalog_sale_price}

  **Package IDs (NES curated offers, if applicable):** {package_id list or "None — CES only"}

  **ITCs in scope:** {from Discount Ticket Summary ITCs field}

  **Existing discount codes to replace:** {from Discount Ticket Summary — or "None"}

  **Term scope:** {from Term Scope header}

  **Market / Geo scope:** {markets from request}

  **Customer segment:** {new / existing / both}

  **Notes / flags for pricing team:**
  {one line per row in the Flags table — omit section if no flags}
  - {flag}: {detail}

  **Requested change:** [analyst to complete — e.g. "Apply DISC123456 to all PFIDs above on slp_wordpress for new customers, 1-year term"]

  Acceptance criteria:
  - [ ] Discount code applied to all PFIDs listed above
  - [ ] Code scoped to correct ITCs — no unintended blast radius
  - [ ] Existing codes verified as safe to override
  {if Flags table included "Zero US USD pricing" or "Unexpected product match":}
  - [ ] Flagged PFIDs reviewed and confirmed in scope
```

---

### Ticket Preview — Blast Radius Mode

*Render when Blast Radius Mode was used in Step B1.*

```
=== Ticket Preview: Pricing / Discount Ticket Request ===

  Summary line (copy into Jira Summary field):
  [Pricing] {product name} — {term} — {ITC(s)} — {market(s)} — {discount target or price change description}

  Description:

  **PFIDs × ITC combinations in scope:**
  {one line per distinct PFID × ITC pairing from the Complete PFID × ITC Inventory table}
  - {pfid} ({product_name}, {term}) on {itc}: offer type {NES/CES}, current code {code or "none"}, {N} orders/30d

  **Package IDs (NES):** {from Discount Ticket Summary Package IDs field}

  **CES slug candidates:** {from Discount Ticket Summary CES Slug Candidates field — or omit if NES only}

  **Existing discount codes to replace:** {from Discount Ticket Summary Existing codes field — or "None"}

  **Term scope:** {from Term Scope header}

  **Market / Geo scope:** {markets from request}

  **Customer segment:** {new / existing / both}

  **Notes / flags for pricing team:**
  {one line per row in the Flags table — omit section if no flags}
  - {flag}: {detail}

  **Requested change:** [analyst to complete]

  Acceptance criteria:
  - [ ] Discount code applied to all PFID × ITC combinations listed above
  - [ ] NES package ID discount configuration confirmed with ecomm
  - [ ] CES slug candidates confirmed with merchandising team before applying code
  - [ ] Blast radius verified — no unintended surfaces included
  {if Flags table included "Blast radius exceeds ticket scope":}
  - [ ] Out-of-scope ITCs reviewed and confirmed excluded
```

---

*No ticket action has been taken. All output above is for analyst review only.*
