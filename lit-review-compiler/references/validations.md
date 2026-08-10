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
