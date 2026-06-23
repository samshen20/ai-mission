# 00 — Playground: Meridian Retail Group Omnichannel Commerce Platform

## Raw brief

Meridian Retail Group (anonymized global retailer) is unifying **22 country sites**, **12 mobile apps**, and **1,400 POS systems** into a single headless commerce platform with shared identity, cart, and loyalty.

**Budget:** $42M  
**Timeline:** 18 months  
**Approach:** No Big Bang cutover — staged rollout  
**Regulatory layer:** EU (GDPR, Digital Services Act), Japan (APPI, Specified Commercial Transactions Act), US (state-level privacy incl. CCPA, CPRA)

### Known constraints / aspirations

- **Headless commerce** — decoupled frontend/backend; composable architecture
- **Shared identity** — single customer profile across all channels and countries
- **Shared cart** — cross-channel cart persistence (web → mobile → in-store)
- **Shared loyalty** — unified points, tiers, and redemption across all 35+ touchpoints
- **No Big Bang** — phased migration; each country/region cut over independently with a fallback mechanism
- **Multi-regulatory compliance** — EU, Japan, and US privacy/consumer protection baked into the architecture (not bolted on after)

### What is NOT in scope (from the brief)

- Physical logistics / supply chain systems (use existing 3PL integrations)
- Manufacturing / procurement (Meridian is a retailer, not a manufacturer)
- Internal HR / finance systems
- New store construction or real estate

### Known unknowns

- Existing tech stack (legacy monolith, middleware, current commerce platform?)
- In-house engineering capability vs. partner-led delivery
- Organizational readiness for headless and composable (change management)
- Current regulatory posture — are they already GDPR-compliant in EU? APPI-compliant in JP?
- Vendor / platform preferences ( commercetools? Shopify? composable? custom?)
- Integration maturity with existing POS vendors
- Customer data unification status (already have a CDP? master data management?)
- Current cart abandonment rates, cross-channel conversion leakage
- Whether "loyalty" means a new program or migrating an existing one

### Key personnel / stakeholders (hypothetical)

- **CIO** — accountable for $42M, timeline, regulatory compliance
- **CCO / CMO** — unified customer experience, loyalty, brand consistency
- **Regional MDs (EU, JP, US)** — local P&L owners, regulatory responsibility
- **CTO** — architecture decisions, platform selection, engineering approach
- **CDO / DPO** — data privacy, cross-border dataflows, consent management
- **VP Supply Chain** — API integration boundaries with existing 3PL systems
