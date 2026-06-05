---
name: pricing-xml-checker
description: Structural checker and comparator for pricing promo XML. Validates generated XML against hard rules derived from 9 source-of-truth examples. Run checker.py directly — this is a developer measurement tool, not a generation skill.
---

# pricing-xml-checker

A Python-based structural checker and comparator for GoDaddy pricing promo XML (`ProductPromo` format).

This tool validates and compares pricing XML outputs against known source-of-truth examples. It catches structural errors deterministically and produces scored comparison reports used to measure generation quality over time.

**This is not a generation tool and does not learn or adapt.** It applies a fixed set of rules and produces measurement output. The value of that output is in identifying what fails — those failures are reviewed by a human and fed back into the generation skill's instructions.

---

## Usage

```bash
# Check structural rules on a single XML
python3 checker.py check <generated.xml>

# Compare generated against a source-of-truth XML
python3 checker.py compare <generated.xml> <expected.xml>

# Scan golden-set/ and update rule statistics in derived_rules.json
python3 checker.py derive

# Aggregate all saved comparison reports
python3 checker.py report
```

---

## What It Checks

### Hard Structural Rules
Zero exceptions observed across all 9 source-of-truth examples. A failure here is a definite error.

| ID | Rule |
|---|---|
| S1 | `<Conditions />` must be empty — no child elements |
| S2 | `<PrivateLabels>` must be present with exactly PL1 |
| S3 | `<AwardAppliesTo>HighestPriceFirstMayOverlapConditions</AwardAppliesTo>` must be present |
| S4 | No `<PFIDList>` block |
| S5 | `<Name>` must be identical to `<Description>` |

### Internal Consistency Rules

| ID | Rule |
|---|---|
| C1 | `AwardAmountType=Unlimited` → `AwardQuantity` must be nil |
| C2 | `AwardAmountType=Units` → `AwardQuantity` must be set |
| C2u | When `UseLimit` is set, it must equal `AwardQuantity` |
| C3 | `AwardType=PercentOff` → no `AwardCurrencies` element |
| C4 | `AwardType=SetAmount` → `AwardCurrencies` must be non-empty |
| C5 | All `DiscountAmount` values must be positive |
| C6 | No PFID may appear in more than one award row |

### Comparison Fields (requires expected XML)

PromoCode · StartDate · ExpirationDate · Name · Description · Rank · Restriction · PFID set · Currency set · USD amounts per PFID · Award row count

---

## What It Does Not Check

These require information the checker does not have:

- PFID completeness — whether all variant SKUs and term lengths are included
- Non-USD currency amounts — requires live FX rate data
- Whether clone inheritance added unintended term tiers
- Whether market scope is correctly reflected in currency set

---

## Golden Set

`golden-set/` contains 9 source-of-truth XMLs used as reference examples and for rule statistics.

| File | Ticket(s) | Notes |
|---|---|---|
| `discOPNCLW.xml` | PRICING-15503 | VPS, USD+INR, 12 PFIDs, 2 plans × 6 terms |
| `DISCWHECON.xml` | PRICING-15666 | WH Economy US, USD only, 31 PFIDs, 4 term tiers |
| `DISC214228.xml` | PRICING-15489 | Email Essentials, 17 currencies, 1 PFID |
| `disc852258.xml` | PRICING-15397 | WH Economy+Deluxe ROW+IN, no USD |
| `disc15265.xml` | PRICING-15265/15290/15606 | WAM Monthly, global currencies, 3 award rows |
| `DISC15278.xml` | PRICING-15278/15393 | WAM Premium+Commerce TrustedSite |
| `DISCWAMBA.xml` | PRICING-15396 | MWP Basic, AwardAmountType=Units, UseLimit=1 |
| `365AF1F1CB.xml` | PRICING-15500 | M365, USD only, 1 PFID |
| `NoAMTxFee1.xml` | PRICING-15534 | Domain fee waiver, AwardType=PercentOff, Restricted |

---

## Known Generation Error Patterns
Observed across generation runs to date.

| Error | Rule |
|---|---|
| Added `<RemainderOfSingleItem>` Conditions block | S1 |
| Added `<PFIDList>` block | S4 |
| Missing `<PrivateLabels>` | S2 |
| Missing `<AwardAppliesTo>` | S3 |
| Start date off by 1 day | Comparison: StartDate |
| USD-only output when INR required | Comparison: Currency set |
| Single PFID when clone covers 31 | Comparison: PFID set |
| UseLimit=1 when ticket states a global cap (e.g. 50k) | Comparison: UseLimit — treat large N as global cap in UseLimit directly |
| NumberOfUses=1 on a multi-award bundle | Comparison: NumberOfUses — equals award count, not literal ticket language |
| Restriction=NoRestriction for targeted distribution codes | Comparison: Restriction — Restricted applies to cap+audience-scoped codes, not only A/B experiments |
