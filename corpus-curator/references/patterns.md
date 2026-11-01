# Corpus Curator Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by corpus-curator.

The governing standard is the Markdown Source Corpus Specification (David Golding, October 2026, https://davidgolding.com/corpus-spec). Rule IDs below (D, N, F, B, M, E, A plus a number) refer to it. `templates/CONVENTIONS.md` restates its rules in short form; read it before converting.

## Patterns

- **Name**: Deterministic Extraction Workspace
- **Description**: Run `scripts/extract.py` on the input into a fresh temporary directory outside the corpus. It writes `extract.txt` (the file's own characters; PDF pages split by form feeds), `structure.md` (pandoc GFM keeping headings, emphasis, and notes), page images for image-only pages, and `info.json` with a classification hint per input, plus a `manifest.json` listing skipped files.
- **When**: At the start of every run, before reading any input.
- **Example**:
```
    WORK=$(mktemp -d)
    python3 corpus-curator/scripts/extract.py "Letters to Add" "$WORK"
    # exit 3 -> report the missing tools it printed and stop
    # skipped / failed inputs in $WORK/manifest.json go straight to the run report
```

---

- **Name**: Classify Then Route
- **Description**: Decide each source's kind from `info.json` and a look at its text. `scan`: read the page images. `text-layer`: decide between born-digital (published typeset text) and existing transcription (someone's rendering of a manuscript, often with their own brackets, strikethroughs, or superscripts). `mixed`: use the text layer for text pages and the images for the rest. A text layer of garbage (stray symbols, words split by spaces) is a bad hidden OCR layer; treat that source as a scan.
- **When**: For every extracted input, before choosing mode or structure.
- **Example**:
```
    hint=text-layer, typeset book with running heads      -> born-digital, prose mode
    hint=text-layer, DOCX with [illegible] and strikeouts -> existing transcription, diplomatic mode
    hint=scan, photographed letter                        -> scan, diplomatic mode
    hint=text-layer, "T h e  C h u r c h" garble          -> scan (bad OCR layer)
```

---

- **Name**: Copy Characters, Add Structure
- **Description**: Build the body by copying text from `extract.txt` (or `structure.md` for emphasis, headings, and notes) and adding only line breaks, blank lines, milestones, marks, and the `@notes` block. Copy with tools or exact string handling rather than retyping, so curly quotes, long s, diacritics, and spellings survive (E2). Normalize the result to NFC with LF endings and a final newline (E1).
- **When**: Every source with a text layer.
- **Example**:
```
    extract.txt page 12: "the Saints’ conference was held..."
    body line:           the Saints’ conference was held...   (U+2019 kept, not ')
```

---

- **Name**: Mode Selection
- **Description**: Choose `diplomatic` when the source's own lines matter (manuscripts, letters, diaries, poetry, inscriptions, existing line-by-line transcriptions), giving one file line per source line. Choose `prose` for typeset prose (books, articles, newspapers), giving one file line per paragraph with a blank line between paragraphs (B1, B3). Keep each unit whole on one line.
- **When**: After classification, once per source.
- **Example**:
```
    Letter, diplomatic:          Book, prose:
    Dear Jane,                   It was a cold morning when the company set out for the river, and ...
    I write in haste to tell     
    you that the wagon left      The second day brought rain.
```

---

- **Name**: Born-Digital Cleanup
- **Description**: In typeset extractions, drop running heads and folios as text and record each printed page with a `@p` milestone on its own line at the point the page begins, using the printed label (`@p12`, `@pxii`) (B2). In prose mode, rejoin words hyphenated across line ends; in diplomatic mode, keep the line-end hyphen. Keep printed headings as `#` headings at their printed level and wording (B4). Move footnotes printed at page foot to `[^n]` references in the text and definitions after `@notes` (B7).
- **When**: Born-digital and mixed sources.
- **Example**:
```
    extract page 13:  "ROUGH STONE ROLLING\n13\ncon-\ntinued the journey..."
    body:             @p13
                      continued the journey...
```

---

- **Name**: Convention Translation
- **Description**: Map an existing transcription's editorial conventions to the specification's marks when the meaning is one-to-one, and flag any convention whose meaning is unclear as an uncertain field in the review table. Common mappings: strikethrough -> `{-abc}`; superscript or caret insertion -> `{+abc@above}`; `[illegible]` -> `[?.?]`; `[word?]` for an unclear reading -> `[?word]`; `[sic]` after a word -> `[!word]`; `<abc>` or `[abc]` for editor-supplied text -> `[+abc]` or `[abc]`; `[page 2]` -> `@p2`; underline -> `{abc@underline}`. Run the fidelity check with `--loose` for these sources, because bracket punctuation changes by design.
- **When**: Sources classified as existing transcriptions.
- **Example**:
```
    source DOCX:  I ~~went~~ ^came^ to [illegible] on Tuesday [sic]
    body:         I {-went+came} to [?.?] on [!Tuesday]
```

---

- **Name**: Marked Uncertainty for Image Pages
- **Description**: Read image-only pages line by line at full resolution. Write each confident reading plainly, an unclear but probable reading as `[?abc]`, illegible characters as `[?.n]` with the estimated count, lost text of unknown extent as `[.?]`, and the hand's additions and deletions with `{+...}` and `{-...}`. Record vision transcription honestly in `resp`.
- **When**: Scans and the image pages of mixed PDFs.
- **Example**:
```
    I write in haste to {+tell@h2 above} you that the [?wagon] left
    this morning with [?.3] aboard.
    resp: corpus-curator 2026-10; transcribed from page images by vision, not proofread
```

---

- **Name**: Key Construction
- **Description**: Build `{Author} - {Short Title} ({Date})` step by step. Author: Chicago surname as given, `A and B`, or `A, et al.`; a letter's writer; omitted for an institution's published work; the issuing body for a generic record (N2). Short title: key words of the main title in order, subtitle and initial article dropped, three to five words, headline case (N3, N4). Date: `Y`, `Y M`, or `Y M j`, as much as needed to tell sources apart, which for primary sources is usually the full day (N5). Then strip every character outside the N8 allowlist, use U+0027 for apostrophes, romanize non-Latin text, and check length (N9).
- **When**: For every source, after the frontmatter `title`, `author`, and `date` are drafted.
- **Example**:
```
    "Zion's Camp: A History of the 1834 March," Jane Q. O'Neil, 1998
    -> O'Neil - Zion's Camp (1998)
    Minutes of the Kirtland High Council, 14 February 1835
    -> Kirtland High Council - Minutes (1835 Feb 14)
```

---

- **Name**: Frontmatter Assembly
- **Description**: Write the keys in spec order, omitting unused optional keys: `title` verbatim with subtitle; `author` as `Surname, Forename` (joined with `; `, roles in parentheses); `date` in EDTF with `~` or `?` when inferred; `source` as the full citation of the witness actually transcribed; `type` from the allowed list; `lang` as BCP 47 tags; `mode`; `hands` when marks name hands; `resp` naming corpus-curator, the month, the method, and the check performed (F1-F4). Wrap a value in double quotes when it contains `: ` or ` #`.
- **When**: For every source.
- **Example**:
```
    ---
    title: "Zion's Camp: A History of the 1834 March"
    author: O'Neil, Jane Q.
    date: 1998
    source: Jane Q. O'Neil, Zion's Camp (Provo, UT: Example Press, 1998), PDF from publisher
    type: book
    lang: en
    mode: prose
    resp: corpus-curator 2026-10; extracted from PDF text layer, diffed against extraction
    ---
```

---

- **Name**: Confidence Triage
- **Description**: Mark a row uncertain when any of these holds: the author, date, or title came from inference rather than the document's own statement; the date needed an EDTF `~` or `?`; `source` lacks a repository or publisher; the collection was guessed rather than given by the user or the input folder; the type or mode is a judgment between two values; a transcription convention had no clear mapping; more than a handful of `[?...]` marks were needed on one page; or the key collides with an existing key. Every other row is confident.
- **When**: At the end of drafting each source, before the review table.
- **Example**:
```
    | Input        | Proposed key                          | Collection        | Uncertain field: draft (reason)              |
    | scan_014.jpg | Doe - Letter to Jane Doe (1900 Jan 1)  | Doe Family Papers | date: 1900-01-01 (year read from faded line) |
```

---

- **Name**: Collision Judgment
- **Description**: Compare a colliding key's frontmatter and opening lines with the existing file. Different text or a different document: assign the next unused N6 suffix (`b`, then `c` ... `z`, `aa` ... `zz`), checking both the corpus and keys issued earlier in this run. Same document (matching text) or another witness of it: put the row in the review table with the choices skip, replace, or suffix. Keep every existing key unchanged.
- **When**: Whenever a drafted key matches an existing or earlier-in-run key after NFC and case folding.
- **Example**:
```
    existing Doe - Letter to Jane Doe (1900 Jan 1).md, new letter with different text
    -> Doe - Letter to Jane Doe (1900 Jan 1b)
```

---

- **Name**: Assets Placement
- **Description**: Copy each scan or page image (and each rendered image page of a scanned PDF) into `Assets/` as `{key} {label}.{ext}`, using the page or folio label that matches the body milestone (`p1`, `f4r`). Leave text-native originals (DOCX, born-digital PDF, TXT, MD) in place and uncopied. Copy originals and leave each one where it was.
- **When**: In the write phase, for sources with image pages.
- **Example**:
```
    Assets/Doe - Letter to Jane Doe (1900 Jan 1) p1.jpg
    Assets/Doe - Letter to Jane Doe (1900 Jan 1) p2.jpg
```

---

- **Name**: Audit Loop
- **Description**: After writing, run the validator scoped to the written files, then the fidelity check on each file that has an extraction. Fix the file for every error and unexplained difference and re-run both until clean. Use `--prose` for prose-mode files and `--loose` for translated transcriptions. Pass `--allow-deletion` only for text deliberately left out (a running head printed once, a publisher's colophon outside the work) and list each one in the report. For image-only sources, re-read each image against the written lines.
- **When**: After every write, before the report.
- **Example**:
```
    python3 corpus-curator/scripts/validate_corpus.py "$CORPUS" --files "$CORPUS/Doe Family Papers/Doe - Letter to Jane Doe (1900 Jan 1b).md"
    python3 corpus-curator/scripts/fidelity_check.py "<written file>" "$WORK/letter.docx/extract.txt"
```

---

- **Name**: Verbose Run Report
- **Description**: End with a table listing every input, followed by short sections for created scaffolding, user corrections, allowed deletions, warnings, and pre-existing corpus errors left untouched. Columns: input file; result (written, skipped, failed); key; collection; kind; extraction method; mode; marks applied (counts by type); metadata inferred or corrected; assets copied; audit (validator and fidelity outcome). Close with the reminder that changes are uncommitted.
- **When**: At the end of every run, including runs that stop early.
- **Example**:
```
    | Input | Result | Key | Collection | Kind | Extraction | Mode | Marks | Metadata | Assets | Audit |
    | letter.docx | written | Doe - Letter to Jane Doe (1900 Jan 1b) | Doe Family Papers | transcription | pandoc | diplomatic | 1 {+}, 1 [?] | date inferred, confirmed by user | none | clean / clean |
    | notes.xyz | skipped (unsupported format) | | | | | | | | | |
```

---

## Anti-Patterns

- **Name**: Retyped Text
- **Description**: Writing the body from the model's own reading of a document that has a text layer.
- **Why**: The model normalizes quotes, fixes spellings, and drops words without noticing, and the fidelity check loses its independent baseline (E2, B8).
- **Instead**: Copy Characters, Add Structure.

---

- **Name**: Silent Best Guess
- **Description**: Writing an unsure reading or inferred date as if it were certain.
- **Why**: Downstream agents quote it as the source's words, and nothing in the file tells them otherwise.
- **Instead**: Marked Uncertainty for Image Pages, EDTF qualifiers in `date`, and Confidence Triage.

---

- **Name**: Editorial Structure
- **Description**: Adding headings, summaries, section labels, tags, or normalized spellings that the source does not have.
- **Why**: B4, F4, M7, and E6 reserve the file for the witness; added structure misleads readers and shifts line numbers.
- **Instead**: Structure From the Source: printed headings, milestones, and source notes only, with editorial comment confined to `[^e]` notes.

---

- **Name**: Hard-Wrapped Lines
- **Description**: Keeping the PDF's or the extractor's line breaks inside a prose paragraph.
- **Why**: Search returns lines; a wrapped paragraph splits every passage and every citation (B1).
- **Instead**: Mode Selection, with one paragraph per line in prose mode.

---

- **Name**: Tool Fallback
- **Description**: Reading a DOCX or text-layer PDF with the model's file reader because pandoc or poppler is missing.
- **Why**: It replaces deterministic characters with model output, which is the Retyped Text failure.
- **Instead**: Stop, report the install command printed by `scripts/extract.py`, and end the turn.

---

- **Name**: Audit by Allow-List
- **Description**: Passing `--allow-deletion` for text that should be in the file to make the fidelity check exit cleanly.
- **Why**: It hides dropped passages, the most damaging fidelity failure.
- **Instead**: Restore the missing text; reserve allowed deletions for material outside the work and report each one.

---

- **Name**: Over-Review
- **Description**: Showing every row, or every field, in the review table.
- **Why**: The user asked to review only uncertain rows; full tables on large folders bury the rows that need judgment.
- **Instead**: Confidence Triage, and full visibility in the Verbose Run Report.

---

- **Name**: Committing or Renaming
- **Description**: Running git commands, or renaming an existing corpus file to make room for a new key.
- **Why**: The user reviews and commits changes; issued keys are permanent (N6, D7).
- **Instead**: Leave changes uncommitted and use Collision Judgment.
