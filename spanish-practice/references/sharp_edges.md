# Sharp Edges

This document defines the sharp edges used by spanish-practice.

---

## Single-Word Drill Fallthrough

- **Id**: single-word-drill-fallthrough
- **Summary**: The agent defaults to testing vocabulary items as single isolated words rather than phrasal expressions.
- **Severity**: high
- **Situation**: During SRS warm-up or vocabulary feedback, the agent asks the student to define or translate a single word without sentence context (e.g., "What does *atiborrarse* mean?").
- **Why**: Traditional language learning datasets focus on single-word translations, causing the model to revert to single-word prompts unless strictly constrained.
- **Solution**:
    - Always wrap vocabulary items in multi-word idiomatic chunks and complete clauses (e.g. *atiborrarse de comida*, *dar por sentado que...*) before presenting prompts to the user.
- **Symptoms**:
    - User is asked to translate or define isolated headwords without surrounding phrasal context.
- **Detection Pattern**: Prompts or SRS warm-up cards asking for the definition or translation of a single standalone Spanish or English word.

---

## Isolated Verb Prompting

- **Id**: isolated-verb-prompting
- **Summary**: The agent prompts verb conjugations as isolated citation forms instead of embedding them into complete phrasal clauses.
- **Severity**: high
- **Situation**: In the Oxford Verb Routine, the agent outputs prompts like "Conjugate *salir* in present subjunctive for *nosotros*" instead of providing a full phrasal frame.
- **Why**: Standard verb tables in NLP training data present verbs as bare paradigms rather than contextualized clause structures.
- **Solution**:
    - Format all verb routine prompts within full sentence frames, especially for reflexive and indirect structures (e.g., *"Tan pronto como nosotros [salir - pres. subj.] del teatro, te llamo"*).
- **Symptoms**:
    - The student receives bare grammatical instruction prompts without a contextual sentence frame.
- **Detection Pattern**: Verb routine prompts displaying infinitive verbs outside of sentence clause templates.

---

## Dialect Drift

- **Id**: dialect-drift
- **Summary**: The agent introduces regional vocabulary or grammatical structures from a different dialect than the user's selected preference.
- **Severity**: high
- **Situation**: The student is practicing Argentine Spanish (voseo) but the agent accidentally suggests European Spanish verbs (vosotros) or Mexican vocabulary (e.g., using "pluma" instead of "lapicera" or "bolígrafo").
- **Why**: Dialect boundaries are complex, and the model's base training averages Spanish dialects, causing it to fall back to general Spanish unless heavily guided.
- **Solution**:
    - Explicitly query the user's dialect preference from the profile at the beginning of each prompt generation and double-check regional vocabulary before suggesting corrections.
- **Symptoms**:
    - The agent uses voseo and vosotros interchangeably in the same output, or corrects regionalisms that are perfectly natural in the target dialect.
- **Detection Pattern**: Dialogue responses containing grammatical conjugations or idiomatic words inconsistent with the active dialectPreference key in the profile.

---

## Infinite Drill Loop

- **Id**: infinite-drill-loop
- **Summary**: The student gets stuck in an infinite drill loop in Correction Mode because the agent does not scaffold the expected response after multiple attempts.
- **Severity**: high
- **Situation**: The user makes a grammatical mistake, receives a drill prompt, tries to answer but makes a different/additional mistake, and the agent demands drills indefinitely without easing the requirements.
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
- **Situation**: The onboarding diagnostic keeps asking increasingly complex questions even after the user has failed simple narrative or conditional tasks.
- **Why**: OPI requires identifying a clear floor and ceiling; if the agent doesn't check for consecutive patterns of errors, it will continue probing higher levels indefinitely.
- **Solution**:
    - Enforce a maximum of 6 diagnostic conversational turns, and terminate the diagnostic early if the user makes critical grammatical/vocabulary errors on 2 consecutive levels.
- **Symptoms**:
    - Onboarding conversation exceeds 6 turns, or continues to present hypothetical/subjunctive probes after the student fails basic preterite/imperfect distinctions.
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
- **Situation**: The agent tells the student something like "tu pronunciación fue excelente" or "noté que confundiste la 'b' con la 'v'" when no audio or voice modality is present in the conversation.
- **Why**: Tutoring dialogue in training data frequently includes pronunciation feedback lines, and the model can generate these reflexively even though it has received no audio signal to evaluate.
- **Solution**:
    - Never assert perceived pronunciation quality. When a phrasal item carries known interference risk for the learner's dialect, flag it as a brief "say this aloud" self-practice note rather than a scored or verified judgment.
- **Symptoms**:
    - Assistant messages reference how something "sounded" or was "pronounced" when the session has no audio input.
- **Detection Pattern**: Assistant turn containing a pronunciation-quality claim (e.g., "pronunciaste bien/mal", "tu acento...") in a session with no active voice/audio modality.

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
- **Summary**: The agent switches to full Spanish too early during onboarding, confusing a beginner student.
- **Severity**: high
- **Situation**: The onboarding student is a complete beginner and responds in English or struggling Spanish to the background prompt, but the agent mistakenly switches to Spanish for the diagnostic probes instead of scaffolding in English.
- **Why**: Overly aggressive immersion defaults or language detection heuristics that mistake brief words or loanwords for advanced proficiency.
- **Solution**:
    - Enforce a rule that the agent must only switch to Spanish dialogue if the user provides a coherent, multi-word response written in Spanish (e.g., using conjugated verbs). If the user responds in English, single-word Spanish, or indicates difficulty, keep the dialog and instructions in English.
- **Symptoms**:
    - The user expresses confusion, uses English questions, or types basic words, but the agent continues to prompt them in complex Spanish.
- **Detection Pattern**: Prompting in Spanish immediately following a user response containing no Spanish verbs, or containing English phrases signaling confusion.
