# Onboarding

Runs once, the first time a request arrives with no resolvable data location or no `profile.toon`. Ask one question at a time; use a blocking question tool with options where the answer set is bounded, and open free text where it isn't (goals, history, injuries). Confirm the captured picture back to the user before writing `profile.toon`.

## Sequence

1. **Data location.** Ask where to keep training data (a folder in their home directory, a project folder, wherever they prefer). Write the answer to `~/.personal-trainer/location.toon` as `data_dir`.
2. **Goals.** What they want and by when, if they have a date. Capture more than one goal if they have them, and ask which is primary if it isn't obvious.
3. **Training history and current capacity.** Background, time training, any current numbers they know (recent lifts, recent race times, current session frequency). Open-ended — this is inherently narrative.
4. **Equipment and schedule.** What they have access to (gym, home equipment, bodyweight-only) and how many days/week and how much time per session they can actually give it.
5. **Preferences.** What they enjoy, what they'll quietly avoid or skip, which modalities interest them (strength, cardio, HIIT, mobility/yoga) — this shapes adherence as much as physiology does.
6. **Medical screen.** Ask directly and specifically, not as a single vague "any health issues?": current conditions, medications, past injuries and surgeries, pregnancy status if relevant, and cardiac or blood-pressure flags (chest pain with exertion, unexplained syncope, diagnosed heart condition). Treat this as a real intake, not a formality — the decisive programming voice that follows depends on it.
7. **Baseline measurements.** Whatever they can report now (bodyweight, known maxes, a recent time trial) goes into the first `measurements.toon` entries. Missing numbers are fine — capture what exists.

## Deriving contraindications

Do not store medical screen answers verbatim as the thing programming checks against. Translate each condition, injury, surgery, or flag into an explicit `contraindications` entry naming the movement pattern and severity (`caution` vs `hard` exclusion) — see `references/schemas.md`. Consult `references/safety.md` for common condition-to-movement mappings. This translation is what R4 (requirements doc) and the Contraindication-Checked Programming pattern depend on; skipping it is what causes the Contraindication Miss sharp edge.

## Closing onboarding

1. Confirm the captured profile back to the user in plain language — goals, constraints, and anything you inferred as a contraindication — so they can correct it before it's written.
2. Write `profile.toon` and `measurements.toon`.
3. Build the first `program.toon` — a full integrated weekly plan for the coming block, sized to the stated schedule and equipment, weighted toward the primary goal.
4. Initialize an empty `entries` array in `log.toon`.
5. Hand the user their first week.
