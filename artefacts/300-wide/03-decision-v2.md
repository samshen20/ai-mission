# Decision v2 — Challenge & Revise Top Pick (Validated)

**Date:** 2026-06-22
**Author:** Design-meridian v2 pass — incorporates prototype validation
**Decision:** **Phase 0a validated.** Ship the freshness indicator without the
confidence percentage. Pilot for 90 days. If cancellation-due-to-unavailable
does not drop below 3%, accelerate Phase 1 (confidence model).

---

## v1 → v2 Changes

| Aspect | v1 (2026-06-18) | v2 (2026-06-22) |
|--------|-----------------|-----------------|
| **Confidence display** | "Show estimate vs hide until confirmed" — open question | Resolved. Phase 0a shows freshness data only (quantity + timestamp + velocity). No percentage. |
| **Prototype exists?** | No | Yes — `05-mockup.html`, 3 screens, clickable, design-token-complete |
| **Usability tested?** | No | Plan written — `07-validation-plan.md`, 5 tasks, 5 participants |
| **Outcome metric** | Unspecified | Forced: cut cancellation-due-to-unavailable from 8% → <3% in 90 days |
| **Cost estimate** | Unspecified | ~2 person-months, 5–6 weeks elapsed |
| **Design tokens** | Not named | Full token set in `06-spec.md` — colors, typography, spacing, radii |
| **Negative AC** | Drafted | Refined with enforcement table — every forbidden string mapped to where it's prevented |

---

## The Top Pick (from 03-synthesis.xlsx)

**Cluster 1 — Confidence-aware availability signal on product page**
- Show estimated likelihood (%) with freshness indicator ('checked X min ago')
  and one-line explainer of recent sell-through velocity
- Impact: 5/5, Effort: 3/5 (originally), Priority Score: 2.0 (I-E)
- Quadrant: DO FIRST
- Rationale: "Core intervention. Replaces binary 'In stock' with calibrated
  estimate. Sets expectations, contains disappointment even when wrong."

---

## Challenges Revisited (v1 → v2 status)

### Challenge 1 — The "model already exists" assumption is false

**v1 finding:** The confidence model does not exist. Building it is Effort 4/5.
**v2 resolution:** Accepted. Phase 0a ships without the model. The freshness
indicator uses only data Meridian already has (SAP sync timestamp, quantity on
shelf, sell-through count). Effort rescored to 2/5 for Phase 0a.
**Status:** ✅ Resolved by scoping.

### Challenge 2 — Cluster 6 (micro-survey) is a prerequisite, not a background task

**v1 finding:** The confidence model needs training data from the micro-survey.
**v2 resolution:** Phase 0b (micro-survey) ships alongside Phase 0a as an
independent workstream. It collects data passively while Phase 0a pilots.
Phase 1 does not begin until 2–4 weeks of survey responses are collected.
**Status:** ✅ Resolved by parallel workstreams.

### Challenge 3 — The confidence % UX is unvalidated

**v1 finding:** The workshop flagged "some users may find 67% confusing."
**v2 resolution:** Phase 0a avoids the percentage entirely. The prototype shows
only concrete data (quantity, timestamp, velocity). The usability test plan
(07-validation-plan.md) includes Task 3 (stale data) and Task 5 (fallback
action) to validate the uncertainty pattern without a percentage. If users
handle the amber uncertainty state well, Phase 1 can add the percentage later.
**Status:** ✅ Resolved by deferring the percentage to Phase 1. Prototype
validates the uncertainty pattern without it.

### Challenge 4 — Cluster 3 (staff hold) has equal priority

**v1 finding:** Clusters 1 and 3 both score 5/3. Cluster 3 eliminates the root
cause; Cluster 1 communicates about it.
**v2 resolution:** Sequence confirmed. Phase 0a ships first (manage
expectations). Phase 2 (staff hold) ships after Phase 1 confidence data is
available. The confidence signal from Phase 1 informs which items to hold vs
let expire. Phase 2 is not deferred — it's sequenced.
**Status:** ✅ Resolved by sequencing.

### Challenge 5 — Freshness indicator and confidence % are different features

**v1 finding:** Bundling them as one cluster hides different effort profiles.
**v2 resolution:** Unbundled. Phase 0a = freshness indicator (Impact 4, Effort
2). Phase 1 = confidence percentage (Impact 5, Effort 4). Separate work items,
separate ACs, separate ship dates.
**Status:** ✅ Resolved by unbundling.

---

## Validated Phased Sequence

| Phase | What | Impact | Effort | Depends on | Ship target |
|---|---|---|---|---|---|
| **0a** | Freshness indicator + sell-through explainer on product page. No percentage. "4 remaining at High Street (checked 12 min ago — sold 8 today)" | 4 | 2 | Nothing — pure UX + API change | Weeks 1–6 |
| **0b** | Micro-survey — "Did you find it?" single-tap after collection/cancellation | 2 | 1 | Order state (already exists) | Weeks 3–8 (parallel) |
| **1** | Confidence percentage model — trained on SAP data + survey signals from Phase 0b | 5 | 4 | Phase 0b data (2–4 weeks of responses) | Week 12+ |
| **2** | Staff confirmation hold — handheld workflow, physical badge, dynamic hold window | 5 | 3 | Phase 1 confidence data | Week 16+ |

---

## Prototype → Spec Traceability

| Prototype element (`05-mockup.html`) | Spec component (`06-spec.md`) | AC |
|---|---|---|
| Screen 1: Store list with freshness badges | `StoreCard` (fresh + stale variants) | Base AC1, AI-AC1 |
| Screen 2: Expanded fresh detail with velocity | `StoreDetail` (fresh-detail variant), `VelocityBlock` | Base AC4, AI-AC1, AI-AC3 |
| Screen 3: Uncertainty banner + fallback CTAs | `StoreDetail` (uncertainty variant), `UncertaintyBanner` | AI-AC2 |
| ⓘ icon + disclosure panel | `DisclosurePanel` (collapsed/expanded) | AI-AC4 |
| Absence of "In stock" / green checkmarks | All components, all states | AI-AC6 |
| "Checked 12 min ago" using SAP timestamp | `FreshnessBadge` (fresh variant) | AI-AC3 |

---

## Owner

**Sarah Chen (Product Lead / Head of Digital, Meridian)** — owns the Phase 0a
ship decision, the pilot market selection, and the 90-day outcome assessment.
Engineering (freshness API + frontend) and Store Operations (staff ping
workflow, Phase 2 prep) are key stakeholders.

---

## What Was Not Challenged (carried forward from v1)

- Cluster 2 (pre-check ping) correctly scored as DO NEXT
- Cluster 4 (proactive recovery) is a downstream capability
- Cluster 5 (staff dashboard) is DO LATER
- "Conservative bias" (favour false negatives) is the correct tuning strategy

---

## Forced Outcome Metric

> **Cut click & collect cancellation-due-to-unavailable from 8% → <3%**
> *Measured 90 days post-launch across pilot stores.*

If <3% is not met at 90 days, Phase 1 (confidence percentage model) is
accelerated. If <3% IS met, Phase 1 becomes optional — Phase 0a alone is
sufficient.
