# Personal Trainer Validations

This document defines the validations used by personal-trainer.

## Profile Resolution Required

- **Id**: pt-profile-resolution-required
- **Severity**: error
- **Type**: semantic
- **Pattern**: A session proceeds to prescribe or manipulate training data without first resolving the training directory per `references/schemas.md` and verifying and reading `profile.toon` from it.
- **Message**: A valid user profile must be resolved prior to processing training requests.
- **Fix Action**: Resolve the training directory per `references/schemas.md`, then verify the presence of `profile.toon` there; when absent, initiate the onboarding workflow before generating training content.
- **Applies To**:
    - references/patterns.md
    - references/interactions.md

---

## Onboarding Completeness

- **Id**: pt-onboarding-completeness
- **Severity**: error
- **Type**: schema
- **Pattern**: `profile.toon` written without all required sections: goals, training history, equipment, schedule, preferences, and the medical screen.
- **Message**: Profile must contain all required onboarding sections before program creation.
- **Fix Action**: Complete all missing intake fields per `references/onboarding.md` before generating the initial training block.
- **Applies To**:
    - profile.toon

---

## Contraindication Field Present

- **Id**: pt-contraindication-required
- **Severity**: error
- **Type**: semantic
- **Pattern**: The medical screen recorded a condition, injury, surgery, or flag, but no corresponding entry was derived into the contraindications field.
- **Message**: Every recorded medical finding must translate into an explicit contraindication entry.
- **Fix Action**: Map each condition, injury, surgery, or clinical flag to an explicit movement contraindication entry per `references/safety.md` prior to programming.
- **Applies To**:
    - profile.toon

---

## Red Flag Symptom Vocabulary

- **Id**: pt-red-flag-vocabulary
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `(?i)\bchest (pain|pressure|tightness)\b`
    - `(?i)\b(can'?t breathe|shortness of breath|dyspnea)\b`
    - `(?i)\b(fainted|fainting|blacked out|passed out|syncope|near-syncope)\b`
    - `(?i)\b(numbness|tingling)\b`
    - `(?i)\b(sharp|searing|radiating) pain\b`
- **Message**: This turn contains red-flag symptom vocabulary and requires the `pt-red-flag-halt` semantic assessment before any progression rule is applied.
- **Fix Action**: Assess the match against `pt-red-flag-halt` — establish whether the symptom is actively reported by the athlete, then either halt per that rule or proceed once it resolves to a negated answer, a resolved history, or the skill's own screening text.
- **Applies To**:
    - workout report responses
    - live conversation turns

---

## Red Flag Halt

- **Id**: pt-red-flag-halt
- **Severity**: error
- **Type**: semantic
- **Pattern**: An athlete actively reports a current symptom from the red-flag list in `references/safety.md` — chest pain/pressure/tightness, syncope or near-syncope, acute numbness/tingling or unilateral weakness, disproportionate dyspnea, or sharp/searing/radiating joint pain — and a progression rule or session prescription is applied in the same turn. A negated answer ("no chest pain"), a resolved historical finding ("numbness cleared up in 2023"), a screening question the skill itself asks, and the symptom vocabulary as it appears in this skill's own reference text all fall outside this pattern.
- **Message**: Immediate cessation of programming is required upon an actively reported red-flag symptom.
- **Fix Action**: Halt training progression immediately, evaluate the symptom directly per `references/safety.md` (active status, duration, prior history), and resume programming only when the athlete confirms the symptom has fully subsided or has received formal medical clearance.
- **Applies To**:
    - workout report responses
    - live conversation turns

---

## Recent-Window Read Only

- **Id**: pt-log-window-bound
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A session reads `log.toon` entries older than the current block's working window instead of relying on a compressed summary.
- **Message**: Session context must remain bounded to the current block's workout entries.
- **Fix Action**: Restrict routine log reading to the active block's entries and access older training history through compressed summary rows.
- **Applies To**:
    - log.toon

---

## Block Review Triad Completeness

- **Id**: pt-block-review-triad
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A block review updates `program.toon` without completing both the profile re-screen and log compression.
- **Message**: Block review requires simultaneous execution of all three triad components.
- **Fix Action**: Execute the plan reshape, profile health re-screen, and log compression together at each block boundary.
- **Applies To**:
    - program.toon
    - profile.toon
    - log.toon

---

## Modality Reference Scoping

- **Id**: pt-modality-scoping
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A request naming a single modality triggers loading of an evidence file for an unrequested modality.
- **Message**: Evidence loading must remain strictly scoped to the active training modality.
- **Fix Action**: Restrict evidence loading to the specific file(s) under `references/evidence/` that directly match the active request modality.
- **Applies To**:
    - references/evidence/*.md

---

## Profile Confirmation Prior to Write

- **Id**: pt-profile-confirmation-gate
- **Severity**: error
- **Type**: semantic
- **Pattern**: `profile.toon` or `program.toon` written to disk during onboarding before the user has reviewed and confirmed the intake summary.
- **Message**: Profile summary must be reviewed and confirmed by the user before files are created.
- **Fix Action**: Present the captured profile summary to the user and obtain explicit confirmation before persisting profile and program files.
- **Applies To**:
    - references/interactions.md
    - references/onboarding.md

---

## Scope Referral for Out-of-Domain Queries

- **Id**: pt-scope-referral
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A question about nutrition, food logging, macro or calorie targets, supplements, or biomarker interpretation is answered with a prescription of the agent's own rather than routed to a qualified specialist.
- **Message**: Nutrition, food logging, supplement, and biomarker questions route to a qualified specialist, as the skill's description states.
- **Fix Action**: Name the right specialist once — a registered dietitian for nutrition and supplementation, the athlete's physician for biomarker interpretation — per the Out-of-Scope Query pathway in `references/interactions.md`, and continue the accompanying training guidance without hedging it.
- **Applies To**:
    - domain query responses
    - references/interactions.md
