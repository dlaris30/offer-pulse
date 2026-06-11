---
name: pricing-promo
description: Given a Jira pricing ticket, classify it and produce a complete validated promo configuration ready for PromoTool entry or PromoAPI submission. Targets DiscountCode Product Promos (OLG scope). Output is a structured field record, not XML.
---

# /pricing-promo

Takes a Jira pricing ticket key and returns a fully-specified promo configuration or a classification verdict (decline / describe-change).

## Invocation

```
/pricing-promo AGIGROWTH-161
/pricing-promo FOSMO-12345
```

Pass a ticket key. The skill fetches the full ticket, classifies intent, resolves all fields, and outputs a configuration record.

---

## Phase 1 — Ticket Intake

Fetch the ticket:

```
mcp__atlassian__getJiraIssue(cloudId="godaddy-corp.atlassian.net", issueIdOrKey="<KEY>")
```

Extract these fields before proceeding:

| Source | What to extract |
|---|---|
| summary | Promo code(s), product names, ticket intent verb (create / update / extend / clone) |
| description | Discount type and amounts, dates, currency scope, shopper eligibility, clone source code, PFID or product references |
| customfield_34656 | Surface (e.g. `slp_wordpress`, `dpp_precheck`) — overrides title/description when they conflict |
| customfield_14809 | Phase (new/renewal) |
| linked issues | Prior tickets, clone source reference |

Read both custom fields regardless of whether they appear in the summary. Values there override what the title says.

---

## Phase 2 — Classification

Classify to one of five outcomes. Work from the full ticket — summary, description, and custom fields together.

| Classification | Key signals | Next step |
|---|---|---|
| `DiscountCode_create` | "Create", "New code", "Launch"; no existing code as the modification target; promo code is alphanumeric+underscore, 1-64 chars; product-scoped award | Proceed to Phase 3 |
| `describe_change` | "Update", "Extend", "Modify", "Change", "Clone"; references an existing live code as the thing being changed | Describe which fields change; do not generate a full new config unless asked |
| `Standard_promo` | Short source code (<=10 chars, no underscore); Standard promo type signals; not WAM/discount-code context | Decline with explanation: Standard promos are not in scope; explain the type distinction |
| `ORDER_promo` | Cart-level, ISC code, order discount, minimum cart threshold | Decline with explanation: Order promos are not in scope for V1 generation |
| `decline_other` | Viral, All Shopper, Fastball, merch-only, offer edits, bundle config | Decline with explanation; name the promo type detected |

**When ambiguous between `DiscountCode_create` and `describe_change`:** default to `describe_change` and ask the analyst to confirm. Generating a new config when the intent was an update wastes EP capacity.

**Merch-only tickets** (no EP ticket expected, no PromoAPI config): decline immediately; do not produce a config. See [[feedback_merch_only_not_offer_pulse]] for signal patterns.

---

## Phase 3 — PFID Resolution (DiscountCode_create only)

PFIDs are required. Resolve before generating other fields.

**Clone path** (ticket references an existing code):

```sql
SELECT DISTINCT pf_id
FROM ba_gdii.product_promo_catalog
WHERE promo_code = '<SOURCE_CODE>'
  AND is_current_config = 1
ORDER BY pf_id;
```

Use connection `bi`. These are the starting PFIDs; apply any product scope changes stated in the ticket on top.

**Net-new path** (no clone source):

Flag PFIDs as `REQUIRES_INPUT`. If product name is in the ticket, run:

```sql
SELECT DISTINCT promo_code, pf_id
FROM ba_gdii.product_promo_catalog
WHERE promo_description ILIKE '%<PRODUCT_NAME>%'
  AND is_current_config = 1
LIMIT 20;
```

Return candidate codes and PFIDs for analyst review. Do not pick one without confirmation.

**PromoAPI direct path** (once access is granted):
When `GetStandardPromoByID` is available, use it for clone lookups instead of ba_gdii. It returns the live promo with exact current PFIDs and all other field values — more authoritative than the catalog view.

---

## Phase 4 — Field Generation

Generate all PromoAPI fields. Apply the rules below. Tag every field:

- `AUTO` — OLG default or direct extraction; high confidence
- `INFERRED` — rule-based derivation; reviewer should confirm
- `REQUIRES_INPUT` — cannot determine from ticket; must be resolved before submission

Never leave a field blank without a tag. Every gap must be visible.

### Fixed OLG defaults (always AUTO)

| Field | Value | Notes |
|---|---|---|
| `itemOrder` | 0 | HighestPriceFirst / MayOverlap; 99.94% of active promos |
| `isActive` | 1 | Set to 0 only for draft/staging; not typical for ticket flow |
| `isPhoneValidationEnabled` | 0 | Only enable for high-abuse-risk codes; not in scope |
| `promoEnabledCountryCodes` | "" | All markets; override only if ticket explicitly geo-restricts |
| `excludePriceTypes` | 0 | No restrictions; set to 456 (DDC) or 472 (DDC+Costco) only if ticket states it |
| `sourceCode` | "" | Blank for DiscountCode type; condition carries the code value |
| `bucketName` | "OLG-2026" | Internal grouping; do not change |
| `serverGroupID` | 0 | Legacy field; always 0 |
| `condRank` | 1 | Single-condition promos |
| `awardRank` | 1 | Single-award promos |
| `leaveAsUnadjusted` | 0 | Promo consumes the line item |
| `promoConditionRestriction` | 0 | No single-item buy restriction |
| `fieldName` (condition) | "discount_code" | Always for DiscountCode type |
| `fieldName` (award) | "pf_id" | Always |
| `relatedCondRank` | "1" | Always for DiscountCode type |

### Rank (AUTO with override check)

Default: `rank = 10` (96% of active promos).

Override to `rank = 5` only if ticket explicitly states this promo should override other active promos on the same product. Never guess; default to 10.

### Promo name / description (AUTO from ticket)

Map the offer name or promo code string to both `name` and `description` (PromoAPI maps the same value to both fields).

### Dates (AUTO from ticket; INFERRED if extrapolated)

Extract `startDate` and `endDate` directly from the ticket in `MM/dd/yyyy` format.

If only a campaign period is described without exact dates, mark as `INFERRED` and state the assumption. If dates are absent entirely, mark as `REQUIRES_INPUT`.

Note: end date scores conservatively (1.7% exact vs live state) because promos are often extended after creation. This does not indicate a generation problem; it reflects measurement method.

### Restriction (INFERRED from ticket; historically 100% accurate)

| Ticket signal | `isRestricted` | Notes |
|---|---|---|
| Public / all eligible shoppers / no gating | 0 | Most OLG codes |
| Targeted segment / gated distribution / restricted list | 1 | Set `restrictedOfferBatch` = promo code; set `restrictedPromoUseLimit` from ticket or -1 |
| New customers only | 2 | `RestrictedNewShoppersOnly` |
| New or inactive customers | 3 | `RestrictedNewShoppersOrInactiveCustomersOnly` |

When `isRestricted > 0`: also populate `restrictedOfferBatch` (= promo code) and `restrictedPromoUseLimit` (from ticket, or -1 if unlimited).

### ICANN fee suppression (AUTO; historically 98% accurate)

`suppressICANNFees = 0` by default.

Set to 1 only when both conditions are true: (a) the product is a domain product (TLD-based), AND (b) the ticket explicitly states ICANN fee suppression. If only one condition is true, default to 0 and flag as `INFERRED`.

### Use limit (INFERRED from ticket; historically 95% accurate)

`useLimit` = uses per purchase per cart, not a global cap.

| Ticket signal | `useLimit` |
|---|---|
| No limit stated / public code | -1 (unlimited) |
| "One per cart" / "single item" | 1 |
| Explicit number | that number |

Global cap (total redemptions across all shoppers) maps to `restrictedPromoUseLimit`, not `useLimit`.

### Usage type (INFERRED; historically 95% accurate)

`usageType = 1` (NotShopperRestricted) by default.

Set to 2 (ShopperRestricted) only if an explicit shopper ID restriction list is being configured. Usage type 3 (AllBaskets) is uncommon; do not use without explicit ticket instruction.

### Award type (INFERRED from ticket; historically 81% accurate)

| Ticket signal | XML element | Notes |
|---|---|---|
| "% off" / percent discount | `PercentDiscount discountAmount="N"` | N is the percent value as a string (e.g., "25" for 25%) |
| "$ off" / fixed discount | `PriceDiscount` with currency Discount elements | Amount in storage units (USD: cents; $10.00 = 1000) |
| "Fixed price" / "set price" | `PriceFixed` with currency Price elements | Storage units; for term products: target monthly price × term months |

When award type is ambiguous, output `REQUIRES_INPUT` rather than guessing.

### Currencies / amounts (INFERRED; historically 55% accurate)

Extract from ticket. For each currency:
- Currency code (USD, CAD, GBP, AUD)
- Award amount (convert to storage units: USD cents = amount × 100)

US+DEM tickets require separate treatment (see [[pricing_ticket_workflow_rules]]): US and DEM markets may need separate promo codes. Flag this if the ticket scope crosses US and non-US.

If currencies are not stated in the ticket, mark as `REQUIRES_INPUT`. Do not assume USD-only without confirmation.

### Award limit (INFERRED)

`awardLimit = -1` (unlimited) for percent-off codes.
`awardLimit = 1` for single-use codes or "one per cart" amount-off codes.

### Shopper restriction (INFERRED; historically 55% accurate)

This maps to `usageType` (per-shopper limit mode) or explicit shopper ID list, not to `isRestricted` (one-use-per-shopper restriction type).

When the ticket says "one use per shopper" or "targeted to specific shoppers": set `usageType = 2`.
When the ticket names a specific shopper list: mark as `REQUIRES_INPUT` (shopper IDs must come from the requester).

### PFIDs

Tag based on Phase 3 resolution:
- Clone path with successful ba_gdii lookup: `AUTO`
- Clone path pending PromoAPI access: `INFERRED` (catalog view is one step removed)
- Net-new: `REQUIRES_INPUT`

---

## Phase 5 — Output

### Quick Reference (default)

```
=== PROMO CONFIG ===
Ticket         : AGIGROWTH-161
Classification : DiscountCode_create
Promo Code     : <code>
Name           : <name>             [AUTO]
Start Date     : MM/DD/YYYY         [AUTO]
End Date       : MM/DD/YYYY         [AUTO]
Rank           : 10                 [AUTO]
Item Order     : 0                  [AUTO]
Usage Type     : 1                  [AUTO]
Is Active      : 1                  [AUTO]
Use Limit      : -1                 [AUTO]
Is Restricted  : 0                  [INFERRED]
Excl Price Types: 0                 [AUTO]
Bucket         : OLG-2026           [AUTO]
Suppress ICANN : 0                  [AUTO]
Award Type     : PercentDiscount     [INFERRED]
Discount Amt   : 25                  [AUTO]
Award Limit    : -1                 [AUTO]
Currencies     : USD                 [INFERRED]
PFIDs          : 1234567, 1234568   [AUTO / INFERRED / REQUIRES_INPUT]

REQUIRES_INPUT items:
- <list any fields flagged>
```

Adjust layout to match actual fields present. All `REQUIRES_INPUT` items must appear in a summary block at the bottom so they cannot be missed.

### Supporting Detail (on request only)

When the analyst asks, add:
- Generation rationale for each `INFERRED` field
- V2 scoring history reference (see scoring/v2-results.md)
- Relevant gotchas from generation-rules.md
- The ba_gdii query results used for PFID resolution

---

## Data Foundation

| Table | Use |
|---|---|
| `ba_gdii.product_promo_catalog` | PFID lookup for clone tickets; existing code inspection |
| `ba_gdii.order_promo_catalog` | Classification signal only (is this an ORDER promo?) |
| PromoAPI `GetStandardPromoByID` | PFID and full config lookup (pending access approval) |

Connections: use `bi` for all ba_gdii queries.

---

## Hard Constraints

- Never generate Order Promos or Viral Promos; decline and explain
- Never generate All Shopper promos; decline and explain
- Never fabricate PFIDs; mark `REQUIRES_INPUT` if unknown
- Never produce XML as primary output; output structured field records
- Never truncate PFID or currency lists; show all or flag all
- Never use em dashes; use semicolons or rephrase
- `isRestricted` controls one-use-per-shopper eligibility type; `restrictedPromoUseLimit` is the global cap for restricted promos; `useLimit` is uses per purchase per cart — these are three distinct fields
- `PercentDiscount` is for percent-based awards; `PriceDiscount` is for amount-off awards; do not conflate
- `product_award_element` for percent codes is `PercentDiscount`, not `PriceDiscount`
- Scores in generation-rules.md compare against live state, not creation-time state; treat as conservative lower bounds

---

## Vocabulary

| Term | Meaning |
|---|---|
| DiscountCode | Product Promo subtype where `fieldName = "discount_code"` and source code is blank. Supports 1-64 alphanumeric+underscore chars. Not the same as a generic promo code. |
| Standard promo | Product Promo subtype where `sourceCode` carries the code (max 10 chars, no underscore). Different field shape; out of scope for V1. |
| ORDER promo | Cart-level promo (ISC code); not product-scoped; out of scope for V1. |
| useLimit | Uses per purchase per cart (not a global cap). Default -1 = unlimited per cart. |
| restrictedPromoUseLimit | Global redemption cap for restricted promos. Separate field from useLimit. |
| isRestricted | One-use-per-shopper restriction type (0=none, 1=any shopper, 2=new shoppers only, 3=new or inactive). |
| suppressICANNFees | Boolean; waives the mandatory ~$0.18/year ICANN fee on .com registrations. Domain products only. |
| OLG | Internal grouping prefix; bucketName "OLG-2026" is standard for all OLG discount codes. |
| awardLimit | Award quantity per promo application (-1 = unlimited, 1 = single item per cart). |
| storage units | PromoAPI money encoding: USD $10.00 = 1000. Not Catalog API x10^6. |

---

## Reference

- generation-rules.md: field-level rules with evidence and pending questions
- scoring/v2-results.md: V2 scoring pass results (June 2026, 189 tickets)
- Confluence PromoAPI Field Definitions: https://godaddy-corp.atlassian.net/wiki/spaces/AGIGROWTH/pages/4441768155
- Herwin's PromoTool docs: Reference Docs/promo tool md files/ (promo-tool-capabilities, promo-api-xml-schemas, promo-catalog-usage, promotool-promo-types-explained, promo-tool-submission-workflow)
