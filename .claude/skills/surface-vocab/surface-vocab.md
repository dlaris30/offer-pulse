# Surface Vocabulary

Last updated  : 2026-05-20
ITCs explored : 685 of 685 (100%) — 685 fully profiled, 0 in bulk reference table

---

## Human Term Index

| If someone says... | They mean | ITC prefix / specific ITC |
|---|---|---|
| front of site | FOS / Sales Landing Page | `slp_*` |
| FOS | FOS / Sales Landing Page | `slp_*` |
| sales page | FOS / Sales Landing Page | `slp_*` |
| landing page | FOS / Sales Landing Page | `slp_*` |
| SLP | FOS / Sales Landing Page | `slp_*` |
| domain checkout | Domain Purchase Path | `dpp_*` |
| DPP | Domain Purchase Path | `dpp_*` |
| domain purchase path | Domain Purchase Path | `dpp_*` |
| checkout | Domain Purchase Path (primary) | `dpp_*` |
| domain landing page | Domain Landing Page | `dlp_*` |
| DLP | Domain Landing Page | `dlp_*` |
| upsell | Upsell / Upgrade Path | `upp_*` |
| upgrade | Upsell / Upgrade Path | `upp_*` |
| UPP | Upsell / Upgrade Path | `upp_*` |
| my account | My Account | `mya_*` |
| MYA | My Account | `mya_*` |
| account page | My Account | `mya_*` |
| renewals | My Account (renewal contains) | `account_myrenewals_*`, `single_product_renewal`, `*renewal*` |
| domain control center | Domain Control Center | `dcc` (contains) |
| DCC | Domain Control Center | `dcc` (contains) |
| Domain Discount Club | Domain Discount Club | `ddc_*` |
| DDC | Domain Discount Club | `ddc_*` |
| cart | Cart | `cart_*`, `misc-purchase`, `notifications_bell`, `*xsell*` |
| shopping cart | Cart | `cart_*` |
| Venture Home | Venture Home | `vh_*`, `ai_onboarding*`, `airohq*` |
| VH | Venture Home | `vh_*` |
| Airo HQ | Venture Home | `airohq*`, `airo_hq*` |
| homepage quickbuy | Homepage Quickbuy | `hp_*` |
| HP | Homepage Quickbuy | `hp_*` |
| GoDaddy Pro | GoDaddy Pro | `pro_*`, `wp_*` |
| Pro dashboard | GoDaddy Pro | `pro_*` |
| Web Pro | GoDaddy Pro | `wp_*` |
| C3 | C3 Sales Site | `mgr_*`, `crm_*`, `shared_shopping_service` |
| reseller | C3 Sales Site / Reseller | `mgr_*`, `crm_*` |
| aftermarket | Aftermarket | `am_*`, `*parked*`, `*tdfs*`, `*buynow*` |
| cash parking | Aftermarket | `*parked*` |
| in-app | GDAPP — In-Product | `app_*`, `studio_*`, `mob_*` |
| GDAPP | GDAPP — In-Product | `app_*`, `studio_*`, `android_*`, `ios_*`, `mob_*` |
| after checkout | After Checkout Special | `auction_*`, `gdc_*` |
| GoCentral | P&C — Website Builder | `*gocentral*` |
| P&C | P&C — Website Builder | `*gocentral*` |
| vNext | P&C — Website Builder | `*gocentral*` |

---

## Prefix Groups

*Priority-ordered matching rules from source of truth (2026-05-20). Match types: Prefix (ITC starts with), Suffix (ITC ends with), Contains (ITC contains anywhere), Exact. When multiple rules match, the higher-priority rule (lower number) wins.*

---

### SLP — Sales Landing Pages (Front of Site)

**Patterns (Priority 15–18, 37, 44, 48–51):**
`slp_` prefix · `slp-` prefix (hyphen) · `_lp` suffix · `domains_valuation_lp_purchase` exact · `hmc_` prefix · `lp_` prefix · `ssl` contains · `recore` contains · `sem_bl_airo_claim` contains · `madmimi` contains
**Human terms:** front of site, FOS, sales page, landing page, SLP, homepage
**ORG:** performance_marketing
**What it is:** The primary pre-purchase marketing pages where customers first encounter a product. Highest-traffic surfaces. Mix of NES and CES depending on product. The `slp-` hyphen variant (e.g. `slp-boost`) is a separate naming convention but same surface family. `hmc_*` = Homepage Multi-Channel. `lp_*` = landing page variants. `_lp` suffix pattern (e.g. `showinbio_lp`) also maps here.
**Full profiles:** 79

### DPP — Domain Purchase Path

**Patterns (Priority 10–12, 26):**
`dpp_` prefix · `_dpp` suffix · `_dpp` mid-string contains · `bulk_search` exact
**Human terms:** domain checkout, DPP, checkout flow, domain purchase
**ORG:** performance_marketing
**What it is:** The checkout flow triggered after a domain search. Surfaces here are shown add-on offers at the moment of domain purchase. The `_dpp` suffix and contains patterns (e.g. `site_search_dpp`) route non-prefixed ITCs into this group. International market variants use `dpp-intl-*` and `dpp-{market}-{ccTLD}-*` (hyphen prefix — geo is explicit in slug).
**Full profiles:** 35

### DLP — Dynamic Landing Page

**Patterns (Priority 21):**
`dlp_` prefix
**Human terms:** DLP, domain landing page
**ORG:** performance_marketing
**What it is:** Product landing pages reached from domain-related journeys. Distinct from SLP — these are mid-funnel pages, not the top-of-funnel sales pages.
**Full profiles:** 33

### UPP — Universal Plans & Pricing

**Patterns (Priority 19):**
`upp_` prefix
**Human terms:** upsell, upgrade, UPP, plan change
**ORG:** AGI
**What it is:** Purchases flowing through the UPP platform — GoDaddy's centralized system for plan, pricing, and discount configuration. Powers purchase, upgrade, downgrade, renewal, and free-to-paid conversion flows across in-product dashboards and the customer account area.

**ITC structure (source: Confluence PC/4311190879, updated 2026-05-15):**

Two formats are in use — v1 (older) includes a product segment; v2 (current) drops it:

| Format | Structure |
|---|---|
| v2 (current) | `UPP_[conversion_type]_[app \| entry_point]_[overrideItc?]` |
| v1 (older) | `UPP_[product]_[conversion_type]_[app]_[entry_point]_[overrideItc?]` |

**Conversion type** (position 2 in v2, position 3 in v1 — always one of):
- `d2p` = direct to paid (new purchase, no prior subscription)
- `f2p` = free to paid (trial → paid conversion)
- `p2p` = paid to paid (plan change, renewal, tier upgrade)

**`app` segment** — where in the product UI the flow originates:
`dashboard`, `vnext-dashboard`, `panel-lite`, `productivity`, `dcc`, `websites`, `sites`, `start`, `account`, `airo-builder`, `airo-compliance`, `airo-sentinel`, `conversations`, `brandbook` — unknown falls back to `unknown-entry-` or `unknown-entry-point`

**`product` segment** (v1 only — ProductId from UPP's enum):
`wamproduct`, `o365product`, `titanproduct`, `dopproduct` (+ `_combo` / `_ultimate` / `_standalone` variants), `managedwordpressproduct`, `webhostingproduct`, `conversationsproduct`, `airobuilderproduct`, `airobuildercreditsproduct`, `logoimageproduct`, `complianceproduct`

**`overrideItc`** (optional tail segment): if a full UPP ITC string, returned as-is; if partial, appended. Explains long tails like `...upgrade_upp_dopproduct`.

**Full profiles:** 217

### MYA — My Account

**Patterns (Priority 13, 43, 47):**
`mya_` prefix · `renewal` contains · `mui_` prefix
**Human terms:** my account, MYA, account page, customer portal, renewals, my renewals
**ORG:** AGI
**What it is:** In-account surfaces shown to existing customers. Renewal offers, upgrade prompts, and cross-sell recommendations. The `renewal` contains pattern covers `account_myrenewals_jtbd`, `account_myrenewals_single`, and `single_product_renewal` — these are classified MYA despite not using the `mya_` prefix. The `mui_` prefix covers My Account UI component surfaces (e.g. `mui_calendar`).
**Full profiles:** 31

### DCC — Domain Control Center

**Patterns (Priority 9, 57):**
`dcc` contains (any ITC containing "dcc") · `whois_serp` prefix · `whoisserp` prefix
**Human terms:** DCC, domain control center, WHOIS, domain management
**ORG:** AGI
**What it is:** Surfaces within the domain management interface. Note: `dcc` is a **contains** match — any ITC containing "dcc" anywhere is DCC (not just `dcc_` prefix). `whois_serp*` and `whoisserp*` are also DCC. **See also: `ddc_` (Domain Discount Club) — a completely separate group with a different prefix.**
**Full profiles:** 31

### CART — Cart

**Patterns (Priority 22, 38–40):**
`cart_` prefix · `misc-purchase` contains · `notifications_bell` contains · `xsell` contains
**Human terms:** cart, shopping cart, cross-sell, in-cart upsell
**ORG:** performance_marketing
**What it is:** Cart and in-cart surfaces. Mix of NES (domain-search cart boxes like `cart_bottom_expresssearch`) and CES (inline cross-sell surfaces like `cart_xsells_inline`, `notifications_bell`, `misc-purchase`).
**Full profiles:** 4 (cart_bottom_expresssearch, cart_xsells_inline, misc-purchase, notifications_bell)

### VH — Venture Home

**Patterns (Priority 3, 5, 24, 56):**
`dpp_bundling_is` exact · `airo_hq` / `airohq` contains · `vh_` prefix · `ai_onboarding` prefix
**Human terms:** Venture Home, VH, Airo HQ, AI onboarding
**ORG:** AGI
**What it is:** Venture Home — GoDaddy's AI-powered website builder and small business hub. Includes `dpp_bundling_is` (domain purchase with bundling step — routes to VH despite the `dpp_` prefix), all Airo HQ surfaces, and the AI onboarding flow (`ai_onboarding_*`).
**Full profiles:** 0 (not yet explored)

### HP — Homepage Quickbuy

**Patterns (Priority 25):**
`hp_` prefix
**Human terms:** homepage quickbuy, HP
**ORG:** performance_marketing
**What it is:** Homepage quick-buy domain search and purchase entry points.
**Full profiles:** 0 (not yet explored)

### DDC — Domain Discount Club

**Patterns (Priority 23):**
`ddc_` prefix
**Human terms:** Domain Discount Club, DDC
**ORG:** AGI
**What it is:** Domain Discount Club surfaces — **distinct from DCC (Domain Control Center)**. Different prefix (`ddc_` vs `dcc`), different product, different org. `ddc_pro_01` is DDC; `dcc_portfolio_renewal` is DCC. Do not confuse these.
**Full profiles:** 0 (not yet explored)

### MGR / C3 — C3 Sales Site

**Patterns (Priority 6–7, 27–28, 59):**
`mgr_` prefix · `mgrzed0ov` exact · `shared_shopping_service` exact · `crm_` prefix · `copilot` contains · `conversations` contains
**Human terms:** C3, C3 sales site, reseller, manager, MGR, CRM
**ORG:** C3
**What it is:** C3 Sales Site — the internal GoDaddy sales tool used by sales agents. Includes CRM surfaces (`crm_*`) and AI-assisted sales surfaces (`copilot`, `conversations`). **Exception:** `netgdpipeline_injecttaxproducts` (100% Conversations product) is an **internal data pipeline**, NOT a C3 sales surface — do not attempt offer resolution for it despite the `conversations` contains match.
**Full profiles:** 0 (not yet explored)

### GDAPP — In-Product / Mobile App

**Patterns (Priority 8, 52–55):**
`app_` prefix · `studio_` prefix · `android_` prefix · `ios_` prefix · `mob_` prefix
**Human terms:** in-app, GDAPP, mobile app, iOS, Android, Studio
**ORG:** AGI
**What it is:** In-product upgrade and add-user flows within GoDaddy's mobile apps (iOS, Android) and Studio. All CES. `app_*` = web in-product. `studio_*` = GoDaddy Studio app. `mob_*` = mobile generic.
**Full profiles:** 0 (not yet explored)

### PRO — GoDaddy Pro

**Patterns (Priority 45–46):**
`pro_` prefix · `wp_` prefix
**Human terms:** GoDaddy Pro, Pro dashboard, Web Pro microsite, Pro
**ORG:** AGI
**What it is:** GoDaddy Pro portal surfaces — targeting freelancers and web professionals. `wp_` = Web Pro microsite. **Important disambiguation:** `wp_` prefix (e.g. `wp_client_card`) = GoDaddy Web Pro, NOT WordPress. WordPress hosting surfaces use the `_wordpress` token within `slp_`, `dlp_`, or `upp_` ITCs — not the standalone `wp_` prefix.
**Full profiles:** 0 (not yet explored)

### PLP — Single Landing Page (PLP variant)

**Patterns (Priority 29):**
`plp_` prefix
**Human terms:** PLP, product landing page
**ORG:** performance_marketing
**What it is:** Product-specific landing pages. Performance marketing. Treat like `slp_*` for NES/CES routing — check CLN for package_id presence.
**Full profiles:** 0 (not yet explored)

### MLP — Multi Landing Page

**Patterns (Priority 31):**
`mlp_` prefix
**Human terms:** MLP, multi landing page, multi-product landing page
**ORG:** performance_marketing
**What it is:** Multi-product landing pages. Performance marketing.
**Full profiles:** 0 (not yet explored)

### AM — Aftermarket

**Patterns (Priority 30, 32–34):**
`am_` prefix · `parked` contains · `tdfs` contains · `buynow` contains
**Human terms:** aftermarket, cash parking, marketplace, parked page, buynow
**ORG:** OTHER
**What it is:** Aftermarket and cash-parking surfaces. Not standard purchase flows — monetized parked domain pages and marketplace entries. Do not attempt standard curated offer resolution for these surfaces.
**Full profiles:** 0 (not yet explored)

### ACS — After Checkout Special

**Patterns (Priority 35, 41):**
`auction_` prefix · `gdc_` prefix
**Human terms:** after checkout, ACS, auction, post-purchase, GDC
**ORG:** AGI
**What it is:** After-checkout special offer surfaces. `auction_*` = Afternic/domain auction surfaces post-checkout. `gdc_*` = GoDaddy post-checkout surfaces.
**Full profiles:** 0 (not yet explored)

### P&C — Website Builder (GoCentral / vNext / WSB 7)

**Patterns (Priority 36):**
`gocentral` contains
**Human terms:** P&C, vNext, WSB 7, GoCentral, website builder (classic)
**ORG:** AGI
**What it is:** P&C (Products & Content) website builder surfaces — the older GoCentral / WSB 7 / vNext family. Distinct from the current WAM/Websites & Marketing product.
**Full profiles:** 0 (not yet explored)

### MYP — My Products

**Patterns (Priority 14):**
`myproducts-` prefix
**Human terms:** My Products, MYP
**ORG:** AGI
**What it is:** My Products area surfaces. Not in the standard ITC surface list. AGI-managed.
**Full profiles:** 0 (not yet explored)

### DNA — DNA Purchase Path

**Patterns (Priority 20):**
`dna_` prefix
**Human terms:** DNA, DNA purchase path, aftermarket auction
**ORG:** AGI
**What it is:** DNA (Domain Name Authority) purchase path — used for aftermarket/escrow domain purchases. Not a standard customer-facing offer surface. Do not attempt offer resolution.
**Full profiles:** 0 (not yet explored)

### Migration

**Patterns (Priority 4):**
`migration_` prefix
**Human terms:** migration
**ORG:** Migration
**What it is:** Product migration surfaces — internal flows for migrating customers between product versions. Not a purchase surface.
**Full profiles:** 0 (not yet explored)

### OTHER — Unclassified / Catch-all

**Patterns (Priority 42, 60):**
`em_domain_attach` contains · `*` default (any ITC not matched above)
**Human terms:** (none standard)
**What it is:** `em_domain_attach` = Email drop-to-cart surfaces (check with BA before routing). Default `*` = catch-all for any ITC not matched by a more specific rule.
**Full profiles:** varies

### Special cases

- **Empty / null ITC (Priority 1):** Group: Null. Not a customer-facing surface — skip offer resolution.
- **`N/A` exact (Priority 2):** Group: N/A. Not a trackable surface — skip offer resolution.

---

## Individual ITC Profiles

## [ITC] slp_wordpress

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : WordPress Hosting Sales Page
Page source   : not mapped (seed entry)
Products      : Managed WordPress Hosting
NES/CES       : NES
Top packages  : wordpress-o365-forever-ssl-deluxe, wordpress-openexchange-forever-ssl-deluxe, wordpress-o365-forever-ssl-basic
Champion      : —
Volume        : ~38 orders/week — Medium
Explored      : 2026-05-15 (seed — from prior catalog work)
Notes         : 100% package attachment rate — every add-to-cart through this surface has a package ID. Primary NES surface for WordPress.

## [ITC] slp_hosting_4gh

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : cPanel Hosting Sales Page (Go Hosting / 4GH)
Page source   : not mapped (seed entry)
Products      : cPanel Shared Hosting, WordPress Hosting
NES/CES       : NES
Top packages  : cpanel-o365-tier1, cpanel-o365-tier2, cpanel-o365-tier3, cpanel-set-1-economy-ssl-365-xtra
Champion      : —
Volume        : High
Explored      : 2026-05-15 (seed — from prior catalog work)
Notes         : One of the two confirmed NES hosting surfaces (alongside dpp_ domain surfaces). All cPanel + M365/OX bundles live here.

## [ITC] slp_rstdstore

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Standard/Shared Hosting Store
Page source   : not mapped (seed entry)
Products      : Shared Hosting (likely CES)
NES/CES       : CES
Top packages  : none (CES — no package IDs)
Champion      : —
Volume        : High (~28 orders/90d for PFID 1320706 alone)
Explored      : 2026-05-15 (seed — from Helix validation data)
Notes         : 31% of add-to-cart events for PFID 1320706 came through here but with zero package ID — confirmed CES surface.

## [ITC] dpp_precheck

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout Pre-Check (Add-on Offer Step)
Page source   : not mapped (seed entry)
Products      : Email (M365 Email Essentials), SSL, domain add-ons
NES/CES       : NES
Top packages  : temp-email-essentials-99, temp-email-essentials-149
Champion      : temp-email-essentials-99 / temp-email-essentials-149 (confirmed live production)
Volume        : High
Explored      : 2026-05-15 (seed — from champion validation work)
Notes         : The pre-checkout add-on step in the domain purchase flow. Confirmed NES with live temp- prefix champions. Do NOT treat temp- slugs as test artifacts.

## [ITC] dlp_wordpress_hosting

Prefix group  : dlp — Domain Landing Page
Human label   : WordPress Hosting Domain Landing Page
Page source   : not mapped (seed entry)
Products      : Managed WordPress Hosting
NES/CES       : NES
Top packages  : wordpress-o365-forever-ssl-deluxe, wordpress-openexchange-forever-ssl-deluxe
Champion      : —
Volume        : ~16 orders/90d for PFID 1320706 — Low
Explored      : 2026-05-15 (seed — from Helix validation data)
Notes         : Mid-funnel WordPress landing page. Same NES packages as slp_wordpress.

## [ITC] upp_d2p_dashboard_vh_buildwebsite_upp_mwp_airo

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Dashboard → Build Website → Managed WordPress (Airo) Upsell
Page source   : not mapped (seed entry)
Products      : Managed WordPress Hosting (Airo variant)
NES/CES       : CES (no package ID)
Top packages  : none (CES)
Champion      : —
Volume        : ~4 orders/90d for PFID 1320706 — Low
Explored      : 2026-05-15 (seed — from Helix validation data)
Notes         : In-dashboard upsell targeting customers building a website, specifically surfacing MWP with Airo. Long ITC encodes the full funnel path.

## [ITC] slp_pro_managed_wordpress_hosting

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Pro Managed WordPress Hosting Sales Page
Page source   : not mapped (seed entry)
Products      : Managed WordPress Hosting (Pro tier)
NES/CES       : NES
Top packages  : wordpress-openexchange-forever-ssl-deluxe
Champion      : —
Volume        : ~1 order/90d for PFID 1320706 — Low
Explored      : 2026-05-15 (seed — from Helix validation data)
Notes         : Dedicated sales page for the Pro MWP tier. Low volume for this PFID — may be higher for other MWP PFIDs.

## [ITC] misc-purchase

Prefix group  : CART
Human label   : Miscellaneous Purchase (unclassified)
Page source   : not mapped (seed entry)
Products      : Various
NES/CES       : CES (no package ID observed)
Top packages  : none
Champion      : —
Volume        : Low
Explored      : 2026-05-15 (seed — from Helix validation data)
Notes         : Catch-all ITC. Likely used when the originating surface is unknown or not tracked. Treat as CES until evidence otherwise.

## [ITC] dpp_absol1.primary_exact

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Registration Checkout — Absolute Step 1 (Primary Exact)
Page source   : not mapped
Products      : Domain Name Registration (dominant ~91%), Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain, redemption (skip — ghost)
Champion      : edf13c43-7d39-4f90-aa81-b40666d51f75 (curatedOfferId "domain", active Rev 3)
Volume        : 873,431 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Highest-volume unexplored ITC in the dataset. The .primary_exact suffix is an experimentation routing suffix — base ITC is dpp_absol1. Domain registration is overwhelmingly dominant. Package "domain" resolved in catalog (NES, active). Package "redemption" is a known ghost — skip catalog call.

## [ITC] mya_dom_srch.primary_exact

Prefix group  : mya — My Account
Human label   : My Account Domain Search Result — Add to Cart (Primary Exact)
Page source   : not mapped
Products      : Domain Name Registration (dominant ~97%), Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain
Champion      : edf13c43-7d39-4f90-aa81-b40666d51f75 (curatedOfferId "domain", active Rev 3)
Volume        : 297,395 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search initiated from within My Account. Same "domain" champion as dpp_absol1. The .primary_exact suffix is an experimentation routing suffix — base ITC is mya_dom_srch. First mya_ profile in vocabulary.

## [ITC] single_product_renewal

Prefix group  : MYA (renewal contains)
Human label   : Single Product Renewal
Page source   : not mapped
Products      : Domain Name Registration (57%), MS Office 365 (13%), Domain Ownership Protection (10%), CnP Hosting (6%), Websites and Marketing (6%), Open XChange (2%), WordPress Managed Plans (1%), Website Protection (1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 179,826 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Broad renewal surface covering nearly every product line. No package IDs observed — pure CES. Very high product diversity (8+ PNL lines). Renewal-path offers here are not NES-managed. Do not attempt curated offer resolution for this surface.

## [ITC] dpp_config1

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout Configuration Step 1 (Add-on Selection)
Page source   : not mapped
Products      : Domain Ownership Protection / Privacy (62%), MS Office 365 (23%), Vendor Email (15%), Airo (<1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 141,342 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : The add-on configuration step during domain checkout — where privacy protection and email are upsold. No package IDs — CES surface despite being within the dpp_ (NES-adjacent) journey. Distinct from dpp_precheck (which IS NES).

## [ITC] dcc_portfolio_renewal_dop_add_cart

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center Portfolio Renewal — Add Domain Privacy (DOP) to Cart
Page source   : not mapped
Products      : Domain Name Registration (75%), Domain Ownership Protection / Privacy (18%), Redemption (5%), Website Protection (1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 140,670 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-DCC surface where customers renewing their domain portfolio are prompted to add Domain Ownership Protection. CES surface. First dcc_ profile in vocabulary. DOP = Domain Ownership Protection (privacy product).

## [ITC] notifications_bell

Prefix group  : CART
Human label   : Notification Bell — In-app Renewal and Upsell Alerts
Page source   : not mapped
Products      : Domain Name Registration (40%), MS Office 365 (19%), Domain Ownership Protection (10%), Websites and Marketing (9%), CnP Hosting (8%), Open XChange (3%), Value Adds (2%), WordPress Managed Plans (2%), Vendor Email (1%), Website Protection (1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 131,406 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : The bell/notification icon in the GoDaddy UI. Renewal and upsell alerts shown to logged-in customers. Extremely broad product mix across all major PNL lines. Pure CES. Do not attempt curated offer resolution for this surface.

## [ITC] mya_acctsettings_subscriptions_multiselect

Prefix group  : mya — My Account
Human label   : My Account Settings → Subscriptions (Multi-select Renewal)
Page source   : not mapped
Products      : Domain Name Registration (37%), MS Office 365 (21%), Domain Ownership Protection (9%), Websites and Marketing (6%), CnP Hosting (4%), SSL (4%), Value Adds (3%), Virtual Hosting (3%), Domain Marketplace (3%), Open XChange (2%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 127,623 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : The subscription management page in My Account Settings where customers can select multiple products for renewal at once. Broad product mix. Pure CES.

## [ITC] cart_xsells_inline

Prefix group  : CART
Human label   : Cart Cross-sells Inline (Add-on Upsell in Cart)
Page source   : not mapped
Products      : Domain Ownership Protection (67%), MS Office 365 (22%), Vendor Email (10%), SSL (<1%), Open XChange (<1%), Website Protection (<1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 105,045 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Inline add-on upsell section rendered within the cart page. Much narrower product mix than other renewal surfaces — heavily DOP and email (M365/Vendor), consistent with cart-stage add-on offers. Pure CES.

## [ITC] account_myrenewals_jtbd

Prefix group  : MYA (renewal contains)
Human label   : My Renewals — Jobs to Be Done View
Page source   : not mapped
Products      : Domain Name Registration (48%), MS Office 365 (19%), Domain Ownership Protection (10%), Websites and Marketing (7%), CnP Hosting (5%), Open XChange (2%), Value Adds (2%), SSL (1%), WordPress Managed Plans (1%), Vendor Email (1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 104,159 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : JTBD = "Jobs to Be Done" — a specific UX view in the My Renewals section, framed around what the customer wants to accomplish. Broad product mix mirrors the overall renewal portfolio. Pure CES. See also: account_myrenewals_single (sibling ITC, single-item view).

## [ITC] account_myrenewals_single

Prefix group  : MYA (renewal contains)
Human label   : My Renewals — Single Item Renewal View
Page source   : not mapped
Products      : Domain Name Registration (48%), MS Office 365 (14%), Domain Ownership Protection (11%), CnP Hosting (7%), Websites and Marketing (5%), Open XChange (2%), Value Adds (2%), SSL (2%), Virtual Hosting (2%), WordPress Managed Plans (2%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 99,758 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Single-item renewal flow within the My Renewals section. Very similar product mix to account_myrenewals_jtbd — these are sibling surfaces. Pure CES. See also: account_myrenewals_jtbd (sibling ITC, JTBD multi-item view).

## [ITC] dcc_portfolio_renew_domain

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center Portfolio Renewal — Domain Renew
Page source   : not mapped
Products      : Domain Name Registration (88%), Domain Ownership Protection (8%), Redemption (4%), Website Protection (<1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 95,520 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : DCC renewal surface focused on domain renewal specifically (vs dcc_portfolio_renewal_dop_add_cart which targets privacy add-on). Pure CES.

## [ITC] dpp_absol1.primary_organicspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Registration Checkout — Organic Spin Variant (Primary Available Domain)
Page source   : not mapped
Products      : Domain Name Registration (97%), Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain, oybo-en-email
Champion      : domain → edf13c43 (active Rev 3); oybo-en-email → e328092f (active Rev 1, plan=defaultEmailessentialsee, disc971321)
Volume        : 74,006 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Part of the dpp_absol1.* experiment routing family (see also: primary_exact, unavailable_organicspin, primary_tldcard, etc.). "organicspin" = organic search/spin experiment variant for available domains. Uniquely serves both a domain offer AND an email add-on (oybo-en-email). The oybo-en-email offer (Office 365 by brand) appears alongside domain as a bundled email upsell at checkout.

## [ITC] netgdpipeline_injecttaxproducts

Prefix group  : other (netgdpipeline_ — internal pipeline prefix)
Human label   : NetGD Tax Pipeline — Inject Tax Products (Internal)
Page source   : not mapped
Products      : Conversations (100%)
NES/CES       : CES (no package IDs)
Top packages  : none
Champion      : —
Volume        : 53,245 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Internal pipeline ITC — not a customer-facing surface. "netgdpipeline" prefix indicates an automated data pipeline or order processing flow. Solely attributed to the Conversations product (GoDaddy AI assistant/Airo Conversations). Only 1 distinct PFID. Do not attempt offer resolution — no customer purchase journey exists here.

## [ITC] dlp_domain

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — Domain Registration
Page source   : not mapped
Products      : Domain Name Registration (86%), Aftermarket Non-Retail (2%), Domain Marketplace (1%), Domain Ownership Protection
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId, alt slug, disc000032); dbs → 0ce223ed (active Rev 1)
Volume        : 43,929 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain-focused landing page. Three NES packages: domain and domain-bundle resolve to the same underlying offerId (edf13c43) — domain-bundle is an alternate slug for the same offer. dbs = Domain Backorder Service curated offer (0ce223ed).

## [ITC] dpp_absol_reoffer5

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Re-offer Step 5 (Alternate Domain Suggestion)
Page source   : not mapped
Products      : Domain Name Registration (100%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 42,833 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Re-offer flow step 5 — shown when the originally searched domain is unavailable and the system is suggesting alternatives. Pure CES. "dpp_absol_reoffer" series likely has multiple steps (reoffer1 through reoffer5+). Only Domain Name Registration — no add-ons on this step.

## [ITC] cart_bottom_expresssearch

Prefix group  : CART
Human label   : Cart — Bottom Express Domain Search
Page source   : not mapped
Products      : Domain Name Registration (dominant)
NES/CES       : Mixed (NES domain package present alongside NULL rows)
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 39,472 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Search box at the bottom of the cart page allowing customers to add additional domains. Mix of NES (domain package) and CES (NULL) rows — NES where the domain offer resolved, CES where it didn't. Similar to cart_empty_search but fires when the cart already has items.

## [ITC] dpp_absol1.unavailable_organicspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Unavailable Domain Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (93%), Domain Marketplace, Domain Name Premium, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, redemption (ghost — skip), dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 34,007 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant for when the searched domain is unavailable — shows organic spin alternative suggestions. "organicspin" = organic spin experiment. Serves domain and domain backorder (dbs) offers. Part of the dpp_absol1.* experiment routing family.

## [ITC] dpp_absol1.primary_tldcard

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Primary TLD Card View
Page source   : not mapped
Products      : Domain Name Registration (97%), Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 31,197 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant using TLD card UI presentation — shows domain availability organized by TLD. "tldcard" = TLD (Top Level Domain) card layout. Part of the dpp_absol1.* experiment routing family.

## [ITC] upp_o365product_d2p_productivity_productivity_add_

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — M365 Product → D2P Productivity Add-on
Page source   : not mapped
Products      : MS Office 365 (89%), Value Adds (7%), Conversations (4%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 28,896 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Upsell path for M365 (Office 365) productivity add-ons, accessed via the domain-to-product (d2p) journey. "productivity_add_" = productivity add-on step. Pure CES M365 surface.

## [ITC] dpp_absol1.unavailable_alternate

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Unavailable Domain Alternate TLD Suggestion
Page source   : not mapped
Products      : Domain Name Registration (97%), Domain Ownership Protection
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 23,681 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant — shown when the searched domain is unavailable; presents alternate TLD suggestions. Distinct from unavailable_organicspin (organic spin) — this is the alternate TLD variant. Part of the dpp_absol1.* experiment routing family.

## [ITC] mya_dom_srch.primary_organicspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (96%), Domain Marketplace, Domain Name Premium, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 23,326 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch family variant — organic spin experiment routing from the My Account domain search. Sibling to mya_dom_srch.primary_exact. Serves domain and domain backorder (dbs) alongside the standard domain offer.

## [ITC] dpp_absol1.aftermarket_organicspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Aftermarket Domain Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (95%), Aftermarket Non-Retail, Domain Marketplace, Domain Name Premium
NES/CES       : NES
Top packages  : domain, dbs, redemption (ghost — skip)
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 22,896 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant for aftermarket/premium domain searches — domains that are already registered but available for purchase via the aftermarket. "aftermarket_organicspin" = organic spin variant for aftermarket results. dbs (Domain Backorder Service) present for domains not immediately available. Part of the dpp_absol1.* experiment routing family.

## [ITC] dpp_absol1.smartdefault_organicspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Smart Default Selection Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (91%), Aftermarket Non-Retail, Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain, dbs, redemption (ghost — skip)
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 22,219 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant — "smartdefault" indicates an AI/algorithmic smart default selection for the domain result. Organic spin experiment variant. Part of the dpp_absol1.* experiment routing family.

## [ITC] app_o365_upgrade_default

Prefix group  : other (app_ prefix — in-app surface)
Human label   : In-App M365 Upgrade — Default Path
Page source   : not mapped
Products      : MS Office 365 (98%), Value Adds (2%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 21,687 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-app (app_ prefix) upgrade path for M365, default routing. Very focused — nearly pure M365. CES surface. The app_ prefix denotes surfaces within a GoDaddy product application rather than the marketing site.

## [ITC] upp_wamproduct_f2p_dashboard_upgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — WAM Free-to-Paid Dashboard Upgrade
Page source   : not mapped
Products      : Websites and Marketing (82%), MS Office 365 (18%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 21,534 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Free-to-paid (f2p) upgrade path for Websites and Marketing (WAM) product accessed via the dashboard. M365 appears as a secondary upsell alongside WAM. Pure CES.

## [ITC] mya_dom_srch_vh

Prefix group  : mya — My Account
Human label   : My Account Domain Search — VH Variant
Page source   : not mapped
Products      : Domain Name Registration (86%), Aftermarket Non-Retail, Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId, alt slug); dbs → 0ce223ed (active Rev 1)
Volume        : 21,423 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch family variant — "vh" suffix likely indicates a variant/holdout experiment bucket. Same NES champion pattern as mya_dom_srch.primary_exact. domain-bundle is an alternate slug for the same offer as domain (both resolve to edf13c43).

## [ITC] slp_airo

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Airo AI Website Builder Sales Page
Page source   : not mapped
Products      : Domain Name Registration (86%), domain-bundle + domain + dbs packages, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 20,471 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : The Airo AI website builder sales landing page. Domain Name Registration is the dominant product (86%) — Airo bundles domain registration as part of the website builder onboarding. NES surface. The domain-bundle slug is an alternate for the same domain offer.

## [ITC] plp_domain_search

Prefix group  : other (plp_ prefix — Product Listing Page)
Human label   : Domain Search Product Listing Page
Page source   : not mapped
Products      : Domain Name Registration (87%), Aftermarket Non-Retail, Domain Marketplace, Domain Name Premium, Domain Name Transfer
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 20,008 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Product listing page for domain search results. "plp" = Product Listing Page. Serves the same NES domain offer family as dpp_* checkout surfaces. All domain-focused products.

## [ITC] upp_o365product_d2p_vnext-dashboard_venture_email_

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — M365 Product → VNext Dashboard Venture Email Add-on
Page source   : not mapped
Products      : MS Office 365 (91%), Conversations (6%), Value Adds (3%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 19,429 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Upsell path for M365 email via the VNext dashboard, venture tier. Sibling to upp_o365product_d2p_productivity_productivity_add_. Both are CES M365 upsell surfaces accessed via the d2p (domain-to-product) journey.

## [ITC] cart_empty_search

Prefix group  : other (cart_ prefix)
Human label   : Cart — Empty Cart Domain Search
Page source   : not mapped
Products      : Domain Name Registration (82%), domain + domain-bundle + dbs packages, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 19,183 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search shown when the cart is empty — the first prompt to add a product. NES surface serving the standard domain offer family. Sibling to cart_bottom_expresssearch (fires when cart already has items).

## [ITC] dna_wonmanagednonescrowauction

Prefix group  : other (dna_ prefix — Domain Name Aftermarket)
Human label   : Domain Aftermarket — Won Managed Non-Escrow Auction
Page source   : not mapped
Products      : Aftermarket Non-Retail (100%), 2 distinct PFIDs
NES/CES       : CES (no package IDs)
Top packages  : none (CES)
Champion      : —
Volume        : 18,413 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Triggered when a customer wins a managed domain auction without escrow. Not a customer-facing purchase surface — an internal event ITC for the domain aftermarket auction system. "dna" prefix = Domain Name Aftermarket (not DNA the product). Only 2 PFIDs.

## [ITC] mgr_shared_shopping_service

Prefix group  : other (mgr_ prefix — Manager/Reseller interface)
Human label   : Manager — Shared Shopping Service (Cross-Product)
Page source   : not mapped
Products      : MS Office 365 (51%), Websites and Marketing (23%), Open XChange (12%), SSL (9%), Professional Web Services (1%), Aftermarket (<1%), WordPress (<1%), Cashparking (<1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 17,960 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Broad multi-product CES surface accessed via the Manager/Reseller interface. "mgr_" prefix likely = GoDaddy Manager (reseller) portal. Sibling to shared_shopping_service (no mgr_ prefix). Very wide product mix — M365 and WAM dominant.

## [ITC] dpp_transfersbulk02

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Purchase Path — Bulk Domain Transfers Step 2
Page source   : not mapped
Products      : Domain Name Transfer (99%), Domain Name Registration (<1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 17,149 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Step 2 of the bulk domain transfer flow. Near-pure transfer surface. "02" = step number in a multi-step flow. CES.

## [ITC] dlp_cheapdomain_buy_domain

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap Domain Landing Page — Buy Domain
Page source   : not mapped
Products      : Domain Name Registration (87%), Domain Ownership Protection, Domain Marketplace, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 16,926 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Landing page for cheap/low-cost domain promotions. Standard NES domain offer family. "cheapdomain" in the slug signals this is a price-led entry point.

## [ITC] shared_shopping_service

Prefix group  : other (no prefix)
Human label   : Shared Shopping Service (Cross-Product Generic)
Page source   : not mapped
Products      : Domain Name Registration (30%), MS Office 365 (18%), CnP Hosting (15%), Website Protection (11%), WordPress Managed Plans (11%), SSL (9%), Paid Support (4%), cPanel Business Hosting (1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 16,914 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Base version of the shared shopping service (vs mgr_shared_shopping_service which adds the manager/reseller context). Widest product mix of any explored surface — 8 distinct product lines. Pure CES infrastructure ITC used across multiple purchase flows.

## [ITC] bulk_search

Prefix group  : other (no prefix)
Human label   : Bulk Domain Search
Page source   : not mapped
Products      : Domain Name Registration (98%), Domain Marketplace, Domain Ownership Protection, Domain Name Transfer, Domain Name Premium
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 16,113 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Bulk domain search tool — customers searching for multiple domains simultaneously. Near-pure Domain Name Registration. CES surface.

## [ITC] dpp_absol1.aftermarket_exact

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Aftermarket Domain Exact Match Variant
Page source   : not mapped
Products      : Domain Marketplace (47%), Domain Name Premium (22%), Domain Name Transfer (22%), Domain Marketplace NULL (8%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 15,649 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant for aftermarket exact-match domain searches. Distinctive product mix — Domain Marketplace and Domain Name Premium dominate (not Domain Name Registration), confirming this fires specifically for already-registered premium/aftermarket domains. Sibling to aftermarket_organicspin. Part of the dpp_absol1.* experiment routing family.

## [ITC] dlp_usoybo

Prefix group  : dlp — Domain Landing Page
Human label   : US Domain Landing Page — Office 365 by GoDaddy (OYBO) Bundle
Page source   : not mapped
Products      : Domain Name Registration + MS Office 365 (both ~46% via oybo-en-email bundle), Domain Ownership Protection (6%), Domain Name Registration via domain-bundle (4%)
NES/CES       : NES
Top packages  : oybo-en-email, domain-bundle
Champion      : oybo-en-email → e328092f (active Rev 1, plan=defaultEmailessentialsee, disc971321)
Volume        : 15,454 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Dedicated landing page for the "Office 365 by GoDaddy" (OYBO) domain+email bundle. The oybo-en-email package covers BOTH domain registration and M365 simultaneously — it is a domain+email bundle offer, not a standalone email offer. "us" = United States market. "oybo" = Office Yearly by Organization (GoDaddy's branded M365 bundle). Key insight: when this ITC appears in offer-pulse context, the champion is a bundle containing domain+email, not a standalone domain offer.

## [ITC] mya_vh_buildwebsite_domain

Prefix group  : mya — My Account
Human label   : My Account — Build Website Flow, Domain Acquisition Step
Page source   : not mapped
Products      : Domain Name Registration (82%), Domain Ownership Protection, Domain Marketplace, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 15,281 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain acquisition step within the "Build a Website" guided onboarding flow in My Account. "vh" suffix = variant/holdout experiment bucket. Standard NES domain offer family.

## [ITC] cart_xsell_single_card

Prefix group  : other (cart_ prefix)
Human label   : Cart Cross-sell — Single Card Layout
Page source   : not mapped
Products      : MS Office 365 (21%), Websites and Marketing (20%), Domain Name Registration (15%), Domain Ownership Protection (15%), Airo (12%), CnP Hosting (6%), SSL (4%), Website Protection (2%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 14,991 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Cart cross-sell presented in a single-card UI format. Very broad product mix including Airo (12%) — widest non-renewal cross-sell surface seen so far. Pure CES. Distinct from cart_xsells_inline (which is DOP/email focused) and cart_bottom_expresssearch (domain search).

## [ITC] dna_wonnonmanagedxfer

Prefix group  : other (dna_ prefix — Domain Name Aftermarket)
Human label   : Domain Aftermarket — Won Non-Managed Transfer
Page source   : not mapped
Products      : Domain Name Transfer (100%), 1 row
NES/CES       : CES (no package IDs)
Top packages  : none (CES)
Champion      : —
Volume        : 14,488 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Non-managed domain transfer for won aftermarket auctions. "nonmanaged" = seller handles transfer without GoDaddy escrow management. Sibling to dna_wonmanagednonescrowauction. Pure transfer, single product, CES.

## [ITC] cart_inline_single_stack

Prefix group  : other (cart_ prefix)
Human label   : Cart Inline Add-on — Single Stack Layout
Page source   : not mapped
Products      : Domain Name Registration (84%), Domain Ownership Protection (16%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 14,203 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Inline add-on in a single-stack (vertical) cart layout. Very focused — only Domain + DOP. Pure CES. Narrower product mix than cart_xsell_single_card.

## [ITC] dpp_absol1.unavailable_dbs

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Unavailable Domain Backorder Service
Page source   : not mapped
Products      : Aftermarket Non-Retail (99.7%), Domain Name Registration, Domain Marketplace, Domain Name Transfer, Domain Name Premium
NES/CES       : NES
Top packages  : dbs, domain (minimal)
Champion      : dbs → 0ce223ed (active Rev 1) — Domain Backorder Service
Volume        : 13,554 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant — fires specifically when a domain is unavailable and the system is offering Domain Backorder Service (dbs). Near-pure Aftermarket Non-Retail. The dbs curated offer is effectively the champion here. Part of the dpp_absol1.* experiment routing family.

## [ITC] dlp_domain?itc=dlp_domain

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page (MALFORMED — query parameter leak)
Page source   : not mapped
Products      : Domain Name Registration (86%), domain + domain-bundle + dbs packages, Aftermarket Non-Retail
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : same as dlp_domain — edf13c43 / 0ce223ed
Volume        : 12,557 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : DATA QUALITY ISSUE — this ITC has a URL query parameter embedded in the string (?itc=dlp_domain). This happens when an ITC is passed as a query parameter and the downstream tracking system captures the full URL fragment. Functionally identical to dlp_domain — same products, same NES packages. Should be deduplicated with dlp_domain in any surface-level analysis. Flag if encountered in offer-pulse billing queries.

## [ITC] slp_hosting_category

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Hosting Category Sales Page (VPS / Server Hosting)
Page source   : not mapped
Products      : WordPress Managed Plans (20% CES), MS Office 365 (13% CES), CnP Hosting (12% CES), SSL via vps4-* NES packages, Vendor Email (5% CES)
NES/CES       : Mixed — VPS4/SSL products are NES; WordPress/M365/cPanel are CES
Top packages  : vps4-self-managed-lin-tier1, vps4-self-managed-lin-tier2, vps4-self-managed-lin-tier4, vps4-self-managed-win-tier2, vps4-self-managed-win-tier4, vps4-self-managed-high-mem-lin-tier4, vps4-self-managed-high-mem-win-tier4, websecuritysuite-tier0
Champion      : vps4-self-managed-lin-tier1 → a405a47c (active Rev 1, offersGrouping geometry — GAP-024); websecuritysuite-tier0 → 5bad7c62 (active Rev 1)
Volume        : 12,461 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Hosting category page serving VPS4 self-managed server tiers (Linux + Windows, standard + high-mem) and Website Security Suite. All VPS4 packages are NES curated offers using offersGrouping parent/child geometry WITHOUT prePurchaseKeyMap — this is the GAP-024 misclassification scenario. Offer-pulse will classify these as Standalone when they are actually Offer Collections. The vps4-* SSL rows appear because SSL certificates are bundled into the VPS4 package. Non-VPS products (WordPress, M365, cPanel) are CES.

## [ITC] account_myrenewals_bulk

Prefix group  : other (account_ prefix)
Human label   : My Renewals — Bulk Renewal
Page source   : not mapped
Products      : Domain Name Registration (38%), MS Office 365 (28%), CnP Hosting (6%), Open XChange (6%), Domain Ownership Protection (6%), Value Adds (4%), Virtual Hosting (3%), Websites and Marketing (3%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 12,283 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Bulk renewal of multiple products simultaneously. Part of the account_myrenewals_* family alongside account_myrenewals_jtbd and account_myrenewals_single. Pure CES. Very broad product mix.

## [ITC] upp_wamproduct_p2p_start_start_upp_start

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — WAM Paid-to-Paid Starter Tier Upgrade
Page source   : not mapped
Products      : Websites and Marketing (83%), MS Office 365 (17%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 12,193 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Paid-to-paid (p2p) WAM upgrade path targeting the Starter tier. "start_start_upp_start" = starting from the Start plan, upgrading within Start tier. Sibling to upp_wamproduct_f2p_dashboard_upgrade (which is free-to-paid). Pure CES.

## [ITC] dpp_absol1.smartdefault_exact

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Smart Default Exact Match Variant
Page source   : not mapped
Products      : Domain Name Registration (97%), Domain Ownership Protection, Domain Marketplace
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 12,176 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family variant — smart default selection with exact match routing. Sibling to smartdefault_organicspin. Part of the dpp_absol1.* experiment routing family.

## [ITC] app_o365_adduser_buymoreaccounts

Prefix group  : other (app_ prefix — in-app surface)
Human label   : In-App M365 — Add User / Buy More Accounts
Page source   : not mapped
Products      : MS Office 365 (78%), Value Adds (22%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 11,282 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-app surface for purchasing additional M365 user seats. "adduser" = add user workflow, "buymoreaccounts" = additional account purchase. Sibling to app_o365_upgrade_default. Both are CES app_ surfaces for M365 management.

## [ITC] mya_dom_srch.primary_tldcard

Prefix group  : mya — My Account
Human label   : My Account Domain Search — TLD Card View
Page source   : not mapped
Products      : Domain Name Registration (97%), Domain Ownership Protection, Domain Marketplace, Domain Name Premium
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 10,912 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch family variant with TLD card UI presentation. Sibling to mya_dom_srch.primary_exact and mya_dom_srch.primary_organicspin. Part of the mya_dom_srch.* experiment routing family.


---


## [ITC] dpp_absol1.primary_paidspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Primary Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (97.5%), Domain Ownership Protection (0.9%), Domain Name Registration uncategorised (1.6%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 10,604 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family member. "paidspin" = paid traffic (SEM/ads) routing bucket, sibling to primary_organicspin (organic) and primary_exact (type-in). Virtually identical product mix to other primary variants. Part of the dpp_absol1.* experiment routing family.

## [ITC] ios_studio_app_your_domains_domain_search

Prefix group  : other (ios_ prefix — iOS app surface)
Human label   : iOS GoDaddy Studio App — Your Domains Domain Search
Page source   : not mapped
Products      : Domain Name Registration (73.1% domain, 14.2% domain-bundle, 11.9% unpackaged), Domain Ownership Protection (0.7%), Aftermarket dbs (< 0.1%)
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 10,538 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search from the "Your Domains" screen inside the iOS GoDaddy Studio mobile app. High NES attachment (~87% of orders have a package_id). Standard domain family. Sibling to android_studio_app_your_domains_domain_search (in bulk table).

## [ITC] mya_dom_srch.unavailable_organicspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Unavailable Result, Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (91.2% domain, 6.4% unpackaged), Domain Ownership Protection (1.6%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 10,419 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch family member. "unavailable" = the searched domain was taken; system offers alternatives. "organicspin" = organic traffic experiment bucket. Despite the domain being unavailable, purchases resolve to standard domain registration (alternative TLDs or suggestions). DBS is handled by dedicated mya_dom_srch.unavailable_dbs ITC. Part of the mya_dom_srch.* experiment routing family.

## [ITC] dpp_transfers01

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Transfer Flow — Step 1
Page source   : not mapped
Products      : Domain Name Transfer (81.9%), Domain Ownership Protection (18.0%), Domain Name Registration (< 0.1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 9,606 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Step 1 of the domain transfer initiation flow. "01" = step number (sibling to dpp_transfersbulk02 which is bulk transfers step 2). Heavily DOP-upsell — 18% of orders are DOP add-ons offered during the transfer. Pure CES.

## [ITC] slp_365_category_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Microsoft 365 Category Sales Page — Seat Configuration
Page source   : not mapped
Products      : MS Office 365 (92.8%), Strategic Partnerships AC / Titan-adjacent (5.4%), Value Adds (1.8%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 9,249 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : M365 category sales page where customers configure seat count before purchasing. "config" = configuration step (seat selector UI). Sibling to slp_365_category (same products, different UI step). Strategic Partnerships AC rows likely reflect Titan Email co-sell. CES.

## [ITC] mya_dom_srch.smartdefault_organicspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Smart Default Selection, Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (90.8% domain, 5.1% unpackaged), Aftermarket dbs (2.1%), Domain Ownership Protection (1.4%), Domain Marketplace (0.4%), Domain Name Transfer (0.1%), Domain Name Premium (< 0.1%)
NES/CES       : NES
Top packages  : domain, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 9,100 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch family member. "smartdefault" = system picks the best available TLD/option automatically. "organicspin" = organic traffic experiment bucket. Includes 2.1% DBS — the smart default algorithm occasionally selects backorder when that's the best option for the searched name. Part of the mya_dom_srch.* experiment routing family.

## [ITC] dcc_portfolio_domain_search_box

Prefix group  : dcc — Domain Control Center
Human label   : DCC Portfolio — Domain Search Box
Page source   : not mapped
Products      : Domain Name Registration (80.5% domain, 8.9% domain-bundle, 5.8% unpackaged), Aftermarket dbs (2.4%), Domain Ownership Protection (1.5%), Domain Marketplace (0.4%), Domain Name Premium (0.3%), Domain Name Transfer (0.1%)
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 9,082 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Domain search box embedded in the DCC portfolio view. Customers managing their domains can search for additional registrations without leaving DCC. Standard NES domain family. Includes dbs (2.4%) for searches that return unavailable domains. Sibling to dcc_portfolio_empty_search_recommendations (which is CES — fires before a search is entered).

## [ITC] dpp_absol1.primary_alternate

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Primary Alternate Variant
Page source   : not mapped
Products      : Domain Name Registration (95.9% domain, 3.0% unpackaged), Domain Ownership Protection (1.1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 8,951 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : dpp_absol1 family member. "alternate" = alternate TLD suggestion routing (customer searched for .com but is shown .net/.io/etc.). Minimal product mix — near-pure domain registration. Part of the dpp_absol1.* experiment routing family alongside primary_exact, primary_organicspin, primary_tldcard, primary_paidspin.

## [ITC] mya_dom_srch.aftermarket_organicspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Aftermarket Query, Organic Spin Variant
Page source   : not mapped
Products      : Domain Name Registration (92.7% domain, 5.4% unpackaged), Domain Ownership Protection (1.3%), Domain Marketplace (0.3%), Domain Name Premium (0.2%), Domain Name Transfer (0.1%), Aftermarket dbs (< 0.1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 8,754 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch family member. "aftermarket" = search returned an aftermarket (already-registered) domain. "organicspin" = organic traffic bucket. Despite the aftermarket label, 92.7% of purchases are standard Domain Name Registration — suggesting most customers buy an alternative TLD rather than the aftermarket domain itself. Minimal dbs (< 0.1%). Part of the mya_dom_srch.* experiment routing family.

## [ITC] dcc_portfolio_empty_search_recommendations

Prefix group  : dcc — Domain Control Center
Human label   : DCC Portfolio — Empty Search State, Recommendations
Page source   : not mapped
Products      : Domain Name Registration (99.8%), Domain Marketplace (< 0.1%), Domain Name Transfer (< 0.1%), Domain Name Premium (< 0.1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 8,311 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DCC portfolio domain search box — fires before the customer types anything (empty state). Displays recommended domain suggestions. All CES (no package IDs). Contrast with dcc_portfolio_domain_search_box (which fires after a search is entered and is NES). Near-pure Domain Registration.

## [ITC] slp_365_category

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Email / M365 Category Sales Page
Page source   : not mapped
Products      : Vendor Email / Titan (70.7%), MS Office 365 (29.3%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 8,271 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Email category landing page presenting both Titan Email (Vendor Email, 70.7%) and Microsoft 365 (29.3%). Sibling to slp_365_category_config (which is the M365 seat-configuration step, M365-dominant). This page is Titan-dominant — most customers land here for basic email, not full M365. CES.

## [ITC] slp_ssl

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SSL Certificate Sales Page
Page source   : not mapped
Products      : SSL (100% — all variants)
NES/CES       : NES
Top packages  : ssl-001sites-tier1 (69.5%), ssl-wildcard-tier1 (12.3%), ssl-001sites-managed-tier1 (12.0%), ssl-005sites-tier1 (4.5%)
Champion      : ssl-001sites-tier1 → 28e5b730 (active Rev 1, plan=standard); ssl-wildcard-tier1 → 28e5b730 (plan=standard_wildcard); ssl-001sites-managed-tier1 → 28e5b730 (plan=managed); ssl-005sites-tier1 → 28e5b730 (plan=standard_ucc_5); ssl-001sites-tier3 → bb0afea9 (active Rev 1, offersGrouping geometry)
Volume        : 7,967 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Pure SSL certificate sales page. Near-100% SSL. Majority of packages (ssl-001sites-tier1/tier2/managed/wildcard/5sites) all resolve to offerId 28e5b730 — same underlying SSL offer, different plans for tier/type. ssl-001sites-tier3 resolves to a separate offerId (bb0afea9) with offersGrouping geometry (GAP-024 misclassification risk). Minor volume tail packages (norton-1-year-free-trial, multi-unit-ssl-setup-service, dlxssl-001domain-tier1dv) not catalog-resolved.

## [ITC] mya_dom_srch.unavailable_alternate

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Unavailable Result, Alternate TLD Variant
Page source   : not mapped
Products      : Domain Name Registration (94.9% domain, 3.8% unpackaged), Domain Ownership Protection (1.3%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 7,866 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch family member. "unavailable" = searched domain was taken; "alternate" = system shows alternate TLD suggestions (e.g. .net when .com is taken). Near-pure domain registration. Part of the mya_dom_srch.* experiment routing family.

## [ITC] upp_wamproduct_f2p_websites_upgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — WAM Free-to-Paid Websites Upgrade
Page source   : not mapped
Products      : Websites and Marketing (73.2%), MS Office 365 (26.8%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 7,861 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Free-to-paid (f2p) upgrade path for WAM, Websites tier. "f2p" distinguishes it from p2p (paid-to-paid). M365 at 26.8% — likely offered as an add-on during the upgrade flow. Sibling to upp_wamproduct_p2p_start_start_upp_start (paid-to-paid) and upp_wamproduct_f2p_dashboard_upgrade (already profiled). CES.

## [ITC] app_o365_archiving_addon

Prefix group  : other (app_ prefix — in-app surface)
Human label   : In-App M365 — Email Archiving Add-On
Page source   : not mapped
Products      : Value Adds (99.97%), MS Office 365 (< 0.1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 7,379 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : In-app purchase surface for M365 Email Archiving (a compliance/retention add-on). "Value Adds" product line confirms this is an add-on, not a base subscription. Sibling to app_o365_encryption_addon and app_o365_backupselectusers_backup (in bulk table). Pure CES.

## [ITC] parkedpage_landers

Prefix group  : other (no prefix — parked page surface)
Human label   : Parked Page Domain Lander
Page source   : not mapped
Products      : Domain Name Registration (60.8% domain, 9.2% domain-bundle, 1.9% unpackaged), Aftermarket dbs (24.0%), Domain Ownership Protection (1.7%), Domain Marketplace (1.2%), Domain Name Premium (0.6%), Domain Name Transfer (0.5%)
NES/CES       : NES
Top packages  : domain, dbs, domain-bundle
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1); domain-bundle → edf13c43 (same offerId)
Volume        : 7,201 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Parked domain landing pages — the "for sale" lander shown when visiting a parked/expired domain. High dbs volume (24%) reflects that many parked domains are already registered, so Domain Backorder Service is the relevant offer. Standard NES domain family for new registrations. One of the few non-standard-prefix ITCs that is NES.

## [ITC] upp_o365product_d2p_dashboard_unknown-entry-point

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — M365 Product Upgrade from Dashboard (Unknown Entry Point)
Page source   : not mapped
Products      : MS Office 365 (85.7%), GoDaddy Conversations (12.3%), Value Adds (2.0%), WAM (< 0.1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 7,200 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : M365 product upgrade triggered from the dashboard when the referring entry point cannot be determined. "unknown-entry-point" is a fallback bucket. Significant GoDaddy Conversations volume (12.3%) — this is GoDaddy's SMS/live chat product, commonly bundled with M365 in upgrade flows. Sibling to upp_o365product_d2p_productivity_productivity_add_ (already profiled). CES.

## [ITC] mya_dom_srch.aftermarket_exact

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Aftermarket Exact Match
Page source   : not mapped
Products      : Domain Marketplace (48.7% domain, 5.7% unpackaged), Domain Name Premium (23.9%), Domain Name Transfer (21.5%), Domain Name Registration (< 0.1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 7,102 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch family member. "aftermarket_exact" = customer searched for a specific domain that is already registered and available through aftermarket channels. Distinctive product mix: Domain Marketplace (48.7%) + Domain Name Premium (23.9%) + Domain Transfer (21.5%) — very different from other mya_dom_srch.* variants which are domain-registration-dominated. The "exact" suffix means the customer's specific searched name matched an aftermarket listing. Part of the mya_dom_srch.* experiment routing family.

## [ITC] dna_dmndtl_closeouts_bin

Prefix group  : other (dna_ prefix — Domain Name Aftermarket)
Human label   : Domain Aftermarket — Closeouts Buy-It-Now
Page source   : not mapped
Products      : Aftermarket Non-Retail (100%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 6,749 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Domain aftermarket closeouts at fixed (buy-it-now) prices. "dmndtl" = domain detail page; "closeouts" = expiring/expired domains available at reduced prices; "bin" = Buy It Now (fixed price, no auction). Pure Aftermarket Non-Retail. CES. Sibling to dna_wonmanagednonescrowauction and dna_wonnonmanagedxfer (both already profiled).

## [ITC] slp_website_security_suites

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : Website Security Suites Sales Page
Page source   : not mapped
Products      : Website Protection (47.4% total incl. ghost rows), Strategic Partnerships AC / Norton free trial (44.9% ghost packages)
NES/CES       : Mixed — websecuritysuite-tier0/1/2 are real NES; nes-wss-nortonsmb-* are ghost packages; bare Website Protection is CES
Top packages  : websecuritysuite-tier0, websecuritysuite-tier1, websecuritysuite-tier2 (real NES); ghost: nes-wss-tier0/1/2-nortonsmb-standardfreetrial (skip)
Champion      : websecuritysuite-tier0/1/2 → 5bad7c62 (active Rev 1, tier1 plan=advanced_1, tier2 plan=premium_1); all three tiers share same offerId
Volume        : 6,622 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Website security suites page (Deluxe/Advanced/Premium tiers). Ghost package dominance: ~59% of rows have nes-wss-*-nortonsmb-standardfreetrial ghost packages — these appear in billing but resolve to nothing in catalog (skip in offer-pulse). Real NES packages are websecuritysuite-tier0/1/2, all sharing offerId 5bad7c62 with plan-level differentiation. CES rows (Website Protection NULL, 32.2%) are legacy orders without NES migration. Offer-pulse must strip ghosts before classifying.

## [ITC] mya_dom_srch.unavailable_dbs

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Unavailable, Domain Backorder Service
Page source   : not mapped
Products      : Aftermarket Non-Retail / dbs (99.8%), Domain Name Registration (< 0.1%), Domain Marketplace (< 0.1%), Domain Name Transfer (< 0.1%)
NES/CES       : NES
Top packages  : dbs
Champion      : dbs → 0ce223ed (active Rev 1)
Volume        : 6,456 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch family member dedicated to the Domain Backorder Service path. Fires when a My Account domain search returns an unavailable domain AND the system routes specifically to DBS (vs alternate TLD suggestions). Near-pure DBS (99.8%). Contrast with mya_dom_srch.unavailable_organicspin and mya_dom_srch.unavailable_alternate which show regular domain registration alternatives. Part of the mya_dom_srch.* experiment routing family.

## [ITC] upp_titanproduct_d2p_productivity_productivity_add

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — Titan Email Product Upgrade, Productivity Add-On
Page source   : not mapped
Products      : Vendor Email / Titan (100%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 6,451 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Titan Email product upgrade path for adding productivity features. "d2p" = direct-to-paid. "productivity_productivity_add" = upgrading to or adding Titan Productivity tier. Pure Vendor Email (Titan). CES. Sibling to app_o365_archiving_addon but for Titan rather than M365.

## [ITC] dcc_domsettings_xgrade_portfolio_bulk_action_bar

Prefix group  : dcc — Domain Control Center
Human label   : DCC Domain Settings — Cross-Grade via Portfolio Bulk Action Bar
Page source   : not mapped
Products      : Domain Ownership Protection (100%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 6,351 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DCC domain settings cross-grade triggered from the portfolio bulk action bar. "xgrade" = cross-grade (changing product tier). "bulk_action_bar" = multi-domain selection bar. Pure Domain Ownership Protection — this surface is exclusively used to add/upgrade DOP on existing domains in bulk. CES.

## [ITC] mgr_slp_365_category_config

Prefix group  : other (mgr_ prefix — Manager/Reseller interface)
Human label   : Manager Portal — M365 Category Sales Page, Seat Configuration
Page source   : not mapped
Products      : MS Office 365 (90.8%), Value Adds (6.9%), Strategic Partnerships AC (2.3%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 6,096 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Manager/reseller portal variant of slp_365_category_config. Resellers purchasing M365 on behalf of customers. Near-identical product mix to slp_365_category_config (M365-dominant) but accessed through the mgr_ reseller interface. CES.

## [ITC] dpp_absol1.ai_search

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — AI-Powered Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (97.5% domain, 0.6% unpackaged), Domain Ownership Protection (1.8%), Domain Marketplace (< 0.1%), Domain Name Premium (< 0.1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 5,576 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : dpp_absol1 family member for AI-powered domain search routing. "ai_search" = customer used GoDaddy's AI domain suggestion/search feature. NES, standard domain champion. Newer addition to the dpp_absol1.* experiment routing family — reflects AI search product expansion.

## [ITC] app_ox_adduser_buymoreaccounts

Prefix group  : other (app_ prefix — in-app surface)
Human label   : In-App Open XChange — Add User / Buy More Accounts
Page source   : not mapped
Products      : Open XChange (100%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 5,527 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : In-app surface for purchasing additional Open XChange (legacy email) user seats. Direct equivalent of app_o365_adduser_buymoreaccounts but for the older OX email platform instead of M365. Pure Open XChange. CES. OX is the legacy email product being migrated to M365/Titan.

## [ITC] dlp_domain_whois

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — WHOIS Lookup Entry
Page source   : not mapped
Products      : Domain Name Registration (89.2% domain, 4.7% domain-bundle, 3.0% unpackaged), Domain Ownership Protection (1.9%), Aftermarket dbs (0.6%), Domain Marketplace (0.3%), Domain Name Premium (0.2%), Domain Name Transfer (0.1%)
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); domain-bundle → edf13c43 (same offerId); dbs → 0ce223ed (active Rev 1)
Volume        : 5,417 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Domain landing page reached from a WHOIS lookup. Customer looked up domain ownership info and is now offered the domain for purchase (if available) or alternatives. Standard NES domain family. Small dbs component (0.6%) for unavailable domains. "whois" entry point is mid-funnel — more research-oriented customer.

## [ITC] mgr_misc-purchase

Prefix group  : other (mgr_ prefix — Manager/Reseller interface)
Human label   : Manager Portal — Miscellaneous Purchase
Page source   : not mapped
Products      : Miscellaneous Fees (85.8%), Professional Web Services (7.2%), MS Office 365 (3.1%), WAM (1.9%), Dedicated Hosting (1.1%), Shared Hosting (0.3%), ISC (0.3%), Website Builder (0.1%), Paid Support (< 0.1%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 5,285 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Manager/reseller portal variant of misc-purchase (already profiled). Miscellaneous Fees dominates (85.8%) — likely professional services, setup fees, and one-time charges billed through the reseller channel. Broader product tail than the non-manager equivalent. CES.

## [ITC] dpp_absol1.smartdefault_paidspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Smart Default, Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (95.7% domain, 2.8% unpackaged), Domain Ownership Protection (1.3%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 4,985 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : dpp_absol1 family member. "smartdefault" = system auto-selects best TLD; "paidspin" = paid search traffic bucket. Sibling to smartdefault_organicspin and smartdefault_exact. Near-pure domain registration. Part of the dpp_absol1.* experiment routing family.

## [ITC] upp_d2p_add-user

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Upsell — Direct-to-Paid Add User (Email / M365)
Page source   : not mapped
Products      : MS Office 365 (71.6%), Vendor Email / Titan (20.0%), Value Adds (6.0%), GoDaddy Conversations (2.4%)
NES/CES       : CES (all package IDs null)
Top packages  : none (CES)
Champion      : —
Volume        : 4,926 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Add-user upsell shown during the direct-to-paid (d2p) onboarding path. Mix of M365 (71.6%) and Titan Email (20%) — the user is adding email seats, not upgrading tiers. GoDaddy Conversations (2.4%) is a cross-sell for the SMS/chat product. CES. Broader email product coverage than app_o365_adduser_buymoreaccounts (M365-only).


## [ITC] dna_wonmanagednonescrowauctionrenewal

Prefix group  : other — Domain Name Auction
Human label   : Domain Name Auction Managed Non-NES Escrow Renewal
Page source   : not mapped
Products      : Domain Name Auction (90.7%), Domain Name Registration (9.3%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4,904 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dna_ prefix = Domain Name Auction. Managed renewal path for escrow-settled auction domains outside the NES system. Distinct from standard domain renewal flows.

## [ITC] dpp_absol1.unavailable_paidspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Unavailable TLD, Paid Search Routing Variant (A/B)
Page source   : not mapped
Products      : Domain Name Registration (93% packaged, 5.5% unpackaged), Domain Ownership Protection (1.5%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 4,729 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "unavailable" = searched TLD is taken; "paidspin" = paid search traffic bucket. Near-pure domain registration. Part of the dpp_absol1.* experiment routing family alongside unavailable_tldcard, aftermarket_paidspin, smartdefault_paidspin, etc.

## [ITC] upp_o365product_p2p_account_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Microsoft 365 Product Upgrade / Downgrade (Account-Level, P2P)
Page source   : not mapped
Products      : MS Office 365 (92.2%), Open XChange (4.8%), Vendor Email (3%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4,594 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Account-level upgrade or downgrade path for M365 (peer-to-peer plan change). Includes small Open XChange (4.8%) and legacy Vendor Email/Titan (3%) — users changing email tiers. All CES; no package IDs observed.

## [ITC] mya_dom_srch.smartdefault_exact

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Smart Default, Exact Match Variant
Page source   : not mapped
Products      : Domain Name Registration (91.9% packaged, 6.4% unpackaged), Domain Ownership Protection (1.4%), Domain Marketplace/Premium/Transfer (<0.3%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 4,593 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "smartdefault" = system auto-selects recommended TLD; "exact" = user searched for exact domain that is available. Sibling of primary_paidspin, primary_alternate. Near-pure domain registration. Part of the NES domain champion family (edf13c43).

## [ITC] app_o365_encryption_addon

Prefix group  : other — App / In-Product
Human label   : Microsoft 365 Email Encryption Add-on (In-App Purchase)
Page source   : not mapped
Products      : Value Adds (99.9%), MS Office 365 (<0.1%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4,580 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-app add-on purchase surface for M365 email encryption. Overwhelmingly Value Adds product line (encryption is a value add to the base M365 seat). 99.9% CES.

## [ITC] slp_email_encryption

Prefix group  : slp — Front of Site (Sales Landing Page)
Human label   : Email Encryption Sales Landing Page (M365 Security Bundle)
Page source   : not mapped
Products      : MS Office 365 (99.5%), Value Adds (0.5%)
NES/CES       : Mixed (0.8% NES attachment — effectively CES-dominant)
Top packages  : office365-securitybundle-tier3, office365-tier3, office365-tier0
Champion      : — (not resolved; NES attachment <1%, too low to prioritize)
Volume        : 4,459 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Sales landing page for M365 email encryption / security bundle. 99.2% of orders have null package_id (CES). A small tail (37 orders, 0.8%) has NES package IDs (office365-securitybundle-tier3, office365-tier3, office365-tier0) — low enough to classify as CES-dominant in practice. Value Adds (0.5%) includes email security feature add-ons.

## [ITC] site_search_dpp

Prefix group  : other — Site-Wide Search
Human label   : Site-Wide Domain Search Results → Domain Purchase Path
Page source   : not mapped
Products      : Domain Name Registration (84.7% domain pkg, 5.9% domain-bundle, 4% unpackaged), Domain Ownership Protection (1.5%), Domain Marketplace (1.4%), Domain by Proxy / DBS (1.1%), Domain Premium (0.8%), Domain Transfer (0.6%)
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 4,306 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : ITC for orders originating from the site-wide search bar landing on the domain purchase path. Broadest domain product mix of all profiled surfaces — includes marketplace, premium, and transfer in addition to standard registration. Multi-product mix reflects that search results surface available AND aftermarket domains simultaneously.

## [ITC] upp_titanproduct_d2p_panel-lite_unknown-entry-poin

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Titan Email Product Upgrade — Panel Lite, Unknown Entry Point (D2P)
Page source   : not mapped
Products      : Vendor Email (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4,198 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Direct-to-paid (d2p) upgrade path for Titan Email (Vendor Email product line) via the Panel Lite interface. Entry point not tracked ("unknown-entry-poin" = truncated ITC name). 100% Vendor Email / Titan, CES.

## [ITC] app_o365_backupselectusers_backup

Prefix group  : other — App / In-Product
Human label   : Microsoft 365 Backup — Select Users (In-App Backup Purchase)
Page source   : not mapped
Products      : Value Adds (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4,120 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-app surface for purchasing M365 email backup for specific users. Entirely Value Adds product line (backup is a value add to the base M365 subscription). 100% CES.

## [ITC] dcc_portfolio_stack_bundle

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center — Portfolio Stack Bundle
Page source   : not mapped
Products      : Domain Name Registration (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,912 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : DCC surface for purchasing domain bundles as a "portfolio stack." 100% Domain Name Registration, CES. Stack bundles are a domain quantity promotion path (buy multiple domains at once). No NES package IDs observed.

## [ITC] mya_dom_srch.primary_paidspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Primary, Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (94.4% packaged, 4.5% unpackaged), Domain Ownership Protection (1.2%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 3,912 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "primary" = primary/default path; "paidspin" = paid search traffic bucket routing variant. Near-pure domain registration. Sibling of smartdefault_exact and primary_alternate. All share the domain NES champion (edf13c43).

## [ITC] slp_365_email_config

Prefix group  : slp — Front of Site (Sales Landing Page)
Human label   : Microsoft 365 Email Configuration Sales Landing Page
Page source   : not mapped
Products      : MS Office 365 (~92%), Strategic Partnerships (~6%), other (<2%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,723 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Sales landing page for M365 email configuration. Strategic Partnerships (~6%) is likely bundled/white-label or partner-channel M365 sales. All CES. Note: product % shares are approximate — query reached LIMIT with ~77 orders in remaining tail products.

## [ITC] mgr_slp_sapi_config

Prefix group  : other — Manager / Reseller Portal
Human label   : Manager Portal — SAPI Configuration Sales Landing Page (Multi-Product Reseller)
Page source   : not mapped
Products      : Pro Web Services (53.6%), Managed WordPress (19.1%), Websites & Marketing (13.3%), MS Office 365 (5.7%), DIFY Social (3.7%), SEV (3.6%), VPS (0.7%), SSL (0.2%), Titan Email (<0.1%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,736 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mgr_ = Manager/reseller portal. SAPI = Service Account/Partner Integration. Extremely broad product mix across 9 product lines — catch-all reseller configuration surface used by partner/agency accounts. Pro Web Services (53.6%) is the dominant product. 100% CES.

## [ITC] mgr_slp_wsb_ft_nocc_config

Prefix group  : other — Manager / Reseller Portal
Human label   : Manager Portal — Website Builder Free Trial, No Credit Card Configuration
Page source   : not mapped
Products      : Websites & Marketing (67.7%), MS Office 365 (31.5%), Titan Email (0.8%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,545 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mgr_ = Manager/reseller portal. Website Builder (WSB) Free Trial (ft) without credit card (nocc) — reseller onboarding surface for Website Builder free trials. WAM (67.7%) + M365 (31.5%) is the classic website + email bundle pattern. CES.

## [ITC] dpp_absol1.aftermarket_paidspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Aftermarket Domain, Paid Search Routing Variant (A/B)
Page source   : not mapped
Products      : Domain Name Registration (94.4% packaged, 4.6% unpackaged), Domain Ownership Protection (1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 3,152 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "aftermarket" = domain being purchased is an expired/aftermarket domain; "paidspin" = paid search traffic bucket. Aftermarket domains still flow through the same domain NES champion. Part of the dpp_absol1.* experiment routing family.

## [ITC] upp_o365product_d2p_productivity_add-user

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Microsoft 365 Productivity Add-User Upgrade (D2P)
Page source   : not mapped
Products      : MS Office 365 (88.9%), Value Adds (7.1%), GoDaddy Conversations (4%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,673 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Direct-to-paid (d2p) upgrade for adding M365 users under the "productivity" product line. Conversations (4%) is a cross-sell for the SMS/chat product. All CES; no package IDs observed.

## [ITC] upp_f2p_upgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Websites & Marketing Free-to-Paid Upgrade Path
Page source   : not mapped
Products      : Websites & Marketing (79.6%), MS Office 365 (20.3%), Airo (<0.1%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,309 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Free-to-paid (f2p) upgrade path converting free website builder trial to paid. WAM (79.6%) is primary; M365 (20.3%) is the email add-on frequently bundled with WAM upgrades. The f2p upgrade path is fully CES across all product lines.

## [ITC] app_o365_downgrade_mailbox

Prefix group  : other — App / In-Product
Human label   : Microsoft 365 Mailbox Downgrade (In-App)
Page source   : not mapped
Products      : MS Office 365 (68.8%), Value Adds (31.2%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,142 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : In-app surface for M365 mailbox tier downgrade. Value Adds (31.2%) likely captures email security/backup features that persist through the downgrade. CES; no package IDs.

## [ITC] am_gdcart_agentassisted_cart_link

Prefix group  : other — Aftermarket / Agent-Assisted
Human label   : Agent-Assisted Cart Link — Aftermarket / Premium Domain Purchase (GoDaddy Cart)
Page source   : not mapped
Products      : Domain Marketplace (51.9%), Domain Name Registration Premium (24%), Domain Name Transfer (23.9%), Domain Name Registration (<0.1%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3,045 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : am_ = Aftermarket. Cart links generated by GoDaddy agents to assist customers purchasing marketplace/premium domains. Predominantly Domain Marketplace (51.9%) + Premium registrations (24%) + Transfers (23.9%). 100% CES — aftermarket transactions do not flow through NES.

## [ITC] android_studio_app_your_domains_domain_search

Prefix group  : other — Mobile App (Android Studio)
Human label   : Android Studio App — Your Domains, Domain Search
Page source   : not mapped
Products      : Domain Name Registration (74.3% unpackaged, 15.5% domain pkg, 9.6% domain-bundle pkg), Domain Ownership Protection (0.6%)
NES/CES       : NES (low attachment — ~25.1% of orders have package_id)
Top packages  : domain, domain-bundle
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 3,013 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Android GoDaddy Studio app, domain search from the "Your Domains" section. Technically NES (package IDs present on ~25% of orders) but significantly lower than the iOS equivalent (ios_studio_* has ~87% NES attachment). Android app likely has incomplete NES billing instrumentation. Domain name registration only.

## [ITC] dpp_absol1.unavailable_tldcard

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Unavailable TLD, TLD Card UI Variant (A/B)
Page source   : not mapped
Products      : Domain Name Registration (87.8% packaged, 5.8% unpackaged), Domain Marketplace (2.3%), Domain Ownership Protection (2.1%), Domain Premium (1.3%), Domain Transfer (0.8%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,976 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "unavailable" = searched TLD is taken; "tldcard" = UI variant showing TLD option cards (vs. paidspin layout). Sibling to unavailable_paidspin. More diverse product mix (marketplace, premium, transfer) than paidspin — TLD card UI surfaces alternative domain options more prominently.

## [ITC] mgr_slp_365_config

Prefix group  : other — Manager / Reseller Portal
Human label   : Manager Portal — Microsoft 365 Configuration Sales Landing Page
Page source   : not mapped
Products      : MS Office 365 (63.9%), Value Adds (34.5%), Strategic Partnerships (1.7%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,889 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mgr_ = Manager/reseller portal. M365 configuration SLP for resellers. Value Adds (34.5%) is unusually high — likely email security/backup add-ons bundled with M365 in the reseller channel. Strategic Partnerships (1.7%) = white-label/partner-branded M365. CES.

## [ITC] mgr_slp_wsb_ft_getstarted_plans_nocc_config

Prefix group  : other — Manager / Reseller Portal
Human label   : Manager Portal — Website Builder Free Trial Get-Started Plans, No Credit Card Configuration
Page source   : not mapped
Products      : Websites & Marketing (67.6%), MS Office 365 (28%), Titan Email (4.4%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,817 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mgr_ = Manager/reseller portal. Extended variant of mgr_slp_wsb_ft_nocc_config (Website Builder Free Trial), specifically the "get started plans" step in the onboarding flow. Near-identical product mix: WAM (67.6%) + M365 (28%) + Titan (4.4%). CES.

## [ITC] upp_airobuilderproduct_p2p_airo-builder_app-builde

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Airo Builder Product — P2P App Builder Upgrade
Page source   : not mapped
Products      : Airo (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,840 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Peer-to-peer (p2p) upgrade path for the Airo AI website builder. 100% Airo product line. ITC name is truncated ("app-builde"). CES; no package IDs.

## [ITC] dlp_hosting

Prefix group  : dlp — Domain Landing Page
Human label   : cPanel Hosting Domain Landing Page
Page source   : not mapped
Products      : CnP Hosting (cPanel), SSL, MS Office 365, Website Protection (all NES-packaged, breakdown by bundle)
NES/CES       : NES (packages partially resolved — see Notes)
Top packages  : nes-cpanel-set-1-economy-ssl-ox, nes-cpanel-set-1-economy-ssl-365-xtra, nes-cpanel-set-2-deluxe-365-xtra
Champion      : cpanel-set-1-economy-ssl-365-xtra → d9918695 (offersGrouping + prePurchaseKeyMap, NES Bundle geometry)
Volume        : 2,783 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dlp_ surface for cPanel-based shared hosting. All orders have NES package IDs (nes-cpanel-set-*). Catalog resolution: nes-cpanel-set-1-economy-ssl-ox → NOT FOUND; nes-cpanel-set-1-economy-ssl-365-xtra → NOT FOUND; nes-cpanel-set-2-deluxe-365-xtra → NOT FOUND. The non-nes-prefixed variant cpanel-set-1-economy-ssl-365-xtra DOES resolve → d9918695. nes-cpanel-set-1-economy-ssl-365-wss-xtra is a ghost package (skip). Volume count reflects product-level aggregation (CnP+SSL+M365+WebProtect in each bundle = 4× counting per order).

## [ITC] mya_dom_srch.primary_alternate

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Primary, Alternate Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (89.7% packaged, 9% unpackaged), Domain Ownership Protection (1.3%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,777 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "primary" = primary search flow; "alternate" = A/B routing variant. Sibling of primary_paidspin and smartdefault_exact. Near-pure domain registration. All share the domain NES champion (edf13c43).

## [ITC] dlp_dpp_dbs

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — Domain + Domain by Proxy + Bulk Domain Services Bundle
Page source   : not mapped
Products      : Domain Name Registration (59% domain, 7.3% domain-bundle, 4.9% unpackaged), Domain by Proxy / DBS (25.6% dbs, 1.7% domain-bundle DOP), Domain Marketplace (0.8%), Domain Premium (0.5%), Domain Transfer (0.3%)
NES/CES       : NES
Top packages  : domain, dbs, domain-bundle
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 2,650 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dlp_ surface targeting domain landing page for Domain by Proxy / Bulk Domain Services bundles. DBS (25.6%) is much higher than most domain surfaces — page is specifically designed for customers seeking privacy protection bundles. Two confirmed NES champions: domain (edf13c43) and dbs (0ce223ed).

## [ITC] upp_airobuildercreditsproduct_p2p_airo-builder_bud

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Airo Builder Credits Product — P2P Budget Upgrade
Page source   : not mapped
Products      : Airo (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,769 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Peer-to-peer (p2p) upgrade path for Airo builder credits — "budget" tier of the Airo credit system. ITC name is truncated ("airo-builder_bud"). Sibling of upp_airobuilderproduct_p2p_airo-builder_app-builde. 100% Airo, CES.

## [ITC] upp_wamproduct_f2p_sites_upgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Websites & Marketing Product — Free-to-Paid Sites Upgrade
Page source   : not mapped
Products      : Websites & Marketing (69.4%), MS Office 365 (30.6%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,695 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Free-to-paid (f2p) upgrade for the Websites & Marketing "sites" component. WAM (69.4%) + M365 (30.6%) is the website + email bundle pattern. Sibling of upp_f2p_upgrade (broader WAM/M365) and other WAM upgrade paths. CES.

## [ITC] studio_ios_domain_renewal

Prefix group  : other — Mobile App (iOS Studio)
Human label   : iOS GoDaddy Studio App — Domain Renewal
Page source   : not mapped
Products      : Domain Name Registration (79.8%), Domain Ownership Protection (19.6%), Website Protection (0.7%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,649 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : iOS GoDaddy Studio app domain renewal surface. All null package IDs — CES. Contrast with android_studio_app_your_domains_domain_search (~25% NES attachment) — iOS renewal path has zero NES instrumentation. Domain Ownership Protection (19.6%) purchased alongside renewal.


## [ITC] slp_365_email

Prefix group  : slp — Front of Site (Sales Landing Page)
Human label   : Microsoft 365 & Email Sales Landing Page (Multi-Product Email)
Page source   : not mapped
Products      : Vendor Email / Titan (64.2%), MS Office 365 (28.7%), Open XChange (7.1%)
NES/CES       : Mixed (27.6% NES — office365-tier0, workspace-openexchange-tier1/tier2, office365-emailplus-tier1)
Top packages  : office365-tier0, workspace-openexchange-tier1, office365-emailplus-tier1
Champion      : office365-tier0 → 575a7d2a (Email Essentials, active Rev 4); workspace-openexchange-tier1 → 2468b30f (OX Startup, active Rev 1)
Volume        : 2,632 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Sells across three email product lines simultaneously: Titan/Vendor Email (64.2% CES), M365 (office365-tier0 NES 21.7% + CES 6.2%), and OX (workspace-openexchange-tier1/2 NES 4.2%+0.8%, CES 2.1%). Distinct from slp_365_email_config which is a configuration SLP. NES champions: 575a7d2a serves both office365-tier0 and office365-emailplus-tier1 (different plans, same offerId).

## [ITC] cart_xsell_carousel_confirmation

Prefix group  : other — Cart
Human label   : Cart Confirmation Page — Cross-sell Carousel
Page source   : not mapped
Products      : MS Office 365 (49.9%), Domain Ownership Protection (32%), Vendor Email / Titan (10.3%), CnP Hosting (1.6%), Domain Name Registration (2%), WordPress Managed Plans (1.2%), SSL (1.1%), Website Protection (0.8%), other (<1.5%)
NES/CES       : Mixed (1.8% NES from domain registration orders — CES-dominant in practice)
Top packages  : domain (negligible NES)
Champion      : domain → edf13c43 (active Rev 3) — negligible volume
Volume        : 2,481 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Cross-sell carousel shown on the cart confirmation/thank-you page after checkout. Extremely broad product mix — this is the catch-all post-purchase upsell surface. M365 (49.9%) + DOP (32%) are the two dominant cross-sells. 98.2% of orders are CES (null package_ids). The 1.8% NES attach comes from a small number of domain registration upsells.

## [ITC] cart_confirmation_search

Prefix group  : other — Cart
Human label   : Cart Confirmation Page — Domain Search Cross-sell
Page source   : not mapped
Products      : Domain Name Registration (70.3% domain, 9.4% domain-bundle, 7.3% unpackaged), Aftermarket Non-Retail / DBS (6%), Domain Marketplace (3.6%), Domain Ownership Protection (1.3%), Domain Premium (1.3%), Domain Transfer (0.9%)
NES/CES       : NES (91% NES attachment)
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 2,434 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search box shown on the cart confirmation page. Broad domain product mix including marketplace, premium, and transfer — customers searching for domains post-purchase often look at all options. High NES attachment (91%) reflecting that confirmed purchasers convert to packaged domain products. Sibling surface to cart_xsell_carousel_confirmation.

## [ITC] pro_hub_dom_srch

Prefix group  : other — Pro Hub
Human label   : Pro Hub — Domain Search
Page source   : not mapped
Products      : Domain Name Registration (87.6% domain, 5.7% domain-bundle, 2.5% unpackaged), Aftermarket Non-Retail / DBS (1.6%), Domain Ownership Protection (1%), Domain Marketplace (1%), Domain Transfer (0.4%), Domain Premium (0.2%)
NES/CES       : NES (96.1% NES attachment)
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 2,406 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search surface within the Pro Hub (GoDaddy's professional/agency dashboard). Near-pure domain registration with high NES attachment (96.1%). Pro users purchasing domains via the hub are nearly all going through NES packaged offers. DBS (1.6%) reflects privacy-oriented pro users.

## [ITC] crm_paidit

Prefix group  : other — CRM
Human label   : CRM — "PaidIt" Conversion Flow (IT Products)
Page source   : not mapped
Products      : Paid IT (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2,387 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : CRM system conversion flow — "PaidIt" event triggered when a customer completes a Paid IT (GoDaddy IT support) purchase. 100% Paid IT product line. CES. The crm_ prefix likely indicates a CRM-triggered purchase flow rather than a web surface.

## [ITC] slp_vps4_linux

Prefix group  : slp — Front of Site (Sales Landing Page)
Human label   : Linux VPS4 Sales Landing Page
Page source   : not mapped
Products      : Virtual Hosting / VPS (~50%), SSL (~50%) — all NES-packaged as VPS+SSL bundles
NES/CES       : NES (offersGrouping geometry — each plan is a VPS+SSL bundle)
Top packages  : vps4-self-managed-lin-tier1/2/4/6/8, vps4-self-managed-win-tier2/4/6, vps4-self-managed-high-mem-*, websecuritysuite-tier0
Champion      : vps4-self-managed-*-tier{N} → a405a47c (offersGrouping geometry, active); websecuritysuite-tier0 → 5bad7c62
Volume        : 2,321 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : VPS4 Linux sales landing page. All orders have NES package IDs from two package families: (1) vps4-self-managed-lin/win/high-mem variants → all resolve to offerId a405a47c (offersGrouping geometry, different plan per tier); (2) websecuritysuite-tier0 → 5bad7c62. Product split is ~50/50 VPS and SSL because each VPS bundle includes a bundled SSL certificate (two product_pnl_line_name rows per order). GAP-024 applies: offersGrouping without prePurchaseKeyMap — offer-pulse may misclassify as Standalone.

## [ITC] whois_serp_search

Prefix group  : other — WHOIS / Search
Human label   : WHOIS Search Engine Results Page — Domain Search
Page source   : not mapped
Products      : Domain Name Registration (89.5% domain, 4.8% unpackaged, 3.7% domain-bundle), Domain Ownership Protection (1.2% domain-bundle), Aftermarket Non-Retail / DBS (0.3%), Domain Marketplace (0.3%), Domain Transfer (0.2%)
NES/CES       : NES (94.9% NES attachment)
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 2,319 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search from the WHOIS search engine results page (SERP). High NES attachment (94.9%) — customers searching WHOIS for domain availability convert to NES packaged domain offers. Nearly pure domain registration. DBS inclusion is small (0.3%) but present — privacy-conscious WHOIS users.

## [ITC] dpp_absol1.aftermarket_tldcard

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Aftermarket, TLD Card UI Variant (A/B)
Page source   : not mapped
Products      : Domain Name Registration (72.2% packaged), Domain Marketplace (12.8%), Domain Premium (7.3%), Domain Transfer (5.2%), Domain Ownership Protection (1.3%), Domain Name Registration unpackaged (1.2%)
NES/CES       : NES (97.6% NES attachment)
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,306 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "aftermarket" = expired/auction domain; "tldcard" = TLD option card UI. This aftermarket variant has notably higher Marketplace (12.8%) and Premium (7.3%) share than the standard primary_tldcard — reflecting that aftermarket searches surface more premium/marketplace alternative domains. Near-peer to aftermarket_paidspin. All domain NES champion.

## [ITC] mya_dom_srch.unavailable_paidspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Unavailable TLD, Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (90% packaged, 7.9% unpackaged), Domain Ownership Protection (2.1%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,291 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "unavailable" = searched domain is taken; "paidspin" = paid search routing bucket. Customer is in My Account and searched for a domain that is unavailable — shown alternatives. Sibling to unavailable_tldcard and unavailable_organicspin.

## [ITC] gocentral_domain_search_from_domain_settings

Prefix group  : other — GoCentral / Website Builder
Human label   : GoCentral Website Builder — Domain Search from Domain Settings
Page source   : not mapped
Products      : Domain Name Registration (99.9%), Domain Marketplace (<0.1%), Domain Premium (<0.1%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 2,236 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Domain search triggered from the domain settings panel within GoCentral (legacy website builder). 99.9% Domain Name Registration, 100% CES. GoCentral domain management flows predate NES instrumentation. Essentially a single-product CES surface.

## [ITC] dpp_absol1.favorites

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Saved Favorites List View
Page source   : not mapped
Products      : Domain Name Registration (83.3% packaged, 10.8% unpackaged), Domain Ownership Protection (2.1%), Aftermarket Non-Retail / DBS (1.8%), Domain Marketplace (1.1%), Domain Premium (0.6%), Domain Transfer (0.5%)
NES/CES       : NES (87.1% NES attachment)
Top packages  : domain, dbs
Champion      : domain → edf13c43 (active Rev 3); dbs → 0ce223ed (active Rev 1)
Volume        : 2,168 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "favorites" = customer is purchasing from their saved/favorited domains list. Moderate NES attachment (87.1%). DBS (1.8%) reflects that favorites shoppers are comparison shoppers who value privacy protection. Broader product mix suggests favorites shoppers explore more options.

## [ITC] mya_acctsettings_billing_privacy

Prefix group  : mya — My Account
Human label   : My Account Billing Settings — Domain Privacy (DOP) Add-on
Page source   : not mapped
Products      : Domain Ownership Protection (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 2,166 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : My Account billing/settings area where customers can add Domain Ownership Protection to existing domains. 100% DOP, 100% CES. Single-product surface — customers are explicitly purchasing privacy protection add-ons for already-registered domains.

## [ITC] dpp_absol1.smartdefault_tldcard

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Checkout — Smart Default, TLD Card UI Variant (A/B)
Page source   : not mapped
Products      : Domain Name Registration (93.2% packaged, 3.4% unpackaged), Domain Marketplace (1%), Domain Ownership Protection (1.5%), Domain Transfer (0.6%), Domain Premium (0.3%)
NES/CES       : NES (95.1% NES attachment)
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,159 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : dpp_absol1 family. "smartdefault" = system auto-selects recommended TLD; "tldcard" = TLD card UI variant. Sibling to smartdefault_paidspin and smartdefault_organicspin and smartdefault_exact. Near-pure domain registration NES.

## [ITC] mya_dom_srch.smartdefault_paidspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Smart Default, Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (93.3% packaged, 5.5% unpackaged), Domain Ownership Protection (1.2%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 2,137 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "smartdefault" = system-recommended TLD; "paidspin" = paid search routing bucket. Sibling to smartdefault_exact and smartdefault_organicspin. Near-pure domain registration, high NES attachment.

## [ITC] upp_d2p_venture_email_buy_more

Prefix group  : upp — Upsell / Upgrade Path
Human label   : M365 Venture Email — Buy More Mailboxes (D2P)
Page source   : not mapped
Products      : MS Office 365 (~90%), GoDaddy Conversations (~5.5%), Value Adds (~3.6%), other (<1%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 2,064 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : Direct-to-paid (d2p) upgrade path for buying additional M365 mailboxes via the "Venture" email journey. Conversations (5.5%) is the SMS/chat cross-sell; Value Adds (3.6%) likely includes email security. All CES; no package IDs. Distinct from upp_d2p_add-user (which covers both M365 and Titan).

## [ITC] slp_vps4_linux_config

Prefix group  : slp — Front of Site (Sales Landing Page)
Human label   : Linux VPS4 Configuration Sales Landing Page
Page source   : not mapped
Products      : Virtual Hosting / VPS (76.1%), SSL (18.1%), Website Protection (5.7%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 2,045 orders as of 2026-05-15 — High
Explored      : 2026-05-15
Notes         : VPS4 Linux configuration SLP — a post-selection configuration page. All CES (null package_ids), unlike slp_vps4_linux which is NES. The config step in the VPS purchase flow loses NES instrumentation. Products: VPS (76.1%), SSL (18.1%), Website Protection (5.7%).

## [ITC] dcc_portfolio_table_inline_alt_tld

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center Portfolio Table — Inline Alternate TLD Suggestions
Page source   : not mapped
Products      : Domain Name Registration (94.9%), Domain Ownership Protection (5.1%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,970 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DCC portfolio domain table surface showing inline alternate TLD suggestions alongside existing domains. 94.9% Domain Name Registration, 5.1% DOP. 100% CES — DCC domain purchase flows do not carry NES package IDs.

## [ITC] upp_default_p2p_account_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Default Hosting Account Upgrade / Downgrade (P2P)
Page source   : not mapped
Products      : CnP Hosting (47%), cPanel Business Hosting (19.7%), Website Protection (13.9%), Virtual Hosting / VPS (9.9%), WordPress Managed Plans (4.7%), Domain Buyers Club (3.1%), Paid Support (0.7%), Express Email Marketing (0.5%), other (<0.5%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,875 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Default peer-to-peer (p2p) upgrade/downgrade path for hosting accounts. Broad mix across cPanel hosting tiers (CnP + cPanel Business = 66.7%), Website Protection (13.9%), and VPS (9.9%). Domain Buyers Club (3.1%) is a domain discount subscription. All CES. "Default" suggests this is a fallback catch-all upgrade path rather than product-specific.

## [ITC] mya_dom_srch.unavailable_tldcard

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Unavailable TLD, TLD Card UI Variant
Page source   : not mapped
Products      : Domain Name Registration (91% packaged, 6.6% unpackaged), Domain Ownership Protection (1.3%), Domain Marketplace (0.8%), Domain Transfer (0.2%), Domain Premium (0.1%)
NES/CES       : NES (92% NES attachment)
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 1,834 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "unavailable" = searched domain is taken; "tldcard" = TLD card UI. Sibling to unavailable_paidspin. Shows TLD alternative cards when the desired domain is unavailable in My Account search. High NES attachment.

## [ITC] ios_studio_app_quick_action_domain_search

Prefix group  : other — Mobile App (iOS Studio)
Human label   : iOS GoDaddy Studio App — Quick Action Domain Search
Page source   : not mapped
Products      : Domain Name Registration (77.6% unpackaged, 11% domain-bundle, 10.3% domain pkg), Domain Ownership Protection (1% domain-bundle)
NES/CES       : NES (low attachment — 22.4% of orders have package_id)
Top packages  : domain-bundle, domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 1,735 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : iOS Studio app — domain search triggered via the quick action shortcut (vs. the "Your Domains" section search at ios_studio_app_your_domains_domain_search which has ~87% NES). This quick action path has markedly lower NES attachment (22.4%) — likely a different code path with incomplete NES billing instrumentation. domain-bundle (11%) edges out plain domain (10.3%) as the top NES package, suggesting bundle promotions are shown in quick action results.

## [ITC] cart_hosting_freesearch

Prefix group  : other — Cart
Human label   : Cart Hosting Page — Free Domain Search
Page source   : not mapped
Products      : Domain Name Registration (85.6%), Domain Ownership Protection (14.4%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,696 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Free domain search shown on the cart hosting page (customers purchasing hosting and searching for a free domain to include). 85.6% Domain Reg + 14.4% DOP. All CES — domain included-with-hosting flows do not carry NES package IDs.

## [ITC] upp_o365product_d2p_dashboard_m365wamspuredirect

Prefix group  : upp — Upsell / Upgrade Path
Human label   : M365 Dashboard Direct-to-Paid Upgrade (WAM/M365 Pure Direct)
Page source   : not mapped
Products      : MS Office 365 (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,695 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : M365 direct-to-paid (d2p) upgrade via the dashboard — "m365wamspuredirect" suggests a pure direct conversion (no intermediate steps) for the M365/WAM product pairing. 100% M365, CES.

## [ITC] cart_xsell_carousel_domain_search

Prefix group  : other — Cart
Human label   : Cart Cross-sell Carousel — Domain Search Add-on (DOP)
Page source   : not mapped
Products      : Domain Ownership Protection (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,689 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Cart carousel cross-sell for domain search — 100% Domain Ownership Protection (privacy add-on). Customers adding DOP to a domain search result from the cart cross-sell carousel. All CES. Single-product surface.

## [ITC] dcc_dop_full_to_ultimate_upgrade

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center — Domain Privacy Full to Ultimate Upgrade
Page source   : not mapped
Products      : Domain Ownership Protection (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,688 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DCC upgrade path for Domain Ownership Protection, specifically upgrading from the "Full" tier to the "Ultimate" tier. 100% DOP, CES. Single-product upgrade surface within the domain settings area.

## [ITC] mya_dom_srch.ai_search

Prefix group  : mya — My Account
Human label   : My Account Domain Search — AI-Powered Search Variant
Page source   : not mapped
Products      : Domain Name Registration (94.3% packaged, 2.4% unpackaged), Domain Ownership Protection (2.9%), Domain Premium (0.2%), Domain Marketplace (0.2%)
NES/CES       : NES (94.7% NES attachment)
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 1,646 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "ai_search" = AI-powered domain name suggestion/search variant. Near-pure domain registration with very high NES attachment (94.7%). The AI search variant converts at high NES rates — customers using the AI-assisted search are buying packaged NES domain offers.

## [ITC] mgrzed0ov

Prefix group  : other — Manager / Reseller Portal
Human label   : Manager Portal — ZED/OV Configuration (Unknown Identifier, Multi-Product)
Page source   : not mapped
Products      : Website Builder (19.3%), Domain Name Registration (17.3%), WordPress Managed Plans (13.3%), Paid Support (9.8%), Pro Web Services (7.2%), MS Office 365 (6.4%), Websites & Marketing (5.3%), Grid Hosting (5%), CnP Hosting (3.9%), DIFY Social (3.8%), Domain Ownership Protection (3.7%), Website Protection (1%), VPS/SSL/cPanel/other (<4%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,559 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mgr_ = Manager/reseller portal. "zed0ov" is an opaque alphanumeric identifier — possibly an internal test endpoint, a specific reseller-channel configuration, or an obscured route name. One of the most product-diverse ITCs profiled (19+ product lines across Website Builder, Domain, MWP, Paid Support, Pro Web Services, M365, WAM, Grid, CnP, DIFY, DOP, etc.). 100% CES.

## [ITC] mya_dom_srch.aftermarket_paidspin

Prefix group  : mya — My Account
Human label   : My Account Domain Search — Aftermarket, Paid Search Routing Variant
Page source   : not mapped
Products      : Domain Name Registration (92% packaged, 6.5% unpackaged), Domain Ownership Protection (1.5%)
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (active Rev 3)
Volume        : 1,466 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mya_dom_srch.* family. "aftermarket" = searched domain is an expired/aftermarket domain; "paidspin" = paid search routing bucket. Near-pure domain registration, high NES attachment. Sibling to aftermarket_exact and aftermarket_organicspin.

## [ITC] app_o365_m365_addons

Prefix group  : other — App / In-Product
Human label   : Microsoft 365 Add-ons (In-App Purchases)
Page source   : not mapped
Products      : Value Adds (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,453 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : In-app surface for purchasing M365 add-on features. 100% Value Adds product line. CES. Similar to app_o365_encryption_addon and app_o365_backupselectusers_backup but for general M365 add-ons.

## [ITC] upp_o365product_p2p_productivity_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path
Human label   : M365 Productivity Product Upgrade / Downgrade (P2P) — Titan Email
Page source   : not mapped
Products      : Vendor Email (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,431 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Peer-to-peer (p2p) upgrade/downgrade for the "productivity" product group. Despite "o365product" in the ITC name, 100% Vendor Email / Titan — this is the Titan email tier change path, not M365. Likely a legacy routing where the Titan product was grouped under the M365/o365 product category. CES.

## [ITC] upp_dopproduct_combo_p2p_account_upgrade_upp_doppr

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Domain Ownership Protection — Combo P2P Account Upgrade (Truncated ITC)
Page source   : not mapped
Products      : Domain Ownership Protection (100%)
NES/CES       : CES (all null package_ids)
Top packages  : none (CES)
Champion      : —
Volume        : 1,413 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : P2P (peer-to-peer) account upgrade for Domain Ownership Protection — a "combo" upgrade path. ITC name is truncated ("upp_doppr" at the end). 100% DOP, CES. Single-product upgrade surface.


## [ITC] tdfs_gdcustom

Prefix group  : other (tdfs_)
Human label   : Third-Party Domain Fulfillment — Aftermarket Custom Surface
Page source   : not mapped
Products      : Domain Marketplace 65.0%, Domain Transfer 18.5%, Domain Premium 16.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,402 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : tdfs_ prefix = third-party domain fulfillment service; 100% aftermarket paths (marketplace, transfer, premium). No NES packages.

## [ITC] mgr_slp_365_email_config

Prefix group  : other (mgr_)
Human label   : M365 Email Configuration / Post-Purchase Setup Surface
Page source   : not mapped
Products      : M365 85.4%, Value Adds 11.5%, Strategic Partnerships 2.9%, OX 0.2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,368 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : mgr_ prefix = manager/configuration surface. Likely a post-purchase flow guiding M365 email setup. No packages — all CES.

## [ITC] slp_vps4_fully

Prefix group  : slp
Human label   : VPS4 Fully Managed Hosting Sales Page (cPanel/Plesk)
Page source   : not mapped
Products      : VH/VPS (SSL-bundled fully managed tiers — cpanel, plesk variants)
NES/CES       : NES
Top packages  : vps4-managed-lin-cpanel-tier1, vps4-managed-lin-plesk-tier1, vps4-managed-lin-cpanel-tier2
Champion      : vps4-managed-lin-cpanel-tier1 → a3e21e25 (offersGrouping geometry, Rev confirmed)
Volume        : 1,366 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DISTINCT from slp_vps4_linux (self-managed, a405a47c). This page = fully managed VPS with server admin included. Both use offersGrouping geometry.

## [ITC] dpp_absol1.regpremium_exact

Prefix group  : dpp
Human label   : Domain Purchase Path — Absolute Domain 1 — Premium Exact-Match Registration
Page source   : not mapped
Products      : Domain Reg 97.6% (packaged ~81%, unpackaged ~16.6%), DOP 2.4%
NES/CES       : NES
Top packages  : domain (packaged reg), unpackaged domain reg
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1,366 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Premium exact-match registration subpath. High NES attachment on packaged domain registrations.

## [ITC] upp_logoimageproduct_d2p_brandbook_gai.vh.dashboar

Prefix group  : upp
Human label   : Upsell — AI Logo/Brand Book — Dashboard to VH Surface
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,350 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : AI brand asset upsell (logo, brand book) originating from dashboard or VH flow. ITC truncated at 50 chars. 100% Airo, CES-only.

## [ITC] upp_airobuildercreditsproduct_p2p_airo-builder_man

Prefix group  : upp
Human label   : Upsell — Airo Builder Credits — P2P (Panel to Panel) Managed Flow
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,331 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : P2P upsell for Airo builder credits, 100% CES. ITC likely truncated. "man" suffix may indicate managed flow variant.

## [ITC] slp_365_config

Prefix group  : slp
Human label   : M365 Configuration / Email Setup Sales Landing Page
Page source   : not mapped
Products      : M365 91.6%, Value Adds 4.7%, Strategic Partnerships 3.6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,294 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : M365-focused landing page or config surface. High M365 concentration with small Value Adds / Strategic Partnerships tail. All CES.

## [ITC] dpp_modsearch_inoybo

Prefix group  : dpp
Human label   : Domain Purchase Path — Modified Search — In-OYBO (Own Your Brand Online) Bundle
Page source   : not mapped
Products      : Domain Reg 46.4%, Vendor Email (Titan) 25.3%, OX 21.8%, DOP 2.6%, domain-bundle 3.9% — all covered by single bundle package oybo-ox-email
NES/CES       : NES
Top packages  : oybo-ox-email
Champion      : oybo-ox-email → c377d7de (bundled domain+email offer — covers all 4 products in one package)
Volume        : 1,290 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : OYBO = "Own Your Brand Online" entry point. The oybo-ox-email package is a true multi-product bundle: Domain Reg + Vendor Email + OX + DOP share a single package_id. c377d7de is the curated offer for this bundle.

## [ITC] dify_attach

Prefix group  : other (dify_)
Human label   : DIFY (Digital Marketing / Social) — Attach / Upsell Surface
Page source   : not mapped
Products      : Pro Web Services 88.7%, DIFY Social 11.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,255 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : dify_ prefix = Digital + DIY or "Do It For You" social product surface. Attach pattern (upsell at attachment point). 100% CES.

## [ITC] dpp_absol1

Prefix group  : dpp
Human label   : Domain Purchase Path — Absolute Domain 1 (Base Path, Mixed Aftermarket)
Page source   : not mapped
Products      : Domain Reg NULL 53.5%, Aftermarket Non-Retail NULL 35.8%, DOP domain-bundle 10.4% (minor NES)
NES/CES       : Mixed (CES-dominant)
Top packages  : domain-bundle (minor NES component only)
Champion      : domain-bundle → edf13c43 (minor, <11% of volume)
Volume        : 1,239 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Base variant (no subpath). Aftermarket Non-Retail at 35.8% with null packages is notable — likely auction/backorder domain purchases. CES-dominant in practice; NES only via small DOP domain-bundle component.

## [ITC] mya_dom_srch.smartdefault_tldcard

Prefix group  : mya
Human label   : My Account — Domain Search Smart Default — TLD Card
Page source   : not mapped
Products      : Domain Reg 98.1% (packaged 93.9%, unpackaged 4.2%), DOP 1.3%, Marketplace 0.3%
NES/CES       : NES
Top packages  : domain (packaged reg)
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1,224 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : My Account domain search with TLD card UI. Very high NES attachment. Smart default + TLD card = specific search UI variant.

## [ITC] upp_dopproduct_ultimate_p2p_account_upgrade_upp_do

Prefix group  : upp
Human label   : Upsell — DOP Ultimate — P2P Account Upgrade
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,210 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Domain Ownership Protection (Ultimate tier) account-to-account upgrade path. ITC likely truncated. 100% CES.

## [ITC] app_o365_adduser_domain

Prefix group  : other (app_)
Human label   : M365 App — Add User — Domain-Context Surface
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,208 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : app_ prefix = in-app surface (post-purchase). M365 "add user" flow that triggers a domain purchase (likely to complete M365 email setup). 100% Domain Reg, all CES.

## [ITC] dlp_email_professional

Prefix group  : dlp
Human label   : Email Professional Domain Landing Page (M365)
Page source   : not mapped
Products      : M365 91.7% (office365-tier0 75.2%, tier1 7.2%, m365-officebusinessep1-aes 4.0%, m365-officebusinessp1-aes 2.7%, emailplus-tier1 2.5%), NULL 8.3%
NES/CES       : NES
Top packages  : office365-tier0, office365-tier1, m365-officebusinessep1-aes
Champion      : office365-tier0 → 575a7d2a (all 5 M365 package IDs resolve to same offerId 575a7d2a)
Volume        : 1,201 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Domain-specific landing page for Professional Email (M365 branding). All five distinct M365 package IDs share the same curated offerId (575a7d2a) — plan-level differentiation within one offer.

## [ITC] upp_wamproduct_f2p_account_upgrade

Prefix group  : upp
Human label   : Upsell — Websites and Marketing — F2P (Free to Paid) Account Upgrade
Page source   : not mapped
Products      : WAM 72.6%, M365 27.3%, OX <0.1%, Airo <0.1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,199 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Free-to-paid upgrade surface for WAM. M365 tail (27.3%) suggests cross-sell opportunity. All CES.

## [ITC] empty_cart_xsell_carousel

Prefix group  : other (empty_cart_)
Human label   : Empty Cart Cross-Sell Carousel
Page source   : not mapped
Products      : M365 44.6%, Vendor Email 14.6%, SSL 12.0%, MWP 11.7%, CnP Hosting 9.2%, WAM 5.4%, Website Protection 2.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,175 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Shown when cart is empty; displays cross-sell product carousel. Broad multi-product distribution reflects the catch-all nature of this surface. All CES.

## [ITC] mgr_slp_vps4_linux_config

Prefix group  : other (mgr_)
Human label   : VPS4 Linux Configuration / Post-Purchase Setup Surface
Page source   : not mapped
Products      : VH/VPS 72.4%, SSL 25.2%, Website Protection 2.4%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,172 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Post-purchase VPS4 Linux configuration flow. SSL is a common add-on at this step (25.2%). All CES — note the parallel SLP (slp_vps4_linux) is CES while the fully managed variant (slp_vps4_fully) is NES.

## [ITC] dcc_portfolio_dopsa_add_cart

Prefix group  : dcc
Human label   : Domain Control Center — Portfolio — DOP Standalone Add to Cart
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,172 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DCC portfolio view where customer adds DOP (Domain Ownership Protection) standalone to cart. dopsa = DOP Standalone. 100% CES.

## [ITC] slp_wsb_ft_nocc

Prefix group  : slp
Human label   : Website Builder Free Trial — No Credit Card — Sales Landing Page
Page source   : not mapped
Products      : M365 76.0%, WAM 23.5%, Vendor Email 0.5%
NES/CES       : NES
Top packages  : vnext-i18no365-tier1, wsb-vnext-tier1, vnext-i18no365-tier0
Champion      : vnext-i18no365-tier1 → 2a999a09 (offersGrouping + prePurchaseKeyMap → inner M365 offer 575a7d2a); wsb-vnext-tier1 → ea9e918c (same architecture)
Volume        : 1,156 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Free trial no-credit-card landing page for Website Builder. NES via offersGrouping+prePurchaseKeyMap layered architecture — outer offer (2a999a09 / ea9e918c) wraps inner M365 offer (575a7d2a). nocc = no credit card.

## [ITC] slp_wordpress_support

Prefix group  : slp
Human label   : WordPress Managed Hosting — Paid Support Upsell Landing Page
Page source   : not mapped
Products      : Paid Support: tier2 30.0%, tier1 26.3%, tier3 22.6%, unpackaged 21.1%
NES/CES       : NES
Top packages  : wordpress-premiumsupport-tier1, wordpress-premiumsupport-tier2, wordpress-premiumsupport-tier3
Champion      : wordpress-premiumsupport-tier1 → 52603ec4 (basic plan, Rev 1); tier2/tier3 likely same offerId
Volume        : 1,153 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Dedicated landing page for WordPress premium/paid support upgrades. Three tiers (1/2/3) with 21% unpackaged (CES) tail. NES dominant.

## [ITC] upp_o365product_d2p_panel-lite_unknown-entry-point

Prefix group  : upp
Human label   : Upsell — M365 — D2P Panel Lite — Unknown Entry Point
Page source   : not mapped
Products      : M365 96.9%, Value Adds 2.8%, Conversations 0.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,110 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : D2P = dashboard-to-panel upsell for M365; "panel-lite" variant with unknown entry point. Unknown-entry-point suffix indicates untracked or direct navigation origin. All CES.

## [ITC] upp_o365product_p2p_account_renewals

Prefix group  : upp
Human label   : Upsell — M365 — P2P (Panel to Panel) Account Renewals Surface
Page source   : not mapped
Products      : M365 71.5%, Value Adds 12.4%, OX 12.0%, Vendor Email 4.2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,107 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Account renewals surface for M365, P2P navigation. OX (12%) and Vendor Email (4.2%) suggest cross-product renewals co-located here. All CES.

## [ITC] app_ox_adduser_buymoreaccounts_vnext-dashboard

Prefix group  : other (app_)
Human label   : Open XChange App — Add User / Buy More Accounts — vNext Dashboard
Page source   : not mapped
Products      : Open XChange 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,098 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : In-app OX surface for adding users or buying additional mailbox accounts. vnext-dashboard = new dashboard UI. 100% CES.

## [ITC] slp_rstore

Prefix group  : slp
Human label   : Reseller Store / Standard Store Sales Landing Page (Domain-Dominant)
Page source   : not mapped
Products      : Domain Reg NULL 93.7%, domain 2.0%, CnP Hosting 1.1%, MWP 1.0%, M365/VPS/other <2%
NES/CES       : Mixed (CES-dominant)
Top packages  : domain (minor NES)
Champion      : domain → edf13c43 (Rev 3, minor 2.3% NES component only)
Volume        : 1,094 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : Likely "reseller store" or legacy "standard store" landing page. 93.7% domain reg with null packages = CES-dominant. NES only for the small packaged domain slice (2%). Compare: slp_rstdstore (related name).

## [ITC] upp_dopproduct_combo_p2p_dcc_upgrade_upp_dopproduc

Prefix group  : upp
Human label   : Upsell — DOP Combo — P2P DCC Upgrade
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,092 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : DOP combo upgrade upsell originating from DCC (Domain Control Center), P2P navigation. ITC likely truncated. 100% CES.

## [ITC] upp_p2p_upgrade-downgrade

Prefix group  : upp
Human label   : Upsell — P2P General Upgrade/Downgrade Surface (Multi-Product)
Page source   : not mapped
Products      : M365 52.2%, Vendor Email 17.9%, WAM 10.3%, CnP Hosting 6.8%, cPanel Business 3.5%, OX 3.5%, Website Protection 2.3%, VPS 1.5%, MWP 1.1%, other <1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,071 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : General-purpose P2P upgrade/downgrade surface used across many product lines. Broadest product distribution of any upp_ ITC in the medium-volume range — a catch-all tier change surface. All CES.

## [ITC] upp_p2p_start_upp_start

Prefix group  : upp
Human label   : Upsell — P2P Start — WAM / M365 Starter Surface
Page source   : not mapped
Products      : WAM 76.5%, M365 23.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,057 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : P2P "start" entry point. WAM-heavy (76.5%) with M365 cross-sell (23.5%). Likely the initial upsell surface shown to new or free-tier customers starting a WAM journey. All CES.

## [ITC] studio_ios_search_recommendation

Prefix group  : other (studio_)
Human label   : Studio iOS App — Domain Search Recommendation Surface
Page source   : not mapped
Products      : Domain Reg 98.9% (domain packaged 62.0%, unpackaged 28.2%, domain-bundle 8.7%), DOP domain-bundle 1.0%
NES/CES       : NES
Top packages  : domain, domain-bundle
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1,055 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : GoDaddy Studio iOS app domain search recommendation flow. High NES attachment (70%+ packaged domains). studio_ prefix = GoDaddy Studio creative app surfaces.

## [ITC] upp_d2p_dashboard

Prefix group  : upp
Human label   : Upsell — D2P (Dashboard to Panel) — General Dashboard Surface
Page source   : not mapped
Products      : M365 85.9%, Conversations 12.0%, Value Adds 2.1%, WAM <0.1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,053 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : General D2P upsell from main dashboard. M365-dominant with Conversations product (12%) — suggests dashboard surface where M365+phone/conversations are paired. All CES.

## [ITC] mya_vh_buildwebsite_website

Prefix group  : mya
Human label   : My Account — VH (Virtual Hosting) — Build Website Surface
Page source   : not mapped
Products      : MWP 57.3%, M365 37.9%, Vendor Email 4.8%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,033 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : My Account surface for Virtual Hosting customers prompted to build a website. MWP + M365 combination suggests a website+email bundling prompt. All CES.


## [ITC] upp_o365product_d2p_vnext-dashboard_venture_discov

Prefix group  : upp
Human label   : Upsell — M365 — D2P vNext Dashboard — Venture Discovery Surface
Page source   : not mapped
Products      : M365 93.9%, Value Adds 5.2%, Conversations 0.9%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,032 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : vNext dashboard D2P upsell targeting Venture plan customers at discovery stage. "venture_discov" = venture discovery path. All CES.

## [ITC] 123reg_slp_webhosting

Prefix group  : other (123reg_)
Human label   : 123-reg UK Partner — Web Hosting Sales Landing Page
Page source   : not mapped
Products      : CnP Hosting 55.6%, Vendor Email 38.5%, SSL 5.9%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,027 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : 123-reg is a GoDaddy-owned UK domain/hosting registrar. 123reg_ prefix = UK partner surface. Hosting + Email + SSL bundle pattern. All CES.

## [ITC] upp_o365product_d2p_start_m365wamspuredirect

Prefix group  : upp
Human label   : Upsell — M365 — D2P Start — M365/WAM Pure Direct Entry
Page source   : not mapped
Products      : M365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,009 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : "start" D2P surface for M365 pure-direct entry (m365wamspuredirect = direct nav without prior WAM context). All CES.

## [ITC] studio_android_domain_renewal

Prefix group  : other (studio_)
Human label   : GoDaddy Studio Android App — Domain Renewal Surface
Page source   : not mapped
Products      : Domain Name Registration (renewal) 80.2%, DOP 19.4%, Website Protection 0.4%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1,006 orders as of 2026-05-15 — Medium
Explored      : 2026-05-15
Notes         : GoDaddy Studio Android app domain renewal flow. High DOP attachment (19.4%) alongside renewals. All null packages = CES.

## [ITC] dna_wonnonmanagednonescrowoffer

Prefix group  : other (dna_)
Human label   : Domain Aftermarket — Won Non-Managed Non-Escrow Offer (Auction)
Page source   : not mapped
Products      : Domain Marketplace 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 995 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Won domain at auction via non-managed (self-service) non-escrow offer path. Domain Marketplace = aftermarket domain acquisition. CES.

## [ITC] upp_wamproduct_p2p_account_upgrade-downgrade

Prefix group  : upp
Human label   : Upsell — WAM — P2P Account Upgrade/Downgrade
Page source   : not mapped
Products      : WAM 87.3%, M365 8.9%, Strategic Partnerships 3.4%, Vendor Email 0.2%, OX <0.1%, MWP <0.1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 990 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : WAM plan change surface (up or down). M365/Partnerships tail reflects cross-product options exposed during WAM tier changes. All CES.

## [ITC] mya_dom_srch.aftermarket_tldcard

Prefix group  : mya
Human label   : My Account — Domain Search Aftermarket — TLD Card
Page source   : not mapped
Products      : Domain Reg 72.2% (packaged 67.9%), Marketplace 13.5%, Transfer 7.1%, Premium 5.6%, DOP 1.7%
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 988 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : My Account domain search aftermarket subpath with TLD card UI. ~94% of orders use the domain package (NES). All aftermarket domain types (reg, marketplace, transfer, premium) flow through same package.

## [ITC] px_xgrade

Prefix group  : other (px_)
Human label   : Pricing Experiment — Cross-Grade (Upgrade/Downgrade) Surface
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 984 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : px_ prefix = pricing experiment surface. xgrade = cross-grade (tier change). 100% DOP purchases. CES.

## [ITC] app_o365_renew_inpanel_suspendedaccount

Prefix group  : other (app_)
Human label   : M365 App — Renew In-Panel — Suspended Account Renewal
Page source   : not mapped
Products      : M365 83.6%, Value Adds 16.4%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 960 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : In-panel renewal surface triggered for suspended M365 accounts. High Value Adds attachment (16.4%) relative to other M365 renewal ITCs — may reflect bundled features prompted at reactivation. All CES.

## [ITC] dna_api_lgcy_closeouts_bin

Prefix group  : other (dna_)
Human label   : Domain Aftermarket — API Legacy Closeouts Bin
Page source   : not mapped
Products      : Aftermarket Non-Retail 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 949 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : API-sourced legacy closeout bin purchases on domain aftermarket. Non-retail = auction/backorder/closeout type transactions not via retail price. All CES.

## [ITC] upp_titanproduct_d2p_productivity_add-user

Prefix group  : upp
Human label   : Upsell — Titan Email — D2P Productivity — Add User
Page source   : not mapped
Products      : Vendor Email (Titan) 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 925 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : D2P productivity add-user flow for Titan email product. Single-product ITC. All CES.

## [ITC] vh_drp_stack_bundle

Prefix group  : other (vh_)
Human label   : Virtual Hosting — Domain Renewal / Drop Stack Bundle
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 922 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : vh_ prefix = Virtual Hosting surface. drp = drop/renewal path. Stack bundle = multi-item renewal bundle at VH context. 100% domain reg, all CES.

## [ITC] slp_wsb_ft_nocc_config

Prefix group  : slp
Human label   : Website Builder Free Trial No-CC — Configuration Landing Page
Page source   : not mapped
Products      : WAM 61.7%, M365 35.9%, Vendor Email 2.4%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 917 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Configuration variant of the WSB free-trial no-credit-card page (compare: slp_wsb_ft_nocc which is NES). This config variant is CES — likely the post-selection plan configuration step rather than the main SLP.

## [ITC] app_cpanelui_upgrade_resources

Prefix group  : other (app_)
Human label   : cPanel App UI — Upgrade Resources (Storage/Bandwidth)
Page source   : not mapped
Products      : cPanel Business Hosting 57.7%, CnP Hosting 42.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 912 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : In-app cPanel UI surface for upgrading hosting resources (storage, CPU, bandwidth). Two cPanel variants (Business vs CnP). All CES. Compare: app_cpanelhui_upgrade_resources (HUI = horizontal UI variant).

## [ITC] mob_gdm_ios_domain_search

Prefix group  : other (mob_)
Human label   : GoDaddy Mobile iOS — Domain Search Surface
Page source   : not mapped
Products      : Domain Reg 97.0%, Domain Marketplace 0.9%, Aftermarket Non-Retail (DBS) 0.9%, Domain Premium 0.4%, Domain Transfer 0.4%, DOP 0.2%
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1)
Volume        : 906 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Mobile GoDaddy app iOS domain search. High NES attachment ~93.7% (domain+domain-bundle+dbs). mob_ prefix = GoDaddy mobile app surfaces.

## [ITC] gocentral_domain_search_from_domain_suggestions

Prefix group  : other (gocentral_)
Human label   : GoCentral — Domain Search From Domain Suggestions
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 861 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : gocentral_ = GoCentral (legacy website builder, predecessor to WAM). Domain search triggered from the domain suggestions panel. All null packages = CES. Legacy surface still generating orders.

## [ITC] upp_complianceproduct_d2p_airo-compliance_genai.se

Prefix group  : upp
Human label   : Upsell — AI Compliance Product — D2P Airo Compliance GenAI Surface
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 861 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : D2P upsell for Airo AI compliance product (genai.se suffix = GenAI social/SEO feature). ITC likely truncated at 50 chars. 100% Airo, CES.

## [ITC] dpp_absol1expdna

Prefix group  : dpp
Human label   : Domain Purchase Path — Absolute Domain 1 — Expired Domain / Auction Path
Page source   : not mapped
Products      : Domain Name Auction 88.0%, Aftermarket Non-Retail 11.7%, Domain Reg 0.2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 852 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : expdna = expired domain name auction. Subpath of dpp_absol1 for expired/expiring domain discovery. Dominated by auction acquisitions. All CES.

## [ITC] app_cpanelhui_upgrade_resources

Prefix group  : other (app_)
Human label   : cPanel App Horizontal UI — Upgrade Resources
Page source   : not mapped
Products      : CnP Hosting 69.0%, cPanel Business Hosting 31.0%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 842 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : HUI = Horizontal UI variant of the cPanel upgrade-resources surface. Opposite product-mix ratio to app_cpanelui_upgrade_resources (69% CnP vs 57.7% cPanel Business). Both CES.

## [ITC] dcc_domsettings_xgrade_portfolio_a

Prefix group  : dcc
Human label   : Domain Control Center — Domain Settings Cross-Grade — Portfolio (Variant A)
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 822 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DCC domain settings cross-grade surface, portfolio view, A-variant (A/B test or UI variant). 100% DOP purchases. All CES.

## [ITC] ios_studio_app_deeplink_domain_search

Prefix group  : other (ios_)
Human label   : GoDaddy Studio iOS App — Deep Link Domain Search
Page source   : not mapped
Products      : Domain Reg 99.3% (NULL 81.3%, domain packaged 10.0%, domain-bundle 8.0%), DOP 0.5%, Marketplace/Transfer <0.2%
NES/CES       : Mixed (CES-dominant)
Top packages  : domain, domain-bundle
Champion      : domain → edf13c43 (Rev 3); minor component only (~18% of volume)
Volume        : 812 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Studio iOS app deep-link triggered domain search (external link → app → domain purchase). 81.3% unpackaged (CES). NES component exists via domain/domain-bundle packages (~18%).

## [ITC] 123reg_titan_prolight

Prefix group  : other (123reg_)
Human label   : 123-reg UK Partner — Titan Email Pro Light
Page source   : not mapped
Products      : Vendor Email (Titan) 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 799 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123-reg UK partner surface for Titan email (pro light tier). Single-product, CES only.

## [ITC] conversations.a2p

Prefix group  : other (conversations.)
Human label   : Conversations Product — A2P (Application-to-Person) Messaging Surface
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 787 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Unusual dot-notation ITC (not underscore). conversations. prefix = GoDaddy Conversations (phone/messaging product). a2p = Application-to-Person messaging (SMS/business messaging). CES.

## [ITC] dcc_domsettings_card_xgrade_overview

Prefix group  : dcc
Human label   : Domain Control Center — Domain Settings Card Cross-Grade — Overview
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 771 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DCC domain settings cross-grade in card/overview layout. 100% DOP. Compare: dcc_domsettings_xgrade_portfolio_a (portfolio list view variant). Both CES.

## [ITC] ios_studio_app_createshelf_domains

Prefix group  : other (ios_)
Human label   : GoDaddy Studio iOS App — Create Shelf — Domains Section
Page source   : not mapped
Products      : Domain Reg 99.3% (NULL 85.7%, domain packaged 13.6%), DOP 0.7%
NES/CES       : Mixed (CES-dominant)
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3); minor component only (~14% of volume)
Volume        : 748 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Studio iOS "create shelf" = asset/domain browsing shelf in the app. 85.7% unpackaged (CES). Small NES component via domain package.

## [ITC] mgr_auctionscart

Prefix group  : other (mgr_)
Human label   : Auctions Cart — Management/Checkout Surface
Page source   : not mapped
Products      : Aftermarket Non-Retail 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 748 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mgr_ = management/configuration surface. Auctions cart checkout flow for aftermarket (auction) domain acquisitions. 100% CES.

## [ITC] upp_o365product_d2p_dashboard_uep

Prefix group  : upp
Human label   : Upsell — M365 — D2P Dashboard — Unknown Entry Point
Page source   : not mapped
Products      : M365 87.0%, Conversations 11.5%, Value Adds 1.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 747 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : D2P dashboard upsell for M365 where entry point is untracked (uep = unknown entry point). Conversations at 11.5% = phone product cross-sell. All CES.

## [ITC] mya_dom_srch.favorites

Prefix group  : mya
Human label   : My Account — Domain Search — Favorites / Saved Domains
Page source   : not mapped
Products      : Domain Reg 91.9% (domain packaged 78.4%, NULL 13.5%), Aftermarket Non-Retail (DBS) 4.1%, DOP 1.8%, Marketplace 1.1%, Transfer 1.1%
NES/CES       : NES
Top packages  : domain, dbs
Champion      : domain → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1)
Volume        : 732 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : My Account domain search — favorites/saved domains subpath. 84.7% packaged (NES dominant). Customers save preferred domains and return to purchase; high NES attachment suggests consistent offer serving.

## [ITC] slp_wsb_ft_getstarted_plans_nocc_config

Prefix group  : slp
Human label   : Website Builder Free Trial Get Started — Plans No-CC — Configuration Page
Page source   : not mapped
Products      : WAM 60.9%, M365 29.9%, Vendor Email 9.2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 726 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Configuration step of the WSB free-trial get-started/plans no-CC flow. WAM+M365+Email bundle pattern mirrors the main slp_wsb_ft_nocc but this is the config variant. All CES. Compare: slp_wsb_ft_getstarted_plans_nocc_config vs slp_wsb_ft_nocc (NES) — config variants are CES.

## [ITC] app_mwpv2ui_myh_upgrade_resources

Prefix group  : other (app_)
Human label   : MWP v2 App UI — My Hosting — Upgrade Resources
Page source   : not mapped
Products      : WordPress Managed Plans (MWP) 88.1%, Website Protection 11.9%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 721 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mwpv2ui = Managed WordPress v2 UI. myh = My Hosting panel. Upgrade resources surface (storage/plan tier). Website Protection at 11.9% = security upsell co-located here. All CES.


## [ITC] dlp_titan_email

Prefix group  : dlp
Human label   : Titan Email Domain Landing Page
Page source   : not mapped
Products      : Vendor Email (Titan) 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 711 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DLP for Titan/Vendor Email product. All CES, null packages.

## [ITC] app_ox_upgrade

Prefix group  : other (app_)
Human label   : Open XChange App — Plan Upgrade Surface
Page source   : not mapped
Products      : Open XChange 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 707 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : In-app OX plan upgrade surface. Single-product, CES only.

## [ITC] cart_inline_dop

Prefix group  : other (cart_)
Human label   : Cart — Inline DOP (Domain Ownership Protection) Add-On
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 697 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Inline DOP upsell rendered within the cart flow. Single-product, CES.

## [ITC] venture-dashboard

Prefix group  : other (no prefix — hyphenated)
Human label   : Venture Dashboard Surface
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 696 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Unusual ITC — hyphenated, no standard prefix. Likely a GoDaddy Ventures product dashboard (may correspond to GoDaddy Commerce/Poynt). 100% DOP, CES.

## [ITC] slp_ssl_config

Prefix group  : slp
Human label   : SSL Configuration / Post-Purchase Setup Landing Page
Page source   : not mapped
Products      : SSL 82.7%, Strategic Partnerships AC 17.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 695 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : SSL configuration page (likely post-purchase setup flow). Strategic Partnerships AC = anti-churn SSL offer variant shown alongside standard SSL. All CES.

## [ITC] auction_fos_afternic_listing_exact

Prefix group  : other (auction_fos_)
Human label   : Afternic Auction Front of Site — Exact-Match Listing
Page source   : not mapped
Products      : Domain Marketplace 52.6%, Domain Transfer 38.2%, Domain Premium 8.9%, Domain Reg 0.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 684 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : auction_fos_ = Afternic auction Front of Site. Exact-match listing = buyer searched for the specific domain and found it in Afternic listings. Mix of Marketplace (buy-now), Transfer, and Premium aftermarket paths. All CES.

## [ITC] ddc_pro_01

Prefix group  : other (ddc_)
Human label   : Domain Discount Club — Pro Tier (Membership Purchase)
Page source   : not mapped
Products      : Domain Buyers Club 100%
NES/CES       : NES
Top packages  : pfid-1809421
Champion      : pfid-1809421 — catalog resolution pending (MCP unavailable at profile time)
Volume        : 678 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ddc_ here = Domain Discount Club (DDC) membership product — NOT Domain Control Center. Pro tier (01 = entry/base variant). Unusual PFID-format package ID (pfid-1809421). Single-product NES surface.

## [ITC] upp_dopproduct_ultimate_p2p_dcc_upgrade_upp_doppro

Prefix group  : upp
Human label   : UPP — DOP Ultimate — P2P DCC Upgrade
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 676 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP-served DOP Ultimate upgrade from DCC context, P2P flow. ITC likely truncated. DCC here = Domain Control Center (source of the upgrade prompt). 100% CES.

## [ITC] hmc_dv_ssl

Prefix group  : other (hmc_)
Human label   : Hosting Management Console — DV SSL Certificate Purchase
Page source   : not mapped
Products      : SSL 100% (ssl-001sites-tier1 57.5%, ssl-001sites-managed-tier1 19.7%, ssl-wildcard-tier1 14.5%, NULL 4.3%, ssl-005sites-tier1 3.8%, ssl-005sites-managed-tier1 0.1%)
NES/CES       : NES
Top packages  : ssl-001sites-tier1, ssl-001sites-managed-tier1, ssl-wildcard-tier1
Champion      : ssl-001sites-tier1 → 28e5b730 or bb0afea9 (catalog resolution pending; known SSL offer family)
Volume        : 676 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : hmc_ = Hosting Management Console. DV = Domain Validated (standard SSL tier). SSL packages follow the ssl-{N}sites-{managed-}tier{N} naming convention. Known champion candidates: 28e5b730 (SAN) or bb0afea9 (single-domain SSL).

## [ITC] dcc_portfolio_transfer_in_stack_bundle

Prefix group  : dcc
Human label   : Domain Control Center — Portfolio — Transfer In Stack Bundle
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 676 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DCC portfolio view — inbound domain transfer bundled as a stack. Domain Reg (transfer) purchases, all CES, null packages.

## [ITC] dcc_drp_overview_settings_xgrade

Prefix group  : dcc
Human label   : Domain Control Center — Domain Renewal Path — Overview Settings Cross-Grade
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 655 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DCC domain renewal path (drp), overview/settings view, cross-grade surface. 100% DOP purchases at this step. CES.

## [ITC] buynow

Prefix group  : other (no prefix)
Human label   : Afternic / Marketplace — Buy Now Surface
Page source   : not mapped
Products      : Domain Marketplace 50.8%, Domain Transfer 28.1%, Domain Premium 21.2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 652 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : No-prefix ITC. "Buy Now" = Afternic/GoDaddy marketplace fixed-price purchase flow (as opposed to auction bidding). Mix of Marketplace, Transfer, and Premium aftermarket acquisition types. All CES.

## [ITC] upp_airobuildercreditsproduct_p2p_airo-builder_usa

Prefix group  : upp
Human label   : UPP — Airo Builder Credits — P2P US-Only Variant
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 639 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : US-market-only variant of the Airo builder credits P2P upsell (compare: _bud and _man variants). ITC likely truncated. 100% CES.

## [ITC] am_gdcart_seller_custom_checkout_link

Prefix group  : other (am_)
Human label   : Aftermarket — GoDaddy Cart — Seller Custom Checkout Link
Page source   : not mapped
Products      : Domain Marketplace 51.5%, Domain Transfer 36.7%, Domain Premium 11.8%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 608 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : am_ = aftermarket. Seller-provided custom checkout link directing buyer to GoDaddy cart for domain purchase. All aftermarket domain types (Marketplace, Transfer, Premium). CES.

## [ITC] upp_d2p_panel-lite_vnext-dashboard

Prefix group  : upp
Human label   : UPP — D2P Panel Lite — vNext Dashboard
Page source   : not mapped
Products      : Vendor Email (Titan) 84.0%, M365 15.7%, Value Adds 0.3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 605 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP-served D2P panel-lite email upsell on vNext dashboard. Titan Email dominant (84%) with M365 cross-sell (15.7%). All CES.

## [ITC] dpp_whois_results

Prefix group  : dpp
Human label   : Domain Purchase Path — WHOIS Results Surface
Page source   : not mapped
Products      : Domain Reg 92.8%, DOP 6.4%, Domain Premium 0.5%, Domain Marketplace 0.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 598 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DPP surface triggered when a customer looks up WHOIS data and is prompted to register or acquire the domain. All null packages = CES. DOP attachment (6.4%) typical for domain purchase flows.

## [ITC] 123reg_slp_m365

Prefix group  : other (123reg_)
Human label   : 123-reg UK Partner — M365 Sales Landing Page
Page source   : not mapped
Products      : M365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 593 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123-reg UK partner surface for Microsoft 365. Single-product, CES.

## [ITC] android_studio_app_deeplink_domain_search

Prefix group  : other (android_)
Human label   : GoDaddy Studio Android App — Deep Link Domain Search
Page source   : not mapped
Products      : Domain Reg 99.7% (NULL 93.4%, domain packaged 6.0%, dbs 0.2%), DOP 0.3%
NES/CES       : Mixed (CES-dominant)
Top packages  : domain, dbs
Champion      : domain → edf13c43 (Rev 3); minor component only (~6% of volume)
Volume        : 580 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Android counterpart to ios_studio_app_deeplink_domain_search. Very similar profile — deep-link triggered domain search, 93.4% unpackaged (CES), small NES component via domain package.

## [ITC] slp_subs_pricing

Prefix group  : slp
Human label   : Subscription Pricing Landing Page — International DEM Bundle (UK/AU/CA)
Page source   : not mapped
Products      : DOP ~35% + Domain Reg ~30% (both via dpp-xx-solution bundles), M365 ~20%, WAM ~5%, other small
NES/CES       : NES
Top packages  : dpp-uk-com-solution-tier1, dpp-au-com-solution-tier1, dpp-ca-com-solution-tier1, dpp-uk-couk-solution-tier1
Champion      : dpp-uk-com-solution-tier1 → catalog resolution pending (international DEM bundle offer)
Volume        : 558 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DEM market (UK, AU, CA) subscription pricing page. The dpp-xx-com/couk-solution-tier{N} packages are international domain+DOP+M365 bundles sold as a unit. Multi-tier (1–3) per market. Compare: plp_starter_bundle uses same package family. Catalog unresolvable at profile time.

## [ITC] slp_ssl_managed

Prefix group  : slp
Human label   : SSL Managed Certificate Sales Landing Page
Page source   : not mapped
Products      : SSL 100% (ssl-001sites-managed-tier1 92.6%, ssl-wildcard-managed-tier1 2.5%, ssl-005sites-managed-tier1 0.9%, NULL 3.9%)
NES/CES       : NES
Top packages  : ssl-001sites-managed-tier1, ssl-wildcard-managed-tier1
Champion      : ssl-001sites-managed-tier1 → 28e5b730 or bb0afea9 (catalog resolution pending; known SSL offer family)
Volume        : 557 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Managed SSL certificate landing page (managed = GoDaddy installs/renews automatically). Compare: hmc_dv_ssl (manual DV SSL) uses same offer family. "managed" = auto-installation included.

## [ITC] upp_logoimageproduct_d2p_brandbook_gai.vnext.brand

Prefix group  : upp
Human label   : UPP — AI Logo / Brand Book — D2P vNext Brand Surface
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 556 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : vNext brand variant of the AI brand book D2P upsell. ITC truncated at 50 chars. Consistent with other upp_logoimageproduct variants (all Airo, CES). .vnext.brand suffix = vNext dashboard brand feature context.

## [ITC] upp_wamproduct_f2p_start_upgrade

Prefix group  : upp
Human label   : UPP — WAM — F2P Start / Starter Upgrade
Page source   : not mapped
Products      : WAM 82.4%, M365 17.6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 533 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Free-to-paid starter upgrade for WAM, with M365 cross-sell (17.6%). Compare: upp_wamproduct_f2p_account_upgrade (similar mix, higher volume). All CES.

## [ITC] upp_default_p2p_account_renewals

Prefix group  : upp
Human label   : UPP — Default P2P Account Renewals (Multi-Product Catch-All)
Page source   : not mapped
Products      : SSL 39.4%, CnP Hosting 27.4%, MWP 12.3%, Website Protection 5.7%, Virtual Hosting 4.5%, Express Email 2.6%, cPanel Business 2.3%, WAM 1.1%, Airo 1.1%, Pro Web Services 0.9%, Domain Buyers Club 0.8%, others <0.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 530 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Default catch-all renewal surface for P2P when no product-specific renewal ITC is matched. Broad product distribution (15 product lines) reflects its fallback role. SSL dominant (39.4%). All CES.

## [ITC] upp_dopproduct_standalone_p2p_account_upgrade_upp_

Prefix group  : upp
Human label   : UPP — DOP Standalone — P2P Account Upgrade
Page source   : not mapped
Products      : DOP 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 516 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Standalone DOP (not bundled) P2P account upgrade via UPP. ITC likely truncated. 100% CES.

## [ITC] notifications_beacon

Prefix group  : other (notifications_)
Human label   : Notifications / Beacon — Cross-Product Renewal / Offer Surface
Page source   : not mapped
Products      : Domain Reg 50.5%, M365 16.6%, WAM 7.3%, CnP Hosting 7.1%, DOP 5.1%, OX 3.4%, Value Adds 2.2%, MWP 1.8%, SSL 1.2%, cPanel Business 1.0%, Website Protection 1.0%, Conversations 0.8%, others <0.5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 505 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Notification/beacon surface (in-app alert or push notification → purchase). Broadest product mix of any single ITC in this volume range (159 distinct pfids). Domain Reg dominant (50.5%). All null packages = CES. Likely a catch-all for notification-triggered purchases.

## [ITC] plp_starter_bundle

Prefix group  : other (plp_)
Human label   : Products Landing Page — Starter Bundle (International DEM Markets)
Page source   : not mapped
Products      : DOP ~37% + Domain Reg ~26% (via dpp-xx-solution bundles), WAM ~8%, M365 ~28% (mix packaged + NULL), small domain-only tail
NES/CES       : NES
Top packages  : dpp-uk-com-solution-tier1, dpp-au-com-solution-tier1, dpp-ca-com-solution-tier1, dpp-uk-couk-solution-tier1
Champion      : dpp-uk-com-solution-tier1 → catalog resolution pending (same international DEM bundle family as slp_subs_pricing)
Volume        : 502 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : plp_ = Products Landing Page. International starter bundle sold in DEM markets (UK, AU, CA). Same dpp-xx-solution package family as slp_subs_pricing — both are DEM market NES bundle surfaces. Catalog resolution pending.

## [ITC] slp_ssl_wildcard

Prefix group  : slp
Human label   : SSL Wildcard Certificate Sales Landing Page
Page source   : not mapped
Products      : SSL 100% (ssl-wildcard-tier1 99.6%, NULL 0.4%)
NES/CES       : NES
Top packages  : ssl-wildcard-tier1
Champion      : ssl-wildcard-tier1 → 28e5b730 or bb0afea9 (catalog resolution pending; known SSL offer family)
Volume        : 500 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Dedicated landing page for Wildcard SSL (covers all subdomains). Near-100% NES via ssl-wildcard-tier1. Known SSL champion candidates: 28e5b730 or bb0afea9.

## [ITC] auction_fos_afternic_listing_search

Prefix group  : other (auction_fos_)
Human label   : Afternic Auction Front of Site — Search Listing (Non-Exact)
Page source   : not mapped
Products      : Domain Marketplace 51.9%, Domain Transfer 28.9%, Domain Premium 17.6%, Domain Reg 1.6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 499 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Afternic auction Front of Site — search results listing (non-exact-match; customer searched broadly and found a listed domain). Compare: auction_fos_afternic_listing_exact (exact-match variant, 684 orders). Same product distribution pattern.

## [ITC] dify-attach

Prefix group  : other (dify-)
Human label   : DIFY (Digital Marketing / Social) — Attach Surface (Hyphenated Variant)
Page source   : not mapped
Products      : Pro Web Services 76.9%, DIFY Social 23.1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 494 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Hyphen-separated variant of dify_attach (compare: dify_attach with underscore, 1,255 orders). Nearly identical product profile. Both are CES DIFY attach surfaces — likely a routing or naming inconsistency between environments.

## [ITC] ddc_starter_01

Prefix group  : other (ddc_)
Human label   : Domain Discount Club — Starter/Basic Tier (Membership Purchase)
Page source   : not mapped
Products      : Domain Buyers Club 100% (ddc-basic-tier1 98.6%, NULL 1.4%)
NES/CES       : NES
Top packages  : ddc-basic-tier1
Champion      : ddc-basic-tier1 → catalog resolution pending (DDC basic membership offer)
Volume        : 488 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ddc_ = Domain Discount Club (DDC) — NOT Domain Control Center. Starter/basic tier membership. Compare: ddc_pro_01 (pro tier, pfid-1809421 package). Both are DDC membership purchase ITCs served via NES.


## [ITC] dcc_mobile_list_app_transfer_in_stack_bundle

Prefix group  : dcc_
Human label   : Domain Control Center Mobile — Transfer In with Bundle Stack
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 486 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] auctionscart

Prefix group  : other
Human label   : Afternic Auctions Cart — Domain Marketplace Purchase
Page source   : not mapped
Products      : Aftermarket Non-Retail 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 483 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Single-segment ITC (no prefix underscore). Likely the Afternic auctions cart surface.

## [ITC] upp_d2p_account.products.account_products.privacy.

Prefix group  : upp_
Human label   : UPP — Account Dashboard Domain Privacy / DOP Add
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 479 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains dots (account.products.account_products.privacy.) — full dotted path preserved in ITC string.

## [ITC] 123reg_slp_wsb

Prefix group  : other
Human label   : 123 Reg UK Partner — Website Builder Sales Page
Page source   : not mapped
Products      : Websites and Marketing 62%, Vendor Email 38%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 465 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123reg_ is the UK partner brand prefix (123 Reg). Analogous to slp_wsb but for the UK partner storefront.

## [ITC] upp_conversationsproduct_d2p_websites_conversation

Prefix group  : upp_
Human label   : UPP — Conversations Product via Websites Dashboard
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 454 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_webhostingproduct_d2p_dashboard_unknown-entry-

Prefix group  : upp_
Human label   : UPP — Web Hosting Product Dashboard (Unknown Entry Point)
Page source   : not mapped
Products      : CnP Hosting 82%, WordPress Managed Plans 17%, cPanel Business Hosting 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 427 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug ends with "unknown-entry-" — entry point not captured in ITC routing. CnP + MWP mix suggests a generic hosting dashboard path.

## [ITC] am_gdcart_afternicfos

Prefix group  : other
Human label   : Afternic GD Cart — Afternic Front of Site Domain Purchase
Page source   : not mapped
Products      : Domain Name Registration 57% (domain + domain-bundle NES), Aftermarket Non-Retail 24% (dbs NES), Domain Marketplace 11%, Domain Name Premium 4%, Domain Name Transfer 3%, Domain Ownership Protection 1%
NES/CES       : Mixed
Top packages  : domain, dbs, domain-bundle
Champion      : domain → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1); domain-bundle → edf13c43 (Rev 3)
Volume        : 425 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : am_ prefix = aftermarket/Afternic. This is the GD cart surface on Afternic's front of site. Distinct from auction_fos_ (Afternic FOS browsing).

## [ITC] mgr_slp_email_encryption_config

Prefix group  : other
Human label   : Manager — Email Encryption Configuration Sales Page (M365)
Page source   : not mapped
Products      : MS Office 365 50%, Value Adds 50%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 425 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mgr_ prefix likely = Manager admin/config UI. Email encryption config page driving M365 and Value Add purchases.

## [ITC] app_hosting_addon_php

Prefix group  : other
Human label   : In-App — Hosting PHP Add-On Purchase
Page source   : not mapped
Products      : CnP Hosting 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 414 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : app_ prefix = in-app purchase flow. PHP add-on specifically for CnP (cPanel) hosting products.

## [ITC] fos_action_service

Prefix group  : other
Human label   : Front of Site — Action Service (Domain Ownership Protection)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 402 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : fos_ as prefix (no slp_) — alternative FOS routing for action-service style flows. DOP-only.

## [ITC] plp_essentials_bundle

Prefix group  : other
Human label   : Product Landing Page — Essentials Bundle (DEM Market Domains + M365 + WAM)
Page source   : not mapped
Products      : Domain Ownership Protection (dpp-xx-com-solution-tier2 NES), Domain Name Registration (dpp-xx-com-solution-tier2 + domain-bundle NES), Websites and Marketing (Mixed), MS Office 365 (CES)
NES/CES       : Mixed
Top packages  : dpp-au-com-solution-tier2, dpp-ca-com-solution-tier2, dpp-uk-com-solution-tier2, dpp-au-comau-solution-tier2, domain-bundle
Champion      : domain-bundle → edf13c43 (Rev 3); dpp-xx-com-solution-tier2 → catalog resolution pending (DEM market bundles)
Volume        : 402 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DEM market bundles (AU, CA, UK) analogous to plp_starter_bundle. plp_ = Product Landing Page. Cross-reference plp_starter_bundle for same package family pattern.

## [ITC] upp_wamproduct_p2p_account_renewals

Prefix group  : upp_
Human label   : UPP — WAM Product Account Renewals (Peer-to-Peer)
Page source   : not mapped
Products      : Websites and Marketing 82%, MS Office 365 17%, Strategic Partnerships AC 1%, Open XChange <1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 379 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mya_dom_srch.regpremium_exact

Prefix group  : mya_
Human label   : My Account — Domain Search Premium Exact Match Registration
Page source   : not mapped
Products      : Domain Name Registration 96% (domain NES 51%, NULL CES 45%), Domain Ownership Protection 4%
NES/CES       : Mixed
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 374 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains dot (.regpremium_exact) in the slug. My Account domain search surface, premium/exact-match variant.

## [ITC] mgr_slp_365_category

Prefix group  : other
Human label   : Manager — Microsoft 365 Category Sales Page
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 370 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] add_addon_downgrade_mailbox

Prefix group  : other
Human label   : Add-On — Mailbox Downgrade Add-On Purchase
Page source   : not mapped
Products      : Value Adds 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 366 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : add_ prefix likely = add-on purchase flow. Value Adds product = mailbox/email add-ons.

## [ITC] slp_365

Prefix group  : slp_
Human label   : Front of Site — Microsoft 365 Sales Landing Page
Page source   : not mapped
Products      : MS Office 365 85% (office365-tier0/1/3 NES + some CES null), Value Adds 15% (office365-* NES packages)
NES/CES       : Mixed
Top packages  : office365-tier0, office365-tier3, office365-tier1, office365-emailplus-tier1
Champion      : office365-tier0 → 575a7d2a (M365 component); office365-tier1/tier3 → catalog resolution pending (same M365 family expected)
Volume        : 351 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] pro_reseller

Prefix group  : other
Human label   : Pro — Reseller Plan Sales Page (Turnkey Reseller)
Page source   : not mapped
Products      : Reseller 98% (turnkeyreseller-tier2 57%, turnkeyreseller-tier1 38%, domainreseller_india_012mo 2%), NULL 2%
NES/CES       : Mixed
Top packages  : turnkeyreseller-tier2, turnkeyreseller-tier1, domainreseller_india_012mo
Champion      : catalog resolution pending (turnkeyreseller-tier1/tier2)
Volume        : 347 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : pro_ prefix = Pro/Reseller products surface. Turnkey reseller = white-label reseller program. India-specific variant (domainreseller_india_012mo) also present.

## [ITC] domains_valuation_lp_purchase

Prefix group  : other
Human label   : Domain Valuation Landing Page — Domain Purchase
Page source   : not mapped
Products      : Domain Name Registration 92%, Aftermarket Non-Retail 3%, Domain Marketplace 2%, Domain Name Premium 1%, Domain Name Transfer 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 341 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : domains_ prefix = domain-specific landing pages. Valuation LP = a page that shows a domain's estimated market value, then drives purchase.

## [ITC] upp_titanproduct_d2p_panel-lite_uep_vnext-dashboar

Prefix group  : upp_
Human label   : UPP — Titan Email Product via Panel Lite Dashboard
Page source   : not mapped
Products      : Vendor Email 100% (Titan Email)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 335 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated at 50 chars (panel-lite_uep_vnext-dashboar). Vendor Email = Titan Email (product was migrated from OX to Titan). Panel Lite = lightweight hosting control panel.

## [ITC] upp_dopproduct_standalone_p2p_dcc_upgrade_upp_dopp

Prefix group  : upp_
Human label   : UPP — DOP Standalone Upgrade via Domain Control Center
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 328 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (ends with _upp_dopp). P2P = peer-to-peer upgrade flow; DCC = Domain Control Center upgrade surface.

## [ITC] studio_android_search_recommendation

Prefix group  : other
Human label   : GoDaddy Studio Android App — Search Recommendation Domain Registration
Page source   : not mapped
Products      : Domain Name Registration 99% (NULL CES 88% + domain NES 12%), Domain Ownership Protection <1%
NES/CES       : Mixed
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 305 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : studio_ prefix = GoDaddy Studio (design/creative app). Android variant; search recommendation feature drives domain registrations.

## [ITC] app_ox_adduser_buymoreaccounts_undefined

Prefix group  : other
Human label   : In-App — OpenXchange Add User / Buy More Accounts (Undefined Entry)
Page source   : not mapped
Products      : Open XChange 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 303 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : app_ prefix = in-app. OX = OpenXchange legacy email. "undefined" entry point = unresolved routing origin in the add-user flow.

## [ITC] mgr_slp_wsb_ft_nocc&ref=slp_trusted_config

Prefix group  : other
Human label   : Manager — Website Builder Free Trial No-CC Sales Page (Trusted Config Ref)
Page source   : not mapped
Products      : Websites and Marketing 54%, Vendor Email 46%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 302 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains URL query string characters (`&ref=slp_trusted_config`). mgr_ prefix = Manager. ft_nocc = free trial without credit card. Unusual — query param leaked into the ITC string.

## [ITC] upp_o365product_d2p_websites_m365wamspuredirect

Prefix group  : upp_
Human label   : UPP — M365 Product via Websites Dashboard (WAM Pure Direct Path)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 296 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : m365wamspuredirect = direct M365 purchase path from within the WAM/Websites product dashboard, no intermediary.

## [ITC] am_gdcart_affiliate_partner

Prefix group  : other
Human label   : Afternic GD Cart — Affiliate/Partner Domain Sales (Marketplace, Transfer, Premium)
Page source   : not mapped
Products      : Domain Marketplace 53%, Domain Name Transfer 30%, Domain Name Premium 18%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 287 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : am_ prefix = aftermarket/Afternic. Affiliate/partner channel — distinct from am_gdcart_afternicfos. No NES packages; all marketplace/transfer/premium domain types.

## [ITC] dpp_absol1.regpremium_alternate

Prefix group  : dpp_
Human label   : Domain Purchase Path — AbSol1 Premium Alternate Domain Registration
Page source   : not mapped
Products      : Domain Name Registration 98% (domain NES 73% + NULL CES 23%), Domain Ownership Protection 3%
NES/CES       : Mixed
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 286 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains dot (.regpremium_alternate). absol1 likely = absolute/absolute-layout experiment variant 1. Premium alternate = alternate search suggestion for premium domains.

## [ITC] mgr_slp_ssl_config

Prefix group  : other
Human label   : Manager — SSL Configuration Sales Page
Page source   : not mapped
Products      : SSL 67%, Strategic Partnerships AC 33%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 279 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Strategic Partnerships AC (33%) is an unusual co-product alongside SSL — likely bundled partner/reseller arrangement. mgr_ = Manager admin config UI.

## [ITC] upp_p2p_budget_exceeded.buy_credits_upp_airo_ai_bu

Prefix group  : upp_
Human label   : UPP — Airo AI Budget Exceeded / Buy Credits (P2P)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 276 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (ends with _airo_ai_bu). Airo = GoDaddy's AI-powered website builder. This surface fires when a user exceeds their Airo AI usage budget and needs to buy more credits.

## [ITC] slp_hosting_category_config

Prefix group  : slp_
Human label   : Front of Site — Hosting Category Configuration Sales Page
Page source   : not mapped
Products      : Virtual Hosting 71%, SSL 21%, Website Protection 7%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 274 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : category_config suffix = a configuration/category-level sales page for hosting. Virtual Hosting = shared/VPS hosting lines. SSL and Website Protection are common hosting add-ons.

## [ITC] upp_d2p_dcc.portfolio.spu

Prefix group  : upp_
Human label   : UPP — DCC Portfolio Single-Product Upgrade (DOP)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 266 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains dots (dcc.portfolio.spu). spu = single-product upgrade. DCC Portfolio view upgrade flow for DOP.


## [ITC] gdc_2_0_microsoft.com

Prefix group  : other
Human label   : GDC 2.0 Microsoft Referral — Domain Registration
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 266 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : gdc_ prefix with version (2_0) and partner domain (.microsoft.com). Likely a Microsoft partnership referral flow driving domain registrations. Unusual ITC format — no standard prefix group.

## [ITC] upp_d2p_m365wamspuredirect

Prefix group  : upp_
Human label   : UPP — M365 Direct Dashboard-to-Purchase Path
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 265 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : m365wamspuredirect = direct M365 purchase from dashboard without WAM intermediary. Counterpart to upp_o365product_d2p_websites_m365wamspuredirect (which is M365 via Websites).

## [ITC] upp_managedwordpressproduct_d2p_dashboard_unknown-

Prefix group  : upp_
Human label   : UPP — Managed WordPress Product Dashboard (Unknown Entry Point)
Page source   : not mapped
Products      : WordPress Managed Plans 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 261 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (ends with unknown-). Entry point not captured in ITC routing; MWP-only surface.

## [ITC] upp_p2p_renewals

Prefix group  : upp_
Human label   : UPP — Generic Multi-Product Renewals (Peer-to-Peer)
Page source   : not mapped
Products      : MS Office 365 35%, Websites and Marketing 14%, Conversations 14%, SSL 9%, CnP Hosting 8%, Vendor Email 5%, Value Adds 4%, Open XChange 4%, cPanel Business Hosting 1%, Express Email Marketing 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 255 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Broad multi-product renewal surface. High product diversity (10+ product lines) suggests a generic renewal dispatch ITC rather than a product-specific flow.

## [ITC] upp_conversationsproduct_d2p_sites_conversationstr

Prefix group  : upp_
Human label   : UPP — Conversations Product via Sites Dashboard (Streaming Variant)
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 254 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (conversationstr = likely conversationsstreaming or similar). Sites dashboard variant; compare to upp_conversationsproduct_d2p_websites_conversation and upp_conversationsproduct_d2p_dashboard_conversatio.

## [ITC] dna_invapp_details_android_expirycloseout

Prefix group  : other
Human label   : DNA — In-App Details Android Expiry Closeout Auction
Page source   : not mapped
Products      : Aftermarket Non-Retail 61%, Domain Name Auction 39%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 254 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : dna_ prefix = Domain Name Auctions. Expiry closeout = domains expiring soon being auctioned off. Android in-app details screen flow.

## [ITC] mgr_slp_365

Prefix group  : other
Human label   : Manager — Microsoft 365 Sales Page (Ungrouped)
Page source   : not mapped
Products      : MS Office 365 94%, Value Adds 5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 254 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Shorter/simpler variant of mgr_slp_365_category and mgr_slp_365_email_config. mgr_ = Manager config page. Likely a base or fallback M365 sales page.

## [ITC] mgr_slp_wsb_ft_nocc

Prefix group  : other
Human label   : Manager — Website Builder Free Trial No-CC Sales Page
Page source   : not mapped
Products      : Websites and Marketing 72%, MS Office 365 27%, Vendor Email <1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 252 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Base version of mgr_slp_wsb_ft_nocc_config (which is in the already-profiled set). ft_nocc = free trial without credit card. WAM + M365 co-sell pattern.

## [ITC] 123reg_slp_mwp

Prefix group  : other
Human label   : 123 Reg UK Partner — Managed WordPress Sales Page
Page source   : not mapped
Products      : WordPress Managed Plans 57%, Vendor Email 34%, SSL 9%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 251 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123reg_ = UK partner brand. MWP + Titan Email (Vendor Email) + SSL bundle typical for 123 Reg managed WordPress offering.

## [ITC] app_mwphui_upgrade_resources

Prefix group  : other
Human label   : In-App — Managed WordPress HUI Upgrade Resources
Page source   : not mapped
Products      : WordPress Managed Plans 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 244 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mwphui = Managed WordPress Hosting UI. In-app (app_) resource upgrade flow within the MWP hosting control panel.

## [ITC] upp_conversationsproduct_d2p_dashboard_conversatio

Prefix group  : upp_
Human label   : UPP — Conversations Product via Main Dashboard
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 243 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (conversatio...). Main/generic dashboard variant for Conversations product. Compare to the sites and websites dashboard variants.

## [ITC] dcc_portfolio_add_premium_product

Prefix group  : dcc_
Human label   : Domain Control Center Portfolio — Add Premium DNS
Page source   : not mapped
Products      : Premium DNS 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 241 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_manage_plan.buy_credits_upp_airo_ai_builde

Prefix group  : upp_
Human label   : UPP — Airo AI Builder Buy Credits (Manage Plan P2P)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 239 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated (ends with _ai_builde) and contains dot (manage_plan.). Manage Plan P2P path for buying additional Airo AI builder credits.

## [ITC] slp_wsb_ft_nocc&ref=slp_trusted_config

Prefix group  : slp_
Human label   : Front of Site — Website Builder Free Trial No-CC (URL Param Leaked in ITC)
Page source   : not mapped
Products      : Websites and Marketing 60%, Vendor Email 40%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 239 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC contains URL query string (`&ref=slp_trusted_config`) — ref param leaked into ITC string at tracking time. slp_ FOS variant of the free trial page; WAM + Titan co-sell. Compare to mgr_slp_wsb_ft_nocc&ref= (same pattern, mgr_ variant in Batch 7).

## [ITC] ddc_tier_01

Prefix group  : other
Human label   : Domain Discount Club — Tier 1 Plan (Domain Buyers Club)
Page source   : not mapped
Products      : Domain Buyers Club 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 234 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ddc_ = Domain Discount Club (NOT DCC). Domain Buyers Club = the subscription product for discounted domain pricing. Tier 01 = entry-level plan.

## [ITC] transferin_dcc_searchdomain

Prefix group  : other
Human label   : Transfer-In — DCC Domain Search (Domain Transfer + Registration)
Page source   : not mapped
Products      : Domain Name Registration 97% (domain NES 79%, domain-bundle NES 7%, NULL CES 10%), Domain Ownership Protection 2%, Domain Name Transfer <1%
NES/CES       : Mixed
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (Rev 3); domain-bundle → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1)
Volume        : 233 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : transferin_ prefix = domain transfer-in flow. Domain search within DCC used to find domains for transfer. Also drives new registrations via same search.

## [ITC] slp_ssl_dv

Prefix group  : slp_
Human label   : Front of Site — SSL Domain Validated (DV) Sales Page
Page source   : not mapped
Products      : SSL 100% (ssl-001sites-tier1 NES 93%, NULL CES 7%)
NES/CES       : Mixed
Top packages  : ssl-001sites-tier1
Champion      : ssl-001sites-tier1 → catalog resolution pending (known SSL offer family: 28e5b730 or bb0afea9)
Volume        : 231 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DV = Domain Validated SSL (entry-level SSL cert). ssl-001sites-tier1 is an NES package with 93% of orders. Strongly NES-migrated surface.

## [ITC] recore

Prefix group  : other
Human label   : Recore — Domain Registration (Internal Recore Flow)
Page source   : not mapped
Products      : Domain Name Registration 94% (domain NES 82%, domain-bundle NES 5%, NULL CES 6%), Domain Ownership Protection 3%, Aftermarket Non-Retail 2%, Domain Marketplace 1%, Domain Name Premium 1%
NES/CES       : Mixed
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (Rev 3); domain-bundle → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1)
Volume        : 223 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Single-word ITC with no prefix separator. "recore" likely = a core renewal/reactivation registration flow. Similar product mix to transferin_dcc_searchdomain and gd_mcp_server.

## [ITC] mgr_slp_365_email

Prefix group  : other
Human label   : Manager — Microsoft 365 Email Sales Page
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 220 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mgr_ Manager M365 email-specific variant. Closely related to mgr_slp_365 (generic) and mgr_slp_365_email_config (configured variant).

## [ITC] upp_o365product_d2p_dcc_add-email-explore

Prefix group  : upp_
Human label   : UPP — M365 Add Email Explore via Domain Control Center
Page source   : not mapped
Products      : MS Office 365 90%, Conversations 6%, Value Adds 3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 219 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : add-email-explore = a discovery/explore mode for adding M365 email, accessed from DCC. Conversations co-purchase suggests email/communications bundle offer.

## [ITC] upp_conversationsproduct_p2p_conversations_renewal

Prefix group  : upp_
Human label   : UPP — Conversations Product Peer-to-Peer Renewal
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 218 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dlp_multi_site_setup

Prefix group  : dlp_
Human label   : Domain Landing Page — Multi-Site SSL Setup Service
Page source   : not mapped
Products      : SSL 100% (multi-unit-ssl-setup-service NES 98%, ssl-setup-service-5site NES 1%, ssl-setup-service-10site NES 1%)
NES/CES       : NES
Top packages  : multi-unit-ssl-setup-service, ssl-setup-service-5site, ssl-setup-service-10site
Champion      : catalog resolution pending (multi-unit SSL setup service packages)
Volume        : 218 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Multi-unit SSL setup service = a managed SSL installation service covering multiple sites. All NES packages. Driven from domain landing pages.

## [ITC] dlp_m365oybo

Prefix group  : dlp_
Human label   : Domain Landing Page — M365 OYBO (Own Your Brand Offer)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 218 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : oybo = "Own Your Brand Offer" — a domain+M365 bundle concept presented on domain landing pages. CES despite oybo branding.

## [ITC] slp-boost

Prefix group  : other
Human label   : Front of Site — Boost / Paid Support Sales Page (Multi-Product)
Page source   : not mapped
Products      : Paid Support 66%, Grid 11%, Open XChange 9%, Strategic Partnerships AC 5%, Website Builder 4%, WordPress Managed Plans 3%, Professional Web Services 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 213 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Uses hyphen (slp-boost) not underscore — atypical ITC format. Paid Support is the dominant product (66%). "Boost" likely refers to GoDaddy's SEO/visibility boost services (now Paid Support category).

## [ITC] mgr_dify_attach

Prefix group  : other
Human label   : Manager — DIFY Social Attach
Page source   : not mapped
Products      : DIFY Social 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 210 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : DIFY = "Do It For You" — GoDaddy's managed social media marketing service. mgr_ = Manager. "attach" = product attachment/add-on flow. Compare to dify_attach and dify-attach ITCs (same product, different flow origins).

## [ITC] app_ox_renew_inpanel_suspendedaccount

Prefix group  : other
Human label   : In-App — OX / M365 Renewal for Suspended Account (In-Panel)
Page source   : not mapped
Products      : MS Office 365 58%, Open XChange 31%, Value Adds 10%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 210 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Renewal flow for suspended email accounts (OX or M365). M365 majority (58%) despite ox_ prefix — likely serves both OX legacy and M365 accounts. In-panel = within the email control panel.

## [ITC] upp_dopproduct_d2p_websites_pandc.vnext.editor_pub

Prefix group  : upp_
Human label   : UPP — DOP via Websites Plan & Create vNext Editor (Published)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 207 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug contains dots (pandc.vnext.editor_pub). pandc = Plan & Create editor; vnext = next-gen WAM; editor_pub = published/live editor state. DOP upsell from within the published website editor.

## [ITC] gd_mcp_server

Prefix group  : other
Human label   : GoDaddy MCP Server — AI-Assisted Domain Registration
Page source   : not mapped
Products      : Domain Name Registration 97% (domain NES 83%, domain-bundle NES 2%, NULL CES 11%), Domain Ownership Protection 3%
NES/CES       : Mixed
Top packages  : domain, domain-bundle
Champion      : domain → edf13c43 (Rev 3); domain-bundle → edf13c43 (Rev 3)
Volume        : 206 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : gd_mcp_server = purchases originating from GoDaddy's MCP (Model Context Protocol) server integration. These are AI assistant-initiated domain purchases (e.g., via Claude Code or similar AI tools using GoDaddy's MCP). Confirms real production usage of the MCP server driving NES domain orders.

## [ITC] mgr_slp_email_archiving_config

Prefix group  : other
Human label   : Manager — Email Archiving Configuration Sales Page (M365 Add-On)
Page source   : not mapped
Products      : Value Adds 63%, MS Office 365 37%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 204 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Email archiving = M365 compliance/archiving add-on. Value Adds (63%) is the dominant product — archiving add-ons classify under Value Adds. Compare to mgr_slp_email_encryption_config (similar pattern for encryption add-on).

## [ITC] studio_android_domain_renewal_homepage

Prefix group  : other
Human label   : GoDaddy Studio Android — Domain Renewal Homepage
Page source   : not mapped
Products      : Domain Name Registration 95%, Domain Ownership Protection 5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 186 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : studio_ prefix = GoDaddy Studio app. Android homepage renewal flow — CES (no NES packages), unlike studio_android_search_recommendation which had some NES domain orders.


## [ITC] drp-cluster

Prefix group  : other
Human label   : Domain Ownership Protection renewal cluster (DRP)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 186 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Non-standard prefix; DRP = Domain Registration/Renewal Protection cluster surface

## [ITC] mgr_slp_email_encryption

Prefix group  : mgr_
Human label   : Manager redirect to Email Encryption sales page
Page source   : not mapped
Products      : Value Adds 65%, MS Office 365 35%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 186 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_portfolio_domain_search_recommendation

Prefix group  : dcc_
Human label   : DCC portfolio domain search recommendation panel
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 182 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_dopupgrade_wf1025923

Prefix group  : dcc_
Human label   : DCC Domain Ownership Protection upgrade flow (workflow 1025923)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 175 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug contains workflow ticket ID (wf1025923) — created for a specific experiment or feature flag

## [ITC] upp_titanproduct_d2p_vnext-dashboard_venture_email

Prefix group  : upp_
Human label   : UPP Titan Email new purchase from Venture dashboard
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 170 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=titanproduct, conversion=d2p, app=vnext-dashboard, entry=venture_email; slug exactly 50 chars — may be truncated

## [ITC] upp_wamproduct_f2p_airo-sentinel_upgrade

Prefix group  : upp_
Human label   : UPP WAM free-to-paid upgrade triggered from Airo Sentinel
Page source   : not mapped
Products      : Websites and Marketing 84%, MS Office 365 16%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 161 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=wamproduct, conversion=f2p, app=airo-sentinel, entry=upgrade

## [ITC] slp_hubmaintenancepack

Prefix group  : slp_
Human label   : Hub Maintenance Pack sales page (professional site maintenance plans)
Page source   : not mapped
Products      : Paid Support 100%
NES/CES       : NES
Top packages  : sitemaintenance-005sites, sitemaintenance-050sites, sitemaintenance-100sites
Champion      : catalog resolution pending
Volume        : 161 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_cart_xsells_inline

Prefix group  : mgr_
Human label   : Manager redirect to cart inline cross-sell
Page source   : not mapped
Products      : MS Office 365 38%, Vendor Email 34%, Value Adds 26%, SSL 1%, Virtual Hosting 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 159 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_security_category

Prefix group  : slp_
Human label   : Security category sales landing page (SSL + website protection bundles)
Page source   : not mapped
Products      : SSL 60%, Website Protection 22%, Strategic Partnerships AC (Norton) 18%
NES/CES       : Mixed
Top packages  : ssl-001sites-tier1, ssl-001sites-tier3, ssl-wildcard-tier1
Champion      : catalog resolution pending
Volume        : 156 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_app-builder-nes_upp_airo_ai_builder_upgrad

Prefix group  : upp_
Human label   : UPP Airo AI Builder paid-to-paid upgrade from App Builder NES entry point
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 155 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v2: conversion=p2p, app=app-builder-nes, overrideItc=upp_airo_ai_builder_upgrad (truncated); slug 50 chars

## [ITC] slp_premiumdns

Prefix group  : slp_
Human label   : Premium DNS sales page
Page source   : not mapped
Products      : Premium DNS 100%
NES/CES       : NES
Top packages  : dns-tier1
Champion      : catalog resolution pending
Volume        : 153 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_cat_manager

Prefix group  : mgr_
Human label   : Manager catalog manager — website restore and care packages
Page source   : not mapped
Products      : Grid (website care) 76%, WordPress Managed Plans 16%, Professional Web Services 7%, cPanel Business Hosting 1%
NES/CES       : NES
Top packages  : restore-wordpressdesign-websitecare-tier2, restore-webstoredesign-wordpress-websitecare-tier1, restore-wordpressdesign-websitecare-tier3
Champion      : catalog resolution pending
Volume        : 152 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_wsb_ft_getstarted_plans_nocc

Prefix group  : slp_
Human label   : WAM website builder free trial get-started plans (no credit card required)
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : Mixed
Top packages  : wsb-vnext-tier1
Champion      : wsb-vnext-tier1 → ea9e918c (from prior catalog resolution)
Volume        : 150 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : nocc = no credit card required; 55% NES (wsb-vnext-tier1), 45% CES (NULL package)

## [ITC] dcc_dns_hosting_transfer_in

Prefix group  : dcc_
Human label   : DCC DNS and hosting transfer in (domain transfer from external registrar)
Page source   : not mapped
Products      : Domain Name Transfer 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 142 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_test-itc

Prefix group  : mgr_
Human label   : Manager test ITC (QA/staging surface code with production order leakage)
Page source   : not mapped
Products      : Miscellaneous Fees and Other 74%, SSL 26%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 139 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC name indicates test/QA usage; real production orders imply test code leaked into production tracking

## [ITC] slp_ssl_ev

Prefix group  : slp_
Human label   : SSL Extended Validation (EV) sales page
Page source   : not mapped
Products      : SSL 100%
NES/CES       : Mixed
Top packages  : ssl-001sites-tier3
Champion      : catalog resolution pending
Volume        : 138 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : tier3 = EV (Extended Validation); 88% NES, 12% CES null; SSL tier convention: tier1=DV, tier2=OV, tier3=EV

## [ITC] myproducts-domain-search-recommendations

Prefix group  : other
Human label   : My Products page domain search recommendations
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 137 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Non-standard prefix (myproducts-); in-account product management surface

## [ITC] upp_d2p_venture_discover_tile_email

Prefix group  : upp_
Human label   : UPP new purchase from Venture dashboard discover tile (email product)
Page source   : not mapped
Products      : MS Office 365 94%, Value Adds 5%, Conversations 2%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 131 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v2: conversion=d2p, entry_point=venture_discover_tile_email

## [ITC] dlp_web_hosting

Prefix group  : dlp_
Human label   : Web hosting domain landing page (cPanel hosting bundles with email and SSL)
Page source   : not mapped
Products      : MS Office 365 36%, SSL 34%, CnP Hosting 21%, Vendor Email 8%
NES/CES       : Mixed
Top packages  : cpanel-openexchange-tier3, cpanel-o365-tier3, cpanel-set-2-ultimate-365-xtra
Champion      : catalog resolution pending
Volume        : 129 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_ssl_san

Prefix group  : slp_
Human label   : SSL SAN (Subject Alternative Name / multi-site) sales page
Page source   : not mapped
Products      : SSL 100%
NES/CES       : NES
Top packages  : ssl-005sites-tier1
Champion      : catalog resolution pending
Volume        : 125 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : SAN = Subject Alternative Name; ssl-005sites = 5-site certificate

## [ITC] plp_domain_whois

Prefix group  : other
Human label   : Domain WHOIS product landing page
Page source   : not mapped
Products      : Domain Name Registration 98%, Domain Ownership Protection 2%
NES/CES       : Mixed
Top packages  : domain, domain-bundle
Champion      : domain → edf13c43 (Rev 3)
Volume        : 124 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : plp_ = Product Landing Page; domain NES 55%, domain-bundle NES 3%, NULL CES 28%

## [ITC] app_ox_adduser_buymoreaccounts_dcc_portfolio_setti

Prefix group  : app_
Human label   : In-app OpenExchange email add user / buy more accounts from DCC portfolio settings
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 120 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated at 50 chars; full ITC likely ends with "...dcc_portfolio_settings"

## [ITC] upp_conversationsproduct_p2p_account_renewals

Prefix group  : upp_
Human label   : UPP Conversations renewal (paid-to-paid account renewals)
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 118 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=conversationsproduct, conversion=p2p, app=account, entry=renewals

## [ITC] 123reg_titan_pro

Prefix group  : other
Human label   : 123-Reg UK partner — Titan Pro email purchase
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 118 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123reg_ prefix = UK partner brand 123-Reg; Titan Pro = professional Titan Email tier

## [ITC] upp_dopproduct_combo_p2p_airo-sentinel_upgrade_upp

Prefix group  : upp_
Human label   : UPP Domain Ownership Protection combo paid-to-paid upgrade from Airo Sentinel
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 115 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=dopproduct_combo, conversion=p2p, app=airo-sentinel, entry=upgrade; slug truncated at 50 chars (overrideItc cut off)

## [ITC] dcc_portfolio_alt_tld_domain_up_sell

Prefix group  : dcc_
Human label   : DCC portfolio alternate TLD domain upsell
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 114 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_domsettings_xgrade_activity_log_a

Prefix group  : dcc_
Human label   : DCC domain settings upgrade CTA from activity log
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 113 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Slug truncated at 50 chars

## [ITC] 123reg_slp_ssl

Prefix group  : other
Human label   : 123-Reg UK partner — SSL sales page
Page source   : not mapped
Products      : SSL 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 111 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 123reg_ prefix = UK partner brand 123-Reg

## [ITC] slp_ssl_ov

Prefix group  : slp_
Human label   : SSL Organization Validation (OV) sales page
Page source   : not mapped
Products      : SSL 100%
NES/CES       : NES
Top packages  : ssl-001sites-tier2
Champion      : catalog resolution pending
Volume        : 111 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : OV = Organization Validation; tier2 in SSL naming convention (tier1=DV, tier2=OV, tier3=EV)

## [ITC] dpp_absol1.namebuilder

Prefix group  : dpp_
Human label   : Domain checkout absolute search — name builder suggestions
Page source   : not mapped
Products      : Domain Name Registration 97%, Domain Ownership Protection 3%
NES/CES       : Mixed
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 108 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 66% NES (domain package), 31% CES (NULL); namebuilder = AI-assisted domain name suggestion variant

## [ITC] upp_d2p_gai.vh.dashboard.logoassistant

Prefix group  : upp_
Human label   : UPP new purchase from VH/Venture dashboard logo assistant (Airo)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 108 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v2: conversion=d2p, entry_point=gai.vh.dashboard.logoassistant; gai = generative AI; entry contains dotted path notation

## [ITC] slp_wsb_ft_nocc&ref=slp_trusted

Prefix group  : slp_
Human label   : WAM website builder free trial no-CC (URL referral param leaked into ITC)
Page source   : not mapped
Products      : Websites and Marketing 61%, Vendor Email 39%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 107 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : URL query parameter &ref=slp_trusted leaked into ITC string at tracking time; functionally same surface as slp_wsb_ft_nocc

## [ITC] mgr_slp_wsb_ft_getstarted_plans_nocc

Prefix group  : mgr_
Human label   : Manager redirect to WAM free-trial get-started plans (no credit card)
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 105 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_default_p2p_account_myproducts_accordion

Prefix group  : upp_
Human label   : UPP default paid-to-paid from My Products accordion panel
Page source   : not mapped
Products      : WordPress Managed Plans 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 103 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v2: conversion=p2p, app=account, entry=myproducts_accordion; "default" = no product-specific override

## [ITC] android_studio_app_createshelf_domains

Prefix group  : other
Human label   : GoDaddy Studio Android app — create shelf domain purchase
Page source   : not mapped
Products      : Domain Name Registration 99%, Domain Ownership Protection 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 102 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : android_ prefix = Android mobile app surface (GoDaddy Studio)

## [ITC] dcc_dns_mgmt_xgrade

Prefix group  : dcc_
Human label   : DCC DNS management upgrade (DOP upsell from DNS settings)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 97 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_airobuilderproduct_d2p_airo-builder_pricing_se

Prefix group  : upp_
Human label   : UPP Airo Builder new purchase from Airo Builder pricing page
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 95 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=airobuilderproduct, conversion=d2p, app=airo-builder, entry=pricing_se (truncated at 50 chars)

## [ITC] slp_conversations

Prefix group  : slp_
Human label   : GoDaddy Conversations (SmartLine) sales landing page
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : Mixed
Top packages  : nes-conversationsessentialsfreetrial
Champion      : catalog resolution pending
Volume        : 93 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 95% CES (NULL), 5% NES (nes-conversationsessentialsfreetrial free trial); primarily CES surface

## [ITC] dcc_whois_domainpurchase

Prefix group  : dcc_
Human label   : DCC WHOIS domain purchase (buying domains from WHOIS lookup in DCC)
Page source   : not mapped
Products      : Domain Marketplace 50%, Domain Name Premium 29%, Domain Name Transfer 21%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 92 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_activity_log_dotnet_banner

Prefix group  : dcc_
Human label   : DCC activity log .NET domain registration banner
Page source   : not mapped
Products      : Domain Name Registration 94%, Domain Ownership Protection 5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 91 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_email_upgrade-downgrade

Prefix group  : upp_
Human label   : UPP WAM paid-to-paid email upgrade or downgrade
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 89 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=wamproduct, conversion=p2p, app=email, entry=upgrade-downgrade

## [ITC] tdfs_pricerequest

Prefix group  : other
Human label   : Third-party domain fulfillment service — price request
Page source   : not mapped
Products      : Domain Marketplace 52%, Domain Name Premium 26%, Domain Name Transfer 22%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 88 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : tdfs_ = third-party domain fulfillment service (aftermarket/Afternic partner channel)

## [ITC] app_mwphui_domainattach_domainpurchase

Prefix group  : app_
Human label   : In-app MWP HUI domain attach — domain purchase flow
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 86 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : mwphui = Managed WordPress Hosting UI; domain attach flow when setting up a new WordPress site

## [ITC] upp_o365product_d2p_sites_m365wamspuredirect

Prefix group  : upp_
Human label   : UPP M365 new purchase from Sites (WAM/M365 pure-direct flow)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 85 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=o365product, conversion=d2p, app=sites, entry=m365wamspuredirect

## [ITC] mya_dom_srch.regpremium_alternate

Prefix group  : mya_
Human label   : My Account domain search — registered premium alternate domain suggestions
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 83 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : 27% NES (domain package), 71% CES (NULL), 2% DOP; regpremium = registered premium domain category

## [ITC] whois_domainpurchase

Prefix group  : other
Human label   : WHOIS domain purchase (buying domain from public WHOIS lookup results)
Page source   : not mapped
Products      : Domain Marketplace 51%, Domain Name Transfer 25%, Domain Name Premium 25%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 81 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : whois_ prefix = standalone WHOIS tool surface (not DCC-specific)

## [ITC] upp_airoplusproduct_d2p_dashboard_airopluswam

Prefix group  : upp_
Human label   : UPP Airo+ new purchase from dashboard (Airo + WAM bundle)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 81 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : UPP v1: product=airoplusproduct (Airo+WAM bundle), conversion=d2p, app=dashboard, entry=airopluswam; airoplusproduct not in standard product enum — newer combo product

## [ITC] am_gdcart_afternicfos_bin

Prefix group  : other
Human label   : Aftermarket GoDaddy cart — Afternic front of site Buy It Now
Page source   : not mapped
Products      : Domain Marketplace 53%, Domain Name Transfer 41%, Domain Name Premium 6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 79 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : am_ = Aftermarket/Afternic; gdcart = GoDaddy cart; FOS = front of site; BIN = Buy It Now price

## [ITC] dcc_domsettings_xgrade_drp_tab_activity_log

Prefix group  : dcc_
Human label   : DCC domain settings upgrade from DRP tab activity log
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 77 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_email_backup_config

Prefix group  : mgr_
Human label   : Manager redirect to Email Backup sales page (config variant)
Page source   : not mapped
Products      : MS Office 365 53%, Value Adds 47%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 74 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_sapi_config

Prefix group  : slp
Human label   : SAPI configuration sales landing page (shared hosting / SSL bundle)
Page source   : not mapped
Products      : Virtual Hosting 50%, SSL 36%, CnP Hosting 11%, Open XChange 3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 73 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] app_o365_upgrade_default_vnext-dashboard

Prefix group  : app
Human label   : In-app Microsoft 365 default upgrade (vnext dashboard)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 72 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_portfolio_table_stack_bundle

Prefix group  : dcc
Human label   : Domain Control Center portfolio table stack bundle
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 72 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] airohq.domain_search.chat

Prefix group  : other
Human label   : Airo HQ chat-based domain search
Page source   : not mapped
Products      : Domain Name Registration 71%, Domain Ownership Protection 29%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 69 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] wp_pro_card

Prefix group  : other
Human label   : WordPress Pro card (multi-product cross-sell)
Page source   : not mapped
Products      : Domain Name Registration 54%, WordPress Managed Plans 16%, MS Office 365 9%, CnP Hosting 7%, Websites and Marketing 6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 69 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_conversationsproduct_d2p_account_conversations

Prefix group  : upp
Human label   : UPP Conversations product direct-to-paid from account screen
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 68 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] test-itc

Prefix group  : other
Human label   : QA test tracking code (leaked into production)
Page source   : not mapped
Products      : SSL 76%, Miscellaneous Fees 22%, Domain Name Registration 1%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 68 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : QA/staging ITC with real production orders; disregard for offer analysis

## [ITC] upp_p2p_app-builder-nes_notifications_bell

Prefix group  : upp
Human label   : UPP paid-to-paid Airo builder NES upgrade via notifications bell
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 68 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_dashboard_vh_buildwebsite_upp_web_hosting

Prefix group  : upp
Human label   : UPP direct-to-paid web hosting from VH dashboard build website flow
Page source   : not mapped
Products      : CnP Hosting 88%, WordPress Managed Plans 12%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 66 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dlp_cheapdomain_godaddy_b.primary_exact

Prefix group  : dlp
Human label   : Cheap domain landing page — GoDaddy brand primary exact match variant
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 65 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_o365product_d2p_panel-lite_uep_vnext-dashboard

Prefix group  : upp
Human label   : UPP M365 product direct-to-paid from Panel Lite UEP (vnext dashboard)
Page source   : not mapped
Products      : MS Office 365 95%, Value Adds 5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 65 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] upp_d2p_genai.sentinel.airo-compliance

Prefix group  : upp
Human label   : UPP direct-to-paid Airo compliance purchase via Airo Sentinel GenAI
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 64 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] ios_studio_app_suggested_action_domain_search

Prefix group  : other
Human label   : iOS GoDaddy Studio app suggested action domain search
Page source   : not mapped
Products      : Domain Name Registration 97%, Domain Ownership Protection 2%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 64 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_app-builder-nes_upp_airo_ai_builder_publis

Prefix group  : upp
Human label   : UPP paid-to-paid Airo builder NES publish upgrade
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 64 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] side_search_whois_results

Prefix group  : other
Human label   : WHOIS results side panel domain search purchase
Page source   : not mapped
Products      : Domain Name Registration 94%, Domain Ownership Protection 6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 63 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] app_o365_adduser_buymoreaccounts_dcc_portfolio_set

Prefix group  : app
Human label   : In-app M365 add user buy more accounts from DCC portfolio settings
Page source   : not mapped
Products      : MS Office 365 90%, Value Adds 10%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 62 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] upp_d2p_add-email-explore

Prefix group  : upp
Human label   : UPP direct-to-paid email add explore flow
Page source   : not mapped
Products      : MS Office 365 93%, Value Adds 3%, Conversations 3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 61 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_gai.vnext.brand.imageassistant

Prefix group  : upp
Human label   : UPP direct-to-paid Airo brand image assistant (vnext)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 59 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] 123reg_titan_premium

Prefix group  : other
Human label   : 123 Reg UK partner — Titan Email Premium plan
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 59 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_logo

Prefix group  : mgr
Human label   : Manager redirect → logo design sales landing page
Page source   : not mapped
Products      : Professional Web Services 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 59 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dna_invapp_watchlist_android_expirycloseout

Prefix group  : dna
Human label   : GoDaddy Domain Auctions Android app watchlist expiry closeout purchase
Page source   : not mapped
Products      : Aftermarket Non-Retail 66%, Domain Name Auction 34%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 58 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mob_df_ios_domain_search

Prefix group  : other
Human label   : Mobile domain finder iOS domain search
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 52 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_websites_upgrade-downgrade

Prefix group  : upp
Human label   : UPP WAM paid-to-paid websites upgrade/downgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 62%, MS Office 365 38%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 52 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_dcc.portfolio.standalone.spu

Prefix group  : upp
Human label   : UPP direct-to-paid Domain Ownership Protection standalone purchase from DCC portfolio
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 51 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] ind_airo_domain_transfer_agent_transfer_in_domain

Prefix group  : other
Human label   : Agent-assisted Airo domain transfer-in purchase
Page source   : not mapped
Products      : Domain Name Transfer 84%, Domain Ownership Protection 16%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 51 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ind_ prefix = independent/agent-assisted flows

## [ITC] dcc_valuationpage_xgrade_ownershipprotection_a

Prefix group  : dcc
Human label   : Domain Control Center valuation page cross-grade to Domain Ownership Protection (variant A)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 50 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_webhostingproduct_d2p_dashboard_uep_vh_buildwe

Prefix group  : upp
Human label   : UPP web hosting product direct-to-paid from dashboard UEP VH build website flow
Page source   : not mapped
Products      : CnP Hosting 76%, WordPress Managed Plans 24%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 50 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated; v1 UPP format

## [ITC] upp_airoplusproduct_d2p_start_airopluswam

Prefix group  : upp
Human label   : UPP Airo Plus product direct-to-paid from start screen (Airo Plus + WAM bundle)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 50 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_app-builder-nes_build_for_free

Prefix group  : upp
Human label   : UPP paid-to-paid Airo builder NES build-for-free upgrade
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 49 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_airoaibuilder

Prefix group  : slp
Human label   : Airo AI builder sales landing page
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 47 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_conversationstrialwam

Prefix group  : upp
Human label   : UPP direct-to-paid Conversations trial with WAM
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 47 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_ssl_san_config

Prefix group  : slp
Human label   : SSL SAN (multi-domain) certificate sales landing page — configuration view
Page source   : not mapped
Products      : SSL 89%, Strategic Partnerships AC 11%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 47 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_managed

Prefix group  : slp
Human label   : Managed SSL wildcard certificate sales landing page
Page source   : not mapped
Products      : SSL 100%
NES/CES       : NES
Top packages  : ssl-wildcard-managed-tier1
Champion      : catalog resolution pending
Volume        : 46 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] airohq.domain_search.hero

Prefix group  : other
Human label   : Airo HQ hero section domain search
Page source   : not mapped
Products      : Domain Name Registration 76%, Domain Ownership Protection 24%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 45 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_ola_upgrade-downgrade

Prefix group  : upp
Human label   : UPP WAM paid-to-paid OLA upgrade/downgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 65%, MS Office 365 35%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 43 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] airo_ai_builder_attach_domain

Prefix group  : other
Human label   : Airo AI builder domain attachment purchase
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain, domain-bundle
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 42 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_dlp_multi_site_setup

Prefix group  : mgr
Human label   : Manager redirect → multi-site setup domain landing page (SSL)
Page source   : not mapped
Products      : SSL 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 42 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_activation_email

Prefix group  : dcc
Human label   : Domain Control Center email service activation purchase
Page source   : not mapped
Products      : Open XChange 52%, MS Office 365 43%, Websites and Marketing 5%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 42 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_o365product_d2p_account_m365wamspuredirect

Prefix group  : upp
Human label   : UPP M365 product direct-to-paid from account screen (M365 WAM pure direct, v1 format)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 42 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dlp_wordpress

Prefix group  : dlp
Human label   : WordPress domain landing page — NES WordPress bundle purchase
Page source   : not mapped
Products      : MS Office 365 48%, WordPress Managed Plans 33%, Vendor Email 10%, other 9%
NES/CES       : Mixed
Top packages  : wordpress-o365-forever-ssl-deluxe, wordpress-o365-forever-ssl-basic, wordpress-openexchange-forever-ssl-basic
Champion      : catalog resolution pending
Volume        : 41 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] app_mwphui_domains_domainspg

Prefix group  : app
Human label   : In-app MWP HUI domains page domain purchase
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 38 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] app_ox_adduser_buymoreaccounts_mya_domain_manager_

Prefix group  : app
Human label   : In-app OX add user buy more accounts from My Account domain manager
Page source   : not mapped
Products      : Open XChange 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 38 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] dcc_portfolio_recommended_domains

Prefix group  : dcc
Human label   : Domain Control Center portfolio recommended domains upsell
Page source   : not mapped
Products      : Domain Name Registration 92%, Domain Ownership Protection 8%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 38 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_account_myproducts_accordion

Prefix group  : upp
Human label   : UPP WAM paid-to-paid from account my products accordion (v1 format)
Page source   : not mapped
Products      : Strategic Partnerships AC 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 37 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] digital_marketing_suite_deluxe

Prefix group  : other
Human label   : Digital Marketing Suite Deluxe (WAM-based)
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 37 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_managedwordpressproduct_d2p_dashboard_uep_vh_b

Prefix group  : upp
Human label   : UPP MWP product direct-to-paid from dashboard UEP VH build flow
Page source   : not mapped
Products      : WordPress Managed Plans 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 36 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated; v1 UPP format

## [ITC] upp_default_p2p_account_addon-update

Prefix group  : upp
Human label   : UPP default paid-to-paid account add-on update
Page source   : not mapped
Products      : WordPress Managed Plans 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 36 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_start

Prefix group  : upp
Human label   : UPP direct-to-paid start screen (M365 / Airo / Conversations)
Page source   : not mapped
Products      : MS Office 365 64%, Airo 28%, Conversations 8%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 36 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] am_gdcart_selfbrokerage

Prefix group  : am
Human label   : GoDaddy Aftermarket self-brokerage cart
Page source   : not mapped
Products      : Domain Marketplace 51%, Domain Name Transfer 26%, Domain Name Premium 23%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_email_encryption_config

Prefix group  : slp
Human label   : Email encryption sales landing page — configuration view
Page source   : not mapped
Products      : MS Office 365 51%, Value Adds 49%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15


## [ITC] upp_p2p_usage_gauge.buy_credits_upp_airo_ai_builde

Prefix group  : upp
Human label   : UPP paid-to-paid Airo AI builder credit purchase via usage gauge
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] slp_airo_plus

Prefix group  : slp
Human label   : Airo Plus sales landing page
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dlp_365_office_config

Prefix group  : dlp
Human label   : Microsoft 365 domain landing page — configuration view
Page source   : not mapped
Products      : MS Office 365 86%, Value Adds 9%, Strategic Partnerships AC 6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dcc_manage_website_activation

Prefix group  : dcc
Human label   : Domain Control Center manage website activation
Page source   : not mapped
Products      : Websites and Marketing 80%, CnP Hosting 9%, SSL 9%, Open XChange 3%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 35 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_dopproduct_ultimate_p2p_airo-sentinel_upgrade_

Prefix group  : upp
Human label   : UPP DOP Ultimate paid-to-paid Airo Sentinel upgrade (v1 format)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 34 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] slp_logo

Prefix group  : slp
Human label   : Logo design sales landing page
Page source   : not mapped
Products      : Professional Web Services 100%
NES/CES       : NES
Top packages  : logodesign_tier2_012mo, logodesign-tier2
Champion      : catalog resolution pending
Volume        : 34 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_conversationsproduct_d2p_start_conversationstr

Prefix group  : upp
Human label   : UPP Conversations product direct-to-paid from start screen (v1 format)
Page source   : not mapped
Products      : Conversations 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 34 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] plp_ecommerce_bundle

Prefix group  : plp
Human label   : Product landing page — e-commerce bundle
Page source   : not mapped
Products      : Domain Ownership Protection 25%, Websites and Marketing 25%, Domain Name Registration 25%, MS Office 365 25%
NES/CES       : Mixed
Top packages  : dpp-uk-com-solution-tier3
Champion      : catalog resolution pending
Volume        : 32 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] 123reg_slp_vps

Prefix group  : other
Human label   : 123 Reg UK partner — VPS hosting sales landing page
Page source   : not mapped
Products      : Virtual Hosting 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 32 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_wds_start_plan

Prefix group  : mgr
Human label   : Manager redirect → WDS start plan sales landing page (web / professional services)
Page source   : not mapped
Products      : Professional Web Services 55%, Websites and Marketing 45%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 31 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_dashboard_upgrade-downgrade

Prefix group  : upp
Human label   : UPP WAM paid-to-paid dashboard upgrade/downgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 90%, Strategic Partnerships AC 10%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 30 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] studio_android_domain_ideasforyou

Prefix group  : other
Human label   : GoDaddy Studio Android app ideas for you domain search
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 30 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_dopproduct_standalone_p2p_airo-sentinel_upgrad

Prefix group  : upp
Human label   : UPP DOP standalone paid-to-paid Airo Sentinel upgrade (v1 format)
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 29 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] upp_p2p_myproducts_accordion

Prefix group  : upp
Human label   : UPP paid-to-paid my products accordion upgrade
Page source   : not mapped
Products      : WordPress Managed Plans 76%, Strategic Partnerships AC 24%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 29 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_norton_smb

Prefix group  : slp
Human label   : Norton SMB security sales landing page
Page source   : not mapped
Products      : Strategic Partnerships AC 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 29 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_vps4_fully_config

Prefix group  : mgr
Human label   : Manager redirect → VPS4 fully managed hosting sales landing page — configuration view
Page source   : not mapped
Products      : Virtual Hosting 54%, SSL 32%, Website Protection 14%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 28 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] airo_ai_builder_domain_purchase

Prefix group  : other
Human label   : Airo AI builder domain purchase
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 28 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_o365product_p2p_productivity_renewals

Prefix group  : upp
Human label   : UPP M365 paid-to-paid productivity renewals (Vendor Email / Titan, v1 format)
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 28 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_ssl_san_config

Prefix group  : mgr
Human label   : Manager redirect → SSL SAN certificate sales landing page — configuration view
Page source   : not mapped
Products      : SSL 63%, Strategic Partnerships AC 37%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 27 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] 123reg_titan_ultra

Prefix group  : other
Human label   : 123 Reg UK partner — Titan Email Ultra plan
Page source   : not mapped
Products      : Vendor Email 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 27 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_cashpark01

Prefix group  : slp
Human label   : Cash parking domain monetization sales landing page (variant 01)
Page source   : not mapped
Products      : Aftermarket Non-Retail 48%, Cashparking 44%, Aftermarket Non-Retail null 7%
NES/CES       : Mixed
Top packages  : cashparking-tier2
Champion      : catalog resolution pending
Volume        : 27 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_ssl_managed_config

Prefix group  : slp
Human label   : Managed SSL certificate sales landing page — configuration view
Page source   : not mapped
Products      : Strategic Partnerships AC 85%, SSL 15%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 26 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_airobuilderproduct_f2p_account_upgrade

Prefix group  : upp
Human label   : UPP Airo builder product free-to-paid account upgrade (v1 format)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 25 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_na

Prefix group  : upp
Human label   : UPP WAM paid-to-paid Airo builder NES (v1 format)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 25 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] gdc_2_0_undefined

Prefix group  : other
Human label   : GoDaddy Connect 2.0 undefined entry point — domain purchase
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 25 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : undefined entry_point variant of gdc_2_0 surfaces; see also gdc_2_0_microsoft.com

## [ITC] dom_whois_dbs

Prefix group  : other
Human label   : Domain WHOIS Domain Backup Service purchase
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain, domain-bundle, dbs
Champion      : domain → edf13c43 (Rev 3); dbs → 0ce223ed (Rev 1)
Volume        : 25 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_budget_exceeded.buy_credits_notifications_

Prefix group  : upp
Human label   : UPP paid-to-paid Airo AI builder credit purchase (budget exceeded) via notifications
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 24 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] slp_email_archiving_config

Prefix group  : slp
Human label   : Email archiving sales landing page — configuration view
Page source   : not mapped
Products      : Value Adds 61%, MS Office 365 39%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 23 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_f2p_email_upgrade

Prefix group  : upp
Human label   : UPP WAM free-to-paid email upgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 87%, MS Office 365 13%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 23 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mob_gdm_android_domain_search

Prefix group  : other
Human label   : GoDaddy mobile Android domain search
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] tdfs_gdcustom_seo

Prefix group  : tdfs
Human label   : TDFS GoDaddy custom SEO domain marketplace
Page source   : not mapped
Products      : Domain Marketplace 68%, Domain Name Premium 23%, Domain Name Transfer 9%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_pandc.vnext.editor_publish_modal.successfu

Prefix group  : upp
Human label   : UPP direct-to-paid DOP from P&C vnext editor publish modal success
Page source   : not mapped
Products      : Domain Ownership Protection 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] hmc_dv_ssl_config

Prefix group  : other
Human label   : HMC DV SSL certificate configuration
Page source   : not mapped
Products      : SSL 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : hmc_ prefix = Hosting Management Console (legacy)

## [ITC] dpp_absol1.auction_tldcard

Prefix group  : dpp
Human label   : Domain Purchase Path — absolute search result auction TLD card
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_up

Prefix group  : upp
Human label   : UPP WAM paid-to-paid Airo builder NES upgrade (v1 format)
Page source   : not mapped
Products      : Airo 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] android_studio_app_suggested_action_domain_search

Prefix group  : other
Human label   : GoDaddy Studio Android app suggested action domain search
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 22 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mya_dom_srch.namebuilder

Prefix group  : mya
Human label   : My Account domain search — name builder results
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : Mixed
Top packages  : domain
Champion      : edf13c43 → catalog resolution pending (Rev 3)
Volume        : 21 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_ssl_ov_config

Prefix group  : slp
Human label   : SSL OV (Organization Validated) certificate sales landing page — configuration view
Page source   : not mapped
Products      : SSL 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 21 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_ssl_ov_config

Prefix group  : mgr
Human label   : Manager redirect → SSL OV certificate sales landing page — configuration view
Page source   : not mapped
Products      : SSL 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 20 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_account_site-renewals

Prefix group  : upp
Human label   : UPP WAM paid-to-paid account site renewals (v1 format)
Page source   : not mapped
Products      : Strategic Partnerships AC 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 20 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_d2p_panel-lite_hub

Prefix group  : upp
Human label   : UPP direct-to-paid Panel Lite hub (M365 / Conversations)
Page source   : not mapped
Products      : MS Office 365 80%, Value Adds 10%, Conversations 10%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 20 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dna_invapp_searchresults_android_expirycloseout

Prefix group  : dna
Human label   : GoDaddy Domain Auctions Android app search results expiry closeout purchase
Page source   : not mapped
Products      : Aftermarket Non-Retail 63%, Domain Name Auction 37%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 19 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] dlp_godaddy_registry

Prefix group  : dlp
Human label   : GoDaddy Registry domain landing page
Page source   : not mapped
Products      : Domain Name Registration 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 19 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_o365product_d2p_airo-sentinel_m365wamspuredire

Prefix group  : upp
Human label   : UPP M365 product direct-to-paid from Airo Sentinel (M365 WAM pure direct, v1 format)
Page source   : not mapped
Products      : MS Office 365 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 19 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : ITC is exactly 50 chars — likely truncated

## [ITC] slp_redeem

Prefix group  : slp
Human label   : GoDaddy gift card / credit redemption sales landing page
Page source   : not mapped
Products      : Domain Name Registration 44%, Websites and Marketing 44%, Domain Ownership Protection 11%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 18 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : Only package present is 'redemption' (ghost — excluded from NES classification); classified CES

## [ITC] tdfs_seo

Prefix group  : tdfs
Human label   : TDFS SEO domain marketplace
Page source   : not mapped
Products      : Domain Marketplace 50%, Domain Name Premium 33%, Domain Name Transfer 17%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 18 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_wsb_ft_nocc&ref=slp_trusted

Prefix group  : mgr
Human label   : Manager redirect → WSB free trial no credit card landing page (ref=slp_trusted variant)
Page source   : not mapped
Products      : Websites and Marketing 56%, Vendor Email 44%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 18 orders as of 2026-05-15 — Low
Explored      : 2026-05-15
Notes         : URL query param &ref=slp_trusted leaked into ITC string at tracking time; same surface as mgr_slp_wsb_ft_nocc

## [ITC] upp_wamproduct_f2p_instantpage_upgrade

Prefix group  : upp
Human label   : UPP WAM free-to-paid instant page upgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 18 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] digital_marketing_suite_essentials

Prefix group  : other
Human label   : Digital Marketing Suite Essentials (WAM-based)
Page source   : not mapped
Products      : Websites and Marketing 100%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 17 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_wamproduct_p2p_sites_upgrade-downgrade

Prefix group  : upp
Human label   : UPP WAM paid-to-paid sites upgrade/downgrade (v1 format)
Page source   : not mapped
Products      : Websites and Marketing 82%, Strategic Partnerships AC 12%, MS Office 365 6%
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 17 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] mgr_slp_email_archiving_config

Prefix group  : mgr
Human label   : Manager (reseller) mirror of email archiving add-on configuration landing page
Page source   : not mapped
Products      : Value Adds 63% (128 orders), MS Office 365 37% (76 orders)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 204 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] slp_ssl_dv_config

Prefix group  : slp
Human label   : SSL Domain Validation (DV) certificate configuration sales landing page
Page source   : not mapped
Products      : SSL 76% (13 orders), Strategic Partnerships AC 24% (4 orders)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 17 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] upp_p2p_app-builder-nes_nav_airo_airo_ai_builder

Prefix group  : upp
Human label   : Airo AI Builder upsell path — navigation surface within NES App Builder flow (paid-to-paid)
Page source   : not mapped
Products      : Airo 100% (16 orders)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 16 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] ios_studio_app_brandkit_domain_search

Prefix group  : other
Human label   : iOS Studio app — domain search initiated from the brand kit feature
Page source   : not mapped
Products      : Domain Name Registration 100% (16 orders)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 16 orders as of 2026-05-15 — Low
Explored      : 2026-05-15

## [ITC] llcfeature_getstarted

Prefix group  : other
Human label   : LLC feature get-started page — domain purchase entry point for LLC formation flow
Page source   : not mapped
Products      : Domain Name Registration 94% (15 orders), Aftermarket Non-Retail 6% (1 order)
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs (aftermarket)
Champion      : domain → edf13c43-7d39-4f90-aa81-b40666d51f75 (active, rev 3)
Volume        : 16 orders as of 2026-05-15 — Low
Explored      : 2026-05-15


## [ITC] slp_ssl_dv_config

Prefix group  : slp
Human label   : SSL Domain Validation Sales Page — Config variant
Page source   : not mapped
Products      : SSL, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 17 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_nav_airo_airo_ai_builder

Prefix group  : upp
Human label   : UPP — Airo AI Builder nav upsell (app-builder NES variant)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 16 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] ios_studio_app_brandkit_domain_search

Prefix group  : ios_studio
Human label   : GoDaddy Studio iOS — Brand Kit domain search
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 16 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] llcfeature_getstarted

Prefix group  : other
Human label   : LLC feature get-started flow — domain and domain bundle offers
Page source   : not mapped
Products      : Domain Name Registration, Aftermarket
NES/CES       : NES
Top packages  : domain, domain-bundle, dbs
Champion      : edf13c43 (domain/domain-bundle); 0ce223ed (dbs)
Volume        : 16 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_email_backup_config

Prefix group  : slp
Human label   : Email Backup Sales Page — Config variant
Page source   : not mapped
Products      : Microsoft 365, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 16 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_slp_airo_banner_airo_ai_bu

Prefix group  : upp
Human label   : UPP — Airo AI Builder SLP banner upsell (app-builder NES; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 15 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full ITC probably ends in _airo_ai_builder or similar

## [ITC] app_o365_upgrade_default_dcc_portfolio_settings_em

Prefix group  : app
Human label   : M365 in-app upgrade default — DCC Portfolio settings email (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 15 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _email_manage or similar

## [ITC] upp_o365product_d2p_panel-lite_uep_hub

Prefix group  : upp
Human label   : UPP — M365 upgrade from Panel-Lite UEP Hub entry point
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 15 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_websites_renewals

Prefix group  : upp
Human label   : UPP — WAM Websites renewals upsell
Page source   : not mapped
Products      : Websites and Marketing, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_d2p_panel-lite_cpanel

Prefix group  : upp
Human label   : UPP — Panel-Lite cPanel upgrade
Page source   : not mapped
Products      : Microsoft 365, Vendor Email, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_productivity_upgrade-downgrade

Prefix group  : upp
Human label   : UPP — WAM productivity upgrade/downgrade
Page source   : not mapped
Products      : Vendor Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] plp_domain_broker

Prefix group  : plp
Human label   : Domain Broker Product Listing Page
Page source   : not mapped
Products      : Aftermarket, Domain Name Registration, Domain Options and Protection
NES/CES       : NES
Top packages  : dbs, domain
Champion      : 0ce223ed (dbs); edf13c43 (domain)
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_d2p_as.dcc-protection-panel-agent.add_protecti

Prefix group  : upp
Human label   : UPP — DCC domain protection panel add-protection (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Domain Options and Protection
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _protection or similar

## [ITC] copilot_email

Prefix group  : other
Human label   : Microsoft Copilot email upsell flow
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : NES
Top packages  : office365-tier1, m365-officebusinessp1-aes
Champion      : catalog resolution pending
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_linkinbio

Prefix group  : slp
Human label   : Link in Bio Sales Landing Page
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_planner

Prefix group  : slp
Human label   : Microsoft Planner / M365 Sales Landing Page
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : NES
Top packages  : office365-tier0
Champion      : catalog resolution pending
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] copilot_email_config

Prefix group  : other
Human label   : Microsoft Copilot email config flow
Page source   : not mapped
Products      : Microsoft 365, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 14 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_vps_upgrade_resources

Prefix group  : app
Human label   : VPS in-app upgrade resources
Page source   : not mapped
Products      : Virtual Hosting
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 13 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain

Prefix group  : dlp
Human label   : Cheap Domain Landing Page
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : NES
Top packages  : domain, domain-bundle
Champion      : edf13c43
Volume        : 13 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_nav_website_menu_airo_ai_b

Prefix group  : upp
Human label   : UPP — Airo AI Builder nav website menu upsell (app-builder NES; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 13 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _airo_ai_builder or similar

## [ITC] 123reg_slp_premiumhosting

Prefix group  : 123reg
Human label   : 123 Reg Premium Hosting Sales Page (UK partner surface)
Page source   : not mapped
Products      : cPanel Business Hosting, Vendor Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_build_for_free

Prefix group  : upp
Human label   : UPP — Airo buy credits (build for free, manage plan variant)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : Product data inferred from naming pattern; not returned in product profile queries

## [ITC] upp_d2p_productivity_add_user

Prefix group  : upp
Human label   : UPP — M365 productivity add user
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_auoybo

Prefix group  : slp
Human label   : Australia / UK Own Your Brand Online (OYBO) Sales Landing Page
Page source   : not mapped
Products      : Microsoft 365, Domain Name Registration
NES/CES       : NES
Top packages  : oybo-au-email, oybo-uk-email
Champion      : catalog resolution pending
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_account_mya_acctsettings_subscript

Prefix group  : upp
Human label   : UPP — My Account settings subscriptions default upsell (ITC truncated at 50 chars)
Page source   : not mapped
Products      : WordPress Managed Plans
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _subscriptions or similar

## [ITC] android_studio_app_brandkit_domain_search

Prefix group  : android_studio
Human label   : GoDaddy Studio Android — Brand Kit domain search
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] airohq.domain_search.spin

Prefix group  : airohq
Human label   : Airo HQ in-product — domain search spin/TLD carousel
Page source   : not mapped
Products      : Domain Name Registration, Domain Options and Protection
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_build_for_free

Prefix group  : upp
Human label   : UPP — Airo buy credits (build for free, budget exceeded; ITC at 50-char limit)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 12 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is exactly 50 chars — may be complete or truncated; consistent with other buy_credits_* ITCs

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_no

Prefix group  : upp
Human label   : UPP — WAM Airo Builder app-builder NES upsell (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 11 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix unknown

## [ITC] upp_d2p_airopluswam

Prefix group  : upp
Human label   : UPP — Airo Plus WAM upgrade (direct-to-purchase)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 11 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_dpp_gc_merchandise

Prefix group  : app
Human label   : Open XChange in-app add user — DPP GC merchandise (buy more accounts)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 10 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] matching_domains

Prefix group  : other
Human label   : Matching domains recommendation surface
Page source   : not mapped
Products      : Domain Name Registration, Domain Options and Protection
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 10 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_slp_cashpark01

Prefix group  : mgr
Human label   : Manager redirect → Cashparking Sales Landing Page
Page source   : not mapped
Products      : Cashparking, Aftermarket
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 10 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_slp_ssl_managed_config

Prefix group  : mgr
Human label   : Manager redirect → SSL Managed Config Sales Page
Page source   : not mapped
Products      : SSL, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 9 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_gdan_airo_ai_builder

Prefix group  : upp
Human label   : UPP — Airo AI Builder GDAN upsell (app-builder NES variant)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 9 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_slp_email_archiving

Prefix group  : mgr
Human label   : Manager redirect → Email Archiving Sales Landing Page
Page source   : not mapped
Products      : Value Adds, Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 9 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mya_dom_srch.auction_tldcard

Prefix group  : mya
Human label   : My Account domain search — auction TLD card
Page source   : not mapped
Products      : Domain Name Registration, Domain Options and Protection
NES/CES       : NES
Top packages  : domain
Champion      : edf13c43
Volume        : 9 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] dlp_m365domainairo

Prefix group  : dlp
Human label   : M365 + Domain + Airo bundle landing page
Page source   : not mapped
Products      : Microsoft 365, Airo, Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 9 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] dlp_365_office

Prefix group  : dlp
Human label   : Microsoft 365 / Office landing page
Page source   : not mapped
Products      : Microsoft 365, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_vps4_fully_config

Prefix group  : slp
Human label   : VPS4 Fully Managed Sales Page — Config variant
Page source   : not mapped
Products      : Virtual Hosting, SSL, Website Protection
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_o365_adduser_buymoreaccounts_studio_ios_email_

Prefix group  : app
Human label   : M365 in-app add user — Studio iOS email (buy more accounts; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Microsoft 365, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _manage or _manage_settings

## [ITC] upp_airobuilderproduct_p2p_account_upgrade-downgra

Prefix group  : upp
Human label   : UPP — Airo Builder product account upgrade/downgrade (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated (full: upgrade-downgrade); product data inferred from naming pattern

## [ITC] upp_p2p_budget_exceeded.buy_credits_nav_airo_airo_

Prefix group  : upp
Human label   : UPP — Airo buy credits nav (budget exceeded; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _ai_builder or similar

## [ITC] slp_email_archiving

Prefix group  : slp
Human label   : Email Archiving Sales Landing Page
Page source   : not mapped
Products      : Value Adds, Microsoft 365
NES/CES       : NES
Top packages  : office365-securitybundle-tier3, office365-emailplus-tier1, office365-tier3, office365-tier1, office365-tier0
Champion      : catalog resolution pending
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_email_backup

Prefix group  : slp
Human label   : Email Backup Sales Landing Page
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : NES
Top packages  : office365-tier0, office365-tier3, office365-tier1
Champion      : catalog resolution pending
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_o365_adduser_buymoreaccounts_mya_domain_manage

Prefix group  : app
Human label   : M365 in-app add user — My Account domain manager (buy more accounts; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Microsoft 365, Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _manager or _manager_email

## [ITC] app_ox_adduser_buymoreaccounts_cpanel

Prefix group  : app
Human label   : Open XChange in-app add user — cPanel (buy more accounts)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 8 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_studio_ios_email_ma

Prefix group  : app
Human label   : Open XChange in-app add user — Studio iOS email manager (buy more accounts; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _manage or _manager

## [ITC] slp_conversations-telephony

Prefix group  : slp
Human label   : Conversations Telephony Sales Landing Page
Page source   : not mapped
Products      : Conversations
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_account_site-renewals

Prefix group  : upp
Human label   : UPP — Default account site renewals
Page source   : not mapped
Products      : WordPress Managed Plans
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_security_category_config

Prefix group  : slp
Human label   : Website Security Category Sales Page — Config variant
Page source   : not mapped
Products      : SSL, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_o365_upgrade_default_studio_ios_email_manage_s

Prefix group  : app
Human label   : M365 in-app upgrade default — Studio iOS email manage settings (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _settings or similar

## [ITC] airohq.domain_search.suggestedaction

Prefix group  : airohq
Human label   : Airo HQ in-product — domain search suggested action
Page source   : not mapped
Products      : Domain Name Registration, Domain Options and Protection
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] dcc_dns_management_dnssec_tab

Prefix group  : dcc
Human label   : DCC DNS Management — DNSSEC tab
Page source   : not mapped
Products      : Premium DNS
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_dlp_email_professional

Prefix group  : mgr
Human label   : Manager redirect → Professional Email Landing Page
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_dashboard_venture_home_upgrade_

Prefix group  : upp
Human label   : UPP — WAM venture home dashboard upgrade (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _upgrade-downgrade or similar

## [ITC] upp_wamproduct_p2p_dashboard_renewals

Prefix group  : upp
Human label   : UPP — WAM dashboard renewals
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_marketing_renewals

Prefix group  : upp
Human label   : UPP — WAM marketing renewals
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_d2p_new_purchase

Prefix group  : upp
Human label   : UPP — new purchase (M365 direct-to-purchase)
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 7 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] gdc_2_0_entri.com

Prefix group  : gdc
Human label   : GoDaddy Commerce 2.0 — Entri.com integration domain purchase
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_o365_backupselectusers_backup_dcc_portfolio_se

Prefix group  : app
Human label   : M365 in-app backup select users — DCC Portfolio settings (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _settings or similar

## [ITC] upp_llcproduct_p2p_start_start_upp_start

Prefix group  : upp
Human label   : UPP — LLC product start upsell
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_marketingconsultantproduct_d2p_airo-assistant_

Prefix group  : upp
Human label   : UPP — Marketing Consultant product Airo Assistant upgrade (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix unknown

## [ITC] sem_bl_airo_claim

Prefix group  : sem
Human label   : SEM / paid search — Airo brand claim domain purchase
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_slp_ssl_wildcard_config

Prefix group  : mgr
Human label   : Manager redirect → SSL Wildcard Config Sales Page
Page source   : not mapped
Products      : Strategic Partnerships AC, SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_ssl_wildcard_config

Prefix group  : slp
Human label   : SSL Wildcard Sales Page — Config variant
Page source   : not mapped
Products      : Strategic Partnerships AC, SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_airoplusproduct_d2p_websites_airopluswam

Prefix group  : upp
Human label   : UPP — Airo Plus websites upgrade (WAM; direct-to-purchase)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_start_upp_start

Prefix group  : upp
Human label   : UPP — start upsell (WAM entry point)
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_o365_upgrade_default_mya_domain_manager_email_

Prefix group  : app
Human label   : M365 in-app upgrade default — My Account domain manager email (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _manage or _manage_settings

## [ITC] upp_wamproduct_p2p_onlinestore_upgrade-downgrade

Prefix group  : upp
Human label   : UPP — WAM online store upgrade/downgrade
Page source   : not mapped
Products      : Microsoft 365, Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_o365product_d2p_panel-lite_uep_cpanel

Prefix group  : upp
Human label   : UPP — M365 upgrade from Panel-Lite UEP cPanel entry point
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_start_mwcs

Prefix group  : app
Human label   : WooSaaS / Managed WooCommerce in-app start
Page source   : not mapped
Products      : WooSaas
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 6 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_hmc_dv_ssl_config

Prefix group  : mgr
Human label   : Manager redirect → HMC DV SSL Config
Page source   : not mapped
Products      : SSL, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] mgr_slp_ssl_dv_config

Prefix group  : mgr
Human label   : Manager redirect → SSL DV Config Sales Page
Page source   : not mapped
Products      : SSL, Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_aiwsb_config

Prefix group  : slp
Human label   : AI Website Builder Sales Page — Config variant
Page source   : not mapped
Products      : Websites and Marketing, Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_notifications_bell

Prefix group  : upp
Human label   : UPP — Airo buy credits via notifications bell (manage plan variant)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_titanproduct_d2p_panel-lite_uep_hub

Prefix group  : upp
Human label   : UPP — Titan email upgrade from Panel-Lite UEP Hub entry point
Page source   : not mapped
Products      : Vendor Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_hub

Prefix group  : app
Human label   : Open XChange in-app add user — Hub (buy more accounts)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_site-renewals

Prefix group  : upp
Human label   : UPP — site renewals upsell
Page source   : not mapped
Products      : Strategic Partnerships AC, WordPress Managed Plans
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_nav_airo_airo_ai_b

Prefix group  : upp
Human label   : UPP — Airo buy credits nav (manage plan; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _ai_builder or similar

## [ITC] upp_termsofuseproduct_d2p_airo-compliance_genai.se

Prefix group  : upp
Human label   : UPP — Terms of Use / Airo Compliance product upgrade (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _sentinel or similar

## [ITC] upp_allaccesspassproduct_p2p_account_renewals

Prefix group  : upp
Human label   : UPP — All Access Pass product account renewals
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 5 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_boost6

Prefix group  : slp
Human label   : Website Builder Boost Sales Page — variant 6
Page source   : not mapped
Products      : Website Builder
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_sl

Prefix group  : upp
Human label   : UPP — WAM Airo Builder SLP app-builder NES upsell (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _slp_airo or similar

## [ITC] upp_titanproduct_d2p_panel-lite_uep_cpanel

Prefix group  : upp
Human label   : UPP — Titan email upgrade from Panel-Lite UEP cPanel entry point
Page source   : not mapped
Products      : Vendor Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_d2p_pricing_section.upgrade_slp_airo_ai_builde

Prefix group  : upp
Human label   : UPP — Airo AI Builder SLP pricing section upgrade (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _builder or similar

## [ITC] slp_powerbi

Prefix group  : slp
Human label   : Power BI / Microsoft 365 Sales Landing Page
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : NES
Top packages  : office365-tier0
Champion      : catalog resolution pending
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_airoplusproduct_d2p_sites_airopluswam

Prefix group  : upp
Human label   : UPP — Airo Plus sites upgrade (WAM; direct-to-purchase)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_nav_website_me

Prefix group  : upp
Human label   : UPP — Airo buy credits nav website menu (budget exceeded; ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _menu or _menu_airo_ai_builder

## [ITC] upp_wamproduct_p2p_account_mya_acctsettings_subscr

Prefix group  : upp
Human label   : UPP — WAM account My Account settings subscriptions upsell (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _subscriptions or similar

## [ITC] dlp_slp_365_config

Prefix group  : dlp
Human label   : Microsoft 365 / 365 Config landing page (DLP variant)
Page source   : not mapped
Products      : Microsoft 365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_bu

Prefix group  : upp
Human label   : UPP — WAM Airo Builder buy/budget upsell (ITC truncated at 50 chars)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16
Notes         : ITC is 50 chars — likely truncated; full suffix probably _budget_exceeded or _buy

## [ITC] slp_wds_start_plan

Prefix group  : slp
Human label   : Website Design Service Start Plan Sales Page
Page source   : not mapped
Products      : Professional Web Services, Websites and Marketing
NES/CES       : NES
Top packages  : pwsdifm_gocentral_ols_012mo
Champion      : catalog resolution pending
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] business_bundle

Prefix group  : other
Human label   : Business Bundle cross-sell surface
Page source   : not mapped
Products      : Microsoft 365, Domain Name Registration
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_airoallaccesstrialproduct_d2p_start_start

Prefix group  : upp
Human label   : UPP — Airo All Access Trial start (direct-to-purchase)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] offer-govalue-api-offer-basic

Prefix group  : other
Human label   : GoValue API — Basic offer surface (aftermarket domain valuation)
Page source   : not mapped
Products      : Aftermarket Non-Retail
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] dpp_absol1.regpremium_tldcard

Prefix group  : dpp
Human label   : Domain Purchase Path — Absolute 1 Reg Premium TLD card
Page source   : not mapped
Products      : Domain Name Registration
NES/CES       : NES
Top packages  : domain
Champion      : edf13c43
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_sites_muse

Prefix group  : upp
Human label   : UPP — Default sites Muse upsell
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] slp_aiwsb

Prefix group  : slp
Human label   : AI Website Builder Sales Landing Page
Page source   : not mapped
Products      : Websites and Marketing
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16

## [ITC] app_wsb_btobp_upgrade

Prefix group  : app
Human label   : Website Builder in-app B-to-BP upgrade
Page source   : not mapped
Products      : Website Builder
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 4 orders — Low (as of 2026-05-16)
Explored      : 2026-05-16


## [ITC] wp_client_card

Prefix group  : wp — WordPress
Human label   : WordPress client card upsell
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_start_start_upp_start

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Default UPP — start flow
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_o365product_d2p_instantpage_m365wamspuredirect

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : M365 product — instant page M365 WAM pure direct
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_airobuilderproduct_f2p_airo-builder_upgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Builder product free-to-paid upgrade
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_vh_ventureredi

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP budget-exceeded screen — buy more Airo credits (vh_ventureredi)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] mgr_cs_bdgt_cal

Prefix group  : mgr — Manager redirect
Human label   : CS budget calculator redirect
Page source   : not mapped
Products      : WAM
NES/CES       : NES
Top packages  : wsb_vnext_tier2_060mo
Champion      : catalog resolution pending
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] digital_marketing_suite_ultimate

Prefix group  : digital_marketing — Digital Marketing Suite
Human label   : Digital Marketing Suite — Ultimate plan landing page
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_productivity_add_user_add_user

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product productivity add-user flow
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_mwphui_domainscard_search

Prefix group  : app — In-app
Human label   : MWP Hub UI — domains card search
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_slp_airo_banne

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP budget-exceeded screen — buy more Airo credits (slp_airo_banne)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_wamproduct_f2p_productivity_upgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM product free-to-paid productivity upgrade
Page source   : not mapped
Products      : Titan Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_conversationsproduct_d2p_airo-sentinel_convers

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Conversations product — Airo Sentinel upsell during Conversations flow
Page source   : not mapped
Products      : Conversations
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 3 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] mgr_slp_ssl_ev_config

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP SSL EV config
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_domain_generator

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — domain name generator
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-builder_app-builder-nes_gd

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM Airo Builder → App Builder NES upsell (GoDaddy variant)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] dlp_email_professional_config

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — email professional config
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_commerce_pay_links_iplp

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Commerce — Pay Links inline PLP
Page source   : not mapped
Products      : Commerce Hardware
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_o365_upgrade_default_studio_ios_manage_email_p

Prefix group  : app — In-app
Human label   : M365 in-app upgrade — Studio iOS manage email (truncated)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] slp_wsba

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Website Builder Annual (WSBA)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_marketing_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM marketing product upgrade/downgrade
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-sentinel_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM Airo Sentinel upgrade/downgrade flow
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_manage_plan.buy_credits_gdan_airo_ai_build

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (gdan_airo_ai_build)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] mgr_slp_hosting_category_config

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP Hosting category config
Page source   : not mapped
Products      : VPS
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain_com_fr

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — .com.fr domains
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_o365_upgrade_default_cpanel

Prefix group  : app — In-app
Human label   : M365 in-app upgrade (default) — cPanel hosting context
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_slp_visio_config

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP Visio config
Page source   : not mapped
Products      : Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_dashboard_vh_ai_website_preview

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM dashboard upsell — Venture Hosting AI website preview
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_o365_upgrade_default_dpp_dpr_post_publish

Prefix group  : app — In-app
Human label   : M365 in-app upgrade — DPP post-publish flow
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] investor_app_afternic_listing_exact

Prefix group  : investor — Aftermarket / Investor
Human label   : Afternic investor app — exact domain listing
Page source   : not mapped
Products      : Domain Transfer
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_dashboard_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Default UPP — dashboard upgrade/downgrade
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_copilot_email_config

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — Copilot email config
Page source   : not mapped
Products      : Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_slp_365

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — SLP 365
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_powerbi_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Power BI (config variant)
Page source   : not mapped
Products      : Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_133881cd-a383-4e20-bbe6-a37b3a3

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM product paid-to-paid (UUID-based variant — unknown context)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_wsb_domain_xsell_settings

Prefix group  : app — In-app
Human label   : Website Builder app — domain cross-sell settings
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_pricing_section.upgrade_nav_airo_airo_ai_b

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product pricing section — Airo AI Builder upgrade nav
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_usage_gauge.buy_credits_nav_airo_airo_ai_b

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP usage-gauge buy-credits flow (nav_airo_airo_ai_b)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_d2p_new_purchase_conversations

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product new purchase — Conversations
Page source   : not mapped
Products      : Conversations
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_f2p_store_upgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM product free-to-paid store upgrade
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_o365_encryption_addon_dpp_dpr_post_publish

Prefix group  : app — In-app
Human label   : M365 encryption add-on — DPP post-publish context
Page source   : not mapped
Products      : Value Adds
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_wordpress_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP WordPress (config variant)
Page source   : not mapped
Products      : MWP
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_slp_airo_ai_builder

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP Airo App Builder NES — SLP Airo AI Builder surface
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_planner_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Microsoft Planner (config variant)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_ssl_certificate_config

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — SSL certificate config
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_slp_marketing_suite

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP Marketing Suite
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain_godaddy_b.smartdefault_exact

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — GoDaddy B variant (smartdefault_exact)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] gdc_2_0_google.com

Prefix group  : gdc — GoDaddy Commerce
Human label   : GoDaddy Commerce 2.0 — Google.com merchant integration
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 2 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_productivity_add_user_titan

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product productivity add Titan email user
Page source   : not mapped
Products      : Titan Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] my

Prefix group  : other
Human label   : My Account (bare "my" ITC — generic/unknown context)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_studio_android_emai

Prefix group  : app — In-app
Human label   : Open XChange add-user — Studio Android email (truncated)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_airo-builder_upp_airo_ai_builder_upgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo AI Builder — cross-sell upgrade to full Airo Builder
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_dpp_dpr_post_publis

Prefix group  : app — In-app
Human label   : Open XChange add-user / buy more accounts — DPP post-publish (truncated)
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_o365_adduser_buymoreaccounts_dpp_dpr_post_publ

Prefix group  : app — In-app
Human label   : M365 add-user / buy more accounts — DPP post-publish (truncated)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_manage_plan.buy_credits_account_myrenewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (account_myrenewals)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] mya-express-checkout

Prefix group  : mya — My Account
Human label   : My Account express checkout
Page source   : not mapped
Products      : Commerce Hardware
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_slp_airo_banner_ai

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (slp_airo_banner_ai)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] gdc_2_0_shopify.com

Prefix group  : gdc — GoDaddy Commerce
Human label   : GoDaddy Commerce 2.0 — Shopify.com integration
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain_godaddy_b.unavailable_organicspin

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — GoDaddy B variant (unavailable_organicspin)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_app-builder-nes_slp_homepage_airo_ai_build

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP Airo App Builder NES — SLP Homepage Airo AI Builder
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] wss_advanced

Prefix group  : wss — Website Security Suite
Human label   : Website Security Suite — Advanced plan
Page source   : not mapped
Products      : Website Security
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] digital_marketing_suite_reach

Prefix group  : digital_marketing — Digital Marketing Suite
Human label   : Digital Marketing Suite — Reach plan landing page
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-sentinel_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM Airo Sentinel renewal upsell
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_airobuilderproduct_p2p_account_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Builder product paid-to-paid account renewals
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_gdan_airo_ai_b

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP budget-exceeded screen — buy more Airo credits (gdan_airo_ai_b)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_usage_gauge.buy_credits_notifications_bell

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP usage-gauge buy-credits flow (notifications_bell)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_o365_adduser_buymoreaccounts_vh_bundling_ai

Prefix group  : app — In-app
Human label   : M365 add-user / buy more accounts — Venture Hosting AI bundling
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_default_p2p_accounts_unknown-entry-point_upp_c

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Default UPP — accounts (unknown entry point, Conversations context)
Page source   : not mapped
Products      : Conversations
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_o365_upgrade_default_studio_android_manage_ema

Prefix group  : app — In-app
Human label   : M365 in-app upgrade — Studio Android manage email (truncated)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_wsb_ptob_upgrade

Prefix group  : app — In-app
Human label   : Website Builder app — paid-to-better-plan upgrade
Page source   : not mapped
Products      : Website Builder
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_managed_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Managed Hosting (config variant)
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_o365_adduser_buymoreaccounts_dcc_usemydomain_a

Prefix group  : app — In-app
Human label   : M365 add-user / buy more accounts — DCC use-my-domain (truncated)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] app_o365_upgrade_default_hub

Prefix group  : app — In-app
Human label   : M365 in-app upgrade — Hub context
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_o365product_p2p_start_start_upp_start

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : M365 product paid-to-paid — start flow
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-builder_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM Airo Builder renewal upsell
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_panel-lite_mwp

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product panel lite — MWP
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_airo

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — Airo
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_slp_email_backup

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP Email Backup
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_f2p_marketing_upgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM product free-to-paid marketing upgrade
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_o365product_d2p_panel-lite_uep_mwp

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : M365 product panel lite — MWP upsell entry point
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_panel-lite_plesk

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product panel lite — Plesk
Page source   : not mapped
Products      : Titan Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] godaddy_hp

Prefix group  : godaddy — GoDaddy Branded
Human label   : GoDaddy homepage
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] hp_commerce_sell_anywhere

Prefix group  : hp — Homepage
Human label   : Homepage — Commerce sell anywhere section
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] auc_acquisition_agent

Prefix group  : auc — Aftermarket Auction
Human label   : Aftermarket auction — acquisition agent
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dcc_standalone_renew_domain_page

Prefix group  : dcc — Domain Control Center
Human label   : Domain Control Center — standalone domain renewal page
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_dopproduct_d2p_dashboard_d2p_shelf_space

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : DOP product — dashboard shelf space upsell
Page source   : not mapped
Products      : DOP
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_spu_airo_plus_logo

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP single-product upsell — Airo Plus logo add-on
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_gum-marketing

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP GUM (Growth User Marketing) — marketing flow
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_vnext_free_trial_expired_renewal

Prefix group  : app — In-app
Human label   : Ventures Next — free trial expired renewal screen
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_account_unknown-entry-point

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM account upsell (unknown entry point)
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_ddc_pro_01

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — DDC Pro 01
Page source   : not mapped
Products      : Domain Buyers Club
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain_godaddy_nb

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — GoDaddy non-B variant
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_airo-sentinel_@gdcorp-im/market

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM Airo Sentinel upsell (internal marketing variant)
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_account

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP paid-to-paid — account view M365
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_productivity_dlp_m365oybo

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product M365 OYBO (own your business offer) DLP
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_slp_homepage_airo_

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (slp_homepage_airo_)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_m365emailshelftrialproduct_p2p_start_start_upp

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : M365 email shelf trial product — start flow
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_airoplusshelftrialproduct_p2p_start_start_upp_

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Plus shelf trial product — start flow
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_default_p2p_sites_upgrade-downgrade

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Default UPP — sites upgrade/downgrade
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP renewals (generic SSL/cert renewals)
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_website_backup

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Website Backup
Page source   : not mapped
Products      : Website Security
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] domains_valuation_lp_protect

Prefix group  : domains — Domains
Human label   : Domain valuation landing page — protect flow
Page source   : not mapped
Products      : DOP
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_airoplusproduct_d2p_airo-sentinel_airopluswam

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Plus product d2p — Airo Sentinel + WAM bundle
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_ox_adduser_buymoreaccounts_vh_bundling_ai

Prefix group  : app — In-app
Human label   : Open XChange add-user — Venture Hosting AI bundling
Page source   : not mapped
Products      : Open XChange
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_visio

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Microsoft Visio
Page source   : not mapped
Products      : M365
NES/CES       : NES
Top packages  : office365-tier0
Champion      : catalog resolution pending
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_usage_gauge.buy_credits_gdan_airo_ai_build

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP usage-gauge buy-credits flow (gdan_airo_ai_build)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_wamproduct_p2p_productivity_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM productivity renewals
Page source   : not mapped
Products      : Titan Email
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_budget_exceeded.buy_credits_account_myrene

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP budget-exceeded screen — buy more Airo credits (account_myrene)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] slp_ssladdtocart1_config

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP SSL add-to-cart 1 (config variant)
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] app_o365_upgrade_default_dpp_gc_merchandise

Prefix group  : app — In-app
Human label   : M365 in-app upgrade — DPP GC merchandise context
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] account.products.domain_recommendations_box.top_ac

Prefix group  : other
Human label   : Account products — domain recommendations box top (truncated)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_wamproduct_p2p_email_renewals

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM email renewals
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_cheapdomain_godaddy_b.primary_tldcard

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — GoDaddy B variant (primary_tldcard)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_editor.post_publish_modal

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP post-publish modal editor upsell
Page source   : not mapped
Products      : WAM
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_usage_gauge.buy_credits_slp_airo_banner_ai

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP usage-gauge buy-credits flow (slp_airo_banner_ai)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] dlp_cheapdomain_godaddy_b.regpremium_exact

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap domain DLP — GoDaddy B variant (regpremium_exact)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : NES
Top packages  : domain
Champion      : domain → edf13c43 (Rev 3)
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] mgr_slp_ssl

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — SLP SSL
Page source   : not mapped
Products      : SSL
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_airobuilderproduct_d2p_airo-builder_header.upg

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Builder header upgrade prompt (d2p flow)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_airoplusproduct_d2p_account_airopluswam

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Airo Plus product d2p — account view + WAM
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dpp_absol1.unavailable_premiumspin

Prefix group  : dpp — Domain Purchase Path
Human label   : Domain Purchase Path — unavailable domain with premium spin
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_d2p_genai.sentinel.assistant

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : Dashboard-to-product GenAI Sentinel AI assistant upsell
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] slp_airo&unifiedsearch=true&maxwordsforlegacysearc

Prefix group  : slp — Sales Landing Pages (Front of Site)
Human label   : SLP Airo (URL param variant — likely truncated URL-encoded ITC)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown; ITC contains URL params — likely miscaptured tracking code

## [ITC] mgr_dlp_365_office_config

Prefix group  : mgr — Manager redirect
Human label   : Manager redirect — DLP 365 Office config
Page source   : not mapped
Products      : M365
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_p2p_manage_plan.buy_credits_nav_website_menu_a

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (nav_website_menu_a)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] upp_p2p_manage_plan.buy_credits_vh_ventureredirect

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : UPP manage-plan buy-credits flow (vh_ventureredirect)
Page source   : not mapped
Products      : Airo
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown

## [ITC] mya_dom_srch

Prefix group  : mya — My Account
Human label   : My Account domain search (base/generic ITC)
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] dlp_domain_payable

Prefix group  : dlp — Domain Landing Page
Human label   : Domain Landing Page — domain payable
Page source   : not mapped
Products      : Domain Reg
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16

## [ITC] upp_wamproduct_p2p_websites_editor.free-trial-bann

Prefix group  : upp — Upsell / Upgrade Path Platform
Human label   : WAM websites editor free-trial banner upsell
Page source   : not mapped
Products      : Strategic Partnerships AC
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-15)
Explored      : 2026-05-16
Notes         : ITC truncated at 50 chars — full name unknown
## [ITC] dlp_cheapdomain_godaddy_b.unavailable_dbs

Prefix group  : dlp — Domain Landing Page
Human label   : Cheap Domain LP — unavailable domain, Domain By Proxy Stealth upsell
Page source   : not mapped
Products      : Aftermarket Non-Retail (100%)
NES/CES       : NES
Top packages  : dbs
Champion      : dbs → 0ce223ed-7bb7-4e02-ae66-960ccd798346 (active Rev 1)
Volume        : 3 orders — Low (as of 2026-05-17)
Explored      : 2026-05-17
Notes         : Variant of dlp_cheapdomain_godaddy_b.* fired when the searched domain is unavailable and the DBS (Domain By Proxy Stealth) offer is shown. Shares champion UUID 0ce223ed with dcc_portfolio_domain_search_box's dbs entry.

## [ITC] upp_d2p_pricing_section.upgrade_nav_website_menu_a

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Airo upgrade from nav website menu pricing section (variant A)
Page source   : not mapped
Products      : Airo (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-17)
Explored      : 2026-05-17
Notes         : Low-volume CES upsell from the pricing section within the nav website menu. Variant A (likely A/B test). ITC name truncated at 50 chars.

## [ITC] digital_marketing_suite_engagement

Prefix group  : other — non-standard prefix
Human label   : Digital Marketing Suite — engagement tier
Page source   : not mapped
Products      : Websites and Marketing (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-17)
Explored      : 2026-05-17
Notes         : Engagement tier of the Digital Marketing Suite. Sister ITCs include digital_marketing_suite_deluxe, digital_marketing_suite_essentials, digital_marketing_suite_ultimate, digital_marketing_suite_reach (all CES).

## [ITC] upp_p2p_start

Prefix group  : upp — Upsell / Upgrade Path
Human label   : P2P upsell — start plan
Page source   : not mapped
Products      : Websites and Marketing (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-17)
Explored      : 2026-05-17

## [ITC] upp_d2p_pricing_section.upgrade_slp_airo_banner_ai

Prefix group  : upp — Upsell / Upgrade Path
Human label   : Airo upgrade from SLP banner AI pricing section
Page source   : not mapped
Products      : Airo (100%)
NES/CES       : CES
Top packages  : none (CES)
Champion      : —
Volume        : 1 orders — Low (as of 2026-05-17)
Explored      : 2026-05-17
Notes         : CES upsell from Airo AI banner on a Sales Landing Page pricing section. ITC name truncated at 50 chars.
