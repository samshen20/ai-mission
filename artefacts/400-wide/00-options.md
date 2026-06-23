# 00-options.md — Three Approaches with Constraint Pressure

**Decision:** Build, not buy. Meridian builds the headless commerce platform.
**Phase 1 scope:** One pilot country end-to-end (identity, cart, loyalty,
catalog, checkout) fronting that country's web site, mobile app, and POS.
**Constraint:** No Big Bang cutover — platform must coexist with legacy.

---

## Approach A: Modular Monolith → Extract Services Later

**Load-bearing dimension:** Synchronous, single deployable. Module boundaries
enforced at compile time. Decompose to services when production data proves
which seams matter.

**Core idea:**
- One deployable commerce core — cart, catalog, checkout, identity, loyalty as
  compile-time modules. API gateway routes all channels (web, mobile, POS) to
  this single runtime. Country variations (tax, payments, fulfillment) are
  configuration, not separate services.
- Pilot country migrates via backend swap: the existing site's backend is
  re-pointed to the monolith's API. Frontend unchanged. Shared identity
  activates first; cart and loyalty follow.
- Module boundaries enforced by compiler dependency rules. Extract to
  independent services only after production traffic patterns, team ownership,
  and scaling bottlenecks are observed — not speculated. Extraction order:
  identity, then cart, then loyalty.

**Optimises for:** Speed to first migration. One deployable, one pipeline, one
team's context. No distributed-systems problems until they're earned.

**Sacrifices:** Independent team velocity from day one. All engineers share a
release cadence. Technology homogeneity — every module uses the same language
and database.

### ↳ Constraint that pressures it hardest: Strangler-fig coexistence

The strangler fig demands per-country isolation: migrate France, leave Germany
untouched, let each country move at its own pace. But the monolith hosts every
country adapter in one deployable. When the France adapter needs a hotfix,
Germany's adapter — unchanged and not yet live — gets redeployed with it. When
a release breaks the Netherlands checkout, Italy can't migrate that week. Every
country's migration timeline is coupled to every other country's through the
shared release. The monolith optimises for unification at exactly the point
where the migration pattern needs independence. This is the fundamental
tension: one platform, one release, but 22 countries that must move
independently.

---

## Approach B: Event-Sourced Platform with CQRS Read Models

**Load-bearing dimension:** Fully asynchronous. Every commerce action is an
immutable event on a shared Kafka log. Services project their own state. No
synchronous call between services — ever.

**Core idea:**
- A single shared event log is the platform spine. Every action
  (`CartItemAdded`, `OrderPlaced`, `LoyaltyPointsEarned`) is an event. Each
  service consumes the events it needs and projects its own read model into its
  own database. No service calls another's API.
- Each channel (web, mobile, POS) gets its own read-model projection. Mobile
  cart is a materialized view optimized for small payloads and offline-readiness.
  POS projection lives on a local store-server so POS transacts even if the WAN
  link drops.
- Strangler fig via event coexistence: legacy backends emit events into the same
  log during migration. New services consume from both legacy and new producers.
  Cutover happens when new services handle the full stream and legacy producers
  are turned off — one event type at a time.

**Optimises for:** Audit trail and replay-ability. Every state change is an
immutable event. GDPR right-to-erasure, FTC Act compliance evidence, APPI data
tracking — the log is the answer. Resilience during migration: legacy and new
coexist as event producers with no synchronous coupling and no dual-write
problem.

**Sacrifices:** Initial velocity and debuggability. Every engineer must
understand event sourcing, CQRS, and eventual consistency before writing their
first feature. The first country migration takes 2–3× longer because the
platform infrastructure (event log, schema registry, projections, replay
tooling) must be built before any commerce logic runs.

### ↳ Constraint that pressures it hardest: Junior team operability

Event sourcing is the hardest operational model of the three options. Kafka
cluster management, schema registry, projection lag monitoring, replay
procedures, event-versioning discipline — these are production concerns before
a single cart is created. When the loyalty projection falls 47 events behind
the cart projection at 3am, the on-call engineer must determine: is this
consumer lag (transient), a poison-pill event (requires replay with skip), or
a schema evolution that broke deserialization (requires rollback)? A junior
engineer cannot reason about this under incident pressure. A mid-level engineer
who hasn't operated Kafka in production cannot either. If Meridian's team is
not staffed with senior distributed-systems engineers who have run
event-sourced systems before, Approach B produces a platform the team cannot
debug when it breaks — and it will break. The architecture assumes a team
seniority level that may not exist.

---

## Approach C: Build the Integration Layer, Buy the Commerce Primitives

**Load-bearing dimension:** Make-or-buy per service. Build only the
orchestration. Buy well-understood commerce primitives as SaaS APIs.

**Core idea:**
- The platform is a thin backend-for-frontend (BFF) per channel that composes
  calls to best-of-breed SaaS: Auth0/Okta for identity, Stripe/commercetools
  for cart and checkout, loyalty SaaS for points, Akeneo/Salsify for catalog.
  Meridian builds only the BFFs and the POS connector.
- "Shared" comes from SaaS providers' multi-region, multi-brand configuration —
  not from building those capabilities. Auth0 handles cross-country SSO. Stripe
  handles multi-currency and local payment methods. The loyalty SaaS handles
  multi-country earn/burn rules.
- Strangler fig is per-endpoint: the BFF routes `/cart/add` to the new backend
  when ready, while `/catalog/search` still hits legacy until PIM migration is
  complete. Migration granularity is a single API endpoint.

**Optimises for:** Fastest path to production. Commerce primitives already work.
Engineering goes into integration code and migration tooling. SaaS providers
carry the compliance burden for GDPR, PSD2/SCA, PCI DSS.

**Sacrifices:** Per-request cost at scale — every cart mutation is a paid API
call. At 22-country volume, the SaaS bill becomes a material cost-of-revenue
line that may force a second migration off the SaaS. Control ceiling set by the
least flexible vendor.

### ↳ Constraint that pressures it hardest: SAP batch-update reality

Every SaaS commerce primitive in this stack assumes real-time data. Stripe
authorizes payments in milliseconds. commercetools updates inventory on every
order event. The loyalty SaaS awards points on purchase confirmation. But
Meridian's inventory runs on SAP batch syncs every 15–30 minutes — the shelf
quantity the BFF shows is a snapshot that was already stale when the batch file
landed. The BFF composes real-time payment capability with batch inventory
data, and these two have fundamentally different time models. A customer pays
(real-time, Stripe confirms in <1s) for an item whose shelf availability was
last confirmed 22 minutes ago (batch SAP). The BFF must reconcile "payment
succeeded" with "stock might not be there" — and none of the bought SaaS
primitives understand this gap because none of them were designed for
batch-synced physical retail. The integration layer Meridian builds is the only
place this mismatch is visible, and it must paper over a time-model
incompatibility that every SaaS vendor in the stack assumes doesn't exist.

---

## Comparison

| | A: Modular Monolith | B: Event-Sourced CQRS | C: Buy Primitives |
|---|---|---|---|
| **Load-bearing dimension** | Synchronous, decompose later | Async event log, project own state | Build orchestration, buy commerce |
| **Time to pilot** | ~3–6 months | ~9–15 months | ~6–12 weeks |
| **Hardest constraint** | Strangler-fig coexistence | Junior team operability | SAP batch-update reality |
| **How the constraint bites** | One release for 22 countries; per-country migration isolation is impossible | The hardest ops model meets a team that may not have the seniority to debug it at 3am | Real-time SaaS assumes data Meridian doesn't have; the BFF must reconcile two time models |
| **Team needed** | 8–12 engineers | 15–25 + platform team | 6–10 + vendor management |

---

## Recommendation

**Start with A, use C tactically for identity and payments, design module
boundaries for eventual B-style extraction.**

- **Identity and payments** are sufficiently commodity and sufficiently
  compliance-heavy (GDPR consent, PSD2/SCA, PCI DSS) that buying them is
  correct even in a build strategy. The compliance surface of building them
  exceeds the control you gain.
- **Cart, catalog, loyalty, and the POS connector** are where Meridian's
  differentiation lives — the freshness indicator (Phase 0a from `300-wide/`),
  the sell-through velocity explainer, the cross-channel cart persistence.
  These are worth building.
- **Design for events internally** — publish domain events within the monolith
  from day one — so that when services are extracted to Approach B, the
  integration backbone is already event-shaped. Don't lead with Kafka, but
  don't design synchronous coupling that blocks the eventual transition.
