# Campaign Builder Interactions

This document defines the interaction flow used by campaign-builder.

## Interaction Rules

1. **One Question Per Turn**: Ask the user exactly one question per turn, then end the turn and wait for the answer. One focused question gets a usable answer; a batch of them gets skimmed.
2. **Blocking Question Tool by Default**: Ask through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini or Pi) with 2-4 concrete options drawn from research, such as the inferred conversion goal or a proposed margin ranking. Include a "Skip - assume for me" option on every interview question. Fall back to numbered options in chat only when no blocking tool exists or the call errors.
3. **Open Questions for Local Knowledge**: Ask open-ended when the answer is local knowledge that options would bias, such as who the client's real competitors are or what the client is known for in town. Name what counts as a useful answer (for example, "the two or three companies the client loses jobs to"), and tell the user they can reply "assume" to skip.
4. **Lead With the Inference**: When research produced a likely answer, state it and ask the user to confirm or correct it, rather than asking from a blank slate.
5. **Skips Become Labeled Assumptions**: When the user skips a question, says "assume", or leaves it unanswered, record the best-supported assumption with its reasoning, mark it as an assumption, and move to the next topic in the same turn.
6. **Approval Means an Explicit Yes**: Treat only an explicit confirmation of the strategy as approval to build. Treat a revision as a revision: integrate it, re-present the strategy, and wait again.
7. **Accept Volunteered Data Anytime**: Whenever the user supplies data (margins, ticket sizes, Keyword Planner exports, account history, current CPL, competitor names), fold it in at once, replace the matching estimate, and re-run any ranking it affects.
8. **Challenge With Evidence**: When research or demand analysis contradicts the user's suggested geography, priorities, or structure, say so with the numbers and a recommended alternative, and let the user decide.

## Execution Flow

### Phase 01: Intake

- **Objective**: Identify the client unambiguously and capture the budget, suggested geography, and any context the user already has.
- **Agent Action**: Take the client name, website URL, monthly budget, suggested geography, and any context from the invoking message (priority services, services to exclude, current performance, current and target CPL, business and call-answering hours, emergency service, desired conversion type, new build or rebuild). Ask for the monthly budget when it is missing. When the client name is common or no URL is given, confirm the exact business (name, city, URL) before researching.
- **Human Gate/Intervention**: The user supplies or confirms the client identity and the monthly budget.
- **Proceed When**: The client is identified by URL or by name plus location, and the monthly budget is known.
- **Pause When**: The budget is missing or the client identity is ambiguous; ask one question and end the turn.

### Phase 02: Research

- **Objective**: Learn the client, their industry, and their competitors from everything public.
- **Agent Action**: Run the Whole-Presence Research Sweep, Review-Mined Differentiators, Industry Primer, and Competitive Landscape Scan patterns from `references/patterns.md`. Determine what the client actually wants to be contacted for. Infer the conversion goal from the site's CTAs. Estimate the margin ranking. Audit the site as a destination for each likely ad group. Record the source of every fact.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Each research source has been checked and the findings are recorded with sources, including a note of any source that returned nothing.
- **Pause When**: Research cannot confirm the business is the one the user meant (for example, listings show a different address or owner); ask the user to confirm and end the turn.

### Phase 03: Demand Analysis

- **Objective**: Estimate how much local demand exists for each service, segment, and area, and how contested it is.
- **Agent Action**: Run the Segment and Area Demand Map, Demand Signal Ladder, and Demand Ceiling patterns. Produce demand ranges by service, by segment where segments differ in buyer or intent (for example, commercial vs. residential), and by area within the suggested geography, each with its signals and a confidence level. Combine with margin and competition to produce a draft Profit-Potential Ranking and draft Service Tiers.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Every candidate service has a demand range, competition note, and draft tier.
- **Pause When**: Not applicable; gaps in demand data become labeled low-confidence estimates.

### Phase 04: Interview

- **Objective**: Fill the gaps research and demand analysis could not close, and confirm the inferences.
- **Agent Action**: Work through the interview topics one question at a time, in this order, skipping any the user already answered: Keyword Planner or account data (explain that it replaces the demand estimates that drive the ranking), service geography (lead with any challenge from the demand analysis), local competitors, conversion goal (state the inferred goal), margin ranking (present the estimate and invite actual margin, ticket-size, or profit figures), business and call-answering hours, and any other context (seasonality, capacity, services to avoid, promotions, lead quality concerns). Apply Assume and Label to every skipped topic. Re-run the Profit-Potential Ranking whenever an answer changes its inputs.
- **Human Gate/Intervention**: The user answers, corrects, supplies data for, or skips each question.
- **Proceed When**: Every interview topic is answered, skipped, or covered by volunteered data.
- **Pause When**: A question is outstanding; end the turn after asking it.

### Phase 05: Strategy Confirmation

- **Objective**: Get explicit approval of the account strategy before writing the build sheet or import files.
- **Agent Action**: Apply Profit-First Budget Fit, Click-Volume Floor, Budget Feasibility Ranges, and Campaign Split Test. Present a compact strategy: service tiers with one-line reasons, the profit-potential ranking with its demand ranges, the campaign and ad group structure with monthly and daily budgets and percent of total, forecast ranges (clicks, leads, CPL), targeted segments and areas with any challenge to the user's suggestions, the conversion goals, destinations with Must Fix Before Launch issues, brand/competitor/Performance Max decisions, and every labeled assumption. When the budget cannot fund even the top Tier 1 service at the floor, run the Budget Shortfall Verdict and ask whether to raise the budget or proceed with a narrow build flagged as below the floor.
- **Human Gate/Intervention**: The user confirms the strategy or revises it; on a shortfall, the user chooses between raising the budget and a flagged narrow build.
- **Proceed When**: The user explicitly confirms the strategy, or explicitly chooses the flagged narrow build after a shortfall.
- **Pause When**: The strategy is presented and awaiting confirmation, or a revised strategy is awaiting confirmation.

### Phase 06: Build

- **Objective**: Produce the strategy brief, build sheet, import files, and landing page specs.
- **Agent Action**: Write the outputs per the Strategy Brief Structure, Build Sheet, Editor Import File Set, Responsive Search Ad Construction, Landing Page Spec, Ad Schedule Table, Conversion Hierarchy, and Search-Term Management Plan patterns. Check every output against `references/validations.md` and fix each failure.
- **Human Gate/Intervention**: None; this phase runs autonomously from the confirmed strategy.
- **Proceed When**: All outputs are written and pass every error-severity validation.
- **Pause When**: A validation failure would require changing the confirmed strategy (for example, a funded ad group has no claim that can be sourced); explain the conflict, propose the fix, and end the turn.

### Phase 07: Owner's-Money Self-Check

- **Objective**: Confirm the build is the structure worth launching with this budget.
- **Agent Action**: Run the Owner's-Money Self-Check pattern. When the answer is no, revise the build, record each revision and its reason in the brief, and re-run the validations. When a revision changes the confirmed strategy (tiers, funded services, campaign split, or budget split), present the change for confirmation.
- **Human Gate/Intervention**: The user confirms any revision that changes the confirmed strategy.
- **Proceed When**: The answer is yes and any strategy-level revision is confirmed.
- **Pause When**: A strategy-level revision is awaiting confirmation.

### Phase 08: Handoff

- **Objective**: Deliver the outputs and the steps to put them to use.
- **Agent Action**: List each output file with its path, summarize Build Now / Phase 2 / Do Not Build Yet in a few lines, list the Must Fix Before Launch items and the estimates to verify against Keyword Planner, and give the import steps: open Google Ads Editor, import the CSVs into the target account, review with Check Changes, set up the primary conversions, and post.
- **Human Gate/Intervention**: None.
- **Proceed When**: The handoff summary is shown.
- **Pause When**: Not applicable.

## Handoff

- **The Completion State**: The strategy brief, build sheet, Google Ads Editor import files, and a landing page spec for every ad group routed to a landing page are written; all error-severity validations pass; the self-check answer is yes; and the handoff summary is shown.
- **Exception/Fallback Handoff**: When the user stops before confirming the strategy, deliver the research, demand analysis, and draft strategy as a brief marked "Unconfirmed" and write no build sheet or import files. When web research is unavailable, say so at intake, build demand estimates from user data and industry benchmarks alone at low confidence, and mark every differentiator as user-stated.
