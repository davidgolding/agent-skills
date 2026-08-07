# Skill Auditor Interactions

This document defines the interaction flow used by skill-auditor.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the user's response is needed, and let the conversation's natural back-and-forth carry the wait. Route through the platform's blocking question tool (e.g. `AskUserQuestion`) whenever presenting the refactor plan or a scope question, so the request surfaces as a first-class prompt instead of plain text.
2. **Validation Gatekeeping**: Advance from the Plan phase to the Migrate phase only once the user's next message is an explicit approval; a revision request or a cancellation keeps the audited skill's files untouched.
3. **State Retention**: Carry the audit findings, scorecard, and change script forward in the conversation and in the audit report file written to the audited skill's folder — not in an internal registry the runtime tracks on its own.

## Execution Flow

### Phase 01: Audit

- **Objective**: Read the audited skill's full file set and score it against PEV-M structural compliance, language quality, and token efficiency.
- **Agent Action**: Read `SKILL.md` and every file under `references/`, `scripts/`, `templates/`, and any other subfolder; compare structure against the required shapes in `patterns.md`, `sharp_edges.md`, and `validations.md`; detect negative-polarity instructions, fictional runtime machinery, and heuristic token-efficiency signals; detect human-in-the-loop behavior to determine whether `interactions.md` is required.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: A valid, readable skill folder was supplied.
- **Pause When**: The supplied path is missing or does not resolve to a readable skill folder — ask the user for a valid skill path.

### Phase 02: Plan

- **Objective**: Turn the audit findings into a refactor plan the user can approve, revise, or reject without reading code.
- **Agent Action**: Compose the executive summary, scorecard, and sequenced change script; write the plan to a new report file inside the audited skill's folder (e.g. `<skill-name>-audit-report.md`); present the plan in chat. Leave every other file in the audited skill's folder untouched during this phase.
- **Human Gate/Intervention**: The user approves, requests changes to, or cancels the presented refactor plan.
- **Proceed When**: The user's response is an explicit approval.
- **Pause When**: The plan has just been presented — end the turn and wait for the user's response before touching any file other than the report.

### Phase 03: Migrate

- **Objective**: Execute the approved change script, migrating the skill's files in place while preserving every original behavior.
- **Agent Action**: Apply each change in the script in sequence; map every original instruction to its PEV-M destination file; check behavior parity against the pre-migration file set.
- **Human Gate/Intervention**: None once approval is granted; a revision request routes back to Phase 02 instead of proceeding.
- **Proceed When**: Every change in the script has been applied and behavior parity holds.
- **Pause When**: The user's Phase 02 response requested changes instead of approving — return to Phase 02 with the requested revisions.

## Handoff

- **The Completion State**: The migrated skill's files pass its own PEV-M structural requirements, behavior parity against the original is confirmed, and the audit report file records the completed migration.
- **Exception/Fallback Handoff**: If behavior parity fails after three consecutive migration attempts, stop autonomous migration and present the unresolved parity gap to the user directly for manual resolution.
