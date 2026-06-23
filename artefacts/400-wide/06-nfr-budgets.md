# 06-nfr-budgets.md — 7 NFR Budgets for Meridian Phase 1

Each NFR names: a concrete gate, the responsible container(s) from
`02-containers.mmd`, a CI-testable verification, and the brief quote
that justifies the number.

---

## Latency

### NFR-1: POS Cart Lookup — p95 ≤ 250ms (cache-hit path)

- **Gate:** `lookupCustomerCart` GraphQL mutation SHALL complete in ≤ 250ms
  p95 when all cart items have fresh inventory-cache entries (no SAP ECC
  fallback). Measured from POS Client request to enriched-cart response at the
  Apollo GraphQL Gateway.
- **Responsible containers:** POS Client → **Apollo GraphQL Gateway** →
  **Identity Service** → **Cart Service** → **Inventory Read Cache**. The
  Gateway is the measurement point; Cart Service and Inventory Read Cache are
  the dominant contributors (3ms × N items).
- **CI test:** A k6 load script runs `lookupCustomerCart` against a
  pre-warmed staging environment with a 3-item cart (all SKUs in cache).
  1,000 iterations at 10 VUs. Assert: `p95 ≤ 250ms`. Fails the build if the
  p95 exceeds 250ms. Run on every PR that touches Cart Service, Inventory
  Read Cache, or the Gateway's `lookupCustomerCart` resolver.
- **Brief quote:** "18 months, $42M, no Big Bang cutover." The POS cart
  lookup is the most latency-sensitive in-store operation — a store associate
  waiting for a cart to hydrate while a customer stands at the counter is the
  highest-cost latency in the system. 250ms is the threshold where the
  interaction feels instantaneous rather than "the system is thinking."

---

### NFR-2: Payment Authorisation — end-to-end ≤ 1,500ms (PSD2 SCA window)

- **Gate:** The full payment authorisation path — Checkout Service → Stripe →
  bank SCA challenge → Stripe webhook → Checkout Service → enriched cart
  response — SHALL complete in ≤ 1,500ms p95. Measured from the Stripe
  `payment_intent.create` call to the `payment_intent.succeeded` webhook
  received and processed by Checkout Service.
- **Responsible containers:** **Checkout Service** → Stripe (`System_Ext`).
  Stripe is the external payment processor; Checkout Service orchestrates the
  call and processes the webhook. The Apollo GraphQL Gateway relays the
  enriched response to the Web App BFF.
- **CI test:** A Playwright E2E test completes a full checkout on a staging
  environment with Stripe test mode. The test measures `performance.now()`
  from the checkout-submit click to the order-confirmation page render.
  Assert: `duration ≤ 1500ms`. Additionally, a contract test asserts that
  Checkout Service's Stripe HTTP client timeout is set to 400ms (so a hung
  Stripe connection fails fast rather than consuming the full SCA window).
  Run on every PR that touches Checkout Service or the Stripe integration.
- **Brief quote:** "strict EU/JP/US regulatory layer." PSD2 Strong Customer
  Authentication (EU Directive 2015/2366) requires that the payment
  authorisation flow completes within a reasonable window before the
  customer's SCA challenge expires. The 1,500ms target is the working budget
  for the full Stripe + bank round-trip; exceeding it risks SCA timeout, a
  declined payment, and an abandoned cart.

---

## Cost

### NFR-3: Pilot Country Live — ≤ 18 months, within $42M program budget

- **Gate:** One pilot country SHALL be live — web site, mobile app, and POS
  integration serving real customers with shared identity, cart, and loyalty
  — within 18 months of architecture approval. The engineering burn rate
  (headcount × loaded cost + infrastructure) SHALL NOT exceed $42M
  cumulative at the pilot go-live date.
- **Responsible containers:** All containers inside
  `System_Boundary(meridian, "Meridian Headless Commerce Platform")` — the
  **Web App**, **Mobile App**, **Apollo GraphQL Gateway**, **Identity
  Service**, **Cart Service**, **Checkout Service**, **Order Event Bus**,
  **Inventory Read Cache**, and **Order Database**. Every container's build
  time, infrastructure cost, and operational overhead contributes to the
  cumulative budget.
- **CI test:** Not a per-PR CI test — this is a program-level gate. A
  monthly burn-rate dashboard (engineer count × loaded cost from HR system +
  AWS/Azure infrastructure cost from cloud billing API) SHALL be computed
  and compared against the remaining budget. If the projected go-live date
  exceeds 18 months at current burn rate, the gate fails and triggers a
  scope re-baseline. The dashboard query is code-reviewed and versioned in
  the same repository as the infrastructure-as-code.
- **Brief quote:** "18 months, $42M." This is the program's binding constraint
  from the brief. Every architecture decision in ADR-001 through ADR-003 was
  evaluated against this gate. The modular monolith was chosen over
  event-sourced CQRS specifically because Approach B would consume 9–15
  months before the first cart is created.

---

## Quality

### NFR-4: Zero Binary Positive-Affirmation Strings in Rendered DOM

- **Gate:** The rendered DOM of the product page, store detail, and cart
  lookup views SHALL NOT contain any of the following strings in any state
  (fresh data, stale data, cache miss, SAP fallback, error): `"In stock"`,
  `"In Stock"`, `"Available"`, `"Available for Click & Collect"`, a green
  checkmark Unicode character (✅, ✔, 🟢), or any CSS class or ARIA label
  containing `"in-stock"` or `"available"` as a substring.
- **Responsible containers:** **Web App** (Next.js), **Mobile App** (React
  Native), **Apollo GraphQL Gateway** (any server-rendered or
  server-composed text that reaches the DOM). The Cart Service's availability
  status enum (`available`, `available-sap-confirmed`, `unavailable`,
  `unavailable-sap-confirmed`, `stale`, `unknown`) is the ONLY permitted
  vocabulary for availability state — these enums are rendered into
  consumer-facing text by the Web App and Mobile App BFFs.
- **CI test:** A Playwright test renders the product page with mock API
  responses for all six availability statuses (available, available-sap-
  confirmed, unavailable, unavailable-sap-confirmed, stale, unknown). For
  each state, a `page.content()` assertion greps for the forbidden strings.
  Any match fails the build. The forbidden string list is stored in a
  version-controlled file (`ci/forbidden-strings.txt`) so that adding a new
  forbidden pattern is a reviewed code change, not a test-code drift. Run on
  every PR that touches the Web App, Mobile App, or Gateway.
- **Brief quote:** "Meridian Retail Group unifies 22 country sites, 12
  mobile apps, and 1,400 POS systems." The binary "In stock" badge on the
  existing 22 country sites is the root cause of phantom-stock
  disappointment — the heuristic evaluation (`300-wide/02-heuristic-
  evaluation.md`) found every competitor fails at inventory transparency.
  This NFR is the automated enforcement of AI-AC6 from `04-ai-ac-v2.md`:
  "the page must NOT show any binary positive-affirmation pattern suggesting
  a guarantee of shelf presence."

---

## Reliability

### NFR-5: Checkout Availability — 99.9% During Store Operating Hours

- **Gate:** The Checkout Service SHALL respond successfully (HTTP 2xx or
  handled GraphQL error, not a connection timeout or 5xx) to ≥ 99.9% of
  checkout-submit requests during store operating hours (06:00–22:00 local
  time, pilot country). Measured at the Apollo GraphQL Gateway as
  `checkout_submit_success / checkout_submit_total` in a rolling 30-day
  window. Planned maintenance windows (announced ≥ 24 hours in advance) are
  excluded from the denominator.
- **Responsible containers:** **Checkout Service** → Stripe (`System_Ext`)
  → **Order Database** (PostgreSQL) → **Order Event Bus** (Kafka). The
  Checkout Service is the critical-path container; Stripe is the critical
  external dependency. The circuit breaker on `checkout → stripe`
  (NFR-applicability analysis, `05-patterns.md`) is the primary resilience
  mechanism.
- **CI test:** A chaos test in the staging environment runs continuously:
  every 10 minutes, a synthetic checkout is submitted. Concurrently, Stripe
  API faults are injected (simulated 5xx responses, connection resets,
  latency spikes up to 5s) using a fault-injection proxy. Assert:
  `checkout_success_rate ≥ 99.9%` over the trailing 1,000 synthetic
  checkouts. Additionally, a static assertion checks that Checkout Service's
  Stripe HTTP client has `timeout = 400ms` and `retry = 0` (no automatic
  retry on payment — the customer retries, not the server). Run continuously
  in staging; a failure triggers a P2 incident.
- **Brief quote:** "1,400 POS systems." Every POS terminal in a Meridian
  store depends on the Checkout Service to complete in-store purchases. A
  checkout outage during store hours means 1,400 stores cannot transact —
  this is the highest-reliability surface in the entire platform. The 99.9%
  target permits ≤ 43 minutes of unplanned checkout downtime per month
  during operating hours.

---

## Security & Compliance

### NFR-6: No Raw Payment Card Data on Meridian Infrastructure (PCI DSS)

- **Gate:** No Meridian-owned container, database, cache, log stream, or
  event topic SHALL store, process, or transmit a raw Primary Account Number
  (PAN), CVV, or magnetic-stripe track data. All payment card data SHALL
  enter Meridian's boundary ONLY through the Stripe iframe or Stripe Elements
  SDK on the Web App and Mobile App — Stripe tokenizes the card and returns a
  `payment_method_id` to Checkout Service. The `payment_method_id` is the
  ONLY card reference permitted inside Meridian's boundary.
- **Responsible containers:** **Web App** (Next.js), **Mobile App** (React
  Native), **Checkout Service**, **Order Event Bus** (Kafka), **Order
  Database** (PostgreSQL). Every container that touches a payment flow is in
  scope. Stripe (`System_Ext`) is the PCI DSS-compliant tokenization boundary.
- **CI test:** A grep-based static scan runs on every PR across all
  repositories. The scan searches for: (a) regex patterns matching PANs
  (`\b[34][0-9]{15}\b` for Amex, `\b[45][0-9]{15}\b` for Visa/Mastercard),
  (b) variable names containing `pan`, `cvv`, `card_number`, `track_data`,
  `magstripe`, (c) any import of a Node.js crypto module with a comment
  referencing "card" or "payment", (d) any API endpoint path containing
  `/card` or `/payment_method` that accepts a raw body rather than a Stripe
  token. A match triggers a blocking review — the PR cannot merge until a
  security reviewer clears it. Additionally, a runtime assertion in the
  Checkout Service integration test verifies that the Stripe SDK is called
  client-side (in the Web App and Mobile App BFFs) and that the Checkout
  Service receives a `payment_method_id`, never a raw card object.
- **Brief quote:** "strict EU/JP/US regulatory layer." PCI DSS v4.0 (in
  effect March 2025) requires that cardholder data never touches merchant
  servers in plaintext. This gate is binary — a single raw PAN in a log file
  is a PCI DSS violation with mandatory breach notification across all three
  jurisdictions. The EU GDPR, Japan APPI, and California CCPA each impose
  additional breach-notification obligations if card data is exposed.

---

### NFR-7: GDPR Right-to-Erasure — Complete Within 30 Days of Verified Request

- **Gate:** When a verified data-subject erasure request is received
  (customer identity confirmed by Identity Service against Auth0), all
  personal data for that customer SHALL be erased or irreversibly
  anonymised from all Meridian-owned data stores within 30 calendar days.
  Personal data includes: customer profile (Identity Service PostgreSQL),
  order history (Order Database PostgreSQL), cart history (Cart Service
  Redis), and loyalty transaction history (future extracted Loyalty Service).
  Kafka events containing personal data SHALL be crypto-shredded by
  destroying the per-customer encryption key — the encrypted event remains in
  the immutable log but can never be decrypted again.
- **Responsible containers:** **Identity Service** (receives and verifies
  the erasure request), **Order Database** (PostgreSQL — anonymise or delete
  order rows), **Cart Service** (Redis — delete cart session keys), **Order
  Event Bus** (Kafka — destroy per-customer partition encryption key). Auth0
  (`System_Ext`) handles consent erasure on its side; Meridian is responsible
  for confirming Auth0's erasure completion via the Auth0 Management API.
- **CI test:** An integration test in the staging environment: (1) creates a
  synthetic customer with a profile, an order, a cart, and a loyalty
  transaction; (2) triggers the erasure workflow via the Identity Service
  erasure endpoint; (3) after a configurable interval (default 60s for test;
  30 days in production), asserts that the customer's profile row is NULL or
  absent from PostgreSQL, the cart keys are absent from Redis, and the Kafka
  partition key for that customer has been destroyed (decryption fails with
  `KeyDestroyed` error). Additionally, a static assertion checks that every
  database table containing a `customer_id` column has an `erasure_status`
  column with a defined state machine (`pending` → `in_progress` →
  `erased`). Run on every PR that touches the Identity Service or adds a new
  `customer_id` column to any database schema.
- **Brief quote:** "strict EU/JP/US regulatory layer." GDPR Article 17
  (Right to Erasure) requires data controllers to erase personal data
  "without undue delay" and within one month of request. The 30-day gate
  matches the statutory maximum. Japan's APPI and California's CCPA/CPRA
  impose similar obligations with shorter windows in some cases — 30 days is
  the floor across all three jurisdictions that Meridian operates in.

---

## NFR Traceability Matrix

| NFR | Family | Gate | Primary container | Brief quote |
|-----|--------|------|-------------------|-------------|
| NFR-1 | Latency | POS cart lookup p95 ≤ 250ms | Apollo Gateway + Cart Service + Inventory Cache | "18 months, $42M, no Big Bang cutover" |
| NFR-2 | Latency | Payment auth ≤ 1,500ms | Checkout Service → Stripe | "strict EU/JP/US regulatory layer" (PSD2 SCA) |
| NFR-3 | Cost | Pilot live ≤ 18 months, ≤ $42M | All containers inside Meridian boundary | "18 months, $42M" |
| NFR-4 | Quality | Zero forbidden strings in DOM | Web App + Mobile App + Gateway | "22 country sites, 12 mobile apps, 1,400 POS" |
| NFR-5 | Reliability | Checkout 99.9% during store hours | Checkout Service + Stripe + Order DB | "1,400 POS systems" |
| NFR-6 | Security | No raw PAN on Meridian infra | Web/Mobile App + Checkout + Order DB + Kafka | "strict EU/JP/US regulatory layer" (PCI DSS) |
| NFR-7 | Compliance | Erasure complete ≤ 30 days | Identity Service + Order DB + Cart Redis + Kafka | "strict EU/JP/US regulatory layer" (GDPR Art. 17) |
