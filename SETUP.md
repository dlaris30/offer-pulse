# Offer Pulse — Setup Guide

## Prerequisites

- **Claude Code CLI** installed and authenticated
- **distillery-mcp** configured in your Claude Code settings (contact dlaris30 if needed)

---

## One-Time Install

**1. Clone the repo**
```bash
git clone https://github.com/dlaris30/offer-pulse.git ~/offer-pulse
```

**2. Add the launch alias to your shell config**

Open `~/.bashrc` (or `~/.zshrc` if you use zsh) and add:
```bash
alias offer-pulse='cd ~/offer-pulse && claude'
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
cd ~/offer-pulse && git pull
```

---

## Usage

At the Claude Code prompt, type `/offer-pulse` and provide one of:
- A Jira ticket key (e.g. `AGIGROWTH-161`)
- A surface ITC (e.g. `slp_wordpress`)
- A product name (e.g. `MWP Basic`)

The skill audits all active offers on that surface and produces a ready-to-use payload for an ecomm engineering ticket.

---

*Questions: reach out to dlaris30*
