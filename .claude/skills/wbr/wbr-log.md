# Offer Pulse — WBR Log

## WBR-001
Category   : Blocker
Status     : resolved
Logged     : 2026-06-02T00:00 (date only)
Week       : 2026-W23

**What happened**
P2P discount code routing was not configured for Titan UPP, blocking the Titan Upgrade Offer (AGIGROWTH-153) from launching. Janani's team patched the routing; Tony's fix was confirmed working June 2. Pricing verification (Joe Callen + Alexandra) completed same day; handoff to Amy for Hivemind experiment setup is the remaining step.

**Why it happened**
P2P routing was built for WAM products and requires explicit per-surface onboarding — it does not carry forward automatically when a new surface is introduced. Titan UPP was added without triggering the routing setup. No EP ticket was created to track the fix; it was resolved through ad-hoc team coordination with no formal trail. D2P (discount-to-purchase) is a separate downstream dependency that follows P2P and was also not configured.

**Risks**
Without a formal ticket, the gap has no post-mortem trail. The same miss will recur on the next new surface (MHWP Precheck, WAM Precheck) unless P2P routing verification is added to the pre-launch checklist for any experiment on a new or recently migrated surface.

**Next steps**
Add P2P routing verification to the pre-launch checklist for any experiment on a new surface. Pricing/discount team to confirm D2P routing is also verified on Titan UPP before the experiment goes live (separate dependency, downstream of P2P).

Resolution : Tony's P2P fix confirmed working June 2. Discount code passing correctly. Pricing verification completed; Amy to proceed with Hivemind experiment setup.
Resolved   : 2026-06-02

---

## WBR-002
Category   : Blocker
Status     : open
Logged     : 2026-06-02T00:00 (date only)
Week       : 2026-W23

**What happened**
TrustedSite add-on offer (AGIGROWTH-186) launched at WAM FOS Precheck with pricing displaying as $0 after the CES package was pushed to production. Add-to-cart is working correctly; the issue is display-only. The same bug occurred on a previous offer and self-resolved after several days without a root cause fix. EP-88830 (the ecomm delivery ticket) is currently On Hold despite packages being live in prod — a status mismatch that could stall experiment setup once the cache clears.

**Why it happened**
Precheck surfaces have an aggressive CDN cache layer that does not invalidate promptly when new package pricing lands in production. The root cause has never been investigated — it resolved on its own after the first occurrence and was never escalated to the precheck engineering team.

**Risks**
Every new precheck offer will hit this $0 display window on launch day. If the cache does not self-clear, a customer-facing pricing error is live with no owner and no playbook. EP-88830 being On Hold may delay experiment setup even after the display issue resolves. The EOW June 5 launch target is at risk.

**Next steps**
Garrett Wright (gwright1) to confirm cache has cleared and pricing is displaying correctly before proceeding with copy finalization. EP-88830 status must be updated from On Hold to reflect current state. Cache invalidation root cause should be raised with the precheck engineering team as a standing fix before the next offer swap on any precheck surface.

Resolution : —
Resolved   : —

---

## WBR-003
Category   : EP Ticket
Status     : open
Logged     : 2026-06-02T00:00 (date only)
Week       : 2026-W23

**What happened**
Dollar Door (AGIGROWTH-133) requires Lock on Create / paid trial billing policy override capability that does not exist for AAB at DPP. EP-88147 ("Dollar Door") was created to scope this work and has spawned 4 sub-implementation tickets: EP-89770 (in progress), EP-89289 (open), EP-89627 (open), and EP-90766 — the curated offer creation ticket (open). EP-88147 itself is unassigned and in Scheduling as of May 28. Saritha confirmed May 26 that ecomm plans a low-code workaround for the initial test, with full LOC build deferred to Q3.

**Why it happened**
The $1 entry price mechanic requires the cart to lock a promotional price at add-to-cart and auto-renew at a different rate — this is "Lock on Create" functionality. DPP + AAB does not have this capability. The gap was identified only after the offer entered solutioning; it was not surfaced at intake or SteerCo.

**Risks**
Dollar Door cannot launch without LOC enablement. If the low-code workaround path is not confirmed and scoped before the current dev sprint (target dev-complete June 15), the end-of-June launch placeholder slips. Additionally: offer and plan details (number of AAB plans in scope, paid trial term) were still unconfirmed as of Saritha's May 27 comment — EP-90766 (curated offer creation) cannot be scoped without them. LOC enablement for any future entry-price offer mechanic is also blocked until this capability is built.

**Next steps**
Saritha to confirm offer and plan details (which AAB plans, paid trial term) so EP-90766 can be scoped. EP-88147 needs an assigned owner in Scheduling. Low-code workaround path must be explicitly confirmed as viable for the experiment (vs. requiring the full Q3 build) before the June 15 dev-complete target can be treated as firm.

Resolution : —
Resolved   : —

---

## WBR-004
Category   : Blocker
Status     : open
Logged     : 2026-06-02T00:00 (date only)
Week       : 2026-W23

**What happened**
Two experiments — WAM M365 EE $0.99/mo Precheck Attach (AGIGROWTH-212) and MHWP M365 EE $0.99/mo Precheck Attach (AGIGROWTH-220) — are fully unblocked from an engineering standpoint as of June 2 (CES packages confirmed in Test and Prod) but cannot advance to SteerCo because the "Estimated Unit Added" field is empty on both tickets. Both are assigned to Ryan Beal. The gap was first flagged April 28 — 35 days without resolution.

**Why it happened**
Required SteerCo fields are not enforced at ticket intake. The missing field was discovered only after engineering completed their work, meaning launch-ready experiments are blocked by a required metadata field that no one caught at submission.

**Risks**
Two M365 precheck experiments are stalled with no path to launch until Ryan Beal populates the field. Engineering resources were consumed on both tickets without a clear forward path. Both miss the 10-day launch window if not addressed this week. The pattern — required fields discovered post-engineering — will repeat on future tickets unless validation moves to intake.

**Next steps**
Ryan Beal to populate Estimated Unit Added on AGIGROWTH-212 and AGIGROWTH-220 immediately so both tickets become SteerCo-eligible. Process fix: add required SteerCo field validation as a gate at ticket submission, not post-engineering.

Resolution : —
Resolved   : —

---

## WBR-005
Category   : Pipeline Decision
Status     : open
Logged     : 2026-06-02T00:00 (date only)
Week       : 2026-W23

**What happened**
AGIGROWTH-182 (AAB Plan + Credit Packs soft bundle) pivoted from a curated offer implementation to a UPP/in-app flow on June 2, after solutioning work had already been underway for the curated offer path. The linked EP intake ticket (EP-90623) is no longer the implementation path. The new approach uses agent impersonation: if a subscription exists, the flow adds the premium-to-paid upgrade plus credit packs to cart; if not, it adds a new subscription.

**Why it happened**
The June 2 execution call surfaced that the UPP/in-app flow covers both existing subscribers and new purchasers in a single path — coverage the curated offer approach could not provide. The decision was made to prioritize the broader-coverage path. This was not identified at intake or solutioning.

**Risks**
Solutioning work done under the curated offer assumption is partially wasted. The UPP/in-app path involves a different implementation team and timeline than the ecomm/EP track — the pivot resets the implementation clock. EP-90623 status has not been updated to reflect the pivot, creating potential confusion for anyone reading the ticket.

**Next steps**
Marcus Ganter to confirm the UPP/in-app path owner and sprint commitment. EP-90623 to be formally closed or updated to reflect the pivot decision. Confirm whether the new implementation path requires its own EP ticket or is tracked elsewhere.

Resolution : —
Resolved   : —

---

## WBR-006
Category   : Risk
Status     : open
Logged     : 2026-06-03T00:00 (date only)
Week       : 2026-W23

**What happened**
SteerCo approved a curated offer + discount code approach for Airo for WordPress (AGIGROWTH-146) on May 11. A product stakeholder (Drew Wilde) arrived weeks later with a conflicting direction — new product tiers / PFID clones instead. The conflict resolved on the May 19 execution call, with Drew's direction prevailing over SteerCo's. The ticket is now in Grooming in the PFID clone phase; curated offer creation has not started and has no timeline. The same decision authority gap was present in at least two other tickets this quarter (AGIGROWTH-133 re-scoped May 26, AGIGROWTH-182 pivoted June 2).

**Why it happened**
Implementation decision authority is not established at SteerCo. When a downstream product stakeholder arrives post-approval with a different preference, there is no defined escalation path — the conflict resolves ad-hoc on execution calls, often reversing the original SteerCo direction. Each reversal resets the full dev cycle.

**Risks**
AGIGROWTH-146 has no launch date and is gated on PFID clone work that must complete before curated offer creation can begin — an unknown-length dependency. If the pattern continues across Q3, mid-cycle reversals will inflate cycle time the same way they did in Q2, compounding the 41.7-day average cycle time problem. Q3 curated offer volume — critical for KR measurement — is at risk if intake-stage alignment is not improved.

**Next steps**
OLG / Natalie to define and document who holds implementation decision authority — SteerCo or product team — and enforce alignment at intake before tickets enter Grooming. For AGIGROWTH-146: confirm PFID clone ETA so curated offer creation can be sequenced. Flag this pattern in the next WBR as a process risk, not just a per-ticket issue.

Resolution : —
Resolved   : —

---
