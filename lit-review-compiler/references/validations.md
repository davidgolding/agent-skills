# Validations

This document defines the validations used by lit-review-compiler.

---

## Every Citation Has a Verification Record

- **Id**: citation-has-verification-record
- **Severity**: error
- **Type**: semantic
- **Pattern**: Every bibliographic entry in the report must correspond to a `scripts/verify_citation.py` run whose result tier (`api_confirmed`, `secondary_confirmed`, or `unverified` with caveat) is known before the entry is written.
- **Message**: A citation appears in the report with no corresponding verification run.
- **Fix Action**: Run `scripts/verify_citation.py` against the citation's title/author/year before including it, or remove it from the report if it cannot be verified through any tier.
- **Applies To**:
    - `*.md` (report output files)

---

## Tier-3 Caveat Is Visible

- **Id**: tier3-caveat-visible
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - Entries whose verification tier is `unverified` must contain a caveat phrase such as `verified by search evidence only` or `not independently confirmed` adjacent to the citation.
- **Message**: A Tier-3 (unverified) citation is present without a visible caveat marking its verification status.
- **Fix Action**: Add an explicit caveat phrase to the entry, or re-attempt verification before deciding it belongs at Tier 3.
- **Applies To**:
    - `*.md` (report output files)

---

## Scope Statement Present Near Opening

- **Id**: scope-statement-present
- **Severity**: error
- **Type**: semantic
- **Pattern**: The report's opening section (introduction or a clearly labeled "Scope" section) must state the time range, sub-field/lens boundaries, language restrictions, and exclusions that were elicited or inferred for this run.
- **Message**: The report does not state its scope boundaries near the opening.
- **Fix Action**: Add a scope statement summarizing the elicited or inferred boundaries before the thematic subsections begin.
- **Applies To**:
    - `*.md` (report output files)

---

## No Conflated Per-Entry Flags

- **Id**: no-conflated-entry-flags
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An entry carries an explicit annotation-depth label (e.g., "per abstract," "full text reviewed") alongside or instead of the Tier-3 verification caveat.
- **Message**: An entry labels its annotation depth explicitly, which conflates two distinct signals (annotation depth vs. verification confidence) that must stay separate.
- **Fix Action**: Remove the annotation-depth label; let annotation length and specificity vary naturally with what was retrieved instead of announcing it.
- **Applies To**:
    - `*.md` (report output files)

---

## No Internal Matrices in Output

- **Id**: no-internal-matrices-in-output
- **Severity**: error
- **Type**: semantic
- **Pattern**: The delivered report includes a Literature Matrix, Synthesis Matrix, or any raw source-by-source extraction table as a standalone section.
- **Message**: The report includes an internal working matrix as a deliverable section.
- **Fix Action**: Remove the matrix section; fold any content worth keeping into the narrative annotated-entry prose instead.
- **Applies To**:
    - `*.md` (report output files)

---

## Verification Tier And Significance Kept Separate

- **Id**: verification-significance-separated
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An entry's verification tier caveat or confirmation appears with no adjacent, separate note on the source's centrality or consensus status within its cluster.
- **Message**: This entry presents verification tier and scholarly significance as a single fused signal instead of two distinct ones.
- **Fix Action**: Add a brief consensus/significance note distinct from the tier line, drawn from what was retrieved, or state plainly that significance could not be assessed from what was retrieved.
- **Applies To**:
    - `*.md` (report output files)

---

## Coverage & Confidence Note Present

- **Id**: coverage-confidence-note-present
- **Severity**: error
- **Type**: semantic
- **Pattern**: The report lacks a closing "Coverage & Confidence" section stating the verification-tier distribution across all cited sources and any lens, sub-field, or lineage named in scope or surfaced by the benchmark cross-check but not reached.
- **Message**: The report does not state its verification-tier distribution or known coverage gaps.
- **Fix Action**: Add a Coverage & Confidence section after the thematic subsections stating tier counts and any named gaps.
- **Applies To**:
    - `*.md` (report output files)

---

## External Benchmark Cross-Check Performed

- **Id**: benchmark-cross-check-performed
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Report Assembly begins with no record, in the working matrix or conversation, of a cross-check against an externally authored domain structure (handbook, encyclopedia entry, flagship review journal).
- **Message**: The domain map was not checked against any externally authored structure before the report was assembled.
- **Fix Action**: Before assembling the report, cross-check the compiled clusters against one externally authored domain structure and note any named gap it surfaces.
- **Applies To**:
    - report assembly process (Phase 03 entry condition)

---

## Precise Classification Checked Against Alternative Framings

- **Id**: precise-classification-checked
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An input classified as precise, with the scoping round skipped, and no record of considering at least one alternative disciplinary framing before proceeding.
- **Message**: A precise-input classification skipped the scoping round without checking whether an alternative framing would change scope.
- **Fix Action**: Before skipping the scoping round, state one or two alternative framings the question could map to and confirm neither changes scope; reclassify as broad and run the scoping round if one does.
- **Applies To**:
    - Phase 01 (Classify & Scope) execution

---

## Scoping Round Offers Candidate Options

- **Id**: scoping-round-offers-candidates
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A scoping round is issued to the user as an open free-text ask for sub-fields, lenses, or exclusions with no candidate options proposed.
- **Message**: The scoping round asks the user to supply boundaries without proposing candidate options drawn from a preliminary scan.
- **Fix Action**: Run a quick preliminary scan and propose a short candidate list of sub-fields/lenses for the user to confirm or edit via the platform's blocking question tool, rather than an open-ended free-text ask.
- **Applies To**:
    - Phase 01 (Classify & Scope) scoping round

---

## Totalizing Language Requires Scoped Claim

- **Id**: totalizing-language-scoped
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `\b(the complete|the definitive|exhaustive(ly)?|settles the debate|the entire literature)\b`
- **Message**: The report uses totalizing language without an adjacent, explicit scope qualifier.
- **Fix Action**: Either remove the totalizing phrase or immediately qualify it with the report's stated scope boundaries (e.g., "the most complete account within [stated scope]").
- **Applies To**:
    - `*.md` (report output files)

---
