# GMEU Copyeditor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by gmeu-copyeditor.

## Patterns

- **Name**: Consciousness-Based Voice Alignment
- **When**: While analyzing text and applying copyediting suggestions — especially at the Heavy level, where rewriting occurs. Define the author's voice as a high-fidelity transmission of their consciousness, and ground every language improvement inside that specific aesthetic context.
- **Example**: ```
  Analyzed Voice: The author's voice represents a consciousness pared down to
  hard facts and direct statements, similar to Hemingway.
  **It was a day that was extremely cold and the wind was blowing very hard**:
  The sentence contains unnecessary wordiness. We suggest copyediting to:
  "The day was cold and the wind blew hard."
  ```

---

- **Name**: Authoritative Source Citation
- **When**: While writing copyediting commentary for a usage or grammar change. Append a precise inline citation to the end of each commentary paragraph naming the specific rule source — GMEU for usage queries, CGG for grammar queries.
- **Example**: ```
  **who was her manipulator**: GMEU advises using "who" for persons and
  restricting "which/that" appropriately, but notes that "manipulator" has
  specific usage connotations. (GMEU, "who; whom")
  **she had received with her husband**: The pronoun "she" correctly aligns
  with its antecedent, but the prepositional phrasing is grammatically
  checked. (CGG, "Pronouns: agreement," 5.34)
  ```

---

- **Name**: Mechanical and Correlating-Parts Sweep
- **When**: At every level — Light, Medium, and Heavy alike.
- **Example**: ```
  Mechanical editing: ensure consistency in spelling, capitalization,
  punctuation, hyphenation, abbreviations, and list formatting.
  Correlating parts: check the numbering of notes, tables, and figures;
  bibliography alphabetization; and citation-to-bibliography alignment.
  ```

---

- **Name**: Light Level Rubric
- **When**: While editing at the Light level.
- **Example**: ```
  Language editing: correct indisputable grammar, syntax, and usage errors.
  Leave non-outright errors as written. Point out egregiously wordy
  paragraphs, leaving the prose itself for the author to revise. Leave minor
  wordiness and jargon in place. Query new terms.
  Content editing: query factual inconsistencies and statements that seem
  incorrect.
  ```

---

- **Name**: Medium Level Rubric
- **When**: While editing at the Medium level.
- **Example**: ```
  Language editing: correct all grammar, syntax, and usage errors. Revise or
  point out infelicities. Point out wordy patches and suggest revisions.
  Define or query new terms.
  Content editing: query incorrect facts, verify them using online or printed
  references, and query faulty organization or logic.
  ```

---

- **Name**: Heavy Level Rubric
- **When**: While editing at the Heavy level.
- **Example**: ```
  Language editing: correct all errors and infelicities. Rewrite wordy or
  convoluted patches while preserving the identified voice. Define or query
  new terms.
  Content editing: verify and revise incorrect facts, and query or fix faulty
  organization and logic.
  ```

---

## Anti-Patterns

- **Name**: Homogenizing AI Style
- **Why**: Rewriting the author's prose into a generic, sanitized AI-style paragraph erases the unique texture of their writing, which violates the copyeditor's core duty — to help the author say what they want to say, rather than what the editor would say.
- **Instead**: Consciousness-Based Voice Alignment — identify the author's voice first and adjust sentences only where an actual usage or grammatical issue exists, keeping the original sentence structure wherever it is clear and correct.

---

- **Name**: Uncited Grammatical/Usage Claims
- **Why**: A suggestion or grammar claim offered without its GMEU or CGG citation is harder for the author to verify and trust, and it steps outside the skill's authority constraints.
- **Instead**: Authoritative Source Citation — locate the relevant GMEU entry or CGG topic and section and append the citation, as `(GMEU, "entry")` or `(CGG, "Topic," section)`.

---

- **Name**: Level Scope Creep
- **Why**: A convoluted sentence invites a rewrite regardless of the level in force, so a Light or Medium pass drifts into Heavy-level machete work and returns changes the user did not authorize.
- **Instead**: Light Level Rubric, Medium Level Rubric, or Heavy Level Rubric — check each suggestion against the rubric for the level actually selected before emitting it.

---
