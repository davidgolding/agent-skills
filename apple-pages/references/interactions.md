# Apple Pages Interactions

This document defines the interaction flow used by apple-pages.

## Interaction Rules

1. **Ask Through the Blocking Tool**: When a decision belongs to the user, ask exactly one question with the platform's blocking question tool (`AskUserQuestion` in Claude Code) and end the turn until they answer.
2. **Confirm Deletes by Path**: Before moving any document to the Trash, show the full path and ask the user to confirm; proceed only on an explicit yes.
3. **Proceed on Clear Writes**: For create, update, and export requests that name the target and the change, carry them out under the backup or separate-copy safety path and report afterward; the backup is the safety net for in-place writes.
4. **Resolve Ambiguous Targets**: When the request matches more than one file, paragraph, or template, or names a file that cannot be found, ask the user to choose before acting.
5. **Announce Separate Copies**: Whenever an edit goes to a separate copy because the original is open, state that in the report, with the copy's path and the note that it lacks the window's unsaved work.

## Execution Flow

### Phase 01: Preflight

- **Objective**: Confirm the environment can perform the operation.
- **Agent Action**: Run the Preflight Check from `references/patterns.md`: Pages.app installed, Automation permission, target exists, is a `.pages` document, and is downloaded.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Every check passes.
- **Pause When**: A check fails. Explain the failure and the fix per `references/sharp_edges.md`, then end the turn.

### Phase 02: Resolve the Request

- **Objective**: Pin down exactly which file, which content, and which template or format the operation targets.
- **Agent Action**: Read the document with Export-Based Read when the request depends on its content; locate the target paragraphs, tables, or objects; run Dictionary Check for any class beyond body text; run Open-Document Detection for updates.
- **Human Gate/Intervention**: Ask the user to choose when the target is ambiguous (Interaction Rule 4); for deletes, ask for confirmation of the exact path (Interaction Rule 2).
- **Proceed When**: The target is unambiguous, the operation is supported by the installed dictionary, and any delete has an explicit confirmation.
- **Pause When**: A choice or delete confirmation is pending. End the turn until the user answers.

### Phase 03: Execute

- **Objective**: Apply the operation through its mechanism and safety path.
- **Agent Action**: For updates, make the timestamped backup (or the separate copy when the document is open), then apply the change through Pages scripting. For creates, use Template-Based Create with a non-conflicting name. For exports, use Export To Requested Format. For deletes, use Trash-Based Delete. Check each step against `references/validations.md`.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The operation completes without a scripting error.
- **Pause When**: A scripting error occurs. Leave the backup in place, report the error and the state of each file, and end the turn.

### Phase 04: Verify and Report

- **Objective**: Confirm the change and tell the user what happened.
- **Agent Action**: Run Read-Back Verification for creates and updates. Report the file changed, the backup or copy path, any layout content flagged as approximate, and any part of the request the installed Pages could not perform.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The report is delivered.
- **Pause When**: Read-back shows a mismatch. Report it with the backup path and end the turn.

## Handoff

- **The Completion State**: The requested operation is applied natively in Pages and verified, a recoverable prior version exists for every modified or trashed file, and the user has a report naming each file touched, each backup or copy, and every limitation encountered.
- **Exception/Fallback Handoff**: When the operation cannot complete (missing Pages, denied permission, unsupported dictionary feature, or a scripting error), leave every original and backup in place, tell the user what failed and how to resolve it, and end the turn.
