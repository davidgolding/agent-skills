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

## No Cognitive Metrics In Response

- **Id**: no-cognitive-metrics-in-response
- **Severity**: error
- **Type**: regex
- **Pattern**: `(?i)(cognitive load|recall probability|current layer|schema integration|elaborative encoding|active recall|dual-coding)\s*:\s*\d+`
- **Message**: Cognitive load or recall scoring metrics are being exposed directly in the response.
- **Fix Action**: Remove all metric displays and output only the Socratic conversational questions.
- **Applies To**:
    - Agent responses

---

## No Mentoring Transitions

- **Id**: no-mentoring-transitions
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Check if the response contains meta-commentary, instructions, or guide-like transitions such as "Let's transition to" or "Now we will test".
- **Message**: Response contains instructional transitional text.
- **Fix Action**: Remove the transitional text and transition directly to the next Socratic question.
- **Applies To**:
    - Agent responses

---

## No Response Validation Praise

- **Id**: no-response-validation-praise
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Check if the response contains praise or flatteries like "excellent point," "brilliant synthesis," or "great observation."
- **Message**: Response contains conversational praise or flattery.
- **Fix Action**: Remove the praise or validation and focus purely on challenging the argument.
- **Applies To**:
    - Agent responses

---

## Verbatim Note Output Only

- **Id**: verbatim-note-output-only
- **Severity**: error
- **Type**: instruction
- **Pattern**: Check if the generated vault note contains any paragraphs, summaries, or synthesis that were not written verbatim by the user.
- **Message**: Note output contains agent-synthesized content.
- **Fix Action**: Strip out any agent-synthesized text and ensure all note sections consist of the user's exact replies repositioned verbatim.
- **Applies To**:
    - Generated `.md` note contents
