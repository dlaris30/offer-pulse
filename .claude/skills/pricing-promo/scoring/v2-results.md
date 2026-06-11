---
type: scoring-results
scoring-pass: V2
date: 2026-06-05
tickets-evaluated: 189
correct-generates-scored: 60
fields-scored: 11
---

# Scoring Results — V2

## Setup

- 189 pricing tickets evaluated blind (no answers shown during generation)
- 60 tickets classified as DiscountCode creates and fully field-scored
- Comparison target: current live state in ba_gdii.product_promo_catalog

**Important:** Scores compare generated output against current live state, not original creation state. Promos that were extended or modified after creation will show as misses even if the original generation was correct. Treat all scores as conservative lower bounds.

## Classification Accuracy

66% overall across 189 tickets.

Main failure mode: Standard and ORDER tickets misclassified as DiscountCode creates, then scoring fails on subsequent field checks. Classification is the highest-leverage improvement area.

## Field Scores (60 correct DiscountCode creates)

| Field | Score | Tag in skill | Notes |
|---|---|---|---|
| Restriction (isRestricted) | 100% | INFERRED | Most reliable field; restriction intent is clearly stated in tickets |
| ICANN fee suppression | 98.3% | AUTO | Near-perfect; conservative default (don't suppress unless explicit) holds |
| Use limit | 95.0% | INFERRED | -1 vs 1 per cart is reliable when ticket language is clear |
| Usage type | 95.0% | INFERRED | Default 1 is almost always correct |
| Rank | 91.7% | AUTO | Default 10 holds; misses = non-standard rank explicitly in ticket |
| Award type | 81.4% | INFERRED | Early iterations: PercentDiscount vs PriceDiscount confusion; now explicit rule |
| Currencies | 55.0% | INFERRED | Multi-currency assumption gap; DEM tickets need separate codes |
| Shopper restriction | 55.0% | INFERRED | "Targeted" language ambiguous across isRestricted / usageType / shopper ID list |
| USD amounts | 51.9% | INFERRED | Storage unit conversion + multi-currency scope gaps |
| PFIDs | 50.0% | AUTO/INFERRED/REQUIRES_INPUT | Clone = catalog query; net-new = REQUIRES_INPUT |
| End date | 1.7% exact / 33.3% close | AUTO | Measurement artifact: live state vs creation state. Not a generation problem. |

## Priority Gaps

1. **Classification (66%):** Improve Standard vs DiscountCode signal detection. Use code format (max 10 chars / no underscore = Standard) as a strong discriminator.

2. **PFIDs (50%):** Net-new path requires manual input. Clone path via ba_gdii is functional. PromoAPI GetStandardPromoByID will close the clone gap entirely once access is available.

3. **Currencies / amounts (55%):** Tickets often omit non-USD amounts or assume single-market scope. Proposed fix: add "Currency Scope" field to Jira ticket template.

4. **Shopper restriction (55%):** Language ambiguity across three different field concepts. Proposed fix: add "Shopper Eligibility" field to Jira ticket template.

## Next Scoring Pass (V3)

Planned improvements before V3:
- Cleaner Standard vs DiscountCode classification using code format signals
- DEM market detection and flagging
- Award type rule update (PercentDiscount explicit rule already applied in skill post-V2)

Run against the same 189-ticket dataset plus any new tickets added since V2 to measure delta.
