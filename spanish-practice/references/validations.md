# Validations

This document defines the validations used by spanish-practice.

---

## Phrasal Vocabulary Rule

- **Id**: phrasal-vocabulary-rule
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify that all vocabulary entries in SRS decks and all vocabulary prompts presented during sessions consist of multi-word phrasal expressions or complete clauses rather than single isolated words.
- **Message**: Vocabulary was presented or stored as an isolated single word.
- **Fix Action**: Reframe the vocabulary item into an idiomatic multi-word expression or clause before presenting or saving.
- **Applies To**:
    - student-profile.toon
    - session state

---

## Oxford Verb Clause Rule

- **Id**: oxford-verb-clause-rule
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Check that verb conjugation prompts in the Oxford Verb Routine embed the target verb inside a complete phrasal sentence frame rather than presenting standalone infinitive conjugation requests.
- **Message**: Verb conjugation routine prompt lacks a contextual clause frame.
- **Fix Action**: Construct a full sentence clause around the targeted verb transformation (e.g., *"Se me [olvidar - pretérito]..."*).
- **Applies To**:
    - session state

---

## TOON Syntax Check

- **Id**: toon-syntax-check
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify the profile declares all required top-level flat keys (`targetLanguage`, `dialectPreference`, `nativeLanguage`, `cefrLevel`, `masteryPercent`, `correctionPreference`, `interests`, `learningGoals`, `persistentErrors`) and both required tabular decks (`srsDeck` with its `item,translation,register,easiness,interval,repetitions,encounterCount,nextReviewDate` columns; `verbMasteryDeck` with its `group,modelVerb,tense,easiness,interval,repetitions,nextReviewDate` columns).
- **Message**: The student profile file has missing required fields or violates TOON format rules.
- **Fix Action**: Ensure the file strictly follows the TOON format syntax, declaring all flat keys above plus the `interests`, `learningGoals`, and `persistentErrors` arrays, and both tabular decks with their full column sets.
- **Applies To**:
    - student-profile.toon

*(Note: a structured, indentation-sensitive format like TOON is validated more reliably by checking for key presence directly than by a single regex — a prior version of this rule used a double negative-lookahead regex that matched only when the required fields were absent, the inverse of its intent.)*

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

## Correction Preference Branching

- **Id**: correction-preference-branching
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify that Halting Correction Mode is only triggered when the error matches an entry in `persistentErrors` or `correctionPreference` is `"explicit"`. Otherwise, minor first-occurrence errors must receive an inline implicit recast without pausing the timer or conversation.
- **Message**: Halting Correction Mode was triggered without checking `correctionPreference` and `persistentErrors` first.
- **Fix Action**: Re-evaluate the error against `correctionPreference` and `persistentErrors` before pausing the timer; downgrade to an inline recast if escalation criteria are not met.
- **Applies To**:
    - student-profile.toon
    - session state

---

## Receptive Input Presence

- **Id**: receptive-input-presence
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Check that each daily session includes a distinct Receptive Micro-Input step (a short leveled text or dialogue plus 1–2 comprehension/inference questions) between the SRS warm-up and core production.
- **Message**: The session skipped the Receptive Micro-Input phase.
- **Fix Action**: Insert a short leveled text recycling the session's target phrasal items, with comprehension questions, before continuing to core production.
- **Applies To**:
    - session state

---

## Pronunciation Claim Check

- **Id**: pronunciation-claim-check
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify the agent never asserts having heard, judged, or verified the learner's spoken pronunciation when no audio/voice modality is active in the session.
- **Message**: The agent made a pronunciation-assessment claim without an audio modality present.
- **Fix Action**: Retract the claim and reframe it as a text-based interference-pattern note for the learner's own self-practice.
- **Applies To**:
    - session state

---

## Quarter-Level Format Check

- **Id**: quarter-level-format-check
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - ^[ABC][12]\.(00|25|50|75)$
- **Message**: `cefrLevel` is not expressed in quarter-level granularity.
- **Fix Action**: Convert the blunt CEFR band to the nearest quarter-level increment (e.g. `B1.50`) using `masteryPercent` progress within the current band.
- **Applies To**:
    - student-profile.toon

---

## Onboarding First Turn Language

- **Id**: onboarding-first-turn-language
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - The first conversational turn in onboarding (when `onboardingComplete` is false) must be written entirely in English.
- **Message**: The onboarding process did not initiate in English.
- **Fix Action**: Reset the onboarding turn, and prompt the student with the greeting and background elicitation questions in English.
- **Applies To**:
    - conversation history
