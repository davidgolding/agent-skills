# Sharp Edges

This document defines the sharp edges used by spanish-practice.

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

---
