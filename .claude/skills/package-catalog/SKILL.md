---
name: package-catalog
description: Reference lookup for NES package_id geometry classification. Maps billing package_id slugs to standalone vs bundle, free trial flag, and component count. Used by offer-pulse and offer-matrix to determine geometry without a live catalog MCP call.
---

# /package-catalog — NES Package ID Geometry Reference

A persistent lookup table classifying every known `package_id` from billing as
standalone, bundle, or unknown — with free trial flag and catalog-verified date.

**Data file:** `.claude/skills/package-catalog/catalog.md`

---

## Invocation Modes

| Invocation | What it does |
|---|---|
| `/package-catalog` | Summary stats + coverage |
| `/package-catalog <package_id>` | Detail for one package_id |
| `/package-catalog bundles` | List all confirmed bundle package_ids |
| `/package-catalog freetrials` | List all free-trial-flagged package_ids |
| `/package-catalog unknown` | List unclassified package_ids |
| `/package-catalog refresh` | Instructions for adding newly-discovered package_ids |

---

## Classification Rules

A `package_id` from billing is the slug/name of a NES curated offer. Geometry is
determined by calling `get_curated_offer(curatedOfferId=<package_id>)` and checking:

- **Standalone**: `prePurchaseKeyMap` absent OR single-component offerCollection
  (one fixed entry with no second distinct product)
- **Bundle**: `prePurchaseKeyMap` present with 2+ component entries, OR
  offerCollection with 2+ distinct product components
- **Free trial flagged**: slug contains "FreeTrial", "freetrial", or catalog
  response contains BPO trial fields (trialDays, billingStartEvent, etc.)
- **Unknown**: catalog lookup returned NOT_FOUND (may be prod-only offer not
  present in test catalog datasource, or slug format mismatch)

## Geometry is immutable. Volume is not.

Once a package_id is classified, its geometry does not change mid-experiment.
The catalog file stores geometry + catalog-verified date only — **not volume**.
Volume is always queried live from billing at run time.

---

## Refresh Protocol

New `package_id` values appear in billing when new experiments are launched
(typically weekly). To detect and classify new ones:

**Step 1 — Detect new package_ids (weekly, via Alation scheduled query):**
```sql
SELECT DISTINCT pkg.package_id
FROM signals_platform_clickstream_cln.add_to_cart_package_event_cln pkg
WHERE pkg.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND pkg.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND pkg.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND pkg.package_id IS NOT NULL
```
Compare results against the package_ids in catalog.md. New ones not in the list
need classification.

**Step 2 — Classify new package_ids:**
For each new slug, call `catalog_query_get_offers(datasource="godaddy", currency="USD",
marketId="us", curatedOfferId="<slug>")`. Apply the classification rules above.
Append to catalog.md using the log entry format.

**Step 3 — Handle NOT_FOUND:**
If a slug returns NOT_FOUND, mark as `unknown` with today's date. Re-attempt on
the next refresh cycle — NOT_FOUND may indicate prod-only offer or slug format
mismatch (try lowercase variant, or try `get_all_packages` to locate by name).

**Refresh cadence:** Weekly is sufficient. Geometry is immutable; new experiments
are the only source of new package_ids. A monthly refresh is acceptable if
experiment launch cadence is low.

**No timestamp per row needed.** The `catalog_verified` date marks when the
classification was confirmed from a live catalog lookup. It does not expire —
geometry doesn't change. Only update it when re-verifying an existing entry.

---

## Log Entry Format

Each entry in catalog.md uses this format:

```
| <package_id> | <standalone/bundle/unknown> | <yes/no> | <YYYY-MM-DD> | <brief note> |
```

Columns: `package_id | geometry | free_trial | catalog_verified | notes`

---

## Output Constraints

- `/package-catalog` summary: always show total classified, standalone count,
  bundle count, unknown count, and free-trial count.
- `/package-catalog <package_id>`: if not found, say so and suggest running
  `/package-catalog refresh` to check for new entries.
- Read-only operations never modify catalog.md.
- Only `/package-catalog refresh` (and direct analyst edits) may append to catalog.md.
