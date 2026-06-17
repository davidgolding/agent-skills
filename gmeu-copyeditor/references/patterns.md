# GMEU Copyeditor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by gmeu-copyeditor.

## Patterns

- **Name**: Consciousness-Based Voice Alignment
- **Description**: The practice of defining the author's voice as a high-fidelity transmission of their consciousness and grounding all language improvements within that specific aesthetic context.
- **When**: Analyzing text and applying copyediting suggestions, especially at the Heavy level where rewriting occurs.
- **Example**:
```
Analyzed Voice: The author's voice represents a consciousness pared down to hard facts and direct statements, similar to Hemingway. 
**It was a day that was extremely cold and the wind was blowing very hard**: The sentence contains unnecessary wordiness. We suggest copyediting to: "The day was cold and the wind blew hard."
```

---

- **Name**: Authoritative Source Citation
- **Description**: Appending a precise inline citation to the end of every commentary paragraph indicating the specific rule source. Use GMEU for usage queries and CGG for grammar queries.
- **When**: Writing copyediting commentaries for usage or grammar changes.
- **Example**:
```
**who was her manipulator**: GMEU advises using "who" for persons and restricting "which/that" appropriately, but notes that "manipulator" has specific usage connotations. (GMEU, "who; whom")
**she had received with her husband**: The pronoun "she" correctly aligns with its antecedent, but the prepositional phrasing is grammatically checked. (CGG, "Pronouns: agreement," 5.34)
```

---

## Anti-Patterns

- **Name**: Homogenizing AI Style
- **Description**: Rewriting the author's prose into a generic, sanitized AI-style paragraph that erases the author's specific voice.
- **Why**: Over-editing destroys the unique texture of the author's writing, which violates the core duty of a copyeditor to help the author say what they want to say, not what the editor would say.
- **Instead**: Identify the author's voice first and adjust sentences only when there are actual usage/grammatical issues, keeping the original sentence structure where possible if it is clear and correct.

---

- **Name**: Uncited Grammatical/Usage Claims
- **Description**: Making copyediting suggestions or grammar claims without providing the required GMEU or CGG citation.
- **Why**: It makes suggestions harder for the author to verify and trust, and violates the strict authority constraints of the skill.
- **Instead**: Always find the relevant entry in GMEU or section/topic in CGG and append the citation, e.g., `(GMEU, "entry")` or `(CGG, "Topic," section)`.

---

