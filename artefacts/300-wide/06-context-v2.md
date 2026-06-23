# 06-context-v2.md — Availability Freshness Indicator (Agent-Ready Handoff)

## Feature (one sentence)

Replace the binary "In stock" badge on click & collect product pages with a
calibrated per-store availability indicator that shows stock quantity, a
freshness timestamp ("Checked 12 min ago" from SAP sync time), and sell-through
velocity — and refuses to show a positive signal when data exceeds the 30-minute
staleness threshold.

## Who uses it

**Primary persona:** The recovery-path shopper — a click & collect customer who
has experienced phantom-stock disappointment (shelf empty despite "In stock"
badge) and now calibrates trust per store before making a trip.

**Secondary persona:** Any click & collect shopper comparing stores by distance,
quantity, and data freshness to decide where to pick up.

**Tertiary beneficiary:** Store staff — fewer "is this actually on the shelf?"
inbound calls because the indicator either shows concrete data or directs the
shopper to call the store before travelling.

## Technical environment

- **Frontend:** Mobile-web product page, responsive, mobile-first. Prototype
  targets 390 px viewport. Framework-agnostic (CSS custom properties).
- **Data source:** SAP inventory batch sync (15–30 min refresh window). API
  endpoint: `GET /api/stores/{storeId}/availability/{sku}`. Response shape:
  `{ storeId, sku, qtyOnShelf, sellThroughToday, lastSyncTimestamp, distance }`.
- **Staleness threshold:** Configurable via remote-config key
  `STALENESS_THRESHOLD_MINUTES` (default 30), overridable per store/region.
- **No AI model in Phase 0a.** The freshness indicator is a pure UX + API
  change. The confidence-percentage model (Phase 1) depends on Phase 0b
  micro-survey training data.
- **Integration surface:** Product Page → Store Availability API → SAP
  inventory batch. No handheld/staff integration in Phase 0a.
- **Design system:** Components reference named design tokens from
  `06-spec-v2.md` — colors (`--color-*`), typography (`--text-*`), spacing
  (`--space-*`), radii (`--radius-*`). No raw hex values in implementation.

## Hard constraints

1. **Never show a binary positive affirmation.** "In stock", "Available",
   "Available for Click & Collect", green checkmarks, or any equivalent
   guarantee of shelf presence must not appear in any state (AI-AC6). Enforced
   by grep in CI.
2. **Timestamp source must be SAP sync time, not page-load time.** The
   component receives `lastSyncTimestamp` as a prop; it does not generate its
   own timestamp (AI-AC3).
3. **Stores with null/missing/timeout stock data are omitted.** No guessing,
   no "unknown" placeholder (Base AC3).
4. **Disclosure wording is verbatim.** The `DisclosurePanel` text must match
   the approved string exactly. No additions, omissions, or marketing gloss
   (AI-AC4).
5. **Staleness threshold enforces visual-gate switch.** At >30 min sync age,
   quantity is hidden ("—") and uncertainty fallback is shown (AI-AC1 +
   AI-AC2 boundary).
6. **Conservative bias.** When in doubt between showing a number and showing
   uncertainty, show uncertainty. False negatives (missing a sale) cost less
   than false positives (wasted trip).

## Out-of-scope

- **Confidence percentage model (Phase 1).** No "87% likely" display.
- **Micro-survey feedback loop (Phase 0b).** "Did you find it?" survey is a
  parallel workstream, not part of this UI.
- **Staff confirmation hold workflow (Phase 2 / Cluster 3).** Handheld
  confirmation, physical badge, dynamic hold windows.
- **Staff dashboard.** Internal tooling not visible to shoppers.
- **Proactive recovery (Cluster 4).** Alternate-store re-routing after failed
  pickup.
- **Accessibility audit.** Screen-reader labels, focus order, ARIA deferred to
  implementation. Dark mode and 320px narrow-phone QA deferred.
- **Localisation.** Disclosure and CTA strings in EN only for Phase 0a pilot.

## Related artifacts

| Artifact | Path | v2? | Purpose |
|----------|------|-----|---------|
| JTBD feasibility | `00-jtbd-feasibility.md` | v1 | Confirmed model does not exist; scoped Phase 0a |
| Journey map | `01-journey-map-v2.md` | v2 | Recovery-path shopper's emotional arc |
| Heuristic evaluation | `02-heuristic-evaluation.md` | v1 | Every competitor fails H1 (visibility) and H2 (real-world match) |
| Workshop plan | `02-workshop-v2.md` | **v2** | HMWs name journey step + emotion; post-decision refinements |
| Decision | `03-decision-v2.md` | **v2** | Phased approach validated; forced outcome metric (8% → <3%) |
| AI acceptance criteria | `04-ai-ac-v2.md` | **v2** | 6 ACs refined to design specifics with 6-slot template |
| HTML mockup | `05-mockup.html` | v1 | Clickable 3-screen prototype |
| Spec (design tokens + components) | `06-spec-v2.md` | **v2** | Agent-ready handoff with Mermaid screen flow |
| Validation plan | `07-validation-plan-v2.md` | **v2** | 5 usability tasks with AC traceability |
| Narrative 1-pager | `07-narrative.md` | v1 | Benefit, costs, forced outcome metric |
| Synthesis spreadsheet | `03-synthesis.xlsx` | v1 | Original cluster scoring |
