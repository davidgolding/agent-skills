# Spanish Practice Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by spanish-practice.

## Patterns

- **Name**: Phrasal Vocabulary Acquisition
- **Description**: Grounding all vocabulary teaching, testing, and feedback in multi-word idiomatic chunks and complete clauses rather than single isolated words.
- **When**: Presenting new vocabulary, correcting user errors, or running SRS flashcards.
- **Example**:
```text
Agent: [Phrasal Drill] En lugar de aprender "asumir" solo, practicamos la locución C2 "dar por sentado":
Ejemplo: "No des por sentado que todo saldrá bien sin planificarlo."
Completa la frase: "Si no confirmas la reservación, ellos van a [dar por sentado / la llegada]..."
```

---

- **Name**: Oxford 31-Transformation Verb Routine
- **Description**: Systematic verb drills targeting the 31 Oxford transformation groups (AR 1–6, ER 7–18, IR 19–31) across 12 tense/mood/aspect stages, featuring reflexive/indirect constructions in full phrasal prompts.
- **When**: User requests on-demand verb practice or during targeted SRS verb warm-ups.
- **Example**:
```text
Agent: [Oxford Verb Routine - Grupo AR-4 (avergonzar) - Pretérito Indefinido]
Consigna: Completa la cláusula impersonal/reflexiva:
Prompt: "Ayer a Juan [avergonzar - pretérito] tener que admitir su error frente al equipo."
User: Ayer a Juan le avergonzó tener que admitir su error frente al equipo.
Agent: ¡Excelente! Observa cómo la transformación o > ue del presente no se produce en el pretérito ("avergonzó"), manteniendo la acentuación temática.
```

---

- **Name**: TOON State Management
- **Description**: Persistent tracking of user quarter-level CEFR proficiency, aggregate mastery, selected dialect, correction preference, interests/goals, recurring errors, active/passive vocabulary (with register and encounter counts), verb transformation group progress, and SM-2 parameters in a single compact `student-profile.toon` file.
- **When**: Initializing the session and saving the state after each session.
- **Example**:
```text
onboardingComplete: true
targetLanguage: "Spanish"
dialectPreference: "Mexican"
nativeLanguage: "English"
cefrLevel: "C1.25"
masteryPercent: 62
correctionPreference: "recasting"
interests: ["cooking", "history", "soccer"]
learningGoals: ["speak with in-laws", "watch news without subtitles"]
persistentErrors: ["si + condicional (should be si + imperfect subjunctive)", "gender agreement with compound nouns"]
lessonsCompleted: 24
lastLessonTopic: "Subjuntivo e Impersonales"
lastLessonDate: "2026-07-26T15:00:00Z"
verbGroupStage: "AR-4"
verbTenseStage: "Present Subjunctive"

srsDeck[2]{item,translation,register,easiness,interval,repetitions,encounterCount,nextReviewDate}:
dar por sentado,to take for granted,neutral,2.5,3,2,4,2026-07-29
atiborrarse de,to stuff oneself with,informal,2.6,6,3,7,2026-08-01

verbMasteryDeck[2]{group,modelVerb,tense,easiness,interval,repetitions,nextReviewDate}:
AR-4,avergonzar,Pretérito,2.5,1,1,2026-07-27
IR-10,salir,Presente Subjuntivo,2.5,6,2,2026-08-02
```

---

- **Name**: Progressive OPI Diagnostic
- **Description**: Conversational diagnostic assessment modeled after the ACTFL Oral Proficiency Interview (OPI). It begins in English to gather background, then dynamically transitions the conversation to Spanish for advanced speakers or scaffolds the quiz in English with targeted prompts for beginners, to find their active ceiling.
- **When**: Running the first practice session if `onboardingComplete` in the profile is set to `false`.
- **Example**:
```text
Agent (OPI Step 1 - English Greet): Welcome to Spanish Practice! Let's start by getting to know your background. How long have you been studying Spanish, and what are your main goals?
User: Yo estudié un poco en la escuela y ahora quiero hablar con mis abuelos.
Agent (OPI Step 2 - Dynamic Transition): ¡Excelente! Qué gran motivación hablar con tus abuelos. Cuéntame, ¿qué sueles hacer cuando los visitas? (Transitions to Spanish dialogue to probe vocabulary and past tenses)
```

---

- **Name**: Paused Halting Correction
- **Description**: Pausing the active lesson timer and conversational progression as soon as a language error is detected, forcing the student into a halting Correction Mode drill that persists until resolved.
- **When**: A grammatical mistake, spelling error, or English calque is identified in user production during standard practice.
- **Example**:
```text
User: Si yo tendría más tiempo, yo leería más libros.
Agent: [Correction Mode - Timer Paused] ¡Cuidado! En las oraciones condicionales hipotéticas, no se usa el condicional en la cláusula del "si". Debes usar el subjuntivo imperfecto ("Si yo tuviera/tuviese..."). Para asimilar esto:
1. Escribe la frase corregida.
2. Escribe dos nuevas oraciones originales siguiendo la estructura "Si yo tuviera [X], [Y-condicional]".
```

---

- **Name**: Preference-Branched Recasting
- **Description**: Correcting minor or first-occurrence errors with an inline implicit recast — restating the sentence correctly in the very next turn — without pausing the timer or conversation, when `correctionPreference` is `"recasting"`. Halting Correction Mode is reserved for errors already logged in `persistentErrors` or for `correctionPreference: "explicit"`.
- **When**: An error occurs during core production or receptive-input debrief and the profile's `correctionPreference` is `"recasting"` and the error is not yet in `persistentErrors`.
- **Example**:
```text
User: Ayer yo iba al cine con mis amigos.
Agent: ¡Qué buen plan! Ayer fui al cine con mis amigos también — a mí me tocó ver una película de terror. ¿Qué vieron ustedes?
(Note: the recast — "fui" instead of "iba" — is modeled inline; the timer keeps running and the conversation is not interrupted.)
```

---

- **Name**: Receptive Micro-Input Step
- **Description**: A short leveled text or dialogue (at or one notch above the learner's quarter-level) that naturally recycles the session's target phrasal items, followed by 1–2 comprehension or inference questions, delivered during the 3-minute receptive slot between SRS warm-up and core production.
- **When**: Every daily session, immediately after SRS warm-up.
- **Example**:
```text
Agent: [Entrada Receptiva] Lee este breve fragmento:
"Marta siempre da por sentado que su hermano la va a ayudar con la mudanza, pero esta vez él se atiborró de trabajo y no pudo llegar a tiempo..."
Pregunta 1: ¿Por qué se sintió sorprendida Marta?
Pregunta 2: ¿Qué habría hecho ella de otra manera?
```

---

- **Name**: Register-Shifting Drill
- **Description**: Drilling the same communicative intent across two registers (e.g. formal vs. informal) for a single phrasal item, for learners at B2 and above.
- **When**: Introducing or reviewing a register-tagged phrasal item for a learner whose `cefrLevel` is B2.00 or higher.
- **Example**:
```text
Agent: [Cambio de Registro - B2] La expresión "tomar cartas en el asunto" es neutral. Practiquemos el mismo mensaje en dos registros:
1. Formal (a tu jefe): "Entiendo la gravedad de la situación; voy a tomar cartas en el asunto de inmediato."
2. Informal (a un amigo): "Tranquilo, ya me pongo las pilas y arreglo esto ahora mismo."
Ahora tú: exprésale a un cliente formalmente que resolverás un problema, y luego exprésaselo informalmente a tu compañero de piso.
```

---

- **Name**: Functional-Need-Triggered Verb Micro-Drill
- **Description**: A short (2–3 item) embedded Oxford verb-group drill surfaced immediately when a conversational stumble reveals a gap in that group, rather than requiring the student to separately invoke the full on-demand Oxford Verb Routine.
- **When**: A core-production or Correction Mode turn reveals an error tied to a specific Oxford transformation group.
- **Example**:
```text
User: Si yo fuera tú, yo *saldría* con ella pero primero le *habla*...
Agent: [Micro-Drill Funcional - Grupo IR-10] Veo que "hablar" necesita el condicional aquí. Practiquemos rápido:
"Si yo *fuera* tú, primero le [hablar - condicional] antes de invitarla a salir."
(Two more quick items, then back to the conversation — no need to run the full on-demand routine.)
```

---

## Anti-Patterns

- **Name**: Single-Word Flashcards & Isolated Verb Drills
- **Description**: Testing vocabulary or verb conjugations in isolation (e.g. "What does *avergonzar* mean?" or "Conjugate *salir* in present subjunctive").
- **Why**: Single-word testing reinforces translation lag and fails to build natural phrasal fluency or native-like instinct for reflexive/indirect verb structures.
- **Instead**: Always embed target vocabulary and verbs inside complete idiomatic expressions or clause frames (e.g. *"A Juan le [avergonzar - pretérito] admitir..."*).

---

- **Name**: Sterile Grammar Drills
- **Description**: Presenting isolated fill-in-the-blank or multiple-choice questions instead of conversational, context-rich active production.
- **Why**: Fill-in-the-blank questions do not build spontaneous language pathways or reduce translation lag, keeping the user stuck at the B2 plateau.
- **Instead**: Prompt the student to draft paragraphs or debate ethical/economic/philosophical issues in their target dialect, weaving in SRS items naturally.

---

- **Name**: Linear Conversation Progression
- **Description**: Continuing the main chat conversation and logic flow while merely printing corrections inline as secondary feedback.
- **Why**: It allows the student to ignore the feedback and continue writing incorrect structures, failing to reinforce correct pathways or break persistent errors.
- **Instead**: Immediately halt the conversational flow, freeze the session timer, and refuse to proceed until the student actively re-types and constructs sentences demonstrating successful correction.

---

- **Name**: Ignoring Correction Preference
- **Description**: Applying Halting Correction Mode uniformly to every detected error regardless of the profile's `correctionPreference` field.
- **Why**: Implicit recasts carry better long-term retention and a lower affective filter for spontaneous oral production than explicit halting corrections, which are better reserved for repeat/persistent errors or written accuracy work. Ignoring the stored preference means the session never actually reflects what the learner has told the system works for them.
- **Instead**: Check `correctionPreference` and `persistentErrors` before escalating; use an inline recast for minor first-occurrence errors under `"recasting"`, and reserve Halting Correction Mode for repeat offenses or an explicit preference.

---

- **Name**: Production-Only Session Collapse
- **Description**: Running the daily session as SRS warm-up → core production → correction → sync, silently dropping the Receptive Micro-Input segment.
- **Why**: Meaning-focused receptive input (reading/listening) is the primary evidence-backed driver of incidental vocabulary growth and the only mechanism that accumulates the contextual encounters needed for durable recall; a production-only session starves that channel entirely.
- **Instead**: Always include the 3-minute Receptive Micro-Input segment between SRS warm-up and core production, recycling that session's target phrasal items in a short leveled text with comprehension questions.
