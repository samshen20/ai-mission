# 04-reversal-cost.md — Three Highest-Cost Reversal Decisions

Scanned from `02-containers.mmd` (C4 Container Diagram, Meridian Phase 1).

---

## Decision 1: Modular Monolith (Build), not Buy Primitives

**Where it appears in the diagram:**
- Title: `Container Diagram (Modular Monolith)` — line 2
- `System_Boundary(meridian, "Meridian Headless Commerce Platform")` — line 8
- Six `Container()` declarations inside the boundary: Identity Service, Cart
  Service, Checkout Service, Order Event Bus (Kafka), Inventory Read Cache
  (Redis), Order Database (PostgreSQL) — lines 12–17
- Internal gRPC edges between Gateway and each service — lines 35–37

**What this decision committed to:**
Meridian builds and operates the commerce core: identity, cart, checkout,
inventory caching, order persistence, and an event bus. These are
Meridian-owned codebases, databases, and infrastructure — not SaaS APIs.

**What reversal to BUY (Approach C) costs:**
- **Identity Service** (line 12) is deleted. Customer profiles, consent records,
  and loyalty tier state move from Meridian PostgreSQL to a SaaS CIAM tenant
  (Okta or equivalent). The Identity Service's event publishing to Kafka
  (`LoyaltyTierChanged`) must be replaced with webhook consumption from the new
  provider — or lost.
- **Cart Service** (line 13) is deleted. Session cart state in Redis is
  replaced by commercetools or equivalent. Every cart mutation path in the
  Gateway (line 36: `gRPC getActiveCart`) is re-wired to a SaaS REST API.
- **Checkout Service** (line 14) is deleted. The fulfillment state machine,
  Stripe orchestration, and SendGrid dispatch must be rebuilt as a BFF
  composition layer over the SaaS checkout API. The `OrderPlaced` →
  `OrderFulfilled` event chain is now vendor-mediated — Meridian no longer
  owns the event stream.
- **Order Event Bus** (line 15) becomes optional. If the SaaS primitives emit
  webhooks, the Kafka log may be demoted to an internal analytics sink rather
  than the platform spine. The Approach B extraction pathway closes — no event
  log means no event-sourced service decomposition.
- **Order Database** (line 17) becomes a read-replica at best. Order
  write-ownership moves to the SaaS checkout provider. Meridian's database
  becomes a cache of vendor data, not the system of record.
- **Inventory Read Cache** (line 16) survives but its population path changes:
  no Cart Service to read from it — the SaaS cart must be taught to query
  Meridian's Redis, or the cache must be exposed as an API the SaaS vendor
  calls. Either way, the clean RESP/TCP path (line 39) becomes a cross-vendor
  integration.
- **Every gRPC edge inside the boundary** (lines 35–43) is deleted and replaced
  with vendor REST API calls. Latency, error semantics, and retry behavior
  change on every path.
- **Team:** 6–10 engineers familiar with the monolith codebase are partially
  displaced by vendor management and integration engineering.

**Estimated reversal cost:** 12–18 months. This is not a refactor — it's a
replatform. The monolith's internal module boundaries don't map 1:1 to SaaS API
boundaries, so the Gateway BFF must be rewritten to compose vendor calls, and
every data migration (customer profiles, order history, cart state) crosses a
trust boundary.

---

## Decision 2: Apache Kafka as the Event Backbone

**Where it appears in the diagram:**
- `ContainerQueue(eventbus, "Order Event Bus", "Apache Kafka")` — line 15
  - Described as: "Immutable event log for all commerce actions…
    Backbone for eventual service extraction to Approach B."
- Three publishers: Cart Service (line 40), Checkout Service (line 41),
  Identity Service (line 42)
- Events named on the edges: `CartItemAdded`, `CartItemRemoved`,
  `CartAbandoned`, `OrderPlaced`, `PaymentAuthorised`, `PaymentCaptured`,
  `OrderFulfilled`, `CustomerRegistered`, `LoyaltyTierChanged`,
  `ConsentUpdated` — 10 distinct event types across 3 producers

**What this decision committed to:**
Kafka is the asynchronous integration backbone. All cross-service state
propagation goes through the log. No service calls another service's API
directly for state changes. The log is the planned extraction surface for
decomposing the monolith into independent services (Approach B pathway).

**What reversal costs — three reversal scenarios:**

*Reversal A — No event bus (services call each other directly):*
- Every `Kafka/TCP` edge (lines 40–42) becomes a synchronous gRPC or REST call.
  Cart Service calls Checkout Service directly when an order is placed.
  Identity Service calls Cart Service when a loyalty tier changes. The
  monolith's clean compile-time module boundaries degrade into runtime spaghetti
  — every service depends on every other service's availability.
- The Approach B extraction pathway closes. Without an event log, there is no
  mechanism to decouple services at migration time — extraction requires
  synchronous API contracts that didn't exist in the monolith.
- Audit trail is lost. The event log was the answer to "show us exactly what
  happened and when" for GDPR/FTC/APPI compliance. Without it, audit must be
  reconstructed from database snapshots and API logs — a different and weaker
  evidence model.

*Reversal B — Cloud-native queue instead of Kafka (SQS/SNS, Google Pub/Sub):*
- Kafka's immutable, replayable log becomes an ephemeral queue with message
  retention limits. Event replay for debugging or projection rebuild is not
  possible — once a message is consumed and acknowledged, it's gone.
- Event ordering guarantees change. Kafka's partition-key ordering (all events
  for one cart arrive in order) is not replicated by a standard queue. Cart
  state projections may process `CartItemRemoved` before `CartItemAdded`.
- The "eventual service extraction" pathway weakens: cloud queues don't support
  the compacted-topic pattern that lets a new service catch up by reading the
  full history.

*Reversal C — Change-data-capture (CDC) on the database instead of
application-level events:*
- Events are database row changes (`INSERT`, `UPDATE`, `DELETE`), not domain
  events (`OrderPlaced`). The semantic gap between "a row changed" and "an
  order was placed" must be bridged by every consumer. Downstream services
  couple to the database schema, not to a stable event contract.
- Event versioning becomes database schema versioning — a much harder problem.
  Adding a column to the orders table should not break the loyalty points
  consumer, but with CDC, it does.

**Estimated reversal cost:** 6–9 months for any of the three reversals. Every
service must change its outbound interface. Every consumer must change its
inbound pattern. The event schema registry (10 event types) must be migrated or
discarded. The extraction pathway to Approach B either closes or must be
redesigned around the new topology. If reversal happens after production data
exists in Kafka, the log must be drained and replayed into the new system
without data loss — a migration within a migration.

---

## Decision 3: Auth0 as the Customer Identity Provider

**Where it appears in the diagram:**
- `System_Ext(auth0, "Auth0", "Customer identity — SSO, social login, MFA,
  GDPR consent management, cross-country tenant federation.")` — line 23
- `Rel(customer, auth0, "Logs in, registers, resets password via hosted login
  page", "OAuth 2.0 / OIDC")` — line 28
- `Rel(gateway, auth0, "Validates access tokens at API entry", "OAuth 2.0 /
  OIDC")` — line 49
- `Rel(identity, auth0, "Resolves detailed user profile claims and consent
  records", "OAuth 2.0 / OIDC")` — line 50
- Gateway description: "Validates Auth0 access tokens at entry" — line 11
- Identity Service description: "Validates and resolves user profile claims
  against Auth0" — line 12

**What this decision committed to:**
All customer authentication flows through Auth0's hosted login page. Token
validation at the API gateway is Auth0-specific (JWKS endpoint, issuer URL,
claim namespacing). The Identity Service resolves profiles against Auth0's
Management API. GDPR consent records live in Auth0. Cross-country SSO uses
Auth0's tenant federation model. Every customer-facing surface (web, mobile)
and every machine client (POS terminal browser) depends on Auth0's SDK and
token format.

**What reversal costs — switching to another CIAM (Okta, Azure AD B2C,
or building in-house):**

- **Every customer must re-register or be migrated.** Auth0 stores hashed
  passwords, MFA enrollments, and social login linkages. None of these
  transfer cleanly to another provider. The migration is either: (a) a
  forced password reset for every Meridian customer across 22 countries, or
  (b) a custom migration bridge that proxies Auth0 during a transition window
  while gradually migrating users — a 6–12 month dual-run.
- **Token validation changes everywhere.** The Gateway's token validation
  (line 49) is coded against Auth0's JWKS endpoint, issuer URL, and claim
  format (`permissions` claim, `sub` format). A new provider means a new SDK,
  new claim namespacing, and new token introspection patterns. Every service
  that checks a JWT claim must be updated.
- **GDPR consent records must be migrated.** Auth0 stores consent grants
  (marketing opt-in, cookie consent, data processing consent). These are
  regulatory records — losing them during migration is a GDPR violation. The
  migration must preserve consent timestamps, scope, and withdrawal history
  for every customer.
- **Cross-country tenant federation must be rebuilt.** Auth0's multi-tenant
  model (one tenant per region with cross-tenant federation) is Auth0-specific.
  Okta uses a different org/domain model. Azure AD B2C uses a different tenant
  structure. The "French customer logs into German site" flow must be
  re-architected for the new provider's federation model — or abandoned and
  replaced with per-country identity silos.
- **Mobile and web SDKs change.** The Meridian mobile app (React Native, line
  10) and web app (Next.js, line 9) use Auth0's SDK for login, token refresh,
  and session management. Switching providers means new SDK integration, new
  token storage patterns, and a forced app update for every mobile user.
- **If building in-house:** The identity service moves from a thin
  profile-resolver (line 12) to a full CIAM — password hashing, MFA, social
  login OAuth flows, brute-force protection, session management, GDPR consent
  UI. This is not a migration; it's building a product Auth0 already built.
  The compliance surface (GDPR, APPI, CCPA) moves from Auth0's SOC 2 report to
  Meridian's own audit scope.

**Estimated reversal cost:** 9–15 months for a CIAM migration with customer
impact (forced password resets). 18–24 months if building in-house. This is the
single highest-cost reversal in the diagram because it touches every customer
and every service boundary simultaneously — it's not an architectural change,
it's a customer-facing identity event.

---

## Summary

| Decision | Where in diagram | Reversal cost | What breaks |
|----------|-----------------|---------------|-------------|
| **1. Build (Monolith)** | `System_Boundary` + 6 internal `Container()` declarations + all gRPC edges | 12–18 months | Replatform, not refactor. Every service replaced by SaaS API. Data migration across trust boundaries. |
| **2. Kafka event backbone** | `ContainerQueue(eventbus, "Apache Kafka")` + 3 publisher edges + 10 event types | 6–9 months | Every cross-service communication path. Event schema migration. Approach B extraction pathway closes. |
| **3. Auth0 identity** | `System_Ext(auth0)` + 3 OAuth edges + Gateway/Identity descriptions | 9–15 months (migrate) / 18–24 months (build) | Every customer re-authenticates. Every token validation path. GDPR consent record migration. Mobile app forced update. |

**None of these three decisions should be reversed without a forcing event**
(acquisition, regulatory mandate, vendor end-of-life). They are load-bearing.
Every other decision in the diagram — database choice, cache technology, BFF
framework, email provider — can be reversed inside a quarter without customer
impact. These three cannot.
