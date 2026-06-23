# Workshop Plan v2 — Meridian Availability Freshness Indicator

**Product:** Meridian Retail Group
**Feature:** Availability Freshness Indicator (Phase 0a — click & collect)
**Date:** 2026-06-22
**Facilitator:** Product Lead + UX Researcher
**Duration:** 4 hours (recommended)
**Status:** Post-decision — workshop validates the phased approach against the
clickable prototype (`05-mockup.html`)

---

## One Decision the Workshop Must Close

> **Does the 3-screen freshness-indicator prototype (quantity + timestamp +
> uncertainty fallback) give shoppers enough information to make an informed
> store choice, or do they need the confidence percentage from Phase 1?**

**Why this is the critical v2 decision:**
Phase 0a (freshness indicator, no AI model) is the quick-win path — ships in
weeks, costs ~2 person-months, uses data we already have. Phase 1 (confidence
percentage model) depends on Phase 0b micro-survey training data and 2–4 weeks
of responses. The question is whether Phase 0a alone is *sufficient* to cut the
cancellation-due-to-unavailable rate from 8% to <3%, or whether shoppers need
the percentage to trust the indicator.

**Decision owner:** Sarah Chen, Product Lead / Head of Digital (Meridian) —
this is a scope and sequencing decision that determines whether Phase 1 is
accelerated or deferred based on Phase 0a pilot results.

**Inputs the team needs to decide:**
- Usability test results from the 3-screen prototype (05-mockup.html, 5 tasks
  in 07-validation-plan.md)
- Pilot data: did cancellation-due-to-unavailable drop below the 3% target in
  the first 30 days?
- Store operations: are staff receiving fewer "is this actually there?" calls?
- Engineering: is the SAP sync timestamp reliably propagated to the frontend?

---

## Workshop Structure

### Goals/Tasks

| Category | Item | Type | Timebox |
|---|---|---|---|
| **Must decide** | Does Phase 0a alone hit the <3% target, or accelerate Phase 1? | **Decide** | 45 min |
| **Must decide** | Staleness threshold: keep at 30 min, or tune per store? | **Decide** | 20 min |
| **Must decide** | Fallback escalation: call store → ping staff → what's the SLA? | **Decide** | 25 min |
| **Should explore** | Phase 0b micro-survey wording and placement | Explore | 20 min |
| **Should explore** | Dark-mode and narrow-viewport (320px) QA findings | Explore | 15 min |
| **Should explore** | Pilot market selection (which 2 stores first?) | Explore | 20 min |
| **Should explore** | Accessibility audit scope (screen-reader, focus order) | Explore | 15 min |

### Timeboxed Agenda

| Time | Activity | Type | Output |
|---|---|---|---|
| 0:00–0:15 | **Set-up** — walk through the 3-screen prototype live, review the phased decision from v1, present the forced outcome metric (8% → <3%) | Context | Shared mental model |
| 0:15–1:00 | **HMW + ideation** — generate HMW questions from the 5 usability-task observations (individual → cluster → vote top 3 themes) | Diverge | 10 HMW questions, 3 themes, 9 refinements |
| 1:00–1:45 | **Decision #1: Phase 0a sufficiency** — review pilot data (if available) or usability-test findings. Vote: ship Phase 0a alone vs accelerate Phase 1 | **Decide** | Recorded decision + rationale |
| 1:45–2:15 | **Decision #2 + #3: Threshold tuning + fallback SLA** — staleness threshold per store vs global; staff ping response time commitment | **Decide** | Two recorded decisions |
| 2:15–2:30 | Break | — | — |
| 2:30–3:15 | **Explore: Pilot scope + accessibility** — which stores, what success looks like at 30/60/90 days, accessibility must-haves | Explore | Pilot measurement plan + a11y checklist |
| 3:15–3:45 | **Explore: Phase 0b readiness** — micro-survey wording A/B test results, notification timing, data granularity for model training | Explore | Phase 0b spec sketch |
| 3:45–4:00 | **Close** — recap decisions, assign action items, confirm next steps (pilot launch date, usability test recruitment, a11y audit) | Close | Decision log + action items |

---

## How Might We Questions (v2)

Generated from the 3-screen prototype usability observations and journey-map
frustrations. Every HMW names a **journey step** and the **shopper's emotion**
at that moment — per the design-meridian skill rule.

### Theme A: Building Trust on the Product Page

*Journey steps: browsing → comparing stores. Emotion: cautious, uncertain.*

1. **HMW** help the shopper at the *browse-and-scan* step (😐 neutral, deciding
   where to go) distinguish a recently-checked store from a stale one at a
   glance, before they tap anything?

2. **HMW** reassure the shopper at the *compare-stores* step (🤔 weighing
   distance against reliability) that "4 units, checked 12 min ago" is more
   trustworthy than "3 units, last checked 47 min ago" without requiring them
   to do mental math?

3. **HMW** give the shopper at the *first-glance* step (😐 scanning the product
   page) an immediate sense that this store data is different from the old
   "In stock" badge — that something has changed for the better?

4. **HMW** support the shopper at the *expand-for-detail* step (🧐 curious but
   busy) so the sell-through velocity ("8 sold today") feels like helpful
   context rather than noise?

### Theme B: Handling Uncertainty Without Abandoning the Shopper

*Journey steps: tapping a stale store → seeing the warning. Emotion: anxious,
disappointed but still wanting the item.*

5. **HMW** prevent the shopper at the *tap-stale-store* step (😟 "why does this
   one look different?") from misreading the amber warning as an error — and
   instead seeing it as the system being honest?

6. **HMW** keep the shopper at the *uncertainty-reveal* step (😞 "the app won't
   even show a number") engaged and action-oriented, so they reach for "call
   the store" instead of closing the app?

7. **HMW** help the shopper at the *decide-anyway* step (🤨 "I still want these
   shoes today") weigh the cost of a call or a staff ping against the cost of
   a wasted trip, without the app feeling preachy?

### Theme C: Building Long-Term Trust Through Transparency

*Journey steps: reading the disclosure → post-collection reflection. Emotion:
sceptical → trust-building.*

8. **HMW** make the shopper at the *read-the-fine-print* step (🧐 "how does
   this even work?") discover the 15–30 minute sync window and "not guaranteed"
   caveat in a way that builds trust ("they're being straight with me") rather
   than anxiety ("so it might be wrong?")?

9. **HMW** turn the shopper's experience at the *successful-pickup* step (😊
   "it was actually there!") into reinforced trust in the freshness indicator,
   so they return to click & collect next time instead of defaulting to
   delivery?

10. **HMW** support the shopper at the *shelf-was-empty-anyway* step (😤 "I
    checked, it said 4, and there were 0") so the disappointment is directed
    at the store's inventory process rather than at the freshness indicator
    that was honest about its limits?

---

## Ideation: 3 Refinements Per Theme

*Rules: build on the existing 3-screen prototype. These are refinements and
edge-case treatments, not new features.*

### Theme A: Building Trust on the Product Page

**A1 — Stale-store card visual contrast**
Increase the visual difference between fresh and stale StoreCards. Fresh cards
use `--color-card-bg` (#f9f9fb) with `--color-card-border` (#e5e5ea). Stale
cards use `--color-stale-card-bg` (#fffbf5) with `--color-stale-border`
(#ffcc80) AND a 2px left-edge amber accent bar. The accent bar makes the stale
state scannable even if colour vision is impaired.

**A2 — "Freshest first" default sort**
Sort the store list by `lastSyncTimestamp` descending (freshest data first),
not by distance. A store 1.4 miles away with data from 8 min ago is a safer bet
than a store 0.8 miles away with data from 47 min ago. The sort order itself
teaches the shopper that freshness matters.

**A3 — Inline freshness comparison**
Add a subtle "Compared to High Street (12 min ago), Oakfield's data is 4× older"
line when the shopper views a stale store. Gives a concrete reference point
without requiring the shopper to remember the other store's timestamp.

### Theme B: Handling Uncertainty Without Abandoning the Shopper

**B1 — "Here's what to say" call script**
When the shopper taps "Can't confirm — call the store", pre-fill a calling
script: "Hi, I'm looking at the Trail Runner X9 on your website — it said stock
was last checked 47 minutes ago. Can you check the shelf for me?" Reduces the
anxiety of calling a store and not knowing what to ask.

**B2 — Staff ping estimated response time**
Replace "Ping staff to check shelf" with "Ping staff (usually responds in 5–10
min)". Sets a time expectation so the shopper isn't staring at the screen
waiting.

**B3 — "Notify me when data refreshes"**
Add a third CTA under the uncertainty banner: "Notify me when stock data
refreshes." The shopper enters their phone/email and gets a push when the next
SAP sync lands with fresh data. Captures shoppers who won't call but might
return if nudged.

### Theme C: Building Long-Term Trust Through Transparency

**C1 — Disclosure on first visit, not every visit**
Show the ⓘ disclosure panel automatically on the shopper's first visit to any
product page with the freshness indicator. On subsequent visits, keep it
collapsed. The shopper learns the caveat once; they don't need to re-read it
every time.

**C2 — "Your last pickup was accurate" reassurance**
On the next product page the shopper visits after a successful pickup, show a
subtle banner: "Your last pickup at High Street was ready when you arrived."
Reinforces the pattern: the indicator works. Builds habit.

**C3 — "We're improving" transparency**
If the shelf-was-empty-anyway case triggers (shopper arrives, item not there
despite fresh data), show a post-collection message: "We're sorry — our data
said 4 were on the shelf. We've flagged this to the store team. This helps us
get better." Turns a failure into a learning signal and acknowledges the
shopper's frustration.

---

## Summary: Workshop Canvas v2

| Section | Output |
|---|---|
| **One decision to close** | Does Phase 0a alone hit <3% or accelerate Phase 1? |
| **Decision owner** | Sarah Chen, Product Lead / Head of Digital (Meridian) |
| **Must decide** (3 items) | Phase 0a sufficiency, staleness threshold tuning, fallback SLA |
| **Should explore** (4 items) | Phase 0b readiness, dark-mode QA, pilot market, a11y audit |
| **HMW questions** | 10 questions → 3 themes (Trust / Uncertainty / Transparency) |
| **Every HMW names a journey step + emotion** | ✅ Browse-and-scan (😐), compare-stores (🤔), tap-stale-store (😟), uncertainty-reveal (😞), decide-anyway (🤨), read-the-fine-print (🧐), successful-pickup (😊), shelf-was-empty-anyway (😤) |
| **Refinements per theme** | 3 per theme = 9 prototype refinements |
| **Design tokens referenced** | `--color-card-bg`, `--color-card-border`, `--color-stale-card-bg`, `--color-stale-border` |
| **Time** | 4 hours |
| **Input artifact** | `05-mockup.html` (clickable prototype) |
