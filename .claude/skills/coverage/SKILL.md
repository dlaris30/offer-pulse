---
name: coverage
description: Unified coverage monitor for offer-pulse. Combines the decision tree (branch map from the use-case log) and the lever × geometry reliability matrix. Shows confirmed/hypothetical branches with run counts and which pricing lever × offer geometry combinations the skill can reliably handle.
---

# /coverage — Offer Pulse Coverage Monitor

Tracks two dimensions of offer-pulse coverage in a single skill:

1. **Branch Map** — the living decision tree of all confirmed, hypothetical, and flagged branches from the use-case log
2. **Offer Matrix** — which pricing lever × offer geometry combinations the skill can reliably handle

**Write-enabled:** Writes `.claude/skills/branch-map/tree.md` and `.claude/skills/offer-matrix/matrix.md`.

---

## Invocation Modes

| Invocation | What it does |
|---|---|
| `/coverage` | Default: branch summary + matrix overview (both) |
| `/coverage tree` | Branch map only — update from log, show result |
| `/coverage tree rebuild` | Branch map — full rebuild from all log entries |
| `/coverage tree show` | Branch map — display current tree without updating |
| `/coverage matrix` | Matrix only — full 11×4 table + coverage stats |
| `/coverage matrix detail <lever> <geometry>` | Matrix — detail for one cell |
| `/coverage matrix gaps` | Matrix — list ⚠️ theoretical cells needing runs |
| `/coverage matrix progress` | Matrix — coverage stats only |
| `/coverage matrix update <lever> <geometry> <status> "<rationale>"` | Update a matrix cell |
| `/coverage matrix evidence <lever> <geometry> "<note>"` | Append evidence to a matrix cell |
| `/coverage update` | Run both tree update + matrix overview (for /overnight use) |

---

## Reference Tables

**Levers (11)**

| Slug | Full Name |
|---|---|
| sale-price-discount | Sale Price Discount |
| sale-price-increase | Sale Price Increase |
| term-based-pricing | Term-Based Pricing |
| free-trial-ccb | Free Trial - Credit Card Backed |
| free-trial-bmat | Free Trial - BMAT |
| free-trial-cmat | Free Trial - CMAT |
| soft-bundle | Soft Bundle |
| lock-on-create | Lock on Create |
| atmp | ATMP |
| freemium | Freemium |
| coupon-code | Coupon Code |

**Geometries (4)**

| Slug | Full Name |
|---|---|
| standalone | Standalone |
| upsell | Upsell (Intensity) |
| add-on | Add-on (Depth) |
| bundle | Bundle (Breadth) |

---

## Step 1 — Parse the Invocation

- No args, or args = `default` → **Default** (tree update + matrix overview)
- Args = `tree` with no sub-args → **Tree Update**
- Args = `tree rebuild` → **Tree Rebuild**
- Args = `tree show` → **Tree Show**
- Args = `matrix` with no sub-args → **Matrix Overview**
- Args starts with `matrix detail` → **Matrix Detail**
- Args = `matrix gaps` → **Matrix Gaps**
- Args = `matrix progress` → **Matrix Progress**
- Args starts with `matrix update` → **Matrix Update**
- Args starts with `matrix evidence` → **Matrix Evidence**
- Args = `update` → **Both Update** (tree update + matrix overview)

---

## Part A — Branch Map

Reads `.claude/skills/offer-pulse/use-case-log.md` and writes `.claude/skills/branch-map/tree.md`.

### Tree Update

**Step A1 — Read Inputs**

Read:
1. `.claude/skills/offer-pulse/use-case-log.md`
2. `.claude/skills/branch-map/tree.md` (may not exist — first run is a full build)

On `tree rebuild`: ignore existing tree.md and re-parse the full log.

**Step A2 — Parse Log Entries**

Filter to **run entries only** — skip any entry where the section title or `Entry type` / `Audit type` contains: `pulse-audit`, `use-cases audit`, `Wendy Measure`, `Assessment`.

For each run entry, extract **six branch signals**:

| Signal | Source Field | Values |
|--------|-------------|--------|
| `input_type` | `Entry type` | `jira` / `pfid` / `product` / `itc` / `jira+product` |
| `path` | `Path` | `A` / `B` |
| `classification` | `NES/CES branch` | `nes` / `ces` / `mixed` / `unknown` |
| `operation` | `Offer operation` | `create` / `create_ces` / `modify` / `pfid_inventory` / `blast_radius` |
| `ces_chain` | `CES chain steps` | comma list — extraction rules below |
| `champion` | `Champion` | `found` / `wrong` / `ambiguous` / `not_found` / `na` |

**`ces_chain` extraction rules** — scan for these keywords and collect all that match:
- `b0_fail` — "B0 fail"
- `step1_match` — "CONFIRMED_MATCH" or "Step 1: ... found"
- `step1_fail` — "CONFIRMED_NO_MATCH"
- `step2_found` — "Step 2: ... found" or "Step 2: ... keyword ... found"
- `step2_fail` — "Step 2: ... fail" or "0 keyword matches" or "no candidates"
- `step3_found` — "Step 3: ... found"
- `step3_error` — "API error" or "AvailabilityServiceInternalError"
- `step3_not_found` — "Step 3: ... not found" or "net-new confirmed"
- `na` — field absent or "N/A"

**`champion` extraction:** "WRONG" → `wrong`; "ambiguous" → `ambiguous`; "NOT FOUND" / "not found" / "None" → `not_found`; "N/A" or absent → `na`; any other non-empty → `found`.

Also extract: `run_date`, `has_flags` (true if Flags fired ≠ "none"), `run_label`.

**Step A3 — Build Node Registry**

Each node: `id`, `label`, `parent`, `confirmed_runs`, `flagged_runs`, `first_seen`, `last_seen`, `example_runs` (up to 2 most-recent).

Structural nodes (complete skeleton):

```
input.jira                      Input: Jira ticket key
input.pfid                      Input: PFID-first
input.product                   Input: Product name
input.itc                       Input: ITC direct
input.jira_product              Input: Jira + Product name

path_a                          Path A — Curated Offer / EP Engineering
path_a.nes                      NES surface (package_id present in billing)
path_a.nes.standalone           NES → Standalone Offer
path_a.nes.standalone.found     NES Standalone → Champion resolved
path_a.nes.standalone.net_new   NES Standalone → NET-NEW build
path_a.nes.bundle               NES → Offer Collection / Bundle
path_a.nes.bundle.found         NES Bundle → Curated offer resolved
path_a.nes.bundle.net_new       NES Bundle → NET-NEW build
path_a.ces                      CES surface (100% null package_id)
path_a.ces.b0_fail              CES → B0 contaminated / failed
path_a.ces.b0_ok                CES → B0 clean, entering chain
path_a.ces.step1_match          CES Chain → Step 1: Merchandising PFID match found
path_a.ces.step1_fail           CES Chain → Step 1: CONFIRMED_NO_MATCH
path_a.ces.step2_found          CES Chain → Step 2: Keyword scan found
path_a.ces.step2_fail           CES Chain → Step 2: No candidates
path_a.ces.step3_found          CES Chain → Step 3: Catalog scan found
path_a.ces.step3_error          CES Chain → Step 3: API error
path_a.ces.step3_not_found      CES Chain → Step 3: Not found → net-new confirmed
path_a.mixed                    Mixed NES + CES surface

edge.champion_wrong             Champion identified incorrectly
edge.champion_ambiguous         Multiple champion candidates, unclear
edge.net_new_confirmed          Net-new build confirmed (any path)
edge.api_error                  Catalog / Merchandising API error
edge.b0_contamination           B0 filter contamination
edge.slug_mismatch              Slug format mismatch
edge.market_missing             Market gate not pre-answered
edge.surface_unrecognized       Surface ITC unrecognized
edge.keyword_seeds_incomplete   CES keyword seeds insufficient
```

Signal → node mapping: (same as prior branch-map skill — increment nodes per signal, increment `flagged_runs` if `has_flags = true`)

NES geometry sub-branches: use Notes/Flags field keywords (`prePurchaseKeyMap` → bundle; `Modify — Add Component` → bundle; otherwise leave at `path_a.nes` level).

**Step A4 — Detect Changes**

Compare updated registry against previous tree.md state:
- New branches confirmed (0 → >0 runs)
- Newly flagged (flagged_runs/confirmed_runs crossed 50%)
- First confirmed (moved from `[?]` to `[✓ 1]`)

**Step A5 — Render and Write tree.md**

Write `.claude/skills/branch-map/tree.md` with:
- Header (last updated, runs parsed, date range)
- Branch Tree visual with badges: `[✓ N]` confirmed, `[⚠ N/M]` flagged, `[○]` not yet reached
- Branch Detail table (nodes where confirmed_runs > 0)
- Hypothetical Branches list (confirmed_runs = 0)

Badge format: `confirmed_runs = 0` → `[○]`; `flagged_runs/confirmed_runs < 0.5` → `[✓ N]`; `≥ 0.5` → `[⚠ N/M]`.

**Step A6 — Output Change Report**

```
/coverage tree — {YYYY-MM-DD}

Runs parsed              : {N total} ({M new, or "full rebuild"})
New branches confirmed   : {labels or "none"}
Branches now flagged     : {labels or "none"}
─────────────────────────────────────────────
Confirmed  : {N} of {total} structural branches
Hypothetical: {M} not yet seen in log
Tree written → .claude/skills/branch-map/tree.md
```

### Tree Show

Read tree.md and output verbatim. If no tree.md: `No tree built yet. Run /coverage tree to build it.`

---

## Part B — Offer Matrix

Reads and writes `.claude/skills/offer-matrix/matrix.md`.

### Matrix Overview

Read matrix.md. Compute coverage counts (scoreable = total minus N/A; evidence-backed = cells where `Basis : evidence`).

```
Lever × Geometry Reliability Matrix
Updated  : {most recent Updated date}
Coverage : {evidence N}/{scoreable N} evidence-backed ({pct}%)
           {⚠️ N} theoretical  {❌ N} structural  {N/A N} N/A

| Lever                    | Standalone | Upsell | Add-on | Bundle |
|--------------------------|------------|--------|--------|--------|
| Sale Price Discount      |     ✅     |   ⚠️  |   ⚠️  |   ✅   |
...

✅ reliable (evidence-backed)  ⚠️ partial (theoretical)  ❌ unsupported (structural)  N/A
```

After the table: "Run `/coverage matrix gaps` to see which ⚠️ cells need test runs."

### Matrix Detail

Find `## [{lever} × {geometry}]` section. Render:

```
=== {Lever Full Name} × {Geometry Full Name} ===
Status     : {status}
Basis      : {evidence | theoretical | structural | n/a}
Evidence   : {evidence text}
Rationale  : {rationale text}
Updated    : {date}
```

### Matrix Gaps

Filter to `Basis : theoretical`. Render:

```
Gaps — {N} theoretical cells need a confirming run

| # | Lever | Geometry | Suggested test input |
|---|-------|----------|----------------------|
```

For each row: include a specific one-line suggested test input (real product type + surface).

### Matrix Progress

```
Coverage Progress — {date}
Evidence-backed ✅ : {N} / {scoreable} ({pct}%)
Theoretical     ⚠️ : {N} — testable, each needs one confirming run
Structural      ❌ : {N} — blocked on architecture
N/A                : {N}
```

### Matrix Update

Parse: lever, geometry, status (✅/⚠️/❌), rationale.
Normalize lever/geometry: lowercase, hyphens, fuzzy match against slug tables. When ambiguous, ask once.

Find `## [{lever-slug} × {geometry-slug}]` in matrix.md.
1. Replace `Status` line value
2. Set `Basis`: ✅ → `evidence`; ❌ with architecture reason → `structural`; ⚠️ → `theoretical`
3. Replace `Rationale`
4. Set `Updated` to today's date
5. Write file. Confirm: `Updated [{lever} × {geometry}] → {new status}`

### Matrix Evidence

Find the matching section. Append new note to `Evidence` line (` ; ` separator). Set `Updated`. Write file. Confirm.

---

## Default View (no args)

Run **Tree Update** (Step A1–A6), then immediately run **Matrix Overview**.

Output tree change report, then matrix table, separated by `---`.

---

## Output Constraints

- Never truncate Branch Detail table. `[○]` nodes appear in Hypothetical list, not in Branch Detail.
- Never truncate the 11×4 matrix table.
- Dates are ISO format (YYYY-MM-DD) throughout.
- Read-only modes (show, overview, detail, gaps, progress) never modify data files.
- Do not propose skill fixes — this skill maps coverage; Wendy fixes gaps.
