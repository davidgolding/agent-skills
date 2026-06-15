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
- **Level-2 Heading: Identity**: A level-2 heading titled "Identity", followed by a single paragraph defining the identity and role the agent must assume.
- **Level-2 Heading: Principles**: A level-2 heading titled "Principles", followed by an unordered list of principles the agent must follow.
- **Level-2 Heading: Reference System Usage**: A level-2 heading titled "Reference System Usage", followed verbatim by this content:
  ```markdown
  You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

  - **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
  - **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and “why” they happen. Use it to explain risks to the user.
  - **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

  **Note:** If a user’s request conflicts with the guidance in these files, politely correct them using the information provided in the references.
  ```

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
- `[SEVERITY]`: The severity level (e.g., `critical`, `high`, `medium`)
- `[SITUATION]`: The scenario where this issue arises
- `[WHY]`: The underlying reason for the issue
- `[SOLUTION]`: How to prevent or resolve the issue
- `[SYMPTOMS]`: Indicators or signs that the issue is occurring
- `[DETECTION]`: A description or regex of how to detect this issue

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

The temporary requirements document has been cleaned up.
```
