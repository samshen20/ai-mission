# 05-pattern-applicability.md — Pattern Scan for Meridian Phase 1

Scanned against: `02-containers.mmd` (container diagram), ADR-001 (modular
monolith), ADR-002 (Kafka event backbone), ADR-003 (Auth0 identity).

---

## Strangler Fig — APPLIES

**Where:** Every country-site backend that the Meridian Headless Commerce
Platform replaces. The platform boundary (`System_Boundary(meridian, ...)`)
is the new system; the 22 legacy country-site backends, 12 legacy mobile-app
backends, and the existing POS integration layer are the legacy systems being
strangled.

**Specific containers/relationships:**
- The **Apollo GraphQL Gateway** is the routing control point. During
  migration, it routes per-endpoint: `/cart/add` → Meridian Cart Service,
  `/catalog/search` → legacy backend until PIM migration completes.
- The **Web App** (Next.js) and **Mobile App** (React Native) serve as BFFs
  that can be pointed at either the legacy or new backend per country.

**Meridian constraint addressed:** "No Big Bang cutover" (from brief). 22
countries must migrate independently. The strangler fig allows the pilot
country to go live while the remaining 21 continue on legacy backends.

---

## Outbox — APPLIES

**Where:** Every service that writes to its own database AND publishes to
Kafka in the same logical transaction.

**Specific containers/relationships:**
- **Cart Service** → **Order Event Bus**: `CartItemAdded`, `CartItemRemoved`,
  `CartAbandoned` events. The Outbox row is written in the same database
  transaction as the cart state change in Cart Service's Redis session store.
- **Checkout Service** → **Order Event Bus**: `OrderPlaced`,
  `PaymentAuthorised`, `PaymentCaptured`, `OrderFulfilled`. The Outbox row is
  written in the same PostgreSQL transaction as the order row in Order
  Database.
- **Identity Service** → **Order Event Bus**: `CustomerRegistered`,
  `LoyaltyTierChanged`, `ConsentUpdated`. The Outbox row is written in the
  same PostgreSQL transaction as the customer profile update in Identity
  Service's local store.

**Meridian constraint addressed:** Consistency between database writes and
event publication without a distributed transaction (which the monolith
doesn't need today but WILL need after service extraction — the Outbox
pattern makes extraction a deployment change, not a rewrite).

---

## Saga — DOES NOT APPLY (deferred to post-extraction)

**Why not:** A Saga coordinates a distributed transaction across multiple
services using compensating actions. In Phase 1, Cart, Checkout, and Identity
compile into a single deployable with a shared transaction context. A checkout
flow that spans Cart → Checkout → Stripe → SAP ECC executes inside one
process — if Stripe authorises but SAP rejects, the compensating refund is a
local function call, not a distributed Saga orchestration.

**When it will apply:** After service extraction (post-Phase 1), when Cart and
Checkout are independent services. At that point, an `OrderPlaced` Saga will
coordinate: Checkout Service calls Stripe, publishes `PaymentAuthorised`,
Cart Service consumes the event and clears the cart, Checkout Service pushes
to SAP. If SAP rejects, a compensating `OrderCancelled` event triggers a
Stripe refund and cart restoration. This is a future concern — ADR-001
explicitly defers extraction, so Saga is not a Phase 1 pattern.

---

## Bulkhead — DOES NOT APPLY (deferred to post-extraction)

**Why not:** Bulkhead isolates thread pools, connection pools, or resource
quotas per service so that one degraded service doesn't exhaust resources for
healthy services. In Phase 1, all modules share a single Node.js event loop
and a single process — there are no per-module thread pools to isolate. A
runaway Cart Service query starves Checkout and Identity equally.

**When it will apply:** After service extraction, each service gets its own
process, its own connection pool to its database, and its own gRPC thread
pool. At that point, a degraded Cart Service doesn't consume Checkout
Service's database connections. For Phase 1, the operational mitigation is
timeouts and request throttling at the Gateway level — not per-service
Bulkheads.

---

## Circuit Breaker — PARTIALLY APPLIES (external calls only)

**Where:** Outbound calls from Meridian-owned containers to external
`System_Ext` dependencies. Not applied to internal gRPC calls during Phase 1
(they are in-process, no network boundary to trip).

**Specific containers/relationships:**
- **Checkout Service → Stripe** (`JSON/HTTPS`): Circuit breaker SHALL open if
  Stripe API error rate exceeds 10% in a 30-second window. Half-open probe
  after 15 seconds. Degraded behavior: queue the payment for retry, show "Payment
  processing — we'll confirm shortly" to the customer instead of blocking
  checkout.
- **Identity Service → Auth0 Management API** (`OAuth 2.0 / OIDC`): Circuit
  breaker SHALL open if Auth0 Management API latency exceeds 2s p95 or error
  rate exceeds 5%. Degraded behavior: serve profile and consent data from the
  local PostgreSQL cache (5-minute TTL). Login itself has no fallback — Auth0
  hosted page degradation is outside Meridian's circuit.
- **Gateway → Auth0 JWKS endpoint** (`OAuth 2.0 / OIDC`): Token validation
  SHALL cache the JWKS response with a 1-hour TTL. If Auth0 JWKS is
  unreachable, the Gateway SHALL validate against the cached keys — do NOT
  open a circuit that rejects all requests. A stale-but-valid key cache is
  safer than denying every customer.

**Meridian constraint addressed:** PSD2 SCA latency budget (1,500ms) and the
operational reality that external SaaS dependencies (Stripe, Auth0) will
degrade independently of Meridian's platform. The circuit breaker prevents a
Stripe degradation from cascading into checkout thread-pool exhaustion that
blocks all customers.

---

## BFF (Backend for Frontend) — APPLIES

**Where:** One BFF per channel, each composing the Apollo GraphQL Gateway
differently for its channel's constraints.

**Specific containers:**
- **Web App (Next.js)** — described as "BFF for web channel — composes
  GraphQL queries for product, cart, checkout, and availability freshness
  views." The web BFF requests full product details, rich availability data
  (quantity + freshness + velocity), and full-page payloads.
- **Mobile App (React Native)** — described as "BFF for mobile channel —
  compact payloads, offline-ready cart, push notification target." The mobile
  BFF requests smaller payloads (fewer fields, pre-computed totals), offline-
  ready cart state, and registers for push notifications.

Both BFFs call the same **Apollo GraphQL Gateway** (`JSON/HTTPS`), but each
requests different field selections optimized for its channel.

**Meridian constraint addressed:** 12 mobile apps and 22 country sites —
each with different latency budgets, payload size constraints, and network
reliability profiles. A single API for all channels would force the mobile app
to receive web-sized payloads over cellular networks, wasting bandwidth and
increasing render time. The BFF pattern isolates channel-specific concerns in
the channel's own backend without duplicating the commerce logic in the
Gateway.

---

## Pipe & Filter — PARTIALLY APPLIES (event pipeline only)

**Where:** The asynchronous event flow from service → Outbox → Kafka →
consumer.

**Specific path:**
1. **Cart Service** writes cart state + Outbox row (filter: domain event
   serialization)
2. Outbox relay reads the Outbox table (pipe: ordered delivery)
3. Outbox relay publishes to **Order Event Bus** (Kafka) (pipe: partitioned
   topic)
4. Future extracted service consumes from Kafka, projects to its own read
   model (filter: projection logic)

**Not applied to:** The synchronous call chain (Web App → Gateway → Cart
Service → Inventory Read Cache). This is a request-response pipeline, not a
Pipe & Filter topology — each step blocks on the previous step's response,
and there is no independent filter stage that can be composed, reordered, or
replaced without changing the caller.

**Meridian constraint addressed:** The event pipeline enables service
extraction without changing producers — a new consumer (extracted Loyalty
Service) can attach to the same Kafka topic without Cart, Checkout, or
Identity changing a single line of code.

---

## Event Sourcing — DOES NOT APPLY (intentionally deferred)

**Why not:** Event Sourcing means the event log IS the source of truth — the
current state is a projection of the event stream. In Meridian Phase 1, the
source of truth is PostgreSQL (Order Database) and Redis (Inventory Read
Cache and Cart session state). Events are published FROM the state change,
not INSTEAD OF the state change. If the Kafka log is lost, orders are not
lost — they're in PostgreSQL. This is event-driven (events notify of state
changes), not event-sourced (events ARE the state).

ADR-001 explicitly rejected full Event Sourcing from day one: "Do NOT
distribute the monolith into independent network services during Phase 1 —
extraction SHALL be deferred until production traffic data identifies the
module whose independent scaling, team velocity, or technology heterogeneity
justifies the distribution cost."

**When it might apply:** Post-extraction, individual services COULD adopt
Event Sourcing internally. The Loyalty Service (future extracted) is the
strongest candidate — a loyalty points ledger is naturally event-sourced
(earn, burn, expire events). But this is a per-service decision, not a
platform-wide pattern.

---

## CQRS — PARTIALLY APPLIES (inventory read model only)

**Where:** The inventory data path has separate write and read models.

**Specific containers/relationships:**
- **Write path:** SAP ECC → Inventory Read Cache (`SFTP/IDoc, batch 15-30
  min`). SAP is the system of record for inventory. The batch file IS the
  write.
- **Read path:** Cart Service → Inventory Read Cache (`RESP/TCP`). The
  Cart Service reads shelf quantities and sell-through velocity from Redis —
  it never writes to this cache. The Redis data model is optimized for the
  Cart Service's query pattern (per-store-SKU hash with `qtyOnShelf`,
  `sellThroughToday`, `lastSync` fields).

This is CQRS-lite: the write model (SAP ECC) and read model (Redis cache)
are separate stores with separate schemas, and the read model is populated
asynchronously by a batch process. But there is no command/query separation
within the Meridian-owned services — Cart Service both reads and writes to
its own Redis session store, Checkout Service both reads and writes to Order
Database.

**Not applied to:** Cart Service (reads and writes cart state in its own
Redis), Checkout Service (reads and writes orders in PostgreSQL), Identity
Service (reads and writes profiles in PostgreSQL). In all three cases, the
same database serves both reads and writes. Full CQRS would split each
service into a command side (writes) and a query side (reads) with separate
databases — this is not justified for Phase 1.

**Meridian constraint addressed:** SAP batch reality. The inventory read
model (Redis) is populated from SAP batch files on a 15–30 minute cadence,
not from real-time events. The CQRS separation makes this batch cadence
explicit: the write path is slow and batch-oriented; the read path is fast
and query-optimized. No synchronous call to SAP ECC is made during a cart
read — the staleness is baked into the architecture, not hidden behind a
synchronous facade.

---

## Summary

| Pattern | Applies? | Phase 1 location | Constraint addressed |
|---------|----------|-----------------|---------------------|
| **Strangler Fig** | Yes | Apollo Gateway routing; Web/Mobile BFF per-country pointing | No Big Bang cutover; 22-country independence |
| **Outbox** | Yes | Cart→Kafka, Checkout→Kafka, Identity→Kafka | DB/event consistency without distributed txns |
| **Saga** | No | — (deferred: monolith uses local txns) | Will apply post-extraction for multi-service checkout |
| **Bulkhead** | No | — (deferred: single process, shared event loop) | Will apply post-extraction for per-service resource isolation |
| **Circuit Breaker** | Partially | Checkout→Stripe, Gateway→Auth0 JWKS, Identity→Auth0 Mgmt API | PSD2 SCA latency budget; external SaaS degradation |
| **BFF** | Yes | Web App (Next.js), Mobile App (React Native) | 12 apps + 22 sites with different payload/latency needs |
| **Pipe & Filter** | Partially | Outbox → Kafka → consumer pipeline | Event pipeline for service extraction |
| **Event Sourcing** | No | — (intentionally deferred by ADR-001) | PostgreSQL/Redis are sources of truth, not Kafka |
| **CQRS** | Partially | Inventory Read Cache (Redis) as read model; SAP ECC as write model | SAP batch reality — slow batch write, fast query-optimized read |
