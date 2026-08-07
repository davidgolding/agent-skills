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
