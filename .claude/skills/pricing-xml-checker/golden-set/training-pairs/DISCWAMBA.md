# Training Pair: DISCWAMBA
**Ticket:** PRICING-15396
**Type:** DiscountCode — New creation (single-use per shopper)
**Expected XML:** See `../DISCWAMBA.xml`

## Raw Ticket

**Summary:** Discount Code for MHWP Basic, 80% off list price (term 1 year)

**Description:** (inferred from XML name/description — ticket description minimal)
> Discount Code for MHWP Basic, 80% off list price (term 1 year) PRICING-15396
> Eligibility: New customers + Inactive customers
> UseLimit: 1 (one use per shopper)
> PFID: 1320692 (MWP Basic 1-year)

## Key Parameters Extracted

| Field | Value |
|---|---|
| Promo code | DISCWAMBA |
| Product | Managed Hosting for WordPress Basic |
| Term | 1-year |
| Discount type | SetAmount (80% off list, = final price) |
| Market | Global (full currency set) |
| Eligibility | New + Inactive customers |
| UseLimit | 1 per shopper |
| Base PFID | 1320692 |

## What the Deployed XML Shows

- AwardAmountType = **Units** (not Unlimited) — because UseLimit=1
- AwardQuantity = 1, UseLimit = 1
- 31 currencies in award (full global set)
- Restriction = `RestrictedNewShoppersOnlyAndInActiveCustomersOnly`
- USD not included in list — wait, actually USD is absent from DISCWAMBA. Let me check... looking at the XML, I don't see USD in the currencies. This is interesting — DISCWAMBA targets new+inactive and uses a full international currency set but no USD.

Actually reviewing the XML: TWD, CHF, EUR, SGD, JPY, NZD, PKR, PEN, MYR, PLN, SAR, AED, ILS, BRL, DKK, CLP, CNY, HKD, NOK, SEK, ZAR, KRW, MXN, CZK, TRY, THB, COP, PHP, INR, IDR, VND — no USD, no GBP. This is a non-US promo despite not being labeled as ROW explicitly.

## Generation Notes

- UseLimit=1 drives Units instead of Unlimited — a single-use promo always uses Units.
- Restriction field is not NoRestriction — it reflects the eligibility constraint from the ticket.
- The absence of USD is notable — this may be an international-only promo or USD was intentionally excluded.
- Full currency set without USD/GBP is unusual — worth flagging in generation if ticket says US market.
