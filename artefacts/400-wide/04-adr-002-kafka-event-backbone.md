# ADR-002: Use Apache Kafka as the Immutable Event Backbone

## Context

Meridian must support incremental service extraction from the Phase 1 modular
monolith to independent services (the Approach B pathway). Three services —
Cart, Checkout, and Identity — produce cross-cutting state changes that other
services consume: `CartItemAdded`, `OrderPlaced`, `PaymentAuthorised`,
`LoyaltyTierChanged`, `ConsentUpdated`. Without a shared integration backbone,
the monolith's compile-time module boundaries degrade into runtime spaghetti
during extraction — every extracted service must call every other service's
API synchronously. The container diagram embeds this backbone:

```
ContainerQueue(eventbus, "Order Event Bus", "Apache Kafka")
Rel(cart, eventbus, "Publishes CartItemAdded, CartItemRemoved, CartAbandoned", "Kafka/TCP")
Rel(checkout, eventbus, "Publishes OrderPlaced, PaymentAuthorised, PaymentCaptured, OrderFulfilled", "Kafka/TCP")
Rel(identity, eventbus, "Publishes CustomerRegistered, LoyaltyTierChanged, ConsentUpdated", "Kafka/TCP")
```

## Decision

We will use Apache Kafka as an immutable, partitioned, replayable event log —
not a transient message queue. Every cross-service state change SHALL be
published as a domain event to Kafka. Services SHALL NOT call each other's
APIs directly for state propagation. The event log SHALL serve jointly as the
integration backbone for service extraction (Approach B) and the audit trail
for regulatory compliance (GDPR right-to-erasure evidence, FTC Act fair-
practice evidence, APPI data-tracking evidence).

## Alternatives Considered

1. **No event bus — synchronous gRPC between services** — rejected because
   extracting a service from the monolith would require it to call every other
   service's API synchronously. A loyalty-tier change by Identity Service
   would need Cart Service, Checkout Service, and the Gateway to all be
   available and responsive. At 22-country scale with per-region deployments,
   this availability coupling is untenable. Additionally, the audit trail
   would need to be reconstructed from database snapshots and API logs — a
   weaker evidence model for Meridian's EU/JP/US regulatory surface.

2. **Ephemeral cloud queue (SQS/SNS, Google Pub/Sub)** — rejected because
   message retention is time-limited (SQS max 14 days, Pub/Sub max 7 days).
   Event replay for debugging, projection rebuild, or new-service catch-up is
   not possible after the retention window closes. A new loyalty service
   extracting 6 months into production cannot replay order history to build
   its initial projection — it must be bootstrapped from a database snapshot,
   introducing dual-write complexity. Kafka's compacted-topic pattern (retain
   the latest event per key indefinitely) enables catch-up subscriptions that
   ephemeral queues cannot support.

## Consequences

- **Positive:** Every service extraction from the monolith follows the same
  pattern: consume the relevant event streams, build a private projection,
  serve reads from the projection. The monolith and the extracted service
  coexist as event producers on the same log during migration — no dual-write
  problem, no synchronous coupling, no distributed transaction between old and
  new databases. The event log is the single source of truth for every state
  transition — satisfying GDPR right-to-erasure (crypto-shred the key for that
  customer's partition), FTC Act evidence (replay the log to show exactly what
  was displayed and when), and APPI data tracking (prove data residency by
  showing which partition the customer's events landed in).

- **Negative:** Meridian must operate a Kafka cluster from Phase 1 — cluster
  provisioning, partition rebalancing, schema registry, consumer-lag alerting,
  and replay runbooks are production concerns before the first cart is created.
  This adds ~2 sprint cycles to the pilot-country timeline vs a monolith with
  no event bus. The team must develop Kafka operational competence early —
  poison-pill message recovery, schema evolution compatibility checks, and
  partition-key design (a bad partition key produces hot partitions that
  throttle the entire event stream). The event log also complicates GDPR right-
  to-erasure: immutable events cannot be deleted, so the platform must support
  crypto-shredding (encrypt per-customer with a key that can be destroyed on
  erasure request) or tombstone events with a separate erasure-eligible
  projection — neither is trivial.

## Agent-Readable Summary

Cart Service, Checkout Service, and Identity Service SHALL publish every
state-changing domain event to Kafka using the transactional Outbox pattern —
the event SHALL be written to the Outbox table in the same database
transaction as the state change, and a relay process SHALL publish it to
Kafka. No service SHALL call another service's API directly to propagate
state. Specifically: Cart Service SHALL NOT call Checkout Service when a cart
is abandoned; Checkout Service SHALL NOT call Cart Service when an order is
placed; Identity Service SHALL NOT call Cart Service or Checkout Service when
a loyalty tier changes. The ONLY communication path between Cart, Checkout,
and Identity is the Kafka event log. Each topic SHALL use compacted cleanup
with infinite retention — do NOT configure time-based retention on any topic,
as this prevents a future extracted service from replaying the full event
history to build its initial projection. Partition keys SHALL be the
aggregate root ID (cartId for cart events, orderId for order events,
customerId for identity events); do NOT use round-robin or random partition
keys, as a single hot partition throttles the entire event stream for that
aggregate type. Do NOT use Kafka Connect or Debezium to capture PostgreSQL
WAL changes — application-level domain events are the stable API between
services; CDC couples every downstream consumer to the current database
schema, turning every DDL migration into a breaking change for Cart,
Checkout, Loyalty, and any future extracted service. The Kafka producer
SHALL be configured with `max.block.ms = 0` — if the producer buffer is
full, the relay SHALL fail immediately rather than blocking the Outbox
polling loop. The relay SHALL retry failed publishes with exponential
backoff (initial 100ms, multiplier 2, max 3 attempts). After 3 failed
retries, the event SHALL be written to a dead-letter topic
(`order-events-dlq`, `cart-events-dlq`, `identity-events-dlq`) and the
relay SHALL continue to the next Outbox row. An alert SHALL trigger if any
dead-letter topic has unconsumed messages for > 5 minutes.
