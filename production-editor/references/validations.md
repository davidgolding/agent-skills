# Validations

---

## Output Format Compliance

- **Id**: output-format-compliance
- **Severity**: error
- **Type**: semantic
- **Pattern**: For inline-commentary output, every item begins with bold referenced text, followed by a colon, followed by commentary.
- **Message**: Output must strictly follow the format: **referenced text**: commentary.
- **Fix Action**: Reformulate the suggestion to match the bold-colon format.
- **Applies To**:
    - substantive, reference, copyedit, mechanical (inline-commentary deliverables)

---

## Citation Class Compliance

- **Id**: citation-class-compliance
- **Severity**: error
- **Type**: semantic
- **Pattern**: Every reference/copyedit/mechanical commentary ends with exactly one citation matching one of the four classes in `references/citation-protocol.md`, drawn from an authority actually loaded for this pass.
- **Message**: Missing, malformed, or misattributed citation. Usage claims cite the usage authority; grammar claims cite the grammar authority; formatting claims cite the style manual; consistency-only calls cite the style sheet.
- **Fix Action**: Identify the correct citation class for the claim, locate the actual entry in a loaded reference, and append it in the matching format. If no authority supports the claim, label it `(editorial judgment)` instead.
- **Applies To**:
    - reference, copyedit, mechanical

---

## Locator Fabrication Check

- **Id**: locator-fabrication-check
- **Severity**: error
- **Type**: semantic
- **Pattern**: A precise section/locator (e.g. "section 6.32," "5.12") is cited only when it is present in a loaded style profile or user-supplied manual.
- **Message**: A precise locator was cited that does not appear in any loaded reference.
- **Fix Action**: Replace with a chapter- or rule-name citation (e.g. "CMOS 18, hyphenation table"), or omit the locator and cite the rule by name.
- **Applies To**:
    - reference, copyedit, mechanical

---

## Intake Resolution Check

- **Id**: intake-resolution-check
- **Severity**: error
- **Type**: semantic
- **Pattern**: Before any edit is produced, the edit type and every parameter that pass requires (per `references/edit-types.md`) has been either explicitly supplied by the user or confirmed after being proposed as an assumption.
- **Message**: Editing began before required intake parameters were resolved.
- **Fix Action**: Stop, state the resolved and outstanding parameters, and ask for confirmation of anything not yet confirmed before proceeding.
- **Applies To**:
    - *

---

## Pass Boundary Compliance

- **Id**: pass-boundary-compliance
- **Severity**: error
- **Type**: semantic
- **Pattern**: All edits/suggestions in the response fall within the scope defined for the requested edit type in `references/edit-types.md`; anything outside scope appears only in `## Out-of-scope observations`.
- **Message**: An edit outside the requested pass's scope was applied directly instead of being flagged separately.
- **Fix Action**: Move the out-of-scope change to the Out-of-scope observations section and revert it from the edited text.
- **Applies To**:
    - *
