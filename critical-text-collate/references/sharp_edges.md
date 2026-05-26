# Critical Text Collation - Sharp Edges

## Sharp Edges

---
  #### **Name**
Alignment Drift on Divergent Witnesses
  #### **Summary**
When witnesses have highly divergent phrasing or structural omissions, standard sequence alignment algorithms can match unrelated words, resulting in skewed rows and excessive blank cells.
  #### **Severity**
critical
  #### **Situation**
  Witness A has a large insertion that doesn't exist in Witness B. A standard Levenshtein-based alignment tries to match individual words of the insertion to unrelated words in B, causing alignment drift.
  #### **Why**
  Naive sequence alignment relies too heavily on local word matching without checking overall sentence-level context.
  #### **Solution**
  - Use hierarchical sentence/line alignment first to anchor matching segments.
  - Set a minimum similarity threshold for matching nodes; if below the threshold, treat it as an addition/deletion (leaving empty cells).
  - Account for variation species (e.g., ORD for reorderings, LEX for synonyms) when calculating alignment penalties.

---
  #### **Name**
Corrupt Excel Rich Text Files
  #### **Summary**
Writing rich text (bold, italic, strikethrough) within Excel cells using openpyxl or other libraries can easily generate malformed OpenXML schemas, making the file unreadable in Microsoft Excel.
  #### **Severity**
high
  #### **Situation**
  The agent creates cell-level formatting using raw XML tags or incorrect object types in openpyxl, causing Excel to report the file as "corrupted and cannot be opened."
  #### **Why**
  Excel requires highly strict, nested XML structures for inline text formatting.
  #### **Solution**
  - Always use `openpyxl.cell.rich_text.CellRichText` and `openpyxl.cell.rich_text.TextBlock` objects.
  - Apply Font properties strictly to `TextBlock` objects and append them to `CellRichText`.
  - Validate generated spreadsheet files programmatically using a test script that opens the workbook.

---
  #### **Name**
Accidental Comment Stripping
  #### **Summary**
Regular expressions for stripping comments (e.g., `//` or `/* ... */`) can strip legitimate transcription text if comments appear inside quotes or escaped sequences.
  #### **Severity**
medium
  #### **Situation**
  A witness transcript has `Preach in their days\//...` (escaped characters) and the parser strips the text after the double slashes.
  #### **Why**
  Overly simplistic regex parsers ignore escape characters.
  #### **Solution**
  - Implement a state-based lexical scanner or parse comments using regex that respects backslash escapes (e.g., matching `\\/` as an escaped slash).
  - Verify that no content inside angle brackets `<...>` is accidentally modified by the comment parser.

---
  #### **Name**
Footnote Disassociation
  #### **Summary**
When text runs are segmented into sentences or individual words, footnotes attached to specific words in the `.docx` file can get misplaced or dropped.
  #### **Severity**
medium
  #### **Situation**
  A footnote is attached to a word in Witness A. During automatic sentence splitting, the footnote text is lost or matched to the wrong segment.
  #### **Why**
  Paragraph text is parsed as a flat string, losing the XML association to footnote elements.
  #### **Solution**
  - Extract footnotes and map them to their character position offsets in the paragraph *before* splitting the paragraph into sentences and words.
  - Carry the footnote references along with the node objects during alignment.
