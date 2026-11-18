# Sharp Edges

This document defines the sharp edges used by process-architect.

---

## Archetype Misclassification

- **Id**: archetype-misclassification
- **Summary**: The diagnosis picks the archetype that matches the caller's framing rather than the evidence in the map.
- **Severity**: critical
- **Situation**: The caller opens with a label ("we're overloaded", "nobody owns this") and the agent adopts it as the diagnosis.
- **Why**: Callers describe symptoms, and the same symptom fits several archetypes. "Overload" is often decision latency (work waiting on approvals piles up) or rework (the same work done twice).
- **Solution**:
    - Test at least two candidate archetypes against the map using their probing questions before naming one.
    - Cite map evidence for the diagnosis, and ask the caller to confirm the fit.
- **Symptoms**:
    - The diagnosis repeats the caller's opening words.
    - Options do not touch the pain points marked on the map.
- **Detection Pattern**: A diagnosis that names an archetype without citing any step, wait, or pain point from the Current-State Map, or that matches the caller's opening phrase with no competing archetype considered.

---

## One-Sided Account

- **Id**: one-sided-account
- **Summary**: The map and diagnosis rest only on the caller's view of other teams' behavior.
- **Severity**: high
- **Situation**: The pain sits at a handoff with another team or with a manager the caller does not control.
- **Why**: The caller sees their side of the handoff; the other side's constraints (their own intake, their approvals, their incentives) are invisible, so options that blame or bypass them fail on contact.
- **Solution**:
    - Ask what the other party would say causes the delay or problem.
    - Mark inferred facts about other teams as assumptions, and include a cheap option to verify them (a conversation, a shared look at the queue).
- **Symptoms**:
    - Options consist of making another team behave differently.
    - The map has detail on the caller's side and a black box on the other.
- **Detection Pattern**: A Current-State Map in which steps owned by other teams have no timings, tools, or constraints, combined with options that all require those teams to change.

---

## Interview Fatigue Under Full Rigor

- **Id**: interview-fatigue
- **Summary**: Running every phase at full rigor turns a quick-ideas request into a long interrogation.
- **Severity**: high
- **Situation**: The caller picks quick ideas and expects a fast exchange.
- **Why**: Full rigor is a requirement of the skill, but rigor lives in the analysis, not the question count; asking every possible question exhausts the caller before the options phase.
- **Solution**:
    - Extract answers from what the caller has already said and keep each phase within 1-3 questions.
    - Batch confirmations ("here's the map, correct anything") instead of asking step by step.
- **Symptoms**:
    - Short or impatient answers; the caller asks "can you just give me ideas?"
    - More than about 15 questions before options appear.
- **Detection Pattern**: A session with more than three questions in any single phase, or questions whose answers already appear in the caller's earlier messages.

---

## Overconfident Forecasts

- **Id**: overconfident-forecasts
- **Summary**: Forecasts are stated as certainties or with invented precision.
- **Severity**: high
- **Situation**: Phase 06, especially when the map has few numbers.
- **Why**: Organizational change outcomes vary widely; precise figures not grounded in the caller's data read as authoritative and set up the follow-up to look like failure.
- **Solution**:
    - Derive numbers only from figures the caller gave, and label each forecast likely, plausible, or uncertain.
    - Prefer directional statements with ranges when data is thin.
- **Symptoms**:
    - Percentages or durations that appear nowhere in the map.
    - No confidence labels.
- **Detection Pattern**: An Option Forecast containing a number that cannot be traced to a figure in the Current-State Map, or a forecast without a confidence label.

---

## Personnel Issue Wearing a Process Costume

- **Id**: personnel-in-process
- **Summary**: The real problem is one person's behavior or performance, framed as a process problem.
- **Severity**: high
- **Situation**: Every pain point on the map traces to the same individual, or the caller's real ask is how to deal with a colleague.
- **Why**: Process fixes aimed at one person (extra checkpoints, new approvals) burden everyone and leave the actual issue untouched, and advising on the person crosses into HR territory.
- **Solution**:
    - Name the pattern neutrally ("most delays trace to one role") and say the individual side belongs with the manager chain or HR.
    - Offer process options that hold regardless of who fills the role (clear expectations, coverage, decision thresholds).
- **Symptoms**:
    - The caller refers to a specific person repeatedly.
    - Options amount to monitoring or constraining one person.
- **Detection Pattern**: A map or diagnosis where the pain points all name the same individual or role-holder, or options whose only effect is to add oversight of one person.

---

## Stale or Ambiguous Engagement Files

- **Id**: stale-engagement-file
- **Summary**: A follow-up resumes the wrong engagement or trusts a file whose situation has changed.
- **Severity**: medium
- **Situation**: Several engagement files exist in the folder, or the last check-in is months old.
- **Why**: Resuming from the wrong or outdated record anchors the check-in on forecasts that no longer apply.
- **Solution**:
    - When more than one file could match, list them by title and last check-in date and ask.
    - In Phase F1, ask whether anything fundamental has changed before checking signals.
- **Symptoms**:
    - The caller corrects the recap.
    - Signals reference teams or tools that no longer exist.
- **Detection Pattern**: A follow-up that resumes an engagement without confirming the recap, when the folder holds multiple engagement files or the last check-in is more than 90 days old.

---

## Sensitive Details in the Record

- **Id**: sensitive-record
- **Summary**: The engagement file captures names, criticisms of colleagues, or confidential figures.
- **Severity**: medium
- **Situation**: The caller vents about colleagues or shares confidential numbers during the interview.
- **Why**: The file lives in a working folder that may be synced or shared, and a record that names and criticizes people can cause real harm if seen.
- **Solution**:
    - Record people by role, summarize friction neutrally, and keep only the figures the analysis uses.
    - Tell the caller what the file contains when it is written.
- **Symptoms**:
    - Personal names or judgmental characterizations in the file.
- **Detection Pattern**: Personal names, or evaluative words about individuals (lazy, incompetent, difficult), in an engagement file or saved deliverable.
