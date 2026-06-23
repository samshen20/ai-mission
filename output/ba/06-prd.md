# 06 — One-Page PRD: UC-04 Multi-Region Consent Management Platform

**Feature:** Multi-Region Consent Management Platform  
**Source:** UC-04 (Value 5/Feasibility 4 — #1 priority from consulting brief)  
**Owner:** DPO / Privacy Ops Lead | **Sponsor:** CIO | **Timeline:** 8–12 weeks to MVP  

---

## Problem Statement

Meridian faces three simultaneous privacy regimes (EU GDPR opt-in, Japan APPI opt-in+notice, US CCPA opt-out) with intensifying enforcement — €5.5B+ cumulative GDPR fines, APPI 2026 amendments, and CPRA enforcement ramping. Currently, consent management is ad-hoc per country. Without an architectural consent layer, Meridian cannot safely unify customer data (UC-01), run AI personalization (UC-07), or operate its loyalty engine (UC-03) across borders without disproportionate regulatory risk.

## Target Outcome

A geo-targeted CMP that captures, propagates, and audits consent signals across all 35+ Meridian touchpoints — reducing DSAR response to ≤30 days (≥80% automated), enabling compliant cross-border data flows, and making each new market addition a ≤4-week configuration task.

## Scope

**In scope:**
- Geo-targeted consent banner serving (EU opt-in, JP opt-in+notice, US opt-out+GPC)
- Consent decision capture + immutable audit log
- Consent signal propagation via API gateway headers to all downstream services
- Google Consent Mode v2 emissions for EU traffic
- GPC (Global Privacy Control) signal detection and honoring
- Self-service DSAR portal with automated data collection across CIAM, commerce, loyalty, CMP
- Right to erasure / data deletion with propagation to all registered services
- Persistent preference center (granular controls, 12-month persistence)
- Compliance monitoring dashboard for privacy operations
- New market onboarding via configuration payload (≤4 weeks, no code)
- 3rd-party CMP vendor integration (OneTrust / Usercentrics / Cookiebot)

**Out of scope:**
- AI/ML decisions on consent patterns (manual analytics only)
- Physical store camera / biometric consent (future phase)
- Cookie scanning engine (use vendor's built-in scanner)
- Cross-border data transfer mechanism design (SCCs / BCRs — legal, not product)
- Vendor sub-processor inventory management (DPO function)

## Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Consent model baseline | GDPR opt-in as safe default | Covers ~80% of global obligations; fallback when geo-unavailable |
| Propagation mechanism | HTTP headers via API gateway | Least coupling; works with any backend protocol; audit-friendly |
| CMP integration pattern | Client-side tag + server-side API | Maximizes coverage: tag for web, API for mobile app and POS |
| GPC handling | GPC = valid opt-out (not "suggestion") | Required by CPRA; multi-state AG enforcements |

## Open Questions for Human Decision

| Question | Options | Recommended | Owner |
|----------|---------|-------------|-------|
| CMP vendor selection | OneTrust / Usercentrics / Cookiebot / Osano | **OneTrust** (enterprise market leader, proven headless support) | DPO/CIO |
| DSAR data scope | Which customer data sources are in scope for automated collection? | Start with CIAM + commerce + loyalty + CMP audit log; add analytics later | DPO |
| Banner language strategy | Which languages for JP users? | Japanese always as default for JP-geo; English secondary for international users | Regional MD JP |
| Deletion legal hold rules | Which business functions can assert a legal hold on deletion? | Transactions, returns, chargebacks — specific, time-bound, audited | Legal / DPO |

## Acceptance Gates (Phase 1 MVP — 8–12 weeks)

1. **Gate 1 (Week 4):** Geo-targeted consent banners displayed correctly for EU/JP/US in a staging environment; vendor CMP integrated
2. **Gate 2 (Week 8):** Consent signals propagate to ≥2 downstream services (analytics + personalization); audit log captures decisions
3. **Gate 3 (Week 12):** DSAR portal returns automated data compilation for the 4 in-scope data sources; GPC signal honored in US
4. **Go-Lite (Week 12+):** Deployed to 1 EU country (pilot); monitored for 2 weeks before scaling

## Out of Scope (Explicit)

- Cross-border data transfer mechanism (SCCs / BCRs) — handled by legal team
- AI consent predictions / "nudging" — intentionally excluded
- Physical loyalty card / POS terminal consent (deferred to Phase 2 POS integration — UC-12)
- Consent preference portability (e.g., IAB TCF string import/export across sites)
