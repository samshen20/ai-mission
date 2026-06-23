# Heuristic Evaluation — Click & Collect Availability UX (5 Retailers)

**Product:** Meridian Retail Group
**Feature:** AI availability assistant (competitor UX baseline)
**Date:** 2026-06-18
**Method:** Nielsen's 10 usability heuristics applied to real omnichannel retail product pages

---

## Screens Analysed

| # | Retailer | Screen | Key UX pattern | Known phantom stock issue? |
|---|---|---|---|---|
| 1 | **Argos** (UK) | Product detail page — store stock grid | "Check stock at nearby stores" — tabular grid of stores + stock level labels ("In stock", "Limited availability", "Check stock") | Yes — "Limited availability" is vague; stock counts are based on batch sync, not real-time |
| 2 | **Target** (US) | Product detail page — pickup card | "Pick up today" badge + store selector + time estimate ("Usually ready in 2 hours") | Yes — "Usually ready" masks variance; popular items sell out within the window |
| 3 | **Walmart** (US) | Product detail page — pickup badge | "Free pickup today" — store picker + "Add to cart" for pickup | Yes — stock status lags behind actual shelf availability during high-traffic periods |
| 4 | **John Lewis** (UK) | Product detail page — C&C availability | "Check availability" CTA → modal with store list + "Collect from [store]" | Yes — modal does not show when stock was last checked |
| 5 | **Tesco** (UK) | Grocery slot booking — click & collect | Time-slot grid for C&C delivery → substitution-heavy on fresh items | Yes — substitutions and out-of-stocks are common but managed as expected (slot, not stock) |

---

## Violations by Heuristic

### H1: Visibility of system status ❌ 5/5 retailers violate

**Heuristic:** The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | Product page shows "In stock" with no timestamp — the shopper cannot tell if this was checked 5 minutes ago or yesterday. The stock grid lists store names and quantities ("2+") but no "last updated" column. When stock is stale, the shopper has no way to know. | 🔴 High |
| **Target** | "Usually ready in 2 hours" — the "usually" is doing important work but the threshold isn't shown. Is it 90% of the time or 60%? When a shopper arrives after 2 hours and the item isn't ready, the system offers no explanation of what went wrong. | 🟡 Medium |
| **Walmart** | After selecting a store, the product page shows "Pickup today" without confirming that the specific item is actually allocated to that order. The shopper only discovers a problem post-payment during the picking phase. | 🔴 High |
| **John Lewis** | The store availability modal shows stock status per store but does not display when the data was last synchronised. The shopper sees "Available" or "Low stock" with no temporal context. | 🟡 Medium |
| **Tesco** | Slot booking shows available time windows but the actual stock of specific items is opaque until the picker assembles the order. Substitutions happen without real-time feedback during booking. | 🟡 Medium |

**Common pattern:** Every retailer shows availability as a static state ("In stock" / "Available") rather than a time-aware estimate. None communicate staleness. None reveal confidence.

---

### H2: Match between system and real world ❌ 4/5 retailers violate

**Heuristic:** The system should speak the users' language, with familiar concepts rather than system-oriented terms.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | "2+ in stock" at store level — the "+" is inventory-system jargon. A shopper reading "2+" interprets as "plenty available" when it could mean "exactly 2 (which may be on the wrong shelf or damaged)." | 🟡 Medium |
| **Target** | "Usually ready in 2 hours" — the shopper interprets "usually" as "almost always" but Target may define it at 70% fulfilment. The gap between shopper expectation and system definition creates phantom stock frustration. | 🟡 Medium |
| **Walmart** | "Free pickup today" — the shopper reads "today" as "right now" or "within an hour." Walmart's operational definition is "by end of day." The mismatch causes frustrated shoppers who arrive within 1 hour expecting an item that hasn't been picked yet. | 🔴 High |
| **John Lewis** | "Check availability" CTA → modal lists stores with "Available" label. The shopper assumes "Available" means a reserved item or at least a guaranteed one. In reality, it means "the system thinks it might be there." | 🟡 Medium |
| **Tesco** | Slot-booking flow: the concept of a "1-hour collection window" maps cleanly to the shopper's mental model. Less problematic here because the model is time-slot-based, not stock-count-based. | ✅ Pass |

**Common pattern:** Retailers use everyday words ("available", "usually", "today") with system-internal definitions that differ from shopper expectations. The gap is invisible until the shopper acts on it.

---

### H3: User control and freedom ❌ 3/5 retailers violate

**Heuristic:** Users should be free to select, undo, and redo actions. Support emergency exits.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | Once an item is ordered for click & collect, there is no way for the shopper to check live stock status before travelling. The order confirmation is the last communication until they arrive. No "check before you go" option. | 🟡 Medium |
| **Walmart** | After the pickup order is placed, the shopper cannot easily switch the fulfilment method (pickup → delivery) without cancelling and reordering. The "Manage order" page is limited to cancellation or address changes for delivery. | 🟡 Medium |
| **John Lewis** | The "Check availability" modal offers no way to save a store preference or get notified if stock changes. Each visit requires re-checking every store. No "notify me when in stock at my store" for C&C. | 🟡 Low |
| **Target** | Shopper can switch store after ordering (via "Change store" in order management) — partial control. | ✅ Pass |
| **Tesco** | Click & collect slot can be modified or cancelled before the picking window opens. Full control. | ✅ Pass |

**Common pattern:** Once the C&C order is placed, the shopper loses visibility and control. They cannot check stock freshness, switch fulfilment mode, or get proactive updates. The journey becomes "order → trust the system → arrive → hope."

---

### H4: Consistency and standards ❌ 2/5 retailers violate

**Heuristic:** Users should not have to wonder whether different words, situations, or actions mean the same thing.

| Retailer | Violation | Severity |
|---|---|---|
| **Walmart** | "Free pickup today" appears on the product page, but the same item may show "Pickup not available" on the store-specific page with no explanation of why. Inconsistent messaging erodes trust. | 🟡 Medium |
| **Tesco** | The substitution and out-of-stock communication differs between the website (opaque — you don't know until the slot is picked) and the app (slightly more transparent — substitutions shown at pick time). Inconsistent channel experience. | 🟡 Low |
| **Argos** | Stock labels are consistent across products ("In stock", "Limited availability", "Check stock"). The pattern is standardised — problem is the staleness, not the consistency. | ✅ Pass |
| **Target** | "Pick up today" / "Pick up in 2 hours" / "Usually ready in 2 hours" all appear on different products for the same store with unclear differentiation. | 🟡 Medium |
| **John Lewis** | "Available" + "Low stock" + "Check stock" pattern is consistent across product pages. | ✅ Pass |

---

### H5: Error prevention ❌ 5/5 retailers violate

**Heuristic:** Even better than good error messages is a careful design that prevents a problem from occurring in the first place.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | The core error vector is the system itself: showing "In stock" when the shelf is empty is a failure of error prevention. No buffer, no confidence estimate, no caveat. The error is designed into the feature. | 🔴 Critical |
| **Target** | "Usually ready in 2 hours" does not prevent the shopper from arriving early (before 2 hours) and finding the item unpicked. No "wait before you go" guidance or real-time picking status. | 🔴 High |
| **Walmart** | Same as Argos — the system shows stock that may not exist. No mechanism to hold inventory at the moment the order is placed (no reservation). Error is inevitable in high-traffic periods. | 🔴 Critical |
| **John Lewis** | No item reservation on C&C orders — stock can be sold to an in-store customer between the online check and the shopper's arrival. The system does not prevent this conflict. | 🔴 High |
| **Tesco** | Substitutions are by design (fresh items cannot be held). The system prevents the phantom stock error for ambient goods but accepts it for fresh/cold lines. | 🟡 Medium |

**Common pattern:** **None of the five retailers reserve inventory at the moment of C&C order placement.** This is the structural root cause of phantom stock. The product page shows availability based on the last batch sync, but no inventory is held until the picker physically collects the item (hours later). In that window, any in-store customer can buy the same item. The system designs the error in rather than preventing it.

---

### H6: Recognition rather than recall ❌ 3/5 retailers violate

**Heuristic:** Minimize the user's memory load by making objects, actions, and options visible.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | The store stock grid lists stores by distance, but the shopper must remember which store they usually use — no "favourite stores" or recent-store recognition. | 🟡 Low |
| **Walmart** | Once a store is selected and the product page refreshes, the stock status is shown but the selected store name is small/dimmed — easy to forget which store you're looking at if you browse away. | 🟡 Low |
| **John Lewis** | The availability modal requires re-entering the postcode or location on each visit. No store preference persistence across sessions for C&C. | 🟡 Low |
| **Target** | Selected store is prominent in the header bar — recognises the shopper's preference across sessions. | ✅ Pass |
| **Tesco** | Delivery slot and store preference persist in the account profile. | ✅ Pass |

---

### H7: Flexibility and efficiency of use ❌ 2/5 retailers violate

**Heuristic:** Accelerators — unseen by the novice user — may speed up interaction for the expert user.

| Retailer | Violation | Severity |
|---|---|---|
| **John Lewis** | No "notify me when available at my store" option for C&C. The power user has to manually check availability per product per store. | 🟡 Medium |
| **Argos** | Frequent C&C users cannot set a default store or save a favourites list. Each session starts from scratch on the store selector. | 🟡 Low |
| **Target** | "Pick up today" products can be filtered and sorted in search results — efficiency for regular shoppers. | ✅ Pass |
| **Walmart** | Recent stores appear at the top of the store picker — moderate efficiency gain. | ✅ Pass |
| **Tesco** | Saved slot preferences and favourite stores are in the account — good efficiency for repeat shoppers. | ✅ Pass |

---

### H8: Aesthetic and minimalist design ✅ 4/5 retailers pass

**Heuristic:** Dialogues should not contain irrelevant or rarely needed information.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | Stock grid shows all nearby stores at once — information-dense but scannable. The "2+" label is minimalist but misleading (see H2). | 🟡 Low |
| **Target** | Pickup card is clean: one badge, one store line, one time estimate. Minimalist by design. | ✅ Pass |
| **Walmart** | Pickup badge is clean. Some product pages have conflicting CTAs ("Add to cart" vs "Pickup" vs "Delivery") that create visual noise. | 🟡 Low |
| **John Lewis** | Availability modal is clean — store list with status labels. No clutter. | ✅ Pass |
| **Tesco** | Slot-booking grid is clean and task-focused. | ✅ Pass |

---

### H9: Help users recognise, diagnose, and recover from errors ❌ 5/5 retailers violate

**Heuristic:** Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.

| Retailer | Violation | Severity |
|---|---|---|
| **Argos** | When a shopper arrives and the item isn't there, there is no system-level error handling — it's a human interaction at the service desk. The system does not help staff diagnose the discrepancy (no audit trail of when "In stock" was shown). The shopper gets "Sorry, the system must have been wrong" — no constructive path to resolution beyond refund. | 🔴 High |
| **Target** | If the item isn't ready after "usually 2 hours," the shopper can contact customer service, but the system provides no explanation of the delay or an updated estimate. The error recovery is entirely manual. | 🟡 Medium |
| **Walmart** | Same pattern — no system-level error recovery. The pickup associate can offer a substitute or refund, but the system does not suggest alternatives based on what the shopper ordered. | 🟡 Medium |
| **John Lewis** | No mechanism to proactively notify the shopper of a stock issue before they travel. The error is discovered at the store, not prevented or recovered digitally. | 🔴 High |
| **Tesco** | Substitutions are surfaced at pick time via app notification — partial recovery. The system tells you what changed before you collect. This is the best recovery behaviour of the five, but only applies to grocery allocation, not hardlines C&C. | 🟡 Low |

**Common pattern:** When phantom stock occurs, **zero of the five retailers use their digital channel to help the shopper recover.** The error is always discovered physically (at the store), after the wasted trip. No real-time notification, no proactive substitute suggestion, no "we'll hold it at another store" workflow. The recovery is entirely staff-mediated, inconsistent, and unfriendly.

---

### H10: Help and documentation ✅ 5/5 retailers pass (mostly)

**Heuristic:** Provide help and documentation that can be easily searched and focused on the user's task.

| Retailer | Violation | Severity |
|---|---|---|
| **All 5** | All have help centre articles explaining click & collect in general terms. None explain what "stock status" means operationally (e.g., "In stock means the system believes it's on the shelf — it's not reserved until we pick it"). This is honesty that would set expectations, but no retailer provides it. | 🟡 Low |

---

## Summary — Violations Count by Retailer

| Heuristic | Argos | Target | Walmart | John Lewis | Tesco |
|---|---|---|---|---|---|
| H1 — Visibility | 🔴 H | 🟡 M | 🔴 H | 🟡 M | 🟡 M |
| H2 — Real world match | 🟡 M | 🟡 M | 🔴 H | 🟡 M | ✅ |
| H3 — User control | 🟡 M | ✅ | 🟡 M | 🟡 L | ✅ |
| H4 — Consistency | ✅ | 🟡 M | 🟡 M | ✅ | 🟡 L |
| H5 — Error prevention | 🔴 C | 🔴 H | 🔴 C | 🔴 H | 🟡 M |
| H6 — Recognition | 🟡 L | ✅ | 🟡 L | 🟡 L | ✅ |
| H7 — Flexibility | 🟡 L | ✅ | ✅ | 🟡 M | ✅ |
| H8 — Minimalist | 🟡 L | ✅ | 🟡 L | ✅ | ✅ |
| H9 — Error recovery | 🔴 H | 🟡 M | 🟡 M | 🔴 H | 🟡 L |
| H10 — Help | 🟡 L | 🟡 L | 🟡 L | 🟡 L | 🟡 L |

**Severity key:** C = Critical, H = High, M = Medium, L = Low

---

## Key Findings for Meridian's AI Assistant

### Finding 1: The most violated heuristic (H5 — Error prevention) is the AI assistant's primary job.

Every single retailer fails at error prevention for phantom stock. The structural root cause is **no inventory reservation at order placement** — the product page shows availability from a batch sync, but no stock is held until a human physically picks the item hours later. The AI assistant cannot fix the reservation gap (that's an ERP/process change), but it can **prevent the error from reaching the shopper** by replacing the binary "In stock" with a confidence estimate that accounts for the staleness window. This is the single highest-impact change Meridian can make.

### Finding 2: Every retailer violates H1 (Visibility) in the same way — no timestamp, no staleness indicator.

Not one of the five retailers shows *when* availability was last checked on the product page. This is a trivial UI change (add "Checked 12 min ago" text) that no retailer implements. For Meridian's AI assistant, the confidence estimate inherently includes a staleness signal — "85% likely available (last checked 18 min ago)" — which directly addresses H1 where every competitor fails.

### Finding 3: H9 (Error recovery) is uniformly poor — an opportunity for proactive digital recovery.

No retailer proactively notifies the shopper of phantom stock before they travel. Meridian's AI assistant, combined with real-time store-level data, could detect when a pick attempt fails and notify the shopper before they leave home — offering a substitute, an alternative store, or a delivery re-route. This turns a 1-on-1 customer reaction into a 1-on-5 proactive recovery, which none of the competitors assessed currently offer.

### Finding 4: Label language (H2) is a low-effort, high-impact fix.

"We estimate this item is available at your store [confidence]%" is clearer than "In stock" or "Available." Every retailer uses inventory-system labels that overpromise. The AI assistant's confidence framing sets calibrated expectations — even when stock is wrong, the disappointment is contained because the shopper knew the risk.

### Priority action list for Meridian

| Priority | Fix | Heuristic | Effort | Impact |
|---|---|---|---|---|
| P0 | Replace binary "In stock" with confidence estimate + timestamp | H1, H2, H5 | Medium | Critical |
| P1 | Add proactive error recovery — notify shopper before travel if stock drops | H3, H9 | High | High |
| P2 | Add inventory reservation at order placement (ERP change) | H5 | High | Critical |
| P3 | Standardise label language across all surfaces | H2, H4 | Low | Medium |
| P4 | Persist store preference and add "notify me" for C&C | H3, H6, H7 | Low | Medium |
