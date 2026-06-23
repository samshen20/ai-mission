# ADR-003: Use Auth0 as the External Customer Identity Provider

## Context

Meridian's 22-country customer base requires SSO, social login, MFA, and GDPR
consent management across web, mobile, and POS channels. Building a CIAM
(customer identity and access management) system in-house means owning password
hashing, brute-force protection, social login OAuth flows, MFA enrollment and
recovery, session management, and GDPR consent UI — a product surface that is
well-understood commodity with severe regulatory consequences if implemented
incorrectly. The container diagram externalizes this surface:

```
System_Ext(auth0, "Auth0", "Customer identity — SSO, social login, MFA,
  GDPR consent management, cross-country tenant federation.")
Rel(customer, auth0, "Logs in, registers, resets password via hosted login
  page", "OAuth 2.0 / OIDC")
Rel(gateway, auth0, "Validates access tokens at API entry", "OAuth 2.0 / OIDC")
Rel(identity, auth0, "Resolves detailed user profile claims and consent
  records", "OAuth 2.0 / OIDC")
```

## Decision

We will use Auth0 as the external customer identity provider for all
authentication and consent management. Meridian SHALL NOT build password
storage, MFA, social login flows, or GDPR consent UI in-house. The Gateway
SHALL validate Auth0-issued access tokens at every API entry point. The
Identity Service SHALL resolve detailed user profiles and consent records
against the Auth0 Management API and cache the results in Meridian-owned
PostgreSQL for low-latency access during cart and checkout operations.

## Alternatives Considered

1. **Build identity in-house** — rejected because a self-built CIAM puts
   password hashing, brute-force detection, MFA enrollment, social login OAuth
   flows, and GDPR consent UI inside Meridian's audit scope. A breach of the
   in-house identity store is a regulatory event across three jurisdictions
   (GDPR, APPI, CCPA). The compliance surface of building identity exceeds any
   control or differentiation Meridian gains — customer login is not where
   Meridian wins against competitors. Additionally, building in-house delays
   the pilot country by 4–6 months (the time to build and harden a CIAM),
   violating the 18-month constraint.

2. **Alternative CIAM vendor (Okta, Azure AD B2C)** — considered but rejected
   because Auth0's cross-tenant federation model maps more directly to
   Meridian's 22-country structure (one tenant per region with federated cross-
   tenant SSO). Okta's org/domain model and Azure AD B2C's per-tenant user
   store require more custom federation code in the Identity Service to achieve
   the same "French customer logs into German site" flow. The decision is
   Auth0-first, not Auth0-exclusive — the OAuth 2.0 / OIDC standard at the
   Gateway boundary means the token validation path is provider-agnostic. A
   future CIAM migration would change the Identity Service's profile resolution
   implementation without changing the Gateway's token validation contract.

## Consequences

- **Positive:** Meridian inherits Auth0's SOC 2, ISO 27001, and GDPR compliance
  posture for the authentication surface. The pilot country goes live without
  Meridian building a login page, password reset flow, MFA enrollment, or
  consent management UI. Cross-country SSO (French customer on German site)
  works through Auth0's tenant federation — Meridian configures it, doesn't
  build it. The OAuth 2.0 / OIDC contract at the Gateway boundary decouples
  the CIAM vendor choice from every service behind the Gateway — services
  validate tokens, they don't know or care which provider issued them.

- **Negative:** Every Meridian customer's identity is stored in a third-party
  system. Auth0 becomes a critical production dependency — if Auth0 is
  degraded, Meridian customers cannot log in, add to cart, or check out on any
  channel. The Identity Service must cache profiles locally (PostgreSQL) to
  survive Auth0 Management API degradation during cart and checkout operations,
  but login itself has no local fallback. Additionally, GDPR consent records
  stored in Auth0 must be migrated if Meridian ever changes CIAM providers — a
  9–15 month migration with customer impact (forced password resets or a
  dual-run migration bridge). This is the highest-cost single-vendor reversal
  in the entire architecture.

## Agent-Readable Summary

No Meridian-owned service SHALL store a customer password hash, issue a
password reset token, enroll an MFA factor, broker a social login OAuth
handshake, or render a GDPR consent checkbox. Every authentication event —
login, registration, password reset, MFA challenge, social linkage, consent
grant — SHALL occur on Auth0's hosted login page, outside the Meridian
deployable boundary. The Gateway SHALL validate the JWT on every request by
fetching Auth0's JWKS; no request SHALL reach Cart, Checkout, or Identity
Service without a validated token. Identity Service SHALL cache resolved
user profiles and consent records in its local PostgreSQL store and SHALL
serve all Cart and Checkout profile requests from that cache — do NOT call
the Auth0 Management API synchronously during a cart read, cart mutation, or
checkout flow; the Auth0 Management API SHALL be called only on cache miss or
during the scheduled 5-minute TTL refresh. When the Auth0 Management API is
unreachable or exceeds a 200ms timeout, the Identity Service SHALL serve the
expired cache entry rather than failing the request — the response SHALL
include a `stale: true` flag so callers can decide whether staleness is
acceptable for their operation. The POS cart lookup (`resolveLoyaltyQr`)
SHALL accept profile staleness up to 300s; the GDPR consent check SHALL
require `stale: false` and fail closed if the cache is expired and Auth0 is
unreachable. Backend services (Cart, Checkout,
Loyalty) SHALL accept a normalized claims object from the Gateway — do NOT
import an Auth0-specific SDK, do NOT reference Auth0 claim namespaces, and do
NOT hard-code the Auth0 issuer URL in any service behind the Gateway. This
ensures a future CIAM migration replaces the Gateway's token validation
implementation and the Identity Service's profile resolution implementation
without a single code change in Cart, Checkout, or Loyalty.
