# Validations

This document defines the validations used by sharepoint-search.

---

## Two-Pass Query Structure Validation

- **Id**: validate-two-pass-query
- **Severity**: error
- **Type**: instruction
- **Pattern**:
  - Must include Pass 1 (Lexical keyword/entity/metadata extraction)
  - Must include Pass 2 (Semantic vector embedding intent matching)
- **Message**: Search invocation missing required two-pass structure. Both lexical and semantic passes are mandatory.
- **Fix Action**: Re-formulate the search request to explicitly perform lexical entity extraction and semantic vector embedding lookup.
- **Applies To**:
  - `*.md`
  - `*.json`

---

## Verbatim Quote Fidelity & Location Anchor Validation

- **Id**: validate-verbatim-quote-fidelity
- **Severity**: error
- **Type**: instruction
- **Pattern**:
  - Must quote primary source passages verbatim in full
  - Must preserve exact orthography, capitalization, and punctuation
  - Must attach stable location anchors (file name, webUrl, path, heading/offset anchor)
- **Message**: Quoted evidence passage is paraphrased or missing location anchors.
- **Fix Action**: Replace paraphrased text with verbatim quote from document and attach full location anchor.
- **Applies To**:
  - `*.md`

---

## Evidence vs Interpretation Separation Validation

- **Id**: validate-evidence-interpretation-separation
- **Severity**: error
- **Type**: instruction
- **Pattern**:
  - Evidence section containing cited verbatim quotations
  - Interpretation section clearly labeled for synthesis, inferences, or candidate readings
- **Message**: Response conflates raw evidence with interpretive claims.
- **Fix Action**: Move synthesis and candidate readings into a labeled `## Interpretation` section, keeping `## Evidence` restricted to quoted text and citations.
- **Applies To**:
  - `*.md`

---

## Search Log & Null Result Accounting Validation

- **Id**: validate-search-log-null-accounting
- **Severity**: error
- **Type**: instruction
- **Pattern**:
  - Log of actual search queries ran
  - Explicit statement of null results if no items found
  - Distinction between exhaustive absence vs non-exhaustive search
- **Message**: Negative search result returned without explicit search log accounting.
- **Fix Action**: Append a `## Searches Run` section listing exact terms and scopes queried.
- **Applies To**:
  - `*.md`

---

## Stop-Loss Pivot Trigger Validation

- **Id**: validate-stop-loss-pivot-trigger
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
  - Stop-loss check after 1-2 zero-hit search attempts
  - Explicit pivot classification (Zoom, Source, or Question pivot)
- **Message**: Multiple failed search iterations executed without a structured pivot.
- **Fix Action**: Stop repeating keyword variations and execute a Zoom, Source, or Question pivot.
- **Applies To**:
  - `*.md`

---
