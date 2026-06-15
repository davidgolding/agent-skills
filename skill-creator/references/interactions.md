# Skill Creator Interactions

This document defines the interaction flow used by skill-creator.

---

## Interaction Rules

1. **Stop and wait after each prompt**: After asking the user a question or presenting options that require a decision, stop and do nothing further until the user replies. Do not continue to the next phase, generate files, or make assumptions based on prior context.
2. **Do not advance without confirmation**: Every phase has an explicit readiness condition. If that condition is not met — because the user has not confirmed, approved, or selected — stay in the current phase and re-prompt if needed. Never skip ahead.
3. **Carry context forward silently**: Track the user's decisions, stated goals, constraints, and any intermediate outputs entirely in memory as the conversation progresses. Do not narrate your internal state, emit tracking labels, or annotate your messages with phase names or variable names.

---

## Dialogue Guidelines

1. **Ask one question at a time**: One question per turn, even when sub-questions feel related. Stacking several questions in a single message produces diluted answers. Pick the single most useful one and ask it.
2. **Prefer single-select multiple choice**: Use single-select when choosing one direction, one priority, or one next step.
3. **Use multi-select rarely and intentionally**: Use it only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist. If prioritization matters, follow up by asking which selected item is primary.
4. **Default to the platform's blocking question tool**: Use `ask_user` or the equivalent native environment tool. These tools include a free-text fallback (e.g., "Other"), so options scaffold the answer without confining it. Fall back to numbered options in chat only when no blocking tool exists. Never silently skip a question.
5. **Use an open-ended question only when the question is genuinely open**: Drop the blocking tool only when (a) the answer is inherently narrative, (b) the question is diagnostic/introspective and options would nudge the user, or (c) you cannot write 3–4 genuinely distinct, plausibly-correct options.
6. **Open-ended questions earn their place only when they're specific enough to elicit a substantive answer**: Anchor open-ended questions in concrete scenarios. Avoid filler warmth openers, yes/no traps, and narration of form choice.

---

## Execution Flow

### Phase 0: Resume, Assess, and Route

**Objective**: Determine whether there is existing work to resume and whether brainstorming is needed before proceeding.

**What to do**: Check whether the user has referenced an existing skill, instruction set, or document. Scan the available context to assess whether the user's intent and topic are already clear enough to proceed.

**Readiness condition**: The user has confirmed a clear topic or work direction — either starting fresh or resuming/refactoring prior work.

**If not ready**: Ask the user directly: *"What skill would you like to build together? Please describe the feature, ability, or agentic workflow you're thinking about."* Then stop and wait for a reply.

---

### Phase 1: Existing Context Scan & Collaborative Dialogue

**Objective**: Scan any referenced files to verify infrastructure and gather specific requirements through focused single-question dialogue.

**What to do**: Review referenced files for relevant context. Identify gaps in the problem frame, constraints, and success criteria. Check for downstream integration requirements. Ask one targeted question at a time until the picture is complete.

**Readiness condition**: The user's idea is clearly understood, constraints are known, and all integration questions are resolved.

**If not ready**: Ask the single most important outstanding question and wait for the user's answer before continuing.

---

### Phase 2: Explore Approaches

**Objective**: Propose 2–3 design approaches and align on a direction before doing any implementation work.

**What to do**: Present 2–3 distinct approaches. For each, describe the key trade-offs, risks, and fit for the user's goals. Include a clear recommendation with rationale.

**Readiness condition**: The user has selected or confirmed an approach (possibly with modifications).

**If not ready**: Present the approaches and ask the user to choose. Wait for their selection before continuing.

---

### Phase 3: Scoping Synthesis

**Objective**: Produce and confirm a scoping synthesis that documents trade-offs, deferred items, and important call-outs.

**What to do**: Internally draft a three-bucket scope (in scope / out of scope / deferred), then format the scoping synthesis following `references/synthesis_summary.md`. Present it to the user for review.

**Readiness condition**: The user has reviewed and confirmed the scoping synthesis.

**If not ready**: Present the synthesis and ask the user to confirm or flag any changes. Wait before proceeding.

---

### Phase 4: Capture the Requirements

**Objective**: Produce a temporary requirements document (`temp-requirements.md`) in the workspace root for the user to review.

**What to do**: Write the requirements document following the structure in `references/requirements_capture.md`, based on everything confirmed so far. Present it to the user for approval.

**Readiness condition**: The user has explicitly approved the requirements document.

**If not ready**: Present the document and ask for approval or requested changes. Do not proceed to Phase 5 until approval is given.

---

### Phase 5: Handoff and Cleanup

**Objective**: Produce the final skill files, remove the temporary requirements document, and deliver a closing summary.

**What to do**: Draft the final skill files (`SKILL.md` and any references) using the appropriate templates. Delete `temp-requirements.md` from the workspace root. Present the closing summary to the user.

**Readiness condition**: The user has reviewed the generated files and confirmed there are no further adjustments.

**If not ready**: Prompt the user for any final changes and apply them. Once the user confirms, the session is complete.

---

## Handoff

**Normal completion**: The session closes when the user confirms the final skill files are correct and complete. No further action is required.

**Error or repeated failure**: If the environment throws errors or a validation step fails three times in a row, stop, tell the user what went wrong, and ask how they would like to proceed — whether that means retrying, adjusting the approach, or escalating for support.