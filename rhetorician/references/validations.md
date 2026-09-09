# Validations

This document defines the validations used by rhetorician.

---

## Identification Quotes Its Segment

- **Id**: identification-quotes-segment
- **Severity**: error
- **Type**: semantic
- **Pattern**:
    - A named figure presented with no quoted segment of the analyzed passage exhibiting it.
- **Message**: Every identification needs the passage segment that carries the figure, so the reader can check the claim against the text.
- **Fix Action**: Quote the exact segment and attach the identification to it, per the Structured Commentary Entry pattern.
- **Applies To**:
    - analysis output

---

## Identification Cites a Catalog Entry

- **Id**: identification-cites-catalog-entry
- **Severity**: error
- **Type**: semantic
- **Pattern**:
    - A named figure with no inline citation to the entry in `references/figures.md` that defines it, or a citation naming an entry that file does not contain.
- **Message**: Each figure must be named by the term the catalog uses and cited to its entry; a citation to a term absent from the catalog is unverifiable.
- **Fix Action**: Look the term up in `references/figures.md`, use that entry's **Name**, and cite it. Where no entry fits the segment, describe the device and state that the catalog does not name it.
- **Applies To**:
    - analysis output

---

## Passage Left Unaltered

- **Id**: passage-left-unaltered
- **Severity**: error
- **Type**: semantic
- **Pattern**:
    - Output that rewrites, paraphrases, corrects, or reorders the analyzed passage, or that presents a revised version of it, where the user asked for analysis.
- **Message**: Analysis identifies figures in the passage as written; altering the wording answers a different request and removes the object of the analysis.
- **Fix Action**: Restore the original wording, quote the segment verbatim, and confine the response to identification and commentary.
- **Applies To**:
    - analysis output

---

## Structured Commentary Shape

- **Id**: structured-commentary-shape
- **Severity**: warning
- **Type**: schema
- **Pattern**:
    - A finding departing from the sequence: bold quoted segment, colon, commentary, inline citation to the catalog entry.
- **Message**: Findings follow the Structured Commentary Entry shape, so that a downstream consumer can parse segment, commentary, and citation apart.
- **Fix Action**: Reformat the finding per the Structured Commentary Entry pattern in `references/patterns.md`.
- **Applies To**:
    - analysis output

---

## Overlapping Figures Reported Together

- **Id**: overlapping-figures-reported-together
- **Severity**: warning
- **Type**: semantic
- **Pattern**:
    - Two or more findings quoting the same passage segment and naming different figures without stating how those figures relate.
- **Message**: Figures sharing a segment belong in one finding that names how they combine, rather than in separate findings that read as unrelated.
- **Fix Action**: Merge the findings per the Nested Figure Reporting pattern, naming the related figures and the combined effect.
- **Applies To**:
    - analysis output

---

## Vice Reported as Vice

- **Id**: vice-reported-as-vice
- **Severity**: warning
- **Type**: semantic
- **Pattern**:
    - A figure drawn from the catalog's `## Figures` section reported as a fault to be removed, or an entry from `## Vices` reported without the specific misuse its definition describes.
- **Message**: A figure becomes a vice through misuse rather than through appearing; the catalog's two sections carry that distinction.
- **Fix Action**: Identify from `## Figures` by default, and cite a `## Vices` entry when the segment shows the misuse that entry defines.
- **Applies To**:
    - analysis output

---

## Catalog Cross-Reference Resolves

- **Id**: catalog-cross-reference-resolves
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `\[\[#([^\]]+)\]\]` in `references/figures.md` whose target matches no entry **Name** in that file.
- **Message**: This cross-reference points at a catalog entry that does not exist, so it reads as resolvable while resolving to nothing.
- **Fix Action**: Point the link at the entry that covers the term, add the missing entry, or render the term in italics as plain text where it belongs to rhetorical theory rather than to the figure catalog.
- **Applies To**:
    - references/figures.md

---
