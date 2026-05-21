---
name: compare
description: Diff two offer-pulse run outputs from the use-case log to show what changed between them — packages added/removed, champion changes, geometry shifts, new flags. Use to answer "what changed on this surface since last time?"
---

# /compare — Offer Pulse Run Diff

Compares two offer-pulse run entries from the use-case log and outputs a structured diff: what changed in champion, packages, geometry, flags, and NES/CES classification.

Answers: "What changed on `slp_wordpress` since last quarter?" or "Did the fix make a difference between these two runs?"

Read-only. Does not write any files.

---

## Invocation

```
/compare <run-A> <run-B>
/compare <ITC> latest vs previous
/compare <ITC>
```

**Input forms:**
- Two run IDs: `/compare MWP-BASIC-SLP-OX-2026-05-01 MWP-BASIC-SLP-OX-2026-05-14`
- ITC shorthand: `/compare slp_wordpress` — compares the two most recent runs for that surface
- "latest vs previous" for a surface: `/compare dpp_precheck latest vs previous`

Section headers in the use-case log are used as run IDs (H2 headings).

---

## Step 1 — Parse the Invocation

- Two explicit run IDs → use exactly those two entries as Run A and Run B
- One ITC (or surface alias) + no run IDs → scan log for all entries where `Surface / ITC` matches that ITC; use the two most recent run entries as A (older) and B (newer)
- If only one matching entry exists for the ITC: `Only one logged run for {ITC}. Nothing to compare yet.`
- If the ITC is an alias, resolve it first (same resolution as `/surface-profile`)

---

## Step 2 — Read the Use-Case Log

Read `.claude/skills/offer-pulse/use-case-log.md`.

Locate the two target entries by their H2 heading. Extract all structured fields from each:

| Field | Extracted from |
|---|---|
| Date | `Date :` |
| Surface / ITC | `Surface / ITC :` |
| Path | `Path :` |
| NES/CES branch | `NES/CES branch :` |
| Offer operation | `Offer operation :` |
| Champion | `Champion :` |
| Geometry | `Geometry :` (or inferred from champion slug) |
| Flags fired | `Flags fired :` |
| Notes | `Notes :` |
| PFIDs | `PFIDs :` or PFID table |
| Packages seen | from Champion + any Supporting Detail packages listed |

If a field is absent in an entry, use `—` for that field.

---

## Step 3 — Build the Diff

For each field, classify the change:

| Change type | Symbol | When |
|---|---|---|
| Unchanged | `=` | Values identical |
| Changed | `↔` | Values differ |
| Added | `+` | Present in B, absent in A |
| Removed | `−` | Present in A, absent in B |

**Champion diff** — most important field. If the champion changed, flag it prominently.

**Package diff** — compare the set of packages (package_ids) visible in each run:
- Packages in A but not B → removed
- Packages in B but not A → added

**Flag diff** — compare the set of flags fired in each run:
- Flags in A but not B → cleared
- Flags in B but not A → new

**NES/CES classification diff** — if the NES/CES branch changed between runs (e.g. NES → CES, CES → Mixed), flag this as a high-significance change.

---

## Step 4 — Render the Diff

```
=== Run Diff: {run-A-label} → {run-B-label} ===
Surface       : {ITC}
Run A date    : {date-A}
Run B date    : {date-B}
Elapsed       : {N days between runs}

─── Key Changes ───────────────────────────────────────────────────
Champion      : {symbol}  A: {champion-A}
                           B: {champion-B}
                {↔ CHANGED — new champion | = unchanged}

NES/CES class : {symbol}  A: {class-A}  →  B: {class-B}

Geometry      : {symbol}  A: {geo-A}  →  B: {geo-B}

─── Package Changes ────────────────────────────────────────────────
Added   (+) : {package-id}
             {package-id}
Removed (−) : {package-id}

─── Flag Changes ───────────────────────────────────────────────────
New flags    : {flag-name}
Cleared flags: {flag-name}

─── Other Fields ───────────────────────────────────────────────────
Path          : {=|↔}  {value-A} → {value-B}
Offer operation : {=|↔}  {value-A} → {value-B}

─── Notes ──────────────────────────────────────────────────────────
Run A: {notes-A}
Run B: {notes-B}
```

If nothing changed across all fields: `No meaningful differences between {run-A} and {run-B}.`

---

## Step 5 — Summary Sentence

After the diff, emit one sentence:

- If champion changed: `Champion rotated from {A} to {B} between {date-A} and {date-B}.`
- If NES/CES classification changed: `Surface classification shifted from {class-A} to {class-B} — may indicate ongoing NES migration.`
- If packages added/removed: `{N package(s) added, M removed} between runs.`
- If nothing changed: `No changes detected — surface state is stable across these two runs.`

---

## Output Constraints

- Read-only. No file writes.
- If either run ID does not exist in the log: `Run '{id}' not found in use-case log. Use the exact H2 heading text as the run ID.`
- Do not attempt catalog MCP calls to validate package IDs — this is a log diff, not a new audit.
- Do not truncate the package change list. Show all added and removed packages.
