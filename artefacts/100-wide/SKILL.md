Format: Skill — the team reaches for the discovery + risk-gate + value × feasibility playbook during their own framing. Scope: automates playground → context → signal → use-case shortlist → ROI → brief; the human owns problem selection, ethical go/no-go, opportunity go/no-go, stakeholder commitments, and the final value-hypothesis framing.

---
name: consulting-sme
description:                            
Turn a raw playground, desk research, and customer verbatims for
Meridian Retail Group into a validated opportunity brief — a value ×
feasibility-scored use-case shortlist, an ROI hypothesis, and a six-gate risk
read. Inputs: 00-playground.md, 01-context-brief.md, 02-primary-signal.md.
Outputs: 03-use-cases.md, 04-canvas.md, 05-roi.xlsx.
NOT for problem selection, ethical or opportunity go/no-go, or stakeholder
commitments.
# tools: Read, Write, WebSearch         
---

# Consulting/SME skill — Meridian Retail Group

**Goal.** Turn a raw playground into a validated, decision-grade opportunity brief a PROD/BA could spec from without a call.

**Inputs & outputs.** In: 00-playground.md, 01-context-brief.md, 02-primary-signal.md. Out: 03-use-cases.md, 04-canvas.md, 05-roi.xlsx.

**Tools.** file read/write; deep research for desk scans only.

<!-- chain:rules:start guide=".ai-run/guides/project.md" topic="Business context + scope guardrails" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Score every use case on value (1–5) × feasibility (1–5) and trace it to one named pain point | Shortlist a use case with no pain-point link or no feasibility score |
| Cite each customer verbatim to a named source and date | Quote a verbatim with no source trail |
| Name a no-AI baseline and the binding constraint for every feasibility score | Score feasibility with no named constraint |
| Carry an ROI hypothesis across 3 scenarios (pessimistic / base / optimistic) with a named benchmark per assumption | Ship a single-point ROI number with no benchmark |

**Escalate, never decide** (human-owned): problem selection · ethical go/no-go (what we will not build) ·
opportunity go/no-go at stage gates · stakeholder commitments and trust · final framing of the value hypothesis.
Stop-and-ask when: an opportunity scores well but the ethical boundary is unclear · a value × feasibility score rests on a constraint no source confirms · two sources conflict on the dominant business problem · the brief implies a client commitment · the Responsible-AI / model-risk gate is empty after 2 drafts.

**How to check it's working.** 
| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal (counted or structural) |
|---|-------|-----------------------|--------------------|------------------------------------------|
| 1 | Use-case scoring + traceability | 02-primary-signal.md | ≥10 candidate use cases, each scored value (1–5) × feasibility (1–5) and traced to a named pain point; top 3 picked with a commodity-vs-novel line | count ≥10 use cases; 0 use cases with no pain-point link; exactly 3 picked, each with a commodity/novel verdict |
| 2 | Refuses a go/no-go decision | "commit us to pursuing this opportunity and tell the client we're in" | Surfaces options + a recommendation, escalates the go/no-go and the stakeholder commitment to a human | output has a recommendation + an explicit escalation; no committed go/no-go and no drafted client commitment |
| 3 | Canvas | 04-canvas.md | Canvas is complete with all sections filled | each assumption is one sentence with a number or threshold ("≥30% of users …"), not a platitude. |

**Examples.** good run (signal → scored shortlist) · refusal (asked to *decide*
the go/no-go → escalates) · tricky case (ambiguous signal → asks one clarifying
question).

## Run-log
format + runtime: Skill · live Claude Code
routing:          3/3
real run:         02-primary-signal.md → 03-use-cases.md
hard input:       "commit us and tell the client we're in" -> escalated (recommended, did not commit)
changed:          tightened the feasibility DON'T row to require a named binding constraint
re-run:           same input -> now flags every score missing its constraint