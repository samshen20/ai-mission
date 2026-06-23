# 04 — Strategic Canvas: Meridian Retail Group Omnichannel Commerce Platform

## 1. Customer Problem / Pain Point

> *Meridian serves customers across 22 countries through 12 apps, 22 websites, and 1,400 stores — but these channels don't recognize the customer or each other.*

**Core pain:** A customer who browses on the JP mobile app, adds to cart, then visits an EU store cannot see their cart, their loyalty points, or get personalized recommendations that reflect their cross-channel behavior. Each channel feels like a different retailer.

**Evidence:**
- Industry-wide fragmentation tax: $2.7B/year lost globally (Signal 6)
- Data silos: $6.8M average annual productivity loss from integration challenges (Signal 2)
- Only 7% of retailers have solved this problem (Manhattan 2026 Benchmark)
- Adding a new channel today requires a "rebuild" not "configuration" (Signal 1)

**Who feels it most:**
- **Customers:** Fragmented experience, lost carts, unrecognized loyalty, generic recommendations
- **Marketing:** Inability to attribute cross-channel conversion, 15–25% advertising waste
- **Operations:** Inventory and fulfillment break at scale across regional systems
- **Legal/Compliance:** Regional privacy regimes managed ad-hoc rather than architecturally

---

## 2. Solution Concept

> *A headless, composable commerce platform unifying identity, cart, and loyalty across all 35+ Meridian touchpoints, with regulatory compliance baked into the architecture layer (not bolted on), deployed via strangler pattern over 18 months.*

**Key architectural principles:**
1. **MACH-compliant** — Microservices, API-first, Cloud-native, Headless
2. **Build to GDPR, localize exceptions** — EU baseline covers ~80% of global regulatory obligations
3. **Strangler pattern** — never Big Bang; each country cut over independently with rollback capability
4. **OAuth 2.0-native** — OIDC for customer identity, enabling agentic commerce readiness (Google UCP, Talon.One UIP)
5. **Data-governance-first** — CDP + governed common data model before API layer

**Not solving:** Physical logistics/3PL, manufacturing/procurement, HR/finance, real estate.

---

## 3. Key Metrics (Success Criteria)

| Metric | Baseline (Est.) | Target (18 mo) | Measurement |
|--------|----------------|----------------|-------------|
| Cross-channel cart recovery rate | ~0% (no shared cart) | ≥15% of abandoned cart users recover across channels | Analytics platform |
| Unified loyalty enrollment | Siloed per country | ≥60% of loyalty members visible across ≥2 channels | CIAM + loyalty engine |
| Repeat purchase rate (unified members) | Siloed baseline | ≥25% higher than non-unified members | CDP attribution |
| Data subject request (DSAR) response time | Unknown / ad-hoc | ≤30 days (GDPR compliant), automated ≥80% | CMP + identity layer |
| New market/channel integration time | 6–12 months (rebuild) | ≤4 weeks (configuration) | Engineering velocity metric |
| Customer identity dedup accuracy | Unknown | ≥98% match rate across countries | CDP dedup quality metrics |
| Advertising waste reduction | 15–25% (industry) | ≤10% | Campaign attribution |
| Regulatory fine exposure | Full exposure | Compliant posture across EU/JP/US | Audit / regulatory filing |

---

## 4. High-Level Architecture (Phase 1 — Foundation, Months 1–6)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDN / Edge Layer                              │
│  (Cloudflare/Akamai/Vercel Edge — geo-targeted consent at edge) │
├─────────────────────────────────────────────────────────────────┤
│                   API Gateway / GraphQL Layer                    │
│     (Apollo Federation / Zuplo / Kong — unified API surface)     │
├────────┬────────┬────────┬────────┬────────┬────────┬──────────┤
│        │        │        │        │        │        │          │
│  CMP   │ CIAM   │ Loyalty│ Cart   │ Catalog│ Search │  Order   │
│ (One-  │ (Okta/ │ Engine │ Service│ Service│ (Algo- │ Service  │
│  Trust)│ Auth0) │(Talon. │        │(commer-│ lia)   │ (Read-   │
│        │        │ One)   │        │ cetools│        │  Only)   │
├────────┴────────┴────────┴────────┴────────┴────────┴──────────┤
│                     CDP / Data Layer                             │
│            (Segment / mParticle — Identity Resolution)          │
├─────────────────────────────────────────────────────────────────┤
│                Integration / Middleware Layer                    │
│   (Legacy country systems — each with an adapter/strangler)      │
├─────────────────────────────────────────────────────────────────┤
│  Country   │  Country   │  Country   │  Country   │    POS      │
│  System 1  │  System 2  │  System N  │  System 22 │  (1,400)   │
└────────────┴────────────┴────────────┴────────────┴────────────┘
```

**Phase 1 builds:** CMP (UC-04), CIAM (UC-01), and OAuth 2.0 endpoints (UC-08 prerequisite).
**Phase 2 builds:** Loyalty engine (UC-03), cart service (UC-02), CDP data unification (UC-07 prerequisite).
**Phase 3 builds:** Headless storefront per country (UC-05), AI personalization (UC-07), data governance (UC-10).
**Phase 4 builds:** POS middleware (UC-12), unified order management (UC-09), real-time inventory (UC-06).

---

## 5. Stakeholders & Impact

| Stakeholder | Current State | Desired Future State | Change Impact |
|-------------|--------------|---------------------|---------------|
| **CIO** | $42M accountable; regulatory exposure; legacy complexity | One platform; compliant; predictable cost profile | Delivery governance; vendor selection |
| **CMO / CCO** | 22 independent marketing stacks; 15–25% ad waste; no cross-channel attribution | Unified customer view; consistent brand; AI-driven personalization; lower CPA | KPIs recalibration; marketing ops redesign |
| **Regional MDs (EU/JP/US)** | Local autonomy + local compliance burden | Global platform + local compliance confidence; local P&L visibility | Fear of losing local control — needs clear regional autonomy hooks |
| **CTO** | Multiple legacy platforms; high integration cost; slow to ship | MACH architecture; feature velocity; API-first engineering culture | Talent strategy; vendor selection; architecture governance |
| **DPO / Legal** | Ad-hoc compliance; manual DSAR; unknown data flows | Compliant-by-design; automated DSAR; full data flow map | Needed from Day 0; must have budget for data flow mapping |
| **Customers** | Fragmented; no loyalty recognition across channels | Seamless; recognized everywhere; loyalty works globally | Communication strategy (opt-in/notification) |

---

## 6. Key Assumptions (Each with a Number or Threshold)

1. **≥30% of Meridian's customers currently shop across ≥2 channels** — without this, shared identity ROI is limited. Validate with existing analytics before proceeding past Phase 1.
2. **Data quality across country systems permits ≥90% identity match rate** — if match rate is <90%, the unified profile (UC-01) foundation is unreliable and all downstream use cases suffer.
3. **≥5 in-house senior engineers with event-driven / API-first architecture experience exist or can be hired within 3 months** — if not, a partner-led delivery model is required (adds 15–20% cost).
4. **POS API availability is ≥60% of top 200 stores** — if <60% of high-volume stores lack API-capable POS, the POS integration layer (UC-12) needs a custom middleware build, delaying cross-channel cart persistence for in-store touchpoints.
5. **GDPR compliance is ≥70% complete in EU countries today** — if Meridian is starting from zero GDPR compliance, the compliance layer (UC-04) foundation timeline is 6–9 months, not 8–12 weeks.
6. **Country-level resistance to data centralization will affect ≤3 of 22 countries** — if >3 MDs push back on sharing customer data, the unified profile initiative faces political barriers that delay adoption regardless of technical readiness.
7. **$42M budget includes a 15% contingency reserve ($6.3M)** — if contingency is <10%, the program is undercapitalized for the integration surface area (22 countries + 1,400 POS).

---

## 7. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data quality too poor for reliable identity resolution | Medium | Critical | Run data quality audit before Phase 1 funding decision; set minimum match rate threshold (≥90%) as a Phase 1 go/no-go gate |
| Country MD resistance to data centralization | Medium | High | Governance model that lets countries retain data ownership and opt into shared identity; regional autonomy hooks in architecture |
| POS integration surface area larger than scoped | High | Medium | POS pilot in top 50 stores first; don't promise 1,400 store integration in Phase 1 |
| Insufficient engineering talent for composable architecture | High | High | Partner-led delivery for Phase 1 (systems integrator with MACH experience); parallel build internal capability |
| Regulatory fragmentation creates compliance conflicts (US opt-out vs EU opt-in) | Medium | High | Build-to-GDPR baseline; rely on geo-targeting at CDN/edge for conflicting requirements; engage external privacy counsel per region |
| AI personalization disappoints due to "automating a fragmented backend" | Medium | Medium | Defer ML-based personalization (UC-07) to Phase 3; start with rules-based; only graduate to ML after UC-01 demonstrated healthy for ≥6 months |
| Schedule slip beyond 18 months | High | Medium | Phase 0 readiness assessment; 8–12 week POC; per-market cutover with independent go/no-go; rollback plan at every stage |

---

## 8. Economic Model / Unit Economics

| Driver | Conservative | Base | Optimistic |
|--------|-------------|------|------------|
| Cross-channel revenue uplift | +3% | +7% | +12% |
| Marketing efficiency (waste reduction) | -5% waste | -12% waste | -22% waste |
| Operations cost reduction (IT ops) | -8% | -15% | -25% |
| Loyalty member CLV increase | +10% | +20% | +35% |
| Regulatory fine avoidance | $5M | $25M | $100M+ |

See 05-roi.xlsx for full three-scenario model.

---

## 9. Regulatory Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Geo-Detection (CDN Edge)                   │
│     Maps visitor to jurisdiction → serves consent rules      │
├─────────────────────────────────────────────────────────────┤
│  EU Path         │  JP Path           │  US Path             │
├───────────────────┼───────────────────┼──────────────────────┤
│  Opt-in (GDPR)   │  Opt-in + notice  │  Opt-out (CCPA)      │
│  Consent Mode V2 │  (APPI 2026 amend)│  GPC signal required │
│  DSA disclosures │  Cross-border     │  State-by-state map  │
│  SCCs for xfer   │   transfer rules  │  CPRA enforcement    │
└───────────────────┴───────────────────┴──────────────────────┘
```

**Key design decision:** Consent signals from CMP must propagate through the entire API chain to every downstream service (loyalty, cart, personalization, analytics). Google Consent Mode v2 signals (`ad_user_data`, `ad_personalization`) are mandatory for any EU traffic using Google services.

---

## 10. Decision Log (to be kept live throughout program)

| Decision | Options | Recommended | Owner | Status |
|----------|---------|-------------|-------|--------|
| Commerce Engine | commercetools / Shopify Plus / BigCommerce / Saleor / Adobe Commerce | **commercetools** (most mature composable for enterprise multi-country) | CTO | ⏳ Pending |
| CIAM Provider | Okta / Auth0 / MojoAuth / Azure AD B2C | **Okta** (strongest multi-country deployment pattern; BeyondID case study) | CTO/CIO | ⏳ Pending |
| CMP Vendor | OneTrust / Cookiebot / Usercentrics / Osano | **OneTrust** (enterprise market leader; proven geo-targeted deployment) | DPO | ⏳ Pending |
| CDP Layer | Segment / mParticle / Treasure Data | **mParticle** (stronger identity resolution for retail) | CTO/CMO | ⏳ Pending |
| Loyalty Engine | Talon.One / LoyaltyLion / Yotpo / Antavo | **Talon.One** (UIP compatibility + real-time API maturity) | CMO | ⏳ Pending |
| Frontend Framework | Next.js / Remix / Nuxt / Hydrogen | **Next.js** (widest SSR ecosystem; Vercel edge deployment) | CTO | ⏳ Pending |
| API Gateway | Kong / Zuplo / Apollo Federation / AWS API GW | **Zuplo** (edge-native; built-in CORS/compliance policies) | CTO | ⏳ Pending |
| SI Partner | Accenture / Publicis.Sapient / Thoughtworks / Valtech | **Depends on geography and composable experience** | CIO | ⏳ Pending |
| Phase 1 Pilot Country | Choose 1 low-complexity EU country | — | Steering Committee | ⏳ Pending |
