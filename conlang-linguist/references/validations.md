# Validations

This document defines the validations used by conlang-linguist.

---

## Engine Check Passes

- **Id**: engine-check-passes
- **Severity**: error
- **Type**: semantic
- **Pattern**: Run `python3 scripts/soundchange.py check <workspace>`; it must exit 0 with no errors.
- **Message**: Workspace inputs are inconsistent (unparseable rule, unknown class, event with no motivation, loan with no source, dangling corpus reference, or an event before its entry stage)
- **Fix Action**: Correct the named input file and line, rerun check, then compile
- **Applies To**:
    - <Language> Cascade.md
    - <Language> Lexicon.md
    - <Language> Events.md
    - <Language> Corpus.md

---

## Every Law Documented

- **Id**: every-law-documented
- **Severity**: error
- **Type**: semantic
- **Pattern**: Every rule ID in `<Language> Cascade.md` appears in `<Language> Phonology.md` with a philological statement, its conditioning, its chronological relationship to neighboring laws, and at least one attested parallel.
- **Message**: A sound law exists in the engine without a philological justification
- **Fix Action**: Add the law to <Language> Phonology.md under the same ID, with its environment, chronology, and a comparandum
- **Applies To**:
    - <Language> Phonology.md
    - <Language> Cascade.md

---

## Compiled Forms Only

- **Id**: compiled-forms-only
- **Severity**: error
- **Type**: semantic
- **Pattern**: Every daughter-stage form quoted in section prose, paradigm tables, or responses matches the current `<Language> Compiled Lexicon.md` or `trace` output.
- **Message**: A surface form was written by hand and doesn't follow from the cascade
- **Fix Action**: Replace it with the compiled form, or change the etymon, law, or event that should produce the intended form, and recompile
- **Applies To**:
    - <Language> Grammar.md
    - <Language> Syntax.md
    - <Language> Pragmatics.md
    - <Language> Number System.md
    - <Language> Phonology.md

---

## Errata After Changed Forms

- **Id**: errata-after-changed-forms
- **Severity**: error
- **Type**: semantic
- **Pattern**: When a compile reports changed forms (`<Language> Compiled Changes.md` exists), `<Language> Errata.md` has a dated entry for that revision with the changed state, the reason, and the changed forms.
- **Message**: The cascade or lexicon changed without an errata record
- **Fix Action**: Write the errata entry using the format in references/workspace.md, drawing the form list from <Language> Compiled Changes.md, before compiling again
- **Applies To**:
    - <Language> Errata.md

---

## Compiled Files Untouched

- **Id**: compiled-files-untouched
- **Severity**: error
- **Type**: semantic
- **Pattern**: `<Language> Compiled *.md` files are written only by `soundchange.py compile`.
- **Message**: Compiled output was edited by hand and will be overwritten or contradicted on the next compile
- **Fix Action**: Discard the manual edit, make the change in the engine inputs, and recompile
- **Applies To**:
    - <Language> Compiled *.md

---

## Bibliographic Citation

- **Id**: bibliographic-citation
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \b[A-Z][a-z]+(?: (?:&|and) [A-Z][a-z]+)?,? \(?(?:1[6-9]|20)\d{2}[a-z]?\)?(?::\s?\d+)?
    - \bpp?\.\s?\d+
    - \bet al\.
- **Message**: Bibliographic reference found; the skill cites attested forms only, so every citation can be checked against the form itself
- **Fix Action**: Remove the reference and support the claim with attested comparanda by language and form, marking any uncertain form [verify]
- **Applies To**:
    - languages/*/*.md

---

## Teleological Justification

- **Id**: teleological-justification
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\bto (?:make it |make the language )?(?:sound|feel|look) (?:more )?\w+
    - (?i)\b(?:for|because of) (?:aesthetic|euphon\w*|elegance|beauty|flavou?r)\b
    - (?i)\bsounds? (?:more )?(?:elegant|beautiful|harsh|exotic|alien|elvish|ancient|cool)\b
- **Message**: A change is justified by its intended sound or aesthetic effect instead of a phonetic, social, or historical cause
- **Fix Action**: Restate the motivation as articulatory, perceptual, or contact-driven, with an attested parallel
- **Applies To**:
    - languages/*/*.md

---

## Hobbyist and Fantasy Vocabulary

- **Id**: hobbyist-fantasy-vocabulary
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:conworld\w*|conculture|conlanger\w*|kitchen[- ]sink|clong|word generator|naturalistic enough)\b
    - (?i)\b(?:elv(?:en|ish)|dwar(?:f|v)(?:en|ish)|orc(?:ish)?|magic system|spell(?:casting|craft)|fantasy race|world-?building)\b
- **Message**: Hobbyist conlang idiom or fantasy scaffolding appears in the workspace
- **Fix Action**: Replace it with historical-linguistics terminology, and restate any fantasy frame as the terrestrial counterfactual recorded in <Language> Premise.md
- **Applies To**:
    - languages/*/*.md

---

## Unmarked Uncertain Comparanda

- **Id**: unmarked-uncertain-comparanda
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Every cited attested form is either a canonical, textbook example of the development or carries a `[verify]` marker.
- **Message**: An attested parallel is asserted without the confidence to stand behind it
- **Fix Action**: Replace it with a canonical example, or append [verify] to the form
- **Applies To**:
    - languages/*/*.md

---

## Loan Entry Stage Consistent

- **Id**: loan-entry-stage-consistent
- **Severity**: error
- **Type**: semantic
- **Pattern**: Every lexicon row whose stratum is not `inherited` has an entry stage within the contact period that <Language> Premise.md assigns to its donor language, and a donor form appropriate to that date.
- **Message**: A loan's entry stage or donor form is anachronistic for the recorded contact history
- **Fix Action**: Correct the entry stage or donor form, or amend <Language> Premise.md (with an errata entry) if the contact history itself was wrong
- **Applies To**:
    - <Language> Lexicon.md
    - <Language> Premise.md

---

## Depth Target Met

- **Id**: depth-target-met
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A section reported as reaching a depth level meets the count in references/workspace.md, counting only items with a historical source, a worked derivation or example, and an attested parallel.
- **Message**: The section is reported at a depth level it doesn't meet with worked items
- **Fix Action**: Report the honest count against the target and continue in batches until it is met
- **Applies To**:
    - languages/*/*.md

---

## Flat Markdown Language Folder

- **Id**: flat-markdown-language-folder
- **Severity**: error
- **Type**: semantic
- **Pattern**: A language folder contains only `.md` files, no subfolders, and every file is named `<Language> <Section>.md` with the same Title Case language prefix; `soundchange.py check` reports no subfolder, non-Markdown, or missing-prefix warnings.
- **Message**: The language folder has a subfolder, a non-Markdown file, or a file name that isn't unique across the project
- **Fix Action**: Fold the content into the matching section file (as a `##` subsection or an additional table) and remove the subfolder or file, or rename the file with the language prefix, with the user's confirmation
- **Applies To**:
    - languages/*/

---

## Absolute Path Detection

- **Id**: absolute-path-detection
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \b/Users/[a-zA-Z0-9_\-\.]+
    - \b/home/[a-zA-Z0-9_\-\.]+
- **Message**: Absolute path detected; workspaces and skill instructions must stay portable
- **Fix Action**: Use paths relative to the working directory or the skill directory
- **Applies To**:
    - *.md
    - *.py
