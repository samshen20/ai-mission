# JTBD & Feasibility Checklist — Meridian Availability Assistant

**Product:** Meridian Retail Group
**Feature:** AI availability assistant (click & collect phantom stock estimator)
**Date:** 2026-06-18
**Status:** Feasibility gate — pre-PRD

---

## JTBD (Job To Be Done)

### Primary functional job

> **"When I'm browsing a product online, help me determine whether it's genuinely available for pickup at my nearby store, so I don't drive over and find nothing."**

**Context:** The shopper has chosen click & collect over delivery — they want speed, zero shipping cost, or immediate gratification. They check the product page, see "available at [store]", add to cart, drive there, and discover the shelf is empty. ~7% of click & collect orders cancel at pickup. The shopper experiences wasted time, transport cost, and eroding trust in the channel.

### Emotional jobs

> **"Give me confidence I won't waste a trip, so I feel smart — not foolish — for choosing click & collect."**

> **"Protect me from the frustration of trusting a system that reliably misleads me, so shopping doesn't feel like a gamble."**

### Related job (store operations)

> **"Flag phantom stock before the customer arrives, so my team stops wasting time processing cancellations and apologising for a system they can't fix."**

---

## Branch 1 — AI IN THE PROCESS (us using AI to design/deliver)

| Check | Verdict | Detail |
|---|---|---|
| **Client permits AI tools for delivery?** | **Yes** | Third-party AI (Claude / GPT / Gemini) explicitly permitted for delivery with anonymised inputs. EPAM CodeMie pre-approved for the engagement. No restriction on using AI to write code, documentation, or analysis for this feature. |
| **Sensitive data kept out of AI inputs?** | **Yes** | Brief mandates non-PII stock + store metadata only to the AI path. Customer identity, order history, payment data, and personal profile are explicitly excluded from AI inputs. Anonymisation boundary is clearly drawn and enforceable. |
| **Approved toolset named?** | **Yes** | Two tiers: (1) EPAM CodeMie — pre-approved, unrestricted use for delivery. (2) Claude / GPT / Gemini — permitted for delivery with anonymised inputs. No other models approved without fresh clearance. |

**Branch 1 verdict:** **Go.** AI tools permitted, data boundary clear, toolset named. No blockers on the process side.

---

## Branch 2 — AI IN THE PRODUCT (the availability assistant itself)

| Check | Verdict | Detail |
|---|---|---|
| **Stock data ready + fresh enough for the promise we'd make?** | **Conditional** | SAP sync latency is 15–30 minutes. Stock can be stale within the window — another customer may have purchased the last unit between the sync and the shopper's arrival. This means the AI cannot promise *certainty*. It must produce a **confidence estimate** ("85% likely available") that accounts for: (a) time since last sync, (b) historical sell-through rate for this SKU at this store (how fast does this item move?), (c) day-of-week/time-of-day traffic patterns, and (d) whether the item is a high-velocity SKU that depletes within the sync window. The promise shifts from "Is it there?" to "How confident are we that it's still there?" — this must be stated explicitly to the shopper. **Gate to close:** confirm SAP can expose per-SKU sell-through velocity at store level, or build a proxy from order history aggregates. |
| **Regulatory framework clear (GDPR/CCPA; AI-Act class)?** | **Conditional** | Non-PII stock data + store metadata means GDPR/CCPA exposure is low — no personal data enters the AI inference path. However, the CCPA applies to "any personalised surface": if the assistant tailors store rankings or confidence scores to user segments (e.g., "your usual store" based on browsing history), a privacy review is needed. The non-PII boundary defined in the brief keeps this clean at MVP scope. **Open gate — EU AI Act classification:** the brief says "No high-risk classification expected, but unconfirmed." An availability estimator that only processes stock data and outputs a confidence score is very unlikely to be classified as high-risk under Annex III (which covers biometrics, critical infrastructure, education, employment, credit, law enforcement, migration, and administration of justice). It is also not a "general-purpose AI system." However, "unconfirmed" means legal should sign off before production — 2–3 week review. **Gate to close:** secure a written AI Act classification opinion from legal (low-risk, no Annex III trigger) before Phase 1 build commit. |
| **Worst-case understood (who's harmed if the estimate is wrong)?** | **Conditional** | Two failure modes — neither is physically harmful, but both have commercial impact: **(a) False positive** — AI says "likely available" but shelf is empty → shopper drives for nothing (~7% of current orders). Customer anger, wasted time, channel trust erosion. Same harm as the current problem, but with higher stakes because the AI assistant raises expectations of accuracy. **(b) False negative** — AI says "uncertain / likely unavailable" but stock is actually there → shopper chooses home delivery instead. Unnecessary shipping cost (Meridian pays), delayed gratification (shopper waits 1–3 days). Margin erosion, not safety harm. **Commercial worst-case:** If both failure modes run at even 5%, the assistant could simultaneously increase cancellations (false positives drive wasted trips) and depress click & collect adoption (false negatives push shoppers to delivery). The assistant must be tuned to bias toward false negatives (conservative: "uncertain" rather than "yes") because the cost of a wasted trip (customer anger + channel abandonment) exceeds the cost of unnecessary delivery (margin impact per order ~EUR 3–5). **Gate to close:** define acceptable error rates per failure mode in PRD. Recommend: false positive rate <3%, false negative rate <15% (conservative bias). Document the bias decision in the model card. |

**Branch 2 verdict:** **Conditional go.** Stock staleness (15–30 min SAP sync) is manageable if the assistant outputs confidence estimates, not binary "yes/no." EU AI Act classification needs legal sign-off before production — 2–3 week review. Error bias must be tuned conservatively (favour false negatives over false positives) and documented in the model card. Both gates are openable within Phase 0.

---

## Approved-Tools List (remainder of series)

| Tool | Scope | Notes |
|---|---|---|
| **EPAM CodeMie** | Unrestricted — design, code, documentation, analysis | Pre-approved for the engagement |
| **Claude** (all models) | Delivery with anonymised inputs | Permitted for code, analysis, documentation. Stock metadata only — no PII. |
| **GPT** (all models) | Delivery with anonymised inputs | Same scope as Claude. |
| **Gemini** (all models) | Delivery with anonymised inputs | Same scope as Claude. |
| **Any other LLM** | Not permitted without fresh clearance | Escalate to engagement lead. |

**Decision rule for tool selection:** Prefer Claude for the AI assistant's inference path (strongest structured output compliance for confidence scoring). Use CodeMie for code generation. Reserve GPT/Gemini for analysis or documentation tasks where the other tools are unavailable.
