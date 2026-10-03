# Campaign Builder Interactions

This document defines the interaction flow used by campaign-builder.

## Interaction Rules

1. **One Question Per Turn**: Ask the user exactly one question per turn, then end the turn and wait for the answer. One focused question gets a usable answer; a batch of them gets skimmed.
2. **Blocking Question Tool by Default**: Ask through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini or Pi) with 2-4 concrete options drawn from research, such as the inferred conversion goal or a proposed margin ranking. Fall back to numbered options in chat only when no blocking tool exists or the call errors.
3. **Open Questions for Local Knowledge**: Ask open-ended when the answer is local knowledge that options would bias, such as who the client's real competitors are or what the client is known for in town. Name what counts as a useful answer (for example, "the two or three companies the client loses jobs to").
4. **Lead With the Inference**: When research produced a likely answer, state it and ask the user to confirm or correct it, rather than asking from a blank slate.
5. **Approval Means an Explicit Yes**: Treat only an explicit confirmation of the strategy as approval to build. Treat a revision as a revision: integrate it, re-present the strategy, and wait again.
6. **Accept Volunteered Data Anytime**: Whenever the user supplies data (margins, ticket sizes, Keyword Planner exports, account history, competitor names), fold it in at once and replace the matching estimate.

## Execution Flow

### Phase 01: Intake

- **Objective**: Identify the client unambiguously and capture the budget.
- **Agent Action**: Take the client name, website URL, and any notes from the invoking message. When the user has not given a monthly budget, ask for it. When the client name is common or no URL is given, confirm the exact business (name, city, URL) before researching.
- **Human Gate/Intervention**: The user supplies or confirms the client identity and the monthly budget.
- **Proceed When**: The client is identified by URL or by name plus location, and the monthly budget is known.
- **Pause When**: The budget is missing or the client identity is ambiguous; ask one question and end the turn.

### Phase 02: Research

- **Objective**: Learn the client, their industry, and their market from everything public.
- **Agent Action**: Run the Whole-Presence Research Sweep, Review-Mined Differentiators, and Industry Primer patterns from `references/patterns.md`. Crawl the client site for services, service area, CTAs, and page inventory. Infer the conversion goal from the site's CTAs. Estimate the margin ranking and local CPC ranges. Audit the site as a destination per likely ad group. Record the source of every fact.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Each research source has been checked and the findings are recorded with sources, including a note of any source that returned nothing.
- **Pause When**: Research cannot confirm the business is the one the user meant (for example, listings show a different address or owner); ask the user to confirm and end the turn.

### Phase 03: Interview

- **Objective**: Fill the gaps research could not close and confirm the inferences.
- **Agent Action**: Work through the interview topics one question at a time, in this order, skipping any the user already answered: service geography (cities, radius, or ZIP codes), local competitors, conversion goal (state the inferred goal and ask for confirmation), margin ranking (present the estimated ranking and invite actual margin, ticket-size, or profit figures), optional Keyword Planner or account data, and any other context (seasonality, capacity limits, services to avoid, upcoming promotions).
- **Human Gate/Intervention**: The user answers each question, confirms or corrects the conversion goal and margin ranking, and optionally supplies data.
- **Proceed When**: Geography, the conversion goal, and the margin ranking are confirmed, and the user has had the chance to add competitors, data, and context.
- **Pause When**: A question is outstanding; end the turn after asking it.

### Phase 04: Strategy Confirmation

- **Objective**: Get explicit approval of the campaign strategy before writing build files.
- **Agent Action**: Apply the Margin-First Budget Fit and Click-Volume Floor patterns. Present a compact strategy: funded ad groups with their daily budgets and estimated daily clicks, services cut and why, the top differentiators with sources, the conversion goal, the destination for each ad group (existing page or landing page), geo targeting, and which numbers are estimates. When the budget cannot fund even the top-margin service at the floor, run the Budget Shortfall Verdict pattern: state the shortfall, recommend a minimum monthly budget, and ask whether to raise the budget or proceed with a narrow build flagged as below the floor.
- **Human Gate/Intervention**: The user confirms the strategy or revises it; on a shortfall, the user chooses between raising the budget and a flagged narrow build.
- **Proceed When**: The user explicitly confirms the strategy, or explicitly chooses the flagged narrow build after a shortfall.
- **Pause When**: The strategy is presented and awaiting confirmation, or the user has revised it and the revised strategy is awaiting confirmation.

### Phase 05: Build

- **Objective**: Produce the strategy brief, the import files, and the landing page specs.
- **Agent Action**: Write the outputs per the Strategy Brief Structure, Editor Import File Set, Responsive Search Ad Construction, and Landing Page Spec patterns. Before handing off, check every output against `references/validations.md` and fix each failure.
- **Human Gate/Intervention**: None; this phase runs autonomously from the confirmed strategy.
- **Proceed When**: All outputs are written and pass every error-severity validation.
- **Pause When**: A validation failure would require changing the confirmed strategy (for example, a funded ad group has no claim that can be sourced); explain the conflict, propose the fix, and end the turn.

### Phase 06: Handoff

- **Objective**: Deliver the outputs and the steps to put them to use.
- **Agent Action**: List each output file with its path, summarize the funded ad groups and budget split in a few lines, list the estimates that should be checked against Keyword Planner, and give the import steps: open Google Ads Editor, import the CSVs into the target account, review with Check Changes, and post.
- **Human Gate/Intervention**: None.
- **Proceed When**: The handoff summary is shown.
- **Pause When**: Not applicable.

## Handoff

- **The Completion State**: The strategy brief, the Google Ads Editor import files, and a landing page spec for every ad group routed to a landing page are written, all error-severity validations pass, and the handoff summary is shown.
- **Exception/Fallback Handoff**: When the user stops before confirming the strategy, deliver the research findings and the draft strategy as a brief marked "Unconfirmed" and write no import files. When web research is unavailable, say so at intake and build from user-supplied information alone, marking every differentiator as user-stated.
