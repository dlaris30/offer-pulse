---
name: ledger
description: Two-mode skill. Mode A (Pre-flight) — devil's advocate check before Wendy designs a fix; reads the use-case log for prior attempts and contradiction risks. Mode B (Measurement) — measures the improvement of a specific Wendy change by comparing pre-fix vs post-fix flag/error rates in the use-case log, then writes a measurement entry.
---

# /ledger — Wendy Change Ledger

Two modes, clearly separated. Wendy calls Mode A before designing a fix. An analyst (or the /overnight skill) calls Mode B after post-fix runs have accumulated.

**What to provide:**
- **Mode A (Pre-flight):** A candidate issue description — the thing Wendy is about to fix (e.g., "B0 term filter contamination", "silent candidate filtering"). No fix date needed.
- **Mode B (Measurement):** The name of the issue or flag Wendy fixed (e.g., "B0 term filter contamination", "CES ticket preview omitting Base Offer ID") and optionally the fix date (YYYY-MM-DD).

**Mode is determined by the caller:**
- If invoked by `/wendy` as a pre-flight check → **Mode A**
- If invoked directly by an analyst or by `/overnight` after runs have accumulated → **Mode B**
- If `$ARGUMENTS` contains "pre-flight" or "mode a" → **Mode A**
- Otherwise → **Mode B** (default)

---

## Mode A — Pre-flight (Devil's Advocate)

Wendy invokes this mode before beginning any fix design. It is read-only. It does not write log entries.

### A1 — Parse Input

Extract the candidate issue description from `$ARGUMENTS`. This is the plain-language description of what Wendy is about to change (e.g., "B0 term filter contamination" or "silent candidate filtering").

If the description is absent or unclear, ask: "What is the candidate issue Wendy is about to address?" and stop.

### A2 — Read Source Files

Read both in parallel:
- `.claude/skills/offer-pulse/use-case-log.md`
- `.claude/skills/offer-pulse/SKILL.md`

### A3 — Scan for Prior Attempts

In the use-case log, locate all entries with `Audit type : wendy-measure` (i.e., `## Wendy Measure` entries).

For each `## Wendy Measure` entry, extract:
- `Change` field — description of what was fixed
- `Fix applied` field — the fix date
- `Verdict` field — the outcome (FIXED, IMPROVED, PARTIAL, INCONCLUSIVE, NO CHANGE, REGRESSION, BASELINE MISSING)

Score each entry against the candidate issue description using keyword overlap:
- Match on: issue name fragments, flag names, scope filter terms, specific field names mentioned, surface prefixes, or path labels (NES/CES/B0/Chain Step/etc.)
- A match requires at least one specific term in common (not just generic words like "fix" or "issue")

Collect all matching entries as **prior attempts**.

### A4 — Contradiction Check

Compare the proposed fix direction (as described in the candidate issue) against the SKILL.md to determine what the fix would change or add.

Then check: does the candidate fix direction appear to **undo, reverse, or remove** logic that was installed by a prior fix with a FIXED or IMPROVED verdict?

Contradiction signals to look for:
- A prior fix added a filter → candidate fix removes or loosens that filter
- A prior fix added a guard or flag → candidate fix removes or conditions away that guard
- A prior fix changed a resolution path → candidate fix changes the same path in the opposite direction
- A prior fix restricted a scope → candidate fix broadens the same scope

If a contradiction is detected, name it explicitly: "This candidate fix would undo [prior fix description], which produced a [verdict] verdict on [fix date]."

### A5 — Render the Conflict Report

**If no prior attempts and no contradictions:**

```
Ledger Pre-flight: CLEAR

No prior attempts found matching "{candidate issue description}".
No contradictions detected.
Proceed.
```

**If findings exist**, render the full Conflict Report:

```
Ledger Pre-flight: FINDINGS

Candidate issue: {candidate issue description}

--- Prior Attempts ---

{For each matching wendy-measure entry:}
  Change    : {change description from log}
  Fix date  : {fix date}
  Verdict   : {verdict}

--- Contradiction Check ---

{Either: "No contradiction detected." }
{Or:     "CONFLICT: This candidate fix would undo [prior fix description] (fix date: [date], verdict: [verdict]). [One-sentence explanation of the reversal.]" }

--- Recommendation ---

{One of:}
  "Proceed with caution — review prior attempt(s) above before finalizing fix direction."
  "Do not re-open — prior fix for this issue produced a FIXED verdict. Confirm the issue has genuinely recurred before making changes."
  "Contradiction detected — reconcile the conflict before proceeding."
```

**Verdict-specific guidance for the Recommendation line:**
- Any prior attempt with verdict FIXED or IMPROVED: "Do not re-open — prior fix produced a [verdict] verdict."
- Any prior attempt with verdict INCONCLUSIVE: note as context only, do not block — "Note: prior attempt was INCONCLUSIVE; treat as weak prior evidence."
- Any prior attempt with verdict BASELINE MISSING: treat as no prior evidence — proceed as if no prior attempt.
- Any prior attempt with verdict PARTIAL, NO CHANGE, or REGRESSION: "Proceed — prior attempt did not fully resolve this issue."
- Contradiction (regardless of prior verdicts): always add "Contradiction detected — reconcile the conflict before proceeding."

### A6 — Mode A Output Constraints

- Mode A is **read-only**. Never write to any file.
- Never run queries. Never compute flag rates. Never classify log entries by pre/post — that is Mode B work.
- If a prior wendy-measure entry has a BASELINE MISSING verdict, exclude it from the prior attempts list (it is not evidence).
- Keep the Conflict Report under 30 lines. If there are more than 5 prior attempts, show the 3 most recent and note "N additional prior attempts exist — all with [verdict summary]."

---

## Mode B — Measurement (Post-run)

Compares pre-fix vs post-fix performance for a specific Wendy change to the offer-pulse SKILL.md. Reads the use-case log, splits runs by fix date, computes improvement rates, and writes a measurement entry to the log.

### B1 — Parse Input

From `$ARGUMENTS`, extract:
- **Issue keyword** — flag name, issue description, or gap title that Wendy fixed
- **Fix date** (optional) — if provided, use it directly; otherwise derive in Step B3

If `$ARGUMENTS` is empty:
1. Read `.claude/skills/offer-pulse/use-case-log.md`
2. Find all lines containing "Wendy fix applied", "fix applied to SKILL.md", or "Issue #N status : CLOSED" in Pulse Audit entries
3. Render them as a numbered list with dates and short descriptions
4. Ask the analyst: "Which change would you like to measure? (Reply with the number, or paste the issue description)"
5. Stop and wait for input.

### B2 — Read Source Files

Read both in parallel:
- `.claude/skills/offer-pulse/use-case-log.md`
- `.claude/skills/offer-pulse/SKILL.md`

### B3 — Locate the Fix Event

Search the log for the fix event matching the issue keyword:
- Scan `Notes`, `Flags fired`, `Issue #N status`, and `Top open issue` fields in every entry
- The fix date is the date of the Pulse Audit entry or run entry that says the Wendy fix was applied for this issue
- If the issue keyword matches a `Issue #N status : CLOSED` line, extract its date from the containing `## Pulse Audit` entry header

If multiple matches exist, use the most recent fix date. Announce which entry was used.

If no fix event is found:
```
No Wendy fix event found for "{keyword}" in the use-case log.
Run /use-cases → /wendy to create and apply a fix first, then re-run /ledger.
```
Stop.

### B4 — Classify All Entries

For each entry in the log, classify it as one of:
- **Live run** — a normal `## Run ...` entry that is not an Assessment or Eval
- **Assessment/Eval** — date string contains `-ASSESS`, `-EVAL`, or `-BLIND` → exclude from all counts
- **Pulse Audit** — `## Pulse Audit ...` entry → exclude from run counts, but use for fix event dating
- **Wendy Measure** — a prior `/ledger` entry (or legacy `/measure` entry) → exclude from run counts

Then split live runs into:
- **Pre-fix** — dated strictly before the fix date
- **Post-fix** — dated on or after the fix date

### B5 — Identify In-Scope Runs

Determine which runs **could have triggered the issue** being measured. Apply scope rules based on the issue type:

| Issue type | Scope filter |
|---|---|
| CES ticket preview field | Runs where `Ticket preview : Requested` AND `NES/CES branch` contains `CES` |
| B0 filter (term/segment/etc.) | Runs where B0 was executed: `NES/CES branch` is not `NES — 100%` |
| NES path issues | Runs where `NES/CES branch` contains `NES` |
| Champion not found | All runs where the issue could arise (all runs) |
| Flag-specific | Runs where the scenario triggering that flag is plausible from the log context |

If scope cannot be narrowed from the issue description, include all live runs in both groups.

Note the scope filter used explicitly in the output.

Count:
- `scope_pre` — pre-fix live runs in scope
- `triggered_pre` — pre-fix in-scope runs where the flag was fired or the issue symptom appears in `Notes` or `Flags fired`
- `scope_post` — post-fix live runs in scope
- `triggered_post` — post-fix in-scope runs where the flag or symptom still appears

### B6 — Compute Metrics

```
Rate before fix : triggered_pre  / scope_pre  × 100  (%)
Rate after fix  : triggered_post / scope_post × 100  (%)
Delta           : rate_before − rate_after  (percentage points improvement; negative = regression)
```

**Verdict rules** (apply top-to-bottom, first match wins):

| Condition | Verdict |
|---|---|
| `scope_pre = 0` | BASELINE MISSING — cannot measure without pre-fix evidence |
| `scope_post < 2` | INCONCLUSIVE — not enough post-fix runs |
| `rate_after = 0` and `scope_post ≥ 2` | FIXED |
| `delta ≥ 30 pp` | IMPROVED |
| `delta > 0` and `delta < 30 pp` | PARTIAL |
| `delta = 0` | NO CHANGE |
| `delta < 0` | REGRESSION |

### B7 — Render the Measurement Card

Output this block exactly. Never truncate the run lists.

```
## Wendy Change Measurement

Change           : {issue description}
Fix applied      : {fix date}
Scope filter     : {what counted as "in scope" — one line}

Pre-fix runs     : {scope_pre} in scope, {triggered_pre} triggered ({rate_before}%)
Post-fix runs    : {scope_post} in scope, {triggered_post} triggered ({rate_after}%)
Delta            : {delta} pp
Verdict          : {FIXED | IMPROVED | PARTIAL | INCONCLUSIVE | NO CHANGE | REGRESSION | BASELINE MISSING}
```

Then list the evidence:

**Pre-fix triggers** (runs that exhibited the issue):
- {date} — {one-line summary from Notes or Flags fired}
- ... (all of them; never truncate)

**Post-fix triggers** (runs where issue recurred after fix):
- {date} — {one-line summary}  ← if none, write "none"

**Verdict note:**
- `FIXED`: "Issue has not recurred across {scope_post} eligible post-fix runs."
- `IMPROVED`: "Issue rate dropped {delta} pp. {triggered_post} recurrence(s) remain — consider a follow-up /use-cases."
- `PARTIAL`: "Issue rate improved only {delta} pp — fix may be incomplete. Consider re-running /use-cases to refine."
- `INCONCLUSIVE`: "Only {scope_post} post-fix run(s) in scope — run /offer-pulse on {scope description} cases, then re-run /ledger."
- `NO CHANGE`: "Fix may not have addressed the root cause, or the issue has not recurred post-fix. Re-run /use-cases."
- `REGRESSION`: "Issue rate increased {abs(delta)} pp after fix. Investigate whether the fix introduced a new failure mode."
- `BASELINE MISSING`: "No pre-fix runs in scope — cannot establish a baseline. Measurement is not meaningful."

### B8 — Write the Log Entry

If verdict is `BASELINE MISSING`: do not write a log entry. Inform the analyst: "No log entry written — baseline is empty."

Otherwise append to `.claude/skills/offer-pulse/use-case-log.md`:

```
## Wendy Measure — {YYYY-MM-DDThh:mm} — {issue short title}

Date             : {timestamp}
Audit type       : wendy-measure
Change           : {issue description}
Fix applied      : {fix date}
Scope filter     : {scope description}
Pre-fix rate     : {triggered_pre}/{scope_pre} ({rate_before}%)
Post-fix rate    : {triggered_post}/{scope_post} ({rate_after}%)
Delta            : {delta} pp
Verdict          : {verdict}
Notes            : {one-line interpretation, or "none"}

```

After writing, confirm: `Measurement logged.`

---

## Output Constraints (Both Modes)

- Mode A is read-only — never writes any file.
- Mode B never suppresses runs from the count. All in-scope live runs must be counted.
- Assessment/Eval/Blind entries (`-ASSESS`, `-EVAL`, `-BLIND` in the date) are never counted — they are not production runs.
- Legacy `/measure` log entries (written before this skill was renamed) are treated identically to `/ledger` entries in both modes.
- Ambiguous in-scope status (Mode B): include the run and note the ambiguity in the Evidence list.
- Do not recommend SKILL.md changes. That is Wendy's job. Only report findings (Mode A) or measurements (Mode B).
- If `scope_post = 0` in Mode B (fix was just applied, no runs yet): verdict = INCONCLUSIVE. Log the entry with 0/0 and note the date the fix was applied.
- Append-only to the log. Never reorder existing entries.
