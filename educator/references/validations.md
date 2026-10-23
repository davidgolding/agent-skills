# Validations

This document defines the validations used by educator.

---

## Required Criteria Established

- **Id**: educator-required-criteria
- **Severity**: error
- **Type**: schema
- **Pattern**: A Build or Audit output produced before all five required criteria are known from the prompt or the interview: learner developmental level(s), subject, prior knowledge of the subject, time and format, and setting and constraints.
- **Message**: The design cannot be fitted to the learners until all five required criteria are established.
- **Fix Action**: Return to the interview phase in `references/interactions.md` and ask for the first missing criterion.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Inferred Criteria Stated

- **Id**: educator-inferred-criteria-stated
- **Severity**: error
- **Type**: semantic
- **Pattern**: A Build or Audit output whose evidence notes do not state the inferred learning goal and whether the task is well-structured or ill-structured.
- **Message**: Inferred criteria must be visible so the requester can correct them.
- **Fix Action**: Add an "Inferred" line to the "Why this design" section naming the learning goal and task structure, with an invitation to correct either.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Evidence Notes Present and Separate

- **Id**: educator-evidence-notes
- **Severity**: error
- **Type**: schema
- **Pattern**: A Build or Audit output without a closing section headed "Why this design", or with citations, effect sizes, or mechanism explanations inside the deliverable body.
- **Message**: The deliverable must stay classroom-ready, with all justification in the closing evidence notes.
- **Fix Action**: Move justification out of the body into a closing "Why this design" section that maps each major design choice to its finding.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Guidance Matches Expertise

- **Id**: educator-guidance-matches-expertise
- **Severity**: error
- **Type**: semantic
- **Pattern**: Novice learners given independent problem solving or open discovery on high-interactivity material before worked examples; experienced learners given full worked examples throughout; or any practice sequence with no fading toward independence.
- **Message**: Guidance must match element interactivity and prior knowledge, and must fade as expertise grows.
- **Fix Action**: Apply Interactivity-Matched Guidance and Guidance Fading Off-Ramp from `references/patterns.md`, stating the fade trigger.
- **Applies To**:
    - Build outputs
    - Audit revisions

---

## Retrieval and Spacing Scheduled

- **Id**: educator-retrieval-spacing
- **Severity**: error
- **Type**: semantic
- **Pattern**: A multi-session Build with no low-stakes retrieval practice, no revisiting of earlier content in later sessions, or retrieval placed only immediately after demanding new instruction.
- **Message**: Multi-session designs must schedule spaced retrieval with feedback, placed after a gap rather than immediately after heavy study.
- **Fix Action**: Apply Spaced Retrieval Schedule from `references/patterns.md`.
- **Applies To**:
    - Build outputs (units, courses, training programs)

---

## Segment Load Within Limits

- **Id**: educator-segment-load
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An instructional segment that introduces more than about four new interacting elements before a check, or materials that separate diagrams from labels, pair narration with identical on-screen text, or include decorative content.
- **Message**: The segment risks overloading working memory with intrinsic or extraneous load.
- **Fix Action**: Split the segment, add a check, and apply Segmented Low-Load Delivery from `references/patterns.md`.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Developmental Fit

- **Id**: educator-developmental-fit
- **Severity**: error
- **Type**: semantic
- **Pattern**: A design whose concreteness, relational demands, self-regulation demands, feedback rhythm, or sensory presentation conflicts with the learners' developmental profile, adjusted for their prior knowledge (for example, symbolic notation first for 6-year-olds, a single end-of-term assessment as the only feedback for adolescents, small low-contrast type for older adults).
- **Message**: The design does not fit the learners' developmental profile.
- **Fix Action**: Apply the matching developmental pattern in `references/patterns.md`: Concrete-Representational-Abstract Sequencing, Externalized Control for Young Learners, Adolescent Micro-Cycles and Structured Peer Explanation, Prior-Knowledge Activation, Contrastive Comparison for Retraining, or Sensory and Pacing Accommodation for Older Adults.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Excluded Claims Absent

- **Id**: educator-excluded-claims
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?i)\blearning\s+styles?\b
    - (?i)\b(?:VAK|VARK)\b
    - (?i)\b(?:left|right)[\s-]brain(?:ed)?\b
    - (?i)\blearning\s+pyramid\b
    - (?i)\bbrain\s+gym\b
    - (?i)\bandragog(?:y|ical)\b
    - (?i)\bPerry'?s?\s+(?:scheme|positions?)\b
    - (?i)\bpomodoro\b
    - (?i)\bworry\s+list\b
- **Message**: An excluded framework or myth appears in the output. It may appear only when the output is correcting it or answering a direct question about its evidence.
- **Fix Action**: Remove the claim from the design rationale and base the choice on a retained finding, or, if the requester asked about the claim, give an honest Advise-mode verdict.
- **Applies To**:
    - Build outputs
    - Audit outputs
    - Advise outputs

---

## Conflict Gate Honored

- **Id**: educator-conflict-gate
- **Severity**: error
- **Type**: semantic
- **Pattern**: A response that builds a deliverable in the same turn it first identifies a conflict between the request and the evidence, or that builds a contradicted element without flagging it.
- **Message**: Evidence conflicts require a stated correction, an offered alternative, and the requester's choice before building.
- **Fix Action**: Replace the deliverable with the conflict statement and alternative, and end the turn per `references/interactions.md`.
- **Applies To**:
    - Build outputs
    - Audit outputs

---

## Out-of-Core Sources Labeled

- **Id**: educator-out-of-core-labeled
- **Severity**: error
- **Type**: semantic
- **Pattern**: A finding used in the output that is not part of the integrated core evidence base and lacks a citation or the label "outside the core evidence base."
- **Message**: Findings beyond the integrated core must be cited and labeled so the requester can weigh them.
- **Fix Action**: Search current peer-reviewed syntheses, add the citation, and add the label in the evidence notes per Out-of-Core Research Labeling.
- **Applies To**:
    - Build outputs
    - Audit outputs
    - Advise outputs

---

## Audit Findings Classified

- **Id**: educator-audit-classified
- **Severity**: error
- **Type**: schema
- **Pattern**: An Audit output that does not sort elements into supported, contradicted, and not addressed by the evidence, or that lists a contradicted element without a concrete revision.
- **Message**: Audits must classify every element and give a revision for each contradicted one.
- **Fix Action**: Apply Three-Way Audit Classification from `references/patterns.md`.
- **Applies To**:
    - Audit outputs

---

## Advise Answer Complete

- **Id**: educator-advise-complete
- **Severity**: error
- **Type**: schema
- **Pattern**: An Advise output missing a leading verdict (works, works under conditions, does not work, or evidence unclear), the mechanism, or the boundary conditions.
- **Message**: Advise answers must lead with a verdict and give the mechanism and the conditions that change it.
- **Fix Action**: Apply Verdict-Mechanism-Boundary Answer from `references/patterns.md`.
- **Applies To**:
    - Advise outputs

---

## Mixed Group Differentiated

- **Id**: educator-mixed-group
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A Build for learners spanning more than one developmental band or expertise level that does not name the governing least-experienced profile or give differentiation for the others.
- **Message**: Mixed groups need a core designed for the least-experienced profile plus stated differentiation.
- **Fix Action**: Apply Least-Experienced Profile for Mixed Groups from `references/patterns.md`.
- **Applies To**:
    - Build outputs

---

## One Question Per Interview Turn

- **Id**: educator-one-question
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An interview turn containing more than one question, or asking for a criterion already present in the prompt, or asking for the learning goal.
- **Message**: The interview asks only for missing required criteria, one per turn.
- **Fix Action**: Keep the single most important missing criterion, in the order set by `references/interactions.md`, and remove the rest.
- **Applies To**:
    - Interview turns

---

## Plain-Language Evidence Notes

- **Id**: educator-plain-evidence
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Evidence notes that rely on unexplained technical terms, brain-region names, or statistics that do not change what the teacher should do.
- **Message**: Evidence notes must be actionable for a teacher, not decorative.
- **Fix Action**: Restate each note as the choice, what the evidence shows, and the condition that makes it apply; keep a statistic only when it helps the teacher weigh the choice.
- **Applies To**:
    - Build outputs
    - Audit outputs
