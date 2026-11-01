# Sharp Edges

This document defines the sharp edges used by corpus-curator.

---

## Typographic Character Drift

- **Id**: typographic-character-drift
- **Summary**: Curly quotes, apostrophes, dashes, or long s in the source become their ASCII look-alikes in the corpus file.
- **Severity**: critical
- **Situation**: The body is retyped or passed through a tool that "smartens" or "dumbs down" punctuation, so `Saints’` is written as `Saints'`.
- **Why**: Exact-string search and citation verification compare bytes; a single substituted apostrophe makes a correct quote fail as unsupported (E2, A3).
- **Solution**:
    - Copy text from `extract.txt` rather than retyping it.
    - Run `scripts/fidelity_check.py`; every CHANGED run must be fixed in the file.
- **Symptoms**:
    - Fidelity check reports CHANGED runs that differ only in punctuation.
    - A quote copied from the original cannot be found by fixed-string search.
- **Detection Pattern**: Fidelity check output listing a CHANGED run where the old and new words differ only by quote, apostrophe, or dash characters.

---

## Decomposed Unicode

- **Id**: decomposed-unicode
- **Summary**: Accented letters arrive as base letter plus combining mark (NFD) from PDFs or macOS filenames.
- **Severity**: high
- **Situation**: A key or body line containing `Brontë` is written in NFD form copied from a file path or a PDF text layer.
- **Why**: NFC and NFD forms are different bytes, so exact matches and key uniqueness checks fail silently (E1, D6).
- **Solution**:
    - Normalize every written body and filename to NFC before writing.
    - Run the validator, which reports non-NFC bodies and filenames.
- **Symptoms**:
    - Validator error E1 "not NFC-normalized".
    - Two keys that look identical but are both accepted by the filesystem.
- **Detection Pattern**: A file body or filename whose NFC normalization differs from its stored form.

---

## Hyphenation Ambiguity

- **Id**: hyphenation-ambiguity
- **Summary**: A hyphen at a printed line end may be a soft break (`con-tinued`) or a real compound (`well-known`).
- **Severity**: medium
- **Situation**: Rejoining line-end hyphens in prose mode turns `well-\nknown` into `wellknown`, or keeps `con-tinued`.
- **Why**: Either error changes the source's words and breaks search for them.
- **Solution**:
    - Rejoin by default in prose mode; keep the hyphen when the joined form is a compound that the same source hyphenates mid-line elsewhere.
    - Keep every line-end hyphen in diplomatic mode.
- **Symptoms**:
    - Fidelity check CHANGED runs at page-line boundaries.
    - Compound words missing their hyphen in prose files.
- **Detection Pattern**: Words in a prose-mode file formed by joining across an extraction line end where the same word appears elsewhere in the source with a hyphen.

---

## Scrambled PDF Reading Order

- **Id**: scrambled-pdf-reading-order
- **Summary**: Multi-column pages, sidebars, and footnotes come out of `pdftotext` interleaved or out of order.
- **Severity**: high
- **Situation**: A newspaper page or a two-column journal is extracted, and column text alternates line by line or footnotes land mid-paragraph.
- **Why**: The text layer stores glyph positions, not reading order; copying it as is corrupts paragraphs.
- **Solution**:
    - Check each page's extraction against its page image when the layout has columns or notes.
    - Reassemble paragraphs in reading order from the extracted characters; MOVED runs in the fidelity check are expected for relocated footnotes.
- **Symptoms**:
    - Sentences that stop mid-clause and resume lines later.
    - Many MOVED or DELETED plus INSERTED pairs in the fidelity output.
- **Detection Pattern**: Extracted pages where consecutive lines alternate between two unrelated sentences, or where footnote text appears between halves of a sentence.

---

## Bad Hidden OCR Layer

- **Id**: bad-hidden-ocr-layer
- **Summary**: A scanned PDF carries a low-quality OCR text layer that `extract.py` reports as `text-layer`.
- **Severity**: high
- **Situation**: The extraction is full of split words, stray symbols, and misread letters, but it is treated as authoritative source characters.
- **Why**: Deterministic extraction is only faithful when the text layer is the document's real text; bad OCR is someone else's unmarked guesses.
- **Solution**:
    - Compare a sample page of the extraction with its rendered image.
    - When the layer is unreliable, treat the source as a scan, transcribe from images with marks, and note the decision in the report.
- **Symptoms**:
    - Words like `t h e` or `rn` for `m` throughout the extraction.
    - Fidelity checks pass while the text plainly differs from the page image.
- **Detection Pattern**: A text-layer extraction with frequent single-letter tokens, non-words, or symbol clusters relative to its page count.

---

## Ligatures in Extraction

- **Id**: ligatures-in-extraction
- **Summary**: Typeset ligatures such as `ﬁ` and `ﬂ` appear as single code points in PDF text.
- **Severity**: medium
- **Situation**: The body copies `ﬁrst` with U+FB01, so searches for `first` fail.
- **Why**: A typeset ligature is a font feature, not a source character; the specification keeps source characters, not typesetting.
- **Solution**:
    - Expand typographic ligatures (U+FB00 to U+FB06) to their letters when copying; the fidelity check already treats them as expanded.
    - Keep ligatures that the source uses as letters (such as `æ` in a Latin text).
- **Symptoms**:
    - Search misses for common words containing fi, fl, ff.
- **Detection Pattern**: Corpus body text containing code points U+FB00 through U+FB06.

---

## Expansion Look-Alikes

- **Id**: expansion-look-alikes
- **Summary**: Source text such as `friend(s)` looks like the abbreviation-expansion mark `a(bc)`.
- **Severity**: low
- **Situation**: The fidelity check's witness view strips `(s)` as an expansion and reports a CHANGED run, or the search view joins it.
- **Why**: The expansion mark is a letter followed directly by parenthesized letters, which ordinary text can also contain.
- **Solution**:
    - Keep the source's parentheses; when the fidelity check flags one, confirm it against the extraction and pass it with `--allow-deletion` only if it is a false positive, naming it in the report.
- **Symptoms**:
    - CHANGED runs where the extraction shows `word(s)` and the witness view shows `word`.
- **Detection Pattern**: Fidelity differences where the extraction token contains a letter immediately followed by a parenthesized group of letters.

---

## Case-Insensitive Key Collisions

- **Id**: case-insensitive-key-collisions
- **Summary**: Two keys that differ only in case or Unicode form are treated as different by the agent but as one file by the filesystem.
- **Severity**: critical
- **Situation**: `Smith - Letter (1840)` exists and a new `Smith - letter (1840)` is written on APFS, silently overwriting the first.
- **Why**: APFS and NTFS are case-insensitive by default; D6 compares keys after NFC and case folding.
- **Solution**:
    - Compare every drafted key with existing keys and earlier keys from this run after NFC and case folding, before writing.
    - Apply Collision Judgment for every match.
- **Symptoms**:
    - An existing file's content changes after a run.
    - Validator error D6.
- **Detection Pattern**: Two drafted or stored keys whose NFC case-folded forms are equal.

---

## Filename and Frontmatter Date Drift

- **Id**: filename-frontmatter-date-drift
- **Summary**: The key's date and frontmatter `date` disagree after one is corrected and the other is not.
- **Severity**: high
- **Situation**: The user corrects a date in the review table, and the agent updates `date` but keeps the old key.
- **Why**: N10 requires the filename date to be a truncation of `date`; disagreement breaks the key as a citation.
- **Solution**:
    - Rebuild the key whenever `date`, `author`, or `title` changes in review, before writing.
- **Symptoms**:
    - Validator error N10 on year, month, or day.
- **Detection Pattern**: A source whose filename year, month, or day differs from the corresponding part of its frontmatter `date`.

---

## Apostrophe Rule Conflict

- **Id**: apostrophe-rule-conflict
- **Summary**: The specification lists `’` among allowed key characters but also says the apostrophe is always U+0027.
- **Severity**: medium
- **Situation**: A key such as `O’Brien - Letters (1850)` is written with U+2019 copied from the title.
- **Why**: Keys are typed into searches and shell commands; one apostrophe form keeps them predictable. The validator enforces U+0027.
- **Solution**:
    - Write U+0027 in keys and collection names; keep the source's own apostrophe in `title` and the body.
- **Symptoms**:
    - Validator error N8 "uses U+2019".
- **Detection Pattern**: A key or collection name containing U+2019.

---

## Unquoted Colon in Frontmatter

- **Id**: unquoted-colon-in-frontmatter
- **Summary**: A title or source citation containing `: ` breaks YAML parsing when left unquoted.
- **Severity**: high
- **Situation**: `title: Zion's Camp: A History` is written as is.
- **Why**: YAML reads `: ` as a nested mapping, so loaders reject the file or truncate the value (F1).
- **Solution**:
    - Wrap any value containing `: ` or ` #` in double quotes, escaping inner `"` as `\"`.
- **Symptoms**:
    - Validator error F1 "contains ': ' or ' #'".
    - The corpus server lists the source with a missing or truncated title.
- **Detection Pattern**: An unquoted frontmatter value containing a colon followed by a space, or a space followed by a hash sign.

---

## Context Flood on Long Works

- **Id**: context-flood-long-works
- **Summary**: Reading a whole book's extraction at once crowds out the instructions and earlier sources.
- **Severity**: high
- **Situation**: A 600-page PDF's `extract.txt` is read in one pass while processing a folder.
- **Why**: Accuracy drops as context grows, and the rest of the run loses its working memory.
- **Solution**:
    - Process sources one at a time and read extractions in page ranges, writing the body incrementally.
    - Split at the work's own volumes or parts when the file would exceed about 2,000 lines (B9, N7).
- **Symptoms**:
    - Later sources in a run show more fidelity failures than earlier ones.
    - Skipped pages or repeated passages.
- **Detection Pattern**: Reading an extraction file longer than a few thousand lines in a single read.

---

## Missing Extraction Tools

- **Id**: missing-extraction-tools
- **Summary**: pandoc or poppler is not installed, so `extract.py` exits with status 3.
- **Severity**: medium
- **Situation**: A user on a fresh machine asks to add DOCX or PDF files.
- **Why**: Falling back to model reading would make the text the model's, not the file's.
- **Solution**:
    - Report each missing tool with the install command `extract.py` prints, and end the turn without converting.
- **Symptoms**:
    - `extract.py` prints "Missing required tools; nothing was extracted".
- **Detection Pattern**: An extraction run that exited with status 3.
