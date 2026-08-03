# German Practice Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by german-practice.

## Patterns

- **Name**: Phrasal Vocabulary Acquisition
- **Description**: Grounding all vocabulary teaching, testing, and feedback in multi-word idiomatic chunks and complete clauses rather than single isolated words, tagged with both register and grammatical gender.
- **When**: Presenting new vocabulary, correcting user errors, or running SRS flashcards.
- **Example**:
```text
Agent: [Phrasal-Drill] Anstatt "vergessen" isoliert zu lernen, üben wir die Wendung "etwas in den Wind schlagen":
Beispiel: "Er hat ihren Rat einfach in den Wind geschlagen."
Vervollständige den Satz: "Wenn du diese Warnung [in den Wind schlagen], wirst du es bereuen."
(Gender-Hinweis: die Warnung — feminin)
```

---

- **Name**: Duden Weak/Strong/Mixed/Modal Verb Routine
- **Description**: Systematic verb drills targeting Duden's four model-verb classes (weak, strong, mixed, modal) across the 12 tense/mood/aspect stages, featuring separable/inseparable prefix handling and full phrasal prompts.
- **When**: User requests on-demand verb practice or during targeted SRS verb warm-ups.
- **Example**:
```text
Agent: [Duden-Verbroutine - Starkes Verb, Gruppe "ei→ie→ie" (schreiben) - Perfekt]
Aufgabe: Vervollständige den Satz mit dem Partizip II:
Prompt: "Sie hat mir gestern einen langen Brief [schreiben - Partizip II]."
User: Sie hat mir gestern einen langen Brief geschrieben.
Agent: Genau! Beachte, dass "schreiben" zur Ablautreihe ei-ie-ie gehört, genau wie "bleiben → blieb → geblieben".
```

---

- **Name**: Case Declension Routine
- **Description**: Systematic declension drills covering Nominativ/Akkusativ/Dativ/Genitiv across der/die/das/plural and strong/weak adjective endings, always embedded in a full clause with a case-governing verb or preposition.
- **When**: User requests on-demand case practice, or during targeted SRS case warm-ups.
- **Example**:
```text
Agent: [Kasusroutine - Dativ, maskulin] Vervollständige den Satz:
Prompt: "Ich fahre mit [der Zug - Dativ] nach Berlin."
User: Ich fahre mit dem Zug nach Berlin.
Agent: Richtig! "mit" verlangt immer den Dativ, und aus "der Zug" wird im Dativ "dem Zug".
```

---

- **Name**: Frequency-Tiered Sequencing
- **Description**: Introducing and drilling verb forms, case forms, and vocabulary headwords in order of real-world frequency rather than canonical grammar-textbook order, while overriding classification order for high-utility irregular auxiliaries.
- **When**: Selecting the next item to introduce in the on-demand routines, in SRS warm-up, or in receptive-input vocabulary selection.
- **Example**:
```text
Tier 1 (introduce first): Präsens (all persons) + sein/haben/werden immediately as auxiliaries, Perfekt, modal-verb present tense, Imperativ, Konjunktiv II of sein/haben/modals ("Ich hätte gern...", "Könnten Sie...").
Tier 2: Präteritum (esp. sein/haben/modals), Futur I, present Passiv, Plusquamperfekt.
Tier 3: Konjunktiv I, morphological Konjunktiv II of ordinary verbs, Futur II, non-present Passiv.
Cases: Nominativ/Akkusativ before Dativ before Genitiv.

Agent (mid-session): masteryPercent for Tier 1 Perfekt is at 40%, Tier 2 items are untouched → introduces one more Perfekt drill before touching Präteritum, even though the curriculum stage list places Präteritum earlier.
```

---

- **Name**: TOON State Management
- **Description**: Persistent tracking of user quarter-level CEFR proficiency, aggregate mastery, selected regional standard, correction preference, interests/goals, recurring errors, active/passive vocabulary (with register, gender, and frequency tier), verb and case mastery progress, and SM-2 parameters in a single compact `student-profile.toon` file.
- **When**: Initializing the session and saving the state after each session.
- **Example**:
```text
onboardingComplete: true
targetLanguage: "German"
regionPreference: "Austria"
nativeLanguage: "English"
cefrLevel: "B1.50"
masteryPercent: 58
correctionPreference: "recasting"
interests: ["hiking", "history", "football"]
learningGoals: ["speak with in-laws", "follow the news without subtitles"]
persistentErrors: ["accusative/dative confusion after two-way prepositions", "separable prefix left unstranded (aufstehen)"]
lessonsCompleted: 19
lastLessonTopic: "Perfekt und trennbare Verben"
lastLessonDate: "2026-07-30T15:00:00Z"
verbGroupStage: "Strong-ei-ie-ie"
verbTenseStage: "Perfekt"
caseStage: "Dativ"

srsDeck[2]{item,translation,gender,register,frequencyTier,easiness,interval,repetitions,encounterCount,nextReviewDate}:
jemandem auf die Nerven gehen,to get on someone's nerves,-,informal,1,2.5,3,2,4,2026-08-02
sich Zeit nehmen für,to take time for,-,neutral,1,2.6,6,3,7,2026-08-05

verbMasteryDeck[2]{group,modelVerb,tense,frequencyTier,easiness,interval,repetitions,nextReviewDate}:
Strong-ei-ie-ie,schreiben,Perfekt,1,2.5,1,1,2026-07-31
Modal,können,Präsens,1,2.5,6,2,2026-08-06

caseMasteryDeck[2]{case,gender,number,frequencyTier,easiness,interval,repetitions,nextReviewDate}:
Dativ,maskulin,singular,2,2.4,2,1,2026-08-01
Akkusativ,feminin,singular,1,2.6,5,2,2026-08-04
```

---

- **Name**: Progressive OPI Diagnostic
- **Description**: Conversational diagnostic assessment modeled after the ACTFL Oral Proficiency Interview (OPI). It begins in English to gather background, then dynamically transitions the conversation to German for advanced speakers or scaffolds the quiz in English with targeted prompts for beginners, to find their active ceiling.
- **When**: Running the first practice session if `onboardingComplete` in the profile is set to `false`.
- **Example**:
```text
Agent (OPI Step 1 - English Greet): Welcome to German Practice! Let's start by getting to know your background. How long have you been studying German, and what are your main goals?
User: Ich habe ein bisschen in der Schule gelernt und möchte jetzt mit meinen Großeltern sprechen.
Agent (OPI Step 2 - Dynamic Transition): Toll, was für eine schöne Motivation! Erzähl mir, was machst du normalerweise, wenn du sie besuchst? (Transitions to German dialogue to probe vocabulary and past tenses)
```

---

- **Name**: Paused Halting Correction
- **Description**: Pausing the active lesson timer and conversational progression as soon as a language error is detected, forcing the student into a halting Correction Mode drill that persists until resolved.
- **When**: A grammatical mistake, case error, prefix-stranding error, or English calque is identified in user production during standard practice.
- **Example**:
```text
User: Ich aufstehe jeden Tag um sieben Uhr.
Agent: [Correction Mode - Timer Paused] Achtung! "aufstehen" ist trennbar — im Hauptsatz wandert die Vorsilbe ans Satzende. Um das zu verinnerlichen:
1. Schreibe den korrigierten Satz.
2. Schreibe zwei neue eigene Sätze mit anderen trennbaren Verben nach demselben Muster.
```

---

- **Name**: Preference-Branched Recasting
- **Description**: Correcting minor or first-occurrence errors with an inline implicit recast — restating the sentence correctly in the very next turn — without pausing the timer or conversation, when `correctionPreference` is `"recasting"`. Halting Correction Mode is reserved for errors already logged in `persistentErrors` or for `correctionPreference: "explicit"`.
- **When**: An error occurs during core production or receptive-input debrief and the profile's `correctionPreference` is `"recasting"` and the error is not yet in `persistentErrors`.
- **Example**:
```text
User: Gestern ich ging ins Kino mit meine Freunde.
Agent: Klingt nach einem schönen Abend! Gestern bin ich auch ins Kino gegangen — mit meinen Freunden haben wir einen Horrorfilm gesehen. Was habt ihr euch angeschaut?
(Note: the recast — correct word order and the dative "meinen Freunden" after "mit" — is modeled inline; the timer keeps running and the conversation is not interrupted.)
```

---

- **Name**: Receptive Micro-Input Step
- **Description**: A short leveled text or dialogue (at or one notch above the learner's quarter-level) that naturally recycles the session's target phrasal items, followed by 1–2 comprehension or inference questions, delivered during the 3-minute receptive slot between SRS warm-up and core production.
- **When**: Every daily session, immediately after SRS warm-up.
- **Example**:
```text
Agent: [Rezeptiver Input] Lies diesen kurzen Abschnitt:
"Martha nimmt sich immer viel Zeit für ihren Bruder, aber dieses Mal ging ihm die ganze Umzugsplanung so auf die Nerven, dass er gar nicht mehr anrief..."
Frage 1: Warum war Martha überrascht?
Frage 2: Was hätte sie anders gemacht?
```

---

- **Name**: Register-Shifting Drill
- **Description**: Drilling the same communicative intent across two registers — critically including the Sie/du choice — for a single phrasal item, for learners at B2 and above.
- **When**: Introducing or reviewing a register-tagged phrasal item for a learner whose `cefrLevel` is B2.00 or higher.
- **Example**:
```text
Agent: [Registerwechsel - B2] Der Ausdruck "sich um etwas kümmern" ist neutral. Üben wir dieselbe Botschaft in zwei Registern:
1. Formell (zu Ihrem Chef): "Ich verstehe die Dringlichkeit; ich werde mich umgehend darum kümmern."
2. Informell (zu einem Freund): "Keine Sorge, ich kümmere mich gleich darum."
Jetzt du: sag einem Kunden formell, dass du ein Problem lösen wirst, und dann informell deinem Mitbewohner.
```

---

- **Name**: Functional-Need-Triggered Verb/Case Micro-Drill
- **Description**: A short (2–3 item) embedded verb-group or case micro-drill surfaced immediately when a conversational stumble reveals a gap, rather than requiring the student to separately invoke the full on-demand routines.
- **When**: A core-production or Correction Mode turn reveals an error tied to a specific verb group or case/gender combination.
- **Example**:
```text
User: Ich gebe das Buch die Frau, weil ich es fertig gelesen habe.
Agent: [Funktionaler Mikro-Drill - Dativ] Ich sehe, dass "geben" ein Dativobjekt braucht. Üben wir kurz:
"Ich gebe [die Frau - Dativ] das Buch."
(Two more quick items, then back to the conversation — no need to run the full on-demand routine.)
```

---

- **Name**: Separable-Verb Clause Discipline
- **Description**: Explicitly checking that separable-prefix verbs split correctly in main clauses (prefix at clause-end) and rejoin correctly in subordinate clauses (verb-final), treating prefix-stranding as its own correction category.
- **When**: Any student production containing a separable or inseparable prefix verb, during core production or correction.
- **Example**:
```text
User: Weil ich aufstehe früh, bin ich müde.
Agent: [Wortstellung] In Nebensätzen steht das (wieder vereinte) Verb ganz am Ende: "Weil ich früh aufstehe, bin ich müde." Schreib den Satz noch einmal korrekt, und bilde einen weiteren Nebensatz mit "anrufen" oder "einkaufen".
```

---

## Anti-Patterns

- **Name**: Single-Word Flashcards & Isolated Verb/Case Drills
- **Description**: Testing vocabulary, verb conjugations, or case endings in isolation (e.g. "What does *vergessen* mean?" or "Decline *der Mann* in the dative.").
- **Why**: Single-word and bare-paradigm testing reinforces translation lag and fails to build natural phrasal fluency or native-like instinct for case-governed structures.
- **Instead**: Always embed target vocabulary, verbs, and case forms inside complete idiomatic expressions or clause frames (e.g. *"Sie hat mir einen Brief [schreiben - Partizip II]..."*, *"Ich fahre mit [der Zug - Dativ]..."*).

---

- **Name**: Sterile Grammar Drills
- **Description**: Presenting isolated fill-in-the-blank or multiple-choice questions instead of conversational, context-rich active production.
- **Why**: Fill-in-the-blank questions do not build spontaneous language pathways or reduce translation lag, keeping the user stuck at the B2 plateau.
- **Instead**: Prompt the student to draft paragraphs or debate ethical/economic/philosophical issues in the target register, weaving in SRS items naturally.

---

- **Name**: Linear Conversation Progression
- **Description**: Continuing the main chat conversation and logic flow while merely printing corrections inline as secondary feedback.
- **Why**: It allows the student to ignore the feedback and continue writing incorrect structures, failing to reinforce correct pathways or break persistent errors.
- **Instead**: Immediately halt the conversational flow, freeze the session timer, and refuse to proceed until the student actively re-types and constructs sentences demonstrating successful correction.

---

- **Name**: Ignoring Correction Preference
- **Description**: Applying Halting Correction Mode uniformly to every detected error regardless of the profile's `correctionPreference` field.
- **Why**: Implicit recasts carry better long-term retention and a lower affective filter for spontaneous oral production than explicit halting corrections, which are better reserved for repeat/persistent errors or written accuracy work.
- **Instead**: Check `correctionPreference` and `persistentErrors` before escalating; use an inline recast for minor first-occurrence errors under `"recasting"`, and reserve Halting Correction Mode for repeat offenses or an explicit preference.

---

- **Name**: Production-Only Session Collapse
- **Description**: Running the daily session as SRS warm-up → core production → correction → sync, silently dropping the Receptive Micro-Input segment.
- **Why**: Meaning-focused receptive input (reading/listening) is the primary evidence-backed driver of incidental vocabulary growth and the only mechanism that accumulates the contextual encounters needed for durable recall.
- **Instead**: Always include the 3-minute Receptive Micro-Input segment between SRS warm-up and core production, recycling that session's target phrasal items in a short leveled text with comprehension questions.

---

- **Name**: Frequency-Blind Sequencing
- **Description**: Introducing forms in canonical grammar-reference order (e.g. teaching Genitiv or Konjunktiv I early because it appears "next" in a textbook's chapter list) rather than by real-world frequency.
- **Why**: Canonical grammar references are organized for completeness, not for functional speed; a learner who masters Genitiv before mastering Dativ, or Konjunktiv I before Perfekt, will be slower to hold a basic conversation than one sequenced by frequency.
- **Instead**: Sequence introductions by frequency tier (Tier 1 → Tier 2 → Tier 3 for both verb forms and cases), overriding classification order for high-utility irregular auxiliaries like *sein/haben/werden*.

---

- **Name**: Prefix-Stranding Blindness
- **Description**: Failing to flag separable-verb prefix placement errors (e.g. accepting "Ich aufstehe früh" as correct) because the sentence superficially resembles valid English SVO structure.
- **Why**: The model's general-purpose training data is dominated by English word order, biasing it toward under-flagging German-specific structural errors that don't have an English analogue.
- **Instead**: Treat every separable/inseparable verb in student production as requiring an explicit clause-position check, independent of whether the sentence "reads fine" by English-order instincts.
