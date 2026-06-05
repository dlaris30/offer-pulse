# Promo Type Reference

When given a pricing ticket, the first decision is whether to generate XML, describe a change, or decline. This reference covers all patterns observed across 25+ tickets.

---

## Step 1 — Classify the ticket

### DiscountCode — New creation (generate XML)
The ticket asks for a **new** discount code to be created. Key signals:
- "Create Discount Code for..."
- "Create a new promo code..."
- "Discount code: [NEW CODE]"
- Ticket has a proposed new promo code name
- No reference to modifying an existing deployed code

**Generated XML uses:** `<Type>DiscountCode</Type>`, `<Conditions />` (empty), no ShopperIdRestrictions

### DiscountCode — Update/extend (describe the change, do not generate full XML)
The ticket modifies an **existing** deployed code. Key signals:
- "Add [currency/shopper/PFID] to [existing code]"
- "Extend the expiration of [code]"
- "Currency refresh on [code]"
- "Validate and extend [code]"
- The code already exists in prod

**Action:** Describe the specific field change (e.g., "Add CAD currency row to award X with amount Y" or "Update ExpirationDate from X to Y"). Do not generate a full XML from scratch.

### Standard type — Shopper-restricted (decline, explain)
Promo tied to specific named customers. Key signals:
- "For Shopper [ID]"
- "Add Shopper [ID] to..."
- "Bespoke client offer"
- "Premier customer"
- ShopperIdRestrictions with explicit shopper IDs
- `UsageType=ShopperRestricted`

**Action:** Decline generation. Explain this is a Standard-type shopper-restricted promo — not a DiscountCode. These require manual configuration by the pricing ops team.

### Standard type — Viral/phone-validated (decline, explain)
Country-targeted promos with phone validation. Key signals:
- "Phone validation"
- "Viral bucket"
- "PromoEnabledCountryCodes"
- Country-specific campaigns (India, etc.)
- `IsPhoneValidationEnabled=true`

**Action:** Decline generation. Standard type with phone validation — outside DiscountCode scope.

### Standard type — Conditional (decline, explain)
Promo requires a purchase trigger. Key signals:
- "Buy X to get Y"
- "Free X with purchase of Y"
- "Must purchase [product] to receive discount"
- Any Conditions block with ProductConditionV3

**Action:** Decline generation. Standard type with purchase condition — outside DiscountCode scope.

### Standard type — Care/service discount (decline, explain)
Customer care-generated codes. Key signals:
- "Care discount"
- "Care agent"
- "Migration discount"
- Regional care operations (LATAM, etc.)

**Action:** Decline generation. These are care-issued vouchers with limited currency sets and are configured manually.

### Maintenance ticket (acknowledge, do not generate)
Periodic reviews of existing codes. Key signals:
- "Currency refresh"
- "Review and update PFIDs"
- "Bi-monthly review"
- References to existing code names without "create"

**Action:** Acknowledge the ticket type. Note that currency refresh requires running current FX rates against existing amounts — this is a data operation, not a new XML generation.

---

## Step 2 — For DiscountCode new creation, identify promo subtype

### SetAmount — Target price promo
Most common. Ticket specifies a target price per term.
- Award amounts = target_monthly × term_months in USD (and other currencies)
- AwardType = SetAmount
- AwardCurrencies present and non-empty

### PercentOff — Percentage discount
Ticket specifies a percentage reduction.
- PercentOff value = the percentage (e.g., 100 for free, 11 for 11% off)
- AwardType = PercentOff
- No AwardCurrencies element

### UsageType — Use limit
Some codes are restricted to one use per shopper.
- UseLimit = 1, AwardQuantity = 1, AwardAmountType = Units
- Distinguished from Unlimited by whether the ticket says "1 per shopper", "single use", etc.

---

## Step 3 — Determine currency scope from market

| Market stated in ticket | Currency set to use |
|---|---|
| US only | USD only |
| DEM only | EUR, GBP, CAD (DEM currencies) |
| ROW only | Non-USD currencies; no USD |
| ROW + IN | Non-USD currencies including INR |
| US + DEM + ROW | Full global currency set |
| India only | INR only |
| LATAM | BRL, CLP, COP, MXN, PEN (plus USD if stated) |
| Global / not specified | Full global currency set |

**Non-USD amounts are FX-converted.** The exact amounts are not derivable from the ticket — they require a FX table. Flag this in the output and use USD as the anchor.

---

## Promo code naming patterns observed

| Pattern | Examples | When used |
|---|---|---|
| DISC + ticket number | disc15265, DISC15278 | WAM sale codes |
| DISC + product abbreviation | DISCWHECON, DISCMWPB5, DISCWAMBA | Product-specific codes |
| DISC + campaign name | discOPNCLW, DISCWAMUP3 | Campaign codes |
| Alphanumeric | 365AF1F1CB, PHP9D15D6A | M365 / technical codes |
| Marketing phrase | NoAMTxFee1, GOINDIA, AIROBLD4U | Brand/campaign codes |
| Premier client code | COM10, COM985, EAKLEIN11 | Bespoke client codes (Standard type) |

Casing is not standardized — it follows whatever the ticket specifies. If the ticket provides a code, use it exactly. If no code is provided, propose one following the relevant pattern above and flag it for confirmation.
