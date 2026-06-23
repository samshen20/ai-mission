# Decision — Challenge & Revise Top Pick

**Date:** 2026-06-18
**Author:** Fresh AI challenge session
**Decision:** **Revise** — split Cluster 1 into phased delivery; surface hidden dependencies.

---

## The Top Pick (from 03-synthesis.xlsx)

**Cluster 1 — Confidence-aware availability signal on product page**
- Show estimated likelihood (%) with freshness indicator ('checked X min ago') and one-line explainer of recent sell-through velocity
- Impact: 5/5, Effort: 3/5, Priority Score: 2.0 (I-E)
- Quadrant: DO FIRST
- Rationale: "Core intervention. Replaces binary 'In stock' with calibrated estimate. Sets expectations, contains disappointment even when wrong. Low effort for UX change; **model already exists**. Highest ROI of any cluster."

---

## Challenges

### Challenge 1 — The "model already exists" assumption is false

The JTBD feasibility check reveals the confidence model does **not** exist. Building it requires:
- Historical sell-through velocity at per-store per-SKU granularity (SAP may not expose this)
- Sync-latency decay curves (the 15–30 min SAP window needs calibration)
- Time-of-day / day-of-week traffic pattern data
- Negative-signal training data from failed pickups

The "Low effort for UX change" may be correct for the UI layer, but **the underlying model pipeline is a significant engineering investment.** Effort should be re-scored as **4/5** for the full Cluster 1, **2/5** for a UI-only subset (explainer + freshness indicator with no percentage).

### Challenge 2 — Cluster 6 (micro-survey) is a prerequisite, not a background task

The synthesis places Cluster 6 as "DO NOW (background)" — low priority, ship whenever. But Cluster 1's confidence model **cannot learn without training data**, and Cluster 6 is the only source of ground-truth negative signals ("No — shelf was empty").

The real dependency chain is: **Cluster 6 → Cluster 1b (confidence %)**, not independent. If we ship Cluster 1's percentage model without the micro-survey feedback loop, the model has no way to improve — it's stuck at launch-day accuracy forever.

Cluster 6's relative effort (1/5) and high strategic leverage actually make it a **P0 dependency**, not a background nice-to-have.

### Challenge 3 — The confidence % UX is unvalidated

The workshop identified this as **the critical decision** — "Do we show estimated availability with a confidence cue, or hide it until staff confirms?" The workshop explicitly flagged: "Some users may find 67% confusing or anxiety-inducing."

The journey map v2 shows the recovery-path shopper at "Cautious" with 67% — "heads or tails?" Yet the synthesis presents the percentage model as the default, with no contingency for user testing results that show confusion.

A UX prototype test is needed before committing to the percentage display. If users find it confusing, the "light" version (explanatory text only) is the safer default.

### Challenge 4 — Cluster 3 (staff hold) has equal priority and addresses the root cause

Clusters 1 and 3 both score 5/3 = 2.0. The synthesis breaks the tie by calling Cluster 1 "Highest ROI" — but Cluster 3 (staff confirmation + physical badge + hold shelf) **eliminates the root cause** of phantom stock for confirmed items, while Cluster 1 only manages expectations about it.

If budget only covers one thing, Cluster 3 prevents the problem and Cluster 1 communicates about it. The sequence matters: confidence signal first builds trust, but without the hold workflow, even a perfect confidence signal doesn't prevent wasted trips for the 67% user.

### Challenge 5 — The freshness indicator and the confidence percentage are different features masquerading as one

"Checked 12 min ago" is a pure UI change — no model needed, just a timestamp from SAP.
"85% likely in stock" requires a predictive model with training data.

Bundling them as one cluster (Impact 5, Effort 3) hides a very different effort profile for the two halves. The freshness indicator alone is Impact 4, Effort 2. The percentage model alone is Impact 5, Effort 4. They should be separate work items.

---

## Revised Recommendation

### Keep the top pick's direction — but split it into a phased sequence

| Phase | What | Impact | Effort | Depends on |
|---|---|---|---|---|
| **0a** | **Freshness indicator + sell-through explainer** on product page. No percentage. "4 remaining at High Street (checked 12 min ago — sold 8 today)" | 4 | 2 | Nothing — pure UX change |
| **0b** | **Micro-survey (Cluster 6)** — "Did you find it?" single-tap after collection/cancellation | 2 | 1 | Order state (already exists) |
| **1** | **Confidence percentage model** — trained on SAP data + survey signals from Phase 0b | 5 | 4 | Phase 0b data (minimum 2–4 weeks of survey responses) |
| **2** | **Staff confirmation hold (Cluster 3)** — handheld workflow, physical badge, dynamic hold window | 5 | 3 | Phase 1 confidence data (to decide which items to hold vs let expire) |

### Why this sequence

1. **Phase 0a** is the quick win — addresses the heuristic violations (H1 visibility, H2 real-world match) that every competitor fails at. Ships in weeks, not months. No model, no handheld integration, no operational change.
2. **Phase 0b** starts collecting training data immediately, so by the time the model team is ready to build the confidence estimator, they have real signal data instead of synthetic assumptions.
3. **Phase 1** deploys the percentage once the model has data to learn from — and after UX testing validates that shoppers understand the pattern.
4. **Phase 2** adds the hold workflow, which is the highest operational lift. By Phase 2, the confidence signal is already shipping, so store staff are already familiar with the availability concept before the handheld workflow changes.

### Revised scoring for the original top pick

If we keep Cluster 1 as written (bundled), the more honest scoring is:
- **Impact:** 5 — still correct
- **Effort:** 4 — not 3, because the model pipeline is non-trivial and the UX pattern needs validation
- **Priority Score:** 1.0 (not 2.0) — still DO FIRST but not by the margin originally claimed
- **New Quadrant:** DO FIRST alongside Cluster 6

---

## Owner

**Sarah Chen (Product Lead / Head of Digital, Meridian)** — owns the phasing decision and the UX prototype test that validates or invalidates the percentage display. Engineering (model pipeline) and Store Operations (hold workflow) are key stakeholders for Phase 1 and Phase 2 timing.

---

## What Was Not Challenged

The following aspects of the synthesis remain sound:
- **Cluster 2 (pre-check ping)** correctly scored as DO NEXT — depends on confidence signal infrastructure.
- **Cluster 4 (proactive recovery)** correctly positioned as a downstream capability — depends on the hold workflow (Cluster 3) for confirmed alternative-store data.
- **Cluster 5 (staff dashboard)** is DO LATER — an internal tool that doesn't directly improve the customer experience.
- **"Conservative bias"** from the JTBD feasibility (favour false negatives over false positives) is the correct tuning strategy and should be baked into the model card.
