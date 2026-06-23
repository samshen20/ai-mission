# 07-narrative.md — 1-Pager: Availability Freshness Indicator (Phase 0a)

## Benefit

Click & collect shoppers today see a binary "In stock" badge that hides the
one fact they need most: **how recently was that confirmed?** When the badge is
wrong — and it is wrong for ~8% of pickups today — the customer drives to the
store, walks to the shelf, and finds nothing. They cancel the order. They leave
a 1-star review. They try a competitor next time.

Phase 0a replaces the lie with the truth. Every store listing shows:

- **How many** units the system last saw on the shelf
- **When** that number was last confirmed ("Checked 12 min ago")
- **How fast** the item is selling today ("8 sold today")
- **When to be careful** — if data is more than 30 minutes old, the system
  refuses to show a number and instead says "Availability uncertain — call the
  store"

The shopper makes an informed decision. The store avoids a wasted-trip
confrontation. Trust compounds with every accurate pickup.

No AI model. No handheld integration. No operational change. This is a pure
UX upgrade: show the data we already have, with the timestamp we already
receive, and refuse to overpromise.

---

## Engineering cost

**2–3 sprints (4–6 weeks, 1 full-stack engineer)**

| Work item | Effort | Notes |
|-----------|--------|-------|
| Store availability API endpoint | 3 days | `GET /api/stores/{id}/availability/{sku}` — expose `qtyOnShelf`, `sellThroughToday`, `lastSyncTimestamp`, `distance` from existing SAP batch data |
| Staleness-threshold config | 1 day | Remote-config key `STALENESS_THRESHOLD_MINUTES` (default 30), overridable per store/region |
| Frontend: StoreCard component | 3 days | Two variants (fresh/stale), 5 states, responsive |
| Frontend: StoreDetail + sub-components | 4 days | FreshnessBadge, UncertaintyBanner, VelocityBlock, DisclosurePanel |
| Frontend: screen navigation | 1 day | Product page → StoreDetail navigation, back-arrow, scroll-to-top |
| Integration + E2E tests | 3 days | Cypress/Playwright tests per AI-AC |
| Accessibility pass | 2 days | Focus order, ARIA labels, screen-reader announcement of stale state |
| **Total** | **~17 days** | One engineer, 3–4 weeks with buffer |

**What makes this cheap:** No model training, no pipeline, no staff handheld
device changes. The SAP sync timestamp already exists — we're just showing it.

---

## Design cost

**1 sprint (2 weeks, 1 product designer)**

| Work item | Effort | Notes |
|-----------|--------|-------|
| Final visual design | 3 days | Polish mockup tokens, dark mode, 320px narrow-phone QA |
| Interaction spec | 1 day | Tap targets, transitions, haptic on stale state |
| Prototype for usability test | 1 day | Clickable Figma prototype from 06-spec.md |
| Usability test (5 participants) | 2 days | Recruit + moderate + synthesis (07-validation-plan.md) |
| Design QA during build | 2 days | Pair with engineer, spot-check states |
| **Total** | **~9 days** | One designer, heavy lifting already done in 05-mockup + 06-spec |

**What makes this cheap:** The critical design decisions (amber uncertainty
styling, verbatim disclosure, no-green-checkmark rule) are already specified.
The designer is refining, not discovering.

---

## Content cost

**0.5 sprint (~3 days, UX writer review)**

| Work item | Effort | Notes |
|-----------|--------|-------|
| Disclosure panel wording | — | Already drafted verbatim in AI-AC4; needs legal + UX writer sign-off |
| Uncertainty banner copy | 0.5 day | "Availability uncertain" + body text; already drafted in mockup |
| Velocity explainer microcopy | 0.5 day | "Sold X today — may deplete within Y hours"; needs edge-case variants (0 sold, 1 sold, etc.) |
| CTA button labels | 0.5 day | "Can't confirm — call the store", "Ping staff to check shelf", "Reserve for pickup" |
| Error / empty-state strings | 0.5 day | "Not collectable nearby" + delivery CTA copy |
| Localisation handoff | 1 day | Key strings to 4 locales (EN-GB, FR, DE, ES) |
| **Total** | **~3 days** | Part-time UX writer; most copy already drafted |

**What makes this cheap:** The verbatim disclosure is locked by AC — there is
no copy exploration cycle. The uncertainty language is deliberately plain and
direct, not marketing-polished.

---

## Expected outcome metric

> ### Cut click & collect cancellation-due-to-unavailable from 8% to < 3%
> *Measured 90 days post-launch across all stores with the freshness indicator.*

**Why 8% → <3% is realistic:**

- **Today's 8%** comes from SAP-synced stores where the binary "In stock" badge
  is stale for 15–30 minutes. High-velocity SKUs (like the Trail Runner X9,
  selling ~1/hr) are wrong ~8% of the time by the time the customer arrives.
- **Phase 0a eliminates the worst cases.** When data is >30 min stale, the
  indicator refuses to show a quantity and directs the shopper to call the
  store. A shopper who calls ahead does not make a wasted trip — they either
  confirm stock or switch stores.
- **The freshness timestamp itself changes behaviour.** A shopper who sees
  "Checked 12 min ago — 4 on shelf" at High Street versus "Last checked 47 min
  ago" at Oakfield will choose High Street. The system nudges them toward the
  store where the data is most reliable.
- **Conservative assumption.** We do not assume zero wasted trips from the fresh
  stores — the 15-minute sync gap can still produce phantom stock. But the
  stale-store fallback removes the worst cohort (data >30 min old), which
  accounts for roughly two-thirds of today's 8% cancellations. 8% × ⅓ ≈ 2.7%.
  Round down to <3% to set a forcing function.

**Measurement:**

```
Cancellation-due-to-unavailable rate =
  (orders cancelled with reason "item not on shelf" OR "shelf empty")
  / (total click & collect orders fulfilled in period)
```

Tracked weekly. Baselines from the 90 days pre-launch. Target assessed at
90 days post-launch. If <3% is not met, Phase 1 (confidence percentage model)
is accelerated.

---

## Cost-benefit summary

| Dimension | Estimate |
|-----------|----------|
| **Benefit** | Eliminates the #1 cause of click & collect disappointment — the binary "In stock" lie |
| **Engineering** | 3–4 weeks, 1 full-stack engineer |
| **Design** | 2 weeks, 1 product designer |
| **Content** | 3 days, part-time UX writer |
| **Total cost** | ~5–6 weeks elapsed (design + engineering overlapped), ~2 person-months |
| **Outcome metric** | Cut cancellation-due-to-unavailable from 8% → <3% in 90 days |
| **Risk if we don't ship** | Phantom-stock disappointment continues at 8%; trust erodes; competitors who show freshness data (none yet, but inevitable) capture the transparency advantage |
