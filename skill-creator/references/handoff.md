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
