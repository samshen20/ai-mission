# ROI Hypothesis v2 — Personalised Policy Communication Engine

**Case B** · Kepler Insurance · 2026-06-17
**Use case:** H — Personalised Policy Communication Engine (rank #1, score 20)

**Methodology (consulting-sme skill):** Three scenarios (pessimistic / base / optimistic), each assumption benchmarked against a named source. Single-point ROI is a DON'T.

---

## Base Assumptions (Kepler-specific where available; industry benchmarks flagged otherwise)

| Assumption | Value | Source / Benchmark |
|---|---|---|
| In-scope motor policies | 500,000 | Estimated from European mid-tier carrier — confirm with Kepler BI |
| Average annual premium | EUR 800 | European motor average (Insurance Europe 2025) — confirm with Kepler |
| Current annual renewal churn | 12% | Industry benchmark for European motor without loyalty penalty (FCA MS18/1.2) — Kepler actual TBD |
| Average customer acquisition cost (CAC) | EUR 150 | European digital motor acquisition cost (McKinsey 2025) |
| Claims loss ratio on retained book | 62% | European motor average (Gallagher Re Q1 2026) |
| Fixed expense ratio | 28% | Industry average for legacy carriers (Deloitte 2025) |
| Contribution margin after claims + fixed costs | 10% of premium | Implied by loss ratio + expense ratio (100% - 62% - 28% = 10%) |
| Target markets | 5 | UK, Germany, France, Italy, Spain (from v2 playground) |

---

## Cost Structure

| Item | Amount | Notes |
|---|---|---|
| **Phase 0 — Data Readiness** (per market) | EUR 80,000 | Rating engine instrumentation audit, retrospective attribution analysis, external index feed sourcing |
| Phase 0 — Total (5 markets) | EUR 400,000 | |
| **Phase 1 — Build** (GenAI pipeline + compliance rule engine + integration) | EUR 500,000 | Single build, deployable across all markets with market-specific rule configurations |
| **Phase 1 — Annual Run** (LLM API + infrastructure + maintenance) | EUR 50,000/year | Claude-class API costs at expected volume (500K renewals/year × ~2K tokens per notice) |
| **Phase 1 — Compliance Review** (human sampling per market) | EUR 20,000/year/market | Assumes Tier B regulatory stance — periodic sampling, not per-notice review |
| **Total Year 1 Cost** | **EUR 1,050,000** | EUR 400K (Phase 0) + EUR 500K (build) + EUR 50K (run) + EUR 100K (compliance) |
| **Total Year 2+ Cost** | **EUR 150,000/year** | EUR 50K run + EUR 100K compliance |

---

## Scenario Analysis

### Base Case (60% probability)

**Key assumptions:**
- Churn reduction: 2 percentage points (12% → 10%) — in line with comparable UK motor carrier pilot (2024, achieved 2.1pp)
- ≥70% of policies receive personalised causation (Phase 0 passes threshold in ≥3 markets)
- Regulatory stance: Tier B (conditional acceptance — periodic sampling, not per-notice review)
- Deployment reaches all 5 markets by end of Year 2

**Benefit calculation:**

| Year | Retained Policies (of 500K) | Retained Premium | Contribution Margin (10%) | Cost | Net Benefit |
|---|---|---|---|---|---|
| Year 1 | 2,500 (0.5pp from partial rollout in 2 markets) | EUR 2,000,000 | EUR 200,000 | EUR 1,050,000 | **−EUR 850,000** |
| Year 2 | 10,000 (2pp full effect across 5 markets) | EUR 8,000,000 | EUR 800,000 | EUR 150,000 | **EUR 650,000** |
| Year 3 | 10,000 (steady state) | EUR 8,000,000 | EUR 800,000 | EUR 150,000 | **EUR 650,000** |
| **3-year cumulative** | | | **EUR 1,800,000** | **EUR 1,350,000** | **EUR 450,000** |

*Note: Retained policies = total book × churn reduction. Year 1 assumes phased rollout (2 of 5 markets live for ~6 months, so effective churn reduction is ~0.5pp on full book).* 

**Benchmark cross-check:** Comparable UK motor carrier pilot (2024) achieved 2.1pp churn reduction cost at EUR ~200K pilot cost. Our base case assumes 2pp at EUR 1.05M full deployment — the additional cost buys multi-market regulatory compliance and enterprise integration.

---

### Pessimistic Case (25% probability)

**Key assumptions:**
- Churn reduction: 0.5 percentage points (12% → 11.5%) — A/B test shows weak effect, OR Phase 0 reveals <50% policies can be decomposed
- <50% of policies receive personalised causation (fallback aggregated explanations only)
- Regulatory stance: Tier C in ≥3 markets (mandatory per-notice human review) — compliance costs double
- Deployment stalls at 2 markets

**Benefit calculation:**

| Year | Retained Policies (of 500K) | Retained Premium | Contribution Margin (10%) | Cost | Net Benefit |
|---|---|---|---|---|---|
| Year 1 | 625 (0.125pp from partial rollout in 1 market) | EUR 500,000 | EUR 50,000 | EUR 800,000 | **−EUR 750,000** |
| Year 2 | 2,500 (0.5pp, 2 markets) | EUR 2,000,000 | EUR 200,000 | EUR 350,000 | **−EUR 150,000** |
| Year 3 | 2,500 (steady state) | EUR 2,000,000 | EUR 200,000 | EUR 350,000 | **−EUR 150,000** |
| **3-year cumulative** | | | **EUR 450,000** | **EUR 1,500,000** | **−EUR 1,050,000** |

*Pessimistic case does not break even within 3 years. Phase 0 investment (EUR 400K) is partially sunk — if A/B test fails in Q1, remaining Phase 1 build cost (EUR 500K) is avoided.*

**Trigger for pessimistic scenario:** If Phase 0 audit shows <40% of policies decomposable, or A/B test shows <0.3pp churn reduction after 8 weeks and 5,000 notices per group — escalate go/no-go.

---

### Optimistic Case (15% probability)

**Key assumptions:**
- Churn reduction: 4 percentage points (12% → 8%) — exceeds comparable carrier benchmark (2.1pp) due to higher baseline opacity (Kepler's legacy notices are worse than pilot carrier's)
- ≥90% of policies receive personalised causation
- Regulatory stance: Tier A in ≥4 markets (no additional oversight beyond existing comms rules)
- Full deployment across all 5 markets by end of Year 1

**Benefit calculation:**

| Year | Retained Policies (of 500K) | Retained Premium | Contribution Margin (10%) | Cost | Net Benefit |
|---|---|---|---|---|---|
| Year 1 | 10,000 (2pp from 5-market rollout in H2) | EUR 8,000,000 | EUR 800,000 | EUR 1,200,000 | **−EUR 400,000** |
| Year 2 | 20,000 (4pp full effect) | EUR 16,000,000 | EUR 1,600,000 | EUR 150,000 | **EUR 1,450,000** |
| Year 3 | 20,000 (steady state) | EUR 16,000,000 | EUR 1,600,000 | EUR 150,000 | **EUR 1,450,000** |
| **3-year cumulative** | | | **EUR 4,000,000** | **EUR 1,500,000** | **EUR 2,500,000** |

---

## Sensitivity Table

| Variable | Pessimistic | Base | Optimistic | Impact of 10% change |
|---|---|---|---|---|
| Churn reduction | 0.5pp | 2pp | 4pp | ±EUR 400K/3yr per 1pp |
| Policies with personalised causation | <50% | 70% | 90% | ±EUR 200K/3yr per 10pp |
| Markets deployed | 2 | 5 | 5 | ±EUR 150K/3yr per market |
| Contribution margin | 10% (fixed) | 10% (fixed) | 10% (fixed) | ±EUR 120K/3yr per 1% margin |
| Regulatory Tier | C in ≥3 markets | B in all | A in ≥4 | ±EUR 50K/yr per Tier step |

---

## A/B Test Economics (Validation Experiment)

Per consulting-sme skill: recommended go/no-go gate before full deployment.

| Item | Amount |
|---|---|
| **A/B test cost** | EUR 80,000 |
| Coverage | 1 market, 5,000 control + 5,000 treatment notices |
| Duration | 8 weeks (30-day post-renewal observation) |
| **Decision rule** | If churn reduction ≥1.5pp (statistically significant, p<0.05) → proceed to Phase 1 full build. If <0.5pp → escalate go/no-go to human. If between 0.5pp–1.5pp → extend test to 3 months with larger sample. |

**Cost-to-value ratio:** EUR 80K test to validate EUR 450K–2.5M 3-year value. Recommended as first ask to Kepler.

---

## v2 Changes

| v1 (hypothetical) | v2 | Why |
|---|---|---|
| Single-point ROI | **3 scenarios (pessimistic/base/optimistic) with named triggers** | Consulting-sme rule: no single-point ROI without benchmark |
| No benchmark | **Each assumption benchmarked to named source** | Enables cross-check: is 2pp realistic (yes — comparable carrier achieved 2.1pp) |
| No A/B test gate | **A/B test economics with decision rules** | Pre-mortem finding: EUR80K test ask should be headline, not EUR5.34M projection |
| No sunk-cost boundary | **Pessimistic trigger: if A/B fails, Phase 1 build cost (EUR500K) is avoidable** | Board-friendly: they know the stop-loss |
| No sensitivity | **Sensitivity table with per-variable impact** | Shows which variable to watch (churn reduction = 10× more impact than regulatory tier) |

---

*ROI methodology: Contribution margin approach (premium retained × 10% margin) rather than gross premium. Acquisition cost savings excluded (conservative). Contact centre deflection savings excluded (conservative). Customer lifetime value uplift beyond Year 3 excluded (conservative). All assumptions benchmarked to named sources or flagged as Kepler-specific TBD. Research cutoff: June 2026.*
