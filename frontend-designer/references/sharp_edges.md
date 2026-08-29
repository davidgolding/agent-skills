# Sharp Edges

This document defines the sharp edges used by frontend-designer.

---

## AI House Style

- **Id**: ai-house-style
- **Summary**: Output drifts to the statistical center of machine-generated frontend design and becomes instantly recognizable as machine-made.
- **Severity**: critical
- **Situation**: Any moment a visual decision is made without an upstream commitment governing it — the first draft of a layout, a component added late in a session, or an iteration where the direction brief was not read first.
- **Why**: Generic output is the default attractor, not a mistake. Absent a specific commitment pulling against it, every unconstrained choice lands on the most common answer in the training distribution, and enough common answers stacked together produce a look that professionals identify on sight.
- **Solution**:
    - Run the named-tell check below before serving anything, and fix what it catches rather than rationalizing it.
    - Named tells: a centered hero with a large gradient headline; a three-column grid of equal rounded cards with soft shadows; one geometric sans (Inter, Geist, or the current equivalent) carrying every level of the hierarchy; purple-to-blue or indigo-to-violet gradients used decoratively; emoji standing in for icons; a shadow on every raised surface; uniform padding at every scale; a single centered fixed-width column as the only spatial idea; badge pills above every heading; a feature list of three items with an icon, a bold phrase, and two lines of copy.
    - When a tell is present and genuinely correct for this project, say so explicitly and record the justification in the direction brief so later sessions do not relitigate it.
    - Prevent rather than correct: commit the Forced Commitment Set upstream so the token layer itself is not generic.
- **Symptoms**:
    - The result would look at home in any product in any industry.
    - Nothing in the layout could be described without using the words "modern" or "clean".
    - The direction brief's project-specific anti-pattern list describes the thing that was just built.
- **Detection Pattern**: Rendered output whose hero is centered with a gradient-filled headline, whose primary content is an evenly divided grid of identically rounded and shadowed cards, and whose entire typographic hierarchy is carried by weight variations of a single geometric sans.

---

## Direction Drift Across Invocations

- **Id**: direction-drift-across-invocations
- **Summary**: A later session builds against defaults instead of the project's established system because it never read the direction brief or tokens.
- **Severity**: high
- **Situation**: The fourth or fifth invocation in a project, adding a new component with fresh context, months after the direction was chosen.
- **Why**: Context does not persist between sessions and the agent never sees its own rendered output, so nothing corrects a drifted choice from inside the session. One inconsistent component establishes a precedent that the next session then matches, and drift compounds silently.
- **Solution**:
    - Walk the Phase 0 resolution order before writing anything: direction brief, then tokens, then existing code, then from scratch.
    - State which rung was hit so the user can catch a missed brief immediately.
    - Extend the existing brief and tokens rather than authoring parallel ones, and say what was added.
    - When the brief and the built components disagree, surface the conflict and ask which governs instead of silently picking one.
- **Symptoms**:
    - A new component introduces a radius, shadow, or type size that appears nowhere else in the project.
    - Two components solve the same layout problem with different spatial logic.
    - The session began producing code without any statement about existing project context.
- **Detection Pattern**: A newly added component that introduces token values or structural conventions absent from every component already present in the project, in a project that contains a direction brief or tokens file.

---

## Accessibility Theater

- **Id**: accessibility-theater
- **Summary**: ARIA attributes are present but the component cannot actually be operated by keyboard or understood by a screen reader.
- **Severity**: high
- **Situation**: Custom interactive components built from generic elements — a dropdown, a modal, a tab set, a custom select, a clickable card.
- **Why**: ARIA attributes are cheap to write and look like compliance in code review, while the expensive parts — focus management, keyboard event handling, focus trapping and restoration, live-region timing — are invisible in the markup. Adding a role without the matching behavior is worse than omitting it, because it promises assistive technology something the component does not deliver.
- **Solution**:
    - Prefer the native element that already has the behavior over a generic element plus a role.
    - When a custom component is unavoidable, implement the full keyboard interaction contract for its role, not only the attributes.
    - Verify focus is visible, reachable, ordered sensibly, restored on close, and never trapped except deliberately in a modal.
    - Treat this as part of the Component Completeness Bar, not as a follow-up pass.
- **Symptoms**:
    - A generic element carries a role attribute but no key handler.
    - A modal opens without moving focus into it, or closes without restoring focus.
    - Focus styles were removed for appearance and nothing replaced them.
- **Detection Pattern**: A non-interactive element carrying an interactive role or ARIA state attribute while having no keyboard event handler and no tab index, or a dialog implementation with no focus move on open and no focus restore on close.

---

## Stale Framework Knowledge

- **Id**: stale-framework-knowledge
- **Summary**: Version numbers, APIs, or configuration defaults asserted from memory are wrong, and the setup instructions fail.
- **Severity**: high
- **Situation**: Proposing stacks in Phase 3, writing a build configuration, or answering a direct question about what a framework currently supports.
- **Why**: Frontend tooling turns over faster than model knowledge. Major versions ship breaking configuration changes, APIs get renamed, and recommended setup paths are replaced entirely — while the confident phrasing of a remembered answer gives the user no signal that it is dated.
- **Solution**:
    - Look up the current state of anything datable at the moment you need it, before it reaches the user or the code.
    - Report what you found and when you checked it, so the user can judge the freshness themselves.
    - Never write version-specific claims into this skill's reference files, where they would age invisibly.
    - When a lookup is unavailable, say the claim is from memory and unverified rather than stating it flatly.
- **Symptoms**:
    - A setup command errors on an unrecognized flag or a renamed configuration key.
    - A configuration file uses a format the installed major version replaced.
    - A version number was stated with no accompanying statement of how it was verified.
- **Detection Pattern**: Specific version numbers, API names, or configuration file formats stated to the user or written into generated files during a session in which no lookup for those specifics was performed.

---

## Utility Default Flattening

- **Id**: utility-default-flattening
- **Summary**: The committed design collapses into a utility framework's default scale, radius, shadow, and color ramps until the direction is no longer visible.
- **Severity**: medium
- **Situation**: Building with a utility-class framework after a direction has been committed, especially under time pressure or on the second and third components.
- **Why**: The framework's defaults are always one keystroke away while the project's tokens require a configuration step, so the path of least resistance leads back to the framework's opinions. Those opinions are shared by every project using the framework, which is precisely what makes them generic.
- **Solution**:
    - Map the project's token layer onto the framework's theme configuration before building the first component, so the defaults are replaced rather than competing.
    - Remove or override the default scales the direction does not use, so reaching for them is not possible by accident.
    - Treat an unmapped default utility class in a component the same as a raw value: flag and justify, do not ship quietly.
- **Symptoms**:
    - Components use the framework's stock radius, shadow, and spacing names rather than project token names.
    - The rendered result resembles the framework's own documentation site.
    - The theme configuration is unmodified from its generated state.
- **Detection Pattern**: Components consuming a utility framework's default scale, radius, shadow, or color class names in a project whose theme configuration was never extended with the direction's token values.

---

## Dependency Install Without Consent

- **Id**: dependency-install-without-consent
- **Summary**: Packages, build tooling, or scaffolding commands are run in the user's workspace before they agreed to them.
- **Severity**: medium
- **Situation**: Phase 3 stack setup, or reaching for a library mid-build in Phase 5 to solve a problem quickly.
- **Why**: Installation writes a dependency tree, lockfile, and configuration the user then owns and must maintain, audit, and eventually remove. A scaffolding command can also overwrite files already present. None of that is reversible by simply undoing an edit.
- **Solution**:
    - State the exact commands and the files they will create or modify, then obtain the user's consent before running them.
    - Prefer a solution with no new dependency when one exists, and say that you preferred it.
    - When scaffolding into a directory that is not empty, list what already exists and what the command would overwrite before proceeding.
- **Symptoms**:
    - A lockfile or dependency manifest changed without a preceding statement of intent.
    - New configuration files appeared that the user was not told about.
    - A library was introduced mid-build to solve a problem that was never discussed.
- **Detection Pattern**: Package installation or project scaffolding commands executed in a session where no statement of the intended commands and affected files preceded them.

---

## Motion Without Reduced Motion

- **Id**: motion-without-reduced-motion
- **Summary**: Animation ships with no reduced-motion path, causing discomfort or harm to users with vestibular sensitivity.
- **Severity**: medium
- **Situation**: Any transition, entrance animation, parallax effect, auto-playing carousel, or scroll-linked movement.
- **Why**: Motion is authored and reviewed by people who are not affected by it, so its absence of a reduced-motion path is invisible during development. For users with vestibular disorders the consequence is nausea or migraine, not mild annoyance, and large-area or parallax movement is the worst offender.
- **Solution**:
    - Give every animation a reduced-motion branch that removes or substantially shortens the movement rather than only slowing it.
    - Treat large-area, parallax, and auto-playing movement as requiring removal under reduced motion, not reduction.
    - Include the reduced-motion path in the Component Completeness Bar so it is authored alongside the animation, not retrofitted.
- **Symptoms**:
    - The stylesheet contains transitions or keyframe animations and no reduced-motion query.
    - A carousel or background effect moves without user initiation and cannot be stopped.
    - Motion durations are the framework defaults rather than the direction's named motion character.
- **Detection Pattern**: Stylesheets or animation code containing transitions, keyframes, or scroll-linked movement with no corresponding reduced-motion media query anywhere in the project.

---

## Unverified Serve Claim

- **Id**: unverified-serve-claim
- **Summary**: The session ends by handing the user an address that was assumed rather than read from the running process.
- **Severity**: medium
- **Situation**: Phase 6 handoff, particularly when the default port is already occupied and the dev server silently selects a different one.
- **Why**: The agent does not observe its own rendered output, so a server that failed to start or moved to another port produces the same confident closing message as a successful one. The user follows a dead address and loses trust in the rest of the summary.
- **Solution**:
    - Read the address and port from the process output rather than assuming the framework default.
    - Confirm the process is still running before reporting success, not merely that the command was issued.
    - When startup fails, report the actual error text and fix it rather than reporting an intended address.
    - Keep the server address parameterized in any generated documentation instead of writing a fixed development address into project files.
- **Symptoms**:
    - The reported port matches the framework default while another process already held it.
    - A closing summary claims the project is running with no output from the server quoted or observed.
    - The server process exited immediately after start and the exit was not noticed.
- **Detection Pattern**: A handoff message stating a running development address in a session where the server process output was never read back or the process status was never confirmed.
