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

## Anti-Patterns

- **Name**: Sterile Grammar Drills
- **Description**: Presenting isolated fill-in-the-blank or multiple-choice questions instead of conversational, context-rich active production.
- **Why**: Fill-in-the-blank questions do not build spontaneous language pathways or reduce translation lag, keeping the user stuck at the B2 plateau.
- **Instead**: Prompt the student to draft paragraphs or debate ethical/economic/philosophical issues in their target dialect, weaving in SRS items naturally.

---
