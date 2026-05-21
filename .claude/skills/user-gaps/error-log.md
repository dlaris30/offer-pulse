# Offer Pulse — Human Error Log

## HE-001
Pattern    : Product name or ITC used as entry instead of Jira ticket key
Status     : active
Category   : Context Error
Frequency  : Very Frequent (>50%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : All 7 logged runs used product-name-first or ITC-first entry; zero used
             Entry Option 1 (ticket key) despite most runs having a source ticket.
             Confirmed by GAP-003.

**What the analyst does:**
Passes a product name ("WAM Premium"), a PFID, or an ITC as the entry point even when
a Jira ticket for the work exists. The ticket-first path auto-extracts target price,
discount code requirements, offers being replaced, and multi-arm flags — none of which
are available when the analyst starts from a product name. The analyst often supplies
these fields manually later, or omits them entirely.

**How to detect:**
- Entry type in the use-case log = "Product name" or "PFID-first" or "ITC-first"
- Run notes mention a Jira ticket in passing (e.g. "AGIGROWTH-51") without it being
  the entry point
- Analyst asks about target price, replacement offers, or discount codes mid-run that
  would have been auto-extracted from a ticket
- Output fields "Target price", "Discount code", "Replace" are blank or "not stated"
  but the Jira ticket (if fetched) contains them

**What to say:**
Ask: "Do you have a Jira ticket for this work? Passing the ticket key first lets me
extract target price, replacement scope, discount codes, and detect multi-arm experiments
automatically." This is not a skill defect — the analyst simply hasn't adopted Entry
Option 1 as the default starting point.

---

## HE-002
Pattern    : ITC alias used instead of actual ITC code
Status     : active
Category   : Input Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : "FOS" / "front of site" / "precheck" used in conversation context without
             full ITC code. Memory note: FOS = slp_* surfaces, not dpp_* (dpp_* = domains
             purchase path, not front of site).

**What the analyst does:**
Uses a business shorthand or internal nickname for a surface instead of the actual ITC
value. Common aliases:
- "FOS" or "front of site" → means slp_* (sales landing page) surfaces
- "precheck" → means dpp_precheck (domain purchase path precheck upsell)
- "domains FOS" → ambiguous; could mean slp_rstdstore or dpp_*
- "checkout" → could mean dpp_checkout, upp_*, or a CES upsell — not a single ITC

The alias may be technically resolvable, but it introduces ambiguity and may match the
wrong surface if the skill guesses rather than asks.

Known aliases and their resolutions:
- "FOS" or "front of site" → `slp_*` (Sales Landing Page surfaces)
- "domain path" or "domain purchase path" → `dpp_*` surfaces
- "precheck" (without prefix) → `dpp_precheck`
- "my account" → `mya_*` surfaces
- "domain control center" or "DCC" → `dcc_*` surfaces
- "domain landing page" or "DLP" → `dlp_*` surfaces
- "checkout" → ambiguous; could be `dpp_checkout`, `upp_*`, or a CES upsell — ask
- "domains FOS" → ambiguous; could be `slp_rstdstore` or `dpp_*` — ask
- "WAM FOS" or "WSB FOS" → `slp_wsb_*` (WAM/Website Builder Sales Landing Page surfaces)
- "vnext surface" → `slp_wsb_*` (vnext products live on slp_wsb_* ITCs)

**How to detect:**
- Entry value contains "FOS", "front of site", "domain path", "precheck" without the
  "dpp_" prefix, "checkout" without a specific ITC code, "my account", "DCC", "DLP",
  or "domains" alone
- Entry value has no underscore where an ITC code should appear
- Output selects an ITC that the analyst later disputes

**What to say:**
Confirm the actual ITC code. Ask: "Can you confirm the ITC value from billing or the
Jira ticket? Common mappings: FOS = slp_* (e.g. slp_wsb_* for WAM); domain path =
dpp_*; precheck = dpp_precheck; my account = mya_*." Not a skill defect — the skill
needs a real ITC to query billing.

**Skill coverage note (2026-05-14):** The Surface Name → ITC Map in SKILL.md now
explicitly covers "FOS / front of site" → `LIKE 'slp_%'` and "precheck (without
dpp_ prefix)" → `dpp_precheck`. The skill will no longer mis-route these two aliases.
This error pattern remains active for other aliases not yet in the table (e.g.
"checkout", "domains FOS", bare "domains").

**Cross-reference (2026-05-14):** See HE-014 for the specific "WAM vnext" / "vnext surface"
alias pattern, which maps to slp_wsb_* ITC surfaces.

---

## HE-003
Pattern    : Out-of-scope ticket type run through offer-pulse
Status     : active
Category   : Scope Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : AGIGROWTH-244 (rebate/cashback), AGIGROWTH-55 (config toggle) confirmed by
             GAP-006 evidence. Ticket-type classifier added to SKILL.md Step Entry Option 1
             step 3 as a result — but the root cause is analyst scope error, not a skill gap.

**What the analyst does:**
Runs offer-pulse on a ticket that requires no EP offer creation:
- Rebate / cashback tickets (e.g. "apply a $5 rebate after purchase")
- Config toggle / feature flag tickets (e.g. "enable trust badge on checkout")
- Reporting-only tickets (analytics change, no pricing impact)
- Legal / compliance tickets (no offer structure change)

The analyst may not realize the distinction between "offer creation" and "configuration
change" tickets, or may be using offer-pulse to understand the surface even when no
ticket output is needed.

**How to detect:**
- Jira ticket description contains "rebate", "cashback", "toggle", "feature flag",
  "enable/disable", "config change", "A/B test measurement only", "compliance"
- No price change, no new bundle, no discount code in the ticket
- The early-exit classifier in Entry Option 1 fires
- Analyst seems surprised that no EP ticket is produced

**What to say:**
"This ticket appears to be a [rebate/config toggle/reporting] ticket — no EP offer
ticket is required. Confirm and close." Not a skill defect; the early-exit classifier
is working as intended. The underlying cause is the analyst not screening ticket type
before invoking the skill.

---

## HE-004
Pattern    : Expecting NES output from a known-CES surface
Status     : active
Category   : Expectation Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Multiple CES runs in use-case log; memory file on CES path transparency
             confirms analysts frequently expect NES-style curated offer output on CES
             surfaces. NES curated offers exist only on domain surfaces + slp_hosting_4gh.

**What the analyst does:**
Asks for a "curated offer ID", "NES bundle", or "package_id" for a surface that is
100% CES in billing data. The analyst may have worked with NES surfaces previously and
expect the same output format. They may also have been told a "package name" exists when
in fact the surface is pre-migration CES.

**How to detect:**
- Run result shows NES% = 0% / CES = 100%
- Analyst pushes back on the CES path output or asks "where is the curated offer ID?"
- Analyst asks why no package was found
- Surface ITC is slp_wsb_*, slp_rstdstore, or other confirmed-CES surface (not
  slp_hosting_4gh or slp_wordpress which are NES-capable)

**What to say:**
"This surface is architecturally CES — curated offer IDs do not exist here. The output
correctly follows the CES path (merchandising package + PFID list). If you expected NES
output, confirm the ITC with engineering — it may need NES migration before a curated
offer can be created." Not a skill defect; the NES curated offer landscape memory
(project_nes_curated_offer_landscape.md) documents which surfaces are NES-capable.

**Cross-reference (2026-05-14):** See HE-014 — analysts who describe the product as
"vnext" or "WAM vnext" are frequently in this situation (expecting NES output for a
known-CES-generation product family).

**Skill coverage note (2026-05-16):** Option 2 surface label enrichment now annotates the
ROUTE line and CES-ONLY SURFACE disclosure with the surface's NES/CES classification from
the surface vocabulary. The analyst will see `ROUTE: CES Package — dpp_precheck (Domain
Purchase Path — Pre-Check) is a known CES-dominant surface` as the first visible output
line, before any catalog calls. This proactively surfaces the architecture reality without
waiting for the analyst to reach the CES output and push back.

---

## HE-005
Pattern    : Term stated as product tier name, not billing cycle
Status     : active
Category   : Input Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Term gate fires in ~91% of runs (GAP-015). A subset of those cases (exact
             frequency unquantified) involve analysts responding to the Term gate question
             with a product tier name.

**What the analyst does:**
When the Term gate fires and asks "What billing cycle?", the analyst answers with a
product tier or plan level instead:
- "Basic" (should be "annual" or "monthly")
- "Premium" (should be "1-year" or "3-year")
- "Starter" (not a billing cycle)
- "Standard" (not a billing cycle)

The tier name is meaningless to the billing query — only the cycle (annual/monthly/
quarterly) is used to filter product_term_unit_desc.

**How to detect:**
- Analyst response to the Term gate contains a product tier word with no billing cycle
  word ("Basic" alone, "Premium" alone, no "year", "month", "annual", "monthly",
  "quarterly", "yr", "mo")
- Downstream billing query returns zero rows because term filter finds no matching
  product_term_unit_desc value

**What to say:**
"The billing term I need is the cycle — annual, monthly, or quarterly. The product tier
(Basic, Premium, etc.) is determined by the PFID. For example: 'annual' means the
customer pays once per year." Re-ask the Term gate question with examples. Not a skill
defect.

---

## HE-006
Pattern    : Single-arm entry for a confirmed multi-arm experiment
Status     : active
Category   : Context Error
Frequency  : Rare (<5%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : Multi-arm experiment context confirmed in AGIGROWTH-161 pulse-audit analysis
             (2026-05-14). Multi-arm detection added to SKILL.md as Entry Option 1 step 4
             — however, this only fires when the Jira ticket is fetched. Analysts who use
             product-name-first entry (HE-001) bypass multi-arm detection entirely.

**What the analyst does:**
Provides one treatment price point or one PFID set for a ticket that actually describes
two or more experiment arms with different price points or bundle compositions. The second
(or third) arm is only discovered when the analyst is explicitly asked. This leads to a
single-arm output when a two-arm EP ticket is needed.

**How to detect:**
- Jira ticket (if fetched) contains multiple price points ("$9.99 arm" and "$12.99 arm")
  or "control vs. treatment" framing
- Entry value lists only one price/SKU but the ticket has multiple
- Output shows one treatment package when the analyst later describes two
- Analyst asks about "the other arm" after the output is produced

**What to say:**
Ask: "Does this experiment have multiple arms with different price points or bundle
compositions? If so, can you describe each arm separately?" The multi-arm detection in
Entry Option 1 would have caught this automatically — see HE-001 about why ticket-first
entry is preferred. This is Mixed — the skill has a gap when multi-arm detection is
bypassed (HE-001 is a prerequisite failure).

---

## HE-007
Pattern    : Expecting billing-backed output for a pre-launch product
Status     : active
Category   : Expectation Error
Frequency  : Rare (<5%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : GAP-008 (pre-launch NES surface looks identical to CES). Skill now has a
             pre-launch NES check, but this depends on catalog having an active=true entry.
             The underlying analyst error is running offer-pulse on a product before it has
             any billing history.

**What the analyst does:**
Runs offer-pulse on a product that has not launched yet (zero billing rows across all
surfaces). Expects to see package data or PFID history from billing. Gets "no results"
and interprets it as a skill failure or CES routing.

**How to detect:**
- All billing queries return zero rows for the queried product
- Product exists in NES catalog with active=true but launch date is in the future
- Jira ticket has a launch-gating milestone or contains "pre-launch", "launch plan",
  "not yet live"
- Analyst is surprised by "no results" when they believe the product exists

**What to say:**
"Zero billing rows on an active catalog entry is a pre-launch signal, not a skill error.
The PRE-LAUNCH NES path should have fired — if it didn't, check whether the product is
in the catalog (active=true) and confirm the launch date with engineering." This is Mixed
because GAP-008 (now fixed) could mask a pre-launch product as CES; verify the pre-launch
NES check is working as expected.

---

## HE-008
Pattern    : Citing a stale or rolled-back champion as the current offer
Status     : active
Category   : Context Error
Frequency  : Rare (<5%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : GAP-007 (rolled-back offer state invisible in catalog — active=true persists
             after rollback). Analyst may independently tell the skill what champion to use,
             which can override billing-based discovery with stale data.

**What the analyst does:**
States explicitly that the current champion is "X" (a slug or curated offer ID from a
prior run, email, or spreadsheet) when that offer has since been rolled back. Because
catalog still shows active=true for rolled-back offers (GAP-007), the skill may confirm
the analyst's stated champion even though billing shows zero rows for it.

**How to detect:**
- Analyst states a specific champion slug before the skill has run billing queries
- The stated champion has zero billing rows in the 7-day window
- The stated champion is the same as in a prior run from weeks ago
- Analyst disputes the billing-discovered champion ("but I thought it was X")

**What to say:**
"The stated champion has zero billing rows in the last 7 days — it may have been rolled
back. Active catalog entry does not confirm live status. Ask ecomm engineering to confirm
the current live champion before cloning." This is Mixed because GAP-007 is a data
limitation: the skill cannot detect rollbacks from catalog data alone. Cross-reference
/system-gaps GAP-007 if this symptom recurs.

---

## HE-009
Pattern    : Scope too broad — entire product line instead of one surface
Status     : active
Category   : Scope Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Observed pattern across WAM runs where analysts ask for "all WAM products"
             or "all hosting surfaces". Offer-pulse is optimized for one surface/experiment
             at a time; broad scopes produce very long unactionable outputs.

**What the analyst does:**
Asks offer-pulse to audit an entire product line or multiple surfaces simultaneously:
- "All WAM products on all surfaces"
- "Every hosting SKU on FOS and precheck"
- "All surfaces where PFID 1320706 appears"

The result is an extremely wide output spanning many ITCs, surfaces, and packages that
cannot be used directly in a single EP or pricing ticket. The analyst often then needs to
re-run per surface anyway.

**How to detect:**
- Entry value contains "all", "every", "across all surfaces", "all surfaces"
- No specific ITC is provided for a product known to appear on multiple surfaces
- Output contains >5 distinct ITCs
- Analyst asks for a "comprehensive audit" or "full picture" in the initial entry

**What to say:**
"Offer-pulse is designed for one surface or experiment at a time — one EP ticket, one
pricing change. For a broad audit across surfaces, I'd recommend running one per ITC.
Which surface should we start with?" Not a skill defect; the skill's output scope is
intentionally per-surface. For pricing/discount scope across surfaces, use /pricing-ticket.

---

## HE-010
Pattern    : Ground truth derived from prior skill runs, not independent source of truth
Status     : active
Category   : Expectation Error
Frequency  : Rare (<5%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : 10-case blind evaluation 2026-05-14; expected_outputs.md derived from
             use-case log Notes/Assessment/Champion fields — retrospective assessments from
             prior skill runs, not independently verified against catalog/billing data.

**What the analyst does:**
When setting up a blind evaluation or scoring an offer-pulse output, derives expected values
(PFIDs, champion slugs, discount codes) from prior offer-pulse run output or retrospective
log assessments rather than from primary sources (catalog MCP, billing queries, confirmed
engineering tickets). The expected output inherits any errors or omissions from the prior
runs. Scoring then conflates genuine skill gaps with expectation calibration issues where
the expected value itself was wrong or under-specified.

**How to detect:**
- Expected output file was written after offer-pulse was run, not before
- Expected values reference "from a prior run" or "per the use-case log assessment"
- Scoring produces ✗ on fields where the PFID or slug cannot be independently confirmed
  against live catalog or billing data
- The analyst is uncertain whether a ✗ reflects a real skill failure or an under-specified
  expected value
- Champion slug in expected output exactly matches what a prior run produced (circular)

**What to say:**
"The expected output was derived from prior skill run output rather than primary sources.
Some ✗ marks may reflect under-specified expectations rather than genuine skill gaps. For
reliable scoring, expected values must be independently verified before the blind run:
PFIDs confirmed via billing query, champion slugs via catalog MCP, discount codes via
billing history. Treat this evaluation as directionally correct but with reduced confidence
on ✗ criteria where the expected value was not independently sourced." This is Mixed —
some failures are real skill gaps; others may be expectation calibration issues.
Cross-reference /system-gaps for confirmed skill defects before invoking /wendy.

---

## HE-011
Pattern    : WAM/WSB conflated — billing label vs catalog slug prefix
Status     : active
Category   : Input Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Crosswalk confirmed 2026-05-14. WAM = billing label (product_pnl_line_name =
             'Websites and Marketing'). WSB = catalog slug prefix (wsb_vnext_*, temp-wsb-*).
             Same product, two abbreviations belonging to different system layers.

**What the analyst does:**
Uses "WAM" and "WSB" interchangeably, or uses the wrong abbreviation in a context where
the other is required. Common failure modes:
- Provides "WSB" as a billing filter value — product_pnl_line_name contains "Websites and
  Marketing", not "WSB" — billing query returns zero rows silently
- Provides "WAM" as a catalog slug prefix — no curated offer or package slug starts with
  "wam_" — catalog search returns nothing
- Asks for "WAM offers on the catalog" expecting wam_* slugs, concludes the product isn't
  in NES when wsb_* slugs are the correct lookup

**How to detect:**
- Analyst uses "WSB" as a billing filter term (no product_pnl_line_name value contains
  "WSB")
- Analyst uses "WAM" as a catalog slug prefix (no curated offer starts with "wam_")
- Billing query returns zero rows when filtering on "WSB" or "WAM" as a label value
- Analyst seems confused that "WAM offers" can't be found in catalog, or "WSB billing
  rows" return nothing

**What to say:**
"WAM and WSB refer to the same product but belong to different systems: WAM is the billing
label (product_pnl_line_name = 'Websites and Marketing') and WSB is the catalog slug prefix
(e.g. wsb_vnext_*). For billing queries, use 'Websites and Marketing'. For catalog lookups,
use wsb_ as the slug prefix. Which layer are you working in?"

---

## HE-012
Pattern    : OX/OpenExchange expected as NES email component — actually migrated to Titan
Status     : active
Category   : Expectation Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Crosswalk confirmed 2026-05-14. OX (OpenExchange) was the legacy CES email
             component. In NES bundles, the email slot is Titan Email (UUID 927a9d45).
             The product was swapped during migration — the slug name retained "openexchange"
             but the component UUID does not.

**What the analyst does:**
Asks for or expects an OX/OpenExchange email component UUID in a NES offer context.
Common failure modes:
- Asks "what is the OX component UUID in NES?" — there is none; NES email component is
  Titan (UUID 927a9d45-7c5b-4652-ad68-d5cd9be75028)
- Expects curated offer wordpress-openexchange-forever-ssl-deluxe to have an OX UUID in
  its component list — it has Titan instead
- Assumes "the package is named openexchange" means "the package contains OX"
- Disputes output that correctly lists Titan UUID, expecting an OX ID

**How to detect:**
- Analyst asks for OX UUID, OX component ID, or OpenExchange component in a NES context
- Analyst confused why a package named *-openexchange-* does not contain an OX component
- Analyst asks "is OX the same as Titan?" (answer: no — different products, different vendors)
- Output lists Titan UUID 927a9d45 and analyst disputes it

**What to say:**
"OpenExchange (OX) was the legacy CES email component — it was not carried into NES catalog.
In NES bundles, the email component is Titan Email (UUID 927a9d45). The package slug may
retain 'openexchange' for historical naming but the component it includes is Titan. OX ≠
Titan; they are distinct products from different vendors."

---

## HE-013
Pattern    : Pro Email / M365 / Titan conflated — three distinct email component products
Status     : active
Category   : Input Error
Frequency  : Rare (<5%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Crosswalk confirmed 2026-05-14. Three distinct email products in NES catalog:
             Microsoft 365 (UUID 575a7d2a), Titan Email (UUID 927a9d45), Professional Email
             (UUID 2468b30f). Analysts frequently treat email as one category.

**What the analyst does:**
Uses "email", "Pro Email", "professional email", "M365", or "OX" vaguely when the specific
email component UUID matters for an EP ticket or bundle audit.
- Says "email" when they mean M365 (575a7d2a) — used in wordpress-o365-* packages
- Says "Pro Email" or "professional email" when they mean Titan Email (927a9d45)
- Uses M365 and "Pro Email" interchangeably when they are different products at different
  price points with different UUIDs
- Passes "professional email" as a search term expecting it to match M365

**How to detect:**
- Analyst refers to an email component without specifying which product
- Package slug contains o365 but analyst calls it "email" or "Pro Email"
- Component resolution in output uses a UUID the analyst did not expect
- Analyst asks "why is the email UUID wrong?"

**What to say:**
"There are three distinct email products in NES catalog, each with a different UUID:
- Microsoft 365 → UUID 575a7d2a (appears in *-o365-* packages; tag: m365)
- Titan Email    → UUID 927a9d45 (NES-era email; replaced OX in NES bundles)
- Professional Email → UUID 2468b30f (tag: professional-email; distinct product)
Check the package slug: o365 in slug = M365; openexchange or titan in slug = Titan Email."

---

## HE-015
Pattern    : Expected champion set at eval time reflects current catalog state, not state at
             ticket creation
Status     : active
Category   : Expectation Error
Frequency  : Occasional (5–25%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : Blind eval 2026-05-14; source tickets span multiple sprints; expected champion
             slugs derived from current catalog, not from billing data at ticket creation
             date. Related to HE-010 (circular ground truth) but distinct — the staleness
             here is temporal, not circular. See also GAP-021.

**What the analyst does:**
When building expected outputs for a backtesting evaluation, looks up the current active
champion in catalog and sets it as the expected value — without checking whether that slug
was also the champion when the source ticket was originally filed. For fast-moving surfaces
(dpp_precheck, slp_wsb_*), the champion can change within a single sprint. A skill output
that correctly reflects the historical champion will be marked ✗ because the expected value
has aged out.

**How to detect:**
- Source ticket is more than ~30 days old
- Expected champion was looked up at eval run time, not at ticket creation time
- A ✗ on N1 or C6 that the analyst cannot explain by reading the skill output
- Skill output champion has billing rows in the week the ticket was filed, but not today
- Billing query at current date shows a different dominant package_id than the eval expected

**What to say:**
"The expected champion reflects current catalog state, not the state when this ticket was
filed. For tickets older than ~30 days, verify the expected champion against billing data
from the week the ticket was created — not today. If historical billing data is unavailable,
mark N1/C6 as ~ (unverifiable) rather than asserting a potentially stale expected value.
This is Mixed: a ✗ on champion may mean the skill failed, or it may mean the expected value
aged out. Cross-reference GAP-021 for the evaluation methodology fix."

---

## HE-016
Pattern    : Jira ticket references offer slug using non-standard format (offer- prefix or
             camelCase) instead of kebab-case catalog slug
Status     : active
Category   : Input Error
Frequency  : Occasional (5–25%)
Verdict    : Mixed — Investigate
Added      : 2026-05-14
Evidence   : CMS-31766 blind eval run 2026-05-14 — slug "offer-sslcert-managedWithMonitoring"
             in ticket body → direct get_curated_offer returned NOT FOUND; ID scan found
             "sslcert-managed-with-monitoring".

**What the analyst does:**
References an offer in a Jira ticket using engineering shorthand or camelCase rather than
the kebab-case catalog slug. Common non-standard formats:
- "offer-sslcert-managedWithMonitoring" (offer- prefix + camelCase)
- "offer-titanemail-ultra" (offer- prefix + concatenated name)
- "sslcert-managedWithMonitoring" (camelCase without offer- prefix but still wrong case)

The catalog uses kebab-case without any prefix (e.g. "sslcert-managed-with-monitoring").
A direct get_curated_offer call on the verbatim ticket slug returns NOT FOUND. If the
skill does not fall back to the ID scan, the run produces a false NOT FOUND result and no
champion is identified — even though the offer exists in catalog under its correct slug.

**How to detect:**
- Jira ticket body or analyst input contains a slug with an "offer-" prefix
- Slug contains camelCase (uppercase letters mid-word) where catalog uses kebab-case
- Direct get_curated_offer on the verbatim ticket slug returns NOT FOUND
- ID scan immediately succeeds after the NOT FOUND, returning the correctly-cased kebab slug
- Analyst's stated slug and the ID-scan champion differ only in casing / prefix convention

**What to say:**
"The slug format in the ticket (`{ticket_slug}`) uses a non-standard prefix or camelCase.
The catalog uses kebab-case without the 'offer-' prefix (`{catalog_slug}`). I've fallen
back to the ID scan and found the correct offer. Note for future tickets: use the catalog
slug format, not the engineering shorthand."

This is Mixed — the skill should fall back to the ID scan automatically (Chain Step 2),
which is the correct recovery path. If the ID scan also fails, investigate whether Chain
Step 2 keyword seeds are sufficient for the product type before concluding the offer does
not exist.

---

## HE-017
Pattern    : FOS WAM experiment designed using NES curated offer path when surface is CES
Status     : active
Category   : Context Error
Frequency  : Occasional (5–25%)
Verdict    : Human Error Only
Added      : 2026-05-17
Evidence   : AGIGROWTH-51 (TrustedSite FOS experiment, Feb-Mar 2026). Team initially planned
             4 curated offers (NES path) for 4 experiment arms. Corrected on 2026-02-18 to
             CES packages. Confirmed via ticket comments and Confluence playbook.

**What the analyst does:**
When designing a multi-arm FOS pricing experiment, plans the implementation using NES curated
offers — requesting one curated offer per arm (e.g. "+$2 Premium w/o TS", "+$2 Premium w/ TS",
"+$3 Commerce w/o TS", "+$3 Commerce w/ TS"). The correct implementation for a CES FOS surface
is CES packages: one control package (PFID + discount code), one or more treatment packages
(PFID only, no discount). NES curated offers do not exist for FOS WAM surfaces (all SLP WAM
surfaces are CES except slp_hosting_4gh).

**How to detect:**
- Ticket requests "curated offer" or "curated offer creation" for slp_wsb_*, slp_rstdstore,
  or other confirmed-CES WAM surface
- Analyst asks for one EP ticket per experiment arm (NES framing) when surface is CES
- Experiment design uses phrases like "new curated offer for Treatment 1" on an FOS WAM context
- Surface ITC is slp_* (not slp_hosting_4gh) and product is WAM/WSB

**What to say:**
"FOS WAM surfaces are CES — NES curated offers don't apply here. The correct path for a CES
FOS pricing experiment is CES packages: raise the PFID sale price to the treatment level, then
create a control CES package with a discount code that restores the current price. See the
Confluence playbook: https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4271539132/FOS+Experiments

For the pricing ticket, this means: (1) a sale price increase request, (2) a discount code
request for the control, (3) CES package creation — NOT a curated offer EP ticket."

---

## HE-014
Pattern    : vnext used as product label without recognizing it as a CES slug prefix
Status     : active
Category   : Context Error
Frequency  : Rare (<5%)
Verdict    : Human Error Only
Added      : 2026-05-14
Evidence   : Crosswalk confirmed 2026-05-14. "vnext" appears in CES slugs as wsb_vnext_*
             denoting WAM v2 generation. Analysts may use "vnext" as a product version label
             without connecting it to CES architecture.

**What the analyst does:**
References "vnext" or "WAM vnext" as a product variant without knowing it implies CES
architecture and a specific slug naming convention. Common failure modes:
- Passes "vnext" as a catalog search term — NES catalog does not use this prefix, returns
  nothing
- Expects NES output for a "vnext" product that is CES by design (see also HE-004)
- Asks whether "vnext" should be in NES as part of migration scoping, not realizing vnext
  = CES generation by definition

**How to detect:**
- Analyst uses "vnext", "WAM v2", or "WAM vnext" as entry term or product descriptor
- Catalog MCP search for "vnext" returns zero results
- Analyst surprised that "vnext" is not in NES
- ITC is slp_wsb_* and analyst describes the product as "vnext"

**What to say:**
"'vnext' is a CES-era slug prefix (wsb_vnext_*) for WAM v2-generation products. It does
not appear in NES catalog because these products are pre-migration CES. If this product
has not been migrated to NES, offer-pulse will follow the CES path. Confirm the migration
status with engineering if NES output is expected."

---
