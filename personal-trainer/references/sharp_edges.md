# Sharp Edges

This document defines the sharp edges used by personal-trainer.

---

## Missed Red Flag

- **Id**: missed-red-flag
- **Summary**: A genuine red-flag symptom appears inside an otherwise routine workout report and programming continues anyway.
- **Severity**: critical
- **Situation**: The user mentions chest pain, fainting, shortness of breath, new numbness or tingling, or sharp joint pain while describing a completed workout, and the response applies progression rules and moves on.
- **Why**: The decisive, disclaimer-free posture exists because screening happened once — but that posture only stays safe if every report is still checked against the fixed red-flag list. Without that explicit check, "no disclaimers" can drift into "no vigilance."
- **Solution**:
    - Screen every workout report against the red-flag list in `references/safety.md` before applying any progression rule.
    - Halt programming and address the symptom directly whenever a match occurs; do not resume until it is resolved or cleared.
- **Symptoms**:
    - A training prescription is issued in the same turn a red-flag symptom was mentioned.
    - The user later reports the same symptom recurring or worsening.
- **Detection Pattern**: A workout report containing language about chest pain, breathing difficulty, fainting, dizziness, numbness, or sharp/searing joint pain is answered with a load or program adjustment instead of a halt.

---

## Stale Profile Drift

- **Id**: stale-profile-drift
- **Summary**: Multiple block reviews pass without re-screening the profile, so an outdated health picture keeps informing programming.
- **Severity**: high
- **Situation**: The user mentions a new injury, medication, or condition in passing, but block review only reshapes the plan and never revisits the profile's health section.
- **Why**: Block review is defined as three actions together; if only the plan-reshape half happens, the profile silently ages while programming keeps trusting stale contraindications.
- **Solution**:
    - Treat the re-screen as a mandatory, not optional, part of every block review — see `references/safety.md`.
    - When the user mentions anything health-relevant outside a block review, update the profile immediately rather than waiting.
- **Symptoms**:
    - The profile's health section's last-updated marker is far older than the current date despite several completed block reviews.
    - The user references a health change the profile doesn't reflect.
- **Detection Pattern**: `program.toon` has changed across several block reviews while `profile.toon`'s medical screen fields have not, despite the user mentioning health-relevant information in the interim.

---

## Log Bloat

- **Id**: log-bloat
- **Summary**: The workout log grows without bound and a session ends up reading far more history than the intended working window.
- **Severity**: high
- **Situation**: Compression at block review is skipped or partial, so `log.toon` accumulates full-detail entries indefinitely.
- **Why**: Context cost is supposed to stay flat because older entries are compressed into summaries; if compression doesn't happen, every session pays for the full history.
- **Solution**:
    - Compress every log entry older than the current block's working window at each block review, per `references/schemas.md`'s compression format.
    - Never read log entries beyond the working window directly — read the compressed summary instead.
- **Symptoms**:
    - Context usage per session rises with tenure instead of staying flat.
    - A session's read includes entries dated well before the current block began.
- **Detection Pattern**: A session start reads `log.toon` entries dated earlier than the current block's start date instead of relying on a prior compressed summary.

---

## Isolated Interference Blindness

- **Id**: interference-blindness
- **Summary**: A single-session request is built without checking it against the same week's other high-fatigue sessions in the active program.
- **Severity**: medium
- **Situation**: The user asks for "a HIIT session" or "a leg day," and the response is generated independently of what the standing weekly plan already has scheduled nearby.
- **Why**: Concurrent-training interference and cumulative fatigue are properties of the whole week, not of any single session; building sessions in isolation reintroduces exactly the problem the integrated weekly plan exists to prevent.
- **Solution**:
    - Always check a single-session request against `program.toon`'s total weekly load and modality ordering before finalizing it.
    - Adjust placement or intensity if the request would stack against an adjacent high-fatigue session.
- **Symptoms**:
    - The user reports unusual fatigue or has to skip a subsequent planned session after two high-intensity sessions landed back to back.
- **Detection Pattern**: A HIIT or heavy-strength session is scheduled on a day adjacent to another high-intensity session without any reference to the active program's load distribution.

---

## Cross-Modality Evidence Leakage

- **Id**: cross-modality-leakage
- **Summary**: A question about one modality pulls in the evidence file for a different, unrequested modality.
- **Severity**: low
- **Situation**: A mobility or yoga question is answered using strength periodization language, or a strength question cites endurance pacing evidence.
- **Why**: The evidence base is split by modality specifically so that a narrow question doesn't inflate context or blur unrelated bodies of evidence together.
- **Solution**: Identify the modality named in the request first, and load only the matching file(s) under `references/evidence/`.
- **Symptoms**: A narrow, single-modality question is answered with evidence-base content from an unrelated file; context usage is high for a simple question.
- **Detection Pattern**: A request naming one modality is answered citing evidence-base content sourced from a different modality's reference file.

---

## Contraindication Miss

- **Id**: contraindication-miss
- **Summary**: A prescribed session includes an exercise that directly loads a movement pattern the profile records as contraindicated.
- **Severity**: critical
- **Situation**: A plausible, well-constructed session is built without cross-checking it against `profile.toon`'s contraindications field.
- **Why**: A session can look correct in isolation — sound sets, reps, and progression — while still violating a specific, previously recorded limit that only the profile check would catch.
- **Solution**: Cross-check every prescribed exercise against the profile's contraindications before presenting any session, per the Contraindication-Checked Programming pattern.
- **Symptoms**: The user reports pain or reinjury from an exercise that directly contradicts a previously recorded injury or medical flag.
- **Detection Pattern**: A session includes a movement pattern matching an entry in the profile's contraindications field.
