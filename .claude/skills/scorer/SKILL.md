---
name: scorer
description: Scores a completed offer-pulse output field-by-field against expected values using path-type-specific criteria (Gates → NES Standalone / NES Bundle / CES). Read-only — produces a Score Card only; does not edit any skill or memory files.
---

# /scorer — Offer Pulse Scorer

**Two ways to provide expected values:**

**Option A — Case ID (golden set lookup)**
Pass a case_id (e.g. `AGIGROWTH-161`) and scorer will look up expected values from `.claude/skills/golden-set/golden-set.md` automatically. If the case_id is not found, scorer will ask you to provide expected values inline (Option B).

**Option B — Inline expected values**
Paste the expected values directly — at minimum the correct path type, geometry, and the fields that matter. This is the fallback when no golden-set entry exists yet.

Scorer will apply the gate checks first, then score every criterion that can be evaluated. Criteria with no expected value on file are marked `~` (unverifiable, excluded from denominator).

**Input handling:** If the offer-pulse output contains a `## Validation` section at the end, ignore everything from that section onward. Score only the offer analysis content above it.

---

## Case ID Lookup

When a case_id is provided:

1. Read `.claude/skills/golden-set/golden-set.md`
2. Find the `## {case_id}` section
3. Extract all `expected:` fields and the `ticket_ready:` block
4. Use these as the expected values for scoring

If the case_id is not found in golden-set.md:
> "No golden-set entry found for `{case_id}`. Please paste the expected values inline, or use `/golden-set promote {case_id}` after a validated run."

If the golden-set entry exists but a field is `unknown`, treat that criterion as `~`.

**What scorer does NOT do:**
- Run queries
- Call any MCP tools
- Edit SKILL.md or any memory file
- Diagnose root causes or propose fixes

---

## Scoring Criteria

**Legend:** ✓ correct  ✗ wrong or missing  ~ unverifiable or not applicable

---

### Gates (all paths)

| # | Criterion | Scoring |
|---|-----------|---------|
| G1 | Path classification (NES vs CES) | Exact match |
| G2 | Geometry type (NES only: Standalone vs Bundle) | Exact match |

If G1 fails, all path-specific criteria are `~`.
If G2 fails, N4 and N5 are invalid and marked `~`.

**Path selection:** After G1 passes, choose the scoring block based on the `path_type` field from the golden-set entry (or analyst-provided input):
- `NES Standalone` → use NES Standalone criteria (N1–N3 only)
- `NES Bundle` → use NES Bundle criteria (N1–N5)
- `CES` → use CES criteria (C1–C7) — see CES Scoring Detail below

---

### NES Standalone — 3 points

| # | Criterion | Scoring |
|---|-----------|---------|
| N1 | Curated Offer ID | Exact UUID match |
| N2 | Plan ID | Exact match |
| N3 | Discount Code | Exact match, or correctly stated as none |

---

### NES Bundle — 5 points

| # | Criterion | Scoring |
|---|-----------|---------|
| N1 | Curated Offer ID | Exact UUID match |
| N2 | Plan ID | Exact match — compound key, both tier and email variant must match |
| N3 | Discount Code | Exact match, or correctly stated as none |
| N4 | Component Offer IDs | All free/bundled component UUIDs present |
| N5 | Provisioning directives | FREEACCOUNT=true on all free components; `~` if no free components |

---

### CES — 7 points

| # | Criterion | Scoring |
|---|-----------|---------|
| C1 | Product Name | Exact or normalized match |
| C2 | PFID | Exact numeric match |
| C3 | Term | Exact match |
| C4 | Tier | Exact match |
| C5 | Discount Code | Exact match, or correctly stated as none |
| C6 | Existing CES Package | Package slug match |
| C7 | Free add-on PFIDs | All free PFID entries present; `~` if standalone with no bundled add-ons |

#### CES Scoring Detail

The golden-set CES entry stores `expected.packages[].rows[]` — a nested structure with one or more packages, each containing multiple product rows. Score each row individually:

1. Flatten `expected.packages[].rows[]` across all packages into a single list.
2. For each row, score C1–C5 against the corresponding row in the offer-pulse output (match by `product_name` + `term` when row order differs).
3. C6 (Existing CES Package): match `expected.packages[].package_name` against the champion package slug in the offer-pulse output. Score once per package.
4. C7 (Free add-on PFIDs): check that all rows where `free_product: Y` are present in the offer-pulse output. Mark `~` if no free rows exist.
5. Report score as `N_correct_criteria / N_total_criteria` across all rows.

**Normalized match (C1):** Case-insensitive, whitespace-trimmed, and known synonyms resolved (e.g. "M365" == "Microsoft 365", "Titan Email" == "Titan Business Email"). If uncertain, treat as exact match (✗).

---

### Field-to-Criterion Mapping (for golden-set lookups)

When reading from a golden-set entry, map these fields to criteria:

**NES Standalone / NES Bundle:**
| golden-set field | Criterion | Notes |
|---|---|---|
| `expected.source_offer_id` | N1 Curated Offer ID | UUID — must match offer-pulse Offer ID or Offer Collection ID |
| `expected.plan_name` | N2 Plan ID | Must match plan string from offer-pulse output |
| `expected.discount_code` | N3 Discount Code | Match or confirm "none" |
| `expected.source_offer_id` (on Collection) | N4 Component IDs | Component UUIDs must all be present in offer-pulse output |

**CES (per row in `expected.packages[].rows[]`):**
| golden-set field | Criterion |
|---|---|
| `rows[].product_name` | C1 Product Name |
| `rows[].pfid_new` | C2 PFID |
| `rows[].term` | C3 Term |
| `rows[].tier` | C4 Tier |
| `rows[].discount_code` | C5 Discount Code |
| `packages[].package_name` | C6 Existing CES Package |
| `rows[].free_product == Y` | C7 Free add-on PFIDs |

---

## Score Card Format

```
## Score Card

Path type : [NES Standalone | NES Bundle | CES]

### Gates
| # | Criterion | Expected | Actual | Result |
|---|-----------|----------|--------|--------|
| G1 | Path classification | | | ✓ / ✗ / ~ |
| G2 | Geometry type | | | ✓ / ✗ / ~ |

### [NES Standalone | NES Bundle | CES] Criteria
| # | Criterion | Expected | Actual | Result |
|---|-----------|----------|--------|--------|
| N1/C1 | ... | | | ✓ / ✗ / ~ |
| ...

Score : N / M  (~ criteria excluded from denominator)

[One sentence summary — e.g. "4/5 correct — wrong email variant in Plan ID compound key."]
```

After the Score Card, always end with exactly this line:

> "No files changed. Take this to `/wendy` if you want to update the skill."
