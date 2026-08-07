# Skill Auditor Sharp Edges

This document defines the sharp edges used by skill-auditor.

## Fabricated Token Score

- **Id**: fabricated-token-score
- **Summary**: skill-auditor reports a numeric U_t value as if it had computed PEV-M's mutual-information formula from the audited skill's text.
- **Severity**: high
- **Situation**: During the token-efficiency scoring step of the audit.
- **Why**: The formula's inputs — token probability distributions, conditional entropy of injected reference material — are not observable from a text-only audit; any number produced from them is invented, not measured.
- **Solution**: Score token efficiency from the heuristic signals in patterns.md (redundancy, negative-instruction density, structural duplication) and present the result as a rubric score, not a computed formula value.
- **Symptoms**: The refactor plan or scorecard cites a specific U_t number, or attaches "mutual information" or "Shannon entropy" to a specific computed value.
- **Detection Pattern**: Scorecard or report text pairing the symbol U_t, "mutual information," or "Shannon entropy" with a specific numeric value presented as measured.

---

## Missing Required Reference File

- **Id**: missing-required-reference-file
- **Summary**: An audited skill lacks one of patterns.md, sharp_edges.md, or validations.md, and the audit proceeds without flagging it.
- **Severity**: critical
- **Situation**: During the PEV-M structural compliance check.
- **Why**: These three files are always required regardless of skill size; skipping the check on a small or simple skill treats "simple" as an exemption PEV-M does not grant.
- **Solution**: Check for all three files on every audit and record each one's presence or absence explicitly in the scorecard before assessing any other axis.
- **Symptoms**: A scorecard rates a skill as compliant despite one of the three always-required files being absent from the audited folder.
- **Detection Pattern**: Skill folder listing missing patterns.md, sharp_edges.md, or validations.md while the compliance score for that axis reads as passing.

---

## Interactions Over-Requirement

- **Id**: interactions-over-requirement
- **Summary**: skill-auditor flags a skill's missing interactions.md as a deficiency even though the skill has no human-in-the-loop behavior.
- **Severity**: medium
- **Situation**: During the PEV-M structural compliance check, specifically the interactions.md requirement.
- **Why**: interactions.md is conditional on detected human-in-the-loop behavior; treating it as universally required contradicts the audited skill's actual design and adds scaffolding it does not need.
- **Solution**: Scan the audited skill's SKILL.md and references for mid-task prompts, multi-turn confirmation, or gated state transitions before deciding whether interactions.md is required; omit the requirement when none are found.
- **Symptoms**: A scorecard deducts points for a missing interactions.md on a skill whose own content shows no interactive checkpoints.
- **Detection Pattern**: Scorecard deduction referencing "missing interactions.md" attached to a skill whose SKILL.md and references contain no prompt, confirmation, or gated-transition language.

---

## Unapproved Migration

- **Id**: unapproved-migration
- **Summary**: skill-auditor modifies the audited skill's files before the user has approved the refactor plan.
- **Severity**: critical
- **Situation**: Between presenting the refactor plan and receiving the user's response.
- **Why**: Editing ahead of approval collapses the plan-then-migrate sequence into a single step and removes the user's opportunity to redirect scope before files change.
- **Solution**: Hold every file write to the audited skill's folder until the user's response is an explicit approval; route any other response to a plan revision instead.
- **Symptoms**: Files inside the audited skill's folder change state before the user has replied to the presented refactor plan.
- **Detection Pattern**: A file-write action targeting the audited skill's folder occurring earlier in the transcript than the user's approval message.

---

## Fictional Runtime Machinery Recommended

- **Id**: fictional-runtime-machinery
- **Summary**: skill-auditor's refactor plan or migrated output includes tokens or tags (`[AWAIT_HUMAN]`, `<state_context>`, `STOP_AND_PROMPT`, `GO_PROCEED`, a `#$` state key) that no part of the agent runtime interprets.
- **Severity**: high
- **Situation**: While drafting or applying an interactions.md migration.
- **Why**: PEV-M's original interactions.md blueprint read as if a state-machine interpreter executes these tokens; no such interpreter exists in the runtime, so the tokens are inert text the model must independently decide to honor — identical in effect to plain prose, but costlier in tokens and misleading about how the skill actually works.
- **Solution**: Express interaction mechanics using the Grounded Interaction Mechanics pattern — turn-ending waits, the platform's real blocking-question tool, and plain Proceed-When/Pause-When conditions.
- **Symptoms**: The refactor plan or migrated skill text contains `[AWAIT_HUMAN]`, `<state_context>`, `STOP_AND_PROMPT`, `GO_PROCEED`, or a `#$` state-key pattern.
- **Detection Pattern**: Any of the literal strings `[AWAIT_HUMAN]`, `<state_context>`, `STOP_AND_PROMPT`, `GO_PROCEED`, or a `<skill>#$` token appearing in SKILL.md or references/*.md.

---

## Numbered Principle Label Leak

- **Id**: numbered-principle-label-leak
- **Summary**: A migrated or drafted Principles list shows literal `P1 (...)`, `P2 (...)`-style prefixes instead of a plain bolded name.
- **Severity**: medium
- **Situation**: While drafting or migrating a skill's SKILL.md Principles section.
- **Why**: The P-number/category label is internal selection-and-ordering scaffolding; rendering it verbatim leaks that scaffolding into text meant to read as elegant, human-facing prose.
- **Solution**: Use the four categories only to decide which principles to include and what order to present them in; render each principle as a short bold descriptive name followed by its instruction, with no numbered label.
- **Symptoms**: A Principles bullet begins with a literal `P1`, `P2`, `P3`, or `P4` prefix.
- **Detection Pattern**: A Principles-section bullet matching `^\s*-\s+\*\*P[1-4]`.

---

## Report Written Into Audited Files

- **Id**: report-written-into-audited-files
- **Summary**: The audit or refactor plan gets written directly into the audited skill's own SKILL.md or reference files instead of a separate report file.
- **Severity**: critical
- **Situation**: During the Plan phase, when saving the refactor plan to disk.
- **Why**: Writing findings into the target files themselves mutates the skill before approval and overwrites the original content the user needs to diff against.
- **Solution**: Always write the plan to a new, separate file inside the audited skill's folder (e.g. `<skill-name>-audit-report.md`); leave the audited skill's own SKILL.md and references/*.md in read-only use until Phase 03 (Migrate) begins after approval.
- **Symptoms**: SKILL.md or a references/*.md file inside the audited skill's folder changes state during the Plan phase, before the user has approved anything.
- **Detection Pattern**: A write/edit action targeting a file inside the audited skill's own folder occurring during the Audit or Plan phase rather than Migrate.

---

## Progressive Disclosure Violation

- **Id**: progressive-disclosure-violation
- **Summary**: SKILL.md contains inlined pattern, sharp-edge, validation, or interaction content that belongs in its dedicated reference file.
- **Severity**: medium
- **Situation**: During the PEV-M structural compliance check of SKILL.md.
- **Why**: Loading all detail at the SKILL.md level defeats progressive disclosure — deep reference content should load lazily only when the agent reaches that execution state, keeping every invocation's base context small.
- **Solution**: Move the inlined content to its correct reference file (patterns.md, sharp_edges.md, validations.md, or interactions.md) and leave SKILL.md to frontmatter, Identity, Principles, and Reference System Usage only.
- **Symptoms**: SKILL.md contains pattern examples, failure-mode write-ups, validation rules, or phase-by-phase interaction blocks instead of a pointer to them.
- **Detection Pattern**: SKILL.md body content, outside Identity, Principles, and Reference System Usage, matching the patterns.md/sharp_edges.md/validations.md/interactions.md element-blueprint shapes.

---

## Behavior Loss During Migration

- **Id**: behavior-loss-during-migration
- **Summary**: The migrated, PEV-M-compliant skill omits an instruction, feature, or effect present in the original.
- **Severity**: critical
- **Situation**: During execution of an approved refactor script.
- **Why**: Moving content between files — collapsing verbose passages, relocating misplaced content into the correct PEV-M file — can silently drop a clause when the mapping from old to new location is not tracked explicitly.
- **Solution**: Build an explicit before/after map from every original instruction to its new PEV-M destination as part of the refactor script, and check the migrated skill's full behavior set against the original before presenting the migration as complete.
- **Symptoms**: A behavior, trigger condition, or edge case present in the pre-migration skill has no corresponding instruction anywhere in the post-migration file set.
- **Detection Pattern**: An instruction or conditional clause present in the original skill's files with no matching phrase or paraphrase anywhere in the migrated files.

---
