# Critical Text Collation - Patterns

## Patterns

---
  #### **Name**
Hierarchical Sequence Alignment
  #### **Description**
First, segment witnesses into sentences automatically using NLP/regex heuristics (standard punctuation). Then, align the sentence segments across all witnesses using a sentence-level similarity metric (e.g. TF-IDF or normalized Levenshtein). Finally, perform fine-grained word/node sequence alignment within each aligned sentence group.
  #### **When**
Aligning multiple highly divergent transcription witnesses to prevent global alignment drift.
  #### **Example**
    - Step 1: Witness A and B split into sentences.
    - Step 2: Sentence 1 of Witness A is aligned with Sentence 1 of Witness B based on semantic similarity.
    - Step 3: Align Witness A's "sat on a wall" against Witness B's "sat on a tall wall" at the word level.

---
  #### **Name**
Composite Node Comparison
  #### **Description**
Parse bracketed emendations `<word>` and interpolations `<prior\interpolated>` as single units (nodes) rather than treating them as separate words or strings. When comparing a composite node to another node (composite or plain), evaluate similarity based on both the prior/canceled readings and the final/interpolated readings.
  #### **When**
Running word-level alignment on transcriptions containing complex corrections or revisions.
  #### **Example**
    - Node A: `<naught\ground>`
    - Node B: `ground`
    - Comparison: The agent recognizes Node A's final reading is `ground`, matching Node B with high similarity, but preserves the full bracketed string `<naught\ground>` in Node A's column cell.

---
  #### **Name**
Rich Text Cell Generation
  #### **Description**
When outputting collation cells to Excel, translate `.docx` rich text run formatting (bold, italic, strikethrough) into cell-level formatted runs using an XML-based Excel generator (such as `openpyxl`'s `CellRichText` or inline XML formatting).
  #### **When**
Preserving editorial formatting (like strikethrough for cancellations) in the final collation.
  #### **Example**
    - Word document run: `saith` (normal), `said` (strikethrough)
    - Excel cell output: A cell containing both runs with individual Font properties applied (one with strikethrough=True).

---
  #### **Name**
Space Replacement with Bullets
  #### **Description**
Before writing text to any cell in the collation spreadsheet, replace all space characters (` `) with the bullet character `•` (U+2022). This groups multiple words inside a single node, ensuring no blank space character exists within cells.
  #### **When**
Writing aligned words or composite entities to the Excel sheet.
  #### **Example**
    - Node: `<naught\ground> for God`
    - Cell Output: `<naught\ground>•for•God`

---
  #### **Name**
Scrub Comments and Annotations
  #### **Description**
Strip all inline comments `//` and block comments `/* ... */` from the transcription content during parsing. Extract Word footnotes separately to map them to the corresponding segment/node as metadata or annotations, rather than aligning comment strings.
  #### **When**
Ingesting `.docx` transcriptions for collation.
  #### **Example**
    - Raw: `saith the Lord // comment`
    - Cleaned: `saith the Lord`
