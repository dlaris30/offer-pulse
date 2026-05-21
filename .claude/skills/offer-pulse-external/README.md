# offer-pulse-external

A Claude Code skill for auditing ecommerce offer surfaces and producing the data payload needed to file curated offer creation tickets with ecomm engineering.

---

## What this skill does

Given a Jira ticket key, a surface ITC, or a product name, the skill queries billing and clickstream data to find every active offer currently running on that surface, classifies each one as NES (catalog-backed) or CES (legacy), and produces a complete, ready-to-use payload for your ecomm engineering ticket. The standard path — when a surface has billing `package_id` data — produces a curated offer creation payload with the Curated Offer ID, Base Offer ID, all Component Offer IDs, and per-component plans filled in. For legacy CES surfaces that have no package ID data, the skill follows a separate path using the merchandising API to identify the constituent PFIDs and candidate packages. The skill also handles offer modification requests — if you are adding a new product component to an existing offer rather than creating a new one, tell the skill that upfront and it will scope the output accordingly.

---

## What you need before you start

1. **Claude Code** installed — either the CLI (`claude`) or the Claude Code desktop app. See [https://claude.ai/code](https://claude.ai/code) for installation instructions.

2. **Distillery MCP** configured in your Claude Code settings — this gives the skill access to Redshift and the `pricing_experiment_dev` tables it queries for billing and CLN add-to-cart data. If you do not have Distillery MCP set up, contact the data infrastructure team or ask dlaris30.

3. **Catalog MCP** (`catalog-mcp-dev`) configured — this gives the skill access to the GoDaddy ecommerce catalog for offer ID and curated offer lookups. Without it, the NES path cannot resolve Curated Offer IDs or Component Offer IDs and will stall.

4. **Atlassian MCP** (optional but recommended) — when you pass a Jira ticket key as input (e.g., `AGIGROWTH-161`), this lets the skill fetch the ticket description directly so you do not have to copy-paste fields manually. Without it, the skill will ask you to provide the surface, product, term, and market yourself.

5. **Redshift access** to the `pricing_experiment_dev` schema (read-only). If you see a permission error on your first run, request access through the standard AD group process for that schema. No other schemas are required for basic use.

---

## Bootstrapping (one-time setup)

**Route A — Already have Distillery MCP set up:**

1. Pull the latest from the repo:
   ```
   git pull
   ```

2. Copy the skill file:
   ```
   cp -r .claude/skills/offer-pulse-external ~/.claude/skills/
   ```

3. **Restart Claude Code** (or open a new session window). Claude Code reads skill files at session start, so an existing session will not see the new skill until you restart.

---

**Route B — Don't have Distillery MCP yet:**

This skill requires Distillery MCP to be installed and configured first — it provides the Redshift and catalog connections the skill queries at runtime. Set that up here: **https://github.com/gdcorp-dna/distillery-mcp**

Once Distillery MCP is running, follow Route A above.

4. **Verify the install.** In a new Claude Code session, type:
   ```
   /offer-pulse-external
   ```
   Claude should acknowledge the skill and ask what surface or ticket you want to audit. If it does not recognize the command, double-check that the folders were copied to the right location and each contains a `SKILL.md` file.

---

---

## How to use it

Three ways to invoke the skill, depending on what you have on hand:

**1. Jira ticket key (recommended)**
```
/offer-pulse-external AGIGROWTH-161
```
The skill fetches the ticket and extracts the surface, product, term, and market automatically. Requires the Atlassian MCP (see prerequisites).

**2. ITC string**
```
/offer-pulse-external slp_wordpress
```
Audits all active offers on that surface. Use this if you already know the ITC and do not have a ticket to point to.

**3. Product name**
```
/offer-pulse-external "MWP Basic"
```
The skill resolves the product name to PFIDs first, then audits the relevant surfaces. This path takes slightly longer because of the extra lookup step.

**Clarifying questions:** If the skill needs to know the market (US vs DEM vs ROW), the billing term (1-year, 2-year, 3-year), or the customer segment (new purchase vs renewal) before it can run, it will ask. You will get results faster if you answer all questions in a single reply rather than one at a time.

---

## Understanding the output

The skill produces a **Quick Reference block** for each active offer found on the surface. Each block covers one offer and contains the fields an ecomm engineer needs to create the curated offer — Champion (the existing offer to clone from), Curated Offer ID, Base Offer ID, Component Offer IDs, and per-component plans.

**The Champion line is the most important field.** It identifies the existing curated offer that ecomm will use as the starting point for your new experiment or configuration. Make sure this matches what your ecomm contact expects before you file the ticket.

**Confidence labels:** When a surface has no billing `package_id` data — meaning it is a legacy CES surface — the Champion and Route lines are labeled `INFERRED`. This means the output was derived from keyword matching or merchandising API lookups rather than from direct billing history. Inferred output is a strong recommendation, not a guaranteed match. Validate with your ecomm engineer before filing the ticket.

**Supporting Detail:** By default the skill outputs only the Quick Reference block. If you need the full breakdown — raw CLN counts, all candidate packages considered, filtering criteria applied — ask for Supporting Detail explicitly after the initial output.

---

## Getting updates

When the skill is updated, pull the latest from the repo and re-copy the files:

```
git pull
cp -r .claude/skills/offer-pulse-external ~/.claude/skills/
```

No other steps are needed. Claude Code reads skill files fresh at the start of each session, so the update takes effect immediately in your next session.

---

## Questions or issues

Contact **dlaris30** on GitHub. File bugs or feature requests in the `distillery-mcp` repo. If you are not sure whether an issue is with the skill or with your MCP configuration, the quickest path is to paste the error message and your input into a Slack message to dlaris30 directly.
