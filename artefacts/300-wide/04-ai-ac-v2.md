# AI Acceptance Criteria v2 — Availability Freshness Indicator (Design-Specific)

**Feature:** Phase 0a — Freshness Indicator (no AI model)
**Date:** 2026-06-22
**Status:** Refined to design specifics using the 6-slot template
**Input:** `05-mockup.html` (clickable prototype), `06-spec.md` (design tokens)

---

## User Story

**AS A** shopper browsing a product for click & collect pickup
**I WANT** to see when the store stock data was last checked and how fast the
item has been selling
**SO THAT** I can gauge whether the item is likely to still be on the shelf when
I arrive, without relying on a vague "In stock" label that has no timestamp or
context.

---

## Base AC (supplied)

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
     THEN it shows last-confirmed timestamp ("Checked 12 min ago") AND distance
     from the shopper's location.
```

---

## AI-Specific AC (6 clauses, each falsifiable by one observation)

### AI-AC1 (confidence)

```
GIVEN a store has stock data
 WHEN the last-confirmed time is within the staleness threshold (≤30 min since
      SAP sync)
 THEN the indicator shows the stock quantity AND the time label
      ("Checked 12 min ago")
 BUT WHEN the last-confirmed time exceeds the staleness threshold (>30 min)
 THEN the indicator replaces the quantity with "Last checked >30 min ago —
      may have changed" AND shows a "Check before you go" CTA.
```

#### Refined to design specifics

| Slot | Value |
|------|-------|
| **Component** | `FreshnessIndicator` — comprises `FreshnessBadge` + quantity label + timestamp text |
| **Variant** | `fresh` (sync age ≤ 30 min) / `stale` (sync age > 30 min) |
| **Color token** | Fresh badge: `--color-fresh-bg` (#e8f5e9), `--color-fresh-text` (#2e7d32). Stale badge: `--color-stale-bg` (#fff3e0), `--color-stale-text` (#e65100). Stale card border: `--color-stale-border` (#ffcc80). Stale card bg: `--color-stale-card-bg` (#fffbf5) |
| **Typography** | Badge: `--text-label-sm` (12px, weight 600). Quantity: `--text-body` (14px, weight 700, `--color-ink`). Timestamp: `--text-body-sm` (13px, weight 400, `--color-text-body`). Stale caveat: `--text-body-sm` (13px, `--color-stale-text`) |
| **Placement** | Inline in `StoreCard` `store-meta` row, between quantity and velocity. In `StoreDetail`: left-aligned in `big-freshness` row alongside big quantity (`--text-qty-xl`, 36px, weight 800) |
| **Visual gate** | `now() - sap_sync_ts ≤ 30 min` → show quantity + "Checked X min ago" + `--color-fresh-bg` badge. `> 30 min` → amber border on `StoreCard`, stale `FreshnessBadge`, quantity prefixed with "may have changed". The timestamp must be the SAP sync time, not page-load time (AI-AC3). |

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

#### Refined to design specifics

| Slot | Value |
|------|-------|
| **Component** | `UncertaintyBanner` + `StoreDetail` (uncertainty variant) |
| **Variant** | `uncertainty` (sync age > 30 min OR sync absent) |
| **Color token** | Banner bg: `--color-stale-bg` (#fff3e0). Banner border: `--color-stale-border` (#ffcc80). Heading: `--color-stale-text` (#e65100). Body: `--color-stale-text-dark` (#bf360c). Low Confidence tag: `--color-stale-text` on `--color-stale-bg`, 1px `--color-stale-border`. Detail card bg: `--color-stale-card-bg` (#fffbf5). No `--color-fresh-*` tokens anywhere |
| **Typography** | Heading: `--text-heading-sm` (16px, weight 700). Body: `--text-body-sm` (13px, 400). Low Confidence tag: `--text-label-xs` (11px, weight 700, uppercase, 0.5px letter-spacing). Quantity: `--text-qty-xl` (36px, weight 800) rendered as "—" not a number |
| **Placement** | Full-width banner at top of `StoreDetail` screen (margin: `--space-lg` 16px). Below: stale detail card with "—" quantity, detail rows, no velocity block. Below card: CTAs stacked in priority order — (1) "📞 Can't confirm — call the store" (`btn-amber`, `--color-stale-bg`), (2) "Ping staff to check shelf" (`btn-outline`), (3) "← View other stores" (`btn-outline`). Bottom: "Why don't I see a quantity?" disclosure |
| **Visual gate** | ① Quantity rendered as "—" (not a number). ② "⚠ Low Confidence" tag visible. ③ "Availability uncertain" heading present. ④ "Can't confirm — call the store" CTA is the primary action. ⑤ No green, no `--color-fresh-*` tokens. ⑥ No positive-affirmation strings (AI-AC6). ⑦ All CTAs are actionable (not disabled, not greyed out) |

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

**Design note:** This is a data-integrity AC, not a visual one. The frontend
must propagate `lastSyncTimestamp` from the API response (`GET
/api/stores/{id}/availability/{sku}`) and compute the displayed "Checked X min
ago" label as `now() - lastSyncTimestamp`. It must NOT use `Date.now()` at
render time as the "checked" time. The `FreshnessBadge` component receives the
timestamp as a prop; it does not generate its own.

**Falsifiable?** Yes. Instrument the API response with a known SAP sync
timestamp (e.g., 15 min ago). Page-load time is independently observable. If
displayed time ≤ 1 min from page load, the test fails.

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

#### Refined to design specifics

| Slot | Value |
|------|-------|
| **Component** | `DisclosurePanel` |
| **Variant** | `collapsed` (default, `display: none`) / `expanded` (on ⓘ tap, `display: block`) |
| **Color token** | Bg: `--color-disclosure-bg` (#f5f5f7). Border: `--color-disclosure-border` (#e5e5ea). Text: `--color-text-secondary` (#6e6e73). Strong label: `--color-text-body` (#48484a) |
| **Typography** | `--text-caption` (12px, weight 400, line-height 1.5). Leading strong label: weight 600 |
| **Placement** | Below "Click & Collect" section title (`--text-heading-sm`, 16px, weight 700), above the first `StoreCard`. Toggled by the ⓘ icon — 18px circle, `--color-text-tertiary` (#8e8e93) border, `inline-flex` next to section title. Padding: 14px 16px. Radius: `--radius-md` (12px). Margin-bottom: `--space-lg` (16px) |
| **Visual gate** | **Verbatim text match required.** Rendered string must equal exactly: "Stock data refreshes from store systems every 15–30 minutes. Quantities may change between refreshes. On-shelf availability is not guaranteed. Contact the store to confirm." Any addition, omission, rewording, or marketing gloss is a failure. No "95% accurate" claims — Phase 0a has no model |

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

**Design note:** This is Phase 0b — delivers independently of Phase 0a. The
survey UI is not in the 3-screen mockup (05-mockup.html covers Phase 0a only).
This AC is carried forward for traceability; the full survey component spec is
deferred to the Phase 0b design pass.

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

#### Enforcement table (carried into `06-spec.md`)

| Forbidden string/pattern | Enforced in component | How |
|---|---|---|
| "In stock" / "In Stock" | `StoreCard`, `StoreDetail`, all states | No label uses "In stock." Store status is quantity + timestamp |
| "Available" / "Available for Click & Collect" | Section headings, CTAs, badges | Section heading: "Click & Collect" (no "Available"). CTA: "Reserve for pickup" (action), not a guarantee |
| Green checkmark (✅ ✔ 🟢) | `FreshnessBadge`, `StoreCard`, `StoreDetail` | Fresh variant uses ● (dot) + "Fresh data" text on `--color-fresh-bg` |
| Binary positive-affirmation pattern | `StoreDetail` CTA row | Footer: "On-shelf availability is not guaranteed" present on every detail screen |
| Any new guarantee-like string | All components, all future states | Code review gate: grep rendered DOM for the forbidden strings before deployment |

**Falsifiable?** Yes. Render the page in every state (fresh, stale, missing,
error). Inspect rendered DOM for forbidden strings. Any hit is a failure.

---

## Comparison with Answer Key (03-decision-v2.md)

| AC | v2 alignment | Verdict |
|---|---|---|
| Base AC1–AC4 | Matches Phase 0a scope — freshness indicator + store listing with timestamps | ✅ |
| AI-AC1 (confidence) | Design-refined with 6-slot template; staleness threshold at 30 min; no percentage | ✅ Aligned |
| AI-AC2 (refusal/fallback) | Design-refined; Low Confidence tag, uncertainty banner, 3 fallback CTAs | ✅ Aligned |
| AI-AC3 (latency) | SAP timestamp source enforced; falsifiable test specified | ✅ Tightened |
| AI-AC4 (disclosure) | Design-refined; verbatim text gate; ⓘ icon placement and tokens specified | ✅ Aligned |
| AI-AC5 (feedback) | Deferred to Phase 0b; carried forward for traceability | ⏳ Deferred |
| AI-AC6 (negative AC) | Enforcement table with per-component prevention; grep-able in CI | ✅ Aligned |

### v2 clauses tightened from v1

1. **AI-AC1** — Added `Visual gate`: `now() - sap_sync_ts ≤ 30 min` check
   explicitly tied to the `FreshnessBadge` variant switch.
2. **AI-AC2** — Added 7-point visual gate checklist (must show "—",
   Low Confidence tag, amber-only tokens, no positive strings).
3. **AI-AC4** — Added exact padding, radius, and margin tokens for the
   `DisclosurePanel`; tied to `--color-disclosure-*` tokens.
