# Validations

This document defines the validations used by anything-tutor.

---

## Mastery Without Criterion Reference

- **Id**: tutor-mastery-without-criterion
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - A mastery-state transition (e.g., marking a unit or criterion element "mastered," "proficient," or advancing its status) is written to the log with no linked criterion-element probe result recorded in the same update.
- **Message**: Mastery rating recorded without a corresponding criterion-aligned probe result
- **Fix Action**: Run a scored probe against the fixed criterion instrument before recording any mastery-state change; if no probe exists, revert the state to its prior value and schedule the probe
- **Applies To**:
    - *.toon (learner log files)
    - any mastery-state log write

---

## Curriculum Before Criterion

- **Id**: tutor-curriculum-before-criterion
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Curriculum units, lesson content, or instruction are proposed or delivered for a subject whose log has no recorded criterion instrument.
- **Message**: Curriculum or instruction is proceeding before an external criterion instrument has been fixed and recorded
- **Fix Action**: Pause instruction, establish the criterion instrument (from supplied canon or tier-sized research), record it in the subject's log state, then resume curriculum derivation
- **Applies To**:
    - SKILL.md
    - *.toon (learner log files)

---

## Uncited Contested Claim

- **Id**: tutor-uncited-contested-claim
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - A claim taught or used in probe feedback corresponds to a field-brief entry marked contested or low-confidence, but is stated without any hedge, source attribution, or acknowledgment of disagreement.
- **Message**: Contested or low-confidence claim asserted as settled fact
- **Fix Action**: Rephrase to teach the state of the disagreement explicitly, or ask the learner which authority should govern if the conflict is material to the lesson
- **Applies To**:
    - field brief content
    - tutoring conversation content sourced from the field brief

---

## Escalation Without Gate

- **Id**: tutor-escalation-without-gate
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - The learner's stated assessment goal for an existing subject implies a materially higher stakes tier than the tier recorded in the log, and the session proceeds to teach or reuse the existing curriculum without presenting the recalibrate / reset / reuse choice.
- **Message**: Stakes escalation detected on a known subject without presenting the required choice to the learner
- **Fix Action**: Stop before teaching, state the mismatch between recorded tier and stated goal, and present recalibrate, reset, and reuse as explicit options before proceeding
- **Applies To**:
    - *.toon (learner log files)
    - session-start logic

---

## Self-Evaluation Leakage Into Mastery

- **Id**: tutor-self-eval-leakage
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - A mastery threshold, mastery rating, or criterion element is adjusted based on the tutor's own instructional self-evaluation notes rather than a criterion-aligned probe result.
- **Message**: Tutor self-evaluation is influencing a mastery rating or criterion threshold
- **Fix Action**: Revert the mastery-related change; keep the self-evaluation note in its own diagnostic record with no write access to mastery state or the criterion instrument
- **Applies To**:
    - *.toon (learner log files)

---

## Ad Hoc Review Interval Language

- **Id**: tutor-ad-hoc-review-interval
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:we'?ll|let'?s)\s+(?:revisit|review|check)\s+(?:this|that|it)\s+(?:again\s+)?(?:soon|later|next\s+time|in\s+a\s+(?:few|couple)\s+(?:days|weeks))\b
- **Message**: Review timing stated as a vague promise instead of a computed spaced-repetition interval
- **Fix Action**: Replace with a specific scheduled interval computed by the log's review-scheduling tooling and record it in the review queue
- **Applies To**:
    - tutoring conversation content

---

## Onboarding Research Leak

- **Id**: tutor-onboarding-research-leak
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Raw search results, full source excerpts, or an extended research transcript from the onboarding research pass appear directly in the tutoring conversation instead of a condensed field brief.
- **Message**: Unfiltered onboarding research material entered the tutoring context
- **Fix Action**: Delegate the onboarding research pass to a subagent and accept only its compact field brief output into the main session
- **Applies To**:
    - tutoring conversation content

---

## Absolute Path Detection

- **Id**: tutor-absolute-path
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \b/Users/[a-zA-Z0-9_\-\.]+
    - \b/home/[a-zA-Z0-9_\-\.]+
    - \b/var/folders/[a-zA-Z0-9_\-\.]+
- **Message**: Absolute path detected in skill instructions or log tooling references - breaks portability across environments and machines
- **Fix Action**: Replace absolute paths with workspace-relative paths (e.g., 'anything-tutor/references/patterns.md' instead of a full local path)
- **Applies To**:
    - SKILL.md
    - *.md
    - *.toon
