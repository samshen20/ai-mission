# Release Communications — Personalised Policy Communication Engine 1.0

**Product:** Kepler Insurance
**Feature:** Personalised Policy Communication Engine
**Release:** 1.0 — "Explain"
**Date:** 2026-06-18

---

## Release-Scope Confirmation

### In This Release

| ID | Story | Deliverable | Dependency |
|---|---|---|---|
| S8 | **Phase 0 data readiness audit** | Per-market report showing attribution coverage % per market, exposure gaps, and ETL backlog for opaque systems | None — first step |
| S1 | **Premium explanation** | Personalised causal renewal notice generated per policy (full attribution) or market-level fallback (partial attribution) per policy | S8 (Phase 0 results determine per-market attribution threshold) |
| S2 | **Batch personalisation at scale** | Pipeline that generates, compliance-checks, and stages 500K notices within 6-hour window at ≤EUR 0.02/notice | S1 (causation data must exist per policy) |
| S4 | **Compliance rule engine pre-flight** | Market-specific rule engine (FCA, BaFin, ACPR, IVASS, DGSFP) validates every notice before dispatch; ≥99.5% pass autonomously | S2 (notices must be generated before they can be checked) |
| S10 | **Multi-language notice generation** | EN, DE, FR, IT, ES from a single pipeline — one prompt template set per language, one rule engine per market | S4 (language + market rules must be loaded per locale) |
| S6 | **Agent-side causation view** | CRM widget showing per-policy causation breakdown to CS agents on inbound calls; P95 <2s at 2,000 concurrent | S1 (causation data must exist to display) |
| S3 | **Fair-value evidence trail** | Evidence pack (notice text + attribution breakdown + source values + compliance checks + audit log) retrievable in <5s per policy; PDF export with DORA headers | S1 + S4 (both the notice and its compliance check must be logged) |

### Deferred to 2.0 — "Respond"

| ID | Story | Deferral reason | Expected release |
|---|---|---|---|
| S5 | **Conversational "why?" follow-up** | RICE 1.0 — value-add on S1; requires Eval Card infrastructure (confidence thresholds, refusal triggers, fallback paths) and additional LLM inference budget | Release 2.0 |

### Parallel Workstream (not gating release)

| ID | Story | Note |
|---|---|---|
| S7 | **A/B test cohort isolation** | Validation experiment that may run alongside or slightly ahead of Release 1.0 build. The S1 value hypothesis (≥2pp controlled churn delta) is tested here. If A/B fails, Release 1.0 ships without the churn-reduction claim — notices are still more transparent and regulator-ready, but the retention ROI hypothesis is invalidated. |

### Dropped

| ID | Story | Reason |
|---|---|---|
| S9 | **Sentiment-driven retention escalation** | RICE 0.5 — lowest score; no outcome metric in the current vision maps to sentiment detection. Unjustified scope creep. Revisit if Release 2.0 requires contact centre automation. |

---

## Open Risks (Release-Blocking or -Delaying)

### Risk 1: Phase 0 attribution coverage fails the threshold

**Description:** If Phase 0 discovers that ≥3 of 5 target markets cannot achieve ≥70% decomposition of premium deltas into tracked causal factors, S1 degrades to fallback templates for those markets. The value hypothesis (≥2pp controlled churn delta) depends on personalised causation — fallback-only markets cannot contribute to the target. The worst case is a market where 0% of variables are exposed (orphaned legacy PAS with read-only access), making even fallback attribution impossible.

**Owner:** Kepler CTO / Migration Lead — owns legacy system access and ETL prioritisation

**Mitigation:** Begin Phase 0 discovery in the 2 highest-volume markets (UK, Germany) first. If either fails the ≥70% threshold, escalate to migration steering committee within 2 weeks — do not wait for all 5 markets. If ≥2 markets fail, scope Release 1.0 to the passing markets only; deferred markets become Release 1.1 with a dedicated ETL bridge programme.

### Risk 2: Regulatory Tier C ruling — mandatory per-notice human review

**Description:** If any target market regulator (FCA, BaFin, ACPR, IVASS, DGSFP) classifies AI-generated renewal notices as requiring mandatory human review before dispatch (Tier C), the 6-hour batch window becomes infeasible. Compliance staffing would need to scale from the current 3-person team to approximately 40 FTEs to review 500K notices within the dispatch cycle. Cost per notice multiplies 10–20×.

**Owner:** Compliance Officer — owns regulator engagement and sandbox submissions

**Mitigation:** Submit sample notices to FCA Innovation Hub and BaFin AI contact point during Phase 0 (Month 1–2). Each submission includes: 3 anonymised notice variants (full causation, fallback, current template) + a 2-page explanation of the human-oversight architecture (compliance rule engine + quarantine workflow + sampling audit). Target: a written Tier B classification (conditional acceptance — periodic sampling, not per-notice review) from ≥3 of 5 regulators before Phase 1 build commit. If any regulator issues a Tier C ruling, that market is deferred to a separate regulatory workstream with pre-approved template library — Release 1.0 ships in the remaining markets.

### Risk 3: Air-gapped orphaned apps block data extraction

**Description:** The 11 orphaned applications (no current owner) include an unknown number running on air-gapped mainframes with no API-level data export. If ≥5 of the 11 are air-gapped, the portion of Kepler's book covered by those systems cannot participate in Phase 0 at all — no attribution data, no personalised notices. Since the scope of these systems is unknown by definition (they're orphaned), the risk cannot be sized until Phase 0 discovery reaches them.

**Owner:** Migration/IT Lead — owns mainframe access and data extraction planning

**Mitigation:** During the Phase 0 discovery kickoff, the first action is an inventory of the 11 orphaned apps with a binary yes/no on "API-level data export possible within 3 months." Any "no" answer triggers a parallel workstream: manual ETL bridge (estimated 4–6 weeks per app, EUR 40K–60K each). If ≥5 apps are air-gapped, the ETL bridge programme becomes a separate Phase 0.5 with its own budget and timeline; those books are deferred to Release 1.1.

---

## Stakeholder Notifications

### To: Delivery Leads (Scope + Risks + Timeline)

**Subject:** Personalised Policy Communication Engine — Release 1.0 confirmation for build

**Body:**

Release 1.0 ("Explain") covers 7 stories across the core pipeline: Phase 0 data audit → per-policy premium decomposition → compliance-validated notice generation in 5 languages → agent-side causation view → fair-value evidence trail. Deferred to 2.0: conversational follow-up (S5). Dropped: sentiment-driven escalation (S9 — no metric justifies it).

**Scope:** S8 → S1 → S2 → S4 → S10 → S6 → S3 (sequential dependency chain — each story depends on the one before it).

**Timeline estimate:** Phase 0 (2–3 months per market, run in parallel for top 2 markets) → Phase 1 build (4–6 months for S1+S2+S4+S10) → S6 and S3 integration (1–2 months, parallel with Phase 1 tail). Estimated first notice in production: Month 8–10 from project start.

**Three risks to track weekly:**

| Risk | Owner | Trigger | Action on trigger |
|---|---|---|---|
| Phase 0 fails ≥70% in ≥2 markets | Kepler CTO | First 2 market audits complete | Escalate to steering committee; scope Release 1.0 to passing markets |
| Regulator issues Tier C (per-notice review) | Compliance Officer | Sandbox response received | Defer affected market to separate workstream; use pre-approved template library |
| ≥5 orphaned apps are air-gapped | Migration/IT Lead | Phase 0 orphaned-app inventory | Launch Phase 0.5 ETL bridge programme with separate budget; defer those books to 1.1 |

**Budget:** Phase 0 EUR 80K per market (top 2 = EUR 160K) + Phase 1 build EUR 500K + S6/S3 integration EUR 150K = EUR 810K total release budget, plus EUR 50K/year run cost.

**Go/no-go gate:** Phase 0 results from top 2 markets + A/B test (S7, EUR 80K) — both must pass before Phase 1 build commit.

---

### To: Business / External Stakeholders (Value + Timeline, Plain Language)

**Subject:** Your renewal notice is about to start making sense

**Body:**

Starting later this year, Kepler Insurance will begin sending renewal notices that actually explain what changed and why.

**What's happening:**
When you receive your next renewal notice, instead of a number with no explanation, you'll see a short, plain-language breakdown of your premium change — for example, "Your premium increased 4%. This is partly because repair costs in your area rose 7%, and partly because your 3-year claims-free record places you in our best-risk tier."

**Why it matters:**
We know renewal notices have been frustrating — our research and customer feedback told us clearly that not understanding a price change feels unfair. From now on, you'll know what you're paying for, and our customer service team will have the same information on their screen if you call with questions.

**When you'll see it:**
Phase 1 launches in two markets later this year (UK and Germany), with all five markets live by mid-2027. If you're in a Phase 1 market, you'll receive the new-style notice at your next renewal. If you're not, the old format continues until your market is added — nothing changes for you until we tell you.

**What we're not doing:**
We're not changing your premium — this is about explaining it, not re-pricing it. We're not selling your data. We're not using AI to make decisions about your policy; the AI only helps write the explanation letter, which is checked by our compliance team before it reaches you.

---

## Release Notes — "Explain" (Customer-Facing)

1. **Your renewal notice now tells you exactly what changed.** Each notice includes a personalised breakdown of your premium change — what went up, what went down, and why — written in plain language, not legalese. *Traces to: S1 — Premium explanation (M1: churn delta, M2: price satisfaction, M3: attribution coverage).*

2. **Calling customer service? They already know what's in your notice.** When you call about your renewal, the agent sees the same causation breakdown on their screen — the total change, the factors driving it, and your policy details. No more reading from a generic script. *Traces to: S6 — Agent-side causation view (M1: churn delta, M3: attribution coverage).*

3. **Your notice has been checked against local regulations before it's sent.** Every notice is reviewed by a compliance rule engine that validates it against the specific requirements of your market's regulator — FCA (UK), BaFin (Germany), ACPR (France), IVASS (Italy), or DGSFP (Spain). You're seeing a regulator-ready explanation, not a marketing message. *Traces to: S4 — Compliance rule engine pre-flight (M6: compliance pass rate).*

4. **Notices generated in English, German, French, Italian, and Spanish** from a single system — one technology pipeline producing regulator-compliant notices in all five Kepler markets. *Traces to: S10 — Multi-language notice generation (M3: attribution coverage per market, M4: batch throughput).*

5. **Complete fair-value evidence available for any policy within seconds.** If a regulator requests evidence for a specific renewal, the complete audit trail — the notice text, the pricing attribution breakdown, the source data values, and the compliance check results — is assembled and exportable within 5 seconds. *Traces to: S3 — Fair-value evidence trail (M7: evidence pack retrieval).*

---

## Spec Section Requiring Update

**06-prd.md — Phase 0 data readiness section:** Update the "In scope / Out of scope" table per-market attribution coverage thresholds with actual Phase 0 results. Specifically: (a) replace the placeholder "≥70% attribution" with actual per-market percentages once Phase 0 completes, (b) document which markets use full personalised causation vs aggregated fallback templates, and (c) add the ETL bridge timeline for any market that falls below the threshold in Phase 0 but is targeted for Release 1.1. This is a living document — the Phase 0 discovery report becomes the new scope authority.
