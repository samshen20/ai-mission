# 00 — Feature Brief: UC-04 Multi-Region Consent Management Platform

## Source Use Case
**UC-04** from consulting/03-use-cases.md — Highest scored use case: Value 5, Feasibility 4, Overall 4.5

## One-Sentence Description
A geo-targeted Consent Management Platform (CMP) integrated at the CDN/edge that serves jurisdiction-specific consent flows (EU GDPR opt-in, Japan APPI opt-in + notice, US CCPA opt-out + GPC) and propagates consent signals to every downstream service in the Meridian headless commerce stack.

## Business Problem
Meridian operates across EU, Japan, and US regulatory regimes with different consent models (opt-in vs opt-out), differing data subject rights, and intensifying enforcement (€5.5B+ cumulative GDPR fines, APPI 2026 amendments, CPRA enforcement). Currently, compliance is managed ad-hoc per country — there is no architectural layer ensuring consent is captured, stored, propagated, and honored consistently.

## Regulatory Requirements
| Region | Consent Model | Key Requirements |
|--------|--------------|------------------|
| EU/EEA | Opt-in (GDPR, ePrivacy) | Affirmative consent before non-essential cookies; 8 data subject rights; 72h breach notification; SCCs for data transfers |
| Japan | Opt-in + Notice (APPI 2022+2026) | Consent + notice of purpose; pseudonymized data rules tightening; cross-border transfer scrutiny via PPC |
| US | Opt-out (CCPA/CPRA + 10+ state laws) | Right to opt-out of sale/sharing; GPC signal must be honored; state-by-state variations |

## Success Metrics (from 04-canvas.md)
- DSAR response time: ≤30 days, automated ≥80% (GDPR compliant)
- Regulatory fine exposure: Reduced from full exposure to compliant posture
- CMP integration time per new market: ≤4 weeks (configuration, not rebuild)

## Architecture Principle
**"Build to GDPR, localize exceptions"** — GDPR baseline covers ~80% of global obligations; add region-specific "plugs" for JP APPI and US CCPA.

## Constraints
- Must work in headless (API-first) architecture — no monolithic assumption
- Consent signals must propagate to every downstream service (loyalty, cart, personalization, analytics, ad platforms)
- Google Consent Mode v2 (`ad_user_data`, `ad_personalization`) mandatory for EU traffic using Google services
- Geo-detection at CDN/edge, not in application layer
- Must support existing OneTrust / Cookiebot / Usercentrics integration (final vendor TBD)
