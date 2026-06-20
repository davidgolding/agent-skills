# Sharp Edges

This document defines the sharp edges used by gmeu-copyeditor.

---

## Voice Erasure in Heavy Rewrite

- **Id**: voice-erasure-heavy-rewrite
- **Summary**: Over-rewriting convoluted passages during Heavy copyediting can lead to loss of the author's unique voice.
- **Severity**: high
- **Situation**: When the agent encounters a highly complex or convoluted sentence under a Heavy copyediting instruction and rewrites it.
- **Why**: The agent might default to standard clean prose templates, ignoring the author's consciousness philosophy.
- **Solution**:
    - Explicitly extract and document the author's voice at the start of the process, and verify that the rewritten sentence still fits that description.
- **Symptoms**:
    - The text sounds generic, bureaucratic, or excessively academic.
- **Detection Pattern**: Compare the syntactic variation of the original and the rewrite; if all sentence variety is flattened to standard Subject-Verb-Object, voice erasure has likely occurred.

---

## Citation Authority Misattribution

- **Id**: citation-authority-misattribution
- **Summary**: Citing grammar corrections to GMEU or usage corrections to CGG, or inventing incorrect entries/section numbers.
- **Severity**: medium
- **Situation**: When the agent suggests a correction and references the wrong authority manual or provides a hallucinated section number.
- **Why**: The agent might blur the boundary between grammatical rules (CGG) and usage conventions (GMEU).
- **Solution**:
    - Strictly separate grammar evaluations (which concern sentence structure, word forms, syntax) from usage evaluations (which concern specific word meanings, spelling variants, idioms). Use CGG for the former and GMEU for the latter, verifying the entry or section matches.
- **Symptoms**:
    - Citations point to non-existent entries in GMEU or incorrect sections in CGG.
- **Detection Pattern**: Verify section numbers against CGG table of contents or GMEU entry alphabetization.

---

