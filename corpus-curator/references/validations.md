# Validations

This document defines the validations used by corpus-curator.

Rules marked as checked by the validator are enforced by `scripts/validate_corpus.py`; run it scoped to the files written in a run. Semantic rules are checked by the agent during the audit phase. Paths below are relative to the corpus root.

---

## Root Layout

- **Id**: corpus-root-layout
- **Severity**: error
- **Type**: schema
- **Pattern**: A corpus root holding anything other than `CONVENTIONS.md`, an `Assets` folder, and collection folders (hidden entries excepted); a collection folder holding a subfolder or a non-Markdown file; a missing `CONVENTIONS.md` (D1, D2, D4). Checked by the validator.
- **Message**: The corpus root and collection folders must stay flat and hold only their allowed contents.
- **Fix Action**: Move binaries into `Assets/`, flatten subfolders into their top-level collection, and create `CONVENTIONS.md` from `templates/CONVENTIONS.md`.
- **Applies To**:
    - CONVENTIONS.md
    - */
    - */*

---

## Collection Name

- **Id**: corpus-collection-name
- **Severity**: error
- **Type**: regex
- **Pattern**: A collection folder name containing a date in parentheses, a character outside the N8 allowlist, or colliding case-insensitively with another collection name (D3). Checked by the validator.
- **Message**: Collection folders take the collection's short title, with a repository identifier in parentheses only to disambiguate.
- **Fix Action**: Rename the new collection to its short title, adding the repository identifier, such as `Smith Family Papers (MS 4152)`, when two share a title.
- **Applies To**:
    - */

---

## Key Pattern

- **Id**: corpus-key-pattern
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?:(?P<author>.+?) - )?(?P<title>.+?) \((?:(?P<y1>\d{4})–(?P<y2>\d{4})|(?P<y>\d{4})(?: (?P<m>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?: (?P<d>[1-9]|[12]\d|3[01]))?)?(?P<sfx>[b-z]|[a-z]{2})?)\)\.md$
- **Message**: The filename does not match `{Author} - {Short Title} ({Date}).md` with a valid date and suffix (N1, N5, N6). Checked by the validator.
- **Fix Action**: Rebuild the key per the Key Construction pattern in `references/patterns.md`.
- **Applies To**:
    - */*.md

---

## Key Characters

- **Id**: corpus-key-characters
- **Severity**: error
- **Type**: regex
- **Pattern**: An author or title part containing anything other than Latin letters, combining marks, ASCII digits, single spaces, and `' , . & -`; U+2019 in place of U+0027; a word starting with a hyphen; ` - ` more than once; a parenthesis or en dash outside the date (N8). Checked by the validator.
- **Message**: Keys use only the N8 character allowlist so they stay legal and typeable on every system.
- **Fix Action**: Drop the disallowed characters from the short title, replace U+2019 with U+0027, and romanize non-Latin text (ALA-LC).
- **Applies To**:
    - */*.md

---

## Key Length

- **Id**: corpus-key-length
- **Severity**: warning
- **Type**: schema
- **Pattern**: A key longer than 80 characters (warning) or a filename longer than 200 bytes of UTF-8 (reported as an error by the validator) (N9).
- **Message**: Long keys are hard to cite and push asset names toward the 255-byte filesystem limit.
- **Fix Action**: Shorten the short title to three to five key words.
- **Applies To**:
    - */*.md

---

## Key Agreement and Calendar

- **Id**: corpus-key-agreement
- **Severity**: error
- **Type**: semantic
- **Pattern**: A filename date that does not exist on the calendar; a suffix without its predecessor sibling; a key author surname missing from frontmatter `author`; a filename date that is not a truncation of frontmatter `date` (N10). Checked by the validator.
- **Message**: The key must agree with the frontmatter and with its suffix siblings.
- **Fix Action**: Rebuild the key from the corrected frontmatter, or assign the next unused suffix.
- **Applies To**:
    - */*.md

---

## Corpus-Wide Key Uniqueness

- **Id**: corpus-key-unique
- **Severity**: error
- **Type**: schema
- **Pattern**: Two source files in any collections whose keys are equal after NFC normalization and case folding (D6). Checked by the validator.
- **Message**: Keys identify sources across the whole corpus and must be unique without regard to case.
- **Fix Action**: Apply the Collision Judgment pattern; leave the existing key unchanged.
- **Applies To**:
    - */*.md

---

## Asset Names

- **Id**: corpus-asset-names
- **Severity**: error
- **Type**: schema
- **Pattern**: A file in `Assets/` whose name is not an existing key, a space, a label without spaces, and an extension (D5). Checked by the validator.
- **Message**: Asset names must start with the key of the source they witness.
- **Fix Action**: Rename the copied asset to `{key} {label}.{ext}`, using the page or folio label of its milestone.
- **Applies To**:
    - Assets/*

---

## Frontmatter Form

- **Id**: corpus-frontmatter-form
- **Severity**: error
- **Type**: syntax
- **Pattern**:
    - First line of the file is anything other than exactly `---`
    - No closing `---` line
    - A frontmatter line that is not one flat `key: value`
    - A duplicate key, a key outside title, author, date, source, type, lang, mode, hands, resp, or keys out of that order
    - An empty value
    - An unquoted value containing `: ` or ` #`, or starting with a YAML indicator character
- **Message**: Frontmatter must be one flat YAML block with the specification's keys in order (F1, F2, F4). Checked by the validator.
- **Fix Action**: Rewrite the block in spec order, drop empty or derived keys, and double-quote values containing `: ` or ` #`.
- **Applies To**:
    - */*.md

---

## Required Frontmatter Values

- **Id**: corpus-frontmatter-values
- **Severity**: error
- **Type**: schema
- **Pattern**: Missing `title`, `date`, `source`, `type`, `lang`, `mode`, or `resp`; `date` not EDTF Level 1 or not on the calendar; `type` outside the spec list and the `## Types` section of `CONVENTIONS.md`; `mode` other than `diplomatic` or `prose`; `lang` not BCP 47; a hand used in marks but absent from `hands` (F2, F3). Checked by the validator.
- **Message**: Required frontmatter values are missing or malformed.
- **Fix Action**: Supply the value from the document or the review table; record uncertain dates with EDTF `~` or `?`.
- **Applies To**:
    - */*.md

---

## Honest Responsibility Statement

- **Id**: corpus-resp-honest
- **Severity**: error
- **Type**: semantic
- **Pattern**: A `resp` value that omits corpus-curator as transcriber, omits the month, or claims a check that did not happen (such as "proofread" or "keyed twice") for an agent-produced file.
- **Message**: `resp` must say who produced the text, when, and how it was actually checked.
- **Fix Action**: Write `resp` as `corpus-curator YYYY-MM; <method>, <check performed>`, such as `corpus-curator 2026-10; transcribed from page images by vision, not proofread`.
- **Applies To**:
    - */*.md

---

## Encoding Bytes

- **Id**: corpus-encoding-bytes
- **Severity**: error
- **Type**: syntax
- **Pattern**: A byte-order mark, CR characters, a missing final newline, trailing whitespace, invalid UTF-8, or a body or filename that is not NFC (E1). Checked by the validator.
- **Message**: Files must be UTF-8 NFC with LF endings so exact-string search always matches.
- **Fix Action**: Re-encode as UTF-8 without BOM, normalize to NFC, convert line endings to LF, strip trailing whitespace, and end with one newline.
- **Applies To**:
    - */*.md

---

## Syntax Set and Indentation

- **Id**: corpus-syntax-set
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?<!\\)<(?:/?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?|!--)>?
    - ^[ \t]+\S
- **Message**: Source files use only CommonMark, GFM tables and footnotes, YAML, TeX, and the specification's marks, and no line begins with whitespace (E4, E5). Checked by the validator; code fences are reported as warnings.
- **Fix Action**: Remove HTML or escape a literal `<`; record meaningful indentation with `[_n]` at the line start.
- **Applies To**:
    - */*.md

---

## Line Units and Blank Lines

- **Id**: corpus-line-units
- **Severity**: error
- **Type**: semantic
- **Pattern**: A prose-mode paragraph spread across several file lines; a diplomatic-mode file whose lines do not follow the source's lines; two or more consecutive blank lines (B1, B3). The validator checks blank-line runs; the agent checks line units.
- **Message**: One file line must be one citable unit, and one blank line marks one structural break.
- **Fix Action**: Join wrapped prose paragraphs onto one line, re-split diplomatic text at the source's line ends, and collapse blank-line runs to one.
- **Applies To**:
    - */*.md

---

## Milestones

- **Id**: corpus-milestones
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^@(?!notes$)(?![A-Za-z][A-Za-z0-9:.\-]*$)
- **Message**: A line opening with `@` must be a milestone (`@p12`, `@f4r`, `@col2`, `@t00:14:05`) or `@notes`; source text opening with `@` must be escaped (B2, M5). Checked by the validator.
- **Fix Action**: Correct the milestone label or escape the literal `@` as `\@`.
- **Applies To**:
    - */*.md

---

## Source Headings Only

- **Id**: corpus-source-headings
- **Severity**: error
- **Type**: semantic
- **Pattern**: A `#` heading whose wording or level does not appear printed in the source, or a summary, label, or section title the editor added (B4, M7).
- **Message**: Headings record only what the source prints.
- **Fix Action**: Remove the added heading, or reword it to match the source's printed heading and level.
- **Applies To**:
    - */*.md

---

## Notes Block

- **Id**: corpus-notes-block
- **Severity**: error
- **Type**: schema
- **Pattern**: More than one `@notes` line; a note definition before `@notes`; anything other than note definitions and blank lines after `@notes`; a note reference without a definition; a label other than `n`, `en`, or `an`; a `[[key]]` cross-reference outside an editorial note or naming no existing key (B7). Checked by the validator; unreferenced definitions are warnings.
- **Message**: Notes keep the source's numbering, and all definitions follow one `@notes` line at the end of the file.
- **Fix Action**: Move definitions below a single `@notes` line, add missing definitions, and confine cross-references to `[^e]` notes.
- **Applies To**:
    - */*.md

---

## Transcription Marks

- **Id**: corpus-transcription-marks
- **Severity**: error
- **Type**: syntax
- **Pattern**: A bracket or brace not closed on its own line; an editorial mark inside an editorial mark, or a source-hand mark inside any mark; an unescaped `](`; a malformed gap `[.n]`, space `[_n]`, illegible `[?.n]`, description `[=figure: ...]`, or sic `[!sic>corr]`; a brace mark with neither an operator nor an `@` value (M1, M3, M4, M5). Checked by the validator.
- **Message**: Marks must use the operator grammar of Section 7, stay on one line, and nest only editorial-inside-source-hand.
- **Fix Action**: Close and reopen the mark on each line it spans, un-nest it, escape literal brackets and braces with `\`, and correct the operator form.
- **Applies To**:
    - */*.md

---

## Verbatim Fidelity

- **Id**: corpus-verbatim-fidelity
- **Severity**: error
- **Type**: semantic
- **Pattern**: Any CHANGED, INSERTED, or DELETED run reported by `scripts/fidelity_check.py` for a file with an extraction; for image-only sources, any written line that differs from the page image without a mark recording the doubt (E2, M7).
- **Message**: The file's text must match its source character for character, apart from the specification's apparatus.
- **Fix Action**: Restore the source's characters in the file and re-run the check; use `--allow-deletion` only for material outside the work, and list each one in the report.
- **Applies To**:
    - */*.md

---

## File Boundaries

- **Id**: corpus-file-boundaries
- **Severity**: warning
- **Type**: schema
- **Pattern**: A source file over 2,000 lines whose work has its own volumes or parts, or a file holding more than one source (B9, N7). The validator reports length.
- **Message**: One file holds one source, split only at the work's own volumes or parts.
- **Fix Action**: Split at the printed volumes or parts with `vol. N` or `pt. N` keys, each with its own year.
- **Applies To**:
    - */*.md

---

## Run Report Completeness

- **Id**: corpus-report-complete
- **Severity**: error
- **Type**: semantic
- **Pattern**: A final report that omits any input from the extraction manifest, any column of the Verbose Run Report pattern, any user correction, any allowed deletion, or the statement that changes are uncommitted.
- **Message**: The run report must account for every input and every judgment the user did not see in review.
- **Fix Action**: Rebuild the report from the manifest and the per-source drafts, adding the missing rows and sections.
- **Applies To**:
    - run report
