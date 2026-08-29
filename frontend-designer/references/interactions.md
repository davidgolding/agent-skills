# Frontend Designer Interactions

This document defines the interaction flow used by frontend-designer.

---

## Interaction Rules

These rules apply to every design session.

1. **Ask one question at a time**: One question per turn. Pick the single most useful one, ask it, and wait for the answer before asking the next.
2. **Prefer single-select multiple choice**: Use single-select when the user is choosing one direction, one stack, or one next unit of work.
3. **Use multi-select rarely**: Reserve it for compatible sets such as required breakpoints, accessibility targets, or content types that can all coexist.
4. **Default to the platform's blocking question tool**: Use `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema is not loaded), `request_user_input` in Codex, `ask_user` in Gemini or Pi. These tools carry a free-text fallback, so options scaffold the answer without confining it. Fall back to numbered options in chat only when no blocking tool exists in the harness or the call errors.
5. **Use an open-ended question only when the question is genuinely open**: Drop the blocking tool when the answer is inherently narrative ("what does this product actually do for someone"), when presented options would nudge the user toward axes that are not on their mind, or when you cannot write three or four genuinely distinct and plausible options without padding.
6. **Show, do not lecture**: Present directions and stacks as decisions with consequences, not as design education. State the choice and its trade-off in a line or two.

## Design Task Description

<design_task> #$ARGUMENTS </design_task>

**If the design task above is empty, ask the user:** "What are we building? Describe the interface, page, or component you have in mind, and tell me anything you already know about who it is for."

Proceed once you have a design task from the user.

## Execution Flow

### Phase 0: Resolve Context

- **Objective**: Establish what visual system, if any, already governs this project before proposing anything.
- **Agent Action**: Walk the resolution order and stop at the first rung that hits.
  - *0.1 Direction brief* — Search the project for a written direction brief (a design or direction document under the project's docs, design, or root directory). If one exists, read it and treat it as governing.
  - *0.2 Design tokens* — Search for a tokens file (CSS custom properties, a tokens stylesheet, a theme configuration). If one exists, read it and treat its values as the available vocabulary.
  - *0.3 Existing code* — With neither artifact present but components already built, read enough of them to infer the type scale, color logic, spacing rhythm, and component conventions in use.
  - *0.4 From scratch* — With nothing present, note that a direction brief will be authored as part of this work in Phase 4.
- **Human Gate-Intervention**: State plainly which rung was hit and what it means for this session — for example, that an existing brief governs and direction-setting will be skipped, or that this project has no system yet and one will be established.
- **Proceed When**: The governing context is identified and stated.
- **Pause When**: The discovered artifacts conflict with each other — a brief that contradicts the tokens in use, or tokens that contradict the built components. Surface the conflict and ask which one governs.

### Phase 1: Understand the Work

- **Objective**: Learn enough about audience, content, and constraints that direction becomes a defensible answer rather than a taste preference.
- **Agent Action**: Follow the Interaction Rules above. Ask what the user is already thinking before offering your own ideas. Establish who this is for and what they are trying to accomplish, what real content it must carry (length, density, media, worst-case strings), the tone it must project, and the hard constraints — brand requirements, accessibility targets, browser or device floor, performance budget, content management needs. Ask about exclusions and edge cases once the center is clear. Resolve product and design decisions here; leave implementation choices for Phase 3 and later.
- **Human Gate-Intervention**: One question per turn through the platform's blocking question tool. Before leaving this phase, combine what the user has said and surface any consequence the dialogue has not probed — when a stated content requirement and a stated constraint collide in a way the user is unlikely to have tracked, raise it now.
- **Proceed When**: Direction could be argued from the answers, and no combination question is pending.
- **Pause When**: The work is still abstract, or a combination question is pending.

### Phase 2: Direction

- **Objective**: Arrive at a specific, committed visual direction rather than a default.
- **Agent Action**: Two routes, determined by whether the user supplied references.
  - *2.1 References supplied* — When the user provides reference URLs, screenshots, an existing brand, or a product they admire, reverse-engineer the system rather than copying its surface: name the type pairing and scale ratio, the color logic (how the palette is generated, not just its values), the spatial grid and density, the corner and edge language, the elevation model, and the motion character. State what you extracted, then state how you will extend it to cover what the reference does not show. Fetch supplied URLs to examine them rather than reasoning from the description alone.
  - *2.2 No references supplied* — Propose two or three genuinely distinct directions. Distinct means they disagree on something structural, not on hue. Each direction carries the Forced Commitment Set from `patterns.md`: a real type pairing with a stated reason, a spatial system that is not a centered fixed-width column by default, a palette derived from a source rather than assembled from a swatch panel, a named motion character, and one deliberate asymmetry or density decision. Present all directions before recommending one.
- **Human Gate-Intervention**: Present the directions first, then state your recommendation and why. Let the user pick or blend.
- **Proceed When**: One direction is selected, or the extracted reference system is confirmed.
- **Pause When**: The user wants a direction revised, or wants to see a different angle. Revise and re-present.

### Phase 3: Stack

- **Objective**: Choose a stack by argument, on this project's actual requirements.
- **Agent Action**: Before proposing anything, look up the present state of the candidates — current major versions, current recommended setup path, anything that changed recently enough to matter. Then present two or three candidate stacks with honest trade-offs against this project's requirements. Zero-build vanilla HTML, CSS, and JavaScript is a genuine candidate: name what it costs and what it saves here specifically. When a framework is warranted, name the specific requirement that makes it warranted. Include what each candidate implies for build tooling, dependency count, and long-term maintenance by whoever inherits this.
- **Human Gate-Intervention**: The user chooses. Before any installation or scaffolding command runs, state the exact commands and the files they will create, and obtain the user's consent.
- **Proceed When**: The stack is chosen and consent for the setup commands is granted.
- **Pause When**: The user has not chosen, or has withheld consent for a command. Offer an alternative that avoids the objection.

### Phase 4: Commit

- **Objective**: Write the design system down before any component consumes it.
- **Agent Action**: Author the direction brief and the token layer inside the project, per the Direction Brief First and Token Layer as Law patterns in `patterns.md`. The brief records the chosen direction, the reasoning, the Forced Commitment Set, and the project-specific anti-patterns — what this project must never look like. The token layer expresses the enforceable values: type scale, color ramps and their semantic assignments, spacing scale, radii, elevation, motion durations and easings. When Phase 0 resolved to an existing brief or existing tokens, extend them rather than authoring new ones, and say what you added.
- **Human Gate-Intervention**: State which files you are creating or extending before writing them.
- **Proceed When**: The brief and tokens exist in the project and the user has seen what was written.
- **Pause When**: The user disagrees with a committed value. Revise the brief or tokens, not the components downstream of them.

### Phase 5: Build One Unit

- **Objective**: Bring a single unit of work to the completeness bar.
- **Agent Action**: Build the one thing the user asked for. Consume tokens rather than raw values. Clear the Component Completeness Bar in `patterns.md` before considering it done: every interaction state, keyboard operation, visible focus, screen-reader semantics, responsive behavior across the project's stated breakpoints, empty and loading and error cases, and a reduced-motion path. Use the project's real content, or content written for this project — never filler text. When you notice adjacent functionality worth building, name it and defer it rather than adding it.
- **Human Gate-Intervention**: When the user asks mid-build for something adjacent, acknowledge it, finish the current unit to the bar, then offer the adjacent work as the next unit.
- **Proceed When**: The unit clears the completeness bar and the pre-serve check in `sharp_edges.md` under the AI House Style edge finds nothing.
- **Pause When**: The unit cannot clear the bar without a decision the user has not made. Ask for that decision.

### Phase 6: Serve and Hand Off

- **Objective**: Put the running result in front of the user and state the boundary of what was done.
- **Agent Action**: State the command you intend to run, obtain consent, start the development server, confirm from its output that it actually started and on which port, and hand the user the address it reported rather than an assumed one. Then state in a few lines what was built, which token values it introduced or consumed, and what was deliberately left undone — including adjacent work you deferred during Phase 5.
- **Human Gate-Intervention**: The user judges the rendered result. Take their reaction as the input to the next iteration.
- **Proceed When**: The server is confirmed running and the summary is delivered.
- **Pause When**: The server fails to start. Report the actual error rather than the intended address, fix it, and retry.

## Handoff

- **Completion State**: The direction brief and token layer exist in the project, the requested unit clears the completeness bar, the development server is confirmed running, and the user has the address plus a short statement of what was built and what was deferred.
- **Exception / Fallback Handoff**: If the user withholds consent for installation or scaffolding, or ends the session mid-build, leave the workspace in its last consistent state, state exactly which files were created or modified and which were not, and name the next step that would resume the work.
