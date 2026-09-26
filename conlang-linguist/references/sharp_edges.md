# Sharp Edges

This document defines the sharp edges used by conlang-linguist.

---

## Silent Regularity Break

- **Id**: silent-regularity-break
- **Summary**: A daughter form is written or "corrected" by hand, so it no longer follows from its etymon through the cascade.
- **Severity**: critical
- **Situation**: While writing a paradigm table or a corpus sentence, the agent types a surface form it expects, or tweaks a compiled form that "looks wrong," instead of changing the etymon, a law, or an event.
- **Why**: Exceptionless regularity is the skill's core guarantee. A hand-written form is an exception with no cause, and it will disagree with the next recompile.
- **Solution**:
    - Write only etyma, laws, and events; obtain every surface form from `soundchange.py compile` or `trace`.
    - If a compiled form seems wrong, diagnose which input is wrong (conditioning, ordering, etymon, or a missing event) and fix that input.
- **Symptoms**:
    - A form in `<Language> Grammar.md` or `<Language> Syntax.md` differs from the same entry in `<Language> Compiled Lexicon.md`.
    - `<Language> Corpus.md` contains words not written as `{entry-id}`.
    - `<Language> Compiled *.md` files have edits that aren't in the inputs.
- **Detection Pattern**: Daughter-stage words appearing in section prose, paradigm tables, or corpus files that aren't quoted from compiled output or trace results, or <Language> Compiled *.md files that were modified other than by the engine.

---

## Cascade–Prose Drift

- **Id**: cascade-prose-drift
- **Summary**: The philological statement of a law in `<Language> Phonology.md` and its engine form in `<Language> Cascade.md` disagree in target, environment, or order.
- **Severity**: high
- **Situation**: A law is revised in one file and not the other, or the prose describes a conditioning ("before front vowels") that the engine rule doesn't encode (`_{e i}` omitting `ɛ`).
- **Why**: Readers trust the prose, but the engine produces the forms. When the two diverge, the explanation no longer accounts for the data.
- **Solution**:
    - Edit both files together whenever a law changes, using the same ID in each.
    - Run `check`, which warns about any cascade ID missing from `<Language> Phonology.md`.
    - Reread the prose environment against the engine class membership after every revision.
- **Symptoms**:
    - A `check` warning that a rule isn't documented.
    - Trace output showing a law applying where the prose says it shouldn't.
- **Detection Pattern**: A sound law whose prose statement names a different target, output, environment, or chronological position than the cascade rule with the same ID.

---

## Loan Undergoing Earlier Laws

- **Id**: loan-undergoes-earlier-laws
- **Summary**: A borrowed word is entered at stage 0, so it undergoes sound changes that were already complete before the contact happened.
- **Severity**: high
- **Situation**: A Norse or Norman loan is added with `entry_stage` 0 (or left at the default), and palatalization or lenition from centuries before the contact applies to it.
- **Why**: Stratification is chronological evidence. A loan that shows pre-contact changes implies contact at an impossible date.
- **Solution**:
    - Give every non-inherited entry the entry stage matching its contact period in `<Language> Premise.md`.
    - Enter the etymon in the recipient's phonology at that stage, with the adaptation explained in `notes`.
- **Symptoms**:
    - Loans showing the same reflexes as inherited words for laws that predate contact.
    - Anachronistic dates implied by the lexicon's strata.
- **Detection Pattern**: Lexicon rows with a stratum other than inherited whose entry stage precedes the period that <Language> Premise.md assigns to the donor contact.

---

## Ordering Interaction Missed

- **Id**: ordering-interaction-missed
- **Summary**: A law is added or reordered without checking how it feeds or bleeds its neighbors, producing outcomes the prose chronology doesn't predict.
- **Severity**: high
- **Situation**: Syncope is placed before palatalization without noticing that it creates new velar-plus-front-vowel sequences, or removes them.
- **Why**: Relative chronology is the explanatory core of a cascade. Unexamined interactions produce reflexes the agent then can't justify.
- **Solution**:
    - Before inserting or moving a law, use `apply` to test representative forms at both positions.
    - State the resulting feeding, bleeding, counterfeeding, or counterbleeding relationship in `<Language> Phonology.md`.
- **Symptoms**:
    - `compile` reports many unexpected changed forms after a small edit.
    - Trace output shows a law applying to inputs created or destroyed by a neighbor the prose doesn't mention.
- **Detection Pattern**: A newly inserted or moved law whose <Language> Phonology.md entry doesn't state its chronological relationship to the laws immediately around it.

---

## Hallucinated Comparanda

- **Id**: hallucinated-comparanda
- **Summary**: An attested-looking parallel is cited with a wrong form, a wrong meaning, or a development that didn't happen.
- **Severity**: critical
- **Situation**: To support a law, the agent cites a Romance, Germanic, or Semitic reflex from memory, and it is misspelled, misglossed, or invented.
- **Why**: The user is a specialist. One false comparandum undermines trust in every correct claim near it.
- **Solution**:
    - Prefer the textbook-canonical examples of a change, which are the ones most reliably recalled.
    - Mark any form you aren't sure of `[verify]`, and cite by language and form alone.
- **Symptoms**:
    - Forms with implausible spellings for their language, or a gloss that doesn't fit the etymology.
    - Citations formatted as bibliography.
- **Detection Pattern**: Cited attested forms that are neither canonical textbook examples nor marked for verification, or any author–year or page reference in skill output.

---

## Symmetry Creep

- **Id**: symmetry-creep
- **Summary**: Output drifts toward balanced inventories, full paradigms, and one-to-one form–function mappings.
- **Severity**: high
- **Situation**: When designing stage-0 morphology or summarizing a paradigm, the agent fills every cell uniquely, or gives each vowel a matching long counterpart and each stop a voiced pair.
- **Why**: A language model's defaults favor neat patterns. Natural systems show gaps, mergers, and uneven functional load.
- **Solution**:
    - Take stage 0 from an attested or carefully reconstructed ancestor with its own irregularities.
    - Let the cascade generate syncretism, and flag any paradigm with zero syncretism or suppletion for review.
- **Symptoms**:
    - Paradigm tables with no repeated forms.
    - Inventories that fill every cell of a place-and-manner grid.
- **Detection Pattern**: A paradigm, inventory, or numeral system with no gaps, syncretism, suppletion, or irregular members, when no auxiliary-language premise justifies it.

---

## Fantasy Frame Leakage

- **Id**: fantasy-frame-leakage
- **Summary**: Lore, fictional peoples, or aesthetic briefs survive the reframe and begin shaping decisions.
- **Severity**: medium
- **Situation**: After a request for "an elvish tongue," later laws are justified as "fitting the elves' grace," or vocabulary fields follow a fantasy setting.
- **Why**: Once a non-historical frame drives choices, derivations stop being explanatory.
- **Solution**:
    - Record the reframed terrestrial premise in `<Language> Premise.md`, and cite only it.
    - When the user reintroduces lore, restate the counterfactual again briefly and continue.
- **Symptoms**:
    - Justifications that mention characters, races, magic, or how the language should feel.
- **Detection Pattern**: Section prose or law justifications that refer to fictional peoples, magic, invented worlds, or intended aesthetic effect instead of phonetic, social, or historical causes.

---

## Stale Compile

- **Id**: stale-compile
- **Summary**: The inputs change but `compile` isn't run, so the section prose quotes forms from a superseded cascade.
- **Severity**: high
- **Situation**: The agent edits `<Language> Cascade.md` or `<Language> Lexicon.md`, then writes grammar prose from memory of the earlier output.
- **Why**: Consistency across sessions depends on every quoted form coming from the current compile.
- **Solution**:
    - Compile immediately after any edit to cascade, lexicon, events, or corpus, and before writing prose that quotes forms.
    - When a compile reports changes, write the errata entry before anything else.
- **Symptoms**:
    - `<Language> Compiled Changes.md` exists but has no matching errata entry.
    - Quoted forms that `trace` doesn't reproduce.
- **Detection Pattern**: Edits to <Language> Cascade.md, <Language> Lexicon.md, <Language> Events.md, or <Language> Corpus.md that aren't followed in the same turn by a compile run and, when forms changed, an errata entry.

---

## Large Lexicon Context Flood

- **Id**: large-lexicon-context-flood
- **Summary**: The whole lexicon or compiled lexicon is read into context at advanced depth and above, crowding out the instructions.
- **Severity**: medium
- **Situation**: With 8,000 or more entries, the agent reads all of `<Language> Lexicon.md` or `<Language> Compiled Lexicon.md` to find a few words.
- **Why**: Large dumps dilute attention and make the agent lose the rigor constraints.
- **Solution**:
    - Search for specific IDs, glosses, or strata instead of reading whole files.
    - Use `trace` for specific entries and `check` for global consistency.
- **Symptoms**:
    - Very long tool outputs of table rows.
    - Later responses dropping notation or comparanda discipline.
- **Detection Pattern**: Whole-file reads of <Language> Lexicon.md or <Language> Compiled Lexicon.md when the workspace holds more than about a thousand entries.

---

## Unannounced Workspace Rewrite

- **Id**: unannounced-workspace-rewrite
- **Summary**: A workspace is created, or a law is revised, without telling the user which files will change.
- **Severity**: medium
- **Situation**: During a critique the agent decides a law is misordered and rewrites the cascade and recompiles in the same step.
- **Why**: A revision can change thousands of forms. The user must be able to predict and approve that before it happens.
- **Solution**:
    - Propose the revision, with a sample of the forms `apply` shows will move, and wait for confirmation.
    - After confirmation, edit, compile, and log in errata.
- **Symptoms**:
    - Errata entries the user didn't approve.
    - Surprise at changed forms in later sessions.
- **Detection Pattern**: Edits to <Language> Cascade.md, <Language> Events.md, <Language> Premise.md, or etyma, or creation of a new workspace folder, without a preceding message that names the change and receives the user's approval.
