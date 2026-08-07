# Skill Creator Interactions

This document defines the interaction flow used by skill-creator.

---

## Interaction Rules

These rules apply to every creation session.

1. **Ask one question at a time**: One question per turn, even when sub-questions feel related. Stacking several questions in a single message produces diluted answers. Pick the single most useful one and ask it.
2. **Prefer single-select multiple choice**: Use single-select when choosing one direction, one priority, or one next step.
3. **Use multi-select rarely and intentionally**: Use it only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist. If prioritization matters, follow up by asking which selected item is primary.
4. **Default to the platform's blocking question tool** - Use `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema isn't loaded), `request_user_input` in Codex, `ask_user` in Gemini, `ask_user` in Pi (requires the `pi-ask-user` extension). These tools include a free-text fallback (e.g., "Other" in Claude Code), so options scaffold the answer without confining it — well-chosen options surface dimensions the user may not have separated, and pick-plus-optional-note is lower activation energy than composing prose from scratch. This default holds for opening and elicitation questions too, not only narrowing. Fall back to numbered options in chat only when no blocking tool exists in the harness or the call errors (e.g., Codex edit modes) — not because a schema load is required. Always ask the question through the blocking tool (or its chat-based fallback) before moving on.
5. **Use an open-ended question only when the question is genuinely open** - Drop the blocking tool only when (a) the answer is inherently narrative ("walk me through how you got here"), (b) the question is diagnostic or introspective and presented options would unintentionally influence the user's answer (e.g., "what concerns you most?" — a 4-option menu would nudge them toward those axes rather than the ones actually on their mind), or (c) you cannot write 3-4 genuinely distinct, plausibly-correct options that cover the space without padding or strawmen. The test: if you'd be straining to fill the option slots, the question is open — ask it open-ended. Rule 1 still applies: still one question per turn.
6. **Open-ended questions earn their place only when they're specific enough to elicit a substantive answer** - Apply Rule 5 silently: just ask the question, do not narrate the form choice. The question itself must give the user something concrete to anchor on. Good: *"What's the most concrete thing someone's already done about this — paid for it, built a workaround, quit a tool over it?"* (this is one of Phase 1.2's rigor probes — it earns its open-endedness by naming what counts as an answer). Too thin: *"What's your take?"* (nothing to bite into; user defaults to a one-liner that wastes the open question). Avoid (a) narrating the form choice ("the most useful question I can ask here is..."), (b) framings that imply a short answer ("briefly", "in one sentence"), (c) yes/no traps, and (d) AI-slop warmth wrappers ("take it wherever feels relevant").

## Feature or Skill Description

<feature_description> #$ARGUMENTS </feature_description>

**If the feature description above is empty, ask the user:** "What skill would you like to build together? Please describe the feature, ability, or agentic workflow you're thinking about."

Proceed once you have a feature or skill description from the user.

## Execution Flow

### Phase 0: Resume, Assess, and Route

- **Objective**: Decide whether to resume existing work and whether a full brainstorm is needed before Phase 1 begins.
- **Agent Action**:
  - *0.1 Resume Existing Work When Appropriate* — If the user references an existing skill or instructions or document: read the skill, instructions, or document; if resuming, summarize the current state briefly, continue from its state, and update the existing document(s), skill, or instructions unless the user indicates starting fresh or producing a duplicate.
  - *0.2 Assess Whether Brainstorming Is Needed* — Check for clear requirements indicators: specific acceptance criteria provided, referenced existing patterns to follow, described exact expected behavior, constrained/well-defined scope.
- **Human Gate-Intervention**: When resuming existing work, confirm with the user before resuming: "Found an existing skill for [topic]. Should I revise this, refer to this, refactor this, or start fresh?"
- **Proceed When**: Requirements are already clear per the 0.2 indicators — keep the interaction brief, confirm understanding, and present concise next-step options rather than forcing a long brainstorm.
- **Pause When**: Requirements are not yet clear — continue into the full dialogue starting at Phase 1.

### Phase 1: Understand the Idea

- **Objective**: Build a concrete, shared understanding of the idea through context scanning and collaborative dialogue.
- **Agent Action**:
  - *1.1 Existing Context Scan* — Scan the referenced skill(s), document(s), or instructions. If nothing obvious appears after a short scan, say so and continue. Two rules govern technical depth during the scan: (1) **Verify before claiming** — when the brainstorm touches checkable infrastructure, read the relevant source files to confirm what actually exists; (2) **Defer design decisions to planning** — implementation details like schemas, migration strategies, endpoint structure, or deployment topology belong in planning, not here, unless the brainstorm is itself about a technical or architectural decision.
  - *1.2 Collaborative Dialogue* — Follow the Interaction Rules above. Ask what the user is already thinking before offering your own ideas. Start broad (problem, users, value) then narrow (constraints, exclusions, edge cases). Clarify the problem frame, validate assumptions, and ask about success criteria. Make requirements concrete enough that planning will not need to invent behavior. Surface dependencies or prerequisites only when they materially affect scope. Resolve product decisions here; leave technical implementation choices for planning. Bring ideas, alternatives, and challenges instead of only interviewing.
- **Human Gate-Intervention**: Use the platform's blocking question tool for one question at a time (per Interaction Rules). Before exiting Phase 1.2, run an integration check: mentally combine what the user has said so far and surface any non-obvious consequences the dialogue hasn't probed. If user-stated X plus user-stated Y plus your-default-Z produces a downstream effect the user is unlikely to have tracked through one-question-at-a-time dialogue ("if mute lives on the rule AND we don't warn on delete, then rule-delete silently loses pause state"), probe it now while still in dialogue. One probe per genuine combination effect, asked open-ended, same discipline as rigor probes.
- **Proceed When**: The idea is clear AND no integration-check questions are pending, OR the user explicitly wants to proceed.
- **Pause When**: The idea is still unclear, or an integration-check question is pending — continue the dialogue.

### Phase 2: Explore Approaches

- **Objective**: Surface and evaluate the plausible directions before committing to one.
- **Agent Action**: If multiple plausible directions remain, propose 2-3 concrete approaches based on research and conversation; otherwise state the recommended direction directly. Use at least one non-obvious angle — inversion (what if we did the opposite?), constraint removal (what if X weren't a limitation?), or analogy from how another domain solves this. For each approach, provide a brief description (2-3 sentences), pros and cons, key risks or unknowns, and when it's best suited. When useful, include one deliberately higher-upside alternative as a challenger option alongside the baseline (omit when the work is already obviously over-scoped or the baseline is clearly right). **Approach granularity: mechanism / product shape, not architecture** — name mechanism-level distinctions and product-relevant trade-offs (plan-tier coupling, complexity surface, migration difficulty), not implementation specifics (column names, table names, file paths, service classes, JSON shapes, exact method names); implementation specifics belong in planning, not the Phase 2.5 synthesis. If relevant, call out whether the choice is: reuse an existing pattern, extend an existing capability, or build something net new.
- **Human Gate-Intervention**: Present approaches first, then evaluate — let the user see all options before hearing which one is recommended, since leading with a recommendation anchors the conversation prematurely. After presenting all approaches, state your recommendation and explain why.
- **Proceed When**: One approach is clearly best and alternatives are not meaningful — skip the menu and state the recommendation directly, or the user has selected an approach from the menu.
- **Pause When**: Multiple plausible directions remain and the user has not yet selected one.

### Phase 2.5: Synthesis Summary

- **Objective**: Confirm scope with the user via a scoping synthesis before the requirements doc is written — the user's last opportunity to correct scope.
- **Agent Action**: **STOP. Before composing the synthesis, read `references/synthesis_summary.md`.** The two-stage shape (internal three-bucket draft → chat-time scoping synthesis), the Path A / Path B gate, the four scoping synthesis sections with their keep tests, the tier-aware bullet budget with re-cut rule, anti-pattern guidance, soft-cut behavior, self-redirect support, and internal-draft routing into doc body sections all live there. Composing a synthesis without these rules loaded reliably produces malformed output — pasting the full internal three-bucket draft verbatim into chat, implementation-detail leakage into the scoping synthesis, the proposal-pitch anti-pattern. Each scoping synthesis bullet must pass the affirmability test (can the user evaluate this without reading code?) AND the detail test (1–2 lines max, conversational not documentary). This is not optional supplementary reading; it is the source of truth for how the phase behaves. The scoping synthesis is shaped like what two product collaborators would confirm before writing a PRD, not like a comprehensive audit or a one-line preview.
- **Human Gate-Intervention**: Path A (announce-mode, Lightweight tier with no blocking questions fired) — state the proposed shape in 1-3 sentences and proceed in the same turn. Path B (every other case) — present the full scoping synthesis and ask the user to confirm or redirect, per `references/synthesis_summary.md`.
- **Proceed When**: Path A — the shape is stated; proceed to Phase 3 in the same turn. Path B — the user confirms the scoping synthesis (or the soft-cut blocking question resolves to "proceed").
- **Pause When**: Path B and the user has not yet confirmed, or has requested a revision — integrate the revision, re-present the synthesis, and wait again.

### Phase 3: Capture the Requirements (Temporary)

- **Objective**: Persist the conversation's durable decisions into a temporary requirements document that Phase 4 will consume.
- **Agent Action**: Write or update a temporary requirements document at `temp-requirements.md` in the workspace root only when the conversation produced durable decisions worth preserving. Read `references/requirements_capture.md` for the document template, formatting rules, visual aid guidance, and completeness checks. This file is temporary and will be deleted after the skill is drafted in Phase 4. For **Lightweight** brainstorms, keep the document compact.
- **Human Gate-Intervention**: None beyond the confirmation already obtained in Phase 2.5.
- **Proceed When**: The requirements document (or the decision to skip it, for brief-alignment Lightweight cases) is settled — proceed to Phase 4.
- **Pause When**: Not applicable — Phase 2.5's confirmation is the gate for this phase; Phase 3 proceeds automatically once it resolves.

### Phase 4: Handoff

- **Objective**: Present next-step options to the user and execute the selection.
- **Agent Action**: Read `references/handoff.md` for the option logic, cleanup instructions, and closing summary format.
- **Human Gate-Intervention**: Present the Phase 4 options via the platform's blocking question tool, per Interaction Rules #4.
- **Proceed When**: The user selects "Draft/Write the skill files" — draft/write the skill files, show the closing summary, and delete `temp-requirements.md`. Or the user selects "Cancel and clean up" — delete `temp-requirements.md` and end the turn.
- **Pause When**: The user selects "More clarifying questions" — return to Phase 1.2 and continue the dialogue, then re-enter Phase 4 once satisfied.

## Handoff

- **Completion State**: The skill's `SKILL.md` and reference files under `references/` are drafted or updated per the templates in `references/handoff.md`, the closing summary has been shown, and `temp-requirements.md` has been deleted from the workspace root.
- **Exception / Fallback Handoff**: If the user cancels at any point in Phase 4, delete `temp-requirements.md` from the workspace root, display the cancellation message from `references/handoff.md`, and end the turn without drafting or writing skill files.
