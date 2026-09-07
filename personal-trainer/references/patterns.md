# Personal Trainer Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by personal-trainer.

## Patterns

- **Name**: Profile-First Session Start
- **Description**: Resolve the data location pointer and read `profile.toon` plus `program.toon` in full, and the current block's log window, before responding to any request.
- **When**: At the start of every session, before routing the request.
- **Example**:
```
    Resolve ~/.personal-trainer/location.toon -> read profile.toon, program.toon,
    log.toon (current block only) -> then route: report / training ask / question / block review.
```

---

- **Name**: Integrated Weekly Load Management
- **Description**: Allocate strength, cardio, HIIT, mobility, and recovery against one standing weekly plan that manages total load, cross-modality interference, and session ordering, rather than treating each modality as independent.
- **When**: Building or updating the active program, and whenever answering a single-session request.
- **Example**: A request for "a HIIT session" is checked against the same week's strength volume and placed with adequate spacing, not generated in isolation.

---

- **Name**: Session Autoregulation on Report
- **Description**: When the user reports a completed workout, immediately apply the codified progression rule for that modality to the next session, and state what changed and why.
- **When**: Every workout report, before any broader plan reshaping.
- **Example**: "5x5 @ 225 lb reported at RIR 3 -> next session's top set moves to 230 lb per the double-progression rule."

---

- **Name**: Block Review Triad
- **Description**: At every block boundary, perform all three block-review actions together: reshape the plan against progress and trends, re-screen the profile for staleness, and compress log entries older than the working window.
- **When**: Block completion or an explicit user reset request.
- **Example**: A four-week block ends -> next block's plan is drafted, the profile's health section is re-confirmed, and week one's set-by-set entries collapse into a trend summary.

---

- **Name**: Modality-Scoped Evidence Loading
- **Description**: Load only the `references/evidence/*.md` file(s) matching the modality named in the request.
- **When**: Answering any domain question or building any session.
- **Example**: A yoga-flow question loads `references/evidence/mobility.md` only, not the strength or endurance files.

---

- **Name**: Cached-First, Lookup-on-Gap
- **Description**: Answer from the curated evidence base by default; perform a targeted live lookup only when the request names a method, claim, or protocol the cached base does not cover, and flag it explicitly if the lookup contradicts the cached position.
- **When**: Any exercise-science question.
- **Example**: A question about an established hypertrophy principle is answered from `references/evidence/strength.md` directly; a question about a niche new interval protocol triggers a lookup.

---

- **Name**: Contraindication-Checked Programming
- **Description**: Cross-check every prescribed exercise or modality against the profile's recorded contraindications before presenting a session.
- **When**: Every session build, including single-session requests and block reshapes.
- **Example**: A profile recording a repaired rotator cuff excludes overhead pressing variants from any prescribed session without needing to be re-asked.

---

- **Name**: Rolling Log Window
- **Description**: Read only a bounded recent window of `log.toon` (the current block) each session; rely on compressed summaries for anything older.
- **When**: Every session start, and whenever assessing progress.
- **Example**: Eighteen months into training, a session still reads only the current block's entries plus the compressed summaries of prior blocks — not the full history.

---

## Anti-Patterns

- **Name**: Disclaimer Creep
- **Description**: Attaching caution language or "consult a professional" framing to routine sessions after the intake and its contraindications are already on file.
- **Why**: The decisive-expert posture is what the one-time medical screen earns; routine hedging after screening defeats the point of having screened at all and erodes trust.
- **Instead**: Program confidently within the recorded limits; reserve caution language for genuine red flags per `references/safety.md`.

---

- **Name**: Full-History Reload
- **Description**: Reading the entire workout log every session instead of the current block's window plus compressed summaries.
- **Why**: Context cost grows without bound as tenure increases, eventually dominating the session and degrading everything else the skill needs to reason about.
- **Instead**: Read only the bounded recent window; trust the compressed summaries block review already produced for anything older.

---

- **Name**: Isolated Session Programming
- **Description**: Building a single requested session without checking it against the standing weekly plan's total load and modality ordering.
- **Why**: Two independently-reasonable sessions can stack into an unmanageable week — for example, back-to-back high-fatigue days that the standing plan would have spaced apart.
- **Instead**: Always place a single-session request against the active `program.toon` before finalizing it.

---

- **Name**: Silent Evidence Substitution
- **Description**: Reaching for a live lookup when the cached evidence base already covers the question, or answering from the cached base when the request has clearly outrun it.
- **Why**: Defeats the cached-first design either by adding needless latency and network dependency, or by presenting stale positions as current.
- **Instead**: Check the relevant `references/evidence/*.md` file first; lookup only when it genuinely does not cover the request, and name the gap when you do.

---

- **Name**: Screening Drift
- **Description**: Treating the onboarding intake as permanent and never revisiting it, so a new injury, medication, or life change the user has mentioned in passing never reaches the profile.
- **Why**: The profile silently goes stale, and programming keeps trusting health information that's no longer accurate.
- **Instead**: Re-screen the profile as part of every block review, per `references/safety.md`, not only at first onboarding.
