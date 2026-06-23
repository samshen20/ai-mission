# User Story & AI Acceptance Criteria — Availability Freshness Indicator

## User Story

**AS A** shopper browsing a product for click & collect pickup
**I WANT** to see when the store stock data was last checked and how fast the item has been selling
**SO THAT** I can gauge whether the item is likely to still be on the shelf when I arrive, without relying on a vague "In stock" label that has no timestamp or context.

---

## Base AC (supplied)

These four acceptance criteria define the basic no-AI behaviour of the availability indicator. They govern all stores and products regardless of whether the AI layer is present.

```
AC1. GIVEN a product has store stock data
     WHEN the shopper views the product page
     THEN the page shows an availability indicator per nearby store.

AC2. GIVEN no store within the configured range has stock data
     WHEN the shopper views stores
     THEN the page shows "Not collectable nearby" AND a home-delivery CTA.

AC3. GIVEN stock data is missing for a store (API timeout, no sync, null)
     WHEN the shopper views nearby stores
     THEN that store is omitted from the list — do not guess or show "unknown".

AC4. GIVEN the shopper taps a store in the list
     WHEN the store detail expands
     THEN it shows last-confirmed timestamp ("Checked 12 min ago") AND distance from the shopper's location.
```

---

## AI-Specific AC (one testable clause per dimension)

These six criteria test the AI-driven decisions in the freshness indicator (Phase 0a from 03-decision.md). Each clause is written to be falsifiable by a single observation.

### AI-AC1 (confidence)
```
GIVEN a store has stock data
 WHEN the last-confirmed time is within the staleness threshold (≤30 min since SAP sync)
 THEN the indicator shows the stock quantity AND the time label ("Checked 12 min ago")
 BUT WHEN the last-confirmed time exceeds the staleness threshold (>30 min)
 THEN the indicator replaces the quantity with "Last checked >30 min ago — may have changed"
      AND shows a "Check before you go" CTA.
```

**Why:** The shopper's confidence in the availability estimate decays with sync staleness. Within the 15–30 min SAP sync window, the raw quantity is shown. Beyond that window, the system consciously refuses to show a quantity because it cannot guarantee the data reflects current shelf state. The staleness threshold is configurable and testable at 30 min.

**Falsifiable?** Yes. Mock a 12-min-old sync → expect quantity shown. Mock a 31-min-old sync → expect staleness text + CTA, no quantity.

---

### AI-AC2 (refusal/fallback)
```
GIVEN the AI freshness layer cannot determine availability
     (stock data is stale beyond threshold OR sync is absent)
 WHEN the shopper views the store's availability indicator
 THEN the indicator shows "Availability uncertain" in amber/neutral styling
      AND displays a "Check current availability" button that triggers a
      real-time staff ping, AND does NOT show a positive green badge.
```

**Why:** When the system doesn't know, it must refuse to display a positive signal. This prevents the phantom-stock error of the current 'In stock' badge when data is stale. The fallback is a real-time staff ping — the only correct action when batch data is unreliable. Amber/neutral styling prevents misinterpretation as a positive signal. The prompt at 03-decision.md warned that the current synthesis glossed over the "87% → still wrong" problem.

**Falsifiable?** Yes. Force a stale-sync scenario → observe indicator styling (must not be green/positive), observe text (must say "uncertain"), observe CTA presence.

---

### AI-AC3 (latency)
```
GIVEN the product page loads
 WHEN the availability indicator is rendered
 THEN the last-confirmed time shown must be the SAP sync timestamp
      (not the page-load timestamp), AND the displayed time must be within
      one sync cycle (±1 min tolerance) of the wall-clock time elapsed
      since the SAP batch arrived.
```

**Why:** If the system shows the page-load time instead of the SAP sync time, the indicator is misleading — it reports freshness that the data does not have. The SAP sync window is 15–30 min; a "Checked 0 min ago" on page load falsely implies real-time data. This requirement forces the frontend to propagate the SAP metadata timestamp, not generate its own.

**Falsifiable?** Yes. Instrument the API response with a known SAP sync timestamp. Page-load time is independently observable. If displayed time ≤ 1 min from page load when SAP sync was 15 min ago, the test fails.

---

### AI-AC4 (disclosure)
```
GIVEN the availability indicator is visible on the product page
 WHEN the shopper taps or hovers the info icon ("ⓘ" or "How is this calculated?")
 THEN a disclosure panel appears stating, verbatim:
      "Stock data refreshes from store systems every 15–30 minutes.
       Quantities may change between refreshes. On-shelf availability
       is not guaranteed. Contact the store to confirm."
     AND no additional claims about accuracy or guarantees appear.
```

**Why:** Shoppers need to know what the indicator is and isn't. The heuristic evaluation (H2 — match between system and real world) found every competitor uses everyday words like "In stock" that overpromise. Verbatim disclosure prevents marketing-language drift. The wording is deliberately conservative — it doesn't say "we're accurate X% of the time" because Phase 0a does not have a model backing it yet. No additional claims ensures the disclosure doesn't contradict itself.

**Falsifiable?** Yes. Open the disclosure. Compare displayed text verbatim to the required string. Any deviation, addition, or omission is a failure.

---

### AI-AC5 (feedback)
```
GIVEN a click & collect order reaches a terminal state
     (collected → closed, or cancelled → refunded)
 WHEN the order status transitions to terminal
 THEN within 5 minutes the shopper receives a single-tap survey notification
      with the text "Did you collect the [item name] today?"
      AND exactly four response options:
        • "Yes"
        • "No — shelf was empty"
        • "No — couldn't find it in store"
        • "Other"
      AND the response is recorded per store+SKU+time-of-day bucket
```

**Why:** Phase 0b from 03-decision.md — the micro-survey is a prerequisite for the confidence model (Phase 1). Without negative training signals, the future confidence percentage has no way to learn. The 5-minute window ensures the collection experience is fresh in the shopper's mind. Per-store+SKU+time-of-day recording is the grain needed for the model to learn patterns. Exactly four options prevents ambiguous categorisation.

**Falsifiable?** Yes. Trigger a collected order → observe notification within 300 s. Count options (must equal 4, must be exact strings). Check the data store log for granularity.

---

### AI-AC6 (negative AC — what must NOT happen)
```
GIVEN any state of the system (fresh data, stale data, missing data, API failure)
 WHEN the availability indicator is displayed
 THEN the page must NOT show any of the following strings:
      "In stock", "Available", "In Stock", "Available for Click & Collect",
      green checkmark, or any binary positive-affirmation pattern
      suggesting a guarantee of shelf presence.
```

**Why:** The binary "In stock" badge is the root cause of phantom stock disappointment per the journey map (step 7: shelf empty despite "In stock"). The entire decision in 03-decision.md is to replace this pattern with a calibrated indicator. Even the freshness indicator ("4 remaining — checked 12 min ago") is not a guarantee — it's a data point. This negative AC prevents regression to the old pattern. Testing this requires grepping the rendered DOM for every forbidden string.

**Falsifiable?** Yes. Render the page in every state (fresh, stale, missing, error). Inspect the rendered DOM for banned strings. Any hit is a failure.

---

## Comparison with Answer Key (03-decision.md)

| AC | Alignment with decision | Verdict |
|---|---|---|
| Base AC1–AC4 | Matches Phase 0a scope — freshness indicator + store listing with timestamps | ✅ Aligned |
| AI-AC1 (confidence) | Implements the "staleness threshold" from Challenge 1 — no percentage shown (that's Phase 1), but quantity shown within sync window and staleness caveat outside it | ✅ Aligned — bias toward conservative display matches the "favour false negatives" decision |
| AI-AC2 (refusal/fallback) | Covers the "what to show when data is stale" edge case — matches the Decision's instruction that the indicator must not show positive affirmation without fresh data | ✅ Aligned |
| AI-AC3 (latency) | Prevents the "page-load timestamp" deception — the decision's Challenge 5 discovered the freshness indicator is a different feature from the confidence percentage; this AC locks down the correct timestamp source | ✅ Tightened from original — original didn't specify SAP vs page-load timestamp |
| AI-AC4 (disclosure) | Matches the heuristic evaluation finding (H2 — set calibrated expectations). Verbatim wording prevents overpromise. | ✅ Aligned — disclosure wording drafted to match Phase 0a scope (no model claims) |
| AI-AC5 (feedback) | Implements Phase 0b of the decision — Cluster 6 micro-survey as prerequisite for Phase 1. Specimen text and response options are newly drafted here. | ✅ Aligned — but note the decision says "ship immediately as background", not "block Phase 0a". This AC tests the survey separately. |
| AI-AC6 (negative) | Directly enforces the decision to replace binary "In stock" badges — the most important operational boundary from the workshop and v1→v2 journey map | ✅ Aligned — most critical AC; tests the core change in behaviour |

### Clauses tightened

1. **AI-AC3** originally would have accepted any "last checked X min ago" text. Tightened to specify the source must be the SAP sync timestamp, not a client-generated timestamp. Without this, a lazy frontend implementation could show "Checked 0 min ago" on every page load, defeating the transparency purpose.

2. **AI-AC4** (disclosure) originally was just "show an explainer." Tightened to verbatim wording with a "no additional claims" clause, so marketing cannot add "95% accurate" language that Phase 0a's non-model indicator doesn't support.

3. **AI-AC6** (negative) originally was just "don't show a binary 'In stock' badge." Tightened to explicitly enumerate all common variant strings and patterns ("green checkmark", "Available", "Available for Click & Collect") to prevent UX regression under different names.

### One gap found

**AI-AC1 and AI-AC2 share a boundary condition.** If the staleness threshold is exactly 30 min, and the sync arrives at 29:59 vs 30:01, the display toggles between "quantity" and "uncertainty." The gap is: the ACs don't specify a debounce or hysteresis zone around the threshold to prevent flickering if the sync timestamp jitters. A real implementation would need a ±2 min hysteresis zone around the threshold where the display doesn't flip. This is a refinement recommendation, not a blocker for the ACs as written — the ACs are testable as-is, and hysteresis can be added during implementation.
