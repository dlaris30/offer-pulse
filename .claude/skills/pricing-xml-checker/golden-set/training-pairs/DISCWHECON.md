# Training Pair: DISCWHECON
**Ticket:** PRICING-15666
**Type:** DiscountCode — New creation
**Expected XML:** See `../DISCWHECON.xml`

## Raw Ticket

**Summary:** Create Discount Code for US: WH Economy - 36m Offer

**Description:**
> Ask: Create Discount Code for WH Economy - 36m, $5.99->$4.99 test
> Eligibility: New customers + Existing
> Markets: US
> "description": "Web Hosting Economy - 3 year"
> PFID: 1338734 (WH Economy Linux cPanel 3-year, new purchase)
>
> Discount code will be attached to the clone of `cpanel-set-1-economy-ssl-365-wss-xtra`
>
> Discount code: **DISCWHECON**

## Key Parameters Extracted

| Field | Value |
|---|---|
| Promo code | DISCWHECON |
| Product | Web Hosting Economy |
| Term | 36-month (primary) |
| Target price | $4.99/mo |
| Market | US only |
| Eligibility | New + Existing |
| Source clone | `cpanel-set-1-economy-ssl-365-wss-xtra` |
| Base PFID | 1338734 |
| Discount type | SetAmount |
| Currency | USD only (US market) |

## What the Deployed XML Shows

Clone of `cpanel-set-1-economy-ssl-365-wss-xtra` inherited 4 term tiers with 9/4/9/9 PFIDs:

| Award | PFIDs | USD Amount | Calculation |
|---|---|---|---|
| 1 (36mo) | 9 PFIDs | $179.64 | $4.99 × 36 |
| 2 (48mo) | 4 PFIDs | $239.52 | $4.99 × 48 |
| 3 (60mo) | 9 PFIDs | $299.40 | $4.99 × 60 |
| 4 (120mo) | 9 PFIDs | $598.80 | $4.99 × 120 |

Rank 80 — consistent with DISCMWPB5. Clone-based US hosting promos use rank 80.

## Generation Notes

- Ticket named only 1 PFID. All 31 PFIDs came from cloning the curated offer collection.
- USD only confirmed by US-only market scope.
- Start date was **May 26** — ticket was last updated May 27 (Alexandra Anderson narrowed from US+DEM+ROW to US-only), deployed May 28.
