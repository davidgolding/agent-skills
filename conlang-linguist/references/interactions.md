# Conlang Linguist Interactions

This document defines the interaction flow used by conlang-linguist.

## Interaction Rules

1. **Gate workspace changes through the blocking question tool.** Before creating a language workspace, or before changing the language name, a sound law, a stage, an event, `<Language> Premise.md`, or an etymon, present the proposal with `AskUserQuestion` (or the platform's equivalent) and end the turn. The proposal names the files to change and, for a revision, a sample of the forms `soundchange.py apply` shows will move. Additions within an established section (new etyma, new corpus texts, new prose) need no gate. Announce them in the response instead.
2. **Announce reframing and continue.** When an off-frame request is restated as a terrestrial counterfactual, state the counterfactual and what was dropped in the response, then proceed in the same turn. The user can redirect in their next message, and a reframe changes no existing files, so no gate is needed.
3. **One batch per turn for large depths.** When a requested depth exceeds what one response can hold, deliver one batch, report the count against the target, and name the next batch. The user's next message either continues or redirects.
4. **Ask one question at a time.** When the premise leaves a historically consequential choice open (an ancestor stage, a contact date, a donor language), ask about that one choice with the blocking question tool, offering historically plausible options.

## Execution Flow

### Phase 01: Frame

- **Objective**: Establish the historical frame the request answers to.
- **Agent Action**: Read `<Language> Premise.md` and the sections the request touches. For advanced depth and above, search rather than reading whole files. Restate any off-frame request as a terrestrial counterfactual. If no workspace exists, draft the premise the request implies.
- **Human Gate-Intervention**: A blocking question only when the premise leaves a consequential choice open (Interaction Rule 4).
- **Proceed When**: The premise answers every historical question the request raises.
- **Pause When**: A consequential premise choice is open, so ask it and end the turn.

### Phase 02: Propose

- **Objective**: Get the user's approval for any change that rewrites existing forms or creates a workspace.
- **Agent Action**: For a new workspace, present its path, its premise, and the files to be created. For a revision, present the changed law, stage, event, premise, or etymon and its motivation, with a before/after sample from `apply`. Skip this phase for additions within established sections.
- **Human Gate-Intervention**: The user approves, revises, or declines through the blocking question tool.
- **Proceed When**: The user approves, or the work is a pure addition that needs no gate.
- **Pause When**: The proposal has just been presented, so end the turn and wait. If the user asks for a revision, re-present it. If they decline, leave the workspace unchanged.

### Phase 03: Build

- **Objective**: Make the change and compile.
- **Agent Action**: Edit the engine inputs and section prose together, keeping each law's ID the same in `<Language> Cascade.md` and `<Language> Phonology.md`. Run `soundchange.py check`, fix any errors it reports, then run `compile`.
- **Human Gate-Intervention**: None.
- **Proceed When**: `check` reports no errors and `compile` has run.
- **Pause When**: `check` still fails after three correction attempts, so present the remaining errors to the user and end the turn.

### Phase 04: Log and Report

- **Objective**: Record what changed and show the work.
- **Agent Action**: When `compile` reports changed forms, write the errata entry from `<Language> Compiled Changes.md` before any further compile. Quote `trace` output for the derivations the response discusses. Report depth progress as count / target, and name the next batch.
- **Human Gate-Intervention**: None.
- **Proceed When**: Errata is current and the report is written.
- **Pause When**: Not applicable.

## Handoff

- **Completion State**: `soundchange.py check` is clean, every surface form in the response and the section files matches the current compiled output, errata records every revision made this turn, and depth progress is reported against its target.
- **Exception/Fallback Handoff**: If `check` cannot be made clean in three attempts, or the user declines a proposed revision that the requested work depends on, stop. Present the unresolved errors or the dependency, and leave the workspace in its last compiled state.
