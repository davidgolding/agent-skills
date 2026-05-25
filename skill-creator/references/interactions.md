# Skill Creator

## Interaction Rules

These rules apply to every creation session.

1. **Ask one question at a time**: One question per turn, even when sub-questions feel related. Stacking several questions in a single message produces diluted answers. Pick the single most useful one and ask it.
2. **Prefer single-select multiple choice**: Use single-select when choosing one direction, one priority, or one next step.
3. **Use multi-select rarely and intentionally**: Use it only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist. If prioritization matters, follow up by asking which selected item is primary.
4. **Default to the platform's blocking question tool** - Use `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema isn't loaded), `request_user_input` in Codex, `ask_user` in Gemini, `ask_user` in Pi (requires the `pi-ask-user` extension). These tools include a free-text fallback (e.g., "Other" in Claude Code), so options scaffold the answer without confining it — well-chosen options surface dimensions the user may not have separated, and pick-plus-optional-note is lower activation energy than composing prose from scratch. This default holds for opening and elicitation questions too, not only narrowing. Fall back to numbered options in chat only when no blocking tool exists in the harness or the call errors (e.g., Codex edit modes) — not because a schema load is required. Never silently skip the question.
5. **Use an open-ended question only when the question is genuinely open** - Drop the blocking tool only when (a) the answer is inherently narrative ("walk me through how you got here"), (b) the question is diagnostic or introspective and presented options would unintentionally influence the user's answer (e.g., "what concerns you most?" — a 4-option menu would nudge them toward those axes rather than the ones actually on their mind), or (c) you cannot write 3-4 genuinely distinct, plausibly-correct options that cover the space without padding or strawmen. The test: if you'd be straining to fill the option slots, the question is open — ask it open-ended. Rule 1 still applies: still one question per turn.
6. **Open-ended questions earn their place only when they're specific enough to elicit a substantive answer** - Apply Rule 5 silently: just ask the question, do not narrate the form choice. The question itself must give the user something concrete to anchor on. Good: *"What's the most concrete thing someone's already done about this — paid for it, built a workaround, quit a tool over it?"* (this is one of Phase 1.2's rigor probes — it earns its open-endedness by naming what counts as an answer). Too thin: *"What's your take?"* (nothing to bite into; user defaults to a one-liner that wastes the open question). Avoid (a) narrating the form choice ("the most useful question I can ask here is..."), (b) framings that imply a short answer ("briefly", "in one sentence"), (c) yes/no traps, and (d) AI-slop warmth wrappers ("take it wherever feels relevant").

## Feature or Skill Description

<feature_description> #$ARGUMENTS </feature_description>

**If the feature description above is empty, ask the user:** "What skill would you like to build together? Please describe the feature, ability, or agentic workflow you're thinking about."

Do not proceed until you have a feature or skill description from the user.

## Execution Flow

### Phase 0: Resume, Assess, and Route

#### 0.1 Resume Existing Work When Appropriate

If the user references an existing skill or instructions or document:

- Read the skill, instructions, or document
- Confirm with the user before resuming: "Found an existing skill for [topic]. Should I revise this, refer to this, refactor this, or start fresh?"
- If resuming, summarize the current state briefly, continue from its state, and update the existing document(s), skill, or instructions unless the user indicates starting fresh or producing a duplicate

#### 0.2 Assess Whether Brainstorming Is Needed

**Clear requirements indicators**:
- Specific acceptance criteria provided
- Referenced existing patterns to follow
- Described exact expected behavior
- Constrained, well-defined scope

**If requirements are already clear:**
- Keep the interaction brief
- Confirm understanding and present concise next-step options rather than forcing a long brainstorm

### Phase 1: Understand the Idea

#### 1.1 Existing Context Scan

Scan the referenced skill(s), document(s), or instructions. If nothing obvious appears after a short scan, say so and continue. Two rules govern technical depth during the scan:

1. **Verify before claiming**: When the brainstorm touches checkable infrastructure, read the relevant source files to confirm what actually exists.
2. **Defer design decisions to planning**: Implementation details like schemas, migration strategies, endpoint structure, or deployment topology belong in planning, not here — unless the brainstorm is itself about a technical or architectural decision, in which case those details are the subject of the brainstorm and should be explored.

#### 1.2 Collaborative Dialogue

Follow the Interaction Rules above. Use the platform's blocking question tool when available.

**Guidelines:**
- Ask what the user is already thinking before offering your own ideas. This surfaces hidden context and prevents fixation on AI-generated framings.
- Start broad (problem, users, value) then narrow (constraints, exclusions, edge cases)
- Clarify the problem frame, validate assumptions, and ask about success criteria
- Make requirements concrete enough that planning will not need to invent behavior
- Surface dependencies or prerequisites only when they materially affect scope
- Resolve product decisions here; leave technical implementation choices for planning
- Bring ideas, alternatives, and challenges instead of only interviewing

**Before exiting Phase 1.2: integration check.** Mentally combine what the user has said so far and surface any non-obvious consequences the dialogue hasn't probed. If user-stated X plus user-stated Y plus your-default-Z produces a downstream effect the user is unlikely to have tracked through one-question-at-a-time dialogue ("if mute lives on the rule AND we don't warn on delete, then rule-delete silently loses pause state"), probe it now while you're still in dialogue. One probe per genuine combination effect, asked open-ended, same discipline as rigor probes.

**Exit condition:** Continue until the idea is clear AND no integration-check questions are pending, OR the user explicitly wants to proceed.

### Phase 2: Explore Approaches

If multiple plausible directions remain, propose **2-3 concrete approaches** based on research and conversation. Otherwise state the recommended direction directly.

Use at least one non-obvious angle — inversion (what if we did the opposite?), constraint removal (what if X weren't a limitation?), or analogy from how another domain solves this. The first approaches that come to mind are usually variations on the same axis.

Present approaches first, then evaluate. Let the user see all options before hearing which one is recommended — leading with a recommendation before the user has seen alternatives anchors the conversation prematurely.

When useful, include one deliberately higher-upside alternative:
- Identify what adjacent addition or reframing would most increase usefulness, compounding value, or durability without disproportionate carrying cost. Present it as a challenger option alongside the baseline, not as the default. Omit it when the work is already obviously over-scoped or the baseline request is clearly the right move.

At product tier, alternatives should differ on *what* is built (product shape, actor set, positioning), not *how* it is built. Implementation-variant alternatives belong at feature tier.

For each approach, provide:
- Brief description (2-3 sentences)
- Pros and cons
- Key risks or unknowns
- When it's best suited

**Approach granularity: mechanism / product shape, not architecture.** Approach descriptions name mechanism-level distinctions ("pause as a rule property" vs "pause as an event filter" vs "pause as a separate entity") and product-relevant trade-offs (plan-tier coupling, complexity surface, migration difficulty). They do NOT name implementation specifics — column names, table names, file paths, service classes, JSON shapes, exact method names. Bringing architecture forward at brainstorm time forces the user to make architectural decisions on our intentionally-shallow research, and the synthesis at Phase 2.5 then has to filter out the leak.

After presenting all approaches, state your recommendation and explain why. Prefer simpler solutions when added complexity creates real carrying cost, but do not reject low-cost, high-value polish just because it is not strictly necessary.

If one approach is clearly best and alternatives are not meaningful, skip the menu and state the recommendation directly.

If relevant, call out whether the choice is:
- Reuse an existing pattern
- Extend an existing capability
- Build something net new

### Phase 2.5: Synthesis Summary

**STOP. Before composing the synthesis, read `references/synthesis_summary.md`.** The two-stage shape (internal three-bucket draft → chat-time scoping synthesis), the Path A / Path B gate, the four scoping synthesis sections with their keep tests, the tier-aware bullet budget with re-cut rule, anti-pattern guidance, soft-cut behavior, self-redirect support, and internal-draft routing into doc body sections all live there. Composing a synthesis without these rules loaded reliably produces malformed output — pasting the full internal three-bucket draft verbatim into chat, implementation-detail leakage into the scoping synthesis, the proposal-pitch anti-pattern. **Each scoping synthesis bullet must pass the affirmability test (can the user evaluate this without reading code?) AND the detail test (1–2 lines max, conversational not documentary); over-share and over-detail are the failure modes to avoid.** This is not optional supplementary reading; it is the source of truth for how the phase behaves.

Surface a scoping synthesis to the user before Phase 3 writes the temporary requirements doc — the user's last opportunity to correct scope. The scoping synthesis is shaped like what two product collaborators would confirm before writing a PRD, not like a comprehensive audit or a one-line preview.

### Phase 3: Capture the Requirements (Temporary)

Write or update a temporary requirements document at `temp-requirements.md` in the workspace root only when the conversation produced durable decisions worth preserving. Read `references/requirements_capture.md` for the document template, formatting rules, visual aid guidance, and completeness checks. This file is temporary and will be deleted after the skill is drafted in Phase 4.

For **Lightweight** brainstorms, keep the document compact. Skip document creation when the user only needs brief alignment and no durable decisions need to be preserved.

### Phase 4: Handoff

Present next-step options and execute the user's selection. Read `references/handoff.md` for the option logic, cleanup instructions, and closing summary format. Ensure `temp-requirements.md` in the workspace root is deleted immediately after the skill is drafted/written or if the session is cancelled.