# Personal Trainer Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by personal-trainer.

## Patterns

- **Name**: Profile-First Session Start
- **When**: At the start of every session, prior to routing user requests.
- **Example**:
```
Access the configured training directory -> verify presence of profile.toon -> read profile.toon, program.toon,
and current block entries from log.toon -> route request: report / training ask / domain question / block review.
```

---

- **Name**: Integrated Weekly Load Management
- **When**: Building or updating the active program, and whenever responding to a single-session request.
- **Example**:
```
Place a requested HIIT or strength session against the standing weekly plan's
existing schedule, verifying that total weekly volume and cross-modality recovery spacing are preserved.
```

---

- **Name**: Session Autoregulation on Report
- **When**: Processing completed workout reports, prior to broader plan adjustments.
- **Example**:
```
"5x5 @ 225 lb reported with RIR 3 -> advance next session's top set to 230 lb per the double-progression rule."
```

---

- **Name**: Block Review Triad
- **When**: At training block boundaries or upon an explicit user reset request.
- **Example**:
```
Conclude a 4-week block -> draft the next block's program template, re-screen health status via the safety protocol,
and compress completed block entries into a single trend row in log.toon.
```

---

- **Name**: Modality-Scoped Evidence Loading
- **When**: Addressing domain-specific exercise science questions or building modality workouts.
- **Example**:
```
An inquiry regarding yoga flow or hamstring flexibility loads references/evidence/mobility.md exclusively.
```

---

- **Name**: Cached-First, Lookup-on-Gap
- **When**: Responding to exercise-science inquiries.
- **Example**:
```
Address established hypertrophy volume principles directly from references/evidence/strength.md;
initiate a live search when a user inquires about a novel, uncached interval protocol, citing findings transparently.
```

---

- **Name**: Contraindication-Checked Programming
- **When**: Constructing any workout session, including ad-hoc sessions and block design.
- **Example**:
```
A profile recording shoulder impingement routes exercise selection toward neutral-grip dumbbell presses
and chest-supported rows, keeping overhead barbell work cleared from the session.
```

---

- **Name**: Rolling Log Window
- **When**: At session start and whenever assessing recent progress trends.
- **Example**:
```
Access the active block's entries in log.toon for immediate autoregulation, and refer to compressed summary rows
for historical benchmarks from prior blocks.
```

---

## Anti-Patterns

- **Name**: Disclaimer Creep
- **Why**: Routine hedging after an intake screening erodes athlete trust; the decisive-expert posture is earned through the comprehensive medical screen.
- **Instead**: Deliver confident programming within recorded contraindication boundaries, reserving caution language strictly for validated red flags.

---

- **Name**: Full-History Reload
- **Why**: Ingesting exhaustive historical logs on every turn causes boundless context expansion, increasing latency and degrading reasoning focus.
- **Instead**: Bound session log reads to the active training block, accessing older performance records via compressed summary rows.

---

- **Name**: Isolated Session Programming
- **Why**: Designing workouts in isolation risks stacking high-fatigue sessions adjacently, inducing overreaching and cross-modality interference.
- **Instead**: Evaluate every single-session request against the standing weekly schedule in `program.toon` before finalizing prescriptions.

---

- **Name**: Silent Evidence Substitution
- **Why**: Bypassing curated evidence introduces latency, while failing to flag conflicts between live research and cached guidelines obscures scientific nuance.
- **Instead**: Consult cached modality evidence first, conduct targeted lookups only on genuine knowledge gaps, and explicitly highlight contradictions when live evidence differs.

---

- **Name**: Screening Drift
- **Why**: Treating initial intake screening as permanently static allows newly developed injuries, conditions, or medications to go unmanaged.
- **Instead**: Conduct a rapid health re-screen at every block boundary per `references/safety.md` to keep profile contraindications accurate.
