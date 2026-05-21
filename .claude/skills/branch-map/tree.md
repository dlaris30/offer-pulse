# Offer Pulse — Decision Tree

Last updated : 2026-05-17T
Runs parsed  : 21 run entries; 10 audit/assessment/measure entries excluded
Date range   : 2026-05-13 → 2026-05-15

---

## Branch Tree

Legend:  [✓ N] confirmed N runs  |  [⚠ N/M] N of M runs flagged  |  [?] hypothetical  |  [○] not yet reached

Note: All confirmed nodes show [⚠] because every log entry has at least one flag fired (flags include
observational/informational notes, not only errors). Flag rate reflects log completeness, not error prevalence.

```
offer-pulse input
│
├── by input type
│   ├── Jira ticket key ..................... [⚠ 4/4]
│   ├── PFID-first .......................... [⚠ 1/1]
│   ├── Product name ........................ [⚠ 11/11]
│   ├── ITC direct .......................... [⚠ 5/5]
│   └── Jira + Product name ................. [○]
│
└── by output path
    │
    └── Path A — Curated Offer / EP Engineering [⚠ 21/21]
        ├── NES surface ..................... [⚠ 4/4]
        │   ├── Standalone offer
        │   │   ├── Champion resolved ....... [⚠ 1/1]
        │   │   └── NET-NEW build ........... [○]
        │   └── Offer Collection / Bundle
        │       ├── Curated offer resolved .. [⚠ 1/1]
        │       └── NET-NEW build ........... [○]
        │
        ├── CES surface (100% null pkg_id) .. [⚠ 14/14]
        │   ├── B0 contamination ............ [⚠ 1/1]
        │   └── B0 clean → chain
        │       ├── Step 1: PFID match ....... [⚠ 4/4]
        │       └── Step 1: no match
        │           ├── Step 2: keyword found . [⚠ 12/12]
        │           └── Step 2: no candidates . [⚠ 2/2]
        │               ├── Step 3: found ..... [○]
        │               ├── Step 3: API error .. [⚠ 1/1]
        │               └── Step 3: not found
        │                   └── Net-new confirmed [○]
        │
        └── Mixed NES + CES ................. [⚠ 3/3]

Edge cases (cross-cutting)
  ├── Champion identified wrong ............. [⚠ 1/1]
  ├── Champion ambiguous .................... [⚠ 5/5]
  ├── Net-new build confirmed ............... [⚠ 2/2]
  ├── API error (Step 3 / Merchandising) .... [⚠ 1/1]
  ├── B0 filter contamination ............... [⚠ 1/1]
  ├── CES keyword seeds incomplete .......... [⚠ 1/1]
  ├── Slug format mismatch .................. [⚠ 1/1]
  ├── Market gate not pre-answered .......... [⚠ 3/3]
  └── Surface ITC unrecognized .............. [○]
```

---

## Branch Detail

| Node | Confirmed Runs | Flagged | Flag Rate | First Seen | Last Seen | Example Run(s) |
|------|---------------|---------|-----------|------------|----------|----------------|
| input.jira | 4 | 4 | 100% | 2026-05-14 | 2026-05-14 | 2026-05-14T-BLIND CMS-31766 MSSL; 2026-05-14T00:30 CMS-31421 Email Essentials |
| input.pfid | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T15:00 TrustedSite dpp_precheck |
| input.product | 11 | 11 | 100% | 2026-05-13 | 2026-05-15 | 2026-05-15-UC-03 MENA Digital Kit; 2026-05-15-UC-02 Deluxe SSL NES Standalone |
| input.itc | 5 | 5 | 100% | 2026-05-13 | 2026-05-15 | 2026-05-15-UC-01 CA .CA domain NES Bundle; 2026-05-14T-EVAL-02 M365 Online Essentials blind |
| path_a | 21 | 21 | 100% | 2026-05-13 | 2026-05-15 | 2026-05-15-UC-03 MENA Digital Kit; 2026-05-15-UC-02 Deluxe SSL Standalone |
| path_a.nes | 4 | 4 | 100% | 2026-05-14 | 2026-05-15 | 2026-05-15-UC-03 MENA Digital Kit NES Bundle; 2026-05-15-UC-02 NES Standalone SSL |
| path_a.nes.standalone | 1 | 1 | 100% | 2026-05-15 | 2026-05-15 | 2026-05-15-UC-02 Deluxe Automated SSL DV Single Domain |
| path_a.nes.standalone.found | 1 | 1 | 100% | 2026-05-15 | 2026-05-15 | 2026-05-15-UC-02 dlxssl-001domain-tier1dv (offerId 35fc5321) |
| path_a.nes.bundle | 3 | 3 | 100% | 2026-05-14 | 2026-05-15 | 2026-05-15-UC-03 MENA Digital Kit (ambiguous); 2026-05-15-UC-01 CA .CA domain (found) |
| path_a.nes.bundle.found | 1 | 1 | 100% | 2026-05-15 | 2026-05-15 | 2026-05-15-UC-01 dpp-ca-ca-solution-tier1 (Collection e328092f) |
| path_a.ces | 14 | 14 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T00:00 Titan 14-day eval run 08; 2026-05-14T WAM Premium 4-arm CES |
| path_a.ces.b0_fail | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T21:00 WAM Premium (new_customer_orders filter excluded base PFIDs) |
| path_a.ces.b0_ok | 13 | 13 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T00:00 Titan 14-day eval 08; 2026-05-14T WAM Premium 4-arm CES |
| path_a.ces.step1_match | 4 | 4 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T WAM 4-arm CES (wsb-vnext-tier3 FOUND); 2026-05-14T00:30 CMS-31421 Email Essentials |
| path_a.ces.step1_fail | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T15:00 TrustedSite dpp_precheck (CONFIRMED_NO_MATCH) |
| path_a.ces.step2_found | 12 | 12 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T00:00 Titan 14-day eval 08 (6 matches); 2026-05-14T WAM 4-arm CES (15 matches) |
| path_a.ces.step2_fail | 2 | 2 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T WAM 4-arm CES (TrustedSite 0 matches); 2026-05-13T15:00 TrustedSite dpp_precheck |
| path_a.ces.step3_error | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T15:00 TrustedSite dpp_precheck (AvailabilityServiceInternalError) |
| path_a.mixed | 3 | 3 | 100% | 2026-05-13 | 2026-05-14 | 2026-05-14T CMS-32825 Deluxe SSL (NES existing + CES new PFIDs); 2026-05-14T09:00 MWP Basic SLP |
| edge.champion_wrong | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T21:00 WAM Premium CES (vnext-i18nox elevated instead of wsb-vnext-tier3/4) |
| edge.champion_ambiguous | 5 | 5 | 100% | 2026-05-13 | 2026-05-15 | 2026-05-15-UC-03 MENA Digital Kit (M365 vs Titan tier families); 2026-05-14T18:30 MWP Deluxe (o365 vs OX series) |
| edge.net_new_confirmed | 2 | 2 | 100% | 2026-05-14 | 2026-05-14 | 2026-05-14T WAM 4-arm CES (TrustedSite net-new); 2026-05-14T-BLIND CMS-31766 MSSL net-new |
| edge.api_error | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T15:00 TrustedSite dpp_precheck (Step 3 AvailabilityServiceInternalError) |
| edge.b0_contamination | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T21:00 WAM Premium CES (new_customer_orders > 0 excluded base annual PFIDs) |
| edge.keyword_seeds_incomplete | 1 | 1 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T15:00 TrustedSite dpp_precheck (only "precheck"+"dpp" seeds; needed vnext/wsb/wam/i18n) |
| edge.slug_mismatch | 1 | 1 | 100% | 2026-05-14 | 2026-05-14 | 2026-05-14T-BLIND CMS-31766 "offer-sslcert-managedWithMonitoring" vs "sslcert-managed-with-monitoring" |
| edge.market_missing | 3 | 3 | 100% | 2026-05-13 | 2026-05-13 | 2026-05-13T21:00 WAM Premium CES; 2026-05-13T17:00 Email Essentials dpp_precheck |

---

## Hypothetical Branches (not yet confirmed in log)

- Input: Jira + Product name (`input.jira_product`)
- NES Standalone → NET-NEW build (`path_a.nes.standalone.net_new`)
- NES Bundle → NET-NEW build (`path_a.nes.bundle.net_new`)
- CES Chain → Step 3: found (`path_a.ces.step3_found`)
- CES Chain → Step 3: not found → net-new confirmed (`path_a.ces.step3_not_found`)
- Surface ITC unrecognized (`edge.surface_unrecognized`)

These paths are structurally expected but have no log evidence yet.
