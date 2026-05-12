# Offer Pulse

A data capability to programmatically answer: "What exact offer was a customer shown, on which surface, at what price?" — replacing today's manual add-to-cart inspection workflow.

**Status:** Pre-V1 feasibility. Data foundation validated 2026-04-16 via Helix. Awaiting engineering alignment on join approach before V1 scoping.

## Skills

| Skill | Invoke | Purpose |
|---|---|---|
| `/offer-pulse` | `offer-pulse` | Given a Jira ticket, ITC, or product name → audit all offers on that surface → produce the full EP engineering payload (curated offer creation) or pricing ticket payload (PFID list + discount codes) |

**`/offer-pulse` workflow:**
1. Pass a Jira ticket key (e.g. `AGIGROWTH-161`), an ITC (e.g. `slp_wordpress`), or a product name (e.g. "MWP Basic")
2. Skill queries 7-day billing + CLN data to find all active `package_id` values on that surface
3. Classifies each as **Standalone Offer** or **Offer Collection**, then looks up all IDs via catalog MCP
4. Outputs a ready-to-use payload for EP engineering (Curated Offer ID, Base Offer ID, all Component Offer IDs + per-component plans) or a pricing ticket (complete PFID list with current pricing and discount codes)

Supports **curated offer creation** (Path A) and **pricing / discount tickets** (Path B).

## The Core Problem

After a customer purchases, order data retains only:
- **PFID** — the product ID (what was sold)
- **ITC** — the surface/journey code (where they came from)

What is **lost** after checkout:
- **Package ID** — the specific offer bundle shown (e.g. `wordpress-o365-forever-ssl-deluxe`)
- Whether the offer was NES (catalog-backed) or CES (legacy)

## Key Definitions

| Term | Meaning |
|------|---------|
| PFID | Product/feature ID — the underlying SKU |
| Package ID | Named offer bundle (e.g. `wordpress-o365-forever-ssl-deluxe`). NES offers always have one. CES offers do not. |
| ITC | Interaction Tracking Code — surface/journey identifier. Persists into order data. Package ID does NOT. |
| NES | New eCommerce System — catalog-backed, curated offers with named package IDs |
| CES | Classic eCommerce — legacy system, no package IDs |

## The Event-Level Join (Key Discovery)

At the moment of add-to-cart, two sibling tables share `add_to_cart_event_id`:

| Table | Key Columns |
|-------|------------|
| `signals_platform_clickstream_cln.add_to_cart_product_event_cln` | `product_item_tracking_code` (ITC), `product_id`, `add_to_cart_event_id` |
| `signals_platform_clickstream_cln.add_to_cart_package_event_cln` | `package_id`, `package_category`, `package_price_usd_amt`, `add_to_cart_event_id` |

Same pattern at checkout — join on `checkout_progress_event_id`.

**This is more precise than the session-backtracking approach discussed at 4/14.** The team was not aware of this join path as of that meeting. Bring it up before V1 scoping locks in.

## Validation Status

**VALIDATED 2026-04-16** via two Helix queries.

### Query 1 — Coverage (all products, last 5 weeks)
- ~45% of all add-to-cart events have a package ID present (~720K events/week)
- Coverage is stable at ±0.5% week over week — reliable infrastructure
- The 55% without package IDs are expected: CES legacy products have no package ID by design
- Helix confirmed it used the exact same two tables identified in Alation

### Query 2 — Accuracy (PFID 1320706, last 90 days)
89 total add-to-cart events. Results:

| ITC | Package ID | Event Count |
|-----|-----------|-------------|
| slp_rstdstore | NULL | 28 |
| slp_wordpress | wordpress-openexchange-forever-ssl-deluxe | 20 |
| slp_wordpress | wordpress-o365-forever-ssl-deluxe | 18 |
| dlp_wordpress_hosting | wordpress-o365-forever-ssl-deluxe | 10 |
| dlp_wordpress_hosting | wordpress-openexchange-forever-ssl-deluxe | 6 |
| upp_d2p_dashboard_vh_buildwebsite_upp_mwp_airo | NULL | 4 |
| misc-purchase | NULL | 2 |
| slp_pro_managed_wordpress_hosting | wordpress-openexchange-forever-ssl-deluxe | 1 |

**Key findings:**
- Package IDs `wordpress-o365-forever-ssl-deluxe` and `wordpress-openexchange-forever-ssl-deluxe` confirmed ✅ — matches prior CSV ground truth
- 62% of events for this PFID have a package ID (above the 45% average — expected for a heavily NES product)
- `slp_wordpress` has 100% package attachment rate — every add-to-cart through that surface had a package ID
- `slp_rstdstore` is the highest-volume ITC (31% of events) with zero package IDs — likely a CES surface, worth flagging to engineering
- Helix discovered new surfaces not in the prior CSV analysis (`dlp_wordpress_hosting`, `upp_d2p_dashboard_vh_buildwebsite_upp_mwp_airo`, `slp_pro_managed_wordpress_hosting`) — confirms manual analysis systematically undercounts blast radius

### Test Product Anchor
- **PFID 1320706** = "Deluxe Managed Hosting for WordPress Websites - SSL included - 3 Years"
- ITCs found via Helix: `slp_rstdstore`, `slp_wordpress`, `dlp_wordpress_hosting`, `upp_d2p_dashboard_vh_buildwebsite_upp_mwp_airo`, `slp_pro_managed_wordpress_hosting`, `misc-purchase`
- NES packages confirmed: `wordpress-o365-forever-ssl-deluxe`, `wordpress-openexchange-forever-ssl-deluxe`

## Milestones

1. **Helix join validation (immediate)** — Confirm event-level join accuracy vs CSV ground truth for PFID 1320706
2. **Confluence prompt library + V1 scope (1-2 weeks from 4/14)** — Collect real user prompts from stakeholders; use to define V1 flows
3. **V1 definition and engineering kickoff** — Gate before real engineering investment

## Supplementary Tables

- `pricing_mart.site_product_price_event` — full funnel (impression → checkout → transaction), has ITC, well-documented in Alation
- `ba_site_app.itc_page_source` — ITC → pagesource lookup (surface label mapping only)
- `dna_approved.website_activity_detail` — session-level WAD, NOT row-level event data

## Open Questions

- Does `package_category` column encode NES/CES distinction? (Run DISTINCT query — still pending)
- Will the team adopt the event-level join vs their session-backtracking approach? (Bring to Saurabh/Harsh/Manish before V1 scoping) **URGENT: As of 2026-04-16 call, team confirmed their current approach is NOT finding package IDs at add-to-cart — only at "remove from cart". They may escalate to source owners. The signals_platform event-level join (validated 45% coverage) likely solves this without source team changes.**
- What does `slp_rstdstore` route to — NES or CES? High volume, zero package IDs.
- Why do some high-volume ITCs from the CSV (e.g. `dpp_precheck`, `shared_shopping_service`) not appear in the Helix results? Different time window, or different upstream table?

## Confluence Pages

| Page | URL |
|------|-----|
| Offer Pulse Use Case | https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4347528113/Offer+Pulse+Use+Case |
| Offer Pulse — DRAFT | https://godaddy-corp.atlassian.net/wiki/spaces/BI/pages/4312433019/Offer+Pulse+-+DRAFT |

## Key Stakeholders

| Name | Role |
|------|------|
| Saurabh Mehta | Product/Program lead |
| Harsh Kapoor | Demo / data exploration |
| Manish Kumar Agarwal | Data / analytics logic |
| Saritha Bhandarkar | Engineering (NES/CES, offer config) |
| Ryan Beal | Pricing / experimentation |
| Alexandra Anderson | Pricing / reporting |
| Herwin Gill | Growth / experimentation |
| Jade Hunter | Pricing validation |
