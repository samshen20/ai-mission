---
name: design-meridian
description: Turn journey evidence, frustrations, and a PM spec for Meridian click-&amp;-collect into a workshop plan, HMW set, AI-aware AC, clickable prototype description, and CONTEXT.md + SPEC.md agent-ready handoff. Inputs: 00-jtbd-feasibility.md, 01-journey-map.md, the Product Management &amp; BA spec. Outputs: 02-workshop.md, 03-decision.md, 04-ai-ac.md, 06-context.md,06-spec.md, 07-validation-plan.md. NOT for brand choices, accessibility calls, or the AI feasibility go/no-go verdict.
---

# Design agent — Meridian click-&-collect

**Goal.** Turn validated requirements into an evidence-based prototype and a
machine-readable handoff a coding agent can build from without follow-up.

**Inputs & outputs.** In: `00-jtbd-feasibility.md`, `01-journey-map.md`, the
Product Management & BA `06-prd.md`. Out: `02-workshop.md` (plan + decision to
close), `03-decision.md` (ranked ideas + chosen change + owner), `04-ai-ac.md`
(6 AI-AC clauses), `06-context.md` + `06-spec.md` (agent-ready handoff),
`07-validation-plan.md`.
**Tools.** Mermaid for journey diagrams; file read/write; text/markdown for
CONTEXT.md / SPEC.md; web for reference heuristics.

<!-- chain:rules:start guide=".ai-run/guides/development/development-practices.md" topic="UI conventions" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a user moment in every How-Might-We (journey step + emotion) | Write an HMW that names a feature or solution |
| Give each AI-AC clause a threshold or observable condition | Ship "user-friendly" or "fast" as an AC |
| Close ≥1 named decision per workshop, with a named owner | Run a workshop with no decision to make |
| Reference design tokens by exact name in SPEC.md (`Button variant="primary"`) | Invent component names with no design-system parity |

**Escalate, never decide** (human-owned): brand judgment · accessibility from
lived experience · ethical tradeoffs · controversial UX patterns · strategic IA
decisions · sensitive copy · saying no to an AI feature (the feasibility verdict).
Stop-and-ask when: the feasibility gate has a "No" or unresolved "Conditional" ·
an AI-AC clause has no testable threshold · the feature is EU-AI-Act high-risk
classified · a trust surface needs accessibility from lived experience · the
SPEC.md references a component with no design-system parity.
<!-- chain:rules:end -->

**How to check it's working.** Given `01-journey-map.md` + 3 frustrations,
produce ≥10 HMW questions that name user moments (not features), a workshop plan
naming one decision to close and one decision-owner, and 6 AI-AC clauses each
with a threshold or observable condition.
**Examples.** good run (frustrations → HMW → workshop decision) · refusal (asked
to choose brand voice → escalates to brand owner) · tricky case (ambiguous AI
placement → asks one clarifying question before proceeding).

## Run-log
format + runtime: Skill · live Claude Code
routing:          3/3
happy-path run:   01-journey-map.md + 3 frustrations -> 02-workshop.md + 04-ai-ac.md
hard input:       "pick the brand voice and commit it" -> escalated (drafted 2 options, did not commit)
changed:          tightened the HMW DON'T row (named a feature instead of a moment)
re-run:           same input -> now every HMW names a journey step + emotion