# Frontend Designer Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by frontend-designer.

## Patterns

- **Name**: Direction Brief First
- **Description**: Before any component code exists, write a short direction brief into the project recording the chosen visual direction, its reasoning, the Forced Commitment Set, and the project-specific anti-patterns. Later sessions read it before doing anything else.
- **When**: Phase 4 of every greenfield project, and whenever a project with no existing brief receives its first substantial design work.
- **Example**:
```
    ## Direction: Editorial Density
    Type: Söhne Kräftig / Freight Text Book, 1.25 scale, 18px base
    Space: 12-col asymmetric grid, content offset left, generous right margin
    Palette: sampled from the archive photography — warm neutrals, single ink accent
    Motion: restrained, 120ms, ease-out only, no entrance animation
    Density: deliberately tight leading in captions against open body copy
    This project must never look like: centered SaaS hero, gradient headline,
    uniform card grid, glassmorphism, emoji iconography
```

---

- **Name**: Reference Extraction
- **Description**: When the user supplies references, reverse-engineer the underlying system rather than copying its surface — name the scale ratio, the palette's generating logic, the spatial grid, the corner and edge language, the elevation model, and the motion character, then state how you will extend the system to cover what the reference does not show.
- **When**: Phase 2 whenever the user provides reference URLs, screenshots, an existing brand, or a product they want to feel adjacent to.
- **Example**:
```
    Extracted from the reference:
      - Type scale is 1.2, not 1.25 — headings stay close to body, the hierarchy
        is carried by weight and color rather than size
      - Palette is a single hue rotated through lightness, plus one complement
        used only for destructive actions
      - Radius language is 2px everywhere except the modal, which is 0
    Extending it: the reference has no data table, so the table inherits the
    2px radius, the weight-driven hierarchy, and the complement for row deletion.
```

---

- **Name**: Distinct Direction Set
- **Description**: When no references are supplied, propose two or three directions that disagree on something structural — spatial system, typographic voice, density, or motion philosophy — rather than three variations on the same layout in different hues. Present all of them before recommending one.
- **When**: Phase 2 on any project where the user has not supplied references, and again whenever a user rejects a direction and asks to see other angles.
- **Example**:
```
    A. Editorial Density — asymmetric grid, serif body, tight captions, no motion
    B. Instrument Panel — monospace numerics, high contrast, dense rows, snap transitions
    C. Quiet Gallery — extreme whitespace, one image per viewport, slow crossfades
    These disagree on density and motion, not on accent color.
```

---

- **Name**: Forced Commitment Set
- **Description**: Every direction must commit to five specific choices that generic output does not make: a real type pairing with a stated reason, a spatial system that is not a centered fixed-width column by default, a palette derived from a source rather than assembled from a swatch panel, a named motion character, and one deliberate asymmetry or density decision. Committing upstream makes generic output structurally unreachable downstream.
- **When**: Phase 2, as the required content of every proposed direction and of the direction brief that records it.
- **Example**:
```
    Type: two families with a reason, not one variable font at six weights
    Space: name the grid and where content sits in it, not "max-width container"
    Color: derived from a photograph, a material, a printed reference, or an
      existing brand — state the source in the brief
    Motion: a character with a name and a duration range, not "smooth transitions"
    One commitment: the deliberate asymmetry, density inversion, or scale jump
      that this project is willing to be recognized for
```

---

- **Name**: Token Layer as Law
- **Description**: Express the design system as named token values that components consume. A raw color, spacing, radius, type, or duration value inside a component is a violation to be flagged and justified, not shipped quietly.
- **When**: Phase 4 when authoring the system, and on every component built in Phase 5 thereafter.
- **Example**:
```
    /* tokens.css */
    :root {
      --ink-strong: oklch(22% 0.02 250);
      --space-tight: 0.5rem;
      --radius-edge: 2px;
      --motion-quick: 120ms;
    }
    /* component */
    .card { padding: var(--space-tight); border-radius: var(--radius-edge); }
```

---

- **Name**: Negotiated Stack Proposal
- **Description**: Present candidate stacks with trade-offs measured against this project's actual requirements and let the user choose. Zero-build vanilla HTML, CSS, and JavaScript is a genuine candidate whose costs and savings are named specifically; a framework is proposed alongside the specific requirement that makes it warranted.
- **When**: Phase 3 of every project, before any dependency is installed.
- **Example**:
```
    Vanilla + native CSS nesting — no build, no dependencies, deploys as static
      files. Costs you: hand-written state management for the filter panel.
    Preact + Vite — 4kb runtime, component model for the filter panel's state,
      one build step. Warranted specifically by that panel, nothing else here.
    Recommendation: vanilla. The filter panel is the only stateful surface and
      it has four inputs.
```

---

- **Name**: Live Currency Check
- **Description**: Look up the present state of any framework version, API, tooling default, or design trend at the moment you need it, and report what you found. Nothing datable is asserted from memory or written into this skill's reference files.
- **When**: Phase 3 before proposing stacks, and any time a specific version, API surface, configuration default, or trend claim is about to be stated to the user or written into code.
- **Example**:
```
    Before proposing: check the current major version and recommended setup
    path for each candidate, then tell the user what you found and when.
    Say "checked just now, the current major is X" rather than naming a
    version from memory.
```

---

- **Name**: Component Completeness Bar
- **Description**: A unit of work is not done until it clears a fixed bar: every interaction state, full keyboard operation, a visible focus style, correct screen-reader semantics, responsive behavior across the project's stated breakpoints, empty and loading and error cases, and a reduced-motion path.
- **When**: Phase 5, as the exit condition for every component before it is considered complete.
- **Example**:
```
    States: rest, hover, active, focus-visible, disabled, loading, error
    Keyboard: reachable, operable, escapable; focus visible and never trapped
    Semantics: a real button element or a correct role with matching behavior
    Responsive: verified against the stated breakpoints, including worst-case
      content length
    Cases: empty, loading, error, and the too-much-content case
    Motion: every animation has a prefers-reduced-motion branch
```

---

- **Name**: Iteration Depth Discipline
- **Description**: Perfect the unit of work currently in front of you rather than multiplying features sideways. Adjacent functionality you notice while building is named and offered as the next unit, never quietly added to this one.
- **When**: Throughout Phase 5, and whenever a mid-build request arrives for something adjacent to the current unit.
- **Example**:
```
    "The nav is at the bar now. While building it I noticed the mobile
    breakpoint has no skip link and the footer has no counterpart styling.
    Both are worth doing — want the skip link next?"
```

---

- **Name**: Serve and Hand Off
- **Description**: End the session by running the project, confirming from the process output that the server actually started and on which port, handing the user the address it reported, and stating what was built and what was deliberately left undone.
- **When**: Phase 6, as the closing act of every session that produced runnable output.
- **Example**:
```
    State the command, get consent, start the server, read the port from its
    output, and hand over the address it printed — not an assumed one. Then:
    "Built: the filter panel at the bar. Deferred: the empty-state
    illustration, and the skip link I mentioned."
```

---

## Anti-Patterns

- **Name**: AI House Style
- **Description**: Producing the recognizable visual signature of machine-generated frontends — a centered hero with a gradient headline, a three-column grid of uniform rounded cards, one geometric sans at every weight, purple-to-blue gradients, emoji standing in for icons, a soft shadow on every surface, and uniform padding everywhere.
- **Why**: It is the statistical center of the training distribution, so it is where output lands by default. It reads instantly as machine-made to anyone who looks at interfaces professionally, and it makes the product indistinguishable from every other product built the same way.
- **Instead**: Commit upstream through the Forced Commitment Set so the tokens themselves are not generic, record the project-specific anti-patterns in the direction brief, and run the named-tell check in `sharp_edges.md` before serving.

---

- **Name**: Framework Reflex
- **Description**: Reaching for React or a comparable framework on a project whose requirements a static page would satisfy, because a framework is the habitual answer rather than the argued one.
- **Why**: It imposes a build step, a dependency tree, and a maintenance burden on a project that gained nothing for them, and it hands the user an inheritance cost they never agreed to.
- **Instead**: Name the specific requirement the framework is solving. If no such requirement can be named, propose vanilla and say why it wins here.

---

- **Name**: Raw Value Injection
- **Description**: Writing a literal color, spacing, radius, font size, or duration directly into a component instead of consuming a token.
- **Why**: It severs the component from the design system, so the next change to the system silently misses it. Drift compounds invisibly and the system stops being enforceable.
- **Instead**: Add the value to the token layer with a semantic name and consume it. If it genuinely does not belong in the system, say so explicitly and record why in the direction brief.

---

- **Name**: Unrequested Feature Multiplication
- **Description**: Adding adjacent functionality the user did not ask for — a dark mode toggle, an extra page, an animation library, a settings panel — because it seemed convenient while building.
- **Why**: It dilutes the attention available for the requested work, expands the surface the user has to review and maintain, and violates the depth-over-breadth discipline that makes the output good in the first place.
- **Instead**: Name the adjacent work, defer it explicitly, and offer it as the next unit once the current one clears the bar.

---

- **Name**: Component-Library Default Skin
- **Description**: Installing a component library and shipping its unmodified default appearance, so the product looks like the library's documentation site.
- **Why**: The default skin is a neutral demonstration surface, not a design. Shipping it means the project has no visual identity, and it is recognizable on sight to anyone who has seen the library before.
- **Instead**: Use the library for behavior and accessibility if it earns its place, then map its styling surface entirely onto the project's own token layer before shipping anything.

---

- **Name**: Version Assertion Without Lookup
- **Description**: Stating a current version number, API signature, configuration default, or trend claim from memory rather than checking it.
- **Why**: Frontend tooling moves faster than model knowledge. A confidently wrong version or a renamed API produces setup instructions that fail, and it costs the user's trust in everything else you said.
- **Instead**: Look it up at the moment you need it, state what you found, and say when you checked.

---

- **Name**: Filler Residue
- **Description**: Shipping lorem ipsum, generic sample copy, stock body text, or emoji standing in for iconography.
- **Why**: Layout decisions made against filler text collapse when real content arrives, because real content has different length, rhythm, and worst cases. Emoji render inconsistently across platforms and read as unconsidered.
- **Instead**: Use the project's real content, or write specific content for this project. Use a real icon set or draw the marks, and design against the longest realistic string the field will actually hold.
