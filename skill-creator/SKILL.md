---
name: skill-creator
description: Create new agentic skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

## Mandate

Guide one agent skill through its lifecycle per invocation: create it from scratch, modify an existing one, or measure how it performs. Decide two things — what the skill should contain, established with the user through the brainstorm in `references/interactions.md`, and whether a draft meets the standard, judged against `references/patterns.md`, `references/sharp_edges.md`, and `references/validations.md`. Ground every judgment in those files rather than in generic skill-writing convention. A correct result is a skill whose files match the templates in `references/handoff.md`, whose description triggers on its intended prompts and holds against near-miss negatives, and whose full behavior the user could predict before running it.

## Principles

- **Interactive Elicitation**: Brainstorm with the user through structured, progressive dialogue — one question at a time — to establish the problem, the candidate approaches, and the requirements before designing or modifying any skill.
- **Progressive Disclosure**: Organize every skill into three loading layers (metadata → SKILL.md → bundled resources), keeping context limited to what the current layer needs.
- **Description as Contract**: Treat the frontmatter description as the trigger mechanism, holding it assertive and specific, and validate it against a real eval set that includes near-miss negatives.
- **Explanatory Instruction**: State why an instruction exists alongside what it requires, so the reasoning survives into situations the instruction did not anticipate.
- **Generalize Over Fit**: Use evals as a development instrument that measures whether a skill generalizes; keep the eval set as the diagnostic and the skill's real population as the target.
- **Design for the Thousandth Invocation**: Treat the population of future users as the design constraint, letting the three test cases in front inform the design rather than define it.
- **Shared Script Extraction**: Watch for behavior that converges across eval runs and extract it into a bundled script once the pattern holds.
- **Iteration as Architecture**: Run the draft → test → review → improve loop as the method itself, treating each pass as the intended path to a finished skill.
- **Behavioral Legibility**: Keep a skill's full behavior legible to the user in advance; treat surprise at runtime as a defect to fix.
- **Human Review Before Automated Iteration**: Route each round of automated iteration through human review before it proceeds.
- **Silence Stops Iteration**: Stop iterating once user feedback goes silent.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Brainstorming:** Always consult **`references/interactions.md`**. This file dictates how to interact, clarify requirements, and explore approaches with the user when starting a new skill or making significant changes.
* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

The brainstorm workflow in `references/interactions.md` loads four further files at the phase that needs each one:

* **For Scoping (Phase 2.5):** Always consult **`references/synthesis_summary.md`** before composing the synthesis. It defines the two-stage shape, the Path A / Path B gate, the four scoping sections and their keep tests, and the tier-aware bullet budget.
* **For Requirements Capture (Phase 3):** Always consult **`references/requirements_capture.md`**. It supplies the `temp-requirements.md` template, formatting rules, and completeness checks.
* **For Visual Aids:** Always consult **`references/visual_communication.md`** when a requirements document may warrant a diagram or comparison table. It governs when a visual earns its place and which format to use.
* **For Handoff (Phase 4):** Always consult **`references/handoff.md`**. It supplies the next-step option logic, the skill-file templates in `templates/`, the cleanup instructions, and the closing summary format.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.