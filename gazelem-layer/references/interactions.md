# Gazelem Layer Interactions

This document defines the interaction flow used by gazelem-layer.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the user's response is needed, and let the conversation's natural back-and-forth carry the wait. Route through the platform's blocking question tool (e.g. `AskUserQuestion`) whenever requesting missing inputs or confirming a destination-folder write.
2. **Validation Gatekeeping**: Advance from Verify Inputs to Segmentation only once both the Source Corpus and Destination Folder are confirmed; advance from Confirm Writes to file output only once the user has explicitly approved the listed file changes.
3. **State Retention**: Carry the confirmed Source Corpus, Destination Folder, and the list of files to be created or modified forward in the conversation — not in an internal registry the runtime tracks on its own.

## Execution Flow

### Phase 01: Verify Inputs

- **Objective**: Confirm the Source Corpus and Destination Folder are both available before any segmentation or extraction begins.
- **Agent Action**: Check the conversation and any supplied paths for both the Source Corpus and the Destination Folder.
- **Human Gate/Intervention**: The user supplies whichever input is missing.
- **Proceed When**: Both the Source Corpus and Destination Folder are confirmed.
- **Pause When**: Either input is missing — ask the user for it directly and wait for their reply before starting Phase 1 (Document Segmentation).

### Phase 02: Confirm Writes

- **Objective**: Get explicit user approval for the destination-folder file changes before writing or modifying any files.
- **Agent Action**: List exactly which files in the destination folder will be created (new) or appended to (existing) as a result of the current run.
- **Human Gate/Intervention**: The user approves, or asks for a change to, the listed writes.
- **Proceed When**: The user's response is an explicit approval.
- **Pause When**: The file list has just been presented — end the turn and wait for the user's response before writing or modifying any file.

## Handoff

- **The Completion State**: All destination files listed in Phase 02 have been appended to (never overwritten or truncated), and the user has seen confirmation of what was written.
- **Exception/Fallback Handoff**: If the user does not approve the listed writes, hold all file output and ask what should change instead, returning to Phase 02 once revised.
