# GMEU Copyeditor Validations

This document defines the validations used by gmeu-copyeditor.

## Output Format Compliance

- **Id**: output-format-compliance
- **Severity**: error
- **Type**: syntax
- **Pattern**: An item in the sequential commentary list that does not begin with bold reference text followed by a colon and the commentary.
- **Message**: Output must strictly follow the format: **referenced text**: commentary.
- **Fix Action**: Reformulate the suggestion to match the bold-colon format.
- **Applies To**:
    - copyediting commentary output
    - proofreading commentary output

---

## Source Citation Format Compliance

- **Id**: source-citation-format-compliance
- **Severity**: error
- **Type**: syntax
- **Pattern**: A usage commentary that does not end with `(GMEU, "entry")`, or a grammar commentary that does not end with `(CGG, "Topic," section)`.
- **Message**: Missing or malformed citation. All usage edits must be cited as `(GMEU, "entry")` and all grammar edits as `(CGG, "Topic," section)`.
- **Fix Action**: Identify the missing citation or correct the format to match the GMEU or CGG citation template, appending it to the end of the commentary paragraph.
- **Applies To**:
    - copyediting commentary output

---

## Copyediting Level Established

- **Id**: copyediting-level-established
- **Severity**: error
- **Type**: semantic
- **Pattern**: An editing pass proceeding with no Light, Medium, or Heavy level stated in the prompt or chosen by the user.
- **Message**: The copyediting level governs which suggestions are in scope; establish it before the pass begins.
- **Fix Action**: Ask the user to choose Light, Medium, or Heavy through the platform's blocking question tool, then run the pass against that level's rubric in `references/patterns.md`.
- **Applies To**:
    - copyediting pass

---

## Voice Statement Precedes Suggestions

- **Id**: voice-statement-precedes-suggestions
- **Severity**: error
- **Type**: semantic
- **Pattern**: Copyediting suggestions emitted before the author's identified voice has been stated to the user.
- **Message**: The identified voice is the baseline every suggestion is checked against, so it comes first.
- **Fix Action**: State the identified voice as the pass's first output, then re-check each suggestion against that description before emitting the commentary list.
- **Applies To**:
    - copyediting commentary output

---

## Level Rubric Scope Respected

- **Id**: level-rubric-scope-respected
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A suggestion exceeding the selected level's rubric — for example, a rewrite offered under Light, or replacement prose supplied for a wordy patch under Medium.
- **Message**: This suggestion goes beyond what the selected copyediting level authorizes.
- **Fix Action**: Reduce the suggestion to what the selected level's rubric permits — a pointer at Light, a suggested revision at Medium — or ask the user whether they want to move the pass to Heavy.
- **Applies To**:
    - copyediting commentary output

---

## Proofreading Pass Scope

- **Id**: proofreading-pass-scope
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A proofreading pass returning usage, grammar, wordiness, or organizational commentary rather than typographical errors and misspellings alone.
- **Message**: A proofreading pass is confined to typographical errors and misspellings.
- **Fix Action**: Remove the out-of-scope commentary, or offer the user a copyediting pass at a stated level as a separate piece of work.
- **Applies To**:
    - proofreading commentary output

---
