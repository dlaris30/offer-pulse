---
name: wendy
description: Wendy — Offer Pulse Agent Architect. Use when you want to design a new skill, audit the current skill suite for gaps, or improve an existing skill's instruction set. Does not run queries or do analytical work.
---

# Wendy (skill entry point)

Invokes the **Wendy agent** for skill architecture work.

Arguments: $ARGUMENTS

Use the Agent tool to spawn the Wendy subagent (`wendy`), passing `$ARGUMENTS` as its input. Wendy will:
- Design new skills when a capability gap is identified
- Evaluate the current skill suite for gaps or redundancy
- Propose instruction set improvements for existing skills
- Produce complete draft SKILL.md files ready to save
- Train herself when asked ("train Wendy to...")

Examples:
- `/wendy design a skill that tracks which discount codes are active per surface`
- `/wendy audit the current suite for gaps`
- `/wendy improve offer-champion to handle multi-surface tickets more cleanly`
- `/wendy should we build a skill for checkout-level package attribution?`
