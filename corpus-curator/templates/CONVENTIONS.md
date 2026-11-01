# Corpus Conventions

This corpus follows the Markdown Source Corpus Specification (David Golding, October 2026, https://davidgolding.com/corpus-spec). Read this file before reading any source. Rule IDs refer to the spec.

## Layout

- The root holds only this file, `Assets/`, and flat collection folders (D1, D2).
- One source per file, directly inside exactly one collection. The folder records membership only; it is not part of a source's identity (D7).
- `Assets/` holds page images, audio and video as `{key} {label}.{ext}`, such as `Hyde - Letter to Joseph Smith (1841 Apr 17) p2.jpg` (D5).

## Keys

- A file's name minus `.md` is its key: `{Author} - {Short Title} ({Date})`. With no known author, the author and ` - ` are omitted (N1).
- Keys are unique across the whole corpus, compared after NFC normalization and case folding (D6). A key never changes once issued.
- Dates use `Y M j`: `1832`, `1832 Feb`, `1832 Feb 16`; year ranges use an en dash, `1839–1843` (N5).
- A second source with the same key takes `b`, then `c` to `z`, then `aa` to `zz`, in order of entry (N6). Split works use `vol. N` or `pt. N` (N7).
- Author and title use Latin letters, digits, spaces and `' , . & -` only; the apostrophe is U+0027 (N8).

## Frontmatter

Flat YAML, one `key: value` per line, in this order: `title`, `author`, `date`, `source`, `type`, `lang`, `mode`, `hands`, `resp`. Unused optional keys are omitted (F1, F2).

- `date` is EDTF: `1832-02-16`, `1832-06`, `1840~` (approximate), `1840?` (uncertain), `184X`, `1839/1843`. Read it as a string (F3).
- `mode` is `diplomatic` (one source line per file line) or `prose` (one paragraph per file line).
- `hands` labels the hands named in marks: `h1 Hyde; h2 later pencil annotator`.
- `resp` says who transcribed, when, and how the text was checked.

## Types

`book`, `chapter`, `article`, `newspaper`, `letter`, `diary`, `minutes`, `record`, `legal`, `manuscript`, `transcript`, `inscription`

## Body

- One file line is one citable unit; text is never hard-wrapped (B1). One blank line marks a structural break (B3).
- `@p12`, `@f4r`, `@col2`, `@t00:14:05` on their own lines mark pages, folios, columns and times (B2).
- `#` headings appear only where the source prints them (B4). Speakers are bold as printed: `**Ham.**` (B5).
- Source notes are `[^1]`, editorial notes `[^e1]`, variants `[^a1]: lemma] reading B`. All definitions follow one `@notes` line at the end (B7).
- Cross-references `[[key]]` or `[[key]]:line` appear only in editorial notes.
- Cite as `{key}:{line}` or `{key}:{start}-{end}` with the exact quoted words (B8).

## Transcription Marks

Square brackets are the editor; curly braces are a hand in the source. The first character is the operator (M1).

| Mark | Meaning |
| --- | --- |
| `[abc]`, `[abc?]` | text lost, supplied by the editor (low certainty with `?`) |
| `[.3]`, `[.?]` | gap of 3 characters, or of unknown extent |
| `[?abc]`, `[?.3]` | unclear reading; illegible characters |
| `[_3]` | blank space left by the scribe |
| `[+abc]`, `[-abc]` | omitted by the scribe and supplied; surplus |
| `[!sic>corr]`, `[!abc]` | source error with correction; source error alone |
| `[=figure: description]` | editorial description |
| `a(bc)`, `a(---)` | abbreviation expanded; unresolved |
| `{+abc}`, `{+abc@h2 above}` | addition, with hand and place |
| `{-abc}`, `{-abc@erasure}` | deletion; erasure |
| `{-old+new}` | substitution |
| `{abc@sc}`, `{abc@la}` | rendition; foreign language |
| `{@h2}` | change of hand |
| `\|` | line break inside a prose-mode paragraph |

- An editorial mark may sit inside a source-hand mark; no other nesting (M3). No mark crosses a line end (M4).
- Literal `[ ] { } | \` and a line-opening `#` or `@` are backslash-escaped (M5).
- Search view: apply the reading of each mark, remove escapes, join split words. It is computed, never stored (M6).

## Encoding

UTF-8 without BOM, LF endings, a final newline, no trailing whitespace, NFC throughout (E1). Source characters are kept exactly (E2). No HTML, XML or JSON in source files (E4). Lines never begin with whitespace (E5).
