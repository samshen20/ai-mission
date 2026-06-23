# 06-spec.md — Availability Freshness Indicator (Phase 0a)

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

## Design Tokens

### Color

| Token | Value | Usage |
|-------|-------|-------|
| `--color-ink` | `#1a1a1a` | Primary text, header bg, primary button bg |
| `--color-ink-hover` | `#333333` | Button hover state |
| `--color-surface` | `#ffffff` | Phone/container background |
| `--color-page` | `#f2f2f7` | Page-level background |
| `--color-card-bg` | `#f9f9fb` | Store card, detail card background |
| `--color-card-border` | `#e5e5ea` | Card border default |
| `--color-text-body` | `#48484a` | Body copy on cards |
| `--color-text-secondary` | `#6e6e73` | Subtitle, velocity, disclosure text |
| `--color-text-tertiary` | `#8e8e93` | Info icon, disabled hints |
| `--color-text-subtle` | `#aeaeb2` | Dot separators, nav hints |
| `--color-fresh-bg` | `#e8f5e9` | Freshness badge — fresh variant background |
| `--color-fresh-text` | `#2e7d32` | Freshness badge — fresh variant text |
| `--color-fresh-velocity-bg` | `#e8f5e9` | Velocity explainer block background |
| `--color-stale-bg` | `#fff3e0` | Freshness badge — stale variant / uncertainty banner bg |
| `--color-stale-text` | `#e65100` | Freshness badge — stale variant text |
| `--color-stale-text-dark` | `#bf360c` | Uncertainty banner body text |
| `--color-stale-border` | `#ffcc80` | Stale card / uncertainty banner border |
| `--color-stale-card-bg` | `#fffbf5` | Stale store detail card background |
| `--color-disclosure-bg` | `#f5f5f7` | Disclosure panel background |
| `--color-disclosure-border` | `#e5e5ea` | Disclosure panel border |
| `--color-disabled` | `#d1d1d6` | Disabled / placeholder elements |
| `--color-hero-gradient-start` | `#e8e8ed` | Product hero gradient start |
| `--color-hero-gradient-end` | `#f5f5f8` | Product hero gradient end |

### Typography

| Token | Font | Size | Weight | Line-height | Usage |
|-------|------|------|--------|-------------|-------|
| `--text-price` | System UI | 22px | 700 | 1.3 | Product price |
| `--text-heading-lg` | System UI | 20px | 700 | 1.3 | Product name |
| `--text-heading-md` | System UI | 17px | 700 | 1.3 | Store name in detail header |
| `--text-heading-sm` | System UI | 16px | 700 | 1.3 | Section titles, uncertainty heading |
| `--text-body-lg` | System UI | 15px | 600 | 1.4 | Store name in card |
| `--text-body` | System UI | 14px | 400/600 | 1.4 | Body, quantity labels, CTAs |
| `--text-body-sm` | System UI | 13px | 400 | 1.4 | Store distance, meta rows, disclosure |
| `--text-caption` | System UI | 12px | 400/600 | 1.5 | Velocity explainer, disclosure body, nav hints |
| `--text-label-sm` | System UI | 12px | 600 | 1.3 | Freshness badge |
| `--text-label-xs` | System UI | 11px | 700 | 1.3 | Low-confidence tag (uppercase, 0.5px letter-spacing) |
| `--text-qty-xl` | System UI | 36px | 800 | 1.1 | Big quantity in detail view |

Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | Gap between badge icon and text |
| `--space-sm` | 8px | Step dots gap, inline gaps |
| `--space-md` | 12px | Header gap, CTA row gap, section internal |
| `--space-lg` | 16px | Card padding, section padding, margin between cards |
| `--space-xl` | 20px | Section padding top/bottom |
| `--space-2xl` | 24px | Product hero padding |

### Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 8px | Step dot (active) |
| `--radius-md` | 12px | Buttons, velocity block, disclosure panel |
| `--radius-lg` | 14px | Store cards |
| `--radius-xl` | 16px | Product image, detail cards, uncertainty banner |
| `--radius-pill` | 20px | Freshness badge |
| `--radius-phone` | 36px | Phone mockup container |

---

## Components

### Component 1: StoreCard

A tappable row summarising one store's availability. Appears in a vertical list
on the product page below the "Click & Collect" section heading.

**AC linkage:** Base AC1, Base AC4, AI-AC1, AI-AC2, AI-AC6

#### Variants

| Variant | Trigger | Visual difference |
|---------|---------|-------------------|
| **fresh** | `now() - last_sync ≤ 30 min` | Shows quantity ("4 units on shelf"), freshness badge (green, "● Fresh data"), "Checked X min ago" timestamp, sell-through velocity ("8 sold today"), border `--color-card-border` |
| **stale** | `now() - last_sync > 30 min` | Shows quantity with caveat ("3 units — may have changed"), freshness badge (amber, "⚠ Stale data"), "Last checked X min ago", border `--color-stale-border`, card bg `--color-stale-card-bg` |

#### States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| **default** | Data present, rendered in list | Card visible, tappable |
| **hover** | Pointer over card | Background shifts to `#f0f0f5` |
| **active/press** | Tap/click | Scale 0.985, transitions to StoreDetail screen |
| **empty** | No stores with stock in range | Card list replaced by "Not collectable nearby" + home-delivery CTA (Base AC2) |
| **omitted** | Store has null/missing/timeout data | Card not rendered (Base AC3) |

#### Structure

```
┌─────────────────────────────────────────┐
│  StoreName          ● Fresh data badge  │  ← store-header row
│  0.8 miles away                         │
│                                         │
│  4 units on shelf · Checked 12 min ago  │  ← store-meta row
│  · 8 sold today                         │
│                                         │
│  Tap for details →                      │
└─────────────────────────────────────────┘
```

#### Token references

- Background: `--color-card-bg` (fresh), `--color-stale-card-bg` (stale)
- Border: `--color-card-border` (fresh), `--color-stale-border` (stale)
- Store name: `--text-body-lg`, `--color-ink`
- Distance: `--text-body-sm`, `--color-text-secondary`
- Quantity: `--text-body` (14px), weight 700, `--color-ink` (fresh) / `--color-stale-text` (stale caveat)
- Separator dots: `--color-text-subtle`
- "Tap for details" hint: `--text-caption` (12px), `--color-text-body` (fresh) / `--color-stale-text` (stale, weight 600)
- Padding: `--space-lg` (16px)
- Radius: `--radius-lg` (14px)

---

### Component 2: StoreDetail

The expanded view shown after tapping a StoreCard. Displays full availability
information for a single store. Navigated to from the product page; back arrow
returns to the store list.

**AC linkage:** Base AC4, AI-AC1, AI-AC2, AI-AC3, AI-AC6

#### Variants

| Variant | Trigger | Key visuals |
|---------|---------|-------------|
| **fresh-detail** | Tapped a fresh StoreCard | Big quantity (36px), freshness badge, detail rows (sync source, distance, last confirmed), velocity block, "Reserve for pickup" CTA |
| **uncertainty** | Tapped a stale StoreCard | Quantity replaced by "—", UncertaintyBanner shown, Low Confidence tag, "Can't confirm — call the store" CTA, no positive affirmation |

#### States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| **fresh** | Sync age ≤ 30 min | Shows quantity, velocity block, reserve CTA |
| **uncertainty** | Sync age > 30 min | Shows UncertaintyBanner, hides quantity, shows fallback CTAs |
| **back-navigation** | User taps ← | Returns to Screen 1 (product page with store list) |

#### Structure (fresh variant)

```
┌─────────────────────────────────────────┐
│  ←  Store Availability                  │  ← header
├─────────────────────────────────────────┤
│         High Street                      │
│    0.8 miles · Open until 20:00         │  ← detail-header
├─────────────────────────────────────────┤
│  4        units on shelf                 │
│           ● Checked 12 min ago          │  ← big-freshness row
│  ─────────────────────────────────────  │
│  Store refreshes    Every 15–30 min     │
│  Sync source        SAP inventory       │  ← detail rows
│  Distance           0.8 miles           │
│  Last confirmed     10:29 AM today      │
├─────────────────────────────────────────┤
│  📊 Sold 8 today at this store           │
│     Sell-through: ~1/hr. May deplete     │  ← velocity block
│     within 4 hours.                      │
├─────────────────────────────────────────┤
│  [Check other stores] [Reserve for pickup]│ ← CTA row
│  On-shelf availability is not guaranteed. │
└─────────────────────────────────────────┘
```

#### Structure (uncertainty variant)

```
┌─────────────────────────────────────────┐
│  ←  Store Availability                  │
├─────────────────────────────────────────┤
│     Oakfield Retail Park                 │
│    2.1 miles · Open until 19:00         │
├─────────────────────────────────────────┤
│  ⚠️                                      │
│  ⚠ LOW CONFIDENCE                       │  ← UncertaintyBanner
│  Availability uncertain                  │
│  Stock data hasn't been refreshed in     │
│  47 minutes. The quantity may no longer  │
│  reflect the shelf.                      │
├─────────────────────────────────────────┤
│  —        Quantity not shown             │
│           ⚠ Last checked >30 min ago    │  ← stale detail card
│  ─────────────────────────────────────  │
│  Data status    Stale — may have changed│
│  Last confirmed 9:54 AM today           │
│  Sync source    SAP inventory (batch)   │
│  Distance       2.1 miles               │
├─────────────────────────────────────────┤
│  [📞 Can't confirm — call the store]     │  ← fallback CTA
│  [Ping staff to check shelf]            │
│  [← View other stores]                  │
├─────────────────────────────────────────┤
│  Why don't I see a quantity?             │
│  Stock data refreshes every 15–30 min.   │  ← disclosure
│  When >30 min old, quantity could be     │
│  wrong — so we don't show it.            │
└─────────────────────────────────────────┘
```

#### Token references

- Detail header bg: `--color-ink`
- Detail header text: `--color-surface`
- Big quantity: `--text-qty-xl`, `--color-ink` (fresh) / `--color-stale-text` (uncertainty)
- Detail row label: `--text-body` (14px), `--color-text-secondary`
- Detail row value: `--text-body` (14px), weight 600, `--color-ink`
- Divider: 1px `--color-card-border`
- Card bg: `--color-card-bg` (fresh), `--color-stale-card-bg` (uncertainty)
- Card border: `--color-card-border` (fresh), `--color-stale-border` (uncertainty)
- Padding: `--space-lg` (16px) / `--space-xl` (20px)
- Radius: `--radius-xl` (16px) for cards, `--radius-md` (12px) for velocity/CTAs

---

### Sub-component: FreshnessBadge

Inline pill indicating data age. Used inside StoreCard and StoreDetail.

| Variant | Token: bg | Token: text | Icon | Label |
|---------|-----------|-------------|------|-------|
| **fresh** | `--color-fresh-bg` | `--color-fresh-text` | ● | "Fresh data" or "Checked X min ago" |
| **stale** | `--color-stale-bg` | `--color-stale-text` | ⚠ | "Stale data" or "Last checked >30 min ago" |

Typography: `--text-label-sm` (12px, weight 600). Radius: `--radius-pill` (20px).
Padding: 3px 10px.

### Sub-component: UncertaintyBanner

Full-width amber banner shown at top of StoreDetail when sync is stale.
Only rendered in the **uncertainty** variant.

- Background: `--color-stale-bg`
- Border: 1.5px `--color-stale-border`
- Icon: ⚠️ (36px)
- Low Confidence tag: `--text-label-xs` (11px, weight 700, uppercase, 0.5px letter-spacing), `--color-stale-text`, border `--color-stale-border`
- Heading: `--text-heading-sm` (16px, weight 700), `--color-stale-text`
- Body: `--text-body-sm` (13px), `--color-stale-text-dark`
- Radius: `--radius-xl` (16px)
- Margin: `--space-lg` (16px)

### Sub-component: DisclosurePanel

Expandable info panel explaining how availability is calculated.
Toggled by tapping the ⓘ icon next to the "Click & Collect" section title.

- **Collapsed state:** Hidden (`display: none`)
- **Expanded state:** Visible below section title, above store cards
- Background: `--color-disclosure-bg`
- Border: 1px `--color-disclosure-border`
- Text: `--text-caption` (12px), `--color-text-secondary`, line-height 1.5
- Strong text: `--color-text-body`
- Radius: `--radius-md` (12px)
- Padding: 14px 16px

**Visual gate:** The text must match the verbatim string from AI-AC4.
Any deviation, addition, or omission is a failure.

### Sub-component: VelocityBlock

Explanatory block showing sell-through rate. Only rendered in the **fresh**
variant of StoreDetail.

- Background: `--color-fresh-velocity-bg`
- Text: `--text-caption` (12px/13px), `--color-fresh-text`
- Icon: 📊 (20px)
- Radius: `--radius-md` (12px)
- Padding: 14px 16px

---

## Refined AI-ACs (3 of 6, design-specific)

Each refined AC maps to the 6-slot template:
**Component · Variant · Color token · Typography · Placement · Visual gate**

---

### AI-AC1 (confidence) — Refined

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

| Slot | Value |
|------|-------|
| **Component** | `FreshnessIndicator` (comprises FreshnessBadge + quantity label + timestamp) |
| **Variant** | `fresh` (sync age ≤ 30 min) / `stale` (sync age > 30 min) |
| **Color token** | Fresh: `--color-fresh-bg` / `--color-fresh-text`. Stale: `--color-stale-bg` / `--color-stale-text` |
| **Typography** | Badge: `--text-label-sm` (12px, 600). Quantity: `--text-body` (14px, 700). Timestamp: `--text-body-sm` (13px, 400) |
| **Placement** | Inline in StoreCard `store-meta` row; right-aligned badge in `store-header` row. In StoreDetail: left-aligned in `big-freshness` row alongside big quantity |
| **Visual gate** | `now() - sap_sync_ts ≤ 30 min` → show quantity + "Checked X min ago". `> 30 min` → hide quantity, show staleness text + CTA. **The displayed timestamp must be the SAP sync timestamp, not page-load time** (AI-AC3) |

---

### AI-AC2 (refusal/fallback) — Refined

```
GIVEN the AI freshness layer cannot determine availability
     (stock data is stale beyond threshold OR sync is absent)
 WHEN the shopper views the store's availability indicator
 THEN the indicator shows "Availability uncertain" in amber/neutral styling
      AND displays a "Check current availability" button that triggers a
      real-time staff ping, AND does NOT show a positive green badge.
```

| Slot | Value |
|------|-------|
| **Component** | `UncertaintyBanner` + `StoreDetail` (uncertainty variant) |
| **Variant** | `uncertainty` (sync age > 30 min OR sync absent) |
| **Color token** | Banner bg: `--color-stale-bg`. Border: `--color-stale-border`. Heading: `--color-stale-text`. Body: `--color-stale-text-dark`. Low Confidence tag: `--color-stale-text` on `--color-stale-bg`. Detail card bg: `--color-stale-card-bg` |
| **Typography** | Heading: `--text-heading-sm` (16px, 700). Body: `--text-body-sm` (13px, 400). Low Confidence tag: `--text-label-xs` (11px, 700, uppercase, 0.5px letter-spacing) |
| **Placement** | Full-width banner at top of StoreDetail screen, above the stale detail card. CTAs stacked below the detail card in priority order: (1) "Can't confirm — call the store", (2) "Ping staff to check shelf", (3) "View other stores" |
| **Visual gate** | Quantity must be rendered as "—" (not a number). "Availability uncertain" heading must appear. Low Confidence tag must be visible. No green, no `--color-fresh-*` tokens. No positive-affirmation strings (AI-AC6). Amber/neutral only |

---

### AI-AC4 (disclosure) — Refined

```
GIVEN the availability indicator is visible on the product page
 WHEN the shopper taps or hovers the info icon ("ⓘ" or "How is this calculated?")
 THEN a disclosure panel appears stating, verbatim:
      "Stock data refreshes from store systems every 15–30 minutes.
       Quantities may change between refreshes. On-shelf availability
       is not guaranteed. Contact the store to confirm."
     AND no additional claims about accuracy or guarantees appear.
```

| Slot | Value |
|------|-------|
| **Component** | `DisclosurePanel` |
| **Variant** | `collapsed` (default, `display: none`) / `expanded` (on ⓘ tap, `display: block`) |
| **Color token** | Bg: `--color-disclosure-bg`. Border: `--color-disclosure-border`. Text: `--color-text-secondary`. Strong text: `--color-text-body` |
| **Typography** | `--text-caption` (12px, 400, line-height 1.5). Strong label: weight 600 |
| **Placement** | Below "Click & Collect" section title, above the first StoreCard. Toggled by the ⓘ icon (18px circle, `--color-text-tertiary` border, inline-flex next to section title) |
| **Visual gate** | **Verbatim text match required.** Rendered string must equal: "Stock data refreshes from store systems every 15–30 minutes. Quantities may change between refreshes. On-shelf availability is not guaranteed. Contact the store to confirm." Any addition, omission, rewording, or marketing gloss is a failure. No "95% accurate" claims permitted since Phase 0a has no model backing |

---

## Negative AC Carried Forward (AI-AC6)

```
GIVEN any state of the system (fresh data, stale data, missing data, API failure)
 WHEN the availability indicator is displayed
 THEN the page must NOT show any of the following strings:
      "In stock", "Available", "In Stock", "Available for Click & Collect",
      green checkmark, or any binary positive-affirmation pattern
      suggesting a guarantee of shelf presence.
```

**Enforcement in this spec:**

| Forbidden | Where enforced | How |
|-----------|---------------|-----|
| "In stock" / "In Stock" | All components, all states | Not present in any mockup label, AC text, or design token usage |
| "Available" / "Available for Click & Collect" | All components, all states | Section heading is "Click & Collect" (no "Available" qualifier). Store status uses quantity + timestamp, never "Available" |
| Green checkmark (✅ / ✔ / 🟢) | FreshnessBadge, StoreCard, StoreDetail | Fresh variant uses ● (dot) + "Fresh data" text on `--color-fresh-bg`. No checkmark shape |
| Binary positive-affirmation pattern | StoreDetail CTA area | CTA is "Reserve for pickup" (action), not "In stock — collect today" (guarantee). Footer disclaimer: "On-shelf availability is not guaranteed" |

---

## Asset & Data References

| Asset | Reference | Resolvable? |
|-------|-----------|-------------|
| Product image | `🏃` emoji placeholder → replace with real SKU image URL from PIM | Yes — PIM CDN URL pattern: `https://cdn.meridian.com/pim/<sku>/hero-2x.jpg` |
| Info icon (ⓘ) | Unicode `U+24D8` → replace with SVG icon from design system ("info-circle", 18px) | Yes — design system icon set, path `icons/info-circle.svg` |
| Back arrow (←) | Unicode `U+2190` → replace with SVG icon ("chevron-left", 22px) | Yes — design system icon set |
| Warning icon (⚠️) | Emoji → replace with SVG icon ("alert-triangle", 36px) | Yes — design system icon set |
| Phone icon (📞) | Emoji in CTA → replace with SVG icon ("phone", 16px) inline in button | Yes — design system icon set |
| Chart icon (📊) | Emoji in VelocityBlock → replace with SVG icon ("trending-up", 20px) | Yes — design system icon set |
| Store stock data | API endpoint: `GET /api/stores/{storeId}/availability/{sku}` | Yes — response shape: `{ storeId, sku, qtyOnShelf, sellThroughToday, lastSyncTimestamp, distance }` |
| SAP sync timestamp | Field `lastSyncTimestamp` in API response (ISO 8601, UTC) | Yes — propagated from SAP batch, NOT client-generated |
| Staleness threshold | Config value `STALENESS_THRESHOLD_MINUTES` (default 30) | Yes — remote-config key, overridable per store/region |

---

## Screen Flow

```
Screen 1: Product Page
  ├─ ProductHero (image, name, price)
  ├─ "Click & Collect" section title + ⓘ → DisclosurePanel (toggle)
  ├─ StoreCard (fresh) × N
  ├─ StoreCard (stale) × M   ← amber border, "⚠ Stale data"
  └─ "Not collectable nearby" fallback (if no stores)
        │
        │ tap any StoreCard
        ▼
Screen 2 or 3: StoreDetail
  ├─ sync age ≤ 30 min → fresh-detail variant
  │   ├─ Big quantity (36px)
  │   ├─ FreshnessBadge (fresh)
  │   ├─ Detail rows (refresh cadence, sync source, distance, confirmed time)
  │   ├─ VelocityBlock (sell-through rate + depletion estimate)
  │   └─ CTA: "Reserve for pickup" / "Check other stores"
  │
  └─ sync age > 30 min → uncertainty variant
      ├─ UncertaintyBanner (⚠️ + Low Confidence tag + "Availability uncertain")
      ├─ Stale detail card (quantity "—", "Last checked >30 min ago")
      ├─ CTA: "📞 Can't confirm — call the store"
      ├─ CTA: "Ping staff to check shelf"
      └─ Disclosure: "Why don't I see a quantity?"
```

---

## Definition of Handoff Done — Self-Check

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | User story + base AC present | ✅ | User story in §1; Base AC1–AC4 in §2 (verbatim from 04-ai-ac.md) |
| 2 | ≥ 3 AI-AC refined to component / variant / token / placement / visual gate | ✅ | AI-AC1, AI-AC2, AI-AC4 each refined to full 6-slot template in §4 |
| 3 | CONTEXT.md covers feature + audience + environment + constraints + out-of-scope | ✅ | `06-context.md` covers all 6 slots |
| 4 | SPEC.md lists ≥ 2 components with states + token references | ✅ | StoreCard (5 states, 2 variants) + StoreDetail (2 variants, 3 states) + 4 sub-components; all reference named design tokens |
| 5 | Asset / data reference explicit and resolvable | ✅ | 8 asset references with resolution paths; API response shape specified; SAP timestamp field named |
| 6 | Negative AC ("must NOT") carried into SPEC.md | ✅ | AI-AC6 reproduced verbatim in §5 with enforcement table mapping each forbidden string to where it's prevented |
