# Critical Text Collation Interactions

This document defines the interaction flow used by critical-text-collate.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the user's response is needed, and let the conversation's natural back-and-forth carry the wait. Route through the platform's blocking question tool (e.g. `AskUserQuestion`) when presenting the witness-siglum choice, the rich-text/highlight schema choice, the segmentation-mode choice, or the collation plan, so each request surfaces as a first-class prompt instead of plain text.
2. **Validation Gatekeeping**: Advance from the Plan phase to the Collate phase only once the user's next message explicitly approves the identified file list and the proposed output path; a revision request or a cancellation leaves the corpus and the output path untouched.
3. **State Retention**: Carry the target folder, the witness sigla, the formatting schema, the segmentation mode, and the approved output path forward in the conversation, rather than in an internal registry the runtime tracks on its own.

## Execution Flow

### Phase 01: Scope

- **Objective**: Establish the corpus, the column labels, the formatting schema, and the segmentation mode before any parsing begins.
- **Agent Action**: Ask the user for the directory containing the `.docx` transcription documents. Confirm how columns should be labeled — document filename, or a custom short name/siglum per witness. Ask whether specific rich-text schemas or highlight colors should apply to variants. Ask whether to group lines/verses by explicit markers such as headings or verse numbers, or to use automatic sentence segmentation.
- **Human Gate/Intervention**: The user supplies the folder path and answers the labeling, formatting, and segmentation questions.
- **Proceed When**: A readable directory containing at least two `.docx` witnesses is identified, and the labeling and segmentation choices are settled.
- **Pause When**: The supplied path is missing, unreadable, or holds fewer than two `.docx` files — ask the user for a valid corpus directory.

### Phase 02: Plan

- **Objective**: Present the collation scope for approval before touching the corpus or writing any output.
- **Agent Action**: List every identified witness file with the siglum assigned to it, state the segmentation mode and formatting schema in effect, and name the proposed output spreadsheet path. Request explicit user approval.
- **Human Gate/Intervention**: The user approves, revises, or cancels the presented plan.
- **Proceed When**: The user's response is an explicit approval.
- **Pause When**: The plan has just been presented — end the turn and wait for the user's response before parsing or writing anything.

### Phase 03: Collate

- **Objective**: Parse each witness and align the corpus into collation rows.
- **Agent Action**: Extract paragraph text and run formatting from each `.docx`, mapping footnotes to their character offsets before segmentation. Scrub `//` and `/* ... */` comments with an escape-aware scanner. Segment into sentences per the agreed mode, align the sentence segments across all witnesses as peers, then align nodes word by word inside each group, parsing `<word>` emendations and `<prior\interpolated>` interpolations as single composite nodes and analyzing variance species to guide each match.
- **Human Gate/Intervention**: None; this phase runs autonomously on the approved plan.
- **Proceed When**: Every witness is parsed and every node is assigned to a `segment` group and an alignment row.
- **Pause When**: An entire sentence group aligns below the minimum similarity threshold across all witnesses — surface that group to the user rather than forcing a match.

### Phase 04: Emit

- **Objective**: Write the collation workbook and confirm it opens cleanly.
- **Agent Action**: Write `segment` to cell A1 and the sentence-group index down Column A, one column per witness under its siglum. Render each node through `CellRichText`/`TextBlock` so `.docx` run formatting survives, join multi-entity nodes with `•` (U+2022), and leave a cell blank where its witness has no node for that row. Validate the workbook programmatically by reopening it, then report the output path.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The workbook reopens cleanly and passes every rule in `validations.md`.
- **Pause When**: The written workbook fails to reopen — repair the rich-text generation per the `corrupt-excel-rich-text` sharp edge before reporting completion.

## Handoff

- **The Completion State**: The output workbook opens cleanly in a library round-trip, Column A carries a populated `segment` index under a `segment` header, every witness occupies its own labeled column, `.docx` run formatting survives in the cells, multi-entity nodes are bullet-joined, absent nodes leave blank cells, and the output path is reported to the user.
- **Exception/Fallback Handoff**: If a sentence group cannot be aligned above the similarity threshold after three attempts, or if the workbook fails to reopen after three rich-text repair attempts, stop autonomous work and present the unresolved group or the failing cell range to the user for manual resolution.
