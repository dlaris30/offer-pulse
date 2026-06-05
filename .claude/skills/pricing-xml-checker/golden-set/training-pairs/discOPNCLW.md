# Training Pair: discOPNCLW
**Ticket:** PRICING-15503
**Type:** DiscountCode — New creation
**Expected XML:** See `../discOPNCLW.xml`

## Raw Ticket

**Summary:** OpenClaw for GoDaddy VPS Coupon

**Description (key excerpt):**
> +++++++ Added by Pricing ++++++++
> USD only
> ++++++++++++++++++++++++++++
>
> A promotional discount coupon is required for the OpenClaw on GoDaddy VPS Early Access launch.
> Auto-applied via curated offer on the OpenClaw SLP.
>
> **Plan IDs & PFIDs:**
> - Starter: `lm00_20` (ex. PFID 1066865) — 2 vCPU / 4 GB / 100 GB NVMe
> - Pro: `lm00_40` (ex. PFID 1066904) — 4 vCPU / 8 GB / 200 GB NVMe
>
> **Source Offer:** `d29f7b62-9766-43bc-b230-353579eaad9c`
> **Tag:** `virtualPrivateServerHostingV4`
> **Pre-purchase key:** `openclaw`
>
> **Target Pricing (post-coupon):**
> | Term | Starter | Pro |
> | Monthly | $13.99/mo | $25.99/mo |
> | 3-month | $13.99/mo | $25.99/mo |
> | 6-month | $9.99/mo | $14.99/mo |
> | **12-month** ⭐ | **$8.99/mo** | **$12.99/mo** |
> | 24-month | $8.99/mo | $12.99/mo |
> | 36-month | $8.99/mo | $12.99/mo |
>
> Coupon stacks on top of existing sale price. New purchases only.

## Key Parameters Extracted

| Field | Value |
|---|---|
| Promo code | discOPNCLW |
| Product | VPS Gen4 Linux (2-CPU Starter + 4-CPU Pro) |
| Terms | 1mo / 3mo / 6mo / 12mo / 24mo / 36mo |
| Discount type | SetAmount (stacks on existing sale price) |
| Market | USD only (ticket says "USD only") |
| Eligibility | New purchases |
| Base PFIDs | 1066865 (Starter), 1066904 (Pro) |

## What the Deployed XML Shows

12 award rows (one per PFID), each with USD + INR:

| Term | Starter USD | Pro USD |
|---|---|---|
| 1mo | $13.99 | $25.99 |
| 3mo | $41.97 | $77.97 |
| 6mo | $59.94 | $89.94 |
| 12mo | $107.88 | $155.88 |
| 24mo | $215.76 | $311.76 |
| 36mo | $323.64 | $467.64 |

**INR was added by the implementer beyond ticket scope.** The ticket explicitly said "USD only." INR presence is an implementer decision, not ticket-driven.

AwardAmountType = Units (not Unlimited) — VPS promos use per-unit limits.

## Generation Notes

- Ticket gave base PFIDs only. Full per-term PFID set (1066865/70/73/74/77/80 for Starter, 1066904/07/09/10/12/14 for Pro) was resolved from catalog.
- INR: include only if ticket says India market is in scope. This ticket said USD only — INR was an implementer addition.
- Promo code is mixed case: `discOPNCLW` (lowercase "disc", then uppercase).
