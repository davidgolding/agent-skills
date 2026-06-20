# Sharp Edges

This document defines the sharp edges used by reading-interlocutor.

---

## Empty Vault Style Failure

- **Id**: empty-vault-style-failure
- **Summary**: Fails to determine note structure because vault is empty or contains non-Markdown notes.
- **Severity**: medium
- **Situation**: The agent performs a vault analysis pass but the vault has zero markdown files or files lack styling cues.
- **Why**: The style extractor expects to find Markdown files to parse styling elements like headers, YAML frontmatter keys, and list indicators.
- **Solution**:
    - Prompt the user with 1-2 configuration questions: "I couldn't find style cues in your vault. Do you prefer folders/tags? Do you prefer a specific header layout?"
- **Symptoms**:
    - Style analysis returns null/empty results.
- **Detection Pattern**: Style analysis passes returning null or empty results on vaults with no markdown files.

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
- **Detection Pattern**: Generating generic, broad Socratic questions that do not reference specific chapters or monograph claims.

---

## Memory Overload Stress

- **Id**: memory-overload-stress
- **Summary**: Scholar suffers cognitive fatigue because questions are too difficult or too rapid.
- **Severity**: high
- **Situation**: Socratic questions trigger high cognitive load scores (e.g., >8/10) over multiple turns without progression.
- **Why**: Asking excessively challenging questions without scaffolded guidance increases frustration and inhibits memory encoding.
- **Solution**:
    - Provide a hint, split the question into smaller steps, or lower the difficulty parameter for the current concept.
- **Symptoms**:
    - User gives short, frustrated, or vague answers like "I don't know" or "Not sure".
- **Detection Pattern**: Multiple consecutive turns of high cognitive load questions without providing hints or lowering difficulty.

---

## Absent CLI Skill Crash

- **Id**: absent-cli-skill-crash
- **Summary**: Agent fails to create notes because the `obsidian-cli` skill is missing from the host environment.
- **Severity**: medium
- **Situation**: The agent attempts to call `obsidian-cli` commands, but the tool is not installed or registered.
- **Why**: The environment doesn't have `npx kepano/obsidian-skills` installed or paths set up.
- **Solution**:
    - Fallback immediately to standard file write or direct Markdown response, recommending the user install the official skill next time.
- **Symptoms**:
    - Command executor returns "command not found" or "skill unavailable".
- **Detection Pattern**: Terminal executor failing with command not found errors when invoking obsidian-cli.

---
