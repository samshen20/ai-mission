# 00-discovery-context.md — Meridian Omnichannel Platform

**Source brief:** "Omnichannel Commerce Platform for a Global Retailer. Meridian
Retail Group unifies 22 country sites, 12 mobile apps, and 1,400 POS systems
into a single headless commerce platform with shared identity, cart, and loyalty
— 18 months, $42M, no Big Bang cutover, strict EU/JP/US regulatory layer."

**Date:** 2026-06-22
**Status:** Architectural discovery — extract, do not summarise

> Convention: direct quotes from the brief are in blockquotes. Inferences are
> marked **[Inferred]** and sourced to either the brief text or supporting
> Meridian artifacts in `300-wide/`.

---

## 1. Business Layer

> "Omnichannel Commerce Platform for a Global Retailer."

- **Revenue:** Not stated in the brief. **[Inferred]** A retailer operating
  1,400 POS systems across 22 countries is likely in the multi-billion-EUR
  revenue band; the $42M program budget is ~1–3% of annual revenue for a
  retailer of this scale.

> "Meridian Retail Group unifies 22 country sites, 12 mobile apps, and 1,400
> POS systems"

- **Market pressure:** Not stated. **[Inferred — from heuristic evaluation in
  `300-wide/02-heuristic-evaluation.md`]** Every assessed competitor fails at
  inventory transparency (H1 visibility, H2 real-world match). The unification
  is partly a competitive response: pure-play digital retailers (Amazon,
  Zalando) offer seamless cross-channel experiences that a fragmented
  22-country architecture cannot match. Consumers increasingly expect cart
  portability and loyalty recognition across borders.

- **Stakeholders:** Not enumerated in the brief. **[Inferred]** Country GMs
  (22 markets, each owning a local P&L), CTO/VP Engineering (platform
  delivery), Head of Digital (customer experience), Store Operations (1,400 POS
  endpoints), CFO ($42M budget owner), country-level legal/compliance officers
  (EU, JP, US).

> "shared identity, cart, and loyalty"

- **Success measure:** Not stated. **[Inferred]** The three named capabilities
  — identity, cart, loyalty — are the success criteria. When all 22 sites and
  12 apps operate on the shared platform with these three services live across
  all markets, the program is done. No revenue or NPS target is stated.

---

## 2. Product Layer

> "22 country sites, 12 mobile apps"

- **Customer-facing surfaces:** 22 country-specific web storefronts, 12 native
  mobile apps (likely iOS + Android across 6–12 markets — the mismatch between
  22 sites and 12 apps implies not all markets have a dedicated app).

> "1,400 POS systems"

- **Channels:** Web (22 sites), mobile (12 apps), physical POS (1,400
  terminals). The POS count signals a brick-and-mortar-heavy business — ~64
  stores per country on average. POS is both a sales channel and an integration
  surface.

> "shared identity, cart, and loyalty"

- **Key user moments (from the three named capabilities):**
  - **Identity:** Single sign-on across all country sites and apps. A shopper
    registered in France can log into the German site without re-registering.
  - **Cart:** Cross-channel cart persistence. A cart started on the mobile app
    is visible on the web storefront and (implied) at the POS.
  - **Loyalty:** Unified rewards program. Points earned in one country or
    channel are redeemable in any other.
  - **[Inferred — from `300-wide/01-journey-map-v2.md`]** Click & collect is a
    critical user moment spanning the web→POS boundary: the shopper checks
    availability online, the system queries SAP inventory via the headless
    platform, and the POS confirms pickup.

---

## 3. Engineering Layer

> "single headless commerce platform"

- **Target tech stack:** Not named in the brief. **[Inferred]** "Headless
  commerce" strongly implies MACH architecture (Microservices, API-first,
  Cloud-native, Headless). Likely candidates: commercetools, Elastic Path, or
  a custom API layer over a composable commerce core. The "single" qualifier
  means one logical platform, not necessarily one physical deployment (see
  Assumption 5).

> "no Big Bang cutover"

- **Migration pattern:** Strangler fig. The 22 sites, 12 apps, and 1,400 POS
  systems are migrated incrementally while coexisting with legacy systems. The
  headless platform must run in parallel with existing country-site backends
  during the transition window.

> "1,400 POS systems"

- **Legacy coexistence:** POS terminals in 1,400 physical stores. **[Inferred]**
  These run diverse on-premise or store-server software with varying network
  reliability. POS integration is likely the long pole: it touches payment
  hardware, receipt printers, barcode scanners, and local tax calculation — a
  higher change-risk surface than the web or mobile migration.

> 22 country sites, 12 mobile apps

- **Integration patterns (from the brief):**
  - **Identity federation:** OAuth 2.0 / OpenID Connect layer serving all
    surfaces. Likely a commercial CIAM (Customer Identity and Access
    Management) — Auth0, Okta, or Azure AD B2C.
  - **Distributed cart service:** A single cart API with regional edge
    deployments. Cart mutations must be eventually consistent across channels.
  - **Loyalty engine:** Event-sourced points ledger consuming purchase events
    from all channels. Must support country-specific earn/burn rules.
  - **API gateway:** Per-region gateways (EU, JP, US) routing to the shared
    commerce core, with country-specific adapters for local payment methods,
    tax engines, and fulfillment providers.

---

## 4. Regulatory Layer

> "strict EU/JP/US regulatory layer"

Every named regulation below carries a concrete architectural implication.

### EU

| Regulation | Architectural implication |
|---|---|
| **GDPR** (Regulation 2016/679) | Data residency controls per EU member state. Right-to-erasure must cascade across all services (identity, cart, loyalty, order history). Consent management platform required for cookies, marketing, and loyalty program enrollment. Cross-border data transfer mechanism needed for any data leaving the EU (SCCs or adequacy decision). |
| **PSD2 / Strong Customer Authentication** (Directive 2015/2366) | Payment flows must support SCA (two-factor authentication) for online transactions. The headless checkout must integrate with EU-mandated PSD2-compliant payment gateways. This is a payment architecture constraint, not a business preference — placed here in Regulatory per layer-hygiene rule. |
| **EU AI Act** (Regulation 2024/1689) | If product recommendations, search ranking, or inventory forecasting use AI/ML, they must be classified by risk tier. High-risk classification (e.g., AI used in pricing or credit for loyalty) triggers conformity assessment, human oversight, and transparency obligations. **[Inferred — from `300-wide/00-jtbd-feasibility.md`]** The confidence-model Phase 1 (availability percentage) touches this boundary. |
| **Digital Services Act** (Regulation 2022/2065) | Applicable if Meridian operates as a marketplace (third-party sellers). Requires seller traceability, content moderation reporting, and algorithmic transparency for推荐 systems. |

### Japan

| Regulation | Architectural implication |
|---|---|
| **APPI** (Act on Protection of Personal Information, amended 2022) | Requires consent for transfer of personal data to third parties and cross-border transfer restrictions. **[Inferred]** Japanese customer data may require domestic hosting or a Japan-specific data store, conflicting with a single global identity service. The APPI's cross-border transfer rules are stricter than GDPR's adequacy framework in some dimensions. |
| **Payment Services Act** | Regulates stored value and prepaid payment instruments. If Meridian operates a digital wallet or stored-value loyalty points redeemable as currency, this triggers licensing requirements in Japan. |

### US

| Regulation | Architectural implication |
|---|---|
| **CCPA/CPRA** (California) + state privacy patchwork | No federal privacy law; 13+ states have enacted their own (CA, VA, CO, CT, UT, TX, OR, etc.). The platform must support per-state opt-out mechanisms, data subject access requests, and sensitive data classifications. A single US privacy toggle is insufficient — the compliance layer must be state-aware. |
| **PCI DSS** (v4.0, in effect March 2025) | Payment card data must never touch Meridian servers in plaintext. Tokenization at the payment gateway boundary. SAQ or ROC depending on transaction volume. The headless checkout's iframe/tokenize-then-charge pattern must be consistent across all 22 country sites. |
| **FTC Act Section 5** | Prohibits unfair or deceptive practices. **[Inferred — from `300-wide/04-ai-ac.md` AI-AC6]** The binary "In stock" badge that overpromises shelf availability is an FTC Act exposure if a US shopper relies on it and the item is absent. The freshness indicator (Phase 0a) mitigates this by replacing the guarantee with a timestamped data point. |
| **ADA / Section 508** | The 22 country sites and 12 mobile apps must meet WCAG 2.1 AA. A headless frontend with a shared component library can enforce accessibility at the platform level — but only if the design system includes a11y from the start. |

---

## 5. Five Architecturally Significant Assumptions Not Stated in the Brief

For each: hint from the brief → assumption → what breaks if wrong.

### Assumption 1 — Platform convergence, not orchestration

> "unifies 22 country sites…into a single headless commerce platform"

**Assumption:** The 22 country sites run on a small enough set of underlying
commerce engines (ideally 2–4, e.g., SAP Hybris + Magento + 1–2 custom stacks)
that "single platform" can mean one API-driven commerce core, not one
orchestration layer federation-over 22 heterogeneous backends.

**What breaks if wrong:** If the 22 sites span 8+ different commerce engines
with incompatible product catalogs, pricing rules, and checkout flows, the
"single platform" becomes a federation/abstraction layer. The integration
surface quadruples — every shared service (cart, identity, loyalty) needs
per-backend adapters. 18 months becomes 36+, and $42M may only cover the
federation layer, not the unification.

---

### Assumption 2 — Cross-border shoppers justify shared cart and identity

> "shared identity, cart, and loyalty"

**Assumption:** A meaningful share of Meridian's customers (≥10–15%) shop
across country boundaries — a French customer buying from the German site,
or a traveler using loyalty points earned in one country at a store in another.
The shared cart and identity services exist because cross-border shoppers need
them, not because "shared" sounds architecturally elegant.

**What breaks if wrong:** If >90% of customers shop exclusively within one
country, the shared cart service adds cross-region latency to every cart
mutation with zero user benefit. GDPR data-residency complexity (a French
customer's cart touching a German-hosted service) is incurred for a user need
that doesn't exist. The architecture should have been single-region identity
and loyalty with an optional cross-border account-linking feature — a much
simpler system. The shared cart in particular may be an expensive architectural
bet with no customer-driven justification.

---

### Assumption 3 — POS systems support incremental re-pointing

> "no Big Bang cutover" (with "1,400 POS systems" as a named integration
> surface)

**Assumption:** Individual POS terminals can be progressively re-pointed from
their legacy country-site backend to the new headless platform via a
configurable routing layer (e.g., API gateway with header-based tenant routing
or store-ID→backend mapping). No simultaneous firmware or hardware update
across all 1,400 terminals is required. A store can migrate independently of
its neighbours.

**What breaks if wrong:** If POS terminals have hard-coded backend URLs in
firmware, use legacy protocols (ISO 8583, fixed-width flat files, or
vendor-proprietary TCP sockets), or require a full software image update to
change their backend endpoint, every POS migration becomes a store-level Big
Bang. The "no Big Bang" constraint fails at the physical retail layer — the one
layer where a failed cutover means a store that can't transact. This is the
highest-risk assumption in the brief because POS is the least abstractable
integration surface.

---

### Assumption 4 — The build-vs-buy decision is settled toward buy

> "18 months, $42M"

**Assumption:** Meridian has selected — or will select — a commercial headless
commerce platform (commercetools, Elastic Path, or equivalent) and a systems
integrator with prior headless-unification delivery at comparable scale. The 18
months reflects configuration + migration + integration of a bought platform,
not the build of a custom headless commerce core from scratch.

**What breaks if wrong:** If Meridian intends to build the headless platform
in-house (custom microservices for cart, checkout, catalog, pricing across 22
markets) with a newly assembled team, 18 months is not achievable. The $42M
burns on platform engineering rather than migration — the 22 sites remain on
legacy stacks while the new platform is still under construction at month 18.
This is the most consequential assumption in the brief because it gates the
entire timeline. A build decision makes this a 30–36 month program and requires
a different budget conversation.

---

### Assumption 5 — A single configurable compliance layer suffices

> "strict EU/JP/US regulatory layer"

**Assumption:** One compliance architecture — a policy-as-code rules engine
with region-tagged data storage directives — can satisfy EU, Japanese, and US
regulatory requirements without physically separate deployments per
jurisdiction. The differences between GDPR, APPI, and US state laws are
differences of configuration, not of architecture.

**What breaks if wrong:** If Japan's APPI requires all personal data of
Japanese residents to reside on servers physically located in Japan (data
localization), AND GDPR's transfer restrictions require EU resident data to
stay in the EEA, the "single platform" must be deployed across at least three
regional clusters with hard data-residency boundaries. The shared identity
service — which by definition holds data about all customers — must be
redesigned as a federated identity mesh with per-region stores and a
jurisdiction-aware routing layer. The shared cart and loyalty services face the
same fragmentation. The architecture shifts from "single platform with
compliance toggles" to "multi-region distributed system with per-jurisdiction
deployments." The $42M and 18 months were sized for the former, not the latter.

---

## Layer-Hygiene Notes

- **PSD2/SCA** is placed under Regulatory (EU), not Business — it constrains
  the payment architecture, not the business model.
- **PCI DSS** is placed under Regulatory (US, but global applicability), not
  Engineering — it is a compliance obligation, not an engineering choice.
- **FTC Act** exposure (deceptive "In stock" claims) is placed under Regulatory
  (US), not Product — the constraint on what the UI may claim is regulatory in
  origin.
- No duplicate items: each bullet in each layer states a distinct fact or
  inference. Where two bullets would paraphrase the same point (e.g., "GDPR
  applies" and "data privacy is regulated"), only the more specific one is kept.
