# Validations

This document defines the validations used by spanish-practice.

---

## TOON Syntax Check

- **Id**: toon-syntax-check
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?!.*interests\b)(?!.*srsDeck\b).*$
- **Message**: The student profile file has missing required fields or violates TOON format rules.
- **Fix Action**: Ensure the file strictly follows the TOON format syntax, declaring flat keys, Interests, learningGoals, persistentErrors arrays, and tabular decks for SRS and Curriculum.
- **Applies To**:
    - student-profile.toon

---
