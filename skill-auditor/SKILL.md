---
name: skill-auditor
description: Audit an existing agent skill against the Pattern-Edge-Validation Matrix (PEV-M) standard, scoring structural compliance, affirmative-language quality, identity-language freedom, description discoverability, and token efficiency, then migrate it to full PEV-M compliance after approval. Use when the user wants to audit a skill, check PEV-M compliance, review a skill folder for best practices, or refactor an existing skill into the PEV-M architecture.
---

# Skill Auditor

## Mandate

Audit one agent skill folder per invocation against the Pattern-Edge-Validation Matrix (PEV-M) standard, then migrate it into compliance once the user approves the plan. Score five axes: PEV-M structural compliance, affirmative-language quality, identity-language freedom, description discoverability, and token efficiency. Ground every judgment in `references/patterns.md`, `references/sharp_edges.md`, `references/validations.md`, and `references/interactions.md`. A correct audit names each failing rule by its Id, cites the file and the line it fires on, and proposes a concrete rewrite; a correct migration applies the approved script while preserving every behavior of the original skill.

## Principles

- **PEV-M Fidelity**: Ground every structural judgment in the rules defined across `references/patterns.md`, `references/sharp_edges.md`, and `references/validations.md` — the full PEV-M structural spec lives there, not in any external standard document — and treat those rules as fixed, never as a target of revision during an audit.
- **Full-Structure Requirement**: Require `patterns.md`, `sharp_edges.md`, and `validations.md` for every audited skill regardless of size, and require `interactions.md` whenever the audited skill shows human-in-the-loop behavior — mid-task prompts, multi-turn confirmation, or gated state transitions.
- **Behavior Preservation**: Migrate every behavior, feature, instruction, and effect of the original skill into its PEV-M-compliant form; treat a compliant structure that drops functionality as a failed refactor, not a finished one.
- **Identity-Free Instruction**: Route persona and credential language — assigned roles, career histories, claimed expertise levels — into the explicit criteria it stands in for, since audited skills perform discriminative work where personas measurably cost accuracy, and hold every Mandate section to naming its decision scope, criteria source, and success condition.
- **Discoverable Description**: Measure the audited skill's frontmatter `description` in characters, treating the 1024-character specification cap as an error boundary and the 200–500 range as the band where a description carries enough trigger cues to be discovered without bloating the always-loaded skill index.
- **Affirmative Routing**: Rewrite negative-polarity instructions ("Never," "Don't," "Do not," "Avoid," "must not," "should not") into affirmative instructions that route the agent toward the correct action — including exception and validation paths — while preserving the original constraint's scope.
- **Grounded Interaction Mechanics**: Express every interaction rule through mechanics the runtime actually performs — turn-ending waits, the platform's blocking-question tool, plain Proceed-When/Pause-When conditions — routing away from tokens or tags dressed as pseudo-code that nothing executes.
- **Heuristic Token Scoring**: Score token efficiency through checkable signals — redundant phrasing, repeated instructions across files, negative-instruction density, structural duplication — routing the score through those signals instead of PEV-M's $U_t$ formula.
- **Plan Before Migration**: Present the executive summary, scorecard, and change script as a new, separate report file inside the audited skill's folder, and hold every edit to the audited skill's existing files until the user approves, revises, or cancels.
- **Single-Skill Scope**: Audit and refactor one skill folder per invocation.

## Reference System Usage

You must ground your response in the provided reference files, treating them as the absolute mathematical source of truth for this domain:

- **For Creation [State 01]**: Always consult `references/patterns.md`. This file dictates *how* components must be structured. Ignore generic boilerplate choices if a specific pattern exists here.
- **For Diagnosis [State 02]**: Always consult `references/sharp_edges.md`. This file indexes critical regression modes and failure metrics. Use it to map risks during execution.
- **For Review [State 03]**: Always consult `references/validations.md`. This file contains strict syntactic and schema rules. Use it to force a rigorous chain-of-verification loop before emitting state output.
- **For Interacting [State 04]**: Always consult `references/interactions.md`. This file governs human-in-the-loop state alignment, boundary negotiations, and environment handshake procedures.
