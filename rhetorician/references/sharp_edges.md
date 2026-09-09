# Sharp Edges

This document defines the sharp edges used by rhetorician.

---

## Over-Identification of Ordinary Prose

- **Id**: over-identification
- **Summary**: Incidental repetition, ordinary word order, and plain coordination get named as figures, so the analysis reports devices the passage does not deploy.
- **Severity**: high
- **Situation**: While scanning a passage whose style is plain, or whose figured segments are few and widely spaced.
- **Why**: The catalog contains 343 entries, and at that breadth some entry's definition can be stretched to cover almost any construction. A repeated conjunction becomes polysyndeton, a pair of adjectives becomes synonymia. The result reads as a rich analysis and is largely an artifact of catalog breadth rather than of the passage.
- **Solution**:
    - Mark the segments that depart from plain statement first, per the Segment-First Scanning pattern, and identify figures only for marked segments.
- **Symptoms**:
    - Findings whose commentary explains the figure's general effect without saying what it does in this passage; a plain passage yielding a long list of figures.
- **Detection Pattern**: A finding count out of proportion to the passage's length, or commentary that would read identically against a different passage.

---

## Nearest-Label Substitution

- **Id**: nearest-label-substitution
- **Summary**: A device with no catalog entry gets reported under the closest available term, producing a confident citation for a figure that is not present.
- **Severity**: high
- **Situation**: When a passage deploys a device the catalog does not name, or names only under a term whose definition does not quite fit the segment.
- **Why**: A citation to a real catalog entry looks verified even when the entry's definition does not cover the segment, so the error survives review in a way that an admitted gap would not. The catalog is broad but finite, and a reader checking the citation finds a real entry and stops.
- **Solution**:
    - Treat each catalog **Definition** as a test the segment has to satisfy; where none is satisfied, describe the device and state that the catalog does not name it.
- **Symptoms**:
    - A cited entry whose definition, read against the quoted segment, describes something other than what the segment does.
- **Detection Pattern**: A finding whose quoted segment fails the cited entry's **Definition** on a direct reading.

---

## Figure Reported as Fault

- **Id**: figure-reported-as-fault
- **Summary**: A legitimate figure gets reported as a defect to be corrected, turning an analysis request into an unrequested edit.
- **Severity**: high
- **Situation**: While identifying devices that have both an ornamental and a vicious sense — alliteration, synecdoche, zeugma, catachresis, tautologia, epenthesis, acyrologia.
- **Why**: This skill's catalog previously filed those seven terms exclusively among the vices, each carrying boilerplate reasoning ("It introduces grammatical error, semantic confusion, stylistic weakness, or unnecessary obscurity") and a remedy pointing at another figure. The seven now sit in `## Figures` with their vice sense recorded inside the definition, but the failure mode is worth holding: a figure becomes a vice through misuse, not through appearing.
- **Solution**:
    - Identify from `## Figures` by default, and cite a `## Vices` entry only where the segment shows the specific misuse that entry's definition describes.
- **Symptoms**:
    - Commentary recommending the removal of a device the passage uses deliberately; a remedy offered where the user asked only for identification.
- **Detection Pattern**: A finding pairing a `## Figures` entry with corrective language, or a `## Vices` citation whose commentary does not name the misuse.

---

## Analysis Drifts Into Editing

- **Id**: analysis-drifts-into-editing
- **Summary**: The response rewrites or paraphrases the passage instead of quoting it, so the object of the analysis is altered by the analysis.
- **Severity**: critical
- **Situation**: When the submitted passage contains errors, awkwardness, or vices that invite correction, or when this skill runs as a sub-skill inside an editing workflow.
- **Why**: A figure exists only in the words that carry it; paraphrasing a segment can dissolve the very figure being identified. The risk rises when `personal-editor` orchestrates this skill as its pass-three sub-skill, since the surrounding workflow *is* an editing task and the editing register is already in play.
- **Solution**:
    - Quote every segment verbatim, and confine the response to identification and commentary; supply a rewrite only where the user asked for one.
- **Symptoms**:
    - Quoted segments differing from the submitted passage's wording; a revised version of the passage in the output.
- **Detection Pattern**: A quoted segment absent from the source passage under exact string comparison.

---

## Overlapping Figures Fragmented

- **Id**: overlapping-figures-fragmented
- **Summary**: A densely figured segment yields several unrelated-looking findings, obscuring that one construction is doing several things at once.
- **Severity**: medium
- **Situation**: While analyzing periodic sentences, catalogues, and other constructions where figures of repetition, omission, and arrangement coincide.
- **Why**: Many catalog entries are genus-species pairs or habitually co-occur — zeugma with ellipsis and parallelism, anaphora with asyndeton and isocolon. Reported separately, they read as a list of ornaments rather than as one rhetorical effect, and the reader cannot see which is doing the work.
- **Solution**:
    - Merge findings that share a segment per the Nested Figure Reporting pattern, naming the related figures and how they combine, and prefer the species term alongside its genus per Genus-Species Precision.
- **Symptoms**:
    - Two or more findings quoting the same words with no statement of how their figures relate.
- **Detection Pattern**: Repeated identical quoted segments across separate findings.

---

## Unresolved Catalog Cross-Reference

- **Id**: unresolved-catalog-cross-reference
- **Summary**: A `[[#term]]` cross-reference in the catalog points at an entry that does not exist, so a citation trail ends in nothing.
- **Severity**: medium
- **Situation**: While following a catalog entry's cross-references to reach a related or more specific figure.
- **Why**: The catalog is adapted from an external corpus whose internal links assumed pages this file does not carry — category pages, canon concepts, author pages. A link that reads as resolvable but resolves to nothing costs tokens and implies a precision the file lacks. The migration rewrote 27 such targets, redirecting eight to the entries that cover them and italicizing the rest; new links added by hand can reintroduce the problem.
- **Solution**:
    - Hold every `[[#term]]` to matching some entry's **Name** in `references/figures.md`, and render theory terms — the canons, the parts of an oration, the *progymnasmata* — in italics without a link.
- **Symptoms**:
    - A cross-reference whose target cannot be found in the catalog.
- **Detection Pattern**: `\[\[#([^\]]+)\]\]` in `references/figures.md` whose target matches no entry **Name**.

---
