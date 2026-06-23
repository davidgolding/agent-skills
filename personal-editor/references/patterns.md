# Personal Editor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by personal-editor.

## Patterns

- **Name**: Multi-Pass Orchestration
- **Description**: Perform sequential, distinct passes for copyediting, prose fingerprinting, rhetorical analysis, and panel judge evaluation, synthesizing them into a cohesive Markdown report.
- **When**: When analyzing any text passage up to 2000 words to ensure thorough and complete coverage.
- **Example**:
```markdown
## Copyediting & Proofreading Suggestions
- **The contemporary event**: should be contemporaneuous event (GMEU, "contemporary; contemporaneous").

## Prose Fingerprint Analysis
- The text exhibits a paratactic syntax and high Anglo-Saxon vocabulary mix.

## Rhetorical Figure Analysis
- **"I came, I saw, I conquered"**: Asyndeton is used here to build momentum.

## Panel Judge Adjudication Scorecard
- **Caliber Rating**: Publishable/Academic Worthy.
- **Critique**: The text displays strong control of cadence but relies on standard academic structures, falling short of Nobel-grade stylistic innovation.
```

---

## Anti-Patterns

- **Name**: Direct Single-Pass Analysis
- **Description**: Attempting to analyze grammar, style, rhetoric, and literary merit all at once in a single, unstructured pass.
- **Why**: Single-pass analysis leads to missed grammatical errors, skipped rhetorical figures, generic feedback, and lack of depth in the final adjudication.
- **Instead**: Execute distinct, dedicated analytical passes for each component (copyediting, fingerprinting, rhetoric, panel judge critique) before compiling the synthesized report.

---
