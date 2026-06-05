---
name: wbr
description: Weekly Business Review logger. Log notable events as they happen (EP blockers, pivots, wins, risks), then pull a timestamped executive-ready briefing filtered by week or month. Four invocation modes: log, week, month, list. Natural language input — infer four-category breakdown, confirm before writing.
---

# /wbr — Weekly Business Review Log

A lightweight running log for executive-reportable events. Log items as they happen;
pull a clean briefing at review time. Every entry carries a full ISO-8601 timestamp so
items can be filtered to the current week, month, or any arbitrary window.

**Log file:** `.claude/skills/wbr/wbr-log.md` (relative to project root)

Entries are append-only. The log is never rewritten — only extended.

---

## When to Use

Log any event that belongs in a WBR or executive recap:

- EP / ecomm engineering tickets created to unblock an offer test (infrastructure gaps,
  routing fixes, LOC enablement, cache bugs)
- Major blockers discovered or resolved
- Pipeline decisions: pivots, scope changes, sequencing holds, go/no-go calls
- Wins worth naming — first live test, coverage milestone, validated join path
- Unresolved risks with potential executive visibility

Do **not** log routine analytical work, individual offer-pulse queries, or
status-update commentary. Those belong in the use-case log, not the WBR log.

---

## Invocation Modes

| Invocation | What it does |
|------------|-------------|
| `/wbr log <description>` | Log a new event — infers four-category breakdown, confirms, then writes |
| `/wbr week` | Pull all entries from the current ISO week (Mon–Sun), formatted as executive briefing |
| `/wbr month` | Pull all entries from the current calendar month, formatted as executive briefing |
| `/wbr list` | Compact table: date | category | one-liner — good for pre-review scanning |
| `/wbr list week` | Compact table filtered to current week |
| `/wbr list month` | Compact table filtered to current month |
| `/wbr resolve WBR-N <note>` | Append a resolution note to an existing entry without creating a duplicate |
| `/wbr WBR-N` | Show full detail for a single entry |

---

## Step 1 — Parse the Invocation

From `$ARGUMENTS`, determine the operation:

- Args start with `log` (or are a plain description with no recognized keyword) → **Log**
- Args = `week` or `this week` → **Pull Week**
- Args = `month` or `this month` → **Pull Month**
- Args start with `list` → **List** (check for trailing `week` / `month` to apply filter)
- Args start with `resolve` followed by `WBR-\d+` → **Resolve**
- Args match a bare `WBR-\d+` → **Detail**
- No args → **List** (default)

---

## Step 2 — Read the Log

Read `.claude/skills/wbr/wbr-log.md`.

If the file does not exist, treat as an empty log. For Log operations, create the file.
For all other operations on an empty log, output:

```
No WBR entries logged yet.
Use /wbr log <description> to log the first entry.
```

Stop.

---

## Step 3 — Execute the Operation

---

### Log

This is the primary write path. Follow all sub-steps exactly.

#### L1 — Extract the Description

The description is everything in `$ARGUMENTS` after the word "log". If `/wbr` was invoked
with no leading "log" keyword but with a plain free-form description, treat the entire
args as the description.

If `$ARGUMENTS` is empty: ask "What happened? (Paste a brief description of the event.)"
and stop.

#### L2 — Infer the Four-Category Breakdown

From the free-form description, infer:

| Field | Question it answers | Guidance |
|-------|---------------------|----------|
| **What happened** | The event itself — what changed, was created, was discovered | Keep to 1–2 sentences; factual, past tense |
| **Why it happened** | Root cause, context, or the gap it exposed | One sentence; if root cause is unknown, say so explicitly |
| **Risks** | What this puts at risk — launch, timeline, scope, a specific offer test | Name the specific risk; avoid vague words like "delay" without a referent |
| **Next steps** | What must happen to resolve or follow through — and who owns it if inferable | Imperative; name a specific action, not a direction |

Inference rules:
- If the description mentions a Jira ticket number, include it in **What happened**.
- If the description mentions a surface (ITC), product, or experiment, include it in
  **What happened** and carry it into **Risks** if a launch risk is plausible.
- If the description is a resolution ("X is now fixed"), set **Risks** to "none —
  resolved" and **Next steps** to the next downstream action (e.g., "unblock the
  dependent offer test").
- If the description clearly states a risk, carry it verbatim rather than inferring.
- If next steps cannot be inferred (the situation is open-ended), set **Next steps** to
  "TBD — needs owner" and flag it for clarification.

#### L3 — Determine the Category Label

Assign one category from this list:

| Category | Use when |
|----------|----------|
| `EP Ticket` | An ecomm-engineering ticket had to be created to unblock something |
| `Blocker` | A hard stop was discovered or a blocker was resolved |
| `Pipeline Decision` | A pivot, scope change, sequencing hold, or go/no-go call |
| `Win` | A positive milestone — first live test, data validation, coverage threshold |
| `Risk` | An unresolved risk flagged for executive visibility without a resolution yet |
| `Other` | Does not fit the above — use sparingly |

#### L4 — Confirm Before Writing

Present the inferred breakdown as a labeled record block and ask for confirmation:

```
Ready to log WBR-{N}:

=== Draft ===
Category    : {category}
What        : {what happened}
Why         : {why it happened}
Risks       : {risks}
Next steps  : {next steps}

Is this accurate? Reply y to write, or correct any field.
```

If the analyst corrects a field, apply the correction and re-present the block once before
writing. Do not loop more than twice — if still uncertain, write with the latest version
and note "entry may need refinement" in the body.

If the analyst replies with a bare `y` or `yes`, proceed immediately to L5.

Ask clarifying questions only when:
- Risks cannot be inferred and the description does not imply a resolution
- Next steps are genuinely ambiguous (no action is apparent)

Ask at most **one clarifying question** per log call, combining both points into one
question if needed. Do not ask about fields that can be reasonably inferred.

#### L5 — Assign ID and Timestamp

1. Determine the next WBR ID: max existing ID + 1, formatted as `WBR-NNN` (zero-padded
   to 3 digits).
2. Timestamp: use `currentDate` from the session context, formatted as
   `YYYY-MM-DDTHH:MM` (local time, 24-hour). If only a date is available (no clock time),
   use `YYYY-MM-DDT00:00` and append `(date only)` to the timestamp field.

#### L6 — Write the Entry

Append the new entry to `.claude/skills/wbr/wbr-log.md` using the **Log Entry Format**
defined below.

Confirm: `Logged WBR-{N} [{category}] — {What happened, first sentence}.`

---

### Pull Week

"Current week" = ISO week containing today (Monday through Sunday inclusive).

1. Determine the Monday and Sunday dates bounding the current ISO week.
2. Filter entries to those whose `Logged` timestamp falls within [Monday 00:00,
   Sunday 23:59].
3. If no entries fall in the window: `No WBR entries for this week (week of {Monday date}).`
   Stop.
4. Render the **Executive Briefing** format (see Step 4).

---

### Pull Month

"Current month" = the calendar month of today.

1. Determine the first and last dates of the current calendar month.
2. Filter entries to those whose `Logged` timestamp falls within that range.
3. If no entries fall in the window: `No WBR entries for {Month YYYY}.` Stop.
4. Render the **Executive Briefing** format (see Step 4).

---

### List

Render a compact scan table. Apply week/month filter if specified; otherwise show all entries.

```
WBR Log — {N entries} [{filter label or "all"}]

| ID      | Date       | Category          | One-liner                                       | Status   |
|---------|------------|-------------------|-------------------------------------------------|----------|
| WBR-001 | 2026-06-02 | EP Ticket         | P2P routing ticket opened to unblock LOC test   | open     |
| WBR-002 | 2026-06-03 | Blocker           | Precheck cache blocked MWP offer test           | resolved |
```

One-liner = first sentence of **What happened**, truncated at 60 characters with `…` if
needed.

Never truncate the table rows. Show all entries matching the filter.

---

### Detail

Find the entry with the matching `## WBR-NNN` heading. Render as a labeled record block:

```
=== WBR-001 ===
Category    : {category}
Status      : {open | resolved}
Logged      : {ISO-8601 timestamp}
Week        : {ISO week label, e.g. "2026-W23 (Jun 2–8)"}

What        : {what happened}
Why         : {why it happened}
Risks       : {risks}
Next steps  : {next steps}

Resolution  : {resolution note, or —}
Resolved    : {date, or —}
```

If the entry number does not exist:
`WBR-{N} not found. Use /wbr list to see all entries.`

---

### Resolve

Find the entry for the given WBR-N. If not found: `WBR-{N} not found.`
If already resolved: `WBR-{N} is already resolved ({date}). Append anyway? (y/n)`

If the resolution note was not provided inline (`/wbr resolve WBR-N` with no note text),
ask: "What was the resolution?" (one line is enough).

Do NOT create a new entry. Update the existing entry in place:
1. Change `Status     : open` → `Status     : resolved`
2. Set `Resolved   : {today's date}`
3. Set `Resolution : {note}`
4. Write the updated file back.

Confirm: `Resolved WBR-{N}: {first sentence of What happened}.`

---

## Step 4 — Executive Briefing Format

Used by Pull Week and Pull Month. Renders entries as clean prose grouped by category,
not as a raw log dump.

### Header

```
WBR Briefing — {Week of Mon DD Mon YYYY | Month YYYY}
{N} item(s) across {K} categories
```

### Body

Group entries by category in this order: `EP Ticket`, `Blocker`, `Pipeline Decision`,
`Win`, `Risk`, `Other`. Skip any category with no entries in the window.

For each category group:

```
**{Category}**

• WBR-{N} ({date}) — {What happened}
  Why: {why}
  Risk: {risks}
  Next: {next steps}
  {If resolved: "→ Resolved {date}: {resolution note}"}

• WBR-{N} ...
```

Omit the "Risk:" line if risks = "none — resolved" or "none".
Omit the "Next:" line if next steps are already reflected in a resolution.

Resolved entries get the `→ Resolved` line; open entries do not.

### Footer

```
---
Open items: {count of entries in window with Status: open}
Resolved:   {count of entries in window with Status: resolved}
```

Keep the briefing tight. Each bullet should read as a self-contained executive talking
point — no jargon, no data-model details unless they are material to the risk or decision.
If the original log entry contains data-model specifics (table names, field names), convert
them to plain language in the briefing output.

---

## Log Entry Format

Each entry uses this exact format. A `---` separator follows each entry.

```
## WBR-001
Category   : {EP Ticket | Blocker | Pipeline Decision | Win | Risk | Other}
Status     : open
Logged     : {YYYY-MM-DDTHH:MM}
Week       : {ISO week label, e.g. 2026-W23}

**What happened**
{1–3 sentences. Factual, past tense.}

**Why it happened**
{1–2 sentences. Root cause or context.}

**Risks**
{1–2 sentences. Name the specific launch, timeline, or scope risk. Or: "None — resolved."}

**Next steps**
{1–2 sentences. Specific action(s) required. Or: "TBD — needs owner."}

Resolution : —
Resolved   : —

---
```

**Critical format rules:**
- The `## WBR-NNN` heading is the primary key. Never modify it after creation.
- Field names in the metadata block are padded so values align vertically.
- Status is exactly `open` or `resolved` (lowercase, no other values).
- The four narrative fields use bold H4-style headers (`**What happened**`, etc.),
  not inline labels.
- Resolution and Resolved go in the dedicated metadata fields at the bottom — not in
  the narrative body.
- Never reorder existing entries. Append new entries at the bottom.
- When resolving: update the existing entry in place. Never append a duplicate.
- The `Week` field uses the ISO 8601 week number of the `Logged` date
  (e.g., `2026-W23`). This is what Pull Week filtering uses.

---

## Output Constraints

- Never truncate the list table. Show all rows that match the filter.
- Log mode: always show the draft confirmation block before writing.
- Log mode: always confirm the assigned WBR ID after writing.
- Resolve: always confirm the WBR ID and first-sentence summary after writing.
- Detail: render immediately, no confirmation step.
- Pull Week / Pull Month: if the window contains no entries, say so and stop — do not
  render an empty briefing.
- Read-only operations (list, detail, week, month) never modify the log file.
- Executive Briefing output: convert data-model vocabulary (table names, column names,
  catalog IDs) into plain language. The briefing is for executives, not analysts.
- Timestamps in the log are in local time (analyst's timezone). Do not convert to UTC.
