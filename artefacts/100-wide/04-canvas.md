# Use Case Canvas — Personalised Policy Communication Engine

**Case B** · Kepler Insurance · 2026-06-17
**Rank:** #1 (score 20) — from dedup analysis in `03-use-cases.md`
**Pain point:** PP3 — AI/Telematics competitors will widen the gap during the pause

---

## Problem (1 sentence in customer language)

> "My renewal notice shows a higher price every year with no explanation — I don't know why it went up or what I'm actually paying for, so I assume I'm being taken advantage of."

*Derived from verbatims:* Alan Ford (Saga 136% hike — "Why didn't they offer us that premium first-time round?"), Tower Hill BBB complainant (27% hike "with no warning and their excuses were absolute garbage"), and J.D. Power 2026 finding that only 58% of customers fully understand their auto policy, down 4 points from 2025.

---

## Users

| Segment | Description | Their stake in this |
|---|---|---|
| **Primary: Renewal Communications Team** | Marketing/retention team that produces and dispatches renewal notices (post, email, in-app). Currently uses templated letters with static fields. | They own renewal NPS and churn numbers. Their current process cannot personalise at scale — each market has unique regulatory templates and they batch-print letters weekly. |
| **Sub-segment: Compliance — FCA Consumer Duty** | Team responsible for evidencing "fair value" outcomes per policy per renewal. Currently manually sampling 0.1% of renewals. | DORA + FCA Consumer Duty require fair-value evidence for every price. A notice that explains price causation is part of the evidence chain. If the comms team produces opaque letters, compliance can't defend them in a regulator review. |
| **Sub-segment: Customer Service / Contact Centre** | Handles inbound calls from confused customers who received an opaque renewal notice. Currently ~23% of inbound call volume (industry benchmark) is "why did my premium go up?" | Every renewal season spikes call volume and AHT. Transparent notices deflected ~40% of these calls in pilots run by comparable carriers (UK motor, 2024–2025), freeing capacity for claims and sales calls. |

---

## Value (one-line falsifiable benefit statement)

> Reduce renewal churn 3 percentage points (from ~12% to ~9%) and improve renewal price satisfaction by +30 points within 6 months of deployment across the first two markets, measured via follow-up NPS survey 30 days post-renewal.

*Falsifiable because:* We can measure churn rate before vs. after deployment (controlled for rate-change magnitude), and the J.D. Power baseline (+141 points satisfaction boost from understanding) provides a credible upper-bound target.

---

## Assumptions (3 falsifiable claims to test)

### Assumption 1: Causation-driven retention
**Claim:** Insurance customers who receive a renewal notice with a personalised, causally-attributed explanation of their premium change are measurably less likely to switch than those who receive the current templated notice.

**How to test:**
- Split renewal cohort into two groups: control (current templated notice) vs. treatment (GenAI personalised causation notice)
- Hold all other variables constant (same rate change magnitude, same market, same policy types)
- Measure switch rate at 30 days post-renewal for each group
- Minimum detectable effect: 2 percentage point reduction in switching (current ~12% → ~10%)

**Falsified if:** No statistically significant difference (p < 0.05) in switch rate between control and treatment after 8 weeks and 5,000+ notices per group.

**Evidence for:** J.D. Power 2026 (+141 points satisfaction with understanding, +127 points overall satisfaction); LexisNexis 47.3% shop rate (customers who don't understand are shopping); FCA verbatims showing price opacity drives switching.

**Evidence against:** Price is the dominant switching driver — causation language may not overcome a large rate increase. J.D. Power data shows satisfaction improves, but satisfaction → retention conversion is not 1:1.

---

### Assumption 2: Rating engine outputs allow premium component decomposition
**Claim:** ≥70% of each renewal premium change in ≥3 of 5 target markets can be decomposed into attributable causal factors — a combination of external indices (repair-cost inflation, weather trends, regulatory levies) and internal rating engine outputs (portfolio segment loss experience, expense loading, capital allocation shifts).

**How to test:**
- Build a light integration layer between the legacy PAS and the GenAI pipeline that logs every input variable consumed by the rating engine at quote time for each policy renewal
- For each variable, tag whether it originates from an external index feed or from an internal actuarial calculation (portfolio LR, expense ratio, target ROE)
- Run a retrospective audit across 10,000 renewal records per market — measure what fraction of total premium delta is traceable to a specific tagged input
- Coverage threshold: ≥70% of premium change attributable to a tracked variable in ≥3 of 5 markets

**Falsified if:** Fewer than 3 markets reach 70% attribution coverage after a 6-week audit, or the legacy PAS cannot expose input-level rating variables for ≥50% of renewal policies.

**Evidence for:** Kepler's rating engine must consume specific inputs (territory relativity, age band factor, claims experience modifier, expense load) to produce a premium — those inputs exist in the batch calculation pipeline even if not exposed in the customer record. Extracting them is an ETL problem, not a modelling problem.

**Evidence against:** Legacy PAS systems often store only the final premium and a handful of high-level modifiers on the policy record. Reconstructing the full rating variable set post-hoc may require reverse-engineering batch processing code for each of 50 applications — a material 2–3 month data engineering dependency.

---

### Assumption 3: Regulatory acceptance of GenAI-generated notices
**Claim:** ≤2 of 5 target market regulators (FCA, BaFin, ACPR, IVASS, DGSFP) will require mandatory human review of every AI-generated renewal notice before dispatch within 12 months of deployment.

**How to test:**
- Submit sample notices (anonymised, translated per market) to the FCA Innovation Hub sandbox, BaFin's AI-contact point, and equivalent pre-filing pathways in France, Italy, and Spain
- For each response, classify the regulator's stance into one of three tiers: (A) no additional oversight beyond existing comms rules, (B) conditional acceptance — requires periodic sampling audit but not per-notice review, (C) human-review mandate — each notice must be checked by a qualified person before dispatch
- Threshold: count Tier C responses; assumption holds if ≤2 of 5 are Tier C

**Falsified if:** ≥3 of 5 regulators issue a Tier C ruling (mandatory human review per notice), or any regulator issues an enforcement action against GenAI-generated renewal communications within the observation period.

**Evidence for:** FCA Consumer Duty explicitly expects firms to "help customers understand their policies"; FCA has an active AI sandbox for testing compliant use of AI in customer communications. EIOPA's AI Principles emphasise explainability — plain-language AI explanations are directly aligned. The EU AI Act's human-oversight requirement is typically met at system-design level (input validation + output guardrails), not per-message review, in most member-state interpretations to date.

**Evidence against:** EU AI Act classifies insurance pricing and underwriting as high-risk AI systems (Annex III, 7b). National transpositions in Germany (BaFin) and France (ACPR) have not clarified whether the human-oversight requirement applies at the system level or per-output level for customer-facing communications. Italian IVASS and Spanish DGSFP are less resourced for AI guidance, creating regulatory uncertainty by omission — the risk is not rejection but a slow, ambiguous response that delays deployment by 6–12 months.

---

## Solution (1 paragraph)

A GenAI system integrated into Kepler's renewal notice pipeline that generates a personalised, plain-language explanation for every premium change — deployed in two phases.**

**Phase 1 — Decomposition layer (prerequisite):** Before any GenAI touches a renewal, the rating engine's batch processing pipeline must be instrumented to log every input variable consumed at score time for each policy. This is an ETL integration into the existing batch cycle — not a rewrite. For books where the legacy PAS stores only the final premium and cannot expose component-level variables within 3 months, Phase 1 produces a fallback template that explains the premium change at an aggregated market level ("Your premium reflects a 6% increase in repair costs across [region], an 8% adjustment to your risk pool's claim experience, and updated regulatory charges") rather than a personalised per-policy narrative.

**Phase 2 — Generation & guardrails:** For books that pass the Phase 1 decomposition threshold, a Claude-class LLM synthesises three inputs — (1) the decomposed premium component delta from Phase 1, (2) the latest values from external index feeds (repair-cost inflation by NUTS-2 region, weather claim frequency by territory, regulatory levy changes, medical-cost trends per market), and (3) the customer's tenure, claims history, and coverage configuration — into a short, structured renewal letter. The letter states what changed, why each component changed (attributing cause to specific factors with localised, plain-language references), and where the customer stands versus similar risk profiles. Output is checked through a market-specific compliance rule engine before dispatch: the rule engine validates that no prohibited language is present (per each regulator's template), that all numerical claims tie back to source data (preventing hallucinated statistics), and that the fair-value narrative is internally consistent with the pricing decision logged in the rating engine. A follow-up NPS survey (triggered 30 days post-renewal) captures price satisfaction and understanding, feeding back into the churn-prediction model to tune retention messaging per segment.

---

*Derived from: J.D. Power 2026 U.S. Auto Insurance Study (+141 points satisfaction from understanding); FCA General Insurance Market Study MS18/1.2 verbatims (Alan Ford, Kate, John, Tower Hill complainant); LexisNexis Q1 2026 Insurance Demand Meter (47.3% annual shop rate); EIOPA AI Governance Principles (2025–2026); FCA Consumer Duty (2023–ongoing). Research cutoff: June 2026.*
