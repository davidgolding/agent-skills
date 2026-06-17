# Sharp Edges

This document defines the sharp edges used by prose-fingerprinter.

---

## Context Window Exhaustion on Large Inputs

- **Id**: context-exhaustion
- **Summary**: Attempting to process and analyze massive raw text files in a single context run, causing high token usage or output truncation.
- **Severity**: high
- **Situation**: The user provides an entire chapter or book (e.g., 20,000+ words) to extract a fingerprint.
- **Why**: Multi-dimensional linguistic parsing (syntax, syllables, etymology, modes) requires dense context space per word. Processing huge files directly will exceed context limits or dilute attention.
- **Solution**:
    - Limit the analysis to a representative sample of 1,000 to 2,000 words from the text.
    - Chunk large documents and average the extracted fingerprint metrics across chunks.
- **Symptoms**:
    - Agent fails to finish the analysis.
    - Incomplete outputs or repetitive metrics.
- **Detection Pattern**: Analyzing input texts containing more than 3,000 words without applying sampling or chunking.

---
