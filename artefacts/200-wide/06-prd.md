# PRD — Personalised Policy Communication Engine

**Product:** Kepler Insurance
**Feature:** Personalised Policy Communication Engine
**Date:** 2026-06-18
**Status:** Draft for stakeholder review

---

## Vision

Every Kepler renewal notice tells the customer, in plain language, exactly what changed and why — turning an opaque cost event into a transparent retention moment.

---

## Problem

53% of insurance customers shop at renewal (J.D. Power 2026). FCA verbatims show they switch not just for price, but because opaque renewal notices feel like unfair treatment — "Why didn't they offer us that premium first-time round?" (Alan Ford, Daily Mail 2024). Legacy templated notices merge 3 static fields; customer service cannot answer "what changed for me?" Kepler's 11 orphaned applications and dual AWS+on-prem footprint mean the migration window is the risk window for RACQ-style data integrity failures (ASIC lawsuit, 570K misleading notices).

Three adjacent products solve parts of this job — Lemonade (proactive UX transparency, captive stack), Zendesk (reactive call deflection, no causation), Compare the Market (adversarial substitution, no explanation) — but none insert a regulator-ready causal explanation into the precise moment of frustration: opening the renewal notice.

---

## Target Users

| Role | Current pain |
|---|---|
| Policyholder (Maria) | Renewal letter shows higher price with no causation → calls CS (23min hold, no answer) → shops → switches |
| Renewal Comms Manager (Sarah) | Template system merges 3 fields; 98% of notices go out unchecked; no data connecting notice quality to churn |
| Compliance Officer (James) | 0.1% manual sampling for FCA fair-value evidence; 99.9% rely on rate filing proxy — regulator has signalled this is inadequate |

---

## Top Stories (RICE-ranked)

| Rank | ID | Story | RICE |
|---|---|---|---|
| 1 | S6 | Agent-side causation view — CS agent sees per-policy breakdown on inbound call | 3.0 |
| 2 | S1 | Premium explanation — policyholder receives causal breakdown with renewal notice | 2.78 |
| 3 | S7 | A/B test cohort isolation — controlled experiment before full rollout | 2.67 |
| 4 | S2 | Batch personalisation at scale — 500K notices within print window | 1.92 |
| 5 | S4 | Compliance rule engine pre-flight — market-specific checks before dispatch | 1.92 |
| 6 | S10 | Multi-language notice generation — EN, DE, FR, IT, ES | 1.80 |
| 7 | S3 | Fair-value evidence trail — auditable pricing attribution per renewal | 1.60 |
| 8 | S8 | Phase 0 data readiness audit — discover which rating variables are exposed | 1.33 |

## Acceptance Criteria (top 4)

**S1 — Premium explanation:** Given ≥70% attribution coverage per Phase 0, when a renewal notice is generated, it MUST decompose the premium delta into ≥1 attributable causal factor citing a specific source (external index or rating input), pass the market-specific compliance rule engine, AND complete in ≤2s P95. **Error path:** if <50% attribution, use aggregated market-level fallback with audit tag; notify compliance if >30% of a market's notices are fallback. **NFR:** numerical claims must trace to source data — untraceable claims quarantine the notice.

**S6 — Agent-side causation view:** When agent looks up a policy, screen MUST display the same causal breakdown as the sent notice within 1s, showing total delta + factor bar chart + benchmark + notice text. **Error path:** if notice used fallback template, display warning banner ("Limited attribution — personalised causation not available") with a list of known reasons. **NFR:** P95 <2s at 2,000 concurrent calls; must not degrade CRM search for non-renewal queries.

**S7 — A/B test cohort isolation:** Treatment group receives personalised notice; control receives current templated notice. Both groups matched on rate-change magnitude, policy type, and market. Minimum 5,000 policies per arm. Measure switch rate at 30 days post-renewal. Target: ≥2pp lower churn in treatment vs control.

**S2 — Batch personalisation at scale:** 500K notices across 5 markets generated Friday 18:00 → Saturday 00:00 (6-hour window). ≥99.5% pass compliance check autonomously. Cost ≤EUR 0.02/notice. **Error path:** if LLM API errors exceed 2% in 5min window, pause + retry (3x, exponential backoff). If >0.1% of batch fails retries, alert on-call; any market with >5% failed is a DORA-reportable incident (24h clock).

---

## Scope Boundary

| In scope | Out of scope |
|---|---|
| Phase 0 — rating engine instrumentation audit per market | Building a real-time risk scoring engine (separate track, feasibility 2) |
| GenAI notice generation pipeline (EN, DE, FR, IT, ES) | Telematics data pipeline build (prerequisite for real-time scoring) |
| Market-specific compliance rule engine (FCA / BaFin / ACPR / IVASS / DGSFP) | Pricing engine modernisation — this is a communication layer, not a rating rewrite |
| Conversational "why?" follow-up (chat/email, post-notice) | Competitive pricing response agent (separate track, highest regulatory barrier) |
| Agent-side causation view (CRM widget) | Core PAS replacement |
| A/B test framework for controlled rollout | |

---

## Success Metric

**Primary — controlled churn delta:** ≥2pp lower renewal churn in the treatment group (personalised causation notice) vs the control group (current templated notice), measured via matched-cohort A/B test with ≥5,000 policies per arm per market, observed at 30 days post-renewal. Stretch goal: ≥3pp.

**Secondary — price satisfaction:** ≥25% relative improvement in the proportion of respondents who agree with "My renewal premium is fair given my risk profile" (3-question survey), measured from a declared 90-day pre-deployment baseline, with ≥400 responses per month per market (margin of error ≤5 points at 95% CI).

**Pre-commitment:** Measure both baselines during Phase 0 before any system build begins. If measured churn is ≤8%, reduce primary target to ≥1.5pp controlled delta and flag floor-effect risk.

> *This metric replaces the original "3pp from ~12%" framing, which was unfalsifiable (baseline was an industry estimate, not Kepler's actual data), used a phantom unit (+30 NPS points with no baseline), and lacked a counterfactual (static comparison cannot distinguish project effect from market movement). See 01-vision.md for the full critique.*

---

## Decision Memory

**Biggest scope call — Phase 0 before Phase 1.**

The most consequential decision across this series was to sequence Phase 0 (rating engine instrumentation audit, EUR80K per market) as a hard prerequisite before any GenAI pipeline build. The alternative was to build the GenAI layer first, assume the PAS exposes component-level variables, and backfill data integration in parallel — which would have saved 2–3 months of calendar time.

We rejected parallel build because the entire value hypothesis depends on ≥70% attribution coverage per policy. If Phase 0 discovers <50% of policies are decomposable, the feature degrades from personalised causation to aggregated market-level fallback — and the 3pp churn reduction target collapses to an estimated 0.5pp. Building the GenAI pipeline before knowing whether the data exists would commit EUR 500K of infrastructure cost against an unvalidated dependency. The risk was not just financial — it was the credibility cost of shipping a feature that promises "your price changed because..." and delivers "your price changed due to market conditions in your region" — the exact opaque language we were hired to fix.

The 2–3 month Phase 0 delay is the price of making the value hypothesis falsifiable before we spend engineering budget. Every story in the backlog downstream of Phase 0 (S1, S2, S3, S5, S6) depends on this data — and the A/B test (S7, EUR80K) is the next gate, not a post-hoc justification.
