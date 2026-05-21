# Offer Pulse — Setup Guide

## Prerequisites

- **Claude Code CLI** installed and authenticated
- **distillery-mcp** configured in your Claude Code settings (contact dlaris30 if needed)

---

## One-Time Install

**1. Clone the repo**
```bash
git clone https://github.com/dlaris30/offer-pulse.git ~/projects/offer-pulse
```

**2. Add the launch alias to your shell config**

Open `~/.bashrc` (or `~/.zshrc` if you use zsh) and add:
```bash
alias offer-pulse='cd ~/projects/offer-pulse && claude'
```

Then reload it:
```bash
source ~/.bashrc
```

---

## Launch

```bash
offer-pulse
```

That's it. Claude Code opens in the Offer Pulse environment with all skills loaded.

---

## Weekly Update

Run this once a week to get the latest skill improvements:
```bash
cd ~/projects/offer-pulse && git pull
```

**What git pull will and won't affect:**
- ✅ Safe — your memory files (`~/.claude/projects/.../memory/`) are outside the repo and never touched
- ✅ Safe — any custom skills you built with unique names won't be touched
- ⚠️ Overwritten — if you edited any of the 10 skill files directly, `git pull` will replace your changes with the latest version

**If you've customized a skill file:** don't edit the cloned files. Build a separate skill with a different name — it will be ignored by git and safe from all future updates.

---

## Usage

At the Claude Code prompt, type `/offer-pulse` and provide one of:
- A Jira ticket key (e.g. `AGIGROWTH-161`)
- A surface ITC (e.g. `slp_wordpress`)
- A product name (e.g. `MWP Basic`)

The skill audits all active offers on that surface and produces a ready-to-use payload for an ecomm engineering ticket.

---

## Already have the skill files? Migrate to the repo

If you previously copied skill files (e.g. `offer-pulse/SKILL.md`) directly into your `~/.claude/skills/` folder, follow these steps to switch to the repo instead.

**1. Clone the repo**
```bash
git clone https://github.com/dlaris30/offer-pulse.git ~/projects/offer-pulse
```

**2. Remove the files you copied in manually**
```bash
rm -rf ~/.claude/skills/offer-pulse
rm -rf ~/.claude/skills/ces-nes
rm -rf ~/.claude/skills/surface-vocab
rm -rf ~/.claude/skills/package-catalog
rm -rf ~/.claude/skills/migration-check
rm -rf ~/.claude/skills/ces-packages
rm -rf ~/.claude/skills/pricing-ticket
rm -rf ~/.claude/skills/ref
rm -rf ~/.claude/skills/gaps
rm -rf ~/.claude/skills/tribal-knowledge
```

Only remove the folders you actually have — skip any that don't exist.

**3. Add the launch alias** (same as above)
```bash
alias offer-pulse='cd ~/projects/offer-pulse && claude'
source ~/.bashrc
```

From now on, launch with `offer-pulse` and update with `cd ~/projects/offer-pulse && git pull`.

---

*Questions: reach out to dlaris30*
