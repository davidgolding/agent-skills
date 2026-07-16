# Spanish Practice Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by spanish-practice.

## Patterns

- **Name**: TOON State Management
- **Description**: Persistent tracking of user CEFR levels, selected dialect (Mexican, Colombian, etc.), active/passive vocabulary, idioms, conjugations, and SM-2 parameters in a single compact `student-profile.toon` file.
- **When**: Initializing the session and saving the state after each session.
- **Example**:
```text
onboardingComplete: true
targetLanguage: "Spanish"
dialectPreference: "Mexican"
nativeLanguage: "English"
cefrLevel: "B2"
correctionPreference: "recasting"
lessonsCompleted: 15
lastLessonTopic: "Hypothetical Subjunctive"
lastLessonDate: "2026-07-16T12:00:00Z"
currentThemeArc: "None"
curriculumStage: "Phase 2"

interests[3]: business, literature, hiking
learningGoals[2]: C2 mastery, natural conversation
persistentErrors[2]: calque_decisions, subjunctive_future

srsDeck[2]{item,translation,easiness,interval,repetitions,nextReviewDate}:
atiborrarse,to stuff oneself,2.5,3,2,2026-07-19
adoptar una medida,to take a decision,2.6,6,3,2026-07-22

curriculumDeck[2]{concept,type,rules,easiness,interval,repetitions,nextReviewDate}:
futuro de subjuntivo,grammar,rare verb tense for formal/legal scenarios,2.5,1,1,2026-07-17
voseo conjugations,grammar,conjugation rules for Argentine Spanish,2.5,6,2,2026-07-22
```

---

- **Name**: Progressive OPI Diagnostic
- **Description**: Conversational diagnostic assessment modeled after the ACTFL Oral Proficiency Interview (OPI), starting from warm-up exchanges and progressively escalating grammatical and lexical complexity to identify the student's active ceiling.
- **When**: Running the first practice session if `onboardingComplete` in the profile is set to `false`.
- **Example**:
```text
Agent (OPI Step 1 - Warm-up B1): ¡Hola! Hablemos un poco sobre tu rutina de estudio y trabajo. ¿Cómo es un día típico para ti?
User: Yo me levanto a las 8 y voy a trabajar en carro.
Agent (OPI Step 2 - Probe B2/C1): Excelente. Imagina que ayer tu auto se averió y tuviste que resolver el problema para llegar a tiempo a una reunión importante. Cuéntame con detalle qué pasó y cómo lo solucionaste.
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
