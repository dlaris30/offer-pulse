# Offer Pulse — Golden Set
<!-- append-only; analyst-confirmed expected outputs; read by /scorer and /batch-test; never read by /offer-pulse -->
<!-- schema: NES entries have expected.source_offer_slug + components + ticket_ready clone fields; CES entries have expected.packages rows + ticket_ready table -->

---

## UC-01

case_id          : UC-01
input_type       : itc
surface          : dpp-ca-ca
path_type        : NES Bundle
reliability      : stable
date_added       : 2026-05-15

expected:
  source_offer_slug  : dpp-ca-ca-solution-tier1
  source_offer_id    : e328092f-972c-4353-a884-78fd086a6866
  collection_name    : domainEmail
  plan_name          : defaultEmailessentialseeDpp
  pfid               : unknown
  discount_code      : disc000013
  sale_price         : unknown
  list_price         : unknown
  term               : annual
  markets            : [CA]
  geometry           : Bundle
  what_changes       : unknown
  components:
    wired:
      - name     : NewDomain
        offer_id : edf13c43
        plan     : default
        notes    : standard new domain registration
      - name     : M365 Email Essentials
        offer_id : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
        plan     : emailEssentialsEe
        term     : 1 YEAR
        notes    : autoRenew=false applied as rule-level override when curated offer selects Dpp-suffix plan; same offerId without Dpp-suffix plan defaults autoRenew=true
    collection_only  : []

ticket_ready:
  clone_source       : dpp-ca-ca-solution-tier1
  pfid_to_swap       : unknown
  discount_code      : disc000013
  sale_price         : unknown
  surface            : dpp-ca-ca

---

## UC-02

case_id          : UC-02
input_type       : itc
surface          : slp_ssl
path_type        : NES Standalone
reliability      : volatile
date_added       : 2026-05-15

expected:
  source_offer_slug  : ssl-001sites-tier1
  source_offer_id    : 28e5b730-4e70-46b0-8672-6e18a17f81a1
  plan_name          : standard
  pfid               : 3604 (Standard SSL 1 Year — paid core product on slp_ssl; same PFID appears as free add-on in hosting bundles on other surfaces)
  discount_code      : none
  sale_price         : unknown
  list_price         : unknown
  term               : 1 Year
  markets            : [US]
  geometry           : Standalone (offerCollectionId=null, offers[] empty, prePurchaseKeyMap absent)
  what_changes       : unknown
  notes              : slp_ssl dominant champion is ssl-001sites-tier1 (10,112 orders/7d as of 2026-05-17); ssl-001sites-* family spans Standard/Deluxe/Premium/Managed tiers using "SSL Certificate Offer" (28e5b730, tag=sslcert, 64-plan schema); each ssl-001sites-* slug selects one plan (standard/deluxe/premium/managed/managedWithMonitoring); reliability=volatile because multiple active package_ids on surface (ssl-001sites-tier1/2/3/managed-tier1); prior expected dlxssl-001domain-tier1dv (separate offer definition 35fc5321) was pre-launch catalog-only with 38 orders/90d test activity — not a live champion

ticket_ready:
  clone_source       : ssl-001sites-tier1
  pfid_to_swap       : 3604
  discount_code      : none
  sale_price         : unknown
  surface            : slp_ssl

---

## UC-03

case_id          : UC-03
input_type       : itc
surface          : mena-digital-kit
path_type        : NES Bundle
reliability      : volatile
date_added       : 2026-05-15

expected:
  result             : AMBIGUOUS — two architectures for "basic tier"; analyst must specify M365 or Titan before ticket can be produced
  geometry           : Bundle (both architectures)

  architecture_1:
    source_offer_slug : mena-digital-kit-tier1
    source_offer_id   : 7683d414-f935-4e62-93b1-89009a814162
    collection_name   : domainDudaEmail
    plan_name         : defaultBasicOfficebusinessps
    discount_code     : disc000001
    term              : annual (1/2/3 Year supported)
    markets           : [MENA]
    components:
      wired:
        - name     : NewDomain
          offer_id : edf13c43
          plan     : unknown
        - name     : Duda
          offer_id : 2c5e3bb2
          plan     : basic
        - name     : M365
          offer_id : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
          plan     : officeBusinessPs

  architecture_2:
    source_offer_slug : mena-digital-kit-tier4
    source_offer_id   : c377d7de-2108-3340-b580-44a32a17c416
    collection_name   : domainProfessionalEmail
    plan_name         : defaultBasicStartup
    discount_code     : disc000007
    term              : annual (1 Year only)
    markets           : [MENA]
    components:
      wired:
        - name     : NewDomain
          offer_id : edf13c43
          plan     : unknown
        - name     : Duda
          offer_id : 2c5e3bb2
          plan     : basic
        - name     : Titan Email
          offer_id : 927a9d45-7c5b-4652-ad68-d5cd9be75028
          plan     : light

  disambiguation_key : Duda plan=basic on both — cannot disambiguate via Duda alone; M365 tiers use *OfficebusinessPs plan family; Titan tiers use *Startup plan family

ticket_ready:
  clone_source       : AMBIGUOUS — specify M365 (tier1) or Titan (tier4)
  pfid_to_swap       : unknown
  discount_code      : AMBIGUOUS — disc000001 (M365) | disc000007 (Titan)
  sale_price         : unknown
  surface            : mena-digital-kit

---

## CMS-32825

case_id          : CMS-32825
input_type       : jira_ticket
surface          : slp_ssl
path_type        : NES Standalone
reliability      : volatile
date_added       : 2026-05-15

expected:
  source_offer_slug  : all 29 dlxssl-* slugs already ACTIVE in catalog (e.g. dlxssl-001domain-tier1dv, dlxssl-005domains-tier1dv, dlxssl-wildcard-tier1dv, and 26 others)
  source_offer_id    : 35fc5321-7723-4c40-906b-7b5c417e61cb (shared across all 29 slugs)
  plan_name          : varies by slug — dvSingleDomain / dvMultiDomain5–100 / dvWildcard / ovSingleDomain / ovMultiDomain5–100 / ovWildcard / evSingleDomain / evMultiDomain5–100 / evWildcard (38 plan variants total in schema)
  pfid               : unknown (pre-launch; 0 production billing rows)
  discount_code      : none
  sale_price         : unknown
  list_price         : unknown
  term               : varies (1–4 Year per PFID group)
  markets            : [all]
  geometry           : Standalone (all 29 slugs share Standalone geometry — prePurchaseKeyMap absent, offers[] empty)
  what_changes       : all 29 slugs already active in catalog — remaining action is CES wiring to SSL Config surface
  notes              : EV Wildcard present in offer definition schema but absent from ticket's 29 packages; 38 orders/90d on slp_ssl for DV Single Domain are test/config activity; slp_ssl current live traffic is ssl-001sites-* family (offerId 28e5b730), not dlxssl-* (offerId 35fc5321); reliability=volatile because automated regression will find ssl-001sites-tier1 as champion, not dlxssl-001domain-tier1dv — this entry documents a pre-launch/pre-wiring catalog state that cannot pass automated overnight testing until dlxssl-* wiring to ssl-config is live

ticket_ready:
  clone_source       : 35fc5321-7723-4c40-906b-7b5c417e61cb (shared base offer)
  pfid_to_swap       : unknown (pre-launch)
  discount_code      : none
  sale_price         : unknown
  surface            : slp_ssl

---

## MWP-BASIC-SLP-OX

case_id          : MWP-BASIC-SLP-OX
input_type       : itc
surface          : slp_wordpress
path_type        : NES Bundle
reliability      : volatile
date_added       : 2026-05-15

expected:
  source_offer_slug  : wordpress-openexchange-forever-ssl-basic
  source_offer_id    : 4ce8a17c-b508-34ab-99d1-e5e5165214d3
  collection_name    : unknown
  plan_name          : unknown
  pfid               : unknown
  discount_code      : unknown (UUID placeholder in billing — not a standard discount code)
  sale_price         : unknown (catalog_list_price and catalog_sale_price NULL in billing; avg_receipt_price only)
  list_price         : unknown
  term               : 1 Year
  markets            : [ROW, IN]
  geometry           : Bundle
  what_changes       : unknown
  components:
    wired:
      - name     : Titan Email (OX)
        offer_id : 927a9d45-7c5b-4652-ad68-d5cd9be75028
        plan     : none specified in prePurchaseKeyMap
        notes    : FREEACCOUNT=true in prePurchaseKeyMap customData
    collection_only:
      - name     : WordPressOffer
        offer_id : 566f8074
        tags     : [wpaas]
        notes    : parentOffer tag; not in prePurchaseKeyMap
      - name     : Norton
        offer_id : 72a57662
        notes    : not in prePurchaseKeyMap

ticket_ready:
  clone_source       : wordpress-openexchange-forever-ssl-basic
  pfid_to_swap       : unknown
  discount_code      : unknown
  sale_price         : unknown
  surface            : slp_wordpress

---

## MWP-BASIC-SLP-GEOSPLIT

case_id          : MWP-BASIC-SLP-GEOSPLIT
input_type       : itc
surface          : slp_wordpress
path_type        : NES Bundle
reliability      : volatile
date_added       : 2026-05-15

expected:
  result             : AMBIGUOUS — two simultaneous geo-split bundles; both active on slp_wordpress
  geometry           : Bundle (both)

  bundle_1_ox:
    source_offer_slug : wordpress-openexchange-forever-ssl-basic
    source_offer_id   : 4ce8a17c-b508-34ab-99d1-e5e5165214d3
    plan_name         : unknown
    discount_code     : unknown (UUID placeholder)
    term              : unknown (3-year PFID 1320704 in bundle; 1-year absent from NES packages)
    markets           : [developing — ROW, IN]
    components:
      wired:
        - name     : Titan Email (OX)
          offer_id : 927a9d45-7c5b-4652-ad68-d5cd9be75028
          plan     : none specified
          notes    : FREEACCOUNT=true in prePurchaseKeyMap customData
      collection_only:
        - name     : WordPressOffer
          offer_id : 566f8074
          tags     : [wpaas]
        - name     : Norton
          offer_id : 72a57662

  bundle_2_o365:
    source_offer_slug : wordpress-o365-forever-ssl-basic
    source_offer_id   : 876fc126-7ce9-3b47-975a-0f0513bf38a8
    plan_name         : unknown
    discount_code     : unknown (4 distinct UUID codes — A/B test likely)
    term              : mixed (3-year WP hosting + 1-year M365 per billing data)
    markets           : [developed — US, CA; NOT IN/developing]
    notes             : M365 geo risk quantityByOfferKey=2 seats; M365 absent from India/developing markets confirmed
    components:
      wired:
        - name     : M365 Email Essentials
          offer_id : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
          plan     : emailEssentialsEe
          notes    : 1-year term for M365 within 3-year WP bundle
      collection_only:
        - name     : WordPressOffer
          offer_id : 566f8074
          tags     : [wpaas]
        - name     : Airo
          offer_id : unknown

ticket_ready:
  clone_source       : AMBIGUOUS — confirm which geo-split bundle applies for target market
  pfid_to_swap       : unknown
  discount_code      : unknown
  sale_price         : unknown
  surface            : slp_wordpress

---

## MWP-DELUXE-SLP

case_id          : MWP-DELUXE-SLP
input_type       : itc
surface          : slp_wordpress
path_type        : NES Bundle
reliability      : volatile
date_added       : 2026-05-15

expected:
  result             : AMBIGUOUS — two simultaneous geo-split bundles; both active on slp_wordpress
  geometry           : Bundle (both)

  bundle_1_ox:
    source_offer_slug : wordpress-openexchange-forever-ssl-deluxe
    source_offer_id   : ce0a7869
    plan_name         : unknown
    pfid              : 1320706 (3-year MWP Deluxe; 1-year PFID 1320700 absent from NES packages)
    discount_code     : unknown (UUID placeholder)
    term              : 3 Year (1-year absent; "first year discount" = overridePolicies on 3-year, not a separate 1-year offer)
    markets           : [developing — ROW, IN]
    components:
      wired:
        - name     : Titan Email (OX)
          offer_id : 927a9d45-7c5b-4652-ad68-d5cd9be75028
          plan     : unknown (personalTitan per related runs)
      collection_only:
        - name     : WordPressOffer
          offer_id : 566f8074
          tags     : [wpaas]
        - name     : Norton
          offer_id : 72a57662

  bundle_2_o365:
    source_offer_slug : wordpress-o365-forever-ssl-deluxe
    source_offer_id   : 658d1af2
    plan_name         : unknown
    pfid              : 1320706 (3-year MWP Deluxe)
    discount_code     : unknown (4 distinct UUID codes — A/B test likely)
    term              : 3 Year (mixed: 3-year WP hosting + 1-year M365)
    markets           : [developed — US, CA]
    notes             : M365 geo risk quantityByOfferKey=2 seats
    components:
      wired:
        - name     : M365 Email Essentials
          offer_id : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
          plan     : emailEssentialsEe
      collection_only:
        - name     : WordPressOffer
          offer_id : 566f8074
          tags     : [wpaas]
        - name     : Airo
          offer_id : unknown

ticket_ready:
  clone_source       : AMBIGUOUS — two series; confirm with ecomm
  pfid_to_swap       : 1320706
  discount_code      : unknown
  sale_price         : unknown
  surface            : slp_wordpress

---

## CMS-31421

case_id          : CMS-31421
input_type       : jira_ticket
surface          : dpp_precheck
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : temp-email-essentials-99
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : emailEssentialsEe
      geometry      : Standalone (offers[] empty, prePurchaseKeyMap absent)
      tags          : [partneremail, m365]
      status        : ACTIVE Rev 1
      special_config : none
      rows:
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867688
          pfid_renewal  : 867688
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867694
          pfid_renewal  : 867694
          term          : annual 2yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867696
          pfid_renewal  : 867696
          term          : annual 3yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
    - package_name  : temp-email-essentials-149
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : emailEssentialsEe
      geometry      : Standalone (offers[] empty, prePurchaseKeyMap absent)
      tags          : [partneremail, m365]
      status        : ACTIVE Rev 1
      special_config : none
      rows:
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867688
          pfid_renewal  : 867688
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867694
          pfid_renewal  : 867694
          term          : annual 2yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867696
          pfid_renewal  : 867696
          term          : annual 3yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
  geo              : global (DISC214228 primary on dpp_precheck; DISC214229 primary on dpp_config1 multi-market)
  billing_volume   : DISC214228 — 2,457 orders/7d for PFID 867688 1yr US

ticket_ready:
  rows:
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867688
      pfid_renewal  : 867688
      term          : annual 1yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867694
      pfid_renewal  : 867694
      term          : annual 2yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867696
      pfid_renewal  : 867696
      term          : annual 3yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)

---

## EMAIL-ESS-DPP-17

case_id          : EMAIL-ESS-DPP-17
input_type       : itc
surface          : dpp_precheck
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : temp-email-essentials-99
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : emailEssentialsEe
      geometry      : Standalone (offers[] empty, prePurchaseKeyMap absent)
      tags          : [partneremail, m365]
      status        : ACTIVE Rev 1
      special_config : none
      rows:
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867688
          pfid_renewal  : 867688
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867694
          pfid_renewal  : 867694
          term          : annual 2yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867696
          pfid_renewal  : 867696
          term          : annual 3yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214228
    - package_name  : temp-email-essentials-149
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : emailEssentialsEe
      geometry      : Standalone (offers[] empty, prePurchaseKeyMap absent)
      tags          : [partneremail, m365]
      status        : ACTIVE Rev 1
      special_config : none
      rows:
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867688
          pfid_renewal  : 867688
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867694
          pfid_renewal  : 867694
          term          : annual 2yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
        - product_name  : Email Essentials From GoDaddy
          pfid_new      : 867696
          pfid_renewal  : 867696
          term          : annual 3yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : DISC214229
  geo              : global

ticket_ready:
  rows:
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867688
      pfid_renewal  : 867688
      term          : annual 1yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867694
      pfid_renewal  : 867694
      term          : annual 2yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)
    - product_name  : Email Essentials From GoDaddy
      pfid_new      : 867696
      pfid_renewal  : 867696
      term          : annual 3yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : DISC214228 (package 1) | DISC214229 (package 2)

---

## M365-OE-NOTEAMS-DPP-EVAL-02

case_id          : M365-OE-NOTEAMS-DPP-EVAL-02
input_type       : itc
surface          : dpp_precheck
path_type        : CES
reliability      : stable
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : microsoftemail-onlineessentialsnoteams-discount-365af1f1cb
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : onlineEssentialsNoTeams
      geometry      : Standalone (prePurchaseKeyMap absent, offers[] empty, offerCollectionId=None)
      tags          : [partneremail, m365]
      status        : ACTIVE Rev 1, modified 2026-04-22
      special_config : base slug microsoftemail-onlineessentialsnoteams does NOT exist — discounted variant is only live config
      rows:
        - product_name  : Online Essentials - 1 year(s)
          pfid_new      : 1768604
          pfid_renewal  : 1768604
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : 365af1f1cb
  geo              : global (US primary 188 orders/7d; CA 3; SA 1)
  sale_price       : $3.99/mo ($47.88/yr) confirmed from CA/SA billing avg receipt
  billing_volume   : PFID 1768604 — 192 orders/7d on dpp_precheck (all null package_id)
  legacy_tiers     : temp-email-essentials-99 (DISC214228) and temp-email-essentials-149 (DISC214229) share same offerId 575a7d2a — all dpp_precheck email offers are plans on the same underlying M365 product

ticket_ready:
  rows:
    - product_name  : Online Essentials - 1 year(s)
      pfid_new      : 1768604
      pfid_renewal  : 1768604
      term          : annual 1yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : 365af1f1cb

---

## M365-OE-NOTEAMS-DPP-19

case_id          : M365-OE-NOTEAMS-DPP-19
input_type       : itc
surface          : dpp_precheck
path_type        : CES
reliability      : stable
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : microsoftemail-onlineessentialsnoteams-discount-365af1f1cb
      offer_id      : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391
      plan          : onlineEssentialsNoTeams
      geometry      : Standalone (prePurchaseKeyMap absent, offers[] empty)
      tags          : [partneremail, m365]
      status        : ACTIVE, modified 2026-04-22
      special_config : base slug microsoftemail-onlineessentialsnoteams does NOT exist
      rows:
        - product_name  : Online Essentials - 1 year(s)
          pfid_new      : 1768604
          pfid_renewal  : 1768604
          term          : annual 1yr
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : 365af1f1cb
  geo              : global
  notes            : all six email curated offers on dpp_precheck share base offer ID 575a7d2a; new offer is a plan on same underlying product as legacy tiers; Fourth email PFID 1556350 (Email Plus, 494 orders/7d) unresolved — not confirmed as part of this offer

ticket_ready:
  rows:
    - product_name  : Online Essentials - 1 year(s)
      pfid_new      : 1768604
      pfid_renewal  : 1768604
      term          : annual 1yr
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : 365af1f1cb

---

## TITAN-FREETRIAL-14D-UPP-08

case_id          : TITAN-FREETRIAL-14D-UPP-08
input_type       : itc
surface          : upp_titanproduct_*
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : titanemail-light-freetrial-14days
      offer_id      : 927a9d45-7c5b-4652-ad68-d5cd9be75028
      plan          : light
      geometry      : Standalone (prePurchaseKeyMap absent, offers[] empty)
      status        : ACTIVE Rev 3, modified 2025-12-18 by EP-82036
      special_config : BPO=FREE_TRIAL (14-day), autoRenew=false; wire-to-surface operation — offer already exists in catalog; NOT a clone/net-new
      rows:
        - product_name  : Titan email (Professional Email Pro Light)
          pfid_new      : unknown (SKU not yet in production — BLOCKING)
          pfid_renewal  : N/A (autoRenew=false)
          term          : 14-day free trial
          tier          : standalone
          otc           : N
          free_product  : Y
          existing_pkg  : Y
          discount_code : N
  geo              : IN/MY/PH/PK/ZA/AR/CL/CO/MX/PE/BR/TR/ID/TH/UA/VN/PL (17 i18n markets)
  notes            : other Titan trial variants (starter-freetrial-1year, starter-freetrial-1month) share same offerId 927a9d45 but use different plan/term — not suppressed; all 6 keyword matches disclosed

ticket_ready:
  rows:
    - product_name  : Titan email (Professional Email Pro Light)
      pfid_new      : unknown (BLOCKING — SKU not yet in production)
      pfid_renewal  : N/A
      term          : 14-day free trial
      tier          : standalone
      otc           : N
      free_product  : Y
      existing_pkg  : Y
      discount_code : N

---

## TITAN-FREETRIAL-14D-UPP-1430

case_id          : TITAN-FREETRIAL-14D-UPP-1430
input_type       : itc
surface          : upp_titanproduct_*
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : titanemail-light-freetrial-14days
      offer_id      : 927a9d45-7c5b-4652-ad68-d5cd9be75028
      plan          : light
      geometry      : Standalone (prePurchaseKeyMap absent, offers[] empty)
      status        : ACTIVE Rev 3, modified 2025-12-18 by EP-82036
      special_config : BPO=FREE_TRIAL (14-day), autoRenew=false; wire-to-surface (offer already exists); confirmed correct by analyst
      rows:
        - product_name  : Titan email (Professional Email Pro Light)
          pfid_new      : unknown (SKU not yet in production — BLOCKING)
          pfid_renewal  : N/A (autoRenew=false)
          term          : 14-day free trial
          tier          : standalone
          otc           : N
          free_product  : Y
          existing_pkg  : Y
          discount_code : N
  geo              : IN/MY/PH/PK/ZA/AR/CL/CO/MX/PE/BR/TR/ID/TH/UA/VN/PL (17 i18n markets)
  notes            : Base Collection ID 927a9d45-7c5b-4652-ad68-d5cd9be75028 confirmed correct by analyst; active CES discount disc444888 on UPP surface noted (existing, not for this offer)

ticket_ready:
  rows:
    - product_name  : Titan email (Professional Email Pro Light)
      pfid_new      : unknown (BLOCKING — SKU not yet in production)
      pfid_renewal  : N/A
      term          : 14-day free trial
      tier          : standalone
      otc           : N
      free_product  : Y
      existing_pkg  : Y
      discount_code : N

---

## WAM-PREM-COMM-FOS-4ARM

case_id          : WAM-PREM-COMM-FOS-4ARM
input_type       : itc
surface          : slp_wsb_* (FOS surfaces)
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : wsb-vnext-tier3
      offer_id      : 6db92066
      plan          : unknown
      geometry      : CES package (resolved via merchandising API de-discounted + ID scan)
      special_config : WAM Premium champion; wsb-vnext-tier3-disc (discounted variant) NOT a standalone curated offer — de-discounts to wsb-vnext-tier3; disc15278 is existing production code — new experiment codes required for all 4 arms
      rows:
        - product_name  : WAM Premium (Website + Marketing)
          pfid_new      : 970463
          pfid_renewal  : 970463
          term          : annual 1yr
          tier          : tier3 (premium)
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : disc15278 (existing; replace with new code for experiment arms)
    - package_name  : vnext-i18nox-tier4
      offer_id      : bc817604
      plan          : unknown
      geometry      : CES package (resolved via merchandising match, High confidence)
      special_config : WAM Commerce champion; Titan Email international variant — confirm vs wsb-vnext-tier4 for US Commerce
      rows:
        - product_name  : WAM Commerce
          pfid_new      : 970473
          pfid_renewal  : 970473
          term          : annual 1yr
          tier          : tier4 (commerce)
          otc           : N
          free_product  : N
          existing_pkg  : Y
          discount_code : unknown
    - package_name  : TBD (challenger)
      offer_id      : none (NET-NEW BUILD required)
      geometry      : N/A — no standalone CES offer exists for TrustedSite
      special_config : TrustedSite add-on — 0 keyword matches in 1,200 IDs; no standalone offer in catalog or merchandising API; listed as availableAddon in WAM product schema (onetime=false); PNL line = Strategic Partnerships AC (not WAM); cross-PNL-line bundle requires approval; monthly-only billing (annual needed for bundle)
      rows:
        - product_name  : TrustedSite
          pfid_new      : 1834961
          pfid_renewal  : 1834961
          term          : annual (monthly-only in billing)
          tier          : add-on
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : TrustedSite
          pfid_new      : 1834962
          pfid_renewal  : 1834962
          term          : annual
          tier          : add-on
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
  geo              : global (new customers only)
  m365_component   : 575a7d2a-d1ef-40f2-a7e5-dbcc09c20391, plan emailEssentialsEe (confirmed in related runs)
  titan_component  : 927a9d45-7c5b-4652-ad68-d5cd9be75028, plan personalTitan (confirmed in related runs)

ticket_ready:
  rows:
    - product_name  : WAM Premium
      pfid_new      : 970463
      pfid_renewal  : 970463
      term          : annual 1yr
      tier          : tier3
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : TBD (new experiment code required)
    - product_name  : WAM Commerce
      pfid_new      : 970473
      pfid_renewal  : 970473
      term          : annual 1yr
      tier          : tier4
      otc           : N
      free_product  : N
      existing_pkg  : Y
      discount_code : TBD (new experiment code required)
    - product_name  : TrustedSite
      pfid_new      : 1834961
      pfid_renewal  : 1834961
      term          : annual
      tier          : add-on
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N

---

## CMS-31766

case_id          : CMS-31766
input_type       : jira_ticket
surface          : slp_ssl / ssl-config (CES-only per architectural constraint)
path_type        : CES
reliability      : stable
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : TBD (challenger)
      offer_id      : none (NET-NEW BUILD — no existing CES package for these PFIDs)
      geometry      : N/A
      special_config : NES reference offer sslcert-managed-with-monitoring (offerId 28e5b730-4e70-46b0-8672-6e18a17f81a1, plan managedWithMonitoring) exists but is NES-only — NOT a valid CES clone source; also aliases as ssl-001sites-managed-tier1 (plan=managed, same offerId); slug format mismatch — ticket uses "offer-sslcert-managedWithMonitoring" (non-standard), catalog uses "sslcert-managed-with-monitoring" (kebab-case, no prefix); direct lookup of ticket slug fails
      rows:
        - product_name  : Managed SSL + Malware Monitoring (1yr)
          pfid_new      : 1840827
          pfid_renewal  : 1840827
          term          : 1 Year
          tier          : managed
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : Managed SSL + Malware Monitoring (2yr)
          pfid_new      : 1840829
          pfid_renewal  : 1840829
          term          : 2 Year
          tier          : managed
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : Managed SSL + Malware Monitoring (3yr)
          pfid_new      : 1840831
          pfid_renewal  : 1840831
          term          : 3 Year
          tier          : managed
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : Managed SSL + Malware Monitoring (4yr)
          pfid_new      : 1840833
          pfid_renewal  : 1840833
          term          : 4 Year
          tier          : managed
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : Managed SSL + Malware Monitoring (5yr)
          pfid_new      : 1840835
          pfid_renewal  : 1840835
          term          : 5 Year
          tier          : managed
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
  geo              : global (not specified in ticket)
  nes_reference    : sslcert-managed-with-monitoring, offerId 28e5b730, plan managedWithMonitoring, Rev 1 (created 2026-04-23) — skill must surface this as NES reference even though it cannot serve as CES clone source
  slug_convention  : ssl-001sites-managed-with-monitoring-tier1 (recommended CES slug following existing naming pattern)

ticket_ready:
  rows:
    - product_name  : Managed SSL + Malware Monitoring (1yr)
      pfid_new      : 1840827
      pfid_renewal  : 1840827
      term          : 1 Year
      tier          : managed
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
    - product_name  : Managed SSL + Malware Monitoring (2yr)
      pfid_new      : 1840829
      pfid_renewal  : 1840829
      term          : 2 Year
      tier          : managed
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
    - product_name  : Managed SSL + Malware Monitoring (3yr)
      pfid_new      : 1840831
      pfid_renewal  : 1840831
      term          : 3 Year
      tier          : managed
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
    - product_name  : Managed SSL + Malware Monitoring (4yr)
      pfid_new      : 1840833
      pfid_renewal  : 1840833
      term          : 4 Year
      tier          : managed
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
    - product_name  : Managed SSL + Malware Monitoring (5yr)
      pfid_new      : 1840835
      pfid_renewal  : 1840835
      term          : 5 Year
      tier          : managed
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N

---

## CMS-32651

case_id          : CMS-32651
input_type       : jira_ticket
surface          : unknown (OrderShim/SAPI not a standard ITC; Email Backup billing appears via app_o365_* / mgr_slp_365_* / upp_o365product_* ITCs — not cart_* or sapi_*)
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : AMBIGUOUS — clone source o365backup does not exist in catalog or merchandising API
      offer_id      : AMBIGUOUS — (A) office365-tier*-backup: offerId 092a9528, no existing discount | (B) email-*-backup family: offerId 575a7d2a, existing disc209800 (conflicts with new disc004590)
      geometry      : Standalone (both candidate families)
      special_config : PFID 996667 appears only as addon inside standard M365 packages in merchandising API — no standalone backup CES package; all existing backup curated offers (email-*-backup) use disc209800, not disc004590; ecomm must confirm clone source and resolve discount conflict before ticket can be filed
      rows:
        - product_name  : Email Backup (Microsoft 365 branded, new purchase)
          pfid_new      : 996667
          pfid_renewal  : 996668
          term          : monthly 1mo
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : disc004590 (new; not in billing history)
        - product_name  : Email Backup (non-M365 renewal)
          pfid_new      : 1499849
          pfid_renewal  : 1499849
          term          : monthly 1mo
          tier          : standalone
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : disc004590 (new)
  geo              : unknown (not specified in ticket)
  candidate_families:
    - family       : office365-tier*-backup (office365-tier0-backup, office365-tier1-backup, office365-tier3-backup)
      offer_id     : 092a9528
      discount     : none existing
    - family       : email-*-backup (email-business-essentials-backup, email-essentials-aes-backup, email-plus-backup)
      offer_id     : 575a7d2a
      discount     : disc209800 (existing — conflicts with requested disc004590)

ticket_ready:
  rows:
    - product_name  : Email Backup (new)
      pfid_new      : 996667
      pfid_renewal  : 996668
      term          : monthly 1mo
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : disc004590
    - product_name  : Email Backup (non-M365 renewal)
      pfid_new      : 1499849
      pfid_renewal  : 1499849
      term          : monthly 1mo
      tier          : standalone
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : disc004590

---

## TRUSTEDSITE-DPP-MODIFY

case_id          : TRUSTEDSITE-DPP-MODIFY
input_type       : itc
surface          : dpp_precheck
path_type        : CES
reliability      : volatile
date_added       : 2026-05-15

expected:
  packages:
    - package_name  : TBD (challenger)
      offer_id      : none (no standalone TrustedSite CES offer exists)
      geometry      : N/A
      special_config : Offer Operation = Modify (Add Component); all three CES chain steps failed: Step 1 merchandising no match for PFIDs 1834961/1834962 (CONFIRMED_NO_MATCH); Step 2 zero keyword matches in 1,200 IDs for "trustedsite"; Step 3 API error (AvailabilityServiceInternalError); two-step ticket required: Step 1 = engineer standalone TrustedSite CES offer, Step 2 = wire TrustedSite into all 7 existing dpp_precheck CES packages
      existing_packages_requiring_modification:
        - vnext-i18no365-tier2-precheck
        - vnext-i18nox-tier1-precheck
        - vnext-i18nox-tier3-precheck
        - vnext-i18nox-tier4-precheck
        - wsb-vnext-tier1
        - wsb-vnext-tier3
        - wsb-vnext-tier4
      rows:
        - product_name  : TrustedSite
          pfid_new      : 1834961
          pfid_renewal  : 1834961
          term          : annual (monthly-only in billing; annual needed for bundle)
          tier          : add-on
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
        - product_name  : TrustedSite
          pfid_new      : 1834962
          pfid_renewal  : 1834962
          term          : annual
          tier          : add-on
          otc           : N
          free_product  : N
          existing_pkg  : N
          discount_code : N
  geo              : global
  idc_billing_gap  : 7-day billing window returned 0 rows for PFIDs 1834961/1834962 on dpp_precheck — low volume or not yet wired to surface; dpp-solution-set scope unclear

ticket_ready:
  rows:
    - product_name  : TrustedSite
      pfid_new      : 1834961
      pfid_renewal  : 1834961
      term          : annual
      tier          : add-on
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
    - product_name  : TrustedSite
      pfid_new      : 1834962
      pfid_renewal  : 1834962
      term          : annual
      tier          : add-on
      otc           : N
      free_product  : N
      existing_pkg  : N
      discount_code : N
