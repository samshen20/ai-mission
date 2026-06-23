# Summary of architecture-meridian SKILL.md

**File:** `.claude/skills/architecture-meridian/SKILL.md`

---

## 1. Frontmatter (YAML header)
Declares the skill name `architecture-meridian`, a one-paragraph description of what it produces (four-layer context doc, three divergent options with scored choice, C4 L1+L2 pack, three ADRs, NFR budgets, pre-mortem), the expected inputs (`00-discovery-context.md`, design question, Design handoff), and the outputs. Also lists what the skill is NOT for: final option sign-off, irreversible cutover sequencing, PCI-scope decisions, or writing production code.

## 2. Goal
States the purpose: turn an ambiguous problem into options, a chosen direction with evidence, a C4 pack, and the ADRs and NFR budgets a delivery team can build against.

## 3. Inputs & Outputs (detailed)
Enumerates the concrete files in and out. Inputs: `00-discovery-context.md`, a one-line design question, and optionally the Design module's `06-context.md`. Outputs: `00-options.md` (three divergent options plus trade-off matrix plus choice), `01-context.mmd` + `02-containers.mmd` (C4 diagrams drawn only after the choice), `04-adr-001..003.md`, `06-nfrs.md`, and `07-adversarial.md` (fresh-session pre-mortem). Notes the tooling: Mermaid for diagrams, file read/write for the pack, web for C4 notation references.

## 4. Decision Rules (DO / DON'T table + escalation gates)
A prescriptive table with four rules:
- Generate ≥3 options differing on a load-bearing dimension before drawing any C4.
- Give every NFR budget a number, a window, and a test approach — never ship vague terms like "fast" or "scalable enough."
- Every ADR must carry an Agent-Readable Summary with an explicit "do-not" clause — not just a label.
- Ground every latency/cost figure in a cited reference range — never invent numbers.

Followed by a "Hand back to a human, never decide" list: final option choice, irreversible migrations & cutover sequencing, trust-boundary & PCI-scope placement, trade-off arbitration between competing concerns, and final acceptance of the architecture as build-ready. Lists five stop-and-ask triggers (PCI trust boundary crossing, untestable NFR, two options within one point, irreversible data migration, organisation-wide blast radius).

## 5. Verification Criteria ("How to check it's working")
Defines the expected shape of a good run: three options differing on a load-bearing dimension, a trade-off matrix, a chosen option with a two-sentence rationale, a C4 L2 matching that option, and three ADRs each with a "do-not" Agent-Readable Summary. Provides three examples: a good run, a refusal (asked to commit cutover → escalates), and a tricky case (brief names the solution → asks for the underlying problem first).

## 6. Run-log
Records operational metadata: format is a Skill run in live Claude Code, routing success rate (3/3), a happy-path run trace, a hard-input case where the skill correctly escalated rather than committing, a note that the "options before any C4" DO row was tightened, and confirmation that a re-run with the same input now emits options + choice before drawing the C4.
