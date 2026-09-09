# Safety Protocol

This document defines the clinical intake fields, contraindication translation guidelines, and immediate red-flag response protocols for personal-trainer.

## Medical Screen Fields (Captured at Onboarding)

- Current diagnosed conditions (cardiovascular, metabolic, musculoskeletal, respiratory).
- Current medications, noting agents that influence exercise tolerance (e.g., beta-blockers blunting heart-rate response, antihypertensives affecting orthostatic regulation, medications altering thermoregulation).
- Past injuries and surgeries, noting dates, rehabilitation history, and ongoing functional impact (fully resolved / intermittent flare / chronic).
- Pregnancy status and gestational stage where applicable.
- Cardiovascular and hemodynamic flags: exertional chest discomfort or tightness, unexplained syncope or near-syncope, diagnosed arrhythmias, structural heart disease, or uncontrolled hypertension.

## Deriving Contraindications from the Screen

Translate each clinical finding into an explicit `contraindications` row (`references/schemas.md`) specifying the affected movement pattern, clinical rationale, and severity level (`caution` vs `hard` exclusion). Apply clinical rationale to determine movement boundaries:

| Screen Finding | Derived Contraindicated Pattern | Typical Severity |
|---|---|---|
| Shoulder impingement / rotator cuff repair | Heavy overhead pressing, behind-the-neck movements | caution (modify active range) to hard (post-surgical) |
| Lumbar disc pathology / radiculopathy | Loaded spinal flexion under fatigue, max axial loading | caution |
| Recent knee ligament reconstruction | Deep unilateral deceleration, plyometrics | hard until cleared, then caution |
| Uncontrolled hypertension / cardiac flags | Maximal isometric straining (heavy Valsalva), supramaximal HIIT | hard until cleared by a physician |
| Late-term pregnancy | Prolonged supine loading, high-fall-risk balance movements | caution, trimester-adapted |

Apply sound exercise mechanics to conditions beyond this table, maintaining the mandatory translation from clinical history to explicit movement pattern constraints.

## Red-Flag Protocol

The following symptoms mandate an immediate halt to all training programming across workout reports, session planning, and general dialogue:

- Chest pain, pressure, or tightness, with or without exertion.
- Syncope, near-syncope, or unexplained dizziness during or after exertion.
- Acute numbness, tingling, or sudden unilateral motor weakness.
- Dyspnea or shortness of breath disproportionate to the workload.
- Sharp, searing, or radiating joint/connective-tissue pain distinct from muscular fatigue.

Upon detection of any red flag: halt programming immediately, state the identified symptom and its clinical risk, and evaluate the symptom directly (active status, duration, prior history). Resume programming in the affected modality only after the athlete confirms the symptom has fully subsided or has received formal medical clearance. When symptoms persist or recur, recommend evaluation by a qualified medical provider plainly and decisively, upholding expert vigilance without repetitive disclaimer hedging.

## Re-Screening at Block Review

Every block review re-opens the medical screen: inquire about newly diagnosed conditions, medication changes, acute injuries, or significant lifestyle stressors (systemic illness, travel fatigue, altered sleep patterns, pregnancy) since the prior review. Update `profile.toon`'s `medical_screen` and `contraindications` fields with new findings, and refresh `last_screened` upon every block review to prevent Stale Profile Drift.
