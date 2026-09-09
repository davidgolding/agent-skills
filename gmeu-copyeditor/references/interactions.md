# GMEU Copyeditor Interactions

This document defines the interaction flow used by gmeu-copyeditor.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the user's response is needed — an unstated copyediting level, a usage problem with several defensible resolutions — and let the conversation's natural back-and-forth carry the wait. Route through the platform's blocking question tool (e.g. `AskUserQuestion`) whenever presenting the level choice or a set of alternatives, so the request surfaces as a first-class prompt instead of plain text.
2. **Validation Gatekeeping**: Begin the editing pass once a Light, Medium, or Heavy level is established and the author's identified voice has been stated, and emit each suggestion once it carries its governing citation and sits inside the selected level's rubric.
3. **State Retention**: Carry the established level and the identified voice forward in the conversation, checking each subsequent suggestion against both — rather than relying on a registry the runtime tracks on its own.

## Execution Flow

### Phase 01: Establish Level

- **Objective**: Fix the copyediting level that governs which suggestions fall in scope.
- **Agent Action**: Read the prompt for a stated Light, Medium, or Heavy level; where the prompt states none, present the three levels and their rubrics through the platform's blocking question tool.
- **Human Gate/Intervention**: The user states or selects the copyediting level.
- **Proceed When**: A Light, Medium, or Heavy level is stated in the prompt or chosen by the user.
- **Pause When**: The prompt names no level — ask the user to choose one before reading the text for errors.

### Phase 02: Identify Voice

- **Objective**: Establish the author's voice as the baseline every later suggestion is checked against.
- **Agent Action**: Analyze the text for the author's voice — the high-fidelity transmission of their consciousness through words — and state that identified voice to the user as the pass's first output.
- **Human Gate/Intervention**: The user may correct or refine the stated voice; a correction replaces the agent's reading for the rest of the pass.
- **Proceed When**: The identified voice has been stated to the user.
- **Pause When**: The supplied text is too short or too fragmentary to support a voice reading — ask the user for more of the manuscript or for their own description of the voice.

### Phase 03: Edit

- **Objective**: Produce the suggestion set the selected level authorizes, each grounded in its authority and holding the identified voice.
- **Agent Action**: Run the mechanical-editing and correlating-parts sweeps, then the language-editing and content-editing scopes the selected level authorizes per `references/patterns.md`; ground each usage judgment in a GMEU entry and each grammar judgment in a CGG topic and section; explain each usage problem through its guideline and offer the alternatives among which the user chooses.
- **Human Gate/Intervention**: The user resolves each flagged usage problem or selects from the offered alternatives.
- **Proceed When**: Every suggestion carries its required citation and sits inside the selected level's rubric.
- **Pause When**: A usage problem admits several defensible resolutions — present the alternatives and let the user choose rather than resolving it unilaterally.

### Phase 04: Report

- **Objective**: Deliver the suggestions in the skill's commentary format.
- **Agent Action**: Present the suggestions as a sequential list of individual Markdown paragraphs, each opening with the referenced text in bold, then a colon, then the commentary, closing with the inline citation where one is required; emit proofreading findings as commentary alone.
- **Human Gate/Intervention**: The user accepts, revises, or requests a different level of pass.
- **Proceed When**: Every suggestion has been formatted and cited, and the voice statement precedes the list.
- **Pause When**: The user requests a different copyediting level — return to Phase 01 with that level and re-run the pass.

## Handoff

- **The Completion State**: The identified voice has been stated, every suggestion is formatted per the commentary contract and carries its governing GMEU or CGG citation, and no suggestion exceeds the selected level's rubric.
- **Exception/Fallback Handoff**: When no GMEU entry or CGG section governs a suspected problem, present it to the user as an unresolved query — describing the problem and asking for their judgment — rather than citing an unverified entry.
