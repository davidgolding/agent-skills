# Validations

This document defines the validations used by personal-editor.

---

## Word Count Validation

- **Id**: word-count-validation
- **Severity**: error
- **Type**: instruction
- **Pattern**: 
    - Passage length <= 2000 words.
- **Message**: The input passage exceeds the 2000-word limit. Please shorten the passage and try again.
- **Fix Action**: Truncate or split the text into chunks under 2000 words.
- **Applies To**:
    - *

---
