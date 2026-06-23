# 03 — Use-Case Shortlist: Scored & Ranked

## Scoring Framework

| Score | Value (Business Impact) | Feasibility (Technical + Organizational) |
|-------|------------------------|------------------------------------------|
| 5 | Unlocks >$50M/year or is a market-entry prerequisite | Proven at scale, internal capability exists, <3 months to MVP |
| 4 | Unlocks $10–50M/year or significant regulatory risk reduction | Commercially proven, some gaps to close, 3–6 months |
| 3 | Unlocks $1–10M/year or material CX improvement | Requires moderate engineering effort or external partner, 6–9 months |
| 2 | Unlocks <$1M/year or minor CX improvement | Experimental approach, significant unknowns, 9–12 months |
| 1 | Incidental benefit | High risk, unproven, or >12 months without clear path |

**Gate check applied to every use case:** ✓ Traced to named pain point in 02-primary-signal.md  
**Constraint named for every feasibility score** ✓

---

## Candidate Use Cases (≥10)

### UC-01: Unified Customer Profile — Single Identity Across All Touchpoints
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **5** | Prerequisite for cross-channel cart, loyalty, personalization, and regulatory compliance. Unlocks all downstream use cases. Fragmentation tax is $2.7B/year industry-wide (Signal 6). |
| **Feasibility** | **3** | Binding constraint: **Data quality across 22 country silos.** If each country has its own customer database with different schemas, deduplication and merge are non-trivial. Requires a CDP layer (Segment, mParticle) and governed common data model before CIAM integration (Okta/Auth0). Also requires OAuth 2.0 readiness (Signal 7). |
| **Pain Point** | **Signal 2, 6** | Data silos cost $6.8M/year; 80% of orgs cite them as top barrier. |
| **Overall Score** | **4.0** |  |

### UC-02: Cross-Channel Cart Persistence (Web → Mobile → In-Store)
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | Directly reduces cart abandonment, which averages 70–80% in retail. Even a 5% recovery translates to significant revenue. Cross-channel cart is the #1 request from unified commerce leaders. |
| **Feasibility** | **3** | Binding constraint: **POS integration surface area (1,400 systems).** Cart persistence on web/mobile is straightforward with shared identity + centralized cart service. Persistence to/in-store POS requires real-time APIs on legacy POS — many POS systems do not expose real-time cart APIs. Likely requires POS middleware layer. |
| **Pain Point** | **Signal 1** | "Adding a channel should feel like configuration, not a rebuild." |
| **Overall Score** | **3.5** |  |

### UC-03: Unified Loyalty Program — Single Tiers/Points/Benefits Across 35+ Touchpoints
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **5** | Loyalty members spend 2–5× more than non-members. Unified loyalty unlocks cross-country earning and redemption (e.g., earn in JP, redeem in EU). Also opens agentic commerce compatibility (Talon.One UIP — Signal 7). |
| **Feasibility** | **3** | Binding constraint: **Existing loyalty program maturity.** If Meridian runs 22 separate country loyalty programs with different rules, currencies, and tiers, consolidation is a multi-year data and business process project. Recommended scope: start with unified profile + single view of loyalty data (read), defer cross-country redemption (write) to Phase 3. |
| **Pain Point** | **Signal 3, 5** | Loyalty as commerce infrastructure; APPI compliance for Japanese members. |
| **Overall Score** | **4.0** |  |

### UC-04: Multi-Region Consent Management Platform (GDPR / APPI / CCPA)
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **5** | Regulatory non-compliance risk: GDPR fines >€5.5B cumulative (Signal 5). A single EU/JP regulatory failure could cost more than the entire $42M program. |
| **Feasibility** | **4** | Binding constraint: **Geo-location accuracy at CDN/edge.** CMPs like OneTrust/Cookiebot have proven integrations with headless architectures. The challenge is data flow mapping, not the CMP itself. |
| **Pain Point** | **Signal 5** | Build-to-GDPR baseline, APPI 2026 amendments. |
| **Overall Score** | **4.5** |  |

### UC-05: Headless Storefront for 22 Country Sites (Progressive Migration)
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | Foundation for brand consistency, localization, and SEO across 22 countries. The "strangler pattern" allows gradual cutover without Big Bang risk. |
| **Feasibility** | **3** | Binding constraint: **Engineering team maturity.** Composable requires 5+ senior engineers with event-driven and API-first skills (industry benchmark). If Meridian doesn't have this in-house, partner dependency adds timeline risk. |
| **Pain Point** | **Signal 1, 4** | "Heart transplant" complexity; John Lewis Partnership case study. |
| **Overall Score** | **3.5** |  |

### UC-06: Real-Time Inventory Visibility Across All Channels
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | Eliminates overselling, silent cancellations, and "order online, find out-of-stock in-store." Direct revenue impact and customer trust. |
| **Feasibility** | **2** | Binding constraint: **22 country PIM/ERP/OMS integration.** Each country has its own inventory system with different refresh cadences. Real-time reconciliation across 22 systems + 1,400 POS is extremely complex. Industry sources say this is where omnichannel "breaks at scale" (Signal 1). |
| **Pain Point** | **Signal 1** | "Omnichannel breaks at the inventory and fulfillment layer, not the storefront." |
| **Overall Score** | **3.0** |  |

### UC-07: AI Personalization Engine Across Shared Customer Profile
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | AI personalization drives 40% more revenue; personalized sessions show 369% higher AOV (industry data). |
| **Feasibility** | **4** | Binding constraint: **This requires UC-01 (unified profile) to be live first.** Once unified profile is in place, AI/ML layers (Bloomreach, Segment, internal) are proven at enterprise scale. |
| **Pain Point** | **Signal 2, 6** | "Fragmented backend → AI automates the mess." |
| **Overall Score** | **4.0** |  |

### UC-08: Agentic Commerce Compatibility (OAuth 2.0 / Google UCP / Talon.One UIP)
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **3** | Emerging — the total addressable commerce-through-AI-agents is still small in 2026 but growing fast. Early mover advantage with UCP/UIP. |
| **Feasibility** | **4** | Binding constraint: **OAuth 2.0 implementation in CIAM.** This is well-understood technology (Okta/Auth0/MojoAuth all support it). The risk is if Meridian's chosen identity vendor doesn't support OAuth 2.0 — but this would be a vendor selection error, not a technical limitation. |
| **Pain Point** | **Signal 7** | "Building a shared identity layer that doesn't support OAuth 2.0 would mean rebuilding within 12 months." |
| **Overall Score** | **3.5** |  |

### UC-09: Unified Order Management — View All Orders Across Channels
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | Customer-facing unified order history and status tracking. Reduces CS load, improves post-purchase experience. |
| **Feasibility** | **2** | Binding constraint: **22+ different OMS/ERP systems.** Each country likely uses a different order management backend. Unifying order data requires either: (a) all countries on one OMS (years-long effort), or (b) a centralized order aggregation layer with normalized schema. Both are high complexity. |
| **Pain Point** | **Signal 1, 2** | Fragmented commerce infrastructure. |
| **Overall Score** | **3.0** |  |

### UC-10: Cross-Border Data Flow Governance & Data Residency Mapping
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **4** | Growing regulatory requirement (EU DSA, China PIPL, JP APPI cross-border). Avoids €1B+ fines. |
| **Feasibility** | **3** | Binding constraint: **No single comprehensive data flow map exists today.** Most enterprises discover data flows they didn't know existed during the mapping process. 3–6 months for initial mapping, then ongoing governance. |
| **Pain Point** | **Signal 5** | GDPR/APPI/CCPA enforcement intensifying. |
| **Overall Score** | **3.5** |  |

### UC-11: Multi-Currency / Multi-Language / Localized Checkout
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **3** | Localized checkout drives conversion (especially Japan — native payment methods like Konbini, PayPay). |
| **Feasibility** | **3** | Binding constraint: **Payment gateway fragmentation.** 22 countries = likely 10+ different payment gateways. Local checkout composability is well-proven, but each integration is custom. |
| **Pain Point** | **Signal 1, 4** | "Lift-and-shift doesn't work." |
| **Overall Score** | **3.0** |  |

### UC-12: POS Systems Integration Layer (1,400 Stores)
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Value** | **3** | Enables in-store loyalty recognition, cross-channel cart visibility, and unified customer touchpoint. |
| **Feasibility** | **2** | Binding constraint: **POS vendor diversity.** 1,400 POS systems could mean 3–5+ different POS vendors with different API maturity. Many retail POS systems lack modern APIs — requires a middleware adapter layer (e.g., NewStore, own-built). |
| **Pain Point** | **Signal 1, 3** | 1,400 stores are the hardest surface area to integrate. |
| **Overall Score** | **2.5** |  |

---

## Ranked Shortlist (by Overall Score)

| Rank | UC ID | Use Case | Value | Feasibility | Overall |
|------|-------|----------|-------|-------------|---------|
| 1 | **UC-04** | Multi-Region Consent Management Platform | 5 | 4 | **4.5** |
| 2 | **UC-01** | Unified Customer Profile — Single Identity | 5 | 3 | **4.0** |
| 2† | **UC-03** | Unified Loyalty Program | 5 | 3 | **4.0** |
| 2† | **UC-07** | AI Personalization Engine | 4 | 4 | **4.0** |
| 5 | **UC-02** | Cross-Channel Cart Persistence | 4 | 3 | **3.5** |
| 5† | **UC-05** | Headless Storefront (Progressive Migration) | 4 | 3 | **3.5** |
| 5† | **UC-08** | Agentic Commerce (OAuth 2.0 / UCP) | 3 | 4 | **3.5** |
| 5† | **UC-10** | Cross-Border Data Flow Governance | 4 | 3 | **3.5** |
| 9 | **UC-06** | Real-Time Inventory Visibility | 4 | 2 | **3.0** |
| 9† | **UC-09** | Unified Order Management | 4 | 2 | **3.0** |
| 9† | **UC-11** | Multi-Currency / Localized Checkout | 3 | 3 | **3.0** |
| 12 | **UC-12** | POS Systems Integration Layer | 3 | 2 | **2.5** |

† Tied with the rank above.

---

## Top 3 Picks — Commodity vs. Novel

### 🥇 Pick 1: UC-04 — Multi-Region Consent Management Platform
| Verdict | **Commodity** — well-established solutions (OneTrust, Usercentrics, Cookiebot) |
|---------|---------|
| **Why it's #1** | Highest value × feasibility. Every other use case depends on compliant data handling. This is the **regulatory foundation** and must be built first. |
| **Implementation** | Vendor selection (OneTrust is enterprise market leader), geo-targeted CMP integration at CDN/edge. 8–12 weeks for initial deployment. |
| **Risk** | Underestimating data flow mapping effort (3–6 months for full map across 22 countries). |

### 🥇 Pick 2: UC-01 — Unified Customer Profile (Shared Identity)
| Verdict | **Commodity** — CIAM at this scale is proven (Okta, Auth0), but data quality across 22 silos is the novel challenge |
|---------|---------|
| **Why it's #2** | Prerequisite for cart (UC-02), loyalty (UC-03), and personalization (UC-07). The "keystone" use case. |
| **Implementation** | CDP layer first (Segment/mParticle for data unification and dedup), then CIAM layer (Okta/Auth0/MojoAuth for identity), then API layer (OAuth 2.0 / OIDC endpoints). |
| **Risk** | If Meridian underestimates country-level data quality and governance investment, the unified profile will be unreliable and all downstream use cases will fail. **This is the single highest-risk architectural dependency.** |

### 🥇 Pick 3: UC-07 — AI Personalization Engine
| Verdict | **Novel-ish** — personalization engines are commodity, but training on a truly unified 35+ touchpoint cross-channel dataset is rare |
|---------|---------|
| **Why it's #3** | Highest ROI potential after foundation is laid. Unified profile (UC-01) + loyalty (UC-03) create the richest first-party dataset in Meridian's history. AI on this dataset is a step-change. |
| **Implementation** | Phased: (1) rules-based cross-channel recommendations at launch, (2) ML models at Month 9–12, (3) real-time AI personalization at Month 15–18. |
| **Risk** | "AI on a fragmented backend automates the mess." UC-01 must be healthy before UC-07 produces reliable results. |

---

## Deferred Use Cases

| UC | Reason for Deferral | Trigger for Revisiting |
|----|---------------------|------------------------|
| UC-06 (Real-Time Inventory) | Feasibility 2 — requires 22 PIM/ERP integrations + POS middleware. | After UC-01 and UC-05 are live; phased rollout in highest-volume country first. |
| UC-09 (Unified Order Management) | Feasibility 2 — OMS fragmentation across 22 countries. | Defer to Phase 4; focus on order history display (read) before unified order operations (write). |
| UC-12 (POS Integration) | Feasibility 2 — 1,400 POS systems with unknown API maturity. | Start with a POS pilot in top 50 stores; validate integration pattern before scaling to 1,400. |

---

## Dependencies Map

```
UC-04 (CMP / Compliance) ── no hard dependencies ── BUILD FIRST
    │
    ▼
UC-01 (Unified Profile) ── depends on UC-04 for compliant data collection ── BUILD SECOND
    │
    ├──► UC-03 (Loyalty) ── depends on UC-01 for member identity
    ├──► UC-02 (Cart) ── depends on UC-01 for session persistence
    ├──► UC-07 (AI Personalization) ── depends on UC-01 for training data
    ├──► UC-08 (Agentic Commerce) ── depends on UC-01 OAuth 2.0 endpoints
    └──► UC-10 (Data Governance) ── feeds back into UC-04
             │
             ▼
       UC-05 (Headless Storefronts) ── consumes APIs from all above
```
