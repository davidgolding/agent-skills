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

---

## Undeclared Namespace Prefixes

- **Id**: undeclared-namespace-prefixes
- **Summary**: TEI exports such as the Joseph Smith Papers use `pm:` and `lds:` attributes without declaring their namespaces, so every standard XML parser rejects the files.
- **Severity**: high
- **Situation**: A JSP file is opened with an XML library and fails with "unbound prefix", or appears to declare its prefixes because the declarations sit inside XML comments.
- **Why**: Namespace declarations inside comments do not count, and an unbound prefix makes the document not namespace-well-formed.
- **Solution**:
    - Convert with `scripts/tei_convert.py`, which declares each prefix used outside comments before parsing and leaves the original file unchanged.
- **Symptoms**:
    - Parse errors "unbound prefix: line 2, column 0" across a whole series.
    - The cause "undeclared namespace prefixes declared for parsing" on every JSP file.
- **Detection Pattern**: An XML file whose element or attribute names use a prefix that no `xmlns:` attribute outside a comment declares.

---

## Page Break Closes the Page

- **Id**: page-break-closes-page
- **Summary**: JSP places `<pb n="N">` after page N's text, so a direct mapping to `@pN` labels every page with the previous page's number.
- **Severity**: critical
- **Situation**: A converter emits `@p1` where the first `pb` sits, putting page 1's label at the top of page 2 and leaving page 1 unlabeled.
- **Why**: Standard TEI `pb` marks the start of a page and spec B2 milestones open a page; JSP's encoding marks the end, so every line citation by page shifts by one.
- **Solution**:
    - Use the jsp profile, which writes the first `pb`'s label before the first line and each later label at the preceding break.
    - In the pilot, check that `@p1` precedes the document's first line and the last page label is the last `pb`'s `n`.
- **Symptoms**:
    - A witness whose first line has no milestone above it while its last line is followed by one.
    - The cause "text follows the final page-closing break".
- **Detection Pattern**: A converted JSP witness whose first body line is not a page milestone, or whose final line is a page milestone.

---

## Transcriber Attributes Read as Hands

- **Id**: transcriber-attributes-as-hands
- **Summary**: `resp` on `del`, `add`, `gap`, and `handShift` names the edition's transcriber, not a hand in the source.
- **Severity**: high
- **Situation**: A deletion encoded `<del resp="Constance Palmer Lewis">` is written as `{-words@Constance Palmer Lewis}`, attributing the deletion to a modern staff member.
- **Why**: TEI `resp` records responsibility for the encoding; the source hand is `hand` on the element or `scribe` on `handShift`.
- **Solution**:
    - Take hands only from `hand` and `handShift/@scribe` (or `@new`), naming them in `hands` from the edition's person references.
- **Symptoms**:
    - `hands` values that are staff usernames such as `seniels` or `DarowskiKH`.
- **Detection Pattern**: A `hands` frontmatter value or `@` mark value that matches a `resp` attribute value in the source XML.

---

## Supplied Text Read as Gap Syntax

- **Id**: supplied-text-as-gap-syntax
- **Summary**: Editor-supplied punctuation such as `<supplied>.</supplied>` becomes `[.]`, which the specification reads as a malformed gap mark.
- **Severity**: medium
- **Situation**: Supplied text, a rendition, or a description begins with a character that is also a mark operator (`.`, `?`, `_`, `+`, `-`, `!`, `=`, `@`).
- **Why**: The first character inside a bracket or brace is the operator (M1), so content beginning with one is parsed as a different mark.
- **Solution**:
    - Escape an operator character at the start of mark content (`[\.]`); `tei_convert.py` does this automatically.
- **Symptoms**:
    - Validator error M1 "gap mark must be [.N] or [.?]: [.]".
- **Detection Pattern**: A bracket or brace mark whose content begins with an unescaped operator character but does not match that operator's mark grammar.

---

## Duplicate TEI Inputs

- **Id**: duplicate-tei-inputs
- **Summary**: The same TEI document appears in more than one folder of an edition export, such as JSP's `Legal Part 1` and `Legal Part 2`.
- **Severity**: high
- **Situation**: A series folder is converted and the same TEI id produces two witness files with suffixed keys.
- **Why**: Exports split for size often repeat boundary files; two copies of one source break key uniqueness by identity rather than by name.
- **Solution**:
    - Identify documents by TEI id; the converter keeps the first by edition order and lists the rest as "duplicate input".
    - Record the TEI id in `source` so later runs recognize documents already in the corpus.
- **Symptoms**:
    - Two corpus files whose `source` values end in the same TEI id.
- **Detection Pattern**: Two inputs or corpus files whose root `xml:id` (or `source` TEI id) is identical.

---

## Editorial Titles and Staff Residue

- **Id**: editorial-titles-and-staff-residue
- **Summary**: Edition titles are editorial descriptions that may carry staff residue such as `LIVE FILE IN D13_`, case names in brackets, and scripture references.
- **Severity**: medium
- **Situation**: A key is built from `LIVE FILE IN D14, Pay Order to Nauvoo City Treasurer for Josiah Arnold, 1 March 1844` without cleanup.
- **Why**: Keys must hold the title's key words in N8 characters; residue and brackets produce invalid or misleading keys.
- **Solution**:
    - Strip staff prefixes from `title` and report the removal; drop bracketed matter and the date phrase from the key's short title while keeping them in `title`.
- **Symptoms**:
    - Keys beginning with "LIVE FILE" or containing case names; the cause "JSP staff prefix removed from title".
- **Detection Pattern**: A title or key containing the words "LIVE FILE IN" or a bracketed segment carried into the key.

---

## Missing Header Authors

- **Id**: missing-header-authors
- **Summary**: Most JSP documents name no author in the header, so keys would omit the author unless it is inferred or set.
- **Severity**: medium
- **Situation**: A Documents-series letter titled "Letter to Oliver Cowdery" has no `listPerson` author and receives the key `Letter to Oliver Cowdery (1829 Oct 22)`.
- **Why**: Only about one JSP file in six lists an author; the rest rely on the series convention that JS is the author or on the title's "A to B" form.
- **Solution**:
    - Let the converter infer authors from the title's "Type, A to B" and "X from A" forms, and settle the remaining "author not stated" cause once per series, with `--default-author` when the series convention applies.
- **Symptoms**:
    - Many keys without an author delimiter in a series where the user expects one.
- **Detection Pattern**: A grouped cause "author not stated (key will omit author)" covering a large share of a series.

---

## Unknown Edition Year

- **Id**: unknown-edition-year
- **Summary**: The editorial companion's date needs the edition's publication year, which most online-only JSP documents do not state.
- **Severity**: medium
- **Situation**: A companion is drafted for a legal record with no print-volume reference and no posting date.
- **Why**: A companion without a date has no valid key (N1, N5), and a guessed year misdates the editors' work.
- **Solution**:
    - Use the print volume's year when known (`--edition-year VOL=YYYY` adds or corrects one), then the posting year, then the latest revision year; otherwise hold the companion back and ask for `--editorial-date`.
- **Symptoms**:
    - The cause "editorial date unknown; companion held back" or "publication year unknown for JSP volume D11".
- **Detection Pattern**: A TEI document with apparatus whose companion has no date source among print volume, posting date, revision history, or option.

---

## Edition Prose in the Transcription Slot

- **Id**: edition-prose-in-transcription-slot
- **Summary**: Some edition files carry the editors' own writing where a transcription would sit, such as JSP legal case introductions and calendars of documents.
- **Severity**: high
- **Situation**: A JSP file titled "Introduction to Gray v. A. Allen" has a `docbody` holding a case history and a calendar, which a converter writes as a primary-source witness.
- **Why**: The editors' prose in a source collection defeats the separation of sources from editorial content and misattributes the text to the documents' authors.
- **Solution**:
    - Let the jsp profile send such documents to the editorial collection alone; check the cause "edition-written document (introduction or calendar) sent to the editorial collection" in the pilot.
    - For other editions, look for structural markers or titles that identify editorial pages and report them as a cause for the user to settle.
- **Symptoms**:
    - Witness files whose text discusses the documents in the third person and cites sources.
- **Detection Pattern**: A TEI document whose transcription contains footnoted narrative about other documents, or whose title begins "Introduction to" or "Calendar of Documents", or which carries `lds:EventGroup` elements.
