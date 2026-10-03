---
name: campaign-builder
description: Research a client and build a budget-fitted Google Ads Search campaign with a strategy brief, Google Ads Editor import files, and landing page specs. Use when the user wants to plan or build a Google Ads campaign for a client, find a client's differentiators from reviews and listings for ad copy, or decide whether ad traffic should go to the website or a landing page.
---

# Campaign Builder

## Mandate

Build one Google Ads Search campaign per invocation for one client, fitted to the budget the user supplies for that client. Decide five things: which of the client's services to fund, ranked by margin and cut until every funded ad group clears the click-volume floor; which differentiators the ads call out, each traced to a review, listing, client page, or user statement; which conversion the campaign optimizes for; whether each ad group lands on an existing page or a dedicated landing page; and how the budget splits across ad groups. Ground the research method, campaign structure, and copy rules in `references/patterns.md`, the risks in `references/sharp_edges.md`, the output checks in `references/validations.md`, and the run order and user checkpoints in `references/interactions.md`. A correct output contains a strategy brief that explains and sources every choice, Google Ads Editor import files that pass every rule in `references/validations.md` and spend no more than the client's budget, and a landing page spec for each ad group routed to a landing page.

## Principles

- **Client Revenue First**: Rank services by margin and fund from the top down, because the campaign exists to make the client as much money as possible, ahead of review popularity or cheap clicks.
- **Whole-Presence Research**: Sweep the client's website, reviews, directory listings, and social profiles before the interview, since most clients have a thin footprint and reviews are where their real differentiators surface.
- **Infer, Then Confirm**: Propose the conversion goal, margin ranking, and local facts from research, then have the user confirm or correct them, so the interview stays short and the user keeps the final say.
- **User Data Overrides Estimates**: Replace any estimate (margins, CPCs, search volumes) with user-supplied figures whenever the user provides them, and label every remaining estimate as an estimate in the brief.
- **Fund Fewer Ad Groups Fully**: Concentrate the budget on fewer ad groups that each clear the click-volume floor, because a campaign spread across every service gathers too little data in any one place to optimize.
- **Sourced Claims Only**: Write ad copy from claims traceable to a cited source and within Google Ads editorial and superlative policy, so ads pass review and the user can defend every line to the client.
- **Strategy Before Build**: Confirm the strategy with the user before writing build files, because the strategy is cheap to change and the build is expensive to redo.
- **Honest Budget Verdicts**: When the budget cannot fund even the top-margin service, say so and recommend a minimum budget, because a quietly underfunded campaign costs the client money and teaches nothing.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
- **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.
- **For Interacting:** Always consult **`references/interactions.md`**. This file governs human-in-the-loop checkpoints, approval gates, and handoffs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
