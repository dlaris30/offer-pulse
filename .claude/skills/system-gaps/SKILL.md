---
name: system-gaps
description: Log, track, and resolve known process gaps and issues in the offer-pulse workflow so they aren't lost between conversations. Supports listing open issues, adding new gaps, resolving gaps, and showing gap detail.
---

# /system-gaps — Process Gap Tracker

A persistent issue log for known gaps, recurring problems, and process issues across the offer-pulse skill suite. Entries survive session boundaries — nothing is lost between conversations.

**Log file:** `.claude/skills/system-gaps/gaps-log.md` (relative to the project root)

---

## Invocation Modes

| Invocation | What it does |
|------------|-------------|
| `/system-gaps` | List all open gaps (default) |
| `/system-gaps all` | List all gaps including resolved ones |
| `/system-gaps N` | Show full detail for gap #N |
| `/system-gaps add` | Add a new gap — prompts for details if not provided inline |
| `/system-gaps add "title"` | Start an add with the title pre-filled |
| `/system-gaps resolve N` | Mark gap #N as resolved |
| `/system-gaps resolve N "resolution text"` | Mark resolved with a one-line explanation |

---

## Step 1 — Parse the Invocation

From the args, determine the operation:

- No args, or args = `list` or `open` → **List open**
- Args = `all` → **List all**
- Args is a bare integer N (e.g. `/system-gaps 2`) → **Detail**
- Args starts with `add` or is a plain description string (not a number, not "all") → **Add**
- Args starts with `resolve` or `close`, followed by a number → **Resolve**

---

## Step 2 — Read the Log

Read `.claude/skills/system-gaps/gaps-log.md`.

If the file does not exist, treat as an empty log. For Add operations, create the file. For all other operations on an empty log, output:

```
No gaps logged yet.
Use /system-gaps add to log the first one.
```

Stop.

---

## Step 3 — Execute the Operation

### List Open

Read all entries. Filter to `Status : open`. Render:

```
Open Gaps — N issue(s)

| # | Title | Category | Skill | Added |
|---|-------|----------|-------|-------|
| GAP-001 | ... | Skill Gap | offer-pulse | 2026-05-14 |
```

If no open gaps: `No open gaps. Use /system-gaps add to log one, or /system-gaps all to see resolved gaps.`

---

### List All

Same table but all entries. Add a Status column:

```
All Gaps — N issue(s)

| # | Title | Category | Skill | Added | Status |
|---|-------|----------|-------|-------|--------|
```

---

### Detail

Find the entry with the matching GAP-NNN heading. Render as a labeled record block:

```
=== GAP-001 ===
Title      : {title}
Status     : {open | resolved}
Category   : {category}
Skill      : {skill}
Added      : {date}
Evidence   : {note or —}

{description block}

Resolution : {note or —}
Resolved   : {date or —}
```

If the gap number does not exist: `GAP-{N} not found. Use /system-gaps to see the current list.`

---

### Add

**Collect required fields.** If the analyst provided a description in the invocation args, use it as the Title. Ask for any missing required fields — all in one batch, not one at a time.

Required fields:
- **Title** — one short line describing the gap (e.g. "B0 applies term filter before PFID discovery")
- **Category** — one of: `Skill Gap` | `Data Gap` | `Output Format` | `Process Gap` | `Known Limitation`
- **Skill** — one of: `offer-pulse` | `ces-nes` | `scorer` | `use-cases` | `general`
- **Description** — what is wrong, what impact it has, and what the fix direction looks like
- **Evidence** — optional; where/when it was observed (run ID, date, session context)

Once all required fields are collected:

1. Determine the next gap ID: max existing ID + 1, formatted as `GAP-NNN` (zero-padded to 3 digits)
2. Append the new entry to the log file using the format in the **Log Entry Format** section
3. Confirm: `Logged GAP-{N}: {Title}`

---

### Resolve

Find the entry for the given number. If not found: `GAP-{N} not found.`

If already resolved: `GAP-{N} is already resolved (resolved {date}).`

If a resolution note was not provided in the invocation, ask for one (one line is enough).

Then:
1. Update the existing entry in place — change `Status : open` → `Status : resolved`
2. Set `Resolved : {today's date}`
3. Set `Resolution : {note}`
4. Write the updated file back
5. Confirm: `Resolved GAP-{N}: {Title}`

---

## Log Entry Format

Each entry uses this exact format. A `---` separator follows each entry.

```
## GAP-001
Title      : {short title — one line}
Status     : open
Category   : {Skill Gap | Data Gap | Output Format | Process Gap | Known Limitation}
Skill      : {offer-pulse | ces-nes | scorer | use-cases | general}
Added      : {YYYY-MM-DD}
Evidence   : {short note, or —}

{Description block. One paragraph or bullet list. Wrap lines at ~90 chars.}

Resolution : —
Resolved   : —

---
```

**Critical format rules:**
- The `## GAP-NNN` heading is the primary key. Never modify it after creation.
- Field names are padded to 10 chars so values align vertically.
- Status is exactly `open` or `resolved` (lowercase, no other values).
- Resolution note goes in `Resolution :` — not in the description block.
- Never reorder existing entries. Append new entries at the bottom.
- When resolving: update the existing entry in place. Never append a duplicate.

---

## Output Constraints

- Never truncate the gaps table. Show all rows.
- List and Detail operations: render immediately, no confirmation step.
- Add: always confirm the assigned gap ID after writing.
- Resolve: always confirm the gap ID and title after writing.
- Read-only operations (list, detail) never modify the log file.
