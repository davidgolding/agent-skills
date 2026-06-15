# Sharp Edges

This document defines the sharp edges used by scholarly-interviewer.

---

## Empty Vault Style Failure

- **Id**: empty-vault-style-failure
- **Summary**: Fails to determine note structure because vault is empty or contains non-Markdown notes.
- **Severity**: medium
- **Situation**: The agent performs a vault analysis pass but the vault has zero markdown files or files lack styling cues.
- **Why**: The style extractor expects to find markdown files to parse styling elements like headers, yaml frontmatter keys, and list indicators.
- **Solution**:
    - Prompt the user with 1-2 configuration questions: "I couldn't find style cues in your vault. Do you prefer folders/tags? Do you prefer a specific header layout?"
- **Symptoms**:
    - Style analysis returns null/empty results.
- **Detection Pattern**: `vault_style_analysis_failed`

---

## Hallucinated Text Mastery

- **Id**: hallucinated-text-mastery
- **Summary**: The agent assumes familiarity with a text and asks generic, off-target questions.
- **Severity**: high
- **Situation**: The user provides a text title/author that is obscure or lacks local text files, and the agent's web research/internal memory fails to retrieve the exact argument structures.
- **Why**: The agent relies on broad disciplinary keywords rather than the specific claims of the monograph.
- **Solution**:
    - Before starting, summarize the text's core thesis and key chapters in 1 paragraph and ask the user to verify/edit it before proceeding.
- **Symptoms**:
    - Socratic questions feel generic (e.g. "What is the author's methodology?" instead of referencing their specific case study).
- **Detection Pattern**: `generic_question_generation`

---
