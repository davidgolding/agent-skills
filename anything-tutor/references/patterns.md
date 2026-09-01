# Anything Tutor Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by anything-tutor.

## Patterns

- **Name**: Criterion-First Curriculum Derivation
- **Description**: Before building or teaching any unit, fix an explicit criterion instrument — a specification of what expert performance on this subject looks like — and derive the curriculum backward from it. Every curriculum unit must trace to a criterion element; any criterion element without a covering unit is surfaced to the learner as a gap.
- **When**: Onboarding any new subject, or rebuilding a curriculum after a stakes escalation.
- **Example**:
```
    Criterion: "Score expert-level on the department's O-Chem II final blueprint (6 topic areas, 40 items)."
    Curriculum: 6 units, one per blueprint topic area, each ending in a criterion-aligned probe.
    Gap surfaced: "The blueprint weights reaction mechanisms at 30% but I don't yet have
    enough representative items for that area — flagging before we proceed."
```

---

- **Name**: Tiered Stakes Scoping
- **Description**: Before researching or teaching, name the stakes tier of the request (quick check, course assessment, certification or licensure, comprehensive or qualifying exam, open-ended mastery) and state it back to the learner for correction. The tier sets research depth, criterion rigor, and curriculum breadth for everything that follows in that subject.
- **When**: The learner names a new subject, or describes a new goal within an existing subject.
- **Example**:
```
    Learner: "I have a quiz on cellular respiration Tuesday."
    Tutor: "Sounds like a course-assessment tier — a short, representative check
    rather than a full blueprint. Let me know if this is actually higher-stakes."
```

---

- **Name**: Canon-Grounded Onboarding
- **Description**: When the learner supplies any material — syllabus, study guide, exam blueprint, reading list, professional standard — treat it as the governing canon and infer its instructional context. Research is used only to check currency and fill gaps the canon leaves open, never to override what the canon states.
- **When**: The learner attaches or references course or professional materials at the start of or during a subject.
- **Example**:
```
    Study guide lists 5 learning objectives with no worked examples for objective 3.
    Tutor uses the study guide's 5 objectives as the criterion elements verbatim,
    and researches only to build worked examples and probes for objective 3.
```

---

- **Name**: Delegated Onboarding Research
- **Description**: Run the subject-authority research pass as a delegated subagent that returns a compact field brief (canon, current consensus, live controversies, professional standards, common misconceptions, assessment norms), each claim carrying its source basis and a confidence marker. Keep source triage out of the tutoring context entirely.
- **When**: A new subject requires research beyond learner-supplied materials, sized to the stakes tier.
- **Example**:
```
    Delegate: "Research current standards and assessment norms for AP Biology
    unit 4 (cell communication). Return a field brief with confidence markers,
    not raw sources."
    Main session receives only the brief, not the search transcript.
```

---

- **Name**: Baseline Probe Framing
- **Description**: At higher stakes tiers, open onboarding with a baseline probe against the fixed criterion, recorded as the starting measurement, and tell the learner in advance that a low score is the expected and useful result.
- **When**: Comprehensive, qualifying, certification, or licensure-tier onboarding completes and teaching is about to begin.
- **Example**:
```
    "Before we build the study plan, I'll give you a short diagnostic against
    the exam blueprint. It's supposed to feel hard — it tells us where to spend
    the next six weeks, not how you'll do on exam day."
```

---

- **Name**: Mode Registry with Mechanism Naming
- **Description**: Offer a registry of named tutoring modes (adaptive-expert as default, plus alternatives such as mastery-cycle, Socratic retrieval, deliberate practice, exam simulation) where every mode names the specific science-of-learning mechanism it exploits — retrieval practice, spaced retrieval, interleaving, desirable difficulty, productive failure, worked-example fading, elaborative interrogation, self-explanation, generative learning, teach-back — rather than describing a vague teaching style.
- **When**: Presenting tutoring options to the learner, or selecting a move within an agreed session agenda.
- **Example**:
```
    "Want the default adaptive style, or something more structured? Options:
    mastery-cycle (strict check-and-repair loop), Socratic retrieval (you do
    most of the producing), or exam simulation (timed, criterion-scored)."
```

---

- **Name**: Predict-Then-Probe Calibration
- **Description**: Ask the learner to predict their performance before a probe, then surface the gap between predicted and actual after scoring. Treat miscalibration itself as a target of instruction, not just a side note.
- **When**: Before any criterion-aligned probe, at any stakes tier.
- **Example**:
```
    "Before I ask — how confident are you on this topic, 1 to 5?"
    [probe runs]
    "You said 4, this scored a 2. Let's spend a minute on why that gap
    exists before moving on — that overconfidence pattern matters more
    than the miss itself."
```

---

- **Name**: Deterministic Log Spine
- **Description**: Perform all log reads, writes, validation, and mastery-state transitions through bundled deterministic tooling rather than by freehand editing within the conversation. The log's integrity must not depend on sustained model attention across a long session.
- **When**: Any point in a session that reads or updates persistent state — profile, criterion, curriculum, mastery map, review queue, session history.
- **Example**:
```
    Instead of composing the TOON diff by hand mid-conversation, invoke the
    log-update tool with the structured mastery-state transition as input
    and let it perform the write and validate the result.
```

---

- **Name**: Retention-Decay-First Resume
- **Description**: At the start of any session on a known subject, reconstitute full state, compute which review items are overdue as of the current date using a published scheduling algorithm, and probe the most-lapsed high-value items before introducing new material. Report overdue counts in other subjects without loading their state.
- **When**: The learner returns to a subject with existing log state.
- **Example**:
```
    "Welcome back — it's been 17 days. Before new material, let's check the
    3 items most likely to have decayed: [items]. (You also have 8 items
    overdue in Spanish, not loading those now.)"
```

---

- **Name**: Stakes Escalation Gate
- **Description**: When a learner returns to a subject with existing state but describes materially higher stakes than the tier on record, stop before teaching, name the mismatch plainly, and present three explicit choices — recalibrate (rebuild criterion and curriculum at the new tier, carry prior mastery evidence forward as provisional), reset (start the subject fresh), or reuse (proceed on existing state as-is). Let the learner choose.
- **When**: A stakes mismatch is detected between recorded tier and the learner's current description of the assessment.
- **Example**:
```
    "Your organic chemistry log is built for a course quiz, and you just said
    MCAT — that's a different standard. Want to recalibrate (rebuild against
    the higher bar, keep what you've shown so far as provisional), reset
    (start fresh), or reuse (proceed as-is)?"
```

---

- **Name**: Separated Self-Evaluation Instrument
- **Description**: Maintain a distinct, diagnostic-only record of the tutor's own instructional effectiveness — which explanations landed, where correctives failed, where predictions of learner performance were wrong — and keep it structurally isolated from mastery ratings, which are set only by criterion-aligned probe results.
- **When**: After any teaching move or probe, when reflecting on session effectiveness.
- **Example**:
```
    Self-evaluation note: "The worked-example approach for integration by parts
    didn't land; switch to a graphical intuition next time." Mastery rating for
    that unit is unaffected and remains based only on the probe score.
```

---

## Anti-Patterns

- **Name**: Self-Graded Mastery
- **Description**: Rating a unit as mastered based on the tutor's impression that the session went well, rather than on a demonstrated result against the fixed criterion instrument.
- **Why**: The tutor is the one selecting the material, running the probe, and judging the answer — if it also sets the bar, "mastered" becomes an unfalsifiable opinion of its own teaching rather than a measured claim.
- **Instead**: Rate mastery only from criterion-aligned probe results scored against the threshold the criterion sets, and keep instructional self-evaluation in a separate diagnostic record.

---

- **Name**: Curriculum-First Onboarding
- **Description**: Building a curriculum or beginning instruction before a criterion instrument and expert-performance specification have been fixed and recorded.
- **Why**: Without an external standard fixed first, the curriculum reflects whatever the tutor happens to know rather than what the learner will actually be evaluated against, and the mastery bar has nothing external to anchor to.
- **Instead**: Establish and record the criterion instrument — from supplied canon or sized research — before deriving a single curriculum unit.

---

- **Name**: One-Size Depth
- **Description**: Running the same research and criterion-building depth regardless of stated stakes — either over-researching a same-day quiz or under-specifying a comprehensive exam.
- **Why**: A quiz and a qualifying exam are different products; matching effort to stakes is what keeps low-stakes sessions fast and high-stakes sessions rigorous.
- **Instead**: Name the stakes tier first and let it set a thin instrument at low tiers and a full blueprint with baseline probe at high tiers.

---

- **Name**: Ad Hoc Review Intervals
- **Description**: Telling the learner "let's revisit this in a few days" or choosing review timing by feel within the conversation instead of computing it.
- **Why**: In-session guesses about spacing drift over months and forfeit the spacing effect, one of the most reliable gains in the literature, exactly where it compounds most.
- **Instead**: Compute review scheduling with a published spaced-repetition algorithm through the log's deterministic tooling, never as an ad hoc turn-level decision.

---

- **Name**: Silent Stakes Escalation
- **Description**: Noticing that a learner's described stakes now exceed the tier on record and proceeding to rebuild or reuse state without surfacing the mismatch.
- **Why**: Recalibrate, reset, and reuse are all reasonable responses depending on facts only the learner knows (how much of the old material is still relevant, how much time remains); deciding on their behalf removes a choice that is genuinely theirs.
- **Instead**: Stop, name the mismatch plainly, and present the three options before doing anything else.

---

- **Name**: Confidence Theater
- **Description**: Presenting a contested or low-confidence claim from the field brief as settled fact to keep the lesson feeling authoritative.
- **Why**: Learners who are later assessed against the actual state of the field are penalized for confidence they were given no reason to doubt, and the tutor's credibility collapses the first time it's caught being wrong about something it asserted flatly.
- **Instead**: Teach the state of the disagreement explicitly when the field brief marks a claim contested or low-confidence, and say so.

---

- **Name**: Mode as Vibe
- **Description**: Choosing a "teaching style" (e.g., "let's be more Socratic") without grounding the choice in a specific, named science-of-learning mechanism.
- **Why**: A style label with no mechanism behind it can't be evaluated, tuned, or explained to the learner, and tends to collapse back into whatever the tutor finds natural rather than what the moment calls for.
- **Instead**: Select from the named mode registry, each entry tied to a specific mechanism (retrieval practice, interleaving, productive failure, and so on), and name the mechanism when proposing a mode.
