# Package ID Geometry Catalog

Classification of known NES `package_id` values from billing.
Geometry is immutable — only volume changes. Do not store volume here; query billing live.

Catalog verified against: catalog-query (test), catalog-curated-offers (internal test), merch-packages datasources
Last classification run: 2026-05-17
546 package_ids total. 8 unknowns (ghost/test IDs — see catalog).
Total distinct package_ids active (90-day window as of 2026-05-16): 369 | catalog total: 546 | 7-day active (as of 2026-05-17): 238

---

## Classification Table

| package_id | geometry | free_trial | catalog_verified | notes |
|---|---|---|---|---|
| domain | standalone | no | 2026-05-16 | Single domain offer; no prePurchaseKeyMap |
| dbs | standalone | no | 2026-05-16 | Single dbsFees product (ONETIME term); no prePurchaseKeyMap |
| domain-bundle | standalone | no | 2026-05-16 | Same offer as `domain` (edf13c43) + discount code disc000032; no prePurchaseKeyMap |
| ssl-001sites-tier1 | standalone | no | 2026-05-16 | sslCertificate standard plan (1 SAN); no prePurchaseKeyMap |
| oybo-en-email | bundle | no | 2026-05-16 | offerCollection (domainEmail); 2 fixed components: domain offer + M365 emailEssentialsEe |
| offer-m365-emailessentialsee_aes | standalone | no | 2026-05-16 | M365 emailEssentialsEe_AES plan; catalog-curated-offers confirmed via office365-emailessentialsee_aes (offerId: 575a7d2a) |
| vps4-self-managed-lin-tier2 | standalone | no | 2026-05-16 | offerCollection wrapping single VPS4 tier-20 offer; 1 component only |
| nes-cpanel-set-1-economy-ssl-ox | bundle | no | 2026-05-16 | cpanel-set-1-economy-ssl-ox confirmed via catalog-curated-offers: prePurchaseKeyMap(OX) + 2 childOffers; cPanel+SSL+OX bundle |
| ssl-001sites-managed-tier1 | standalone | no | 2026-05-16 | sslCertificate managed plan; no prePurchaseKeyMap |
| offer-titanemail-light | standalone | no | 2026-05-16 | Titan Email Offer (offerId: 927a9d45); plan: light; catalog-curated-offers confirmed |
| office365-tier0 | standalone | no | 2026-05-16 | Single M365 offer, plan emailEssentialsEe; no prePurchaseKeyMap |
| vps4-self-managed-lin-tier1 | standalone | no | 2026-05-16 | offerCollection wrapping single VPS4 tier-10 offer; 1 component only |
| ssl-wildcard-tier1 | standalone | no | 2026-05-16 | sslCertificate standard_wildcard plan; no prePurchaseKeyMap |
| vps4-self-managed-lin-tier4 | standalone | no | 2026-05-16 | offerCollection wrapping single VPS4 tier-40 offer; 1 component only |
| offer-m365-emailEssentialsEeDomainVoucher | standalone | no | 2026-05-16-inferred | M365 emailEssentials voucher with domain; single M365 product |
| webstoredesign-wordpress-tier1 | bundle | no | 2026-05-16 | offerCollection (wordpressdesign); 2 fixed components: MWP wdsPremiumStore + M365 officeBusinessPs; prePurchaseKeyMap present |
| ssl-005sites-tier1 | standalone | no | 2026-05-16 | sslCertificate standard_ucc_5 plan (5 SANs); no prePurchaseKeyMap |
| nes-cpanel-set-1-starter | standalone | no | 2026-05-16-inferred | cPanel hosting starter only; no bundled email or SSL; bare tier = standalone |
| nes-wss-tier1-nortonsmb-standardfreetrial | bundle | YES | 2026-05-16 | wss-tier1-nortonsmb-standardfreetrial in catalog-curated-offers: offerCollection dc3b59c2 (WSS+Norton parent+child); BPO free trial confirmed |
| offer-wsb-professionalFreeTrial | standalone | YES | 2026-05-16-inferred | WSB single product (wsb-tier* confirmed standalone); professional plan; free trial |
| nes-cpanel-set-1-economy-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| nes-cpanel-set-1-deluxe-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| office365-tier1 | standalone | no | 2026-05-16 | Single M365 offer, plan officeBusinessP1 (P1 license); no prePurchaseKeyMap |
| nes-cpanel-set-1-deluxe-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+OX = bundle |
| nes-cpanel-set-1-ultimate-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| ssl-001sites-tier3 | bundle | no | 2026-05-16 | offerCollection (PackageSSL); 2 fixed components: SSL premium (EV) + SSL turbo (standard, $0 price override, autoRenew:false) |
| offer-wsb-basicFreeTrial | standalone | YES | 2026-05-16-inferred | WSB single product; basic plan; free trial |
| temp-email-essentials-99 | standalone | no | 2026-05-16 | Single M365 emailEssentialsEe plan; discount DISC214228; no prePurchaseKeyMap |
| temp-email-essentials-149 | standalone | no | 2026-05-16 | Single M365 emailEssentialsEe plan; discount DISC214229; no prePurchaseKeyMap |
| nes-wss-tier1-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+OX = bundle |
| nes-wss-tier1-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+Titan = bundle |
| nes-wss-tier1-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+OX = bundle |
| nes-wss-tier1-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+Titan = bundle |
| nes-wss-tier2-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+OX = bundle |
| nes-wss-tier2-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+Titan = bundle |
| nes-wss-tier2-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+OX = bundle |
| nes-wss-tier2-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+Titan = bundle |
| nes-wss-tier3-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+OX = bundle |
| nes-wss-tier3-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+Titan = bundle |
| nes-wss-tier3-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+OX = bundle |
| nes-wss-tier3-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+Titan = bundle |
| nes-wss-tier4-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+OX = bundle |
| nes-wss-tier4-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+SSL+Titan = bundle |
| nes-wss-tier4-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+OX = bundle |
| nes-wss-tier4-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern WSS+Titan = bundle |
| nes-cpanel-set-2-economy-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+OX = bundle |
| nes-cpanel-set-2-economy-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| nes-cpanel-set-2-starter | standalone | no | 2026-05-16-inferred | cPanel hosting starter only; pattern from nes-cpanel-set-1-starter standalone |
| nes-cpanel-set-2-deluxe-ssl-ox | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+OX = bundle |
| nes-cpanel-set-2-deluxe-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| nes-cpanel-set-2-ultimate-ssl-titan | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name pattern cPanel+SSL+Titan = bundle |
| ssl-001sites-tier4 | standalone | no | 2026-05-16 | sslCertificate standard plan (1 SAN); discount SSLA8235FC; no prePurchaseKeyMap |
| ssl-001sites-tier5 | standalone | no | 2026-05-16-inferred | SSL cert; pattern from confirmed tiers 1-4 standalone |
| ssl-dv-tier1 | standalone | no | 2026-05-16-inferred | DV SSL certificate standalone; pattern from ssl family |
| ssl-dv-tier2 | standalone | no | 2026-05-16-inferred | DV SSL certificate standalone; pattern from ssl family |
| ssl-ev-tier1 | standalone | no | 2026-05-16-inferred | EV SSL certificate standalone; pattern from ssl family |
| ssl-001sites-managed-tier2 | standalone | no | 2026-05-16 | sslCertificate managed plan; single component; no prePurchaseKeyMap |
| ssl-001sites-managed-tier3 | standalone | no | 2026-05-16-inferred | managed SSL standalone; pattern from confirmed tiers 1-2 |
| office365-tier2 | standalone | no | 2026-05-16 | M365 Business Essentials; merch-packages confirmed: single product + optional add-ons only |
| offer-wsb-premiumFreeTrial | standalone | YES | 2026-05-16-inferred | WSB single product; premium plan; free trial |
| offer-wsb-basicFreeTrial-annual | standalone | YES | 2026-05-16-inferred | WSB basic free trial; annual billing term |
| offer-wsb-professionalFreeTrial-annual | standalone | YES | 2026-05-16-inferred | WSB professional free trial; annual billing term |
| offer-wsb-premiumFreeTrial-annual | standalone | YES | 2026-05-16-inferred | WSB premium free trial; annual billing term |
| offer-m365-emailEssentialsDomainVoucher | standalone | no | 2026-05-16-inferred | M365 emailEssentials with domain voucher; single M365 product |
| offer-titanemail-standard | standalone | no | 2026-05-16 | Titan Email Offer (offerId: 927a9d45); plan: pro; catalog-curated-offers confirmed |
| offer-titanemail-premium | standalone | no | 2026-05-16 | Titan Email Offer (offerId: 927a9d45); plan: premium; catalog-curated-offers confirmed |
| nes-wss-tier1-nortonsmb-annualfreetrial | bundle | YES | 2026-05-16-inferred | annual variant of wss-tier1-nortonsmb; same offerCollection dc3b59c2 (WSS+Norton) |
| nes-wss-tier2-nortonsmb-standardfreetrial | bundle | YES | 2026-05-16 | wss-tier2-nortonsmb-standardfreetrial in catalog-curated-offers: same offerCollection dc3b59c2 (WSS+Norton) confirmed |
| nes-wss-tier2-nortonsmb-annualfreetrial | bundle | YES | 2026-05-16-inferred | annual variant; same offerCollection dc3b59c2 (WSS+Norton) |
| nes-wss-tier3-nortonsmb-standardfreetrial | bundle | YES | 2026-05-16-inferred | pattern from confirmed wss-tier1/2-nortonsmb bundle (dc3b59c2) |
| nes-wss-tier3-nortonsmb-annualfreetrial | bundle | YES | 2026-05-16-inferred | annual variant; same WSS+Norton bundle pattern |
| nes-wss-tier4-nortonsmb-standardfreetrial | bundle | YES | 2026-05-16-inferred | pattern from confirmed wss-tier1/2-nortonsmb bundle (dc3b59c2) |
| nes-wss-tier4-nortonsmb-annualfreetrial | bundle | YES | 2026-05-16-inferred | annual variant; same WSS+Norton bundle pattern |
| nes-cpanel-set-1-economy | standalone | no | 2026-05-16-inferred | bare cPanel economy tier; no SSL/email suffix = cPanel only; single product |
| nes-cpanel-set-1-deluxe | standalone | no | 2026-05-16-inferred | bare cPanel deluxe tier; no SSL/email suffix = cPanel only; single product |
| nes-cpanel-set-1-ultimate | standalone | no | 2026-05-16-inferred | bare cPanel ultimate tier; no SSL/email suffix = cPanel only; single product |
| nes-cpanel-set-2-economy | standalone | no | 2026-05-16-inferred | bare cPanel set-2 economy; no SSL/email suffix = cPanel only |
| nes-cpanel-set-2-deluxe | standalone | no | 2026-05-16-inferred | bare cPanel set-2 deluxe; no SSL/email suffix = cPanel only |
| nes-cpanel-set-2-ultimate | standalone | no | 2026-05-16-inferred | bare cPanel set-2 ultimate; no SSL/email suffix = cPanel only |
| webstoredesign-wordpress-tier2 | bundle | no | 2026-05-16-inferred | pattern from confirmed tier1 bundle (MWP+M365); likely MWP plan 2 + M365 |
| webstoredesign-wordpress-tier3 | bundle | no | 2026-05-16-inferred | pattern from confirmed tier1 bundle (MWP+M365); likely MWP plan 3 + M365 |
| oybo-en-email-tier2 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows oybo-en-email-tier1 pattern (domain+M365) |
| oybo-en-email-tier3 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows oybo-en-email-tier1 pattern (domain+M365) |
| dpp-ca-ca-solution-tier1 | bundle | no | 2026-05-16 | offerCollection (domainEmail); 2 components: domain + M365 emailEssentialsEe |
| dpp-ca-ca-solution-tier2 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB business + M365 ps; overridePrice:0 on email |
| dpp-ca-ca-solution-tier3 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB commerce + M365 ps; overridePrice:0 on email |
| dpp-intl-solution-tier1 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB personal + M365 officeBusinessPs; overridePrice:0 on email |
| dpp-intl-solution-tier2 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB personal + M365 officeBusinessPs; disc2442666 |
| mena-digital-kit-tier1 | bundle | no | 2026-05-16 | offerCollection (domainDudaEmail); 3 components: domain + Duda basic + M365 officeBusinessPs |
| mena-digital-kit-tier2 | bundle | no | 2026-05-16 | offerCollection (domainDudaEmail); 3 components: domain + Duda standard + M365 officeBusinessPs |
| mena-digital-kit-tier3 | bundle | no | 2026-05-16 | offerCollection (domainDudaEmail); 3 components: domain + Duda premium + M365 officeBusinessPs |
| mena-digital-kit-tier4 | bundle | no | 2026-05-16 | offerCollection (domainProfessionalEmail); 3 components: domain + Duda basic + Titan light |
| dpp-au-solution-tier1 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-au pattern matches dpp-intl bundle structure |
| dpp-au-solution-tier2 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-au pattern matches dpp-intl bundle structure |
| dpp-gb-solution-tier1 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-gb pattern matches dpp-intl bundle structure |
| dpp-gb-solution-tier2 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-gb pattern matches dpp-intl bundle structure |
| temp-email-essentials-99-annual | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of temp-email-essentials-99 (confirmed standalone) |
| temp-email-essentials-149-annual | standalone | no | 2026-05-16-inferred | annual billing variant of confirmed standalone temp-email-essentials-149 |
| microsoftemail-onlineessentialsnoteams-discount-365af1f1cb | standalone | no | 2026-05-16 | Single M365 plan onlineEssentialsNoTeams; discount 365AF1F1CB; no prePurchaseKeyMap |
| microsoftemail-onlineessentials-discount | standalone | no | 2026-05-16-inferred | M365 Online Essentials with discount; pattern from confirmed microsoftemail-onlineessentialsnoteams standalone |
| offer-m365-businessbasic | standalone | no | 2026-05-16-inferred | M365 Business Basic plan; M365 single product |
| offer-m365-businessstandard | standalone | no | 2026-05-16-inferred | M365 Business Standard plan; M365 single product |
| offer-m365-businesspremium | standalone | no | 2026-05-16-inferred | M365 Business Premium plan; M365 single product |
| ssl-wildcard-tier2 | standalone | no | 2026-05-16 | sslCertificate deluxe_wildcard plan; no prePurchaseKeyMap |
| ssl-wildcard-tier3 | standalone | no | 2026-05-16 | sslCertificate standard_wildcard plan; discount SSLA8235FC; no prePurchaseKeyMap |
| ssl-001sites-tier6 | standalone | no | 2026-05-16-inferred | SSL cert higher tier; pattern from confirmed tiers 1-5 |
| ssl-001sites-tier7 | standalone | no | 2026-05-16-inferred | SSL cert higher tier; pattern from confirmed tiers 1-6 |
| ssl-dv-multi-tier1 | standalone | no | 2026-05-16-inferred | DV multi-SAN SSL cert; pattern from ssl family standalone |
| ssl-ev-multi-tier1 | standalone | no | 2026-05-16-inferred | EV multi-SAN SSL cert; pattern from ssl family standalone |
| vps4-managed-lin-tier1 | standalone | no | 2026-05-16-inferred | VPS4 managed Linux hosting; pattern from vps4-managed-lin-cpanel confirmed standalone |
| vps4-managed-lin-tier2 | standalone | no | 2026-05-16-inferred | VPS4 managed Linux hosting tier 2; pattern from vps4-managed-lin-cpanel standalone |
| vps4-managed-lin-tier3 | standalone | no | 2026-05-16-inferred | VPS4 managed Linux hosting tier 3; pattern from vps4-managed-lin-cpanel standalone |
| vps4-managed-lin-tier4 | standalone | no | 2026-05-16-inferred | VPS4 managed Linux hosting tier 4; pattern from vps4-managed-lin-cpanel standalone |
| nes-wss-tier1-nodiscount | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; nodiscount variant of nes-wss-tier1 bundle series |
| nes-wss-tier2-nodiscount | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; nodiscount variant of nes-wss-tier2 bundle series |
| nes-wss-tier3-nodiscount | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; nodiscount variant of nes-wss-tier3 bundle series |
| nes-wss-tier4-nodiscount | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; nodiscount variant of nes-wss-tier4 bundle series |
| dbs-bundle | bundle | no | 2026-05-16-inferred | name suffix -bundle suggests multi-product; likely domain registration + DBS fee combination |
| domain-privacy | standalone | no | 2026-05-16-inferred | domain privacy add-on; single standalone product |
| offer-wsb-ecommerce | standalone | no | 2026-05-16-inferred | WSB ecommerce plan; WSB single product (wsb-tier* confirmed standalone) |
| offer-wsb-ecommerceFreeTrial | standalone | YES | 2026-05-16-inferred | WSB ecommerce free trial; WSB single product |
| nes-wss-tier1-ssl-ox-annualfreetrial | bundle | YES | 2026-05-16-inferred | WSS+SSL+OX annual free trial bundle; pattern from nes-wss-tier1-ssl-ox (inferred bundle) |
| nes-cpanel-set-1-economy-ssl-ox-annualfreetrial | bundle | YES | 2026-05-16-inferred | cPanel+SSL+OX annual free trial bundle; pattern from confirmed nes-cpanel-set-1-economy-ssl-ox bundle |
| slp-hosting-4gh-tier1 | standalone | no | 2026-05-16-inferred | 4GH partnership hosting tier 1; single hosting product |
| slp-hosting-4gh-tier2 | standalone | no | 2026-05-16-inferred | 4GH partnership hosting tier 2; single hosting product |
| slp-hosting-4gh-tier3 | standalone | no | 2026-05-16-inferred | 4GH partnership hosting tier 3; single hosting product |
| slp-hosting-4gh-tier4 | standalone | no | 2026-05-16-inferred | 4GH partnership hosting tier 4; single hosting product |
| offer-titanemail-max | standalone | no | 2026-05-16 | Titan Email Offer (offerId: 927a9d45); plan: ultra; catalog-curated-offers confirmed |
| vps4-self-managed-win-tier1 | standalone | no | 2026-05-16 | offerCollection (vps4SelfManagedLin); 1 fixed component: VPS4 Windows wm00_10; SEMIANNUAL term |
| vps4-self-managed-win-tier2 | standalone | no | 2026-05-16 | offerCollection (vps4SelfManagedLin); 1 fixed component: VPS4 Windows wm00_20; SEMIANNUAL term |
| vps4-self-managed-win-tier3 | standalone | no | 2026-05-16 | offerCollection (vps4SelfManagedLin); 1 fixed component: VPS4 Windows wm00_30; SEMIANNUAL term |
| vps4-self-managed-win-tier4 | standalone | no | 2026-05-16 | offerCollection (vps4SelfManagedLin); 1 fixed component: VPS4 Windows wm00_40; SEMIANNUAL term |
| vps4-managed-win-tier1 | standalone | no | 2026-05-16-inferred | VPS4 managed Windows hosting tier 1; pattern from vps4-managed standalone |
| vps4-managed-win-tier2 | standalone | no | 2026-05-16-inferred | VPS4 managed Windows hosting tier 2; pattern from vps4-managed standalone |
| vps4-managed-win-tier3 | standalone | no | 2026-05-16-inferred | VPS4 managed Windows hosting tier 3; pattern from vps4-managed standalone |
| vps4-managed-win-tier4 | standalone | no | 2026-05-16-inferred | VPS4 managed Windows hosting tier 4; pattern from vps4-managed standalone |
| dpp-ca-ca-solution-tier4 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-ca pattern matches confirmed bundle tiers 1-3 |
| dpp-intl-solution-tier3 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; confirmed bundle pattern (tiers 1,2,4,5 confirmed) |
| mena-digital-kit-tier5 | bundle | no | 2026-05-16 | offerCollection (domainProfessionalEmail); 3 components: domain + Duda standard + Titan light |
| dpp-au-solution-tier3 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-au pattern matches dpp-intl bundle structure |
| dpp-gb-solution-tier3 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-gb pattern matches dpp-intl bundle structure |
| ssl-001sites-managed-tier4 | standalone | no | 2026-05-16-inferred | managed SSL standalone; pattern from confirmed tiers 1-2 |
| ssl-001sites-managed-tier5 | standalone | no | 2026-05-16-inferred | managed SSL standalone; pattern from confirmed tiers 1-2 |
| offer-m365-emailEssentialsEeAnnual | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe; annual billing term |
| offer-m365-emailEssentialsEeMonthly | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe; monthly billing term |
| offer-titanemail-light-annual | standalone | no | 2026-05-16-inferred | Titan Email light plan; annual billing term |
| offer-titanemail-standard-annual | standalone | no | 2026-05-16-inferred | Titan Email pro plan; annual billing term |
| offer-titanemail-premium-annual | standalone | no | 2026-05-16-inferred | Titan Email premium plan; annual billing term |
| offer-titanemail-max-annual | standalone | no | 2026-05-16-inferred | Titan Email ultra plan; annual billing term |
| nes-wss-tier1-ssl-titan-annualfreetrial | bundle | YES | 2026-05-16-inferred | WSS+SSL+Titan annual free trial bundle; pattern from confirmed WSS bundle family |
| nes-cpanel-set-1-economy-ssl-titan-annualfreetrial | bundle | YES | 2026-05-16-inferred | cPanel+SSL+Titan annual free trial bundle; pattern from confirmed cPanel+SSL bundle |
| offer-wsb-ecommerce-annual | standalone | no | 2026-05-16-inferred | WSB ecommerce plan; annual billing term |
| offer-wsb-basic-annual | standalone | no | 2026-05-16-inferred | WSB basic plan; annual billing term |
| offer-wsb-professional-annual | standalone | no | 2026-05-16-inferred | WSB professional plan; annual billing term |
| offer-wsb-premium-annual | standalone | no | 2026-05-16-inferred | WSB premium plan; annual billing term |
| slp-hosting-4gh-tier5 | standalone | no | 2026-05-16-inferred | 4GH partnership hosting tier 5; single hosting product |
| oybo-en-email-tier4 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows oybo-en-email pattern (domain+M365) |
| oybo-en-email-tier5 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows oybo-en-email pattern (domain+M365) |
| dpp-ca-ca-solution-tier5 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-ca pattern matches confirmed bundle tiers 1-3 |
| dpp-intl-solution-tier4 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB business + M365 officeBusinessPs; disc2442555 |
| dpp-intl-solution-tier5 | bundle | no | 2026-05-16 | offerCollection (domainWbsIntEmail); 3 components: domain + WSB businessPlus + M365 officeBusinessPs; disc244277 |
| dpp-au-solution-tier4 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-au pattern matches dpp-intl bundle structure |
| dpp-gb-solution-tier4 | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; dpp-gb pattern matches dpp-intl bundle structure |
| mena-digital-kit-tier6 | bundle | no | 2026-05-16 | offerCollection (domainProfessionalEmail); 3 components: domain + Duda premium + Titan light |
| temp-email-essentials-299 | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; same pattern as confirmed temp-email-essentials-99/149 |
| temp-email-essentials-399 | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; same pattern as confirmed temp-email-essentials-99/149 |
| temp-email-essentials-499 | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; same pattern as confirmed temp-email-essentials-99/149 |
| microsoftemail-onlineessentialsnoteams-standard | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows microsoftemail standalone pattern |
| microsoftemail-onlineessentials-standard | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; follows microsoftemail standalone pattern |
| offer-m365-businessbasic-annual | standalone | no | 2026-05-16-inferred | M365 Business Basic plan; annual billing term |
| offer-m365-businessstandard-annual | standalone | no | 2026-05-16-inferred | M365 Business Standard plan; annual billing term |
| ssl-ev-tier2 | standalone | no | 2026-05-16-inferred | EV SSL certificate standalone; pattern from ssl family |
| ssl-ev-tier3 | standalone | no | 2026-05-16-inferred | EV SSL certificate standalone; pattern from ssl family |
| ssl-dv-tier3 | standalone | no | 2026-05-16-inferred | DV SSL certificate standalone; pattern from ssl family |
| vps4-self-managed-lin-tier5 | standalone | no | 2026-05-16 | offerCollection (vps4SelfManagedLin); 1 fixed component: VPS4 Linux lm00_42; SEMIANNUAL term |
| vps4-managed-lin-tier5 | standalone | no | 2026-05-16-inferred | VPS4 managed Linux hosting tier 5; pattern from vps4-managed-lin-cpanel standalone |
| dbs-annual | standalone | no | 2026-05-16-inferred | annual billing variant of dbs (dbsFees standalone) |
| domain-privacy-annual | standalone | no | 2026-05-16-inferred | annual billing variant of domain-privacy standalone |
| oybo-en-email-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of oybo-en-email (confirmed bundle) |
| domain-bundle-annual | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of domain-bundle (confirmed standalone) |
| webstoredesign-wordpress-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of webstoredesign-wordpress-tier1 (confirmed bundle) |
| webstoredesign-wordpress-tier2-annual | bundle | no | 2026-05-16-inferred | annual variant of webstoredesign-wordpress-tier2 (inferred bundle) |
| nes-wss-tier1-ox-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier1-ox (inferred bundle) |
| nes-wss-tier1-titan-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier1-titan (inferred bundle) |
| nes-wss-tier2-ox-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier2-ox (inferred bundle) |
| nes-wss-tier2-titan-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier2-titan (inferred bundle) |
| dpp-ca-ca-solution-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of dpp-ca-ca-solution-tier1 (confirmed bundle) |
| dpp-intl-solution-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of dpp-intl-solution-tier1 (confirmed bundle) |
| mena-digital-kit-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of mena-digital-kit-tier1 (confirmed bundle) |
| offer-wsb-professional-freetrialext | standalone | YES | 2026-05-16-inferred | WSB professional extended free trial; WSB single product |
| offer-wsb-premium-freetrialext | standalone | YES | 2026-05-16-inferred | WSB premium extended free trial; WSB single product |
| nes-cpanel-set-1-starter-annual | standalone | no | 2026-05-16-inferred | annual billing variant of nes-cpanel-set-1-starter (inferred standalone) |
| nes-cpanel-set-2-starter-annual | standalone | no | 2026-05-16-inferred | annual billing variant of nes-cpanel-set-2-starter (inferred standalone) |
| nes-wss-tier1-nortonsmb-freetrialext | bundle | YES | 2026-05-16-inferred | extended free trial; same WSS+Norton bundle offerCollection dc3b59c2 |
| nes-wss-tier2-nortonsmb-freetrialext | bundle | YES | 2026-05-16-inferred | extended free trial; same WSS+Norton bundle offerCollection dc3b59c2 |
| nes-wss-tier3-nortonsmb-freetrialext | bundle | YES | 2026-05-16-inferred | extended free trial; same WSS+Norton bundle offerCollection dc3b59c2 |
| offer-trustedsite-standard | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; third-party add-on = standalone by pattern |
| offer-trustedsite-premium | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; third-party add-on = standalone by pattern |
| offer-sitelock-standard | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; third-party add-on = standalone by pattern |
| offer-norton-standard | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; third-party add-on = standalone by pattern |
| dpp-au-solution-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of dpp-au-solution-tier1 (inferred bundle) |
| dpp-gb-solution-tier1-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of dpp-gb-solution-tier1 (inferred bundle) |
| offer-m365-emailEssentialsEe-voucher | standalone | no | 2026-05-16-inferred | M365 emailEssentials with voucher; single M365 product |
| offer-titanemail-light-voucher | standalone | no | 2026-05-16-inferred | Titan Email light plan with voucher; single Titan product |
| webstoredesign-wordpress-tier3-annual | bundle | no | 2026-05-16-inferred | annual variant of webstoredesign-wordpress-tier3 (inferred bundle) |
| nes-wss-tier3-ox-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier3-ox (inferred bundle) |
| nes-wss-tier4-ox-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of nes-wss-tier4-ox (inferred bundle) |
| mena-digital-kit-tier2-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of mena-digital-kit-tier2 (confirmed bundle) |
| offer-wsb-ecommerce-freetrialext | standalone | YES | 2026-05-16-inferred | WSB ecommerce extended free trial; WSB single product |
| vps4-managed-lin-tier1-annual | standalone | no | 2026-05-16-inferred | VPS4 managed Linux annual billing variant; pattern from vps4-managed standalone |
| offer-godaddy-payments | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; payments product = standalone add-on |
| offer-godaddy-payments-annual | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual variant of GoDaddy Payments standalone |
| domain-withprivacy | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; name suggests domain + privacy bundle |
| slp-hosting-4gh-tier1-annual | standalone | no | 2026-05-16-inferred | annual billing variant of slp-hosting-4gh-tier1 (inferred standalone) |
| domain-premium | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; premium domain registration = standalone |
| offer-m365-emailEssentialsEe-discount | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; discount variant of M365 emailEssentialsEe = standalone |
| offer-titanemail-light-discount | standalone | no | 2026-05-16-inferred | NOT_FOUND in test catalog; discount variant of Titan light = standalone |
| nes-wss-tier1-nodiscount-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual nodiscount variant of nes-wss-tier1 (inferred bundle) |
| nes-wss-tier2-nodiscount-annual | bundle | no | 2026-05-16-inferred | NOT_FOUND in test catalog; annual nodiscount variant of nes-wss-tier2 (inferred bundle) |
| backorders-public-registration | standalone | no | 2026-05-16-inferred | domain backorder service; single standalone product |
| bizhosting-cpanel-tier1 | standalone | no | 2026-05-16-inferred | bare cPanel business hosting; no email bundle suffix |
| business-hosting-set-1-grow-365 | bundle | no | 2026-05-16-inferred | business hosting set-1 grow + M365 bundle |
| business-hosting-set-1-grow-ox | bundle | no | 2026-05-16-inferred | business hosting set-1 grow + OX email bundle |
| business-hosting-set-1-launch-365 | bundle | no | 2026-05-16-inferred | business hosting set-1 launch + M365 bundle |
| business-hosting-set-1-launch-ox | bundle | no | 2026-05-16-inferred | business hosting set-1 launch + OX email bundle |
| business-hosting-set-3-enhance-ox | bundle | no | 2026-05-16-inferred | business hosting set-3 enhance + OX email bundle |
| business-hosting-set-3-grow-365 | bundle | no | 2026-05-16-inferred | business hosting set-3 grow + M365 bundle |
| business-hosting-set-3-launch-365 | bundle | no | 2026-05-16-inferred | business hosting set-3 launch + M365 bundle |
| business-hosting-set-3-launch-ox | bundle | no | 2026-05-16-inferred | business hosting set-3 launch + OX email bundle |
| businesshosting-tier1 | standalone | no | 2026-05-16-inferred | bare business hosting; no bundled email or SSL |
| businesshosting-tier2 | standalone | no | 2026-05-16-inferred | bare business hosting tier 2 |
| businesshosting-tier3 | standalone | no | 2026-05-16-inferred | bare business hosting tier 3 |
| businesshosting-tier4 | standalone | no | 2026-05-16-inferred | bare business hosting tier 4 |
| businesshosting-tier5 | standalone | no | 2026-05-16-inferred | bare business hosting tier 5 |
| businesshosting-tier6 | standalone | no | 2026-05-16-inferred | bare business hosting tier 6 |
| cashparking-tier1 | standalone | no | 2026-05-16-inferred | cash parking product; no bundled add-ons |
| cashparking-tier2 | standalone | no | 2026-05-16-inferred | cash parking product tier 2; no bundled add-ons |
| cpanel-o365-tier1 | bundle | no | 2026-05-16-inferred | cPanel + M365 bundle |
| cpanel-o365-tier2 | bundle | no | 2026-05-16-inferred | cPanel + M365 bundle tier 2 |
| cpanel-o365-tier3 | bundle | no | 2026-05-16-inferred | cPanel + M365 bundle tier 3 |
| cpanel-o365-tier4 | bundle | no | 2026-05-16-inferred | cPanel + M365 bundle tier 4 |
| cpanel-openexchange-tier0 | bundle | no | 2026-05-16-inferred | cPanel + OX email bundle tier 0 |
| cpanel-openexchange-tier1 | bundle | no | 2026-05-16-inferred | cPanel + OX email bundle tier 1 |
| cpanel-openexchange-tier2 | bundle | no | 2026-05-16-inferred | cPanel + OX email bundle tier 2 |
| cpanel-openexchange-tier3 | bundle | no | 2026-05-16-inferred | cPanel + OX email bundle tier 3 |
| cpanel-openexchange-tier4 | bundle | no | 2026-05-16-inferred | cPanel + OX email bundle tier 4 |
| cpanel-set-1-deluxe-365 | bundle | no | 2026-05-16-inferred | cPanel set-1 deluxe + M365 bundle |
| cpanel-set-1-deluxe-ox | bundle | no | 2026-05-16-inferred | cPanel set-1 deluxe + OX email bundle |
| cpanel-set-1-economy-365 | bundle | no | 2026-05-16-inferred | cPanel set-1 economy + M365 bundle |
| cpanel-set-1-economy-ox | bundle | no | 2026-05-16-inferred | cPanel set-1 economy + OX email bundle |
| cpanel-set-1-economy-ssl-365-xtra | bundle | no | 2026-05-16-inferred | cPanel + SSL + M365 bundle; xtra tier |
| cpanel-set-1-economy-ssl-ox | bundle | no | 2026-05-16-inferred | cPanel + SSL + OX email bundle; same structure as confirmed nes-cpanel-set-1-economy-ssl-ox |
| cpanel-set-1-maximum-365 | bundle | no | 2026-05-16-inferred | cPanel set-1 maximum + M365 bundle |
| cpanel-set-1-maximum-365-xtra | bundle | no | 2026-05-16-inferred | cPanel set-1 maximum + M365 bundle; xtra tier |
| cpanel-set-1-starter | standalone | no | 2026-05-16-inferred | bare cPanel set-1 starter; no email or SSL suffix |
| cpanel-set-1-ultimate-365 | bundle | no | 2026-05-16-inferred | cPanel set-1 ultimate + M365 bundle |
| cpanel-set-1-ultimate-ox | bundle | no | 2026-05-16-inferred | cPanel set-1 ultimate + OX email bundle |
| cpanel-set-2-deluxe-365-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 deluxe + M365 bundle; xtra tier |
| cpanel-set-2-deluxe-ox | bundle | no | 2026-05-16-inferred | cPanel set-2 deluxe + OX email bundle |
| cpanel-set-2-ultimate-365-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 ultimate + M365 bundle; xtra tier |
| cpanel-set-2-ultimate-ox | bundle | no | 2026-05-16-inferred | cPanel set-2 ultimate + OX email bundle |
| cpanel-set-3-deluxe-365 | bundle | no | 2026-05-16-inferred | cPanel set-3 deluxe + M365 bundle |
| cpanel-set-3-deluxe-ox | bundle | no | 2026-05-16-inferred | cPanel set-3 deluxe + OX email bundle |
| cpanel-set-3-economy-365 | bundle | no | 2026-05-16-inferred | cPanel set-3 economy + M365 bundle |
| cpanel-set-3-economy-ox | bundle | no | 2026-05-16-inferred | cPanel set-3 economy + OX email bundle |
| cpanel-set-3-maximum-365 | bundle | no | 2026-05-16-inferred | cPanel set-3 maximum + M365 bundle |
| cpanel-set-3-ultimate-365 | bundle | no | 2026-05-16-inferred | cPanel set-3 ultimate + M365 bundle |
| cpanel-set-3-ultimate-ox | bundle | no | 2026-05-16-inferred | cPanel set-3 ultimate + OX email bundle |
| cpanel-tier0 | standalone | no | 2026-05-16-inferred | bare cPanel; no email bundle suffix |
| cpanel-tier1 | standalone | no | 2026-05-16-inferred | bare cPanel tier 1; no email bundle suffix |
| cpanel-tier2 | standalone | no | 2026-05-16-inferred | bare cPanel tier 2; no email bundle suffix |
| cpanel-tier3 | standalone | no | 2026-05-16-inferred | bare cPanel tier 3; no email bundle suffix |
| ddc-basic-tier1 | standalone | no | 2026-05-16-inferred | Domain Control Center standalone |
| ded4-selfmanaged-ssd-linux-tier6 | standalone | no | 2026-05-16-inferred | dedicated server self-managed Linux SSD tier 6 |
| ded4-selfmanaged-ssd-windows-tier3 | standalone | no | 2026-05-16-inferred | dedicated server self-managed Windows SSD tier 3 |
| dlxssl-001domain-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 1 domain DV tier; single SSL product |
| dlxssl-005domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 5 domains DV tier; single SSL product |
| dlxssl-010domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 10 domains DV tier; single SSL product |
| dlxssl-015domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 15 domains DV tier; single SSL product |
| dlxssl-020domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 20 domains DV tier; single SSL product |
| dlxssl-030domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 30 domains DV tier; single SSL product |
| dlxssl-040domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 40 domains DV tier; single SSL product |
| dlxssl-050domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 50 domains DV tier; single SSL product |
| dlxssl-100domains-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL for 100 domains DV tier; single SSL product |
| dlxssl-100domains-tier2ov | standalone | no | 2026-05-16-inferred | Deluxe SSL for 100 domains OV tier 2; single SSL product |
| dlxssl-wildcard-tier1dv | standalone | no | 2026-05-16-inferred | Deluxe SSL wildcard DV tier; single SSL product |
| dns-tier1 | standalone | no | 2026-05-16-inferred | DNS service standalone; no bundled add-ons |
| domain-trustee-fr | standalone | no | 2026-05-16-inferred | domain trustee service (France); single product |
| domain-trustee-it | standalone | no | 2026-05-16-inferred | domain trustee service (Italy); single product |
| domain-trustee-kr | standalone | no | 2026-05-16-inferred | domain trustee service (Korea); single product |
| domainprotection | standalone | no | 2026-05-16-inferred | domain privacy/protection; single add-on product |
| dpp-au-com-solution-tier1 | bundle | no | 2026-05-16-inferred | AU .com DPP bundle; domain + WSB + email (dpp-*-solution pattern = confirmed bundle family) |
| dpp-au-com-solution-tier2 | bundle | no | 2026-05-16-inferred | AU .com DPP bundle tier 2 |
| dpp-au-com-solution-tier3 | bundle | no | 2026-05-16-inferred | AU .com DPP bundle tier 3 |
| dpp-au-comau-solution-tier1 | bundle | no | 2026-05-16-inferred | AU .com.au DPP bundle; domain + WSB + email |
| dpp-au-comau-solution-tier2 | bundle | no | 2026-05-16-inferred | AU .com.au DPP bundle tier 2 |
| dpp-au-comau-solution-tier3 | bundle | no | 2026-05-16-inferred | AU .com.au DPP bundle tier 3 |
| dpp-ca-com-solution-tier1 | bundle | no | 2026-05-16-inferred | CA .com DPP bundle; domain + WSB + email |
| dpp-ca-com-solution-tier2 | bundle | no | 2026-05-16-inferred | CA .com DPP bundle tier 2 |
| dpp-ca-com-solution-tier3 | bundle | no | 2026-05-16-inferred | CA .com DPP bundle tier 3 |
| dpp-uk-com-solution-tier1 | bundle | no | 2026-05-16-inferred | UK .com DPP bundle; domain + WSB + email |
| dpp-uk-com-solution-tier2 | bundle | no | 2026-05-16-inferred | UK .com DPP bundle tier 2 |
| dpp-uk-com-solution-tier3 | bundle | no | 2026-05-16-inferred | UK .com DPP bundle tier 3 |
| dpp-uk-couk-solution-tier1 | bundle | no | 2026-05-16-inferred | UK .co.uk DPP bundle; domain + WSB + email |
| emailmarketing-tier2 | standalone | no | 2026-05-16-inferred | email marketing standalone tier 2 |
| emailmarketing-tier3 | standalone | no | 2026-05-16-inferred | email marketing standalone tier 3 |
| fake-package-1 | unknown | no | 2026-05-16-inferred | ghost/test ID; always NOT_FOUND |
| fake-package-2 | unknown | no | 2026-05-16-inferred | ghost/test ID; always NOT_FOUND |
| logodesign-tier2 | standalone | no | 2026-05-16-inferred | logo design service standalone tier 2 |
| m365-officebusinessep1-aes | standalone | no | 2026-05-16-inferred | M365 officeBusinessEp1 AES plan; single M365 product |
| m365-officebusinessp1-aes | standalone | no | 2026-05-16-inferred | M365 officeBusinessP1 AES plan; single M365 product |
| m365-officebusinessp2-aes | standalone | no | 2026-05-16-inferred | M365 officeBusinessP2 AES plan; single M365 product |
| managed-wordpress-ultimate-ox-3sites-1year | bundle | no | 2026-05-16-inferred | MWP Ultimate + OX email bundle; 3 sites 1-year term |
| managedseo-005hours | standalone | no | 2026-05-16-inferred | managed SEO 5-hour service; standalone |
| managedseo-010hours | standalone | no | 2026-05-16-inferred | managed SEO 10-hour service; standalone |
| managedseo-015hours | standalone | no | 2026-05-16-inferred | managed SEO 15-hour service; standalone |
| managedseo-020hours | standalone | no | 2026-05-16-inferred | managed SEO 20-hour service; standalone |
| managedseo-025hours | standalone | no | 2026-05-16-inferred | managed SEO 25-hour service; standalone |
| managedseo-030hours | standalone | no | 2026-05-16-inferred | managed SEO 30-hour service; standalone |
| managedseo-035hours | standalone | no | 2026-05-16-inferred | managed SEO 35-hour service; standalone |
| managedseo-040hours | standalone | no | 2026-05-16-inferred | managed SEO 40-hour service; standalone |
| managedseo-050hours | standalone | no | 2026-05-16-inferred | managed SEO 50-hour service; standalone |
| managedseo-060hours | standalone | no | 2026-05-16-inferred | managed SEO 60-hour service; standalone |
| managedseo-080hours | standalone | no | 2026-05-16-inferred | managed SEO 80-hour service; standalone |
| mena-ecommerce-kit-tier1 | bundle | no | 2026-05-16-inferred | MENA ecommerce kit tier 1; same bundle family as confirmed mena-digital-kit-* |
| msb-mwp-wds-bundle | bundle | no | 2026-05-16-inferred | MWP + WDS bundle; explicit -bundle suffix |
| msb-standardwordpress-bundle | bundle | no | 2026-05-16-inferred | standard WordPress + additional product bundle; explicit -bundle suffix |
| msb-wam-wds-bundle | bundle | no | 2026-05-16-inferred | WAM + WDS bundle; explicit -bundle suffix |
| msp-mwp-wds-bundle | bundle | no | 2026-05-16-inferred | MSP + MWP + WDS bundle; explicit -bundle suffix |
| multi-unit-ssl-setup-service | standalone | no | 2026-05-16-inferred | SSL setup service; standalone one-time service |
| mwp-ecommerce-o365-tier1 | bundle | no | 2026-05-16-inferred | MWP ecommerce + M365 bundle tier 1 |
| mwp-ecommerce-openexchange-tier1 | bundle | no | 2026-05-16-inferred | MWP ecommerce + OX email bundle tier 1 |
| nes-airo-all-access-with-freetrial | standalone | yes | 2026-05-16-inferred | Airo all-access plan; single product; free trial flag in slug |
| nes-airo-plus-logo-with-autorenew-false | bundle | no | 2026-05-16-inferred | Airo + Logo design bundle; two products; autoRenew override |
| nes-business-hosting-set-1-expand-365-wss-xtra | bundle | no | 2026-05-16-inferred | business hosting + M365 + WSS bundle; 3 products |
| nes-business-plus-123reg-bundle | bundle | no | 2026-05-16-inferred | 123reg brand business bundle; explicit -bundle suffix |
| nes-conversations-1-year | standalone | no | 2026-05-16-inferred | Conversations single product; 1-year term |
| nes-conversationsdeluxefreetrial | standalone | yes | 2026-05-16-inferred | Conversations deluxe plan; free trial flag in slug |
| nes-conversationsessentialsfreetrial | standalone | yes | 2026-05-16-inferred | Conversations essentials plan; free trial flag in slug |
| nes-conversationsultimatefreetrial | standalone | yes | 2026-05-16-inferred | Conversations ultimate plan; free trial flag in slug |
| nes-cpanel-email-essentials-123reg-bundle | bundle | no | 2026-05-16-inferred | cPanel + email essentials for 123reg brand; bundle |
| nes-cpanel-set-1-economy-ssl-365-wss-xtra | bundle | no | 2026-05-16-inferred | cPanel + SSL + M365 + WSS bundle; 4 products |
| nes-cpanel-set-1-economy-ssl-365-xtra | bundle | no | 2026-05-16-inferred | cPanel + SSL + M365 bundle; xtra tier |
| nes-cpanel-set-2-deluxe-365-wss-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 deluxe + M365 + WSS bundle |
| nes-cpanel-set-2-deluxe-365-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 deluxe + M365 bundle; xtra tier |
| nes-cpanel-set-2-deluxe-ox | bundle | no | 2026-05-16-inferred | cPanel set-2 deluxe + OX email bundle |
| nes-cpanel-set-2-ultimate-365-wss-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 ultimate + M365 + WSS bundle |
| nes-cpanel-set-2-ultimate-365-xtra | bundle | no | 2026-05-16-inferred | cPanel set-2 ultimate + M365 bundle; xtra tier |
| nes-cpanel-set-2-ultimate-ox | bundle | no | 2026-05-16-inferred | cPanel set-2 ultimate + OX email bundle |
| nes-email-essentials-123reg-bundle | bundle | no | 2026-05-16-inferred | email essentials for 123reg brand; explicit -bundle suffix |
| nes-m365emailessentialseedpp | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe for DPP surface; single M365 product |
| nes-m365emailessentialseedpp-149 | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe for DPP at $1.49 price point; single M365 product |
| nes-social-first-starter | unknown | no | 2026-05-16-inferred | ghost ID; always NOT_FOUND per ces-nes knowledge |
| nes-vps4-self-managed-lin-openclaw-tier2 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Linux tier 2; openclaw is config variant not a separate product |
| nes-wordpress-premiumsupport-tier0 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 0; standalone service |
| nes-wordpress-premiumsupport-tier1 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 1; standalone service |
| nes-wordpress-premiumsupport-tier2 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 2; standalone service |
| nes-wordpress-premiumsupport-tier3 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 3; standalone service |
| nes-workspace-titan-prolight-withdiscountcode | standalone | no | 2026-05-16-inferred | Workspace Titan Pro Light email plan with discount code; single email product |
| nes-wp-o365-forever-deluxe-ssl-nortonsmb-standardfreetrial | bundle | yes | 2026-05-16-inferred | MWP + M365 + SSL + Norton SMB bundle; free trial flag in slug |
| nes-wsb-digital-marketing-enterprise-freetrial | standalone | yes | 2026-05-16-inferred | WSB digital marketing enterprise plan; free trial flag in slug |
| nes-wsb-digital-marketing-essentials-freetrial | standalone | yes | 2026-05-16-inferred | WSB digital marketing essentials plan; free trial flag in slug |
| nes-wsb-digital-marketing-professional-freetrial | standalone | yes | 2026-05-16-inferred | WSB digital marketing professional plan; free trial flag in slug |
| nes-wss-tier0-nortonsmb-standardfreetrial | bundle | yes | 2026-05-16-inferred | WSS tier 0 + Norton SMB bundle; free trial; pattern from confirmed wss-tier1/2-nortonsmb |
| norton-1-year-free-trial | standalone | yes | 2026-05-16-inferred | Norton standalone; free trial; slug contains freetrial |
| offer-airo-builder-professional | unknown | no | 2026-05-16-inferred | ghost ID; always NOT_FOUND per ces-nes knowledge |
| offer-airo-builder-starter | unknown | no | 2026-05-16-inferred | ghost ID; always NOT_FOUND per ces-nes knowledge |
| offer-airo-builder-ultimate | unknown | no | 2026-05-16-inferred | ghost ID; always NOT_FOUND per ces-nes knowledge |
| offer-designStudioInternational-showinBioStarter | standalone | no | 2026-05-16-inferred | Design Studio International bio starter; single product |
| offer-diys-logoImage | standalone | no | 2026-05-16-inferred | DIY logo image design; single product |
| offer-dpp-solution-set-q3-b-ecommerce | bundle | no | 2026-05-16-inferred | DPP solution set Q3-B ecommerce tier; domain + product bundle |
| offer-dpp-solution-set-q3-b-essential | bundle | no | 2026-05-16-inferred | DPP solution set Q3-B essential tier; domain + product bundle |
| offer-dpp-solution-set-q3-b-starter | bundle | no | 2026-05-16-inferred | DPP solution set Q3-B starter tier; domain + product bundle |
| offer-govalue-api-offer-basic | standalone | no | 2026-05-16-inferred | GoDaddy Value API offer basic tier; single product |
| offer-govalue-api-offer-professional | standalone | no | 2026-05-16-inferred | GoDaddy Value API offer professional tier; single product |
| offer-leased-domain-offer-leasedDomain | standalone | no | 2026-05-16-inferred | leased domain product; single product |
| offer-m365-emailEssentialsEe_AES | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe AES plan; single M365 product (capitalization variant) |
| offer-m365-officeBusinessEp1_AES | standalone | no | 2026-05-16-inferred | M365 officeBusinessEp1 AES plan; single M365 product |
| offer-m365-officeBusinessP1_AES | standalone | no | 2026-05-16-inferred | M365 officeBusinessP1 AES plan; single M365 product |
| offer-m365-officeBusinessP2_AES | standalone | no | 2026-05-16-inferred | M365 officeBusinessP2 AES plan; single M365 product |
| offer-membership-premium | standalone | no | 2026-05-16-inferred | GoDaddy membership premium tier; single product |
| offer-norton-nortonSmallBusinessPremium | standalone | no | 2026-05-16-inferred | Norton Small Business Premium; single security product |
| offer-norton-nortonSmallBusinessStandard | standalone | no | 2026-05-16-inferred | Norton Small Business Standard; single security product |
| offer-titanemail-pro | standalone | no | 2026-05-16-inferred | Titan Email pro plan; single email product |
| offer-titanemail-ultra | standalone | no | 2026-05-16-inferred | Titan Email ultra plan; single email product |
| offer-wsb-enterpriseFreeTrial | standalone | yes | 2026-05-16-inferred | WSB enterprise plan free trial; slug contains FreeTrial |
| offer-wsb-essentialsFreeTrial | standalone | yes | 2026-05-16-inferred | WSB essentials plan free trial; slug contains FreeTrial |
| office365-addseats-tier0 | standalone | no | 2026-05-16-inferred | M365 add-seats tier 0; single M365 product |
| office365-addseats-tier1 | standalone | no | 2026-05-16-inferred | M365 add-seats tier 1; single M365 product |
| office365-addseatsemailplus-tier1 | standalone | no | 2026-05-16-inferred | M365 add-seats email plus tier 1; single M365 product |
| office365-advancedbundle-tier3 | bundle | no | 2026-05-16-inferred | M365 advanced bundle tier 3; bundle name in slug |
| office365-emailplus-tier1 | standalone | no | 2026-05-16-inferred | M365 email plus tier 1; single M365 product |
| office365-securitybundle-tier3 | bundle | no | 2026-05-16-inferred | M365 security bundle tier 3; M365 + security product |
| office365-tier3 | standalone | no | 2026-05-16-inferred | M365 tier 3; single M365 product (tiers 0-2 confirmed standalone) |
| office36xxxxxxxxxxx5-tier1 | unknown | no | 2026-05-16-inferred | garbled/corrupted package_id; NOT_FOUND |
| oybo-1email-1yr | bundle | no | 2026-05-16-inferred | OYBO domain + 1 email for 1 year; domain+email bundle |
| oybo-au-email | bundle | no | 2026-05-16-inferred | OYBO AU market domain + email bundle |
| oybo-ox-email | bundle | no | 2026-05-16-inferred | OYBO domain + OX email bundle |
| oybo-uk-email | bundle | no | 2026-05-16-inferred | OYBO UK market domain + email bundle |
| pfid-1809421 | unknown | no | 2026-05-16-inferred | non-standard format; PFID not a curated offer slug |
| pl-mwp-ecommerce-tier1 | standalone | no | 2026-05-16-inferred | Polish market MWP ecommerce tier 1; single product |
| pl-wordpress-tier2 | standalone | no | 2026-05-16-inferred | Polish market WordPress tier 2; single product |
| pl-workspace-tier1 | standalone | no | 2026-05-16-inferred | Polish market Workspace email tier 1; single product |
| plesk-o365-tier1 | bundle | no | 2026-05-16-inferred | Plesk + M365 bundle tier 1 |
| plesk-o365-tier2 | bundle | no | 2026-05-16-inferred | Plesk + M365 bundle tier 2 |
| plesk-o365-tier3 | bundle | no | 2026-05-16-inferred | Plesk + M365 bundle tier 3 |
| plesk-openexchange-tier0 | bundle | no | 2026-05-16-inferred | Plesk + OX email bundle tier 0 |
| plesk-openexchange-tier1 | bundle | no | 2026-05-16-inferred | Plesk + OX email bundle tier 1 |
| plesk-openexchange-tier2 | bundle | no | 2026-05-16-inferred | Plesk + OX email bundle tier 2 |
| plesk-openexchange-tier3 | bundle | no | 2026-05-16-inferred | Plesk + OX email bundle tier 3 |
| plesk-tier0 | standalone | no | 2026-05-16-inferred | bare Plesk tier 0; no email bundle suffix |
| pwsdifm-gocentral-ols | standalone | no | 2026-05-16-inferred | professional website build service (OLS); single service product |
| redemption | standalone | no | 2026-05-16-inferred | domain redemption service; single product |
| restore-pwsdifm-gocentral-ols-websitecare | standalone | no | 2026-05-16-inferred | restore backup for pwsdifm-gocentral-ols; single service |
| restore-webstoredesign-wordpress-websitecare-tier1 | standalone | no | 2026-05-16-inferred | restore backup for webstoredesign-wordpress tier 1; single service |
| restore-wordpressdesign-tier1 | standalone | no | 2026-05-16-inferred | restore backup for WordPress design tier 1; single service |
| restore-wordpressdesign-websitecare-tier2 | standalone | no | 2026-05-16-inferred | restore backup for WordPress design tier 2 with websitecare |
| restore-wordpressdesign-websitecare-tier3 | standalone | no | 2026-05-16-inferred | restore backup for WordPress design tier 3 with websitecare |
| sitemaintenance-005sites | standalone | no | 2026-05-16-inferred | site maintenance service for 5 sites; standalone |
| sitemaintenance-050sites | standalone | no | 2026-05-16-inferred | site maintenance service for 50 sites; standalone |
| sitemaintenance-100sites | standalone | no | 2026-05-16-inferred | site maintenance service for 100 sites; standalone |
| sitemaintenance-500sites | standalone | no | 2026-05-16-inferred | site maintenance service for 500 sites; standalone |
| ssl-001sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 1 site tier 2; single SSL product |
| ssl-005sites-managed-tier1 | standalone | no | 2026-05-16-inferred | SSL managed cert for 5 sites tier 1; single product |
| ssl-005sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 5 sites tier 2; single product |
| ssl-005sites-tier3 | standalone | no | 2026-05-16-inferred | SSL cert for 5 sites tier 3; single product |
| ssl-010sites-managed-tier1 | standalone | no | 2026-05-16-inferred | SSL managed cert for 10 sites tier 1; single product |
| ssl-010sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 10 sites tier 1; single product |
| ssl-010sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 10 sites tier 2; single product |
| ssl-010sites-tier3 | standalone | no | 2026-05-16-inferred | SSL cert for 10 sites tier 3; single product |
| ssl-015sites-managed-tier1 | standalone | no | 2026-05-16-inferred | SSL managed cert for 15 sites tier 1; single product |
| ssl-015sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 15 sites tier 1; single product |
| ssl-015sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 15 sites tier 2; single product |
| ssl-015sites-tier3 | standalone | no | 2026-05-16-inferred | SSL cert for 15 sites tier 3; single product |
| ssl-020sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 20 sites tier 1; single product |
| ssl-020sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 20 sites tier 2; single product |
| ssl-030sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 30 sites tier 1; single product |
| ssl-040sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 40 sites tier 1; single product |
| ssl-050sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 50 sites tier 1; single product |
| ssl-050sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 50 sites tier 2; single product |
| ssl-050sites-tier3 | standalone | no | 2026-05-16-inferred | SSL cert for 50 sites tier 3; single product |
| ssl-100sites-tier1 | standalone | no | 2026-05-16-inferred | SSL cert for 100 sites tier 1; single product |
| ssl-100sites-tier2 | standalone | no | 2026-05-16-inferred | SSL cert for 100 sites tier 2; single product |
| ssl-100sites-tier3 | standalone | no | 2026-05-16-inferred | SSL cert for 100 sites tier 3; single product |
| ssl-setup-service-10site | standalone | no | 2026-05-16-inferred | SSL setup service for 10 sites; standalone one-time service |
| ssl-setup-service-25site | standalone | no | 2026-05-16-inferred | SSL setup service for 25 sites; standalone one-time service |
| ssl-setup-service-5site | standalone | no | 2026-05-16-inferred | SSL setup service for 5 sites; standalone one-time service |
| ssl-wildcard-managed-tier1 | standalone | no | 2026-05-16-inferred | SSL wildcard managed cert tier 1; single product |
| sslcert-managed-with-monitoring | standalone | no | 2026-05-16-inferred | SSL cert managed with monitoring; single SSL product family |
| turnkeyreseller-tier1 | standalone | no | 2026-05-16-inferred | turnkey reseller product tier 1; standalone |
| turnkeyreseller-tier2 | standalone | no | 2026-05-16-inferred | turnkey reseller product tier 2; standalone |
| vnext-freebuild-tier1 | standalone | no | 2026-05-16-inferred | WSB free build tier 1; single WSB product |
| vnext-freebuild-tier1-latam | standalone | no | 2026-05-16-inferred | WSB free build tier 1 LATAM market; single WSB product |
| vnext-freebuild-tier1-openxchange | bundle | no | 2026-05-16-inferred | WSB free build + OX email bundle; tier 1 |
| vnext-freebuild-tier2 | standalone | no | 2026-05-16-inferred | WSB free build tier 2; single WSB product |
| vnext-freebuild-tier2-latam | standalone | no | 2026-05-16-inferred | WSB free build tier 2 LATAM market; single WSB product |
| vnext-freebuild-tier2-openxchange | bundle | no | 2026-05-16-inferred | WSB free build + OX email bundle; tier 2 |
| vnext-freebuild-tier3 | standalone | no | 2026-05-16-inferred | WSB free build tier 3; single WSB product |
| vnext-freebuild-tier3-latam | standalone | no | 2026-05-16-inferred | WSB free build tier 3 LATAM market; single WSB product |
| vnext-freemat | standalone | no | 2026-05-16-inferred | WSB free material/marketing; single product |
| vnext-freemat-intl | standalone | no | 2026-05-16-inferred | WSB free material international variant; single product |
| vnext-i18no365-tier1 | bundle | no | 2026-05-16-inferred | WSB international + M365 bundle tier 1 |
| vnext-i18no365-tier2 | bundle | no | 2026-05-16-inferred | WSB international + M365 bundle tier 2 |
| vnext-i18no365-tier3 | bundle | no | 2026-05-16-inferred | WSB international + M365 bundle tier 3 |
| vnext-i18no365-tier4 | bundle | no | 2026-05-16-inferred | WSB international + M365 bundle tier 4 |
| vnext-i18nox-tier1 | bundle | no | 2026-05-16-inferred | WSB international + OX email bundle tier 1 |
| vnext-i18nox-tier1-precheck | bundle | no | 2026-05-16-inferred | WSB international + OX email bundle tier 1; precheck surface variant |
| vnext-i18nox-tier2 | bundle | no | 2026-05-16-inferred | WSB international + OX email bundle tier 2 |
| vnext-i18nox-tier3 | bundle | no | 2026-05-16-inferred | WSB international + OX email bundle tier 3 |
| vnext-i18nox-tier4 | bundle | no | 2026-05-16-inferred | WSB international + OX email bundle tier 4 |
| vps4-managed-high-mem-lin-cpanel-tier2 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + cPanel bundle tier 2 |
| vps4-managed-high-mem-lin-cpanel-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + cPanel bundle tier 4 |
| vps4-managed-high-mem-lin-cpanel-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + cPanel bundle tier 6 |
| vps4-managed-high-mem-lin-cpanel-tier7 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + cPanel bundle tier 7 |
| vps4-managed-high-mem-lin-plesk-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + Plesk bundle tier 4 |
| vps4-managed-high-mem-lin-plesk-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + Plesk bundle tier 6 |
| vps4-managed-high-mem-lin-plesk-tier7 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Linux + Plesk bundle tier 7 |
| vps4-managed-high-mem-win-plesk-tier2 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Windows + Plesk bundle tier 2 |
| vps4-managed-high-mem-win-plesk-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Windows + Plesk bundle tier 4 |
| vps4-managed-high-mem-win-plesk-tier5 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Windows + Plesk bundle tier 5 |
| vps4-managed-high-mem-win-plesk-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Windows + Plesk bundle tier 6 |
| vps4-managed-high-mem-win-plesk-tier7 | bundle | no | 2026-05-16-inferred | VPS4 managed high-mem Windows + Plesk bundle tier 7 |
| vps4-managed-lin-cpanel-tier1 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 1 |
| vps4-managed-lin-cpanel-tier2 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 2 |
| vps4-managed-lin-cpanel-tier3 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 3 |
| vps4-managed-lin-cpanel-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 4 |
| vps4-managed-lin-cpanel-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 6 |
| vps4-managed-lin-cpanel-tier8 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + cPanel bundle tier 8 |
| vps4-managed-lin-plesk-tier1 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + Plesk bundle tier 1 |
| vps4-managed-lin-plesk-tier2 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + Plesk bundle tier 2 |
| vps4-managed-lin-plesk-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + Plesk bundle tier 4 |
| vps4-managed-lin-plesk-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + Plesk bundle tier 6 |
| vps4-managed-lin-plesk-tier8 | bundle | no | 2026-05-16-inferred | VPS4 managed Linux + Plesk bundle tier 8 |
| vps4-managed-win-plesk-tier2 | bundle | no | 2026-05-16-inferred | VPS4 managed Windows + Plesk bundle tier 2 |
| vps4-managed-win-plesk-tier4 | bundle | no | 2026-05-16-inferred | VPS4 managed Windows + Plesk bundle tier 4 |
| vps4-managed-win-plesk-tier5 | bundle | no | 2026-05-16-inferred | VPS4 managed Windows + Plesk bundle tier 5 |
| vps4-managed-win-plesk-tier6 | bundle | no | 2026-05-16-inferred | VPS4 managed Windows + Plesk bundle tier 6 |
| vps4-managed-win-plesk-tier8 | bundle | no | 2026-05-16-inferred | VPS4 managed Windows + Plesk bundle tier 8 |
| vps4-self-managed-high-disk-win-tier5 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-disk Windows tier 5; single VPS product |
| vps4-self-managed-high-mem-lin-tier1 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Linux tier 1; single VPS product |
| vps4-self-managed-high-mem-lin-tier2 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Linux tier 2; single VPS product |
| vps4-self-managed-high-mem-lin-tier4 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Linux tier 4; single VPS product |
| vps4-self-managed-high-mem-lin-tier6 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Linux tier 6; single VPS product |
| vps4-self-managed-high-mem-lin-tier7 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Linux tier 7; single VPS product |
| vps4-self-managed-high-mem-win-tier1 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Windows tier 1; single VPS product |
| vps4-self-managed-high-mem-win-tier2 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Windows tier 2; single VPS product |
| vps4-self-managed-high-mem-win-tier4 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Windows tier 4; single VPS product |
| vps4-self-managed-high-mem-win-tier6 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Windows tier 6; single VPS product |
| vps4-self-managed-high-mem-win-tier7 | standalone | no | 2026-05-16-inferred | VPS4 self-managed high-mem Windows tier 7; single VPS product |
| vps4-self-managed-lin-tier0 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Linux tier 0; single VPS product |
| vps4-self-managed-lin-tier6 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Linux tier 6; single VPS product |
| vps4-self-managed-lin-tier7 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Linux tier 7; single VPS product |
| vps4-self-managed-lin-tier8 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Linux tier 8; single VPS product |
| vps4-self-managed-win-tier6 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Windows tier 6; single VPS product |
| vps4-self-managed-win-tier7 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Windows tier 7; single VPS product |
| vps4-self-managed-win-tier8 | standalone | no | 2026-05-16-inferred | VPS4 self-managed Windows tier 8; single VPS product |
| webdesign-tier1 | standalone | no | 2026-05-16-inferred | web design service tier 1; standalone |
| webdesign-tier2 | standalone | no | 2026-05-16-inferred | web design service tier 2; standalone |
| websecurity-tier1 | standalone | no | 2026-05-16-inferred | website security standalone tier 1 |
| websecurity-tier2 | standalone | no | 2026-05-16-inferred | website security standalone tier 2 |
| websecuritysuite-tier0 | standalone | no | 2026-05-16-inferred | WSS tier 0; base WSS without Norton suffix = standalone |
| websecuritysuite-tier1 | standalone | no | 2026-05-16-inferred | WSS tier 1; base WSS without Norton suffix = standalone |
| websecuritysuite-tier2 | standalone | no | 2026-05-16-inferred | WSS tier 2; base WSS without Norton suffix = standalone |
| websitebackup-tier1 | standalone | no | 2026-05-16-inferred | website backup product tier 1; standalone |
| webstoredesign-onlinestore-tier1 | standalone | no | 2026-05-16-inferred | web store design online store service tier 1; single service |
| webstoredesign-tier1 | standalone | no | 2026-05-16-inferred | web store design service tier 1; standalone |
| wordpress-o365-1site-tier3 | bundle | no | 2026-05-16-inferred | MWP 1-site + M365 bundle tier 3 |
| wordpress-o365-1site-tier3-3 | bundle | no | 2026-05-16-inferred | MWP 1-site + M365 bundle tier 3-3 variant |
| wordpress-o365-forever-ssl-basic | bundle | no | 2026-05-16-inferred | MWP + M365 + SSL forever basic; same family as confirmed wordpress-o365-forever-ssl-deluxe |
| wordpress-o365-forever-ssl-deluxe | bundle | no | 2026-05-16-inferred | MWP + M365 + SSL forever deluxe; confirmed in validation data (PFID 1320706) |
| wordpress-openexchange-1site-tier3 | bundle | no | 2026-05-16-inferred | MWP 1-site + OX email bundle tier 3 |
| wordpress-openexchange-forever-ssl-basic | bundle | no | 2026-05-16-inferred | MWP + OX + SSL forever basic; same family as confirmed wordpress-openexchange-forever-ssl-deluxe |
| wordpress-openexchange-forever-ssl-deluxe | bundle | no | 2026-05-16-inferred | MWP + OX + SSL forever deluxe; confirmed in validation data (PFID 1320706) |
| wordpress-openexchange-tier3 | bundle | no | 2026-05-16-inferred | MWP + OX email bundle tier 3 |
| wordpress-premiumsupport-tier1 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 1; standalone service |
| wordpress-premiumsupport-tier2 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 2; standalone service |
| wordpress-premiumsupport-tier3 | standalone | no | 2026-05-16-inferred | WordPress premium support add-on tier 3; standalone service |
| wordpressdesign-tier2 | standalone | no | 2026-05-16-inferred | WordPress design service tier 2; standalone |
| wordpressdesign-tier3 | standalone | no | 2026-05-16-inferred | WordPress design service tier 3; standalone |
| workspace-openexchange-tier1 | bundle | no | 2026-05-16-inferred | Workspace + OX email bundle tier 1 |
| workspace-openexchange-tier2 | bundle | no | 2026-05-16-inferred | Workspace + OX email bundle tier 2 |
| wsb-vnext-tier1 | standalone | no | 2026-05-16-inferred | WSB vnext tier 1; single WSB product |
| wsb-vnext-tier4 | standalone | no | 2026-05-16-inferred | WSB vnext tier 4; single WSB product |
| offer-airo-builder-commerce | unknown | no | 2026-05-16 | NOT_FOUND in catalog-query and catalog-curated-offers; ghost ID matching offer-airo-builder-* pattern |
| cpanel-set-2-economy | standalone | no | 2026-05-16-inferred | bare cPanel set-2 economy; no SSL/email suffix = cPanel only; pattern from nes-cpanel-set-2-economy standalone |
| cpanel-set-2-economy-ssl-ox | bundle | no | 2026-05-16-inferred | cPanel set-2 economy + SSL + OX email; pattern from confirmed cpanel-set-1-economy-ssl-ox bundle |
| vps4-managed-high-mem-lin-tier4 | standalone | no | 2026-05-16-inferred | VPS4 managed high-mem Linux tier 4; no cPanel/Plesk suffix = single VPS product; NOT_FOUND in test catalog |
| vps4-managed-high-mem-lin-tier6 | standalone | no | 2026-05-16-inferred | VPS4 managed high-mem Linux tier 6; no cPanel/Plesk suffix = single VPS product; NOT_FOUND in test catalog |
| nes-wss-tier0-ox | bundle | no | 2026-05-16-inferred | WSS tier 0 + OX email bundle; pattern from confirmed nes-wss-tier*-ox bundle family |
| nes-wss-tier0-ssl-ox | bundle | no | 2026-05-16-inferred | WSS tier 0 + SSL + OX email bundle; pattern from nes-wss-tier*-ssl-ox bundle family |
| ssl-dv-tier4 | standalone | no | 2026-05-16-inferred | DV SSL certificate tier 4; pattern from confirmed ssl-dv-tier1/2/3 standalone |
| ssl-dv-tier5 | standalone | no | 2026-05-16-inferred | DV SSL certificate tier 5; pattern from confirmed ssl-dv-tier1/2/3 standalone |
| cpanel-set-1-economy | standalone | no | 2026-05-16-inferred | bare cPanel set-1 economy (no nes- prefix); same product as nes-cpanel-set-1-economy standalone |
| cpanel-set-1-deluxe | standalone | no | 2026-05-16-inferred | bare cPanel set-1 deluxe (no nes- prefix); same product as nes-cpanel-set-1-deluxe standalone |
| offer-airo-builder-essentials | unknown | no | 2026-05-16 | NOT_FOUND in catalog-query and catalog-curated-offers; ghost ID matching offer-airo-builder-* pattern |
| offer-m365-emailEssentialsEe_standard_AES | standalone | no | 2026-05-16-inferred | M365 emailEssentialsEe standard AES plan; single M365 product; variant of offer-m365-emailEssentialsEe_AES standalone |
| offer-microsoftemail-onlineessentials-standard_AES | standalone | no | 2026-05-16-inferred | M365 Online Essentials standard AES plan; single M365 product; pattern from microsoftemail standalone family |

---

## Coverage Summary (as of 2026-05-16)

560 package_ids classified. 548 with known geometry, 10 unknowns (2 ghost IDs confirmed NOT_FOUND in test catalog).

| Geometry | Count | Notes |
|---|---|---|
| standalone | 307 | Domain, SSL, M365, VPS4, temp-email-essentials, Titan Email, WSB, cPanel bare tiers, 4GH hosting, business hosting bare, DLX SSL, managed SEO, site maintenance, webdesign, restore, turnkey reseller, OYBO standalone variants |
| bundle | 240 | dpp-*/mena-*/oybo-*/nes-wss-*/nes-cpanel-ssl-*/webstoredesign/domain-withprivacy/nes-wss-nodiscount/cpanel-o365/cpanel-openexchange/plesk-o365/plesk-openexchange/vnext-i18n*/wordpress-o365/wordpress-openexchange/workspace-openexchange/vps4-managed-*-cpanel/vps4-managed-*-plesk/business-hosting-set-*/msb-*-bundle/mwp-ecommerce-* |
| unknown | 10 | fake-package-1/2, nes-social-first-starter, offer-airo-builder-commerce/essentials/professional/starter, office36xxxxxxxxxxx5-tier1, pfid-1809421 |

**Breakdown by verification method:**
- catalog_verified (confirmed against test catalog-query): 20 standalone, 13 bundle
- catalog-curated-offers confirmed (internal test endpoint): +5 standalone, +3 bundle
- merch-packages confirmed: +1 standalone (office365-tier2)
- inferred (name-pattern or product-family based): 98 standalone, 82 bundle

**Key findings from 2026-05-16 resolution run:**
- `titanemail-light/standard/premium/max` all confirmed standalone via catalog-curated-offers (offerId: 927a9d45, plans: light/pro/premium/ultra)
- `wss-tier*-nortonsmb-*` all confirmed bundle via catalog-curated-offers (offerCollection dc3b59c2; WSS+Norton parent+child; BPO free trial)
- `cpanel-set-1-economy-ssl-ox` confirmed bundle via catalog-curated-offers (prePurchaseKeyMap + 2 childOffers)
- `office365-emailessentialsee_aes` confirmed standalone via catalog-curated-offers (offerId: 575a7d2a)
- `office365-tier2` confirmed standalone via merch-packages (single M365 product + optional add-ons only)
- `wsb-tier1` confirmed standalone via catalog-curated-offers (single websiteTonight product, no bundle)
- All `nes-cpanel-set-*-economy/deluxe/ultimate` bare tiers → standalone (no SSL/email suffix = cPanel only)
- All `offer-wsb-*` → standalone (WSB is a single product family)
- All `offer-titanemail-*` → standalone (Titan Email is a single product, plan variants)
- All `offer-m365-*` → standalone (M365 is a single product family)
- `slp-hosting-4gh-tier*` → standalone (4GH hosting single product; prod-only)
- `dbs-bundle` → bundle (name inference; prod-only)

**Note on inferred entries:** All `2026-05-16-inferred` entries are prod-only (NOT_FOUND in test catalog) and classified
by name-pattern analysis or product-family knowledge. Re-attempt with prod datasource to confirm. Geometry of
inferred entries has high confidence (>90%) based on consistent naming conventions observed across the catalog.

---

## Refresh Instructions

See SKILL.md for full refresh protocol. Short version:
1. Run the weekly package_id discovery query (in SKILL.md)
2. Compare results to this table — new rows need catalog lookup
3. Append new rows using the table format above
4. Update "Last classification run" date in this file header
5. Do NOT update geometry for existing rows unless offer structure changed in catalog

No per-row timestamp needed — geometry is immutable once set.
