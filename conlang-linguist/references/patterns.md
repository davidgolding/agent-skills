# Conlang Linguist Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by conlang-linguist.

## Patterns

- **Name**: Premise-First Scenario
- **Description**: Before any derivation, fix the historical frame in `<Language> Premise.md`: the attested or reconstructed ancestor, the point of divergence, dated stages, geography, and each contact language with its period and social relationship (substratum, superstratum, adstratum).
- **When**: Starting a new variety, or when a request implies a historical situation that the premise doesn't yet record.
- **Example**:
```
    Ancestor: Late Latin of Roman Britain (c. 400), as reconstructed from British Latin loans in Welsh.
    Divergence: No Anglo-Saxon settlement east of the Pennines; Romano-British urban elite persists.
    Stages: 0 Late British Latin (c. 400) · 1 Early Britannic Romance (400–650) · 2 Old (650–1050) · 3 Middle (1050–1400)
    Contact: Brittonic substratum (stage 0–1, rural bilingualism); Old Norse adstratum (stage 2, Danelaw-type trade);
             Norman French superstratum (stage 3, administrative and legal registers).
```

---

- **Name**: Ordered Cascade with Stated Chronology
- **Description**: State every sound law with its conditioning, its cascade ID, and the evidence for where it falls in the relative chronology (feeding, bleeding, counterfeeding, or counterbleeding with its neighbors), plus one attested parallel.
- **When**: Writing or extending `<Language> Phonology.md` and `<Language> Cascade.md`.
- **Example**:
```
    L4. Syncope of unstressed medial vowels: *V > ∅ / VC_CV
        Chronology: after L3 (palatalization), since *dodeke yields dodtʃe, not *dodke.
        Parallel: Lat. duodecim > Fr. douze (velar palatalized before the e that syncope later removed).
        <Language> Cascade.md: L4: {e o} > ∅ / VC_CV
```

---

- **Name**: Etymon-and-Stratum Lexicon
- **Description**: Record each word as an etymon with its stratum, entry stage, and source, leaving the surface form to the engine. The engine produces the surface form, and the stratum records the word's history.
- **When**: Adding any word to the lexicon.
- **Example**:
```
    id        gloss          etymon     stratum    entry_stage  source
    centum    'hundred'      *kentum    inherited  0
    wik       'inlet'        wiːk       loan       2            Old Norse vík 'bay', via trade
    domnell   'little lord'  domnella   coinage    1            internal: *domn- + *-ella
```

---

- **Name**: Irregularity as Dated Event
- **Description**: Enter every departure from regular development as an event tied to a point in the chronology, with its type and a motivation specific enough that another philologist could dispute it.
- **When**: A paradigm levels, a suppletive stem is recruited, a learned form is reintroduced, or a taboo or spelling pronunciation deforms a word.
- **Example**:
```
    E7  ed-2sg  after L9  edes  analogy  Stem vowel leveled from 1sg ed- on the proportion
                                          1sg ed- : 2sg ed-es :: 1sg bib- : 2sg bibes; the regular
                                          outcome *ides would have split the paradigm.
```

---

- **Name**: Paradigm Cells as Inherited Wholes
- **Description**: Enter each inflected form as its own lexicon entry with its own proto-form, and let sound change produce the alternations, syncretisms, and opacity that follow. Leveling is then recorded as an event on specific cells.
- **When**: Building <Language> Grammar.md paradigms or any inflectional morphology.
- **Example**:
```
    Entries: pater-nom *patɛr, pater-acc *patrem, pater-gen *patris
    After loss of final -m and -s and the merger of short i with e, acc and gen fall together as *patre:
    syncretism produced by sound change, not by design.
    <Language> Grammar.md reports the merged cell and cites the laws responsible.
```

---

- **Name**: Compile, Then Explain
- **Description**: Run `soundchange.py compile` after every change to the inputs, then quote `trace` output to show derivations. Explain results from what the engine produced, not from what you expected.
- **When**: Presenting any derived form, paradigm, or text.
- **Example**:
```
    $ python3 scripts/soundchange.py trace languages/britannic-romance centum
    centum 'hundred'
      etymon   kentum
      L1       kentu
      L3       tʃentu
      L8       tʃento
```

---

- **Name**: Re-derive and Log
- **Description**: When a law, ordering, event, or etymon changes, confirm the change with the user, edit the inputs, recompile the whole workspace, and write an errata entry from `<Language> Compiled Changes.md`.
- **When**: Any revision, whether the user asked for it or a critique proposed it.
- **Example**:
```
    1. "Moving L3 before L4 will change forms with velar + syncopated front vowel. Proceed?"
    2. Edit <Language> Cascade.md and <Language> Phonology.md.
    3. compile → "37 forms changed."
    4. <Language> Errata.md: dated entry with old/new ordering, the reason, and the changed forms from <Language> Compiled Changes.md.
```

---

- **Name**: Counterfactual Reframing
- **Description**: Restate a fantasy-, game-, or aesthetics-framed request as a terrestrial counterfactual with a concrete ancestor and contact history. Name what was dropped and why, then proceed.
- **When**: The request mentions fictional peoples, lore, magic, alien physiology, "sounding" a certain way, or game balance.
- **Example**:
```
    Request: "A harsh-sounding language for the mountain dwarves in my novel."
    Reframe: "Taken as a counterfactual: a Kartvelian-type highland variety, with ejectives and dense onset
    clusters inherited from a Caucasian-type areal system, persisting in isolation. I've dropped the
    dwarven frame and the 'harsh' brief. Phonotactics come from inheritance and areal contact, not from a
    target sound, but the result will have the clusters you're picturing, for historical reasons."
```

---

- **Name**: Comparanda by Form
- **Description**: Support each claim with attested forms, giving the language abbreviation, the form in italics, and the meaning where useful. Mark uncertain forms `[verify]`, and give no bibliography.
- **When**: Justifying a law, an ordering, a typological claim, or a critique point.
- **Example**:
```
    Intervocalic voicing of voiceless stops: Lat. vīta > Sp. vida, Lat. lacum > Sp. lago;
    the same process across Gallo-Italic (Lomb. fadiga 'toil' < Lat. *fatīca [verify]).
```

---

- **Name**: Register and Dialect Layering
- **Description**: Model liturgical, legal, and literary registers as conservative strata that preserve older stages or reborrow from them. Model dialects as a continuum defined by isoglosses (laws whose geographic extent differs). Record reborrowed doublets as separate entries with the source register.
- **When**: Writing <Language> Pragmatics.md, building a corpus with more than one genre, or accounting for doublets.
- **Example**:
```
    Doublet: popular tʃoza 'thing' < stage-0 *kausa (inherited, all laws) vs legal kauza 'lawsuit' < liturgical
    *kausa (learned, entry_stage 3), parallel to Fr. chose / cause < Lat. causa.
```

---

- **Name**: Grammaticalization Chains
- **Description**: Derive each grammatical morpheme from a lexical or less grammatical source along an attested pathway, with the intermediate stages dated.
- **When**: Introducing articles, auxiliaries, case markers, tense-aspect affixes, or clitics.
- **Example**:
```
    Future: stage 1 periphrasis *kantare habeo 'I have to sing' > stage 2 enclitic > stage 3 fused suffix -ajo,
    parallel to Fr. chanterai < cantāre habeō.
```

---

- **Name**: Depth Accounting
- **Description**: When building a section to a level, report the count against the target from `references/workspace.md`, count only fully worked items, and say what the next batch will cover.
- **When**: Any request that names a depth level, or any batch toward one.
- **Example**:
```
    Lexicon: 412 / 1,000 (essentials). This batch added 180 entries in kinship, agriculture, and law.
    Next: numerals 11–100 and the Norse trade stratum.
```

---

## Anti-Patterns

- **Name**: Kitchen-Sink Inventory
- **Description**: A phoneme inventory that collects clicks, ejectives, retroflexes, and tones for novelty, with no inheritance or contact to explain them.
- **Why**: Inventories are historical products. Every segment needs a source (inheritance, conditioned split, borrowing) or the variety is not naturalistic.
- **Instead**: Derive each stage's inventory from the previous stage through the cascade, and account for any exotic segment by its origin.

---

- **Name**: Paradigm Symmetry
- **Description**: Perfectly regular conjugations or declensions, balanced 3×3 case-number grids, or vowel systems with no gaps.
- **Why**: Sound change erodes endings unevenly and analogy repairs only some of the damage. Clean systems signal invention, not history.
- **Instead**: Enter paradigm cells as inherited wholes, let the cascade produce the mess, and record only the leveling that has a motivation.

---

- **Name**: Hand-Patched Surface Form
- **Description**: Writing or adjusting a daughter form directly in a lexicon, paradigm, corpus text, or `<Language> Compiled *.md` file instead of changing its etymon, a law, or an event.
- **Why**: It silently breaks exceptionless regularity, and the next recompile erases or contradicts it.
- **Instead**: Change the input that explains the form (etymon, law, or event with a motivation) and recompile.

---

- **Name**: Unconditioned or Unordered Law List
- **Description**: Sound changes listed without environments, or with no stated chronology.
- **Why**: Conditioning and ordering are what make a cascade explanatory. Without them, outcomes are arbitrary and can't be tested.
- **Instead**: Give every law an environment (or state explicitly that it is unconditioned) and a position justified by its interaction with neighboring laws.

---

- **Name**: Teleological Change
- **Description**: Justifying a change by how it sounds ("to make it more elegant," "to sound more ancient") or by a goal the language supposedly pursues.
- **Why**: Sound change has phonetic, articulatory, perceptual, and social causes. Aesthetic intent belongs to the designer, not to the history.
- **Instead**: Give the phonetic motivation (lenition, assimilation, coarticulation) or social motivation (prestige dialect, contact), plus an attested parallel.

---

- **Name**: Lore Scaffolding
- **Description**: Organizing the language around fictional peoples, magic systems, invented religions, or world-building templates.
- **Why**: It replaces historical explanation with narrative convenience and moves the work out of comparative linguistics.
- **Instead**: Reframe as a terrestrial counterfactual (see Counterfactual Reframing) and ground culture-specific vocabulary in an attested cultural context.

---

- **Name**: Fabricated Citation
- **Description**: Author–date references, page numbers, or confidently stated comparanda the agent cannot vouch for.
- **Why**: One invented form or reference discredits the surrounding correct analysis for a specialist reader.
- **Instead**: Cite by attested form only, and mark any doubtful form `[verify]`.

---

- **Name**: Anachronistic Contact
- **Description**: Loans from a language, or with a phonology, that couldn't have been in contact at the entry stage (e.g., Modern English loans at a stage dated to 600, or a Norse loan showing post-Viking-Age sound changes).
- **Why**: A contact stratum dates the stages. An anachronism collapses the relative chronology.
- **Instead**: Check each loan's donor form against the donor language's own history at the entry date, and record the donor form as it stood then.

---

- **Name**: Hobbyist Idiom
- **Description**: The vocabulary and tropes of online conlanging: "conworld," "kitchen sink," "naturalistic enough," "word generator," phonology chosen for how it looks or for game balance.
- **Why**: It signals the design-first frame the skill exists to replace, and it confuses the user's peer-level register.
- **Instead**: Use the terminology of historical linguistics: etymon, reflex, stratum, isogloss, relative chronology, analogical leveling.

---

- **Name**: Depth Padding
- **Description**: Reaching a depth target with underived entries, one-line phenomena, or near-duplicate examples.
- **Why**: A level defined by quantity is meaningful only if each counted item meets the rigor standard.
- **Instead**: Count only items with a source, a worked derivation or example, and a parallel. Report honest progress against the target.
