# Validations

This document defines the validations used by gmeu-copyeditor.

---

## Output Format Compliance

- **Id**: output-format-compliance
- **Severity**: error
- **Type**: instruction
- **Pattern**: Ensure all items in the sequential list begin with bold reference text, followed by a colon and the commentary.
- **Message**: Output must strictly follow the format: **referenced text**: commentary.
- **Fix Action**: Reformulate the suggestion to match the bold-colon format.
- **Applies To**:
    - *

---

## Source Citation Format Compliance

- **Id**: source-citation-format-compliance
- **Severity**: error
- **Type**: instruction
- **Pattern**: Ensure all usage commentaries end with `(GMEU, "entry")` and all grammar commentaries end with `(CGG, "Topic," section)`.
- **Message**: Missing or malformed citation. All usage edits must be cited as `(GMEU, "entry")` and all grammar edits as `(CGG, "Topic," section)`.
- **Fix Action**: Identify the missing citation or correct the format to match the GMEU or CGG citation template, appending it to the end of the commentary paragraph.
- **Applies To**:
    - *

---

