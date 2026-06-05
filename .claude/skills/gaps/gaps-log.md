# Offer Pulse — Gaps Log

## GAP-001
Title      : B0 over-filtering: demand-side filters applied at PFID discovery step
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-13; two independent instances (agi-51 run + 18:00 run)

B0 PFID discovery must never filter by term, customer segment, or demand threshold
(new_customer_orders > 0). Two confirmed instances:
- 18:00 run: `product_term_num = 1` excluded PFID 1320704 (3-year WP hosting) → missed
  `wordpress-o365-forever-ssl-basic` bundle entirely
- agi-51: `new_customer_orders > 0` excluded PFIDs 958797/958799 (base annual WAM SKUs) →
  `wsb-vnext-tier3` and `wsb-vnext-tier4` unresolvable

Demand-side filters applied at B0 make valid package-component PFIDs permanently invisible
to all downstream steps (A1, A2, CES chain). Filters belong in A1/B1 experiment queries
only. Wendy brief ready (from 2026-05-13 pulse-audit report). Fix = two additions to B0:
(1) explicit prohibition on term/segment/demand filtering; (2) carry-forward rule to hold
analyst requirements for A1/B1 use.

Resolution : Wendy applied HARD CONSTRAINT to B0 step in SKILL.md: explicit prohibition on
             term/segment/demand filtering + carry-forward rule for A1/B1 use (2026-05-14).
             Dimension 5 positive instruction updated 2026-05-14 to explicitly exclude B0/M1
             from term filter carry-forward — co-locating the prohibition with the instruction
             that previously caused agents to apply the filter to all queries.
Resolved   : 2026-05-14

---

## GAP-002
Title      : product_term_unit_desc case mismatch: billing stores lowercase, SKILL.md documented Title Case
Status     : resolved
Category   : Instruction Ambiguity
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14 regression tests; UC5 and UC7 both returned zero rows on initial
             queries using 'Year' instead of 'year'; required manual retry to recover

The billing table offer_pulse_experiment stores product_term_unit_desc as lowercase ('year', 'month',
'quarter'). SKILL.md Dimension 5 (line 196) documented examples as 'Year', 'Month' (Title Case).
Agents following the documentation wrote `AND product_term_unit_desc = 'Year'` in query WHERE clauses,
which returned zero rows because the actual column values are lowercase. Both UC5 and UC7 encountered
this failure. While both agents self-corrected, the retry cost is unnecessary and there may be runs
where the agent doesn't notice the zero-row return and proceeds with an empty PFID list.

CES/NES architectural context: The term column encodes the billing cycle dimension of a PFID's term
matrix (MONTH/YEAR/QUARTER/SEMIANNUAL x N). A missed case match is a hard data contract failure —
the filter returns no rows even when the product and term actually exist. An empty B0 PFID list causes
the entire downstream chain to produce "no results" even for active products.

Resolution : SKILL.md Dimension 5 examples corrected to lowercase + explicit "lowercase only" warning
             added at lines 196, 224, and 230. Fixed 2026-05-14 (Wendy, pulse-audit regression session).
Resolved   : 2026-05-14

---

## GAP-003
Title      : Ticket-first entry path never exercised in practice
Status     : open
Category   : Process Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : All 7 logged runs used product-name-first or ITC-first entry; zero used
             Entry Option 1 (Jira ticket key as starting point) despite most runs having
             a source ticket. Confirmed pattern across 6 real source tickets
             (CMS-33982, CMS-31421, EP-82036, AGIGROWTH-92, AGIGROWTH-51, AGIGROWTH-161).

Analysts consistently open offer-pulse with a product name or ITC even when a Jira ticket
is available. This means the richer Jira-extraction steps added in Entry Option 1 — target
price, offers being replaced, discount codes, multi-arm decomposition — are never triggered
automatically. Analysts miss these extracted fields and must supply them manually later (or
not at all), which was the root cause of several ticket quality gaps (JT-3a/b/c, JT-4)
identified in the 2026-05-14 pulse-audit.

This is a behavioral/habit issue, not a skill logic issue. SKILL.md was updated to support
ticket-first entry correctly, but uptake requires analyst awareness. Consider:
- Adding a prompt at product-name-first entry: "Do you have a Jira ticket for this work?
  Passing the ticket key first lets me extract price targets, removal scope, and detect
  multi-arm experiments automatically."
- Adding a note to onboarding / skill README pointing to Entry Option 1 as the preferred
  starting point when a ticket exists.

Resolution : —
Resolved   : —

---

## GAP-004
Title      : Market gate fires without stated default
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; market gate fired in 63.6% of runs across all entry types

The Clarifying Questions Gate asks "What market(s)?" on every run where market was not
pre-stated. No documented default exists in SKILL.md, so the agent always asks even when
the analyst's intent is US/USD (the overwhelming majority case). This creates unnecessary
friction and means catalog calls (which require a currency/marketId) cannot proceed until
the gate clears. Fix: add "globally scoped unless stated otherwise" default — US/USD for
catalog calls — so the gate only fires when a non-default market is explicitly relevant.

Resolution : Wendy added US/USD default to Dimension 3 — gate now fires only when a non-US
             or multi-market scope is explicitly stated. Catalog calls default to US/USD
             without blocking on the gate. Fixed 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-005
Title      : Source offer to clone not identified as distinct output field
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; NES Modify/Clone output doesn't emit Source to Clone
             as a separate field; analysts must infer it from Champion line

When Offer Operation = Modify or Clone, the champion IS the source to clone — but the
Quick Reference template has no dedicated "Source to Clone" field. Ecomm engineers report
confusion about whether to clone the champion slug or one of its components. Fix:
when the discounted-variant flag fires or Offer Operation = Clone/Modify, restructure
the Champion line to two fields: `Champion : {slug}` and `Source to Clone : {slug}` —
where Source to Clone is the base (non-discounted) slug when a discounted variant was
detected, or the champion slug otherwise. This makes the clone target unambiguous.

Resolution : Wendy added conditional "Source to Clone" field — emits as a distinct line
             below Champion when Offer Operation = Modify/Clone AND discounted-variant flag
             fired; base slug is the clone target. No duplication on clean runs. Fixed
             2026-05-14.
Resolved   : 2026-05-14

---

## GAP-006
Title      : Ticket type classifier missing — config/toggle/rebate tickets have no early exit
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; AGIGROWTH-244 (rebate), AGIGROWTH-55 (config toggle)
             went through full gate + query chain before being determined out-of-scope

Config change tickets, feature toggles, and rebate/cashback tickets (e.g. AGIGROWTH-244,
AGIGROWTH-55) have no offer to create or price to change — they require no EP ticket.
Currently these reach the full Clarifying Questions Gate and query chain before the analyst
or agent determines they are out-of-scope. Fix: add a pre-gate classifier in Entry Option 1
step 4 that detects ticket-type signals ("rebate", "cashback", "config toggle", "feature
flag", "enable/disable") and emits an early-exit block: "This ticket appears to be a
{type} ticket — no EP offer ticket is required. Confirm and close." Gate and queries are
skipped entirely when the classifier fires.

Resolution : Wendy added ticket-type classifier as step 3 of Entry Option 1 (before multi-arm
             detection, now step 4). Covers rebate/cashback, config toggle/feature flag,
             reporting-only, and legal/compliance signals. Emits EARLY EXIT block and halts
             for analyst confirmation. Fixed 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-007
Title      : Rolled-back offer state invisible — active catalog + zero billing is ambiguous
Status     : open
Category   : Data Coverage Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; NES catalog has no rollback field;
             active=true is human-set and may persist after rollback

NES catalog has no native rollback/deactivated state. When an offer is rolled back,
engineering sets `active=false` manually — but this does not always happen. An offer with
`active=true` and zero billing rows in the last 7 days is ambiguous: it could be pre-launch,
rolled-back, or legitimately zero-volume. The skill currently has no way to distinguish
these states, which means a rolled-back champion may be incorrectly presented as the
clone source. This is a data limitation, not a routing issue — the catalog API does not
expose rollback history. Fix: add a diagnostic-only flag in the output: "Active catalog
entry with zero billing rows — may be pre-launch, rolled-back, or zero-volume. Confirm
live status with ecomm before cloning." Do not change routing based on this flag.

Resolution : —
Resolved   : —

---

## GAP-008
Title      : Pre-launch NES surface looks identical to CES — catalog scan required first
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; zero billing rows for a NES product
             triggers CES path in error if catalog scan is skipped

When a product exists in NES catalog but has not yet launched (zero billing rows), Step A1
returns zero rows and the current routing sends the analyst down the CES chain. The CES
chain will exhaust without finding a champion because the product is NES, not CES. This
produces a false "net-new build required" conclusion. Fix: before concluding CES and
entering the CES chain, run a catalog ID scan (get_curated_offers filtered by product name
or tag) to check whether the product exists in NES catalog with zero billing. If found,
route as NES pre-launch and emit a "PRE-LAUNCH NES" disclosure rather than triggering
the CES chain. This distinguishes pre-launch NES from genuine CES surfaces.

Resolution : Wendy replaced the simple NES=0%→A2b branch with a three-way routing table
             including a mandatory pre-launch NES check (get_curated_offers keyword match
             before entering A2b). Active catalog matches with zero billing → PRE-LAUNCH NES
             disclosure + route to A2a. No catalog matches → falls through to A2b as before.
             Fixed 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-009
Title      : WAM FOS dual-path detection missing — slp_wsb_* (CES) + NES surfaces require
             two EP tickets
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; AGIGROWTH-161 WAM tier experiment spanned slp_wsb_*
             (CES) and slp_hosting_4gh (NES); single-path output produced; two EP tickets
             required with different engineering owners

WAM experiments frequently span both CES surfaces (slp_wsb_*) and NES surfaces
(slp_hosting_4gh, slp_wordpress). These require two separate EP tickets filed to different
engineering owners: CES requests go to @sparmar, NES requests go to catalog tools. The
current skill produces a single-path output even when both surface types are detected in
Step A1. Fix: in Step A2, after the NES/CES surface split, detect when PFIDs are active
on both slp_wsb_* AND slp_hosting_4gh/slp_wordpress simultaneously. If dual-path is
detected, generate two separate output blocks — one NES Quick Reference and one CES
Quick Reference — with a header: "DUAL-PATH EXPERIMENT: Two EP tickets required."
Each block must include its respective engineering owner note.

Resolution : Wendy added WAM dual-path detection block to Step A2. Triggers when product PNL
             = WAM/WSB and PFIDs are active on both CES-pattern ITCs (slp_wsb_*) and NES-
             pattern ITCs (slp_hosting_4gh, slp_wordpress) simultaneously. Emits DUAL-PATH
             EXPERIMENT header + two separate output sections with engineering owner notes.
             Fixed 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-010
Title      : Free-trial $0 components invisible on CES path
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; free component checkpoint exists only
             on NES path (A2a); CES path (A2b) has no equivalent check

Free-trial PFIDs (purchaseType=Free) generate zero billing rows permanently — they are
invisible to Step A1 billing queries on all paths. The NES path has a "Free component
checkpoint" that scans prePurchaseKeyMap for FREEACCOUNT entries. The CES path has no
equivalent. After a successful A2b merchandising match, if the matched package contains
pfids[] entries with purchaseType=Free, those PFIDs will be missing from the PFID list.
Fix: after Step A2b merchandising match, check matched package pfids[] array for any
entries where purchaseType=Free. If found, add those PFIDs to the PFID list with a
"(free trial component — not in billing)" annotation and include them in the completeness
count. This mirrors the NES free component checkpoint for the CES path.

Resolution : Wendy added CES free-trial component check block after Step A2b match. Inspects
             matched package pfids[] for entries absent from Step A1 billing; resolves
             purchaseType=Free entries and adds them to PFID list with annotation. Mirrors
             the NES free component checkpoint. Fixed 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-011
Title      : CM email / shelf channel blind spot — no ITC in billing, returns zero rows
Status     : open
Category   : Data Coverage Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; CM/SAPI delivery channels produce
             no ITC in billing; skill runs full query chain and returns zero rows with
             generic "no results" advice

CM (Cohort Marketing) and SAPI (shelf) channels deliver offers via email and in-app
prompts. These channels do not produce ITC-tagged add-to-cart events in the billing
tables that offer-pulse queries. An analyst who enters a CM or shelf surface ITC gets
zero rows from every billing query and no useful output. This is a data architecture
limitation — these channels are fundamentally not captured in CLN/billing data. Fix:
add a channel pre-check step before all billing queries. If the ITC or surface name
matches known CM/SAPI patterns (e.g. contains "email", "shelf", "cohort", "cm_", "sapi_"),
emit an early exit: "CM/shelf channels are not captured in billing or CLN data — offer
discovery via this path is not supported. Use catalog MCP tools directly with the known
curated offer slug if available." Do not run billing queries for these channels.

Resolution : —
Resolved   : —

---

## GAP-012
Title      : Incumbent offers not enumerated — deactivation scope missing from output
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; Modify path discovers existing active packages in
             Step A1 billing data but output spec has no dedicated deactivation-scope
             table; ecomm engineers must infer which offers to deactivate

When Offer Operation = Modify, Step A1 discovers all currently-active package_id values
on the surface. The Quick Reference output shows a Champion for cloning but has no field
that explicitly lists the incumbent offers that must be deactivated when the new offer
goes live. Ecomm engineers have reported filing deactivation requests for the wrong offers
as a result. Fix: add a mandatory "Deactivation Scope" table to the Modify/Clone output,
immediately after the Quick Reference block. The table lists every currently-active
package_id observed in Step A1 billing (7d), with volume and a Status column defaulting
to "Deactivate on launch". One-column annotation: "Confirm deactivation list with ecomm
before filing — do not deactivate offers active on other surfaces."

Resolution : —
Resolved   : —

---

## GAP-013
Title      : Chain Step 3 unreachable when billing returns 0 rows for catalog-native products
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : AGIGROWTH-161 Runs 19:00 and 22:00 — 0 billing rows / all-null package_ids for
             M365 on dpp_precheck; chain resolved via Step 2 ID scan; analyst confirmed
             catalog_query_get_offers with tags=["m365"] is the direct path for this geometry.
             Identified by ces-nes + pulse-audit analysis 2026-05-14.

Chain Step 3 instruction says "derive product type tags from the surface PFIDs." This fails
when billing returns zero rows for the target product — no PFIDs exist to derive tags from.
For catalog-native products (M365, Titan Email, SSL), the tags are resolvable from the
product name in the request without any billing data:
  "Microsoft 365" / "M365" → tags=["m365"]
  "Titan Email" / "Titan" → tags=["titanemail"]
  "SSL" / "certificate" → tags=["sslcert"]

When the request names the target product and it maps to a known catalog tag, Chain Step 3
should run IN PARALLEL with Chain Step 2 — not only as a sequential fallback after both
Steps 1 and 2 exhaust. In the AGIGROWTH-161 case the ID scan (Step 2) found the champion,
but catalog_query_get_offers would have returned 124 M365 plans; filtering by plan attribute
keywords from the request ("online", "essentials", "no teams") would have confirmed the
same offer ID via plan name "onlineEssentialsNoTeams".

Fix direction: add a product-name → known-tag mapping table to Chain Step 3. When the
target product name matches a known-tag entry, trigger Step 3 in parallel with Step 2.
Also add plan-attribute filtering guidance for large plan sets: when the request specifies
plan attributes (e.g. "Online Essentials w/o Teams"), filter returned plans[] by extracting
keywords from those attributes and matching against plan name strings.

Resolution : Wendy added known-tag product mapping table to Chain Step 3 (M365, Titan Email,
             SSL, WAM, Professional Email → confirmed stable tags). When product name matches,
             Step 3 fires IN PARALLEL with Step 2. Added plan-attribute keyword filtering
             guidance for large plan sets (extract attributes from request, match against plan
             name strings). Fallback PFID-derived path retained for unlisted products. Fixed
             2026-05-14.
Resolved   : 2026-05-14

---

## GAP-014
Title      : Chain Step 2 keyword seeds (Create/Clone mode) don't cover full surface vocab
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : Run 21:00 (WAM on dpp_precheck) — seeds too narrow, missed wsb-vnext and
             i18nox family. Run 15:00 (TrustedSite on dpp_precheck) — 7 required CES packages
             absent from candidate table; seed list lacked vnext, wsb, wam, i18n terms. Both
             confirmed by pulse-audit 2026-05-14.

SKILL.md has a surface → keyword seed table in Step M1 (Modify mode) mandating seeds like
"precheck, dpp, wsb, vnext, wam, i18n, m365, solutionset" for dpp_precheck. That table does
NOT apply to Step A2c Chain Step 2 (Create/Clone mode). Chain Step 2 derives keywords only
from: (1) target product name/SKU, (2) surface ITC string tokens, (3) PFID labels from A1.

For a surface like dpp_precheck, ITC-token seeds ("dpp", "precheck") are insufficient. The
surface hosts multiple product families (WAM/WSB vnext, i18n variants, M365 email tiers,
solutionset bundles) with no string overlap with the ITC or target product name. An incomplete
keyword seed produces a candidate table that misses live packages on the surface — directly
causing wrong or incomplete ecomm tickets (confirmed: Runs 21:00 and 15:00, multiple missed
packages each).

Fix direction: add the M1 surface → keyword seed table (or a reference to it) into Chain
Step 2 so it applies to Create/Clone mode equally. Alternatively, consolidate into a single
shared Keyword Seed table referenced from both Step M1 and Chain Step 2.

Resolution : Wendy added surface keyword seed table as source 4 in Chain Step 2 keyword
             derivation (identical to M1 table, plus slp_hosting_4gh row). Added explicit
             rule: "Score matches on ANY of the surface's required keywords." HARD CONSTRAINTS
             updated to reference both M1 and Chain Step 2 as seed-table-required. Fixed
             2026-05-14.
Resolved   : 2026-05-14

---

## GAP-015
Title      : Term gate fires in 91% of runs — pre-parse rarely matches Jira ticket language
Status     : open
Category   : Known Limitation
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; Term asked in 10/11 runs (91%); only run where term was
             pre-answered was Titan free-trial (explicit "14-day" in entry). All other entries
             were Jira tickets or product names without parseable term language.

Dimension 5's Term pre-parse table targets explicit text patterns ("annual", "1-year",
"$X/mo", etc.). In practice, most offer-pulse entries are Jira ticket descriptions or
product-name phrases that reference pricing or target SKUs without stating the billing
term explicitly. As a result, the pre-parse table fires in <10% of runs and the Term gate
fires in >90% — adding a clarification round-trip to nearly every run.

The underlying cause is partly a data limitation: term cannot be reliably inferred from
billing context before B0 runs (the product's PFID matrix spans multiple terms by design),
and B0 must run without a term filter. A secondary inference after B0 (check whether all
active-surface PFIDs for this product cluster into one dominant term) is possible but
risky — a product legitimately sold at multiple terms (1yr and 3yr simultaneously) would
produce a false single-term inference.

Fix direction (if addressed): after B0 produces the PFID list, query the billing table for
term distribution of those PFIDs on the target surface. If one term accounts for >80% of
volume, infer it and ask for confirmation rather than asking from scratch. This reduces the
gate to a confirm-or-override rather than an open question. Not fixing currently — the
round-trip cost is low and a wrong term inference causes more damage than asking.

Resolution : —
Resolved   : —

---

## GAP-016
Title      : Component PFID ambiguity — base vs add-on role undetectable from billing data alone
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; shared component PFIDs (SSL 3604, M365
             464069, OX email 1192198) appear in pfids[] of dozens of CES packages; B0 has no
             classification step to distinguish base-product vs add-on role.

Three failure modes:

1. CES path — one PFID, many packages. Shared add-on PFIDs (SSL 3604, M365 464069, OX
   email 1192198) appear in pfids[] across dozens of packages, sometimes as the primary
   product, sometimes as a purchaseType=Free add-on. A2b merchandising match returns an
   undifferentiated candidate list with no grouping by role. Champion identification
   degrades — analyst cannot tell which candidates are bundles-with-this-as-add-on vs
   offers-for-this-product-specifically.

2. NES path — CLN join resolves at event level, but not semantically. Querying by a
   component PFID (e.g., M365 PFID on a hosting surface) returns the parent bundle slug
   via the add_to_cart_event_id join — correct technically, but the analyst querying
   "what M365 offer is on this surface" may receive a hosting bundle slug without
   realizing M365 is a bundled component, not the priced base product.

3. B0 PFID discovery — no add-on flag. When the input product is a component category
   (SSL, M365, email), B0 may surface PFIDs from two populations: (a) standalone offer
   PFIDs and (b) component PFIDs appearing in billing because they were provisioned as
   part of a bundle. No B0 instruction distinguishes these; the mixed list flows into
   A1 without disclosure.

Fix direction:
- CES A2b: after merchandising match, classify each candidate package by whether the
  target PFID is a core term-matrix entry (purchaseType=Standard) vs a free add-on
  (purchaseType=Free with fixedTerm). Emit in two groups: "Primary product packages"
  and "Bundle add-on packages."
- NES A2a: when input PFID maps to a known reusable component UUID (M365 575a7d2a,
  SSL 28e5b730, Titan Email 927a9d45, Professional Email 2468b30f), emit a disclosure:
  "This product is a known bundle component — champion will reflect parent bundle(s),
  not a standalone offer for this product."
- B0: flag known high-cardinality add-on PFIDs (3604 SSL, 464069 M365 free trial,
  1192198 OX email) before the A1 step, noting they appear as components in many
  bundles and champion resolution will require bundle-level disambiguation.

Resolution : Two-part fix applied to SKILL.md 2026-05-14. Part A: B0 add-on annotation
             block added — known add-on PFIDs (3604 SSL, 464069 M365, 1192198 OX/Titan)
             are flagged automatically in the B0 confirmation table when present; not
             suppressed. Part B: Dimension 0b gate question added between Dimension 0 and
             Dimension 1 — fires only when B0 annotation triggered and role not explicit
             in entry. Three routing outcomes: Primary (filter A2b to products[].pfids[]),
             Add-on (filter to addons[]), Unsure (dual-group output, analyst selects).
             ces-nes + analyst signed off at high confidence 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-017
Title      : Surface-context filtering absent — wrong-surface NES candidates not flagged
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : Blind eval Case 4 (CMS-32825, slp_ssl_config); dlxssl-* NES offers (serving
             slp_ssl) returned as answer for slp_ssl_config request; confirmed by buddy
             scoring 2026-05-14.

After catalog candidate retrieval (Chain Step 2/3 or CES chain), no step verifies that
returned offer slugs actually serve the target surface. In Case 4, the catalog scan returned
dlxssl-* curated offers — all active, all matching "ssl" keywords — but those offers are
wired to slp_ssl, not slp_ssl_config. The skill presented them as valid candidates rather
than flagging them as false positives for the requested surface.

Fix direction: after assembling the candidate list, add a surface-verification step. For
each NES candidate, call get_curated_offer and inspect the wiredSurfaces/ITC field to
confirm the offer actually serves the target ITC pattern. Flag candidates that serve a
different surface: "WARNING: this offer serves {served_surface}, not {requested_surface}
— confirm wiring with ecomm before using." For CES candidates, cross-check the ITC column
in offer_pulse_experiment billing data.

Resolution : Partial — Option 2 surface label enrichment (2026-05-16) adds surface_nes_ces
             annotation from surface-vocab to the ROUTE line and Quick Reference Surface
             field. Analyst sees the surface's NES/CES classification before reviewing
             catalog candidates, which reduces the risk of silently accepting a wrong-
             surface match. Full fix (per-candidate wiredSurfaces/ITC verification against
             catalog) is still pending.
Resolved   : —

---

## GAP-018
Title      : Wire-to-surface mode detection missing — active offers proposed as Clone targets
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : Blind eval Case 8 (Titan email, UPP surface); active Rev-3 Titan email offer
             in catalog; skill proposed Clone instead of Wire-to-surface; confirmed by
             buddy scoring 2026-05-14.

When an offer already exists in the catalog in an active state, the correct operation is
Wire-to-surface — not Clone to create a new offer instance. The skill has no logic to detect
whether an active offer already exists for the target product before recommending Create/Clone.
In Case 8, catalog contained an active Rev-3 Titan email free trial offer; the skill found it
via Chain Step 3 but defaulted to "Clone from this."

Fix direction: after Chain Step 2/3 resolves a candidate offer, check active=true status and
revision count (Rev > 1 is a strong signal of a production offer). If active=true AND the
offer has been previously active, emit: "EXISTING ACTIVE OFFER DETECTED — consider
Wire-to-surface rather than Clone. Confirm with ecomm whether this offer can be wired
directly vs. requires a new offer instance." Only recommend Clone when the candidate is
in draft/inactive status or has never been wired to a production surface.

Resolution : —
Resolved   : —

---

## GAP-019
Title      : Multi-product B0 discovery is single-anchor — sibling PFIDs in bundle missed
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : Blind eval Case 1 (WAM+Commerce TrustedSite); base WAM PFIDs 958797/958799
             absent; B0 anchored only on TrustedSite PFID. Case 3: 4 precheck-suffixed i18n
             slug variants missed; keyword seeds insufficient for full slug coverage.

When a request names multiple products, B0 discovers PFIDs for only the anchor product and
silently omits sibling products unless they share a billing experiment row with the anchor.
This is distinct from the resolved term-filter regression (GAP-001): the architectural
issue is that B0 runs once per request, not once per named product.

Fix direction: at B0 entry, parse the distinct product list from the input. For each named
product, run a separate billing query against offer_pulse_experiment. Union the PFID results.
Emit a "Products discovered" header listing each product and its PFID count so the analyst
can verify completeness before A1 runs.

Resolution : Multi-product B0 handling block added to SKILL.md 2026-05-14. Rule: parse
             distinct named products from the entry (products the analyst explicitly wants
             to price/scope — not bundle components discovered via catalog). Run one B0
             query per product in parallel. Union results; deduplicate on pf_id. Confirmation
             step presents results grouped by product family (one sub-table per product),
             hard-stops until analyst confirms all groups. HARD CONSTRAINT on per-product
             queries: filter prohibition (no term/segment/volume) applies to each query
             individually. Also added: surface FOS→slp_* and product alias columns to
             known-tag table (inline crosswalk) — ces-nes + analyst signed off 2026-05-14.
Resolved   : 2026-05-14

---

## GAP-021
Title      : Dual-series CES champion suppression — shared PFID across multiple product series
             silently resolves to one champion; alternatives buried in Candidate table
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : PFID 970473 (WAM Commerce annual) confirmed present in both wsb-vnext-tier4
             (US/M365) and vnext-i18nox-tier4 (International/Titan Email). Chain Step 1
             resolved to vnext-i18nox-tier4 (High-confidence merchandising match); wsb-vnext-
             tier4 was buried in Section 4. Analyst: "How come you didn't also pull
             wsb-vnext-tier4?" PFID presence in both packages confirmed by analyst 2026-05-14.

When Chain Step 1 finds a High-confidence merchandising match for a PFID, it emits "Chain
resolved." and the skill stops gathering evidence. This is correct for single-series surfaces.
But when the same PFID is present in packages from two distinct product-series families
(e.g. wsb-vnext-* and vnext-i18nox-*), both families simultaneously serve the surface with
different email products (M365 vs Titan Email) and different geographic scope (US/Global vs
International). Chain Step 1's "stop" instruction has no carve-out for this case. Chain
Step 2 runs the right keyword seeds and surfaces the second series in the Candidate table,
but the output instruction provides no rule to split the Candidate table into separate
champion blocks — so both series land in Section 4 as an undifferentiated list and the
analyst never sees that two parallel, independently-valid configurations exist.

The failure generalizes: any surface where two product-series slug families share a PFID
and represent meaningfully different configurations (different email product, different geo
scope, different term matrix) will silently pick one series as the output champion.

Fix: three-part instruction change to SKILL.md.
(1) Chain Step 1 — after "Chain resolved.", add a Dual-series continuation check: if the
    matched package slug belongs to a known dual-series family (i18nox or wsb-vnext), do
    NOT stop. Continue to Chain Step 2 to check whether the sibling series also has a
    candidate. Only stop if Chain Step 2 confirms no sibling series is present.
(2) Chain Step 2 — after the "All-M-shown rule", add a Series-split rule: after all M
    candidates are collected, inspect the candidate slugs for entries from two or more
    distinct slug-prefix series families. If two or more series are detected AND they
    represent different product configurations (different email product, different geo scope),
    emit SEPARATE Quick Reference champion blocks — one per series — rather than a single
    block with an ambiguous champion. Each block carries its own series label.
(3) Shared Series Disambiguation block — extract the i18nox/wsb-vnext disambiguation table
    from M1 and move it to a shared block referenced from both M1 and Chain Step 2. Extend
    the rule to cover the general pattern: any two slug-prefix families that share a PFID
    and represent different configurations require separate blocks. M1 now references this
    shared block instead of containing it inline.

Resolution : Three-part fix applied to SKILL.md 2026-05-14. (1) Chain Step 1 gains a
             Dual-series continuation check — when matched slug belongs to a dual-series
             family, does not stop; continues to Chain Step 2 to gather the sibling.
             (2) Chain Step 2 gains a Series-split rule — after all-M candidates collected,
             detects multi-series presence and emits separate champion blocks per series.
             (3) Shared Series Disambiguation block added between Step A2c and Path A Modify
             Mode; M1 inline disambiguation table replaced with a reference to the shared
             block. Fix is systematic — covers any future dual-series case, not just
             i18nox/wsb-vnext by name. No change to single-series output path.
Resolved   : 2026-05-14

---

## GAP-020
Title      : Discount codes from Jira not verified against billing history
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : Blind eval Case 5 (CMS-32651 Email Backup); DISC004590 extracted from Jira,
             passed to output without billing validation; expected flag missing; confirmed
             by buddy scoring 2026-05-14.

When a discount code is extracted from a Jira ticket or analyst input, it is passed directly
to the Discount Ticket Summary without any billing verification step. If the code has no
billing history on the target surface it may be a draft code, a code from a different
surface, or a code from a prior inactive experiment — and the analyst cannot know this from
the output alone.

Fix direction: after extracting a discount code, query offer_pulse_experiment for
`discount_code = '{code}'` on the target surface. If zero rows: emit warning "Discount
code {code} has no billing history on this surface — confirm with pricing/experimentation
team that this code is active and intended for {surface}." If rows found: include most
recent order date and volume as confirmation. Does not block output — surfaces an
actionable validation signal before the ticket is filed.

Resolution : —
Resolved   : —

---

## GAP-022
Title      : Path B (Pricing/Discount) workflow unvalidated — never exercised in logged runs
Status     : resolved
Category   : Process Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : pulse-audit 2026-05-14; 0 of 21 logged runs used Path B (PFID Inventory Mode
             or Blast Radius Mode); confirmed by use-case log review.

The Path B instructions (PFID Inventory Mode, Blast Radius Mode) exist in SKILL.md but have
never been exercised in the logged use-case history. Accuracy is entirely unvalidated. All
21 runs used Path A (Create/Clone/Modify). Pricing ticket requests will hit this path; if
instructions are incorrect or incomplete, failures won't be caught until a real pricing
ticket is mis-produced and the error surfaces through a downstream pricing change.

Fix direction: intentionally run two Path B scenarios — one PFID Inventory Mode run and one
Blast Radius Mode run — against known real pricing tickets. Log results to use-case log and
run buddy scoring against expected outputs. Fix any gaps found before the next pricing
experiment kicks off.

Resolution : Path B (Pricing/Discount) was removed from offer-pulse entirely on 2026-05-17.
             PFID Inventory Mode and Blast Radius Mode instructions were deleted. All pricing
             and discount scope is now owned by /pricing-ticket. Gap is moot.
Resolved   : 2026-05-17

---

## GAP-023
Title      : apiVersion 3 component resolution silently fails — no disclosure to distinguish
             V3 from a real lookup error
Status     : open
Category   : Known Limitation
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; curated offers created by
             entities-transformation-job (June 2023 batch) have offerIds[] arrays with
             internal IDs that return NOT FOUND via get_offer_definition_by_id.

Curated offers created by the entities-transformation-job batch (apiVersion 3, June 2023)
have offerIds[] arrays containing internal IDs that do not resolve via the public
get_offer_definition_by_id tool — they return NOT FOUND. SKILL.md has no explicit
instruction for this case. Current behavior is "lookup failed — verify manually" but there
is no disclosure to distinguish a V3 ID from a genuine lookup error on a valid offer ID.

Affected products: IT services, SEO, DNS listings, and related products from the June 2023
batch. If a ticket targets those surfaces, component resolution will silently fail with no
useful output for ecomm — the analyst sees "NOT FOUND" for every component and cannot
distinguish this from a real gap.

Fix direction: add an apiVersion detection step. After get_curated_offer returns, inspect
the apiVersion field. If apiVersion = 3, emit a disclosure before attempting component
lookups: "This offer was created by entities-transformation-job (apiVersion 3). Component
offer IDs in this version are internal IDs that may not resolve via get_offer_definition_by_id.
If component lookups return NOT FOUND, this is expected for V3 offers — verify component
list directly with ecomm or the catalog team." Do not present V3 NOT FOUND results as
ambiguous lookup failures.

Resolution : —
Resolved   : —

---

## GAP-024
Title      : offersGrouping-without-prePurchaseKeyMap geometry misclassification — components
             invisible in Standalone classification
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; VPS4-style bundles have offersGrouping
             parent/child structure but no prePurchaseKeyMap; classified as Standalone.

Some Offer Collections (e.g. VPS4-style bundles, dedicated server bundles, custom bundles)
have an offersGrouping parent/child structure but no prePurchaseKeyMap. The current geometry
classification rule is: "prePurchaseKeyMap absent → Standalone." This is incorrect for
offersGrouping bundles — components exist in offers[] but are invisible because the
Standalone path does not inspect offers[]. Any VPS4, dedicated server, or custom bundle
that uses offersGrouping without prePurchaseKeyMap provisioning overrides will be
misclassified as Standalone and its components will be missing from the output.

Fix direction: add a secondary geometry check. After classifying as Standalone (no
prePurchaseKeyMap), inspect whether the offer has an offersGrouping field with child offer
entries. If offersGrouping is present with child offers, reclassify as "Offer Collection
(offersGrouping)" and extract components from the offers[] array using the offersGrouping
parent/child structure. The prePurchaseKeyMap path remains for the standard Offer Collection
geometry; this is an additive second path for the offersGrouping variant.

Resolution : —
Resolved   : —

---

## GAP-025
Title      : Backtest ground truth is time-sensitive — champion at eval run may differ from
             champion at ticket creation
Status     : open
Category   : Process Gap
Skill      : use-cases
Added      : 2026-05-14
Evidence   : Blind eval 2026-05-14; source tickets span multiple sprints; no timestamp
             alignment performed between ticket creation date and champion lookup date.
             Identified during leadership readout prep — distinct from HE-010 (circularity
             from prior runs).

When a blind evaluation uses real historical tickets as test cases, the expected champion
slug is typically sourced from the current catalog state — not the catalog state at the time
the ticket was filed. If the champion has since been superseded, rolled back, or replaced
by a new experiment winner, the eval will incorrectly mark a historically-correct skill
output as ✗, or a currently-correct-but-historically-wrong output as ✓.

This problem compounds as source tickets age. A ticket filed three sprints ago on a fast-
moving surface (e.g. dpp_precheck M365, WAM FOS) may have had a completely different
champion than what catalog shows today. No timestamp alignment was performed in the
2026-05-14 evaluation — all expected slugs reflect current catalog state.

Fix direction: when assembling expected outputs for a backtest eval, record the ticket
creation date alongside the expected champion. For tickets older than ~30 days, query
offer_pulse_experiment billing data for the dominant package_id on the target surface
during the week the ticket was filed — use that as the expected champion, not the current
one. Alternatively, mark N1/C6 as ~ (unverifiable) for historical tickets rather than
asserting a point-in-time champion that may be stale.

Resolution : —
Resolved   : —

---

## GAP-026
Title      : Non-standard slug format has no normalization step — camelCase/offer- prefix
             causes Chain Step 2 to be the only recovery path, with no explicit fallback
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : HE-016; CMS-31766 blind eval — slug "offer-sslcert-managedWithMonitoring" in
             Jira ticket body; direct get_curated_offer returned NOT FOUND; Chain Step 2
             ID scan recovered the correct kebab-case slug "sslcert-managed-with-monitoring".

When a Jira ticket or analyst input contains a non-standard slug format (offer- prefix,
camelCase, or mixed case), the skill's first action is a direct get_curated_offer call that
returns NOT FOUND. Recovery flows to Chain Step 2 (ID scan by keyword). Chain Step 2 worked
in the CMS-31766 case, but only because SSL keyword seeds are broad enough to surface the
correct slug.

The gap: there is no explicit slug normalization step between the NOT FOUND and the Chain
Step 2 fallback. For products with narrow keyword coverage (e.g. niche bundles, short
product names), Chain Step 2 may also miss the offer. The skill has no instruction to:
(1) strip the "offer-" prefix and retry the direct lookup;
(2) convert camelCase to kebab-case and retry;
(3) note that the verbatim slug was NOT FOUND but a normalized version was found.

Without normalization, the analyst never learns that their ticket slug was in the wrong
format — the skill just silently succeeds via the ID scan with no disclosure.

Fix direction: after a NOT FOUND on direct get_curated_offer, before Chain Step 2:
(1) Check whether the slug matches the `offer-` prefix or camelCase patterns.
(2) If yes, attempt normalization: strip "offer-", convert camelCase → kebab-case, retry
    get_curated_offer on the normalized slug. If the normalized slug succeeds, note in
    output: "Slug '{original}' not found — resolved via normalization to '{normalized}'."
(3) Only fall through to Chain Step 2 if both the original and normalized slug return NOT
    FOUND. This makes the normalization attempt explicit and informs the analyst that their
    ticket slug format is non-standard.

Resolution : —
Resolved   : —

---

## GAP-027
Title      : D0/D1 gate pricing-framing inference auto-proceed unsafe — direction-neutral
             signals cannot distinguish Path A from Path B
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : ces-nes architectural review 2026-05-14; Wendy Fix 1 implemented auto-proceed
             when pricing-amount signals ($X/mo, DISC######) present alongside
             surface+product. ces-nes vetoed: "$X/mo display price" and "DISC######" appear
             equally in Path A ("create a new offer at $6.99/mo") and Path B ("verify the
             $6.99/mo display price is correct for MWP Basic") — inferring Create/Clone from
             these alone produces false positives on audit requests.

Wendy's original Fix 1 treated pricing-amount signals as Path A indicators and auto-
proceeded when they were present alongside a surface or product name. ces-nes disagreed:
these signals are direction-neutral descriptors of the artifact under discussion, not
operation-type signals. An analyst asking "verify the display price is $3.99/mo for M365
Online Essentials on dpp_precheck" would be misrouted to Path A (create) when their intent
is Path B (audit). The fix is a one-question approach: when pricing-amount signals are
present but no explicit Create/Clone/Modify tokens are found, ask ONE combined D0+D1
question that disambiguates in a single round-trip. Explicit Create/Clone/Modify tokens
(new offer, clone, add component to, etc.) still resolve D0 without asking.

Resolution : Combined D0+D1 question approach applied to SKILL.md 2026-05-14. Auto-proceed
             inference removed. Pricing-amount signals now trigger the combined question
             instead of auto-proceeding. Explicit Create/Modify tokens still resolve D0
             without asking.
Resolved   : —

---

## GAP-028
Title      : CES output missing canonical PFID field — C2 criterion unscoreable; reason code
             absent; term-matrix grouping absent
Status     : open
Category   : Output Format
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : UC-T06 buddy blind test 2026-05-14; C2 (PFID) scored ~ (unverifiable) because
             no PFID field was present in the CES Quick Reference output. ces-nes
             modification: (a) when PFID field blank, emit a reason code (new surface /
             low traffic / catalog-era product) not generic "not identified in billing data";
             (b) for CES packages with 13-PFID term matrices, group output by tier and term.

CES Quick Reference output did not include a mandatory PFID field, making the C2 buddy
criterion unscoreable in blind tests. Wendy added a mandatory PFID field. ces-nes
recommended two modifications: (1) when the PFID field cannot be populated from billing
data, emit a specific reason code rather than the generic "not identified in billing data"
phrasing — options: new surface (no 7-day billing traffic), low-traffic surface (fewer than
3 distinct PFIDs), or catalog-era product (PFIDs not tracked in billing for this category);
(2) for CES packages with large PFID term matrices (4+ PFIDs per tier), group the CES
Terminal Payload table by tier with sub-header rows so the full term matrix per tier is
visible, not a flat undifferentiated PFID list.

Resolution : Wendy added PFID field; ces-nes reason code + grouped matrix modifications
             applied to SKILL.md 2026-05-14. Status: open pending verification in blind test.
Resolved   : —

---

## GAP-029
Title      : WAM Commerce PFID 970473 — Chain Step 1 merchandising match resolves to
             vnext-i18nox-tier4 (Intl) instead of wsb-vnext-tier4 (US); dual-series
             continuation check does not fire
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-14
Evidence   : UC-T04 blind eval 2026-05-14; PFID 970473 (WAM Commerce annual); Chain Step 1
             merchandising API primary match returned vnext-i18nox-tier4 (International/
             Titan Email variant); expected wsb-vnext-tier4 (US/M365 variant); analyst
             confirmed both series share PFID 970473. Buddy scored G1 incorrectly — expected
             path IS NES (both series are curated offers); buddy agent error corrected.

The Chain Step 1 dual-series continuation check is supposed to fire when the matched slug
"belongs to a known dual-series family." For PFID 970473, the merchandising API returned
vnext-i18nox-tier4 as the primary match. The continuation check did not fire, so the chain
stopped at vnext-i18nox (International/Titan) without checking for the sibling wsb-vnext
(US/M365) series.

Root cause: the continuation check relies on recognizing that the matched slug is from a
"known dual-series family." If the check's pattern detection does not cover all i18nox and
wsb-vnext slug variants by prefix string match, the check is bypassed. Additionally, when
market scope is US-only, the skill should prefer wsb-vnext-tier{N} over vnext-i18nox-tier{N}
regardless of merchandising API primary match order.

Fix direction: (1) ensure the dual-series continuation check triggers on any slug containing
"i18nox", "i18no365", or "wsb-vnext" as a substring — not only when the slug is in a
pre-configured known-family table; (2) add a US-scope preference rule: when geo scope is
confirmed US-only, select wsb-vnext-tier{N} as the primary champion and label vnext-i18nox
and vnext-i18no365 as "market excluded: international scope"; (3) the three-series table in
the Series Disambiguation block already covers this — ensure Chain Step 1 consults it before
declaring "chain resolved."

Resolution : —
Resolved   : —

---

## GAP-030
Title      : CES Tier column — product_pnl_subline_name null for M365/PMail PFIDs; fallback
             produces accounting category label instead of tier descriptor
Status     : open
Category   : Data Coverage Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : batch-test 2026-05-15; CMS-31421 (Email Essentials M365, dpp_precheck);
             6/6 C4 (Tier) failures; output produced "PMail" for all rows; expected "standalone"

The CES Terminal Payload Tier column is sourced from product_pnl_subline_name with fallback
to product_pnl_line_name. For Email Essentials M365 PFIDs (867688, 867694, 867696),
product_pnl_subline_name is null, so the skill falls back to product_pnl_line_name = "PMail"
— an accounting PNL category, not a tier descriptor. The golden-set expected value is
"standalone", reflecting the offer's geometry (Standalone: offers[] empty, prePurchaseKeyMap
absent).

Two open questions before any fix is applied:
1. Is the null subline_name pattern isolated to M365/PMail PFIDs, or does it affect a
   broader class of non-hosting standalone CES products?
2. When product_pnl_subline_name is not null, what values does it actually contain — are
   they meaningful tier labels (Economy, Deluxe, Business) or also accounting categories?

Until these are answered via a billing query, it is unknown whether a geometry-derived
fallback ("standalone" for Standalone geometry, "tier{N}" for bundle slugs) is the right
fix or whether a different source column should be used.

Fix direction (pending validation): insert a geometry-derived label as a second fallback
step between product_pnl_subline_name (null check) and product_pnl_line_name: standalone
geometry → "standalone"; bundle slug containing -tier{N} → "tier{N}"; other bundle →
"bundle". Apply product_pnl_line_name only as last resort with a [TIER-FALLBACK] warning
flag. Do not implement until billing query confirms the null pattern is systemic and
geometry-derived labels are the correct replacement.

Resolution : —
Resolved   : —

---

## GAP-031
Title      : CES-only surface registry missing — pre-launch NES check routes CES-only surfaces
             to NES when catalog entries exist but are not wired
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : batch-test 2026-05-15; CMS-31766 (slp_ssl / ssl-config surface); expected CES
             NET-NEW BUILD; actual output was NES Standalone (sslcert-managed-with-monitoring,
             offerId 28e5b730); G1 misclassification

The pre-launch NES check (GAP-008 fix) scans the NES catalog for active curated offers
matching the product when billing rows = 0. On slp_ssl / ssl-config, it found
sslcert-managed-with-monitoring and routed the output as NES Standalone. But slp_ssl is a
CES-only surface — the NES SSL offer exists in catalog but is NOT wired to this surface.
The pre-launch NES check has no registry of surfaces that are structurally CES-only, so it
cannot distinguish "catalog entry exists but not wired here" from a genuine pre-launch NES
case.

Open question: Which other surfaces are CES-only and would trigger this false-positive NES
routing? The registry needs to be built before the fix is applied. At minimum:
- slp_ssl / ssl-config: NES SSL catalog entries exist but surface runs CES only

Fix direction: add a CES-only surface registry to the pre-launch NES check. When the surface
is on the registry and a catalog match is found, emit a NES disclosure but proceed to the
CES chain. Do not implement until the registry has been validated — an incomplete registry
will still silently misroute unlisted surfaces.

Resolution : Partial — Option 2 surface label enrichment (2026-05-16) attaches the surface
             NES/CES classification from surface-vocab to the ROUTE line. For surfaces
             profiled as CES in the vocab (e.g. slp_ssl), the analyst sees "is a known
             CES-dominant surface" before any NES pre-launch routing fires, providing a
             transparency layer. Option 1 vocab advisory does NOT fire for CES-classified
             surfaces (it only fires when surface_nes_ces = NES or Mixed). The registry-
             based routing fix — blocking the pre-launch NES check for confirmed CES-only
             surfaces — is still pending.
Resolved   : —

---

## GAP-032
Title      : Bare ITC input stops at gate — no Surface Audit inference mode for ITC-first
             entries without product/path/operation signals
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : batch-test 2026-05-15; 3/5 cases (M365-OE-NOTEAMS-DPP-19, WAM-PREM-COMM-FOS-4ARM,
             CMS-31766) had input_type=itc with no product/PFID/path/term in the entry;
             all three stopped at the gate and produced zero output; 0/3 scoreable

When the only input is an ITC string with no product name, PFID, price target, or offer
operation signal, the six-dimension gate fires on Dimensions 0, 1, and 5 simultaneously.
The agent waits for analyst input and produces no output. For Surface Audit use cases —
"show me everything on this surface" — the gate is unnecessary friction.

Open question before implementing: Should the inference mode auto-proceed or prompt once?
Risk of fully auto-proceeding: a bare ITC might be an accidental incomplete entry rather
than a deliberate Surface Audit request.

Fix direction (pending decision): add a pre-gate ITC-first inference rule. If the entry
matches only an ITC pattern (slp_*, dpp_*, dlp_*, etc.) with no other signals, infer
Surface Audit mode, skip the gate, run full Path A discovery, and append a follow-up prompt
for ticket-creation inputs. Confirm approach before implementing — this touches the highest-
traffic entry path in the skill.

Resolution : —
Resolved   : —

---

## GAP-033
Title      : Rolled-back experiment variant naming — no heuristic distinguishes rollback
             artifacts from pre-launch NES offers in catalog
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-92 overnight analysis 2026-05-15; -wamba variants
             (wordpress-o365-forever-ssl-basic-wamba, wordpress-openexchange-forever-ssl-basic-wamba)
             found active=true in catalog (rev 1, March 2026) with zero billing in 7-day
             window; pre-launch NES check surfaces them as live candidates alongside
             genuinely pre-launch offers

The skill cannot distinguish three superficially identical states: (1) Pre-launch NES —
active in catalog, genuinely never wired/shipped; (2) Rolled-back experiment — was
shipping, experiment ended, billing fell to zero, active flag not updated after rollback;
(3) Decommissioned offer — active=true by oversight, not intentional.

The -wamba variants in AGIGROWTH-92 are experiment rollback artifacts. The pre-launch
NES check (GAP-008 fix) surfaces them as valid candidates alongside genuinely unreleased
offers, and the output gives no signal to distinguish them. An analyst who picks a
rolled-back variant as the clone source files a ticket for an inactive baseline.

Fix direction: after the pre-launch NES check returns active=true candidates with zero
billing, add a naming-convention heuristic scan. Slug patterns containing `-wamba`,
`-test`, `-rollback`, `-v2`, `-experiment`, `-hold` are common experiment-variant naming
conventions. Annotate these candidates: "Naming convention suggests experiment variant —
confirm live status before using as clone source." Do not suppress from candidate list;
annotate only. Also: rev=1 + zero billing = possibly rolled back or never wired; rev>1
+ zero billing = likely pre-launch revision.

Resolution : —
Resolved   : —

---

## GAP-034
Title      : ROW vs ROW+IN filter ambiguity — India excluded from default ROW but included
             in ROW+IN; no override instruction in skill
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-92 overnight analysis 2026-05-15; ticket explicitly stated
             "ROW & IN" (India included); skill default ROW filter not documented;
             standard GoDaddy ROW excludes India (NOT IN ('US','CA','AU','GB','IN'));
             ROW+IN override requires NOT IN ('US','CA','AU','GB') — India removed from
             exclusion; skill has no instruction covering this distinction

The Dimension 3 market gate distinguishes US, DEM, ROW, and All Markets, but does not
document: (1) the exact WHERE clause for "ROW" — default excludes US + DEM + India;
(2) what "ROW+IN" means — India included, DEM still excluded; (3) that "ROW & IN",
"ROW including India", or "India + ROW" in a Jira ticket is a non-default override
requiring a different filter. Without this, an agent running a ROW+IN ticket silently
uses the default ROW filter, understating geographic scope. India is a high-volume
market — a missed India scope means the EP ticket covers only part of the intended
geography.

Fix direction: add a ROW filter definition table to Dimension 3:

  US only   : country_code = 'US'
  DEM       : country_code IN ('CA','AU','GB')
  ROW       : country_code NOT IN ('US','CA','AU','GB','IN')
  ROW+IN    : country_code NOT IN ('US','CA','AU','GB')
  All mkts  : (no country filter)

Add pre-parse rule: if ticket text contains "ROW & IN", "ROW and IN", "ROW including
India", "India + ROW", or "ROW+IN", resolve D3 = ROW+IN and use the corresponding filter.

Resolution : —
Resolved   : —

---

## GAP-035
Title      : catalog_query_get_offers file size — M365 plan list (129K tokens) exceeds
             Read tool limit; agents error or stall with no fallback instruction
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-161 overnight analysis 2026-05-15; agent read attempt on
             mcp-catalog-mcp-dev-catalog_query_get_offers result containing 129,226 tokens
             (124 M365 plans); Read tool limit = 25K tokens; agent errored on all attempts;
             required spawning replacement agent with Bash grep workaround; original
             agent stalled mid-run

When catalog_query_get_offers is called with tags=["m365"] or other broad parameters,
the result file can contain 124+ plans at ~1K tokens each, totaling 129K+ tokens. The
Read tool 25K limit causes an error on every read attempt. The skill has no instruction
for this case. Agents either retry the same failing read (stalling the run) or abandon
the plan scan entirely (missing valid champions). Both failure modes confirmed in
AGIGROWTH-161. This is high-frequency risk: all dpp_precheck M365 tickets and all
Microsoft 365 email tickets route here via Chain Step 3 known-tag mapping.

Fix direction: add an explicit file-size handling instruction to Chain Step 3 immediately
after the catalog_query_get_offers call. For products known to produce large result sets
(m365 → 124+ plans, sslcert → ~40+ plans), do NOT attempt to Read the full result file.
Use Bash grep for specific plan name keywords from the request:

  grep -o '"planName":"[^"]*"' {result_file} | grep -i "{keyword}"

For these tags, always use the Bash grep path. Read only when the estimated plan count
is small (< 20 plans, e.g. titanemail, wam, professional-email).

Resolution : —
Resolved   : —

---

## GAP-036
Title      : Post-creation audit mode absent — skill always produces a "create this offer"
             payload even when the EP ticket has already been deployed
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-161 overnight analysis 2026-05-15; EP-87620 deployed 2026-04-29;
             challenger microsoftemail-onlineessentialsnoteams-discount-365af1f1cb
             confirmed active in catalog with 261 orders/7d via discount code; skill
             produced a "create this offer" payload as if the offer did not yet exist;
             no output mode for confirming deployed offer parameters

When a Jira ticket references an EP ticket already deployed, the task is
confirmation/audit — verify parameters match the spec, confirm billing traffic, flag
discrepancies — not a new "create this offer" payload. The skill has one output mode:
pre-creation Quick Reference. In AGIGROWTH-161, the agent correctly identified the live
challenger via the discount code in billing but framed all output as if the offer was
still to be built, making the output misleading and the distinction between "what to
build" vs "what was already built" invisible.

Fix direction: add an EP-deployed signal detector to Entry Option 1 Step 3. If the
ticket body, comments, or linked tickets contain "EP-XXXXX deployed", "EP-XXXXX merged",
"went live on [date]", or "launched [date]", set audit_mode = true. In audit mode:
(1) look up the deployed offer via catalog MCP; (2) confirm active=true and retrieve
plan/pricing; (3) confirm billing traffic via discount_code or package_id query on
offer_pulse_experiment for last 7 days; (4) output a DEPLOYMENT AUDIT block instead of
Quick Reference. The DEPLOYMENT AUDIT block confirms: slug, offer ID, active status,
billing volume, and whether parameters match the ticket spec. Flag any discrepancy as
ACTION REQUIRED.

Resolution : —
Resolved   : —

---

## GAP-037
Title      : Discount code expiry not proactively calculated — imminent expirations
             undetected until offer surface goes dark
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-161 overnight analysis 2026-05-15; discount code 365AF1F1CB found
             in billing; get_curated_offer returns endDate "2026-06-01" for associated
             offer; 17 days from run date (2026-05-15); skill produced output with no
             mention of imminent expiry

When the champion curated offer is identified, the skill does not check the `endDate`
field. A discount code or time-limited offer expiring in under 30 days represents a
production risk: if the new experiment does not deploy before the incumbent expires, the
surface will have no active offer for the promotion period. For AGIGROWTH-161, the
challenger microsoftemail-onlineessentialsnoteams-discount-365af1f1cb expires 2026-06-01
— 17 days from the run date — an urgent deployment dependency invisible in the output.

Fix direction: after calling get_curated_offer on the identified champion, check the
`endDate` field. If `endDate` is within 30 days of the current date, emit a warning
prominently in the Quick Reference output (not only in the validation block):

  ⚠ EXPIRY ALERT: [slug] expires [date] — [N] days from today.
  New experiment must deploy before this date to avoid surface gap.

If `endDate` is within 7 days, escalate to hard blocker status. Applies to both the
incumbent champion (being replaced) and the new challenger if it has an end date.

Resolution : —
Resolved   : —

---

## GAP-038
Title      : vnext-i18nox-*-precheck slug naming inconsistency — precheck-suffixed variants
             don't exist for i18n series; keyword seed "precheck" silently misses base slugs
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-186 overnight analysis 2026-05-15; expected packages
             vnext-i18nox-tier1-precheck, vnext-i18nox-tier3-precheck,
             vnext-i18nox-tier4-precheck NOT FOUND in catalog; base slugs
             vnext-i18nox-tier1/3/4 DO exist; wsb-vnext series uses -precheck suffix
             at dpp_precheck (confirmed); i18n series uses base slugs on ALL surfaces

The dpp_precheck surface uses two distinct slug naming conventions:
- wsb-vnext series: surface-specific suffix appended (wsb-vnext-tier3-precheck)
- vnext-i18nox / vnext-i18no365 series: NO suffix — base slug used on all surfaces

The Chain Step 2 keyword seed table for dpp_precheck includes "precheck" as a required
seed. This correctly surfaces wsb-vnext variants but produces zero matches for i18nox
base slugs (no "precheck" substring). An analyst searching for i18n variants at
dpp_precheck gets a partial candidate table that silently omits the entire i18n family.
Confirmed by exhausting the catalog search in AGIGROWTH-186: 3 of 7 expected packages
NOT FOUND via precheck-suffixed slug names; base slug search confirmed they exist.
This naming inconsistency is undocumented in SKILL.md.

Fix direction: add a naming convention footnote to the dpp_precheck surface keyword seed
entry: "wsb-vnext series uses -precheck suffix; vnext-i18nox and vnext-i18no365 series
use BASE slugs on dpp_precheck — do not filter by 'precheck' when searching for i18n
family slugs." Add a secondary seed pass for i18n series at dpp_precheck: after the
"precheck"-seeded ID scan, run a second scan with seeds ["i18nox", "i18no365"] WITHOUT
the "precheck" filter. Union the results.

Resolution : —
Resolved   : —

---

## GAP-039
Title      : Strategic Partnerships products (TrustedSite, Norton, SiteLock) have no
             catalog tags — CES Chain Step 3 blind spot; chain exhaustion produces no
             actionable guidance
Status     : open
Category   : Data Coverage Gap
Skill      : offer-pulse
Added      : 2026-05-15
Evidence   : AGIGROWTH-186 overnight analysis 2026-05-15; TrustedSite has NO existing
             curated offer in catalog (confirmed via Chain Steps 1 and 2 exhaustion);
             CES Chain Step 3 known-tag mapping table does not include TrustedSite,
             Norton, SiteLock, or any Strategic Partnerships product; Step 3 cannot
             run for these products; result = silent chain exhaustion with no guidance

CES Chain Step 3 relies on a product-name → catalog-tag mapping table. Strategic
Partnerships products — TrustedSite, Norton Security, SiteLock — have no stable catalog
tags: they are third-party add-ons without a dedicated NES product ontology. When a
ticket targets one of these products and the CES chain reaches Step 3, no tag can be
derived and Step 3 cannot run.

For AGIGROWTH-186, the correct answer was "TrustedSite has no existing curated offer —
two-step operation required: (1) create a standalone TrustedSite offer, (2) add it as
an add-on component to 7 existing WAM precheck bundles." But the skill cannot distinguish
"no tag available" from "no offer exists" — both produce no catalog output and no
actionable output for the analyst.

These products are always CES add-ons; running the pre-launch NES check for them is
wasted work and risks false-positive NES routing.

Fix direction: add Strategic Partnerships products to the pre-launch NES check early-exit
list (alongside the CES-only surface registry from GAP-031). When the input product is
TrustedSite, Norton, SiteLock, or another recognized Strategic Partnerships brand:
(1) Skip the NES catalog scan — always CES add-ons
(2) Run CES chain Steps 1 and 2 with name-based keyword seeds only
(3) If chain exhausts, emit explicitly:
    "NET-NEW BUILD required — [product] is a Strategic Partnerships add-on with no
    existing curated offer. Two-step operation: create standalone [product] offer, then
    add to target bundle(s). Confirm with @sparmar before filing EP ticket."

Resolution : —
Resolved   : —

---

## GAP-040
Title      : Ghost IDs and CES term aliases counted in NES% — inflated NES% triggers false
             NES routing on mixed or CES-dominant surfaces
Status     : resolved
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-16
Evidence   : ces-nes architecture review; TK-002, TK-003, TK-004. Ghost IDs (nes-*, offer-*
             prefix slugs) and CES term aliases (_NNNmo/_NNNyr suffix slugs) both appear as
             non-null package_id values in billing/CLN data. The Step A2 NES% calculation
             counted these as NES evidence, inflating the percentage and potentially routing
             CES-dominant surfaces into the NES path.

When ghost IDs or CES term aliases appear as non-null package_id values in billing data,
the Step A2 NES% calculation incorrectly counts them as NES volume. This inflates NES%
and can force a surface into the NES path (A2a catalog calls) when the true NES-eligible
volume is zero or lower than the threshold.

Three slug types to exclude from NES% calculation:
1. CES term aliases — slugs ending in _NNNmo or _NNNyr (e.g. wsb_vnext_tier2_060mo).
   These are CES merchandising API aliases encoding term overrides. NOT NES slugs.
2. Ghost IDs by prefix — slugs starting with offer-. Consistently unresolvable.
   NOTE: nes- prefix behavior updated 2026-05-20 — see below.
3. Known ghost list — nes-wss-tier0/1/2-nortonsmb-standardfreetrial family.
   Same behavior as prefix-matched ghosts.

Resolution : Option 4 pre-classification filter added to Step A2a (2026-05-16). Before any
             get_curated_offer call, all package_id values are classified as CES term aliases,
             ghost IDs (prefix + known list), or valid NES slugs. NES% is recomputed using
             only valid NES slugs. Excluded slugs appear in the Flags table.
             Cross-reference TK-002/003/004.

             Updated 2026-05-20 (GAP-042 investigation): nes- prefix reclassified. The page
             emits nes-{slug} as a pkgid field; the catalog stores the clean {slug}. SKILL.md
             updated to strip the nes- prefix and retry catalog lookup before classifying as
             ghost. nes-cpanel-set-1-economy-ssl-365-wss-xtra removed from known ghost list
             — it is a valid live offer when prefix is stripped. nes-wss-tier0/1/2-nortonsmb-*
             remain in the known ghost list (unconfirmed in catalog).
Resolved   : 2026-05-16

---

## GAP-041
Title      : pricing-ticket outputs no UPP-specific warnings — wrong implementation path
             and silent path exclusions
Status     : resolved
Category   : Process Gap
Skill      : pricing-ticket
Added      : 2026-05-17
Evidence   : 2026-03-12 Hivemind UPP experiment walkthrough transcript (TK-040, TK-042)

When an analyst enters a `upp_*` ITC, the skill runs Blast Radius Mode and produces a "CES
Offer Candidates" table pointing to the merchandising API as the discount configuration path.
This is incorrect for UPP surfaces. Three critical facts are missing from the output:
(1) UPP discount experiments are configured via Hivemind cohort JSON (DISC-##### codes
from the pricing team), NOT by updating the CES package in the merchandising API. The CES
Offer Candidates section implies the analyst should configure the discount in the merch API
— which is the wrong implementation path entirely.
(2) BMAT (Bill Me After Trial) customers CANNOT receive UPP discount codes due to an ecom
billing agent limitation. Experiments silently do nothing for this segment with no error.
(3) Direct-to-paid (new purchase flow) customers are also excluded from UPP discount logic.
Fix direction: Add UPP surface detection in the Flags section of Blast Radius Mode output:
when any ITC in B1 results matches LIKE 'upp_%', emit a UPP WARNING block:
- Implementation path: Hivemind cohort JSON (not merchandising API config)
- Path exclusions: BMAT customers and direct-to-paid customers receive no discount
- Suppress or relabel the "CES Offer Candidates" merchandising lookup to avoid implying
  it is the actionable configuration step for UPP discounts (slug lookup still useful for
  PFID identification, but should NOT be presented as the discount configuration target)
Related    : TK-040, TK-042

Resolution : UPP surface detection added to pricing-ticket: UPP exception in B2 CES
             lookup, UPP warning flag in Blast Radius Flags table, UPP Hivemind
             Configuration output section with cohort JSON template, path exclusions,
             and test→prod workflow. CES Offer Candidates table excludes UPP ITCs.
Resolved   : 2026-05-17

---

## GAP-042
Title      : NES event schema mismatch — pf_id_package_details_v1 cannot join new NES events
             because productId changed from integer PFID to customer UUID path format
Status     : open
Category   : Data Coverage Gap
Skill      : offer-pulse
Added      : 2026-05-20
Updated    : 2026-05-20 (root cause + ITC attribution mechanics + doc sources)
Evidence   : AGIGROWTH-228 investigation 2026-05-20. cpanel-set-1-economy-ssl-365-wss-xtra
             confirmed live via CMT page inspection (Tony Hill, $5.99/mo × 36 = $215.64,
             PFID 1338734). Direct queries of gd_traffic_mart.traffic_page_event,
             pricing_experiment_dev.pf_id_package_details_v1, and
             pricing_experiment_dev.offer_pulse_experiment confirm the root cause.

Root cause (confirmed):
New NES add-to-cart events emitted from /configure/traffic pages (dlp_hosting ITC) use a
different productId format than old CES events:

  Old CES format (/configure, slp_hosting_4GH):
    productId = integer PFID (e.g. "1338734")
    package_json = [{"id": "cpanel-set-1-economy-365", ...}]   ← no nes- prefix
    → captured by pf_id_package_details_v1, flows into offer_pulse_experiment

  New NES format (/configure/traffic, dlp_hosting):
    productId = customer UUID path (e.g. "/customers/31430a42-6f4f-4646-...")
    package_json = [{"id": "nes-cpanel-set-1-economy-ssl-365-wss-xtra", ...}]
    → NOT captured — pf_id_package_details_v1 joins on integer PFID and finds no match

Volume (90 days, gd_traffic_mart.traffic_page_event):
  nes-cpanel-set-1-economy-ssl-365-wss-xtra: 6,018 add-to-cart events
    - US (/configure/traffic): 1,534 events
    - UK (/en-uk/): 777, CA (/en-ca/): 208, AU (/en-au/): 146, and more
    - ALL under dlp_hosting ITC
  cpanel-set-1-economy-365 (old slug): 12 US events, all on legacy /configure path
  cpanel-set-1-economy-ox (old slug): India only, /en-in/configure

Result in pf_id_package_details_v1 (all-time):
  slp_hosting_4GH + cpanel-set-1-economy-ox: 2 events (India, old format)
  slp_hosting_4GH + cpanel-set-1-economy-365: 1 event (old format)
  dlp_hosting: 0 rows — all 6,018 NES events invisible due to UUID productId

Result in offer_pulse_experiment:
  slp_hosting_4gh: old slugs only (ox=361, 365=274 transactions joined from billing)
  dlp_hosting: 11 billing transactions with NULL package_id (no lookup match)
  nes-cpanel-set-1-economy-ssl-365-wss-xtra: never appears

Secondary blocker (GAP-040):
  Even if the pipeline were fixed, SKILL.md ghost ID filter discards all nes- prefixed
  slugs before catalog lookup. Both the pipeline fix and the ghost ID fix are required.

Resolves Daniel Hill's two suspicions (Teams thread 2026-05-20):
  Suspicion 1 (bad package_id data): Confirmed. The pipeline correctly parses integer
    PFID events but was never updated to handle UUID-path productId events from the new
    NES page format. The data exists in traffic_page_event (6K events) — it just doesn't
    flow downstream.
  Suspicion 2 (wrong ITC): Confirmed. dlp_hosting IS the correct NES surface (1,534 US
    events with the live slug). slp_hosting_4GH is a legacy CES path still emitting old
    slugs. offer-pulse was looking at the wrong ITC for the NES offer.

ITC attribution mechanics — why slp_hosting_4gh is correct but empty for NES:
  The SLP at /hosting/web-hosting uses slp_hosting_4gh as its ITC on links and CTAs.
  But the add-to-cart event is fired from the NES configure page (/configure/traffic),
  not the SLP. The configure page emits its own ITC: dlp_hosting. Per the ITC funnel
  design spec, ITC on an add-to-cart event belongs to the page that fires the event
  (the configure page), not the referrer (the SLP). slp_hosting_4gh is the entry
  surface; dlp_hosting is the add-to-cart surface. These are sequential funnel steps.

  Old CES path: the add-to-cart fired on or adjacent to the SLP (/configure) →
    slp_hosting_4GH appears in pf_id_package_details_v1.
  New NES path: the add-to-cart fires at /configure/traffic with ITC dlp_hosting →
    slp_hosting_4gh gets no events; dlp_hosting gets all 6,018 NES events.

  This is the same phenomenon the "Offer Pulse - In Progress" Confluence page (BI space,
  updated 2026-05-20) documents as: "Cart tracking ≠ purchase tracking." That page lists
  it as a known current challenge with the pipeline, separate from the UUID productId
  issue.

Documentation (2026-05-20):
  (1) ITC Funnel Instrumentation & Reporting (BI space, updated 2026-05-19):
      "ITC identifies the surface where the customer can add a product to cart.
       add_to_cart event Owner/Data Producer: team who owns the CTA surface."
      https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/3134915218
  (2) Pricing Experiment — Offer Pulse — In Progress (BI space, updated 2026-05-20):
      "Current Challenges: Tracking Code Mismatches — Cart tracking ≠ purchase tracking."
      https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4394484952

Ecomm team context (2026-05-20 meeting):
- Tony Hill: package slug is in package_json column; suggested table owner could surface
  it as a standalone field
- Saritha Bhandarkar: confirmed ecomm does not persist product package ID as a discrete
  field in their system
- Harsh Kapoor: their bundle classification works at subscription/transaction level
  (completed orders), not add-to-cart events

Fix direction:
(1) Short term — add cpanel-set-1-economy-ssl-365-wss-xtra to a known-override registry
    for dlp_hosting + 3-year + WH Economy, bypassing offer_pulse_experiment entirely.
(2) Pipeline fix — update pf_id_package_details_v1 to extract PFID from the UUID path
    format in product_json, or join on a different field that remains stable across event
    formats. This unblocks all NES products on the new page format, not just WH Economy.
(3) Ghost ID fix (required alongside pipeline fix) — update SKILL.md to strip the nes-
    prefix before catalog lookup (see GAP-040). Without this, a fixed pipeline would still
    produce discarded slugs.

Resolution : —
Resolved   : —

---

## GAP-043
Title      : offer-pulse → pricing-ticket handoff: ghost IDs and V3 offers need graceful
             fallback — Entry Option 0 must not attempt catalog resolution on inherited context
Status     : open
Category   : Skill Gap
Skill      : pricing-ticket
Added      : 2026-05-22
Evidence   : ces-nes architectural review 2026-05-22; pre-implementation check before
             Entry Option 0 (post-offer-pulse handoff) is built

When the offer-pulse → pricing-ticket handoff is implemented (Entry Option 0), the inherited
package_id may be a ghost ID (NOT FOUND in catalog even after nes- prefix strip) or a V3
apiVersion record (offerIds[] UUIDs not resolvable via V2 endpoint). If Entry Option 0 attempts
catalog resolution on inherited context, it will fail silently or produce a misleading NOT FOUND.

Three cases to handle safely:
1. Ghost package_id (nes-wss-*, offer-* prefix, confirmed unresolvable) — carry the slug as
   display context only; do not call get_curated_offer; emit: "Package ID {slug} is a known
   ghost — catalog resolution skipped. Proceeding with PFID list inherited from offer-pulse."
2. V3 apiVersion offer — get_curated_offer returns a record but offerIds[] are internal UUIDs
   that return NOT FOUND via get_offer_definition_by_id. Entry Option 0 only needs the slug
   and plan name for the pricing ticket; do not attempt component decomposition for V3 records.
3. CES surface (package_id null in inherited context) — no catalog call needed; use PFID list
   directly. Do not query "WHERE package_id = {champion}" for discount code lookup — use
   item_tracking_code + pf_id filter against offer_pulse_experiment instead.

Fix direction: build these three cases into Entry Option 0 explicitly. Each is a routing
decision at the top of Entry Option 0 before any catalog calls. V3 detection = check apiVersion
field from get_curated_offer response; ghost detection = NOT FOUND after nes- strip; CES =
package_id null in inherited context.

Resolution : —
Resolved   : —

---

## GAP-044
Title      : Surface data gate bypassed before path selection — Jira ticket chain shortcuts
             Step A1, so surface type is never confirmed from billing data
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-28
Evidence   : EP-89137 Norton precheck case (2026-05-27). Entry via Jira ticket with
             dpp_precheck as target surface. Execution followed EP-89137 → AGIGROWTH-79 →
             EP-84398 → EP-75969 to find source curated offers, then went directly to
             catalog lookup. Step A1 surface audit on dpp_precheck never ran. Surface
             data shows 100% CES (NULL package_ids, 198K orders). If Step A1 had run
             first, surface would have been typed as CES before any catalog path selection.

The HARD CONSTRAINT "champion is determined from data and the catalog MCP only" implies
Step A1 must run before catalog lookups — but execution can shortcut it by using offers
identified in the Jira ticket chain as the anchor for get_curated_offer calls. When the
ticket names source curated offers (or links to prior EP tickets containing them), there
is no explicit gate preventing those slugs from being used as the catalog anchor before
billing data is checked.

Impact: incorrect path selection when the Jira ticket chain points to NES offers that are
not live on the target surface. The skill will produce NES output for a CES-dominant
surface, and the surface type disclosure will be absent from the output.

Fix direction: add an explicit guard in Entry Option 1 after the multi-arm detection step:
"Never use curated offer slugs identified from linked tickets as the anchor for catalog
lookup before Step A1 runs. Extract slug context from the ticket for orientation only.
The surface type gate (Step A2 NES% calculation) must complete before any catalog path
is selected. Only slugs confirmed in billing data (Step A1) or the pre-launch NES check
serve as catalog anchors." This makes the existing HARD CONSTRAINT explicit at the Entry
Option 1 step where the shortcut occurs.

Resolution : —
Resolved   : —

---

## GAP-045
Title      : Source-surface ≠ target-surface cloning unhandled — when ticket requests
             cloning NES offers from FOS for deployment on precheck, skill has no
             separate source/target surface path
Status     : open
Category   : Skill Gap
Skill      : offer-pulse
Added      : 2026-05-28
Evidence   : EP-89137 Norton precheck case (2026-05-27); /ces-nes architectural review
             2026-05-28 confirmed merch API is CES-only — cannot surface NES curated
             offers under any PFID query.

Original framing (pre /ces-nes review): "add PFID → merch API lookup in parallel with
catalog path when surface is CES/ambiguous." /ces-nes verdict: the V1 merch API
(https://merchandising.api.godaddy.com/v1/packages) contains CES packages only. Querying
it with the champion MWP PFID would return CES packages on that surface — confirming
CES type — but would never surface wp-o365-forever-*-nortonsmb-standardfreetrial.
These are catalog entries, not merch packages.

The real gap: the skill assumes source surface = target surface in all clone operations.
EP-89137 is a "clone NES offers from FOS for deployment on precheck" ticket. The correct
source (wp-o365-forever-*-nortonsmb-standardfreetrial) is confirmed on slp_wordpress
(FOS). The target is dpp_precheck (CES-dominant). The skill has no instruction for this
pattern — it only knows how to find the champion on the target surface, not on a separate
source surface named in the ticket.

Fix direction: in Entry Option 1, after ticket field extraction, check whether the ticket
identifies a source surface distinct from the target surface (signals: "clone from FOS",
"clone existing [product] offer", "extend to precheck", "bring to [target surface]").
If source ≠ target:
1. Run Step A1 on SOURCE surface to find the NES champion there.
2. Run Step A1 separately on TARGET surface to classify it (NES/CES/pre-launch).
3. Emit separate surface blocks: "Source Surface: {ITC} — champion found" and
   "Target Surface: {ITC} — CES-dominant / pre-launch / etc."
4. The clone source is from the SOURCE surface, not the target surface.
Do NOT attempt merch API lookup to find NES source offers — /ces-nes confirmed this
is architecturally invalid. NES offers are in catalog only.
Related    : GAP-044, TK-001

Resolution : —
Resolved   : —

---
