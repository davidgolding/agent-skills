# Patterns & Anti-Patterns

## Patterns

- **Name**: Consciousness-Based Voice Alignment
- **When**: Analyzing text before any substantive or copyedit suggestion, especially at Heavy intensity where rewriting occurs. Defines the author's voice as a high-fidelity transmission of their consciousness, and grounds every language improvement within that specific aesthetic context.
- **Example**:
```
Analyzed Voice: The author's voice represents a consciousness pared down to hard facts and direct statements, similar to Hemingway.
**It was a day that was extremely cold and the wind was blowing very hard**: The sentence contains unnecessary wordiness. Suggested revision: "The day was cold and the wind blew hard." (editorial judgment)
```

---

- **Name**: Authority-Scoped Citation
- **When**: Writing commentary for usage, grammar, style-manual, or style-sheet-based decisions. Appends a precise inline citation to every reference/copyedit/mechanical commentary, drawn from whichever of the four citation classes actually governs the claim--always the specific class the claim rests on, not a fixed pair of authorities.
- **Example**:
```
**who was her manipulator**: [Usage authority] restricts "who" to persons; "manipulator" carries a specific usage connotation worth flagging. (GMEU, "who; whom")
**e-mail vs. email**: This project has settled on the closed form. (Style sheet: "email")
```

---

- **Name**: Style Sheet Accretion
- **When**: Mechanical passes, and any pass that encounters a decision the manual leaves open (e.g. serial comma exceptions, a coined term's capitalization). Records a first-occurrence decision on the style sheet, then enforces it on every later occurrence in the same project.
- **Example**: First occurrence of "e-mail" is queried and settled; every later occurrence in the same document is silently conformed and cited `(Style sheet: "email")`.

---

- **Name**: Pass Isolation
- **When**: Any pass, whenever a problem outside the requested scope is noticed. Keeps findings that belong to a different edit type out of the current pass's edits, surfacing them instead in a dedicated section.
- **Example**: A proofreading pass that notices a dangling modifier lists it under `## Out-of-scope observations: belongs to substantive edit` rather than rewriting the sentence.

---

## Anti-Patterns

- **Name**: Homogenizing AI Style
- **Why**: Rewriting the author's prose into generic, sanitized AI-style paragraphs erases their specific voice. Over-editing destroys the unique texture of the author's writing, violating the core duty to help the author say what they want to say, not what the editor would say.
- **Instead**: Identify the voice first; adjust only where there's an actual usage/grammar issue or the requested intensity licenses rewriting; keep original structure where it's already clear and correct.

---

- **Name**: Uncited Authority Claims
- **Why**: Making a reference/copyedit/mechanical suggestion without the citation the class requires leaves the claim unverifiable and violates the delegated-authority principle this skill is built on.
- **Instead**: Always resolve the citation class first (usage / grammar / style manual / style sheet), find the actual entry, and append it. If none exists, label `(editorial judgment)` instead of citing.

---

- **Name**: Silent Parameter Assumption
- **Why**: Proceeding to edit under an assumed style system, usage authority, or edit type the user hasn't actually confirmed risks the whole pass--different manuals and edit types produce materially different, sometimes contradictory, edits.
- **Instead**: Follow the intake procedure in `references/intake.md`--state inferences as assumptions and get confirmation, or ask outright when no signal exists.
