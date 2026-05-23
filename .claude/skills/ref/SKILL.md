---
name: ref
description: Quick reference card for all offer-pulse skills — what each does, when to invoke it, and what it produces. Default mode outputs the static card instantly. /ref rebuild regenerates it from live skill descriptions.
---

# /ref — Skill Reference Card

## Invocation

```
/ref            ← output the reference card (fast, static)
/ref rebuild    ← re-read all skill descriptions and regenerate the card
```

---

## Default Mode

Output the reference card below verbatim. Do not read any other files.

---

## Reference Card

```
╔══════════════════════════════════════════════════════════════════╗
║              OFFER PULSE — SKILL REFERENCE CARD                  ║
╚══════════════════════════════════════════════════════════════════╝

── CORE PRODUCTION ─────────────────────────────────────────────────

/offer-pulse <ticket|ITC|product>
  Full surface audit → EP engineering ticket payload (curated offer
  creation). NES and CES paths. Primary workflow skill.

/surface-profile <ITC|alias>
  2-query lightweight scout before a full audit. Returns NES/CES
  split, top packages, top PFIDs, and last-audited date. Use first
  when you don't know a surface's state.

/surface-vocab <alias>                     e.g. "FOS", "precheck"
  Translate human surface names to specific ITCs. 680 ITCs profiled.
  Add: /surface-vocab explore <ITC>

/migration-check <ITC|product>
  Live NES% query against CLN/billing. Use before assuming a surface
  is NES or CES — migration timelines are estimates.

/ces-nes <question>
  Architecture Q&A: three-layer NES hierarchy, CES PFID arrays,
  offer resolution paths, ghost IDs, migration candidacy. Built from
  80 live catalog samples.

/ces-packages [slug]
  CES merch API reference: maps package slugs → constituent PFIDs,
  domain options, email add-ons. ~105 of ~300 packages scanned.

/package-catalog [slug]
  NES geometry reference: maps billing package_id slugs → standalone
  vs bundle, free trial flag, component count. Top 239 active slugs.

/pricing-ticket <ticket|product|ITC|PFID>
  Pricing/discount ticket builder. Produces full PFID list with
  current discount codes. Different output from /offer-pulse.

── QUALITY & TESTING ───────────────────────────────────────────────

/golden-set                                curator of expected outputs
  Add/query/promote analyst-confirmed correct answers. Oracle for
  /scorer and /batch-test. Write-only by this skill.

/scorer [case-id | inline expected]
  Score one completed offer-pulse output field-by-field. Read-only.
  Gates: NES Standalone / NES Bundle / CES.

/batch-test <case list>                    [spawns agents: isolated]
  Run multiple offer-pulse cases in isolated agents — no golden-set
  or memory visible to each agent. Scores each against the oracle.

/coverage [tree | matrix | update]
  Branch map (confirmed/hypothetical decision tree nodes + run
  counts) + lever × geometry reliability matrix.

/gaps [check | list | add | resolve]
  Unified issue tracker: GAP-NNN (skill defects) + HE-NNN (analyst
  input errors). Run /gaps check to rule out user error.

── AGENT TYPES (subagent_type values) ──────────────────────────────

Agent: general-purpose
  Open-ended research, multi-step investigation, codebase search
  when target is uncertain. Catch-all for complex delegated tasks.
  ← used by: /refresh, /use-cases, /batch-test

Agent: Explore
  Fast read-only codebase search. Use for file-pattern lookups,
  symbol/keyword greps, "where is X defined?" — not for analysis.

Agent: Plan
  Software architect. Designs implementation plans, identifies
  critical files, considers trade-offs. Use before multi-file edits.

Agent: claude-code-guide
  Q&A on Claude Code CLI, Claude Agent SDK, and the Anthropic API
  (features, hooks, caching, tool use, model versions).

── UTILITY ─────────────────────────────────────────────────────────

/tribal-knowledge [log | search | get]
  Persistent log of domain facts, quirks, and naming conventions
  that don't fit /gaps or memory. Survives session boundaries.

/ref
  This card.

── DEPRECATED (stubs removed, data files intact) ───────────────────

/branch-map   → /coverage tree
/offer-matrix → /coverage matrix
/system-gaps  → /gaps
/user-gaps    → /gaps user
/measure      → /ledger measure

════════════════════════════════════════════════════════════════════
Last rebuilt: 2026-05-17
════════════════════════════════════════════════════════════════════
```

---

## Rebuild Mode

When invoked as `/ref rebuild`:

1. Read the frontmatter `description:` field from each SKILL.md in `.claude/skills/*/SKILL.md`
2. Re-categorize skills using these groups:
   - **Core Production** — skills that directly produce analyst outputs or look up reference data
   - **Quality & Testing** — skills that validate, score, or track coverage
   - **Improvement Loop** — skills that maintain and improve the skill suite itself
   - **Utility** — everything else
3. For each active skill, write one entry in the card format above:
   - `/skill-name [key args]` on the first line with a right-aligned role tag
   - 2-line description: what it does + when/why to use it
4. Include a Deprecated section listing any SKILL.md-less directories that still contain data files
5. Replace the Reference Card section in this SKILL.md with the regenerated card
6. Update the `Last rebuilt:` date
7. Confirm: `Reference card rebuilt. N skills catalogued.`

Do not rebuild unless the analyst explicitly invokes `/ref rebuild`.
