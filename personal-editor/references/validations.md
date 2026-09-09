# Validations

This document defines the validations used by personal-editor.

---

## Word Count Validation

- **Id**: word-count-validation
- **Severity**: error
- **Type**: semantic
- **Pattern**:
    - Passage length exceeding 2000 words.
- **Message**: The input passage exceeds the 2000-word limit. Please shorten the passage and try again.
- **Fix Action**: Truncate or split the text into chunks under the limit, then resubmit one chunk per invocation.
- **Applies To**:
    - *

---

## CriticMarkup Syntax Well-Formed

- **Id**: criticmarkup-syntax-well-formed
- **Severity**: warning
- **Type**: syntax
- **Pattern**:
    - A deletion, addition, or comment annotation with an unmatched or malformed delimiter — an opening `{--`, `{++`, or `{>>` with no matching `--}`, `++}`, or `<<}`.
- **Message**: This CriticMarkup annotation has an unbalanced delimiter, so the passage renders with literal markup showing.
- **Fix Action**: Close the annotation with its matching delimiter, keeping the annotated segment inside the braces.
- **Applies To**:
    - Copyediting & Proofreading Suggestions section of the report

---

## Report Carries All Four Sections

- **Id**: report-four-sections-present
- **Severity**: error
- **Type**: schema
- **Pattern**:
    - Delivered report missing any of the Copyediting & Proofreading Suggestions, Prose Fingerprint Analysis, Rhetorical Figure Analysis, or Panel Judge Adjudication Scorecard sections, or presenting them out of that order.
- **Message**: The report must carry all four pass sections, in order — a missing section means a pass was skipped rather than reported.
- **Fix Action**: Run the missing pass and add its section in position, per the Four-Section Synthesized Report pattern.
- **Applies To**:
    - final report output

---

## Adjudication Cites Its Evidence

- **Id**: adjudication-cites-evidence
- **Severity**: warning
- **Type**: semantic
- **Pattern**:
    - A caliber rating stated with no reference to a specific stylistic feature or passage segment supporting it.
- **Message**: A caliber rating needs the stylistic evidence that produced it, so the writer can check the judgment against the text.
- **Fix Action**: Name the specific stylistic features — cadence, syntax, diction, structural choices — and the segments exhibiting them that place the passage at that rating.
- **Applies To**:
    - Panel Judge Adjudication Scorecard section of the report

---
