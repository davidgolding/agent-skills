# Skill Auditor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by skill-auditor.

## Patterns

- **Name**: Full-Folder Ingestion
- **When**: At the start of every audit.
- **Example**: ```
  Read SKILL.md, then read every file under references/, scripts/, templates/,
  and any other subfolder, before scoring anything against pev-m.md.
  ```

---

- **Name**: Conditional Interactions Requirement
- **When**: While checking whether the audited skill needs references/interactions.md.
- **Example**: ```
  Scan SKILL.md and references/*.md for mid-task prompts, multi-turn confirmation
  language, or gated state transitions. Require interactions.md only when found;
  otherwise omit the requirement entirely.
  ```

---

- **Name**: Affirmative Rewrite
- **When**: While rewriting any negative-polarity instruction found during the language review.
- **Example**: ```
  Before: "Never transition states or emit output payloads without passing
  strict validation criteria."
  After:  "Whenever transitioning states or emitting output payloads, pass
  strict validation criteria."
  ```

---

- **Name**: Heuristic Token Scoring
- **When**: While scoring the token-efficiency axis of the scorecard.
- **Example**: ```
  Count negative-instruction density, cross-file repetition, and redundant
  phrasing as concrete signals. Report the score against those signals, not
  against a computed value of PEV-M's U_t formula.
  ```

---

- **Name**: Plan-Then-Migrate Sequencing
- **When**: Between completing the audit and touching any file in the audited skill's folder.
- **Example**: ```
  Write the executive summary, scorecard, and change script to a file inside
  the audited skill's folder. Present it in chat. Hold all edits to the
  audited skill until the user responds with explicit approval.
  ```

---

- **Name**: Behavior-Preserving Migration
- **When**: While executing an approved refactor script.
- **Example**: ```
  Map every original instruction, feature, and effect to its PEV-M
  destination file before rewriting or deleting the source content. Confirm
  the mapping is complete before presenting the migration as finished.
  ```

---

## Anti-Patterns

- **Name**: Formula Literalism
- **Why**: PEV-M's U_t formula requires token probability distributions and entropy measures a text-only audit has no access to; a fabricated number reads as measured when it is invented.
- **Instead**: Heuristic Token Scoring

---

- **Name**: Negation Preservation
- **Why**: Rewriting "Don't do X" as "Do not do X" or another synonym negation keeps the model reasoning about what to avoid rather than what to do, defeating the purpose of the rewrite.
- **Instead**: Affirmative Rewrite

---

- **Name**: Premature Mutation
- **Why**: Editing the audited skill's files before approval collapses the plan-then-migrate sequence into one step and removes the user's last chance to redirect scope before files change.
- **Instead**: Plan-Then-Migrate Sequencing

---

- **Name**: Uniform Interactions Mandate
- **Why**: Forcing an empty or fabricated interactions.md onto a skill with no interaction loop adds unneeded scaffolding and buries the real PEV-M state matrix in filler.
- **Instead**: Conditional Interactions Requirement

---

- **Name**: Behavior Drop
- **Why**: A structurally compliant skill that silently loses functionality during migration is a regression, not a refactor.
- **Instead**: Behavior-Preserving Migration

---
