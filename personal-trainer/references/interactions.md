# Personal Trainer Interactions

This document defines the human-in-the-loop interaction flow and protocols for personal-trainer.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever input or confirmation from the user is required, allowing the natural conversational exchange to drive state progression. Use the platform's blocking question tool when presenting constrained multiple-choice options (such as training frequency, session duration, or primary goal selection), and reserve open dialogue for narrative history.
2. **Validation Gatekeeping**: Gate profile persistence, program generation, and load progression behind explicit validation checks. Present captured intake data to the user for explicit confirmation before writing `profile.toon`.
3. **State Retention**: Maintain complete conversational and domain state inside persistent TOON files (`profile.toon`, `program.toon`, `log.toon`, `measurements.toon`) within the agent's configured training directory, ensuring all recommendations remain grounded across sessions.
4. **Immediate Red-Flag Interruption**: Halt training prescription immediately whenever a red-flag symptom appears in a workout report or conversation, prioritizing user health assessment above any scheduled programming.

## Execution Flow

### Phase 01: Onboarding Intake & Profile Initialization

- **Objective**: Establish the athlete's training background, goals, schedule, equipment, and medical screening before generating any training content.
- **Agent Action**: Verify the presence of `profile.toon` in the agent's configured training directory. If missing, execute the 6-step onboarding sequence from `references/onboarding.md` one topic at a time. Translate medical findings into explicit movement contraindications per `references/safety.md`. Summarize the captured profile to the user in clear language. Upon confirmation, write `profile.toon`, `measurements.toon`, and `program.toon`, and initialize `log.toon` in the configured directory.
- **Human Gate/Intervention**: The user provides intake responses and explicitly approves the profile summary before any program file is written.
- **Proceed When**: The user confirms the intake summary and all required profile fields are populated.
- **Pause When**: Awaiting an intake response or explicit approval of the captured profile summary.

### Phase 02: Routine Session Programming & Autoregulation

- **Objective**: Address daily training requests, autoregulate upcoming sessions based on completed workout reports, and answer exercise-science queries.
- **Agent Action**: Read `profile.toon`, `program.toon`, and the current block's window from `log.toon` in the configured training directory. Route requests across three pathways:
  - *Workout Report*: Screen report against red-flag symptoms. If clear, record entry in `log.toon`, apply modality-specific progression rules from `references/progression.md`, and state the next session's adjusted load and rationale.
  - *Session Request*: Verify prescribed movements against `profile.toon` contraindications and place within the standing weekly program load.
  - *Domain Query*: Consult the matching evidence file under `references/evidence/`. If the inquiry outruns the cached evidence, conduct a targeted search and report findings with explicit source citation.
- **Human Gate/Intervention**: The user submits workout metrics, raises training inquiries, or answers clarifying questions regarding ambiguous RIR/RPE values.
- **Proceed When**: Workout data is successfully logged, autoregulation adjustments are calculated, or training sessions are verified and delivered.
- **Pause When**: Clarification is needed on ambiguous workout metrics (e.g., unspecified RIR or incomplete set details), or a red-flag symptom requires immediate user assessment.

### Phase 03: Block Review & Re-Screening

- **Objective**: Transition between training blocks, adjust the macrocycle based on measurement trends, re-screen medical status, and compress historical workout logs.
- **Agent Action**: When a block completes or the user requests a program reset, execute the triad:
  1. Evaluate measurement trends and draft the subsequent block's `program.toon`.
  2. Prompt the user with the brief medical re-screen from `references/safety.md` to capture any new injuries, medications, or constraints, updating `profile.toon`.
  3. Compress the completed block's workout entries in `log.toon` into a compact trend summary row per `references/schemas.md`.
- **Human Gate/Intervention**: The user completes the medical re-screen and reviews the proposed program for the upcoming block.
- **Proceed When**: The medical re-screen is recorded, the log entries are compressed, and the user approves the new block structure.
- **Pause When**: Awaiting the user's responses to the medical re-screen or confirmation of the new block's plan.

## Handoff

- **The Completion State**: Persistent TOON files reflect current training status, the user possesses an actionable prescription or clear progression adjustment, and all movement prescriptions comply with recorded contraindications.
- **Exception/Fallback Handoff**: If a user reports a red-flag symptom (chest pain, unexplained syncope, severe shortness of breath, new neurological symptoms, or acute joint pain), stop all programming immediately, explain the health rationale, and recommend direct consultation with a qualified medical professional before resuming training.
