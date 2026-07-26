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
- **Description**: Persistent tracking of user CEFR levels, selected dialect, active/passive vocabulary, verb transformation group progress, and SM-2 parameters in a single compact `student-profile.toon` file.
- **When**: Initializing the session and saving the state after each session.
- **Example**:
```text
onboardingComplete: true
targetLanguage: "Spanish"
dialectPreference: "Mexican"
nativeLanguage: "English"
cefrLevel: "C1"
correctionPreference: "recasting"
lessonsCompleted: 24
lastLessonTopic: "Subjuntivo e Impersonales"
lastLessonDate: "2026-07-26T15:00:00Z"
verbGroupStage: "AR-4"
verbTenseStage: "Present Subjunctive"

srsDeck[2]{item,translation,easiness,interval,repetitions,nextReviewDate}:
dar por sentado,to take for granted,2.5,3,2,2026-07-29
atiborrarse de,to stuff oneself with,2.6,6,3,2026-08-01

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
