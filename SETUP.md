# Offer Pulse — Setup Guide

Offer Pulse is a **dedicated Claude Code environment** — not a plugin you add to an existing project. You launch it in its own session from the cloned repo. All skills and context load automatically when you open it.

---

## Step 1 — Set Up the Required MCPs

Offer Pulse depends on three MCP servers. Complete all three before cloning the repo.

---

### 1a — distillery-mcp (Redshift + Alation)

This is the primary data connection. Full instructions are at the repo:
👉 https://github.com/gdcorp-dna/distillery-mcp

**Critical path:**

**Authenticate with GitHub (one-time)**
```bash
gh auth login
```
Select GitHub.com → HTTPS → Login with a web browser. When prompted, authorize SSO for GoDaddy.

**Clone and install**
```bash
git clone https://github.com/gdcorp-dna/distillery-mcp.git ~/projects/distillery-mcp
cd ~/projects/distillery-mcp
python3 install.py
```
The installer will prompt for your Redshift and Alation credentials and generate the Claude Code config. **Allow ~10 minutes.**

You'll need:
- Redshift host, username, and password
- Alation refresh token (from your Alation profile settings page)
- Alation user ID (found in the URL when you open your Alation profile)
- Alation data source ID (ask your team if unsure)

**Configure Claude Code** — the installer will show you a JSON snippet. Add it to your VS Code `settings.json`:
```json
{
  "claude.mcpServers": {
    "distillery": {
      "command": "/home/yourusername/projects/distillery-mcp/.venv/bin/python",
      "args": ["-m", "src"],
      "cwd": "/home/yourusername/projects/distillery-mcp"
    }
  }
}
```
Replace `yourusername` with your actual username.

**Verify**
```bash
python3 install.py --verify
```
Then open Claude Code and try: *"Show me my Redshift schemas"*

> **VPN required.** Claude Code routes through GoCaaS. If Claude can't reach the API, connect to VPN first.

> **API key expiry.** GoCaaS keys expire every 30 days. When yours expires you'll see an `Authentication Error - Expired Key` message. Generate a new key from GoCaaS and update `ANTHROPIC_API_KEY` in your `~/.bashrc`, then run `source ~/.bashrc`.

---

### 1b — Atlassian MCP (Jira + Confluence)

Full instructions: 👉 https://godaddy-corp.atlassian.net/wiki/spaces/ERI/pages/4192470027/Claude+Code+Not+just+for+developers#Atlassian-MCP

**Add the server:**
```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```
Authentication is via OAuth — no API tokens needed. The first time you use an Atlassian tool, Claude will open your browser to authenticate. If that doesn't trigger automatically, open Claude Code, type `/mcp`, select the Atlassian server, and authenticate from there.

---

### 1c — Catalog MCP (NES offer catalog)

```bash
claude mcp add --transport http catalog-mcp-dev https://catalog-mcp.ecomm.int.test-gdcorp.tools/mcp --scope user
```

No additional authentication required.

---

## Step 2 — Clone the Offer Pulse Repo

```bash
git clone https://github.com/dlaris30/offer-pulse.git ~/projects/offer-pulse
```

---

## Step 3 — Install the Live-Surface Scrapers

The `/live-surface` skill uses Puppeteer to scrape GoDaddy test pages for live curated offer IDs. The scripts are included in the repo under `scrapers/`.

```bash
cd ~/projects/offer-pulse/scrapers
npm install
```

This installs Puppeteer and its bundled Chromium browser (~300 MB). Only needed once.

> **VPN required.** The scraper hits `test-godaddy.com`, which is only reachable on the GoDaddy internal network. If `/live-surface` returns an empty result or a navigation timeout, connect to VPN first.

**Verify the install:**
```bash
node ~/projects/offer-pulse/scrapers/extract_curated_offers.js https://www.test-godaddy.com/hosting/wordpress-hosting 2>/dev/null
```
Should return a JSON array of curated offer objects. If it returns `[]`, check VPN.

---

## Step 4 — Add the Launch Alias

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

Claude Code opens in the Offer Pulse environment with all skills and MCP connections loaded.

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
rm -rf ~/.claude/skills/offer-pulse-external
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
