# 07-validation-plan.md — Usability Validation Plan

**Feature:** Availability Freshness Indicator (Phase 0a)
**Prototype:** `05-mockup.html`
**Method:** Moderated task-based usability test, 5 participants
**Target persona:** Click & collect shopper who has experienced at least one
phantom-stock disappointment (ordered for pickup, arrived, shelf empty)

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

**Success criteria:**
- [ ] Participant scrolls to/near the Click & Collect section without prompting
- [ ] Participant correctly identifies the closest store (High Street, 0.8 mi)
- [ ] Participant can state how many units are on the shelf at that store
- [ ] Participant notices the "Checked 12 min ago" freshness information
- [ ] Participant does NOT say "it's in stock" — uses timestamp-aware language

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
Does the participant use the freshness data (quantity, velocity, timestamp)
to make a comparative decision? Or do they default to distance alone?

**Success criteria:**
- [ ] Participant opens at least one store detail view (Screen 2)
- [ ] Participant compares quantity across stores (4 vs 2 vs 3)
- [ ] Participant notices the sell-through velocity ("8 sold today")
- [ ] Participant articulates a reason beyond just distance
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

**Success criteria:**
- [ ] Participant notices the amber/orange visual difference without prompting
- [ ] Participant can explain why the data is uncertain ("it hasn't been checked
      in a while")
- [ ] Participant sees the "⚠ Low Confidence" label and can paraphrase its
      meaning
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

**Success criteria:**
- [ ] Participant taps/hovers the ⓘ icon without prompting, or finds it when
      asked
- [ ] Participant reads the disclosure text aloud
- [ ] Participant can paraphrase the key caveat: data is 15–30 min old,
      availability is not guaranteed
- [ ] Participant does NOT interpret the disclosure as "the system knows exactly
      what's there"

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

## Summary matrix

| Task | Screen(s) | AC tested | Risk if failed |
|------|-----------|-----------|----------------|
| 1 — Check closest store | 1 | Base AC1, AI-AC1 | Shoppers can't find availability info |
| 2 — Compare stores | 1 → 2 | Base AC4, AI-AC1 | Shoppers ignore freshness data, choose by distance only |
| 3 — Stale data warning | 1 → 3 | AI-AC2 | Stale data misinterpreted as reliable |
| 4 — Disclosure discoverability | 1 | AI-AC4 | Shoppers don't know sync window; over-trust the data |
| 5 — Fallback action | 3 | AI-AC2 | Shoppers feel abandoned; no clear next step |

---

## Participant screener (recruit 5)

- [ ] Has used click & collect at least 3 times in the past 6 months
- [ ] Has experienced at least one occasion where an item ordered for pickup
      was not available on arrival (self-reported)
- [ ] Mix of tech comfort: 2 high, 2 medium, 1 low
- [ ] Mix of age: at least 1 participant 45+
- [ ] Exclude: Meridian Retail Group employees, anyone who worked on the project
