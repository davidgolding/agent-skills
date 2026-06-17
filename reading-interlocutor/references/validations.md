# Validations

This document defines the validations used by reading-interlocutor.

---

## Vault Note Exists

- **Id**: vault-note-exists
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Check if a note with the target file name already exists in the Obsidian vault.
- **Message**: A note with this file name already exists at the top level of your vault.
- **Fix Action**: Suggest appending a suffix (e.g., "-seminar-notes") to avoid overwriting existing notes.
- **Applies To**:
    - `*.md`

---

## Empty Response Validation

- **Id**: empty-response-validation
- **Severity**: error
- **Type**: regex
- **Pattern**: `^\s*$`
- **Message**: Your reply appears to be empty.
- **Fix Action**: Prompt the scholar to input a response to continue the Socratic dialogue.
- **Applies To**:
    - User input responses

---

## Memory Scoring Consistency

- **Id**: memory-scoring-consistency
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Check if both cognitive load and recall probability scores are between 1 and 10.
- **Message**: Evaluation scores are invalid or missing.
- **Fix Action**: Re-evaluate the user's response and ensure both scores are recorded invisibly on a 1-10 scale.
- **Applies To**:
    - Evaluation pass

---

## Obsidian CLI Availability

- **Id**: obsidian-cli-availability
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Check if the `obsidian-cli` command is available/registered in the environment or active session.
- **Message**: The obsidian-cli skill is not available in the current environment.
- **Fix Action**: Switch to the fallback standard file write mechanism.
- **Applies To**:
    - Initialization pass

---
