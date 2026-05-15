---
name: scorer
description: Scores a completed offer-pulse output field-by-field against expected values using path-type-specific criteria (Gates → NES Standalone / NES Bundle / CES). Read-only — produces a Score Card only; does not edit any skill or memory files.
---

# /scorer — Offer Pulse Scorer

**What to provide:**
1. The actual offer-pulse output (paste it in full, or the key fields)
2. The expected values — at minimum the correct path type, geometry, and the fields that matter

Scorer will apply the gate checks first, then score every criterion that can be evaluated. Criteria the analyst did not provide expected values for are marked `~` (unverifiable, excluded from denominator).

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
