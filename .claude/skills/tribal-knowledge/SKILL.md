---
name: tribal-knowledge
description: Log, search, and retrieve tribal knowledge — unexplained facts, quirks, naming conventions, and domain truths that don't fit in /system-gaps or /user-gaps but must not be lost between conversations.
---

# /tribal-knowledge — Tribal Knowledge Log

A persistent log of facts, quirks, and domain truths about the offer-pulse ecosystem. These are not bugs or user mistakes — they are things that are simply true, often unexplained, and critical to know before acting. Entries survive session boundaries.

**Log file:** `.claude/skills/tribal-knowledge/knowledge-log.md` (relative to the project root)

---

## Skill Routing — Which Log?

| What it is | Where it goes |
|------------|---------------|
| A skill defect or process issue that can be fixed | `/system-gaps` |
| A recurring analyst behavioral mistake | `/user-gaps` |
| A permanently-true domain fact, data quirk, or naming convention | `/tribal-knowledge` ← here |

**The one-question test:** "Would fixing SKILL.md make this irrelevant?" Yes → `/system-gaps`. No → `/tribal-knowledge`.

**Exception (same event, two entries):** A domain fact that also underlies a gap or user error is valid in both logs — they just cover different angles. The TK entry states the fact; the GAP/HE entry describes the failure mode. Cross-reference via Related fields; never duplicate the body text between entries.

Examples of tribal knowledge: "M365 catalog_query_get_offers returns 129K tokens — never read the full file." "product_term_unit_desc is lowercase in billing, not Title Case." "vnext-i18nox series uses base slugs on all surfaces — no -precheck suffix." "FOS means SLP, not DPP."

---

## Invocation Modes

| Invocation | What it does |
|------------|-------------|
| `/tribal-knowledge` | List all active entries (default) |
| `/tribal-knowledge all` | List all entries including archived |
| `/tribal-knowledge N` | Show full detail for entry TK-N |
| `/tribal-knowledge add` | Add a new entry — prompts for required fields |
| `/tribal-knowledge add "title"` | Start an add with the title pre-filled |
| `/tribal-knowledge search <query>` | Search active entries by keyword across title, body, and tags |
| `/tribal-knowledge archive N` | Mark entry TK-N as archived (superseded or no longer true) |

---

## Step 1 — Parse the Invocation

From the args, determine the operation:

- No args, or args = `list` → **List active**
- Args = `all` → **List all**
- Args is a bare integer N → **Detail**
- Args starts with `add` → **Add**
- Args is a plain descriptive string (not a number, not "all", not "search", not "archive") → **Add**
- Args starts with `search` → **Search** (everything after "search" is the query)
- Args starts with `archive`, followed by a number → **Archive**

---

## Step 2 — Read the Log

Read `.claude/skills/tribal-knowledge/knowledge-log.md`.

If the file does not exist, treat as an empty log. For Add operations, create the file. For all other operations on an empty log, output:

```
No tribal knowledge logged yet.
Use /tribal-knowledge add to log the first entry.
```

Stop.

---

## Step 3 — Execute the Operation

### List Active

Read all entries. Filter to `Status : active`. Render:

```
Tribal Knowledge — N active entries

| ID     | Title                                        | Category           | Tags                   | Added      |
|--------|----------------------------------------------|--------------------|------------------------|------------|
| TK-001 | M365 catalog_query returns 129K tokens       | System Behavior    | m365, catalog, mcp     | 2026-05-15 |
```

If no active entries: `No tribal knowledge logged yet. Use /tribal-knowledge add to log the first entry.`

---

### List All

Same table but all entries. Add a Status column:

```
All Tribal Knowledge — N entries

| ID     | Title                                        | Category           | Tags                   | Added      | Status   |
|--------|----------------------------------------------|--------------------|------------------------|------------|----------|
```

---

### Detail

Find the entry with the matching `## TK-NNN` heading. Render as a labeled record block:

```
=== TK-001 ===
Title      : {title}
Status     : {active | archived}
Category   : {category}
Tags       : {comma-separated tag list}
Added      : {YYYY-MM-DD}
Source     : {where/how this was learned, or —}
Related    : {GAP-NNN, HE-NNN, etc., or —}

{Body — the fact itself, full detail}

Archive note : {reason for archiving, or —}
Archived     : {date, or —}
```

If the entry number does not exist: `TK-{N} not found. Use /tribal-knowledge to see the current list.`

---

### Add

**Routing check first.** Before collecting fields, confirm this belongs in tribal-knowledge:
- Is this a permanently-true fact, quirk, or naming convention that no skill fix can make irrelevant? → proceed
- Is this a fixable skill or instruction defect? → redirect to `/system-gaps` instead
- Is this a behavioral mistake analysts make repeatedly? → redirect to `/user-gaps` instead

**Collect required fields.** If a title was provided in the invocation args, use it. Ask for any missing required fields in one batch — not one at a time.

Required fields:
- **Title** — one short line describing the fact (e.g. "product_term_unit_desc is lowercase in billing")
- **Category** — one of: `Domain Fact` | `Data Quirk` | `Naming Convention` | `System Behavior` | `Historical Context` | `Terminology`
- **Tags** — comma-separated keywords: surfaces, products, tools, or concepts this fact applies to (e.g. "m365, catalog, dpp_precheck")
- **Body** — the full fact. What is true, why it matters, what breaks if you don't know it. One paragraph or bullet list. Wrap lines at ~90 chars.

Optional fields:
- **Source** — where/how this was learned (run ID, Jira ticket, session date). Leave blank to default to `—`.
- **Related** — links to related gap or error entries (e.g. "GAP-035, GAP-038"). Leave blank to default to `—`.

Once all required fields are collected:

**Dedup check.** Before writing, scan all existing active TK entries for keyword overlap with the new entry's Title + Tags. Score matches: count matching keywords across Title and Tags fields. If any existing entry scores 2+ keyword overlaps, show that entry:

```
Possible duplicate: TK-{N} — {Title} (tags: {tags})
Run /tribal-knowledge {N} to review before adding.
Proceed anyway? (y/n)
```

If analyst confirms this is distinct, proceed. If it's a duplicate, stop and suggest cross-referencing via the Related field of the relevant entry instead.

**Related GAP/HE reminder.** If the cross-log check (Step 4) surfaced any open system gaps or active user patterns with keyword overlap, prompt: "Consider adding the related IDs to the Related field (e.g. GAP-NNN, HE-NNN) so the cross-referencing stays bidirectional."

1. Determine the next TK ID: max existing ID + 1, formatted as `TK-NNN` (zero-padded to 3 digits)
2. Append the new entry to the log file using the format in the **Log Entry Format** section
3. Confirm: `Logged TK-{N}: {Title}`

---

### Search

Input: the query text provided after "search".

Algorithm:
1. Read all **active** entries
2. For each entry, tokenize: Title + Tags + Body (lowercase, split on spaces/punctuation)
3. Score each entry against the query tokens (count keyword overlaps; partial substring matches count)
4. Rank by score descending. Show all entries with at least 1 match.

Render results:

```
Tribal Knowledge Search: "{query}"

N matching entries:

=== TK-001 ===
Title    : M365 catalog_query_get_offers returns 129K tokens
Category : System Behavior
Tags     : m365, catalog, mcp
Match    : "m365", "catalog" matched in title and tags

{First 2–3 sentences of the body as a preview}

→ /tribal-knowledge 1 for full detail
```

If no entries match:
```
No tribal knowledge entries matched: "{query}"

Use /tribal-knowledge add to log this fact if it should be recorded.
```

---

### Archive

Find the entry for the given number. If not found: `TK-{N} not found.`

If already archived: `TK-{N} is already archived (archived {date}).`

Ask for an archive reason (one line is enough — e.g. "superseded by GAP-031 fix", "no longer true as of 2026-05-20").

**Staleness check.** Before writing, check: does this TK entry have any Related field values (GAP-NNN, HE-NNN)? If yes, note: "TK-{N} is referenced by {related IDs}. After archiving, confirm those entries' Related fields still point to something valid — they may need a note that this TK entry has been archived."

Then:
1. Update the existing entry in place — change `Status : active` → `Status : archived`
2. Set `Archived : {today's date}`
3. Set `Archive note : {reason}`
4. Write the updated file back
5. Confirm: `Archived TK-{N}: {Title}`

---

## Step 4 — Cross-Log Check

Run after every **Add**, **Search**, and **Detail** operation. Skip for List and Archive operations (no specific subject to cross-reference).

**Read the files directly — do not invoke `/system-gaps` or `/user-gaps` as skills. This prevents circular calls.**

1. Read `.claude/skills/system-gaps/gaps-log.md`
2. Read `.claude/skills/user-gaps/error-log.md`
3. Extract keywords from the current subject (entry title + tags + key terms from the body)
4. Score all open/active entries in both files against those keywords (title, tags, pattern name — partial matches count)
5. If matches found, append a compact section after the main output:

```
Cross-log:
• /system-gaps GAP-{N} — {Title}
• /user-gaps HE-{N} — {Pattern name}
```

If no matches: omit this section entirely — do not say "no matches found."

One pass each through the other two files. Stop there — no further chaining.

---

## Log Entry Format

Each entry uses this exact format. A `---` separator follows each entry.

```
## TK-001
Title      : {short title — one line}
Status     : active
Category   : {Domain Fact | Data Quirk | Naming Convention | System Behavior | Historical Context | Terminology}
Tags       : {comma-separated keywords}
Added      : {YYYY-MM-DD}
Source     : {where/how this was learned, or —}
Related    : {GAP-NNN, HE-NNN, or — }

{Body — the full fact. One paragraph or bullet list. Wrap lines at ~90 chars.}

Archive note : —
Archived     : —

---
```

**Critical format rules:**
- The `## TK-NNN` heading is the primary key. Never modify it after creation.
- Field names are padded to 10 chars so values align vertically.
- Status is exactly `active` or `archived` (lowercase, no other values).
- Archive note and Archived date go in the dedicated fields — not in the body.
- Never reorder existing entries. Append new entries at the bottom.
- When archiving: update the existing entry in place. Never append a duplicate.

---

## Output Constraints

- Never truncate the entries table. Show all rows.
- List and Detail operations: render immediately, no confirmation step.
- Search: always state the query back verbatim before showing matches.
- Add: always confirm the assigned TK ID after writing.
- Archive: always confirm the TK ID and title after writing.
- Read-only operations (list, detail, search) never modify the log file.
