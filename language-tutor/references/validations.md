# Language Tutor Validations

## TOON Schema and Formatting Constraints

Every write to `working-memory.toon` must strictly conform to this schema and syntax:

```text
onboardingComplete: [true|false]
targetLanguage: "[language name]"
dialectPreference: "[dialect name or none]"
nativeLanguage: "[language name]"
cefrLevel: "[pre-A1|A1|A2|B1|B2|C1|C2]"
correctionPreference: "[recasting|explicit]"
lessonsCompleted: [integer]
lastLessonTopic: "[topic name or none]"
lastLessonDate: "[YYYY-MM-DDTHH:MM:SSZ or none]"
currentThemeArc: "[theme name or none]"

interests[count]: [comma-separated list of interests]
learningGoals[count]: [comma-separated list of goals]
persistentErrors[count]: [comma-separated list of errors, max 10]

srsDeck[count]{item,translation,easiness,interval,repetitions,nextReviewDate}:
[item],[translation],[easiness],[interval],[repetitions],[nextReviewDate]
...
```

### TOON Syntax Constraints
- No quotes or braces around keys.
- Flat fields must be on separate lines.
- Arrays (like `interests`, `learningGoals`, `persistentErrors`) must match the format `key[count]: val1, val2` (e.g. `interests[3]: travel, cooking, music`).
- Tabular array `srsDeck` must declare headers in curly braces and rows on subsequent lines with exactly 6 comma-separated fields. Dates must be in `YYYY-MM-DD` or ISO format.

---

## SM-2 Quality Rating Scale

When evaluating the learner's production of a target vocabulary item in conversation, assign a quality score ($q$) from 0 to 5:

- **0 (Blackout)**: Complete failure. The learner did not recognize or produce the item at all.
- **1 (Wrong but recognized)**: Learner produced it incorrectly but recognized it when you recasted/corrected it.
- **2 (Wrong but familiar)**: Learner got it wrong but was in the correct semantic area or showed strong familiarity.
- **3 (Correct with difficulty)**: Learner produced it correctly but with significant hesitation, self-correction, or effort.
- **4 (Correct with minor hesitation)**: Learner produced it correctly with only slight delay or minor uncertainty.
- **5 (Instant recall)**: Learner produced it correctly, fluently, and without any hesitation.

---

## SM-2 Spaced Repetition Algorithm

For every reviewed word, calculate the updated spaced repetition parameters using these rules:

1. **Calculate New Easiness Factor (EF')**:
   $$EF' = EF + (0.1 - (5 - q) \times (0.08 + (5 - q) \times 0.02))$$
   *Constraint*: If $EF' < 1.3$, clamp it to $EF' = 1.3$.

2. **Calculate New Repetitions (Rep') and Interval (Int')**:
   - If quality score **$q < 3$**:
     - Reset repetitions: $Rep' = 1$
     - Reset interval: $Int' = 1$ (1 day)
   - If quality score **$q \ge 3$**:
     - If repetitions **$Rep = 1$**:
       - $Int' = 1$ (1 day)
     - If repetitions **$Rep = 2$**:
       - $Int' = 6$ (6 days)
     - If repetitions **$Rep > 2$**:
       - $Int' = \text{round}(Int \times EF')$ (days)
     - Increment repetitions: $Rep' = Rep + 1$

3. **Calculate New Next Review Date**:
   $$\text{nextReviewDate} = \text{currentDate} + Int' \text{ days}$$
