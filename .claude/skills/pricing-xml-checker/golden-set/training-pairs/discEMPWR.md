# Training Pair: discEMPWR
**Ticket:** PRICING-15371
**Type:** DiscountCode — New creation (global cap, targeted distribution, bundle)
**Expected XML:** See `../discEMPWR.xml`

## Key Parameters

| Field | Value |
|---|---|
| Promo code | discEMPWR |
| Product | .com domain (1yr) + WAM Commerce (multi-term) bundle |
| Discount type | PercentOff 100% — free bundle |
| Market | US (USD only, no AwardCurrencies) |
| Restriction | Restricted — targeted student distribution, controlled channel |
| UseLimit | 50000 — global cap ("50,000 bundles is cap for offer") |
| NumberOfUses | 2 — one per award (domain award + WAM Commerce award) |
| AwardAmountType | Units |
| Name | PRICING-15371 GoDaddy Empower Student Distribution 2026 (ticket number + full title verbatim) |

## What This Example Teaches

**UseLimit = global cap, not per-shopper only.** "50k bundles cap" → `<UseLimit>50000</UseLimit>`. Previously the rule said UseLimit encodes per-shopper restriction only. This confirms UseLimit also encodes a global total redemption cap when the ticket specifies one.

**NumberOfUses = award count.** Two awards (domain + WAM Commerce) → NumberOfUses=2, even though ticket says "1 use per purchase." NumberOfUses is not a literal reading of the ticket — it equals the number of ProductAwardV2 entries.

**Restriction=Restricted for targeted distribution.** Not an A/B experiment — a student distribution campaign with a cap and a controlled audience. Signals: named audience (students), explicit cap, distributed via controlled channel.

**Name includes ticket number + verbatim title.** Third confirmed example of this convention alongside discOPNCLW and DISCWAMBA. Pattern: external programs, partner/distribution campaigns, niche non-sale codes.

**SuppressIcannFees split.** Domain award: true. WAM award: false. Rule: domain PFIDs always get SuppressIcannFees=true.

**AwardId ordering.** Domain award is AwardId=2 (listed first), WAM is AwardId=1 (listed second). AwardIds are not always in ascending document order — assigned by the admin system, not the implementer.

## Generation Result (PRICING-15371 run 2026-06-04)

| Field | Generated | SSOT | Result |
|---|---|---|---|
| ExpirationDate | 2027-01-01 | 2027-01-01 | ✅ |
| PromoCode | discEMPWR | discEMPWR | ✅ |
| AwardType | PercentOff | PercentOff | ✅ |
| AwardAmountType | Units | Units | ✅ |
| AwardQuantity | 1 | 1 | ✅ |
| PercentOff | 100 | 100 | ✅ |
| SuppressIcannFees (domain) | true | true | ✅ |
| SuppressIcannFees (WAM) | false | false | ✅ |
| Two-award structure | ✅ | ✅ | ✅ |
| StartDate | 2026-06-04 (today proxy) | 2026-03-18 | ❌ approximate |
| UseLimit | 1 | 50000 | ❌ misread global cap as per-shopper |
| NumberOfUses | 1 | 2 | ❌ literal read vs award count |
| Name | Free 2-Year .com and WAM Commerce Bundle | PRICING-15371 GoDaddy Empower Student Distribution 2026 | ❌ missed team convention |
| Restriction | NoRestriction | Restricted | ❌ rule gap (targeted distribution) |
