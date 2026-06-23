# Personal Editor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by personal-editor.

## Patterns

- **Name**: Multi-Pass Orchestration
- **Description**: Perform sequential, distinct passes for copyediting, prose fingerprinting, rhetorical analysis, and panel judge evaluation, synthesizing them into a cohesive Markdown report.
- **When**: When analyzing any text passage up to 2000 words to ensure thorough and complete coverage.
- **Example**:
```markdown
## Copyediting & Proofreading Suggestions
- The father and the doctor {>>Maybe: “Both the father and doctor” or “Together, the father and doctor” or leave it the same<<} petitioned...
- ...thereby forestalling an arrest warrant. {>>The previous is murky, and can sound like Alice is the one who forestalled the arrest warrant. Maybe: “forestalling an arrest warrant by, in effect, pleading insanity against Alice” or “in effect pleading insanity against Alice for having become ‘dangerous to the community,’ thereby forestalling an arrest warrant.”<<}
- As a matter of course, {>>except now this too many “of courses” in two sentences :)<<} Fanny took charge of Alice’s two essentially orphaned children.

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
