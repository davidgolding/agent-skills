# Edit Types

Six passes, each independently invokable. One pass per invocation--see Principle 4 (Pass isolation) in `SKILL.md`.

---

## Developmental

**Scope:** structure, argument, audience fit, scope, chapter/section sequence, gaps and redundancies at the macro level--the shape of the whole, not the sentences.
**Out of bounds:** line-level wording, grammar, citation formatting, mechanics.
**Required authorities:** none--genre and audience conventions, not a style manual.
**Intensity:**
- *Light:* Note the most significant structural issues only.
- *Medium:* Full structural review--organization, argument gaps, audience mismatch, redundant sections.
- *Heavy:* As Medium, plus proposed restructuring (a new outline or section order), still without touching prose.
**Output:** an editorial memo--prose framing plus a numbered list of recommendations. Not an inline commentary list.

---

## Substantive (line)

**Scope:** paragraph- and sentence-level flow, transitions, pacing, diction, redundancy, dead metaphor, tonal consistency.
**Out of bounds:** wholesale restructuring (developmental), citation/reference formatting, spelling/punctuation consistency (mechanical).
**Required authorities:** usage authority in force; style manual generally not needed.
**Intensity:**
- *Light:* Flag issues only, no suggested rewrites.
- *Medium:* Flag and suggest a specific revision for each issue.
- *Heavy:* Rewrite wordy or convoluted passages, preserving the documented voice (Principle 1).
**Output:** inline commentary list (see format in `references/citation-protocol.md` / `references/validations.md`).

---

## Reference

**Scope:** notes, in-text citations, bibliography/works-cited/reference list--format compliance against the named citation system, note numbering, cross-reference integrity, citation-to-bibliography alignment, alphabetization, ibid./short-form handling.
**Out of bounds:** prose quality, mechanics unrelated to citations.
**Required authorities:** the named citation/style system profile (`references/styles/`).
**Intensity:**
- *Light:* Format compliance only.
- *Medium:* + internal consistency and completeness of each entry (all required elements present).
- *Heavy:* + verify that cited sources exist and their metadata is correct where verifiable; state explicitly when a source could not be verified rather than asserting it checks out.
**Output:** inline commentary list, keyed to note/entry number.

---

## Copyedit

**Scope:** grammar, syntax, usage, punctuation, agreement, modifier placement.
**Out of bounds:** structural or citation issues; spelling/hyphenation/capitalization consistency belongs to mechanical, though an isolated typo encountered along the way may be corrected silently.
**Required authorities:** named style manual + named usage authority, both in force.
**Intensity:**
- *Light:* Correct indisputable grammar/syntax/usage errors. Ignore non-outright errors. Point out, without revising, egregiously wordy paragraphs. Ignore minor wordiness/jargon. Query new terms.
- *Medium:* Correct all grammar/syntax/usage errors. Revise or point out infelicities. Point out wordy patches and suggest revisions. Define or query new terms.
- *Heavy:* Correct all errors and infelicities. Rewrite wordy or convoluted patches while preserving the documented voice. Define or query new terms.
**Output:** inline commentary list, one bold-referenced-text-plus-colon paragraph per item, cited per `references/citation-protocol.md`.

---

## Mechanical

**Scope:** consistency only--spelling variants, hyphenation and compounds, capitalization, number style, abbreviations, italics vs. roman, quotation and dash conventions, list formatting, serial comma, correlating parts (numbering of notes/tables/figures).
**Out of bounds:** anything that changes meaning or wording choice.
**Required authorities:** named style manual; this is the pass most tightly coupled to `references/stylesheet.md`--every decision not settled by the manual gets recorded there and enforced on all subsequent passes for this project.
**Intensity:** single--mechanical editing is either done or not; there is no Light/Medium/Heavy distinction.
**Output:** inline commentary list for ambiguous/first-occurrence decisions; silent correction for decisions already settled on the style sheet.

---

## Proofread

**Scope:** typographical errors, misspellings, transpositions, duplicated or dropped words, spacing, bad breaks, running-head and folio errors.
**Out of bounds:** anything beyond a typo--no substantive change permitted. If a proofread pass surfaces a real grammar or wording problem, query it rather than fixing it.
**Required authorities:** dialect/spelling default only (e.g. Merriam-Webster vs. Oxford); no usage or grammar authority, no citations required.
**Intensity:** single.
**Output:** inline list of corrections; queries for anything beyond scope, in the "Out-of-scope observations" section.

---

## Pass-boundary rule

Applies across all six: a problem noticed that belongs to a different pass always routes to a separate `## Out-of-scope observations` section at the end of the response, naming which pass would address it, rather than being folded into the current edit.
