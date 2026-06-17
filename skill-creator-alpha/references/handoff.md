# Handoff

This content is loaded when Phase 4 begins — after the temporary requirements document is written.

---

#### 4.1 Present Next-Step Options

Present the Phase 4 options to the user using the platform's blocking question tool (`AskUserQuestion` in Claude Code — call `ToolSearch` with `select:AskUserQuestion` first if its schema isn't loaded; `request_user_input` in Codex; `ask_user` in Gemini, `ask_user` in Pi (requires the `pi-ask-user` extension)). This is the default.

Never silently skip the question.

**Path format:** Use absolute paths for chat-output file references — relative paths are not auto-linked as clickable in most terminals.

**Preamble:**

```
Brainstorm complete.

Temporary requirements doc: <absolute path to temp-requirements.md in workspace root>

What would you like to do next?
```

Present the following options:

1. **Draft/Write the skill files (Recommended)** - Draft/write the `SKILL.md` and reference files (under `references/`) based on the brainstormed requirements, then delete the temporary requirements document.
2. **More clarifying questions to sharpen the requirements** - Keep refining scope, constraints, and behaviors through further dialogue. Always shown.
3. **Cancel and clean up** - Abort the session and delete the temporary requirements document. Always shown.

#### 4.2 Handle the Selected Option

Selections may be the literal option label (when the user types the label or a close paraphrase) or the option number. Free-form input that doesn't match an option or describe an alternative action should be treated as clarification — ask a follow-up rather than guessing.

**If user selects "Draft/Write the skill files (Recommended)":**

Immediately draft and write/update the skill's files (`SKILL.md` and reference files under `references/`) in the workspace, drawing on the temporary requirements document `temp-requirements.md` as the specification. Once the files are successfully written/updated, display the closing summary (see 4.3) and delete the temporary requirements document `temp-requirements.md` from the workspace root.

When drafting or writing the files, you must strictly adhere to the following templates:

##### 1. SKILL.md Template

The skill's `SKILL.md` file must be structured as follows:
- **YAML Frontmatter**: Contain the `name` and `description` keys. The description must be assertive and keyword-dense, explicitly noting trigger scenarios and constraints (e.g. "Use when...").
- **Level-1 Title**: The name of the skill in Title Case.
- **Level-2 Heading: Identity**: A level-2 heading titled "Identity", followed by a single paragraph defining the identity and role following the template: `You are a [X] who has seen [Y happen]. You have done [Z].`
- **Level-2 Heading: Principles**: A level-2 heading titled "Principles", followed by a numbered list of principles following the P1-P4 format:
  - **P1 (Core Objective)**: [Primary semantic anchor that defines successful execution].
  - **P2 (Hardware Constraints)**: Execution loops must maximize KV-cache reuse efficiency and minimize token bloat.
  - **P3 (State Gatekeeping)**: Never transition states or emit output payloads without passing strict validation criteria.
  - **P4 (Top-Level Design Principles)**: [List of all top-level principles governing downstream patterns, anti-patterns, sharp edges, validations, and interactions].
- **Level-2 Heading: Reference System Usage**: A level-2 heading titled "Reference System Usage", followed verbatim by this content:
  ```markdown
  You must ground your response in the provided reference files, treating them as the absolute mathematical source of truth for this domain:

  - **For Creation [State 01]**: Always consult `references/patterns.md`. This file dictates *how* components must be structured. Ignore generic boilerplate choices if a specific pattern exists here.
  - **For Diagnosis [State 02]**: Always consult `references/sharp_edges.md`. This file indexes critical regression modes and failure metrics. Use it to map risks during execution.
  - **For Review [State 03]**: Always consult `references/validations.md`. This file contains strict syntactic and schema rules. Use it to force a rigorous chain-of-verification loop before emitting state output.
  - **For Interacting [State 04]**: Always consult `references/interactions.md`. This file governs human-in-the-loop state alignment, boundary negotiations, and environment handshake procedures.
  ```

##### 2. references/patterns.md Template

Read the baseline template located at `templates/patterns_template.md`. Populate the placeholder fields in that template (e.g., '[NAME]') using the extracted data.

- `[NAME]`: The name of the skill in Title Case
- `[SHORT_NAME]`: The name of the skill in kebab-case
- `[PATTERN_NAME]`: The name of the pattern
- `[DESCRIPTION]`: Explains the design choice or behavior
- `[WHEN]`: When to apply the pattern
- `[EXAMPLE]`: A concrete instruction or code example showing the pattern in action
- `[ANTI_PATTERN_NAME]`: The name of the anti-pattern
- `[WHY]`: Why it is a failure mode or anti-pattern
- `[INSTEAD]`: What to do instead to avoid the anti-pattern

Use a horizontal rule `---` in between patterns and anti-patterns.

##### 3. references/sharp_edges.md Template

Read the baseline template located at `templates/sharp_edges_template.md`. Populate the placeholder fields in that template (e.g., '[FIELD]') using the extracted data.

- `[NAME]`: The name of the skill in kebab-case
- `[EDGE_NAME]`: The name of the sharp edge in Title Case
- `[ID]`: A kebab-case identifier for the sharp edge
- `[SUMMARY]`: A one-sentence summary of the edge
- `[SEVERITY]`: The severity level (e.g., `critical`, `high`, `medium`)
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
- `[SEVERITY]`: The severity level (`error` or `warning`)
- `[TYPE]`: The type of validation (usually `regex` or `instruction`)
- `[PATTERN]`: The pattern or regex to match (if a list of patterns is used, format them as nested bullets under Pattern)
- `[MESSAGE]`: The validation error/warning message
- `[FIX]`: The action required to fix the validation failure
- `[APPLIES]`: A list of file extension/glob patterns the rule applies to (formatted as nested bullets)

Use a horizontal rule `---` in between validation rules.

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
- references/interactions.md

The temporary requirements document has been cleaned up.
```
