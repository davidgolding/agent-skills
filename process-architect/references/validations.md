# Validations

This document defines the validations used by process-architect.

---

## Option Authority Label

- **Id**: option-authority-label
- **Severity**: error
- **Type**: instruction
- **Pattern**: Every option in the deliverable and the engagement file carries a label of either "You can do this" or "Needs buy-in: <role>", and every buy-in option states the core of the case to make.
- **Message**: An option has no authority label, or a buy-in option has no named role or case.
- **Fix Action**: Add the label from the Phase 02 authority map; for buy-in options, name the approving role and a one-sentence case.
- **Applies To**:
    - Quick ideas in chat
    - process-architect/*.md

---

## Minimum Option Spread

- **Id**: minimum-option-spread
- **Severity**: error
- **Type**: instruction
- **Pattern**: The options include at least three distinct options, at least one of which the caller can start alone.
- **Message**: Fewer than three options, or none the caller can start without buy-in.
- **Fix Action**: Generate options following the Option Spread pattern in references/patterns.md.
- **Applies To**:
    - Quick ideas in chat
    - process-architect/*.md

---

## Forecast Completeness

- **Id**: forecast-completeness
- **Severity**: error
- **Type**: instruction
- **Pattern**: Every option has a forecast with a likely outcome, a second-order effect, an adoption risk, a typical failure mode, and a confidence label (likely, plausible, uncertain). In quick ideas, the forecast may be one line in the deliverable but is complete in the engagement file.
- **Message**: An option is missing its forecast or one of the forecast elements.
- **Fix Action**: Write the missing elements using the Option Forecast pattern; draw failure modes from the matched archetype.
- **Applies To**:
    - process-architect/*.md

---

## Observable Success Signals

- **Id**: observable-success-signals
- **Severity**: error
- **Type**: instruction
- **Pattern**: The chosen direction has at least one leading indicator with a target, one lagging outcome, a milestone, a dated check-in, and a tripwire, each observable by the caller in existing tools or meetings.
- **Message**: Success signals are missing, undated, or not observable (for example "better morale" or "improved efficiency").
- **Fix Action**: Replace vague measures with observable indicators and add the missing date or tripwire.
- **Applies To**:
    - Quick ideas in chat
    - process-architect/*.md

---

## Vague Success Language

- **Id**: vague-success-language
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:better|improved|enhanced|increased)\s+(?:collaboration|communication|alignment|efficiency|morale|visibility|synergy)\b
- **Message**: A success measure or forecast uses unmeasurable language.
- **Fix Action**: Restate it as an observable indicator with a target and a date.
- **Applies To**:
    - process-architect/*.md

---

## Diagnosis Cites the Map

- **Id**: diagnosis-cites-map
- **Severity**: error
- **Type**: instruction
- **Pattern**: The diagnosis names its archetype(s) in the org's terms and cites at least one specific step, wait, or pain point from the Current-State Map as evidence.
- **Message**: The diagnosis is not grounded in the map.
- **Fix Action**: Add the map evidence, or re-test the diagnosis against the archetype probes.
- **Applies To**:
    - Diagnosis statements in chat
    - process-architect/*.md

---

## Framework Jargon Untranslated

- **Id**: framework-jargon-untranslated
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - \b(?:DMAIC|ADKAR|RAPID|DACI|RACI|WIP|OKRs?|Theory of Constraints|value[- ]stream)\b
- **Message**: A framework term appears in a recommendation; check that the action itself is stated in the org's vocabulary.
- **Fix Action**: Lead with the concrete action in the org's terms and keep the framework name, if any, in a parenthetical rationale.
- **Applies To**:
    - Quick ideas in chat
    - process-architect/*.md

---

## Engagement File Sections

- **Id**: engagement-file-sections
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^## Problem$
    - ^## Authority
    - ^## Current-State Map$
    - ^## Diagnosis$
    - ^## Options and Forecasts$
    - ^## Chosen Direction$
    - ^## Success Signals$
    - ^## Check-ins$
- **Message**: The engagement file is missing a required section; a later session cannot resume from it.
- **Fix Action**: Add the missing section following the Engagement File pattern, with content or an explicit "not yet decided".
- **Applies To**:
    - process-architect/*.md (engagement files, not -report or -proposal files)

---

## Role, Not Name

- **Id**: role-not-name
- **Severity**: warning
- **Type**: instruction
- **Pattern**: The engagement file and saved deliverables refer to people by role (pod lead, director, CS team lead), not by personal name, and contain no evaluative words about individuals.
- **Message**: A personal name or a judgment of an individual appears in a saved file.
- **Fix Action**: Replace names with roles and restate friction neutrally as a process observation.
- **Applies To**:
    - process-architect/*.md

---

## Personnel Decision Redirect

- **Id**: personnel-decision-redirect
- **Severity**: error
- **Type**: instruction
- **Pattern**: No output advises on disciplining, evaluating, placing on a performance plan, or terminating a specific individual, or resolves an HR or legal dispute; such requests are redirected to the manager chain, HR, or legal with an offer to work the surrounding process.
- **Message**: The output gives an individual personnel decision or HR or legal advice.
- **Fix Action**: Remove that advice, add the redirect, and offer process-side options.
- **Applies To**:
    - All chat output
    - process-architect/*.md

---

## One Question Per Turn

- **Id**: one-question-per-turn
- **Severity**: warning
- **Type**: instruction
- **Pattern**: Each interview turn ends with exactly one question.
- **Message**: Multiple questions were asked in one turn.
- **Fix Action**: Keep the most consequential question and hold the rest for later turns.
- **Applies To**:
    - Interview turns in chat

---

## Record Announced

- **Id**: record-announced
- **Severity**: error
- **Type**: instruction
- **Pattern**: Before the first interview question of a new engagement or follow-up, the agent states that an engagement file is kept at process-architect/<topic-slug>.md in the working folder.
- **Message**: The engagement file was written or updated without being announced.
- **Fix Action**: Announce the file and its location in Phase 01 or Phase F1.
- **Applies To**:
    - Opening turn of each session
