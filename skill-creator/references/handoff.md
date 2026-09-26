# Handoff

This content is loaded when Phase 4 begins — after the temporary requirements document is written.

---

#### 4.1 Present Next-Step Options

Present the Phase 4 options to the user using the platform's blocking question tool, per Interaction Rules #4 in `references/interactions.md` (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini/Pi). This is the default.

Always ask the question through the blocking tool before moving on.

**Path format:** Use absolute paths for chat-output file references — relative paths are not auto-linked as clickable in most terminals.

**Preamble:**

```
Brainstorm complete.

Temporary requirements doc: <absolute path to temp-requirements.md in workspace root>

What would you like to do next?
```

Present the following options:

1. **Draft/Write the skill files (Recommended)** - Draft/write the `SKILL.md` and reference files (under `references/`, including `interactions.md` when the skill has human-in-the-loop behavior) based on the brainstormed requirements, then delete the temporary requirements document.
2. **More clarifying questions to sharpen the requirements** - Keep refining scope, constraints, and behaviors through further dialogue. Always shown.
3. **Cancel and clean up** - Abort the session and delete the temporary requirements document. Always shown.

#### 4.2 Handle the Selected Option

Selections may be the literal option label (when the user types the label or a close paraphrase) or the option number. Free-form input that doesn't match an option or describe an alternative action should be treated as clarification — ask a follow-up rather than guessing.

**If user selects "Draft/Write the skill files (Recommended)":**

Immediately draft and write/update the skill's files (`SKILL.md` and reference files under `references/`) in the workspace, drawing on the temporary requirements document `temp-requirements.md` as the specification. Once the files are successfully written/updated, read back the new `SKILL.md` frontmatter and check it against the `skill-frontmatter-valid-yaml` rule in `references/validations.md`, fixing each match before moving on. Then display the closing summary (see 4.3) and delete the temporary requirements document `temp-requirements.md` from the workspace root.

When drafting or writing the files, you must strictly adhere to the following templates:

##### 1. SKILL.md Template

The skill's `SKILL.md` file must be structured as follows, and must pass the `skill-structure-skill-md` and `skill-mandate-task-framed` rules in `references/validations.md`:
- **YAML Frontmatter**: Contain the `name` and `description` keys. Write the description as one clause naming what the skill does and one clause naming when to use it (e.g. "Use when..."), landing the total between 200 and 500 characters. Treat 1024 characters as a hard cap — past it the skill fails to register. Move procedural detail into the body or a reference file.
  - **YAML safety**: Open the file with `---` as its very first bytes and close the block with `---`. Keep each value on a single line, use spaces only, and write the description in plain ASCII punctuation (`-` for dashes, straight quotes), since characters copied from surrounding prose — em dashes, curly quotes, non-breaking or zero-width spaces — are how invalid bytes slip in. Write the description as an unquoted value by default; reword it to remove any `: ` or ` #` sequence and any leading `` ` ``, `"`, `'`, `[`, `{`, `>`, `|`, `*`, `&`, `!`, `%`, `@`, `-`, or `?`. When the wording genuinely needs one of those, wrap the whole value in double quotes and escape inner `"` as `\"`.
- **Level-1 Title**: The name of the skill in Title Case.
- **Level-2 Heading: Mandate**: A level-2 heading titled "Mandate", followed by a single task-framed paragraph that names (1) the unit of work the skill performs per invocation, (2) the decisions or axes it judges, (3) the reference files those judgments ground in, and (4) what a correct output contains. State the task and its criteria rather than a role for the agent to adopt; when the requirements imply expertise, convert it into the explicit criteria it stands for.
- **Level-2 Heading: Principles**: A level-2 heading titled "Principles", followed by an unordered list of principles the agent must follow. Render each as a bold descriptive name, a colon, and the principle (e.g. `- **Behavior Preservation**: ...`). Order them core objective → efficiency → gatekeeping → downstream-governing, using those categories to choose order only, with no `P1`-style labels in the output.
- **Level-2 Heading: Reference System Usage**: A level-2 heading titled "Reference System Usage", followed verbatim by this content:
  ```markdown
  You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

  - **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
  - **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
  - **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

  **Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
  ```
  When the skill gets a `references/interactions.md` (see template 5), add this bullet after the Review bullet:
  ```markdown
  - **For Interacting:** Always consult **`references/interactions.md`**. This file governs human-in-the-loop checkpoints, approval gates, and handoffs.
  ```

Keep `SKILL.md` to exactly these parts. Route every pattern, failure mode, validation rule, and interaction phase into its dedicated reference file so it loads only when the agent reaches that state.

##### Language Rules for Every Generated File

Apply these to `SKILL.md` and every reference file, since `references/validations.md` checks them across the whole skill (`skill-persona-identity-language`, `skill-negative-polarity-instruction`, `skill-fictional-runtime-tokens`):
- **Task-criteria framing**: Describe what the agent decides and the criteria it decides against. Replace assigned roles, career histories, and claimed expertise levels with the explicit criteria they imply.
- **Affirmative phrasing**: Phrase each instruction as the action to take and its trigger condition. When the requirements state a prohibition, restate it as the correct action while keeping the constraint's scope (e.g. "Whenever emitting output, pass validation first").
- **Grounded interaction mechanics**: Express waits as ending the turn, choices as the platform's blocking question tool, and gates as plain Proceed-When / Pause-When conditions, using runtime mechanics the platform actually performs in place of invented tokens or tags.

##### 2. references/patterns.md Template

Read the baseline template located at `templates/patterns_template.md`. Populate the placeholder fields in that template (e.g., '[FULL_NAME]') using the extracted data.

- `[NAME]`: The name of the skill in Title Case
- `[SHORT_NAME]`: The name of the skill in kebab-case
- `[PATTERN_NAME]`: The name of the pattern
- `[PATTERN_DESCRIPTION]`: A short description of the pattern
- `[WHEN]`: When to apply the pattern
- `[EXAMPLE]`: A concrete instruction or code example showing the pattern in action
- `[ANTI_PATTERN_NAME]`: The name of the anti-pattern
- `[ANTI_PATTERN_DESCRIPTION]`: A description of the incorrect behavior/structure
- `[WHY]`: Why it is a failure mode or anti-pattern
- `[INSTEAD]`: What to do instead to avoid the anti-pattern

Use a horizontal rule `---` in between patterns and anti-patterns.

##### 3. references/sharp_edges.md Template

Read the baseline template located at `templates/sharp_edges_template.md`. Populate the placeholder fields in that template (e.g., '[FIELD]') using the extracted data.

- `[NAME]`: The name of the skill in kebab-case
- `[EDGE_NAME]`: The name of the sharp edge in Title Case
- `[ID]`: A kebab-case identifier for the sharp edge
- `[SUMMARY]`: A one-sentence summary of the edge
- `[SEVERITY]`: The severity level — exactly one of `critical`, `high`, `medium`, or `low`
- `[SITUATION]`: The scenario where this issue arises
- `[WHY]`: The underlying reason for the issue
- `[SOLUTION]`: How to prevent or resolve the issue
- `[SYMPTOMS]`: Indicators or signs that the issue is occurring
- `[DETECTION]`: A natural language description of the pattern or behavior the agent would need to detect (e.g. `Registry entries with page ranges spanning 1 page or less containing incomplete sentences.` rather than shorthand, error codes, or function names like `incomplete_sentences`).

Use a horizontal rule `---` in between sharp edges.

##### 4. references/validations.md Template

Read the baseline template located at `templates/validations_template.md`. Populate the placeholder fields in that template (e.g., '[FIELD]') using the extracted data.

- `[NAME]`: The name of the skill in kebab-case
- `[VALIDATION_NAME]`: A name for the validation rule in Title Case
- `[ID]`: A kebab-case identifier for the validation rule
- `[SEVERITY]`: The severity level — exactly one of `error` or `warning`
- `[TYPE]`: The type of validation — exactly one of `regex` (a pattern matched against file text), `schema` (required structure, fields, enumerated values, or lengths), `semantic` (a judgment about meaning or behavior), or `syntax` (well-formedness, such as valid YAML or JSON)
- `[PATTERN]`: The pattern or regex to match (if a list of patterns is used, format them as nested bullets under Pattern)
- `[MESSAGE]`: The validation error/warning message
- `[FIX]`: The action required to fix the validation failure
- `[APPLIES]`: A list of file extension/glob patterns the rule applies to (formatted as nested bullets)

Use a horizontal rule `---` in between validation rules.

##### 5. references/interactions.md Template (Conditional)

Generate this file only when the requirements show human-in-the-loop behavior: mid-task prompts, multi-turn confirmation, approval gates, or gated state transitions. For a skill with none of these, leave the file out — an empty or fabricated interactions.md is scaffolding filler (see `skill-interactions-conditional` in `references/validations.md`).

Read the baseline template located at `templates/interactions_template.md`. Populate the placeholder fields in that template using the extracted data.

- `[NAME]`: The name of the skill in Title Case
- `[SHORT_NAME]`: The name of the skill in kebab-case
- `[RULE_NAME]` / `[RULE]`: A named interaction rule and its mechanics (turn-ending waits, the blocking question tool, what counts as approval)
- `[PHASE_NUMBER]` / `[PHASE_NAME]`: The phase's two-digit number and name
- `[OBJECTIVE]`: What the phase accomplishes
- `[AGENT_ACTION]`: What the agent does during the phase
- `[HUMAN_GATE]`: What the user decides at this phase, or "None; this phase runs autonomously."
- `[PROCEED_WHEN]`: The plain condition that advances to the next phase
- `[PAUSE_WHEN]`: The plain condition that ends the turn to wait for the user
- `[COMPLETION_STATE]`: What is true when the skill's run is complete
- `[FALLBACK]`: What the agent does when it cannot reach the completion state

Repeat the phase block once per phase.

**If user selects "More clarifying questions to sharpen the requirements":**

Return to Phase 1.3 (Collaborative Dialogue) and continue asking the user clarifying questions one at a time to further refine scope, edge cases, constraints, and preferences. Continue until the user is satisfied, then return to Phase 4. Do not show the closing summary yet.

**If user selects "Cancel and clean up":**

Delete the temporary requirements document `temp-requirements.md` from the workspace root. Display:

```text
Session cancelled. Temporary requirements cleaned up.
```

And end the turn.

#### 4.3 Closing Summary

Use the closing summary only when this run of the workflow is complete, not when returning to the Phase 4 options.

When complete, display:

```text
Skill creation complete!

Created/Updated files:
- SKILL.md
- references/patterns.md
- references/sharp_edges.md
- references/validations.md
- references/interactions.md (only when generated)

The temporary requirements document has been cleaned up.
```
