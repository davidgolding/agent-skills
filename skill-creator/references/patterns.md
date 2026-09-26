# Skill Creator Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by skill-creator.

## Patterns

- **Name**: Three-Layer Loading Pattern
- **Description**: Organize the skill's file layout into three distinct layers: triggering metadata (frontmatter in `SKILL.md`), core instructions and mandate (body of `SKILL.md`), and detailed references/scripts/examples in subdirectories.
- **When**: Designing any new skill to keep the initial agent context lightweight and avoid overloading the context window during triggers.
- **Example**:
```
    - Metadata Layer: Trigger description in frontmatter
    - Core Instruction Layer: `SKILL.md` containing Mandate, Principles, and Reference System Usage
    - Resource Layer: `references/patterns.md`, `references/sharp_edges.md`, `scripts/run_eval.py`
```

---

- **Name**: Assertive Trigger Description
- **Description**: Write the YAML frontmatter description as one clause naming what the skill does and one clause naming when to use it, choosing specific trigger terms over generic ones and landing the total between 200 and 500 characters — enough trigger cues for discovery without paying index cost in every session. Treat 1024 characters as a hard cap.
- **When**: Defining the trigger contract in `SKILL.md` frontmatter.
- **Example**:
```
    description: Create new agentic skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch or edit or optimize an existing skill.
```
 
---

- **Name**: Rigid Eval-Driven Iteration Loop
- **Description**: Develop a test suite consisting of positive and negative triggering prompts, plus execution correctness checks. Run these tests automatically after any modification to measure performance improvement.
- **When**: Optimizing prompts, adding features, or debugging failures in a skill.
- **Example**:
```
    Test inputs:
      - Positive: "Help me write a git commit skill"
      - Negative (Near-miss): "Write a git commit for my current changes" (triggers a git commit skill, not skill-creator)
    Metrics: Trigger rate (%), task success rate (%), execution latency (ms).
```

---

- **Name**: Behavioral Legibility ("No Surprise")
- **Description**: Always outline planned tool executions (commands, file modifications) to the user first. Obtain explicit confirmation before running mutating commands or side-effects.
- **When**: Executing actions on the user's codebase.
- **Example**: "I will now create the script `scripts/deploy.sh` and run it. Do you approve?"

---

- **Name**: Shared Helper Scripts
- **Description**: Extract logic that involves complex CLI invocations, calculations, or multi-step environment setups from the prompt into a script. Bundle the script inside the skill's `scripts/` directory.
- **When**: The same sequence of terminal commands or processing logic is executed repeatedly across different runs.
- **Example**: Instead of teaching the agent how to parse and average test runs in a prompt, write `scripts/average_runs.py` and have the agent execute `python3 scripts/average_runs.py`.

---

- **Name**: Progressive Output Disclosure
- **Description**: Present high-level summaries and action items in the direct chat response. Keep detailed code, long lists, and data dumps inside markdown artifacts or collapsible sections.
- **When**: Formatting responses that contain code diffs, logs, or multi-step reports.
- **Example**: "I have updated the implementation plan. You can view the full file here: [implementation_plan.md](file:///path/to/plan.md). Key change: added validation for absolute paths."

---

- **Name**: Design for the Thousandth Invocation
- **Description**: Design skills with robust error handling, generalized paths, and parameterization so they can run repeatedly and reliably across different users' environments.
- **When**: Writing any instructions, paths, or code scripts within a skill.
- **Example**:
    - Avoid hardcoding `/Users/user/repo` -> Use `cwd` or environment-relative paths.
    - Check if a file exists before attempting to read it.
    - Handle command failures and log readable errors.

---

- **Name**: Interactive Dialogue Protocol
- **Description**: Brainstorm requirements using one question at a time, leveraging platform-native blocking questions where possible.
- **When**: Engaging in cooperative scoping or clarifying ambiguous developer requirements.
- **Example**:
    - Good: Asking "Should X be a rule property or filter?" and presenting options using ask_user tool.
    - Bad: Stacking three questions in one chat message.

---

- **Name**: Two-Stage Scoping Synthesis
- **Description**: Produce an internal three-bucket scope draft (Stated / Inferred / Out of scope) first, then derive a conversational scoping synthesis to confirm with the user.
- **When**: Summarizing decisions made in a brainstorming session before writing a requirements doc.
- **Example**: Formulate the internal draft in agent thoughts, then output: "Based on our dialogue, here's the scope I'm proposing..." with Trade-offs, Deferred, and Call-outs.

---

- **Name**: Conversational Scope Bullets
- **Description**: Write scope bullets that are 1-2 lines maximum and focus entirely on product shape rather than code-level implementation details.
- **When**: Writing the scoping synthesis or summarizing requirements.
- **Example**:
    - Good: "Rule-delete silently loses pause state — confirm no warning needed"
    - Bad: "Use existing rule entity to store pause, adding a database column is_paused"

---

- **Name**: Temporary Intermediate Artifacts
- **Description**: Use a single, un-nested temporary file in the workspace root (e.g., `temp-requirements.md`) to capture intermediate requirements or states, deleting it immediately after drafting/writing the final skill files to avoid repository clutter.
- **When**: Writing temporary documents during brainstorming or planning before generation is completed.
- **Example**: Write the brainstormed requirements directly to `temp-requirements.md` in the workspace root, compile the skill, and delete `temp-requirements.md` once complete. Do not create nested folders (like `docs/brainstorms/`) for temporary files.

---

- **Name**: Standardized Skill Structure Pattern
- **Description**: Output newly created skill files using standardized templates to ensure structured, consistent layout in `SKILL.md`, `references/patterns.md`, `references/sharp_edges.md`, and `references/validations.md`.
- **When**: Drafting, writing, or editing any agent skill's files.
- **Example**: Generate `SKILL.md` containing name/description frontmatter, a Level-1 title heading, and Level-2 headings for "Mandate", "Principles", and "Reference System Usage" (verbatim), in that order. Generate reference markdown files (`patterns.md`, `sharp_edges.md`, `validations.md`, plus `interactions.md` when the skill has human-in-the-loop behavior) with their standard heading layouts and required bullet key attributes, so the result passes the structure rules in this file's companion `references/validations.md`.

---

- **Name**: Task-Criteria Mandate
- **Description**: Frame the generated `SKILL.md`'s Mandate section as the task and its criteria — the unit of work, the decisions judged, the reference files those judgments ground in, and what a correct output contains — converting any implied role or expertise into those explicit criteria.
- **When**: Drafting the Mandate section of any generated `SKILL.md`, or rewriting a passage that assigns the agent an identity.
- **Example**:
```
    Before: "You are a seasoned release engineer who has shipped hundreds of changelogs."
    After:  "Draft one changelog entry per invocation from the merged PRs since the last tag. Judge each PR's user-facing impact against references/patterns.md. A correct entry groups changes by type and links every PR."
```

---

- **Name**: Conditional Interactions File
- **Description**: Generate `references/interactions.md` from `templates/interactions_template.md` only when the requirements show human-in-the-loop behavior — mid-task prompts, multi-turn confirmation, approval gates, or gated state transitions — and add its "For Interacting" bullet to Reference System Usage.
- **When**: Deciding the generated skill's file set during Phase 4 drafting.
- **Example**: A skill that presents a plan and waits for approval before editing files gets `interactions.md` with Plan and Apply phases; a skill that formats a document in one pass gets only the three core reference files.

---

## Anti-Patterns

- **Name**: Fuzzy Trigger Description
- **Description**: Using broad, generic, or conversational language in the YAML frontmatter description.
- **Why**: Causes the router to trigger the skill for unrelated queries (false positives) or fail to activate it for relevant tasks (false negatives).
- **Instead**: Use specific, assertive language naming what the skill does and when to use it, held to the 200–500 character discovery band (Assertive Trigger Description).

---

- **Name**: Monolithic Context Overload
- **Description**: Placing entire JSON schemas, code templates, or long reference documents directly inside the core `SKILL.md` file.
- **Why**: Bloats the agent's context window on every invocation, wasting tokens, raising latency, and diluting instruction adherence.
- **Instead**: Delegate deep content to reference files under the `references/` directory and instruct the agent to load them only when needed.

---

- **Name**: Silent Automation (No Consent)
- **Description**: Modifying the user's workspace, running build steps, or deleting files without informing the user or getting approval.
- **Why**: Destroys trust, risks data loss, and makes it impossible for the user to understand what changes occurred in their project.
- **Instead**: Always present a plan, summarize the changes, and ask for permission before modifying the workspace.

---

- **Name**: Speculative Feature-Creep
- **Description**: Designing skill files and inputs to handle complex hypothetical scenarios that are not required by the current user goal.
- **Why**: Adds unnecessary maintenance overhead, increases complexity, and makes the skill harder to test and debug.
- **Instead**: Apply YAGNI (You Aren't Gonna Need It). Build only what is needed for the active user requirements.

---

- **Name**: Hardcoded Local Assumptions
- **Description**: Writing absolute file paths, hardcoded API keys, or machine-specific environment configurations inside skill code or instructions.
- **Why**: Breaks portability. The skill will fail to run when transferred to other team members' machines or environments.
- **Instead**: Use relative paths, workspace-relative paths, and read configurations from standard environment variables or input parameters.

---

- **Name**: Single-Run Overfitting
- **Description**: Modifying a skill's prompt or logic based on a single failed test run without verifying the change against the rest of the eval suite.
- **Why**: Often introduces regressions that break other previously working test cases.
- **Instead**: Maintain a diverse eval suite and run the full test suite to check for regressions before committing prompt changes.

---

- **Name**: Question Stacking
- **Description**: Asking multiple distinct questions or sub-questions in a single turn.
- **Why**: Dilutes user responses, causes confusion, and makes the elicitation loop inefficient.
- **Instead**: Pick the single most critical next question, ask it, and wait for the response before asking more.

---

- **Name**: Granularity Leakage
- **Description**: Documenting implementation-specific choices (e.g. database schemas, column names, code paths) inside brainstorming scopes or requirements.
- **Why**: Forces the user to make premature design decisions and complicates the requirements with unnecessary detail.
- **Instead**: Focus on product shape and behavior; defer architectural design to the planning phase.

---

- **Name**: Persona Framing
- **Description**: Opening a generated `SKILL.md` with an assigned identity, career history, or claimed expertise level in place of a Mandate.
- **Why**: Implied competence gives the model nothing checkable to reason against, and personas measurably cost accuracy on the discriminative work — judging, classifying, verifying — most skills perform. `references/validations.md` flags it under `skill-persona-identity-language` and `skill-mandate-task-framed`.
- **Instead**: Task-Criteria Mandate

---

- **Name**: Overstuffed Description
- **Description**: Packing the frontmatter description with the skill's procedure, long keyword lists, or constraints until it runs past 500 characters.
- **Why**: The description loads in every session's skill index, so extra length pays that cost everywhere without improving the trigger decision; past 1024 characters the skill stops registering at all.
- **Instead**: Assertive Trigger Description
