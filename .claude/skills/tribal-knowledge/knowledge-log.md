# Offer Pulse — Tribal Knowledge Log

## TK-001
Title      : package_id null/non-null is the ONLY authoritative CES vs NES signal
Status     : active
Category   : Domain Fact
Tags       : ces, nes, package_id, billing, cln
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : GAP-008, GAP-031

There is no CES/NES flag column anywhere in billing or CLN data. The only way to determine
which system a surface is running is to check whether `package_id` is non-null in
`add_to_cart_package_event_cln`. Non-null = NES. Null = CES. A product existing in the NES
catalog does NOT confirm the surface is running NES — only live billing data does.
The catalog-fos-automation-job (April 2024) registered many CES slugs in the NES catalog,
so catalog presence is unreliable as a routing signal.

Archive note : —
Archived     : —

---

## TK-002
Title      : Three distinct ID types all appear as package_id in CLN
Status     : active
Category   : System Behavior
Tags       : package_id, cln, ces, nes, ghost-id, term-alias
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : GAP-023

CLN `add_to_cart_package_event_cln`.`package_id` contains three completely different things:
1. True NES curated offer slugs — resolvable via get_curated_offer
2. CES merch-package term aliases with encoded suffixes (e.g. wsb_vnext_tier2_060mo →
   resolves to wsb-vnext-tier2 with Term 60:MONTH via merchandising API)
3. Ghost IDs — unresolvable in all three catalog systems (catalog-curated-offers,
   catalog-offers, merch-packages)
Any offer-pulse workflow must handle all three. A NOT FOUND result could be any of them.

Skill coverage note : Option 4 pre-classification filter added to Step A2a (2026-05-16).
  Before any get_curated_offer call, slugs are classified as CES term aliases (_NNNmo/_NNNyr),
  ghost IDs (nes-/offer- prefix, known ghost list), or valid NES slugs. NES% is recomputed
  after exclusion. Ghost and alias slugs appear in the Flags table, not as NOT FOUND errors.

Archive note : —
Archived     : —

---

## TK-003
Title      : _NNNmo and _NNNyr suffix slugs are CES term aliases, not NES
Status     : active
Category   : Naming Convention
Tags       : package_id, ces, term, slug, cln, wsb
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

Slugs with suffixes like `_060mo`, `_012mo`, `_012yr` are CES merchandising API aliases.
Example: `wsb_vnext_tier2_060mo` → resolves to package wsb-vnext-tier2 with Term `60:MONTH`.
The suffix encodes a term override. Despite appearing in CLN `package_id`, these are CES —
not NES. They will return NOT FOUND from get_curated_offer; look them up via get_package in
the merch-packages datasource instead.

Skill coverage note : Handled by Option 4 pre-classification filter (2026-05-16). Pattern
  `_\d+mo` and `_\d+yr` now excluded from NES catalog lookups in Step A2a. Flagged as
  "CES term aliases found" in the Flags table; NES% recomputed after exclusion.

Archive note : —
Archived     : —

---

## TK-004
Title      : nes- prefix is a CMT transport layer convention, not a ghost ID marker — strip
             prefix before catalog lookup; offer- prefix remains a true ghost
Status     : active
Category   : Naming Convention
Tags       : ghost-id, slug, not-found, catalog, nes, offer, prefix, cmt
Added      : 2026-05-16
Updated    : 2026-05-20 (reclassified — original conclusion was an overgeneralization)
Source     : ces-nes architecture review; corrected via GAP-042 investigation 2026-05-20
Related    : GAP-026, GAP-040, GAP-042

The `nes-` prefix is emitted by the CMT/page layer as a transport convention: the page sends
`nes-{slug}` as the pkgid field; the catalog stores the offer under the clean `{slug}` without
the prefix. Strip `nes-` and retry — the clean slug resolves. This is NOT a ghost ID marker.

Original (incorrect) classification (2026-05-16): Multiple `nes-` slugs tested in the
architecture review all returned NOT FOUND — `nes-social-first-starter`,
`nes-cpanel-set-2-ultimate-365-xtra`, `nes-wss-*-nortonsmb` family. The review concluded
the prefix meant "deprecated/pre-launch." This was an overgeneralization: those slugs were
ghost IDs *independently* (no catalog backing even after stripping), and the `nes-` prefix
was an observer artifact, not the cause. Confirmed broken by AGIGROWTH-228:
`nes-cpanel-set-1-economy-ssl-365-wss-xtra` has 6,018 add-to-cart events in 90 days;
stripping to `cpanel-set-1-economy-ssl-365-wss-xtra` resolves in catalog.

`offer-` prefix (e.g. `offer-airo-builder-professional`, `offer-titanemail-ultra`): still
a true ghost ID pattern. Consistently NOT FOUND with no strip-and-retry path confirmed.

Known genuine ghost list (ghost regardless of prefix): `nes-wss-tier0/1/2-nortonsmb-*`
family — these are NOT FOUND even after stripping. Keep on known ghost list.

Archive note : —
Archived     : —

---

## TK-005
Title      : OX email ≠ Titan Email in CES, but OX was swapped to Titan Email in NES migration
Status     : active
Category   : Historical Context
Tags       : ox, titan-email, migration, ces, nes, pfid, 1192198, 927a9d45
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

In CES, OX (OpenExchange) Professional Email is PFID 1192198 and appears in `*-ox` slug
packages. In NES, the migration swapped OX for Titan Email (component UUID 927a9d45) —
a different product with different plans. The FREEACCOUNT provisioning flag survived the
migration but the underlying product and billing term changed. A cPanel-ox CES package
and its NES equivalent offer different email products. Treat OX and Titan Email as distinct
products in CES; they coincide only in NES migration artifacts.

Archive note : —
Archived     : —

---

## TK-006
Title      : CES merchandising WebFetch must request raw JSON for specific PFIDs — never broad summary
Status     : active
Category   : System Behavior
Tags       : ces, merchandising, webfetch, pfid, json
Added      : 2026-05-16
Source     : ces-nes architecture review; feedback memory
Related    : —

The merchandising API endpoint https://merchandising.api.godaddy.com/v1/packages returns
200+ packages. WebFetch summarizes this incorrectly when asked broadly. The correct prompt
is: "Find all packages where pfids[] contains any of {pfid_list}. Return full id,
description, and pfids for each match — do not summarize." Without this explicit
instruction, WebFetch condenses the response and misses valid candidate packages,
producing false "no match" results or incomplete candidate tables.

Archive note : —
Archived     : —

---

## TK-007
Title      : apiVersion 3 curated offers have offerIds[] with internal IDs that return NOT FOUND
Status     : active
Category   : Historical Context
Tags       : apiversion3, entities-transformation-job, nes, component, not-found, june-2023
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : GAP-023

Curated offers created by the entities-transformation-job batch (2023-06-29) have apiVersion
= 3. Their offerIds[] arrays contain internal IDs not resolvable via get_offer_definition_by_id
— all return NOT FOUND. Affected products: IT services, SEO, DNS local listings, financing.
This is not a lookup error; it is an architectural limitation of the V3 format. When you see
apiVersion 3, do not attempt component resolution. Emit a disclosure: "V3 offer — component
IDs are internal and not resolvable via the catalog API."

Archive note : —
Archived     : —

---

## TK-008
Title      : diablo tag on NES offers is harmless migration metadata — offer is real and active
Status     : active
Category   : Naming Convention
Tags       : diablo, migration, nes, tag, catalog
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

Offer definitions with `diablo` tags and names like "BusinessHostingOffer <uuid>" were
machine-generated during the legacy CES-to-NES hosting migration pipeline (pipeline
internal name: Diablo). The tag is not a warning. The offer is real, active, and resolvable.
Do not flag diablo-tagged offers as test artifacts or stale migrations. They are production
offers in normal use.

Archive note : —
Archived     : —

---

## TK-009
Title      : temp- prefix curated offers are live production champions — never flag as test
Status     : active
Category   : Naming Convention
Tags       : temp, curated-offer, dpp_precheck, production, slug
Added      : 2026-05-16
Source     : ces-nes blind eval; feedback memory
Related    : —

Curated offers with slugs like `temp-email-essentials-99` and `temp-email-essentials-149`
are confirmed live production champions (verified on dpp_precheck as of 2026-05-14). The
`temp-` prefix is a naming artifact from how these offers were originally created, not a
signal of temporary or test status. Never add a warning or caveat about temp- prefix offers.
Treat them the same as any other active curated offer.

Archive note : —
Archived     : —

---

## TK-010
Title      : M365 catalog_query_get_offers returns 129K tokens — never Read the full result
Status     : active
Category   : System Behavior
Tags       : m365, catalog, catalog_query_get_offers, token-limit, bash-grep
Added      : 2026-05-16
Source     : AGIGROWTH-161 overnight analysis 2026-05-15
Related    : GAP-035

catalog_query_get_offers with tags=["m365"] returns 124+ plans at ~1K tokens each = 129K
total tokens. The Read tool 25K limit causes an error on every attempt. Never try to Read
the full result file. Instead, use Bash grep to extract specific plan names:

  grep -o '"planName":"[^"]*"' {result_file} | grep -i "{keyword}"

This applies to any broad tag query. Estimated safe tags: titanemail (~5 plans), wam
(~4 plans), professional-email (~6 plans) — these can be Read directly. m365 (~124 plans)
and sslcert (~40 plans) always require the grep path.

Archive note : —
Archived     : —

---

## TK-011
Title      : product_term_unit_desc is lowercase in billing — 'year' not 'Year'
Status     : active
Category   : Data Quirk
Tags       : billing, offer_pulse_experiment, term, sql, lowercase
Added      : 2026-05-16
Source     : pulse-audit regression tests 2026-05-14
Related    : GAP-002

The billing table `offer_pulse_experiment`.`product_term_unit_desc` stores values as
lowercase: 'year', 'month', 'quarter', 'semiannual'. Any WHERE clause using Title Case
('Year', 'Month') returns zero rows. Both UC5 and UC7 hit this silently before the fix —
one agent self-corrected on retry, the other may not. Always write term filters as lowercase.
This is a hard data contract; the column was never normalized to Title Case.

Archive note : —
Archived     : —

---

## TK-012
Title      : vnext-i18nox and vnext-i18no365 use base slugs on ALL surfaces — no -precheck suffix
Status     : active
Category   : Naming Convention
Tags       : slug, dpp_precheck, i18nox, i18no365, wsb-vnext, naming-convention
Added      : 2026-05-16
Source     : AGIGROWTH-186 overnight analysis 2026-05-15
Related    : GAP-038

Two distinct naming conventions exist for WAM/WSB slugs on dpp_precheck:
- wsb-vnext-* series: uses surface-specific suffix → wsb-vnext-tier3-precheck
- vnext-i18nox-* and vnext-i18no365-* series: uses BASE slug on all surfaces →
  vnext-i18nox-tier3 (no -precheck suffix)

Searching for "precheck" as a keyword seed finds wsb-vnext variants but returns zero
matches for i18nox and i18no365 families. Must run a second seed pass with ["i18nox",
"i18no365"] WITHOUT the "precheck" filter when searching for international WAM variants
at dpp_precheck. Confirmed by exhaustive catalog search: 3 of 7 expected packages were
missed via precheck-only seeds.

Archive note : —
Archived     : —

---

## TK-013
Title      : FOS means SLP surfaces (slp_*), not DPP surfaces (dpp_*)
Status     : active
Category   : Terminology
Tags       : fos, slp, dpp, terminology, surface
Added      : 2026-05-16
Source     : feedback memory
Related    : —

"Front of Site" (FOS) refers to Sales Landing Pages — the slp_* ITC family. It does NOT
refer to the Domain Purchase Path (dpp_*). This distinction matters for routing: FOS NES
curated offers live on slp_hosting_4gh and domain surfaces; dpp_precheck and dpp_config1
are CES (not FOS). When a ticket says "FOS", translate to slp_* before routing.

Archive note : —
Archived     : —

---

## TK-014
Title      : WAM in billing is product_pnl_line_name = 'Websites and Marketing' — exact match required
Status     : active
Category   : Data Quirk
Tags       : wam, billing, sql, product_pnl_line_name, wsb
Added      : 2026-05-16
Source     : feedback memory
Related    : —

The billing column `product_pnl_line_name` stores Websites and Marketing products as the
literal string 'Websites and Marketing'. Filtering on 'WAM', 'wsb', 'website', or any
other variant returns zero rows. This is the only billing column that identifies WAM
products — `product_pnl_subline_name` can be null for some WAM SKUs. Always filter with
exact match: WHERE product_pnl_line_name = 'Websites and Marketing'.

Archive note : —
Archived     : —

---

## TK-015
Title      : DEM = CA + AU + GB only — US excluded, DE (Germany) is NOT DEM
Status     : active
Category   : Terminology
Tags       : dem, market, billing, country_code, germany, canada, australia, uk
Added      : 2026-05-16
Source     : reference memory
Related    : —

DEM (Developed English Markets) = country_code IN ('CA','AU','GB'). US is always handled
separately. DE (Germany) sounds like DEM but is NOT in this group — it's a non-English
market. UK billing code is 'GB', not 'UK'. A query filtering for DEM that includes US or DE
will produce inflated counts. When a ticket says "DEM + US", that is two separate groups.

Archive note : —
Archived     : —

---

## TK-016
Title      : ROW filter excludes India by default — ROW+IN is a distinct override
Status     : active
Category   : Domain Fact
Tags       : row, india, market, billing, country_code, dem
Added      : 2026-05-16
Source     : AGIGROWTH-92 overnight analysis 2026-05-15
Related    : GAP-034

Standard GoDaddy ROW (Rest of World) filter:
  NOT IN ('US','CA','AU','GB','IN') — India excluded by default

ROW+IN override (explicitly includes India):
  NOT IN ('US','CA','AU','GB') — India included

Jira tickets that say "ROW & IN", "ROW including India", or "India + ROW" require the
ROW+IN filter. Silently using the default ROW filter understates geographic scope — India
is a high-volume market and its exclusion materially affects order counts.

Archive note : —
Archived     : —

---

## TK-017
Title      : NES curated offers are live only on domain surfaces and slp_hosting_4gh
Status     : active
Category   : Domain Fact
Tags       : nes, surface, ces, slp_hosting_4gh, domain, dpp
Added      : 2026-05-16
Source     : ces-nes architecture review; project memory
Related    : GAP-031

As of 2026-05-11, NES curated offers are confirmed live on:
- All domain purchase path surfaces (dpp_* domain packages)
- slp_hosting_4gh (90.3% NES, 16 curated offers, M365/OX variants)
- dlp_usoybo (single offer: oybo-en-email)
- dcc_* (Domain Control Center, apiVersion 3)

All other SLP, DLP, UPP, and MYA surfaces are CES. dpp_precheck and dpp_config1 are CES
(97–100%), despite being DPP surfaces — the DPP prefix alone does not mean NES.

Archive note : —
Archived     : —

---

## TK-018
Title      : planTier numbers encode CES bundle variant identity across both CES and NES
Status     : active
Category   : Naming Convention
Tags       : plantier, ces, nes, cpanel, slug, plan-name
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

The planTier number in CES PFID series and NES plan names encodes which variant of a
multi-variant bundle it represents. Key mappings:
  2000 = cPanel Economy (OX/Titan email variant)
  2003 = cPanel Economy (M365 variant)
  4000 = cPanel Ultimate (OX variant)
  4007 = cPanel Ultimate (M365 variant)
  30000 = Business Hosting Grow (no email / reseller)
  30003 = Business Hosting Grow (M365 variant)

The -ox slug suffix = OX/Titan Email component. The -365 slug suffix = M365 component.
The planTier difference (4000 vs 4007) is how CES and NES both distinguish these variants
in the same product family. In NES plan names: `economy2003StartupOfficebusinessps` decodes
as Economy, planTier 2003, Startup email, M365 Business Standard.

Archive note : —
Archived     : —

---

## TK-019
Title      : PFID 970473 (WAM Commerce annual) is in BOTH wsb-vnext-tier4 AND vnext-i18nox-tier4
Status     : active
Category   : Domain Fact
Tags       : pfid, wam, wsb-vnext, i18nox, dual-series, dpp_precheck, 970473
Added      : 2026-05-16
Source     : UC-T04 blind eval 2026-05-14; analyst confirmed
Related    : GAP-021, GAP-029

PFID 970473 (WAM Commerce annual term) is present in BOTH package series simultaneously:
- wsb-vnext-tier4: US/M365 variant (the correct champion for US-scoped tickets)
- vnext-i18nox-tier4: International/Titan Email variant

These represent different product configurations for different geographic scopes. Chain Step 1
merchandising API primary match returns vnext-i18nox-tier4 — the wrong choice for US-scoped
work. The dual-series continuation check must fire to surface both. For US-only scope,
wsb-vnext-tier4 is the correct champion.

Archive note : —
Archived     : —

---

## TK-020
Title      : The plan field on a curated offer is ONE PINNED SELECTION, not the full plan list
Status     : active
Category   : Domain Fact
Tags       : nes, curated-offer, plan, offer-collection
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

A curated offer's `plan` field contains one value selected from the parent Offer Collection's
full plan menu. Example: a VPS4 Offer Collection has 27 plans (linux/windows × managed/plesk
× 10 tiers); the curated offer pinned to it selects exactly one (e.g. `wm0044Standard`). To
see all available plans, call get_offer_collection_definition on the offerId UUID — the
collection's plan schema is the full menu. The curated offer's plan field is not a list; it
is the configuration that this specific named bundle represents.

Archive note : —
Archived     : —

---

## TK-021
Title      : package_id does NOT persist to order data — only ITC and PFID survive checkout
Status     : active
Category   : Domain Fact
Tags       : package_id, itc, pfid, order-data, billing, post-purchase
Added      : 2026-05-16
Source     : offer-pulse project CLAUDE.md
Related    : —

After a customer completes checkout, only two identifiers persist into order/billing data:
- PFID — the product SKU (what was sold)
- ITC — the surface/journey code (where they came from)

Package ID (the offer bundle shown at purchase time) is lost after checkout. This is the
core problem offer-pulse solves — reconstructing the package shown by joining CLN
add-to-cart event data BEFORE it is dropped. The CLN join must happen at the
add_to_cart_event_id level, not at the order level.

Archive note : —
Archived     : —

---

## TK-022
Title      : catalog-fos-automation-job April 2024 registered CES slugs in NES catalog — explains dual presence
Status     : active
Category   : Historical Context
Tags       : migration, fos-automation-job, ces, nes, april-2024, catalog, slug
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : TK-001, GAP-031

In April 2024, the `catalog-fos-automation-job` performed a sweep that registered many
previously-CES slugs (cPanel-set-*, wsb-vnext-*, wordpress-*-deluxe) in the NES catalog.
This is why CES packages often have catalog entries today. The NES catalog entry alone
does NOT mean the surface switched to NES — billing/CLN data is still the authoritative
signal. The automation job created dual presence: the CES merchandising API still serves
the offer on most surfaces, while the catalog has an NES record waiting to go live.

Archive note : —
Archived     : —

---

## TK-023
Title      : Professional Email component (2468b30f) is NOT inside any NES offer collection
Status     : active
Category   : Domain Fact
Tags       : professional-email, 2468b30f, nes, component, standalone
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : —

The Professional Email component offer (UUID 2468b30f, tag: professional-email) exists as:
- A standalone NES curated offer
- A component in CES atmp packages

It has NOT been found as a child component inside any NES offer collection. Unlike M365
(575a7d2a) and Titan Email (927a9d45) which appear bundled inside cPanel/MWP/WAM
collections, Professional Email appears to remain standalone in the NES catalog. Do not
expect to find it in prePurchaseKeyMap entries of multi-product bundles.

Archive note : —
Archived     : —

---

## TK-024
Title      : offersGrouping is UI-only — it carries zero provisioning behavior
Status     : active
Category   : Domain Fact
Tags       : nes, offersGrouping, prePurchaseKeyMap, provisioning
Added      : 2026-05-16
Source     : ces-nes architecture review
Related    : GAP-024

`offersGrouping` on an NES Offer Collection is a pure UI rendering hint — it tells the
frontend which products to show as "primary" (parentOffers) vs "included extras"
(childOffers). It has no effect on provisioning, pricing, or checkout behavior. All actual
provisioning overrides (free email, quantity limits, routing keys) live in
`prePurchaseKeyMap`. A component in offersGrouping.childOffers but absent from
prePurchaseKeyMap is zero-priced via a PRICE_OVERRIDE=0 policy — not via the key map.
SSL in cPanel bundles is the canonical example of this pattern.

Archive note : —
Archived     : —

---

## TK-025
Title      : office365-tier0 bundle includes M365 Email Backup as a second monthly-billed component
Status     : active
Category   : Domain Fact
Tags       : office365-tier0, dpp_precheck, m365, email-backup, pfid, bundle, discount-code
Added      : 2026-05-16
Source     : Precheck + Ecomm Collaboration Confluence (last modified 2026-05-11); live basket payload
Related    : —

The dpp_precheck NES email bundle `office365-tier0` is NOT just M365 Email Essentials. It
contains two components:

1. M365 Email Essentials — PFID 867688, productTypeId 466, 1-year annual term.
   Discount code: AES902437.
2. M365 Email Backup — PFID 996667, productTypeId 484, 24-month term billed MONTHLY.
   Discount code: disc333457. auto-renew: true.

The backup component's billing model is unusual: 24-month commitment, monthly billing cycle.
This means it will be invisible in billing queries that filter on product_term_unit_desc =
'year' — it is a 'month' term. If running offer-pulse on a dpp_precheck M365 email ticket
after migration, expect two PFIDs and two discount codes, not one. Confirmed via live Order
Shim basket payload in E2E testing (March 2026 test transaction).

Archive note : —
Archived     : —

---

## TK-026
Title      : offer-pulse reads surface-vocab.md after ITC resolution — surface_label and surface_nes_ces
Status     : active
Category   : System Behavior
Tags       : surface-vocab, surface_label, surface_nes_ces, itc, route-line, ces-only, offer-pulse
Added      : 2026-05-16
Source     : offer-pulse SKILL.md update 2026-05-16 (Option 2 — surface label enrichment)
Related    : GAP-017, GAP-031

After ITC resolution by any method, offer-pulse reads `.claude/skills/surface-vocab/surface-vocab.md`
and extracts two fields from the matching `## [ITC]` profile:
- `surface_label` — the Human label field (e.g. "Domain Purchase Path — Pre-Check")
- `surface_nes_ces` — the NES/CES classification (values: NES, CES, Mixed, CES (NES in progress))

These become working-state variables used to annotate three output locations:
1. ROUTE line — appends "(surface_label)" if resolved
2. CES-ONLY SURFACE disclosure — enriched with surface_nes_ces classification
3. Quick Reference Surface field — enriched with surface_label

The lookup is silent on miss — if the ITC has no full profile in surface-vocab.md, execution
continues without error. surface-vocab.md is the single authoritative vocabulary source for
surface annotations within offer-pulse. Do not hardcode surface labels in SKILL.md; they live
in the vocab file.

Archive note : —
Archived     : —

---

## TK-027
Title      : Vocab advisory fires only when NES%=0 AND vocab says NES or Mixed — never for CES
Status     : active
Category   : System Behavior
Tags       : vocab-advisory, vocab-note, nes, ces, routing, surface_nes_ces, pre-launch-nes
Added      : 2026-05-16
Source     : offer-pulse SKILL.md update 2026-05-16 (Option 1 — vocab advisory)
Related    : GAP-031, HE-004

The vocab advisory (`VOCAB NOTE:` line) fires only when BOTH conditions are simultaneously true:
1. NES% computed from billing data = 0% (zero NES package_id rows after pre-classification filter)
2. surface_nes_ces resolved to `NES` or `Mixed` in surface-vocab.md

It does NOT fire when:
- surface_nes_ces = `CES` or `CES (NES in progress)` (billing and vocab agree — no tension)
- The vocab lookup returned no result for the ITC (no profile to compare against)

This is a transparency-only signal. It does not change routing — the pre-launch NES check always
runs when NES%=0, regardless of whether the advisory fires. The advisory simply tells the analyst
why the pre-launch check is running: "vocab says this surface should be NES, but billing shows none."

Archive note : —
Archived     : —

---

## TK-029
Title      : M365 vs Titan Email on MWP follows the same US/International split as WAM
Status     : active
Category   : Domain Fact
Tags       : m365, titan-email, mwp, wordpress, us, international, market, slug, curated-offer
Added      : 2026-05-17
Source     : MWP Deluxe SLP offer-pulse run 2026-05-17
Related    : TK-019, TK-005

The wordpress-*-o365-* slug series = M365 email (US-primary); the wordpress-*-openexchange-*
slug series = Titan Email (international). This mirrors the WAM/WSB split documented in
TK-019 (wsb-vnext = US/M365; vnext-i18nox = International/Titan). Both MWP series run
simultaneously on the same surfaces — billing shows both UUID discount codes side-by-side.
On a US-scoped ticket, clone from the o365 variant (wordpress-o365-forever-ssl-deluxe,
wordpress-o365-forever-ssl-basic, etc.). The pattern is consistent across product lines:
-o365- in slug = M365 component; -openexchange- in slug = Titan Email component.
Confirmed 2026-05-17: slp_wordpress billing shows o365 series at ~10x volume vs OX series,
consistent with US-dominant data. Cross-reference GAP-021 and GAP-029 for the skill
mechanics of dual-series champion selection.

Archive note : —
Archived     : —

---

## TK-030
Title      : UUID-format item_discount_code in billing identifies the NES offerId being
             served on a CES surface
Status     : active
Category   : Data Quirk
Tags       : item_discount_code, uuid, ces, nes, offerid, billing, offer_pulse_experiment,
             slp_wordpress
Added      : 2026-05-17
Source     : MWP Deluxe SLP offer-pulse run 2026-05-17
Related    : TK-001, TK-022

When item_discount_code in offer_pulse_experiment stores a UUID-format value (dashes
replaced with underscores, e.g. 658d1af2_62be_333d_ba1d_41383bfa7b33), it is the offerId
of an active NES curated offer being served via a legacy CES billing mechanism — package_id
is null but the offer config is identified through the UUID. This is how CES billing on an
NES-capable surface references an NES series without a real package_id present.

To identify the NES series: restore dashes → look up via get_curated_offer(curatedOfferId).

Confirmed 2026-05-17: slp_wordpress showed two UUID discount codes mapping exactly to the
offerIds of wordpress-o365-forever-ssl-deluxe (658d1af2-...) and
wordpress-openexchange-forever-ssl-deluxe (ce0a7869-...). This is the key signal for a
surface that is billing 0% NES but actively serving NES offer configs — do not conclude
CES-only until UUID codes are checked.

Archive note : —
Archived     : —

---

## TK-031
Title      : wordpress-o365-forever-ssl-deluxe bundles 3 M365 licenses — quantityByOfferKey
             must carry forward on clone
Status     : active
Category   : Domain Fact
Tags       : m365, mwp, wordpress, quantitybyofferkey, quantity, clone, component, 575a7d2a
Added      : 2026-05-17
Source     : MWP Deluxe SLP offer-pulse run 2026-05-17
Related    : TK-029

The curated offer wordpress-o365-forever-ssl-deluxe carries quantityByOfferKey:
{"a581f39b-867b-3b80-b084-aa82e50287aa": 3} — provisioning 3 M365 licenses per purchase,
not 1. Offer key a581f39b maps to component offer 575a7d2a (M365). The Titan Email
counterpart (wordpress-openexchange-forever-ssl-deluxe) has no quantity override —
defaults to 1.

When cloning the o365 series, quantityByOfferKey must be explicitly included in the
engineering ticket. It is not part of the base Offer Collection definition — it lives on
the curated offer layer. Omitting it causes the new cloned offer to provision 1 M365
license instead of 3, silently underdelivering the expected email allocation. This is
invisible in billing (FREEACCOUNT = no revenue) and would only surface via a post-launch
provisioning audit.

Archive note : —
Archived     : —

---

## TK-032
Title      : Hivemind UPP discount experiment requires "UPPDCX" suffix AND "UPLIB" label — both are mandatory
Status     : active
Category   : System Behavior
Tags       : hivemind, upp, experiment, naming, uppdcx, uplib, discount-code
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : —

Two fields in Hivemind are required for UPP to pick up a discount code experiment, and both
must be correct simultaneously:
1. Experiment name must end with the suffix "UPPDCX" (stands for "discount code experiment").
   Typical pattern: `{descriptive-name}UPPDCX`, e.g. `dim_market_test_UPPDCX`.
2. Experiment must be labeled "UPLIB" (short for "upgrade library" — the legacy internal name
   for the UPP pricing system).

The UPP code looks for BOTH signals at runtime. If either is missing or misspelled, the
experiment is silently ignored — no error, no discount applied. Confirmed directly by
engineering in the March 2026 walkthrough: "it's not gonna work" without both.

Archive note : —
Archived     : —

---

## TK-033
Title      : Hivemind cohort JSON format for UPP — product type key + discount code array
Status     : active
Category   : System Behavior
Tags       : hivemind, upp, cohort, json, discount-code, wam, product
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-032

The "Add JSON" field on a Hivemind cohort for UPP discount experiments must follow this
exact format:

  { "WAM product": ["DISC-CODE-1", "DISC-CODE-2"] }

Key rules:
- Key = product type string (e.g. "WAM product", "365") — this must match the product type
  ID mapping hardcoded in the UPP codebase
- Value = array (square brackets) containing the exact discount code strings from the pricing
  team — DISC###### format codes
- Can include multiple product types in the same JSON object
- Even a single discount code must still be in an array: ["DISC123456"]
- Monthly discount codes are NOT separate keys — use the exact code(s) from pricing for all
  billing cycles

The UPP code reads this JSON and looks for matching product IDs to apply the discount codes.
Unrecognized key names are silently ignored.

Archive note : —
Archived     : —

---

## TK-034
Title      : UPP discount codes are defined at currency level, not per market
Status     : active
Category   : Domain Fact
Tags       : discount-code, currency, market, pricing, upp
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : —

Discount codes from the pricing team are scoped at the currency level, not per market.
Markets that share a currency share a discount code — this is NOT a perfect 1:1 mapping
of market to code. Some markets share currencies and therefore share a single discount
code; others are distinct. Practical impact: when requesting discount codes for DEM markets
(CA/AU/GB), three currencies are involved; when requesting for ROW, currency fragmentation
is much higher. Always clarify currency vs. market scope with the pricing team when
requesting codes for multi-market experiments.

Archive note : —
Archived     : —

---

## TK-035
Title      : Hivemind experiment propagation delay is ~25 minutes — not instant on save
Status     : active
Category   : System Behavior
Tags       : hivemind, propagation-delay, experiment, upp, testing
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-032

After saving or updating an experiment in Hivemind (including the initial JSON save and any
targeting rule updates), there is an ~25 minute propagation delay before the experiment is
live. During this window, the UPP code continues to read the old experiment state. This is
expected behavior — not a bug. When testing after experiment creation, wait 25+ minutes
before refreshing the upgrade library page to confirm the new discount code appears. If the
old code appears immediately after save, this is the delay in effect, not a configuration
error. The delay applies equally to test and prod environments.

Archive note : —
Archived     : —

---

## TK-036
Title      : UPP best-price guarantee — overlapping experiments always give customer lowest price
Status     : active
Category   : System Behavior
Tags       : hivemind, upp, best-price, concurrent-experiments, discount-code
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-032

If a customer is bucketed into two concurrent UPP experiments that both apply a discount
code to the same product, UPP will apply whichever code gives the customer the lowest price.
This is a hard guarantee — not randomized, not "first match wins" in the typical sense.
Practical consequences:
- Running two concurrent pricing experiments on the same cohort/product is unreliable for
  measurement — customers always drift to the cheaper option, confounding results
- Best practice confirmed by engineering: NEVER run two pricing experiments on the same
  cohorts concurrently. Run sequentially or in different variants instead
- If overlap is unavoidable, the customer WILL receive the best discount — this cannot be
  overridden

Archive note : —
Archived     : —

---

## TK-037
Title      : UPP supports 2 discount codes simultaneously; cart checkout supports only 1
Status     : active
Category   : System Behavior
Tags       : upp, cart, discount-code, stacking, ecom
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-036

The UPP layer can apply 2 discount codes at once (e.g. a rolled-out champion + a new
experiment variant). Cart checkout is limited to 1 discount code. This distinction matters
when stacking a rolled-out winner with a new sequential experiment: UPP handles the dual
code, but cart sees only one. When a prior experiment wins and is rolled out to 100%, there
is an open engineering ticket to clean up the monthly discount into a single unified discount
code — until that cleanup happens, two codes are active simultaneously (valid for UPP, but
the cart still resolves to one via best-price logic at checkout).

Archive note : —
Archived     : —

---

## TK-038
Title      : Hivemind Test→Prod is a COPY operation, not a promotion — traffic must be manually
             turned on in prod after copying
Status     : active
Category   : System Behavior
Tags       : hivemind, upp, test, prod, deploy, traffic, copy
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-035

The Hivemind workflow for moving a UPP experiment from test to production is:
1. Set up experiment in test environment
2. Add yourself to the variant approved list and verify the discount code flows through
3. From the test experiment, switch environment to "prod" and click Copy
4. This creates a SEPARATE COPY in production — it does NOT promote the test experiment
5. In the prod copy: run the duration calculator with BA team, then manually TURN ON TRAFFIC

Critical: turning on the traffic slider in prod goes live IMMEDIATELY — there is no staging
or grace period once traffic is enabled. The engineering team specifically called this out:
"be really conscious of doing that." If the slider is moved accidentally, the experiment is
live. Also: test and prod are independent copies — if you update the test experiment after
copying, the prod copy does NOT receive those updates (they are out of sync by design).

Archive note : —
Archived     : —

---

## TK-039
Title      : Hivemind MCP API cannot fill experiment details in test or prod — dev only
Status     : active
Category   : System Behavior
Tags       : hivemind, mcp, api, automation, experiment
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12; feature request logged
Related    : —

As of 2026-03-12, the Hivemind MCP API has a significant limitation: it can create an
experiment shell in the dev environment, but cannot fill in cohort JSON, targeting rules,
market filters, traffic allocation, or any other details via MCP API calls in test or prod
environments. All of those configuration steps require the Hivemind UI. A feature request
to enable full experiment configuration via MCP/API was raised during the meeting — not yet
delivered as of the meeting date. For any automation workflow that expects to create UPP
experiments programmatically, plan on the UI for test/prod configuration steps.

Archive note : —
Archived     : —

---

## TK-040
Title      : WAM pricing experiments require discount codes — sale price logic does not apply
             to WAM (upgrade/renewal product)
Status     : active
Category   : Domain Fact
Tags       : wam, discount-code, sale-price, upp, pricing, upgrade, renewal
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-033

WAM (Websites and Marketing) products are upgrade products — they are shown in-product to
existing customers as upsells, discounted off the renewal/list price. This means:
- WAM cannot use "new purchase sale price" logic for pricing experiments
- Discount codes are the ONLY lever for WAM pricing experiments in UPP
- Attempting to set a sale price for WAM experiments (as you might for front-of-site new
  purchase products) will not work in the UPP context

The exact words from the March 2026 walkthrough: "WAM doesn't work on new purchase sale
price logic because WAM is an upgrade... it is on the renewal price where we discount off
of the list price, the free to paid." When working on WAM pricing tickets, the required
output from /pricing-ticket or offer-pulse is always a discount code specification, not a
price point in the catalog.

Archive note : —
Archived     : —

---

## TK-041
Title      : Hivemind experiment targeting supports pathway filter (e.g. DPP only) via
             "pathway" targeting rule field
Status     : active
Category   : System Behavior
Tags       : hivemind, upp, targeting, pathway, dpp, rule-block
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : —

In Hivemind's targeting rules (rule block section), you can filter an experiment to a
specific pathway in addition to market filtering. The field name is "pathway" and the value
is the pathway identifier (e.g. "DPP" to target the Domain Purchase Path only). This was
confirmed live in prior shelf-of-trials experiments where the pathway field was used
successfully. The targeting rule system also supports arbitrary custom properties — if
a field you need is not already sent by the UPP code, the engineering team confirmed it is
relatively light work to add a new property to the context. Useful for scoping an experiment
to a specific surface or journey step without market-level filtering.

Archive note : —
Archived     : —

---

## TK-042
Title      : UPP discount experiments have three hard scope exclusions — BMAT path, direct-to-paid,
             and Arabic market
Status     : active
Category   : Domain Fact
Tags       : upp, bmat, direct-to-paid, ecom, scope, arabic-market, discount-code
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-040

UPP discount code experiments work for free-to-paid and paid-to-paid transitions but have
three confirmed scope exclusions:

1. BMAT path (Bill Me After Trial): Customers on the "bill me after trial" path from a free
   trial CANNOT receive UPP discount codes. This is an ecom billing agent limitation — the
   billing agent commits the customer to a price in a way that does not support discount code
   injection. Confirmed by engineering: "it's an E COM limitation with how billing agent
   actually commits a particular customer to a price."

2. Direct-to-paid (new purchase): The UPP discount code logic is not set up for direct
   new-purchase flows. It is available for free-to-paid upgrades and paid-to-paid upgrades
   only. Email in direct-to-paid does not work (as of March 2026); engineering noted it could
   be moved over.

3. Arabic market: UPP does not support the Arabic language market for these experiments —
   all other supported markets work.

Archive note : —
Archived     : —

---

## TK-043
Title      : Packaging and merchandising experiments in UPP go through Contentful, not Hivemind
             JSON — Hivemind JSON is discount codes only
Status     : active
Category   : Domain Fact
Tags       : contentful, hivemind, packaging, merchandising, upp, bundling
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-032, TK-033

The Hivemind cohort JSON for UPP is designed ONLY for discount codes. Packaging changes
(which products are bundled together) and merchandising changes (display, positioning) are
handled through Contentful CMS, not through the Hivemind experiment JSON. The coordination
mechanism is: create the Hivemind experiment ID, then in Contentful select that same
experiment ID for the merchandising/packaging variant. The two systems pick up the shared
experiment ID to coordinate a combined price + merchandising experiment.

Timeline as of the March 2026 meeting:
- Merchandising via Contentful: coming in the next few weeks (from 3/12)
- Packaging via Contentful: later still — requires capability graph integration
- Discount codes via Hivemind JSON: already live

Practical impact for offer-pulse: if a ticket asks for packaging changes on UPP, the
engineering path is Contentful + capability graph, not an EP catalog offer ticket. Only
discount code changes require Hivemind experiment JSON.

Archive note : —
Archived     : —

---

## TK-044
Title      : UPP discount codes should NOT be recycled — each experiment gets a fresh code
Status     : active
Category   : Domain Fact
Tags       : discount-code, recycling, pricing, experiment, cleanup
Added      : 2026-05-17
Source     : UPP Experiments Overview meeting recording 2026-03-12
Related    : TK-034

Discount codes for UPP experiments should be used once and retired. Engineering confirmed
this as a best practice recommendation: "we recommend we don't recycle discount codes."
Recycling a discount code (reusing a code from a prior experiment in a new one) makes
billing analysis ambiguous — billing rows for that code span multiple experiments with
different treatment conditions, making it impossible to cleanly attribute results to the
current experiment. Each new experiment should request fresh discount codes from the pricing
team. The work required from pricing is confirmed to be less than 24 hours at normal priority
(assuming scope is clear upfront and not changing). Plan ahead rather than making just-in-time
requests — having a pre-staged library of codes for upcoming experiments is better practice
than requesting them at launch.

Archive note : —
Archived     : —

---

## TK-045
Title      : FOS CES pricing is unidirectional — price-up experiments require raise-then-discount pattern
Status     : active
Category   : Domain Fact
Tags       : fos, slp, ces, pricing, discount-code, experiment, price-up, ces-package, token, atomic-deploy
Added      : 2026-05-17
Source     : AGIGROWTH-51 (TrustedSite FOS experiment, March 2026); Confluence playbook at
             https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4271539132/FOS+Experiments
Related    : TK-013, HE-004, HE-017

FOS renders prices using pricing tokens that read the ACTIVE CES package at render time:
  package[wsb-vnext-tier4].prices[12:month].salePrice[1:month]
Whatever CES package is active on a page determines what ALL customers see — FOS does not
hardcode prices. CES packages are site-wide blast radius: any change affects plan cards,
PDPs, homepage modules, and comparison tables simultaneously.

CES pricing is UNIDIRECTIONAL: FOS can only render prices ≤ the catalog sale price. There
is no mechanism to surcharge above the PFID sale price via the CES package layer.

To run a price-UP experiment on a CES FOS surface:
1. Raise the PFID sale price globally to the treatment price (affects ALL customers immediately)
2. Create a discount code that nets the price back to the original (pre-test) level
3. Create a new CONTROL CES package = PFID + discount code (renders original / current price)
4. Treatment CES packages = PFID only, no discount (renders new higher price)

ATOMIC DEPLOYMENT REQUIRED: Pricing change + discount code + CES package update + FoS publish
must all deploy together in the same coordinated window. Any step alone = broken pricing:
- Price ↑ without discount → treatment price exposed site-wide immediately (AGIGROWTH-51 incident)
- Discount without price ↑ → under-pricing
- Package publish alone → FoS blast radius across all plan cards, PDPs, homepage modules

Production-gated QA risk: catalog pricing cannot be deployed to prod-preview only. QA cannot
happen until pricing is live in production — creates a 1-3 day window where incorrect prices
may be customer-facing while bugs are found and fixed. Compress this window with tight
cross-team coordination (Pricing + CMS + FoS in a single release window).

Archive note : —
Archived     : —

---

## TK-028
Title      : surface-vocab Explore runs a reclassification sweep as step 4 — flags stale CES profiles
Status     : active
Category   : System Behavior
Tags       : surface-vocab, explore, reclassification, ces, nes, sweep, itc, stale-profile
Added      : 2026-05-16
Source     : offer-pulse SKILL.md update 2026-05-16 (surface-vocab Explore step 4)
Related    : —

`/surface-vocab explore` always runs a CES-to-NES reclassification sweep as its step 4. The sweep:
1. Queries the top 20 CES-profiled ITCs from billing data (last 7 days)
2. Checks whether any have NES package_id values present now (has_nes_now = NES)
3. Flags any ITC where billing shows NES activity but the profile says CES

The sweep does NOT auto-update profiles. It is flag-only — the analyst must review and confirm
before re-profiling. This prevents a surface that has migrated from CES to NES from silently
continuing to route as CES in offer-pulse. The sweep catches the migration as soon as billing
data shows NES package_ids on the surface. Consistent with the broader principle: validate
NES migration in data before changing any skill behavior.

Archive note : —
Archived     : —

---

## TK-046
Title      : Exact curated offer variant requires dev tools (F12) confirmation
Status     : active
Category   : Domain Fact
Tags       : curated-offer, dev-tools, f12, champion, variant, clone, slp_hosting_4gh,
             dlp_hosting, base-offer, offer-collection
Added      : 2026-05-21
Source     : Teams thread with Tony Hill (EP engineering), AGIGROWTH-228 investigation 2026-05-21
Related    : GAP-042

When billing data identifies a base offer collection (e.g. 05730877-89bd-49c0-8fff-c9880b743bf0
for cPanel hosting) that has multiple curated offer variants mapped to it (e.g. cpanel economy
-365 variants vs -ox variants, each tied to different term/email combinations in billing),
data alone cannot uniquely select which exact slug is currently live on the page. Offer-pulse
can reliably identify the base offer collection and plan, but the last-mile "which curated
offer variant to clone" question requires human confirmation.

The ground-truth method: open browser dev tools (F12 → Network tab) on the target surface,
then trigger the product card / pricing call. The request to the GoDaddy pricing or catalog
API will reveal the exact curated offer slug being served. Tony Hill's EP team did a POC
screen-scrape of curated offers using this same principle and confirmed it works.

Practical example from AGIGROWTH-228: starting from a 3-year term PFID (1338734) yields
base offer 05730877 + plan economy_2000. But the specific curated offer to clone
(nes-cpanel-set-1-economy-ssl-365-wss-xtra, stripping nes- prefix) only appears in billing
under the 1-year PFID (1338722) — the 3-year anchor misses it. Dev tools on the live
slp_hosting_4gh / dlp_hosting page would have surfaced the correct slug directly.

Offer-pulse output implication: when multiple curated offer variants map to the same base
offer collection and the billing path does not uniquely resolve one, emit a BLOCKING
confirmation step pointing the analyst to dev tools before filing the engineering ticket.

Archive note : —
Archived     : —

---

## TK-047
Title      : dpp_precheck product mix is domain protection + email — NOT WAM or MHWP
Status     : active
Category   : Domain Fact
Tags       : dpp_precheck, precheck, product-mix, domain-protection, m365, email, mhwp,
             wam, ces, migration
Added      : 2026-05-22
Source     : CLN add_to_cart_product_event_cln query 2026-05-22; offer_pulse_experiment
             precheck ITC breakdown
Related    : TK-017, TK-025

dpp_precheck is a domain checkout upsell surface — it fires add-to-cart CLN events but
has 0 package_ids on every product (confirmed CES, not a cart bypass issue). Top products
by CLN event volume (7-day window as of 2026-05-22):

  Full Domain Protection (all market variants)   ~55K events
  Microsoft 365 Email Essentials                 ~14K events
  Professional Email Pro Light                    ~4K events
  M365 Email Essentials with Security             ~1.5K events
  Online Essentials                               ~1.4K events
  Domain Ownership Protection                      ~350 events
  .COM / .ME / .IN domain registrations           small volume

Two common assumptions that are WRONG:
1. MHWP (Managed Hosting for WordPress) is on precheck — FALSE. Zero CLN events for
   any managed wordpress product on precheck. MHWP is not sold through this surface.
2. WAM website builder products dominate precheck — FALSE. WAM is not significant
   precheck volume. "Online Essentials" (~1.4K) may be WAM-adjacent but it is negligible.

Migration roadmap implications:
- Full Domain Protection: no NES migration date as of 2026-05-22
- M365 Email: target 6/30/2026 (E2E testing active); NES offer = office365-tier0
- Professional Email: no migration date
- WAM (if any): Q3 2026 TBD

When the CES migration story is told ("precheck will gain package_ids once WAM/email
migrates"), the accurate framing is: domain protection + email products, with domain
protection as the #1 volume driver. Domain protection has no confirmed migration date
and represents the majority of precheck volume — the migration unlocks email first,
not domain protection.

Archive note : —
Archived     : —

---

## TK-048
Title      : Remaining CES migration has low ceiling for offer pulse coverage improvement
Status     : active
Category   : Domain Fact
Tags       : offer-pulse, ces, migration, coverage, dpp_precheck, domain-protection,
             cart-bypass, upp, dpp, null-itc
Added      : 2026-05-22
Source     : offer_pulse_experiment + CLN precheck investigation 2026-05-22
Related    : TK-047, TK-001

The narrative "once WAM and email on precheck migrate, offer pulse will have more coverage"
overstates the impact. CLN-confirmed analysis shows the ceiling is low:

WHAT MIGRATION FIXES (precheck specifically):
- M365 Email Essentials (~14K events/week) gains package_id after 6/30/2026
- Professional Email Pro Light (~4K/week): no migration date — stays CES

WHAT MIGRATION DOES NOT FIX:
- Full Domain Protection (~55K events/week on precheck, ~73% of precheck volume):
  no NES migration date as of 2026-05-22. This is the dominant precheck product.
- DPP non-precheck (dpp_config1: ~72K orders/7d, 100% CES): not on any migration roadmap
- UPP surfaces (~97K orders/7d, 100% CES): not on any migration roadmap
- Cart bypass: ~46% of purchases skip the add-to-cart event entirely — structural gap,
  CES→NES migration cannot fix this
- Null ITC bucket: eComm API was never passed an ITC at purchase time — not a CES/NES issue

COVERAGE CEILING ON PRECHECK:
Even after the 6/30/2026 M365 email migration, ~80%+ of precheck add-to-cart volume
remains CES (domain protection + professional email + minor products). The FOS category
missing rate in offer_pulse_experiment will improve only marginally.

BOTTOM LINE FOR OFFER PULSE:
The remaining CES migration is a data quality win for specific products (M365 email on
precheck). It is not a meaningful coverage inflection point for offer pulse overall.
The dominant precheck product — Full Domain Protection — has no migration date. The
precheck gap in offer pulse is a domain protection coverage problem, not an email/WAM
problem.

Archive note : —
Archived     : —

---

## TK-049
Title      : Three distinct reasons why package_id is NULL in offer_pulse_experiment
Status     : active
Category   : Domain Fact
Tags       : package_id, null, offer_pulse_experiment, cart-bypass, itc-mismatch, ces, pipeline
Added      : 2026-05-31
Source     : Validation thread with Daniel Laris, 2026-05-31
Related    : TK-001, TK-021, TK-048, GAP-042

package_id is NULL for a row in offer_pulse_experiment for one of three distinct reasons:

1. Cart bypass — the customer went directly from impression to checkout without an
   add-to-cart event firing. No cart event means no package_id was ever captured.
   The pipeline has nothing to join on.

2. ITC mismatch — the ITC recorded at the cart step did not match the ITC recorded
   at purchase. The join between add-to-cart events and billing uses ITC as a key;
   when the two ITCs diverge (e.g. referring ITC vs referred ITC at add-to-cart),
   the lookup misses and package_id is left NULL even if the offer was NES.

3. CES by design — the product has no package_id because it was served through the
   CES legacy system. No package_id was ever emitted.

Implication: the ~42.5% null figure in completed transactions is NOT purely a CES
coverage problem. An unknown portion of those null rows are NES products that lost
their package_id due to cart bypass or ITC mismatch — infrastructure gaps, not CES/NES
classification gaps. The three causes are not distinguishable from offer_pulse_experiment
alone. This means NES migration alone will not close the full null gap — cart bypass and
ITC mismatch are structural pipeline issues that exist independently of CES/NES status.

Archive note : —
Archived     : —

---

## TK-050
Title      : office365-tier0 carries ITC slp_powerbi on /email hub and /business/office-365, but slp_365_email on the professional email sub-page
Status     : active
Category   : System Behavior
Tags       : office365-tier0, slp_365_category, slp_365_email, slp_365, itc, email, m365, live-surface
Added      : 2026-06-02
Source     : live-surface scrape observation

The M365 Email Essentials package (`office365-tier0`) appears on three M365 email pages with
different embedded ITCs depending on the page:
- `/email` (hub, slp_365_category): office365-tier0 carries ITC `slp_powerbi`
- `/email/professional-business-email` (slp_365_email): office365-tier0 carries ITC `slp_365_email`
- `/business/office-365` (slp_365): office365-tier0 carries ITC `slp_powerbi`

This is not a scraper error — it reflects how each page's Sitecore config embeds the ITC.
The "canonical" ITC for Email Essentials purchases that originate on the professional email
sub-page is `slp_365_email`. The `slp_powerbi` ITC on the hub and business page is anomalous
and may cause billing attribution confusion.

Archive note : —
Archived     : —

---

## TK-051
Title      : errorRedirectUrl pointing to /godaddy-503 observed in page source of M365 email pages
Status     : active
Category   : System Observation
Tags       : live-surface, email, m365, errorRedirectUrl, page-source, scraper
Added      : 2026-06-02
Source     : analyst observation during /live-surface inspection of /email

The page source of https://www.godaddy.com/email (and possibly other M365 email pages)
contains `"errorRedirectUrl": "https://www.godaddy.com/godaddy-503"`. This is a fallback
redirect URL embedded in the page config — likely a Sitecore or component-level error
handler that redirects users to the standard 503 maintenance page if the component fails
to load. Not a signal of an active error; it is a static config value. Analysts doing
manual page inspection should not interpret its presence as indicating a problem unless
the page is actually failing to render plan boxes.

Archive note : —
Archived     : —
