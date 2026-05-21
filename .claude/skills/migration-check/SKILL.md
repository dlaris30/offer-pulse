---
name: migration-check
description: Check NES migration status for a surface or product. Queries live CLN/billing data to determine current NES%, compares against the known 59.7%/40.3% baseline, and flags surfaces that have migrated, are in-progress, or are still CES-only. Use before relying on any surface-specific NES assumption.
---

# /migration-check — NES Migration Status

Answers: "Has this surface migrated to NES? Has this product migrated? Should I expect NES output or CES output today?"

Critical rule: **migration timelines are estimates**. Never update skill behavior for a surface until the transition shows in CLN/billing data. This skill provides the data check.

---

## Invocation

```
/migration-check <ITC or product name or PFID>
/migration-check slp_wsb_*
/migration-check "WAM Premium"
/migration-check dpp_precheck
```

Accepts ITC codes, surface aliases, product names, or PFIDs.

---

## Step 1 — Resolve Input

- If input matches an ITC pattern (`slp_`, `dpp_`, `dlp_`, `upp_`, `mya_`, `dcc_`, or contains `_`) → treat as surface ITC
- If input is a product name (contains spaces or is a known product alias) → run product name lookup in Step 2B
- If input is a PFID (all digits) → run PFID lookup in Step 2C
- If input is a surface alias → resolve via surface-vocab map first

---

## Step 2 — Query CLN

### 2A — Surface-Level NES% (for ITC input)

```sql
SELECT
    CASE WHEN pkg.package_id IS NULL THEN 'CES'
         WHEN pkg.package_id ~ '_[0-9]+mo$|_[0-9]+yr$' THEN 'CES alias'
         WHEN pkg.package_id ~ '^(nes-|offer-)' THEN 'Ghost ID'
         ELSE 'NES' END           AS arch_class,
    COUNT(*)                      AS events_7d
FROM signals_platform_clickstream_cln.add_to_cart_product_event_cln   prod
JOIN signals_platform_clickstream_cln.add_to_cart_package_event_cln   pkg
    ON prod.add_to_cart_event_id = pkg.add_to_cart_event_id
   AND prod.src_receive_utc_year_num  = pkg.src_receive_utc_year_num
   AND prod.src_receive_utc_month_num = pkg.src_receive_utc_month_num
WHERE prod.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND prod.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND prod.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND prod.product_item_tracking_code {ITC_FILTER}
GROUP BY 1
ORDER BY 2 DESC
```

### 2B — Product-Level NES% (for product name input)

```sql
SELECT
    prod.product_item_tracking_code    AS itc,
    CASE WHEN pkg.package_id IS NULL THEN 'CES'
         WHEN pkg.package_id ~ '_[0-9]+mo$|_[0-9]+yr$' THEN 'CES alias'
         WHEN pkg.package_id ~ '^(nes-|offer-)' THEN 'Ghost ID'
         ELSE 'NES' END                AS arch_class,
    COUNT(*)                           AS events_7d
FROM signals_platform_clickstream_cln.add_to_cart_product_event_cln   prod
JOIN signals_platform_clickstream_cln.add_to_cart_package_event_cln   pkg
    ON prod.add_to_cart_event_id = pkg.add_to_cart_event_id
   AND prod.src_receive_utc_year_num  = pkg.src_receive_utc_year_num
   AND prod.src_receive_utc_month_num = pkg.src_receive_utc_month_num
LEFT JOIN pricing_mart.site_product_price_event  pe
    ON prod.product_id = pe.pf_id
   AND pe.report_date >= CURRENT_DATE - 7
WHERE prod.src_receive_utc_year_num  = EXTRACT(year  FROM CURRENT_DATE)
  AND prod.src_receive_utc_month_num = EXTRACT(month FROM CURRENT_DATE)
  AND prod.src_receive_utc_day_num  >= EXTRACT(day   FROM CURRENT_DATE) - 7
  AND LOWER(pe.product_pnl_subline_name) LIKE LOWER('%{product_name}%')
GROUP BY 1, 2
ORDER BY 1, 3 DESC
```

### 2C — PFID-Level NES% (for PFID input)

Same as 2A but filter: `AND prod.product_id = {pfid}` without the ITC filter. Group by ITC additionally to show per-surface breakdown.

---

## Step 3 — Compute Migration Status

From the query results, compute true NES% (excluding ghost IDs and CES aliases):

```
nes_events = events where arch_class = 'NES'
total_events = all events
ghost_events = events where arch_class = 'Ghost ID'
ces_alias_events = events where arch_class = 'CES alias'
true_nes_pct = nes_events / (nes_events + ces_events) × 100
```

Apply status thresholds:

| NES% | Status |
|---|---|
| 0% | **CES Only** — no NES migration detected |
| 1–30% | **NES Starting** — migration underway, mostly CES still |
| 31–69% | **NES in Progress** — active migration, both architectures live |
| 70–99% | **NES Dominant** — mostly migrated, CES tail remains |
| 100% | **Fully NES** — complete migration |

Baseline for comparison: **59.7% NES / 40.3% CES** across all new purchase orders (as of 2026-05-11).

---

## Step 4 — Check Known Context

1. Check `.claude/skills/surface-vocab/surface-vocab.md` for existing NES/CES classification for this ITC.
2. Check memory files for any known migration announcements or timelines for this product/surface.
3. Check `.claude/skills/tribal-knowledge/knowledge-log.md` for any TK entries about this surface's migration status.

If the live data contradicts a stored surface-vocab classification (e.g. surface-vocab says "CES" but NES% is now 70%), flag the discrepancy prominently.

---

## Step 5 — Render the Report

```
=== Migration Check: {ITC or product} ===
As of        : {today's date} (7-day window)
Total events : {N}

Architecture Breakdown
  True NES     : {N} ({pct}%)
  True CES     : {N} ({pct}%)
  Ghost IDs    : {N} ({pct}%) — excluded from NES%
  CES aliases  : {N} ({pct}%) — excluded from NES%

Migration Status : {status badge}

Baseline comparison : {surface NES%} vs 59.7% overall NES baseline
  {Above baseline | Below baseline | At baseline} by {N ppts}

Known classification (surface-vocab) : {stored NES/CES status, or "Not profiled"}
  {Match | ⚠ MISMATCH — live data shows {pct}% NES but surface-vocab says {stored}}

Tribal knowledge notes : {any relevant TK entries, or —}
```

For product-level runs (2B), show a breakdown by surface:

```
Per-Surface Breakdown
| ITC | Events | NES% | Status |
|-----|--------|------|--------|
| slp_wordpress       | 2,450 | 100% | Fully NES    |
| slp_wsb_*           |   830 |   0% | CES Only     |
| dpp_precheck        | 1,200 |  45% | NES in Progress |
```

---

## Step 6 — Offer-Pulse Implication

End with a one-line practical note:

- Fully NES: `Expect NES path output from /offer-pulse. Curated offer ID will be emitted.`
- CES Only: `Expect CES path output from /offer-pulse. No curated offer ID — merchandising package only.`
- NES in Progress: `Mixed output expected from /offer-pulse. Confirm which experiment arm this ticket targets (NES or CES) before filing EP ticket.`
- NES Starting: `Mostly CES still. /offer-pulse will likely route CES. Re-check migration status before each run — this surface is actively migrating.`
- Data discrepancy vs surface-vocab: `⚠ Surface classification in surface-vocab may be stale. Run /surface-vocab explore to refresh before relying on it.`

---

## Output Constraints

- Maximum 1 Redshift query (2A, 2B, or 2C — choose based on input type; do not run all three unless the analyst explicitly asks for all).
- Read-only. No file writes.
- If zero events in 7-day window: emit the zero-event block and suggest checking catalog directly for pre-launch NES status.
- Do not make migration timeline predictions. Report what the data shows today only.
