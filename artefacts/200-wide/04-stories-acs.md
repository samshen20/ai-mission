# Stories & Acceptance Criteria — Personalised Policy Communication Engine

**product:** Kepler Insurance
**feature:** Personalised Policy Communication Engine
**date:** 2026-06-18

---

## Stories (10)

### S1 — Premium explanation (policyholder → understand → trust)
> **As a** policyholder, **I want** my renewal notice to explain exactly why my premium changed (broken down by causal factor), **so that** I can decide whether the price is fair without calling customer service.

### S2 — Batch personalisation at scale (comms manager → scale → ship)
> **As a** renewal communications manager, **I want** the system to generate a personalised causal explanation for every policy in the batch, **so that** I can send 500K notices without manually editing each one.

### S3 — Fair-value evidence trail (compliance → audit → defend)
> **As a** FCA compliance officer, **I want** every renewal notice to be logged with its full pricing attribution trail, **so that** I can produce fair-value evidence for any policy within 24 hours of a regulator request.

### S4 — Compliance rule engine pre-flight (compliance → prevent → avoid)
> **As a** compliance officer, **I want** each generated notice to be checked against market-specific regulatory rules (FCA, BaFin, ACPR, IVASS, DGSFP) before dispatch, **so that** no notice violates local pricing communication requirements.

### S5 — Conversational "why?" follow-up (policyholder → clarify → understand)
> **As a** policyholder, **I want** to ask "why?" after reading my renewal notice and get a specific, conversational answer about my premium, **so that** I can understand nuance the letter didn't cover.

### S6 — Agent-side causation view (CS agent → answer → retain)
> **As a** customer service agent, **I want** to see the same causal breakdown that was sent to the customer on my screen when they call, **so that** I can answer "why did my premium go up?" without reading a generic script.

### S7 — A/B test cohort isolation (comms manager → measure → decide)
> **As a** renewal communications manager, **I want** to run a controlled A/B test comparing personalised notices vs current templated notices across matched cohorts, **so that** I can measure the churn impact before committing to full rollout.

### S8 — Phase 0 data readiness audit (actuary → discover → prioritise)
> **As a** pricing actuary, **I want** the Phase 0 audit to report which rating variables are exposed per market and which are opaque, **so that** I can prioritise the downstream ETL work to instrument the legacy PAS.

### S9 — Sentiment-driven retention escalation (CS agent → rescue → retain)
> **As a** customer service agent, **I want** the system to flag an inbound renewal enquiry when the customer's sentiment indicates likely switching, **so that** I can intervene with a targeted retention offer before they leave.

### S10 — Multi-language notice generation (comms manager → localise → deploy)
> **As a** renewal communications manager, **I want** the system to generate notices in EN, DE, FR, IT, and ES from a single pipeline, **so that** I can deploy across all 5 target markets without separate production pipelines.

---

## Top 4 Stories — Gherkin Acceptance Criteria

### S1 — Premium explanation

```gherkin
Scenario: Policyholder receives personalised causation breakdown with their renewal notice
  Given the policy is in a book where Phase 0 achieved ≥70% attribution coverage
    And the rating engine exposed ≥1 component-level input variable for this policy
    And the external index feeds (repair-cost, weather, regulatory levies) are available for the policy's region
  When the renewal notice is generated for this policy
  Then the notice MUST include a plain-language explanation of what changed
    And the explanation MUST decompose the total premium delta into ≥1 attributable causal factor
    AND the explanation MUST cite a specific external index or internal rating input as the cause
    AND the policyholder-facing text MUST pass the market-specific compliance rule engine (FCA Consumer Duty plain-language check)
    AND the response MUST be generated within 2 seconds P95 across the batch

  # Error path — decomposition fallback
  Scenario: Rating engine does not expose component-level variables for this policy
    Given the policy is in a book where Phase 0 achieved <50% attribution coverage
      And the rating engine stores only the final premium for this policy
    When the renewal notice is generated
    Then the notice MUST use the aggregated market-level fallback template
      And the fallback explanation MUST state "Your premium reflects a [X]% change in [market-level factor] across [region]" — not a personalised causal attribution
      AND the notice MUST be tagged in the audit log as "fallback — partial attribution"
      AND the compliance officer MUST be notified if >30% of a market's notices use fallback in any batch

  # NFR — accuracy guard against hallucination
  Scenario: Generated explanation contains a numerical claim that cannot be traced to source data
    Given the LLM has generated the explanation text
    When the compliance rule engine scans the output for numerical claims
    Then any numerical claim in the explanation MUST be cross-referenced against source data (external index value, rating engine input, policy field)
      AND if a numerical claim cannot be traced to a source, the notice MUST be quarantined for human review
      AND the LLM call must be logged for drift monitoring
      AND the compliance team must receive a daily summary of all quarantined notices, including the specific untraceable claim and the policy ID
```

### S2 — Batch personalisation at scale

```gherkin
Scenario: Batch of 500K notices generated within the print window
  Given the batch contains 500,000 policies across 5 markets (UK, DE, FR, IT, ES)
    And Phase 0 attribution coverage is ≥70% for ≥3 of 5 markets
    And the compliance rule engine is loaded with all 5 market rule sets
  When the batch generation is triggered at Friday 18:00 (latest allowable start for Monday dispatch)
  Then 100% of notices MUST be generated and passed through the compliance rule engine within 6 hours (by Saturday 00:00)
    AND ≥99.5% of notices MUST pass the compliance rule engine without human intervention
    AND any notice that fails the compliance check MUST be quarantined with the specific rule violation logged
    AND the generation cost MUST NOT exceed EUR 0.02 per notice (LLM inference + compliance check)
    AND the batch MUST be retried automatically up to 3 times on transient LLM API failures, with exponential backoff (1s, 4s, 16s)

  # Error path — partial batch failure
  Scenario: LLM API returns errors for a subset of policies mid-batch
    Given the batch generation is in progress
      And the LLM API returns 503 errors for policy IDs 320,001 through 320,050 (consecutive failure)
    When the error rate in a 5-minute window exceeds 2%
    Then the system MUST pause new generation requests
      AND the system MUST retry failed policies up to 3 times with exponential backoff (1s, 4s, 16s)
      AND if retries fail for >0.1% of the batch, the system MUST alert the on-call engineer and flag the remainder for manual prioritisation
      AND any market with >5% of its notices in the failed set MUST be treated as a DORA-reportable incident (24-hour notification clock starts)

  # NFR — cost ceiling
  Scenario: Monthly LLM inference cost projection exceeds budget
    Given the batch generation runs weekly (52 cycles/year)
      And the target cost is EUR 0.02 per notice
    When the projected monthly cost exceeds EUR 40,000 at current volume
    Then an alert MUST be sent to the FinOps team
      AND the system MUST provide a cost-per-market breakdown to identify the most expensive market
      AND the compliance team MUST review whether any market's rule engine adds excessive re-generation overhead
```

### S3 — Fair-value evidence trail

```gherkin
Scenario: Regulator requests fair-value evidence for a specific renewal
  Given a regulator (FCA, BaFin, ACPR, IVASS, or DGSFP) has requested evidence for policy ID KPL-2026-48321
    And this policy renewed in the period after the system was deployed
    And the renewal notice was generated with ≥70% attribution coverage
  When the compliance officer queries the evidence trail for this policy
  Then the system MUST return the complete evidence pack within 5 seconds
    AND the evidence pack MUST contain: (a) the final generated notice text, (b) the attribution breakdown (which causal factors drove what share of the premium delta), (c) the source values for each attributed factor from the rating engine at time of generation, (d) the compliance rule engine check results (passed rules, any warnings), (e) a timestamped audit log of every system interaction during generation
    AND the evidence pack MUST be exportable as a PDF with DORA-compliant metadata headers (generation timestamp, system version, signing key hash)

  # Error path — evidence for a pre-deployment renewal
  Scenario: Evidence requested for a policy that renewed before system deployment
    Given the regulator requests evidence for a policy that renewed in the 2025-2026 cycle (pre-deployment)
    When the compliance officer queries the evidence trail
    Then the system MUST return a clear indication that the policy was processed before system deployment
      AND the system MUST link to the legacy manual evidence procedure (the 0.1% sampling protocol + rate filing proxy) that was in effect at that time
      AND the response MUST complete within 10 seconds

  # NFR — retention period
  Scenario: Evidence requested for a renewal that occurred 7 years ago
    Given the regulator requests evidence for a policy that renewed in 2020
      And the system retention policy is set to 6 years (matching FCA record-keeping requirements)
    When the compliance officer queries the evidence trail
    Then the system MUST return a clear indication that the evidence retention period has expired
      AND the system MUST log the query in an access audit trail
      AND the compliance officer MUST be offered a link to the offline archive procedure if applicable
```

### S6 — Agent-side causation view

```gherkin
Scenario: Customer service agent sees causation breakdown during an inbound call
  Given a policyholder calls customer service asking about their renewal premium
    And their policy has a personalised causation notice generated in the current renewal cycle
  When the agent looks up the policy in the CRM
  Then the agent's screen MUST display the same causal breakdown that was sent in the renewal notice within 1 second of policy lookup
    AND the display MUST show: (a) total premium delta, (b) broken bar chart of causal factors (external indices vs internal rating factors vs policy-specific), (c) the market-level benchmark comparison if available, (d) the exact text that was sent to the customer
    AND the agent MUST be able to click any causal factor to drill into the source data used for that attribution

  # Error path — no AI-generated notice exists for this policy
  Scenario: Customer calls about a policy that used the fallback template
    Given the policyholder's renewal used the aggregated market-level fallback (not personalised causation)
    When the agent looks up the policy
    Then the display MUST show the fallback explanation text
      AND the system MUST display a warning banner: "Limited attribution — personalised causation not available for this policy"
      AND the agent MUST see a list of known reasons for the fallback (e.g., "rating engine variables not exposed — Phase 0 gap in this market")
      AND the agent MUST receive a suggested script for escalating to the pricing team if the customer presses for details

  # NFR — lookup latency during peak
  Scenario: Call centre at peak volume (Monday morning, renewal season)
    Given the call centre is handling 2,000 concurrent calls
      And 1,200 of those calls involve renewal enquiries requiring causation view
    When each agent looks up a policy simultaneously
    Then 95% of causation view responses MUST render within 2 seconds
      AND 99% MUST render within 5 seconds
      AND the system MUST not degrade CRM search performance for non-renewal enquiries (claims, policy changes)
```

---

## AI Eval Card — S5: Conversational "Why?" Follow-up

**Story:** As a policyholder, I want to ask "why?" after reading my renewal notice and get a specific, conversational answer about my premium, so that I can understand nuance the letter didn't cover.

**Why an Eval Card instead of Gherkin:** The system's response is probabilistic — the same input can produce different-quality outputs. Given/When/Then assumes deterministic outcomes. An eval card defines the operating envelope within which the AI is trusted to respond autonomously.

### Confidence thresholds

| Response type | Minimum confidence | Measured by | Action if below threshold |
|---|---|---|---|
| Direct causation question ("why did my premium go up?") | ≥0.85 | Semantic similarity to the verified attribution data from Phase 0 + LLM self-reported confidence | Route to human agent with causation view (S6) display |
| Policy detail question ("am I covered for X?") | ≥0.70 | RAG retrieval relevance score against policy document corpus | Respond with "I can see your policy covers [matched items], but for specific coverage questions let me connect you to a specialist" |
| General insurance question ("why is insurance more expensive in my area?") | ≥0.60 | RAG retrieval relevance score + LLM confidence | Respond with curated market-level answer from pre-approved content library; never generate novel analysis |

### Refusal triggers (must not answer — route to human immediately)

- Query contains PII beyond the authenticated customer's policy data (third-party name, address, health data)
- Query asks for regulatory advice ("is this compliant with FCA rules?")
- Query disputes coverage specifics ("you should have paid my claim")
- Query contains aggressive, abusive, or suicidal sentiment (sentiment score <0.2 on pre-trained classifier)
- Query is in a language not supported by the deployment (only EN, DE, FR, IT, ES served)
- Customer has been escalated to retention team in this session (avoid conflicting messages)

### Latency ceiling

| Percentile | Target | Enforcement |
|---|---|---|
| P50 | <1.5 seconds | Monitor; alert if trend exceeds 2s for 3 consecutive days |
| P95 | <3.0 seconds | Hard timeout at 4.0 seconds — system returns "Let me look that up for you — one moment please" and queues the query for async response via email |
| P99 | <5.0 seconds | Escalate to engineering; DORA-reportable if sustained >10 minutes |

### Fallback paths (ordered — try #1 first)

| # | Fallback | Trigger | Customer experience |
|---|---|---|---|
| 1 | Async response via email | P95 latency >3s OR LLM returns empty response 3x in a row | "I'm gathering the details — you'll receive a personalised answer by email within 2 hours" — system generates answer async, emails customer |
| 2 | Route to human agent | Confidence below threshold for 2 consecutive turns OR refusal trigger activated | "Let me connect you with someone who can help with that specifically" — transfer to CS agent with causation view (S6) displayed on their screen |
| 3 | Escalation to retention team | Sentiment score <0.2 OR customer explicitly mentions switching | Immediate transfer to retention-trained agent, bypassing queue |
| 4 | Hard fail — degraded service | LLM API unavailable for >5 minutes | Switch to static FAQ mode: "I'm sorry, our personalised assistant is temporarily unavailable. Here are answers to common renewal questions." Serve from pre-approved content library. Alert on-call. DORA-reportable if downtime exceeds 30 minutes. |

### Evaluation criteria (used in CI/CD gate before deployment)

| Criterion | Pass | Fail |
|---|---|---|
| E2E test: causation question returns correct factor attribution | ≥90% of 200 test queries | <90% |
| Refusal trigger precision (correctly identifies PII queries) | ≥95% of 50 test queries | <95% |
| Refusal trigger recall (does not refuse benign causation questions) | ≤2% false refusal rate | >2% |
| Latency P95 under load (50 concurrent simulated users) | <3.0 seconds | ≥3.0 seconds |
| Fallback path invoked gracefully (no raw error shown to user) | 100% of 50 simulated failure scenarios | <100% |

---

## Adversarial Review — Edge Cases, Error Paths & NFRs

*Simulated adversarial session. Each story was attacked for missing edge cases, unhandled error paths, and implicit NFRs.*

### S1 — Premium explanation

| Attack | Missing in original | Action taken |
|---|---|---|
| What if attribution is 0%? (policy with no exposed variables, no external index match) | Not handled — assumed Phase 0 always succeeds | Added fallback scenario: aggregated market-level template with audit tag |
| What if the premium *decreased*? The explanation framing is different from an increase | Not specified — assumed only increases need explanation | Decrease still needs explanation (positive attribution) — S1 framing covers both directions |
| What if all causal factors sum to less than the total delta? (residual gap) | Residual gap not addressed — implied 100% attribution | Fallback scenario tags notice as "partial attribution"; compliance team notified if >30% fallback per batch |
| Latency at batch scale — 2 seconds per policy × 500K = 278 hours sequentially | Not addressed | Added NFR: 2 seconds P95 across batch, not per policy — implies parallel processing architecture |
| Hallucinated numerical claims — LLM invents a statistic | Not guarded | Added accuracy guard scenario: numerical claims traced to source data; non-traceable claims quarantined |

### S2 — Batch personalisation at scale

| Attack | Missing in original | Action taken |
|---|---|---|
| What if the LLM API is down for 30 minutes during the batch window? | No fallback for mid-batch API failure | Added partial batch failure scenario with retry logic + DORA escalation |
| What if market rules conflict? (cross-border policy — lives in FR, works in DE — which regulator applies?) | Not addressed — assumed clean market boundaries | Added rule conflict as open risk: S2 assumes 1 policy = 1 market; cross-border cases escalated to compliance team |
| Cost explosion — 500K × EUR 0.02 = EUR 10K per batch × 52 = EUR 520K/year | Cost not mentioned | Added cost ceiling NFR: EUR 0.02/notice and EUR 40K/month alert |
| What if the compliance rule engine itself is slow? (100ms per check × 500K = 14 hours) | Not addressed — assumed instantaneous | Compliance check latency folded into 6-hour batch window implicitly; added as explicit NFR in batch scenario |

### S3 — Fair-value evidence trail

| Attack | Missing in original | Action taken |
|---|---|---|
| What if the evidence is requested for a renewal *before* system deployment? | Not handled — assumed all renewals in scope | Added pre-deployment scenario with link to legacy procedure |
| What if the evidence trail is corrupted by a system migration event? | Not addressed | Added audit log integrity check as implicit requirement — full coverage would need a separate scenario; flagged in known unknowns |
| 24-hour DORA reporting clock — what if the evidence can't be assembled in time? | Not addressed | DORA reporting is a separate system concern; S3 assumes evidence assembly within 5 seconds once data is available. Reporting pipeline is out of scope for this AC but flagged in deployment checklist |
| What if the regulator requests evidence in a format the system doesn't support? | Not addressed | Added PDF export with DORA-compliant headers as minimum deliverable; custom format requests handled by compliance team |
| Evidence retention — 6 years for FCA, what about other regulators? | Not addressed | Added retention expiry scenario; 6-year policy is conservative (covers FCA, exceeds BaFin 5-year requirement) |

### S5 — Conversational "why?" (AI Eval Card)

| Attack | Missing in original | Action taken |
|---|---|---|
| What if the customer asks in a language not supported? | Not handled | Added language refusal trigger — route to human with translation request |
| What if the customer asks the same question 5 times? | Not addressed — assumes single-turn | No limit added intentionally — repeating customer may be confused, not adversarial. If repetition indicates frustration, sentiment classifier will trigger retention escalation |
| What if the causal decomposition data is stale? (Phase 0 data from 8 months ago, rating engine changed since) | Not addressed | Added as implicit requirement: Phase 0 attribution mapping must be re-validated per renewal cycle. Full scenario would need "data freshness" as a monitored metric |
| P95 latency under load — 50 concurrent users is low for a 500K-policy book | Underestimated | Load test threshold increased to 200 concurrent users in deployment checklist (outside Eval Card scope but flagged) |

### S6 — Agent-side causation view

| Attack | Missing in original | Action taken |
|---|---|---|
| What if the CRM doesn't have a field for causation data? | Not addressed — assumes CRM integration exists | Added integration as deployment dependency; S6 assumes the causation view is embedded in the CRM via an iframe or API widget |
| Monday morning peak — 2,000 concurrent calls is conservative for renewal season | Underestimated | 2,000 is used as a minimum; deployment load test target set to 5,000 concurrent |
| What if the causation view shows data the agent shouldn't share? (e.g., internal cost allocation) | Not addressed | Added as a design requirement: the agent view must clearly demarcate customer-facing vs internal-only data. Not captured in AC but flagged for UX audit |

### S7 — A/B test cohort isolation

*(Not in top 4 Gherkin stories, but attacked as part of full review)*

| Attack | Action |
|---|---|
| What if the control group notices they received a different letter? (social media backlash) | Flagged for comms team — A/B tests should be invisible to customers. No action in ACs |
| What if the A/B test runs during a rate change? (price effect confounds comms effect) | Added as design constraint: A/B test must control for rate-change magnitude across cohorts |
| What if the test market has regulatory restrictions on A/B testing of renewal communications? | Added as Phase 0 pre-check: verify regulatory acceptance of A/B test design per market before launch |

### S10 — Multi-language notice generation

*(Not in top 4 Gherkin stories)*

| Attack | Action |
|---|---|
| What if the LLM hallucinates in a low-resource language variant? (e.g., Swiss German vs German, Canadian French vs France French) | Flagged: all 5 target languages have high-resource LLM support. Dialect variants handled by market-specific rule engine, not by the LLM |
| What if a legal term doesn't have a recognised translation? (e.g., "fair value" has different legal meaning in UK vs Germany) | Added as compliance rule engine requirement: key legal terms must use the regulator-approved phrasing per market, not a literal translation |

---

## Patch Log — Error Paths & NFRs Added

| Story | Error path added | NFR added |
|---|---|---|
| S1 | Decomposition fallback (attribution <50% → market-level fallback template + audit tag + compliance officer notification) | Hallucination guard: numerical claims traced to source data; quarantine on failure |
| S2 | Partial batch failure (LLM API errors >2% → pause + retry + DORA escalation) | Cost ceiling (EUR 0.02/notice, EUR 40K/month alert) |
| S3 | Pre-deployment evidence request (link to legacy procedure) + retention expiry (response + audit log) | Response latency (5s evidence pack assembly) |
| S4 (story AC not expanded to Gherkin in this draft, but errors captured in adversarial review) | Cross-border rule conflict → escalate to compliance team | Rule coverage completeness ≥99.5% pass rate |
| S5 (AI Eval Card) | Language refusal trigger, repeated low-confidence responses → route to human | P95 latency <3.0s, P50 <1.5s, hard timeout at 4.0s |
| S6 | Fallback template causation view (warning banner + suggested script) | P95 <2.0s at 2,000 concurrent calls |

---

*All stories trace to personas in 02-personas-journey.md. Acceptance criteria are derived from the value hypothesis in 01-vision.md and the competitive gaps identified in 03-competitors.md. AI Eval Card methodology: probabilistic systems require confidence envelopes, not deterministic pass/fail.*
