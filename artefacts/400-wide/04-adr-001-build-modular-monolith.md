# ADR-001: Build the Commerce Core as a Modular Monolith

## Context

Meridian must unify 22 country sites, 12 mobile apps, and 1,400 POS systems
into a single headless commerce platform in 18 months with a $42M budget and
no Big Bang cutover. The brief's "strict EU/JP/US regulatory layer" and the
operational reality of SAP batch-synced inventory (15–30 min staleness) mean
the platform must understand batch cadence natively — no commercial SaaS
commerce engine assumes batch inventory. The container diagram excerpt below
reflects the target Phase 1 architecture for one pilot country:

```
System_Boundary(meridian, "Meridian Headless Commerce Platform") {
  Container(web, "Web App", "Next.js")
  Container(mobile, "Mobile App", "React Native")
  Container(gateway, "Apollo GraphQL Gateway", "Node.js / Apollo Server")
  Container(identity, "Identity Service", "Node.js / Express + PostgreSQL")
  Container(cart, "Cart Service", "Node.js / Express + Redis")
  Container(checkout, "Checkout Service", "Node.js / Express")
  ContainerQueue(eventbus, "Order Event Bus", "Apache Kafka")
  ContainerDb(inventory, "Inventory Read Cache", "Redis")
  ContainerDb(orders, "Order Database", "PostgreSQL")
}
System_Ext(stripe, "Stripe")
System_Ext(auth0, "Auth0")
```

The foundational decision gating this diagram: should Meridian build the
commerce core (identity, cart, checkout) or buy it as SaaS APIs behind a thin
integration layer?

## Decision

We will build the commerce core — identity, cart, checkout, inventory caching,
and order persistence — as a single deployable modular monolith with
compiler-enforced module boundaries, and extract modules to independent
services only after production traffic patterns prove which seams are worth the
distribution cost.

## Alternatives Considered

1. **Buy commerce primitives as SaaS (Approach C)** — rejected because every
   commercial commerce engine (commercetools, Elastic Path, Stripe Checkout)
   assumes real-time inventory. Meridian's inventory runs on SAP batch syncs
   every 15–30 minutes. A customer paying in real-time for an item whose shelf
   availability was last confirmed 22 minutes ago creates a time-model mismatch
   that no SaaS vendor in the stack understands. The integration layer Meridian
   would build to paper over this gap becomes the de facto commerce core —
   negating the "buy" premise and producing the worst of both architectures: a
   custom integration layer maintained at SaaS margins, with a per-request cost
   that grows linearly to 22-country scale outside the $42M capital budget.

2. **Event-sourced CQRS from day one (Approach B)** — rejected because the
   platform infrastructure (Kafka cluster, schema registry, consumer-lag
   monitoring, event-replay tooling, projection rebuild procedures) must be
   built, tested, and hardened before any commerce logic runs. The first pilot
   country would take 9–15 months — consuming half the program timeline before
   a single cart is created. Meridian's 18-month constraint demands a pilot
   country live in 3–6 months. Additionally, event sourcing imposes an
   operational burden (poison-pill replay, projection lag diagnosis,
   event-versioning discipline) that assumes a team with senior distributed-
   systems engineers — an assumption the Meridian staffing profile may not
   support.

## Consequences

- **Positive:** A pilot country can be live in 3–6 months. One deployable, one
  pipeline, one team's context. The cart module reads SAP-populated inventory
  cache synchronously with no translation layer between batch data and the
  query path — the freshness indicator (Phase 0a) is co-located with the cart
  logic it enriches. Domain events are published internally from day one
  (`CartItemAdded`, `OrderPlaced`, `LoyaltyTierChanged` to Kafka), so the
  extraction pathway to independent services (Approach B) remains open without
  the operational cost of running a fully event-sourced system. Identity and
  payments are bought tactically (Auth0, Stripe) — the two commodity services
  where the compliance surface of building exceeds the differentiation value.

- **Negative:** The monolith's single deployable couples all country migrations
  to one release cadence. When the France adapter needs a hotfix, Germany's
  unchanged adapter is redeployed with it. This is the fundamental tension: the
  architecture optimises for unification while the strangler-fig migration
  pattern needs per-country isolation. This cost is accepted for Phase 1 (pilot
  country — only one country to migrate) and must be resolved before multi-
  country rollout by extracting country adapters into configuration or
  extracting the first service (likely Identity) to its own deployable. The
  monolith also forces technology homogeneity — every module uses Node.js and
  the same database family — which becomes a constraint if a module (e.g.,
  loyalty ledger) outgrows PostgreSQL at scale.

## Agent-Readable Summary

No commerce state mutation — cart add, checkout submit, inventory deduction,
loyalty point award — SHALL cross a SaaS boundary. Cart, Checkout, Inventory,
and Loyalty code SHALL execute inside the Meridian-owned deployable, reading
SAP-batch-populated cache directly rather than through a vendor API that
assumes real-time stock. The ONLY outbound commerce calls permitted are
Checkout Service → Stripe (payment authorisation/capture) and Gateway →
Auth0 (token validation). Do NOT introduce commercetools, Elastic Path,
CommerceTools, or any headless-commerce SaaS SDK into Cart, Checkout, or
Catalog modules — these libraries embed a real-time inventory assumption that
conflicts with Meridian's 15–30 minute SAP batch cadence, and their presence
in the dependency tree would allow a future developer to call a SaaS cart API
bypassing the Inventory Read Cache. During Phase 1, Cart, Checkout, Identity,
and Catalog SHALL compile into a single deployable; do NOT extract any module
to an independent network service before production traffic data for that
module exists — the extraction decision SHALL cite a specific p95 latency,
throughput ceiling, or team-velocity metric from production, not a
speculative concern.
