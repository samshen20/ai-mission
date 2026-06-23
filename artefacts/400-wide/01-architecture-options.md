# 01-architecture-options.md — Three Approaches for Meridian Phase 1 (Build)

**Decision context:** Meridian will **build** the headless commerce platform
rather than buy a commercial one. This invalidates Assumption 4 from
`00-discovery-context.md` — the 18-month, $42M baseline was sized for
configuration + migration of a bought platform. A build decision makes this a
30–36 month program and requires a different architecture conversation.

**Phase 1 scope (assumed for all three approaches):** Get the platform live
serving one pilot country end-to-end — shared identity, shared cart, shared
loyalty, product catalog, and checkout — fronted by that country's web site
and mobile app. Prove the migration and POS integration patterns on one market
before expanding to the remaining 21.

**Constraint carried forward:** "no Big Bang cutover" — the pilot country's
site, app, and POS systems must coexist with the new platform during migration.

---

## Approach A: Modular Monolith with Clean Boundaries

**Load-bearing dimension:** Synchronous, single-deployable, module boundaries at
compile time — not runtime. Decompose to services later, when the seams prove
themselves in production.

### Core idea

- Build one deployable commerce core with enforced module boundaries (cart,
  catalog, checkout, identity, loyalty as packages/libraries, not network
  services). The API gateway routes all channel traffic (web, mobile, POS) to
  this single runtime. Country-specific variations — tax rules, payment
  methods, fulfillment providers — are configuration modules loaded at startup,
  not separate services.

- Migrate the pilot country by placing the modular monolith *behind* the
  existing country site. The site's backend is re-pointed to the monolith's
  API. The site's frontend (HTML/CSS/JS) stays unchanged for now — the monolith
  serves the same data contracts the old backend served. This is a backend
  swap, not a replatform. The shared identity service is the first module
  activated; cart and loyalty follow.

- The module boundaries are enforced by a compiler-level dependency rule (no
  import from `cart` into `loyalty`, shared kernel only). When a module's
  traffic patterns, team ownership, and scaling requirements are understood
  from production data — not speculation — extract it to an independent
  service. Extraction order: identity first (highest auth load, most
  cross-cutting), cart second (session-state-heavy, benefits from isolated
  scaling), loyalty last (read-heavy, event-sourced internally).

### What it optimises for

**Speed to first migration.** One deployable, one pipeline, one team's context.
The pilot country can be live in months because no distributed-systems problems
(network partition, eventual consistency, distributed tracing) exist yet. All
the energy goes into getting the commerce logic right for one market.

**Deferring decomposition decisions until production data exists.** The module
that *looks* like it needs independent scaling may not; the module that seems
trivial may become a bottleneck. Extracting after production observation means
every service boundary is earned, not guessed.

### What it sacrifices

**Independent team scaling from day one.** All engineers work in the same
codebase with the same release cadence. A team that wants to ship a loyalty
feature must coordinate with the team changing the cart. This is fine for a
single pilot country with one engineering team; it becomes the bottleneck when
5+ countries are live and multiple teams need independent velocity.

**Technology heterogeneity.** Every module uses the same language, same
database, same deployment. The loyalty module can't use a graph database if the
monolith is on PostgreSQL. This is acceptable during Phase 1 — the loyalty
read model won't outgrow PostgreSQL with one country's data — but becomes a
constraint at scale.

---

## Approach B: Event-Sourced Platform with CQRS Read Models

**Load-bearing dimension:** Fully asynchronous. Every commerce action is an
immutable event on a shared log. Services project their own state. No
synchronous call between services — ever.

### Core idea

- A single shared event log (Kafka, with compacted topics for state) is the
  platform's spine. Every commerce action — `CartItemAdded`, `OrderPlaced`,
  `LoyaltyPointsEarned`, `IdentityLinked` — is an event written to this log.
  Each service (cart, catalog, checkout, identity, loyalty) is a consumer that
  reads the events it cares about and projects its own read model into its own
  database. No service calls another service's API to get data. If loyalty
  needs cart data, it consumes `CartItemAdded` events and keeps its own
  projection — it never asks the cart service.

- Each channel (web, mobile, POS) gets its own read-model projection optimized
  for that channel's query patterns. The mobile app's cart view is a materialized
  view built from the same events as the web cart, but projected into a
  mobile-optimized shape (smaller payload, pre-computed totals, offline-ready).
  The POS read model is projected into a local store-server database so POS can
  transact even if the WAN link to the platform is down.

- The strangler fig works differently here: the event log *also* consumes
  events emitted by the legacy country-site backends during the migration
  window. A legacy order placed on the old site emits an `OrderPlaced` event
  into the same log. The new loyalty service sees it and awards points. The old
  and new systems coexist as event producers on the same log, not as
  synchronized databases. Cutover happens when the new services handle the full
  event stream and the legacy producers are turned off — one event type at a
  time.

### What it optimises for

**Audit trail and replay-ability.** Every state change is an event. The full
history of every cart, every order, every loyalty point is queryable by
replaying the log. For a retailer with EU/JP/US regulatory obligations
(GDPR right-to-erasure, FTC Act compliance evidence, APPI data tracking), this
is the strongest possible data-governance foundation. If a regulator asks "show
us exactly what this customer saw and when," the answer is in the log.

**Resilience during migration.** Legacy and new systems coexist as event
producers — no synchronous coupling, no dual-write problem, no distributed
transaction between old and new databases. When the legacy backend for the
pilot country emits its last event and is decommissioned, nothing else changes.
The event log is the migration safety net.

### What it sacrifices

**Initial velocity and debuggability.** Every engineer must understand event
sourcing, CQRS, and eventual consistency before writing their first feature.
A simple "show the cart" query that would be a `SELECT` in Approach A becomes:
which events form the cart aggregate, which projection has the current state,
is the projection caught up, and what does the UI show while it's not? The
first country migration takes 2–3× longer than Approach A because the platform
infrastructure (event log, schemas, projections, replay tooling) must be built
before any commerce logic runs.

**Operational complexity from day one.** Kafka cluster management, schema
registry, projection lag monitoring, replay procedures, and event-versioning
discipline are production concerns before a single cart is created. A team that
hasn't operated an event-sourced system before will spend Phase 1 learning
these patterns — and the mistakes (bad partition keys, oversized events,
runaway projections) are hard to fix after the log has production data.

---

## Approach C: Build the Integration Layer, Buy the Commerce Primitives

**Load-bearing dimension:** Make-or-buy per service. Build only the
orchestration and the things Meridian uniquely needs. Buy well-understood
commerce primitives as SaaS APIs. The "build" is the headless integration
layer, not the commerce engine.

### Core idea

- The platform is an API orchestration layer — a thin backend-for-frontend
  (BFF) per channel (web BFF, mobile BFF, POS BFF) that composes calls to
  best-of-breed SaaS services behind it. Identity → Auth0/Okta. Cart and
  checkout → Stripe or a headless commerce API (commercetools). Loyalty →
  a loyalty SaaS provider (Annex Cloud, LoyaltyLion, or similar). Product
  catalog → a commercial PIM (Akeneo, Salsify). The BFFs are the only
  Meridian-built code — they translate between channel-specific needs
  (mobile wants compact payloads, POS wants local resilience) and the
  SaaS APIs they compose.

- The "shared" in shared identity/cart/loyalty comes from choosing SaaS
  providers that support multi-region, multi-brand configurations — not from
  building those capabilities. Auth0 handles cross-country SSO via its tenant
  federation. Stripe handles multi-currency and local payment methods. The
  loyalty SaaS handles multi-country earn/burn rules. Meridian's build
  investment goes into the integration code that makes these SaaS services
  behave as one platform — unified error handling, unified observability,
  unified deployment — and into the POS integration (no SaaS for that).

- The strangler fig is per-endpoint, not per-service. The BFF routes
  `/cart/add` to the new Stripe/commercetools backend when that endpoint is
  ready, while `/catalog/search` still routes to the legacy backend until the
  PIM migration is complete. Migration granularity is a single API endpoint,
  not a whole service or country. The pilot country's site is gradually
  re-pointed endpoint-by-endpoint, with the BFF as the routing control point.

### What it optimises for

**Getting to production with the fewest built-from-scratch services.** Meridian
doesn't build a cart — a solved problem. Doesn't build an identity provider —
a solved problem. Doesn't build a loyalty points ledger — a solved problem.
Engineering effort goes into the integration code (the BFFs, the POS
connector, the monitoring) and the migration tooling. A pilot country can be
live in weeks because the commerce primitives already work — the work is wiring
them together and teaching the old site to talk to the new BFF.

**Leveraging SaaS provider investment in compliance.** Auth0 already handles
GDPR consent flows and data residency configuration. Stripe already handles
PSD2/SCA and PCI DSS (Meridian never touches raw card data). The commercial PIM
already handles multi-currency pricing and localized catalogs. Every compliance
obligation that a SaaS provider has already solved is one Meridian doesn't
build, audit, and maintain.

### What it sacrifices

**Per-request cost at scale.** Every cart mutation is a paid API call to a SaaS
provider. With 22 countries and millions of monthly active users, the SaaS bill
is substantial — and it grows linearly with traffic. In Approaches A and B, the
marginal cost of an additional cart-add is near-zero (your own infrastructure).
In Approach C, it's a line item on a vendor invoice. At pilot-country scale
this is negligible; at 22-country scale it becomes a material cost-of-revenue
issue that may eventually justify migrating off the SaaS (a second migration).

**Control over the commerce logic.** If commercetools' cart model doesn't
support a Meridian-specific promotion rule, the options are: configure around
it (compromise on the business requirement), ask the vendor to build it (their
timeline), or build a compensating service that patches the gap (adds
complexity). The platform's differentiation ceiling is set by the least
flexible SaaS provider in the stack. This is acceptable for commodity commerce
(carts work the same everywhere) but risky if Meridian's competitive advantage
is in novel cart, pricing, or loyalty mechanics.

---

## Comparison

| Dimension | A: Modular Monolith | B: Event-Sourced CQRS | C: Build-Integration-Buy-Primitives |
|-----------|--------------------|------------------------|-------------------------------------|
| **Load-bearing difference** | Synchronous, single deployable, decompose later | Fully async event log, services project own state | Build orchestration, buy commerce primitives as SaaS |
| **Time to pilot country live** | Months (~3–6) | Months (~9–15) | Weeks (~6–12) |
| **Team size needed** | 8–12 engineers (one codebase) | 15–25 engineers (distributed systems + platform team) | 6–10 engineers (BFF + integration code) + vendor management |
| **Compliance foundation** | Retrofit (add audit, add consent, add erasure) | Built-in (event log IS the audit trail) | Inherited (SaaS providers' compliance + Meridian's BFF layer) |
| **Scaling model** | Vertical + extract services later | Horizontal from day one | Vendor scales; Meridian scales BFFs |
| **POS integration fit** | Monolith serves POS API directly | POS gets local event-store projection for offline resilience | BFF serves POS API; POS resilience is Meridian-built |
| **Risk if wrong** | Monolith becomes a ball of mud before extraction; extraction becomes a rewrite | Team never masters event sourcing; projection bugs cause wrong data shown to customers; difficult to unwind | Vendor lock-in; SaaS costs at 22-country scale force a second migration; least-flexible vendor caps product differentiation |

---

## Recommendation

**Start with Approach A, design the module boundaries as if preparing for
Approach B, and use SaaS tactically (Approach C) for identity and payments
only.**

Rationale:

- The "build" decision already stretches the timeline. Approach A gets a pilot
  country live fastest — critical for proving the platform works and
  maintaining stakeholder confidence during a build program.
- The module boundaries designed into the monolith are the service boundaries
  for future extraction. If they're clean (no `cart` importing from `loyalty`,
  shared kernel for cross-cutting types only), extracting to services later is
  a deployment change, not a rewrite.
- Identity (Auth0/Okta) and payments (Stripe) are sufficiently commodity and
  sufficiently compliance-heavy that buying them is correct even in a
  build-first strategy. The FTC, GDPR, PCI DSS, and PSD2 compliance
  surface area of a custom-built identity or payment service is not worth the
  control it buys.
- Approach B is the right long-term architecture for Meridian's regulatory
  surface (event log as audit trail) but the wrong Phase 1 move — the learning
  curve is too steep for a team that hasn't built an event-sourced system before.
  Design for events in the monolith (publish domain events internally), adopt
  the event log as the integration backbone when extracting services, but don't
  lead with it.
