# Validations

This document defines the validations used by spanish-practice.

---

## TOON Syntax Check

- **Id**: toon-syntax-check
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?!.*interests\b)(?!.*srsDeck\b).*$
- **Message**: The student profile file has missing required fields or violates TOON format rules.
- **Fix Action**: Ensure the file strictly follows the TOON format syntax, declaring flat keys, Interests, learningGoals, persistentErrors arrays, and tabular decks for SRS and Curriculum.
- **Applies To**:
    - student-profile.toon

---

## Diagnostic OPI Turn Bound

- **Id**: diagnostic-opi-turn-bound
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Check that during diagnostic onboarding, the session exits the diagnostic state and sets `onboardingComplete: true` in the profile within 6 total diagnostic conversational turns.
- **Message**: Onboarding diagnostic session is exceeding the 6-turn limit.
- **Fix Action**: Evaluate the user's current performance ceiling immediately, write the diagnosed CEFR level to `student-profile.toon`, set `onboardingComplete: true` to true, and transition to the first standard practice lesson.
- **Applies To**:
    - student-profile.toon
    - conversation history

---

## Drill State Validation

- **Id**: drill-state-validation
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify that the core practice session timer is paused during an active drill and that the conversation does not advance until the active drill state is marked cleared.
- **Message**: The core conversation advanced or the timer decreased while a student correction drill was active and unresolved.
- **Fix Action**: Immediately pause the timer, restore the active drill prompt, and require the student to resolve it before proceeding.
- **Applies To**:
    - student-profile.toon
    - session state

---
