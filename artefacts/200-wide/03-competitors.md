# Competitive Landscape — Personalised Policy Communication Engine

**product:** Kepler Insurance
**feature:** Personalised Policy Communication Engine
**date:** 2026-06-18
**approach:** Research mode on three adjacent products that solve the same job ("help insurance customers understand their renewal pricing so they don't churn"). Comparison table with strength/weakness/gap analysis.

---

## Products Selected

| # | Product | Why adjacent | Angle on the job |
|---|---|---|---|
| 1 | **Lemonade — AI Policy Management** (Crystal / Policy 2.0) | Digital-native carrier that made transparent, chatbot-driven policy communication its differentiator from founding. They solve "customer doesn't understand insurance" proactively — at point of sale and point of claim. | **Proactive UX transparency** — explain everything up front so there's no surprise at renewal |
| 2 | **Zendesk for Insurance** (CX platform — AI-powered customer service) | The reactive substitute: when customers can't understand their renewal, they call or message support. Zendesk's insurance vertical uses AI to deflect those calls, auto-answer "why did my premium go up?" queries, and reduce AHT. | **Reactive deflection** — answer the question when the customer asks, in the channel they choose |
| 3 | **Compare the Market / Moneysupermarket** (aggregator platforms) | The adversarial substitute: when customers don't understand and don't trust, they leave. Aggregators solve "help me find a better deal" from the opposite direction — no explanation, just a faster exit. | **Competitive substitution** — don't explain, just offer alternatives |

---

## Comparison Table

| Product | How they solve it | Strength | Weakness |
|---|---|---|---|
| **Lemonade — AI Policy Management** | Uses an AI chatbot (AI Jim) to explain policy terms, coverage, and pricing in conversational plain language at every touchpoint. Policy 2.0 rebuilt the policy document itself as an interactive, searchable experience — no PDF, no legalese. | Conversational UX is the best in insurance. AI Jim achieves 96%+ intent recognition on policy questions. They rebuilt the core artifact (the policy) rather than layering communication on top of a legacy system. | Only works in Lemonade's own stack — they control the entire tech chain from rating to delivery. Not available as a platform for carriers with legacy PAS. US-first; European multi-market regulatory compliance (FCA, BaFin, ACPR) is unproven. Cannot decompose a premium from a system they didn't build. |
| **Zendesk for Insurance (AI CX)** | Uses retrieval-augmented generation (RAG) on an insurer's knowledge base + policy data to auto-answer "why did my premium go up?" in email, chat, or voice. Intent detection routes questions about pricing to the AI; human agents handle appeals. Deflects ~35% of renewal-related contacts per Zendesk insurance benchmarks. | Works with any existing policy admin system — no core system change needed. Multi-channel (web chat, WhatsApp, email, voice). Observable deflection ROI (reduced call volume) that traditional insurers understand. Built-in compliance audit trail for DORA evidence. | Reactive only — the customer must already be frustrated enough to contact support. Does not *prevent* the frustration at the point of the renewal notice. Cannot generate causal pricing explanations if the PAS doesn't expose component-level data (same dependency as our feature). Generic RAG on insurance docs produces plausible-sounding but sometimes wrong answers — hallucination risk in a regulated context. |
| **Compare the Market / Moneysupermarket** | Aggregates quotes from multiple carriers on a single form. Customer enters details once, sees ranked options by price. No explanation of *why* their current premium changed — just an alternative. Compara (Latin America) adds behavioural nudges ("you could save EUR 142") timed to renewal windows. | Zero switching cost for the customer. One form, 8 quotes, 5 minutes. Transparent pricing by design — there is no opacity when you see 8 prices side by side. Proven to capture 53%-shopping-rate customers (J.D. Power 2026). | Actively adversarial to the incumbent carrier. Their business model depends on customers being unhappy enough to switch. Zero explanatory value — they don't help customers understand pricing, they help them escape it. Cannot be a retention tool; only a leakage accelerant. No regulatory fair-value evidence. |
| **Us — Kepler Personalised Policy Communication Engine** | GenAI pipeline integrated into the renewal notice production system. Decomposes each premium change into causal factors (external indices + internal rating inputs + policy-specific variables). Generates plain-language explanation per policy. Passes through market-specific compliance rule engine before dispatch. Follow-up NPS captures satisfaction. | Proactive (sent with the notice, not reactive to a call). Causal (explains the specific *why*, not generic deflect). Regulator-ready (each notice is its own fair-value evidence). Multi-market by design (FCA / BaFin / ACPR rule engines per market). | Requires Phase 0 data readiness — if legacy PAS cannot expose component-level rating variables, personalisation degrades to aggregated market-level fallback. Requires human-in-the-loop compliance validation per market. Unproven at 500K policy scale in production. |

---

## Gap Analysis — Where All Three Competitors Are Weak or Identical

### Gap 1: Proactive causal explanation at the point of frustration

Lemonade explains proactively *before* the premium is set (at quote/policy issue), not at renewal when the price actually changes. Zendex explains reactively *after* the customer is frustrated enough to call. Compare the Market explains *nothing* — it helps the customer leave.

**All three are weak** at the specific moment that matters: the instant a customer opens their renewal notice and sees a number they don't expect. None of them insert an explanation into that moment.

**Us:** The personalised renewal notice *is* that moment. We own it by being the first explanation the customer sees — they don't have to call, chat, or search to get one.

---

### Gap 2: Regulatory evidence chain per customer communication

Lemonade's customer communications are not designed as regulatory evidence (they don't need to be — Lemonade is a US/EU carrier but doesn't decompose rating for FCA fair-value purposes). Zendesk's audit trail is operational (ticket history) not regulatory (fair-value attribution per policy). Compare the Market produces no regulatory evidence at all — they mediate, they don't underwrite.

**All three are identical** in that they cannot produce a regulator-ready fair-value evidence pack from a renewal communication. The customer-facing communication is decoupled from the compliance evidence requirement.

**Us:** Each personalised notice *is* the evidence. The compliance rule engine that validates the output also logs the attribution trail — one artifact serves both customer and regulator. This is the opening.

---

### Gap 3: Multi-market regulatory compliance as a feature, not a bolt-on

Lemonade operates in the US and a handful of EU markets with a single product (renters/contents) — their AI comms don't need to handle 5 different regulatory templates. Zendesk's compliance is generic (GDPR, DORA incident logging) — it doesn't map to FCA Consumer Duty fair-value templates vs BaFin pricing breakdown formats vs ACPR transparency requirements. Compare the Market complies with each market's comparison-site regulations (which are light) — not pricing communication rules.

**All three are weak** at jurisdictional regulatory nuance in insurance pricing communications. They either operate in one regulatory regime or treat compliance as a generic layer.

**Us:** Built for 5 markets from day one. The compliance rule engine is market-specific by design — not a generic document template but a rule set per regulator. This is our second opening.

---

## Differentiator Statement

> **Explain why the price changed, specific to that policyholder's data, in a regulator-ready form, before the customer has to ask.**

Verb + dimension: **instrument the renewal notice as a fair-value evidence artifact** — creating an auditable causation chain that no adjacent product produces, because none of them operate at the intersection of policy-level pricing decomposition + multi-market regulatory compliance + proactive customer communication.

---

## Strongest Competitor AI Feature to Fold In

**Lemonade's conversational AI (AI Jim) — the ability to answer "why?" in natural language, not just in a letter.**

Lemonade's AI Jim achieves 96%+ intent recognition on policy questions by treating every communication as a conversation, not a broadcast. The customer can ask "why?" and get a specific, contextual answer — they're not limited to what's printed on the letter.

**Fold into our feature:** The personalised renewal notice should be the *first* explanation, but not the *only* channel. Add a conversational follow-up capability: after the customer receives the notice, they can reply "why?" via email, web chat, or WhatsApp and receive a specific, policy-level causal breakdown generated by the same decomposition pipeline. This turns a one-directional communication event into a two-directional understanding loop — without routing through a human call centre.

**Implementation note:** This requires a lightweight conversational UI layer on top of the existing decomposition pipeline. The causation data is already generated for the letter; the conversational layer just re-renders it per the customer's question. Estimated +EUR 60K on build scope, +EUR 10K/year on LLM inference costs.

---

## Summary Table

| Dimension | Lemonade | Zendesk | Compare the Market | **Us** | Gap we own |
|---|---|---|---|---|---|
| Proactive explanation | ✅ At quote/policy issue | ❌ Reactive (customer calls first) | ❌ None | ✅ At renewal (the moment of frustration) | Gap 1 |
| Causal per-policy pricing decomposition | ❌ Doesn't decompose pricing | ❌ RAG on generic KB, not policy data | ❌ Not applicable | ✅ Phase 0 rating engine instrumentation | Gap 1 |
| Regulatory evidence chain per notice | ❌ Not designed as evidence | ❌ Operational audit trail only | ❌ No regulatory role | ✅ Notice = fair-value evidence artifact | **Gap 2 — our opening** |
| Multi-market regulator rule engines | ❌ US + 2 EU markets only | ❌ Generic compliance only | ❌ Comparison-site regulation only | ✅ 5 markets (FCA, BaFin, ACPR, IVASS, DGSFP) | **Gap 3 — our second opening** |
| Conversational follow-up ("why?") | ✅ AI Jim (best-in-class) | ✅ AI deflection for known queries | ❌ None | 🛠 **Proposed: add conversational layer** | Fold in Lemonade's strongest AI feature |
