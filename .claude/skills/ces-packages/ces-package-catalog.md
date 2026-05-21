# CES Package Catalog

Built from merch API (`merch-packages` datasource) + CLN top CES PFID analysis.
Last updated: 2026-05-16 (Rounds 1+2+3+priority complete). ~255 of ~300 targeted packages scanned.

---

## Key Structural Findings (Rounds 1 + 2 + 3)

1. **Domain PFIDs (101, 102, etc.) are never explicit PFIDs.** They live in `domainOptions.allowedTlds`. Any package with `domainOptions` present is a DPP (Domain Purchase Path) package. Only `m365-businessessentials-domain` outside the dpp-* family has `domainOptions` (free domain for AU/CA/UK markets).

2. **M365 Email Essentials paid PFIDs appear across five package contexts:**
   - PFID 464069 = Free Trial (1yr) — appears in almost every non-DPP hosting/WSB package (not a target)
   - PFIDs 867686/867688/867696 = Paid — AU/UK/CA DPP packages, `office365-tier0`, `dpp-us-solution-fixed-tier4`, `dop-email-essentials`, `email-essentials-backup`, `email-essentials-byob`
   - **PFID 867694 (2yr, not in original target list)** — appears in `email-essentials-byob` only
   - `email-essentials-backup` = M365 Email Essentials 1yr (867688) + M365 Email Backup (996667)
   - `email-essentials-byob` = M365 Email Essentials standalone (867688/867694/867696, 1yr/2yr/3yr) — "bring your own domain"

3. **The email suffix pattern is universal across all hosting families:**
   - Base (no suffix) = Professional Email Individual (1192198) + M365 Free Trial (464069)
   - `-365` = M365 Free Trial only (drops OX email)
   - `-ox` = OpenXchange email only — ONLY specific set-1 variants and cpanel-set-2-ultimate contain paid OX PFID 1798083

4. **Prof Email Pro Light (1798083/1798074) appears in a precise subset of `-ox` variants:**
   - `business-hosting-set-1-launch-ox`, `grow-ox`, `enhance-ox`, `expand-ox` → 1798083 (free)
   - `business-hosting-set-3/4-*-ox` variants → 1798083 (free, all tiers)
   - `cpanel-set-2-ultimate-ox` → 1798074 (free)
   - **business-hosting-set-2 `-ox` variants → 1192198 (NOT 1798083)** — set-2 breaks the set-1 pattern
   - All cPanel, cpanel-openexchange, WSB, MWP `-ox` packages use Prof Email Individual (1192198) instead

5. **Domain protection PFIDs (1329767, 900) appear in ZERO packages.** Sold standalone alongside domain purchases. Explains high CLN volume (~137K and ~8.8K events/week) — add-on upsells at domain checkout, not package components.

6. **WSB packages (wsb-tier*, wsb-o365-*, wsb-vnext-*, wsb-workspace-*)**: No target PFIDs. All use legacy WSB PFIDs or unified 632xxx PFIDs. Email add-ons are Free Trial (464069) or GoDaddy Business Email (965772, canBeSold=false).

7. **Legacy email packages (business-email-tier*, workspace-personalap-tier1)**: canBeSold=false — stale/no longer actively sold.

8. **`dop-*` family splits into two subtypes:**
   - `dop-email-essentials` = Domain Protection (DopClone) + M365 Email Essentials (867688) + M365 Email Backup — has both domain + email
   - `dop-byob`, `dop-lite`, `dop-only` = domain protection only — zero PFIDs (represented as productType=Dop, not PFID arrays). These do NOT bundle email.

9. **`email-essentials-*` family — standalone M365 email bundles:**
   - `email-essentials-backup` = M365 Email Essentials 1yr (867688) + M365 Email Backup monthly (996667)
   - `email-essentials-byob` = M365 Email Essentials 1yr/2yr/3yr (867688/867694/867696) — "bring your own domain" variant
   - **PFID 867694 (M365 Email Essentials 2yr)** surfaced here — was not in the original CLN target list but is a real purchasable PFID.

10. **`temp-email-essentials` (full multi-term package)** carries all three paid M365 term variants — 867686 (monthly), 867688 (1yr), 867696 (3yr). This is the same product as `office365-tier0` under a temp-* slug (likely a live champion or repriced variant). Not a test artifact.

11. **The merch API has 1,096 slugs across 129 distinct top-level prefixes.** Major uncataloged families (by size): `vps4` (105), `ded4` (64), `ssl` (42), `dlxssl` (29) — these are infrastructure/security products, not email/domain bundles. Email-adjacent uncataloged families worth a follow-up scan: `oybo` (7, intl email bundles), `woosaas` (2, domain+email), `emailhosting-*-123reg` (3).

---

## Pattern → Surface Mapping (for offer-pulse)

| CLN PFID | Product | Package source |
|---|---|---|
| 867688 | M365 Email Essentials 1yr | `dpp-au-*`, `dpp-uk-*`, `dpp-ca-*`; `dop-email-essentials`; `email-essentials-backup`; `email-essentials-byob`; `temp-email-essentials`; `temp-email-essentials-99/149` |
| 867686 | M365 Email Essentials monthly | `dpp-us-solution-fixed-tier4`, `office365-tier0`, `temp-email-essentials` |
| 867694 | M365 Email Essentials 2yr | `email-essentials-byob` only — not in original CLN target list |
| 867696 | M365 Email Essentials 3yr | `office365-tier0`, `email-essentials-byob`, `temp-email-essentials`, `temp-email-essentials-99/149` |
| 1798083 | Prof Email Pro Light 1yr | `business-hosting-set-1-*-ox` + `business-hosting-set-3/4-*-ox` variants (free) |
| 1798074 | Prof Email Pro Light monthly | `cpanel-set-2-ultimate-ox` (free bundled) |
| 1329767/1329768 | Full Domain Protection | **Standalone only — not in any package** |
| 900 | Domain Ownership Protection | **Standalone only — not in any package** |
| 101/102/103/etc | Domain registrations | In `domainOptions` of all dpp-* packages — not explicit PFIDs |

**Critical insight:** High CLN volume for 867688 with NULL package_id = purchases through CES dpp-AU/UK/CA packages, `dop-email-essentials` bundle, OR standalone email purchases. Not a gap in the catalog — these ARE the CES packages.

---

## DPP — Domain Purchase Path Packages

All have `domainOptions` (domain registration). Primary product = domain + optional WAM + email add-on.

### US Market

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-us-solution-tier1 | yes | none | W+M Starter (1/2/3/5yr) |
| dpp-us-solution-tier2 | yes | none | W+M Basic + M365 Free Trial (464069) |
| dpp-us-solution-tier3 | yes | none | W+M Essentials + M365 Free Trial (464069) |
| dpp-us-solution-tier4 | yes | none | W+M Standard + M365 Free Trial (464069) |
| dpp-us-solution-tier5 | yes | none | W+M Premium + M365 Free Trial (464069) + SmartLine Unlimited |
| dpp-us-solution-tier6 | yes | none | W+M Commerce + M365 Free Trial (464069) |
| dpp-us-solution-fixed-tier4 | yes | **867686** | W+M Standard (monthly + annual) + M365 Email Essentials monthly |
| dpp-us-solution-alacarte-protection | yes (COM only) | none | Domain + optional M365 Free Trial + optional W+M |
| dpp-us-solution-alacarte-base | yes (COM only) | none | Domain + optional M365 Free Trial + optional W+M |

Notes:
- `fixed-tier4` is the only US DPP package with a monthly billing term and paid M365.
- `alacarte-*` packages have optional (min 0) add-ons vs the tiered bundled approach.
- tier1 has no email component at all.

### Canada Market

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-ca-com-solution-tier1 | yes (.COM) | **867688** | M365 Email Essentials 1yr |
| dpp-ca-com-solution-tier2 | yes (.COM) | **867688** | W+M Standard Intl + M365 free |
| dpp-ca-com-solution-tier3 | yes (.COM) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-ca-ca-solution-tier1 | yes (.CA) | **867688** | M365 Email Essentials 1yr |
| dpp-ca-ca-solution-tier2 | yes (.CA) | **867688** | W+M Standard Intl + M365 free |
| dpp-ca-ca-solution-tier3 | yes (.CA) | **867688** | W+M Ecommerce Intl + M365 free |
| ddpp-au-ca-solution-tier3 | yes (.CA) | **867688** | W+M Ecommerce Intl + M365 free |
| josh-dpp | yes (.COM + 40 TLDs) | **867686** | W+M Standard (monthly/annual) + M365 monthly |

Notes:
- `ddpp-au-ca-solution-tier3` has a double-d typo but is live; structurally identical to `dpp-ca-ca-solution-tier3`.
- CA/COM packages use paid 867688 at tier1; tier2/3 use it as free add-on.

### Australia Market

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-au-com-solution-tier1 | yes (.COM) | **867688** | M365 Email Essentials 1yr |
| dpp-au-com-solution-tier2 | yes (.COM) | **867688** | W+M Standard Intl + M365 free |
| dpp-au-com-solution-tier3 | yes (.COM) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-au-comau-solution-tier1 | yes (.COM.AU) | **867688** | M365 Email Essentials 1yr |
| dpp-au-comau-solution-tier2 | yes (.COM.AU) | **867688** | W+M Standard Intl + M365 free |
| dpp-au-comau-solution-tier3 | yes (.COM.AU) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-au-au-solution-tier1 | yes (.AU) | **867688** | M365 Email Essentials 1yr |
| dpp-au-au-solution-tier2 | yes (.AU) | **867688** | W+M Standard Intl + M365 free |
| dpp-au-au-solution-tier3 | yes (.AU) | **867688** | W+M Ecommerce Intl + M365 free |

Notes: Tier structure is identical across all three TLD groups. 867688 appears in all 9.

### UK Market

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-uk-couk-solution-tier1 | yes (.CO.UK) | **867688** | M365 Email Essentials 1yr |
| dpp-uk-couk-solution-tier2 | yes (.CO.UK) | **867688** | W+M Standard Intl + M365 free |
| dpp-uk-couk-solution-tier3 | yes (.CO.UK) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-uk-uk-solution-tier1 | yes (.UK) | **867688** | M365 Email Essentials 1yr |
| dpp-uk-uk-solution-tier2 | yes (.UK) | **867688** | W+M Standard Intl + M365 free |
| dpp-uk-uk-solution-tier3 | yes (.UK) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-uk-com-solution-tier1 | yes (.COM) | **867688** | M365 Email Essentials 1yr |
| dpp-uk-com-solution-tier2 | yes (.COM) | **867688** | W+M Standard Intl + M365 free |
| dpp-uk-com-solution-tier3 | yes (.COM) | **867688** | W+M Ecommerce Intl + M365 free |
| dpp-uk-couk-comau-solution-tier2 | yes (.CO.UK) | **867688** | W+M Standard Intl + M365 free |

### International + Plan Packages (use Free Trial only — no target PFID matches)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-intl-solution-tier2 | yes (.COM) | none | W+M Basic Intl + M365 Free Trial (464069) |
| dpp-intl-solution-tier4 | yes (.COM) | none | W+M Standard Intl + M365 Free Trial |
| dpp-intl-solution-tier5 | yes (.COM) | none | W+M Premium Intl + M365 Free Trial |
| dpp-intl-solution-tier6 | yes (.COM) | none | W+M Ecommerce Intl + M365 Free Trial |
| dpp-plan-tier1 | yes (.COM) | none | W+M Starter (1/2/3/5yr) |
| dpp-plan-tier2 | yes (.COM) | none | W+M Essentials + M365 Free Trial |
| dpp-plan-tier3 | yes (.COM) | none | W+M Commerce + M365 Free Trial |
| dpp-plan-2020-tier1 | yes (.COM) | none | W+M Basic + M365 Free Trial |
| dpp-plan-2020-tier2 | yes (.COM) | none | W+M Standard + M365 Free Trial |
| dpp-br-com-solution-tier1 | yes (.COM) | none | Domain + M365 Free Trial |
| dpp-br-combr-solution-tier1 | yes (.COM.BR) | none | Domain + M365 Free Trial |
| dpp-in-com-solution-tier1 | yes (.COM) | none | Domain + M365 Free Trial |
| dpp-in-in-solution-tier1 | yes (.IN) | none | Domain + M365 Free Trial |
| dpp-mx-com-solution-tier1 | yes (.COM) | none | Domain + M365 Free Trial |
| dpp-mx-mx-solution-tier1 | yes (.MX) | none | Domain + M365 Free Trial |

---

## Email-Only Packages

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| office365-tier0 | no | **867686, 867688, 867696** | M365 Email Essentials (monthly/1yr/3yr + quarterly/2yr) |
| office365-tier1 | no | none | M365 Online Business Essentials (monthly/1yr/2yr/3yr) |
| office365-tier2 | no | none | M365 Business Essentials (monthly/1yr/2yr) |
| office365-tier3 | no | none | M365 Business Professional (monthly/1yr/2yr/3yr) |
| office365-emailplus-tier1 | no | none | M365 Email Plus (monthly/1yr/2yr/3yr) |
| office365-addseats-tier1 | no | none | M365 Online Business Essentials add-seats |
| office365-addseats-tier3 | no | none | M365 Business Professional add-seats |
| m365-officebusinessp1-aes | no | none | M365 Secure Online Essentials |
| m365-officebusinessp2-aes | no | none | M365 Secure Business Professional |

Notes:
- `office365-tier0` is the exact package for standalone M365 Email Essentials purchases (all three term variants).
- Other office365/m365 tiers are higher-tier products (Business Essentials, Business Pro) — different PFIDs.

---

## Hosting Packages (cPanel + Business Hosting)

### cPanel Legacy + o365 Variants

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-tier0 | no | none | Web Hosting Starter |
| cpanel-tier1 | no | none | Web Hosting Economy (US legacy) |
| cpanel-tier2 | no | none | Web Hosting Deluxe (US legacy) |
| cpanel-tier3 | no | none | Web Hosting Ultimate (US legacy) + SSL free |
| cpanel-tier4 | no | none | Web Hosting Maximum |
| cpanel-pro | no | none | Web Hosting Ultimate + GoDaddy Pro Membership |
| cpanel-o365-tier0 | no | none | Web Hosting Starter |
| cpanel-o365-tier1 | no | none | Web Hosting Economy + M365 Free Trial |
| cpanel-o365-tier2 | no | none | Web Hosting Deluxe + M365 Free Trial |
| cpanel-o365-tier3 | no | none | Web Hosting Ultimate + SSL free + M365 Free Trial |

### cPanel Set-9 Variants

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-9-economy-365 | no | none | Web Hosting Economy (set-9) + M365 Free Trial |
| cpanel-set-9-deluxe-ox | no | none | Web Hosting Deluxe (set-9) + Prof Email Individual free |
| cpanel-set-9-deluxe-365 | no | none | Web Hosting Deluxe (set-9) + M365 Free Trial |
| cpanel-set-9-ultimate-ox | no | none | Web Hosting Ultimate (set-9) + Prof Email Individual free + SSL free |
| cpanel-set-9-ultimate-365 | no | none | Web Hosting Ultimate (set-9) + M365 Free Trial + SSL free |

### cPanel Set-2 + Set-3 (partial)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-2-maximum | no | none | Web Hosting Maximum + Prof Email Individual free + M365 Free Trial |
| cpanel-set-2-maximum-365 | no | none | Web Hosting Maximum + M365 Free Trial |
| cpanel-set-2-ultimate | no | none | Web Hosting Ultimate + Prof Email Individual free + M365 Free Trial + SSL free |
| cpanel-set-2-ultimate-ox | no | **1798074** | Web Hosting Ultimate + Prof Email Pro Light free (1798074) |
| cpanel-set-2-ultimate-365 | no | none | Web Hosting Ultimate + M365 Free Trial |
| cpanel-set-3-economy | no | none | Web Hosting Economy + Prof Email Individual free + M365 Free Trial |
| cpanel-set-3-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free |
| cpanel-set-3-economy-365 | no | none | Web Hosting Economy + M365 Free Trial |
| cpanel-set-3-starter | no | none | Web Hosting Starter (no email) |
| cpanel-set-3-starter-ox | no | none | Web Hosting Starter + Prof Email Individual free |
| cpanel-set-3-deluxe | no | none | Web Hosting Deluxe + Prof Email Individual free + M365 Free Trial |
| cpanel-set-3-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free |
| cpanel-set-3-deluxe-365 | no | none | Web Hosting Deluxe + M365 Free Trial |
| cpanel-set-3-maximum | no | none | Web Hosting Maximum + Prof Email Individual free + M365 Free Trial |
| cpanel-set-3-maximum-ox | no | none | Web Hosting Maximum + Prof Email Individual free |

Note: `-ox` suffix = OX (OpenXchange) email; `-365` suffix = M365 email; base = both offered.

### Business Hosting Set-3 + Set-4

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| business-hosting-set-3-grow | no | none | Web Hosting Plus (AutoSSL) + Prof Email free + M365 Free Trial |
| business-hosting-set-3-grow-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-3-grow-ox | no | none | Web Hosting Plus (AutoSSL) + Prof Email free |
| business-hosting-set-3-enhance | no | none | Web Hosting Plus (AutoSSL) + Prof Email free + M365 Free Trial |
| business-hosting-set-3-enhance-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-3-enhance-ox | no | none | Web Hosting Plus (AutoSSL) + Prof Email free |
| business-hosting-set-3-expand | no | none | Web Hosting Plus (AutoSSL) + Prof Email free + M365 Free Trial |
| business-hosting-set-3-expand-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-3-expand-ox | no | none | Web Hosting Plus (AutoSSL) + Prof Email free |
| business-hosting-set-4-launch | no | none | Web Hosting Plus (AutoSSL) + Prof Email free + M365 Free Trial |
| business-hosting-set-4-launch-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-4-launch-ox | no | none | Web Hosting Plus (AutoSSL) + Prof Email free |
| business-hosting-set-4-grow | no | none | Web Hosting Plus (AutoSSL) + Prof Email free + M365 Free Trial |
| business-hosting-set-4-grow-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-4-grow-ox | no | none | Web Hosting Plus (AutoSSL) + Prof Email free |

---

## Business Hosting Set-1 + Set-2

### Business Hosting Set-1 (Round 2)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| business-hosting-set-1-launch | no | none | Web Hosting Plus (AutoSSL) + Prof Email Individual free + M365 Free Trial |
| business-hosting-set-1-launch-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-1-launch-ox | no | **1798083** | Web Hosting Plus (AutoSSL) + Prof Email Pro Light 1yr free (1798083) |
| business-hosting-set-1-grow | no | none | Web Hosting Plus (AutoSSL) + Prof Email Individual free + M365 Free Trial |
| business-hosting-set-1-grow-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-1-grow-ox | no | **1798083** | Web Hosting Plus (AutoSSL) + Prof Email Pro Light 1yr free (1798083) |
| business-hosting-set-1-enhance | no | none | Web Hosting Plus (AutoSSL) + Prof Email Individual free + M365 Free Trial |
| business-hosting-set-1-enhance-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-1-enhance-ox | no | **1798083** | Web Hosting Plus (AutoSSL) + Prof Email Pro Light 1yr free (1798083) |
| business-hosting-set-1-expand | no | none | Web Hosting Plus (AutoSSL) + Prof Email Individual free + M365 Free Trial |
| business-hosting-set-1-expand-365 | no | none | Web Hosting Plus (AutoSSL) + M365 Free Trial |
| business-hosting-set-1-expand-ox | no | **1798083** | Web Hosting Plus (AutoSSL) + Prof Email Pro Light 1yr free (1798083) |

Notes:
- All four plan tiers (launch/grow/enhance/expand) follow the same base/-365/-ox email suffix pattern.
- `-ox` variants across all set-1 tiers match **1798083** — this is the source of the high CLN volume for Prof Email Pro Light 1yr.
- Base and `-365` variants use Free Trial 464069 or Prof Email Individual (1192198); no target PFIDs.

### Business Hosting Set-2 (Round 3, complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| business-hosting-set-2-launch | no | none | Web Hosting Plus AutoSSL (launch tier) + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| business-hosting-set-2-launch-365 | no | none | Web Hosting Plus AutoSSL (launch tier) + M365 Free Trial (464069) |
| business-hosting-set-2-launch-ox | no | none | Web Hosting Plus AutoSSL (launch tier) + Prof Email Individual free (1192198) |
| business-hosting-set-2-grow | no | none | Web Hosting Plus AutoSSL (grow tier) + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| business-hosting-set-2-grow-365 | no | none | Web Hosting Plus AutoSSL (grow tier) + M365 Free Trial (464069) |
| business-hosting-set-2-grow-ox | no | none | Web Hosting Plus AutoSSL (grow tier) + Prof Email Individual free (1192198) |
| business-hosting-set-2-enhance | no | none | Web Hosting Plus AutoSSL (enhance tier) + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| business-hosting-set-2-enhance-365 | no | none | Web Hosting Plus AutoSSL (enhance tier) + M365 Free Trial (464069) |
| business-hosting-set-2-enhance-ox | no | none | Web Hosting Plus AutoSSL (enhance tier) + Prof Email Individual free (1192198) |
| business-hosting-set-2-expand | no | none | Web Hosting Plus AutoSSL (expand tier) + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| business-hosting-set-2-expand-365 | no | none | Web Hosting Plus AutoSSL (expand tier) + M365 Free Trial (464069) |
| business-hosting-set-2-expand-ox | no | none | Web Hosting Plus AutoSSL (expand tier) + Prof Email Individual free (1192198) |

**Key difference from set-1:** Despite the `-ox` suffix, set-2 `-ox` variants use Prof Email Individual (PFID 1192198), NOT Prof Email Pro Light (1798083). Only set-1 carries 1798083. Zero target PFIDs anywhere in set-2.

---

## WSB Packages

### WSB Tiers + O365 Variants (Round 2)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| wsb-tier1 | no | none | W+M Basic (legacy WSB PFIDs) |
| wsb-tier2 | no | none | W+M Standard (legacy WSB PFIDs) |
| wsb-tier3 | no | none | W+M Premium (legacy WSB PFIDs) |
| wsb-tier4 | no | none | W+M Ecommerce (legacy WSB PFIDs) |
| wsb-o365-tier1 | no | none | W+M Basic + M365 Free Trial (464069) |
| wsb-o365-tier2 | no | none | W+M Standard + M365 Free Trial (464069) |
| wsb-o365-tier3 | no | none | W+M Premium + M365 Free Trial (464069) |
| wsb-o365-tier4 | no | none | W+M Ecommerce + M365 Free Trial (464069) |
| wsb-vnext-tier1 | no | none | W+M Next-Gen Basic (unified 632xxx PFIDs) |
| wsb-vnext-tier2 | no | none | W+M Next-Gen Standard (unified 632xxx PFIDs) |
| wsb-workspace-tier1 | no | none | W+M Basic + GoDaddy Business Email (965772, canBeSold=false) |
| wsb-workspace-tier2 | no | none | W+M Standard + GoDaddy Business Email (965772, canBeSold=false) |

Notes:
- Zero target PFID matches across all WSB families.
- `wsb-tier*` use legacy WSB-specific PFIDs (not in target list).
- `wsb-o365-*` use only Free Trial 464069 — not the paid M365 target PFIDs.
- `wsb-workspace-*` use GoDaddy Business Email PFID 965772 (canBeSold=false — bundled legacy asset).
- `wsb-vnext-*` use unified 632xxx product family PFIDs.

---

## Businesshosting + vnext-freebuild (Round 2)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| businesshosting-tier1 | no | none | Business Hosting legacy tier 1 |
| businesshosting-tier2 | no | none | Business Hosting legacy tier 2 |
| businesshosting-tier3 | no | none | Business Hosting legacy tier 3 |
| vnext-freebuild | no | none | W+M Basic (free plan) + Free Trial email |

Notes: Legacy products; no target PFIDs. `vnext-freebuild` is the free-plan entry point.

---

## cPanel OpenXchange + Workspace + Bizhosting (Round 2)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-openexchange-economy | no | none | Web Hosting Economy + Prof Email Individual (1192198) |
| cpanel-openexchange-deluxe | no | none | Web Hosting Deluxe + Prof Email Individual (1192198) |
| cpanel-openexchange-ultimate | no | none | Web Hosting Ultimate + Prof Email Individual (1192198) + SSL free |
| cpanel-workspace-economy | no | none | Web Hosting Economy + GoDaddy Workspace Email |
| cpanel-workspace-deluxe | no | none | Web Hosting Deluxe + GoDaddy Workspace Email |
| cpanel-workspace-ultimate | no | none | Web Hosting Ultimate + GoDaddy Workspace Email + SSL free |
| bizhosting-basic | no | none | BizHosting Basic (legacy) |
| bizhosting-advanced | no | none | BizHosting Advanced (legacy) |

Notes:
- `cpanel-openexchange-*` use Prof Email Individual (1192198), not Pro Light (1798083) — these are a different OX email tier.
- `cpanel-workspace-*` use GoDaddy Workspace Email (legacy product, canBeSold=false on some).
- No target PFIDs in any of these families.

---

## M365 + Workspace Remainder (Round 2, sampled)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| m365-businessessentials-domain | yes (.COM/.CA/.AU) | none | M365 Business Essentials + free domain (AU/CA/UK only) |
| workspace-personalap-tier1 | no | none | GoDaddy Workspace Email Personal (canBeSold=false — legacy) |
| workspace-businessap-tier1 | no | none | GoDaddy Workspace Email Business (canBeSold=false — legacy) |

Notes:
- `m365-businessessentials-domain` is the only non-dpp-* package with `domainOptions` (free domain add-on for AU/CA/UK markets). Uses M365 Business Essentials PFIDs — not the Email Essentials target PFIDs (867688/686/696).
- `workspace-*` packages are canBeSold=false — no longer actively sold.

---

## cPanel Set-4 (Round 3, complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-4-economy | no | none | Web Hosting Economy + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-4-economy-365 | no | none | Web Hosting Economy + M365 Free Trial (464069) |
| cpanel-set-4-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free (1192198) |
| cpanel-set-4-starter-365 | no | none | Web Hosting Starter + M365 Free Trial (464069) |
| cpanel-set-4-deluxe | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-4-deluxe-365 | no | none | Web Hosting Deluxe + M365 Free Trial (464069) |
| cpanel-set-4-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) |
| cpanel-set-4-ultimate | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + M365 Free Trial (464069) + SSL free |
| cpanel-set-4-ultimate-365 | no | none | Web Hosting Ultimate + M365 Free Trial (464069) + SSL free |
| cpanel-set-4-ultimate-ox | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + SSL free |
| cpanel-set-4-maximum | no | none | Web Hosting Maximum + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-4-maximum-365 | no | none | Web Hosting Maximum + M365 Free Trial (464069) |
| cpanel-set-4-maximum-ox | no | none | Web Hosting Maximum + Prof Email Individual free (1192198) |

Notes: Zero target PFIDs. Hosting PFIDs in 1338xxx range. `-ox` always 1192198, not 1798083.

---

## cPanel Set-6 (Round 3, complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-6-starter | no | none | Web Hosting Starter (no email add-on) |
| cpanel-set-6-starter-365 | no | none | Web Hosting Starter + M365 Free Trial (464069) |
| cpanel-set-6-starter-ox | no | none | Web Hosting Starter + Prof Email Individual free (1192198) |
| cpanel-set-6-economy | no | none | Web Hosting Economy + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-6-economy-365 | no | none | Web Hosting Economy + M365 Free Trial (464069) |
| cpanel-set-6-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free (1192198) |
| cpanel-set-6-deluxe | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-6-deluxe-365 | no | none | Web Hosting Deluxe + M365 Free Trial (464069) |
| cpanel-set-6-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) |
| cpanel-set-6-ultimate | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + M365 Free Trial (464069) + SSL free |
| cpanel-set-6-ultimate-365 | no | none | Web Hosting Ultimate + M365 Free Trial (464069) + SSL free |
| cpanel-set-6-ultimate-ox | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + SSL free |
| cpanel-set-6-maximum | no | none | Web Hosting Maximum + Prof Email Individual free (1192198) + M365 Free Trial (464069) |
| cpanel-set-6-maximum-365 | no | none | Web Hosting Maximum + M365 Free Trial (464069) |
| cpanel-set-6-maximum-ox | no | none | Web Hosting Maximum + Prof Email Individual free (1192198) |

Notes: Hosting PFIDs in 1339xxx range. Same suffix email pattern. Zero target PFIDs.

---

## cPanel Set-7 (Round 3, complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-7-economy-365 | no | none | Web Hosting Economy + M365 Free Trial (464069) |
| cpanel-set-7-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free (1192198) |
| cpanel-set-7-deluxe-365 | no | none | Web Hosting Deluxe + M365 Free Trial (464069) |
| cpanel-set-7-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) + SSL free |
| cpanel-set-7-ultimate-365 | no | none | Web Hosting Ultimate + M365 Free Trial (464069) + SSL free |
| cpanel-set-7-ultimate-ox | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + SSL free |

Notes: All 6 slugs in family — complete coverage. No base (no-suffix) variants exist in set-7. Zero target PFIDs.

---

## cPanel Set-8 (Round 3, complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-8-economy-365 | no | none | Web Hosting Economy + M365 Free Trial (464069) |
| cpanel-set-8-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free (1192198) |
| cpanel-set-8-deluxe-365 | no | none | Web Hosting Deluxe + M365 Free Trial (464069) |
| cpanel-set-8-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free (1192198) |
| cpanel-set-8-ultimate-365 | no | none | Web Hosting Ultimate + M365 Free Trial (464069) + SSL free |
| cpanel-set-8-ultimate-ox | no | none | Web Hosting Ultimate + Prof Email Individual free (1192198) + SSL free |

Notes: All 6 slugs in family — complete coverage. Same as set-7: only -365/-ox variants (no base). Hosting PFIDs in 1351xxx range. Zero target PFIDs.

---

## cPanel Set-1 (Round 2, sampled)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| cpanel-set-1-economy | no | none | Web Hosting Economy + Prof Email Individual free + M365 Free Trial |
| cpanel-set-1-economy-ox | no | none | Web Hosting Economy + Prof Email Individual free |
| cpanel-set-1-deluxe | no | none | Web Hosting Deluxe + Prof Email Individual free + M365 Free Trial |
| cpanel-set-1-deluxe-ox | no | none | Web Hosting Deluxe + Prof Email Individual free |

Notes: Sampled only; full set-1 family unscanned (~15 packages). Pattern matches other cPanel families — no target PFIDs expected.

---

## WordPress + MWP + Professional Email + Business Email

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| wordpress-tier1 | no | none | MWP Basic (no email) |
| wordpress-o365-tier1 | no | none | MWP Basic + M365 Free Trial (464069) |
| wordpress-o365-tier2 | no | none | MWP Deluxe (PFIDs 580969+) + M365 Free Trial (464069) |
| wordpress-o365-tier3 | no | none | MWP Ultimate (PFIDs 580995+) + M365 Free Trial (464069) |
| wordpress-o365-tier4 | no | none | MWP Developer (PFIDs 581013+) + SSL free + M365 Free Trial (464069) |
| wordpress-workspace-tier1 | no | none | MWP Basic + GoDaddy Workspace Email |
| wordpress-o365-forever-ssl-ultimate-free30-annual | no | none | MWP Ultimate intro (PFID 1525404, 30-day free trial, 1yr) |
| mwp-bulkpro-ox-05sites | no | none | MWP Pro 5-site + optional Prof Email Starter (1192190) or GD Business Email (canBeSold=false) |
| mwp-ecommerce-o365-tier1 | no | none | MWP eCommerce + M365 Free Trial (464069, 5 seats) |
| professional-email-tier1 | no | none | Professional Email Starter (PFID 1192190) standalone |
| business-email-tier1 | no | none | Business Email tier 1 (canBeSold=false — legacy) |
| business-email-tier2 | no | none | Business Email tier 2 (canBeSold=false — legacy) |
| business-email-tier3 | no | none | Business Email tier 3 (canBeSold=false — legacy) |

Notes:
- No target PFIDs anywhere in WordPress/MWP/email families. All use 464069 (free trial) or 1192190 (Prof Email Starter).
- `business-email-*` canBeSold=false — stale, no longer sold.
- tier4 MWP drops M365 in favor of Standard SSL as the free add-on.

---

---

## DOP — Domain Protection-First Packages (complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dop-email-essentials | no | **867688** | Domain Protection (DopClone) + M365 Email Essentials 1yr (867688) + M365 Email Backup (996667) |
| dop-byob | yes | none | Domain Protection (DopLite) + domain registration (allowedTlds=[]) + discount code disc699698. Zero PFIDs — no email. |
| dop-lite | yes | none | Domain Protection (DopLite) + domain registration. Zero PFIDs — no email. |
| dop-only | yes | none | Domain Protection (DopClone) + domain registration (allowedTlds=[]). Zero PFIDs — no email. |

Notes:
- Family splits cleanly: `dop-email-essentials` = protection + M365 email bundle; `dop-byob/lite/only` = protection-only, no email, no explicit PFIDs.
- `dop-byob/lite/only` have `domainOptions` (has_domain=yes) — they register a domain as part of the flow.
- `dop-email-essentials` has no `domainOptions` (has_domain=no) — domain is assumed pre-existing ("bring your own").
- Protection subtypes: DopLite = lighter tier; DopClone = full clone/transfer protection.

---

## Email Essentials — Standalone Email Packages (complete)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| email-essentials-backup | no | **867688** | M365 Email Essentials 1yr (867688) + M365 Email Backup monthly (996667) |
| email-essentials-byob | no | **867688, 867696** | M365 Email Essentials: 1yr (867688), 2yr (867694), 3yr (867696) — "bring your own domain" |

Notes:
- `email-essentials-byob` surfaces PFID **867694** (M365 Email Essentials 2yr) — not in the original CLN target list but is a live purchasable PFID.
- Neither package has `domainOptions` — customers must already own a domain.
- Both are pure standalone email purchases with no hosting component.

---

## MENA Regional Packages (Round 4, complete)

### mena-digital-kit (tiers 1–6)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| mena-digital-kit-tier1 | yes (.COM) | none | Arabic WSB Basic (1317311) + M365 Free Trial (464069) |
| mena-digital-kit-tier2 | yes (.COM) | none | Arabic WSB Standard (1317317) + M365 Free Trial (464069) |
| mena-digital-kit-tier3 | yes (.COM) | none | Arabic WSB Premium (1317321) + M365 Free Trial (464069) |
| mena-digital-kit-tier4 | yes (.COM) | none | Arabic WSB Basic (1317311) + Prof Email Individual (1192198) |
| mena-digital-kit-tier5 | yes (.COM) | none | Arabic WSB Standard (1317317) + Prof Email Individual (1192198) |
| mena-digital-kit-tier6 | yes (.COM) | none | Arabic WSB Premium (1317321) + Prof Email Individual (1192198) |

### mena-ecommerce-kit (tiers 4–6)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| mena-ecommerce-kit-tier4 | yes (.COM) | none | GoDaddy e-Store Starter (1317325) + Prof Email Individual (1192198) |
| mena-ecommerce-kit-tier5 | yes (.COM) | none | GoDaddy e-Store Premium (1317329) + Prof Email Individual (1192198) |
| mena-ecommerce-kit-tier6 | yes (.COM) | none | GoDaddy e-Store Unlimited (1321521) + Prof Email Individual (1192198) |

Notes:
- Tiers 1–3 use M365 Free Trial (464069); tiers 4–6 switch to Prof Email Individual (1192198). No paid email target PFIDs in any tier.
- MENA-specific product PFIDs (1317xxx, 1321xxx) — Arabic Website Builder and GoDaddy e-Store regional products.

---

## Workspace + Professional Email (Round 4, complete)

### workspace-* (complete — 12 slugs)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| workspace-openexchange-tier1 | no | none | Prof Email Individual (1192189–1192204, mo/1/2/3yr, canBeSold=true) |
| workspace-openexchange-tier2 | no | none | Prof Email Team (1192206–1192216, mo/1/2/3yr, canBeSold=true) |
| workspace-openexchange-tier3 | no | none | Prof Email Group+Security (1192218–1192228, mo/1/2/3yr, canBeSold=true) |
| workspace-webmail-tier1 | no | none | GoDaddy Business Email Plus (965792–965796, 1/2/3yr, canBeSold=false) |
| workspace-webmail-tier2 | no | none | GoDaddy Business Email Plus (965792–965796, canBeSold=false) + disc888222 |
| workspace-webmail-tier3 | no | none | GoDaddy Business Email Plus (965792–965796, canBeSold=false) + disc777111 |
| workspace-i18npro-tier1 | no | none | GoDaddy Business Email (965769–965778, mo/1/2/3yr, canBeSold=false) |
| workspace-i18nproplus-tier1 | no | none | GoDaddy Business Email Plus (965790–965796, mo/1/2/3yr, canBeSold=false) |
| workspace-tier1 | no | none | GoDaddy Business Email (965772, 1yr only, canBeSold=false) — legacy stub |
| workspace-personaleu-tier1 | no | none | Email Personal EU (1069449–1069457, canBeSold=false) + Calendar free + Storage free |
| workspace-personalus-tier1 | no | none | Email Personal US (1069427–1069435, canBeSold=false) |
| workspace-personalap-tier1 | no | none | GoDaddy Workspace Email Personal (canBeSold=false — legacy) |

Notes:
- **workspace-businessap-tier1** (previously in catalog) no longer exists in the merch API — retired.
- Only `workspace-openexchange-tier1/2/3` are canBeSold=true (live OX email product line).
- All workspace-webmail-*/i18n-*/personal-* are legacy (canBeSold=false).

### professional-email-* (complete — 1 slug only)

`professional-email-tier1` is the only professional-email-* slug in the API. No tier2/3 exists.

---

## Temp Packages — Live Champions (Round 4)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| temp-email-essentials-99 | no | **867688, 867696** | M365 Email Essentials (1yr=867688, 3yr=867696) — champion at dpp_precheck, discounted |
| temp-email-essentials-149 | no | **867688, 867696** | M365 Email Essentials (1yr=867688, 3yr=867696) — champion variant |
| temp-email-essentials | no | **867686, 867688, 867696** | M365 Email Essentials all terms: monthly (867686), 1yr (867688), 3yr (867696) + addon groups |
| temp-mwp-basic | no | none | MWP Basic + free SSL — champion variant |

Notes:
- `temp-` prefix packages are live production champions — NOT test artifacts (confirmed in prior rounds and by this inventory).
- `temp-email-essentials` is the full multi-term Email Essentials package; functionally equivalent to `office365-tier0` under a different slug.
- `temp-titan-discount` and `temp-wam-basic-discount` were found in the prefix inventory but not scanned.

---

## 123reg Extended Family (Round 4, sampled)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| managed-wordpress-pro-123reg-tier3 | no | none | Ultimate MWP (1317516–1317521) + 3× Prof Email Starter (1192190) free |
| hosting-ultimate-123reg-tier4 | no | none | Web Hosting Maximum (1339109+) + 5× Prof Email Starter (1192190) free |
| vps4-self-managed-lin-123reg-tier1 | no | none | Gen4 VPS Linux 1 CPU self-managed |
| vps4-self-managed-win-123reg-tier4 | no | none | Gen4 VPS Windows 4 CPU self-managed |
| m365-businessessentias-123reg | no | none | M365 Online Business Essentials (31xxx series, 123reg reseller SKUs) |
| m365-businesspremium-123reg | no | none | M365 Business Professional (31xxx series, 123reg reseller SKUs) |

Notes:
- 43 total 123reg slugs. All sampled use Prof Email Starter (1192190) or legacy M365 Business (31xxx), not target PFIDs.
- `emailhosting-individual-123reg`, `emailhosting-starter-123reg`, `emailhosting-team-123reg` (3 slugs) not yet scanned — these email-hosting-specific packages may carry target PFIDs.

---

## Miscellaneous Packages (Round 3+4, sampled)

| package_slug | has_domain | matched_target_pfids | primary_products |
|---|---|---|---|
| dpp-plan-2020-tier1 | yes | none | W+M Basic (multi-term) + M365 Free Trial (464069) + domain (COM, full protection) |
| m365-businessessentials-domain | yes | none | M365 Business Essentials (31825) + free domain (COM/CA/AU/UK) |
| office365-addseats-tier0 | no | none | M365 Email Essentials add-seats (1082902–1082912) + optional Email Archiving/Backup/Security addons |
| office365-emailessentials-atmp-tier1 | no | none | M365 Email Essentials monthly only (PFID 1502992) — ATMP A/B test variant |

---

## Prefix Inventory — Full Catalog Coverage (Round 4)

Total: 1,096 slugs across 129 distinct prefixes in `merch-packages`.

| Prefix family | Slug count | Coverage |
|---|---|---|
| cpanel | 133 | ✅ sets 1/2/3/4/6/7/8/9, tier, o365, openexchange, workspace, bizhosting |
| vps4 | 105 | ❌ VPS hosting — no email/domain target PFIDs expected |
| business-hosting | 73 | ✅ set-1/2/3/4 complete |
| ded4 | 64 | ❌ Dedicated servers — no target PFIDs expected |
| dpp | 49 | ✅ all country variants complete; 3 retired slugs noted |
| wordpress | 43 | ✅ tier1–4, o365, workspace, MWP families |
| ssl | 42 | ❌ SSL certs — no target PFIDs |
| vnext | 34 | ✅ freebuild + wsb-vnext complete |
| dlxssl | 29 | ❌ Deluxe SSL — no target PFIDs |
| office365 / m365 | 31 | ✅ 16 cataloged; 17 unscanned (addon/migration variants, low priority) |
| mwp | 20 | ✅ representative coverage |
| wsb | 20 | ✅ complete |
| conversations | 18 | ❌ Smartline replacement — no email target PFIDs expected |
| businesshosting | 17 | ✅ complete |
| mena | 12 | ✅ digital-kit/ecommerce-kit tiers 1–6 complete |
| workspace | 12 | ✅ complete |
| dop | 5 | ✅ complete |
| email-essentials | 2 | ✅ complete |
| hosting (123reg) | 43 | ✅ sampled; emailhosting-*-123reg (3 slugs) unscanned |
| oybo | 7 | ❌ International email bundles — **HIGH PRIORITY, likely carry target PFIDs** |
| woosaas | 2 | ❌ Domain + email bundles — **medium priority** |
| temp | 6 | ✅ email-essentials variants confirmed; titan/wam variants unscanned |

**Families confirmed no target PFIDs:** vps4, ded4, ssl, dlxssl, conversations, plesk, test, paidit, managedseo, dedicated, web (atmp), websecurity, websitebackup, restore, marketing/msb/mss/msp, getfound, emailmarketing, wam, norton, domain (bundles).

---

## Remaining Unscanned (after Round 4)

**Medium priority (may carry target PFIDs):**
- `oybo-*` (7 slugs) — international email bundles; likely 867688 or regional variants
- `emailhosting-individual/starter/team-123reg` (3 slugs) — 123reg email hosting
- `woosaas-m365` — domain + M365 bundle; `woosaas-ox` uses 1192198

**Low priority (no target PFIDs expected):**
- `office365-addon-*` + `office365-*-mass-migration-*` (17 slugs) — add-on and migration fee packages
- `temp-titan-discount` + `temp-wam-basic-discount` — champion pricing variants
- All VPS, dedicated, SSL, security families

To resume, invoke `/ces-packages refresh` and prioritize `oybo-*` + `emailhosting-*-123reg`.
