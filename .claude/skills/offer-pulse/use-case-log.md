# Offer Pulse — Use Case Log
<!-- append-only; one entry per run; written by offer-pulse after every output -->

## Run 2026-05-13T21:00 — Product-first: WAM Premium + Commerce annual, TrustedSite bundle, FOS surfaces

Date            : 2026-05-13T21:00
Entry type      : Product name + experiment description
Entry value     : "WAM Premium and Commerce annual SKUs, TrustedSite bundle experiment, FOS surfaces (slp_wsb_* ITCs), new customers only, global market, CES package request, +$2–$3/month treatment + discount-code control packages"
Path            : A — Curated Offer
Offer operation : Create — CES Package Request
Mode            : N/A
NES/CES branch  : CES — 100% (all FOS billing rows for WAM Premium/Commerce had null package_id)
Gate asked      : Market (confirmed global), Customer segment (confirmed new only), Term (confirmed annual)
CES chain steps : B0 fail — new_customer_orders > 0 filter excluded PFIDs 958797 and 958799 (base annual SKUs with no/minimal recent new-customer billing); WebFetch returned wsb-vnext-tier3-disc (discounted variant) not wsb-vnext-tier3 (base, includes 958797); Step 2 keyword scan surfaced vnext-i18nox-tier3/tier4 and wsb-vnext-tier3/tier4 as candidates; wrong champion elevated
Champion        : WRONG — identified ambiguous geo-split (wsb-vnext-tier3/4 + vnext-i18nox-tier3/4); correct answer was wsb-vnext-tier3 and wsb-vnext-tier4 globally (TrustedSite bundle is US/global; vnext-i18nox series is international Titan variant, not applicable)
Flags fired     : MISSED CES PACKAGES, B0 new_customer_orders filter contamination, WebFetch discounted variant surfaced instead of base package, Missing CES email addon PFID 464069 (product-email), Wrong high-volume renewal PFIDs included (966982/966984/970472/970482 are legacy renewal SKUs not package-managed), Wrong Commerce champion elevated (vnext-i18nox-tier4 instead of wsb-vnext-tier4)
Ticket preview  : Requested (for self-assessment)
Notes           : MISSED CES PACKAGES — wsb-vnext-tier3 and wsb-vnext-tier4 were the correct champions. Root cause 1: B0 PFID discovery query applied `new_customer_orders > 0` filter, which excluded PFIDs 958797 (WAM Premium annual base) and 958799 (WAM Commerce annual base) — these have zero or minimal recent new-customer billing but ARE required components of the correct packages. Fix: B0 must discover all PFIDs for the product across all customer segments; new-customer filter belongs in A1/B1 experiment queries only, not in B0 discovery. Root cause 2: WebFetch of full /v1/packages JSON returned wsb-vnext-tier3-disc (discounted variant) instead of wsb-vnext-tier3 (base package containing 958797); WebFetch summarizes instead of parsing, and surfaced the discounted variant prominently. The merchandising API PFID match step is the authoritative source for package composition — billing-first approach inflated wrong high-volume renewal PFIDs (966982/966984) as primary. Root cause 3: Email addon component PFID 464069 (product-email, CES) was not resolved — skill resolved email through NES catalog layer (offer UUID 575a7d2a) instead of identifying CES PFID 464069. Correct packages each include product-email addon with PFID 464069, purchaseType=Free, 1-year fixed term, autoRenewal=false, FREEACCOUNT=true. Analyst confirmed diagnosis and provided ground truth JSON for wsb-vnext-tier3 and wsb-vnext-tier4.

## Pulse Audit — 2026-05-13T20:00

Date            : 2026-05-13T20:00
Audit type      : pulse-audit
Runs analyzed   : 5 (2026-05-13T14:30 → 2026-05-13T19:00)
Path split      : A: 5 (100%) | B: 0 (0%)
NES/CES split   : CES 80%, Mixed 20% (of Path A)
Champion stats  : Found 3 (60%), Ambiguous 1 (20%), N/A 1 (20%)
Anomaly rate    : 5/5 (100%)
Issues found    : 4 systemic issues
Issue #1 status : CLOSED — CES ticket preview omitting Base Offer ID/Plan/discount code — Wendy fix applied to SKILL.md this session (Catalog Resolution block + carry-forward rule added)
Top open issue  : B0 term filter contamination (Skill Gap) — term filter in B0 discovery query caused missed bundle in Run 18:00; fix = explicit prohibition on term filtering at B0 stage; filter belongs in A1/B1 only
Flag spike      : "Plan not specified" — only flag above 30% threshold (2/5 = 40%)
Gate spike      : Term asked in 80% of runs (4/5)
Wendy prompt    : Issue #2 brief provided; Wendy invocation pending analyst approval

## Run 2026-05-13T15:00 — PFID-first: 1834961, 1834962 (TrustedSite) on dpp_precheck

Date            : 2026-05-13T15:00
Entry type      : PFID-first
Entry value     : PFIDs 1834961, 1834962 — TrustedSite add-on, WAM FOS Precheck surface (dpp_precheck)
Path            : A — Curated Offer
Offer operation : Modify — Add Component
Mode            : N/A
NES/CES branch  : CES — 0 NES package_ids in billing for dpp_precheck (7d window)
Gate asked      : Offer Operation, Term
CES chain steps : Step 1: fail (merchandising CONFIRMED_NO_MATCH for PFIDs 1834961/1834962) | Step 2: fail (0 keyword matches in 1,200 IDs for "trustedsite") | Step 3: fail (API error — AvailabilityServiceInternalError)
Champion        : N/A (Modify path)
Flags fired     : ITC billing gap, TrustedSite net-new (two-step ticket required), Plan not specified, dpp-solution-set scope unclear, Discount codes on existing packages, Chain Step 3 API error
Ticket preview  : Requested
Notes           : MISSED PACKAGES — 7 CES packages required for Step 2 were absent from the Existing Packages on Surface table: vnext-i18no365-tier2-precheck, vnext-i18nox-tier1-precheck, vnext-i18nox-tier3-precheck, vnext-i18nox-tier4-precheck, wsb-vnext-tier1, wsb-vnext-tier3, wsb-vnext-tier4. Root cause: Step M1 ID scan used only "precheck" and "dpp" as keyword seeds; WAM precheck surface requires additional seeds (vnext, wsb, wam, i18n). This would have produced an incomplete Step 2 package list and an incorrect ticket to ecomm. Also: Run Logger step was not executed by offer-pulse at end of session — this entry was written manually via pulse-audit.

## Run 2026-05-13-ASSESS-CMS32825 — CES use case assessment: CMS-32825 Deluxe Automated SSL

Date            : 2026-05-13T-ASSESS
Entry type      : Jira / Product name
Entry value     : "CMS-32825 — Deluxe Automated SSL, 29 CES packages for SSL SLP → SSL Config"
Path            : A — Curated Offer
Offer operation : Create (net-new CES packages)
Mode            : N/A
NES/CES branch  : CES confirmed — slp_ssl_config shows 100% CES for DV PFIDs in range; 28 NES dlxssl-* curated offers exist in catalog but serve slp_ssl not slp_ssl_config; OV range PFIDs (1916658–1916670) zero billing (net-new confirmed); DV Single Domain PFIDs (1859854–1859862) ~130 orders on slp_ssl_config — contradicts ticket's "no FOS presence prior" claim
Gate asked      : Market (Reseller implied but not explicitly specified); Term (7 variants per group listed but not disambiguated for which terms apply to which packages)
CES chain steps : Billing → slp_ssl_config 100% CES for DV PFIDs; Merchandising API → no existing CES packages for target PFIDs; Catalog scan → 28 dlxssl-* NES offers found, not applicable to CES surface; Net-new build confirmed for all 29 groups
Champion        : None — no existing CES packages; 28 NES dlxssl-* curated offers exist but cannot serve SSL Config (CES-only surface); DV group already selling CES on slp_ssl_config without package_id
Flags fired     : Product name mismatch ("Deluxe Automated SSL" not in billing; internal name is "dvSingleDomain SSL|Subs|DV"); DV PFIDs partially live despite net-new claim; NES offers for same product on different surface create false-candidate risk; PFID range query unreliable (range spans domain name products)
Ticket preview  : Not requested
Notes           : Input quality issues: no market specified (Reseller stated as requirement but offer-pulse has no gate for this); PFID list given as approximate ranges not flat list — range-based billing query spans unrelated products; product marketing name diverges from billing product_name — name-based lookup fails; "no FOS presence" claim partially inaccurate — DV group has ~130 orders on slp_ssl_config; 29 package count includes 7 terms × ~4 domain configs per tier — not explicit in breakdown
Assessment      : PARTIAL MATCH — offer-pulse correctly identifies CES path and net-new build need, but would fail the product name lookup, miss the DV-group pre-existing billing discrepancy, and return 28 NES catalog offers as false candidates without surface-context filtering
Input quality   : Missing market (Reseller required); PFID list given as ranges not flat list; product marketing name ≠ billing product_name; "net-new" claim inconsistent with DV group billing history

## Run 2026-05-13-ASSESS-CMS32651 — CES use case assessment: CMS-32651 Email Backup SAPI Package

Date            : 2026-05-13T-ASSESS
Entry type      : Product name
Entry value     : "CMS-32651 — Email Backup, OrderShim/Cart, DISC004590, template: o365backup"
Path            : A — Curated Offer
Offer operation : Create
Mode            : N/A
NES/CES branch  : CES — 100% (3 PFIDs: 996667 Microsoft 365 Email Backup 1mo, 996668 Renewal 1mo, 1499849 Email Backup Renewal 1mo; zero NES orders, zero package IDs across all ITCs)
Gate asked      : Market (not specified); Term (not specified — referenced "o365backup package" as proxy, which is not a real term); Surface/ITC ("OrderShim" not a standard ITC — no Email Backup billing rows on cart_* or sapi_* ITCs)
CES chain steps : Product name search → FOUND PFIDs 996667/996668/1499849; ITC match for OrderShim/Cart → NO MATCH; Merchandising API for o365backup → NOT FOUND (pfid 996667 appears only as addon inside M365 packages, not as standalone); Catalog MCP for o365backup → NOT FOUND; Backup-related NES slugs found (email-business-essentials-backup etc.) all use disc209800 not DISC004590
Champion        : NONE — o365backup template does not exist in any system; structural template unresolvable
Flags fired     : PFID not provided (listed as "same as o365backup" — not a real PFID); template o365backup not found in merchandising API or catalog MCP; surface "OrderShim/SAPI" has no Email Backup billing rows; DISC004590 not in Email Backup billing history; Market not specified
Ticket preview  : Not requested
Notes           : Two structural input problems: (1) template package o365backup does not exist as a standalone CES package — appears only as addon within M365 packages; (2) "OrderShim/Cart checkout" does not produce Email Backup billing rows — surface is an engineering-side construct (order intake layer), not a customer-facing ITC string. Email Backup sells exclusively via in-product/app ITCs (app_o365_*, mgr_slp_365_*, upp_o365product_*). Three distinct PFIDs present; ticket did not specify which. All existing backup NES offers use disc209800, not DISC004590.
Assessment      : PARTIAL MATCH — offer-pulse correctly determines CES path and finds PFIDs + term, but cannot produce complete CES package creation payload: (a) template o365backup unresolvable, (b) surface ambiguous/unrecognized, (c) PFID not specified between new/renewal variants, (d) market not specified
Input quality   : PFID missing (listed as "same as o365backup"); Term missing (same ref); Market not specified; Surface "OrderShim" not a standard ITC string; Template reference o365backup does not exist in merchandising API or catalog MCP

## Run 2026-05-13-ASSESS-CMS31766 — CES use case assessment: CMS-31766 MSSL + Malware Monitoring

Date            : 2026-05-13T-ASSESS
Entry type      : PFID-first + Product name
Entry value     : "CMS-31766 — Managed SSL + 5 Malware Monitoring, SSL SLP → SSL Config, PFIDs 1840827/1840829/1840831/1840833/1840835"
Path            : A — Curated Offer
Offer operation : Create
Mode            : N/A
NES/CES branch  : CES declared by ticket; contradicted by billing — SSL surfaces (slp_ssl, slp_ssl_managed, hmc_dv_ssl) show 100% NES in last 30 days; PFIDs 1840827/29/31/33/35 have zero billing rows (SKUs not yet in production)
Gate asked      : Market (not specified in ticket — Reseller implied); Term (5 terms provided in PFID list, no ambiguity)
CES chain steps : Billing lookup for PFIDs → 0 rows; Merchandising API PFID scan → no packages; Keyword scan (managed-ssl, mssl, malware, monitoring) → no CES package match; Direct slug "offer-sslcert-managedWithMonitoring" → NOT FOUND; Full catalog scan 1,200 offers → found "sslcert-managed-with-monitoring" (plan=managedWithMonitoring, active, modified 2026-04-23); same offerId (28e5b730) aliases as ssl-managed-005sites-tier1
Champion        : None (CES). NES reference identified: sslcert-managed-with-monitoring (plan=managedWithMonitoring, active)
Flags fired     : Slug format mismatch — ticket uses "offer-sslcert-managedWithMonitoring" (offer- prefix + camelCase); catalog uses "sslcert-managed-with-monitoring" (kebab-case, no prefix); direct lookup fails; CES-only constraint contradicted by data — SSL surfaces show 100% NES in billing; PFIDs not in production — cannot validate 4yr term from data; Market not specified
Ticket preview  : Not requested
Notes           : NES reference exists but under different slug format. CES-only constraint is a policy decision (NES not on SSL roadmap) — not supported by current billing data which shows 100% NES on SSL surfaces. The 4yr term (PFID 1840833) is unusual; cannot be validated from billing since SKUs not yet in production. Market gate cannot fire without analyst input on Reseller support.
Assessment      : PARTIAL MATCH — no existing CES package confirmed (matches expected); NES reference found via full scan despite slug format mismatch; data contradicts CES-only surface claim; term validation blocked by missing production billing history
Input quality   : Market not specified (Reseller implied); 4yr term unusual; NES reference slug in ticket uses non-standard format with "offer-" prefix and camelCase; PFIDs not in production — data validation limited

## Run 2026-05-13-ASSESS-CMS31421 — CES use case assessment: CMS-31421 Email Essentials dpp_precheck

Date            : 2026-05-13-ASSESS
Entry type      : Product name + surface description
Entry value     : "CMS-31421 — Email Essentials, domain purchase flow (FOS), two price-point variants, DISC214228 + DISC214229"
Path            : A — Curated Offer
Offer operation : Create
Mode            : N/A
NES/CES branch  : CES — 100% null package_id at dpp_precheck for all email products
Gate asked      : Surface/ITC clarification (FOS vs DPP ambiguity); Billing term; Customer segment; Market
CES chain steps : Step 1: fail (monthly PFIDs 867686/1556326 no merchandising match — expected for catalog-era product) | Step 2: ~20+ keyword matches in 1,200 IDs; 4 shown, 16+ suppressed without disclosure — SILENT FILTERING, all-M-shown rule violated | Step 3: not run
Champion        : Correct — temp-email-essentials-99 (DISC214228) + temp-email-essentials-149 (DISC214229), Offer ID 575a7d2a, plan emailEssentialsEe, PFIDs 867688/867694/867696 (annual)
Flags fired     : CES delivery gap; Product ambiguity (two Email Essentials products at dpp_precheck); temp- prefix over-flagged as possible test artifact (now fixed in SKILL.md); SLP email volume annual-only; term gate answered "monthly" by analyst but correct PFIDs are annual
Ticket preview  : Requested
Notes           : Four issues: (1) SILENT CANDIDATE FILTERING — ~20+ matches, 4 shown, 16+ suppressed; Classified: Skill Issue; Fixed: all-M-shown rule in SKILL.md. (2) TEMP- PREFIX OVER-FLAGGED — production champions flagged as possible test artifacts; Classified: Skill Issue; Fixed: feedback_temp_prefix_curated_offers.md. (3) TERM SCOPE MISREAD — gate fired correctly; analyst answered "monthly" but annual was correct; required manual correction; Classified: User Input Issue (primary) + Skill gap (no post-B0 term × PFID confirmation grid); Open. (4) RUN LOGGER NOT EXECUTED — entry written manually by pulse-audit; Classified: Skill Issue; Fixed: on-demand only. Additive value beyond ticket scope: Offer ID 575a7d2a and plan emailEssentialsEe both surfaced.
Assessment      : PARTIAL MATCH — champions and key IDs found correctly; three of four issues now fixed in SKILL.md; open gap is term-gate answer validation (structural — requires B0 grid confirmation step)
Input quality   : Term not specified (gate fired; analyst answer was imprecise — "monthly" but annual was correct); Market not specified (gate may not have fired — potential skill gap for Chain Step 3); BPO/Renewal/CartRemoval not specified (not material for this use case)

## Pulse Audit — 2026-05-13T-ASSESS (CES Document Deep Dive)

Date            : 2026-05-13T-ASSESS
Audit type      : pulse-audit (CES document assessment)
Runs analyzed   : 4 assessment runs from CES_Package_Requests_2025.docx
EP file status  : ep_curated_offer_requests_2025.docx blocked — GD-Internal DRM encryption; content not accessible from WSL CLI
Assessment match rate : PARTIAL MATCH on all 4 — champions found or correctly determined to be net-new, but complete payloads blocked by input quality gaps in 3 of 4

## Run 2026-05-14T00:00 — Jira: CMS-32651 — Email Backup SAPI package with disc004590

Date            : 2026-05-14T00:00
Entry type      : Jira
Entry value     : CMS-32651 — "Create new SAPI package for Email Back up and include a discount code" (clone o365backup, apply disc004590)
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (PFIDs 996667, 996668, 1499849; all billing rows package_id NULL; 0 NES orders in 7d window)
Gate asked      : none (Term inferred as 1 Month from billing data; Market and Segment not asked due to evaluation run — flagged as BLOCKING in output)
CES chain steps : Step 1: o365backup NOT FOUND in catalog | Step 2: 6 keyword matches in 1,200 IDs (email-business-essentials-backup, email-essentials-aes-backup, email-plus-backup, office365-tier0-backup, office365-tier1-backup, office365-tier3-backup) — all 6 shown | Step 3: not run
Champion        : Not found — o365backup slug does not exist; two candidate families found (office365-tier*-backup offerId 092a9528, no existing discount; email-*-backup offerId 575a7d2a, existing disc209800). AMBIGUOUS — ecomm must confirm clone source.
Flags fired     : Clone source not found, Ambiguous plan, Geo scope missing, Existing discount code conflict (disc209800 on Candidate B), Surface 100% CES, Wide blast radius (25+ ITCs)
Ticket preview  : Not requested
Notes           : Ticket references o365backup as template — slug does not exist in catalog or merchandising API. PFID 996667 appears as an addon inside standard M365 packages in merchandising API but has no standalone backup CES package. Three distinct billing PFIDs present (new, renewal M365 branded, renewal non-M365). All are 1 Month. Market not specified in ticket — hard BLOCKING for offer creation. Discount code disc004590 is new (not in billing). Existing backup curated offers (email-*-backup family) already carry disc209800 — conflict must be resolved. Wide blast radius across 25+ ITCs in multiple countries noted.

## Run 2026-05-13T14:30 — Product-first: Titan email — 14-day standalone free trial, UPP surface

Date            : 2026-05-13T14:30
Entry type      : Product name
Entry value     : "Titan email — 14-day standalone free trial, auto-renew OFF, new customers, UPP surface, 17 i18n markets (IN/MY/PH/PK/ZA/AR/CL/CO/MX/PE/BR/TR/ID/TH/UA/VN/PL)"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100%
Gate asked      : Market
CES chain steps : Step 1: success (vnext-i18nox-tier4, oybo-ox-email, business-hosting-set-1-expand-ox confirmed as curated offers) | Step 2: success (titanemail-light-freetrial-14days found via keyword scan of 1200 IDs) | Step 3: N/A (chain resolved at Step 2)
Champion        : Found — titanemail-light-freetrial-14days (source: ID scan); offer already active in catalog rev 3, last modified 2025-12-18 by EP-82036; action is wire-to-surface not clone
Flags fired     : Offer already exists in catalog, CES surface, No billing PFID for free trial SKU, Active CES discount on surface (disc444888)
Ticket preview  : Requested
Notes           : Product billing label is "Professional Email Pro Light / Pro Plus" — not "Titan"; product name search returned zero rows globally; UPP surface ITCs follow upp_titanproduct_* pattern. Champion offer titanemail-light-freetrial-14days already existed with exact config (14-day FREE_TRIAL, plan=light, autoRenew=false). Base Collection ID 927a9d45-7c5b-4652-ad68-d5cd9be75028 confirmed correct by analyst. No PFID assigned yet for 14-day free trial SKU — flagged as BLOCKING. WebFetch correctly found partial merchandising matches for PFID 1798083 only; absence of titanemail-light-freetrial-14days from merchandising table explained by missing PFID (new offer), not WebFetch truncation.

## Run 2026-05-13T18:00 — Product-first: MWP Basic, SLP, ROW + India, 80% discount

Date            : 2026-05-13T18:00
Entry type      : Product name + surface category
Entry value     : "MWP Basic, 1 Year, SLP surface, 80% discount, ROW + India, new and existing customers"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : Mixed — NES 100% on slp_wordpress (two simultaneous geo-split bundles); CES 100% on slp_hosting_category, slp_hosting_4gh, slp_rstdstore
Gate asked      : Term
CES chain steps : N/A — NES path (both champions found via billing data)
Champion        : AMBIGUOUS — geo-split: wordpress-openexchange-forever-ssl-basic (Titan Email, developing markets, Base Collection ID 4ce8a17c-b508-34ab-99d1-e5e5165214d3) + wordpress-o365-forever-ssl-basic (M365, developed markets, Base Collection ID 876fc126-7ce9-3b47-975a-0f0513bf38a8)
Flags fired     : Ambiguous champion (geo-split), M365 geo risk (quantityByOfferKey=2 seats), Plan not specified (both bundles), Mixed-term bundle (o365 has 3-year WP hosting + 1-year M365), CES surface gap (3 SLP surfaces), Pricing overridePolicies required
Ticket preview  : Not yet requested
Notes           : MISSED BUNDLE — wordpress-o365-forever-ssl-basic was not surfaced by initial pre-flight. Root cause: term filter (product_term_num = 1, product_term_unit_desc = 'year') was applied in the B0 PFID discovery step, which excluded PFID 1320704 (3-year WP hosting) from the PFID list. Because 1320704 never entered the pre-flight query, pf_id_package_details_v1 was never searched for it, and the o365 bundle was missed entirely. Fix: B0 should discover all PFIDs for the product across all terms; term filter belongs in the Step A1 experiment query only, not in B0. Analyst confirmed this diagnosis. Also: initial B0 returned zero rows due to case sensitivity ('Year' vs 'year'). Two UUID placeholder codes in billing correspond to Base Collection IDs of the two bundles — they encode which geo-split offer was used. M365 absence in India/developing markets confirmed by billing (zero IN rows for o365 bundle).

## Run 2026-05-13T17:00 — Product-first: Email Essentials on dpp_precheck

Date            : 2026-05-13T17:00
Entry type      : Product name + surface description (no Jira ticket)
Entry value     : "Email Essentials, domain purchase flow (FOS), two price-point variants, CES package requested"
Path            : A — CES Package Request
Offer operation : Create / Clone
Mode            : N/A
NES/CES branch  : CES — 100% null package_id for all email at dpp_precheck
Gate asked      : Surface/ITC clarification (FOS vs DPP ambiguity); Billing term; Customer segment; Market
CES chain steps : Step 1: no merchandising package for monthly PFIDs 867686/1556326 | Step 2: 1,200 IDs scanned — ~20+ keyword matches found; only 4 surfaced in Candidate table (remainder silently dropped — see Notes) | Step 3: not run
Champion        : temp-email-essentials-99 (DISC214228) + temp-email-essentials-149 (DISC214229) — both Standalone, Base Offer ID 575a7d2a, plan emailEssentialsEe, PFIDs 867688/867694/867696
Flags fired     : CES delivery gap; Product ambiguity (two Email Essentials products at dpp_precheck); temp- prefix overlap with m365emailessentialseedpp variants; SLP email volume annual-only
Ticket preview  : Requested
Notes           : SILENT CANDIDATE FILTERING — Chain Step 2 found ~20+ keyword matches for emailessentials/dpp/m365emailessentials across 1,200 IDs but only 4 were surfaced in Candidate table. Remaining ~16+ (including m365emailessentialseedpp-nortonsmb-standardfreetrial, emailessentialsee_aes-nortonsmb-standardfreetrial, email-essentials-aes-7daytrial, o365-solutionset-tier3, email-essentials-byob, pb-contract variants, etc.) were dropped without disclosure. Analyst caught this: "there can be many-to-1 relationships — you need to disclose that you filtered X many out." Violates the all-M-shown rule. Also: correct champions (temp-email-essentials-99/149) were found but flagged with cautionary notes about "temp-" naming prefix — analyst confirmed these are production champions, not test artifacts. Term scope misread: gate clarified "monthly" but correct champion PFIDs are annual (867688/867694/867696); analyst had to manually provide the correct champion row. Run Logger not executed by offer-pulse — entry written manually via pulse-audit.

## Run 2026-05-13T22:00 — ITC-first: dpp_precheck, M365 Online Essentials (w/o Teams), $3.99/mo annual, new customers

Date            : 2026-05-13T22:00
Entry type      : ITC-first / Product name
Entry value     : "dpp_precheck, Microsoft 365 Online Essentials (w/o Teams) at $3.99/mo annual display price, new customers only, all markets"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (billing query returned 0 rows for email/M365 on dpp_precheck, 1 Year, 7d window; lean mapping 0 rows)
Gate asked      : Term
CES chain steps : Step 1: fail (no standalone M365 Online Essentials in merchandising API — expected for catalog-era product; 5 domain+email bundle packages found, not target) | Step 2: success (17 keyword matches in 1,200 IDs; microsoftemail-onlineessentialsnoteams-discount-365af1f1cb identified as champion) | Step 3: not run
Champion        : Found — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb (source: ID scan); offerId 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan onlineEssentialsNoTeams, active, modified 2026-04-22
Flags fired     : PFID unknown (0 billing rows), M365 geo risk, Existing tiers share Offer ID with champion
Ticket preview  : Not yet requested
Notes           : Re-run of prior session run at 19:00 which found PFID 1768604 (125 billing rows, all null package_id). Current run returned 0 rows — product name filter (LIKE '%microsoft%', '%365%', '%email%', '%essentials%') may not match billing label for PFID 1768604; recommend ITC-only SQL to confirm. All 17 keyword matches shown (vs 9 in prior run — broader seed set). Two confirmed live tiers at dpp_precheck: temp-email-essentials-99 (plan emailEssentialsEe, discount DISC214228) and temp-email-essentials-149 (plan emailEssentialsEe, discount DISC214229) — both share Offer ID 575a7d2a with new champion; only plan and discount differ.

## Run 2026-05-14T09:00 — Product name: MWP Basic, 1-year, SLP (all slp_*), ROW + India, 80% discount

Date            : 2026-05-14T09:00
Entry type      : Product name + surface category
Entry value     : "MWP Basic, 1-year term, SLP surface (all slp_* ITCs), 80% discount, ROW and India, new and existing customers"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : Mixed — NES 100% on slp_wordpress (1 bundle); CES 100% on slp_hosting_category, slp_hosting_4gh, slp_rstdstore
Gate asked      : none (all 6 dimensions resolved from entry)
CES chain steps : N/A — NES path executed (champion found via billing data on slp_wordpress)
Champion        : Found — wordpress-openexchange-forever-ssl-basic (source: billing data); Offer Collection ID 4ce8a17c-b508-34ab-99d1-e5e5165214d3; Component: Titan Email Offer 927a9d45-7c5b-4652-ad68-d5cd9be75028 (FREEACCOUNT=true, plan NOT SPECIFIED)
Flags fired     : CES surface gap (3 SLP surfaces: slp_hosting_category 123 orders/7d, slp_hosting_4gh 65, slp_rstdstore 5); Plan not specified (Titan Email component)
Ticket preview  : Not yet requested
Notes           : Single NES bundle on slp_wordpress only. Three other slp_* surfaces are 100% CES — no curated offer on those surfaces. Offer Collection confirmed: Titan Email component has FREEACCOUNT=true in prePurchaseKeyMap customData; no plan specified in prePurchaseKeyMap entry. Additional catalog offers in collection (not in prePurchaseKeyMap): WordPressOffer (566f8074, parentOffer, tags: wpaas) and Norton (72a57662, tags: norton). Both discount codes in billing are UUID placeholders. catalog_list_price and catalog_sale_price are NULL in billing — pricing from avg_receipt_price only.

## Run 2026-05-14T — Jira: CMS-32825 — Deluxe Automated SSL, Create CES Packages for FOS SSL SLP

Date            : 2026-05-14T
Entry type      : Jira
Entry value     : CMS-32825 — "Deluxe Automated SSL - Create CES Packages for FOS selling"
Path            : A — Curated Offer
Offer operation : Create
Mode            : N/A
NES/CES branch  : Mixed — slp_ssl is 100% NES for existing products; new dlxssl-* PFIDs are pre-launch CES per ticket architectural constraint (SSL-config only accepts CES)
Gate asked      : none — all 6 dimensions resolved from ticket body (operation=Create, path=A, segment=both, market=all/Reseller, surface=slp_ssl FOS, terms=7 variants explicit in ticket)
CES chain steps : N/A (all 29 curated offer slugs found already ACTIVE in catalog — ticket may be substantially complete; CES wiring into SSL-config is the remaining action)
Champion        : Found — all 29 dlxssl-* curated offers already exist in catalog under offerId 35fc5321-7723-4c40-906b-7b5c417e61cb (source: ID scan; 1 confirmed via billing data)
Flags fired     : All 29 packages already exist in catalog; Single offerId for all 29 packages; Pre-launch volume only; CES config constraint; EV Wildcard missing
Ticket preview  : Not requested
Notes           : All 29 requested dlxssl-* curated offer slugs were found ACTIVE in the catalog under a single shared offerId (35fc5321-7723-4c40-906b-7b5c417e61cb, "SSL Certificate Subscriptions Offer", plan-differentiated Standalone). Ticket is a net-new SSL product line (DV/EV/OV, 9–10 SKUs per tier, 7 term lengths each = 203 PFID × Term combinations). Key structural finding: one base offer definition with plan enum covers all 29 package slugs — not 29 separate offer IDs. EV Wildcard is absent from the ticket's 29 packages but is present in the offer definition schema — may be intentional omission by Security team. Early billing data (38 orders/90d on slp_ssl for DV Single Domain group) is test/config activity. slp_ssl current live traffic is Standard SSL NES packages only.

## Run 2026-05-13T19:00 — ITC-first: dpp_precheck, M365 Online Essentials (no Teams), replacing two legacy email tiers

Date            : 2026-05-13T19:00
Entry type      : Surface description + product name
Entry value     : "dpp_precheck, Microsoft 365 Online Essentials (w/o Teams) at $3.99/mo annual, new customers only, all markets, replacing two legacy email upsell tiers"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (125 billing rows, all package_id NULL)
Gate asked      : Term
CES chain steps : Step 1: o365-solutionset-tier3 confirmed (offerId e328092f) — does not match target product; Step 2: 9 keyword matches in 1,200 IDs; microsoftemail-onlineessentialsnoteams-discount-365af1f1cb found via noteams keyword, confirmed by discount code cross-ref to billing PFID 1768604; Step 3: not run
Champion        : Found — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb (source: ID scan), Base Offer ID 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan onlineEssentialsNoTeams, active, modified 2026-04-22
Flags fired     : Price confirmation needed ($3.99/mo vs avg catalog sale $95.88), Fourth email PFID unresolved (1556350 Email Plus, 494 orders), Legacy discount code gap (office365-emailessentialsee_aes has no catalog discountCode but billing shows disc444888), Champion recently modified (2026-04-22)
Ticket preview  : Requested
Notes           : Key structural finding — all six email curated offers on dpp_precheck share the same base offer ID 575a7d2a (M365 offer). The champion and both legacy tiers are all plans on the same underlying product. Engineer is creating a new curated offer slug at an existing base offer plan, not building from scratch. WebFetch returned no merchandising match for PFIDs 1556330/1768604/1556350 — consistent with newer M365 offers absent from legacy /v1/packages endpoint (confirmed: microsoftemail-onlineessentialsnoteams-discount-365af1f1cb exists only in curated offer catalog). All 9 candidates disclosed in Section 4, none suppressed. Ticket preview was produced but initially omitted Base Offer ID, Plan, and catalog discount code — analyst caught the omission; this was the trigger for the pulse-audit that identified the CES ticket preview template gap (fixed same session via Wendy).

## Run 2026-05-14T00:00 — Direct input: dpp_precheck, M365 Online Essentials (w/o Teams), $3.99/mo annual, new customers, all markets, Path A Create/Clone

Date            : 2026-05-14T00:00
Entry type      : ITC-first / Product name
Entry value     : "Path A — Curated Offer, Create/Clone. Microsoft 365 Online Essentials (without Teams) at $3.99/month annual display price, replacing two legacy email upsell tiers. Surface: dpp_precheck. New customers only. All markets. Annual term (1 year)."
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (141,650 orders over 90d, all null package_id; 0 NES rows in 7d window)
Gate asked      : none (all six dimensions resolved from intake)
CES chain steps : Step 1: fail (no merchandising package match for PFID 1768604 — expected for catalog-era M365; WebFetch confirmed no match on targeted retry) | Step 2: success (11 keyword matches in 1,200 IDs; microsoftemail-onlineessentialsnoteams-discount-365af1f1cb identified as champion via exact name + plan + discount code match) | Step 3: not run
Champion        : Found — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb (source: ID scan — confirm with ecomm); offerId 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan onlineEssentialsNoTeams, active, modified 2026-04-22, revisionNumber 1
Flags fired     : CES surface 100%, Discounted variant (base slug not found), M365 geo risk (all markets scope), Legacy tiers active (temp-email-essentials-99/149 being replaced), Offer revisionNumber=1 (recently created, not yet confirmed in billing)
Ticket preview  : Not requested
Notes           : All 11 Chain Step 2 candidates disclosed, none suppressed. PFID 1768604 (Online Essentials - 1 year) confirmed in billing: 192 orders/7d (US: 188, CA: 3, SA: 1), all CES, discount code 365af1f1cb — cross-references to catalog discountCode 365AF1F1CB on champion slug. Two legacy tiers identified: temp-email-essentials-99 (DISC214228, ~2,500 orders/7d) and temp-email-essentials-149 (DISC214229) — both share offerId 575a7d2a with champion, plan emailEssentialsEe. Base slug microsoftemail-onlineessentialsnoteams NOT_FOUND in catalog — BLOCKING note added. Surface confirmed 100% CES via 90-day window (not just 7d). Merchandising API WebFetch returned no matches for PFID 1768604 on both initial and targeted retry — consistent with catalog-era M365 products not in legacy merchandising system.

## Run 2026-05-14T00:00 — Product name: WAM Premium + Commerce annual, TrustedSite bundle experiment, slp_wsb_* FOS, CES Package Request

Date            : 2026-05-14T00:00
Entry type      : Product name + experiment description
Entry value     : "WAM Premium and Commerce annual SKUs. TrustedSite bundle experiment on FOS surfaces (slp_wsb_* ITCs). New customers only. Global market. Annual term (1 year). Request: CES package payloads for two treatment variants (+$2–$3/month price points) plus a discount-code control package."
Path            : A — Curated Offer
Offer operation : Create — CES Package Request
Mode            : N/A
NES/CES branch  : CES — 100% (all billing rows for WAM Premium 970463 and Commerce 970473 on slp_wsb_* ITCs in 7-day window carry null package_id)
Gate asked      : none (all six dimensions resolved from entry)
CES chain steps : Step 1: wsb-vnext-tier3-disc NOT FOUND in curated offers; de-discounted wsb-vnext-tier3 FOUND (offerId 6db92066); wsb-vnext-tier4 FOUND (offerId 60d0894f); vnext-i18nox-tier4 FOUND (bc817604, Titan Email international variant) | Step 2: 15 keyword matches in 1,200 IDs scanned; all 15 shown | Step 3: not run
Champion        : AMBIGUOUS — wsb-vnext-tier3 (Premium; source: merch match de-discounted + ID scan) and wsb-vnext-tier4 (Commerce; source: ID scan); both confirmed active Rev 1
Flags fired     : CES surface 100%, Discounted variant (wsb-vnext-tier3-disc → base wsb-vnext-tier3), M365 geo risk (global scope both tiers), TrustedSite is available-addon not wired component, Discount code conflict (disc15278 vs DISC696637), i18nox/Titan Email market gap, wam*_soft monthly-only out of scope, Low volume
Ticket preview  : Not requested
Notes           : TrustedSite listed as availableAddon in WAM product schema (onetime=false) — not currently wired as prePurchaseKeyMap component. Treatment packages require ecomm to ADD TrustedSite to prePurchaseKeyMap; PFID not discoverable in billing. Six packages total: 2 tiers x 3 arms. wam*_soft slugs monthly-only per catalog schema. wsb-vnext-tier3-disc slug absent from curated offers catalog. All 15 ID scan candidates disclosed.

## Run 2026-05-14T-EVAL-02 — ITC-first: dpp_precheck, M365 Online Essentials (without Teams), $3.99/mo annual, new customers, all markets (blind eval)

Date            : 2026-05-14T-EVAL-02
Entry type      : ITC-first / Product name
Entry value     : "dpp_precheck, Microsoft 365 Online Essentials (without Teams) at $3.99/month annual display price, new customers only, all markets, annual term (1 year)"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (PFID 1768604; 192 orders/7d on dpp_precheck; all package_id NULL)
Gate asked      : none (all 6 dimensions resolved from entry)
CES chain steps : Step 1: fail (merchandising partial match only — office365-tier1-teams-duplicate covers legacy PFIDs 31819/31825, not live PFID 1768604; catalog-era M365 absent from /v1/packages) | Step 2: success (26 keyword matches in 1,200 IDs; microsoftemail-onlineessentialsnoteams-discount-365af1f1cb confirmed as champion by plan name + discount code cross-ref) | Step 3: not run
Champion        : Found — microsoftemail-onlineessentialsnoteams-discount-365af1f1cb (source: ID scan); offerId 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan onlineEssentialsNoTeams, active Rev 1, modified 2026-04-22
Flags fired     : Discounted variant (base slug does not exist), CES surface gap, M365 geo risk, Discount code carries over (365af1f1cb), New customer segment note
Ticket preview  : Not yet requested
Notes           : Standalone offer confirmed (prePurchaseKeyMap absent, offers[] empty, offerCollectionId=None). All 26 keyword matches disclosed in Candidate table — none suppressed. PFID 1768604 sole live 1-year SKU on surface. BLOCKING: base slug microsoftemail-onlineessentialsnoteams does NOT exist — discounted variant is only live config (Rev 1, 2026-04-22). Target price $3.99/mo ($47.88/yr) consistent with CA/SA market billing avg receipt. Tags: partneremail, m365. Merchandising WebFetch run twice; no match for PFID 1768604 on either attempt — expected for catalog-era M365.

## Run 2026-05-14T-BLIND-CMS31766 — Jira: CMS-31766 MSSL + Malware Monitoring CES Package

Date            : 2026-05-14T-BLIND
Entry type      : Jira
Entry value     : CMS-31766 — MSSL+Malware Monitoring - Create CES Package for SSL Config
Path            : A — Curated Offer
Offer operation : Create
Mode            : N/A
NES/CES branch  : CES (ticket-declared — SSL Config accepts CES only); billing shows 0 rows for new PFIDs (net-new, pre-launch); SSL SLP surface is 95% NES in billing; new PFIDs never transacted
Gate asked      : none — all 6 dimensions resolved from ticket body (Path=A/CES, Operation=Create, PFIDs=1840827/29/31/33/35, Terms=1–5yr, Surface=SSL SLP/Config, Market=not stated→assumed all)
CES chain steps : Step 1: sslcert-managed-with-monitoring NOT a CES package — found as NES curated offer (fail as CES source) | Step 2: 1,200 IDs scanned; 1 keyword match (sslcert-managed-with-monitoring); confirmed NES reference offer offerId 28e5b730, plan managedWithMonitoring, active | Step 3: not run
Champion        : Not found — NET-NEW CES package required (merchandising API truncated but no match in visible content; no CES package slug for new PFIDs exists)
Flags fired     : CES surface gap (surface is actually 95% NES — CES requirement is policy not data), Merchandising API ambiguous (WebFetch truncated), New PFIDs zero billing data, NES reference offer Rev 1 (created 2026-04-23), 4yr term unusual, Multiple terms unfiltered
Ticket preview  : Not requested
Notes           : Slug format mismatch — ticket body uses "offer-sslcert-managedWithMonitoring" (offer- prefix + camelCase); direct lookup fails; catalog uses "sslcert-managed-with-monitoring" (kebab-case, no prefix). sslcert-managed-with-monitoring and ssl-001sites-managed-tier1 share the same offerId (28e5b730-4e70-46b0-8672-6e18a17f81a1) — both are standalone NES offers for the SSL Certificate product, using different plan strings (managedWithMonitoring vs managed). WebFetch truncated on all three attempts — confirmed no match in visible content but truncated portion unverified. Market not specified in ticket; assumed all markets. Recommended CES slug convention: ssl-001sites-managed-with-monitoring-tier1 (matching existing pattern).

## Run 2026-05-14T00:30 — Jira: CMS-31421 — Email Essentials CES packages for dpp_precheck (blind eval run 07)

Date            : 2026-05-14T00:30
Entry type      : Jira
Entry value     : CMS-31421 — "Create temporary CES packages to support discounted email packages that can be attached to a domain" (temp-email-essentials-99 / temp-email-essentials-149, PFIDs 867688/867694/867696, DISC214228/DISC214229)
Path            : A — Curated Offer
Offer operation : Create (requested) — both packages already active in catalog since 2025-10-23 (ticket Closed)
Mode            : N/A
NES/CES branch  : CES — 100% (all dpp_precheck and dpp_config1 rows for these PFIDs have package_id = NULL; NES traffic for same PFIDs flows via dlp_usoybo/dlp_email_professional on separate package_ids)
Gate asked      : none — ticket contained full JSON package definitions with PFIDs, discount codes, and slug names; all six dimensions resolved from ticket body
CES chain steps : Step 1: temp-email-essentials-99 confirmed as curated offer (575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, emailEssentialsEe, DISC214228, active, Rev 1) | Step 1: temp-email-essentials-149 confirmed (same offerId, emailEssentialsEe, DISC214229, active, Rev 1) | Steps 2–3: not required
Champion        : Found — temp-email-essentials-99 (DISC214228) + temp-email-essentials-149 (DISC214229), both Standalone, shared Offer ID 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan emailEssentialsEe, PFIDs 867688/867694/867696 (source: catalog direct lookup)
Flags fired     : Ticket already fulfilled (both packages created Oct 2025, CMS-31421 Closed); same offerId on both packages; temp- prefix confirmed production; dpp_precheck 100% CES; NES on separate surfaces; multi-surface blast radius DISC214228/DISC214229
Ticket preview  : Not requested
Notes           : Clean run — both slugs resolved at Chain Step 1 with no fallback. Billing: DISC214228 active on dpp_precheck (2,457 orders/7d for 867688 1yr US); DISC214229 active on dpp_config1 (multi-market). All three term variants in billing (1yr/2yr/3yr). Catalog: M365 standalone, tags=[partneremail, m365], status=ACTIVE, offers[] empty, prePurchaseKeyMap absent. No unexpected geometry. CMS-31421 Closed status consistent with Oct 2025 creation date.

## Run 2026-05-14T — Product-first: WAM Premium + Commerce annual, TrustedSite bundle experiment, slp_wsb_* FOS, 4-arm CES package request

Date            : 2026-05-14T
Entry type      : Product name + experiment description
Entry value     : "WAM Premium and Commerce annual SKUs, TrustedSite bundle experiment, FOS surfaces (all slp_* SLP), new customers only, annual term. Create CES package payloads: Treatment arm (+$2–$3/mo price increase with TrustedSite bundled) + Control arm (clone with new discount code preserving current pricing)."
Path            : A — Curated Offer
Offer operation : Create — CES Package Request
Mode            : N/A
NES/CES branch  : CES — 100% (all slp_wsb_ft_* billing rows for PFID 970463 WAM Premium and 970473 WAM Commerce carry null package_id; catalog_list_price and catalog_sale_price both NULL — CES surface confirmed)
Gate asked      : Offer Operation (create vs modify), Customer segment (new only), Surface (all slp_*)
CES chain steps : Premium — Step 1: wsb-vnext-tier3-disc not found as standalone curated offer; base wsb-vnext-tier3 FOUND (offerId 6db92066) | Step 2: 15 keyword matches; wsb-vnext-tier3 confirmed as champion; wsb-vnext-tier4 and vnext-i18nox-* also found | Step 3: not run. Commerce — Step 1: vnext-i18nox-tier4 FOUND (offerId bc817604) via merchandising match for PFID 970473 | Step 2: not needed | Step 3: not run. TrustedSite — Step 1: fail | Step 2: fail (0 matches for "trusted/trust/seal/security-seal" in 1,200 IDs) | Step 3: tag search not run
Champion        : Found — wsb-vnext-tier3 for Premium (source: ID scan, discounted variant de-discounted); vnext-i18nox-tier4 for Commerce (source: merchandising match High confidence). TrustedSite: Not found — NET-NEW BUILD required (no standalone offer in catalog or merchandising API)
Flags fired     : CES surface 100%; TrustedSite BLOCKING x3 (no annual SKU, no curated offer, cross-PNL-line bundle needs approval); Discounted variant (wsb-vnext-tier3-disc → base wsb-vnext-tier3); WAM platform component UUID partial (d9e7bde4-????); i18nox vs wsb-vnext disambiguation surfaced for Commerce (vnext-i18nox is international/Titan; confirm if US Commerce should use wsb-vnext series); disc15278 is production code — new experiment codes required for all 4 arms
Ticket preview  : Requested — 4 previews rendered (Control-Premium, Control-Commerce: ready to file after UUID + i18nox confirmation; Treatment-Premium, Treatment-Commerce: BLOCKED until all 3 TrustedSite items resolved)
Notes           : Supplemental subagent (Agent 5) was required because initial Q2 pre-flight scope filter (package_id IN i18n package IDs) incorrectly excluded main US WAM PFIDs with null package_id — CES rows for 970463/970473 are not scoped by package_id. get_offer_collection_definition tool returned results wrapped in a list [{}] instead of dict (API response format bug); data was successfully extracted from the error body. TrustedSite PFIDs 1834961/1834962 have monthly-only billing; PNL line is 'Strategic Partnerships AC' (not WAM). M365 component UUID confirmed from memory (575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan emailEssentialsEe). OX/Titan component confirmed (927a9d45-7c5b-4652-ad68-d5cd9be75028, plan personalTitan). WAM platform component UUID partial across both packages — ecomm must confirm before filing either ticket.

## Run 2026-05-14T18:30 — Product name: MWP Deluxe, first-year 20% discount, SLP surface

Date            : 2026-05-14T18:30
Entry type      : Product name + surface category
Entry value     : "MWP Deluxe, 20% first-year discount, SLP surface (all slp_*)"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : NES — 100% on slp_wordpress (two simultaneous bundles: o365 and OX series); 1-year PFID 1320700 absent from all NES packages on SLP
Gate asked      : none (Term inferred 1 Year from "first year"; Market defaulted US/USD; Segment inferred new customers; B0 hard-stop skipped per "fan out" instruction)
CES chain steps : N/A — NES path (both champions found via billing data on slp_wordpress)
Champion        : AMBIGUOUS — two series simultaneously active on slp_wordpress: wordpress-o365-forever-ssl-deluxe (Offer Collection ID 658d1af2, US/M365 series) + wordpress-openexchange-forever-ssl-deluxe (Offer Collection ID ce0a7869, International/Titan series); source: billing data
Flags fired     : Ambiguous champion (two series), Term mismatch (1-year inferred but NES bundles are 3-year/PFID 1320706; 1-year PFID 1320700 absent from NES packages), A/B test likely (4 distinct UUID discount codes on o365 bundle), M365 geo risk, Component plan not specified, Pricing data gap
Ticket preview  : Not yet requested
Notes           : TERM MISMATCH — "first year" was inferred as 1-year billing term but A1 data showed only 3-year PFID 1320706 in these NES bundles. PFID 1320700 (1-year) absent from pf_id_package_details_v1 for slp_% deluxe packages. "First year discount" most likely means a first-year price override via overridePolicies on the 3-year bundle, not a 1-year billing term offer — flagged prominently for analyst to confirm. Both packages are Offer Collections with one free email component (M365 for o365; Titan Email for OX). Collection plan encodes both MWP tier and email tier; no per-component plan in prePurchaseKeyMap. Also in collection (not wired): Airo (o365 bundle) and Norton (OX bundle). Parallel fan-out used across 5 phases with 9+ simultaneous tool calls. get_offer_collection_definition and get_offer_definition_by_id tools returned data in list-wrapped error bodies — data successfully extracted from error payload.

## Run 2026-05-14T00:00 — Product-first: Titan email 14-day standalone free trial, UPP surface (eval run 08)

Date            : 2026-05-14T00:00
Entry type      : Product name
Entry value     : "Titan email 14-day standalone free trial, auto-renew OFF, new customers only, 17 i18n markets (IN/MY/PH/PK/ZA/AR/CL/CO/MX/PE/BR/TR/ID/TH/UA/VN/PL), UPP surface (upp_titanproduct_* ITCs)"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : CES — 100% (6 ITCs, 875 orders/7d, all null package_id; 0 rows for free trial PFID — SKU not yet in production)
Gate asked      : none
CES chain steps : Step 1: fail (no merchandising match — expected for Titan catalog-era product) | Step 2: success (6 keyword matches in 1,200 IDs; titanemail-light-freetrial-14days identified as champion) | Step 3: not run
Champion        : Found — titanemail-light-freetrial-14days (source: ID scan); offerId 927a9d45-7c5b-4652-ad68-d5cd9be75028, plan=light, FREE_TRIAL BPO (14-day), autoRenew=false, active, modified 2025-12-18 by EP-82036, revision 3
Flags fired     : CES surface, SKU not yet in production (0 billing rows for free trial), Champion via ID scan only (no billing confirmation), i18n market scope (17 markets)
Ticket preview  : Not yet requested
Notes           : SKU not yet in production — zero billing rows confirmed for any Titan email 14-day free trial across all surfaces. All 6 keyword matches disclosed in Section 4. Curated offer already exists in catalog at revision 3 (last modified 2025-12-18); this is a wire-to-surface operation for the 17 i18n markets, not a net-new build. No PFID assigned yet for free trial SKU — BLOCKING flag added. Offer geometry confirmed Standalone (prePurchaseKeyMap absent, offers[] empty in get_offer_collection_definition response). All other Titan trial variants (starter-freetrial-1year, starter-freetrial-1month) share the same offerId (927a9d45) but different plan/term configs — not suppressed, all shown in candidate table. titan-pro-plus-dpp included in candidate count but labeled as DPP-scoped slug.

## Run 2026-05-15-UC-01 — NES Bundle: CA .CA domain + Email Essentials (dpp-ca-ca-solution-tier1)

Date            : 2026-05-15T-UC-01
Entry type      : ITC-first
Entry value     : "CA .CA domain with Email Essentials included, dpp-ca-ca surface tier1, annual term, new customers, CA market, Path A curated offer"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : NES — 100% (dpp-ca-ca-* surfaces are NES-only; domainEmail collection e328092f confirmed active)
Gate asked      : none (all 6 dimensions resolved from entry)
CES chain steps : N/A — NES path
Champion        : Found — curated offer dpp-ca-ca-solution-tier1, Offer Collection ID e328092f-972c-4353-a884-78fd086a6866 (domainEmail), plan defaultEmailessentialseeDpp, discount disc000013, revision 3, modified 2026-04-20
Flags fired     : M365 autoRenew=false set explicitly at rule level for the Dpp-suffix plan variant (defaultEmailessentialseeDpp) — the non-Dpp plan (defaultEmailessentialsee) omits autoRenew entirely so it defaults to true; disc000013 applies at curated offer level (tier3 uses disc000015 instead); tier3 uses a different collection (e4836329, plan defaultCommerceEmailessentialsee, 3 components) — do not clone tier1 for tier3 work
Ticket preview  : Not requested
Notes           : 2-component domainEmail collection: NewDomain (edf13c43, plan default) + M365 (575a7d2a, plan emailEssentialsEe, term 1 YEAR, autoRenew=false). The autoRenew=false is a rule-level override applied only when the curated offer selects the Dpp-suffix plan — it is not a property of the M365 offer itself, meaning the same collection under a different plan resolves M365 with autoRenew defaulting to true. Tier3 (e4836329, domainWbsIntEmail) is a 3-component collection and uses a separate discount code — catalog-verified confidence 98%.

## Run 2026-05-15-UC-02 — NES Standalone: Deluxe Automated SSL DV Single Domain (dlxssl-001domain-tier1dv)

Date            : 2026-05-15T-UC-02
Entry type      : Product name + surface
Entry value     : "Deluxe Automated SSL DV Single Domain certificate, 1-year term, slp_ssl surface, US market, all customers, Path A curated offer"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : NES — 100% (slp_ssl is NES for dlxssl-* products; 29 active curated offer slugs all confirmed under single offerId 35fc5321)
Gate asked      : none (all 6 dimensions resolved from entry)
CES chain steps : N/A — NES path
Champion        : Found — slug: dlxssl-001domain-tier1dv | Offer ID: 35fc5321-7723-4c40-906b-7b5c417e61cb | Offer Collection ID: Not available (Standalone — offerCollectionId returns null, offers[] is empty) | Plan: dvSingleDomain | Active: true | Discount codes: none
Flags fired     : 29-variant family sharing single offerId (all dlxssl-* slugs route to 35fc5321); Standalone geometry confirmed (no prePurchaseKeyMap, offers[] empty, offerCollectionId null); plan naming convention encodes validation type + domain count + tier (dv=Domain Validation, ov=Organization Validation, ev=Extended Validation; SingleDomain / MultiDomain5–100 / Wildcard); 38 total plan variants on this offerId across dv/ov/ev tiers; other tier/domain-count variants exist (dlxssl-005domains-tier1dv → dvMultiDomain5, dlxssl-wildcard-tier1dv → dvWildcard, etc.)
Ticket preview  : Not requested
Notes           : Standalone geometry means the EP ticket needs only Curated Offer ID (the specific slug) and Offer ID (35fc5321) — no Offer Collection ID field, no component offers, no prePurchaseKeyMap. The entire dlxssl SSL catalog is served from one offer definition ("SSL Certificate Subscriptions Offer", tag: sslsubs) with plan+term as the key differentiators. Each curated offer slug selects one plan from the 38-variant schema — that is the only configuration difference between all 29 dlxssl-* slugs. No discount codes present on either verified slug. Catalog-verified confidence: 97%.

## Run 2026-05-15-UC-03 — NES Bundle: MENA Digital Kit basic tier — two collection architectures (M365 tiers 1-3 vs Titan tiers 4-6)

Date            : 2026-05-15T-UC-03
Entry type      : Product name + surface
Entry value     : "MENA Digital Kit basic tier on mena-digital-kit surface, annual, MENA markets, all customers, Path A curated offer — email product unspecified"
Path            : A — Curated Offer
Offer operation : Create/Clone
Mode            : N/A
NES/CES branch  : NES — 100% (mena-digital-kit-* surfaces are NES-only)
Gate asked      : none — skill resolves to AMBIGUOUS rather than asking a clarifying gate; both architectures must be disclosed and ticket output blocked until analyst specifies email product
CES chain steps : N/A — NES path
Champion        : AMBIGUOUS — two architectures resolve for "basic tier": (1) mena-digital-kit-tier1: Offer Collection ID 7683d414-f935-4e62-93b1-89009a814162 (domainDudaEmail, ACTIVE), plan defaultBasicOfficebusinessps, discount disc000001 — components: NewDomain edf13c43 + Duda 2c5e3bb2 (plan basic) + M365 575a7d2a (plan officeBusinessPs). (2) mena-digital-kit-tier4: Offer Collection ID c377d7de-2108-3340-b580-44a32a17c416 (domainProfessionalEmail, ACTIVE), plan defaultBasicStartup, discount disc000007 — components: NewDomain edf13c43 + Duda 2c5e3bb2 (plan basic) + Titan Email 927a9d45 (plan light). Analyst must specify M365 or Titan Email before ticket output can be produced.
Flags fired     : Dual collection architecture on same surface — "basic tier" resolves to two structurally distinct NES bundles with different collection IDs and different email components; Tier naming collision — tier1 and tier4 are both "basic" in plan namespace (defaultBasicOfficebusinessps vs defaultBasicStartup) but belong to separate tier families; M365 vs Titan Email disambiguation required (575a7d2a officeBusinessPs vs 927a9d45 light); Duda plan=basic is identical in both architectures and cannot be used to disambiguate; disc000001 (M365 tiers) vs disc000007 (Titan tiers)
Ticket preview  : Not requested
Notes           : Tiers 1-3 use collection domainDudaEmail (7683d414), which carries M365 officeBusinessPs and supports multi-year terms (1/2/3 YEAR). Tiers 4-6 use collection domainProfessionalEmail (c377d7de), which carries Titan Email light and is annual-only (1 YEAR per collection schema). Both collections share NewDomainOffer (edf13c43) and dudaOffer (2c5e3bb2) components — Duda plan alone cannot disambiguate. The domainDudaEmail plan namespace is *OfficebusinessPs only; domainProfessionalEmail is *Startup only — non-overlapping plan families confirming architectural separation. A skill run without email product specified must not guess or default; it must disclose both architectures and block ticket output until disambiguation. Tier numbering is visible only in the curated offer slug, not in the plan field. Catalog-verified confidence: 100%.

---

## Wendy Measure — 2026-05-15T — i18nox vs wsb-vnext disambiguation on slp_wsb_* FOS surfaces

Date             : 2026-05-15
Audit type       : wendy-measure
Change           : Add slp_wsb_* surface champion filter in Step A2b branch decision: prefer wsb-vnext-* over vnext-i18nox-* on non-DEM FOS surfaces; flag as AMBIGUOUS when no wsb-vnext-* sibling exists.
Fix applied      : 2026-05-15
Scope filter     : Runs where surface ITC matches slp_wsb_* AND merchandising API returned vnext-i18nox-* as candidate for WAM Commerce PFID
Pre-fix rate     : 3/3 (100%)
Post-fix rate    : 0/0 (N/A — fix applied this session; no post-fix runs yet)
Delta            : N/A
Verdict          : INCONCLUSIVE
Notes            : Fix applied this session. Only 3 post-fix runs needed on slp_wsb_* WAM Commerce surfaces to confirm effectiveness. Re-run /ledger after next WAM Commerce FOS run.

---

## Wendy Measure — 2026-05-15T — Chain Step 2 NES-only slug disqualification when A2b returns zero matches

Date             : 2026-05-15
Audit type       : wendy-measure
Change           : Add merchandising validation check before Chain Step 2 success declaration: when A2b returned zero matches, disqualify any slug absent from the A2b match list as DISQUALIFIED (NES-only); proceed to Chain Step 3 if all candidates disqualified.
Fix applied      : 2026-05-15
Scope filter     : CES runs where A2b returned zero merchandising matches AND Chain Step 2 executed (catalog-era products, new/pre-launch PFIDs)
Pre-fix rate     : 0/7 (0%) — note: failure mode not observable in logged runs; WebFetch truncation prevented targeted slug retrieval; failure was only reproducible via batch-test agents using direct slug fetch
Post-fix rate    : 0/0 (N/A — fix applied this session; no post-fix runs yet)
Delta            : N/A
Verdict          : INCONCLUSIVE
Notes            : scope_post=0 — fix applied this session. The 0% pre-fix rate reflects a measurement gap: the failure mode was only observable in batch-test agents using targeted slug fetches, not in logged production runs that use truncated WebFetch. The fix addresses the keyword-scan path only; the targeted-fetch path (where agent fetches /v1/packages/{slug} directly and gets a PFID match) is not covered. Re-run /ledger after first post-fix batch-test or SSL surface production run.

---

## Wendy Measure — 2026-05-15T — M365 geo risk handling decision table

Date             : 2026-05-15
Audit type       : wendy-measure
Change           : M365 geo risk handling — decision table for stated target market (BLOCK for IN / WARN for global-unspecified / no-action for developed-market-only)
Fix applied      : 2026-05-15
Scope filter     : Live runs where M365 appeared as a product or bundle component in the offer analysis output
Pre-fix rate     : 5/10 (50%)
Post-fix rate    : 0/0 (N/A — fix applied this session; no post-fix runs yet)
Delta            : N/A
Verdict          : INCONCLUSIVE
Notes            : scope_post=0 — fix applied this session. 5 pre-fix triggers: MWP Basic SLP ROW+India (13T18:00), dpp_precheck M365 OE (13T22:00), dpp_precheck M365 OE full run (14T00:00), WAM+TrustedSite v1 (14T00:00), MWP Deluxe SLP (14T18:30) — all fired M365 geo risk flag with no downstream handling instruction. Re-run /ledger after first M365-component offer run post-fix.

---

## Wendy Measure — 2026-05-17T — Chain Step 1 NES-vs-CES validity check on CES surfaces

Date             : 2026-05-17
Audit type       : wendy-measure
Change           : NES-vs-CES validity check in Chain Step 1 success block — when get_curated_offer returns active for A2b merchandising match slug, confirm slug was present in A2b PFID match table; if absent (NES-only offer), emit NES reference block + NET-NEW BUILD instead of treating chain as resolved
Fix applied      : 2026-05-17
Scope filter     : CES-100% runs where Chain Step 1 executed with a successful curated offer match from A2b merchandising
Pre-fix rate     : 0/5 (0%) — failure mode not triggered in logged production runs; identified only via CMS-31766 batch-test (blind eval excluded from counts)
Post-fix rate    : 0/0 (N/A — fix applied this session; no post-fix runs yet)
Delta            : N/A
Verdict          : INCONCLUSIVE
Notes            : scope_post=0. Pre-fix rate was 0% in logged runs; failure mode detected via batch-test only. WebFetch truncation in production runs likely prevented the bug from manifesting — if A2b WebFetch couldn't retrieve the NES-only slug from a truncated response, Chain Step 1 wouldn't fire for that slug. Fix targets the targeted-fetch path used by batch-test agents. Note: Wendy's fix targets Chain Step 1 but CMS-31766's actual failure path goes through Chain Step 2 — fix does not resolve CMS-31766. Re-run /ledger after first CES surface Chain Step 1 run where a slug is fetched directly.
