---
name: surface-profile
description: Quick surface overview before a full offer-pulse run. Given an ITC or surface alias, returns the surface's product mix, NES/CES split, top packages, and last-audited date — in under 2 CLN queries. Lightweight scout, not a full audit.
---

# /surface-profile — Surface Overview

A lightweight scout. Use this before running `/offer-pulse` when you want to understand a surface's current state without committing to a full curated offer audit.

Answers: "What's on this surface right now? Is it NES, CES, or mixed? What are the top packages? Has it been audited recently?"

---

## Invocation

```
/surface-profile <ITC or surface alias>
```

Examples:
- `/surface-profile slp_wordpress`
- `/surface-profile dpp_precheck`
- `/surface-profile FOS`  ← resolved via surface alias table

Accepts the same surface aliases that `/surface-vocab` resolves (FOS, front of site, precheck, etc.).

---

## Step 1 — Resolve ITC

If the input is an alias (not an ITC code starting with a known prefix like `slp_`, `dpp_`, `dlp_`, `upp_`, `mya_`, `dcc_`):

1. Check the Surface Name → ITC map in `/offer-pulse` SKILL.md, or
2. Search `.claude/skills/surface-vocab/surface-vocab.md` for the alias

If the alias is ambiguous (e.g. "checkout" maps to multiple ITCs), ask once: "Which ITC did you mean?"

---

## Step 2 — Query CLN (2 queries)

**Query 1 — Volume and NES/CES split (last 7 days)**

```sql
SELECT
    pkg.package_id,
    COUNT(*)                                         AS events_7d,
    CASE WHEN pkg.package_id IS NULL THEN 'CES'
         ELSE 'NES candidate' END                    AS arch_signal
FROM signals_platform_clickstream_cln.add_to_cart_product_event_cln   prod
JOIN signals_platform_clickstream_cln.add_to_cart_package_event_cln   pkg
    ON prod.add_to_cart_event_id = pkg.add_to_cart_event_id
   AND prod.src_receive_utc_year_num  = pkg.src_receive_utc_year_num
   AND prod.src_receive_utc_month_num = pkg.src_receive_utc_month_num
WHERE prod.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND prod.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND prod.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND prod.product_item_tracking_code {ITC_FILTER}
GROUP BY 1, 3
ORDER BY 2 DESC
LIMIT 30
```

For exact ITC: use `= '{itc}'`. For wildcard (e.g. `slp_wsb_*`): use `LIKE 'slp_wsb_%'`.

**Query 2 — Top products on this surface (last 7 days)**

```sql
SELECT
    prod.product_id                                  AS pfid,
    COUNT(DISTINCT prod.add_to_cart_event_id)        AS events_7d
FROM signals_platform_clickstream_cln.add_to_cart_product_event_cln prod
WHERE prod.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND prod.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND prod.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND prod.product_item_tracking_code {ITC_FILTER}
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20
```

---

## Step 3 — Compute NES/CES Split

From Query 1 results:
- `nes_events` = sum of `events_7d` where `package_id IS NOT NULL`
- `ces_events` = sum of `events_7d` where `package_id IS NULL`
- `nes_pct` = nes_events / (nes_events + ces_events) × 100

Apply pre-classification filter before computing: exclude slugs matching `_\d+mo$` or `_\d+yr$` (CES term aliases), and slugs with `nes-` or `offer-` prefix (ghost IDs). These are not valid NES. Recompute NES% from clean slugs only.

Classification:
- NES% ≥ 60% → **NES-dominant**
- NES% ≤ 20% → **CES-dominant**
- 20% < NES% < 60% → **Mixed**

---

## Step 4 — Check Known Context

1. Check `.claude/skills/surface-vocab/surface-vocab.md` for an existing ITC profile (NES/CES status, known products, champion slug, volume tier).
2. Check `.claude/skills/package-catalog/catalog.md` for any of the top package_ids from Query 1 — lookup geometry (standalone/bundle) and free trial flag.
3. Check use-case log `.claude/skills/offer-pulse/use-case-log.md` for any prior audit run on this ITC — extract date of most recent run and champion found.

---

## Step 5 — Render the Profile

```
=== Surface Profile: {ITC} ===
Surface      : {ITC}
Label        : {human label from surface-vocab, or —}
As of        : {today's date} (7-day window)

NES/CES Split
  Total events : {N}
  NES          : {N} ({pct}%)
  CES          : {N} ({pct}%)
  Classification : {NES-dominant | CES-dominant | Mixed}

Top Packages (NES)
  {package_id}         {N events}  {geometry from package-catalog or "unknown"}
  {package_id}         {N events}  ...

Top PFIDs
  {pfid}               {N events}
  ...

Last Audited
  {date of most recent offer-pulse run, or "No prior audit found"}
  {champion from that run, or —}

Surface Vocab Profile
  {summary from surface-vocab.md entry, or "Not yet profiled — run /surface-vocab explore"}
```

If zero results in both queries: output a zero-signal block:
```
=== Surface Profile: {ITC} ===
Zero add-to-cart events in the last 7 days.
Possible reasons: pre-launch, rolled-back, or ITC is inactive.
Run /offer-pulse to check catalog for pre-launch NES entries.
```

---

## Step 6 — Offer-Pulse Readiness Assessment

After the profile, output a one-line readiness note:

- If NES-dominant: `Ready for /offer-pulse — NES path likely. Champion from package-catalog: {slug or "run offer-pulse to identify"}.`
- If CES-dominant: `Ready for /offer-pulse — CES path expected. No curated offer ID will be emitted.`
- If Mixed: `Ready for /offer-pulse — Mixed surface. Expect split output (NES + CES blocks).`
- If zero events: `Catalog-only run recommended — no billing data to anchor against.`

---

## Output Constraints

- Maximum 2 Redshift queries. Do not expand scope mid-run.
- This is a scout, not a full audit — do not attempt catalog MCP calls or champion resolution.
- If surface-vocab has no profile for this ITC, note it but do not run explore mode.
- Geometry lookups from package-catalog are fast reads — use them; do not call catalog MCP.
- Do not write any files.
