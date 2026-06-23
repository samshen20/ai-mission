# Traceability Matrix — Stories → Outcome Metrics

**Product:** Kepler Insurance
**Feature:** Personalised Policy Communication Engine
**Date:** 2026-06-18

**Source of metrics:** Vision (01-vision.md) — primary (controlled churn delta) and secondary (price satisfaction). Supporting metrics drawn from Gherkin acceptance criteria NFRs (04-stories-acs.md).

---

## Outcome Metrics

| ID | Metric | Target | Source |
|---|---|---|---|
| **M1** | **Controlled churn delta** | ≥2pp lower churn in treatment vs control (A/B, ≥5K per arm per market, 30-day observation) | 01-vision.md — primary metric |
| **M2** | **Price satisfaction** | ≥25% relative improvement in "premium is fair" agreement (3-question survey, ≥400 responses/mo/market, 95% CI ≤5pt) | 01-vision.md — secondary metric |
| **M3** | **Attribution coverage** | ≥70% of premium change decomposable into tracked causal factors per market | 04-stories-acs.md — S1, S8 ACs |
| **M4** | **Batch throughput** | 500K notices generated + compliance-checked within 6-hour window | 04-stories-acs.md — S2 AC |
| **M5** | **Cost per notice** | ≤EUR 0.02 per notice (LLM inference + compliance check) | 04-stories-acs.md — S2 NFR |
| **M6** | **Compliance pass rate** | ≥99.5% of notices pass market-specific compliance rule engine autonomously | 04-stories-acs.md — S2 AC |
| **M7** | **Evidence pack retrieval** | Complete fair-value evidence pack returned within 5 seconds per policy | 04-stories-acs.md — S3 AC |

---

## Matrix — Stories × Metrics

| Story | M1: Churn delta | M2: Price satisfaction | M3: Attribution coverage | M4: Batch throughput | M5: Cost per notice | M6: Compliance pass rate | M7: Evidence pack retrieval |
|---|---|---|---|---|---|---|---|
| **S1** — Premium explanation | ✅ Generates the delta — personalised causation is the treatment being tested | ✅ Causal language drives understanding → satisfaction | ✅ Requires Phase 0 to decompose premium per policy | | | ✅ Must pass rule engine before dispatch | |
| **S2** — Batch personalisation at scale | | | | ✅ Owns the throughput target — 500K notices in 6h | ✅ Owns the cost ceiling — EUR 0.02/notice | ✅ Enables ≥99.5% autonomous pass rate at scale | |
| **S3** — Fair-value evidence trail | | | | | | | ✅ Owns the 5-second retrieval target |
| **S4** — Compliance rule engine pre-flight | | | | | | ✅ Owns the compliance check — prevents regulatory violations | ✅ Produces the compliance evidence logged for each notice |
| **S6** — Agent-side causation view | ✅ Supports retention — enables agent to answer "why?" and intervene | | ✅ Displays attribution data to agent (same data S1 sends) | | | | |
| **S7** — A/B test cohort isolation | ✅ **Measures this metric** — the A/B test is the measurement instrument for M1 | ✅ Also measures this — NPS/satisfaction survey runs on both cohorts | | | | | |
| **S8** — Phase 0 data readiness audit | | | ✅ **Establishes this metric** — the audit reveals per-market attribution coverage | | | | |
| **S10** — Multi-language notice generation | | | ✅ Requires ≥70% attribution in all 5 target languages/markets | ✅ Adds multi-language throughput but M4 target unchanged | | ✅ Each language market has its own compliance rules | |

---

## Coverage Audit

### Unjustified stories (linked to no metric)

| Story | Status | Reason |
|---|---|---|
| **S5** — Conversational "why?" follow-up | ✅ **Justified (not in top 8)** | Ranked 9/10 (RICE 1.0); not included in this top-8 matrix but links to M1 (supports retention) and M2 (improves understanding) — would be flagged if it were in the top 8 scope |
| **S9** — Sentiment-driven retention escalation | 🔴 **UNJUSTIFIED if scoped into Phase 1** | Ranked 10/10 (RICE 0.5); sentiment detection maps to no outcome metric in the current vision. If this story is in the build scope, it needs a metric: "retention offer acceptance rate" or "switching-intent calls deflected to retention." Without one, it's scope creep. **Recommendation:** Drop S9 from Phase 1 or add a retention-specific metric. |

### Dead metrics (no linked story)

| Metric | Status | Reason |
|---|---|---|
| All 7 metrics (M1–M7) | ✅ **All covered** | Each metric is owned by ≥1 story in the top 8. No dead metrics. |

---

## Summary

| Check | Result |
|---|---|
| Stories in scope (top 8) | **8/8 linked to ≥1 metric** — clean |
| Stories out of scope | **S9 is unjustified** — no metric in current vision maps to sentiment detection. Either define a metric or drop it. S5 is ranked low but would link cleanly. |
| Metrics defined | **7/7 metrics have ≥1 owning story** — no dead metrics |
| Missing metric area | Batch accuracy (hallucination rate) is an NFR in S1 ACs but has no formal metric. If hallucination rate is a board-level concern, add **M8: Notice accuracy** — ≥99% of numerical claims traceable to source data (measured via quarantine rate). |
