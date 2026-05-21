# Offer Pulse — Lever × Geometry Matrix

Tracks which pricing lever × offer geometry combinations the offer-pulse skill can reliably handle.
Updated by `/offer-matrix update` and `/offer-matrix evidence` commands.

## Coverage
Updated    : 2026-05-16
Total cells: 44  (2 N/A, 42 scoreable)
✅ reliable  : 5   (12% evidence-backed)
⚠️ partial   : 14  (33% theoretical — testable)
❌ unsupported: 23  (55% structural — blocked on architecture)

---

## [sale-price-discount × standalone]
Status     : ✅ reliable
Basis      : evidence
Evidence   : CMS-31421 2026-05-14T00:30 — temp-email-essentials-99 (DISC214228, 2,457 orders/7d on dpp_precheck) + temp-email-essentials-149 (DISC214229); both Standalone, Offer ID 575a7d2a, prePurchaseKeyMap absent; discount codes confirmed in billing and catalog. M365-OE-NOTEAMS-DPP runs 2026-05-13T19:00, 14T00:00, 14T-EVAL-02 — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb, DISC 365AF1F1CB, 192 orders/7d, Standalone confirmed.
Rationale  : Discount codes appear in billing (item_discount_code) and catalog (discountCode field on curated offer). Standalone geometry is deterministically confirmed via prePurchaseKeyMap absent. Champion found and cross-validated in 5 independent runs without errors.
Updated    : 2026-05-16

---

## [sale-price-discount × upsell]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : Upsell geometry (tier upgrade within same product) is not explicitly modeled. The skill can identify offers at adjacent tiers via billing but has no tier-relationship graph. A discounted upgrade offer may be found via Chain Step 2 ID scan if it exists in catalog — but the skill cannot confirm that the candidate is the correct upgrade path from the customer's current tier. No confirming run.
Updated    : 2026-05-16

---

## [sale-price-discount × add-on]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : Add-on geometry (same-category product depth) is discoverable via billing PFID + catalog chain. A discounted add-on offer should be findable if it exists in catalog with a discount code. However no run has specifically tested this combination — the discount code discovery path has only been confirmed on Standalone geometry. Requires one confirming run.
Updated    : 2026-05-16

---

## [sale-price-discount × bundle]
Status     : ✅ reliable
Basis      : evidence
Evidence   : Run 2026-05-14T09:00 — wordpress-openexchange-forever-ssl-basic, Offer Collection ID 4ce8a17c-b508-34ab-99d1-e5e5165214d3, components: WP Offer 566f8074 + Titan Email 927a9d45 (FREEACCOUNT) + Norton 72a57662; UUID discount codes in billing confirmed as pricing mechanism. Run 2026-05-14T18:30 — wordpress-o365-forever-ssl-deluxe (658d1af2) + wordpress-openexchange-forever-ssl-deluxe (ce0a7869) found via billing on slp_wordpress; overridePolicies noted.
Rationale  : NES Offer Collection (Bundle) champion found reliably via billing → catalog chain. Discount codes present at collection level confirmed in billing. Component IDs fully resolved. Multiple confirming runs on different bundle families.
Updated    : 2026-05-16

---

## [sale-price-increase × standalone]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : The skill can identify the current champion (the base offer to modify) reliably for Standalone geometry. The target price is analyst-provided and appears in the ticket. However the skill has no instruction to validate the new price against catalog overridePolicies constraints — it cannot confirm whether the increase is within allowed bounds. Output is partially useful (champion found, current pricing from billing) but incomplete (no price-cap validation).
Updated    : 2026-05-16

---

## [sale-price-increase × upsell]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : Same constraint as Standalone — champion findable, price-cap validation absent. Compounded by upsell tier-relationship gap: the skill cannot confirm which tier is the upgrade source.
Updated    : 2026-05-16

---

## [sale-price-increase × add-on]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : Same constraint as Standalone. Add-on offer is discoverable via catalog chain; new price is analyst-provided; no price-cap validation.
Updated    : 2026-05-16

---

## [sale-price-increase × bundle]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : Champion bundle is findable. However bundle pricing is more complex — the "new price" applies to a combined price that depends on component mix and overridePolicies. The skill retrieves overridePolicies from catalog but has no instruction to validate or produce a new combined-price override. More incomplete than the Standalone case.
Updated    : 2026-05-16

---

## [term-based-pricing × standalone]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : PFID matrix across terms is discoverable from billing (B0 returns all terms after GAP-001 fix). However GAP-015 means term gate fires in ~40% of runs — analyst input is still required to confirm which terms are in scope for the new offer. Multi-term standalone output is possible but requires analyst disambiguation. Not confirmed by a run specifically testing multi-term standalone configuration.
Updated    : 2026-05-16

---

## [term-based-pricing × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : No tier-relationship model exists in skill or data sources.
Rationale  : Term-based tier upgrade requires knowing both the term matrix per tier AND the upgrade relationship between tiers. Neither is modeled — the skill has no tier-graph and billing data does not encode tier-to-tier relationships. Structurally unsupported.
Updated    : 2026-05-16

---

## [term-based-pricing × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : No term-differentiated add-on configuration path in skill instructions.
Rationale  : Term-differentiated add-on pricing (e.g., different discount for 1yr vs 3yr add-on attachment) requires the skill to produce a per-term pricing table for an add-on product. No instruction or output field exists for this. Structurally unsupported.
Updated    : 2026-05-16

---

## [term-based-pricing × bundle]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : Run 2026-05-14T09:00 (MWP Basic) — skill identified both o365 (3yr PFID 1320706) and openexchange series with note "Mixed-term bundle (o365 has 3-year WP hosting + 1-year M365)". Term mismatch was flagged but not resolved.
Rationale  : Bundle term matrix is partially discoverable — the skill identifies that different components in a bundle have different billing terms and flags the mismatch. However it has no instruction to produce a per-term pricing configuration table for a bundle. Partially useful but output is incomplete.
Updated    : 2026-05-16

---

## [free-trial-ccb × standalone]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : Run 2026-05-13T14:30 — titanemail-light-freetrial-14days found in catalog (Standalone, offerId 927a9d45, plan=light, FREE_TRIAL BPO, autoRenew=false). Zero billing rows (PFID not in production). BLOCKING flag fired on missing PFID.
Rationale  : Skill finds the free trial offer in catalog and confirms geometry. However PFID not yet assigned is BLOCKING — the output cannot be filed as an engineering ticket without the PFID. The CCB mechanism (BPO type) is not explicitly validated in output. Partial: champion found, PFID gap surfaces correctly, but BPO configuration not confirmed.
Updated    : 2026-05-16

---

## [free-trial-ccb × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : No upsell tier model; free trial upgrade paths not in skill instructions.
Rationale  : Free trial with credit card requirement on an upsell path requires modeling the trial-to-upgrade conversion. No tier-relationship model and no BPO output fields. Structurally unsupported.
Updated    : 2026-05-16

---

## [free-trial-ccb × add-on]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : A free trial add-on component (purchaseType=Free with CCB BPO) is detectable via the GAP-010 fix — the skill checks for Free components in the catalog after chain resolution. Whether the BPO type (CCB vs BMAT) is correctly identified and output is unknown. No confirming run.
Updated    : 2026-05-16

---

## [free-trial-ccb × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : No BPO output fields in skill; bundle free trial configuration not modeled.
Rationale  : Free trial CCB on a bundle requires BPO configuration at the collection level — which component(s) trigger the trial, what the post-trial pricing is. These are overridePolicies/BPO fields the skill retrieves but does not parse or output. Structurally unsupported.
Updated    : 2026-05-16

---

## [free-trial-bmat × standalone]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BMAT = Bill Me After Trial. BPO type field not read or validated by skill.
Rationale  : BMAT encodes its commercial logic in the Billing Policy Override (BPO) type field in catalog — not in discount codes or geometry fields the skill reads. The skill cannot distinguish BMAT from CCB from CMAT in its output. Structurally unsupported across all geometries.
Updated    : 2026-05-16

---

## [free-trial-bmat × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read; upsell tier model absent.
Rationale  : Same BPO constraint as Standalone, compounded by missing tier-relationship model.
Updated    : 2026-05-16

---

## [free-trial-bmat × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [free-trial-bmat × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [free-trial-cmat × standalone]
Status     : ❌ unsupported
Basis      : structural
Evidence   : CMAT = Cancel Me After Trial. BPO type field not read or validated by skill.
Rationale  : CMAT encodes its commercial logic in the BPO type field — same structural gap as BMAT. The auto-convert vs auto-cancel distinction is invisible to the skill. Structurally unsupported across all geometries.
Updated    : 2026-05-16

---

## [free-trial-cmat × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read; upsell tier model absent.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [free-trial-cmat × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [free-trial-cmat × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [soft-bundle × standalone]
Status     : N/A
Basis      : na
Evidence   : —
Rationale  : Soft Bundle by definition requires combining multiple products. Standalone geometry (single product, no bundling) is mutually exclusive with Soft Bundle lever.
Updated    : 2026-05-16

---

## [soft-bundle × upsell]
Status     : N/A
Basis      : na
Evidence   : —
Rationale  : Upsell is a tier upgrade within the same product. Soft Bundle is a combination of multiple products. These are mutually exclusive — an upsell is not a bundle.
Updated    : 2026-05-16

---

## [soft-bundle × add-on]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : Run UC-01 2026-05-15 — dpp-ca-ca-solution-tier1 (domain + M365 email) is arguably a domain add-on depth bundle. 2-component NES collection; both components confirmed. The email component is a depth add-on within the communications category.
Rationale  : A soft bundle with add-on depth geometry (same-category add-on combined at a discount, e.g., domain + email) is partially supported — the NES collection chain handles it correctly when the bundle already exists. However the skill has no explicit instruction to produce a "depth add-on soft bundle" output distinct from a standard bundle. Classified as ⚠️ because it works in practice but is not a first-class output type.
Updated    : 2026-05-16

---

## [soft-bundle × bundle]
Status     : ✅ reliable
Basis      : evidence
Evidence   : UC-01 2026-05-15 — dpp-ca-ca-solution-tier1 (domainEmail collection e328092f, NewDomain + M365, disc000013, confidence 98%). UC-03 2026-05-15 — mena-digital-kit-tier1 (domainDudaEmail 7683d414, NewDomain + Duda + M365, disc000001) + mena-digital-kit-tier4 (domainProfessionalEmail c377d7de, NewDomain + Duda + Titan, disc000007), confidence 100%. Runs 14T09:00 + 14T18:30 — wordpress-o365-* and wordpress-openexchange-* bundles (3-component collections) confirmed with discount codes.
Rationale  : Soft Bundle × Bundle (Breadth) is the core NES Offer Collection use case — the skill was built around this geometry. Collection ID, all component Offer IDs + plans + discount codes are reliably resolved. Multiple product families confirmed across 5+ runs.
Updated    : 2026-05-16

---

## [lock-on-create × standalone]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Lock on Create = free trial followed by sale price for 1st term. Compound BPO configuration.
Rationale  : Lock on Create is a compound lever: it requires a trial-period BPO followed by a first-term overridePolicy. Both mechanisms are in catalog configuration fields (BPO type + overridePolicies) that the skill retrieves but does not parse or output. No single catalog field or discount code encodes the full Lock on Create configuration. Structurally unsupported across all geometries.
Updated    : 2026-05-16

---

## [lock-on-create × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Compound BPO; upsell tier model absent.
Rationale  : Same structural gap as Standalone, plus missing tier-relationship model.
Updated    : 2026-05-16

---

## [lock-on-create × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Compound BPO configuration not in output spec.
Rationale  : Same structural gap as Standalone.
Updated    : 2026-05-16

---

## [lock-on-create × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Compound BPO configuration not in output spec.
Rationale  : Same structural gap as Standalone.
Updated    : 2026-05-16

---

## [atmp × standalone]
Status     : ❌ unsupported
Basis      : structural
Evidence   : ATMP = Annual Term Monthly Payment. Billing policy override — annual commitment billed monthly.
Rationale  : ATMP is encoded as a BPO in catalog configuration — the annual commitment + monthly billing cycle combination is not derivable from billing product_term_unit_desc alone (which would show 'month'). The skill has no BPO output fields and cannot distinguish ATMP from a standard monthly offer. Structurally unsupported across all geometries.
Updated    : 2026-05-16

---

## [atmp × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read; upsell tier model absent.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [atmp × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [atmp × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : BPO type not read.
Rationale  : Same BPO constraint as Standalone.
Updated    : 2026-05-16

---

## [freemium × standalone]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : Run 2026-05-13T14:30 — titanemail-light-freetrial-14days found (Standalone, plan=light, purchaseType=FREE_TRIAL, autoRenew=false, rev 3). This is the free tier of a freemium-adjacent product. GAP-010 fix enables detection of purchaseType=Free components in billing. However the paid upgrade tier and the conversion trigger are not in the skill's output spec.
Rationale  : The skill can find the free-tier offer (purchaseType=Free or FREE_TRIAL) and confirm its geometry. It cannot model the paid upgrade path or the conversion mechanism. Partially useful for confirming what the free tier looks like; the upgrade arm requires a separate run for the paid tier.
Updated    : 2026-05-16

---

## [freemium × upsell]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Freemium upgrade path (free → paid tier) is not modeled.
Rationale  : The conversion from free to paid tier is the defining mechanism of Freemium. This is a tier-relationship (upsell intensity) that the skill has no data model for. Structurally unsupported.
Updated    : 2026-05-16

---

## [freemium × add-on]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Freemium depth add-on (free tier + paid add-on) not modeled.
Rationale  : A freemium offer with a paid add-on at depth requires modeling both the free base product and the add-on's purchase trigger. No instruction or output field covers this. Structurally unsupported.
Updated    : 2026-05-16

---

## [freemium × bundle]
Status     : ❌ unsupported
Basis      : structural
Evidence   : Freemium bundle conversion path not modeled.
Rationale  : Freemium bundle (free tier bundle that converts to paid bundle) requires modeling the bundle conversion trigger across components. Structurally unsupported.
Updated    : 2026-05-16

---

## [coupon-code × standalone]
Status     : ✅ reliable
Basis      : evidence
Evidence   : CMS-31421 2026-05-14T00:30 — temp-email-essentials-99 DISC214228 + temp-email-essentials-149 DISC214229 (both Standalone, 575a7d2a, confirmed in billing and catalog; clean run zero anomalies). Runs 13T19:00 + 14T-EVAL-02 — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb, coupon 365AF1F1CB, 192 orders/7d; all 26 candidates disclosed, Standalone confirmed. 5 total confirming runs on same champion.
Rationale  : Coupon codes are first-class fields in both billing (item_discount_code) and catalog (discountCode on curated offer). Standalone geometry confirmation is deterministic. Cross-validation of code between billing and catalog is reliable. Most consistently confirmed combination in the entire matrix.
Updated    : 2026-05-16

---

## [coupon-code × upsell]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : A coupon code on an upsell (tier upgrade discount) is theoretically findable — the discounted upgrade offer should exist in catalog with a discount code, discoverable via Chain Step 2 ID scan. However the tier-relationship gap means the skill cannot confirm it is the correct upgrade source. No confirming run.
Updated    : 2026-05-16

---

## [coupon-code × add-on]
Status     : ⚠️ partial
Basis      : theoretical
Evidence   : —
Rationale  : A coupon code on a same-category add-on is theoretically findable via the standard chain. discount code should appear in billing and catalog. No confirming run — only Standalone and Bundle coupon codes have been tested.
Updated    : 2026-05-16

---

## [coupon-code × bundle]
Status     : ✅ reliable
Basis      : evidence
Evidence   : UC-01 2026-05-15 — dpp-ca-ca-solution-tier1 disc000013 at curated offer level (domainEmail bundle, 2 components confirmed). UC-03 2026-05-15 — mena-digital-kit-tier1 disc000001 (M365 arch) + mena-digital-kit-tier4 disc000007 (Titan arch); all discount codes confirmed in catalog. Run 14T09:00 — wordpress-openexchange-forever-ssl-basic with UUID discount codes confirmed in billing.
Rationale  : Discount codes on NES Offer Collections (Bundles) are reliably findable — they appear at the curated offer level in catalog and cross-reference to billing. Component IDs and plans also confirmed. Multiple product families. No anomalies in confirming runs.
Updated    : 2026-05-16
