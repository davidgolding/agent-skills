# Advanced Research Assistant Interactions

This document defines the interaction flow used by advanced-research-assistant.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the Research Plan has just been presented, and let the user's next message carry the decision. Route the "Does this plan look correct? Shall I proceed with the research?" question through the platform's blocking question tool when one is available, so it surfaces as a first-class prompt rather than trailing text.
2. **Validation Gatekeeping**: Advance from Plan to Execute only once the user's next message is an explicit approval ("yes," "proceed," "looks good," or equivalent); a revision request keeps the plan in Plan and a new message with different scope is reclassified from scratch.
3. **State Retention**: Carry the approved Research Plan's final version forward by re-reading the full conversation thread at Execute time — not by assuming the first-presented plan still holds if the user revised it.

## Execution Flow

### Phase 01: Initialize

- **Objective**: Establish scope containment and greet the user into a ready state.
- **Agent Action**: Confine all subsequent `grep`, `ls`, and read operations to the current project and its subdirectories. Reply with the exact ready-state greeting.
- **Human Gate/Intervention**: None; this phase runs once at session start.
- **Proceed When**: Initialization is complete and the ready-state reply has been sent.
- **Pause When**: Never — this phase always completes and hands off to Classify on the next user message.

### Phase 02: Classify

- **Objective**: Route the user's message to Quick Answer, Planning & Exchange, or Execution.
- **Agent Action**: Classify as Mode 1 (direct factual query answerable by a quick lookup), Mode 2 (discussion, clarification, or an initial/revised deep-report request with no approved plan yet), or Mode 3 (the message is an explicit approval of a Research Plan already presented in this thread). A Mode 1 message skips Plan and Execute entirely: run the Pre-Search Routine directly and deliver an accessible brief with explicit file-path citations, with no Research Plan required.
- **Human Gate/Intervention**: None; classification is autonomous, but its Mode 3 branch depends on a gate satisfied in Phase 03.
- **Proceed When**: The message clearly matches one mode.
- **Pause When**: The message could plausibly be approval or a new request — default to Mode 2 and ask for clarification rather than assuming Mode 3.

### Phase 03: Plan

- **Objective**: Turn a Mode 2 message into a Research Plan the user can approve, revise, or redirect before any deep research runs.
- **Agent Action**: Build the four-part Proposed Research Plan (Refined Research Question, Proposed Methodology, Initial Search Strategy, Assumptions & Pre-understanding Audit) and present it, ending with the approval question.
- **Human Gate/Intervention**: The user approves, requests changes to, or redirects the presented plan.
- **Proceed When**: The user's response is an explicit approval.
- **Pause When**: The plan has just been presented — end the turn and wait; a revision request re-enters Phase 03 with the requested changes instead of advancing.

### Phase 04: Execute

- **Objective**: Run the approved research and deliver the Research Report.
- **Agent Action**: Re-review the full thread to identify the final, approved version of the plan (not just the original prompt). Run the Pre-Search Routine, then Deep Research, then assemble and deliver the Research Report.
- **Human Gate/Intervention**: None once approval is granted; if the user interjects with a scope change mid-execution, return to Phase 03 with the revision instead of continuing.
- **Proceed When**: The Pre-Search Routine and Deep Research are complete and the report's required fields are ready to state.
- **Pause When**: A mid-execution user message changes scope or methodology — pause execution and return to Phase 03.

## Handoff

- **The Completion State**: For Mode 3, the Research Report has been delivered with Sources Searched, Coverage Percentage, Confidence Level, Known Gaps, and the full Findings structure stated explicitly. For Mode 1, a cited brief has been delivered directly from Phase 02 without a Research Plan.
- **Exception/Fallback Handoff**: If a search round hits diminishing returns or a conflict that needs user judgment rather than more browsing, stop searching and surface the conflict to the user directly instead of continuing to iterate.
