# Sharp Edges

This document defines the sharp edges used by german-practice.

---

## Single-Word Drill Fallthrough

- **Id**: single-word-drill-fallthrough
- **Summary**: The agent defaults to testing vocabulary items or case endings as single isolated items rather than phrasal expressions.
- **Severity**: high
- **Situation**: During SRS warm-up or vocabulary feedback, the agent asks the student to define or translate a single word, or to give a bare case ending, without sentence context (e.g., "What does *vergessen* mean?" or "What's the dative ending for feminine nouns?").
- **Why**: Traditional language learning datasets focus on single-word translations and bare grammar tables, causing the model to revert to isolated prompts unless strictly constrained.
- **Solution**:
    - Always wrap vocabulary items and case forms in multi-word idiomatic chunks and complete clauses before presenting prompts to the user.
- **Symptoms**:
    - User is asked to translate, define, or decline in isolation, without surrounding phrasal or clause context.
- **Detection Pattern**: Prompts or SRS warm-up cards asking for the definition, translation, or bare declension of a single standalone word.

---

## Isolated Verb & Case Prompting

- **Id**: isolated-verb-case-prompting
- **Summary**: The agent prompts verb conjugations or case declensions as isolated citation forms instead of embedding them into complete phrasal clauses.
- **Severity**: high
- **Situation**: In the Duden Verb Routine or Case Declension Routine, the agent outputs prompts like "Conjugate *schreiben* in the Perfekt for *sie*" or "Decline *der Mann* in the accusative" instead of providing a full phrasal frame.
- **Why**: Standard verb and declension tables in NLP training data present forms as bare paradigms rather than contextualized clause structures.
- **Solution**:
    - Format all verb and case routine prompts within full sentence frames (e.g., *"Sie hat mir gestern einen Brief [schreiben - Partizip II]"*, *"Ich sehe [der Mann - Akkusativ] am Bahnhof"*).
- **Symptoms**:
    - The student receives bare grammatical instruction prompts without a contextual sentence frame.
- **Detection Pattern**: Verb or case routine prompts displaying infinitives or bare articles outside of sentence clause templates.

---

## Regional Drift

- **Id**: regional-drift
- **Summary**: The agent introduces vocabulary or grammatical structures from a different regional standard than the user's selected preference.
- **Severity**: high
- **Situation**: The student is practicing Austrian German, but the agent accidentally suggests Germany-standard vocabulary (e.g., "Januar" and "Sahne" instead of "Jänner" and "Rahm") or unfamiliar Swiss constructions.
- **Why**: Regional boundaries are complex, and the model's base training averages German-language content toward the Germany standard, causing it to fall back to that default unless heavily guided.
- **Solution**:
    - Explicitly query the user's `regionPreference` from the profile at the beginning of each prompt generation and double-check regional vocabulary before suggesting corrections.
- **Symptoms**:
    - The agent uses Germany-standard and Austrian/Swiss vocabulary interchangeably in the same output, or corrects regionalisms that are perfectly natural in the target standard.
- **Detection Pattern**: Dialogue responses containing vocabulary inconsistent with the active `regionPreference` key in the profile.

---

## Infinite Drill Loop

- **Id**: infinite-drill-loop
- **Summary**: The student gets stuck in an infinite drill loop in Correction Mode because the agent does not scaffold the expected response after multiple attempts.
- **Severity**: high
- **Situation**: The user makes a grammatical or case error, receives a drill prompt, tries to answer but makes a different/additional mistake, and the agent demands drills indefinitely without easing the requirements.
- **Why**: Rigid validation logic without scaffolding or difficulty downgrading causes user frustration and session abandonment.
- **Solution**:
    - If a student fails a drill response twice, automatically downgrade the drill complexity (e.g., from dynamic sentence creation to literal repetition of the correct sentence) and provide clear hints.
- **Symptoms**:
    - The conversation logs show three or more consecutive turns in Correction Mode with the user repeating variations of incorrect structures or expressing confusion.
- **Detection Pattern**: More than 2 consecutive failing drill evaluations in the conversation history without the agent offering structural scaffolding or simplified repetition.

---

## Diagnostic Ceiling Loop

- **Id**: diagnostic-ceiling-loop
- **Summary**: The OPI diagnostic continues to escalate complexity beyond the student's ceiling or fails to terminate when the student is clearly overwhelmed.
- **Severity**: medium
- **Situation**: The onboarding diagnostic keeps asking increasingly complex questions (e.g. Konjunktiv II hypotheticals) even after the user has failed simple Perfekt narration or case-marking tasks.
- **Why**: OPI requires identifying a clear floor and ceiling; if the agent doesn't check for consecutive patterns of errors, it will continue probing higher levels indefinitely.
- **Solution**:
    - Enforce a maximum of 6 diagnostic conversational turns, and terminate the diagnostic early if the user makes critical grammatical/vocabulary errors on 2 consecutive levels.
- **Symptoms**:
    - Onboarding conversation exceeds 6 turns, or continues to present subjunctive/Konjunktiv probes after the student fails basic Perfekt/Präteritum or case distinctions.
- **Detection Pattern**: Conversational OPI diagnostic steps exceeding 6 total turns, or probing higher CEFR levels when the previous level contains unresolved semantic breakdowns.

---

## Correction Preference Ignored

- **Id**: correction-preference-ignored
- **Summary**: The agent applies Halting Correction Mode to every error regardless of the profile's `correctionPreference` field.
- **Severity**: high
- **Situation**: A learner with `correctionPreference: "recasting"` makes a minor, first-occurrence error, and the agent freezes the timer and forces a full correction drill anyway, instead of recasting inline.
- **Why**: Training data over-represents maximally explicit tutor-correction dialogue, biasing the model toward the halting path by default even when a stored preference says otherwise.
- **Solution**:
    - Before pausing the timer, check `correctionPreference` and whether the error already appears in `persistentErrors`. Only escalate to Halting Correction Mode when the preference is `"explicit"` or the error is a repeat offense.
- **Symptoms**:
    - Every single error in a session — regardless of severity or repetition — triggers a full halting drill even though `correctionPreference` is `"recasting"`.
- **Detection Pattern**: Halting Correction Mode invoked on a first-occurrence error while `correctionPreference` in the active profile is `"recasting"`.

---

## False Pronunciation Verification

- **Id**: false-pronunciation-verification
- **Summary**: The agent claims to have heard, assessed, or verified the student's spoken pronunciation in a text-only session.
- **Severity**: high
- **Situation**: The agent tells the student something like "deine Aussprache war ausgezeichnet" or "ich habe gehört, dass du den ich-Laut mit dem ach-Laut verwechselt hast" when no audio or voice modality is present in the conversation.
- **Why**: Tutoring dialogue in training data frequently includes pronunciation feedback lines, and the model can generate these reflexively even though it has received no audio signal to evaluate.
- **Solution**:
    - Never assert perceived pronunciation quality. When a phrasal item carries known interference risk (e.g., ich-Laut/ach-Laut, umlaut vowel length), flag it as a brief "say this aloud" self-practice note rather than a scored or verified judgment.
- **Symptoms**:
    - Assistant messages reference how something "sounded" or was "pronounced" when the session has no audio input.
- **Detection Pattern**: Assistant turn containing a pronunciation-quality claim in a session with no active voice/audio modality.

---

## Receptive Phase Skipped

- **Id**: receptive-phase-skipped
- **Summary**: The agent collapses the daily session back into SRS warm-up → core production → correction → sync, omitting the 3-minute Receptive Micro-Input segment.
- **Severity**: medium
- **Situation**: A session transcript moves directly from the SRS warm-up into core spontaneous production with no leveled text or comprehension questions in between.
- **Why**: The original four-part partition is more heavily represented in prior session transcripts and examples, so the model can default back to the older habit unless explicitly checked.
- **Solution**:
    - Verify all five partition segments (SRS, Receptive Micro-Input, core production, correction, sync) occur before saving the profile at session end.
- **Symptoms**:
    - The student never receives a short reading/listening text with comprehension questions during the session.
- **Detection Pattern**: No distinct receptive-input turn (leveled text + comprehension question) appears between the SRS warm-up and core-production turns.

---

## Premature Language Switch

- **Id**: premature-language-switch
- **Summary**: The agent switches to full German too early during onboarding, confusing a beginner student.
- **Severity**: high
- **Situation**: The onboarding student is a complete beginner and responds in English or struggling German to the background prompt, but the agent mistakenly switches to German for the diagnostic probes instead of scaffolding in English.
- **Why**: Overly aggressive immersion defaults or language detection heuristics that mistake brief words or loanwords for advanced proficiency.
- **Solution**:
    - Enforce a rule that the agent must only switch to German dialogue if the user provides a coherent, multi-word response written in German (e.g., using conjugated verbs). If the user responds in English, single-word German, or indicates difficulty, keep the dialog and instructions in English.
- **Symptoms**:
    - The user expresses confusion, uses English questions, or types basic words, but the agent continues to prompt them in complex German.
- **Detection Pattern**: Prompting in German immediately following a user response containing no German verbs, or containing English phrases signaling confusion.

---

## Frequency-Blind Sequencing

- **Id**: frequency-blind-sequencing
- **Summary**: The agent introduces or drills low-frequency verb forms, case forms, or vocabulary before high-frequency ones because they appear "next" in a canonical grammar reference or textbook chapter order.
- **Severity**: high
- **Situation**: The agent runs the on-demand verb sweep strictly through weak-verb spelling subgroups before ever touching *sein*, *haben*, or the modal verbs, or introduces Genitiv practice before the learner has solid Dativ coverage, simply because that's the next stage in a fixed list.
- **Why**: Systematic-sweep instructions (progress through classification groups in order) can be followed too literally, overriding the frequency-tier prioritization that should govern which forms actually get surfaced to a given learner first.
- **Solution**:
    - Before introducing a new form, check per-tier mastery coverage in `verbMasteryDeck`/`caseMasteryDeck`/`srsDeck` and prioritize the lowest not-yet-mastered tier; only let functional-need triggers or a learner's diagnosed ceiling override this order.
- **Symptoms**:
    - A learner with near-zero Perfekt or modal-verb mastery is being drilled on Genitiv or Konjunktiv I; frequency tier 3 items appear in a deck before tier 1 items reach adequate mastery.
- **Detection Pattern**: New-item introductions in the mastery decks whose `frequencyTier` is 2 or 3 while tier-1 items in the same deck remain below an adequate mastery threshold, with no functional-need trigger justifying the exception.

---

## Prefix-Stranding Blindness

- **Id**: prefix-stranding-blindness
- **Summary**: The agent fails to flag separable-verb prefix placement errors because the sentence superficially resembles valid English word order.
- **Severity**: high
- **Situation**: The student writes "Ich aufstehe früh" or "Weil ich früh aufstehe möchte" and the agent does not flag the un-split or mis-placed prefix, or lets it pass as an inline recast without calling out that it's a structural (not merely stylistic) error.
- **Why**: The model's general-purpose training skews toward English SVO structure, which has no separable-prefix analogue, so it under-flags this specific German structural error relative to more "English-shaped" mistakes like gender or case.
- **Solution**:
    - Explicitly check every clause containing a separable or inseparable prefix verb for correct split/rejoin placement, independent of whether the sentence otherwise "reads fine."
- **Symptoms**:
    - Un-split separable verbs, or prefixes stranded mid-sentence, go uncorrected in student production.
- **Detection Pattern**: Student production containing a known separable-prefix verb in its unsplit infinitive-like form within a main clause, with no correction issued.

---

## Case Substitution Fallback

- **Id**: case-substitution-fallback
- **Summary**: The agent defaults to producing or accepting nominative-form articles and adjective endings regardless of the grammatical case actually required by the governing verb or preposition.
- **Severity**: high
- **Situation**: The student writes "Ich sehe der Mann" (should be "den Mann," accusative) and the agent's own generated example sentences, or its correction, also default back to the nominative article instead of the case-correct one.
- **Why**: The nominative is the citation/default form most heavily represented in training data, so both student and model carry a bias toward it unless the case-governing element is explicitly checked.
- **Solution**:
    - For every noun phrase in a generated or corrected sentence, explicitly identify its governing verb/preposition and required case before finalizing the article and adjective ending.
- **Symptoms**:
    - Accusative or dative contexts (direct objects, dative verbs, case-governing prepositions) surface with nominative-form articles in either the student's or the agent's own sentences.
- **Detection Pattern**: A noun phrase following a case-governing verb or preposition that retains its nominative article/ending instead of the required case form.

---

## False Präteritum Correction

- **Id**: false-preteritum-correction
- **Summary**: The agent "corrects" a learner's correct spoken-register use of Perfekt into Präteritum, treating Präteritum as inherently more correct.
- **Severity**: medium
- **Situation**: A learner narrates a past event using Perfekt ("Ich habe das Buch gelesen") in a conversational context, and the agent flags it as an error, recasting it into Präteritum ("Ich las das Buch") as if Perfekt were a mistake.
- **Why**: Written training data and formal grammar references disproportionately favor Präteritum, biasing the model toward treating it as the "more correct" past tense even though Perfekt is the dominant, native-like choice in spoken/conversational German for most verbs.
- **Solution**:
    - Treat Perfekt as the default-correct past tense in conversational register for all but a small set of high-frequency exceptions (*sein, haben*, modal verbs, a few others) that stay in Präteritum even in speech; only correct toward Präteritum for those exceptions or for genuinely formal/narrative-register production.
- **Symptoms**:
    - The agent penalizes or "improves" grammatically and register-appropriate Perfekt usage into Präteritum during conversational drills.
- **Detection Pattern**: A correction or recast that changes a learner's Perfekt construction to Präteritum in a conversational-register context, for a verb outside the sein/haben/modal exception set.
