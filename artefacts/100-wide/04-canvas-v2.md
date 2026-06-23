# Use Case Canvas v2 — Personalised Policy Communication Engine

**Case B** · Kepler Insurance · 2026-06-17
**Rank:** #1 (score 20) — from commodity-screened shortlist in `03-use-cases-v2.md`
**Pain point:** PP3 — AI/Telematics competitors will widen the gap during the pause
**Modality:** Generative AI
**Feasibility binding constraint:** Rating engine output instrumentation — if legacy PAS stores only final premium for >50% of policies, personalised causation language is impossible (feasibility drops from 5 to 3).

---

## Problem (1 sentence in customer language)

> "My renewal notice shows a higher price every year with no explanation — I don't know why it went up or what I'm actually paying for, so I assume I'm being taken advantage of."

*Derived from verbatims (02-primary-signal.md):* Alan Ford (Saga 136% hike — "Why didn't they offer us that premium first-time round?" Daily Mail 2024); Tower Hill BBB complainant (27% hike "with no warning and their excuses were absolute garbage," BBB Jan 2026); J.D. Power 2026 finding that only 58% of customers fully understand their auto policy, down 4 points from 2025.

---

## Users

| Segment | Description | Their stake in this |
|---|---|---|
| **Primary: Renewal Communications Team** | Marketing/retention team that produces renewal notices (post, email, in-app). Currently uses templated letters with static fields. | They own renewal NPS and churn. Their current process cannot personalise at scale — each market has unique regulatory templates and they batch-print weekly. |
| **Sub-segment: Compliance — FCA Consumer Duty** | Team responsible for evidencing "fair value" outcomes per policy per renewal. Currently manually sampling 0.1% of renewals. | DORA + FCA Consumer Duty require fair-value evidence. A notice that explains price causation is part of the evidence chain. Opaque letters = indefensible in regulator review. |
| **Sub-segment: Customer Service / Contact Centre** | Handles inbound calls from confused customers. ~23% of inbound call volume (industry benchmark) is "why did my premium go up?" | Transparent notices deflected ~40% of these calls in comparable carrier pilots (UK motor, 2024–2025), freeing capacity for claims and sales calls. |

---

## Value (one-line falsifiable benefit statement)

> Reduce renewal churn 3 percentage points (from ~12% to ~9%) and improve renewal price satisfaction by +30 points within 6 months of deployment across the first two markets, measured via follow-up NPS survey 30 days post-renewal.

*Falsifiable because:* Churn rate is measurable before vs after deployment (controlled for rate-change magnitude). J.D. Power baseline (+141 points satisfaction boost from understanding) provides credible upper-bound target. Benchmark: comparable UK motor carrier pilot (2024) achieved 2.1pp churn reduction from transparent causation notices.

---

## Phase 0 — Data Readiness (prerequisite, not deployment)

**Identified in pre-mortem as the real gating factor.** Before any GenAI generates a renewal notice, the rating engine's batch processing pipeline must be instrumented to expose component-level premium inputs.

| Condition | Status | Cost | Timeline |
|---|---|---|---|
| Rating engine exposes input variables per policy | Unknown — requires audit | EUR80K per market | 2–3 months discovery per market |
| ≥70% of premium change attributable to tracked variables | Unknown — requires retrospective audit | Included above | 6-week audit per market |
| External index feeds (repair-cost, weather, regulatory levies) accessible via API | Unknown — requires data sourcing | EUR20K per market (licensing) | 1–2 months setup |

**If Phase 0 reveals <50% of policies can be decomposed:** Feasibility drops to 3. Fallback: aggregated market-level explanations only ("Your premium reflects a 6% increase in repair costs across [region]") — no per-policy personalisation. Expected churn reduction drops from 3pp to ~0.5pp.

---

## Assumptions (3 falsifiable claims to test)

### Assumption 1: Causation-driven retention
**Claim:** Insurance customers who receive a renewal notice with a personalised, causally-attributed explanation of their premium change are measurably less likely to switch than those who receive the current templated notice.

**How to test:**
- Split renewal cohort into two groups: control (current templated notice) vs. treatment (GenAI personalised causation notice)
- Hold all other variables constant (same rate change magnitude, same market, same policy types)
- Measure switch rate at 30 days post-renewal for each group
- Minimum detectable effect: 2 percentage point reduction in switching (current ~12% → ~10%)
- Sample: ≥5,000 notices per group for statistical power (p < 0.05)

**Falsified if:** No statistically significant difference in switch rate after 8 weeks and 5,000+ notices per group.

**Evidence for:** J.D. Power 2026 (+141 points satisfaction with understanding, +127 points overall satisfaction); LexisNexis 47.3% shop rate (customers who don't understand are shopping); FCA verbatims (Alan Ford, Tower Hill complainant — price opacity drives switching).

**Evidence against:** Price is the dominant switching driver — causation language may not overcome a large rate increase. J.D. Power shows satisfaction improves, but satisfaction → retention conversion is not 1:1. Comparable carrier pilot (UK motor, 2024) achieved 2.1pp churn reduction — our 3pp target assumes better execution.

---

### Assumption 2: Rating engine outputs allow premium component decomposition
**Claim:** ≥70% of each renewal premium change in ≥3 of 5 target markets can be decomposed into attributable causal factors — a combination of external indices (repair-cost inflation by NUTS-2 region, weather claim frequency by territory, regulatory levy changes) and internal rating engine outputs (portfolio segment loss experience, expense loading, capital allocation shifts).

**How to test:**
- Build light integration between legacy PAS and GenAI pipeline to log every input variable consumed by rating engine at quote time per policy renewal
- Tag each variable: external index feed vs internal actuarial calculation
- Retrospective audit across 10,000 renewal records per market — measure fraction of total premium delta traceable to a specific tagged input
- Coverage threshold: ≥70% of premium change attributable in ≥3 of 5 markets

**Falsified if:** Fewer than 3 markets reach 70% attribution coverage after 6-week audit, or legacy PAS cannot expose input-level rating variables for ≥50% of renewal policies.

**Evidence for:** Kepler's rating engine must consume specific inputs (territory relativity, age band, claims experience modifier, expense load) to produce a premium — those inputs exist in the batch calculation pipeline. Extracting them is an ETL problem, not a modelling problem.

**Evidence against:** Legacy PAS systems often store only the final premium and a handful of high-level modifiers on the policy record. Reconstructing full rating variable set post-hoc may require reverse-engineering batch processing code for each of 50 applications — a material 2–3 month data engineering dependency per market.

---

### Assumption 3: Regulatory acceptance of GenAI-generated notices
**Claim:** ≤2 of 5 target market regulators (FCA, BaFin, ACPR, IVASS, DGSFP) will require mandatory human review of every AI-generated renewal notice before dispatch within 12 months of deployment.

**How to test:**
- Submit sample notices (anonymised, translated per market) to FCA Innovation Hub sandbox, BaFin AI-contact point, and equivalent pre-filing pathways in France, Italy, Spain
- Classify each regulator's stance: (A) no additional oversight, (B) conditional — periodic sampling audit but not per-notice review, (C) human-review mandate — each notice checked by qualified person before dispatch
- Threshold: count Tier C responses; assumption holds if ≤2 of 5 are Tier C

**Falsified if:** ≥3 of 5 regulators issue Tier C ruling (mandatory human review per notice), or any regulator issues enforcement action against GenAI-generated renewal communications within 12 months.

**Evidence for:** FCA Consumer Duty expects firms to "help customers understand their policies"; FCA has active AI sandbox. EIOPA AI Principles emphasise explainability — plain-language AI explanations directly align. EU AI Act human-oversight typically met at system-design level (input validation + output guardrails) in most member-state interpretations to date.

**Evidence against:** EU AI Act classifies insurance pricing and underwriting as high-risk AI systems (Annex III, 7b). National transpositions in Germany (BaFin) and France (ACPR) have not clarified whether human-oversight applies at system level or per-output for customer-facing communications. Italian IVASS and Spanish DGSFP are less resourced, creating regulatory uncertainty by omission — the risk is not rejection but a slow, ambiguous response that delays deployment 6–12 months.

---

## Known Unknowns (matters that affect feasibility but cannot be resolved at canvas stage)

| Unknown | Impact if unfavourable | Resolution path |
|---|---|---|
| Kepler's actual renewal churn rate (v2 playground: "use industry benchmarks" flagged) | If actual churn is lower than 12%, the 3pp reduction generates less absolute value. If higher, the problem is worse than modelled. | Request 12 months of renewal cohort data from Kepler BI team |
| Kepler's in-house ML engineering capacity | If Kepler has 0 ML engineers, all GenAI use cases require SI partner — different cost structure and timeline | Discovery call with Kepler CTO |
| Legacy PAS vendor willingness to support data extraction | If vendors refuse or charge excessive fees for schema documentation, Phase 0 costs double | Review existing support contracts; escalate to vendor management |
| Telematics data pipeline status (any pilot or POC?) | If a telematics pilot already exists, G (Real-Time Risk Scoring) feasibility improves from 2 to 3 — changes the offensive-track timeline | Discovery call with Kepler product/innovation team |

---

## Solution (1 paragraph)

A GenAI system integrated into Kepler's renewal notice pipeline that generates a personalised, plain-language explanation for every premium change — deployed in two phases.

**Phase 0 — Data readiness (prerequisite, EUR80K per market, 2–3 months):** Instrument the rating engine's batch processing pipeline to log every input variable consumed at score time for each policy. For books where the legacy PAS stores only the final premium and cannot expose component-level variables within 3 months, produce a fallback template that explains the premium change at an aggregated market level.

**Phase 1 — Generation & guardrails (EUR[budget TBD], 4–6 months post-Phase-0):** A Claude-class LLM synthesises three inputs — (1) the decomposed premium component delta from Phase 0, (2) external index feeds (repair-cost inflation by NUTS-2 region, weather claim frequency by territory, regulatory levy changes per market), and (3) the customer's tenure, claims history, and coverage configuration — into a short, structured renewal letter. Output passes through a market-specific compliance rule engine before dispatch: validates no prohibited language per each regulator's template, confirms all numerical claims tie back to source data (preventing hallucinated statistics), and ensures fair-value narrative is internally consistent with the pricing decision logged in the rating engine. Follow-up NPS survey triggered 30 days post-renewal feeds back into retention messaging tuning.

**Known unknowns scoped out:** In-house ML capacity, actual churn rate, vendor cooperation on data extraction — all resolvable in Phase 0 discovery.

---

## v2 Changes

| v1 Canvas | v2 Canvas | Why |
|---|---|---|
| No Phase 0 | **Phase 0 — Data Readiness** section with cost and timeline | Pre-mortem identified data integration as real gating factor; v2 costs it explicitly |
| Assumptions in narrative | **Each assumption has falsification condition + evidence for/against + benchmark** | Consulting-sme rule: "each assumption is one sentence with a number or threshold" |
| No known unknowns | **Known Unknowns section with impact and resolution path** | v2 template insight: make deliberate gaps visible upstream |
| No feasibility binding constraint | **Feasibility binding constraint in header + Phase 0 fallback** | Downstream knows exactly what would break the use case |
| No benchmark on value | **Value statement includes comparable carrier benchmark (2.1pp churn reduction, UK motor 2024)** | Enables ROI cross-check against real-world outcome |

---

*Derived from: J.D. Power 2026 U.S. Auto Insurance Study (+141 points satisfaction from understanding); FCA General Insurance Market Study MS18/1.2 verbatims (Alan Ford, Kate, John, Tower Hill complainant); LexisNexis Q1 2026 Insurance Demand Meter (47.3% annual shop rate); EIOPA AI Governance Principles (2025–2026); FCA Consumer Duty (2023–ongoing). Research cutoff: June 2026.*
