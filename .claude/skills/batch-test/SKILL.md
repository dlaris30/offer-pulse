---
name: batch-test
description: Run a list of offer-pulse test cases in isolation and score each against the golden set. Each case gets a fresh, sandboxed offer-pulse agent with no access to expected answers, memory files, or prior runs.
---

# /batch-test — Isolated Batch Test Runner

**One sentence:** Spawn isolated offer-pulse agents for a list of cases, collect outputs, score each against the golden set, and produce a batch report.

**What it does NOT do:**
- Read expected values from golden-set.md before agents run (that is scorer's job — isolation must be preserved)
- Pass any expected-answer context to offer-pulse agents
- Read use-case-log.md, memory files, or any other context files before spawning agents
- Make any judgment about correctness — that is scorer's job

---

## Isolation Guarantee

This is the core invariant. Every offer-pulse agent spawned by batch-test receives **only**:

1. The full content of `/offer-pulse SKILL.md`
2. The raw input string for that case (Jira ticket key, ITC, or PFID — nothing else)

**Never passed to agents:**
- golden-set.md or any expected outputs
- use-case-log.md or prior run history
- Memory files or session context
- Scorer SKILL.md or any scoring criteria
- Any other batch-test case inputs or outputs

If isolation is broken, the run is invalid. Stop and tell the analyst before proceeding.

---

## Invocation

```
/batch-test [case_id_1] [case_id_2] ...
/batch-test all
/batch-test stable
```

- Pass one or more case_ids from the golden set (e.g. `/batch-test AGIGROWTH-161 CMS-33982`)
- Or `/batch-test all` to run every entry in golden-set.md
- Or `/batch-test stable` to run only entries where `reliability: stable` — this is the mode used by the overnight regression gate
- Cases not in the golden set can still be run — they will be scored "No expected values on file" and excluded from the pass rate

---

## Execution Flow

### Step 1 — Load case list

Read `.claude/skills/golden-set/golden-set.md` to get the raw input for each case_id. The `input_type` field determines what string to pass to offer-pulse:

| input_type | raw input to pass | example |
|---|---|---|
| `jira_ticket` | The case_id itself (it IS the ticket key) | `AGIGROWTH-161` |
| `itc` | The case_id itself (it IS the ITC string) | `dpp_precheck` |
| `pfid` | The case_id itself (it IS the numeric PFID) | `1768604` |

**If invoked with `/batch-test stable`:** filter the case list to entries where `reliability: stable`. Entries with no `reliability` field present are treated as `volatile` (excluded). Print the filtered count before spawning: `Running stable-only batch: {N} of {M} total golden-set entries`.

**Stop after reading the case list.** Do not read expected values, expected fields, or ticket_ready blocks. The only information needed from golden-set at this step is: case_id → what raw input string to pass (and `reliability` when filtering).

### Step 2 — Spawn isolated agents

For each case, spawn a subagent using the Agent tool with:
- **Prompt:** The full text of offer-pulse SKILL.md followed by: `\n\nRun /offer-pulse for the following input and produce the complete output:\n\n{raw_input}`
- **No additional context.** No memory. No golden-set. No log.

Run agents in parallel where the case count is small (≤5). For larger batches, run in groups of 5 to avoid overwhelming the session.

### Step 3 — Collect outputs

After each agent completes, capture the full offer-pulse output text. Label each with its case_id.

**Strip the Validation Block** before passing to scorer: remove everything from the `---\n## Validation` marker to the end of the output. The Validation Block is analyst-facing and must not be included in the scored output — scorer scores only the offer analysis content above it.

### Step 4 — Score each case

For each case, invoke `/scorer` with:
- The case_id (scorer will look up expected values from golden-set independently)
- The captured offer-pulse output

Collect the Score Card for each case.

### Step 5 — Render batch report

### Step 6 — Golden Set Coverage

After all agents have completed and scores are collected, invoke the `/golden-set` skill by reading and following `.claude/skills/golden-set/SKILL.md` with no arguments (list mode).

From the list output, compute:
- `total_oracle` — total entries in the golden set
- `tested` — entries that were run in this batch
- `untested` — case_ids in the golden set that were NOT included in this batch run

Append a Coverage section at the end of the batch report (below Patterns). The isolation guarantee is not affected — all agents have already completed before this step.

---

## Batch Report Format

```
## Batch Test Report — {YYYY-MM-DD}

Mode      : {all | stable-only | {case_ids}}
Cases run : {N}
Pass      : {P} ({P/N}%)
Fail      : {F}
No oracle : {cases with no golden-set entry}

---

### Results

| # | case_id | Path | Score | Result | Top failure |
|---|---------|------|-------|--------|-------------|
| 1 | AGIGROWTH-161 | NES Standalone | 5/5 | ✓ PASS | — |
| 2 | CMS-33982 | CES | 4/7 | ✗ FAIL | C2: PFID mismatch |
| ...

---

### Failures

For each failed case, paste the full Score Card from /scorer inline.

---

### Patterns

{If 2+ failures share the same criterion, call it out here — e.g. "3/4 failures on C2 (PFID) suggest a systematic data query issue."}
{If no patterns: "No systematic patterns detected."}

---

### Coverage

Coverage  : {N tested} of {M total} golden-set entries run in this batch
Not run   : {list of case_ids not included, or "all entries covered"}

---

> No files changed. Take failure patterns to `/wendy` to update the skill.
```

---

## Pass/Fail Definition

- **PASS:** All non-`~` criteria are ✓ (score = M/M where M is the verifiable denominator)
- **FAIL:** Any non-`~` criterion is ✗
- **No oracle:** case_id not found in golden-set.md — excluded from pass rate, shown in "No oracle" count

---

## After the Report

The batch report is read-only output. batch-test does not:
- Write to use-case-log.md
- Write to golden-set.md
- Propose skill changes

If failures show a pattern, tell the analyst: "Take this to `/wendy` with the failure pattern."
If a no-oracle case produced good output, tell the analyst: "Use `save {case_id}` at the end of the individual offer-pulse run to promote it to the golden set."
