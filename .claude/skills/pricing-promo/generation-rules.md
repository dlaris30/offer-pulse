---
type: reference
updated: 2026-06-05
description: Evidence base for pricing-promo field generation rules. One section per field group. Each section has: the rule, the evidence, the score (if measured), and open questions.
---

# Generation Rules — Evidence Base

This file explains *why* each rule exists. SKILL.md contains *what* to do. Update this file when:
- A new scoring pass changes a confidence level
- PromoAPI access reveals something different from the ba_gdii / xml-schema inference
- Herwin confirms or corrects a field behavior
- A real EP ticket outcome contradicts an INFERRED assumption

---

## Classification

**Rule:** Four-way classification (DiscountCode_create / describe_change / Standard / ORDER / decline_other). Default to describe_change when ambiguous.

**Evidence:** V2 scoring pass (189 tickets): 66% classification accuracy. Standard and ORDER tickets were the main misclassification source — they were incorrectly classified as DiscountCode creates, then failed field scoring. The conservative default (prefer describe_change over create when ambiguous) directly addresses this.

**Pending:** Improve signal detection for Standard vs DiscountCode. Key differentiator: Standard promo codes are max 10 chars with no underscore; DiscountCode allows up to 64 chars with underscore. This structural signal should be extractable from ticket text. Needs V3 validation.

---

## OLG defaults (itemOrder, isActive, isPhoneValidationEnabled, excludePriceTypes, bucketName, serverGroupID, condRank, awardRank, leaveAsUnadjusted, promoConditionRestriction)

**Rule:** Apply fixed values from the OLG defaults table in SKILL.md.

**Evidence:** Analysis of 3,335 active promos in ba_gdii.product_promo_catalog (2026-06-01):
- itemOrder=0: 99.94% of promos
- rank=10: 96% of promos
- isPhoneValidationEnabled=0: overwhelming majority; phone validation only for high-abuse-risk codes
- excludePriceTypes=0: majority; DDC/Costco exclusions are explicitly configured on relevant tickets

Schema source: Herwin's promo-api-xml-schemas.md (confirmed against PromoTool source models).

**Open question:** bucketName "OLG-2026" — should this be updated annually? Confirm with Herwin whether this changes each year or stays persistent.

---

## Rank

**Rule:** Default 10. Only use 5 if ticket explicitly requires overriding other active promos.

**Evidence:** V2 score: 91.7%. Misses were cases where non-standard rank was specified in the ticket and not extracted correctly. The rule is correct; extraction is the improvement area.

**Open question:** Are there rank values besides 5 and 10 in use? A DISTINCT query on active promos would confirm.

---

## Restriction (isRestricted / restrictedPromoUseLimit / restrictedOfferBatch)

**Rule:** 0 (no restriction) for public codes. 1-3 for targeted/gated distribution based on shopper eligibility language.

**Evidence:** V2 score: 100%. This was the strongest-scoring field. Restriction intent is reliably present in ticket language.

**Note:** restrictedPromoUseLimit = global cap (total redemptions). useLimit = per-purchase/per-cart limit. These are different fields. Herwin's XML schema says useLimit = uses per purchase; our Confluence Field Definitions page says "global cap" which is conceptually the restrictedPromoUseLimit. Pending Herwin confirmation to reconcile.

---

## ICANN fee suppression

**Rule:** 0 by default. 1 only when product is domain + ticket explicitly states suppression.

**Evidence:** V2 score: 98.3%. The rule is reliable. The 1.7% miss was a domain product where suppression was implied rather than stated; conservative default (don't suppress unless explicit) is correct.

**Definition:** ICANN charges ~$0.18/year per .com domain registration. suppressing it means GoDaddy absorbs the fee. Only applies to domain products (TLD-based). Must be an explicit business requirement, not assumed.

---

## Use limit

**Rule:** -1 (unlimited per cart) by default. 1 for "one per cart" or single-item codes.

**Evidence:** V2 score: 95.0%. The distinction between "unlimited" and "one per cart" is usually clear in ticket language. The per-cart (not global) semantics of useLimit are confirmed in Herwin's XML schema doc.

---

## Usage type

**Rule:** 1 (NotShopperRestricted) by default. 2 (ShopperRestricted) when explicit shopper ID list is configured.

**Evidence:** V2 score: 95.0%. Default is almost always correct; the rare override is explicitly described in tickets.

---

## Award type

**Rule:** PercentDiscount for percent-based, PriceDiscount for amount-off, PriceFixed for set-price.

**Evidence:** V2 score: 81.4%. Misses came from two patterns: (a) ambiguous "save $X" language that could be either amount-off or fixed-price, and (b) percent-based awards in early iterations incorrectly mapped to PriceDiscount instead of PercentDiscount. Rule is now explicit: percent = PercentDiscount (not PriceDiscount).

**Critical note:** For percent-based product promo awards, the correct XML element is PercentDiscount with discountAmount attribute. PriceDiscount is for fixed-dollar-amount-off awards. These are structurally different in the PromoAPI XML.

---

## Currencies / amounts

**Rule:** Extract from ticket. Convert to storage units (USD cents). Flag REQUIRES_INPUT if absent.

**Evidence:** V2 score: 55.0% (currencies), 51.9% (USD amounts). The low score reflects cases where currencies were assumed (USD-only) when the ticket actually required multiple currencies, or where DEM markets needed separate treatment. 

**DEM rule:** CA + AU + GB are DEM markets. US and DEM often require separate ticket / separate promo code due to pricing differences. Flag this at ticket intake if scope is multi-market.

**Storage units:** PromoAPI uses currency storage integers, not display dollars. For USD with 2 decimal places: $10.00 = 1000. This is NOT the same as Catalog Pricing API (which uses x10^6). Herwin's XML schema confirms this.

**Pending:** Once PromoAPI access is available, validate non-USD storage unit conversion using the GoDaddy currency cache (same approach PromoTool uses).

---

## Shopper restriction

**Rule:** Derived from usageType and isRestricted. Flag REQUIRES_INPUT for explicit shopper ID list.

**Evidence:** V2 score: 55.0%. Main miss: tickets using "targeted" or "segmented" language without specifying whether that meant isRestricted (one-use-per-shopper) or usageType (shopper-restricted mode) or a literal shopper ID list. These three fields serve different purposes and the distinction isn't always clear in tickets.

**Pending:** Propose adding explicit "Shopper Eligibility" field to Jira ticket template (tracked in Confluence Pricing Ticket Format Suggestions page). This would directly close this 55% gap.

---

## PFIDs

**Rule:** Clone path via ba_gdii lookup. Net-new path: REQUIRES_INPUT. Candidate lookup available via product_promo_catalog for product name hints.

**Evidence:** V2 score: 50.0%. This is the biggest mechanical gap. Clone-path tickets are solvable via catalog query; net-new tickets currently require human input.

**ba_gdii path:** `ba_gdii.product_promo_catalog` has 51,769 product promo codes, refreshed daily at 9AM UTC from DynamoDB event stream. Use is_current_config=1 for current PFIDs on a clone source. Use effective date range for historical reconstruction.

**PromoAPI path (pending):** GetStandardPromoByID returns the full live promo including all PFIDs. Once we have the mTLS cert or PromoTool proxy access, this becomes the primary path for clone tickets and eliminates the ba_gdii one-step-removed concern.

---

## End date (measurement note)

**Evidence:** V2 exact score: 1.7%, close score: 33.3%. This is a measurement artifact, not a generation problem. The evaluation compares our generated end date against the current live end date in ba_gdii — but promos are frequently extended after creation. A promo created with endDate = 12/31/2026 that was later extended to 06/30/2027 will show as a miss even if our generation was correct.

**Implication:** Do not use end date accuracy as a signal to change the generation rule. Extract from ticket as stated.

---

## Fields outside current scope

| Field | Status | Notes |
|---|---|---|
| Order promo (all fields) | Out of scope | Different XML shape, different classification |
| Viral promo (all fields) | Out of scope | Different XML shape; TLD/product-type/yard-value logic not built |
| All Shopper promo | Out of scope | No promo code; different condition structure |
| Fastball promo | Out of scope | Numeric code; system-triggered; different condition structure |
| Multi-condition promos | Known gap | EP-90729: multi-condition values combine into single cell in ba_gdii; cannot cleanly reconstruct. Treat as low-confidence/excluded. |

---

## Pending questions for Herwin

1. **Use limit API param name:** Our Confluence Field Definitions says the global cap field is "use_limit" — but Herwin's schema doc shows useLimit = per-purchase and restrictedPromoUseLimit = global cap. Which name is correct in the PromoAPI SOAP payload?

2. **bucketName annual rotation:** Does "OLG-2026" update each year, or is it a persistent label?

3. **Non-USD storage unit conversion:** What is the precise multiplier for CAD, GBP, AUD in PromoAPI storage units? Is it always cents-equivalent (2 decimal places)?

4. **PromoAPI read access timeline:** When will we have GetStandardPromoByID access? This closes the PFID gap for clone tickets.
