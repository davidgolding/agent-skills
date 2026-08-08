# TCG Designer Validations

This document defines the validations used by tcg-designer.

## Mandatory Core Loop Validation

- **Id**: core-loop-validated
- **Severity**: error
- **Type**: semantic
- **Pattern**: Proposing progression systems, meta-economies, or card art/lore additions before the 30-second micro loop is validated as intrinsically satisfying.
- **Message**: The 30-second micro loop must be validated as engaging before designing macro progression or meta-systems.
- **Fix Action**: Isolate the 30-second core loop, evaluate it under the Gray Box test, and verify engagement without rewards before adding meta-layers.
- **Applies To**:
    - card game mechanics proposal
    - core loop evaluation

---

## Meaningful Decisions Verification

- **Id**: meaningful-decisions-present
- **Severity**: error
- **Type**: semantic
- **Pattern**: Card or mechanic designs where a single dominant play strategy renders all alternative choices sub-optimal across all contexts.
- **Message**: Every player choice must involve situational trade-offs, incomplete information, or context-dependent value rather than a dominant strategy.
- **Fix Action**: Adjust card stats, resource costs, or situational triggers so competing choices excel under distinct game states.
- **Applies To**:
    - card design
    - deck building mechanics

---

## Playtest-Grounded Claims Verification

- **Id**: playtest-grounded-claims
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Game design decisions justified by designer intent or hypothetical ideal play rather than empirical playtest observation.
- **Message**: Playtest findings must guide design adjustments; designer intent is invisible to players.
- **Fix Action**: Reframe the design rationale around observed player behavior during playtests rather than expected player compliance.
- **Applies To**:
    - playtest analysis
    - rule adjustments

---

## Skill Floor and Ceiling Balance Check

- **Id**: skill-floor-ceiling-balanced
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Mechanics featuring high execution barriers with low strategic mastery ceilings, or complex rules producing shallow decisions.
- **Message**: Aim for low skill floors (accessible entry) paired with high skill ceilings (room for emergent mastery).
- **Fix Action**: Simplify input requirements and initial rules while expanding situational interactions and emergent combo space.
- **Applies To**:
    - mechanic specifications
    - rulebook drafts

---

## Affirmative Instruction Alignment

- **Id**: affirmative-instruction-alignment
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `\bnever\b`
    - `\bdon't\b`
    - `\bdo not\b`
    - `\bavoid\b`
    - `\bmust not\b`
    - `\bshould not\b`
- **Message**: Instructions should name required actions and their trigger conditions rather than prohibitions.
- **Fix Action**: Rewrite negative prohibitions into positive instructions that direct the agent toward the correct evaluation step.
- **Applies To**:
    - SKILL.md
    - references/*.md
