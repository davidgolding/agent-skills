# Validations

This document defines the validations used by german-practice.

---

## Phrasal Vocabulary Rule

- **Id**: phrasal-vocabulary-rule
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify that all vocabulary entries in SRS decks and all vocabulary prompts presented during sessions consist of multi-word phrasal expressions or complete clauses rather than single isolated words, and that every noun-headed entry carries a gender tag (`der`/`die`/`das`) alongside its register tag.
- **Message**: Vocabulary was presented or stored as an isolated single word, or is missing its gender tag.
- **Fix Action**: Reframe the vocabulary item into an idiomatic multi-word expression or clause before presenting or saving, and add the missing gender tag.
- **Applies To**:
    - student-profile.toon
    - session state

---

## Duden Verb & Case Clause Rule

- **Id**: duden-verb-case-clause-rule
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Check that verb conjugation prompts in the Duden Verb Routine and declension prompts in the Case Declension Routine embed the target verb or noun phrase inside a complete phrasal sentence frame rather than presenting standalone infinitive conjugation or bare-article declension requests.
- **Message**: Verb conjugation or case declension routine prompt lacks a contextual clause frame.
- **Fix Action**: Construct a full sentence clause around the targeted verb transformation or case form (e.g., *"Sie hat mir gestern einen Brief [schreiben - Partizip II]..."*, *"Ich fahre mit [der Zug - Dativ]..."*).
- **Applies To**:
    - session state

---

## TOON Syntax Check

- **Id**: toon-syntax-check
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Verify the profile declares all required top-level flat keys (`targetLanguage`, `regionPreference`, `nativeLanguage`, `cefrLevel`, `masteryPercent`, `correctionPreference`, `interests`, `learningGoals`, `persistentErrors`) and all three required tabular decks (`srsDeck` with its `item,translation,gender,register,frequencyTier,easiness,interval,repetitions,encounterCount,nextReviewDate` columns; `verbMasteryDeck` with its `group,modelVerb,tense,frequencyTier,easiness,interval,repetitions,nextReviewDate` columns; `caseMasteryDeck` with its `case,gender,number,frequencyTier,easiness,interval,repetitions,nextReviewDate` columns).
- **Message**: The student profile file has missing required fields or violates TOON format rules.
- **Fix Action**: Ensure the file strictly follows the TOON format syntax, declaring all flat keys above plus the `interests`, `learningGoals`, and `persistentErrors` arrays, and all three tabular decks with their full column sets.
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
- **Fix Action**: Evaluate the user's current performance ceiling immediately, write the diagnosed CEFR level to `student-profile.toon`, set `onboardingComplete: true`, and transition to the first standard practice lesson.
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

---

## Frequency Tier Sequencing Check

- **Id**: frequency-tier-sequencing-check
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Check that newly introduced items in `verbMasteryDeck`, `caseMasteryDeck`, and `srsDeck` are drawn from the lowest not-yet-adequately-mastered `frequencyTier` before higher tiers are introduced, unless a functional-need trigger from the conversation justifies the exception.
- **Message**: A higher-frequency-tier item was introduced while a lower-tier item remains unmastered.
- **Fix Action**: Re-order the next introduced item to the lowest not-yet-mastered tier, or record the functional-need trigger that justified the exception.
- **Applies To**:
    - student-profile.toon
    - session state

---

## Noun Capitalization Check

- **Id**: noun-capitalization-check
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Check that all German nouns in agent-generated example sentences and corrections are capitalized, and that student production is checked for missing noun capitalization as its own error category rather than folded into general spelling notes.
- **Message**: A German noun was presented in lowercase, or a student's missing capitalization went uncorrected.
- **Fix Action**: Capitalize the noun in agent-generated text, and flag missing capitalization in student production as a distinct, briefly-noted mechanical error.
- **Applies To**:
    - session state
