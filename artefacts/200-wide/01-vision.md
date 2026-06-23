# Vision Attack — Personalised Policy Communication Engine

**product:** Kepler Insurance
**feature:** Personalised Policy Communication Engine
**date:** 2026-06-18
**source of attacked claim:** `00-feature.md` + `04-canvas-v2.md`

---

## Attacked framing

> "Reduce renewal churn 3 percentage points (from ~12% to ~9%) and improve renewal price satisfaction by +30 points within 6 months of deployment across the first two markets, measured via follow-up NPS survey 30 days post-renewal."

---

## Critique 1 (CRITICAL): The churn baseline is unfalsifiable — it's an industry benchmark, not Kepler's actual data

**Problem:** The 12% baseline comes from FCA MS18/1.2 industry averages, not Kepler's books. The canvas's own Known Unknowns section flags this. If Kepler's actual renewal churn is, say, 8% (because they already have a sticky book), a 3pp reduction is impossible — you can't reduce churn below 0%. If actual churn is 18%, a 3pp reduction is too conservative.

**What this makes unfalsifiable:** You cannot verify whether you achieved "3pp reduction from ~12%" because the starting point is an estimate. If the A/B test measures 11.5% vs 10.5% (= 1pp reduction from the measured baseline), but Kepler's real churn turns out to have been 14% all along, then the treatment actually achieved 3.5pp — but the claim framework can't capture this because it committed to a fixed ~12%.

**Worse:** The "~" in "~12%" is doing unearned work. It protects the claim from being wrong without protecting the reader from being misled. If Kepler's real churn is 9%, the project can never hit its target through no fault of its own — and the target was wrong from day one.

**Fix:** Remove the fixed baseline. Frame the metric as a relative reduction with a measurement-first commitment:

> "Measure current renewal churn via a 90-day baseline observation period across both target markets (minimum 10,000 renewal events, reported with 95% CI). **Then** target a 25% relative reduction from that measured baseline, measured again at 6 months post-deployment. If the measured baseline is ≤8%, escalate the target to 15% relative reduction (acknowledging floor effects)."

---

## Critique 2 (HIGH): "+30 points on NPS" is a phantom unit — no baseline, no confidence interval, no confounder control

**Problem:** NPS is scored on a −100 to +100 scale. "+30 points" from an unstated baseline is meaningless:

- 20 → 50 is a very different business outcome from −10 → +20, even though both are "+30 points."
- If the current renewal NPS is not measured (it isn't — no baseline is cited), then "+30" is a P value floating in search of a null hypothesis.
- NPS response rates for insurance renewal surveys typically run 5–15%, which means the observed score carries a margin of error of ±5–8 points at 95% CI for a typical monthly cohort. A claim of "+30" requires the true effect to be 4–6× the noise floor — which is possible, but the claim doesn't acknowledge that it's operating within measurement noise.

**Hand-wavy:** "Renewal price satisfaction" is not an NPS question. NPS measures "how likely are you to recommend us to a friend?" — a loyalty proxy. Price satisfaction is a different construct (J.D. Power uses a multi-question battery). Mapping "+30 points on NPS" to "price satisfaction" is combining two different measurement instruments. If the real goal is price satisfaction, measure price satisfaction directly — don't use NPS as a proxy and pretend it's the same thing.

**Fix:** Replace with a directly measured construct:

> "Improve price satisfaction by ≥25% (proportion of respondents who agree or strongly agree with 'My renewal premium is fair given my risk profile') measured via a 3-question survey (not single-prompt NPS) sent 30 days post-renewal, with a minimum target of 400 responses per month per market (margin of error ≤5 points at 95% CI). Declare the baseline score from the 90-day pre-deployment observation period."

---

## Critique 3 (HIGH): The counterfactual is missing — the frame compares against a static baseline in a dynamic market

**Problem:** The claim is "churn goes from 12% to 9%." This assumes the control group stays at 12%. But:

- The market is softening (Marsh Q1 2026: −9% rate decline). Competitors are dropping prices. Allianz is improving CMT telematics scores. Industry churn is rising.
- If Allianz cuts prices 5% in Kepler's target markets during the 6-month observation window, control-group churn might spike from 12% to 16%. In that case:
  - Treatment churn = 12% (flat) → the static-frame says "0pp improvement, project failed"
  - But treatment held churn flat against a 4pp headwind → the project actually delivered 4pp vs counterfactual
  - The static frame penalises the project for a market shift it cannot control
- Conversely, if a regulatory change locks all rates (Solvency II review), churn might drop to 8% across the board. The project appears to succeed when the market did all the work.

**Unfalsifiable because:** Without specifying *what the control group actually did*, the claim "3pp reduction" cannot be distinguished from "market moved and we rode the wave" or "market moved against us and we held our ground."

**Fix:** Commit to a controlled measurement design, not a static baseline:

> "Primary metric: **Controlled churn reduction** — A/B test across matched renewal cohorts. Treatment group receives personalised causation notice; control group receives current templated notice. Both groups experience the same market conditions, same premium change magnitude, same policy types. Target: ≥2pp lower churn in treatment vs control (directional minimum) with ≥3pp as the stretch goal. Measure at 30 days post-renewal for a minimum of 5,000 policies per arm per market. A secondary metric tracks absolute churn movement, but the project is evaluated on the controlled delta."

---

## Revised vision & metric (answering all three critiques)

> **Vision:** Every Kepler renewal notice tells the customer, in plain language, exactly what changed and why — turning an opaque cost event into a transparent retention moment.
>
> **Primary metric — controlled churn delta:** ≥2pp lower renewal churn in the treatment group (personalised causation notice) vs the control group (current templated notice), measured via matched-cohort A/B test with ≥5,000 policies per arm per market, observed at 30 days post-renewal. Stretch goal: ≥3pp.
>
> **Secondary metric — price satisfaction:** ≥25% relative improvement in the proportion of respondents who agree with "My renewal premium is fair given my risk profile" (3-question survey, not single-prompt NPS), measured from a declared 90-day pre-deployment baseline, with ≥400 responses per month per market.
>
> **Pre-commitment:** Measure both baselines (actual churn rate per market, pre-deployment price satisfaction score) during Phase 0 before any system build begins. If measured churn is ≤8%, reduce primary target to ≥1.5pp controlled delta and flag floor-effect risk in the project charter.

---

## Summary of fixes

| Problem | Symptom | Fix |
|---|---|---|
| Unfalsifiable baseline | "~12%" hangs on an industry benchmark; delta expressed as absolute pp | Remove fixed baseline → commit to measurement-first relative target |
| Phantom unit | "+30 points on NPS" combines a measurement instrument (NPS) with an unmeasured construct (price satisfaction) | Replace with measured price satisfaction construct + declared baseline + confidence interval |
| Missing counterfactual | Static comparison ("goes from 12% to 9%") cannot distinguish project effect from market movement | Replace with controlled A/B delta as primary metric; absolute movement as secondary |
