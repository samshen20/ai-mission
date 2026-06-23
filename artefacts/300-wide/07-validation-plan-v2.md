# 07-validation-plan-v2.md — Usability Validation Plan

**Feature:** Availability Freshness Indicator (Phase 0a)
**Prototype:** `05-mockup.html` (3 screens, clickable)
**Method:** Moderated task-based usability test, 5 participants
**Date:** 2026-06-22
**Target persona:** Click & collect shopper who has experienced ≥1 phantom-stock
disappointment (ordered for pickup, arrived, shelf empty)

---

## Task 1 — Check availability at the closest store

**Scenario:**
You want to buy the Trail Runner X9 for pickup today. You're on the product
page and you'd prefer the store closest to you.

**Instruction:**
"Show me how you'd check whether this item is collectable at a store near you
today."

**What we're testing:**
Can the participant locate the Click & Collect section, scan the store list,
and identify the closest store with available stock?

**AC tested:** Base AC1, AI-AC1 (confidence — fresh variant)

**Success criteria:**
- [ ] Participant scrolls to/near the Click & Collect section without prompting
- [ ] Participant correctly identifies High Street (0.8 mi) as closest
- [ ] Participant can state how many units are on the shelf (4)
- [ ] Participant notices "Checked 12 min ago" freshness information
- [ ] Participant does NOT say "it's in stock" — uses timestamp-aware language
      ("it was checked 12 minutes ago, there were 4")

**Observation notes:**

---

---

---

---

## Task 2 — Compare two stores and pick the better option

**Scenario:**
You notice two stores have the shoes. One is closer, but the other seems to
have more units. You want to make sure the shoes will be there when you arrive.

**Instruction:**
"One of these stores might be a safer bet than the other. Show me how you'd
figure out which store to pick, and tell me why you chose it."

**What we're testing:**
Does the participant use freshness data (quantity, velocity, timestamp) to
make a comparative decision? Or do they default to distance alone?

**AC tested:** Base AC4 (expand store detail), AI-AC1 (confidence — velocity
explainer), AI-AC3 (latency — SAP timestamp, not page-load time)

**Success criteria:**
- [ ] Participant opens at least one StoreDetail view (Screen 2)
- [ ] Participant compares quantity across stores (4 vs 2 vs 3)
- [ ] Participant notices the sell-through velocity ("Sold 8 today")
- [ ] Participant articulates a reason beyond just distance (e.g., "this one
      was checked more recently," "this one is selling fast")
- [ ] Participant does NOT express false certainty ("they definitely have it")

**Observation notes:**

---

---

---

---

## Task 3 — Respond to the low-confidence / stale data warning

**Scenario:**
You're considering the Oakfield Retail Park store, but something looks
different about its listing. The information seems older.

**Instruction:**
"This store's information looks different from the others. Can you tell me what
you think is going on, and what you'd do next?"

**What we're testing:**
Does the participant understand the stale-data state? Do they see the
low-confidence label, the amber styling, and the fallback actions?

**AC tested:** AI-AC2 (refusal/fallback — uncertainty variant), AI-AC6
(negative AC — no green/positive in stale state)

**Success criteria:**
- [ ] Participant notices the amber/orange visual difference without prompting
- [ ] Participant can explain why the data is uncertain ("it hasn't been checked
      in a while — 47 minutes")
- [ ] Participant sees "⚠ Low Confidence" label and can paraphrase its meaning
- [ ] Participant identifies at least one fallback action (call store, ping
      staff, or view other stores)
- [ ] Participant does NOT assume the quantity shown (3) is reliable
- [ ] Participant does NOT express false confidence about this store

**Observation notes:**

---

---

---

---

## Task 4 — Understand how availability is calculated

**Scenario:**
You see a small "ⓘ" icon next to "Click & Collect." You're curious how the
store knows what's on the shelf.

**Instruction:**
"If you wanted to understand how this availability information works — like how
often it updates, or how reliable it is — show me where you'd look."

**What we're testing:**
Is the disclosure discoverable? Does the participant understand the 15–30 min
sync window and the "not guaranteed" caveat?

**AC tested:** AI-AC4 (disclosure — verbatim text, ⓘ icon discoverability)

**Success criteria:**
- [ ] Participant taps/hovers the ⓘ icon without prompting, or finds it when
      asked with minimal guidance
- [ ] Participant reads the disclosure text aloud
- [ ] Participant can paraphrase the key caveat: data refreshes every 15–30
      minutes, availability is not guaranteed
- [ ] Participant does NOT interpret the disclosure as "the system knows exactly
      what's there"
- [ ] Participant does NOT express reduced trust because of the caveat — ideally
      expresses "they're being honest"

**Observation notes:**

---

---

---

---

## Task 5 — Decide what to do when data is too old to trust

**Scenario:**
You've tapped into the Oakfield store detail. The system says the data is stale
and it won't show you a quantity. You still want the shoes today.

**Instruction:**
"The app says availability is uncertain and won't show a number. What would you
actually do here? Walk me through it."

**What we're testing:**
Is the "Can't confirm — call the store" CTA clear and actionable? Does the
participant feel abandoned or supported? Do they find the explanation for *why*
no quantity is shown?

**AC tested:** AI-AC2 (refusal/fallback — CTAs), AI-AC6 (negative AC — no
positive signal)

**Success criteria:**
- [ ] Participant reads "Availability uncertain" and can explain what it means
- [ ] Participant identifies the primary CTA ("Can't confirm — call the store")
- [ ] Participant finds the "Why don't I see a quantity?" explanation
- [ ] Participant expresses a concrete next step (call, ping staff, switch
      store) — not "I guess I'll just go and hope"
- [ ] Participant does NOT express frustration that "the app should just tell me"
      — understands the honesty as intentional

**Observation notes:**

---

---

---

---

## Task-to-AC Traceability Matrix

| Task | Screen(s) | Base AC | AI-AC | Risk if failed |
|------|-----------|---------|-------|----------------|
| 1 — Check closest store | 1 | AC1 | AI-AC1 | Shoppers can't find availability info |
| 2 — Compare stores | 1 → 2 | AC4 | AI-AC1, AI-AC3 | Shoppers ignore freshness; choose by distance only |
| 3 — Stale data warning | 1 → 3 | — | AI-AC2, AI-AC6 | Stale data misinterpreted as reliable |
| 4 — Disclosure | 1 | — | AI-AC4 | Shoppers don't know sync window; over-trust data |
| 5 — Fallback action | 3 | — | AI-AC2, AI-AC6 | Shoppers feel abandoned; no clear next step |

---

## Success Metrics (per task)

| Task | Target | Measurement |
|------|--------|-------------|
| 1 | 5/5 participants locate freshness info within 10s | Time-to-locate, moderator observation |
| 2 | ≥4/5 participants use freshness data (not just distance) in their decision | Verbatim quote: did they mention timestamp, velocity, or quantity difference? |
| 3 | ≥4/5 participants correctly interpret the stale state as "data is old, may be wrong" | Verbatim paraphrase; 0/5 say "it's in stock" |
| 4 | ≥4/5 participants find ⓘ and paraphrase the 15–30 min caveat | Observed discovery (prompted vs unprompted), paraphrase accuracy |
| 5 | ≥4/5 participants name a concrete next step (call/ping/switch) | Verbatim: did they say "call" or "go anyway"? |

**Overall success bar:** ≥4/5 tasks pass at ≥4/5 participants. If Task 3 or 5
fail (uncertainty not understood), the Low Confidence label and fallback CTAs
need redesign before ship.

---

## Participant Screener (recruit 5)

- [ ] Has used click & collect ≥3 times in past 6 months
- [ ] Has experienced ≥1 phantom-stock disappointment (self-reported)
- [ ] Tech comfort: 2 high, 2 medium, 1 low
- [ ] Age: ≥1 participant 45+
- [ ] Exclude: Meridian Retail Group employees, project team members
