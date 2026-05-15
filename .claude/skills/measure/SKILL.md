---
name: measure
description: Measures the improvement of a specific Wendy change by comparing pre-fix vs post-fix flag/error rates in the use-case log, then writes a measurement entry.
---

# /measure — Wendy Change Impact Measurement

Compares pre-fix vs post-fix performance for a specific Wendy change to the offer-pulse SKILL.md. Reads the use-case log, splits runs by fix date, computes improvement rates, and writes a measurement entry to the log.

**What to provide:**
- The name of the issue or flag Wendy fixed (e.g., "B0 term filter contamination", "CES ticket preview omitting Base Offer ID")
- Optionally: the fix date (YYYY-MM-DD). If omitted, the skill derives it from the log.

---

## Step 1 — Parse Input

From `$ARGUMENTS`, extract:
- **Issue keyword** — flag name, issue description, or gap title that Wendy fixed
- **Fix date** (optional) — if provided, use it directly; otherwise derive in Step 3

If `$ARGUMENTS` is empty:
1. Read `.claude/skills/offer-pulse/use-case-log.md`
2. Find all lines containing "Wendy fix applied", "fix applied to SKILL.md", or "Issue #N status : CLOSED" in Pulse Audit entries
3. Render them as a numbered list with dates and short descriptions
4. Ask the analyst: "Which change would you like to measure? (Reply with the number, or paste the issue description)"
5. Stop and wait for input.

---

## Step 2 — Read Source Files

Read both in parallel:
- `.claude/skills/offer-pulse/use-case-log.md`
- `.claude/skills/offer-pulse/SKILL.md`

---

## Step 3 — Locate the Fix Event

Search the log for the fix event matching the issue keyword:
- Scan `Notes`, `Flags fired`, `Issue #N status`, and `Top open issue` fields in every entry
- The fix date is the date of the Pulse Audit entry or run entry that says the Wendy fix was applied for this issue
- If the issue keyword matches a `Issue #N status : CLOSED` line, extract its date from the containing `## Pulse Audit` entry header

If multiple matches exist, use the most recent fix date. Announce which entry was used.

If no fix event is found:
```
No Wendy fix event found for "{keyword}" in the use-case log.
Run /use-cases → /wendy to create and apply a fix first, then re-run /measure.
```
Stop.

---

## Step 4 — Classify All Entries

For each entry in the log, classify it as one of:
- **Live run** — a normal `## Run ...` entry that is not an Assessment or Eval
- **Assessment/Eval** — date string contains `-ASSESS`, `-EVAL`, or `-BLIND` → **exclude from all counts**
- **Pulse Audit** — `## Pulse Audit ...` entry → exclude from run counts, but use for fix event dating
- **Wendy Measure** — a prior `/measure` entry → exclude from run counts

Then split live runs into:
- **Pre-fix** — dated strictly before the fix date
- **Post-fix** — dated on or after the fix date

---

## Step 5 — Identify In-Scope Runs

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

---

## Step 6 — Compute Metrics

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

---

## Step 7 — Render the Measurement Card

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
- `INCONCLUSIVE`: "Only {scope_post} post-fix run(s) in scope — run /offer-pulse on {scope description} cases, then re-run /measure."
- `NO CHANGE`: "Fix may not have addressed the root cause, or the issue has not recurred post-fix. Re-run /use-cases."
- `REGRESSION`: "Issue rate increased {abs(delta)} pp after fix. Investigate whether the fix introduced a new failure mode."
- `BASELINE MISSING`: "No pre-fix runs in scope — cannot establish a baseline. Measurement is not meaningful."

---

## Step 8 — Write the Log Entry

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

## Output Constraints

- Never suppress runs from the count. All in-scope live runs must be counted.
- Assessment/Eval/Blind entries (`-ASSESS`, `-EVAL`, `-BLIND` in the date) are never counted — they are not production runs.
- Ambiguous in-scope status: include the run and note the ambiguity in the Evidence list.
- Do not recommend SKILL.md changes. That is Wendy's job. Only report the measurement.
- If `scope_post = 0` (fix was just applied, no runs yet): verdict = INCONCLUSIVE. Log the entry with 0/0 and note the date the fix was applied.
- Prepend all entries to the log at the bottom (append-only). Never reorder existing entries.
