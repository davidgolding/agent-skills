# Language Workspace

This document defines the layout of a conlang-linguist workspace, what each of the eight sections contains, the quantitative depth targets, and the errata format.

---

## Location

Each language variety has one workspace folder. By default it goes at `languages/<variety-slug>/` under the current working directory. Use a location the user names instead when they give one. Before creating a new workspace, state its path and the files that will be created, and wait for the user's confirmation.

Every file in a language folder is Markdown, and the folder has no subfolders. That keeps the whole language readable in any Markdown viewer, and a single directory listing shows all of it.

## File names

A project can hold several languages, and editors like Obsidian index files by name across the whole project, not per folder. So every workspace file is named `<Language> <Section>.md`: the language's full name in Title Case, a space, then the section name in Title Case. For "Archaic Lithic-Brittonic," the corpus is `Archaic Lithic-Brittonic Corpus.md` and the compiled lexicon is `Archaic Lithic-Brittonic Compiled Lexicon.md`. That makes every file name unique across the project and lets `[[Archaic Lithic-Brittonic Phonology]]` resolve unambiguously as an Obsidian link.

- **Choosing the name.** Settle the language name with the user when the workspace is created, and record it in `<Language> Premise.md`. Use the characters valid in file names on every platform and in Obsidian, which excludes `# ^ [ ] | \ / : * ? " < >`.
- **Detecting the name.** The engine reads the language name from the folder's one `<Language> Cascade.md`, and uses that prefix for every file it reads or writes. `check` warns about any Markdown file in the folder that lacks the prefix.
- **Renaming a language.** A rename changes every file name in the workspace. Treat it as a revision: propose it, get confirmation, rename every file together, and log it in errata. In Obsidian, renaming through the editor also updates links to the files.
- **Naming the folder.** The folder name is free, since uniqueness comes from the file names. The default is a lowercase slug of the language name, e.g., `languages/archaic-lithic-brittonic/`.

```
languages/<variety-slug>/
├── <Language> Premise.md             counterfactual scenario, ancestor, timeline, contact map
├── <Language> Phonology.md           section: inventories per stage, every law, chronology
├── <Language> Grammar.md             section: morphology and morphophonology, with history
├── <Language> Syntax.md              section: word order, alignment, clause structure, history
├── <Language> Pragmatics.md          section: register, politeness, discourse, deixis
├── <Language> Number System.md       section: numerals, counting base, number agreement
├── <Language> Lexicon.md             section: etyma, strata, entry stages (engine input)
├── <Language> Corpus.md              section: texts composed from lexicon IDs (engine input)
├── <Language> Errata.md              section: dated revision log
├── <Language> Cascade.md             ordered sound laws in fenced cascade blocks (engine input)
├── <Language> Events.md              irregularity events (engine input)
├── <Language> Compiled Lexicon.md    compiled output; written only by the engine
├── <Language> Compiled Corpus.md     compiled output; written only by the engine
└── <Language> Compiled Changes.md    forms changed by the last compile; written only by the engine
```

Keep every file in a language folder a top-level Markdown file, including scratch notes, exports, and per-text or per-field material. When a section grows large, split it into `##` subsections or several tables within its one file.

`<Language> Premise.md` isn't a section. It is the frame every section answers to: the ancestor (attested or reconstructed), the point of divergence, dated stages, geography, and the substrata, superstrata, and adstrata along with when each contact occurred. Write it first. Every later decision cites it.

---

## Section contents

| Section | Contents | Counted unit |
|---|---|---|
| Phonology | Phoneme inventory at each stage. Every law stated in philological notation with its cascade ID, its conditioning, and its comparative parallel. The relative chronology, with the evidence for each ordering. Accent history. Sandhi. Residues and exceptions (each tied to an event). | Laws and phenomena, each with worked derivations |
| Grammar | Inflectional and derivational morphology traced from the ancestor: ablaut, umlaut, and other morphophonemic alternations that sound change produced. Syncretism, suppletion, and leveling, with their events. Paradigm tables generated from the compiled lexicon. | Phenomena, each with a derivation |
| Syntax | Word order and its drift. Alignment, including any splits. Clause linkage and grammaticalization chains (e.g., a demonstrative becoming an article, a verb becoming an auxiliary, a postposition becoming a case marker), with the stages of each. | Phenomena, each with glossed examples |
| Pragmatics | Registers (liturgical, legal, colloquial) and the archaisms each preserves. Politeness and address systems. Discourse particles and their sources. Deixis. | Phenomena, each with examples |
| Number system | Numerals and their etymologies. Counting base, along with any substrate base (vigesimal residues, for example). Ordinals. Number agreement. Irregular teens and decades. | Numerals and phenomena, each derived |
| Lexicon | Entries in the tables of `<Language> Lexicon.md`, compiled into `<Language> Compiled Lexicon.md`. Coverage priorities, from first to last: Swadesh-type core vocabulary, then culturally central fields of the premise, then derivational families. | Entries |
| Corpus | Texts in `<Language> Corpus.md`, one `##` section each, headed with its genre, date, register, and the stage it represents, and compiled into `<Language> Compiled Corpus.md`. Include interlinear glossing for the first texts at each depth. | Texts |
| Errata | A log of every revision. It has no depth level and grows with the work. | — |

In the prose sections, a "worked" item has a stated historical source, at least one derivation or glossed example, and an attested comparative parallel. An item without all three doesn't count toward a depth target.

---

## Depth targets

A section's level is met when its counted units reach the target and every earlier level's coverage is also present. Levels are cumulative.

| Level | Lexicon entries | Corpus texts | Other sections (worked phenomena) |
|---|---|---|---|
| starter | 200 | 3 | 10 |
| essentials | 1,000 | 10 | 25 |
| intermediate | 3,000 | 25 | 50 |
| advanced | 8,000 | 60 | 100 |
| native | 20,000 | 150 | 200 |
| complete | exhaustive | exhaustive | exhaustive |

"Complete" means no productive pattern, attested register, or lexical field the premise implies is left undocumented. When a requested level exceeds what one response can hold, build toward it in batches. Report progress as current count / target and say what the next batch will add.

---

## Errata format

Every revision to a law, a stage, an event, the premise, or an entry's etymon gets one entry, newest first:

```markdown
## 2026-09-25 — Palatalization moved before syncope

- **Changed:** L3 (k > tʃ / _{e i}) now precedes L4 (syncope); formerly followed it.
- **Why:** Velars that stood before a front vowel later lost to syncope show affricate reflexes, so palatalization must have applied first (parallel: Lat. *duodecim* > Fr. *douze*, where the velar palatalized before the syncopated *e*).
- **Forms changed (37):** see list below, from <Language> Compiled Changes.md.
  - dodeke: dodke → dodtʃe
  - …
```

Write the entry before compiling again, since a compile with no changes deletes `<Language> Compiled Changes.md`. Paste the full list from `<Language> Compiled Changes.md` when it has 50 or fewer rows. Beyond that, give the count and a representative sample of 20.
