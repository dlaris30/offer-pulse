---
name: use-cases
description: Reads the offer-pulse use-case log, analyzes patterns across all logged runs, compares against the current SKILL.md, and flags systemic issues. Ends with a Wendy-ready brief for the top issue.
---

# /use-cases — Offer Pulse Systemic Issue Analyzer

Read-only. Does not run queries, call catalog tools, or modify any files. Produces a diagnostic report and a Wendy handoff brief.

---

## Step 1 — Read the Log

Read `.claude/skills/offer-pulse/use-case-log.md`.

If the file does not exist or contains fewer than 3 run entries, output:

```
Not enough runs to analyze yet.
Run /offer-pulse a few more times, then come back.
```

Stop. Do not continue.

---

## Step 2 — Read the Skill

Read `.claude/skills/offer-pulse/SKILL.md`.

You need this to:
- Cross-reference which scenarios the skill claims to handle
- Identify instructions that may be missing, ambiguous, or contradicted by the log

---

## Step 3 — Parse and Compute Summary Statistics

From the log entries, extract the following counts. Show all as absolute numbers and percentages.

| Metric | Value |
|---|---|
| Total runs | N |
| Date range | {first entry date} to {last entry date} |
| Path A (Curated Offer) | N ({pct}%) |
| Path B (Pricing/Discount) | N ({pct}%) |
| NES path (Path A) | N ({pct}% of Path A runs) |
| CES path (Path A) | N ({pct}% of Path A runs) |
| Mixed NES/CES (Path A) | N ({pct}% of Path A runs) |
| PFID Inventory mode (Path B) | N ({pct}% of Path B runs) |
| Blast Radius mode (Path B) | N ({pct}% of Path B runs) |
| Champion found | N ({pct}%) |
| Champion not found / NET-NEW BUILD | N ({pct}%) |
| Ticket preview requested | N ({pct}%) |
| Runs with Notes ≠ "none" | N ({pct}%) |

**Flag distribution** — count every flag name across all "Flags fired" fields and rank by frequency:

| Flag Name | Times Fired | % of Runs |
|---|---|---|

**Gate dimension ask frequency** — count how often each dimension appeared in "Gate asked" fields:

| Dimension | Times Asked | % of Runs |
|---|---|---|

**Entry type distribution:**

| Entry Type | Count | % of Runs |
|---|---|---|

---

## Step 4 — Detect Systemic Patterns

Apply these detection rules. Every triggered rule is a candidate systemic issue. Collect all that trigger.

### Detection Rules

| Rule | Trigger condition | Default threshold |
|---|---|---|
| **High CES rate** | CES path > 40% of Path A runs | >40% |
| **Low champion-found rate** | Champion not found > 20% of all runs | >20% |
| **Frequent Term question** | Term asked in > 60% of runs | >60% |
| **Frequent Market question** | Market asked in > 60% of runs | >60% |
| **CES chain exhausted repeatedly** | Step 3 fires AND returns fail in > 30% of CES runs | >30% |
| **WebFetch ambiguity recurring** | "WebFetch" appears in Notes field in > 2 runs | >2 occurrences |
| **Recurring flag** | Any single flag fires in > 30% of runs | >30% |
| **Zero rows / data gap** | "zero rows" or "no results" appears in Notes in > 1 run | >1 occurrence |
| **NET-NEW BUILD pattern** | Champion = "Not found — NET-NEW BUILD" in > 15% of runs | >15% |
| **Anomaly cluster** | Notes ≠ "none" in > 40% of runs | >40% |

For each triggered rule:
1. Note which log entries are evidence
2. Cross-reference the current SKILL.md — is this scenario addressed? Is the instruction clear?
3. Classify the root cause (see below)

### Root Cause Categories

| Category | When to apply |
|---|---|
| **Skill Gap** | The scenario appears repeatedly but SKILL.md has no instruction for it |
| **Instruction Ambiguity** | SKILL.md addresses the scenario but the wording is unclear or being inconsistently applied (evidenced by varying handling across similar runs) |
| **Data Coverage Gap** | The data foundation doesn't support the scenario (zero rows, CES where NES expected, product not in tables) |
| **Output Format Error** | Formatting issues recurring (flag fired about a field that the skill claims to populate) |

A single pattern can have more than one root cause. If so, note both.

---

## Step 5 — Render the Report

Render all sections in this order. Never truncate any table.

---

### Summary

```
Offer Pulse — Systemic Issues Report
Runs analyzed  : {N} runs ({first date} → {last date})
Path split     : A: {N} ({pct}%) | B: {N} ({pct}%)
NES/CES split  : NES: {pct}% | CES: {pct}% | Mixed: {pct}% (of Path A runs)
Champion found : {N} ({pct}%) | Not found: {N} ({pct}%)
Anomaly rate   : {N} runs with non-trivial Notes ({pct}%)
```

---

### Flag Distribution

Render the flag frequency table from Step 3. If no flags were ever fired, write "No flags fired across all logged runs."

---

### Gate Dimension Ask Frequency

Render the gate dimension table from Step 3. Include an interpretation line:
- If Term was asked in > 60% of runs: "Term is almost never pre-answered — consider whether Jira ticket extraction can infer it more aggressively."
- If Market was asked in > 60% of runs: "Market is almost never pre-answered — consider whether the default should be stated rather than asked."
- If any dimension was asked in 0% of runs: "{dimension} is always pre-answered — no change needed."

---

### Systemic Issues

One row per triggered detection rule. If no rules triggered, write "No systemic issues detected."

| # | Issue | Frequency | Root Cause | Evidence (run IDs or dates) | SKILL.md cross-ref |
|---|-------|-----------|------------|-----------------------------|--------------------|

Rank by frequency (highest first). If two issues have the same frequency, rank Skill Gap before Data Coverage Gap before Instruction Ambiguity before Output Format Error.

---

### Top Issue Brief (for Wendy)

Render this section only if at least one systemic issue was found.

Write a 1–2 paragraph brief covering:
1. What the issue is and how often it occurs
2. Which skill rule is missing, ambiguous, or contradicted by the evidence
3. A concrete recommendation for what the fix should say (a specific instruction, threshold, or added step)

This brief is designed to be passed verbatim to Wendy. It should be actionable — Wendy should be able to produce a revised SKILL.md section from it without asking clarifying questions.

---

### Human Error Gate

Before rendering the Wendy prompt, run a user-gaps check on the top issue's symptom description.

Invoke `/user-gaps check <top issue symptom>` using the issue title and root cause description from the Systemic Issues table as the symptom text.

- If one or more patterns match with Verdict = `Human Error Only`: add a warning block before the Wendy prompt:

  ```
  ⚠ Human Error Check — Issue #1 may be input-caused
  Matching pattern: HE-{N} "{Pattern name}" (Verdict: Human Error Only)
  Before changing the skill, confirm the issue recurs when the analyst provides correct input.
  ```

- If a pattern matches with Verdict = `Mixed — Investigate`: note it without blocking Wendy:

  ```
  Note: Issue #1 partially overlaps with HE-{N} "{Pattern name}" (Mixed).
  Investigate whether the skill fails even when input is correct. Cross-check /system-gaps for a related entry.
  ```

- If no patterns match: proceed to the Wendy prompt without comment.

---

After the report, always end with:

> "Would you like me to invoke `/wendy` to address issue #1? I'll pass the brief above as input — Wendy will produce a revised skill instruction for your review. No files will be changed until you approve."

---

## Output Constraints

- Never show partial statistics. If a field is missing from some log entries (e.g. older entries before a field was added), note the gap and compute stats on available data only.
- Never editorialize beyond what the data supports. If only 3 runs exist and one had a WebFetch anomaly, note it but do not declare a systemic issue — apply the detection thresholds strictly.
- Do not propose fixes in the Systemic Issues table. That is Wendy's job. The table identifies and classifies; the Top Issue Brief gives enough context for Wendy to act.
