# Critical Text Collation Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by critical-text-collate.

## Patterns

- **Name**: Hierarchical Sequence Alignment
- **When**: Aligning multiple highly divergent transcription witnesses, where a single global pass would drift. Segment witnesses into sentences automatically using NLP/regex heuristics over standard punctuation, align those sentence segments across all witnesses with a sentence-level similarity metric (TF-IDF or normalized Levenshtein), then run fine-grained word/node alignment inside each aligned sentence group.
- **Example**: ```
  Step 1: Witness A and Witness B split into sentences.
  Step 2: Sentence 1 of A aligns to Sentence 1 of B on semantic similarity.
  Step 3: Inside that group, align A's "sat on a wall" against B's
  "sat on a tall wall" at the word level.
  ```

---

- **Name**: Composite Node Comparison
- **When**: Running word-level alignment on transcriptions containing complex corrections or revisions. Parse bracketed emendations `<word>` and interpolations `<prior\interpolated>` as single units (nodes) rather than as separate words or strings, and score similarity against another node — composite or plain — using both the prior/canceled reading and the final/interpolated reading.
- **Example**: ```
  Node A: <naught\ground>
  Node B: ground
  Comparison: A's final reading is "ground", matching B with high
  similarity; A's column cell still carries the full bracketed
  string <naught\ground>.
  ```

---

- **Name**: Rich Text Cell Generation
- **When**: Writing collation cells to Excel while preserving editorial formatting such as strikethrough for cancellations. Translate `.docx` rich text run formatting (bold, italic, strikethrough) into cell-level formatted runs through an XML-based Excel generator — `openpyxl`'s `CellRichText` or equivalent inline XML formatting.
- **Example**: ```
  Word document runs: "saith" (normal), "said" (strikethrough)
  Excel cell: one cell holding both runs, each with its own Font
  properties applied (the second with strikethrough=True).
  ```

---

- **Name**: Space Replacement with Bullets
- **When**: Writing aligned words or composite entities to the Excel sheet. Before any text reaches a cell, replace every space character with the bullet character `•` (U+2022), which groups multiple words inside a single node and keeps cells free of space characters.
- **Example**: ```
  Node: <naught\ground> for God
  Cell output: <naught\ground>•for•God
  ```

---

- **Name**: Scrub Comments and Annotations
- **When**: Ingesting `.docx` transcriptions for collation. Strip inline `//` comments and `/* ... */` block comments from the transcription content during parsing, and extract Word footnotes separately, mapping them to their corresponding segment/node as metadata rather than aligning comment strings as text.
- **Example**: ```
  Raw:     saith the Lord // comment
  Cleaned: saith the Lord
  ```

---

## Anti-Patterns

- **Name**: Flat Global Alignment
- **Why**: Running one word-level pass across each witness end to end lets a single large insertion or omission shift every subsequent match, so unrelated words pair up and the sheet fills with skewed rows and stray blank cells.
- **Instead**: Hierarchical Sequence Alignment

---

- **Name**: Base-Text Collation
- **Why**: Electing one witness as the base makes its readings the layout's spine, so its omissions become the corpus's omissions and its word order silently becomes the norm against which peers read as deviant.
- **Instead**: Peer multi-way alignment, where every witness contributes equally to row structure

---

- **Name**: Node Splitting on Brackets
- **Why**: Tokenizing `<naught\ground>` on its punctuation yields fragments like `naught` and `ground` as independent words, which align to unrelated nodes in other witnesses and destroy the correction's record of what was canceled in favor of what.
- **Instead**: Composite Node Comparison

---

- **Name**: Raw XML Rich Text
- **Why**: Hand-writing inline formatting tags or passing incorrect object types into a cell produces malformed OpenXML that Excel rejects outright, reporting the workbook as corrupted rather than as mis-formatted.
- **Instead**: Rich Text Cell Generation through `CellRichText` and `TextBlock` objects

---

- **Name**: Naive Comment Regex
- **Why**: A pattern matching `//` without regard for escapes strips legitimate transcription text wherever a witness carries an escaped slash, so `Preach in their days\//` loses everything after the slashes with no trace that content was removed.
- **Instead**: Escape-aware lexical scanning — see the `accidental-comment-stripping` sharp edge

---
