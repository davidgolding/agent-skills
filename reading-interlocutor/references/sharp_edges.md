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
- **Summary**: The agent assumes familiarity with a text, leading to fabricated or off-target Socratic questions.
- **Severity**: high
- **Situation**: The user provides a text title/author that is obscure or lacks local text files, and the agent's web research/internal memory fails to retrieve the exact argument structures.
- **Why**: The agent relies on broad disciplinary keywords or hallucinates monograph claims rather than referencing the specific, verified claims of the work.
- **Solution**:
    - If the work is not locally available to the agent, the agent must ask the user to supply a summation or description from the work, and formulate queries based strictly on the user's provided context.
- **Symptoms**:
    - Socratic questions reference chapters or specific arguments that do not exist in the work.
- **Detection Pattern**: Generating questions that make assumptions about specific claims or structures of a text without local source text or user-provided summary verification.

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

## Cognitive Metrics Exposure

- **Id**: cognitive-metrics-exposure
- **Summary**: Internal cognitive scores or layer transition info is exposed to the user.
- **Severity**: medium
- **Situation**: The agent prints "Cognitive Load", "Recall Probability", or "Current Layer" statistics in its response.
- **Why**: The agent incorrectly formats its reply by copying internal tracking variables into the chat-facing text block.
- **Solution**:
    - Ensure all cognitive load and recall probability scores are kept strictly within internal thought blocks.
- **Symptoms**:
    - The chat output contains sections labeled "Invisible Cognitive Metrics" or similar bullet points.
- **Detection Pattern**: User-facing responses containing numerical metrics or labels referring to Socratic layer names.

---

## Pedagogical Persona Slip

- **Id**: pedagogical-persona-slip
- **Summary**: Agent acts as an instructional mentor/guide rather than a challenging academic peer.
- **Severity**: medium
- **Situation**: The agent uses transitional phrases indicating Socratic progression.
- **Why**: The agent defaults to user-friendly instructional chat behavior instead of maintaining a rigorous seminar professor persona.
- **Solution**:
    - Remove all meta-commentary about the state of the conversation (e.g., "Let's transition to..."). Pose Socratic questions directly and challenging.
- **Symptoms**:
    - Sentences like "Let's transition to Active Recall" or "Now we will test your comprehension of..."
- **Detection Pattern**: Conversational responses containing meta-comments about the current step, phase, or Socratic layer of the session.

---

## Purple Prose Dilution

- **Id**: purple-prose-dilution
- **Summary**: The agent uses flattering praise or wordy validation in response to user answers.
- **Severity**: low
- **Situation**: The agent praises the user's responses (e.g., "Your distinction is a brilliant synthesis").
- **Why**: The agent mimics standard helper chatbot politeness instead of professional academic critique.
- **Solution**:
    - Eliminate all congratulatory remarks and proceed directly to challenging the user's assertions.
- **Symptoms**:
    - Responses beginning with "Excellent point," "Brilliant synthesis," or "That is correct."
- **Detection Pattern**: The presence of praise or validations in user-facing responses.

---

## Editorial Note Distortion

- **Id**: editorial-note-distortion
- **Summary**: The agent synthesizes or edits the user's answers when generating the final vault note.
- **Severity**: high
- **Situation**: The final Markdown note contains paragraphs of summaries, explanations, or altered phrasing of the user's statements.
- **Why**: The agent attempts to polish the note by writing its own summaries instead of extracting the user's verbatim text.
- **Solution**:
    - Copy the user's responses verbatim and reposition them under clean, structured headings.
- **Symptoms**:
    - Note output contains words, definitions, or synthesis sentences not written by the user.
- **Detection Pattern**: Vault note content that does not match the user's chat input responses verbatim.
