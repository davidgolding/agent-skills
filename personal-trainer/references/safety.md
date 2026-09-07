# Safety Protocol

## Medical screen fields (captured at onboarding)

- Current diagnosed conditions (cardiovascular, metabolic, musculoskeletal, respiratory)
- Current medications (note any with exertion-relevant effects: beta-blockers blunt heart-rate response, some blood pressure medications affect orthostatic tolerance, some affect thermoregulation)
- Past injuries and surgeries, with rough dates and current status (resolved / ongoing / flares occasionally)
- Pregnancy status, where relevant
- Cardiac and blood-pressure flags: chest pain or pressure with exertion, unexplained syncope or near-syncope, diagnosed arrhythmia or structural heart condition, uncontrolled hypertension

## Deriving contraindications from the screen

Translate each answer into a `contraindications` row (`references/schemas.md`) — a movement pattern, a reason, and a severity. Typical mappings to reason from, not a lookup table to apply blindly:

| Screen finding | Likely contraindicated pattern | Typical severity |
|---|---|---|
| Shoulder impingement / rotator cuff history | Heavy overhead pressing, behind-the-neck work | caution (modify range, monitor) to hard (recent surgery) |
| Lumbar disc history | Loaded spinal flexion under fatigue, max-effort axial loading | caution |
| Knee ligament reconstruction (recent) | Deep unilateral loading, plyometrics | hard until cleared, then caution |
| Uncontrolled hypertension or cardiac flag | High-intensity interval work, max-effort strength testing | hard until cleared by a physician |
| Pregnancy (varies by trimester) | Supine positions late-term, high-fall-risk movements, Valsalva-heavy maxing | caution, trimester-dependent |

Use clinical judgment for anything not listed rather than treating this table as exhaustive — the point is the translation habit, not the specific rows.

## Red-flag protocol

These halt programming immediately, in any workout report or ongoing conversation, regardless of what else is being discussed:

- Chest pain or pressure, with or without exertion
- Fainting, near-fainting, or unexplained dizziness
- New numbness, tingling, or weakness, especially one-sided
- Shortness of breath disproportionate to effort
- Sharp or searing joint pain (distinct from normal training discomfort or fatigue)

On a match: stop, name what was said and why it's a stop, and ask about the symptom directly (still present? resolved? has it happened before?) rather than continuing to program. Do not resume programming in that modality until the user indicates it has resolved or been cleared; a recurring pattern warrants recommending they see a physician before continuing, stated plainly and once — not as a repeated disclaimer.

## Re-screening at block review

Every block review re-opens the medical screen briefly: any new conditions, medications, injuries, or life changes (illness, travel, sleep disruption, pregnancy) since the last screen. Update `profile.toon`'s `medical_screen` and `contraindications` fields whenever the answer changes anything, and update `last_screened` regardless. This is what prevents Stale Profile Drift — it happens every block review, not only when something seems obviously wrong.
