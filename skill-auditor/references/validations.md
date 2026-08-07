# Skill Auditor Validations

This document defines the validations used by skill-auditor.

## No Literal Formula Scoring

- **Id**: no-literal-formula-scoring
- **Severity**: error
- **Type**: semantic
- **Pattern**: Scorecard or refactor plan text pairing a specific numeric value with PEV-M's U_t formula, or presenting "mutual information" or "Shannon entropy" as measured rather than illustrative.
- **Message**: The token-efficiency score must come from heuristic signals, not a literal computation of the U_t formula.
- **Fix Action**: Replace the formula-derived value with a score based on redundancy, negative-instruction density, and structural duplication counts, and remove any language implying the formula was computed.
- **Applies To**:
    - refactor plan output
    - scorecard output

---

## Required Reference Files Present

- **Id**: required-reference-files-present
- **Severity**: error
- **Type**: schema
- **Pattern**: Audited skill folder missing one or more of `references/patterns.md`, `references/sharp_edges.md`, `references/validations.md`.
- **Message**: patterns.md, sharp_edges.md, and validations.md are required for every audited skill regardless of size.
- **Fix Action**: Add the missing file(s) to the refactor plan's change script, populated per PEV-M's file-layout and element-blueprint rules for that file.
- **Applies To**:
    - audited skill folder structure

---

## Interactions File Conditional on Detected Interaction

- **Id**: interactions-conditional
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Audited skill's SKILL.md or references contain mid-task prompts, multi-turn confirmation language, or gated state transitions, but `references/interactions.md` is absent.
- **Message**: This skill shows human-in-the-loop behavior; add interactions.md to house its Interaction Rules, Execution Flow, and Handoff Protocols.
- **Fix Action**: Add `references/interactions.md` to the change script, structured per PEV-M's interactions template, and move any interaction logic embedded in other files into it.
- **Applies To**:
    - audited skill folder structure

---

## Negative-Polarity Instruction Detected

- **Id**: negative-polarity-instruction
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `\bnever\b`
    - `\bdon't\b`
    - `\bdo not\b`
    - `\bavoid\b`
    - `\bmust not\b`
    - `\bshould not\b`
- **Message**: This instruction is phrased as a prohibition rather than an action to take.
- **Fix Action**: Rewrite the instruction to name the required action and its trigger condition, preserving the original constraint's scope, per the Affirmative Rewrite pattern.
- **Applies To**:
    - SKILL.md
    - references/*.md

---

## Approval Gate Before File Mutation

- **Id**: approval-gate-before-mutation
- **Severity**: error
- **Type**: semantic
- **Pattern**: A write or edit action targeting the audited skill's folder occurring before an explicit user approval message in the session transcript.
- **Message**: The audited skill's files must stay unchanged until the user approves the refactor plan.
- **Fix Action**: Revert or withhold the change, re-present the refactor plan, and wait for explicit approval before writing to the audited skill's folder.
- **Applies To**:
    - audited skill folder (all files)

---

## Behavior Parity Between Original and Migrated Skill

- **Id**: behavior-parity-check
- **Severity**: error
- **Type**: semantic
- **Pattern**: An instruction, trigger condition, or edge case present in the original skill's files with no corresponding phrase or paraphrase anywhere in the migrated file set.
- **Message**: A behavior from the original skill appears to be missing from the migrated version.
- **Fix Action**: Locate the correct PEV-M destination file for the missing behavior and add it back before presenting the migration as complete.
- **Applies To**:
    - migrated skill folder (all files)

---
