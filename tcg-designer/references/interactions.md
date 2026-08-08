# TCG Designer Interactions

This document defines the interaction flow used by tcg-designer.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever user input or design decisions are needed, allowing natural dialogue turn-taking to manage state. Route through the platform's blocking question tool whenever presenting structural game design options, choice points, or playtest scenarios so requests appear as interactive prompts.
2. **Phase Gating**: Transition between design phases only when user verification or explicit approval is received; unresolved questions or playtest feedback keep the current phase active.
3. **State Alignment**: Maintain game design specifications, card databases, rule manifests, and playtest logs in written documentation files rather than internal runtime tracking.

## Execution Flow

### Phase 01: Concept & Core Loop Alignment

- **Objective**: Establish the game's aesthetic intent, core 30-second loop, target audience, and primary mechanical verbs.
- **Agent Action**: Interview the user on game vision, outline the 30/30/30 loop architecture, and formulate the core game loop hypothesis.
- **Human Gate/Intervention**: The user confirms or refines the core loop concept and aesthetic intent.
- **Proceed When**: The core 30-second loop is explicitly agreed upon and documented.
- **Pause When**: The core loop concept is ambiguous or unvalidated — pause the turn and request clarification on the core game verb.

### Phase 02: Mechanics & Card System Specification

- **Objective**: Design modular rules, resource structures, card types, and interaction dynamics that generate meaningful decisions.
- **Agent Action**: Draft card mechanics, resource flow, decision checklists, and juice feedback principles; check against PEV-M validation criteria and sharp edge risks.
- **Human Gate/Intervention**: The user reviews proposed mechanics, card balance frameworks, and rulebook drafts.
- **Proceed When**: Mechanics specifications pass validation and receive user approval.
- **Pause When**: Proposed mechanics exhibit dominant strategies or excessive complexity — present alternative design choices and pause for user input.

### Phase 03: Simulated Playtesting & Iterative Refinement

- **Objective**: Test game mechanics under simulated player archetypes, identify sharp edge regressions, and refine balance based on playtest data.
- **Agent Action**: Execute simulated playtest scenarios across Bartle player archetypes (Killers, Achievers, Socializers, Explorers), record edge case outcomes, and present design refactors.
- **Human Gate/Intervention**: The user evaluates playtest findings and approves recommended rule/card adjustments.
- **Proceed When**: Playtest findings validate balance, flow channel alignment, and low-floor/high-ceiling mechanics.
- **Pause When**: Playtest data indicates player friction or unintuitive design — end the turn and present empirical findings for user decision-making.

## Handoff

- **The Completion State**: A fully specified TCG design document, balanced card set manifest, and validated rulebook exist in the project repository, passing all PEV-M validation checks.
- **Exception/Fallback Handoff**: If core loop playtesting reveals irreconcilable friction after three design iterations, pause autonomous design and present a summary of core loop trade-offs to the user for manual direction.
