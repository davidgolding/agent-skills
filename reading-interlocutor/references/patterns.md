# Reading Interlocutor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by reading-interlocutor.

## Patterns

- **Name**: Socratic-Memory Layer Progression
- **Description**: Structure the Socratic interview into four cognitive encoding layers: Schema Integration (evaluating exigency/prior knowledge), Elaborative Encoding (building argument structures), Active Recall (testing detail retention), and Dual-Coding (generating speculation/extensions). Score recall probability and cognitive load behind the scenes on a 1-10 scale to dynamically adjust pacing and gating.
- **When**: Conducting the Socratic interview loop.
- **Example**:
```
    Phase 1: Schema Integration. Ask: "How does the author's intervention connect to your existing knowledge of the field?" Scholar replies. Score cognitive load: 4/10, recall: 8/10. Since recall is high and load is manageable, proceed to Elaborative Encoding.
```

---

- **Name**: Obsidian CLI Decoupled Formatting
- **Description**: Check for the availability of the `obsidian-cli` skill. If present, use it to inspect the vault layout, query files, and write notes. If absent, fallback gracefully to outputting a best-guess Markdown structure, avoiding failing or prompting the user with error messages.
- **When**: Interacting with the Obsidian vault for layout inspection or saving final notes.
- **Example**:
```
    If obsidian-cli is available:
      Run: obsidian-cli vault="Research" create path="Notes/BookNote.md" content="..."
    Else:
      Fallback to creating a standard Markdown note at the default workspace path.
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

- **Name**: Silent CLI Dependency Failure
- **Description**: Crashing or throwing hard errors to the user when `obsidian-cli` is not configured or installed.
- **Why**: Prevents the user from completing their session on systems that lack the specific command configuration.
- **Instead**: Fallback to generating a beautifully formatted Markdown block inside the chat or a local markdown file, prompting the user to save it manually.

---
