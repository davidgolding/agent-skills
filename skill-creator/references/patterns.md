# Skill Creator Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by skill-creator.

## Patterns

- **Name**: Three-Layer Loading Pattern
- **When**: Designing any new skill to keep the initial agent context lightweight and avoid overloading the context window during triggers by organizing the file layout into three distinct layers: triggering metadata (frontmatter in `SKILL.md`), core instructions and identity (body of `SKILL.md`), and detailed references/scripts/examples in subdirectories.
- **Example**:
  ```
  - Metadata Layer: Trigger description in frontmatter
  - Core Instruction Layer: `SKILL.md` containing Identity, Principles, and Reference Usage
  - Resource Layer: `references/patterns.md`, `references/sharp_edges.md`, `scripts/run_eval.py`
  ```

---

- **Name**: Assertive Trigger Description
- **When**: Defining the trigger contract in `SKILL.md` frontmatter to ensure high trigger precision by listing exact trigger keywords, commands, target files, and negative constraints.
- **Example**:
  ```
  description: Create new agentic skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch or edit or optimize an existing skill.
  ```

---

- **Name**: Rigid Eval-Driven Iteration Loop
- **When**: Optimizing prompts, adding features, or debugging failures in a skill by developing a test suite consisting of positive and negative triggering prompts, plus execution correctness checks. Run these tests automatically after any modification to measure performance improvement.
- **Example**:
  ```
  Test inputs:
    - Positive: "Help me write a git commit skill"
    - Negative (Near-miss): "Write a git commit for my current changes" (triggers a git commit skill, not skill-creator)
  Metrics: Trigger rate (%), task success rate (%), execution latency (ms).
  ```

---

- **Name**: Behavioral Legibility ("No Surprise")
- **When**: Executing actions on the user's codebase to maintain developer trust by always outlining planned tool executions (commands, file modifications) to the user first and obtaining explicit confirmation before running mutating commands or side-effects.
- **Example**:
  ```
  "I will now create the script `scripts/deploy.sh` and run it. Do you approve?"
  ```

---

- **Name**: Shared Helper Scripts
- **When**: Repeatedly executing the same sequence of terminal commands or processing logic across different runs, where complex logic (involving complex CLI invocations, calculations, or multi-step environment setups) should be extracted from the prompt into a script inside the skill's `scripts/` directory.
- **Example**:
  ```
  Instead of teaching the agent how to parse and average test runs in a prompt, write `scripts/average_runs.py` and have the agent execute `python3 scripts/average_runs.py`.
  ```

---

- **Name**: Progressive Output Disclosure
- **When**: Formatting responses that contain code diffs, logs, or multi-step reports to keep chat logs readable by presenting high-level summaries and action items in the direct chat response, keeping detailed code, long lists, and data dumps inside markdown artifacts or collapsible sections.
- **Example**:
  ```
  "I have updated the implementation plan. You can view the full file here: [implementation_plan.md](file:///path/to/plan.md). Key change: added validation for absolute paths."
  ```

---

- **Name**: Design for the Thousandth Invocation
- **When**: Writing any instructions, paths, or code scripts within a skill to ensure long-term reliability and portability across different users' environments through robust error handling, generalized paths, and parameterization.
- **Example**:
  ```
  - Avoid hardcoding `/Users/user/repo` -> Use `cwd` or environment-relative paths.
  - Check if a file exists before attempting to read it.
  - Handle command failures and log readable errors.
  ```

---

- **Name**: Interactive Dialogue Protocol
- **When**: Engaging in cooperative scoping or clarifying ambiguous developer requirements to avoid overwhelming the user by asking one question at a time and leveraging platform-native blocking questions where possible.
- **Example**:
  ```
  - Good: Asking "Should X be a rule property or filter?" and presenting options using ask_user tool.
  - Bad: Stacking three questions in one chat message.
  ```

---

- **Name**: Two-Stage Scoping Synthesis
- **When**: Summarizing decisions made in a brainstorming session before writing a requirements doc by producing an internal three-bucket scope draft first, then deriving a conversational scoping synthesis to confirm with the user.
- **Example**:
  ```
  Formulate the internal draft in agent thoughts, then output: "Based on our dialogue, here's the scope I'm proposing..." with Trade-offs, Deferred, and Call-outs.
  ```

---

- **Name**: Conversational Scope Bullets
- **When**: Writing the scoping synthesis or summarizing requirements to keep scope bullets conversational, 1-2 lines maximum, and focused entirely on product shape rather than code-level implementation details.
- **Example**:
  ```
  - Good: "Rule-delete silently loses pause state — confirm no warning needed"
  - Bad: "Use existing rule entity to store pause, adding a database column is_paused"
  ```

---

- **Name**: Temporary Intermediate Artifacts
- **When**: Writing temporary documents during brainstorming or planning before generation is completed to avoid repository clutter by using a single, un-nested temporary file in the workspace root (e.g., `temp-requirements.md`) and deleting it immediately after use.
- **Example**:
  ```
  Write the brainstormed requirements directly to `temp-requirements.md` in the workspace root, compile the skill, and delete `temp-requirements.md` once complete. Do not create nested folders (like `docs/brainstorms/`) for temporary files.
  ```

---

- **Name**: Standardized Skill Structure Pattern
- **When**: Drafting, writing, or editing any agent skill's files to ensure a structured, consistent layout in `SKILL.md` and references (`patterns.md`, `sharp_edges.md`, `validations.md`, `interactions.md`).
- **Example**:
  ```
  Generate `SKILL.md` containing name/description frontmatter, a Level-1 title heading in Title Case, and Level-2 headings for "Identity", "Principles", and "Reference System Usage" verbatim. Generate reference markdown files (`patterns.md`, `sharp_edges.md`, `validations.md`) with their standard heading layouts and required bullet key attributes.
  ```

---

## Anti-Patterns

- **Name**: Fuzzy Trigger Description
- **Why**: Using broad, generic, or conversational language in the YAML frontmatter description causes the router to trigger the skill for unrelated queries (false positives) or fail to activate it for relevant tasks (false negatives).
- **Instead**: Use the **Assertive Trigger Description** pattern to specify exact tasks and commands.

---

- **Name**: Monolithic Context Overload
- **Why**: Placing entire JSON schemas, code templates, or long reference documents directly inside the core `SKILL.md` file bloats the agent's context window on every invocation, wasting tokens, raising latency, and diluting instruction adherence.
- **Instead**: Use the **Three-Layer Loading Pattern** to delegate deep content to reference files under the `references/` directory.

---

- **Name**: Silent Automation (No Consent)
- **Why**: Modifying the user's workspace, running build steps, or deleting files without informing the user or getting approval destroys trust, risks data loss, and makes it impossible for the user to track changes.
- **Instead**: Use the **Behavioral Legibility ("No Surprise")** pattern to present a plan, summarize changes, and get approval.

---

- **Name**: Speculative Feature-Creep
- **Why**: Designing skill files and inputs to handle complex hypothetical scenarios that are not required by the current user goal adds unnecessary maintenance overhead, increases complexity, and makes the skill harder to test and debug.
- **Instead**: Apply YAGNI (You Aren't Gonna Need It) and build only what is needed for the active user requirements.

---

- **Name**: Hardcoded Local Assumptions
- **Why**: Writing absolute file paths, hardcoded API keys, or machine-specific environment configurations inside skill code or instructions breaks portability and causes the skill to fail when run on other developers' systems.
- **Instead**: Use the **Design for the Thousandth Invocation** pattern (relative paths and parameterized configurations).

---

- **Name**: Single-Run Overfitting
- **Why**: Modifying a skill's prompt or logic based on a single failed test run without verifying the change against the rest of the eval suite often introduces regressions that break other previously working test cases.
- **Instead**: Use the **Rigid Eval-Driven Iteration Loop** pattern to run the full test suite and check for regressions before committing prompt changes.

---

- **Name**: Question Stacking
- **Why**: Asking multiple distinct questions or sub-questions in a single turn dilutes user responses, causes confusion, and makes the elicitation loop inefficient.
- **Instead**: Use the **Interactive Dialogue Protocol** pattern to ask exactly one question at a time.

---

- **Name**: Granularity Leakage
- **Why**: Documenting implementation-specific choices (e.g. database schemas, column names, code paths) inside brainstorming scopes or requirements forces the user to make premature design decisions and complicates the requirements.
- **Instead**: Use the **Conversational Scope Bullets** pattern to focus on product shape and behavior.
