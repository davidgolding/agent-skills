# Sharp Edges

This document defines the sharp edges used by personal-editor.

---

## Context Bloat and Word Count Limit

- **Id**: context-bloat-limit
- **Summary**: Processing texts larger than 2000 words degrades analysis quality and triggers context/performance issues.
- **Severity**: high
- **Situation**: When the user submits a text passage larger than 2000 words.
- **Why**: The multi-pass analysis requires deep reasoning and multiple internal passes; larger texts exceed performance boundaries and dilute feedback.
- **Solution**:
    - Check the word count upfront and reject inputs over 2000 words immediately.
- **Symptoms**:
    - Slow response times, generic critiques, missing citations, or incomplete runs.
- **Detection Pattern**: Text inputs where the word count exceeds 2000 words.

---
