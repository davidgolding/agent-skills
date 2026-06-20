# Validations

This document defines the validations used by prose-fingerprinter.

---

## Minimum Passage Length

- **Id**: min-passage-length
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Input text containing less than 150 words
- **Message**: The input passage is too short to construct a reliable, statistically significant prose fingerprint.
- **Fix Action**: Ask the user to provide a larger text sample (ideally 300 to 1,000 words) for a more accurate stylistic profile.
- **Applies To**:
    - *.txt
    - *.md

---
