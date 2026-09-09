# Personal Trainer Sharp Edges

This document defines the sharp edges used by personal-trainer.

## Missed Red Flag

- **Id**: missed-red-flag
- **Summary**: A genuine red-flag symptom appears inside an otherwise routine workout report and programming continues without immediate health evaluation.
- **Severity**: critical
- **Situation**: The user mentions chest pain, fainting, shortness of breath, new numbness or tingling, or sharp joint pain while describing a completed workout, and the response applies progression rules and moves on.
- **Why**: The decisive, disclaimer-free posture relies upon continuous screening against the fixed red-flag list. Omitting this check allows serious clinical warnings to pass unaddressed.
- **Solution**: Screen every workout report against the red-flag list in `references/safety.md` prior to applying any progression rule; halt programming immediately upon a match, address the symptom directly, and resume only when the issue is resolved or medically cleared.
- **Symptoms**: A training prescription is issued in the same turn a red-flag symptom was mentioned, or the user reports the symptom worsening over subsequent turns.
- **Detection Pattern**: A workout report containing language about chest pain, breathing difficulty, fainting, dizziness, numbness, or sharp/searing joint pain is answered with load adjustments rather than a clinical halt.

---

## Stale Profile Drift

- **Id**: stale-profile-drift
- **Summary**: Multiple block reviews pass without re-screening the profile, allowing outdated health data to inform ongoing programming.
- **Severity**: high
- **Situation**: The user mentions a new injury, medication, or condition in passing, but block review only reshapes the plan and never revisits the profile's health section.
- **Why**: Block review requires all three triad actions; omitting the profile re-screen allows contraindications to become stale while programming continues under outdated assumptions.
- **Solution**: Execute the health re-screen as a mandatory step in every block review per `references/safety.md`, and integrate health-relevant updates immediately whenever mentioned in routine conversation.
- **Symptoms**: The profile's `last_screened` timestamp reflects an outdated date despite completed block reviews, or the user references an injury not documented in `profile.toon`.
- **Detection Pattern**: `program.toon` updates across successive blocks while `profile.toon`'s medical screen fields remain unchanged despite conversational references to health changes.

---

## Log Bloat

- **Id**: log-bloat
- **Summary**: The workout log grows without bound, forcing sessions to ingest excessive historical records beyond the working window.
- **Severity**: high
- **Situation**: Log compression at block review is skipped or partial, allowing `log.toon` to accumulate full-detail entries indefinitely.
- **Why**: Context usage remains bounded across months of training only when older entries are consolidated into compact block summaries.
- **Solution**: Compress every log entry preceding the active block's working window at each block review per `references/schemas.md`, reading exclusively from current block rows and compressed summaries.
- **Symptoms**: Session context length grows steadily with user tenure, and routine session reads include raw set-by-set entries from past blocks.
- **Detection Pattern**: Session initialization reads `log.toon` entries dated prior to the current block start date rather than referencing compressed summary rows.

---

## Isolated Interference Blindness

- **Id**: interference-blindness
- **Summary**: A single-session request is built without evaluating its recovery impact against the standing weekly plan.
- **Severity**: medium
- **Situation**: The user requests an ad-hoc HIIT or heavy strength workout, and the response is generated without coordinating with the active program's surrounding schedule.
- **Why**: Concurrent-training interference and systemic fatigue accumulate across the whole weekly cycle; isolated design creates compounding fatigue spikes.
- **Solution**: Cross-reference every single-session request against `program.toon`'s weekly schedule, adjusting placement, intensity, or volume to preserve adequate recovery spacing.
- **Symptoms**: The user reports excessive fatigue or skips scheduled sessions after two high-intensity workouts occur on adjacent days.
- **Detection Pattern**: A high-intensity interval or heavy strength workout is prescribed on a day adjacent to an existing high-demand session without adjusting the standing weekly schedule.

---

## Cross-Modality Evidence Leakage

- **Id**: cross-modality-leakage
- **Summary**: An inquiry about one discipline pulls evidence base files for an unrelated training modality.
- **Severity**: low
- **Situation**: A mobility or yoga question is answered using strength periodization references, or an endurance pacing question pulls HIIT interval citations.
- **Why**: Modality evidence files are compartmentalized to maintain focused reasoning and minimize context footprint.
- **Solution**: Identify the specific modality named in the inquiry and load exclusively the matching file(s) under `references/evidence/`.
- **Symptoms**: Context length spikes during simple domain questions, and answers cite principles irrelevant to the requested modality.
- **Detection Pattern**: A request specifying one training modality produces responses containing citations from an unrelated modality reference file.

---

## Contraindication Miss

- **Id**: contraindication-miss
- **Summary**: A prescribed workout includes an exercise loading a movement pattern documented as contraindicated in the user profile.
- **Severity**: critical
- **Situation**: An otherwise well-designed session is built without verifying movements against `profile.toon`'s contraindications array.
- **Why**: Workouts that are physiologically sound in the abstract remain unsafe if they challenge an individual's documented orthopedic or clinical limits.
- **Solution**: Check every prescribed movement against `profile.toon`'s contraindications before presenting a session, selecting safe alternative movement patterns per `references/patterns.md`.
- **Symptoms**: The user reports acute pain or aggravation of a documented injury following a prescribed session.
- **Detection Pattern**: A session prescription contains a movement pattern matching an entry in `profile.toon`'s contraindications list.
