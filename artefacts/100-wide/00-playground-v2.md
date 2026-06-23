# Playground Template v2

**Lessons from Meridian Retail Group Case A (June 2026).** This template incorporates upstream context that downstream analysis kept needing to infer. It preserves the original's sparse, research-driven approach — the additions are anchor points, not pre-judgements.

---

## Required Fields

```
**case**: <case label — e.g. "Case B — Cloud-to-Cloud Migration of 50 Legacy Applications">
**industry**: <industry>
**region**: <primary market(s) — list countries, not just region>
**target markets**: <list the specific regulatory jurisdictions that matter — e.g. "UK, Germany, France, Italy, Spain">
**date**: <YYYY-MM-DD>
```

## Background

One paragraph. Capture the operational problem, the hard constraints, and the current operating state.

```
<Client> must <do something> within <timeframe> — <budget remaining> remaining,
<critical constraints> (e.g. zero downtime, SOX-ready audit trail),
<ownerless assets> (e.g. "n applications with no current owner"),
and a current operating state of <baseline metrics>.
```

**Baseline metrics worth including** (if known — leave blank if not; do not fabricate):

- Current churn / retention rate
- Current pricing cycle frequency
- Current tech cost as % of premium or absolute
- Current telematics / usage-based penetration (if relevant)
- Number of applications, environments (on-prem, cloud)

## Markets & Regulatory Scope

```
Target markets: <countries>
Key regulators: <list>
Active regulatory frameworks: <e.g. DORA, FCA Consumer Duty, EIOPA AI Principles, GDPR, Solvency II review>
```

## Output

```
1. Run a Deep Research query: "<research prompt>"
   — Covers (a) top N market trends, (b) competitive moves by named players,
     (c) regulatory shifts in the past <N> months.
   — Include source citations with dates.
   — Guardrail: if the research surface is thin on <area>, run a second query targeting <area> specifically.

2. Cluster the output into N strategic pain points the segment is feeling now.

3. For each pain point, name the source-of-evidence.
   — If a claim has no source, downgrade it to a hypothesis or drop it.

4. Trim to one page and write to <output file>.
```

**Guardrail rationale:** The Kepler run surfaced Allianz/CMT telematics as the dominant competitive threat — but this emerged from the research, not from a prompt hint. That's the correct behaviour, but a second query guardrail ("if thin on competitive pricing / telematics") protects against a shallow first pass that misses the critical angle.

## Known Unknowns (optional — things you deliberately don't know at playground stage)

```
- <e.g. Actual churn rate for this client — use industry benchmarks and flag>
- <e.g. Budget composition — cloud infra vs. consulting vs. licensing>
- <e.g. Team capability profile — in-house ML engineering capacity?>
```

---

## v1 → v2 Changes

| v1 | v2 | Why |
|---|---|---|
| `region: Europe` | `region: ...` + `target markets: UK, DE, FR, IT, ES` | DORA is EU-wide, but FCA is UK-specific. Customer verbatims, regulator engagement, and deployment rollout all needed market-level precision that "Europe" couldn't provide. |
| No budget note | Budget in Background — `$31M remaining` | Downstream ROI and feasibility scoring (e.g. "build vs buy vs not-at-all") depends on knowing what's left to spend. Add composition note if available. |
| No baseline metrics | Optional baseline metrics section | The Kepler pipeline reached for J.D. Power / industry churn benchmarks because the actual client numbers weren't in the mandate. That's fine — but if you have them, put them here. If not, note "use industry benchmarks" so downstream knows the limitation. |
| No guardrail on research | Optional second-query guardrail | Prevents a shallow Deep Research pass from missing the critical competitive angle (e.g. telematics) without biasing the first pass. |
| No known unknowns | Optional known unknowns section | Makes deliberate gaps visible rather than having downstream discover them. |
