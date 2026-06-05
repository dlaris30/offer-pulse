---
name: pricing-xml
description: Given a Jira pricing ticket, classify it and produce a deployable ProductPromo XML for new DiscountCode creation. Correctly identifies and declines update, Standard-type, and deactivation requests.
---

# /pricing-xml — Pricing XML Generator

Given a Jira pricing ticket, determine what type of request it is and produce the correct output. Only new DiscountCode creation tickets produce XML.

---

## Step 1 — Classify the ticket

**Four outcomes. Determine this before doing anything else.**

**→ Generate XML** when the ticket creates a new discount code from scratch with no shopper restrictions and no purchase condition required.
Signals: "Create Discount Code for…" · "Discount Code: DISCXXX" · "added by pricing" block with a code name

**→ Describe the change only** when the ticket modifies an existing code.
Signals: "update code X" · "extend expiry" · "add PFID to" · "add shopper to" · "currency refresh"

**→ Decline** when the ticket is a Standard-type promo. Explain why and stop.
Signals: named shopper IDs · phone validation · viral bucket · "Premier Services" · "bespoke client offer" · purchase condition required ("must have .COM in cart")

**→ Don't generate** for deactivation, disable, or "remove PFID from" requests.

**Ticket type hints:**
- Jira type `Sanctioned Price Execution` → almost always Standard type or update
- Jira type `Pricing Experiment` → usually an update to an existing code
- Jira type `Promo Code` + "added by pricing" block → generate
- `PFID Management` ticket → only generate if it contains an explicit "added by pricing" block with a code name

**Multi-code tickets:** One ticket can create multiple codes. State "This ticket creates N codes" and generate one XML per code.

---

## Step 2 — Read the ticket

**The "added by pricing" block overrides everything else.** When the pricing team has annotated a ticket filed by another team, their block (typically surrounded by `++++` lines) contains the authoritative code name, PFIDs, and pricing intent.

**Ticket evolution:** Tickets are amended. Use the most recent version of the description only.

**Implementer comments** confirm PFIDs and deployment details — but never use comment casing for the PromoCode. The ticket body is authoritative.

**Ask before generating if:**
- No promo code is named anywhere in the ticket
- No target price or percentage is stated
- No PFID is stated and no clone is referenced

---

## Step 3 — Generate the XML

### PromoCode
Use the exact code from the ticket body. Preserve casing character-for-character.

Common patterns (not always followed — trust the ticket):
- `disc` + ticket number → `disc15200` for PRICING-15200
- `DISC` + product abbreviation → `DISCWHECON`, `DISCWAMBA`
- Free-form → `NETSERP671`, `NoAMTxFee1`, `365AF1F1CB`, `GDWELCOME`

### StartDate
The date the promo is deployed and active in the system — **not** the campaign go-live date. When a ticket says "from [date]" or "live from [date]", that is when the surface team activates their offer, not when the code itself starts.

Use the ticket creation date as a proxy. Only use a future StartDate when the ticket explicitly says "do not activate before [date]."

### ExpirationDate
Use the date stated in the ticket. Midnight convention: "until March 29" → `2026-03-30T00:00:00`.

When no end date is given:

| Promo type | Default ExpirationDate |
|---|---|
| A/B experiment | `[deployment year + 1]-01-01` |
| Short campaign | Calculate from ticket dates |
| Standing / bundle offer | Long-dated (e.g. `2036-01-01`) |
| Evergreen, no planned end | `2099-01-01` |

Do not default to `2099-01-01` for experiment codes.

### Name and Description
Always identical to each other. 5–10 words. Reflect the spirit of the ticket — not the implementation details.

- A/B experiment → include "A/B Experiment": `Discount for A/B Experiment 50% off DOP`
- Bundle → include total: `Solution Set for Domain, EE, DOP, and WAM Lite - 47.88`
- Standard offer → product + context + price: `50% off WAM Monthly`
- Regional offer → `Discount Code for US: WH Economy - 36m Offer`

No ticket number in the name unless the ticket or program convention calls for it. Observed in corpus: three codes include the ticket number (discOPNCLW, DISCWAMBA, discEMPWR); the remainder do not. No confirmed rule for when to include it — when in doubt, omit it and flag the assumption. Match product capitalisation from the ticket (`.UK` not `.uk`).

### AwardType
- Ticket gives a target price → `SetAmount`. AwardCurrencies required.
- Ticket gives "X% off" → `PercentOff`. No `<AwardCurrencies>` element at all.

### SetAmount calculation
`DiscountAmount = target_monthly_price × number_of_months`

Examples: `$4.99 × 36 = $179.64` · `$8.99 × 12 = $107.88` · `$0.99 × 12 = $11.88`

For bundle codes, verify the component amounts sum to the stated bundle total.

### What an award is
An award is a **price tier** — a group of PFIDs that all receive the same discounted price. Multiple PFIDs share one award when they should cost the same. Multiple awards exist when different groups of PFIDs have different prices (different plan tiers, different term lengths).

Each award contains: the PFID list + the price in every relevant currency.

### AwardAmountType, UseLimit, NumberOfUses

| Scenario | AwardAmountType | UseLimit | AwardQuantity | NumberOfUses |
|---|---|---|---|---|
| Standard promo | `Unlimited` | nil | nil | nil |
| A/B experiment | `Unlimited` | nil | nil | `1` |
| Use-limited code | `Units` | [value from ticket] | `1` | [see note] |

`UseLimit` — encode the numeric limit from the ticket directly. Observed: UseLimit=1 (per-shopper, DISCWAMBA), UseLimit=50000 (total cap, discEMPWR). The system takes whatever the ticket states.

`NumberOfUses` — observed values: nil (Unlimited codes), 1 (A/B experiment; single-award Units codes), 2 (two-award Units bundle, discEMPWR). The pattern for Units codes appears to be award count, but confirmed on only 2 examples. When generating a Units code with multiple awards, use the award count and note the assumption.

**Source:** discEMPWR (PRICING-15371) — "50,000 bundles is cap for offer" → UseLimit=50000; two-award bundle (domain + WAM) → NumberOfUses=2.

### Restriction

| Ticket says | Value |
|---|---|
| No restriction stated | `NoRestriction` |
| A/B experiment / experiment cohort | `Restricted` |
| Code is not freely available — requires eligibility, a specific channel, or cohort membership to access | `Restricted` |
| New customers + inactive customers only | `RestrictedNewShoppersOnlyAndInActiveCustomersOnly` |
| Named shoppers | Standard type — decline |

**Source:** discEMPWR (PRICING-15371) — student distribution with 50k cap → `Restricted`, not `NoRestriction`. Rule previously only covered A/B experiments.

### Rank
Default `10`. Use `80` only when all three apply: ticket says "clone of [offer]" + product is Hosting or MWP + market is US only.

### Currency scope

| Market | Currencies |
|---|---|
| US only | USD only |
| UK / GBP-specific | GBP only |
| DEM (CA + AU + GB) | CAD, AUD, GBP |
| India only | INR only |
| ROW only | Non-USD regional currencies, no USD |
| ROW + India | Non-USD including INR |
| LATAM | BRL, CLP, COP, MXN, PEN |
| Global / not stated | Full set (~35 currencies) |

Note: DEM = Canada + Australia + UK. Germany is ROW, not DEM.

Non-USD amounts require FX conversion. Output `[FX REQUIRED]` as a placeholder — the implementer fills these in. Only the USD anchor amount (or named anchor currency) can be calculated directly from the ticket.

### PFID set
Use only PFIDs explicitly stated in the ticket or confirmed by an implementer comment.

When a ticket says "clone of [offer-slug]": the deployed promo inherits all PFIDs from that cloned offer — potentially 10–30 more than the ticket names. Use the stated base PFID only and flag: "Full PFID set requires catalog lookup."

Do not pull PFIDs from similar tickets. US-only and experiment codes use a tighter subset than global launches of the same product.

---

## Step 4 — Structural requirements

Every valid DiscountCode XML must include these exactly:

```xml
<Conditions />
```
Always empty. Never add child elements.

```xml
<AwardAppliesTo>HighestPriceFirstMayOverlapConditions</AwardAppliesTo>
```
Always this exact value.

```xml
<PrivateLabels>
  <PrivateLabelV2>
    <PrivateLabelID>1</PrivateLabelID>
    <IsActive>true</IsActive>
    <StartDate>0001-01-01T00:00:00</StartDate>
    <EndDate>0001-01-01T00:00:00</EndDate>
    <New>false</New>
    <Remove>false</Remove>
  </PrivateLabelV2>
</PrivateLabels>
```
Always PL1.

**Never include:**
- `<PFIDList>` block
- Child elements inside `<Conditions>`
- `<AwardCurrencies>` when AwardType is `PercentOff`

---

## Step 5 — Pre-output checklist

- [ ] PromoCode casing matches ticket body exactly (not comment)
- [ ] StartDate is deployment date, not campaign go-live date
- [ ] ExpirationDate uses the right convention for this promo type
- [ ] Name equals Description exactly
- [ ] Name is 5–10 words, reflects ticket intent, no ticket number
- [ ] `<Conditions />` is empty
- [ ] `<PrivateLabels>` contains PL1
- [ ] `<AwardAppliesTo>` is present and correct
- [ ] No `<PFIDList>` block anywhere
- [ ] PercentOff awards have no `<AwardCurrencies>` element
- [ ] SetAmount awards have non-empty `<AwardCurrencies>`
- [ ] No PFID appears in more than one award row
- [ ] `Restriction=Restricted` if ticket signals A/B experiment
- [ ] `NumberOfUses=1` if A/B experiment

---

## Known failure patterns

Confirmed errors from real test runs — check these every time.

| Field | Common mistake | Correct behaviour |
|---|---|---|
| `PromoCode` | Used casing from implementer comment | Ticket body is authoritative |
| `StartDate` | Used campaign go-live date | Use deployment / ticket creation date |
| `ExpirationDate` | Defaulted to 2099 for experiment codes | Experiments → `year+1-01-01` |
| `Name` / `Description` | Verbose, included ticket number and prices | Short (5–10 words), spirit of ticket |
| PFID set | Pulled from similar-looking training example | Only ticket-specified PFIDs; flag clone gaps |
| `Restriction` | Defaulted to `NoRestriction` for A/B test | A/B experiment → `Restricted` |
| `NumberOfUses` | Left nil for experiment codes | A/B experiment → `1` |

---

## Admin-only configuration

The XML covers the discount code definition only. The following require action in the pricing admin system and are **not representable in the XML**. Flag these in output when relevant; add to this list as new items are confirmed.

| Item | Status | Notes |
|---|---|---|
| Global usage cap | ❌ NOT admin-only — encode in XML | Use `UseLimit=[cap from ticket]`. Confirmed: discEMPWR "50k bundles cap" → `<UseLimit>50000</UseLimit>` in SSOT. Admin-only assumption was wrong. |
| Offer catalog attachment | ✅ Confirmed admin-only | Linking the code to a NES curated offer for auto-apply (e.g. discOPNCLW on OpenClaw SLP) — done in offer catalog, not promo system |
| TEST → PROD promotion | ✅ Confirmed admin-only | Implementers deploy to TEST first, then promote to PROD as a separate step |
| `Version` counter | ✅ System-managed | Auto-incremented by admin system on each edit — never set in XML (observed 1–31 across corpus) |
| `NumberOfCurrencies` | ✅ System-managed | Always 0 in XML even when 35 currencies present — computed by system, not set by implementer |
| Per-private-label activation beyond PL1 | ⚠️ Unconfirmed | XML always contains only PL1; multi-market codes may require additional PL config in admin |

---

## XML → PromoAPI field mapping

The XML is a PromoTool UI format. The production system uses the PromoAPI, which has different field names and conventions. Use this table when comparing XML output against API data.

| XML field | API field | Notes |
|---|---|---|
| `PromoCode` | `promo_code` | Direct match |
| `Type=DiscountCode` | `promo_sub_type=DISCOUNT_CODE` | Standard type → `STANDARD` |
| `AwardType=SetAmount` | `promo_awardTypes_raw=FIXED_DISCOUNT` | |
| `AwardType=PercentOff` | `promo_awardTypes_raw=PERCENT_OFF` | |
| `DiscountAmount` (dollars) | `promo_awardValue_payload` (cents) | Multiply by 100 to compare |
| `<AwardCurrencies>` list | `promo_currencies` (pipe-separated) | |
| No `<AwardCurrencies>` (PercentOff) | `promo_currencies=ALL` | Currency-agnostic in API |
| `StartDate` | `promo_startDate` | |
| `ExpirationDate` | `promo_endDate` | |
| `SuppressIcannFees=true` | `product_suppressICANNFees=1` | |
| `SuppressIcannFees=false` | `product_suppressICANNFees=0` | |
| `UseLimit xsi:nil` | `product_useLimit=-1` | -1 = no limit |
| `UseLimit=N` | `product_useLimit=N` | |
| `<PfIds>` list | `product_award_pfids` (pipe-separated) | |
| `RankValue=10` | `product_rank=10` | |
| `AwardAppliesTo=HighestPriceFirstMayOverlapConditions` | `product_itemOrder=HIGHEST_PRICE_FIRST_OVERLAP` | |
| `<Conditions />` (empty) | `product_condition_element=RemainderOfSingleItem` | Default for all DiscountCode promos in API |
| `PrivateLabels PL1` | `promo_privateLabelIDs=1` (minimum) | Admin may add additional PLs not in XML |
| `<Restriction>Restricted</Restriction>` | **no direct mapping** | `promo_isRestricted` is a different concept — do not use it to score the XML Restriction field |

---

## Field reliability reference

**Top-level fields**

| Field | Status |
|---|---|
| `Active`, `IsActive`, `CreatedDate`, `Type`, `CampaignTypeID`, `NumberOfCurrencies`, `IsPhoneValidationEnabled`, `ShopperIdRestrictions`, `UsageType`, `PromoExclusion`, `DeprecatedMatchedAwardPromo`, `UnsupportedConditionsOrAwards`, `Conditions`, `AwardAppliesTo`, `PrivateLabels (PL1)` | ✅ Locked — never vary |
| `Rank`, `Restriction`, `NumberOfUses`, `UseLimit` | ✅ Reliable — rule-derivable from ticket |
| `StartDate`, `ExpirationDate` | ⚠️ Variable — approximate without deployment system access |
| `PromoCode`, `Name`, `Description` | ❌ User-determined — free-form, read from ticket |

**Award-level fields**

| Field | Status |
|---|---|
| `AwardId`, `SuppressIcannFees` | ✅ Locked |
| `AwardType`, `AwardAmountType`, `AwardQuantity`, `PercentOff`, USD `DiscountAmount` | ✅ Reliable — derivable from ticket |
| PFID set (`PfIds`) | 🔍 Explore — catalog lookup should make this fully derivable |
| Non-USD `DiscountAmount` | 🔍 Explore — FX conversion via real-time rate lookup may automate this |

---

## Minimal XML skeleton

```xml
<?xml version="1.0" encoding="utf-16"?>
<ProductPromo xmlns:xsd="http://www.w3.org/2001/XMLSchema"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <StartDate>[DEPLOYMENT DATE]T00:00:00</StartDate>
  <ExpirationDate>[END DATE]T00:00:00</ExpirationDate>
  <Active>1</Active><IsActive>true</IsActive>
  <CreatedDate>0001-01-01T00:00:00</CreatedDate>
  <UseLimit xsi:nil="true" />
  <PromoCode>[EXACT CODE FROM TICKET]</PromoCode>
  <IsPhoneValidationEnabled>false</IsPhoneValidationEnabled>
  <Name>[SHORT DESCRIPTION]</Name>
  <Description>[SAME AS NAME]</Description>
  <Type>DiscountCode</Type>
  <CampaignTypeID>1</CampaignTypeID>
  <NumberOfCurrencies>0</NumberOfCurrencies>
  <RankValue>10</RankValue><Rank>10</Rank>
  <NumberOfUses xsi:nil="true" />
  <PromoExclusion>0</PromoExclusion>
  <Conditions />
  <Awards>
    <ProductAwardV2>
      <AwardId>1</AwardId>
      <AwardAmountType>Unlimited</AwardAmountType>
      <AwardType>SetAmount</AwardType>
      <AwardQuantity xsi:nil="true" />
      <PercentOff xsi:nil="true" />
      <SuppressIcannFees>false</SuppressIcannFees>
      <PfIds><int>[PFID]</int></PfIds>
      <AwardCurrencies>
        <ProductAwardCurrency>
          <Currency>USD</Currency>
          <DiscountAmount>[AMOUNT]</DiscountAmount>
        </ProductAwardCurrency>
      </AwardCurrencies>
    </ProductAwardV2>
  </Awards>
  <AwardAppliesTo>HighestPriceFirstMayOverlapConditions</AwardAppliesTo>
  <PrivateLabels>
    <PrivateLabelV2>
      <PrivateLabelID>1</PrivateLabelID>
      <IsActive>true</IsActive>
      <StartDate>0001-01-01T00:00:00</StartDate>
      <EndDate>0001-01-01T00:00:00</EndDate>
      <New>false</New>
      <Remove>false</Remove>
    </PrivateLabelV2>
  </PrivateLabels>
  <ShopperIdRestrictions />
  <Restriction>NoRestriction</Restriction>
  <UsageType>NotShopperRestricted</UsageType>
  <DeprecatedMatchedAwardPromo>false</DeprecatedMatchedAwardPromo>
  <UnsupportedConditionsOrAwards>false</UnsupportedConditionsOrAwards>
</ProductPromo>
```
