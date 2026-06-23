# AI Use Cases Against Three Strategic Pain Points

**Case B** · Kepler Insurance · 2026-06-17

**Pain points drawn from:** `01-context-brief.md` (original research) and `02-primary-signal.md` (customer verbatims + competitor teardown + re-rating).

---

## Pain Point 1: Legacy Tech Cost Base Is Unsustainable in a Soft Market

**Confirmed & Sharpened** — the FCA verbatims prove customers have zero loyalty friction and switching is efficient. Every $1 of legacy overhead directly limits pricing flexibility in a market where 53% of customers are shopping.

### 1.1 Infrastructure Cost Anomaly Detection & Forecasting (Classical ML)

**What:** A supervised/unsupervised ML model on AWS + Azure billing streams that learns normal spend patterns per application (50 in scope), detects anomalies in real-time (orphaned resources, oversized instances, unused reserved capacity), and forecasts 30/60/90-day costs per migration wave.

**Why it addresses the pain point:** The dual AWS+on-prem footprint is the most controllable cost variable during migration. The RACQ precedent proves that system transitions create data-integrity blind spots. Cost anomalies during migration are invisible without automated monitoring — by the time a finance report catches a $50K/month orphaned instance, the spend has compounded.

**Feasibility check:**
- Data: abundant (CloudWatch, Azure Cost Management, AWS CUR)
- Model: gradient boosting or Prophet on time-series billing data
- Integration: push alerts to FinOps dashboard or migration ops channel
- Precedent: well-established in cloud FinOps (Vanderbill, CloudHealth)

**Fallback if blocked:** Threshold-based rules (cloud vendor budgets + alerts) if labelling historical spend data is impossible during migration chaos.

---

### 1.2 Legacy Code Documentation & Migration Translator (Generative AI)

**What:** A GenAI assistant (RAG on the codebase + architecture docs) that reads legacy COBOL, Java, and proprietary 4GL code, generates business-logic documentation, data-flow diagrams, and target-Azure service mapping. For each of the 11 orphaned applications (no current owner), it produces a "survival guide" summarising what the app does, what data it touches, what integrations it depends on, and a recommended migration pattern (rehost / refactor / replace).

**Why it addresses the pain point:** 11 orphaned apps represent an outsized share of migration risk — no SME to explain business logic or validate parity. GenAI can recover institutional knowledge from the code itself, reducing the risk of re-engineering errors or missed functionality during lift-and-shift. Directly reduces the time SMEs spend on documentation, freeing them for validation.

**Feasibility check:**
- Data: source code repos (if accessible), architecture diagrams, network topology
- Model: Claude / GPT-4 class for code analysis + summarisation
- Integration: internal wiki or migration knowledge base
- Precedent: GitHub Copilot for legacy code analysis, AWS App2Container docs
- **Risk:** Code may be on isolated/air-gapped mainframes; GenAI may hallucinate business rules; governance approval needed for code upload to LLM

**Fallback if blocked:** Semi-automated — run static analysis tools (sonarcloud, CAST) and feed output to LLM for summarisation only, without raw code exposure.

---

### 1.3 Autonomous Cloud Cost Optimisation Agent (Agentic)

**What:** A continuous agent that monitors the AWS + on-prem → Azure migration pipeline and autonomously:
- Identifies and terminates orphaned cloud resources (instances running post-cutover)
- Recommends reserved-instance / savings-plan purchases based on confirmed migration waves
- Detects on-prem servers that have been idle since workload migration and triggers decommission workflow
- Escalates to FinOps only when savings exceed a configurable threshold ($XK/month)

**Why it addresses the pain point:** The migration runs 18 months — a human FinOps team cannot monitor 50 applications' resource utilisation daily across three environments. An agent that runs continuously captures savings that would otherwise leak through the cracks of manual oversight. The agent's orchestration layer also produces an audit trail for DORA resilience testing (proving cost controls operate during transition).

**Feasibility check:**
- Tools: AWS Lambda + Azure Automation + vendor APIs (VMware, Hyper-V)
- Orchestration: simple state machine with approval gates for destroy actions
- Precedent: automated EC2 right-sizer agents; FinOps automation (ProsperOps)
- **Risk:** Destructive actions (instance termination) must have approval guardrails; migration schedule changes may cause false positives on "idle" resources

**Fallback if blocked:** Read-only agent that surfaces recommendations to a human approver via Slack/Jira (semi-autonomous).

---

### 1.4 Migration Sequencing Optimiser (Classical ML / Optimisation)

**What:** A combinatorial optimisation model (ML + operations research) that takes as input the 50 applications' dependency graph, data volumes, compliance tier (SOX, GDPR), owner status (11 orphaned flagged as high-risk), and cost-per-migration-wave, and outputs the optimal migration sequence — minimising total cost while respecting zero-downtime-on-claims constraint and regulatory audit trail continuity.

**Why it addresses the pain point:** Migration sequencing is traditionally done via spreadsheet ranked by "easiest first." This ignores the cost of keeping a dual-environment running an extra month for an orphaned app while low-risk apps wait. The model surfaces non-obvious savings — e.g., migrating claims apps early (despite their complexity) because cutting over claims means the revenue-generating platform can decommission its AWS footprint sooner.

**Feasibility check:**
- Data: dependency graph (from architecture docs), cost-per-app, risk scores
- Model: constraint programming (OR-Tools / OptaPlanner) or RL
- Precedent: cloud migration sequencing tools (Cloudamize, VMware AVI)
- **Risk:** dependency graph may be incomplete; hard constraints (regulatory freeze periods, seasonal claims spikes) shift over time

**Fallback if blocked:** Heuristic rules (any claims app = wave 1; any orphaned app with no known dependencies = wave 3; all others = wave 2) with manual override.

---

## Pain Point 2: Regulatory Risk Peaks During Migration Without DORA-Compliant Resilience Planning

**Confirmed** — the RACQ case (ASIC lawsuit over 570K misleading renewal notices) is a direct precedent for data-integrity failures during system transitions. 11 orphaned apps are material DORA compliance exposures.

### 2.1 Data Integrity Anomaly Detection During Cutover (Classical ML)

**What:** An ML model that monitors dual-running systems (old + new) during each application cutover and cross-validates policy data, premium calculations, renewal notice content, and claims records. It flags discrepancies — e.g., the new system calculates a renewal premium 3% higher than the old system for the same policy — before the notice is issued. Directly addresses the RACQ scenario (fabricated "last period premium" from a system transition error).

**Why it addresses the pain point:** The RACQ case proves that data integrity failures during system transitions materialise as regulatory liability. ASIC sued over 570K+ misleading renewal notices caused by a system miscalculating comparative pricing. Kepler has 50 applications transitioning over 18 months — the surface area for similar errors is 50×. ML-based cross-validation catches discrepancies that manual reconciliation (sampling N policies) will miss.

**Feasibility check:**
- Data: policy snapshots from old + new systems during parallel run
- Model: supervised (trained on past migration discrepancy patterns) or unsupervised (distributional shift detection between old/new outputs)
- Integration: gates the renewal notice generation pipeline — no notice issued if discrepancy > threshold
- Precedent: Amazon's "canary" deployment validation, financial reconciliation ML
- **Risk:** False positives could delay renewals; requires policy data mapping (field-by-field) across old and new schema

**Fallback if blocked:** Rule-based reconciliation (field-by-field comparison of a sample set, with automated expansion when discrepancies found).

---

### 2.2 DORA Compliance Evidence Generator (Generative AI)

**What:** A GenAI pipeline that ingests structured and unstructured data from the migration programme — incident logs, resilience test results, third-party vendor risk assessments (Azure, migration tooling vendors), change tickets, and architecture decisions — and produces DORA-mandated documentation: ICT Risk Assessment reports, resilience testing evidence packs, third-party risk register updates, and SOX-ready audit trail summaries. Uses a RAG store of DORA regulation text, EIOPA guidelines, and EBA technical standards (all EU financial entities) to ensure regulator-ready formatting and coverage.

**Why it addresses the pain point:** DORA (in force Jan 2025) mandates incident reporting within 24 hours (major incidents) and annual resilience testing. The 18-month migration is a continuous state of ICT change — every cutover window is reportable. Manually compiling compliance evidence across 50 applications, multiple cloud vendors, and a compressed timeline is not sustainable with a human compliance team. GenAI compresses a 40-hour-per-milestone documentation effort into minutes.

**Feasibility check:**
- Data: ServiceNow/Jira tickets, Azure Monitor logs, PagerDuty incidents, vendor SOC2 reports
- Model: Claude / GPT-4 class with RAG on regulatory corpus
- Integration: scheduled weekly run producing compliance pack; ad-hoc for incidents
- Precedent: existing RegTech GenAI tools (SymphonyAI, Ayasdi); FCA-approved AI compliance tools
- **Risk:** Hallucinated evidence or mis-attributed controls must be human-verified before regulator submission; GenAI cannot attest — human sign-off still required

**Fallback if blocked:** Structured compliance checklist generator (prompt-engineered output) with manual evidence upload — less automation but still a 3× productivity gain over manual drafting.

---

### 2.3 DORA Compliance Monitoring & Remediation Agent (Agentic)

**What:** A continuous agent that monitors the 50-application migration against DORA requirements and autonomously:
- Tracks incident-reporting timelines (major incidents → 24-hour notification; impacts cross-system → regulator notification)
- Validates resilience testing coverage per application (every app must be tested per DORA article 24 schedule)
- Detects orphaned-app compliance gaps (11 apps with no owner → automatic escalation to migration governance board)
- Assembles remediation tickets with regulator-ready evidence requirements when a gap is found
- Maintains a live DORA compliance scoreboard across all 50 applications, updated per migration wave

**Why it addresses the pain point:** 50 applications migrating over 18 months creates a moving compliance target — app N moves from pre-migration (old compliance posture) to post-migration (new compliance posture). A human compliance officer cannot track 50× this transition simultaneously, especially when 11 apps have no owner. The agent surfaces compliance drift in hours, not weeks, and automates the evidence-gathering prep that currently consumes compliance teams.

**Feasibility check:**
- Tools: Jira/ServiceNow API, Azure Policy, AWS Config, vendor compliance feeds
- Orchestration: periodic scan + event-driven trigger on Jira issue create/update
- Integration: compliance dashboard for CRO and migration steering committee
- Precedent: DORA-readiness automation tools; AI compliance agents (Deloitte DORA Accelerator)
- **Risk:** False negatives (agent misses a compliance gap due to incomplete data) could create false confidence; agent scope must be clearly bounded as "screening, not attesting"

**Fallback if blocked:** Rule-based compliance checklist with Jira automation (email reminders per app per DORA requirement) — lower sophistication but still beats manual tracking at 50-app scale.

---

## Pain Point 3: AI/Telematics Competitors Will Widen the Gap During the Pause

**Sharpened** — CMT's DriveWell Atlas foundation models (Oct 2025) and Allianz's $350M co-ownership stake create compounding, non-linear competitive advantage. FCA verbatims show customers feel zero loyalty friction — lower price = immediate switch.

### 3.1 Real-Time Risk Scoring Engine (Classical ML)

**What:** An ML model that, as telematics data becomes available during/after migration, ingests driving behaviour data, claims history, credit indicators, and external contextual signals (weather, road type, time-of-day accident rates) to produce a real-time risk score per policy at quote time — replacing the current batch-rated (weekly) pricing cycle. During the pre-telematics phase, the model uses proxy signals (demographic + location + vehicle characteristics) and improves accuracy as telematics data accumulates.

**Why it addresses the pain point:** Allianz + CMT already has real-time risk scoring across 55M+ drivers. Kepler's batch-rating cycle means a quote issued today uses risk data that is up to 7 days old. A 53%-shopping market selects for carriers whose prices reflect the most current risk reality — batch-rated carriers systematically misprice good risks (too high → they leave) and bad risks (too low → adverse selection). Real-time scoring compresses Kepler's pricing cycle from weekly to per-quote, directly narrowing the Allianz gap.

**Feasibility check:**
- Data: motor book claims history, external data (weather, traffic), telematics pipeline (post-migration)
- Model: GBM or neural network with online learning for real-time updates
- Integration: replaces existing rating engine call in the quote API
- Precedent: Progressive Snapshot, Allianz CMT, all major US auto carriers
- **Risk:** EIOPA AI Principles (2025–2026) require explainability for pricing models — black-box neural net risk scores may need SHAP/LIME wrapper for regulatory compliance. Model drift monitoring needed per market.

**Fallback if blocked:** Simplified GLM-based score with fewer features — less accurate than the ML model but explainable by default for regulators.

---

### 3.2 Personalised Policy Communication Engine (Generative AI)

**What:** A GenAI system that generates personalised renewal communications per customer — in their language, with their specific policy details, explaining premium changes in plain language with transparent causation ("Your premium increased 4%. This is driven by a 7% rise in repair costs in your region and your 3-year claims-free status placing you in our best-risk tier. Here's how you compare to similar drivers in your area.") Integrates with policy data and external indices (repair-cost inflation, weather loss trends) for accurate causal attribution.

**Why it addresses the pain point:** The customer verbatims in 02-primary-signal.md are devastating for retention: Alan Ford ("Why didn't they offer us that premium first-time round?"), Kate ("easier to leave it run" — inertia, not loyalty), John ("if everyone who is new is getting a cheaper option, I should get one too"). The common thread is opaque pricing. J.D. Power (2026) confirms that customers who understand their premium changes are +141 points more satisfied on price — even when rates rise. GenAI-generated personalisation turns opaque renewal notices into transparent retention moments, directly counteracting the 53% shopping rate.

**Feasibility check:**
- Data: policy data, claims history, customer interaction history, external index feeds
- Model: Claude / GPT-4 class with RAG on policy data + regulatory templates
- Integration: renewal notice generation pipeline (email/post/app)
- Precedent: J.D. Power research (understanding drives retention); Lemonade's AI-driven policy communication
- **Risk:** Must comply with FCA Consumer Duty (fair value evidence) and EIOPA transparency principles in each market. Over-personalisation (e.g., telling a bad driver they're a bad driver) could trigger complaints. EU Digital Services Act AI transparency.

**Fallback if blocked:** Templated renewal letters with dynamic variables for the causal explanation section — less personalised but still beats the current opaque notice.

---

### 3.3 Competitive Pricing Response Agent (Agentic)

**What:** An agentic system that continuously monitors the competitive landscape — aggregate pricing data, competitor rate filings (where publicly available), Allianz telematics product pricing signals, aggregator market quotes — and simulates Kepler's optimal pricing response in real-time. The agent:
- Detects when a competitor has changed pricing in a specific segment (e.g., "Allianz reduced telematics motor rates 5% in Bavaria")
- Simulates what Kepler's pricing response would do to retention, acquisition, and profitability at various response levels
- Auto-adjusts the rating engine parameters within a pre-approved risk-appetite band (±X% per segment)
- Escalates to actuarial team when the optimal response exceeds the pre-approved band

**Why it addresses the pain point:** The FCA verbatims prove switching is frictionless and loyalty is dead. In a 53%-shopping market, a competitor pricing change captures market share within days, not weeks. Kepler's current response cycle (competitor changes price → actuaries detect → model iteration → compliance review → implementation) takes 4–8 weeks. By then, the market has moved on. The agent compresses this to hours for in-band changes, and hours-to-notify for out-of-band changes. This is the operational counterweight to Allianz's $350M data moat — speed of response, not depth of data.

**Feasibility check:**
- Data: aggregator API feeds, competitor rate filings, Kepler's own risk models, portfolio profitability by segment
- Orchestration: periodic competitor scan → simulate response → auto-adjust within guardrails → log for compliance
- Integration: rating engine API, actuarial dashboard, compliance log
- Precedent: algorithmic trading in capital markets (auto-pricing in competitive markets); Amazon's repricing engine; airline revenue management
- **Risk:** DORA and EIOPA require algorithmic pricing governance — the agent's decision criteria must be auditable and explainable. FCA Consumer Duty requires fair value evidence for every price — auto-adjusting parameters must not produce unfair outcomes. Guardrails must be set by humans and reviewed quarterly.

**Fallback if blocked:** Semi-autonomous — agent surfaces recommended pricing responses to an actuarial team member via a daily digest with "approve all" / "approve selected" / "reject" workflow. Still compresses from 4–8 weeks to same-day.

---

## Summary Matrix

| Use Case | Pain Point | AI Modality | Key Evidence From Context | Key Evidence From Primary Signal | Risk |
|---|---|---|---|---|---|
| 1.1 Infra Cost Anomaly Detection | PP1 | Classical ML | 9% rate decline (Marsh Q1 2026) | Tower Hill 27% hike (BBB 2026) | Migration schedule false positives |
| 1.2 Legacy Code Documentation | PP1 | Generative AI | 11 orphaned applications | RACQ data integrity failure | Code air-gap, hallucinated rules |
| 1.3 Autonomous Cost Optimisation | PP1 | Agentic | Dual AWS+on-prem footprint | Peter verbatim (switching efficiency) | Destructive action guardrails |
| 1.4 Migration Sequencing Optimiser | PP1 | Classical ML / OR | $31M remaining budget | Kate verbatim (loyalty paid zero) | Incomplete dependency graph |
| 2.1 Data Integrity Anomaly Detection | PP2 | Classical ML | DORA in force Jan 2025 | RACQ 570K misleading notices | False positive delays renewals |
| 2.2 DORA Compliance Evidence Gen | PP2 | Generative AI | 18-month migration timeline | Tower Hill opacity complaint | Hallucinated evidence |
| 2.3 DORA Compliance Agent | PP2 | Agentic | 11 orphaned apps | DORA resilience testing mandate | False confidence from gaps |
| 3.1 Real-Time Risk Scoring | PP3 | Classical ML | Allianz $350M CMT partnership | DriveWell Atlas foundation models | EIOPA explainability requirements |
| 3.2 Personalised Policy Comms | PP3 | Generative AI | 53% shopping rate (J.D. Power) | Alan Ford verbatim (opacity) | EIOPA transparency compliance |
| 3.3 Competitive Pricing Response | PP3 | Agentic | Progressive vs GEICO divergence | FCA verbatims (zero loyalty friction) | DORA algorithmic pricing governance |

---

*Each use case links back to specific evidence in 01-context-brief.md (market research) or 02-primary-signal.md (customer verbatims and competitor teardown). All three AI modalities — classical ML, generative AI, and agentic — are covered per pain point where operationally plausible. Risk and fallback paths are documented per use case. Research cutoff: June 2026.*

---

## Dedup Analysis

### Near-duplicates: Consolidate

| Pair | Rationale | Action |
|---|---|---|
| **1.1** (Infra Cost Anomaly Detection) + **1.3** (Autonomous Cost Optimisation Agent) | Detection is a prerequisite for action; without 1.1, the agent in 1.3 has no trigger. Without 1.3, 1.1 surfaces findings with no remediation path. They are the same operational loop (monitor → detect → act) at different automation levels. | **CONSOLIDATE** into a single entry: **Cloud Cost Anomaly Detection & Autonomous Optimisation** covering both sensing and remediation. |

### Partial overlaps: Flag for user — do not auto-merge

| Pair | Nature of overlap | Why not merge |
|---|---|---|
| **2.2** (DORA Compliance Evidence Generator) ↔ **2.3** (DORA Compliance Monitoring & Remediation Agent) | Both draw on the same DORA compliance data pipeline (incident logs, resilience test results, vendor assessments). | 2.2 produces *documentation for regulators* (reports, evidence packs). 2.3 produces *operational alerts for the migration team* (gaps, remediation tickets). Different output, different consumer, different cadence. Merging would force a single tool to serve two incompatible workflows (scheduled reporting vs. event-driven escalation). |
| **3.1** (Real-Time Risk Scoring Engine) ↔ **3.3** (Competitive Pricing Response Agent) | The risk score from 3.1 is a key input to the pricing agent in 3.3. | They are architecturally distinct: 3.1 is a model that produces a number (risk score). 3.3 is an agent that consumes multiple inputs (risk score + competitor data + portfolio profitability) to decide a price. 3.1 has independent value as a rating engine improvement. 3.3 has independent value even if the risk score is sub-optimal (speed of response can compensate for accuracy in the short term). |

### No overlap — orthogonal

- **1.4** (Migration Sequencing Optimiser) — orthogonal to 1.1/1.3; sequencing addresses *when* to move apps, cost optimisation addresses *how much* to spend while they move.
- **2.1** (Data Integrity Anomaly Detection During Cutover) — orthogonal to 2.2/2.3; cutover data integrity addresses *one specific moment* in migration, not ongoing compliance monitoring.
- **3.2** (Personalised Policy Communication Engine) — orthogonal to 3.1/3.3; retention communication is a separate capability from risk scoring or pricing response.

### Survivors after dedup (9 entries)

| ID | Survivor | Origin Consolidation |
|---|---|---|
| **A** | **Cloud Cost Anomaly Detection & Autonomous Optimisation** | 1.1 + 1.3 |
| **B** | Legacy Code Documentation & Migration Translator | 1.2 (unchanged) |
| **C** | Migration Sequencing Optimiser | 1.4 (unchanged) |
| **D** | Data Integrity Anomaly Detection During Cutover | 2.1 (unchanged) |
| **E** | DORA Compliance Evidence Generator | 2.2 (unchanged; **partial overlap** with F — see table above) |
| **F** | DORA Compliance Monitoring & Remediation Agent | 2.3 (unchanged; **partial overlap** with E — see table above) |
| **G** | Real-Time Risk Scoring Engine | 3.1 (unchanged; **partial overlap** with I — see table above) |
| **H** | Personalised Policy Communication Engine | 3.2 (unchanged) |
| **I** | Competitive Pricing Response Agent | 3.3 (unchanged; **partial overlap** with G — see table above) |

---

## Scoring: Value (1–5) × Feasibility (1–5)

### A: Cloud Cost Anomaly Detection & Autonomous Optimisation
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Real savings (15–30% cloud spend reduction typical). Finite window — benefits decline post-migration when dual footprint is decommissioned. |
| **Feasibility** | 5 | Cloud billing data is clean, abundant, and standardized (AWS CUR, Azure exports). ML anomaly detection on time-series is a solved problem. Mature SaaS vendor ecosystem (CloudHealth, ProsperOps). |
| **Score** | **20** | |

### B: Legacy Code Documentation & Migration Translator
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | 11 orphaned apps are existential migration risk. Without business-logic documentation, those apps cannot be migrated reliably — one re-engineering error could cost more than the entire documentation programme. |
| **Feasibility** | 3 | Code air-gap on mainframes is a real barrier. LLM hallucination risk for undocumented business rules. Governance approval needed for code upload to LLM. Requires careful human-in-the-loop validation. |
| **Score** | **15** | |

### C: Migration Sequencing Optimiser
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 3 | One-time optimization; a rule-based heuristic (claims-first, orphaned-last) captures most of the same savings. Estimated 5–15% improvement over heuristics at best, bounded by the $31M budget. |
| **Feasibility** | 3 | Dependency graph is likely incomplete or out of date. Hard constraints (regulatory freeze periods, seasonal claims spikes) shift unpredictably. Model needs frequent manual override. |
| **Score** | **9** | |

### D: Data Integrity Anomaly Detection During Cutover
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | RACQ precedent (ASIC lawsuit, 570K notices) proves regulatory liability from migration data errors is real and expensive. This use case directly prevents that outcome across 50 application cutovers. |
| **Feasibility** | 3 | Cross-schema field mapping is labor-intensive per application. False positives could delay renewals (operational risk). Needs dual-system read access during parallel run windows. |
| **Score** | **15** | |

### E: DORA Compliance Evidence Generator
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Automates a mandatory recurring process (estimated 40 hours per compliance milestone). Direct regulatory requirement with no optionality. Reduces manual effort from weeks to hours. |
| **Feasibility** | 4 | RAG on regulatory corpus is well-understood tech. Data sources (Jira, Azure Monitor, PagerDuty) are structured and API-accessible. Output is for human review — 95% accuracy acceptable, hallucination risk is containable. |
| **Score** | **16** | |

### F: DORA Compliance Monitoring & Remediation Agent
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | Continuous monitoring across 50 apps provides compliance oversight a human team cannot maintain at scale. But overlaps with E — they share data sources and domain. |
| **Feasibility** | 3 | Orchestration across Jira, Azure Policy, AWS Config, and vendor compliance APIs creates integration complexity. False negatives (missed compliance gaps) are dangerous because they create false confidence. Lower maturity precedent than E. |
| **Score** | **12** | |

### G: Real-Time Risk Scoring Engine
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | Core competitive response to Allianz CMT. Without real-time scoring, Kepler systematically misprices good risks (too high → they churn at 53% shopping rate) and bad risks (too low → adverse selection). Strategic must-have. |
| **Feasibility** | 2 | Chicken-and-egg problem: scoring accuracy improves with telematics data, but telematics adoption requires the scoring capability to exist. Legacy batch-rated PAS cannot easily ingest real-time scores. EIOPA explainability requirements add a regulatory gate. |
| **Score** | **10** | |

### H: Personalised Policy Communication Engine
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 4 | J.D. Power data (+141 points price satisfaction when customers understand premium changes) is compelling. Low investment, measurable retention impact. But primarily *retains* existing customers — doesn't improve acquisition or pricing competitiveness. |
| **Feasibility** | 5 | Simplest tech stack (GenAI + RAG on policy data + external index calls). Single API hook into the renewal notice pipeline. Regulatory alignment (FCA Consumer Duty transparency requirement) is an advantage, not a barrier. |
| **Score** | **20** | |

### I: Competitive Pricing Response Agent
| Dimension | Score | Rationale |
|---|---|---|
| **Value** | 5 | Compresses pricing response from 4–8 weeks to hours. Directly counters Allianz's speed advantage. In a 53%-shopping market, a 24-hour response to competitor moves captures share before the competitor's marketing cycle completes. |
| **Feasibility** | 2 | Requires aggregator API data (availability varies by European market). Needs rating engine API access (legacy PAS may not support real-time writes). Faces DORA algorithmic pricing governance + FCA fair value compliance for every auto-adjusted price. Highest regulatory barrier of all 9 survivors. |
| **Score** | **10** | |

### Scoreboard

| Rank | ID | Survivor | Value | Feasibility | **Score** |
|---|---|---|---|---|---|
| 1 | A | Cloud Cost Anomaly Detection & Optimisation | 4 | 5 | **20** |
| 1 | H | Personalised Policy Communication Engine | 4 | 5 | **20** |
| 3 | E | DORA Compliance Evidence Generator | 4 | 4 | **16** |
| 4 | B | Legacy Code Documentation & Migration Translator | 5 | 3 | **15** |
| 4 | D | Data Integrity Anomaly Detection During Cutover | 5 | 3 | **15** |
| 6 | F | DORA Compliance Monitoring & Remediation Agent | 4 | 3 | **12** |
| 7 | G | Real-Time Risk Scoring Engine | 5 | 2 | **10** |
| 7 | I | Competitive Pricing Response Agent | 5 | 2 | **10** |
| 9 | C | Migration Sequencing Optimiser | 3 | 3 | **9** |

---

## Top 3 Selection & Commodity Check

Preliminary top 3 by score: **A (20)** · **H (20)** · **E (16)**

### Commodity check: A — Cloud Cost Anomaly Detection & Optimisation

| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Yes** | CloudHealth, ProsperOps, Vantage, Azure Cost Management, AWS Cost Explorer, CloudCheckr — mature, competitive market with 10+ established tools. |
| Standardized? | **Yes** | Cloud billing data schemas (AWS CUR, Azure exports) are standardized per provider. The ML pattern (forecast × anomaly-detect × alert/remediate) is identical across vendors. |
| Low switching cost? | **Yes** | SaaS tools with API access; switching between vendors takes weeks, not months. No proprietary data lock-in. |
| **Verdict** | **COMMODITY** | Carrying a cloud cost optimisation tool as a competitive AI capability would be like calling a spreadsheet a data platform. Replace with next-best non-commodity. |

### Commodity check: H — Personalised Policy Communication Engine

| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Partial** | Generic personalised-content engines exist (CRM content automation, marketing personalisation), but none specifically solve *insurance renewal causation with regulatory compliance*. Lemonade's AI comms is closest (US focus, not EU-regulated). |
| Standardized? | **No** | Each market has different regulatory requirements (FCA Consumer Duty, EIOPA transparency). The causal-attribution model (tying premium change to external indices + policy-specific claims history + risk score movement) is bespoke. |
| Low switching cost? | **Medium** | The GenAI model is swappable (Claude ↔ GPT ↔ open-source), but the data integration (policy DB, index feeds, regulatory template corpus) creates meaningful lock-in. |
| **Verdict** | **NOT COMMODITY** | The regulatory context integration and causal-attribution engine do not exist off the shelf. Build once, deploy across all markets. Keep. |

### Commodity check: E — DORA Compliance Evidence Generator

| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **Yes** | Deloitte DORA Accelerator, PwC DORA toolkit, Ayasdi, SymphonyAI RegTech — dedicated compliance documentation tools already target this exact regulation. |
| Standardized? | **Yes** | DORA is an EU-wide regulation; compliance requirements are identical for all EU financial entities. A generic DORA evidence generator can serve any firm. |
| Low switching cost? | **Medium** | The GenAI model is swappable, but data integration (Jira, Azure Monitor, PagerDuty with Kepler-specific field mappings) creates partial lock-in. |
| **Verdict** | **COMMODITY** | The core pattern (RAG on regulation text + structured incident data → formatted compliance report) is a standard GenAI implementation already productised by multiple vendors. The marginal differentiation from Kepler-specific data integration is not defensible. Replace with next-best non-commodity. |

### Final top 3 after commodity replacements

Replacing **A** (commodity) and **E** (commodity) with the next-highest non-commodity survivors:

| Rank | ID | Survivor | Score | Commodity? | Action |
|---|---|---|---|---|---|
| 1 | H | Personalised Policy Communication Engine | 20 | No | **Keep** |
| 2 | B | Legacy Code Documentation & Migration Translator | 15 | No | **Promote** (replaces A) |
| 3 | D | Data Integrity Anomaly Detection During Cutover | 15 | No | **Promote** (replaces E) |

### B: Commodity check cross-reference

| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **No** | No commercial tool specifically addresses *insurance legacy code documentation with migration intent*. GitHub Copilot documents code; it doesn't produce migration-target-specific business logic summaries. |
| Standardized? | **No** | Each legacy system (COBOL, 4GL, Java) has unique patterns, and each migration target (Azure, refactor target) has different mapping requirements. |
| Low switching cost? | **Low** | If built as an internal RAG tool using an open-source model (Llama, Mistral), there is no vendor lock-in at all. |
| **Verdict** | **NOT COMMODITY** | Highly specific to Kepler's orphaned-app problem. No off-the-shelf equivalent. |

### D: Commodity check cross-reference

| Question | Answer | Detail |
|---|---|---|
| Multiple vendors? | **No** | General-purpose data reconciliation tools exist (Talend, Informatica), but none are purpose-built for *insurance policy data cross-validation during migration cutover with regulatory audit trail*. |
| Standardized? | **No** | Schema mapping is unique to each old-system/new-system pair. The specific risk profile (RACQ-style renewal pricing errors) is insurance-specific. |
| Low switching cost? | **Low** | Built on open-source ML stack (scikit-learn, Prophet) using internal data pipelines. No proprietary lock-in. |
| **Verdict** | **NOT COMMODITY** | Custom to Kepler's migration topology and regulatory context. No off-the-shelf alternative. |

### Final recommendation

| Rank | ID | Survivor | Score | Pain Point | Modality |
|---|---|---|---|---|---|
| **1** | **H** | **Personalised Policy Communication Engine** | **20** | PP3 | GenAI |
| **2** | **B** | **Legacy Code Documentation & Migration Translator** | **15** | PP1 | GenAI |
| **3** | **D** | **Data Integrity Anomaly Detection During Cutover** | **15** | PP2 | Classical ML |

All three are **non-commodity** with defensible differentiation for Kepler's specific context. The top-3 spans all three pain points (PP3, PP1, PP2) and two AI modalities (GenAI + Classical ML). Agentic use cases (F: DORA Agent, I: Pricing Agent) scored highest on value but lowest on feasibility — they are the natural next wave once the top-3 automation layer is in place.

### What was knocked out and why

| Use Case | Reason eliminated |
|---|---|
| **A** Cloud Cost Anomaly Detection & Optimisation | **Commodity** — 10+ mature vendors; no defensible advantage |
| **E** DORA Compliance Evidence Generator | **Commodity** — EU-wide regulation, multiple RegTech tools already serve this |
| **C** Migration Sequencing Optimiser | **Lowest score** (9) — bounded savings, one-time value, heuristics capture most benefit |
| **F** DORA Compliance Monitoring Agent | **Score too low** (12) — partially overlaps with E; higher complexity, lower maturity |
| **G** Real-Time Risk Scoring Engine | **Score too low** (10) — highest-value intent but blocked by telematics data gap + legacy PAS + EIOPA regulation |
| **I** Competitive Pricing Response Agent | **Score too low** (10) — highest regulatory barrier; requires DORA pricing governance + FCA fair value compliance per auto-adjusted price |
