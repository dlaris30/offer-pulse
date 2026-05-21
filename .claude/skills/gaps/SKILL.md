---
name: gaps
description: Unified gap tracker for offer-pulse. Combines system gaps (skill defects, process issues) and user error patterns (analyst input mistakes) in a single skill. Run /gaps check before any skill change to rule out input-caused issues.
---

# /gaps — Offer Pulse Gap Tracker

A unified persistent log for two distinct gap types:
- **System gaps** (GAP-NNN) — skill defects, bad instructions, process issues that can be fixed by changing a SKILL.md
- **User patterns** (HE-NNN) — recurring analyst input mistakes that the skill cannot fix

**Log files:**
- `.claude/skills/system-gaps/gaps-log.md` — system gaps
- `.claude/skills/user-gaps/error-log.md` — user error patterns

Both files survive session boundaries. All IDs are permanent.

---

## Routing — Which Entry Type?

| What it is | Entry type |
|------------|------------|
| A skill defect or bad instruction that can be fixed by changing SKILL.md | System gap (GAP-NNN) |
| A recurring analyst behavioral mistake — wrong input, wrong expectation, scope error | User pattern (HE-NNN) |
| A permanently-true domain fact, data quirk, or naming convention | `/tribal-knowledge` |

**One-question test:** "Would fixing SKILL.md make this irrelevant?" Yes → system gap. No → `/tribal-knowledge`. "Is this a skill problem or did the analyst do something wrong?" Analyst → user pattern.

**Exception:** The same event can generate both a GAP and an HE entry if the skill amplifies an analyst mistake. Cross-reference via the Related / Evidence fields. Don't duplicate body text — each entry covers its own angle.

---

## Invocation Modes

| Invocation | What it does |
|------------|-------------|
| `/gaps` | List open system gaps (default) |
| `/gaps user` | List active user error patterns |
| `/gaps all` | Combined overview — both logs, counts by status |
| `/gaps GAP-N` | Detail for system gap N |
| `/gaps HE-N` | Detail for user pattern N |
| `/gaps add system` | Add a new system gap — prompts for fields |
| `/gaps add system "title"` | Add system gap with title pre-filled |
| `/gaps add user` | Add a new user pattern — prompts for fields |
| `/gaps add user "title"` | Add user pattern with title pre-filled |
| `/gaps add "title"` | Routing check first, then adds to correct log |
| `/gaps check <symptom>` | Search both logs + tribal-knowledge for matching patterns |
| `/gaps resolve GAP-N` | Mark system gap as resolved |
| `/gaps resolve GAP-N "note"` | Mark resolved with explanation |
| `/gaps archive HE-N` | Mark user pattern as archived (superseded) |
| `/gaps summary` | User-gaps context block for skill-change decisions |

---

## Step 1 — Parse the Invocation

Determine operation and type from args:

- No args, or args = `list` or `open` → **List System Open**
- Args = `user` or `user list` → **List User Active**
- Args = `all` → **List Both**
- Args matches `GAP-\d+` → **Detail System** (extract N)
- Args matches `HE-\d+` → **Detail User** (extract N)
- Args starts with `add system` → **Add System** (remaining text = title if provided)
- Args starts with `add user` → **Add User** (remaining text = title if provided)
- Args starts with `add` followed by a description string (not "system"/"user") → **Add (routing check)**
- Args starts with `check` → **Check** (everything after "check" is the symptom text)
- Args starts with `resolve` + `GAP-\d+` → **Resolve System**
- Args starts with `archive` + `HE-\d+` → **Archive User**
- Args = `summary` → **Summary**

---

## Step 2 — Read the Logs

For operations that need system gaps: read `.claude/skills/system-gaps/gaps-log.md`.
For operations that need user patterns: read `.claude/skills/user-gaps/error-log.md`.
For **Check**, **List Both**, **Add (routing check)**, and **Summary**: read both files.

If a file does not exist, treat as empty. For Add operations, create the file if needed.

---

## Step 3 — Execute the Operation

### List System Open

Filter system gaps to `Status : open`. Render:

```
Open System Gaps — N issue(s)

| # | Title | Category | Skill | Added |
|---|-------|----------|-------|-------|
| GAP-001 | ... | Skill Gap | offer-pulse | 2026-05-14 |
```

If no open gaps: `No open system gaps. Use /gaps add system to log one, or /gaps all to see resolved gaps.`

---

### List User Active

Filter user patterns to `Status : active`. Render:

```
User Error Patterns — N active

| ID | Pattern | Category | Frequency | Verdict |
|----|---------|----------|-----------|---------|
| HE-001 | ... | Context Error | Very Frequent | Human Error Only |
```

If no active patterns: `No active user patterns. Use /gaps add user to log one.`

---

### List Both

Render two sections:

```
=== System Gaps ===
Open: N | Resolved: M | Total: T

| # | Title | Category | Status |
...

=== User Error Patterns ===
Active: N | Archived: M | Total: T

| ID | Pattern | Category | Frequency | Verdict |
...
```

---

### Detail System

Find the `## GAP-NNN` entry in gaps-log.md. Render:

```
=== GAP-001 ===
Title      : {title}
Status     : open | resolved
Category   : {category}
Skill      : {skill}
Added      : {date}
Evidence   : {note or —}

{description block}

Resolution : {note or —}
Resolved   : {date or —}
```

If not found: `GAP-{N} not found. Run /gaps to see the current list.`

---

### Detail User

Find the `## HE-NNN` entry in error-log.md. Render:

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
{description}

How to detect:
{signals}

What to say:
{response guidance}
```

If not found: `HE-{N} not found. Run /gaps user to see the current list.`

---

### Add System

**Routing check first.** Before collecting fields:
- Is this a fixable skill/instruction defect? → proceed
- Is it a permanently-true data or API fact (not fixable)? → redirect to `/tribal-knowledge`
- Is it a recurring analyst behavioral mistake? → redirect to `/gaps add user`

Collect required fields (one batch, not one at a time):
- **Title** — one short line (e.g. "B0 applies term filter before PFID discovery")
- **Category** — `Skill Gap` | `Data Gap` | `Output Format` | `Process Gap` | `Known Limitation`
- **Skill** — `offer-pulse` | `ces-nes` | `scorer` | `use-cases` | `general`
- **Description** — what is wrong, impact, fix direction
- **Evidence** — optional; where/when observed

Assign next GAP ID (max existing + 1, zero-padded to 3 digits). Append to gaps-log.md using the format in the **System Gap Log Format** section. Confirm: `Logged GAP-{N}: {Title}`

---

### Add User

**Routing check first.**
- Is this a recurring analyst mistake? → proceed
- Is the root cause a broken skill instruction? → redirect to `/gaps add system`
- Is the underlying cause a domain fact? → also log it in `/tribal-knowledge` and reference it in "What to say"

Collect required fields (one batch):
- **Pattern name** — short title
- **Category** — `Input Error` | `Context Error` | `Expectation Error` | `Scope Error`
- **Frequency** — `Rare (<5%)` | `Occasional (5–25%)` | `Frequent (25–50%)` | `Very Frequent (>50%)`
- **Verdict** — `Human Error Only` | `Mixed — Investigate` | `Skill Issue Masked as Human Error`
- **What the analyst does** — description of the mistake
- **How to detect** — detection signals (keywords, zero-row results, analyst pushback)
- **What to say** — response guidance; whether a skill change is warranted
- **Evidence** — optional

Assign next HE ID (max existing + 1, zero-padded to 3 digits). Append to error-log.md using the format in the **User Pattern Log Format** section. Confirm: `Logged HE-{N}: {Pattern name}`

---

### Add (Routing Check)

Read the title/description provided. Ask: "Is this a skill defect (something fixable by changing SKILL.md) or a recurring analyst mistake?" based on the content. Route to Add System or Add User accordingly, explaining the routing decision. If genuinely ambiguous, ask once.

---

### Check

**This is the primary pre-Wendy gate.** Always run this before invoking `/wendy` or acting on a `/use-cases` systemic issue.

Input: symptom text after "check".

1. Read both logs
2. For system gaps: search open entries by title + category + description keywords
3. For user patterns: search active entries by pattern name + "How to detect" keywords
4. Score all entries against symptom (keyword overlap, partial matches count)
5. Rank by score. Show all entries with at least 1 match.

Render matched system gaps:
```
System Gaps — matching: "{symptom}"

=== GAP-NNN ===
Title     : {title}
Status    : open
Category  : {category}
Match     : "{keyword}" matched in title/description

→ /gaps GAP-{N} for full detail
```

Render matched user patterns:
```
User Patterns — matching: "{symptom}"

=== HE-NNN ===
Pattern   : {name}
Verdict   : {verdict}
Frequency : {frequency}
Match     : "{keyword}" matched detection signals

What to say: {paste the "What to say" block}

→ Before invoking /wendy: confirm this is skill-caused, not input-caused.
```

For user patterns where Verdict = `Mixed — Investigate`: add:
> "This pattern overlaps with a known skill issue. Cross-check related system gaps before concluding analyst error."

If no matches in either log:
```
No matching patterns found in either log for: "{symptom}"
Proceed to /use-cases or /wendy — no known user-gap precedent.
```

After both log sections, run the **Cross-log check** against tribal-knowledge (Step 4).

---

### Resolve System

Find GAP-{N} in gaps-log.md. If not found: `GAP-{N} not found.`
If already resolved: `GAP-{N} is already resolved ({date}).`

If no resolution note provided in invocation, ask for one (one line).

1. Update entry in place: `Status : open` → `Status : resolved`
2. Set `Resolved : {today's date}`
3. Set `Resolution : {note}`
4. Write file back
5. Confirm: `Resolved GAP-{N}: {Title}`

**TK prompt:** Ask: "Does this resolution encode a permanent domain fact (e.g. 'this API always behaves X', 'this column is stored as lowercase')? If yes, consider logging it via `/tribal-knowledge add` — the skill fix handles the instruction, but the underlying fact is worth keeping permanently." Only ask; do not auto-log.

**Dedup check:** Before asking about TK, check if any existing TK entry covers the same domain fact. If a match exists, suggest cross-referencing it rather than creating a duplicate.

---

### Archive User

Find HE-{N} in error-log.md. If not found: `HE-{N} not found.`
If already archived: `HE-{N} is already archived ({date}).`

Ask for an archive reason.

1. Update entry in place: `Status : active` → `Status : archived`
2. Set archived date
3. Write file back
4. Confirm: `Archived HE-{N}: {Pattern name}`

---

### Summary

Produce a context block for skill-change evaluation:

```
Gap Context Block
─────────────────────────────────────────────────────
System gaps   : {open N} open | {resolved M} resolved
User patterns : {active N} active | {archived M} archived

Frequent user patterns (25%+):
| ID | Pattern | Frequency | Verdict |
...

Open system gaps by category:
| Category | Count |
...

→ Run /gaps check <symptom> before any skill change.
```

---

## Step 4 — Cross-Log Check (Tribal Knowledge)

Run after every **Add**, **Resolve**, **Archive**, **Check**, and **Detail** operation. Skip for List, Summary, and routing-only operations.

**Read the file directly — do not invoke `/tribal-knowledge` as a skill.**

1. Read `.claude/skills/tribal-knowledge/knowledge-log.md`
2. Extract keywords from the current subject (title + category + key terms)
3. Score all active TK entries against those keywords (partial matches count)
4. If matches found, append after the main output:

```
Cross-log (tribal-knowledge):
• TK-{N} — {Title}
```

If no matches: omit this section entirely.

---

## System Gap Log Format

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

**Format rules:**
- `## GAP-NNN` heading is the primary key. Never modify after creation.
- Status is exactly `open` or `resolved` (lowercase).
- Never reorder existing entries. Append new entries at the bottom.
- When resolving: update the existing entry in place. Never append a duplicate.

---

## User Pattern Log Format

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
{One paragraph or bullet list. Wrap at ~90 chars.}

**How to detect:**
{Bullet list of signals — these are the keywords used for /gaps check matching.}

**What to say:**
{Response guidance. State whether this warrants a skill change.}

---
```

**Format rules:**
- `## HE-NNN` heading is the primary key. Never modify after creation.
- Status is exactly `active` or `archived` (lowercase).
- Never reorder existing entries. Append new entries at the bottom.

---

## Output Constraints

- Never truncate either log table. Show all rows.
- Check mode: state the symptom verbatim before showing matches.
- Check mode: if no matches in either log, say so explicitly — do not force a partial match.
- Add: always confirm the assigned ID after writing.
- Resolve/Archive: always confirm the ID and title after writing.
- Read-only operations (list, detail, check, summary) never modify log files.
