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

## No Fictional Runtime Tokens

- **Id**: no-fictional-runtime-tokens
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `\[AWAIT_HUMAN\]`
    - `<state_context>`
    - `STOP_AND_PROMPT`
    - `GO_PROCEED`
    - `#\$\[`
- **Message**: This text uses runtime-machinery notation the agent runtime does not interpret.
- **Fix Action**: Rewrite using the Grounded Interaction Mechanics pattern — turn-ending waits, the platform's real blocking-question tool, and plain Proceed-When/Pause-When conditions.
- **Applies To**:
    - SKILL.md
    - references/interactions.md

---

## No Numbered Principle Labels

- **Id**: no-numbered-principle-labels
- **Severity**: warning
- **Type**: regex
- **Pattern**: `^-\s+\*\*P[1-4]`
- **Message**: This principle is rendered with a literal P-number label instead of a plain descriptive name.
- **Fix Action**: Replace the P-number prefix with a short bold descriptive name; use the four categories only to choose content and order, not to label output.
- **Applies To**:
    - SKILL.md

---

## Plan Written to Dedicated Report File

- **Id**: plan-written-to-dedicated-file
- **Severity**: error
- **Type**: semantic
- **Pattern**: A write or edit action modifying SKILL.md or any references/*.md file inside the audited skill's own folder during the Audit or Plan phase.
- **Message**: The refactor plan must be written to a new, separate report file, not into the audited skill's own files.
- **Fix Action**: Write the executive summary, scorecard, and change script to `<skill-name>-audit-report.md` inside the audited skill's folder instead, and leave the audited skill's existing files untouched until Migrate.
- **Applies To**:
    - audited skill folder (all files)

---

## SKILL.md Required Shape

- **Id**: skill-md-required-shape
- **Severity**: error
- **Type**: schema
- **Pattern**: YAML frontmatter missing `name` or `description`; missing H1 matching `name` in Title Case; missing `## Mandate`, `## Principles`, or `## Reference System Usage` headings, or out of that order; Mandate section omitting the decision scope, the criteria source, or the success condition; Reference System Usage missing the grounding directive or a bullet for any reference file the skill actually has.
- **Message**: SKILL.md must contain frontmatter (name, description), an H1 matching the skill name, and Mandate, Principles, and Reference System Usage sections in that order.
- **Fix Action**: Add or reorder the missing piece, following the SKILL.md template: frontmatter, then H1, then Mandate (the unit of work, the axes judged, the reference files those judgments ground in, and what a correct output contains), then Principles (category-ordered, label-free), then Reference System Usage (grounding directive plus one bullet per reference file).
- **Applies To**:
    - SKILL.md

---

## Patterns File Required Shape

- **Id**: patterns-md-required-shape
- **Severity**: error
- **Type**: schema
- **Pattern**: patterns.md missing its `## Patterns` or `## Anti-Patterns` heading; a pattern entry missing Name/When/Example; an anti-pattern entry missing Name/Why/Instead; entries not separated by a horizontal rule.
- **Message**: patterns.md must have Patterns and Anti-Patterns sections, with each pattern carrying Name/When/Example and each anti-pattern carrying Name/Why/Instead, separated by `---`.
- **Fix Action**: Add the missing heading or field, or insert the missing `---` separator between entries.
- **Applies To**:
    - references/patterns.md

---

## Sharp Edges File Required Shape

- **Id**: sharp-edges-md-required-shape
- **Severity**: error
- **Type**: schema
- **Pattern**: sharp_edges.md entry missing any of Id/Summary/Severity/Situation/Why/Solution/Symptoms/Detection Pattern; Severity value outside {critical, high, medium, low}; entries not separated by `---`.
- **Message**: Every sharp edge needs Id, Summary, Severity, Situation, Why, Solution, Symptoms, and Detection Pattern, with Severity one of critical/high/medium/low.
- **Fix Action**: Add the missing field or correct the Severity value; insert the missing `---` separator between edges.
- **Applies To**:
    - references/sharp_edges.md

---

## Validations File Required Shape

- **Id**: validations-md-required-shape
- **Severity**: error
- **Type**: schema
- **Pattern**: validations.md entry missing any of Id/Severity/Type/Pattern/Message/Fix Action/Applies To; Severity value outside {error, warning}; Type value outside {regex, schema, semantic, syntax}; entries not separated by `---`.
- **Message**: Every validation needs Id, Severity, Type, Pattern, Message, Fix Action, and Applies To, with Severity one of error/warning and Type one of regex/schema/semantic/syntax.
- **Fix Action**: Add the missing field or correct the Severity/Type value; insert the missing `---` separator between validations.
- **Applies To**:
    - references/validations.md

---

## Interactions File Required Shape

- **Id**: interactions-md-required-shape
- **Severity**: error
- **Type**: schema
- **Pattern**: interactions.md missing `## Interaction Rules`, `## Execution Flow`, or `## Handoff`; a phase block missing Objective/Agent Action/Human Gate-Intervention/Proceed When/Pause When; Handoff missing Completion State or Exception/Fallback Handoff.
- **Message**: interactions.md must have Interaction Rules, Execution Flow (phase blocks with Objective/Agent Action/Human Gate-Intervention/Proceed When/Pause When), and Handoff (Completion State plus Exception/Fallback Handoff) sections.
- **Fix Action**: Add the missing section or field, following the grounded interactions.md template — see no-fictional-runtime-tokens for what to avoid.
- **Applies To**:
    - references/interactions.md

---

## SKILL.md Progressive Disclosure

- **Id**: skill-md-progressive-disclosure
- **Severity**: warning
- **Type**: semantic
- **Pattern**: SKILL.md body sections beyond frontmatter, Mandate, Principles, and Reference System Usage, or reference-file-shaped content (pattern, sharp-edge, validation, or interaction element blueprints) appearing inline in SKILL.md.
- **Message**: SKILL.md should contain only frontmatter, Mandate, Principles, and Reference System Usage — deeper content belongs in its dedicated reference file.
- **Fix Action**: Move the inlined content into the matching reference file and replace it in SKILL.md with the standard Reference System Usage pointer.
- **Applies To**:
    - SKILL.md

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

## Persona or Identity Language Detected

- **Id**: persona-identity-language
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `^You are an?\b`
    - `\bAct as an?\b`
    - `\bAs an? (expert|experienced|seasoned|veteran)\b`
    - `\bworld-class\b`
    - `\byears of experience\b`
    - `\bwho has (seen|spent|worked)\b`
    - `\bYou have (done|built|shipped|audited)\b`
    - `\b(Imagine|Pretend) (you|that you)\b`
- **Message**: This text assigns an identity instead of stating criteria; personas cost accuracy on the discriminative work — judging, classifying, verifying — that most skills perform.
- **Fix Action**: Rewrite the passage per the Task-Criteria Framing pattern, converting the implied competence into the explicit decision scope, criteria source, and success condition it was standing in for.
- **Applies To**:
    - SKILL.md
    - references/*.md

---

## Mandate Section Is Task-Framed

- **Id**: mandate-section-task-framed
- **Severity**: error
- **Type**: semantic
- **Pattern**: A `## Mandate` section describing who the agent is, what it has experienced, or how skilled it is, rather than naming the decision scope, the criteria source, and the condition that makes an output correct.
- **Message**: The Mandate section states the task the skill performs and the criteria it performs it against, not an identity the agent adopts.
- **Fix Action**: Rewrite the section per the Task-Criteria Framing pattern: name the unit of work, the axes judged, the reference files the judgments ground in, and what a correct output contains.
- **Applies To**:
    - SKILL.md

---

## Description Within Specification Cap

- **Id**: description-length-over-cap
- **Severity**: error
- **Type**: schema
- **Pattern**: Frontmatter `description` value exceeding 1024 characters.
- **Message**: The Agent Skills specification caps `description` at 1024 characters; past the cap the skill fails to register and never triggers, while still appearing installed.
- **Fix Action**: Cut the description to the two clauses auto-discovery uses — what the skill does and when to use it — and move the procedural detail it absorbed into SKILL.md or the matching reference file.
- **Applies To**:
    - SKILL.md

---

## Description Within Discovery Band

- **Id**: description-length-out-of-band
- **Severity**: warning
- **Type**: schema
- **Pattern**: Frontmatter `description` value shorter than 200 characters or longer than 500 characters.
- **Message**: Under 200 characters a description carries too few trigger cues for reliable auto-discovery; over 500 it pays index cost in every session without improving the trigger decision.
- **Fix Action**: Restate the description as one clause naming what the skill does and one clause naming when to use it, landing the total between 200 and 500 characters.
- **Applies To**:
    - SKILL.md

---
