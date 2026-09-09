# GMEU Copyeditor Sharp Edges

This document defines the sharp edges used by gmeu-copyeditor.

## Voice Erasure in Heavy Rewrite

- **Id**: voice-erasure-heavy-rewrite
- **Summary**: Over-rewriting convoluted passages during Heavy copyediting can lead to loss of the author's unique voice.
- **Severity**: high
- **Situation**: When the agent encounters a highly complex or convoluted sentence under a Heavy copyediting instruction and rewrites it.
- **Why**: The agent might default to standard clean prose templates, ignoring the author's consciousness philosophy.
- **Solution**: Explicitly extract and document the author's voice at the start of the process, and verify that the rewritten sentence still fits that description.
- **Symptoms**: The text sounds generic, bureaucratic, or excessively academic.
- **Detection Pattern**: Compare the syntactic variation of the original and the rewrite; if all sentence variety is flattened to standard Subject-Verb-Object, voice erasure has likely occurred.

---

## Citation Authority Misattribution

- **Id**: citation-authority-misattribution
- **Summary**: Citing grammar corrections to GMEU or usage corrections to CGG, or inventing incorrect entries or section numbers.
- **Severity**: medium
- **Situation**: When the agent suggests a correction and references the wrong authority manual or provides a hallucinated section number.
- **Why**: The agent might blur the boundary between grammatical rules (CGG) and usage conventions (GMEU).
- **Solution**: Strictly separate grammar evaluations — which concern sentence structure, word forms, and syntax — from usage evaluations — which concern specific word meanings, spelling variants, and idioms. Use CGG for the former and GMEU for the latter, verifying that the entry or section matches.
- **Symptoms**: Citations point to non-existent entries in GMEU or incorrect sections in CGG.
- **Detection Pattern**: Verify section numbers against the CGG table of contents or GMEU entry alphabetization.

---

## Unstated Voice

- **Id**: unstated-voice
- **Summary**: Editing begins before the author's voice has been identified and stated, so voice preservation has no baseline to check against.
- **Severity**: medium
- **Situation**: When suggestions are emitted immediately after the text arrives, particularly on a short excerpt where the voice reads as self-evident.
- **Why**: An unstated voice leaves each suggestion measured against the agent's own prose instincts rather than the author's, and the user has no statement to correct if the reading is wrong.
- **Solution**: State the identified voice to the user as the first output of the pass, and check each subsequent suggestion against that stated description.
- **Symptoms**: The commentary list opens with a suggestion rather than a voice statement, and no suggestion references the author's characteristic rhythm or diction.
- **Detection Pattern**: Output whose first paragraph matches the `**referenced text**:` commentary shape rather than a voice statement.

---

## Level Scope Creep

- **Id**: level-scope-creep
- **Summary**: A Light or Medium pass drifts into Heavy-level rewriting because a convoluted sentence invites it.
- **Severity**: medium
- **Situation**: When a wordy or tangled patch appears under a Light or Medium instruction, where the rubric authorizes pointing it out or suggesting a revision rather than rewriting it.
- **Why**: The repair is obvious once the problem is seen, so the pass supplies it and returns a change the user's selected level did not authorize.
- **Solution**: Check each suggestion against the selected level's rubric in `references/patterns.md` before emitting it, and hold Light-level wordiness findings to a pointer and Medium-level findings to a suggested revision.
- **Symptoms**: A Light pass returns rewritten sentences, or a Medium pass returns replacement prose for patches it was asked only to flag.
- **Detection Pattern**: Suggestions containing full replacement sentences for wordiness under a stated Light or Medium level.

---
