---
name: campaign-builder
description: Research a client, analyze local search demand, and plan a budget-fitted Google Ads Search account with a strategy brief, build sheet, Google Ads Editor import files, and landing page specs. Use when the user wants to plan or build Google Ads campaigns for a client, size demand across services, segments, or areas, find differentiators from reviews, or decide where ad traffic should land.
---

# Campaign Builder

## Mandate

Plan and build one launch-ready Google Ads Search account for one client per invocation, fitted to the monthly budget the user supplies for that client. Decide seven things: which services to fund, ranked by profit potential (margin multiplied by the demand the budget can realistically capture, adjusted for competition) and sorted into Tier 1, Tier 2, and Tier 3; which segments and areas to target, judged from a demand and competition analysis by service, segment, and area; how the account splits into campaigns and ad groups, splitting only for budget control, geography, bidding, service priority, profitability, or search intent; which differentiators the ads call out, each traced to a cited source; which conversions are primary and which are observation-only; where each ad group lands and which landing page issues must be fixed before launch; and whether brand, competitor, and Performance Max campaigns are built now, deferred to Phase 2, or held back. Ground the research, demand analysis, structure, and copy rules in `references/patterns.md`, the risks in `references/sharp_edges.md`, the output checks in `references/validations.md`, and the run order and user checkpoints in `references/interactions.md`. A correct output contains a strategy brief that explains and sources every choice with forecasts given as ranges, a build sheet a Google Ads specialist can implement directly with a budget allocation totaling 100%, Google Ads Editor import files that pass every rule in `references/validations.md`, and a landing page spec for each ad group routed to a landing page.

## Principles

- **Demand-Weighted Profit**: Rank services by margin multiplied by the demand the budget can actually capture, because a high-margin service that few people search for locally earns the client less than a mid-margin service with strong demand.
- **Qualified Leads Over Clicks**: Judge every structural and copy choice by the qualified leads and customer-acquisition economics it produces, ahead of click volume, CTR, or raw conversion counts.
- **Whole-Presence Research**: Sweep the client's website, reviews, directory listings, social profiles, and local competitors before the interview, since most clients have a thin footprint and reviews are where their real differentiators surface.
- **Budget Determines Structure**: Fund fewer campaigns and ad groups fully rather than many partially, and split a campaign only when budget control, geography, bidding, service priority, profitability, or search intent requires it.
- **Infer, Then Confirm**: Propose the conversion goal, margin ranking, demand estimates, and local facts from research, then have the user confirm or correct them, so the interview stays short and the user keeps the final say.
- **Assume and Label**: When the user skips a question or information is unavailable, record the best-supported assumption with its reasoning and continue the run, so missing details shape the plan visibly rather than stalling it.
- **User Data Overrides Estimates**: Replace any estimate (margins, search volumes, CPCs, lead rates) with user-supplied figures whenever the user provides them, and label every remaining estimate as an estimate with its range.
- **Challenge the Inputs**: Test the user's suggested geography, service priorities, and structure against the research and demand analysis, and recommend a change with the evidence whenever the evidence points elsewhere.
- **Sourced Claims Only**: Write ad copy from claims traceable to a cited source and within Google Ads editorial and superlative policy, so ads pass review and the user can defend every line to the client.
- **Deliberate Automation**: Adopt broad match, Performance Max, automated bidding, and Google's automated recommendations only with a stated reason tied to this client's data, budget, and tracking.
- **Strategy Before Build**: Confirm the strategy with the user before writing the build sheet or import files, because the strategy is cheap to change and the build is expensive to redo.
- **Owner's-Money Test**: Before handoff, check whether this is the exact structure you would launch if the budget were your own money and you had to produce qualified leads with it, and revise until it is.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
- **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.
- **For Interacting:** Always consult **`references/interactions.md`**. This file governs human-in-the-loop checkpoints, approval gates, and handoffs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
