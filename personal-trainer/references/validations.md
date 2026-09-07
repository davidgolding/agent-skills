# Validations

This document defines the validations used by personal-trainer.

---

## Data Location Pointer Required

- **Id**: pt-data-pointer-required
- **Severity**: error
- **Type**: instruction
- **Pattern**: A session proceeds to read or write profile, program, log, or measurement data without first resolving `~/.personal-trainer/location.toon`.
- **Message**: No data location pointer was resolved before accessing training data.
- **Fix Action**: Resolve the pointer file first. If it does not exist, run onboarding to establish and record the data location before doing anything else.
- **Applies To**:
    - SKILL.md session start

---

## Onboarding Completeness

- **Id**: pt-onboarding-completeness
- **Severity**: error
- **Type**: instruction
- **Pattern**: `profile.toon` is written without all of: goals, training history, equipment, schedule, preferences, and the full medical screen populated.
- **Message**: Profile is missing required onboarding fields.
- **Fix Action**: Return to onboarding and complete the missing fields per `references/onboarding.md` before producing any program.
- **Applies To**:
    - profile.toon

---

## Contraindication Field Present

- **Id**: pt-contraindication-required
- **Severity**: error
- **Type**: instruction
- **Pattern**: The medical screen recorded a condition, injury, surgery, or flag, but no corresponding entry was derived into the contraindications field.
- **Message**: Medical screen answers exist without derived contraindications.
- **Fix Action**: Translate every recorded condition, injury, surgery, or flag into an explicit contraindication entry per `references/safety.md` before programming.
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
- **Message**: A red-flag symptom was reported and programming continued anyway.
- **Fix Action**: Halt progression, address the symptom per `references/safety.md`, and do not resume programming until it is resolved or cleared.
- **Applies To**:
    - workout report responses

---

## Recent-Window Read Only

- **Id**: pt-log-window-bound
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A session reads `log.toon` entries older than the current block's working window instead of relying on a compressed summary.
- **Message**: Session context included historical log entries beyond the working window.
- **Fix Action**: Read only the current block's window plus compressed summaries; compress anything older at the next block review.
- **Applies To**:
    - log.toon

---

## Block Review Triad Completeness

- **Id**: pt-block-review-triad
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A block review updates `program.toon` without also completing the profile re-screen and the log compression.
- **Message**: Block review ran without completing all three required actions.
- **Fix Action**: Perform all three actions of block review — plan reshape, profile re-screen, and log compression — every time a block boundary is reached.
- **Applies To**:
    - program.toon
    - profile.toon
    - log.toon

---

## Modality Reference Scoping

- **Id**: pt-modality-scoping
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A request naming a single modality triggers loading of an evidence file for a different, unrequested modality.
- **Message**: Evidence file loaded outside the requested modality's scope.
- **Fix Action**: Load only the evidence file(s) under `references/evidence/` matching the modality named in the request.
- **Applies To**:
    - references/evidence/*.md
