# Generation Rules

Specific rules for producing correct XML from a pricing ticket. Each rule is sourced from a confirmed test result. Rules marked with a ticket reference were validated against SSOT.

---

## PromoCode

**Rule:** Use the exact code from the ticket body (description/ask field), not from implementer comments or changelogs. Preserve casing exactly.

- Ticket body says `DISC15348` → use `DISC15348` ✓
- Implementer comment says `disc15348` → do NOT use this as the source
- If the ticket body has both (e.g., "Discount code: **DISC15278**"), use the bolded/explicit value

**Casing patterns observed:**
- `DISC` + ticket number → usually all caps (disc15265 is an exception — ticket body used lowercase)
- `DISC` + product abbreviation → usually all caps (DISCWHECON, DISCMWPB5, DISCWAMBA)
- `disc` + number → ticket explicitly lowercased (disc15265, disc852258, discOPNCLW)
- Alphanumeric/mixed → match exactly (365AF1F1CB, NoAMTxFee1)

**Source:** PRICING-15348 test — used comment casing instead of ticket body → mismatch

---

## StartDate

**Rule:** StartDate = the date the promo is deployed and activated in the system — NOT the campaign go-live date stated in the ticket.

When a ticket says "From March 16" or "Live from [date]" or "active from [date]":
- That date is when the **cart team / surface team** will flip their switch
- The promo itself is deployed earlier so it exists in the system when they need it
- Use the ticket creation date or the date the ticket is being processed as StartDate

**When to use a future StartDate:**
- Only when the ticket explicitly says the promo must NOT be active before a certain date
- Language like "do not activate before...", "scheduled launch on...", or "embargo until..."
- This is rare — most tickets use deployment date

**Practical rule when generating without knowing exact deployment date:**
- If ticket has a due date: use that
- If ticket has no start date and no embargo language: use the ticket creation date
- Never use a stated campaign/surface date as StartDate unless it has explicit "do not activate before" language

**Source:** PRICING-15348 test — used campaign date (March 16) instead of deployment date (March 3) → 13-day StartDate error

---

## Name and Description

**Rule:** Name and Description must always be identical. Keep them concise (5–10 words). Do not include the ticket number unless the product/team consistently uses it.

**Format pattern:** `[Product] [surface/context] [price point] [currency if single-currency]`

**Examples from SSOT:**
- `.UK cart cross-sell promo 1.99 GBP`
- `discount code for 80% off WH Deluxe and Economy`
- `WAM Monthly Sale 16.99 Basic 29.99 Premium 34.99 Commerce USD DEM and ROW`
- `Discount Code for US: WH Economy - 36m Offer`
- `New Discount Code – M365 Online Essentials w/o Teams @ $3.99/mo`

**With ticket number (only these cases observed):**
- `Discount Code for MHWP Basic, 80%  off list price (term 1 year) PRICING-15396` — DISCWAMBA only
- `PRICING-15503 OpenClaw for GoDaddy VPS Coupon` — discOPNCLW only

Both of these are exceptions. Default: no ticket number.

**Capitalisation:** Match how the product/domain is written in the ticket. `.UK` not `.uk`, `WH Economy` not `wh economy`.

**The name describes the spirit of the ticket in plain language — not the implementation details.**

More examples confirmed from batch test:
- `50% off WAM Monthly` (not "WAM Monthly sale Basic 10.99 Premium 19.99 Commerce 22.99 USD")
- `Discount for A/B Experiment 50% off DOP` (includes experiment context)
- `Solution Set for Domain, EE, DOP, and WAM Lite - 47.88` (includes bundle total)

When the ticket is an A/B experiment: include "A/B Experiment" or "experiment" in the name.
When the ticket is a bundle/solution set: include the bundle total price.
Otherwise: product + offer type + key price point.

**Source:** PRICING-15348 and batch test — names should be shorter and reflect ticket intent, not PFID details

---

## Currency Scope

**Rule:** Currency set is driven entirely by market scope stated in the ticket, not by product type.

| Ticket says | Currency set |
|---|---|
| US only | USD only |
| UK only / GBP | GBP only |
| DEM | EUR, GBP, CAD |
| ROW only | Non-USD; no USD |
| ROW + India | Non-USD including INR |
| India only | INR only |
| LATAM | BRL, CLP, COP, MXN, PEN (+ USD if stated) |
| Global / not stated | Full currency set (20+ currencies) |

**Non-USD amounts:** Cannot be derived from the ticket alone — they require a FX table. Flag these as `[FX REQUIRED]` in your output for the implementer to fill in. Only USD and the anchor currency (GBP, EUR, etc.) can be calculated directly.

---

## PFID Resolution

**Rule:** Use PFIDs exactly as stated in the ticket. If the ticket names only base PFIDs and references a clone, flag that the full PFID set requires catalog lookup.

- Ticket gives explicit PFIDs → use them
- Ticket gives one base PFID + clone reference → use base PFID for the named term, flag that clone expansion will add more (do not guess)
- PFID from implementer comments > PFID guessed from ticket description
- When implementer comment names a PFID explicitly (e.g., "PFID 410930") → that is authoritative

---

## Rank

**Rule:** Default rank is `10`. Use `80` only for clone-based US hosting/MWP promos.

Pattern observed:
- DISCWHECON: Rank 80 (clone-based, US hosting)
- DISCMWPB5: Rank 80 (clone-based, US MWP)
- All others in corpus: Rank 10

If a ticket says "clone of [offer]" and the product is Hosting or MWP and the market is US → use Rank 80. Otherwise default to 10.

---

## ExpirationDate

**Rule:** Use the date stated in the ticket. When no date is given, use the convention for the promo type.

- Ticket says "until March 29" → `2026-03-30T00:00:00` (midnight convention: start of next day)
- Ticket says "expires [date]" → use that date directly as `T00:00:00`
- Ticket says "X months from [deployment]" → calculate exact date
- Ticket says "90 days" or "Early Access validation period" → calculate from deployment date

**When no end date is given — use promo type convention:**

| Promo type | Convention | Examples |
|---|---|---|
| A/B experiment | ~1 year from deployment | discdop467: 2027-01-01, disc15200: 2027-01-01 |
| Short-term campaign | Stated end date in ticket | disc15348: 2026-03-30 |
| Standing offer / bundle | Long-dated (10yr) or 2099 | discwam478: 2036-01-01, discOPNCLW: 2027-01-01 |
| Evergreen sale code | `2099-01-01` | DISCWAMUP3, DISCWAMUPP2 |

**Do NOT default to 2099 for experiment codes.** Experiments have a planned end — use `[deployment year + 1]-01-01` as a safe default when no date is stated and the ticket signals A/B test.

**Source:** Batch test — used 2099-01-01 on disc15200 (experiment) and discwam478 (bundle) → both wrong

---

## AwardAmountType, UseLimit, and NumberOfUses

**Rule:** Default is `Unlimited` with nil UseLimit, nil AwardQuantity, and nil NumberOfUses.

Use `Units` (with UseLimit=1 and AwardQuantity=1) only when:
- Ticket says "1 per shopper", "single use per account", "one use only"

`NumberOfUses` is a separate field from `UseLimit`:
- `UseLimit` — per-shopper restriction (nil = no per-shopper limit)
- `NumberOfUses` — per-cart/transaction count (nil = unlimited per transaction)
- For A/B experiment codes, `NumberOfUses=1` is common even when `UseLimit` is nil
- When ticket says "A/B experiment": set `NumberOfUses=1`, keep `UseLimit=nil`

| Ticket says | UseLimit | AwardQuantity | NumberOfUses | AwardAmountType |
|---|---|---|---|---|
| No restriction stated | nil | nil | nil | Unlimited |
| A/B experiment | nil | nil | 1 | Unlimited |
| 1 per shopper / single use | 1 | 1 | = award count | Units |
| Global cap / distribution campaign | [cap from ticket] | 1 | = award count | Units |

`NumberOfUses` observed pattern for Units codes: appears to equal the award count (DISCWAMBA: 1 award → 1; discEMPWR: 2 awards → 2). Two data points — treat as a working hypothesis, not a confirmed rule. When generating a multi-award Units code, use award count and flag the assumption in pre-generation notes.

`UseLimit` — encode the ticket's stated numeric limit directly. Observed: UseLimit=1 (per-shopper, DISCWAMBA), UseLimit=50000 (total cap, discEMPWR). The ticket determines the value; the rule is "take what the ticket gives you."

**Source:** discdop467 batch test — missed `NumberOfUses=1` for A/B experiment code; discEMPWR (PRICING-15371) — UseLimit=50000 global cap, NumberOfUses=2 for two-award bundle

---

## Restriction

**Rule:** Default is `NoRestriction`. Use others only when explicitly stated.

| Ticket language | Restriction value |
|---|---|
| Not stated / all customers | `NoRestriction` |
| New customers only + inactive | `RestrictedNewShoppersOnlyAndInActiveCustomersOnly` |
| **A/B experiment / experiment cohort** | **`Restricted`** |
| Specific named shoppers | Standard type — do not generate |

**Underlying principle:** `Restricted` = code is not freely available to all shoppers. `NoRestriction` = anyone can apply it.

Observed Restricted on: A/B experiment cohorts (discdop467, NoAMTxFee1) and a capped student distribution code (discEMPWR). Common thread: access is gated — by experiment cohort membership or by a controlled distribution channel. When the ticket describes a code that only certain people can get or use, lean toward `Restricted`.

**Source:** discdop467 batch test — used NoRestriction for A/B experiment; discEMPWR — used NoRestriction for student distribution campaign, SSOT has Restricted

---

## PFID Selection

**Rule:** Use PFIDs exactly as stated in the ticket. When the ticket does not list PFIDs explicitly, do not pull from similar training examples — flag as unknown.

**Known failure mode:** Using the full PFID set from a similar training example (e.g., disc15265 had 24 PFIDs for US+DEM+ROW) on a narrower ticket (disc15200 was US-only and had only 15 PFIDs). The implementer selects the current-generation PFIDs relevant to the scope — older variants and regional extras are excluded.

- If ticket gives explicit PFIDs → use them exactly
- If ticket says "clone of [offer]" → flag for catalog lookup, use base PFID only
- If ticket says "WAM Monthly" without PFIDs → flag as unknown, do not guess from training data
- Do not assume "more PFIDs = more complete" — the SSOT often has fewer than training examples

**Source:** disc15200 batch test — included 24 PFIDs from training data, SSOT had 15 (9 extra PFIDs flagged as mismatch)
