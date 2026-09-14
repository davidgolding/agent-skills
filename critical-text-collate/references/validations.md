# Critical Text Collation Validations

This document defines the validations used by critical-text-collate.

## No Spaces in Collation Cells

- **Id**: collate-no-spaces-in-cells
- **Severity**: error
- **Type**: semantic
- **Pattern**: A written collation cell value containing a space character (U+0020) between entities rather than the bullet character `•` (U+2022).
- **Message**: Collation cell contains a raw space character; spaces within cells must be replaced by the bullet character '•' to represent multiple-entity nodes.
- **Fix Action**: Replace raw spaces with the bullet character (U+2022) in the cell string formatting, per the Space Replacement with Bullets pattern.
- **Applies To**:
    - output workbook cells
    - cell-writing code paths

---

## Segment Column Missing

- **Id**: collate-segment-column-missing
- **Severity**: error
- **Type**: schema
- **Pattern**: An output workbook whose cell A1 holds a value other than `segment`, or whose Column A carries something other than the sentence-group index.
- **Message**: Excel sheet is missing the required 'segment' column in Column A.
- **Fix Action**: Write `segment` into the first cell (A1) and reserve Column A for the sentence group index as an integer.
- **Applies To**:
    - output workbook header row
    - output workbook Column A

---

## Strikethrough Formatting Mappings

- **Id**: collate-invalid-strikethrough
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `<(?!del|strike|s\b)[^>]*\\.*?>`
- **Message**: Canceled text run within an interpolation lacks correct strikethrough formatting in the spreadsheet representation.
- **Fix Action**: Map all prior text before backslashes — as in `<prior\interpolated>` — to the strikethrough font property in Excel.
- **Applies To**:
    - output workbook cells
    - composite node rendering

---

## Blank Cell for Absent Node

- **Id**: collate-blank-cell-for-absent-node
- **Severity**: error
- **Type**: semantic
- **Pattern**: A cell carrying a placeholder — a hyphen, an ellipsis, `[om.]`, `null`, or a lone bullet — where its witness has no node for that alignment row.
- **Message**: A witness lacking a node for an alignment row leaves that cell completely blank, since a placeholder reads as a reading the witness does not carry.
- **Fix Action**: Write nothing to the cell, leaving it empty, per the Blank Gaps principle.
- **Applies To**:
    - output workbook cells

---

## Comments Scrubbed from Collation Text

- **Id**: collate-comments-scrubbed
- **Severity**: error
- **Type**: semantic
- **Pattern**: A collation cell or aligned node containing `//` comment text or a `/* ... */` block, or a footnote's text aligned as a witness reading rather than attached as an annotation.
- **Message**: Comments and footnotes are metadata; collation text carries neither as an aligned reading.
- **Fix Action**: Strip `//` and `/* ... */` comments during parsing with an escape-aware scanner, and route footnotes to their segment as separate annotations, per the Scrub Comments and Annotations pattern.
- **Applies To**:
    - parsed witness text
    - output workbook cells

---
