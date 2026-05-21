---
name: ces-packages
description: Reference catalog of CES merchandising packages — maps merch API package slugs to their constituent PFIDs, domain options, and email add-on type. Used to identify which CES packages are most prevalent based on top NULL-package_id PFIDs from CLN add-to-cart data.
---

# /ces-packages — CES Package Catalog

A persistent reference catalog built from the GoDaddy Merchandising API (`merch-packages` datasource).
Maps package slugs → constituent PFIDs, domain options, and email add-on type.

Companion to `/package-catalog` (NES). This catalog covers CES — packages in the merch API
that do NOT produce a `package_id` in billing/CLN add-to-cart events.

**Data file:** `.claude/skills/ces-packages/ces-package-catalog.md`

---

## Invocation Modes

| Invocation | What it does |
|---|---|
| `/ces-packages` | Summary stats + coverage |
| `/ces-packages <slug>` | Detail for one package slug |
| `/ces-packages domain` | List all domain-purchase-path packages (has domainOptions) |
| `/ces-packages email` | List packages containing email PFIDs |
| `/ces-packages pfid <pfid>` | Find packages containing a specific PFID |
| `/ces-packages unscanned` | List package families not yet profiled |
| `/ces-packages refresh` | Re-scan a package family using the merch API |

---

## Data Sources

- **Merch API**: `get_package(datasource="merch-packages", packageId=slug)` for package structure
- **CLN**: `add_to_cart_product_event_cln` LEFT JOIN `add_to_cart_package_event_cln` WHERE `package_id IS NULL`
  — top PFIDs from CES (null package_id) events drive which PFIDs are "target" PFIDs

### Current Target PFIDs (top 19 CES PFIDs by add-to-cart volume, 7-day window ending 2026-05-16)

| PFID | Product Name | ATC Events |
|---|---|---|
| 101 | .COM Domain Registration | 213,846 |
| 1329767 | Full Domain Protection | 137,669 |
| 103 | .COM Domain Registration | 46,616 |
| 102 | .COM Domain Registration | 44,488 |
| 867688 | Microsoft 365 Email Essentials (1yr) | 30,676 |
| 9850 | .IN Domain Registration | 26,646 |
| 110 | .COM Domain Registration | 19,369 |
| 1798083 | Professional Email Pro Light | 19,257 |
| 105 | .COM Domain Registration | 18,593 |
| 10101 | .COM Domain Renewal | 17,688 |
| 10102 | .COM Domain Renewal | 14,070 |
| 57465 | .UK (.CO.UK) Domain Registration | 11,243 |
| 12001 | .NET Domain Registration | 11,140 |
| 2004092 | .CO Domain Registration | 11,057 |
| 1329768 | Full Domain Protection - Renewal | 10,810 |
| 867686 | Microsoft 365 Email Essentials (monthly) | 9,977 |
| 1798074 | Professional Email Pro Light (monthly) | 9,691 |
| 900 | Domain Ownership Protection | 8,848 |
| 867696 | Microsoft 365 Email Essentials (3yr) | 8,727 |

**Key insight:** Domain PFIDs (101, 102, 103, etc.) do NOT appear as explicit PFID numbers in
merch API package responses — they are encoded in `domainOptions.allowedTlds`. A package with
`domainOptions` present is a domain-purchase-path (DPP) package by definition.

---

## Classification Schema

Each entry in the catalog includes:

| Field | Values |
|---|---|
| `has_domain` | yes/no — `domainOptions` present in response |
| `email_type` | `m365-paid`, `m365-free-trial`, `ox-free`, `ox-paid`, `none` |
| `matched_target_pfids` | explicit PFID numbers from the target list found in `products[].pfids[]` or `addons[]` |
| `primary_products` | human-readable product names |
| `scan_date` | when this entry was profiled |

---

## Scan Coverage (as of 2026-05-16, Rounds 1+2+3+4)

| Package Family | Slugs Scanned | Status |
|---|---|---|
| dpp-us-* | 9 | ✅ complete |
| dpp-ca-* + dpp-plan-* | 13 | ✅ complete |
| dpp-au-* | 9 | ✅ complete |
| dpp-uk-* + dpp-intl-* | 14 | ✅ complete |
| dpp-br-* + dpp-in-* + dpp-mx-* | 6 | ✅ complete |
| office365-* + m365-* | 16 | ✅ complete (16 cataloged; office365-addon/migration low priority) |
| cpanel-set-1-* | 15 | ✅ complete (all 4 tiers × base/-ox/-365; no target PFIDs) |
| cpanel-set-2-upper + set-3 | 15 | ✅ complete |
| cpanel-set-4-* | 13 | ✅ complete (all tiers) |
| cpanel-set-6-* | 15 | ✅ complete (all tiers) |
| cpanel-set-7-* | 6 | ✅ complete |
| cpanel-set-8-* | 6 | ✅ complete |
| cpanel-set-9 + cpanel-tier + cpanel-o365-* | 15 | ✅ complete |
| business-hosting-set-1-* | 12 | ✅ complete (all 4 tiers × 3 email variants) |
| business-hosting-set-2-* | 12 | ✅ complete (all 4 tiers × 3 email variants; -ox = 1192198 NOT 1798083) |
| business-hosting-set-3 + set-4 | 15 | ✅ complete |
| cpanel-openexchange + cpanel-workspace + bizhosting | 8 | ✅ complete |
| wsb-* + wsb-o365-* + wsb-vnext-* + wsb-workspace-* | 12 | ✅ complete (representative) |
| businesshosting-* + vnext-freebuild | 4 | ✅ complete |
| wordpress-* + mwp-* + business-email-* + professional-email-* | 13 | ✅ complete (representative) |
| workspace-* (openexchange/businessap tiers) | 12 | ✅ complete (12 slugs; openexchange-tier1/2/3 canBeSold=true) |
| dop-email-essentials | 1 | ✅ confirmed 867688 match |
| dop-byob + dop-lite + dop-only | 3 | ✅ complete — protection-only, zero PFIDs |
| email-essentials-backup | 1 | ✅ confirmed 867688 match |
| email-essentials-byob | 1 | ✅ confirmed 867688 + 867696 + 867694 (2yr) match |
| temp-email-essentials + temp-email-essentials-99 + -149 | 3 | ✅ confirmed 867686 + 867688 + 867696 match |
| mena-* (digital-kit/ecommerce-kit) | 9 | ✅ complete — no target PFIDs in any tier |
| 123reg hosting families (6 sampled; emailhosting-* unscanned) | 6 | ✅ sampled — no target PFIDs in scanned slugs |
| oybo-* (intl email bundles) | 0 | ❌ not scanned — HIGH PRIORITY (7 slugs, likely carry 867688) |
| emailhosting-individual/starter/team-123reg | 0 | ❌ not scanned — medium priority |
| woosaas-m365 | 0 | ❌ not scanned — medium priority (domain + M365 bundle) |
| office365-addon-* + office365-migration-* | 0 | ❌ not scanned — low priority |

**Total scanned:** ~290 of ~310 targeted packages (Round 1: ~105, Round 2: ~80, Round 3: ~60, Priority: ~10, Round 4: ~35)
**Full catalog:** 1,096 slugs across 129 prefixes (prefix inventory in ces-package-catalog.md)

---

## Integration with /offer-pulse (CES Path)

When `/offer-pulse` identifies a surface as CES (null package_id), use this catalog to look up which merch API packages are the likely source. The mapping below translates ITC prefix → package family → expected email PFID:

### ITC Prefix → CES Package Family Lookup

| ITC prefix / surface pattern | CES package family | Expected target PFIDs | Notes |
|---|---|---|---|
| `dpp_*` (AU/UK/CA) | `dpp-au-*`, `dpp-uk-*`, `dpp-ca-*` | **867688** (M365 1yr) | Tier1 = paid; tier2/3 = free add-on |
| `dpp_*` (US general) | `dpp-us-solution-tier1` through `tier6` | none (464069 only) | Free trial M365 only |
| `dpp_*` (US fixed) | `dpp-us-solution-fixed-tier4` | **867686** (M365 monthly) | Monthly billing, paid M365 |
| `dpp_*` (intl/BR/IN/MX) | `dpp-intl-*`, `dpp-br-*`, `dpp-in-*`, `dpp-mx-*` | none | Free trial only |
| `slp_hosting*`, `dlp_hosting*` | `business-hosting-set-1/2/3/4-*` | **1798083** on `-ox` variants only | Check if surface shows -ox packages |
| `slp_hosting*`, `dlp_hosting*` | `cpanel-set-2/3/9-*` | **1798074** on `cpanel-set-2-ultimate-ox` only | One specific package |
| `slp_m365*`, `slp_email*` | `office365-tier0` | **867686, 867688, 867696** | Pure M365 Email Essentials purchasers |
| `slp_wsb*`, `dpp_wsb*` | `wsb-tier*`, `wsb-o365-*` | none | Free trial or legacy PFIDs only |
| Any surface with `slp_rstdstore` | Unknown (NULL package_id confirmed) | — | CES surface, no package attached |

### Decision Rules for /offer-pulse CES Path

1. **Domain protection PFIDs (1329767, 1329768, 900)**: Always standalone — skip merch API package lookup. These are add-on upsells at domain checkout, never bundled. Report as "standalone add-on."

2. **Domain registration PFIDs (101–115, 9850, 57465, etc.)**: These appear inside `domainOptions.allowedTlds`, not as explicit PFIDs. Any `dpp-*` package is a domain purchase path package by definition. Match the surface ITC to the market (AU/UK/CA vs US/intl) to identify the right dpp family.

3. **Prof Email Pro Light (1798083 = 1yr, 1798074 = monthly)**: Source is `-ox` suffix hosting packages. `1798083` → `business-hosting-set-1/2/3/4-*-ox` + `business-hosting-set-3-*-ox`. `1798074` → `cpanel-set-2-ultimate-ox` only. Present both slugs as CES catalog candidates.

4. **M365 Email Essentials paid (867688/867686/867696)**: `867688` (1yr) → dpp-AU/UK/CA packages. `867686` (monthly) → `dpp-us-solution-fixed-tier4` or `office365-tier0`. `867696` (3yr) → `office365-tier0` only.

5. **M365 Free Trial (464069)**: Not a target PFID — appears in nearly every hosting/WSB package. If the only email PFID is 464069, no paid email package match to surface.

6. **WSB families**: No target PFIDs. If surface is WSB, CES path cannot surface a paid email candidate.

### What "NULL package_id" Actually Means for CES

A NULL `package_id` in `add_to_cart_package_event_cln` does NOT mean the customer had no offer. It means the offer came through the CES path, where the merch API drives the purchase but no NES curated offer ID is emitted. The package slug that drove the session is recoverable via:
- ITC prefix → market → dpp-* family lookup (this catalog)
- PFID match against known `-ox` package slugs (for email)
- Standalone classification (for domain protection)
