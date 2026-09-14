# Critical Text Collation Sharp Edges

This document defines the sharp edges used by critical-text-collate.

## Alignment Drift on Divergent Witnesses

- **Id**: alignment-drift-divergent-witnesses
- **Summary**: Witnesses with highly divergent phrasing or structural omissions drive standard sequence alignment to match unrelated words, producing skewed rows and excessive blank cells.
- **Severity**: critical
- **Situation**: Witness A carries a large insertion absent from Witness B, and a Levenshtein-based alignment tries to match the insertion's individual words against unrelated words in B.
- **Why**: Naive sequence alignment leans on local word matching without checking sentence-level context, so one unmatched span displaces every match that follows it.
- **Solution**:
    - Anchor matching segments with hierarchical sentence/line alignment before any word-level pass.
    - Set a minimum similarity threshold for matching nodes; below the threshold, record an addition/deletion and leave the cell blank.
    - Account for variation species — ORD for reorderings, LEX for synonyms — when calculating alignment penalties.
- **Symptoms**: Rows where semantically unrelated readings sit side by side; long diagonal runs of blank cells trailing a single insertion; a witness's readings drifting one row further out of register with each subsequent sentence.
- **Detection Pattern**: A collation row pairing nodes whose similarity falls below the configured match threshold, or a run of consecutive rows in which one witness's column is offset from its sentence group's `segment` value.

---

## Corrupt Excel Rich Text Files

- **Id**: corrupt-excel-rich-text
- **Summary**: Writing rich text (bold, italic, strikethrough) inside Excel cells through openpyxl or similar libraries easily generates malformed OpenXML, leaving the file unreadable in Microsoft Excel.
- **Severity**: high
- **Situation**: The agent builds cell-level formatting from raw XML tags or incorrect object types in openpyxl, and Excel reports the file as corrupted and unopenable.
- **Why**: Excel requires strictly nested XML structures for inline text formatting, and rejects the whole workbook rather than degrading a single malformed cell.
- **Solution**:
    - Always use `openpyxl.cell.rich_text.CellRichText` and `openpyxl.cell.rich_text.TextBlock` objects.
    - Apply Font properties strictly to `TextBlock` objects and append those to `CellRichText`.
    - Validate generated spreadsheet files programmatically with a test script that opens the workbook.
- **Symptoms**: Excel reports "corrupted and cannot be opened" or offers to repair the file; the workbook opens in openpyxl but fails in Excel; repaired files open with all formatting stripped.
- **Detection Pattern**: A generated `.xlsx` that fails to reopen cleanly through a library round-trip, or cell-writing code passing raw markup strings or bare `Font` objects where `CellRichText` and `TextBlock` are required.

---

## Accidental Comment Stripping

- **Id**: accidental-comment-stripping
- **Summary**: Regular expressions for stripping `//` and `/* ... */` comments also strip legitimate transcription text wherever comment delimiters appear inside quotes or escaped sequences.
- **Severity**: medium
- **Situation**: A witness transcript carries `Preach in their days\//...` with escaped characters, and the parser deletes everything after the double slashes.
- **Why**: Overly simplistic regex parsers ignore escape characters, so an escaped slash reads to them as the start of a comment.
- **Solution**:
    - Implement a state-based lexical scanner, or parse comments with a regex that respects backslash escapes — matching `\\/` as an escaped slash.
    - Verify that content inside angle brackets `<...>` comes through the comment parser unmodified.
- **Symptoms**: A witness's readings truncate mid-sentence; a segment ends abruptly where the source continues; text following an escaped slash or an angle-bracketed node disappears from the collation.
- **Detection Pattern**: Post-scrub witness text measurably shorter than its source paragraph at a position where the source holds `\/` or `\\/`, or a scrubbed string terminating immediately after an escape sequence.

---

## Footnote Disassociation

- **Id**: footnote-disassociation
- **Summary**: Segmenting text runs into sentences or individual words misplaces or drops footnotes that the `.docx` attaches to specific words.
- **Severity**: medium
- **Situation**: A footnote attaches to a word in Witness A, and automatic sentence splitting loses the footnote text or matches it to the wrong segment.
- **Why**: Paragraph text parsed as a flat string loses the XML association to its footnote elements, and nothing in the flattened form records where each reference sat.
- **Solution**:
    - Extract footnotes and map them to their character position offsets in the paragraph *before* splitting that paragraph into sentences and words.
    - Carry the footnote references along with the node objects through alignment.
- **Symptoms**: The output annotation count falls short of the source document's footnote count; a footnote surfaces against a segment whose text it does not discuss; annotations cluster on the first or last segment of a paragraph.
- **Detection Pattern**: A parsed witness whose collected footnote count differs from the count of footnote reference elements in the source `.docx`, or a footnote mapped to a segment index other than the one containing its character offset.
