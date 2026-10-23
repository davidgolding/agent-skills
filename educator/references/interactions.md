# Educator Interactions

This document defines the interaction flow used by educator.

## Interaction Rules

1. **One Question Per Turn**: Ask exactly one interview question per turn and end the turn to wait for the answer. A single focused question gets a complete answer; stacked questions get partial ones.
2. **Blocking Question Tool First**: Ask interview and conflict-gate questions through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini or Pi), with 2-4 concrete options; the tool's free-text fallback covers answers the options miss. Fall back to numbered options in chat when no blocking tool exists or the call errors.
3. **Extract Before Asking**: Before the first question, read the prompt and any attached material for every required criterion, and treat any criterion stated or clearly implied there as answered (for example, "my 4th graders" answers developmental level).
4. **Approval Means an Explicit Choice**: At the conflict gate, proceed only on the requester's explicit choice of the evidence-aligned alternative, the original request, or a variant they describe.

## Execution Flow

### Phase 01: Route the Request

- **Objective**: Identify the mode.
- **Agent Action**: Classify the request as Build (create a lesson plan, unit, course outline, activity, or assessment), Audit (evaluate supplied material or a named technique), or Advise (answer a standalone evidence question). When a request combines modes, such as "review this plan and then rewrite it," run Audit first and then Build from its revisions.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The mode is identified. Build and Audit go to Phase 02; Advise goes to Phase 03.
- **Pause When**: The request fits no mode or could be either Build or Audit with different results; ask which the requester wants through the blocking question tool and end the turn.

### Phase 02: Interview Gate

- **Objective**: Establish the five required criteria.
- **Agent Action**: Check the prompt for each criterion in this order, then ask for the first missing one: (1) developmental level of the learners (young child, child, pre-adolescent, adolescent, young adult, adult, older adult, or a mix); (2) subject and topic; (3) prior knowledge of the subject (new to it, some exposure, or experienced); (4) time and format (session length, number of sessions, span); (5) setting and constraints (classroom, online, workplace, or home; group size; available materials; inclusive or remedial needs). Infer the learning goal and whether the task is well-structured or ill-structured, without asking, and carry both forward to the evidence notes.
- **Human Gate/Intervention**: The requester answers one criterion question per turn.
- **Proceed When**: All five criteria are known from the prompt or the requester's answers.
- **Pause When**: Any criterion is missing; ask for the first missing one and end the turn.

### Phase 03: Evidence Conflict Check

- **Objective**: Catch request elements the evidence contradicts before building.
- **Agent Action**: Check the request against the anti-patterns in `references/patterns.md` and the sharp edges in `references/sharp_edges.md`, such as learning styles, unguided discovery for novices, full scaffolding for experienced learners, massed study with a single final test, or a framework presented as science. For each conflict, prepare a one- or two-sentence statement of what the evidence shows and the closest evidence-aligned alternative. For Advise requests, note whether the question falls outside the integrated core and needs out-of-core research.
- **Human Gate/Intervention**: When a conflict exists, the requester chooses the evidence-aligned alternative, the original request, or a variant, through the blocking question tool.
- **Proceed When**: No conflict exists, or the requester has made an explicit choice for every conflict.
- **Pause When**: A conflict exists and the requester has not yet chosen; present the conflict and alternative and end the turn. When the requester keeps the contradicted element, build it as chosen and record the evidence conflict in the "Why this design" notes.

### Phase 04: Design or Evaluate

- **Objective**: Produce the deliverable from the integrated evidence base.
- **Agent Action**: For Build, pick the developmental profile (the least-experienced profile for mixed groups), set guidance by element interactivity and prior knowledge, segment content, choose bounded generative strategies, schedule retrieval and spacing, and apply the matching developmental patterns. For Audit, classify every element as supported, contradicted, or not addressed and write a revision for each contradicted one. For Advise, form the verdict, mechanism, and boundary conditions. For any question the integrated core does not answer, search current peer-reviewed syntheses and record citations for labeling.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: A complete draft exists.
- **Pause When**: Out-of-core research is needed and search tools are unavailable; tell the requester the core does not cover the question, give the nearest core principle, and ask whether to proceed on that basis, then end the turn.

### Phase 05: Self-Review

- **Objective**: Check the draft before delivery.
- **Agent Action**: Check the draft against every rule in `references/validations.md` that applies to its mode, and fix each failure.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The draft passes every applicable error-severity rule and any remaining warnings are deliberate and explained in the evidence notes.
- **Pause When**: A fix requires information only the requester has; ask for it as one question and end the turn.

### Phase 06: Deliver

- **Objective**: Hand the requester a usable result.
- **Agent Action**: Present the deliverable as structured markdown. For Build and Audit, end with the "Why this design" section, including the inferred learning goal and task structure and any labeled out-of-core sources. For Advise, lead with the verdict.
- **Human Gate/Intervention**: The requester may correct an inferred criterion or ask for revisions.
- **Proceed When**: The deliverable is presented.
- **Pause When**: The requester corrects an inferred criterion or requests changes; return to Phase 03 for the change and re-run Phases 04-06.

## Handoff

- **The Completion State**: The requester has a classroom-ready deliverable fitted to the five criteria, or a complete Advise answer, and every Build or Audit deliverable closes with "Why this design" notes naming inferred criteria and labeled out-of-core sources.
- **Exception/Fallback Handoff**: When the requester declines to give a required criterion, build for the most conservative assumption (the least-experienced learners in the most constrained setting), state that assumption at the top of the evidence notes, and invite correction. When the requester stops before resolving a conflict, end without a deliverable and summarize the open choice.
