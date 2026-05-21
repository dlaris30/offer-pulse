---
name: freshness
description: Quick staleness check for all offer-pulse reference files. Reports which catalogs, vocab files, and data artifacts are fresh vs. overdue for an update — without triggering a full overnight run.
---

# /freshness — Reference File Staleness Check

A lightweight pre-session check. Run this when starting a new offer-pulse session to know which reference files might be stale before you rely on them.

Does not write any files. Read-only.

---

## Invocation

```
/freshness                — check all reference files (default)
/freshness <file-name>    — check one specific file (e.g. /freshness package-catalog)
```

Valid single-file names: `package-catalog`, `ces-packages`, `surface-vocab`, `golden-set`, `coverage`, `ces-nes`

---

## Step 1 — Read Reference File Headers

Read the following files and extract their last-updated metadata:

| File | Path | Metadata to extract |
|---|---|---|
| package-catalog | `.claude/skills/package-catalog/catalog.md` | `Last classification run:` header line |
| ces-packages | `.claude/skills/ces-packages/knowledge-log.md` or the header of the catalog file | Last scan date from the header |
| surface-vocab | `.claude/skills/surface-vocab/surface-vocab.md` | `Last explore run:` or `Last updated:` header |
| golden-set | `.claude/skills/golden-set/golden-set.md` | Most recent `Added:` date across all entries |
| coverage (tree) | `.claude/skills/branch-map/tree.md` | `Last updated :` line |
| coverage (matrix) | `.claude/skills/offer-matrix/matrix.md` | Most recent `Updated :` date across all `## [` sections |

If a file does not exist, mark as `MISSING`.
If a file exists but has no parseable date, mark as `NO DATE`.

---

## Step 2 — Compute Age

For each file, compute `age_days = today − last_updated_date`.

Today's date: use the current date from context.

---

## Step 3 — Apply Staleness Thresholds

| Reference | Stale threshold | Very stale threshold |
|---|---|---|
| package-catalog | 7 days | 14 days |
| ces-packages | 14 days | 30 days |
| surface-vocab | 7 days | 14 days |
| golden-set | 30 days | 60 days |
| coverage (tree) | 7 days | 14 days |
| coverage (matrix) | 14 days | 30 days |
| ces-nes | — (knowledge embedded in SKILL.md; no file to check) | — |

Status:
- `age < stale threshold` → ✅ Fresh
- `stale ≤ age < very stale` → ⚠️ Stale
- `age ≥ very stale threshold` → ❌ Very Stale
- `MISSING` → ❌ Missing
- `NO DATE` → ❓ Unknown

---

## Step 4 — Render the Report

```
/freshness — {YYYY-MM-DD}

| Reference File     | Last Updated | Age  | Status          | Refresh Command            |
|--------------------|-------------|------|-----------------|----------------------------|
| package-catalog    | 2026-05-16  | 1d   | ✅ Fresh        | /overnight (Phase 5)       |
| ces-packages       | 2026-05-12  | 5d   | ✅ Fresh        | /ces-packages refresh      |
| surface-vocab      | 2026-05-10  | 7d   | ⚠️ Stale        | /surface-vocab explore     |
| golden-set         | 2026-05-05  | 12d  | ✅ Fresh        | /golden-set promote        |
| coverage (tree)    | 2026-05-09  | 8d   | ⚠️ Stale        | /coverage tree             |
| coverage (matrix)  | 2026-05-08  | 9d   | ⚠️ Stale        | /coverage matrix update    |

{N} reference files need attention.
```

If all files are fresh: `All reference files are current. No action needed.`

---

## Step 5 — Prioritized Recommendations

After the table, if any files are ⚠️ Stale or ❌ Very Stale, emit a prioritized action list:

```
Recommended actions (highest impact first):

1. Run /overnight — updates package-catalog, surface-vocab, tree, and matrix in one pass
   OR run individual refreshes if you only need one file:
2. /surface-vocab explore — profile 5 new ITCs
3. /coverage tree — update branch map from use-case log
4. /ces-packages refresh — scan new CES package families
```

Prioritize: package-catalog and surface-vocab affect active offer-pulse runs directly. Coverage files are informational. Golden-set staleness only matters before a batch-test run.

---

## Output Constraints

- This skill is read-only. Never write or edit any file.
- If a file is MISSING, note it but do not attempt to create it.
- Do not interpret what the content means — only report freshness status.
- For single-file invocations: show only that file's row and its recommended action.
