# Pre-Mortem — Personalised Policy Communication Engine

## Top 3 Weaknesses (Sceptical Board Member)

### 1. (CRITICAL) Circular value thesis — the deck presents EUR4.5M of hypothetical returns as earned value

**One-line patch:** Add a "Contingent Value" callout to every ROI slide — "85% of projected returns depend on Assumption 1 validation (A/B test); if A/B fails this value is EUR0" — and restructure the deck so the A/B test ask (EUR80K) is the headline ask, not the EUR5.34M projection.

### 2. (HIGH) Data integration is the real gating factor but isn't costed or scheduled

**One-line patch:** Add a "Phase 0 — Data Readiness" line to the implementation budget (EUR80K per market, 2-3 months discovery) and a fallback scenario in the ROI sensitivity table: "If fallback templates used for >50% of policies, expected churn reduction drops to 0.5pp."

### 3. (HIGH) Regulatory timeline risk makes the 6-month deployment target unrealistic

**One-line patch:** Add a regulatory-delay scenario to the sensitivity table (EUR0 savings Year 1, EUR3.2M Year 2) and restate the 6-month target as "6 months post-regulatory clearance (estimated 12-18 months from project start)."
