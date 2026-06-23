# Onboarding Baseline 

**Date:** 2026-06-15 
**Name:** Samuel Shen 
**Role:** Quality 
**Primary skill (Deep role):** Quality 

## Maturity Self-Read (project: Omnichannel Commerce Platform for a Global Retailer) 

| # | Dimension | Level (L1 / L2 / L3) | Evidence (one sentence) | 
|---|-----------|----------------------|-------------------------| 
| 1 | AI Capabilities | L2| engaged Copilot, shared skills| 
| 2 | Reusability | L2| Skills are used| 
| 3 | AI Champions | L1| no named perple drive AI adoption on the team| 
| 4 | Performance Tracking | L1| no enough data to measure performance| 
| 5 | DAU (Daily Active Use) | L2| all the team members are using AI| 

**Weakest dimension:** [Name + one sentence why] 

## What I Expect From This Course [Learn how to engage AI in real project] 

## Tool Setup 

| # | Tool | Verified? (Y/N) | 
|---|------|------------------| 
| 1 | Chat assistant (DIAL): one prompt run | Y| 
| 2 | IDE + coding agent: one AI completion accepted | Y| 
| 3 | Claude via CodeMie: one message routed | Y| 
| 4 | DIAL API key: one model call succeeded | N| 

## Running Case 
### The project
MRG grew through acquisitions: each region runs its own e-commerce stack (some Shopify, some bespoke .NET), its own mobile app, and its own loyalty program. There is no unified customer identity, no shared inventory view between online and store, and no shared promotions engine. The board approved an 18-month program to consolidate onto a single headless commerce platform with one customer identity, one cart, one loyalty program, and a live inventory view across channels.
Discovery wrapped two months ago. Phase 1 (unified identity + cart + checkout) is being built now. Phase 2 (loyalty + cross-channel inventory) starts in month 8. Phase 3 (ML personalization, marketing automation) starts in month 14. There is no acceptable downtime window — stores must keep selling throughout.
### Team
~80 people across three SIs and MRG. Six product squads (8–10 people each), one BA cell (4 people), one QA chapter (2 leads + 8 engineers), one architecture team (1 lead + 3), two PMs, one delivery manager, three embedded designers. Mixed seniority — about a third of the squad engineers are mid-level or junior.

### Tech stack
Legacy (per region, varies): Shopify Plus, custom .NET monoliths, Magento 2, on-prem Oracle DBs, SAP ECC for inventory and finance, region-specific CRMs (Salesforce, Hubspot, Dynamics).
Target platform: commercetools (headless commerce), Apollo GraphQL gateway, microservices on AWS EKS, Kafka for eventing, React Native for mobile, Next.js for web, Auth0 for identity, Segment for CDP.
Data layer: Snowflake for analytics, dbt for transformations, MRG keeps SAP as inventory ground truth (read-only sync to platform).

**Gut-check:** [Value hypothesis, a user-facing surface, a codebase, data, a team context — note any gaps.]