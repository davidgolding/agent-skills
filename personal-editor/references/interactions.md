# Personal Editor Interactions

This document defines the interaction flow used by personal-editor.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the user's input is needed, and let the conversation's natural back-and-forth carry the wait. Route through the platform's blocking question tool (e.g. `AskUserQuestion`) when offering the user a choice between concrete options, such as which chunk of an over-length passage to analyze first.
2. **Validation Gatekeeping**: Advance from intake to analysis once the passage passes the word-count check; past the limit, hold every pass until the user supplies a passage within it.
3. **State Retention**: Carry the passage, the word count, and each completed pass's findings forward in the conversation, so the four sections of the final report all reference the same text.

## Execution Flow

### Phase 01: Intake

- **Objective**: Confirm the submitted passage is within the analyzable bound before any analytical pass runs.
- **Agent Action**: Count the words in the submitted passage and compare against the 2000-word limit per the `word-count-validation` rule.
- **Human Gate/Intervention**: Required only when the passage exceeds the limit — the user supplies a shorter passage or chooses a chunk to analyze first.
- **Proceed When**: The passage measures 2000 words or fewer.
- **Pause When**: The passage exceeds 2000 words — report the measured count, politely request a shorter passage, and offer to split it into chunks under the limit, one chunk per invocation.

### Phase 02: Analyze and Report

- **Objective**: Run the four passes and deliver the synthesized report.
- **Agent Action**: Execute the copyediting, prose-fingerprint, rhetorical-figure, and adjudication passes as distinct sequential passes, grounding each in its sub-skill; compile the results into the four-section Markdown report, marking line edits in CriticMarkup and phrasing each as an offer the writer can decline.
- **Human Gate/Intervention**: None; this phase runs to completion once intake passes.
- **Proceed When**: All four passes have run and the report carries all four sections in order.
- **Pause When**: A submitted passage turns out to be unreadable or empty — ask the user to resupply the text.

## Handoff

- **The Completion State**: The four-section report is delivered, every claim cites the passage segment it attaches to, the caliber rating names its supporting evidence, and the writer's voice and intent are intact.
- **Exception/Fallback Handoff**: When the user's request conflicts with the guidance in `patterns.md`, `sharp_edges.md`, or `validations.md`, politely state the conflicting guidance and the reason behind it, then let the user decide how to proceed. When a sub-skill named in the Mandate is unavailable, state which grounding was missing in the affected section rather than presenting that pass's findings as rule-derived.
