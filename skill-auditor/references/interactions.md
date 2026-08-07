# Skill Auditor Interactions

This document defines the interaction flow used by skill-auditor.

## Interaction Rules

1. **The Turn-Taking Paradigm**: Append the `[AWAIT_HUMAN]` token immediately whenever skill-auditor yields the execution loop to wait for the user's response to a presented refactor plan.
2. **Validation Gatekeeping**: Block the transition from the Plan state to the Migrate state ($S_{plan} \not\rightarrow S_{migrate}$) unless the user's response is an explicit approval.
3. **State Retention**: Track the audit findings, scorecard, and change script within state keys encapsulated inside `<state_context>` tags across the Audit, Plan, and Migrate phases.

## Execution Flow

### Phase 01: Audit

- **Objective**: Read the audited skill's full file set and score it against PEV-M structural compliance, language quality, and token efficiency.
- **State Input Key**: `skill-auditor#$[TARGET_SKILL_PATH]`
- **Agent Action**: Read `SKILL.md` and every file under `references/`, `scripts/`, `templates/`, and any other subfolder; compare structure against `pev-m.md`; detect negative-polarity instructions and heuristic token-efficiency signals; detect human-in-the-loop behavior to determine whether `interactions.md` is required.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Execution Commands**:
	- `STOP_AND_PROMPT`: Triggered when `[TARGET_SKILL_PATH]` is missing or does not resolve to a readable skill folder; append a prompt asking the user for a valid skill path.
	- `GO_PROCEED`: Triggered when a valid, readable skill folder is supplied.
- **Success Criteria/Output Key**: `skill-auditor#$[AUDIT_FINDINGS]`

### Phase 02: Plan

- **Objective**: Turn the audit findings into a refactor plan the user can approve, revise, or reject without reading code.
- **State Input Key**: `skill-auditor#$[AUDIT_FINDINGS]`
- **Agent Action**: Compose the executive summary, scorecard, and sequenced change script; write the plan to a file inside the audited skill's folder; present the plan in chat.
- **Human Gate/Intervention**: The user approves, requests changes to, or cancels the presented refactor plan.
- **Execution Commands**:
	- `STOP_AND_PROMPT`: Triggered immediately after presenting the plan; append `[AWAIT_HUMAN]` and wait for the user's response.
	- `GO_PROCEED`: Triggered only when the user's response is an explicit approval.
- **Success Criteria/Output Key**: `skill-auditor#$[APPROVED_PLAN]`

### Phase 03: Migrate

- **Objective**: Execute the approved change script, migrating the skill's files in place while preserving every original behavior.
- **State Input Key**: `skill-auditor#$[APPROVED_PLAN]`
- **Agent Action**: Apply each change in the script in sequence; map every original instruction to its PEV-M destination file; check behavior parity against the pre-migration file set.
- **Human Gate/Intervention**: None once approval is granted; a revision request routes back to Phase 02 instead of proceeding.
- **Execution Commands**:
	- `STOP_AND_PROMPT`: Triggered when the user's Phase 02 response requests changes instead of approving; return to Phase 02 with the requested revisions.
	- `GO_PROCEED`: Triggered once every change in the script has been applied and behavior parity holds.
- **Success Criteria/Output Key**: `skill-auditor#$[MIGRATION_COMPLETE]`

## Handoff

- **The Completion Safe-State**: `skill-auditor#$COMPLETE`, emitted once the migrated skill passes its own PEV-M structural requirements and behavior parity is confirmed.
- **Exception/Fallback Handoff**: If behavior parity fails after three consecutive migration attempts, route to `ESCALATE_TO_SUPERVISOR` — stop autonomous migration and present the unresolved parity gap to the user directly for manual resolution.
