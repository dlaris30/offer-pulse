# Training Pair: DISCMWPB5
**Ticket:** PRICING-15704
**Type:** DiscountCode — New creation
**Expected XML:** See `../DISCMWPB5.xml`

## Raw Ticket

**Summary:** Create Discount Code for US: Wordpress Basic on WH Economy SLP - 36m Offer

**Description:**
> Ask: Create Discount Code for Wordpress Basic - 36m, $5.99->$4.99 test
> Eligibility: New customers + Existing
> Markets: US
> "description": "Wordpress Basic - 3 year"
> PFID: 1320704 (Basic Managed Hosting for WordPress, 3-year, new purchase)
>
> Discount code will be attached to the clone of `wordpress-o365-forever-ssl-basic`
>
> Discount code: **DISCMWPB5**

## Key Parameters Extracted

| Field | Value |
|---|---|
| Promo code | DISCMWPB5 |
| Product | Managed WordPress Basic |
| Term | 36-month (primary) |
| Target price | $4.99/mo |
| Market | US only |
| Eligibility | New + Existing |
| Source clone | `wordpress-o365-forever-ssl-basic` |
| Base PFID | 1320704 |
| Discount type | SetAmount |
| Currency | USD only (US market) |

## What the Deployed XML Shows

The deployed promo expanded to 4 term tiers (same pattern as DISCWHECON) with 2 PFIDs per award row via clone inheritance:

| Award | PFIDs | USD Amount | Calculation |
|---|---|---|---|
| 1 (36mo) | 1320704, 580982 | $179.64 | $4.99 × 36 |
| 2 (48mo) | 1320707, 580985 | $239.52 | $4.99 × 48 |
| 3 (60mo) | 1320710, 580988 | $299.40 | $4.99 × 60 |
| 4 (120mo) | 1320713, 580991 | $598.80 | $4.99 × 120 |

Rank is 80 (not the standard 10) — consistent with DISCWHECON, suggesting clone-based US hosting promos use rank 80.

## Generation Notes

- Ticket specified only the 36-month PFID. All 8 PFIDs came from cloning `wordpress-o365-forever-ssl-basic`.
- USD only — US-market scope confirmed.
- Rank 80 is notable: matches DISCWHECON exactly. Clone-based US hosting/WAM promos consistently use rank 80.
- StartDate matches DISCWHECON (2026-05-26) — both deployed same day.
