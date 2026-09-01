# Interactions

This document governs production-editor's human-in-the-loop flow: how intake questions are batched, when a phase gates on the user, and how a pass hands off when it's done.

## Interaction Rules

1. **Batched intake, not serial interrogation**: when parameters are missing, ask for all of them together in one round. Full procedure and inference cues: `references/intake.md`.
2. **Assumptions are proposals, not resolutions**: an inferred parameter (e.g., "the existing notes use author-date citations, so I'll assume Chicago 18") is presented for the user to confirm or correct. Only an explicitly stated or explicitly confirmed parameter counts as resolved.
3. **Conflicts route to the user for resolution**: when a loaded manual and a settled style-sheet entry (or a user request) conflict, present the conflict to the user rather than picking a side silently.

## Execution Flow

### Phase 01: Intake

- **Objective**: Resolve six parameters before any editing begins — edit type, intensity, citation/style system, usage authority, dialect/spelling, deliverable format.
- **Agent Action**: Parse the opening prompt for parameters already supplied; identify which remaining parameters the requested edit type actually needs (see `references/edit-types.md`); if the active project section of `references/stylesheet.md` already has a resolved set for this document and nothing contradicts it, reuse it and confirm briefly instead of re-asking.
- **Human Gate/Intervention**: The user supplies or confirms every parameter the requested pass needs.
- **Proceed When**: Every parameter the pass requires is either explicitly stated by the user or explicitly confirmed after being proposed as an assumption.
- **Pause When**: A required parameter is still unresolved — ask for every outstanding parameter together in a single batched round, then end the turn and wait for the reply.

### Phase 02: Load authorities

- **Objective**: Resolve which style manual, usage authority, and style-sheet entries govern this pass, in precedence order (explicit instruction > user-supplied house style > active project's style-sheet section > named style-manual profile > named usage authority > skill default).
- **Agent Action**: Load each source in precedence order; read the active project's section of `references/stylesheet.md` before editing so settled entries are treated as binding.
- **Human Gate/Intervention**: None for a clean load. If the loaded manual contradicts a settled style-sheet entry, that conflict routes to the user rather than being resolved silently.
- **Proceed When**: The authority chain for this pass is fully resolved with no unresolved conflict.
- **Pause When**: A loaded manual and a settled style-sheet entry disagree — surface the conflict to the user instead of picking one.

### Phase 03: Execute the pass

- **Objective**: Perform the one requested, bounded edit type at the resolved intensity.
- **Agent Action**: Apply the scope, boundaries, authority requirements, intensity rubric, and output format defined for that edit type in `references/edit-types.md`. Route any problem that belongs to a different pass into a separate "Out-of-scope observations" section instead of fixing it directly.
- **Human Gate/Intervention**: None mid-execution, except where the pass/intensity itself calls for a query instead of an action (see Principle: Query-first licensing in `SKILL.md`).
- **Proceed When**: Every suggestion or edit in the response falls within the requested edit type's defined scope, and every reference/copyedit/mechanical claim carries its required citation.
- **Pause When**: It's unclear whether a change is licensed by the requested pass or intensity — raise it as a query in the response rather than acting on it.

### Phase 04: Update the style sheet

- **Objective**: Persist newly settled decisions so later passes on the same project can reuse them.
- **Agent Action**: Append newly settled decisions to the active project section of `references/stylesheet.md`, keyed to that project only, and report what was added. Treat an already-settled entry as binding rather than re-deriving it.
- **Human Gate/Intervention**: A conflict between the governing manual and an existing style-sheet entry.
- **Proceed When**: New decisions are recorded without contradicting an already-settled entry.
- **Pause When**: A new decision would contradict a settled entry or the governing manual — surface the conflict to the user instead of resolving it silently.

## Handoff

- **The Completion State**: The requested pass is delivered in its required output format (editorial memo, inline commentary list, or clean revised text), every reference/copyedit/mechanical claim carries a compliant citation, out-of-scope findings are isolated in their own section, and the style sheet reflects any newly settled decisions.
- **Exception/Fallback Handoff**: If an intake gap remains unresolved after one batched round, or a manual/style-sheet conflict can't be settled from the loaded authorities, stop and present the open question to the user directly rather than guessing past it.
