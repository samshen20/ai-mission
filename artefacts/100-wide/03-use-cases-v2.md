# AI Use Cases Against Three Strategic Pain Points — v2

**Case B** · Kepler Insurance · 2026-06-17

**Methodology (consulting-sme skill):** Each use case is scored value (1–5) × feasibility (1–5), traced to one named pain point, and given a no-AI baseline + binding constraint per feasibility score. Top 3 pass a commodity-vs-novel screen.

**Pain points drawn from:** 01-context-brief.md (market research) and 02-primary-signal.md (customer verbatims + competitor teardown + re-rating).

---

## Pain Point 1: Legacy Tech Cost Base Is Unsustainable in a Soft Market

**Confirmed & Sharpened** — FCA verbatims prove switching is efficient and loyalty is zero. Every $1 of legacy overhead limits pricing flexibility when 53% of customers are shopping.

### 1.1 Infrastructure Cost Anomaly Detection & Forecasting (Classical ML)

**What:** A supervised/unsupervised ML model on AWS + Azure billing streams that learns normal spend patterns per application (50 in scope), detects anomalies in real-time (orphaned resources, oversized instances, unused reserved capacity), and forecasts 30/60/90-day costs per migration wave.

**Pain point link:** PP1 — Legacy cost base
**Key evidence from 02:** Tower Hill 27% hike (BBB 2026) — opaque pricing on legacy systems is a regulatory liability; Peter verbatim (switching efficiency means cost advantage compounds).

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Real savings (15–30% cloud spend reduction typical). Finite window — benefits decline post-migration. |
| **Feasibility** | 5 | Cloud billing data is clean and standardized (AWS CUR, Azure exports). ML on time-series is a solved problem. Mature vendor ecosystem. |
| **Feasibility binding constraint** | None — data is abundant, models are commodity, integration is API-level. |

**No-AI baseline:** Threshold-based cloud vendor budgets + email alerts. Catches major overruns (>20% of budget) but misses gradual drift, orphaned resources, and right-sizing opportunities. Typical savings capture: 5–10% vs 15–30% with ML.

**Fallback if blocked:** Threshold-based rules (cloud vendor budgets + alerts) if labelling historical spend data is impossible.

---

### 1.2 Legacy Code Documentation & Migration Translator (Generative AI)

**What:** A GenAI assistant (RAG on the codebase + architecture docs) that reads legacy COBOL, Java, and proprietary 4GL code, generates business-logic documentation, data-flow diagrams, and target-Azure service mapping. For each of the 11 orphaned applications it produces a "survival guide."

**Pain point link:** PP1 — Legacy cost base
**Key evidence from 02:** RACQ data integrity failure during system transition (ABC News, Sep 2025); 11 orphaned apps have no SME to explain business logic.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | 11 orphaned apps are existential migration risk. Without business-logic documentation, those apps cannot be migrated reliably. |
| **Feasibility** | 3 | Code may be on isolated/air-gapped mainframes. LLM hallucination risk for undocumented business rules. Governance approval needed for code upload to LLM. |
| **Feasibility binding constraint** | Code accessibility — if ≥5 of 11 orphaned apps are on air-gapped mainframes with no API-level code export, feasibility drops to 2 (requires manual transcription). |

**No-AI baseline:** Manual SME-led documentation (2–3 senior engineers, 6 months, estimated EUR250K–400K). Still impossible if no SME exists for the orphaned apps — the AI baseline is the only viable path for 11 orphaned apps with no owner.

**Fallback if blocked:** Semi-automated — run static analysis tools (SonarCloud, CAST) and feed output to LLM for summarisation only, without raw code exposure.

---

### 1.3 Autonomous Cloud Cost Optimisation Agent (Agentic)

**What:** A continuous agent that monitors the AWS + on-prem → Azure migration pipeline and autonomously identifies/terminates orphaned resources, recommends RI/SP purchases based on confirmed migration waves, detects idle on-prem servers post-cutover, and triggers decommission workflows.

**Pain point link:** PP1 — Legacy cost base
**Key evidence from 02:** Peter verbatim ("you work for an hour and save £50" — switching efficiency means cost compounds into market share shift); dual AWS+on-prem footprint.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Continuous savings capture across 18-month migration window. Human FinOps team cannot monitor 50 apps daily across 3 environments. |
| **Feasibility** | 4 | Orchestration (Lambda + Azure Automation + vendor APIs) is well-understood. Destruction guardrails are the only complexity. |
| **Feasibility binding constraint** | Approval workflow maturity — Kepler's change management process must support automated resource termination. If change advisory board requires >48h approval for all infra changes, autonomous remediation is blocked and feasibility drops to 2 (read-only agent). |

**No-AI baseline:** Weekly FinOps meeting reviewing cost reports. Orphaned resources survive 5–7 days on average before detection. Estimated 40–60% of potential savings lost to detection lag.

**Fallback if blocked:** Read-only agent that surfaces recommendations to a human approver via Slack/Jira (semi-autonomous).

---

### 1.4 Migration Sequencing Optimiser (Classical ML / Optimisation)

**What:** A combinatorial optimisation model that takes the 50 applications' dependency graph, data volumes, compliance tier (SOX, GDPR), owner status, and cost-per-wave, and outputs the optimal migration sequence.

**Pain point link:** PP1 — Legacy cost base
**Key evidence from 02:** $31M remaining budget; Kate verbatim ("loyalty paid zero" — every month of dual-footprint is dead money); 11 orphaned apps increase sequencing risk.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 3 | One-time optimisation. Rule-based heuristic (claims-first, orphaned-last) captures most savings. |
| **Feasibility** | 3 | Dependency graph likely incomplete. Hard constraints shift unpredictably (freeze periods, claims spikes). |
| **Feasibility binding constraint** | Dependency graph completeness — if <60% of inter-app dependencies are documented, the model's output is no more reliable than heuristic ranking. |

**No-AI baseline:** Spreadsheet-ranked "easiest first" heuristic with manual override. Captures ~80% of optimal savings with zero modelling cost.

**Fallback if blocked:** Heuristic rules (any claims app = wave 1; orphaned app with no known dependencies = wave 3; all others = wave 2) with manual override.

---

## Pain Point 2: Regulatory Risk Peaks During Migration Without DORA-Compliant Resilience Planning

**Confirmed** — the RACQ case (ASIC lawsuit over 570K misleading renewal notices) is a direct precedent for data-integrity failures during system transitions. 11 orphaned apps are material DORA compliance exposures.

### 2.1 Data Integrity Anomaly Detection During Cutover (Classical ML)

**What:** An ML model that monitors dual-running systems (old + new) during each application cutover and cross-validates policy data, premium calculations, renewal notice content, and claims records. Flags discrepancies before notice issuance.

**Pain point link:** PP2 — Regulatory risk
**Key evidence from 02:** RACQ 570K misleading renewal notices (ABC News, Sep 2025; ASIC lawsuit); Tower Hill 27% hike with no warning (BBB, Jan 2026); DORA in force Jan 2025.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | RACQ precedent proves regulatory liability from migration data errors is real and expensive. Prevents that outcome across 50 cutovers. |
| **Feasibility** | 3 | Cross-schema field mapping is labour-intensive per application. False positives could delay renewals (operational risk). Needs dual-system read access. |
| **Feasibility binding constraint** | Dual-system read access — if <60% of legacy systems can expose policy data in real time during parallel run, coverage gap means ML model validates an incomplete picture. |

**No-AI baseline:** Manual sampling (0.1% of policies) comparing old vs new system outputs. Misses the systematic error that caused the RACQ failure. Regulatory liability remains.

**Fallback if blocked:** Rule-based reconciliation (field-by-field comparison of a sample set, with automated expansion when discrepancies found).

---

### 2.2 DORA Compliance Evidence Generator (Generative AI)

**What:** A GenAI pipeline that ingests structured and unstructured data from the migration programme — incident logs, resilience test results, third-party vendor risk assessments, change tickets, architecture decisions — and produces DORA-mandated documentation (ICT Risk Assessment reports, resilience testing evidence packs, third-party risk register updates).

**Pain point link:** PP2 — Regulatory risk
**Key evidence from 02:** DORA resilience testing mandate (Regulation 2022/2554); 18-month migration means continuous ICT change — every cutover is reportable.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Automates a mandatory recurring process (~40 hours per compliance milestone). Direct regulatory requirement, no optionality. |
| **Feasibility** | 4 | RAG on regulatory corpus is well-understood tech. Data sources are structured and API-accessible. Output is for human review — 95% accuracy acceptable. |
| **Feasibility binding constraint** | Data pipeline integration — if Jira, Azure Monitor, and PagerDuty APIs are not accessible from the GenAI pipeline's environment (e.g. air-gapped compliance network), feasibility drops to 2. |

**No-AI baseline:** Manual compliance evidence compilation by a 3-person compliance team. Estimated 40 hours per milestone, risk of missed deadlines, inconsistent formatting across reports.

**Fallback if blocked:** Structured compliance checklist generator (prompt-engineered output) with manual evidence upload — less automation but still 3× productivity gain.

---

### 2.3 DORA Compliance Monitoring & Remediation Agent (Agentic)

**What:** A continuous agent that monitors the 50-application migration against DORA requirements — tracks incident-reporting timelines, validates resilience testing coverage, detects orphaned-app compliance gaps, assembles remediation tickets, maintains a live compliance scoreboard.

**Pain point link:** PP2 — Regulatory risk
**Key evidence from 02:** 11 orphaned apps with no owner = material DORA gap; DORA resilience testing mandate; RACQ precedent.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Continuous oversight across 50 apps — human team cannot maintain this at scale. Overlaps with 2.2 but serves a different consumer (ops team vs regulator). |
| **Feasibility** | 3 | Cross-system orchestration complexity (Jira, Azure Policy, AWS Config, vendor APIs). False negatives create false confidence — dangerous. |
| **Feasibility binding constraint** | API coverage across compliance toolchain — if <4 of 6 required data sources (Jira, Azure Monitor, Azure Policy, AWS Config, PagerDuty, vendor compliance feeds) are API-accessible, agent's monitoring coverage is gappy and unreliable. |

**No-AI baseline:** Manual compliance tracking via spreadsheet, updated weekly by a compliance officer. Detection lag of 5–10 business days for any compliance gap.

**Fallback if blocked:** Rule-based compliance checklist with Jira automation (email reminders per app per DORA requirement).

---

## Pain Point 3: AI/Telematics Competitors Will Widen the Gap During the Pause

**Sharpened** — CMT's DriveWell Atlas foundation models (Oct 2025) and Allianz's $350M co-ownership stake create compounding, non-linear competitive advantage. FCA verbatims show zero loyalty friction.

### 3.1 Real-Time Risk Scoring Engine (Classical ML)

**What:** An ML model that ingests telematics data, claims history, credit indicators, and external contextual signals to produce a real-time risk score per policy at quote time — replacing batch-rated (weekly) pricing.

**Pain point link:** PP3 — AI/Telematics gap
**Key evidence from 02:** CMT DriveWell Atlas foundation models (Oct 2025); Allianz $350M co-ownership stake (2026); 55M+ driver dataset; FCA verbatims (zero loyalty friction).

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | Core competitive response to Allianz CMT. Without real-time scoring, Kepler systematically misprices good risks (too high → they churn) and bad risks (too low → adverse selection). |
| **Feasibility** | 2 | Chicken-and-egg: scoring accuracy improves with telematics data, but telematics adoption requires the scoring capability. Legacy PAS cannot easily ingest real-time scores. EIOPA explainability adds regulatory gate. |
| **Feasibility binding constraint** | Telematics data pipeline — Kepler has 0% telematics penetration today. Building a telematics data pipeline + achieving statistically significant volume (>10K active policies) is an 18–24 month programme before the ML model trains on meaningful data. |

**No-AI baseline:** Current batch-rated GLM pricing on weekly cycle. Allianz's real-time scores are 7 days fresher on day 1 of any quote — the gap compounds with every shopping event for 53% of the market.

**Fallback if blocked:** Simplified GLM-based score with fewer features — explainable by default for regulators, but no real-time capability.

---

### 3.2 Personalised Policy Communication Engine (Generative AI)

**What:** A GenAI system that generates personalised renewal communications per customer — in their language, explaining premium changes with transparent causation ("Your premium increased 4% due to 7% repair-cost inflation in your region and your 3-year claims-free status in our best-risk tier").

**Pain point link:** PP3 — AI/Telematics gap
**Key evidence from 02:** Alan Ford verbatim ("Why didn't they offer us that premium first-time round?" Daily Mail 2024); Tower Hill complainant ("excuses were absolute garbage," BBB Jan 2026); Kate verbatim ("easier to leave it run" — inertia, not loyalty); J.D. Power 2026 (+141 points satisfaction from understanding).

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | +141 points price satisfaction (J.D. Power 2026). Low investment, measurable retention impact. Primarily retains existing customers — does not improve acquisition or pricing competitiveness. |
| **Feasibility** | 5 | Simplest tech stack (GenAI + RAG on policy data + external index calls). Single API hook into renewal pipeline. Regulatory alignment (FCA Consumer Duty transparency requirement). |
| **Feasibility binding constraint** | Rating engine output instrumentation — if legacy PAS stores only final premium for >50% of policies (no component-level variables), personalised causation language is impossible for those policies. Feasibility drops to 3 (fallback: aggregated market-level explanation). |

**No-AI baseline:** Templated renewal letters with static fields. Current opaque notices drive the verbatim complaints in 02-primary-signal.md. J.D. Power shows only 58% of customers understand their policy.

**Fallback if blocked:** Templated renewal letters with dynamic variables for the causal explanation section — less personalised but still beats opaque notices.

---

### 3.3 Competitive Pricing Response Agent (Agentic)

**What:** An agentic system that continuously monitors competitor pricing — aggregate data, rate filings, Allianz telematics product signals, aggregator market quotes — and simulates Kepler's optimal pricing response in real-time, auto-adjusting within pre-approved risk appetite bands.

**Pain point link:** PP3 — AI/Telematics gap
**Key evidence from 02:** FCA verbatims prove switching is frictionless and loyalty is dead (53% shopping rate, J.D. Power 2026); Allianz CMT gives Allianz faster pricing cycles; Progressive vs GEICO divergence shows speed advantage compounds.

| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | Compresses pricing response from 4–8 weeks to hours. In a 53%-shopping market, 24-hour response captures share before competitor's marketing cycle completes. |
| **Feasibility** | 2 | Aggregator API data availability varies by European market. Legacy PAS may not support real-time rating engine writes. Faces DORA algorithmic pricing governance + FCA fair value compliance per auto-adjusted price. Highest regulatory barrier. |
| **Feasibility binding constraint** | Regulatory approval for algorithmic pricing — if the FCA and/or BaFin require pre-approval of any automated pricing engine (not yet clarified in 2026 guidance), the timeline extends 6–12 months regardless of technical readiness. |

**No-AI baseline:** Manual actuarial pricing review cycle (4–8 weeks). By the time Kepler responds to a competitor move, Allianz has captured the switching cohort, refiled rates, and moved to the next segment.

**Fallback if blocked:** Semi-autonomous — agent surfaces recommended pricing responses via daily digest with "approve all" / "approve selected" / "reject" workflow. Still compresses from 4–8 weeks to same-day for approved changes.

---

## Summary Matrix

| Use Case | PP | Modality | Key Evidence from 02 | Feasibility Constraint | No-AI Baseline |
|---|---|---|---|---|---|
| 1.1 Infra Cost Anomaly Detection | PP1 | Classical ML | Tower Hill 27% hike (BBB 2026) | None — abundant data | Threshold-based alerts |
| 1.2 Legacy Code Documentation | PP1 | GenAI | RACQ data integrity failure | Code accessibility (air-gap) | Manual SME (EUR250–400K) |
| 1.3 Autonomous Cost Optimisation | PP1 | Agentic | Peter verbatim (switching efficiency) | CAB approval speed | Weekly FinOps meeting |
| 1.4 Migration Sequencing Optimiser | PP1 | ML/OR | Kate verbatim (loyalty = zero) | Dependency graph completeness | Spreadsheet heuristic |
| 2.1 Data Integrity Anomaly Detection | PP2 | Classical ML | RACQ 570K notices (ASIC lawsuit) | Dual-system read access | Manual 0.1% sampling |
| 2.2 DORA Compliance Evidence Gen | PP2 | GenAI | DORA in force Jan 2025 | API accessibility (air-gap) | 3-person compliance team |
| 2.3 DORA Compliance Agent | PP2 | Agentic | 11 orphaned apps (DORA gap) | API coverage of toolchain | Manual weekly spreadsheet |
| 3.1 Real-Time Risk Scoring | PP3 | Classical ML | DriveWell Atlas (Oct 2025); $350M Allianz | Telematics data pipeline (0% today) | Batch GLM weekly cycle |
| 3.2 Personalised Policy Comms | PP3 | GenAI | Alan Ford (Daily Mail 2024); +141 JDP | Rating engine instrumentation | Opaque templated letters |
| 3.3 Competitive Pricing Response | PP3 | Agentic | FCA verbatims (zero loyalty); 53% shop rate | Reg pre-approval for algo pricing | 4–8 week actuarial cycle |

---

## Scoring: Value (1–5) × Feasibility (1–5)

### A: Cloud Cost Anomaly Detection & Optimisation (1.1 + 1.3 consolidated)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 4 | 15–30% cloud spend reduction | — |
| Feasibility | 5 | Abundant data, commodity models, API-level integration | None — mature SaaS ecosystem; lowest-risk of all 10 |
| **Score** | **20** | | |

### B: Legacy Code Documentation & Migration Translator (1.2)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 5 | Existential migration risk for 11 orphaned apps | — |
| Feasibility | 3 | Code air-gap, LLM hallucination, governance approval | ≥5 orphaned apps air-gapped → feasibility drops to 2 |
| **Score** | **15** | | |

### C: Migration Sequencing Optimiser (1.4)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 3 | One-time, bounded savings (5–15% over heuristic) | — |
| Feasibility | 3 | Incomplete dependency graph + shifting hard constraints | <60% deps documented → model no better than heuristic |
| **Score** | **9** | | |

### D: Data Integrity Anomaly Detection During Cutover (2.1)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 5 | Prevents RACQ-style regulatory liability | — |
| Feasibility | 3 | Cross-schema mapping; false positive risk; dual-read access | <60% legacy systems expose real-time data → incomplete coverage |
| **Score** | **15** | | |

### E: DORA Compliance Evidence Generator (2.2)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 4 | Mandatory recurring process; 40h/milestone | — |
| Feasibility | 4 | RAG on regulation text; structured data sources | API access blocked by air-gap → feasibility 2 |
| **Score** | **16** | | |

### F: DORA Compliance Monitoring & Remediation Agent (2.3)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 4 | Continuous oversight at 50-app scale | — |
| Feasibility | 3 | Cross-system orchestration; false negative risk | <4/6 API sources accessible → gappy coverage |
| **Score** | **12** | | |

### G: Real-Time Risk Scoring Engine (3.1)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 5 | Core competitive response to Allianz CMT | — |
| Feasibility | 2 | 0% telematics today; legacy PAS; EIOPA gate | Telematics data pipeline requires 18–24 months to build before model trains |
| **Score** | **10** | | |

### H: Personalised Policy Communication Engine (3.2)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 4 | +141 pts satisfaction; low investment | — |
| Feasibility | 5 | Simplest tech stack; regulatory alignment | >50% policies store only final premium → feasibility 3 (fallback mode) |
| **Score** | **20** | | |

### I: Competitive Pricing Response Agent (3.3)
| Dimension | Score | Rationale | Binding Constraint |
|---|---|---|---|
| Value | 5 | Compresses 4–8 weeks → hours | — |
| Feasibility | 2 | Highest regulatory barrier of all 10 | FCA/BaFin pre-approval unclear → 6–12 month timeline risk |
| **Score** | **10** | | |

### Scoreboard

| Rank | ID | Survivor | Value | Feasibility | **Score** | Binding Constraint (if any) |
|---|---|---|---|---|---|---|
| 1 | A | Cloud Cost Anomaly Detection & Optimisation | 4 | 5 | **20** | None |
| 1 | H | Personalised Policy Communication Engine | 4 | 5 | **20** | Rating engine instrumentation |
| 3 | E | DORA Compliance Evidence Generator | 4 | 4 | **16** | API air-gap |
| 4 | B | Legacy Code Documentation & Migration Translator | 5 | 3 | **15** | Code accessibility |
| 4 | D | Data Integrity Anomaly Detection During Cutover | 5 | 3 | **15** | Dual-system read access |
| 6 | F | DORA Compliance Monitoring & Remediation Agent | 4 | 3 | **12** | API coverage |
| 7 | G | Real-Time Risk Scoring Engine | 5 | 2 | **10** | Telematics pipeline (18–24mo) |
| 7 | I | Competitive Pricing Response Agent | 5 | 2 | **10** | Reg pre-approval |
| 9 | C | Migration Sequencing Optimiser | 3 | 3 | **9** | Dependency graph completeness |

---

## Top 3 Selection & Commodity Check

### Commodity check: A — Cloud Cost Anomaly Detection & Optimisation
| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Yes** | CloudHealth, ProsperOps, Vantage, Azure Cost Management, AWS Cost Explorer, CloudCheckr — 10+ established tools. |
| Standardized? | **Yes** | Cloud billing data schemas (AWS CUR, Azure exports) are standardised per provider. ML pattern is identical across vendors. |
| Low switching cost? | **Yes** | SaaS tools with API access; switching takes weeks. No proprietary lock-in. |
| **Verdict** | **COMMODITY** | Carrying this as a competitive AI capability is indefensible. |

### Commodity check: H — Personalised Policy Communication Engine
| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Partial** | Generic personalisation engines exist; none solve *insurance renewal causation with regulatory compliance*. |
| Standardized? | **No** | Each market has different regulatory requirements (FCA Consumer Duty, EIOPA transparency). Causal-attribution model is bespoke. |
| Switching cost? | **Medium** | GenAI model swappable, but data integration creates meaningful lock-in. |
| **Verdict** | **NOVEL** | Regulatory context integration + causal-attribution engine don't exist off the shelf. |

### Commodity check: E — DORA Compliance Evidence Generator
| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Yes** | Deloitte DORA Accelerator, PwC DORA toolkit, Ayasdi, SymphonyAI RegTech — productised tools exist. |
| Standardized? | **Yes** | DORA is EU-wide; compliance requirements identical for all EU financial entities. |
| Switching cost? | **Medium** | GenAI model swappable, but data integration creates partial lock-in. |
| **Verdict** | **COMMODITY** | Core pattern (RAG + structured data → formatted report) productised by multiple vendors. |

### Final top 3 after commodity replacements

Replace **A** (commodity) and **E** (commodity) with next-highest non-commodity:

| Rank | ID | Survivor | Score | Commodity? | Action |
|---|---|---|---|---|---|
| 1 | H | Personalised Policy Communication Engine | 20 | Novel | **Keep** |
| 2 | B | Legacy Code Documentation & Migration Translator | 15 | Novel | **Promote** |
| 3 | D | Data Integrity Anomaly Detection During Cutover | 15 | Novel | **Promote** |

### Commodity check: B — Legacy Code Documentation
| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **No** | No commercial tool specifically addresses *insurance legacy code documentation with migration intent*. |
| Standardized? | **No** | Each legacy system (COBOL, 4GL, Java) has unique patterns; each migration target has different mapping. |
| Switching cost? | **Low** | Built as internal RAG tool on open-source LLM — zero vendor lock-in. |
| **Verdict** | **NOVEL** | Highly specific to Kepler's orphaned-app problem. |

### Commodity check: D — Data Integrity Anomaly Detection
| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **No** | Data reconciliation tools exist (Talend, Informatica); none purpose-built for *insurance policy data cross-validation during migration cutover*. |
| Standardized? | **No** | Schema mapping unique to each old/new system pair. RACQ-style risk is insurance-specific. |
| Switching cost? | **Low** | Built on open-source ML stack using internal data pipelines. |
| **Verdict** | **NOVEL** | Custom to Kepler's migration topology and regulatory context. |

### Final recommendation

| Rank | ID | Survivor | Score | Pain Point | Modality | Feasibility Binding Constraint |
|---|---|---|---|---|---|---|
| **1** | **H** | **Personalised Policy Communication Engine** | **20** | PP3 | GenAI | Rating engine instrumentation (>50% policies store final premium only → fallback) |
| **2** | **B** | **Legacy Code Documentation & Migration Translator** | **15** | PP1 | GenAI | Code accessibility (≥5 orphaned apps air-gapped → feasibility drops to 2) |
| **3** | **D** | **Data Integrity Anomaly Detection During Cutover** | **15** | PP2 | Classical ML | Dual-system read access (<60% real-time → incomplete coverage) |

All three are **novel** with defensible differentiation for Kepler's specific context. The top 3 spans all three pain points (PP3, PP1, PP2) and two AI modalities (GenAI + Classical ML).

### Knocked out

| Use Case | Reason |
|---|---|
| **A** Cloud Cost Anomaly Detection & Optimisation | Commodity — 10+ mature vendors; no defensible advantage |
| **E** DORA Compliance Evidence Generator | Commodity — productised RegTech tools exist for EU-wide regulation |
| **C** Migration Sequencing Optimiser | Lowest score (9) — bounded savings, one-time value, heuristics capture most benefit |
| **F** DORA Compliance Monitoring Agent | Score too low (12) — overlaps with E; higher complexity, lower maturity |
| **G** Real-Time Risk Scoring Engine | Score too low (10) — value 5 but feasibility 2; blocked by 18–24 month telematics data pipeline |
| **I** Competitive Pricing Response Agent | Score too low (10) — highest regulatory barrier; DORA + FCA fair value compliance per auto-adjusted price |

---

## v2 Changes

| v1 | v2 | Why |
|---|---|---|
| Feasibility scores without named constraints | **Every feasibility score has a named binding constraint** | Consulting-sme skill rule: "Name a no-AI baseline and the binding constraint for every feasibility score" |
| No-AI baselines implicit | **Explicit no-AI baseline per use case** | Enables defensible ROI comparison (build vs do-nothing vs buy) |
| Commodity/novel verdict in text | **Structured 3-question commodity check per top-5 candidate** | Transparent, reproducible screening criteria |
| Feasibility constraints in narrative only | **Feasibility binding constraint row per use case + summary matrix column** | Downstream knows exactly what would break each use case |

---

*Each use case links back to specific evidence in 01-context-brief.md (market research) or 02-primary-signal.md (customer verbatims and competitor teardown). Binding constraints are falsifiable conditions that would change the feasibility score. Research cutoff: June 2026.*
