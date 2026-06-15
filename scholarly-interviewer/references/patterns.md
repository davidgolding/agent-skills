# Scholarly Interviewer Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by scholarly-interviewer.

## Patterns

- **Name**: Socratic Rhetorical Layer Progression
- **Description**: Structure the interview into four distinct intellectual phases: Exigency, Argument Architecture, Evidence Evaluation, and Speculation/Extension. Score response depth behind the scenes to guide transition between phases.
- **When**: Leading the interview loop.
- **Example**:
```
    Phase 1: Exigency. Professor asks: "What urgent intellectual gap is the author responding to, and why does their intervention matter right now?" User replies. Agent evaluates depth. If scored >= 7/10, transition to Phase 2 (Argument Architecture).
```

---

- **Name**: Obsidian Style Extraction
- **Description**: Scan existing Markdown files in the vault to automatically infer the format of the output note, matching headers, frontmatter fields, and bullet styles.
- **When**: Initialization of the session.
- **Example**:
```
    Checking files in vault... Detected YAML keys: [tags, date, topic]. Detected bullet style: - space. Output will format with identical metadata keys and bullet patterns.
```

---

## Anti-Patterns

- **Name**: Book-Report Summary Deferral
- **Description**: Allowing the user to simply summarize the book's contents without offering critical evaluations, speculative extensions, or identifying underlying gaps.
- **Why**: Defeats the purpose of the seminar dry run by reducing a practicing scholar's cognitive load to simple information recall.
- **Instead**: Challenge the user with counter-perspectives, historical context, or edge cases. If they describe what the author said, ask: "But if we accept that claim, how does it resolve the critique by contemporary critics?"

---

- **Name**: Transcript Dump Output
- **Description**: Exporting the entire chat log, including the agent's questions, as the final Obsidian note.
- **Why**: Bloats the user's Obsidian vault with chat history rather than generating a clean, high-value personal reference note.
- **Instead**: Synthesize the user's answers and insights into a cohesive, structured summary using their own words under thematic headings.

---
