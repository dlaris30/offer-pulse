# Offer Pulse — One Pager
*As of 2026-05-17*

---

## The Problem

After a customer checks out, two fields survive in order data: **PFID** (what SKU was sold) and **ITC** (which surface they came from). Everything about the offer they were actually shown — which bundle, which addons, what price, what discount — is gone.

The "obvious" workaround — look up the PFID in the merchandising API to find which package it belongs to — doesn't work. **A single PFID appears in many packages simultaneously.** For example, an MWP PFID may be a component of a standalone hosting offer, three different domain+email bundles, and a free trial variant. Transaction data alone cannot tell you which one the customer was shown. The merchandising API reflects offer structure, not purchase context.

This means the OLG (Offer Led Growth) team cannot answer: *"What exact offer configuration is winning on this surface right now?"* Today that answer requires a manual analyst effort per ticket, per surface.

---

## The Discovery

At add-to-cart — before checkout clears the slate — two sibling event tables share an `add_to_cart_event_id`:

| Table | What it holds |
|---|---|
| `add_to_cart_product_event_cln` | ITC + PFID (the SKU) |
| `add_to_cart_package_event_cln` | `package_id` (the offer slug) + price |

Joining on `add_to_cart_event_id` recovers the offer configuration the customer actually saw. **This join was unknown to the team as of April 2026.** The team's existing approach (session-level backtracking) was not capturing package IDs at add-to-cart — only at "remove from cart."

---

## What We Know Now

### Coverage (week of 2026-05-11 to 2026-05-17)
- **~820K add-to-cart events/week** have a `package_id` present — **43% of all add-to-cart volume**
- The 57% without `package_id` are CES (Classic eCommerce) surfaces by design — NES offers always carry a package ID, CES never do
- Coverage is stable week-over-week (±0.5%) — reliable signal, not noise

### Offer Landscape (239 active NES package_ids)
| Geometry | Package IDs | % of NES Events |
|---|---|---|
| Standalone | 121 | ~95% |
| Bundle | 98 | ~5% |

**The most important single fact:** `domain` (standalone) is **79% of all NES add-to-cart volume** — ~648K events/week from a single offer slug.

**Bundle reality check:** Bundles are ~5% of NES events but represent the highest-complexity configuration surface. The `nes-wss-*`, `dpp-*`, `mena-digital-kit-*`, `oybo-*`, and `webstoredesign-*` families are all bundles — domain + website + email in various combinations.

### NES vs CES Split (as of 2026-05-11)
- **59.7% NES** / **40.3% CES** for new purchase orders
- NES migration is ongoing — CES surfaces (null `package_id`) require a different lookup path via the merchandising API

---

## What Offer Pulse Does

Given a Jira ticket, ITC, or product name, the skill:

1. Queries billing to find all `package_id` values active on that surface in the last 7 days
2. Classifies each as NES standalone, NES bundle, or CES
3. Looks up the full offer configuration from the NES catalog (Curated Offer ID, Base Offer ID, all component IDs + per-component plans)
4. Outputs a ready-to-use payload for an ecomm engineering ticket — no manual catalog spelunking required

**Two paths:**
- **NES Path** — `package_id` present → catalog lookup → full offer spec including component IDs and plans
- **CES Path** — `package_id` null → PFID → merchandising API → package configuration

---

## Confirmed High-Confidence Examples

The following are verified cases from the Offer Pulse golden set — analyst-confirmed correct answers, each independently validated.

| Pattern | When It Applies | Confidence |
|---|---|---|
| Champion offer on an NES surface | Surface has active billing data with package IDs | High — billing is the oracle |
| Existing CES offer lookup | Offer already exists in catalog; product or PFID known | High — catalog lookup is deterministic |
| Pre-launch validation | Ticket requests offer creation; catalog may already have them | High — prevents redundant engineering work |

**CA .CA Domain + Email Essentials** (`dpp-ca-ca` surface, NES Bundle)
- *Input:* "What offer is live on the CA .CA domain surface with email included?"
- *Output:* Champion `dpp-ca-ca-solution-tier1` — M365 Email Essentials bundled, plan and discount code fully resolved. Time: ~2 min.

**Email Essentials at Domain Precheck** (Jira CMS-31421, CES Standalone)
- *Input:* Jira ticket requesting two discounted email packages for the domain purchase flow
- *Output:* Both packages already active — `temp-email-essentials-99` (DISC214228) and `temp-email-essentials-149` (DISC214229) — all PFIDs and term variants confirmed
- *Notable:* Ticket was already fulfilled in Oct 2025. Offer Pulse confirmed the work was done before any re-build began.

**M365 Online Essentials at Domain Precheck** (CES Standalone, 3 independent blind runs)
- *Input:* "M365 Online Essentials, $3.99/mo annual, dpp_precheck, new customers"
- *Output:* Champion `microsoftemail-onlineessentialsnoteams-discount-365af1f1cb` — Offer ID, plan, and discount code confirmed. Time: ~2 min.
- *Notable:* Same champion found correctly across three separate blind runs with no shared context.

**SSL Package Pre-launch Check** (Jira CMS-32825, NES Standalone)
- *Input:* Jira ticket requesting creation of 29 CES packages for a new SSL product line
- *Output:* All 29 `dlxssl-*` slugs already active in catalog under a single shared Offer ID — remaining work was surface wiring, not package creation
- *Notable:* Prevented engineering from building 29 packages that already existed.

---

## Business Value

| Use Case | Before | After |
|---|---|---|
| "What's the champion offer on slp_wordpress?" | 2–4 hours manual catalog search | ~2 min automated lookup |
| "What are all the bundle components for this NES offer?" | Requires Saritha / NES team | Fully automated component resolution |
| "Which surfaces are NES vs CES?" | Unknown without deep investigation | Instant from billing data |
| "How many distinct offer configs are active on this surface?" | Not answerable at all | Answered from 7-day billing window |
| Pricing experiment ticket creation | Manual offer spec + catalog IDs | Automated payload, engineer-ready |

**The OLG team's specific need:** For each pricing/configuration experiment ticket, they need the current champion offer identified and all offer IDs resolved before handing to engineering. Offer Pulse automates the 80% of that work that is mechanical lookup.

---

## Key Stakeholders

| Name | Role |
|------|------|
| Saurabh Mehta | Product / Program lead |
| Saritha Bhandarkar | Engineering — NES/CES offer config |
| Harsh Kapoor | Data exploration / demos |
| Manish Kumar Agarwal | Data / analytics logic |
| Ryan Beal | Pricing / experimentation |

---

*Data: `signals_platform_clickstream_cln.add_to_cart_package_event_cln` + `add_to_cart_product_event_cln` joined on `add_to_cart_event_id`. Catalog: GoDaddy NES catalog MCP (test environment). Coverage as of 2026-05-17.*
