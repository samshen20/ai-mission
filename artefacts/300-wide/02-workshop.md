# Workshop Plan — Meridian Availability Assistant

**Product:** Meridian Retail Group
**Feature:** AI availability assistant (click & collect phantom stock estimator)
**Date:** 2026-06-18
**Facilitator:** Product lead + UX researcher
**Duration:** 4 hours (recommended)

---

## One Decision the Workshop Must Close

> **Do we show estimated availability with a confidence cue (e.g., "67% likely in stock — checked 12 min ago"), or do we hide the estimate and only show a binary signal after a store staff member confirms the item via handheld?**

**Why this is the critical decision:**
- Showing the confidence estimate (the v2 journey path) enables calibrated expectations, pre-trip re-checks, and proactive error recovery — but requires the shopper to interpret a probabilistic number. Some users may find 67% confusing or anxiety-inducing.
- Hiding the estimate and showing only a confirmed binary signal ("Available — confirmed by staff") is simpler UX but removes the pre-trip calibration benefit. If the confirm ping fails, the shopper sees nothing at all — returning to the current opacity problem.
- This decision cascades into everything: the UI pattern for the product page, whether we need a "check before you go" button, how staff handheld tasks are prioritised, the notification flow for recovery, and the error messaging when stock can't be confirmed.

**Decision owner:** Product Lead / Head of Digital (Meridian) — this is a customer-facing UX decision with operational (staff workflow) and technical (real-time ping infrastructure) dependencies. Engineering, Store Operations, and Legal must provide input, but Product owns the call.

**Inputs the team needs to decide:**
- UX research (prototype test: do shoppers understand "67% likely in stock"?)
- Store operations (can staff handle real-time confirmation pings at volume?)
- Engineering (what's the latency ceiling for the confirm ping workflow?)
- Legal (does a confidence estimate constitute a "guarantee" from a liability standpoint?)

---

## Workshop Structure

### Goals/Tasks

| Category | Item | Type (Decide / Explore) | Timebox |
|---|---|---|---|
| **Must decide** | Confidence display: show estimate vs hide until confirmed | **Decide** | 45 min |
| **Must decide** | Fallback behaviour when store can't confirm (what the shopper sees) | **Decide** | 30 min |
| **Must decide** | Hold duration policy (how long staff hold confirmed items — 1h / 2h / 4h?) | **Decide** | 20 min |
| **Must decide** | Error bias: favour false negatives or false positives in the confidence model? | **Decide** | 15 min |
| **Should explore** | Implementation phasing (MVP scope vs v2 deferred features) | **Explore** | 30 min |
| **Should explore** | Staff handheld workflow changes (confirmation ping → hold → release) | **Explore** | 25 min |
| **Should explore** | How the confidence model learns from post-collection feedback ("did you find it?") | **Explore** | 20 min |
| **Should explore** | Legal and compliance review timeline (EU AI Act classification letter) | **Explore** | 10 min |
| **Should explore** | Success metrics for pilot (what we measure in the first 2 markets) | **Explore** | 25 min |

### Timeboxed Agenda

| Time | Activity | Type | Output |
|---|---|---|---|
| 0:00–0:15 | **Set-up** — problem brief, journey map walkthrough, the one decision | Context | Shared mental model |
| 0:15–1:00 | **HMW + ideation** — generate HMW questions from frustrations (individual → cluster → vote top 3 themes) | Diverge | 10 HMW questions, 3 themes, 9 solution sketches |
| 1:00–1:45 | **Decision #1: Confidence display approach** — present UX prototype options, staff ops input, engineering constraints. Vote: show estimate vs hide until confirmed | **Decide** | Recorded decision + rationale |
| 1:45–2:15 | **Decision #2 + #3: Fallback + hold policy** — what the shopper sees when ping fails; how long items are held | **Decide** | Two recorded decisions |
| 2:15–2:30 | Break | — | — |
| 2:30–3:15 | **Explore: Implementation phasing** — what ships in MVP, what defers to v2. Staff workflow impact mapping | Explore | MVP scope sketch + deferred backlog |
| 3:15–3:45 | **Explore: Success metrics for pilot** — what we measure, what success looks like, pilot duration | Explore | Pilot measurement plan |
| 3:45–4:00 | **Close** — recap decisions, assign action items, confirm next steps (legal opinion, prototype testing, staff ops deep-dive) | Close | Decision log + action items |

---

## How Might We Questions

Generated from journey map frustrations (v1 current state + v2 recovery gaps). 10 questions, clustered into 3 themes.

### Theme A: Building Trust Before the Trip

*Frustration sources: no timestamp, binary "in stock" overpromises, no pre-trip verification, vague language.*

1. **HMW** show the shopper how *fresh* the availability data is, so they can gauge reliability before acting?
2. **HMW** communicate availability as an estimate rather than a guarantee, so expectations are calibrated and disappointment is contained?
3. **HMW** let the shopper verify stock in real time before they leave home, so they never arrive at an empty shelf?
4. **HMW** surface *why* the estimate is what it is ("sold 8 units today"), so the shopper trusts the number rather than treating it as a black box?

### Theme B: Confident Recovery When Stock Fails

*Frustration sources: no error recovery, staff can't find items, no proactive notification, post-failure resolution is purely manual.*

5. **HMW** detect a stock failure before the shopper leaves home, so they never travel for nothing?
6. **HMW** proactively offer an alternative (other store, delivery, substitute) when the first choice fails, so the shopper has a next step instead of a dead end?
7. **HMW** give store staff better data about what was promised to the shopper, so they can diagnose and fix stock discrepancies faster?

### Theme C: Closing the Loop — Learning & Holding

*Frustration sources: no reservation at order placement, channel inconsistency, no feedback loop.*

8. **HMW** create a lightweight "hold" workflow (staff → handheld → confirm → keep aside) that doesn't increase store labour costs?
9. **HMW** close the feedback loop ("did you find it?") so the confidence model improves per store per SKU over time?
10. **HMW** keep the experience consistent across web, app, and in-store touchpoints, so the shopper never gets conflicting information?

---

## Ideation: 3 Solutions Per Theme

*Rules: diverge, capture everything, judge nothing yet. These are raw ideas — feasibility comes later.*

### Theme A: Building Trust Before the Trip

**A1 — Confidence meter with freshness indicator**
On the product page, replace the "Available for Click & Collect" badge with a confidence meter (0–4 segments filled) + "Checked X min ago." Colour-coded: green (≥3 segments filled), amber (2), grey (≤1). Tapping expands to show the estimate as a percentage and a one-line explainer ("Sold 8 units today — stock is moving fast"). No real-time ping needed — uses batch data + sell-through velocity.

**A2 — "Reserve & Check" dual throttle**
Two buttons on the product page: "**Reserve now**" (places order immediately, triggers staff confirm in background — shopper gets notified within 10 min) and "**Check first**" (sends real-time ping to store handheld — staff responds yes/no within 2 min — shopper decides after response). "Reserve now" is for confident shoppers; "Check first" is for risk-averse shoppers. Both paths eventually converge on the same hold workflow.

**A3 — Explainable AI label**
Instead of a single number, show a 2-line summary: "**High demand:** 8 sold here today. **Checked 12 min ago:** 4 remaining at High Street." No percentage — just the data points that feed the model. The shopper makes their own judgment from transparent signals. Works best for analytically-minded shoppers; may overwhelm less engaged users.

### Theme B: Confident Recovery When Stock Fails

**B1 — Proactive re-route notification**
When the store staff fails to confirm the item (can't find it, system says 0), the system automatically: (a) checks the next nearest store for availability, (b) sends a push notification: "High Street couldn't confirm — but Low Earth orbit has 12 in stock (confirmed). Tap to switch stores." The shopper switches in one tap — no cancellation, no re-order. If no alternative store has stock: offer home delivery with expedited shipping covered by Meridian.

**B2 — Staff-side discrepancy dashboard**
A store-level tablet/terminal view showing a live feed of "Items promised to online shoppers but not yet picked." Green = allocated to a picker. Amber = not yet picked but confirmed on shelf. Red = picker couldn't find it. Staff can see the pipeline of commitments and proactively resolve red items *before* the shopper arrives. Flips the staff role from "apologising after failure" to "preventing failure before arrival."

**B3 — "Shopper in transit" timer**
When the system detects the shopper is en route (GPS permission, or estimated travel time from store selection + current time), it triggers a pre-arrival check: staff handheld buzzes "Customer arriving in ~15 min — verify item for Kate.000." If staff responds "can't find it," the system sends the shopper a notification *before* they arrive: "We're checking the back — if we can't locate it, we'll have it ready at [alternative store] by the time you get there." Catches failures mid-travel, not post-arrival.

### Theme C: Closing the Loop — Learning & Holding

**C1 — Staff confirmation hold (low-tech badge)**
When staff confirms via handheld, they print a "**Held for C&C**" sticker and place it on the item in a designated "C&C holding shelf" near the pickup desk. No system integration needed beyond the handheld confirmation flow. The physical badge makes the held item visible to all staff — no "I didn't know it was held" confusion. Items not collected within the hold window (e.g., 2 hours) return to shelf automatically — system sends a "we've released your hold" notification.

**C2 — Post-collection "Did you find it?" micro-survey**
After collection (or cancellation), the app shows a single-tap question: "**Did you collect the [item] today?** (Yes / No — it wasn't there)." If "No" → "What happened? (Shelf was empty / Couldn't find it in store / Changed my mind)." This closes the feedback loop at ~3 seconds per response. The confidence model uses "No — shelf empty" responses as negative training signal for that store+SKU+time-of-day. Over 1,000+ responses, the model learns: "SKU X at store Y at 5pm has a 40% false-positive rate → reduce confidence estimate from 90% to 80%."

**C3 — Dynamic hold window based on store traffic**
Instead of a fixed 2-hour hold, the hold window adapts: during low-traffic periods (Tuesday 10am), hold for 4 hours. During peak (Saturday 2pm), hold for 1 hour. The confidence model predicts the optimal hold window per store+time+SKU velocity. If the shopper hasn't collected within the window, system sends "Your hold has expired — we still show stock available, but it's no longer reserved for you." Balances customer convenience with store operational efficiency.

---

## Summary: Workshop Canvas

| Section | Output |
|---|---|
| **One decision to close** | Confidence display: show estimate vs hide until confirmed |
| **Decision owner** | Product Lead / Head of Digital (Meridian) |
| **Must decide** (4 items) | Confidence display, fallback behaviour, hold duration, error bias |
| **Should explore** (5 items) | Phasing, staff workflow, learning model, legal timeline, pilot metrics |
| **HMW questions** | 10 questions → 3 themes (Trust / Recovery / Learning) |
| **Solutions per theme** | 3 solutions per theme = 9 raw ideas (unjudged) |
| **Time** | 4 hours workshop + pre-work (UX prototype, staff ops input, engineering constraints brief) |
