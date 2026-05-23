---
name: refresh
description: Manual post-run refresh orchestrator. Runs freshness check → stable-only batch test → targeted Wendy fix (if needed) → surface vocab expansion → branch map → offer matrix → package catalog. Call after a use-case run or whenever reference artifacts need refreshing. Does NOT run automatically.
---

# /refresh — Post-Run Refresh Orchestrator

Call this after an offer-pulse run, or any time you want to flush learnings, validate reference artifacts, and expand coverage. All phases run inline — you watch each one complete.

**Invoking this skill is consent to edit SKILL.md, use-case-log.md, tree.md, surface-vocab.md, matrix.md, and catalog.md.** No mid-run confirmation prompts will be issued.

---

**One sentence:** Validate what we know is still true, expand what we know, and fix only when there is a clean signal that the skill is wrong — not when the test case is wrong.

---

## Design Principles

The core problem this skill solves is different from what a simple batch re-run would solve. A naive design treats all batch-test failures as skill defects. They are not. Some failures are caused by structurally unreliable test cases — WebFetch truncation, A/B surface ambiguity, champion rotation, Jira ticket body routing sensitivity. Fixing the skill against those failures degrades it.

This skill separates three jobs that must never be conflated:

1. **Freshness validation** — Are our golden-set expected values still live in billing and catalog?
2. **Regression detection** — Did the skill break on cases we know are deterministic?
3. **Knowledge expansion** — What new surfaces, branches, offer geometries, and package IDs have appeared since the last run?

Only job 2 drives skill edits. Jobs 1 and 3 are always-on, edit-free, and produce flagged output for analyst review.

---

## Reliability Classification

Every golden-set entry has (or should have) a `reliability` field: `stable`, `volatile`, or `retired`.

| Class | Definition | Batch-test eligible? | Freshness-check eligible? |
|---|---|---|---|
| `stable` | Single deterministic champion, analyst-confirmed, not WebFetch-dependent | Yes | Yes |
| `volatile` | A/B surface, WebFetch-dependent CES step 1, multi-champion geo-split, AMBIGUOUS expected result, BLOCKING unknown PFIDs, or Jira-routed input where ticket body drives path | No | No |
| `retired` | Surface dark, product EOL, champion replaced | No | No |

**Conservative default:** Entries without a `reliability` field are treated as `volatile`. They are excluded from batch-test and freshness checks. The analyst promotes entries to `stable` using `/golden-set promote` or by directly editing the entry.

**Current stable set (as of 2026-05-16):**
- UC-01 (`dpp-ca-ca`, NES Bundle)
- UC-02 (`slp_ssl`, NES Standalone)
- CMS-32825 (`slp_ssl`, NES Standalone — catalog resolution test)
- M365-OE-NOTEAMS-DPP-EVAL-02 (`dpp_precheck`, CES — chain step 2/3, no WebFetch)
- M365-OE-NOTEAMS-DPP-19 (`dpp_precheck`, CES — chain step 2/3, no WebFetch)
- CMS-31766 (`slp_ssl / ssl-config`, CES — catalog resolution, NES reference surfacing test)

**Current volatile set (excluded from batch test):**
- UC-03 (MENA — two simultaneous architectures)
- MWP-BASIC-SLP-OX (`slp_wordpress`, NES Bundle — geo-split, two champions)
- MWP-BASIC-SLP-GEOSPLIT (geo-split, two champions)
- MWP-DELUXE-SLP (geo-split, two champions)
- CMS-31421 (CES step 1 WebFetch)
- EMAIL-ESS-DPP-17 (CES step 1 WebFetch)
- TITAN-FREETRIAL-14D-UPP-08 (UPP CES-only, BLOCKING pfid)
- TITAN-FREETRIAL-14D-UPP-1430 (UPP CES-only, BLOCKING pfid)
- WAM-PREM-COMM-FOS-4ARM (CES step 1 WebFetch)
- CMS-32651 (AMBIGUOUS clone source)
- TRUSTEDSITE-DPP-MODIFY (all three CES chain steps structurally failed)

---

## Pre-requisites

Already configured in `.claude/settings.json`:
- `mcp__catalog-mcp-dev__*` — catalog MCP tool calls
- `Edit` on SKILL.md, use-case-log.md, surface-vocab.md, tree.md, matrix.md, catalog.md
- `execute_query` — Redshift SELECT queries (needed for Phase 1a and Phase 5)

---

## Files That Will Change

| File | Change |
|---|---|
| `.claude/skills/offer-pulse/SKILL.md` | Edited if Phase 1d finds a clean skill failure and Wendy designs a fix |
| `.claude/skills/offer-pulse/use-case-log.md` | One `/ledger` entry appended if a fix was applied (Phase 1d only) |
| `.claude/skills/surface-vocab/surface-vocab.md` | 5 new ITC profiles appended (Phase 2 — always runs) |
| `.claude/skills/branch-map/tree.md` | Decision tree updated (Phase 3 — always, written by /coverage) |
| `.claude/skills/offer-matrix/matrix.md` | Reliability matrix updated (Phase 4 — always, written by /coverage) |
| `.claude/skills/package-catalog/catalog.md` | New package_ids appended + header updated (Phase 5 — always) |

---

## Invocation

```
/refresh [max_fix_cycles]
```

`max_fix_cycles` is optional. Default: **1**. Maximum: **2**.

This is the cap on Phase 1d fix cycles — not on the total run. Phases 2–5 always run regardless. The cap is low by design: the fix loop only runs when there is a clean failure signal, and a single well-targeted fix is more reliable than multiple speculative ones.

---

## Execution

### Initialize

Parse `$ARGUMENTS` for an integer (max fix cycles). Default: 1. Cap at 2.

Initialize tracking:
- `fix_cycles_run = 0`
- `fix_applied = false`
- `pre_pass_rate = null`
- `stable_failures = []`
- `freshness_flags = []`
- `catalog_flags = []`

Output the run header:

```
## /refresh — {YYYY-MM-DDThh:mm}
Max fix cycles : {max_fix_cycles}
```

---

## Phase 1 — Validation Loop

### Phase 1a — Freshness Check (Redshift)

**Goal:** Confirm that each stable golden-set entry's expected package_id (or PFID for CES) is still appearing in live CLN data for its surface.

Read `.claude/skills/golden-set/golden-set.md`. Extract all entries where `reliability: stable`.

For NES stable entries with a `source_offer_slug`: execute one query per surface to confirm the slug is still present in recent billing data:

```sql
SELECT
    pkg.package_id,
    COUNT(*) AS events_7d
FROM signals_platform_clickstream_cln.add_to_cart_product_event_cln   prod
JOIN signals_platform_clickstream_cln.add_to_cart_package_event_cln   pkg
    ON prod.add_to_cart_event_id = pkg.add_to_cart_event_id
   AND prod.src_receive_utc_year_num  = pkg.src_receive_utc_year_num
   AND prod.src_receive_utc_month_num = pkg.src_receive_utc_month_num
WHERE prod.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND prod.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND prod.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND prod.product_item_tracking_code = '{surface_itc}'
  AND pkg.package_id IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20
```

Replace `{surface_itc}` with the surface ITC. For surfaces that are wildcard patterns (e.g. `slp_wsb_*`, `upp_titanproduct_*`), use `LIKE 'slp_wsb_%'` in the WHERE clause instead of `=`.

For each stable entry, check whether the expected `source_offer_slug` appears in the query results.

**Flag conditions (add to `freshness_flags`):**
- Expected slug is completely absent from 7-day results
- Expected slug was previously the top-volume slug but has dropped to < 10% of its previous rank

Do not auto-retire entries. Flag only. The analyst reviews the flags after the run.

If Redshift is unavailable: note `Phase 1a: skipped — Redshift unavailable` and proceed to Phase 1b.

For CES stable entries: freshness check is not applicable (CES entries have null package_ids by definition). Skip CES stable entries in Phase 1a.

---

### Phase 1b — Catalog Consistency Check (catalog MCP)

**Goal:** Confirm NES expected UUIDs still resolve to the expected slug and plan in the catalog.

For each stable NES entry with a known `source_offer_id` (not `unknown`):

Call `get_offer_definition_by_id(datasource="catalog-offers", offerId=<source_offer_id>)`.

Check:
- UUID still resolves (not 404)
- The slug in the catalog response matches `source_offer_slug`
- The plan in the catalog response includes the expected `plan_name`

**Flag conditions (add to `catalog_flags`):**
- UUID returns 404 or NOT_FOUND
- Slug has changed
- Expected plan_name is no longer present in the plan list

Do not auto-retire entries. Flag only.

If catalog MCP is unavailable: note `Phase 1b: skipped — catalog MCP unavailable` and proceed to Phase 1c.

---

### Phase 1c — Stable-Only Batch Test

**Goal:** Regression detection on the clean, deterministic subset. This is the only pass/fail signal that drives skill edits.

Invoke the `/batch-test` skill by reading and following `.claude/skills/batch-test/SKILL.md` with argument `stable`.

`/batch-test stable` filters to only entries where `reliability: stable` in golden-set.md. Do not pass a hardcoded case_id list — the golden set is the source of truth for which cases are stable.

From the batch report, extract:
- `pass_count`
- `fail_count`
- `pass_rate` = pass_count / (pass_count + fail_count) × 100

Set `pre_pass_rate = pass_rate`.

If pass_count + fail_count = 0 (no stable entries found): note `Phase 1c: no stable entries in golden set — skipping regression gate` and proceed to Phase 2.

If `fail_count = 0`: note `Phase 1c: all stable cases PASS — no fix needed` and proceed to Phase 2 (skip Phase 1d).

If `fail_count > 0`: collect `stable_failures` list (list of case_ids that failed). Proceed to Phase 1d.

---

### Phase 1d — Targeted Fix Loop (only if stable_failures is non-empty)

**Gate:** Before entering this loop, verify each failure in `stable_failures` against the freshness and catalog flags.

If a failing case_id also has a freshness flag or catalog flag raised in Phase 1a or 1b, it means the expected value may have drifted — not that the skill is wrong. For those cases: output a note per case:

```
Phase 1d note: {case_id} failed but also has a freshness/catalog flag — champion may have rotated. Skipping Wendy fix for this case. Recommend analyst review before next run.
```

Remove flag-matched cases from `stable_failures`. If `stable_failures` is now empty: output `Phase 1d: all failures attributed to data drift — no skill fix warranted` and proceed to Phase 2.

**For remaining stable_failures (clean skill failures):**

Run up to `max_fix_cycles` fix cycles. Each cycle:

**Cycle step A — Architecture check:**

Invoke the `/ces-nes` skill by reading and following `.claude/skills/ces-nes/SKILL.md`.

Pass: "Review the following failure pattern and provide an architectural verdict (APPROVED or BLOCKED — see Pipeline Review Mode). State any constraints Wendy must respect:\n\n{failure summary from batch report for stable_failures}"

Capture as `arch_context`.

**Cycle step B — Wendy fix:**

Spawn the Wendy subagent using the Agent tool with subagent_type `wendy`, passing:
1. `"NES/CES Architecture Review:\n{arch_context}\n\n---\n\n"`
2. The failure summary and Score Card(s) for the failed stable cases

If Wendy outputs "no change needed" or "cannot improve without more data": note `Phase 1d: Wendy found no actionable fix` and exit the loop. Proceed to Phase 2.

If `arch_context` is BLOCKED and Wendy's fix contradicts the constraints: note `Phase 1d: Wendy's proposed fix blocked by architecture constraints — skipping` and exit the loop. Proceed to Phase 2.

**Cycle step C — Apply fix:**

Apply Wendy's proposed change to `.claude/skills/offer-pulse/SKILL.md` using the Edit tool.

Output:
```
Phase 1d — Cycle {N}: Applied — "{one-line description of what changed}"
```

Set `fix_applied = true`.

**Cycle step D — Re-test stable set:**

Re-run `/batch-test` with the same stable case_ids.

From the new report, extract `new_pass_rate`.

If `new_pass_rate < pre_pass_rate`: REGRESSION.
```
REGRESSION — Phase 1d Cycle {N}
Pass rate dropped : {pre_pass_rate}% → {new_pass_rate}%
Fix has been applied but caused regression. SKILL.md has been edited.
Review the change before the next run.
```
Set `regression_detected = true`. Exit the loop. Proceed to Phase 2.

Update `pre_pass_rate = new_pass_rate`. Increment fix_cycles_run.

**Cycle step E — Gap reconciliation:**

Read the three knowledge logs directly (do not invoke as skills — circular call risk):
1. `.claude/skills/gaps/gaps-log.md`
2. `.claude/skills/gaps/error-log.md`
3. `.claude/skills/tribal-knowledge/knowledge-log.md`

Extract keywords from Wendy's change description. Score open entries against those keywords. If matches found:

```
Gap Reconciliation — Phase 1d Cycle {N}
• /gaps GAP-{N} — {Title}  [may be resolved by this fix]
• /gaps HE-{N} — {Pattern}  [may be addressed by this fix]
• /tribal-knowledge TK-{N} — {Title}  [may need updating]
```

If no matches: omit the block.

**Cycle step F — Measure:**

Invoke the `/ledger` skill by reading and following `.claude/skills/ledger/SKILL.md`, passing the failure description as the argument. This appends a `Wendy Measure` entry to the use-case log.

**Loop control:** If `fix_cycles_run < max_fix_cycles` and `stable_failures` still has unresolved cases: increment cycle and return to Cycle step A.

Otherwise: exit the loop and proceed to Phase 2.

---

## Phase 2 — Surface Vocabulary Expansion

**Always runs.** Not conditioned on whether Phase 1 made any changes.

Invoke the `/surface-vocab` skill in **explore** mode by reading and following `.claude/skills/surface-vocab/SKILL.md` with argument `explore`, but profile only **5 ITCs** this run. Stop after 5 regardless of what the skill's own step count says.

This profiles 5 unexplored ITCs from `offer_pulse_experiment`, ordered by volume (highest first), and appends them to `.claude/skills/surface-vocab/surface-vocab.md`.

If Redshift is unavailable or returns an error: note `Phase 2: skipped — Redshift unavailable` and continue to Phase 3.

---

## Phase 3 — Branch Map Update

Invoke the `/coverage` skill by reading and following `.claude/skills/coverage/SKILL.md` in tree update mode (pass `tree` as the argument).

Capture:
- `new_branches` — count of new branches confirmed this run
- `flagged_branches` — count of branches newly flagged (≥ 50% flag rate)
- `total_confirmed` — total confirmed branches out of structural total

If coverage tree errors: note the error and continue to Phase 4.

---

## Phase 4 — Offer Matrix Update

Invoke the `/coverage` skill by reading and following `.claude/skills/coverage/SKILL.md` in matrix mode (pass `matrix` as the argument, no sub-args — runs overview).

Capture:
- `cells_updated` — count of matrix cells whose status changed this run
- `cells_confirmed` — total cells currently marked ✅ evidence-backed

If coverage matrix errors: note the error and continue to Phase 5.

---

## Phase 5 — Package Catalog Refresh

**Step 1 — Detect new package_ids.** Execute:

```sql
SELECT DISTINCT package_id
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE bill_modified_mst_date >= DATEADD(day, -7, CURRENT_DATE)
  AND package_id IS NOT NULL
```

If Redshift is unavailable: note `Package catalog: skipped — Redshift unavailable` in the Final Report and proceed to the Final Report.

**Step 2 — Compare.** Read `.claude/skills/package-catalog/catalog.md`. Find slugs in the query result that are NOT in catalog.md and do not match `_\d+mo$` (CES term-alias slugs).

If no new slugs: note `Package catalog: up to date` and proceed to the Final Report.

**Step 3 — Classify new slugs.** For each new slug, call `get_curated_offer(datasource="catalog-curated-offers", curatedOfferId=<slug>)`. Apply classification rules:
- **Standalone**: no `prePurchaseKeyMap`, or single-component offerCollection
- **Bundle**: `prePurchaseKeyMap` with 2+ components, or offerCollection with 2+ distinct products
- **Free trial**: `configKeyValues.billingPolicyOverride.planType = FREE_TRIAL`, or slug contains `FreeTrial`/`freetrial`
- **Unknown**: NOT_FOUND in all datasources

Append each new row to catalog.md:
```
| <package_id> | <geometry> | <yes/no> | {today's date} | <brief note> |
```

Update catalog.md header: `Last classification run: {today's date}` and `Total distinct package_ids active this week: {new total}`.

**Step 4 — Report.** Capture `pkg_classified` = count of new slugs added.

---

## Final Report

```
## /refresh — Complete
{YYYY-MM-DDThh:mm}

Phase 1a — Freshness flags  : {count}  ({list of flagged case_ids, or "none"})
Phase 1b — Catalog flags    : {count}  ({list of flagged case_ids, or "none"})
Phase 1c — Stable pass rate : {pass_rate}%  ({pass_count} PASS / {fail_count} FAIL / {no_oracle_count} no oracle)
Phase 1d — Fix applied      : {yes — "{one-line description}" | no — {reason: all pass / data drift / arch blocked / Wendy no fix}}
Regression detected         : {yes — see above | no}
Gap items flagged           : {N | none}

Phase 2 — Surface vocab     : {5 new ITCs profiled | "skipped — Redshift unavailable"}
Phase 3 — Branch map        : {N new} new branches, {M} flagged  ({total_confirmed} confirmed)
Phase 4 — Offer matrix      : {N cells updated}  ({cells_confirmed} ✅ evidence-backed)
Phase 5 — Package catalog   : {N new slugs classified | "up to date" | "skipped — Redshift unavailable"}

{One of:}
  All stable cases PASS — system healthy.
  Stable cases failed; fix applied — verify with analyst before promoting to volatile set.
  Stable cases failed; failures attributed to data drift — review freshness flags above.
  Stable cases failed; Wendy found no actionable fix — log to /gaps.
  REGRESSION detected — SKILL.md was changed in Phase 1d and caused a regression. Review before next run.
  No stable golden-set entries — run /golden-set to classify existing entries and promote new ones.
```

---

## Bail Conditions

| Condition | What happens |
|---|---|
| No stable entries in golden set | Skip Phase 1c and 1d; note in Final Report |
| All stable cases PASS | Skip Phase 1d entirely |
| All stable failures have freshness or catalog flags | Skip Wendy fix; attribute to data drift |
| arch_context BLOCKED and Wendy cannot resolve | Skip fix; note in Final Report |
| Wendy outputs no actionable change | Skip fix; note in Final Report |
| Post-fix pass rate drops | Flag REGRESSION; stop Phase 1d loop; continue Phases 2–5 |
| Cycle cap reached | Stop Phase 1d loop; continue Phases 2–5 |
| Redshift unavailable | Skip Phase 1a, 1c's data-dependent queries, Phase 2, Phase 5; note in Final Report |
| Catalog MCP unavailable | Skip Phase 1b; note in Final Report |

---

## Output Constraints

- Never ask for confirmation mid-run
- Each phase header must be visible — it is the progress marker for analyst review
- Never truncate batch-test or measure output
- If a sub-skill errors, capture the error message, include it in the Final Report, and continue to the next phase — do not stop the whole run for a single sub-skill failure
- Freshness flags and catalog flags are output for analyst review — do not auto-retire golden-set entries

---

## Supporting Changes Required (Not Part of This Skill)

**batch-test:** Add `stable` as a valid argument. When invoked with `/batch-test stable`, filter the case list in Step 1 to entries where `reliability: stable`. All other behavior (isolation guarantee, scoring, report format) unchanged.

**golden-set:** Add `reliability` as a required field in the entry schema. Default: `volatile` for CES entries, `stable` for NES entries where analyst confirms single-champion. The `/golden-set add` and `/golden-set promote` flows should ask for `reliability` when creating a new entry. Existing entries without this field are treated as `volatile` by `/refresh` and batch-test.
