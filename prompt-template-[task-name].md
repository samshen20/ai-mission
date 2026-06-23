# Prompt Template: [Generate a test case list from a story description] 

**Date:** 2026-06-16
**Author:** [Samuel Shen — Quality] 
**Project:** [Project name — Omnichannel Commerce Platform for a Global Retailer] 
**Model:** [Claude Code] 
**DIAL location:** [DIAL shared link or folder path] 
**Committed location:** [https://github.com/samshen20/ai-mission.git] 

--- 

## Purpose 

Generate test case list from a user story which used by qa to check the functionalities in sprint.

--- 

## Variable Placeholders 

| Placeholder | Description | Example value | 
|---|---|---| 
| `{{user_story}}` | user story ticket id | EPMCDMETST-1 | 
| `{{type}}` | test case type | smoke, regression | 
| `{{lang}}` | test case lang | en, zh | 

--- 

## Output Format Instruction 

Return a markdown table with columns: ID, Test Scenario, Test Steps, Expected Result, Type. Maximum 20 rows. No preamble.

--- 

## Prompt Body 

You are a QA engineer. From Jira ticket `{{user_story}}`, generate a test case list covering:

- **Happy path** — primary success flow(s)
- **Negative/error handling** — invalid inputs, missing data, permission denials, system failures
- **Edge cases** — boundary values, empty states, concurrency, timeouts, duplicate submissions
- **State transitions** — workflow status changes, UI state toggles, navigation guards

Add the correct test case `{{type}}` (smoke|regression|uat) as a tag per row. Write test steps and expected results in `{{lang}}`. Prioritize scenarios that directly validate the acceptance criteria, then expand to adjacent risk areas.

Return a markdown table with columns: ID, Test Scenario, Test Steps, Expected Result, Type. Maximum 20 rows. No preamble.

--- 

## Test Run (Author) 

**Input values used:** 
- `{{user_story}}` = EPMCDMETST-49619 
- `{{type}}` = regression
- `{{lang}}` = en 

**Output quality:** Usable as-is — covered all acceptance criteria with good negative cases 

--- 

## Peer Review 

**Reviewer:** [Tom — QA] 
**Date reviewed:** 2026-06-16
**Model used by reviewer:** Claude Sonnet 

**Reviewer input values used:** 
- `{{user_story}}` = EPMCDMETST-49619 
- `{{type}}` = regression

| Review question | Reviewer answer | 
|---|---| 
| Could you run the template without asking the author anything? | Yes / No — [one sentence] | 
| Was the output format what you expected? | Yes / No — [one sentence] | 
| Would you use this template on your own work? | Yes / No — [one sentence] | 
| One concrete improvement suggestion | [One sentence] | 

--- 

## Revision History | Version | Date | Change | Author | 
|---|---|---|---| 
| 1.0 | 2026-06-15 | Initial commit | Samuel Shen | 
| 1.1 | 2026-06-16 | Post-review update | Samuel Shen |
| 1.2 | 2026-06-16 | Expanded prompt body with coverage categories (happy/negative/edge/state), fixed table formatting | Samuel Shen |


