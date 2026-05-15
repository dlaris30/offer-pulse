---
name: user-gaps
description: Log and check known analyst input error patterns when using the offer-pulse skill. Run /user-gaps check before making any skill change to confirm the issue is skill-caused rather than input-caused.
---

# /user-gaps — User Input Error Tracker

A persistent log of recurring analyst input mistakes when invoking `/offer-pulse`. Use this skill **before modifying any skill** to confirm that a reported problem is a skill defect — not the analyst providing wrong or ambiguous input.

**Log file:** `.claude/skills/user-gaps/error-log.md` (relative to the project root)

---

## Invocation Modes

| Invocation | What it does |
|------------|-------------|
| `/user-gaps` | List all active error patterns (default) |
| `/user-gaps all` | List all patterns including archived ones |
| `/user-gaps N` | Show full detail for pattern HE-N |
| `/user-gaps add` | Add a new pattern — prompts for required fields |
| `/user-gaps add "title"` | Start an add with the title pre-filled |
| `/user-gaps check <symptom>` | Check if a reported symptom matches a known human error pattern |
| `/user-gaps summary` | Produce a context block for use in skill-change decisions |

---

## Step 1 — Parse the Invocation

From the args, determine the operation:

- No args, or args = `list` → **List active**
- Args = `all` → **List all**
- Args is a bare integer N → **Detail**
- Args starts with `add` or is a plain descriptive string that doesn't begin with a number, "all", "check", or "summary" → **Add**
- Args starts with `check` → **Check** (everything after "check" is the symptom text)
- Args = `summary` → **Summary**

---

## Step 2 — Read the Log

Read `.claude/skills/user-gaps/error-log.md`.

If the file does not exist, treat as an empty log. For Add operations, create the file. For all other operations on an empty log, output:

```
No user gap patterns logged yet.
Use /user-gaps add to log the first one.
```

Stop.

---

## Step 3 — Execute the Operation

### List Active

Read all entries. Filter to `Status : active`. Render:

```
Human Error Patterns — N active

| ID     | Pattern                              | Category           | Frequency      | Verdict                        |
|--------|--------------------------------------|--------------------|----------------|-------------------------------|
| HE-001 | ...                                  | Context Error      | Very Frequent  | Human Error Only              |
```

If no active patterns: `No active patterns. Use /user-gaps add to log one.`

---

### List All

Same table but all entries. Add a Status column.

---

### Detail

Find the entry with the matching `## HE-NNN` heading. Render as a labeled record block:

```
=== HE-001 ===
Pattern    : {short name}
Status     : active | archived
Category   : {category}
Frequency  : {Rare | Occasional | Frequent | Very Frequent}
Verdict    : {Human Error Only | Mixed — Investigate | Skill Issue Masked as Human Error}
Added      : {date}
Evidence   : {note or —}

What the analyst does:
{description block}

How to detect:
{detection signals block}

What to say:
{response guidance block}
```

If not found: `HE-{N} not found. Use /user-gaps to see the current list.`

---

### Add

Collect required fields. If a title was provided in the args, use it. Ask for all missing required fields in one batch.

Required fields:
- **Pattern name** — short title (e.g. "Product name instead of Jira ticket key")
- **Category** — one of: `Input Error` | `Context Error` | `Expectation Error` | `Scope Error`
- **Frequency** — one of: `Rare (<5%)` | `Occasional (5–25%)` | `Frequent (25–50%)` | `Very Frequent (>50%)`
- **Verdict** — one of: `Human Error Only` | `Mixed — Investigate` | `Skill Issue Masked as Human Error`
- **What the analyst does** — description of the mistake
- **How to detect** — signals that indicate this pattern is occurring (keywords in input, zero-row results, analyst pushback, etc.)
- **What to say** — how to respond to the analyst; why this does or does not require a skill change
- **Evidence** — optional; where/when observed (run date, Jira ticket, gap number)

Once all fields are collected:

1. Determine the next ID: max existing ID + 1, formatted as `HE-NNN` (zero-padded to 3 digits)
2. Append to the log using the format in the **Log Entry Format** section
3. Confirm: `Logged HE-{N}: {Pattern name}`

---

### Check

**This is the primary integration mode.** Run this before invoking `/wendy` or acting on any `/use-cases` systemic issue.

Input: the symptom text provided after "check" (e.g. `/user-gaps check analysts getting zero results on CES surfaces`)

Algorithm:

1. Read all **active** log entries
2. For each entry, extract keywords from:
   - The Pattern name
   - The Category
   - The "How to detect" block
3. Score each entry against the symptom text (count keyword overlaps — partial matches count)
4. Rank by score. Show all entries with at least 1 match; if none match, say so explicitly.

Render results:

```
Human Error Check: "{symptom text}"

Matching patterns (ranked by relevance):

=== HE-004 ===
Pattern    : Expecting NES output from CES surface
Verdict    : Human Error Only
Frequency  : Occasional
Match      : "zero results", "CES surfaces" match detection signals

What to say: {paste the "What to say" block from the entry}

→ Before invoking /wendy: confirm the analyst understood the surface was CES.
  If they knew the surface was CES and still got wrong output, this may not be HE-004 — investigate the skill.
```

For entries where Verdict = `Mixed — Investigate`, add:
> "This pattern overlaps with a known skill issue. Cross-check /system-gaps for a related entry."

For entries where Verdict = `Skill Issue Masked as Human Error`, add:
> "This looks like analyst error but the root cause is a skill defect. Investigate the skill — do not dismiss without checking."

If no patterns match:
```
No matching human error pattern found for: "{symptom text}"

This symptom has no known user-gap precedent. Proceed to /system-gaps or /use-cases
to determine if this is a skill issue.
```

---

### Summary

Produce a decision-context block for use when evaluating skill changes:

```
Human Error Context Block
Active patterns : {N}
Frequent+       : {list HE IDs with Frequency = Frequent or Very Frequent}

Pattern overview:

| ID     | Pattern                              | Frequency      | Verdict                        |
|--------|--------------------------------------|----------------|-------------------------------|

→ Before acting on a reported issue, run /user-gaps check <symptom> to confirm
  the issue is skill-caused rather than input-caused.
```

---

## Log Entry Format

```
## HE-001
Pattern    : {short name — one line}
Status     : active
Category   : {Input Error | Context Error | Expectation Error | Scope Error}
Frequency  : {Rare (<5%) | Occasional (5–25%) | Frequent (25–50%) | Very Frequent (>50%)}
Verdict    : {Human Error Only | Mixed — Investigate | Skill Issue Masked as Human Error}
Added      : {YYYY-MM-DD}
Evidence   : {short note, or —}

**What the analyst does:**
{One paragraph or bullet list describing the mistake. Wrap lines at ~90 chars.}

**How to detect:**
{Bullet list of signals that indicate this pattern is occurring. These are the keywords
used for matching in /user-gaps check.}

**What to say:**
{Guidance on how to respond. State clearly whether this warrants a skill change or not.}

---
```

**Format rules:**
- `## HE-NNN` heading is the primary key. Never modify it after creation.
- Field names padded to 10 chars so values align vertically.
- Status is exactly `active` or `archived` (lowercase).
- `archived` = pattern no longer relevant (e.g., a skill fix eliminated it as a distinct concern).
- Never reorder existing entries. Append new entries at the bottom.
- When archiving: update Status in place. Never append a duplicate.

---

## Output Constraints

- Never truncate the patterns table. Show all rows.
- Check mode: always state the symptom back verbatim before showing matches.
- Check mode: if no matches, say so explicitly — do not force a partial match.
- Add: confirm the assigned HE ID after writing.
- Read-only operations (list, detail, check, summary) never modify the log file.
