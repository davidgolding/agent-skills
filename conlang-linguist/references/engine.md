# Sound-Change Engine

This document defines the input notation and commands of `scripts/soundchange.py`, the engine that compiles every surface form in a conlang-linguist workspace. Run it with `python3` from the skill directory, passing the workspace path.

Every file the engine reads or writes is Markdown, and all of them sit directly in the language folder with no subfolders. The engine reads `<Language> Cascade.md`, `<Language> Lexicon.md`, `<Language> Events.md`, and `<Language> Corpus.md`, and writes `<Language> Compiled Lexicon.md`, `<Language> Compiled Corpus.md`, and `<Language> Compiled Changes.md` beside them. `<Language>` is the language's full name in Title Case (see `references/workspace.md`). The engine reads it from the folder's one `<Language> Cascade.md` and uses it as the prefix for every other file. `check` warns about any subfolder, any non-Markdown file, or any Markdown file lacking that prefix, and it refuses to run if the folder has zero or several Cascade files, or if the name contains a character Obsidian can't use in file names.

---

## Commands

| Command | Purpose |
|---|---|
| `check <ws>` | Parse and validate the cascade, lexicon, events, and corpus references. Warns when a rule ID is not documented in `<Language> Phonology.md`. |
| `compile <ws>` | Rewrite `<Language> Compiled Lexicon.md` and `<Language> Compiled Corpus.md`. Reports every form that differs from the previous `<Language> Compiled Lexicon.md` and writes that list to `<Language> Compiled Changes.md` for the errata entry. A compile with no changes deletes `<Language> Compiled Changes.md`, so write the errata entry before compiling again. |
| `trace <ws> <id>...` | Print the derivation of each entry, step by step, showing only the rules and events that changed the form. Use it to show work in a response. |
| `apply <ws> <form> [--from N]` | Run a form not in the lexicon through the cascade, entering at stage N. Use it to test a hypothesis or a user's proposed etymon before committing it. |

Every command validates first and refuses to run on errors. A nonzero exit means the inputs are inconsistent: fix the inputs and leave the `<Language> Compiled *.md` files to the next compile.

---

## `<Language> Cascade.md`

The engine reads only the lines inside fenced code blocks tagged `cascade`, in file order. Everything outside them is ordinary Markdown: stage headings, notes, and cross-references to `<Language> Phonology.md`. A cascade can be split across several blocks, and the blocks are concatenated. Inside a block there is one directive per line. A line whose first non-blank character is `#` is a comment, and ` ;` begins a trailing comment.

````markdown
## Stage 1: Early British Romance

```cascade
segments: tʃ dʒ kʷ gʷ          ; multigraphs to treat as one segment
class V: a e i o u aː eː iː oː uː
class P: p t k
class B: b d g
stage 0: Late Latin (c. 300)
stage 1: Early British Romance (c. 400–600)
L1: m > ∅ / V_#                ; loss of final -m
L2: P > B / V_V                ; intervocalic lenition
L3: k > tʃ / _{e i} ! #_       ; palatalization, not word-initially
stage 2: Medieval British Romance (c. 600–1100)
L4: {e o} > ∅ / VC_CV          ; syncope of pretonic mid vowels
L5: ∅ > e / #_s{p t k}         ; prothesis
```
````

**Segments.** The tokenizer takes declared multigraphs (and class members) longest-first. Combining diacritics, `ː`, `ʰ`, `ʷ`, `ʲ`, and similar modifiers attach to the preceding segment automatically, and a tie bar (`t͡s`) joins the next character. Declare an affricate or labiovelar written without a tie bar under `segments:`.

**Classes.** A single ASCII capital letter. Member order matters: in `P > B`, the nth member of P becomes the nth member of B.

**Stages.** `stage N: name (date)` with N increasing. Stage 0 is the ancestor and normally has no rules. Every rule belongs to the most recent stage line above it, even across blocks. Lexicon entries entering at stage N undergo that stage's rules and all later ones.

**Rules.** `ID: target > replacement / environment ! exception`.
- The ID is a letter followed by letters, digits, `.`, or `-`, and must be unique. The same ID labels the law in `<Language> Phonology.md`.
- The target and replacement are sequences of segments, `{sets}`, and classes. `∅` (or `0`) is empty: `∅ > e` inserts, `m > ∅` deletes. A literal sequence performs metathesis (`ar > ra`).
- The environment has exactly one `_`. `#` is a word boundary. `(X)` marks an optional element. Commas separate alternative environments (`V_V , _#`).
- `! env` lists environments where the rule is blocked. Use it sparingly and state the phonological reason in `<Language> Phonology.md`.

**Application.** Each rule applies once, simultaneously, left to right, and every environment is read against the rule's input form. The cascade's order is the relative chronology. Feeding, bleeding, counterfeeding, and counterbleeding all follow from where a rule sits in the file.

**Limitations.** There is no feature arithmetic, no iterative or right-to-left application, and no separate suprasegmental tier. Mark stress or tone as a segment (`ˈ`, or a vowel diacritic), place it in the etymon, and let rules refer to it. For a process that needs iteration (e.g., vowel harmony spreading across several syllables), write one rule per step and justify the steps in `<Language> Phonology.md`.

---

## `<Language> Lexicon.md`

A Markdown file of one or more tables with the columns below. Header names are matched case-insensitively, and a space reads as an underscore, so `Entry stage` matches `entry_stage`. Rows with an empty `id` are skipped. Split the lexicon into several tables under `##` headings (by semantic field or stratum) to keep it readable. The engine reads every table whose header has the required columns and ignores other tables. A cell may be wrapped in backticks (`` `*kentum` ``) to keep Markdown from styling it. Write a literal pipe as `\|`.

```markdown
## Numerals

| ID | Gloss | Etymon | Stratum | Entry stage | Source | Notes |
|---|---|---|---|---|---|---|
| centum | hundred | `*kentum` | inherited | 0 | | |
| wik | inlet | wiːk | loan | 2 | Old Norse vík 'bay' | via trade |
```

| Column | Content |
|---|---|
| `id` | Unique, stable key. Corpus texts and events refer to it. Use a transparent Latin-letter key (`centum`, `ed-1sg`), not the surface form, because surface forms change on recompile. |
| `gloss` | Meaning, ideally with the semantic history if it has shifted. |
| `etymon` | The form as it stood at `entry_stage`, in the cascade's segments. A leading `*` is allowed and ignored. |
| `stratum` | `inherited`, `loan`, `coinage` (an internal derivation made at a later stage), or another stratum label the grammar defines (`learned`, `substrate`). |
| `entry_stage` | The stage the form enters at: 0 for inherited words, the stage of borrowing or coinage otherwise. |
| `source` | Required unless inherited. The donor language and donor form, e.g., `Old English *wīc`, or `internal: *X + *-Y`. |
| `notes` | Optional. Loan adaptation reasoning, dialect distribution, register. |

**Paradigm cells are entries.** Inherited inflected forms descend as wholes: `ed-1sg`, `ed-2sg`, and `ed-3sg` each carry their own proto-form. That's what lets sound change produce syncretism and opaque alternations naturally. Leveled or suppletive cells are then recorded as events.

---

## `<Language> Events.md`

One or more Markdown tables with the columns below, following the same table rules as `<Language> Lexicon.md`. Each row is a dated irregularity. At the stated point, the event replaces an entry's current form.

| Column | Content |
|---|---|
| `id` | Unique, e.g., `E12`. |
| `entry` | The lexicon `id` affected. |
| `after` | A rule ID (the event takes effect immediately after that rule) or `stage:N` (at the start of stage N, before its first rule). It cannot precede the entry's `entry_stage`. |
| `form` | The new form, in the segments current at that point. Later rules then apply to it. |
| `type` | One of: `analogy`, `suppletion`, `learned`, `semi-learned`, `taboo`, `spelling-pronunciation`, `dialect-borrowing`, `contamination`, `back-formation`, `other`. |
| `motivation` | Required. The model and proportion for an analogy (e.g., `3sg *ama- : 1sg *amo :: 3sg *ride- : 1sg X`), the source dialect, the taboo, or the prestige register. |

---

## `<Language> Corpus.md`

One Markdown file holding every text. Each text is a `##` section, headed with its title, followed by its genre, date, register, and stage. Write each word as `{entry-id}`. Everything else (headings, punctuation, glossing lines, notes) passes through unchanged into `<Language> Compiled Corpus.md`, with each reference replaced by its compiled form. Word order and particles come from `<Language> Syntax.md` and `<Language> Pragmatics.md`, and each inflected word must reference the paradigm-cell entry for its form. A word the lexicon lacks must be added to it (with its etymon) before the text can use it.

---

## Compiled files

| File | Content |
|---|---|
| `<Language> Compiled Lexicon.md` | A table of ID, Surface, Gloss, Etymon, Stratum (with source), Entry stage, and Events for every entry. The next compile diffs against this file. |
| `<Language> Compiled Corpus.md` | `<Language> Corpus.md` with every `{entry-id}` replaced by its surface form. |
| `<Language> Compiled Changes.md` | A table of ID, Old, and New for the forms the last compile changed. Present only when that compile changed something. |

Each starts with a notice saying it is generated. Only the engine writes these files.
