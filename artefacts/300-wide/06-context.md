# 06-context.md — Availability Freshness Indicator

## Feature (one sentence)

Replace the binary "In stock" badge on click & collect product pages with a
calibrated per-store availability indicator that shows stock quantity, a
freshness timestamp ("Checked 12 min ago"), and sell-through velocity — and
refuses to show a positive signal when data is stale.

## Who uses it

**Primary persona:** The recovery-path shopper — a click & collect customer who
has experienced a phantom-stock disappointment (shelf empty despite "In stock"
badge) and now calibrates trust per store before making a trip.

**Secondary persona:** Any click & collect shopper browsing a product page who
needs to decide which store to pick up from. They compare stores by distance,
quantity on shelf, and how recently that quantity was confirmed.

## Technical environment

- **Frontend:** Mobile-web product page (responsive, mobile-first). The mockup
  targets a 390 px-wide viewport (phone form factor).
- **Data source:** SAP inventory batch sync (15–30 min refresh window). Each
  store+SKU record carries a `last_sync_timestamp` from the SAP batch, NOT a
  client-generated page-load timestamp.
- **Staleness threshold:** Configurable, default 30 minutes. When
  `now() - last_sync_timestamp > 30 min`, the indicator switches from the
  "fresh" variant to the "stale/uncertainty" variant.
- **No AI model in Phase 0a:** The freshness indicator is a pure UX change. The
  confidence-percentage model is Phase 1 and depends on micro-survey training
  data (Phase 0b). Phase 0a shows data we already have; it does not predict.
- **Integration surface:** Product Page → Store Availability API →
  SAP inventory batch. No handheld/staff integration in this phase.

## Hard constraints

1. **Never show a binary positive affirmation.** The strings "In stock",
   "Available", "Available for Click & Collect", a green checkmark, or any
   equivalent guarantee of shelf presence must not appear in any state (AI-AC6).

2. **Timestamp source must be SAP sync time, not page-load time.** A "Checked 0
   min ago" label computed from `Date.now()` at render time is a defect (AI-AC3).

3. **Stores with null/missing/timeout stock data are omitted** — no guessing, no
   "unknown" placeholder (Base AC3).

4. **Disclosure wording is verbatim.** The info panel text must match the
   approved string exactly with no additions, omissions, or marketing gloss
   (AI-AC4).

5. **Staleness threshold enforces visual-gate switch.** At >30 min sync age, the
   quantity is hidden and the uncertainty fallback is shown. No quantity
   displayed in the stale state (AI-AC1 + AI-AC2 boundary).

6. **Conservative bias.** When in doubt between showing a number and showing
   uncertainty, show uncertainty. False negatives (missing a real sale) are
   cheaper than false positives (wasted trip).

## Out-of-scope

- **Confidence percentage model (Phase 1).** Phase 0a does not predict
  availability; it surfaces the data we already have with a freshness timestamp.
  No "87% likely" display.
- **Micro-survey feedback loop (Phase 0b).** The "Did you find it?" post-
  collection survey is a prerequisite for Phase 1 but is not part of this UI.
- **Staff confirmation hold workflow (Phase 2 / Cluster 3).** Handheld
  confirmation, physical badge, and dynamic hold windows are downstream.
- **Staff dashboard.** Internal tooling not visible to shoppers.
- **Proactive recovery (Cluster 4).** Alternate-store re-routing after a failed
  pickup is out of scope for this feature.
- **Accessibility audit.** This mockup is visual-only; screen-reader labels,
  focus order, and ARIA are deferred to implementation.

## Related artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| JTBD feasibility | `00-jtbd-feasibility.md` | Confirmed the confidence model does not exist; scoped Phase 0a as a model-free quick win |
| Journey map v2 | `01-journey-map-v2.md` | Maps the recovery-path shopper's emotional arc through phantom-stock disappointment |
| Heuristic evaluation | `02-heuristic-evaluation.md` | Found every competitor's "In stock" badge violates H1 (visibility) and H2 (real-world match) |
| Workshop output | `02-workshop.md` | Identified the critical decision: show confidence cue or hide until staff confirms |
| Decision | `03-decision.md` | Split Cluster 1 into phased delivery; Phase 0a = freshness indicator alone |
| Synthesis spreadsheet | `03-synthesis.xlsx` | Original cluster scoring and quadrant placement |
| AI acceptance criteria | `04-ai-ac.md` | Full AC suite: 4 base + 6 AI-specific, each falsifiable by one observation |
| AC template | `04-template` | 6-slot structure for AI-AC refinement |
| HTML mockup | `05-mockup.html` | Clickable 3-screen prototype (Product → Fresh Detail → Stale Fallback) |
