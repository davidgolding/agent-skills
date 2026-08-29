# Validations

This document defines the validations used by frontend-designer.

---

## Raw Value Outside The Token Layer

- **Id**: fd-raw-value-outside-tokens
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - #(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b
    - \b(?:rgba?|hsla?|oklch|oklab|lab|color-mix)\s*\(
    - (?:padding|margin|gap|border-radius|font-size|line-height)\s*:\s*[\d.]+(?:px|rem|em)
- **Message**: Raw color, spacing, radius, or type value found in a component file instead of a token reference
- **Fix Action**: Move the value into the token layer under a semantic name and consume it through a token reference in the component. If the value genuinely does not belong to the system, state why and record the exception in the project's direction brief. This rule does not apply to the token definition file itself, where literal values are expected.
- **Applies To**:
    - *.css
    - *.scss
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte

---

## Interactive Element Without Visible Focus

- **Id**: fd-missing-focus-style
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Any interactive element — link, button, form control, custom control, or element carrying an interactive role — that has no visible focus style, or whose default focus indicator was removed without a replacement.
    - Any rule that clears the browser's default focus indicator with no accompanying focus-visible style defined for the same element.
- **Message**: Interactive element has no visible focus indicator, making it unusable for keyboard navigation
- **Fix Action**: Define a focus-visible style for the element using the project's token values, with contrast sufficient against every background the element appears on. Removing the default indicator is only acceptable when a replacement is defined in the same rule set.
- **Applies To**:
    - *.css
    - *.scss
    - *.html
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte

---

## Non-Semantic Interactive Markup

- **Id**: fd-non-semantic-interactive
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - <(?:div|span)\b[^>]*\bon(?:Click|click)\b
    - <(?:div|span)\b[^>]*\brole=["'](?:button|link|checkbox|tab|menuitem)["']
    - <h([1-6])\b[^>]*>(?:(?!</h\1>).)*</h\1>\s*(?:<[^>]+>\s*)*<h(?!\1)[1-6]\b
- **Message**: Interactive behavior or heading structure expressed through generic elements rather than semantic markup
- **Fix Action**: Replace the generic element with the native element that carries the behavior — a button, anchor, or form control. When a custom control is genuinely unavoidable, implement the complete keyboard interaction contract for its role alongside the attributes. Keep heading levels sequential without skipping.
- **Applies To**:
    - *.html
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte

---

## Missing Direction Brief

- **Id**: fd-missing-direction-brief
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Component or page code written into a project that contains no direction brief and no design tokens file, where the agent never authored one during the session.
    - A session that produced visual output without any statement of which context rung the Phase 0 resolution order landed on.
- **Message**: Design work was produced without a committed direction brief governing it
- **Fix Action**: Author a direction brief in the project recording the chosen direction, its reasoning, the Forced Commitment Set, and the project-specific anti-patterns, then confirm the built components conform to it. When an existing brief or token file was already present, state that it was read and is governing this work.
- **Applies To**:
    - *.html
    - *.css
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte

---

## Default Font Stack Without Reason

- **Id**: fd-default-font-stack
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - font-family\s*:\s*(?:["']?(?:Inter|Geist|Roboto|Open Sans|Montserrat|Poppins)["']?|system-ui|-apple-system|ui-sans-serif)\b
    - \bfont-(?:sans|serif|mono)\b(?!.*var\()
- **Message**: Typography relies on a default or ubiquitous font stack with no stated reason, a primary marker of undifferentiated design
- **Fix Action**: Commit to a type pairing chosen for this project with the reason recorded in the direction brief, and expose it through token values. When a system or ubiquitous stack is genuinely the right answer — a performance floor, an offline requirement, a brand mandate — state that reason in the brief so later sessions do not relitigate it.
- **Applies To**:
    - *.css
    - *.scss
    - *.html

---

## Emoji As Iconography

- **Id**: fd-emoji-as-icon
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - An emoji character used as an interface element — a button affordance, a list bullet, a status marker, a feature icon, or a navigation glyph — rather than appearing inside user-authored content.
    - A pictographic character standing in a position where the direction's icon set would otherwise supply a mark.
- **Message**: Emoji used as interface iconography, which renders inconsistently across platforms and reads as unconsidered
- **Fix Action**: Replace emoji with a real icon set consistent with the direction's line weight and corner language, or with drawn marks. Emoji remain acceptable inside user-authored content and copy, not as interface elements.
- **Applies To**:
    - *.html
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte

---

## Filler Content Left In Place

- **Id**: fd-filler-content
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\blorem\s+ipsum\b
    - (?i)\b(?:dolor\s+sit\s+amet|consectetur\s+adipiscing)\b
    - (?i)>\s*(?:Your\s+(?:headline|title|text)\s+here|Card\s+title|Feature\s+(?:one|two|three)|Sample\s+text)\s*<
- **Message**: Filler or sample copy present in the built output
- **Fix Action**: Replace with the project's real content, or content written specifically for this project. Verify the layout still holds against the longest realistic string each field will carry, since filler text hides the worst case.
- **Applies To**:
    - *.html
    - *.jsx
    - *.tsx
    - *.vue
    - *.svelte
    - *.md

---

## Animation Without A Reduced-Motion Path

- **Id**: fd-missing-reduced-motion
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?s)\b(?:transition|animation)\s*:(?:(?!prefers-reduced-motion).)*$
    - (?s)@keyframes\b(?:(?!prefers-reduced-motion).)*$
- **Message**: Transitions or keyframe animations defined with no reduced-motion branch anywhere in the project
- **Fix Action**: Add a reduced-motion media query that removes or substantially shortens the movement. Large-area, parallax, and auto-playing motion should be removed under reduced motion rather than merely slowed.
- **Applies To**:
    - *.css
    - *.scss
    - *.jsx
    - *.tsx

---

## Uniform Surface Treatment

- **Id**: fd-uniform-surface-treatment
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Every raised surface in the project carrying the same corner radius and the same shadow value, with no distinction between elevation levels or surface roles.
    - A primary content region composed of equally sized cards in an evenly divided grid, where the content itself has no equal weighting.
    - Padding applied at a single uniform value across containers of different scale and density.
- **Message**: Surfaces are treated uniformly, producing the flattened, undifferentiated look characteristic of generated interfaces
- **Fix Action**: Differentiate the corner, elevation, and density language by surface role as recorded in the direction brief. Let content hierarchy drive size and prominence rather than dividing the region evenly, and scale padding with container size.
- **Applies To**:
    - *.css
    - *.scss
    - *.html
    - *.jsx
    - *.tsx

---

## Machine-Specific Path Or Address

- **Id**: fd-machine-specific-reference
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \/(?:Users|home)\/[a-zA-Z0-9_.-]+\/
    - \b(?:127\.0\.0\.1|0\.0\.0\.0)\b
    - \/\/[a-z]+\.local\b
- **Message**: Generated file contains a machine-specific filesystem path or a fixed loopback address, which breaks the project on any other machine
- **Fix Action**: Use project-relative paths and parameterize server addresses through configuration or environment values. Report the running development address to the user from the server's own output rather than writing a fixed address into project files.
- **Applies To**:
    - *.html
    - *.css
    - *.js
    - *.jsx
    - *.ts
    - *.tsx
    - *.json
    - *.md
