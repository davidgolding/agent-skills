# Personal Editor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by personal-editor.

## Patterns

- **Name**: Multi-Pass Orchestration
- **When**: When analyzing any submitted passage — perform sequential, distinct passes for copyediting, prose fingerprinting, rhetorical analysis, and panel-judge evaluation, then synthesize them into a cohesive Markdown report, so that coverage stays thorough and complete.
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

- **Name**: CriticMarkup Line Edit
- **When**: While marking any line-level copyediting suggestion during pass one — attach the markup to the specific segment it applies to rather than describing the change abstractly.
- **Example**: ```
  Deletion:  The {--very--}quiet room
  Addition:  The quiet{++, shuttered++} room
  Comment:   the doctor and the father {>>Maybe: “both the doctor and the father,”
             or leave it the same<<} petitioned the court
  Combined:  She walked {--quickly--}{++briskly++} {>>“quickly” echoes “quick”
             two lines up :)<<} to the door
  ```

---

- **Name**: Four-Section Synthesized Report
- **When**: While compiling the four completed passes into the single deliverable at the end of an analysis.
- **Example**: ```
  One Markdown report, these four H2 sections, in this order:

  ## Copyediting & Proofreading Suggestions
     Annotated passage excerpts in CriticMarkup, each on its own segment.
  ## Prose Fingerprint Analysis
     Stylistic claims, each tied to cited passage evidence.
  ## Rhetorical Figure Analysis
     Named figure, quoted segment, the effect it produces.
  ## Panel Judge Adjudication Scorecard
     Caliber Rating plus the critique naming the evidence behind it.
  ```

---

## Anti-Patterns

- **Name**: Direct Single-Pass Analysis
- **Why**: Attempting to analyze grammar, style, rhetoric, and literary merit all at once in a single unstructured pass leads to missed grammatical errors, skipped rhetorical figures, generic feedback, and lack of depth in the final adjudication.
- **Instead**: Execute distinct, dedicated analytical passes for each component (copyediting, fingerprinting, rhetoric, panel-judge critique) before compiling the synthesized report.

---

- **Name**: Abstract Edit Description
- **Why**: Describing a suggested change in prose ("consider tightening the second clause") leaves the writer to locate the segment and reconstruct the proposed wording, which loses the precision the CriticMarkup annotation exists to carry.
- **Instead**: CriticMarkup Line Edit

---
