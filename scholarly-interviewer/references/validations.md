# Validations

This document defines the validations used by scholarly-interviewer.

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
