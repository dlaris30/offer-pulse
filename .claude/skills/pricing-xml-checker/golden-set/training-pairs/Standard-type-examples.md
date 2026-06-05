# Standard Type Examples — Reference Only

These tickets produced Standard-type XMLs, not DiscountCode. They are included in the training corpus so the generation skill can recognize and correctly decline these request types.

---

## EAKLEIN11 — PRICING-15643
**Type:** Standard — Premier customer discount (shopper-restricted)
**Signals:** Multiple shopper IDs in ShopperIdRestrictions, UsageType=ShopperRestricted, Type=Standard, Conditions block with ProductConditionV3, AwardAppliesTo=LowestPriceFirst (unique — only example with this value)
**Ticket ask:** COG-based pricing update for .ORG Premier Services codes, specific to two shopper accounts
**Why not DiscountCode:** Tied to specific shoppers, requires a purchase condition, uses Standard promo type

---

## GOINDIA — PRICING-15322
**Type:** Standard — Viral/phone-validated country promo
**Signals:** IsPhoneValidationEnabled=true, PromoEnabledCountryCodes (India dial codes), Bucket=ViralBucket26, UseLimit=1000000, Conditions block
**Ticket ask:** Recreate GOINDIA promo for India .IN/.CO.IN at INR 99, with phone validation, viral bucket, 1 per shopper
**Why not DiscountCode:** Phone validation + viral bucket = Standard type. INR-only currency, purchase condition required.

---

## COM1026 — PRICING-15499
**Type:** Standard — Shopper-specific (update ticket: add shopper)
**Signals:** Large ShopperIdRestrictions list, UsageType=ShopperRestricted, Type=Standard, Conditions block
**Ticket ask:** Add shopper 5326722 to existing promo COM1026 (.COM transfers at $10.26)
**Why not DiscountCode:** Adding a shopper to an existing Standard-type promo. Also an update, not a new creation.

---

## COM10 — PRICING-15498
**Type:** Standard — Shopper-specific (update ticket: add shopper)
**Signals:** ShopperIdRestrictions, UsageType=ShopperRestricted, Type=Standard, Conditions block
**Ticket ask:** Add shopper 454542230 to existing COM10 ($10 .COM transfer, bespoke client)
**Why not DiscountCode:** Bespoke client promo tied to specific shopper. Update ticket.

---

## COM985 — PRICING-15389
**Type:** Standard — Shopper-specific (new creation)
**Signals:** 1 shopper ID, Type=Standard, Conditions block, USD only
**Ticket ask:** Create promo COM985 for shopper 7053098, .COM transfers at $9.85, ~2500 domains
**Why not DiscountCode:** Tied to a specific shopper. Even though it's a new creation, the shopper restriction makes it Standard.

---

## LATAMMIG75 — PRICING-15601
**Type:** Standard — Care/service discount (update ticket: extend)
**Signals:** Type=Standard, Conditions block, AwardAmountType=Units, LATAM+UAE currency set only
**Ticket ask:** Extend voucher LATAMMIG75 by 6 months for LATAM+UAE migrations care discount
**Why not DiscountCode:** Care-issued voucher. Also an extend ticket, not new creation.

---

## WDSOFF11 — PRICING-15675
**Type:** Standard — Conditional PercentOff (update ticket: extend)
**Signals:** Type=Standard, Conditions block (must buy WDS product), AwardType=PercentOff, Restriction=Restricted
**Ticket ask:** Extend existing promo codes WDSOFF11/WDSOFF17/WDSOFF21 to end of Q3
**Why not DiscountCode:** Requires purchase of WDS product (Conditions). Also extend ticket.

---

## AIROBLD4U — PRICING-15568
**Type:** Standard — Conditional PercentOff (influencer campaign, new creation)
**Signals:** Type=Standard, Conditions block, AwardType=PercentOff (100%), UseLimit=50, AwardAmountType=Units, Restriction=Restricted
**Ticket ask:** Create coupon codes for Influencers.club campaign for Airo AI Builder, 50 redemptions max, 1 per account, free 1yr Starter plan
**Why not DiscountCode:** Purchase condition (must buy product to get free), campaign-style distribution cap. UseLimit=50 at promo level (not per-shopper).

---

## PHP9D15D6A — PRICING-15608
**Type:** DiscountCode but non-standard structure
**Signals:** Type=DiscountCode, AwardType=PercentOff (100%), Two PrivateLabels (PL1 + PL 587240), no AwardCurrencies
**Ticket ask:** Validate and extend PHP9D15D6A for cPanel PHP monetization add-on
**Note:** This IS DiscountCode type but has a second PrivateLabel (587240) that breaks checker rule S2. The dual PrivateLabel indicates a white-label/reseller variant. When generating, PL1 is standard — additional PLs indicate specific channel deployments not derivable from the ticket alone.
