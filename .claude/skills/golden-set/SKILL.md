---
name: golden-set
description: Curate, promote, and query expected outputs for known offer-pulse test cases. The golden set is the oracle for /scorer and /batch-test — it contains analyst-confirmed correct answers. Read-only during test runs; writeable only by this skill.
---

# /golden-set — Test Oracle Curator

**One sentence:** This skill owns the expected-output store for all known offer-pulse test cases.

**What it does NOT do:**
- Run queries against Redshift
- Call catalog MCP tools
- Diagnose offer-pulse failures (take those to /wendy)
- Write log entries to use-case-log.md

---

## Invocation Modes

| Invocation | Action |
|-----------|--------|
| `/golden-set` | List all cases — table of case_id, path_type, surface, input_type, reliability, date added |
| `/golden-set add` | Interactive promote: prompts field-by-field and writes a new entry |
| `/golden-set N` | Show detail for the Nth entry in the list (1-indexed) |
| `/golden-set <case_id>` | Show full detail for a specific case_id (e.g. `/golden-set AGIGROWTH-161`) |
| `/golden-set promote <case_id>` | Promote a confirmed offer-pulse output to the golden set — structured intake from the analyst, then writes the entry |

---

## Data File

All entries live in `.claude/skills/golden-set/golden-set.md`.

**Read boundary:** /scorer and /batch-test read this file directly. /offer-pulse NEVER reads this file under any circumstances — the skill being tested must not have access to the oracle. If /offer-pulse ever loads this file during a run, that run is invalid.

**Write boundary:** Only this skill (/golden-set) writes to golden-set.md. All other skills are read-only consumers. Entries are append-only — historical entries are never modified after promotion.

---

## Entry Schema

Two path types are supported: NES and CES. The path_type field determines which expected fields are present.

### NES Entry

```
## {case_id}

case_id          : {e.g. AGIGROWTH-161}
input_type       : jira_ticket | itc | pfid
surface          : {ITC string, e.g. dpp_precheck}
path_type        : NES Standalone | NES Bundle
reliability      : stable | volatile | retired
date_added       : {YYYY-MM-DD}

expected:
  source_offer_slug  : {e.g. office365-tier1}
  source_offer_id    : {UUID, e.g. 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391}
  plan_name          : {e.g. onlineEssentialsNoTeams}
  pfid               : {numeric, e.g. 1768604}
  discount_code      : {code string | none}
  sale_price         : {e.g. $3.99/mo | unknown}
  list_price         : {e.g. $10.99/mo | unknown}
  term               : {annual | monthly | {N} Year | {N} Month}
  markets            : [{e.g. en-US, DEM}]
  what_changes       : [{e.g. pfid_swap, discount_code}]

ticket_ready:
  clone_source       : {slug}
  pfid_to_swap       : {numeric}
  discount_code      : {code | none}
  sale_price         : {e.g. $3.99/mo | unknown}
  surface            : {ITC}
```

### CES Entry

```
## {case_id}

case_id          : {e.g. CMS-33982}
input_type       : jira_ticket | itc | pfid
surface          : {ITC string}
path_type        : CES
reliability      : stable | volatile | retired
date_added       : {YYYY-MM-DD}

expected:
  packages:
    - package_name  : {slug | TBD (challenger)}
      special_config : {e.g. TrustedSite add-on, opt-in | none}
      rows:
        - product_name  : {e.g. TrustedSite}
          pfid_new      : {numeric}
          pfid_renewal  : {numeric | same}
          term          : {annual | monthly}
          tier          : {e.g. add-on | basic | deluxe}
          otc           : {Y | N}
          free_product  : {Y | N}
          existing_pkg  : {Y | N}
          discount_code : {code | N}
  geo              : {global | US | ROW | India | ...}

ticket_ready:
  rows:
    - product_name  : {same as expected.packages.rows}
      pfid_new      : {numeric}
      pfid_renewal  : {numeric | same}
      term          : {annual | monthly}
      tier          : {tier}
      otc           : {Y | N}
      free_product  : {Y | N}
      existing_pkg  : {Y | N}
      discount_code : {code | N}
```

**Field rules:**
- Use `unknown` (not blank) when a value is not yet confirmed by the analyst.
- `ticket_ready` is the scoring target for downstream ticket usability — it must mirror `expected.packages.rows` exactly for CES, or the key clone fields for NES.
- Do not compress multi-row bundles into a single row. One row per PFID × term.
- `reliability` controls whether the entry is included in automated overnight regression testing:
  - `stable` — deterministic output expected; included in `/batch-test stable` and overnight Phase 1c. Use for: NES cases with a single confirmed champion, CES cases where chain steps 2/3 only are tested (no WebFetch dependency).
  - `volatile` — output is non-deterministic or structurally dependent on a system constraint that cannot pass reliably (e.g. WebFetch truncation, A/B surface with two live champions, CES-only surface with no NES anchor). Excluded from automated loops; still runnable manually.
  - `retired` — no longer a valid test case (product discontinued, surface changed architecture). Excluded from all runs. Keep for historical record; never delete.
  - **Default for new entries with no field present:** treated as `volatile` by `/batch-test stable` and overnight.
  - Ask for `reliability` during `/golden-set add` and `/golden-set promote`. When in doubt, default to `volatile` — it is always safe to promote a case from volatile to stable, but a wrongly-stable case will produce false overnight alerts.

---

## Invocation Behaviors

### `/golden-set` — List

Read golden-set.md. Render a summary table:

| # | case_id | path_type | surface | input_type | reliability | date_added |
|---|---------|-----------|---------|------------|-------------|------------|

If the file does not exist or has no entries, print: "No entries in golden set yet. Use `/golden-set add` or save a confirmed run with `save <case_id>`."

---

### `/golden-set add` — Interactive Promote

Ask for each required field in a single block (not sequentially):

> "To add a new golden-set entry, please provide:
> 1. case_id (e.g. AGIGROWTH-161)
> 2. path_type: NES Standalone, NES Bundle, or CES?
> 3. surface (ITC string)
> 4. input_type: jira_ticket, itc, or pfid?
> 5. reliability: stable, volatile, or retired? (default: volatile — see field rules for guidance)
> 6. [NES only] source_offer_slug, source_offer_id, plan_name, pfid, discount_code, sale_price, list_price, term, markets, what_changes
> 6. [CES only] package_name, special_config, and rows (product_name, pfid_new, pfid_renewal, term, tier, otc, free_product, existing_pkg, discount_code); also geo
>
> Paste or type the values — I'll format them into the entry."

After collecting the values, preview the formatted entry to the analyst. Ask: "Does this look right? Reply 'confirm' to write it." Do not write until confirmed.

On confirmation, read golden-set.md (or create it with the header below), append the new entry, write the file.

---

### `/golden-set N` or `/golden-set <case_id>` — Detail

Read golden-set.md. Locate the requested entry. Render the full entry block verbatim — do not summarize or reformat.

If not found: "No entry found for '{value}'. Use `/golden-set` to list all case_ids."

---

### `/golden-set promote <case_id>` — Promote from Confirmed Run

This is the production path — called when the analyst types `save <case_id>` after a validated offer-pulse output.

1. Ask the analyst to paste the confirmed output fields (or accept them if already in context from the Validation Block exchange).
2. Apply any corrections the analyst stated during validation.
3. Ask: "Should this entry be `stable` or `volatile`? (stable = deterministic output expected, include in overnight regression; volatile = exclude from automated runs)" Default to `volatile` if the analyst doesn't specify.
4. Format into the schema above (NES or CES, based on path_type), including the `reliability` field.
5. Preview the entry.
6. Write to golden-set.md on confirmation.
7. Print: "Saved to golden set as {case_id} (reliability: {stable|volatile})."

Do not auto-promote without analyst preview and confirmation. The analyst must see the formatted entry before it is written.

---

## File Header

When creating golden-set.md for the first time:

```markdown
# Offer Pulse — Golden Set
<!-- append-only; analyst-confirmed expected outputs; read by /scorer and /batch-test; never read by /offer-pulse -->
<!-- schema: NES entries have expected.source_offer_slug + ticket_ready clone fields; CES entries have expected.packages rows + ticket_ready table -->
```
