# Training Pair: NoAMTxFee1
**Ticket:** PRICING-15534
**Type:** DiscountCode — New creation (PercentOff, Restricted, A/B test)
**Expected XML:** See `../NoAMTxFee1.xml`

## Raw Ticket

**Summary:** Waive Domain Registration/Transfer Fee on Aftermarket Premium Purchases | A/B Test (AGIGROWTH-168)

**Description:** (inferred — ticket details reference AGIGROWTH-168 A/B test)
> Waive the domain registration/transfer fee on aftermarket premium purchases.
> A/B test component of AGIGROWTH-168.
> 100% off the fee PFIDs (domain registration/transfer).
> Restriction: Restricted (experiment cohort targeting)
> PFIDs: 111, 12011, 12111, 780, 781, 782 (domain registration/transfer fee PFIDs)

## Key Parameters Extracted

| Field | Value |
|---|---|
| Promo code | NoAMTxFee1 |
| Product | Domain aftermarket registration/transfer fees |
| Discount type | PercentOff (100%) = free |
| Market | Not currency-specific — fee waiver has no amount |
| Restriction | Restricted (A/B test cohort) |
| AwardAmountType | Unlimited |

## What the Deployed XML Shows

- AwardType = **PercentOff** with PercentOff = 100
- **No AwardCurrencies element** — PercentOff promos have no currency amounts
- Restriction = `Restricted` (used for A/B test experiments)
- StartDate = 2026-04-19, ExpirationDate = 2026-10-21 (~6 months, experiment duration)

## Generation Notes

- PercentOff promos never have AwardCurrencies. Checker rule C3 enforces this.
- `Restriction=Restricted` is used for experiment targeting — not the same as shopper restriction. The code is still NotShopperRestricted but has Restriction=Restricted.
- Mixed-case promo code (`NoAMTxFee1`) is legitimate — casing follows ticket exactly.
- 6 domain fee PFIDs: 111 (domain reg), 12011, 12111 (bulk), 780-782 (transfer variants).
