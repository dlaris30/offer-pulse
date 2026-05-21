---
name: wendy
description: Wendy — Offer Pulse Agent Architect. Use when you want to design a new skill, audit the current skill suite for gaps, or improve an existing skill's instruction set. Does not run queries or do analytical work.
---

# Wendy (agent launcher)

Spawns the **Wendy agent** in the background for skill architecture work, with ledger pre-flight, NES/CES architectural pre-check, and post-recommendation gap reconciliation. Returns a confirmation immediately; the design work runs unattended and you'll be notified when Wendy responds.

Arguments: $ARGUMENTS

---

## Step 0 — Ledger Pre-flight

Before analyzing the use-case log or designing any fix, run a pre-flight check to detect prior attempts and contradiction risks.

**Determine the candidate issue description:**
- If `$ARGUMENTS` names a specific issue, flag, or fix target → use that as the candidate issue description
- If `$ARGUMENTS` is a general audit request (e.g., "audit the suite for gaps") with no specific issue → skip Step 0 and proceed directly to Step 1
- If the candidate issue came from a prior `/use-cases` output (the analyst is passing Wendy a top issue from that run) → use the issue title from that output

**Invoke Mode A of `/ledger`:**

Read `.claude/skills/ledger/SKILL.md` and follow the **Mode A — Pre-flight** instructions, passing the candidate issue description.

Receive the Conflict Report.

**Interpret the result:**

If the report is `Ledger Pre-flight: CLEAR`:
- Proceed to Step 1 without delay. No output needed for the pre-flight result.

If the report is `Ledger Pre-flight: FINDINGS`:
1. Display the full Conflict Report to the analyst before proceeding.
2. For each prior attempt with verdict **FIXED** or **IMPROVED**: Wendy must explicitly state, in her final recommendation output, one of:
   - Why her proposed change does not undo that fix (explain the mechanism — e.g., "The prior fix added a guard on field X; this change modifies field Y and does not touch that guard")
   - Or acknowledge the conflict and propose a reconciliation approach (e.g., "The proposed change reverses the prior B0 filter fix — reconciliation: apply the new filter only to the CES branch, preserving the NES guard from the prior fix")
3. For prior attempts with verdict **INCONCLUSIVE**: note them as context in the recommendation but do not block — "Note: a prior INCONCLUSIVE attempt exists for this issue."
4. For prior attempts with verdict **BASELINE MISSING**: treat as no prior evidence. Proceed.
5. For a detected **contradiction**: Wendy must not proceed with the fix as described. She must either reframe the fix to avoid the contradiction or explicitly reconcile it in her recommendation.

**Wendy documents conflict resolution in her final output** under a `Conflict Resolution` section, immediately after the proposed change description. If pre-flight was CLEAR, omit this section.

---

## Step 1 — NES/CES Architecture Pre-Check

Invoke the `/ces-nes` skill by reading and following `.claude/skills/ces-nes/SKILL.md`.

Pass this question: "Review the following proposed skill work for NES/CES architectural implications. Flag any constraints, risks, or incompatibilities with the NES three-layer hierarchy, CES branch logic, offer geometry classification, or catalog resolution paths:\n\n{$ARGUMENTS}"

Capture the response as `arch_context`.

If the arguments clearly do not touch NES/CES routing (e.g. purely output formatting, unrelated skill design, non-routing logic), note `arch_context = null` and proceed without prepending it to Wendy's prompt.

---

## Step 2 — Design (Wendy)

Use the Agent tool to spawn the Wendy subagent (`wendy`), passing:
1. If a Conflict Report with FINDINGS was returned in Step 0: prepend it as `"Ledger Pre-flight Findings:\n{conflict_report}\n\n---\n\n"` before all other context
2. If `arch_context` is non-null: prepend it as `"NES/CES Architecture Context:\n{arch_context}\n\n---\n\n"` before the original arguments
3. The original `$ARGUMENTS`

Wendy will:
- Design new skills when a capability gap is identified
- Evaluate the current skill suite for gaps or redundancy
- Propose instruction set improvements for existing skills
- Produce complete draft SKILL.md files ready to save
- Train herself when asked ("train Wendy to...")
- Document conflict resolution reasoning when Step 0 returned FINDINGS

---

## Step 3 — Gap Reconciliation

After Wendy returns a recommendation, read the three knowledge logs **directly** (do not invoke as skills — that would create circular calls):

1. `.claude/skills/system-gaps/gaps-log.md`
2. `.claude/skills/user-gaps/error-log.md`
3. `.claude/skills/tribal-knowledge/knowledge-log.md`

Extract keywords from Wendy's proposed change. Score all open/active entries against those keywords (title, category, key terms — partial matches count).

If matches found, append after Wendy's output:

```
Gap Reconciliation:
• /gaps GAP-{N} — {Title}  [may be resolved by this change]
• /gaps HE-{N} — {Pattern name}  [may be addressed by this change]
• /tribal-knowledge TK-{N} — {Title}  [may need updating]
```

If no matches across any log: omit the Gap Reconciliation section entirely.

Do not auto-resolve any entries — flag only. The analyst decides what to close.

---

## Examples

- `/wendy design a skill that tracks which discount codes are active per surface`
- `/wendy audit the current suite for gaps`
- `/wendy improve offer-pulse to handle multi-surface tickets more cleanly`
- `/wendy should we build a skill for checkout-level package attribution?`
- `/wendy fix: silent candidate filtering` ← triggers Step 0 pre-flight for "silent candidate filtering"
