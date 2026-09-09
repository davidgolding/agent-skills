# Prose Fingerprinter Validations

This document defines the validations used by prose-fingerprinter.

## Minimum Passage Length

- **Id**: min-passage-length
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Input text containing fewer than 150 words.
- **Message**: The input passage is too short to construct a reliable, statistically significant prose fingerprint.
- **Fix Action**: Ask the user to provide a larger text sample — ideally 300 to 1,000 words — for a more accurate stylistic profile.
- **Applies To**:
    - input passage

---

## Metric Paired With Function

- **Id**: metric-paired-with-function
- **Severity**: error
- **Type**: semantic
- **Pattern**: A quantitative finding reported without the stylistic function it performs.
- **Message**: Every metric needs the effect it produces; a number alone leaves the fingerprint abstract.
- **Fix Action**: Append the qualitative explanation of how that mechanic manipulates the reader's attention, per the Flat Metric Reporting anti-pattern in `references/patterns.md`.
- **Applies To**:
    - fingerprint report
    - comparison table

---

## Measurement Basis Disclosed

- **Id**: measurement-basis-disclosed
- **Severity**: error
- **Type**: semantic
- **Pattern**: A figure reported without stating whether it was counted exhaustively across the passage or estimated from a sample.
- **Message**: Each figure states its basis, so the reader can tell which parts of the fingerprint would survive a recount.
- **Fix Action**: Mark the figure as counted or estimated, naming the sample's size and location where the figure rests on one.
- **Applies To**:
    - fingerprint report
    - comparison table

---

## All Five Dimensions Reported

- **Id**: all-five-dimensions-reported
- **Severity**: warning
- **Type**: schema
- **Pattern**: A fingerprint omitting one of the five dimensions — syntactic architecture, prosodic scansion, etymological register, presentation-mode mix, thematic clustering — with no statement of why the passage does not support it.
- **Message**: A fingerprint covers all five dimensions, or says which one the passage cannot support and why.
- **Fix Action**: Add the missing dimension, or state explicitly that the passage provides too little evidence for it and report the gap rather than estimating past it.
- **Applies To**:
    - fingerprint report

---
