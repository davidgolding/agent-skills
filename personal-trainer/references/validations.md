# Personal Trainer Validations

This document defines the validations used by personal-trainer.

## Profile Resolution Required

- **Id**: pt-profile-resolution-required
- **Severity**: error
- **Type**: semantic
- **Pattern**: A session proceeds to prescribe or manipulate training data without first verifying and reading `profile.toon` from the configured training directory.
- **Message**: A valid user profile must be resolved prior to processing training requests.
- **Fix Action**: Verify the presence of `profile.toon` in the configured training directory; when absent, initiate the onboarding workflow before generating training content.
- **Applies To**:
    - SKILL.md session start
    - references/interactions.md

---

## Onboarding Completeness

- **Id**: pt-onboarding-completeness
- **Severity**: error
- **Type**: schema
- **Pattern**: `profile.toon` written without all required sections: goals, training history, equipment, schedule, preferences, and the medical screen.
- **Message**: Profile must contain all required onboarding sections before program creation.
- **Fix Action**: Complete all missing intake fields per `references/onboarding.md` before generating the initial training block.
- **Applies To**:
    - profile.toon

---

## Contraindication Field Present

- **Id**: pt-contraindication-required
- **Severity**: error
- **Type**: semantic
- **Pattern**: The medical screen recorded a condition, injury, surgery, or flag, but no corresponding entry was derived into the contraindications field.
- **Message**: Every recorded medical finding must translate into an explicit contraindication entry.
- **Fix Action**: Map each condition, injury, surgery, or clinical flag to an explicit movement contraindication entry per `references/safety.md` prior to programming.
- **Applies To**:
    - profile.toon

---

## Red Flag Halt

- **Id**: pt-red-flag-halt
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?i)\bchest pain\b
    - (?i)\b(can'?t breathe|shortness of breath)\b
    - (?i)\b(fainted|fainting|blacked out|passed out)\b
    - (?i)\bnumbness|tingling\b
    - (?i)\b(sharp|searing) pain\b
- **Message**: Immediate cessation of programming is required upon detection of red-flag symptoms.
- **Fix Action**: Halt training progression immediately, address the symptom directly per `references/safety.md`, and resume programming only when the issue is resolved or medically cleared.
- **Applies To**:
    - workout report responses
    - references/interactions.md

---

## Recent-Window Read Only

- **Id**: pt-log-window-bound
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A session reads `log.toon` entries older than the current block's working window instead of relying on a compressed summary.
- **Message**: Session context must remain bounded to the current block's workout entries.
- **Fix Action**: Restrict routine log reading to the active block's entries and access older training history through compressed summary rows.
- **Applies To**:
    - log.toon

---

## Block Review Triad Completeness

- **Id**: pt-block-review-triad
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A block review updates `program.toon` without completing both the profile re-screen and log compression.
- **Message**: Block review requires simultaneous execution of all three triad components.
- **Fix Action**: Execute the plan reshape, profile health re-screen, and log compression together at each block boundary.
- **Applies To**:
    - program.toon
    - profile.toon
    - log.toon

---

## Modality Reference Scoping

- **Id**: pt-modality-scoping
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A request naming a single modality triggers loading of an evidence file for an unrequested modality.
- **Message**: Evidence loading must remain strictly scoped to the active training modality.
- **Fix Action**: Restrict evidence loading to the specific file(s) under `references/evidence/` that directly match the active request modality.
- **Applies To**:
    - references/evidence/*.md

---

## Profile Confirmation Prior to Write

- **Id**: pt-profile-confirmation-gate
- **Severity**: error
- **Type**: semantic
- **Pattern**: `profile.toon` or `program.toon` written to disk during onboarding before the user has reviewed and confirmed the intake summary.
- **Message**: Profile summary must be reviewed and confirmed by the user before files are created.
- **Fix Action**: Present the captured profile summary to the user and obtain explicit confirmation before persisting profile and program files.
- **Applies To**:
    - references/interactions.md
    - references/onboarding.md
