# Onboarding Protocol

The onboarding workflow initiates when a request arrives and `profile.toon` is absent from the configured training data directory. Present questions sequentially, asking one question at a time. Use a blocking question tool with defined choices when options are bounded (such as schedule days or primary modality), and use open text for narrative history, goals, and injury backgrounds. Present the captured profile summary to the user for explicit confirmation before persisting `profile.toon`.

## Sequence

1. **Goals**: Record desired physical adaptations and target completion dates. When multiple goals are stated, establish which goal takes primary programming priority.
2. **Training history and current capacity**: Gather narrative training background, years of consistent lifting or running, recent performance numbers (e.g., estimated 1RMs, recent 5k times), and current weekly frequency.
3. **Equipment and schedule**: Document accessible training environments (commercial gym, home barbell setup, dumbbells, bodyweight only) and confirm realistic weekly commitment (available training days and minutes per session).
4. **Preferences**: Note preferred training styles, disliked movements, and areas of enthusiasm across strength, cardio, HIIT, and mobility/yoga.
5. **Medical screen**: Administer a thorough clinical intake: current diagnosed medical conditions, current medications (noting exertion-relevant effects), past injuries and surgeries with resolution status, pregnancy status where applicable, and cardiac or cardiovascular flags (exertional chest pain, unexplained syncope, structural heart conditions).
6. **Baseline measurements**: Log available physical markers (bodyweight, benchmark lift loads, resting heart rate) into the initial entries of `measurements.toon`. Missing numbers may remain unpopulated until tested.

## Deriving Contraindications

Translate each medical screen finding into an explicit `contraindications` row (`references/schemas.md`) specifying the affected movement pattern and severity level (`caution` vs `hard` exclusion). Consult `references/safety.md` for standard condition-to-movement translation models. Transforming clinical findings into clear movement pattern boundaries enables safe, decisive programming and prevents the Contraindication Miss sharp edge.

## Closing Onboarding

1. Present the complete intake summary back to the user in plain language—detailing goals, schedule limits, and derived movement contraindications—allowing the user to confirm or adjust before saving.
2. Upon user confirmation, create `profile.toon` and `measurements.toon` in the configured training data directory.
3. Generate the initial `program.toon`—an integrated weekly schedule tailored to available equipment and weighted toward the primary objective.
4. Initialize `log.toon` with an empty `entries` collection.
5. Deliver the first week's training schedule to the athlete.
