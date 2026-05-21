---
name: surface-vocab
description: Semantic ITC lookup and periodic refresh. Translates human surface names ("front of site", "checkout") to specific ITCs. Explore mode discovers new ITCs and flags NES/CES reclassifications. All 680 known ITCs are fully profiled.
---

# /surface-vocab — ITC Semantic Layer

**The problem it solves:** Users say "front of site" but mean `slp_wordpress` (or one of ~50 other slp_ variants). All 680 known ITCs are fully profiled with human labels, NES/CES classification, top packages, and champions. Explore mode detects new ITCs that have appeared in billing since the last run and flags any existing profiles where the NES/CES classification may have changed (e.g., a CES surface that has migrated to NES).

---

## Two modes

| Invocation | Mode |
|---|---|
| `/surface-vocab "term"` | **Lookup** — translate a human surface term to matching ITCs |
| `/surface-vocab explore` | **Explore** — find new ITCs + flag stale NES/CES classifications |
| `/surface-vocab` (no args) | **Summary** — show coverage stats and any pending updates |

---

## Vocab file

All knowledge lives at `.claude/skills/surface-vocab/surface-vocab.md`.

**Coverage state (as of 2026-05-16):** 680 ITCs fully profiled, 0 in bulk reference table. Every ITC has a `## [ITC]` heading with label, NES/CES classification, top packages, and champion.

An ITC is **fully profiled** only if a `## [ITC] {name}` heading exists. Explore mode detects new ITCs that have appeared in billing and flags profiles where NES/CES status may have changed.

---

## Key SQL facts

`pricing_experiment_dev.offer_pulse_experiment` is pre-aggregated. Use these column names:

| Concept | Column name |
|---|---|
| Surface code | `item_tracking_code` |
| Order volume | `SUM(total_orders)` — do NOT use COUNT(order_id) |
| Product | `product_pnl_line_name` |
| Package | `package_id` |
| PFID | `pf_id` |

`ba_site_app.itc_page_source` does not exist in this environment — always set `Page source : not mapped`.

Ghost packages to skip in catalog resolution: `redemption`, `nes-wss-tier0-nortonsmb-standardfreetrial`, `nes-wss-tier1-nortonsmb-standardfreetrial`, `nes-wss-tier2-nortonsmb-standardfreetrial`, `nes-cpanel-set-1-economy-ssl-365-wss-xtra`.

---

## MODE: Lookup

**Input:** A human surface term — e.g., "front of site", "checkout", "domain page", "hosting upgrade", "my account"

**Step 1 — Read vocab file**

Read `.claude/skills/surface-vocab/surface-vocab.md`.

**Step 2 — Match, full profiles first**

Search in priority order:
1. `## Prefix Group` human terms lists (broad match → return all ITCs in that prefix)
2. `Human label` field of `## [ITC]` entries (specific full-profile match)
3. `Products` field of `## [ITC]` entries (product-name match)
4. **Bulk table fallback** — if no full profile found, search the ITC name and Top Product column of the bulk reference table for the term

If multiple matches: return full-profile entries first, ranked by order volume. Bulk table matches appended at the bottom labeled **(bulk table — low confidence)**.

**Step 3 — Render results**

For full-profile matches: render the labeled record block. For bulk table matches: render the table row with a note that full profiling is pending.

Append at the bottom:
```
Full profiles: {N of 675}. Run /surface-vocab explore to promote more.
```

If zero matches:
```
"{term}" not found in surface vocabulary.
Closest prefix match: {prefix group name, or "none"}

Run /surface-vocab explore or provide a Jira ticket / PFID and offer-pulse will
discover the correct ITC from transaction data.
```

---

## Naming Pattern Hints

Use these to interpret an unfamiliar ITC before querying:

| Pattern in ITC slug | Meaning |
|---|---|
| `_f2p_` | Free-to-paid conversion → CES |
| `_p2p_` | Paid-to-paid plan change → CES |
| `_d2p_` | Domain-to-product in-app journey → CES |
| `_config` | Configuration step in a flow → usually CES |
| `_reoffer` | Re-offer / alternative suggestion step → CES |
| `.primary_exact`, `.primary_organicspin`, `.primary_tldcard`, `.primary_paidspin` | dpp_absol1 or mya_dom_srch experiment routing suffix → NES domain family |
| `.unavailable_*`, `.aftermarket_*`, `.smartdefault_*` | dpp_absol1 or mya_dom_srch experiment routing suffix → NES domain family |
| `_365`, `_o365` | M365 email surface → typically CES |
| `_wordpress`, `_mwp` | Managed WordPress surface → check CLN; may be NES |
| `temp-` prefix in a package_id | Live production champion — not a test artifact |

If an ITC is not matched by any of the above: query CLN directly for package_id null-rate to determine NES/CES routing. Never block execution on a vocab miss.

### Prefix Fallback (for ITCs not matching any full profile)

When an ITC is not found in the vocab file, use this table to determine expected NES/CES routing before querying CLN:

| ITC prefix / pattern | Surface family | Expected NES/CES | Guidance |
|---|---|---|---|
| `slp_*` | Sales Landing Page (SLP) | Mixed — check CLN | Hosting (4GH, MWP, Pro MWP) and SSL are NES. M365, WAM, and most others are CES. Query CLN for package_id null-rate to confirm. |
| `slp-*` (hyphen), `hmc_*`, `lp_*`, `plp_*`, `mlp_*`, `_lp` suffix | SLP-family variants | Mixed — check CLN | Same routing logic as `slp_*`. Check CLN for package_id presence before assuming CES. |
| `dpp_*` with `.primary_*`, `.unavailable_*`, `.aftermarket_*`, `.smartdefault_*` suffix | Domain checkout experiment variant | NES | dpp_absol1 family — same domain champion. |
| `dpp_*` without experiment suffix | Domain checkout step | CES | `_config`, `_reoffer`, `_transfers` variants are CES add-on or re-offer steps. |
| `_dpp` suffix / contains, `bulk_search` exact | Domain Purchase Path non-prefix variants | Mixed — check CLN | These route to the DPP group. Query CLN for package_id null-rate. |
| `dlp_*` | Domain Landing Page (DLP) | NES (typically) | Standard domain family. Confirm via CLN. |
| `upp_*` | Upsell / Upgrade Path (UPP) | CES | 100% CES. No NES migration planned. Skip curated offer resolution. |
| `mya_*` | My Account (MYA) | Mixed | `mya_dom_srch.*` variants are NES (domain). `mya_acctsettings_*` and renewal flows are CES. |
| `renewal` contains, `mui_*` | My Account — renewal / UI extension | CES | Covers `account_myrenewals_*`, `single_product_renewal`, `mui_*` — all MYA group, all CES. |
| `dcc` contains, `whois_serp*`, `whoisserp*` | Domain Control Center (DCC) | Mixed | `dcc` is a **contains** match. Domain search surfaces are NES; portfolio renewal and DOP flows are CES. **Do not confuse with `ddc_*`** (Domain Discount Club — separate group below). |
| `ddc_*` | Domain Discount Club (DDC) | CES | Distinct from DCC. All DDC surfaces are CES. |
| `cart_*`, `misc-purchase` contains, `xsell` contains | Cart (CART) | Mixed | NES for domain-search cart boxes. CES for inline cross-sells (`cart_xsells_inline`, `misc-purchase`). |
| `vh_*`, `ai_onboarding_*`, `airohq*`, `dpp_bundling_is` exact | Venture Home (VH) | CES | AGI-managed. Not on NES migration path. Skip curated offer resolution. |
| `hp_*` | Homepage Quickbuy (HP) | Mixed — check CLN | Performance marketing. Query CLN for package_id presence. |
| `mgr_*`, `crm_*`, `shared_shopping_service` exact | C3 Sales Site / Reseller | CES | Internal sales tool surfaces — all CES. |
| `pro_*`, `wp_*` | GoDaddy Pro / Web Pro Microsite | CES | `wp_` = Web Pro microsite (NOT WordPress). All CES. For WordPress hosting surfaces use `slp_wordpress`, `dlp_wordpress_*`, etc. |
| `mui_*` | My Account UI extension | CES | Part of the MYA group. |
| `app_*` | In-app product surface (GDAPP) | CES | In-product upgrade / add-user flows — all CES. |
| `studio_*`, `android_*`, `ios_*`, `mob_*` | GDAPP — Mobile / Studio | CES | GoDaddy mobile apps and Studio. All CES. |
| `am_*`, `parked` contains, `tdfs` contains, `buynow` contains | Aftermarket (AM) | n/a | Cash-parking and marketplace surfaces. Not standard purchase surfaces. Do not attempt offer resolution. |
| `auction_*`, `gdc_*` | After Checkout Special (ACS) | CES | Post-checkout surfaces. Rarely the target for curated offer creation. |
| `gocentral` contains | P&C — Website Builder (GoCentral / vNext) | CES | Classic website builder surfaces. Distinct from current WAM product. |
| `netgdpipeline_*`, `dna_*` | Internal pipeline / aftermarket | n/a | Not customer-facing purchase surfaces. Do not attempt offer resolution. |

---

## MODE: Explore

**Pre-requisites:**
- `execute_query` (Redshift) must be allowed
- `mcp__catalog-mcp-dev__*` must be allowed

**Purpose:** Two tasks per run — (1) discover new ITCs that have appeared in billing since the last explore, (2) spot-check existing profiles where the NES/CES classification may have changed.

**Step 1 — Read vocab file**

Read `.claude/skills/surface-vocab/surface-vocab.md`. Extract all ITC names from `## [ITC]` headings into a set: `{profiled_itcs}`.

**Step 2 — Find new ITCs (not yet in vocab)**

```sql
SELECT
    item_tracking_code                                          AS itc,
    SUM(total_orders)                                          AS order_count,
    MAX(CASE WHEN package_id IS NOT NULL
             AND package_id NOT IN (
                 'redemption',
                 'nes-wss-tier0-nortonsmb-standardfreetrial',
                 'nes-wss-tier1-nortonsmb-standardfreetrial',
                 'nes-wss-tier2-nortonsmb-standardfreetrial',
                 'nes-cpanel-set-1-economy-ssl-365-wss-xtra'
             ) THEN 'NES' END)                                 AS has_nes,
    COUNT(DISTINCT pf_id)                                      AS distinct_pfids
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE item_tracking_code NOT IN ({comma-separated quoted list of profiled_itcs})
  AND (
      item_tracking_code LIKE 'slp_%'
   OR item_tracking_code LIKE 'dpp_%'
   OR item_tracking_code LIKE 'dlp_%'
   OR item_tracking_code LIKE 'upp_%'
   OR item_tracking_code LIKE 'mya_%'
   OR item_tracking_code LIKE 'dcc_%'
   OR item_tracking_code LIKE 'dpp-%'
   OR item_tracking_code LIKE 'dlp-%'
   OR item_tracking_code LIKE 'mena-%'
  )
GROUP BY item_tracking_code
ORDER BY order_count DESC
LIMIT 10
```

If this returns 0 rows: no new ITCs found — skip to Step 4.

If it returns rows: these are new ITCs to profile this run (up to 10).

**Step 3 — Profile each new ITC**

Run 3a and 3b in parallel for each new ITC.

**3a — Product profile**
```sql
SELECT
    product_pnl_line_name,
    package_id,
    SUM(total_orders) AS orders
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE item_tracking_code = '{itc}'
GROUP BY 1, 2
ORDER BY orders DESC
LIMIT 10
```

**3b — Skip page source** — `ba_site_app.itc_page_source` does not exist. Set `Page source : not mapped` for all entries.

**3c — NES package resolution** (only if `has_nes = 'NES'`)

For each distinct non-null, non-ghost package_id from 3a: call `get_curated_offer` (datasource: `catalog-curated-offers`). Run calls in parallel.

**Classify each ITC:**

| Field | How to determine |
|---|---|
| **Prefix group** | First segment before `_` → look up in prefix crosswalk |
| **Human label** | Combine ITC slug tokens + product_pnl_line_name into plain English |
| **Products** | Distinct product_pnl_line_names with % share from 3a |
| **NES/CES** | `has_nes` + catalog resolution → `NES`, `CES`, or `Mixed` |
| **Top packages** | Top 3 package_ids by order count from 3a |
| **Champion** | If NES and top package resolved in catalog, note curatedOfferId → offerId |
| **Volume** | SUM(total_orders): ≥10K = High, 1K–10K = Medium, <1K = Low |

Append new `## [ITC]` entries to the Individual ITC Profiles section and update the header stats.

**Step 4 — NES/CES reclassification sweep (runs every time, even when no new ITCs)**

Sample the 20 highest-volume ITCs currently profiled as `CES` or `CES (NES in progress)` and re-query for non-null package_ids in the last 7 days:

```sql
SELECT
    item_tracking_code                                          AS itc,
    MAX(CASE WHEN package_id IS NOT NULL
             AND package_id NOT IN (
                 'redemption',
                 'nes-wss-tier0-nortonsmb-standardfreetrial',
                 'nes-wss-tier1-nortonsmb-standardfreetrial',
                 'nes-wss-tier2-nortonsmb-standardfreetrial',
                 'nes-cpanel-set-1-economy-ssl-365-wss-xtra'
             ) THEN 'NES' END)                                 AS has_nes_now,
    SUM(CASE WHEN package_id IS NOT NULL
             AND package_id NOT IN (
                 'redemption',
                 'nes-wss-tier0-nortonsmb-standardfreetrial',
                 'nes-wss-tier1-nortonsmb-standardfreetrial',
                 'nes-wss-tier2-nortonsmb-standardfreetrial',
                 'nes-cpanel-set-1-economy-ssl-365-wss-xtra'
             ) THEN total_orders ELSE 0 END)                   AS nes_orders,
    SUM(total_orders)                                          AS total_orders
FROM pricing_experiment_dev.offer_pulse_experiment
WHERE item_tracking_code IN ({top 20 CES-profiled ITCs by volume})
  AND bill_modified_mst_date >= DATEADD(day, -7, CURRENT_DATE)
GROUP BY item_tracking_code
```

For any ITC where `has_nes_now = 'NES'` but the current profile says `CES`:
- Flag it: `RECLASSIFICATION NEEDED: {ITC} is now showing NES package_ids in billing — profile says CES`
- Do NOT auto-update the profile — emit the flag and let the analyst decide whether to re-profile
- The analyst can re-run the profile steps (3a/3b/3c) for the flagged ITC to update it

**Step 5 — Update vocab file header**

Update:
- `Last updated : {YYYY-MM-DD}`
- `ITCs explored : {N} of {N} (100%)` if no new ITCs; or `{N} of {N+new}` if new ITCs added

**Step 6 — Session output**

```
## surface-vocab — Explore complete

New ITCs found: {N} (profiled and added) | 0 (none found — vocab is current)
  - {itc}  → {human label} ({NES/CES}, {volume tier})

Reclassification flags: {N}
  - {ITC}: profiled as CES, now showing NES package_ids — re-profile to update
  | "none — all sampled CES profiles still current"

Total fully profiled: {N} ITCs
Last updated: {YYYY-MM-DD}
```

---

## MODE: Summary

Read `.claude/skills/surface-vocab/surface-vocab.md`. Output:

```
## Surface Vocabulary — Coverage Summary

Total ITCs    : 675
Full profiles : {N} ({pct}%)
Bulk table    : {617 - promoted} (low-confidence labels, promotion queue)
Last updated  : {date}

Full profiles by prefix group:
  slp_  : {N}  (Front of Site — Sales Landing Pages)
  dpp_  : {N}  (Domain Purchase Path)
  dlp_  : {N}  (Domain Landing Page)
  upp_  : {N}  (Upsell / Upgrade Path)
  mya_  : {N}  (My Account)
  dcc_  : {N}  (Domain Control Center)
  other : {N}  (non-standard prefixes)

Top unprofiled by volume (promotion queue):
  1. {itc} — {orders} orders, {NES/CES}
  2. ...
  (run /surface-vocab explore to promote these to full profiles)
```

---

## Integration with offer-pulse

When `/offer-pulse` receives a human surface description (not a raw ITC):
1. Read `.claude/skills/surface-vocab/surface-vocab.md`
2. Search `Human label` and `Products` fields of full-profile entries first
3. Fall back to bulk table Top Product column
4. Return matching ITC(s) before running the offer audit

When `/offer-pulse` encounters an ITC that only has a bulk table entry (no full profile), note it in the output as **surface label confidence: low** and suggest running `/surface-vocab explore` for that ITC.

---

## Output constraints

- Never truncate results
- Catalog calls: skip known ghost package IDs (list above)
- Human labels: plain English, no acronyms, no internal codes
- Volume counts: always include "as of YYYY-MM-DD" — counts drift as data accumulates
- Label confidence: mark bulk table results as low confidence; full profiles are trusted
