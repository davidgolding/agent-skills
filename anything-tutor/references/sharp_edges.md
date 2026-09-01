# Sharp Edges

This document defines the sharp edges used by anything-tutor.

---

## Self-Graded Mastery

- **Id**: self-graded-mastery
- **Summary**: The tutor rates a unit as mastered based on its own impression of how the lesson went, rather than on a criterion-aligned probe result.
- **Severity**: critical
- **Situation**: A session goes smoothly, the learner seems to follow along and asks good questions, and the tutor marks the unit mastered without running a probe scored against the fixed criterion threshold.
- **Why**: The tutor selects the material, runs the probe, and judges the answer in every tutoring interaction. If it also sets the bar for "mastered," the rating measures the tutor's satisfaction with its own teaching, not the learner's actual capability — the exact failure mode that makes a 2-sigma claim untestable.
- **Solution**:
    - Require a scored, criterion-aligned probe result before any mastery-state transition.
    - Keep the tutor's own effectiveness notes in a separate, clearly diagnostic-only record.
    - Never let a mastery threshold move because a session felt productive.
- **Symptoms**:
    - Mastery ratings advance with no corresponding probe score in the log.
    - The learner is later surprised by a real assessment result that contradicts the log's mastery map.
- **Detection Pattern**: A mastery-state write in the log with no linked criterion-element probe result, or a rating justified by session tone rather than a scored answer.

---

## Curriculum Before Criterion

- **Id**: curriculum-before-criterion
- **Summary**: The tutor builds or begins teaching a curriculum before fixing an external criterion instrument for expert performance.
- **Severity**: critical
- **Situation**: A new subject is named and the tutor jumps straight to lesson one, using whatever it happens to know about the topic, without first establishing what the learner will actually be evaluated against.
- **Why**: Without a criterion fixed first, curriculum content reflects the tutor's own knowledge distribution rather than the standard the learner needs to meet, and there is nothing external to check "mastered" against later.
- **Solution**:
    - Always produce and record a criterion instrument — from supplied canon or tier-sized research — before deriving curriculum units.
    - Trace every curriculum unit back to a specific criterion element.
    - Surface any criterion element with no covering unit as an explicit gap.
- **Symptoms**:
    - Curriculum units exist in the log with no reference to a criterion element.
    - The learner cannot answer "what am I being measured against" at any point in the subject.
- **Detection Pattern**: Curriculum content recorded or taught before a criterion instrument exists in the subject's log state.

---

## Stale State on Stakes Escalation

- **Id**: stale-state-stakes-escalation
- **Summary**: The tutor reuses an existing subject's curriculum, criterion, and mastery ratings after the learner's stated stakes have materially increased, without surfacing the mismatch.
- **Severity**: high
- **Situation**: A subject was onboarded for a course quiz months ago; the learner now says they're preparing for a certification or comprehensive exam in the same subject, and the tutor continues teaching from the old plan.
- **Why**: A criterion and curriculum built for one stakes tier do not transfer to a higher one — the mastery ratings on file were validated against a bar that no longer applies, and treating them as still valid produces false confidence exactly where the consequences of being wrong are highest.
- **Solution**:
    - Compare the learner's stated goal against the recorded tier at the start of every session on a known subject.
    - On any material mismatch, stop before teaching and present recalibrate / reset / reuse as an explicit choice.
    - On recalibrate, carry prior mastery evidence forward as provisional only, pending re-test against the new criterion.
- **Symptoms**:
    - Teaching proceeds on a known subject after the learner has described a higher-stakes goal, with no acknowledgment of the change.
    - Mastery ratings from a lower tier are treated as valid evidence for a higher-tier assessment.
- **Detection Pattern**: A session on an existing subject where the learner's stated assessment context implies a higher stakes tier than the tier recorded in the log, with no escalation choice presented.

---

## Onboarding Context Flood

- **Id**: onboarding-context-flood
- **Summary**: Raw search results, full source documents, or an unfiltered research transcript from subject onboarding enter the main tutoring context instead of a compact field brief.
- **Severity**: high
- **Situation**: Onboarding a new, research-heavy subject pulls in long articles, multiple source excerpts, or an extended search trace directly into the conversation the learner is tutored in.
- **Why**: Source triage material dilutes the tutor's attention on the actual tutoring task for the rest of the session and crowds out room for the learner's own work and the log's context.
- **Solution**:
    - Delegate subject-authority research to a subagent.
    - Require the subagent to return only a compact field brief with confidence markers, not raw sources or search transcripts.
    - Discard or leave undelegated any research material that would otherwise enter the main session context wholesale.
- **Symptoms**:
    - Long blocks of pasted source text or search results appear in the tutoring conversation.
    - The tutor's responses become slower or less focused immediately after an onboarding pass.
- **Detection Pattern**: Multi-paragraph raw source excerpts or search-tool output appearing directly in the tutoring conversation rather than a condensed brief.

---

## Silent Assertion of Contested Claims

- **Id**: silent-assertion-contested-claims
- **Summary**: The tutor states a claim the field brief marked as contested or low-confidence as though it were settled, uncontested fact.
- **Severity**: high
- **Situation**: A field is actively debated or fast-moving, the researched field brief flags a claim as contested, and the tutor teaches it flatly as the answer during a lesson or probe feedback.
- **Why**: A learner assessed later against the real state of the field is penalized for confidence the tutor gave them no reason to question, and the tutor's credibility is damaged the first time the flat assertion turns out to be one side of a live disagreement.
- **Solution**:
    - Check any claim against its field-brief confidence marker before asserting it.
    - For contested or low-confidence claims, teach the state of the disagreement explicitly rather than picking a side silently.
    - When a claim cannot be confidently verified at all, ask the learner which authority should govern rather than guessing.
- **Symptoms**:
    - The tutor states a claim with no hedge or acknowledgment of debate on a topic the field brief flagged as contested.
    - The learner later encounters an authoritative source that contradicts what was taught as settled.
- **Detection Pattern**: A confident, unqualified assertion in tutoring content that corresponds to a field-brief claim marked contested or low-confidence.

---

## Hand-Maintained Log Drift

- **Id**: log-drift
- **Summary**: The persistent TOON log is read, written, or transitioned by hand within the conversation rather than through deterministic tooling, allowing schema or state corruption to accumulate silently.
- **Severity**: medium
- **Situation**: Deep into a long session, the tutor composes a log update inline from memory of the schema instead of invoking the log tooling, and a field is malformed, omitted, or inconsistent with a prior entry.
- **Why**: The log is the skill's only cross-session memory; anything load-bearing that depends on sustained model attention many turns into a session degrades exactly where it matters most — long-horizon continuity.
- **Solution**:
    - Route every log read, write, and mastery-state transition through the bundled deterministic tooling.
    - Never hand-compose a log diff mid-conversation as a shortcut.
    - Validate the log's structure after any update before trusting it in the same session.
- **Symptoms**:
    - Log entries with inconsistent field names, missing sections, or malformed structure across sessions.
    - Session-resume behavior that contradicts what a prior session actually recorded.
- **Detection Pattern**: A log write performed as free-form text composition within the conversation rather than a tool invocation, or a resumed session whose reconstituted state disagrees with the prior session's recorded outcome.

---

## Ad Hoc Review Scheduling

- **Id**: ad-hoc-review-scheduling
- **Summary**: Review timing for previously studied material is decided by in-conversation guess ("let's check this again soon") instead of a computed spaced-repetition schedule.
- **Severity**: medium
- **Situation**: The tutor tells the learner it will revisit a topic "in a few days" or "next time" without recording a scheduled interval tied to a spacing algorithm.
- **Why**: Spacing effects are among the most reliable gains in the learning literature, but only when intervals are actually tracked and honored; ungoverned guesses drift and the review queue silently stops reflecting real decay.
- **Solution**:
    - Compute every review interval through the log's spaced-repetition tooling, keyed to the current date.
    - Treat "overdue" as a computed property of the queue at session start, never an impression.
    - Surface the actual overdue queue rather than a vague promise to revisit later.
- **Symptoms**:
    - The log's review queue has no scheduled dates, or dates that don't correspond to any documented algorithm.
    - Topics the learner previously struggled with are never resurfaced despite elapsed time.
- **Detection Pattern**: Review-related language in the conversation ("we'll revisit this soon") with no corresponding scheduled entry in the log's review queue.

---

## Thin-Tier Overreach

- **Id**: thin-tier-overreach
- **Summary**: Building a full criterion blueprint and exhaustive curriculum for a low-stakes request, delaying the start of actual teaching.
- **Severity**: medium
- **Situation**: A learner says they need to review for tomorrow's short quiz, and the tutor responds by researching the entire field and drafting a comprehensive blueprint before teaching a single concept.
- **Why**: Effort must scale with stated stakes; over-building at low tiers wastes the learner's limited time and defeats the purpose of a fast, useful low-stakes session.
- **Solution**:
    - Confirm the stakes tier first, and at low tiers build only a short, representative item set as the criterion instrument.
    - Begin teaching within the first few turns for low-stakes requests.
    - Reserve full blueprint construction and baseline probes for tiers that warrant them.
- **Symptoms**:
    - A same-day or short-timeline request results in extended research or planning before any instruction occurs.
    - The learner explicitly expresses impatience or restates the limited time available.
- **Detection Pattern**: Research or criterion-building activity disproportionate to a stated near-term, low-stakes deadline.

---

## Modality Overreach

- **Id**: modality-overreach
- **Summary**: The tutor claims or implies it can directly observe or verify a physical, performance, or hands-on skill (an instrument, a lab technique, a clinical procedure) rather than coaching and relying on the learner's self-report.
- **Severity**: medium
- **Situation**: A learner is practicing a skill that requires physical execution the tutor cannot see or hear, and the tutor's feedback is phrased as though it directly assessed the performance rather than the learner's description of it.
- **Why**: A text-based tutor has no channel for direct observation of physical performance; treating self-report as direct evidence overstates the reliability of the mastery rating for that skill.
- **Solution**:
    - Design the practice protocol and probes for the skill, but base any mastery judgment explicitly on the learner's self-report or described outcome, not on claimed direct observation.
    - State the evidentiary limitation to the learner when it is relevant to how much to trust a mastery rating in that domain.
- **Symptoms**:
    - Feedback language implies the tutor watched or heard the performance directly.
    - A mastery rating for a physical or performance skill carries the same confidence framing as one based on a written or verbal probe.
- **Detection Pattern**: Feedback or mastery-rating language for a physical/performance skill that does not acknowledge it is based on the learner's self-report rather than direct observation.
