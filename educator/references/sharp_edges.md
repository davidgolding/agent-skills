# Sharp Edges

This document defines the sharp edges used by educator.

---

## Expertise Misread

- **Id**: expertise-misread
- **Summary**: Guidance is set for the wrong level of prior knowledge, so novices are overloaded or experienced learners are slowed by guidance they no longer need.
- **Severity**: critical
- **Situation**: The requester names a grade or age but not what the learners already know, and the design assumes "typical" knowledge for that age; or a mixed-knowledge group gets one level of guidance.
- **Why**: Whether worked examples help or hurt depends on prior knowledge (the expertise-reversal effect), and prior knowledge, not age, sets effective working-memory capacity through chunking. A wrong assumption reverses the effect of the core design choice.
- **Solution**:
    - Treat prior knowledge as a required interview criterion and ask for it whenever the prompt leaves it open.
    - Build a short diagnostic check into the first session and state a fading rule that responds to it.
    - For mixed-knowledge groups, apply Least-Experienced Profile for Mixed Groups with a fast track.
- **Symptoms**:
    - Plan uses full worked examples throughout for learners the requester describes as experienced.
    - Plan opens with independent problem solving for learners new to the topic.
    - Requester reports students were bored or lost in the first session.
- **Detection Pattern**: A Build or Audit output whose guidance level (worked examples, completion problems, independent practice) is fixed throughout and was chosen without a stated prior-knowledge level for the learners.

---

## Neuromyth Request

- **Id**: neuromyth-request
- **Summary**: The request is built on a popular claim the evidence contradicts, and the output carries the myth forward.
- **Severity**: high
- **Situation**: The requester asks for learning-styles stations, left-brain/right-brain activities, a learning pyramid retention scheme, "brain breaks" justified by brain-gym claims, or pure discovery for beginners.
- **Why**: These claims are widely taught in education programs and feel intuitive, so they arrive framed as settled requirements. Building them as asked spends instructional time on methods that do not improve learning.
- **Solution**:
    - Run the conflict gate in `references/interactions.md`: state what the evidence shows in one or two sentences, offer the closest evidence-aligned alternative, and end the turn to wait for the requester's choice.
    - Keep the correction brief and respectful; the requester is usually repeating professional training.
- **Symptoms**:
    - Output contains learner-style categories or matching activities.
    - Output justifies an activity with a brain claim that has no replicated support.
- **Detection Pattern**: A request or draft output that names learning styles, VAK, left-brain or right-brain learning, the learning pyramid, or unguided discovery for novices, where the response does not first state the conflict and wait for a choice.

---

## Excluded Claim Leakage

- **Id**: excluded-claim-leakage
- **Summary**: Claims deliberately excluded from the evidence base reappear in outputs from general training knowledge.
- **Severity**: high
- **Situation**: Designing adult training, adolescent courses, or senior classes, where familiar frameworks and productivity tips (andragogy principles, Perry's positions, Pomodoro or 90-minute blocks, worry lists, Anki prescriptions, multimodal redundancy for seniors, AI-chatbot bans for young children based on a single brain-imaging study) come readily to mind.
- **Why**: These claims are common in the education and productivity literature and fit the age groups naturally, so they slip in as if they were findings unless excluded actively.
- **Solution**:
    - Base adult and older-adult designs on the retained findings: prior-knowledge activation, contrastive comparison for retraining, sensory and pacing accommodation, retrieval and spacing.
    - When a requester asks for one of these frameworks by name, answer in Advise mode with an honest verdict on its evidence.
    - Give any session-length or tool choice as a practical suggestion, not as a finding.
- **Symptoms**:
    - Evidence notes cite andragogy, Perry, Pomodoro, or a single imaging study as the basis for a choice.
    - Senior materials recommend reading text aloud word for word with identical on-screen text as a compensatory technique.
- **Detection Pattern**: Evidence notes or design rationale that attribute a design choice to andragogy, Perry or Arnett, Pomodoro or fixed deep-work blocks, worry lists, Anki, Network Memory Task framing, multimodal redundancy reversal for seniors, or a first-grader brain-imaging study.

---

## Hidden Overload in Rich Materials

- **Id**: hidden-overload
- **Summary**: Materials that look engaging impose extraneous load that crowds out learning.
- **Severity**: high
- **Situation**: The design includes busy slides, separate legends, decorative images, verbatim narration of on-screen text, long teacher monologues, or several new interacting ideas in one segment.
- **Why**: Working memory holds only a few new interacting elements; split attention, redundancy, and decoration use that capacity for processing that teaches nothing.
- **Solution**:
    - Apply Segmented Low-Load Delivery: integrate labels, cut decoration, keep narration and text complementary, segment new content.
    - Count the new interacting elements in each segment and split any segment that introduces more than about four.
- **Symptoms**:
    - Requester reports students "followed along" but could not explain the content later.
    - A single segment introduces a whole system with many named parts at once.
- **Detection Pattern**: A lesson segment that introduces more than about four new interacting elements without a check, or materials that separate diagrams from their labels or pair narration with identical on-screen text.

---

## Practice Performance Mistaken for Learning

- **Id**: performance-learning-confusion
- **Summary**: Strong practice scores are read as learning, and productive difficulty is removed because it lowers scores in the moment.
- **Severity**: high
- **Situation**: A requester or the design favors massed, blocked, immediately tested practice because scores are high, or abandons interleaving and spacing because scores dip.
- **Why**: Massing and blocking boost immediate performance while producing weaker long-term retention; spacing, interleaving, and delayed retrieval lower practice performance while strengthening durable learning. Immediate tests after taxing study also understate what was learned.
- **Solution**:
    - Explain the dip in the evidence notes so the teacher expects it.
    - Measure learning with delayed, cumulative checks rather than end-of-lesson scores.
    - Keep blocked practice for first acquisition only, then interleave.
- **Symptoms**:
    - Plan's only assessment is an exit ticket on the same lesson's content.
    - Audit recommends removing mixed practice because students' scores fell.
- **Detection Pattern**: A multi-session design that assesses only immediately after instruction, or a recommendation that cites lower practice scores as the reason to drop spacing or interleaving.

---

## Concrete Anchor Skipped

- **Id**: concrete-anchor-skipped
- **Summary**: Young learners are given symbols or abstract rules before they have concrete or pictorial referents.
- **Severity**: high
- **Situation**: A Build for young children or children in math or science starts at symbolic notation, or a design asks children to coordinate three or more relationships at once without visual support.
- **Why**: Children's internal working memory is costly to maintain, so they rely on perceptual support; unanchored abstraction exceeds what they can hold.
- **Solution**:
    - Apply Concrete-Representational-Abstract Sequencing with explicit criteria for moving between stages.
    - Externalize steps and references onto cards, charts, or materials.
- **Symptoms**:
    - Children can recite the procedure but cannot model it with objects or drawings.
    - Errors increase sharply when a task adds one more relationship.
- **Detection Pattern**: A lesson for learners aged roughly 4-11 that introduces symbolic notation for a new concept without a preceding concrete or pictorial stage.

---

## Proactive Interference Ignored

- **Id**: proactive-interference-ignored
- **Summary**: Retraining experienced learners as if they were blank slates, so old habits override the new routine.
- **Severity**: medium
- **Situation**: Adult or professional training introduces a revised procedure, tool, or rule that resembles what learners already do.
- **Why**: Established knowledge interferes with new learning when surface features match but the underlying rule differs, and learners fall back to the old habit under load.
- **Solution**:
    - Apply Contrastive Comparison for Retraining: name the old routine, set it beside the new one, and practice the cases where they diverge.
    - Schedule spaced follow-up retrieval after training.
- **Symptoms**:
    - Learners perform correctly in training and revert on the job.
    - Error reports cluster on steps that changed.
- **Detection Pattern**: An adult training design that replaces an existing routine without naming the old routine or practicing cases where old and new give different answers.

---

## Mixed-Group Mismatch

- **Id**: mixed-group-mismatch
- **Summary**: A group spanning developmental bands or expertise levels is designed for its average or its strongest members.
- **Severity**: medium
- **Situation**: Multi-grade classrooms, community classes, family learning events, or groups on an overlapping age band such as 18-19-year-olds.
- **Why**: Designing for the average overloads the least-experienced learners and still under-serves the most experienced.
- **Solution**:
    - Apply Least-Experienced Profile for Mixed Groups and state the differentiation for each other profile present.
    - Name in the evidence notes which profile governed the core design.
- **Symptoms**:
    - Youngest or newest learners disengage early.
    - Plan has a single path with no differentiation.
- **Detection Pattern**: A Build for a group spanning more than one developmental band or expertise level that has a single path with no stated governing profile or differentiation.

---

## Out-of-Core Overclaiming

- **Id**: out-of-core-overclaiming
- **Summary**: Findings from outside the integrated evidence base are presented with the same certainty as the core, or without citation.
- **Severity**: medium
- **Situation**: A request involves dyslexia, ADHD, sleep, bilingualism, a specific disability, or a technique the core does not cover, and the response answers from general knowledge.
- **Why**: Without a search and a label, the teacher cannot tell replicated core findings from weaker or uncited claims.
- **Solution**:
    - Apply Out-of-Core Research Labeling: search current peer-reviewed syntheses, cite them, and label them in the evidence notes.
    - Give single-study findings as provisional.
- **Symptoms**:
    - Evidence notes contain claims with no source that are not in the core.
    - Strong claims about specific conditions with no cited synthesis.
- **Detection Pattern**: Evidence notes containing a finding that is neither part of the integrated core nor accompanied by a citation and the label "outside the core evidence base."

---

## Interview Fatigue

- **Id**: interview-fatigue
- **Summary**: The interview asks more than it needs to, delaying the deliverable and frustrating the requester.
- **Severity**: medium
- **Situation**: The prompt already gives the grade, subject, and length, but the skill asks for them again, asks several questions at once, or asks for the learning goal.
- **Why**: The five criteria exist so the design fits the learners; asking for answered or inferable ones costs turns without improving the fit.
- **Solution**:
    - Extract every criterion the prompt supplies before asking anything.
    - Ask for missing criteria one at a time, in the order in `references/interactions.md`.
    - Infer the learning goal and task structure and state them in the evidence notes.
- **Symptoms**:
    - Requester repeats information they already gave.
    - Requester answers only one of several stacked questions.
- **Detection Pattern**: An interview turn that asks for a criterion already present in the prompt, contains more than one question, or asks for the learning goal.

---

## Silent Substitution

- **Id**: silent-substitution
- **Summary**: The skill quietly changes or quietly complies with a request element the evidence contradicts.
- **Severity**: medium
- **Situation**: The request includes an element the evidence contradicts, and the skill builds a deliverable in the same turn.
- **Why**: The requester agreed to correct-and-ask behavior so the teacher keeps the decision; building in the same turn removes that choice.
- **Solution**:
    - End the turn after stating the conflict and offering the alternative; build only after the requester chooses.
- **Symptoms**:
    - Deliverable differs from the request with no explanation.
    - Deliverable contains the contradicted element with no flag.
- **Detection Pattern**: A response that contains a full Build deliverable in the same turn as the first mention of an evidence conflict in the request.
