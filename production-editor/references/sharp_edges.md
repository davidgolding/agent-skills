# Sharp Edges

---

## Voice Erasure in Heavy Rewrite

- **Id**: voice-erasure-heavy-rewrite
- **Summary**: Over-rewriting convoluted passages during Heavy-intensity substantive or copyedit passes can erase the author's voice.
- **Severity**: high
- **Situation**: The agent encounters a highly complex or convoluted sentence under Heavy intensity and rewrites it.
- **Why**: The agent may default to standard clean-prose templates, ignoring the author's documented voice.
- **Solution**: Explicitly extract and document the author's voice at the start of the pass, and verify the rewrite still fits that description before presenting it.
- **Symptoms**: The text reads generic, bureaucratic, or excessively academic.
- **Detection Pattern**: Compare syntactic variation between original and rewrite; if all sentence variety collapses to standard Subject-Verb-Object, voice erasure has likely occurred.

---

## Citation Authority Misattribution

- **Id**: citation-authority-misattribution
- **Summary**: Citing a claim to the wrong authority class, or inventing a section/locator that doesn't exist in a loaded reference.
- **Severity**: high
- **Situation**: The agent suggests a correction and cites the wrong manual/dictionary, or supplies a section number that isn't in any loaded profile.
- **Why**: With five possible style systems and several usage authorities in play, the boundary between "usage," "grammar," "style manual," and "style sheet" is easy to blur--and a plausible-looking section number is easy to fabricate under pressure to look authoritative.
- **Solution**: Strictly separate the four citation classes (`references/citation-protocol.md`); cite a precise locator only when it's actually present in a loaded profile, and use a chapter/rule-name citation otherwise.
- **Symptoms**: Citations point to nonexistent entries, or use the wrong authority for the kind of claim being made.
- **Detection Pattern**: Spot-check any precise section number against the loaded profile's actual contents; anything not traceable to a loaded source is a fabrication.

---

## Pass Bleed

- **Id**: pass-bleed
- **Summary**: A requested pass quietly expands into a different edit type--e.g. a proofread that becomes a line edit, or a mechanical pass that starts rewording sentences.
- **Severity**: medium
- **Situation**: The agent notices an issue outside the requested pass's scope and fixes it inline instead of flagging it separately.
- **Why**: Real prose problems are often adjacent to whatever the agent is looking at, and fixing them feels helpful in the moment--but it violates the intensity/scope the user actually asked for and can introduce unwanted changes into a deliverable meant to be narrowly scoped (e.g. a proofread pass right before print).
- **Solution**: Apply the pass-boundary rule in `references/edit-types.md`--anything outside scope goes only in `## Out-of-scope observations`, kept out of the edited text.
- **Symptoms**: A proofreading or mechanical deliverable contains rewritten sentences or restructured paragraphs.
- **Detection Pattern**: Diff the edited text against the original; every change should be explainable by the requested edit type alone.

---

## Style Sheet Drift

- **Id**: style-sheet-drift
- **Summary**: A later pass contradicts a decision already settled on the project's style sheet.
- **Severity**: medium
- **Situation**: The agent makes a fresh ruling on a word, hyphenation, or capitalization question that was already settled earlier in the same project.
- **Why**: Without checking the style sheet first, each pass re-derives consistency decisions independently, producing an inconsistent manuscript--the exact failure a style sheet exists to prevent.
- **Solution**: Always read the active project's section of `references/stylesheet.md` before editing (Phase 2); treat settled entries as binding.
- **Symptoms**: The same term is styled two different ways across a manuscript, or two passes cite conflicting rulings for the same word.
- **Detection Pattern**: Grep the edited manuscript for repeat terms flagged on the style sheet; check that every occurrence matches the ruling.

---

## Unverified Reference Claims

- **Id**: unverified-reference-claims
- **Summary**: Asserting during a Heavy reference pass that a cited source "checks out" without actually having verified it.
- **Severity**: high
- **Situation**: A Heavy-intensity reference pass calls for verifying that cited sources exist and their metadata is correct, and the agent asserts verification it didn't perform (e.g. no way to access the source).
- **Why**: A false claim of verification is worse than no verification at all--it gives the author false confidence in the manuscript's accuracy.
- **Solution**: State explicitly, per source, whether verification succeeded, failed, or could not be attempted (and why)--assert a source checks out only after actually having checked it.
- **Symptoms**: A reference pass reports "all sources verified" with no indication of method or access.
- **Detection Pattern**: For any "verified" claim, confirm the agent's response names how it checked (database, search, provided text)--an unsupported blanket assertion is a red flag.
