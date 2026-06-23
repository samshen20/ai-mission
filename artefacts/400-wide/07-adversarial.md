# 07-adversarial.md — Adversarial Analysis: Where Meridian Phase 1 Breaks First

**Rule:** Name the container or relationship, the first user symptom, and the
triage verdict. Patch = change a named artifact. Accept = name the owner.

---

## (a) 10× Black Friday Peak Load

80,000 RPS sustained / 120,000 RPS burst. Pilot country only — but the
architecture must not require a rewrite to survive multi-country scale.

### Break A1 — Apollo Gateway Event-Loop Saturation

- **Container:** Apollo GraphQL Gateway (`Node.js / Apollo Server`).
- **Relationship:** `web → gateway` and `mobile → gateway` (both `JSON/HTTPS`).
  All inbound traffic funnels through one Gateway process.
- **First user symptom:** The product page spinner never resolves. The Gateway
  health check (`GET /healthz`) returns 200 OK because the Node.js process is
  alive and the port is bound — the load balancer keeps routing traffic. p50
  latency is 180ms (healthy); p99 latency is 32 seconds (event-loop backlog).
  No 5xx errors are emitted, so the error budget shows green. Customers abandon
  their carts; Meridian has no alert because every monitoring signal looks
  healthy except p99 latency — and p99 latency is not on the default dashboard.
- **Verdict:** ACCEPT RISK for Phase 1.
- **Owner:** Tomás (architecture risk).
- **Rationale:** Phase 1 is a single pilot country — Black Friday scale
  (22-country equivalent) is not the pilot traffic profile. The Gateway can be
  horizontally scaled behind a load balancer when multi-country rollout begins.
  The acceptance condition: a horizontal-scaling runbook must be tested before
  the second country goes live. Add an NFR: Gateway must demonstrate linear
  throughput scaling with instance count up to 8 instances in a staging load
  test before multi-country rollout.

### Break A2 — Inventory Read Cache Connection Exhaustion

- **Container:** Inventory Read Cache (Redis `ContainerDb`).
- **Relationship:** `cart → inventory` (`RESP/TCP`). Every cart read opens a
  Redis connection to check per-item stock. At 80K RPS with 3-item carts, the
  Cart Service opens ~240K Redis connections/second.
- **First user symptom:** Cart Service throws `Redis connection refused` after
  Redis hits `maxclients` (default 10,000). The Cart Service's error handler
  catches the Redis error and marks every cart item as `availability:
  "unknown"` rather than crashing. The product page renders with a grey "Can't
  check stock right now" label on every item. The system is technically "up"
  (HTTP 200, valid GraphQL response) but functionally useless — no customer can
  see shelf availability.
- **Verdict:** PATCH NOW.
- **Changes:** Add connection-pool maximum and per-item Redis circuit breaker
  to `06-nfrs.md`. The Cart Service's Redis client SHALL use a pooled
  connection with `maxConnections = 50` and `maxWaitingClients = 200`. When
  the pool is exhausted, the Cart Service SHALL serve `availability: "unknown"`
  for remaining items rather than blocking the request or crashing.

### Break A3 — Kafka Producer Buffer Overflow Blocks DB Transactions

- **Container:** Order Event Bus (Apache Kafka `ContainerQueue`).
- **Relationship:** `cart → eventbus`, `checkout → eventbus`, `identity →
  eventbus` (all `Kafka/TCP`). The Outbox relay publishes events to Kafka. At
  10× load, the Kafka producer buffer fills faster than brokers acknowledge.
- **First user symptom:** The Outbox relay's `send()` call blocks (default
  `max.block.ms = 60000`). Because the Outbox row was written in the same DB
  transaction as the business state change, a blocked Outbox relay means the
  relay's polling loop stalls. Events accumulate in the Outbox table. Consumers
  see stale state. If the buffer stays full for > 60s, the producer throws
  `TimeoutException` and the relay crashes. On restart, it replays accumulated
  Outbox rows — potentially publishing duplicate events. No customer-visible
  break yet, but the event pipeline is stalled and the system is one relay
  crash away from losing event ordering.
- **Verdict:** PATCH NOW.
- **Changes:** Add producer buffer configuration to ADR-002. Kafka producer
  SHALL use `max.block.ms = 0` (fail fast — if the buffer is full, return an
  error immediately rather than blocking the relay thread). The relay SHALL
  retry with exponential backoff. Add a dead-letter topic for events that
  exceed `retries = 3`. Add an alert: if the dead-letter topic has > 0
  unconsumed messages for > 5 minutes, trigger P2.

---

## (b) Hostile Inputs at EU Checkout

### Break B1 — Malformed PSD2 SCA Callback with Valid Signature

- **Container:** Checkout Service (`Node.js / Express`).
- **Relationship:** `stripe → checkout` (`Stripe Webhooks, JSON/HTTPS`). Stripe
  sends a `payment_intent.succeeded` webhook. The Checkout Service verifies the
  `stripe-signature` header (prevents body tampering) and processes the event.
- **First user symptom:** An attacker with access to a legitimate Stripe
  webhook (captured from a test environment or a misconfigured webhook
  endpoint) replays it with a modified `amount_captured` field — but this is
  prevented by Stripe's webhook signature verification. The REAL risk is
  subtler: the attacker replays a LEGITIMATE webhook for a different order
  (same customer, different purchase). The Checkout Service's webhook handler
  matches the `payment_intent_id` to the order but does NOT verify that the
  `amount_captured` in the webhook matches the order total in Order Database.
  If Stripe's webhook reports a captured amount that diverges from the order
  total (Stripe partial capture, or a race condition where the order was
  modified between payment and capture), the Checkout Service marks the order
  as "paid" without reconciling amounts.
- **Verdict:** ACCEPT RISK with compensating control.
- **Owner:** Asha Sundaram (compliance).
- **Rationale:** Stripe's webhook signature verification (`stripe-signature`
  header) is the primary defense against webhook tampering — a malformed
  webhook body would fail signature verification and be rejected by the Stripe
  SDK before reaching application code. The residual risk is amount mismatch
  between the webhook and the order. Mitigation: add a nightly reconciliation
  job that compares `amount_captured` from Stripe's API against `order_total`
  in Order Database for all orders in `paid` status. Any mismatch > €0.01
  triggers a P2 incident and a manual refund/re-bill. This is an operational
  control, not an architecture change.

### Break B2 — Replayed Payment Webhooks (No Idempotency)

- **Container:** Checkout Service (`Node.js / Express`).
- **Relationship:** `stripe → checkout` (`JSON/HTTPS`). The webhook handler
  processes `payment_intent.succeeded` events.
- **First user symptom:** An attacker replays a captured `payment_intent.
  succeeded` webhook 50 times. The Checkout Service processes each replay as a
  new event because it has no idempotency guard. The Order Database records 50
  duplicate `payment_captured` state transitions. The fulfillment state machine
  advances 50 times. SendGrid dispatches 50 "Your order is ready for pickup"
  emails. The customer receives 50 identical emails in 2 minutes and calls
  support, convinced Meridian has been hacked.
- **Verdict:** PATCH NOW.
- **Changes:** Add webhook idempotency to `03-integrations.md`. The Checkout
  Service webhook handler SHALL extract `stripe_event_id` from the webhook
  payload and check it against a `processed_stripe_events` table in Order
  Database BEFORE processing the event. If the event ID exists, the handler
  SHALL return HTTP 200 (acknowledge receipt) without processing. The
  `processed_stripe_events` table SHALL have a 30-day retention period.
  Idempotency SHALL be tested in CI: a contract test replays an identical
  webhook payload and asserts that the second processing is a no-op.

### Break B3 — SQL Injection at Loyalty-QR Lookup

- **Container:** Identity Service (`Node.js / Express + PostgreSQL`).
- **Relationship:** `gateway → identity` (`gRPC`). The Gateway calls
  `resolveLoyaltyQr(qrCode)` with a raw QR string scanned at the POS.
- **First user symptom:** An attacker prints a QR code containing a SQL
  injection payload: `MRD-LOY-\'; DROP TABLE customers; --`. The store
  associate scans it at the POS. The Identity Service's `resolveLoyaltyQr`
  resolver concatenates the QR string into a SQL query: `SELECT * FROM
  customers WHERE qr_code = '${input}'`. PostgreSQL executes the injected
  statement. If the `customers` table is dropped, every subsequent loyalty-QR
  lookup across the pilot country returns `LOYALTY_QR_UNKNOWN`. Every store
  associate at every POS cannot look up customer carts. The pilot country's
  in-store experience is dead.
- **Verdict:** PATCH NOW.
- **Changes:** Add SQL injection gate to `06-nfrs.md` (NFR-8). The Identity
  Service SHALL use parameterized queries for ALL database access. The CI
  pipeline SHALL run a static analysis rule that rejects any string
  concatenation or template literal used to construct a SQL query. The
  `resolveLoyaltyQr` handler SHALL validate the QR code format against a regex
  (`^MRD-LOY-[A-Z0-9]{4}-[A-Z0-9]{4}$`) BEFORE passing it to the database
  layer. Format validation failure SHALL return `LOYALTY_QR_UNKNOWN` — do not
  echo the invalid QR string in the error response (prevents reflected XSS at
  the POS display). Additionally, the PostgreSQL user for the Identity Service
  SHALL NOT have `DROP TABLE` privileges — the application database user SHALL
  have only `SELECT`, `INSERT`, `UPDATE`, `DELETE` on its schema.

---

## (c) Partner Outage

### Break C1 — SAP ECC Down for 2 Hours

- **Container:** Inventory Read Cache (Redis `ContainerDb`).
- **Relationship:** `sap → inventory` (`SFTP/IDoc, batch 15–30 min`). No batch
  files arrive during the outage.
- **First user symptom:** After 30 minutes (the staleness threshold), every
  StoreCard on every product page switches to the `stale` variant. The amber
  "⚠ Stale data" badge replaces the green "● Fresh data" badge. After 60
  minutes, the `lastSync` timestamp on every store+SKU reads "Last checked >60
  min ago." The freshness indicator degrades from a calibrated data point to a
  blanket uncertainty message: every store, every product, every customer sees
  "Availability uncertain — call the store." The system is technically correct
  — it's refusing to show data it can't verify — but the user experience has
  collapsed from "calibrated confidence" to "we don't know anything."
- **Verdict:** ACCEPT RISK.
- **Owner:** David Park (store-ops impact).
- **Rationale:** This is the DESIGNED degradation behavior from AI-AC2. The
  freshness indicator was built to do exactly this: when data is too stale to
  trust, show uncertainty rather than false confidence. A blanket "call the
  store" message during a known SAP outage is honest. The mitigation is
  operational, not architectural: store managers need a communication plan
  ("SAP is down — tell customers to call ahead, staff the phones"). An
  architectural mitigation (showing "SAP ECC maintenance — stock data
  refreshing at 14:00 UTC") could reduce the customer confusion but requires
  SAP ECC to publish a maintenance schedule Meridian can consume — out of scope
  for Phase 1.

### Break C2 — Stripe Circuit Breaker Blocks All Payments

- **Container:** Checkout Service (`Node.js / Express`).
- **Relationship:** `checkout → stripe` (`JSON/HTTPS`). The circuit breaker
  (`05-patterns.md`) opens when Stripe error rate exceeds 10% in a 30-second
  window.
- **First user symptom:** Stripe experiences a partial degradation — credit
  card payments return intermittent 5xx, but iDEAL (Dutch online banking) and
  SEPA Direct Debit continue to work. The circuit breaker sees 10% error rate
  across all payment methods, opens, and blocks ALL payment methods — including
  the healthy ones. Every customer sees "Payment processing unavailable —
  please try again later." iDEAL customers who could have completed their
  purchase are blocked. The binary circuit breaker (open/closed) has turned a
  partial payment-method degradation into a total checkout outage.
- **Verdict:** PATCH NOW.
- **Changes:** Edit `05-patterns.md` — the Circuit Breaker on `checkout →
  stripe` SHALL be per-payment-method, not global. Each payment method (card,
  iDEAL, SEPA, Klarna) SHALL have its own circuit breaker with independent
  error-rate tracking. When the card circuit opens, iDEAL and SEPA payments
  continue to flow. The Checkout Service SHALL expose a `payment_methods:
  [available_methods]` field in the cart response so the Web App BFF can
  disable only the degraded payment method's button rather than blocking the
  entire checkout. Additionally, the circuit breaker SHALL support a half-open
  state with a 15-second probe interval — not a hard 30-second closed window.

### Break C3 — Auth0 Management API Degraded During Peak

- **Container:** Identity Service (`Node.js / Express + PostgreSQL`).
- **Relationship:** `identity → auth0` (`OAuth 2.0 / OIDC`). The Identity
  Service resolves customer profiles against Auth0 Management API on cache miss
  or TTL expiry (5 minutes).
- **First user symptom:** A store associate scans a loyalty QR code at the POS.
  The customer's profile cache entry expired 30 seconds ago. The Identity
  Service attempts to refresh from Auth0 Management API — but Auth0 is
  experiencing a 3-second latency spike. The `resolveLoyaltyQr` gRPC call
  blocks for 3 seconds, then times out. The Identity Service returns an error
  to the Gateway. The Gateway returns `LOYALTY_QR_UNKNOWN` to the POS. The
  store associate sees "Customer not found — check the QR code." The customer
  — who is a Gold-tier loyalty member and has shopped at Meridian for 5 years
  — is standing at the counter. The associate scans the QR code again. Same
  error. The associate apologizes and manually looks up the customer by name.
- **Verdict:** PATCH NOW.
- **Changes:** Edit ADR-003 — the Identity Service SHALL serve profile
  resolution from the local PostgreSQL cache EVEN WHEN the cache entry has
  expired, if the Auth0 Management API is unreachable or exceeds a 200ms
  timeout. The expired cache entry SHALL be returned with a `stale: true` flag
  so the Gateway can decide whether to accept staleness. For the POS cart
  lookup, a stale profile is acceptable (loyalty tier rarely changes
  mid-session). For a GDPR consent check, a stale profile is NOT acceptable —
  the consent must be confirmed live. The `resolveLoyaltyQr` handler SHALL
  accept a `maxStalenessSeconds` parameter: POS cart lookup allows 300s
  staleness; consent check requires 0s staleness.

---

## Triage Summary

| # | Break | Verdict | Artifact changed or owner |
|---|-------|---------|--------------------------|
| A1 | Gateway event-loop saturation at 10× load | ACCEPT | Tomás (architecture) — Phase 1 pilot scale; horizontal-scaling runbook required before multi-country rollout |
| A2 | Redis connection exhaustion under cart-read flood | **PATCH** | `06-nfrs.md` — add connection-pool maximum + per-item Redis circuit breaker |
| A3 | Kafka producer buffer overflow blocks DB txns | **PATCH** | `04-adr-002-kafka-event-backbone.md` — `max.block.ms=0`, dead-letter topic, retry with backoff |
| B1 | Malformed PSD2 SCA callback | ACCEPT | Asha Sundaram (compliance) — Stripe signature verification prevents tampering; add nightly amount-reconciliation job |
| B2 | Replayed payment webhooks (no idempotency) | **PATCH** | `03-integrations.md` — `stripe_event_id` idempotency table, contract test |
| B3 | SQL injection at loyalty-QR lookup | **PATCH** | `06-nfrs.md` — NFR-8: parameterized queries, QR format regex, least-privilege DB user |
| C1 | SAP ECC down for 2 hours | ACCEPT | David Park (store-ops) — designed degradation behavior per AI-AC2; stores need communication plan |
| C2 | Stripe circuit breaker blocks all payment methods | **PATCH** | `05-patterns.md` — per-payment-method circuit breakers, not global |
| C3 | Auth0 Management API degraded, blocks POS cart lookup | **PATCH** | `04-adr-003-auth0-identity-provider.md` — serve stale cache entry on Auth0 timeout for non-consent operations |

---

## Patches Applied

### Patch A2 → `06-nfrs.md`

Appended NFR-8: Cart Service Redis client SHALL use connection pooling with
`maxConnections = 50`, `maxWaitingClients = 200`. When pool exhausted, SHALL
degrade to `availability: "unknown"` rather than blocking.

### Patch A3 → `04-adr-002-kafka-event-backbone.md`

Agent-Readable Summary updated: Kafka producer SHALL use `max.block.ms = 0`.
Failed publishes retried with exponential backoff (3 attempts). After 3
failures, events go to a dead-letter topic. Alert if dead-letter topic has
unconsumed messages for > 5 minutes.

### Patch B2 → `03-integrations.md`

Added idempotency section: Checkout Service SHALL store `stripe_event_id` in
`processed_stripe_events` table before processing. Duplicate events SHALL
return HTTP 200 (no-op). CI contract test replays webhook and asserts no-op.

### Patch B3 → `06-nfrs.md`

Appended NFR-9: Identity Service SHALL use parameterized queries exclusively.
CI static analysis SHALL reject string-concatenated SQL. QR format SHALL be
validated against regex before DB query. DB user SHALL lack DDL privileges.

### Patch C2 → `05-patterns.md`

Circuit Breaker pattern updated: `checkout → stripe` SHALL use per-payment-
method circuit breakers. Card, iDEAL, SEPA, and Klarna each have independent
error-rate tracking. Half-open probe interval = 15s.

### Patch C3 → `04-adr-003-auth0-identity-provider.md`

Agent-Readable Summary updated: Identity Service SHALL serve expired cache
entries when Auth0 Management API is unreachable or exceeds 200ms timeout.
`stale: true` flag included so callers can decide. POS cart lookup accepts
300s staleness; consent check requires 0s staleness.
