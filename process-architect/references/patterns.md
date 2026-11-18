# Process Architect Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by process-architect.

## Patterns

- **Name**: Current-State Map
- **Description**: A compact textual map of how the work flows today, written in the org's own vocabulary: trigger, steps with the role that does each, handoffs, tools, approval points, volumes and timings, and pain points marked where they occur.
- **When**: Phase 03 of every new engagement, and again whenever a follow-up reveals the process has changed.
- **Example**:
```
    Trigger: Client success files a "change request" in the shared tracker (~15/week)
    1. CS lead triages in Monday sync -> assigns to a dev pod        [wait: up to 7 days]
    2. Pod lead estimates; >3 days of work needs director sign-off   [PAIN: sign-off takes 1-3 weeks]
    3. Dev builds; QA in staging
    4. Release on fortnightly train                                   [wait: up to 14 days]
    Tools: shared tracker, Slack #cs-requests, release calendar
    Vocabulary: "CR", "pod", "the train", "director sign-off"
```

---

- **Name**: Problem Archetypes
- **Description**: Six recurring problem shapes used as the diagnostic lens in Phase 04. Each has the signals that suggest it, probing questions to test the fit, framework lenses to generate options, and the ways fixes for it typically fail. Problems often combine two archetypes; name a primary and a secondary when that is the case.
- **When**: Phase 04 diagnosis, Phase 05 option generation, and Phase 06 forecasting (failure modes feed the forecasts).
- **Example**:
```
    1. Bottleneck / throughput
       Signals: work piles up at one step; one person or team is always "the hold-up"; cycle time long but touch time short.
       Probes: Where does work wait longest? What happens when that person is out? How much of the wait is queue vs work?
       Lenses: Theory of Constraints (find, exploit, subordinate, elevate); WIP limits; value-stream mapping of wait vs work time.
       Failure modes: speeding up a non-constraint step; adding headcount before removing waste at the constraint; the bottleneck moves and nobody notices.

    2. Handoff / ownership gap
       Signals: things "fall through the cracks"; repeated "I thought you had it"; rework after handoffs; no single owner of the end-to-end outcome.
       Probes: Who would be blamed if this failed? What does the receiver need that it doesn't get? Is there a definition of "done" at each handoff?
       Lenses: RACI or DACI for ownership; explicit handoff checklists or definitions of ready/done; service-level agreements between teams.
       Failure modes: RACI charts that nobody consults; too many "Accountable" roles; checklists that grow until they are skipped.

    3. Decision latency
       Signals: work waits for approval or consensus; decisions get revisited; escalations are slow; meetings end without decisions.
       Probes: Who actually decides, and who thinks they decide? What is the cost of a wrong call vs a late one? Which decisions could be pre-approved under a threshold?
       Lenses: decision-rights mapping (DACI, RAPID); thresholds and delegated authority; reversible vs irreversible decision split; decision logs.
       Failure modes: delegation on paper while the senior person keeps overruling; thresholds set so low nothing changes; consensus culture reasserting itself.

    4. Overload / prioritization
       Signals: everything is urgent; constant context switching; missed deadlines across the board; intake has no gate.
       Probes: How does new work arrive, and who can say no? How many things are in progress per person? What was dropped last quarter, and did anyone notice?
       Lenses: Kanban and WIP limits; a single intake with a triage owner; OKRs or a stop-doing list; capacity allocation (e.g., 70/20/10).
       Failure modes: priorities set but the intake bypassed by senior requesters; WIP limits ignored under pressure; a "priority 1" label inflating.

    5. Rework / quality
       Signals: work comes back; defects found late; the same mistakes recur; heavy inspection at the end.
       Probes: Where are errors introduced vs where are they found? What does the rework cost in time? Is there a standard for "good"?
       Lenses: root-cause tools (5 Whys, fishbone); shift checks left (standards, templates, peer review at the source); DMAIC for measurable recurring defects.
       Failure modes: adding a final inspection layer instead of fixing the source; root-cause sessions that blame individuals; templates nobody updates.

    6. Change adoption
       Signals: a new process or tool exists but people work around it; the rollout "didn't stick"; shadow spreadsheets.
       Probes: What did people lose with the change? Who was consulted before it launched? Which part of the old way do people still use, and why?
       Lenses: ADKAR (awareness, desire, knowledge, ability, reinforcement); pilot with willing teams; remove the old path; make the new way the easy way.
       Failure modes: training as the only lever; mandates without reinforcement; leaving the old path open "for now".
```

---

- **Name**: Framework Translation
- **Description**: Use a framework's logic to find the fix, then express the fix in the org's own vocabulary and concrete actions. Name the framework only in the rationale, in parentheses, if at all.
- **When**: Every option in Phase 05 and every recommendation in the deliverable.
- **Example**:
```
    Lens: Theory of Constraints, "exploit the constraint".
    Translated option: "Protect director sign-off time: batch CRs into a 20-minute Thursday slot with a one-page summary for each, so the director decides in the room instead of reading threads." (Why: sign-off is where CRs wait longest.)
```

---

- **Name**: Option Spread
- **Description**: Generate at least three distinct options that differ in reach and cost: one the caller can start alone this week, one at team or process-owner level, one structural. Label each with its authority level, and for buy-in options name the role and the one-sentence core of the case.
- **When**: Phase 05.
- **Example**:
```
    A. [You can do this] Pre-fill a one-page CR summary before each sign-off request.
    B. [Needs buy-in: pod leads] Pod leads approve CRs under 3 days without director sign-off.
       Case: "Sign-off delays cost 1-3 weeks per CR; 80% of CRs are under 3 days; the director keeps everything above that."
    C. [Needs buy-in: director + VP] Replace the fortnightly train with weekly releases for CRs.
```

---

- **Name**: Option Forecast
- **Description**: For each option, a short forecast block: likely outcome over 4-12 weeks, second-order effects, adoption risk, the typical way it goes wrong (drawn from the archetype's failure modes), and a confidence label (likely, plausible, uncertain).
- **When**: Phase 06, and as the baseline for comparison in follow-up Phase F2.
- **Example**:
```
    Option B - pod leads approve CRs under 3 days
    Likely outcome: median CR wait drops from ~2 weeks to ~1 week within a month. (likely)
    Second-order: pod leads take on more judgment calls; the director sees less of the CR flow.
    Adoption risk: medium. The director may keep reviewing "just to be safe".
    Typical failure: delegation on paper, overruled in practice; watch for re-reviews in the first two weeks.
```

---

- **Name**: Success Signals
- **Description**: A checkable definition of "working" for the chosen direction: 1-2 leading indicators observable within two weeks, one lagging outcome, a milestone, a dated check-in, and a tripwire that triggers switching options. Use signals visible in existing tools or meetings.
- **When**: Phase 07, and the basis of every follow-up check-in.
- **Example**:
```
    Leading: share of sub-3-day CRs approved by pod leads within 2 working days (target: 80% by week 2).
    Leading: number of director re-reviews of pod-approved CRs (target: zero after week 2).
    Lagging: median CR request-to-release time (from ~4 weeks to under 2.5 weeks by week 8).
    Milestone: approval threshold announced in #cs-requests by <date>.
    Check-in: <date + 4 weeks>.
    Tripwire: more than 2 pod-approved CRs reversed in a month -> revisit the threshold or switch to option A.
```

---

- **Name**: Deliverable Tiers
- **Description**: Three output formats over the same full analysis. Quick ideas are given in chat; reports and proposals are saved beside the engagement file and summarized in chat.
- **When**: Phase 08, and whenever the caller moves up the ladder.
- **Example**:
```
    Quick ideas (chat, ~1 screen):
      One-line diagnosis -> 3-5 ideas, each with authority label, one-line forecast, one signal it's working -> recommended first move -> check-in date.

    Report (process-architect/<topic-slug>-report.md):
      Summary - Current state - Diagnosis (archetypes + evidence) - Options with forecasts - Recommendation - Success signals - Risks and open questions.

    Proposal (process-architect/<topic-slug>-proposal.md, written for the decision-maker named in Phase 02):
      The ask (one paragraph) - Why now (cost of the status quo, with numbers from the map) - Proposed change - Alternatives considered (from the forecasts) - Rollout plan and owner - Success signals and check-in - Risks and mitigations.
```

---

- **Name**: Engagement File
- **Description**: One Markdown file per engagement at `process-architect/<topic-slug>.md` in the working folder, recording everything a later session needs to resume. People appear by role, not name. Check-ins are appended, never overwritten.
- **When**: Created in Phase 08; updated in every follow-up Phase F3 and on every tier change.
- **Example**:
```
    ---
    title: Change-request approval delays
    started: 2026-11-18
    tier: report
    caller_role: CS team lead
    next_check_in: 2026-12-16
    ---
    ## Problem
    ## Authority (can change directly / needs buy-in)
    ## Current-State Map
    ## Diagnosis
    ## Options and Forecasts
    ## Chosen Direction
    ## Success Signals
    ## Check-ins
    ### 2026-11-18 - Engagement opened; tier: report
```

---

## Anti-Patterns

- **Name**: Framework-First Prescription
- **Description**: Opening with "you should adopt Kanban / OKRs / RACI" before mapping how the org works.
- **Why**: Imported frameworks arrive in foreign vocabulary, ignore local constraints, and read as consultant theater, so teams resist or adopt them in name only.
- **Instead**: Complete the Current-State Map first and apply frameworks through Framework Translation.

---

- **Name**: Authority Blindness
- **Description**: Recommending changes without stating who must approve or carry them out.
- **Why**: The caller cannot act on options that need power they lack, and discovers this only after investing effort.
- **Instead**: Label every option with its authority level and give buy-in options a named role and the case to make.

---

- **Name**: Tier-Scaled Rigor
- **Description**: Skipping forecasts, success signals, or the engagement file because the caller picked quick ideas.
- **Why**: Forecasts and measures are the skill's core value, and cutting them makes later escalation and follow-up impossible without redoing the interview.
- **Instead**: Run every phase at full rigor and shorten only the deliverable.

---

- **Name**: Single-Answer Advice
- **Description**: Presenting one recommended fix with no alternatives.
- **Why**: The caller cannot weigh trade-offs or fall back when the fix stalls, and the tripwire has nothing to switch to.
- **Instead**: Follow the Option Spread pattern and forecast every option before recommending one.

---

- **Name**: Unfalsifiable Success
- **Description**: Success measures like "better collaboration" or "improved efficiency".
- **Why**: Nobody can tell at a check-in whether the change worked, so follow-ups turn into opinion.
- **Instead**: Use Success Signals with observable indicators, targets, a date, and a tripwire.

---

- **Name**: Silent Record-Keeping
- **Description**: Writing or updating the engagement file without telling the caller.
- **Why**: Writing files the caller didn't expect breaks trust, especially when the content concerns colleagues.
- **Instead**: Announce the file and its location in Phase 01 (or F1) and record people by role.

---

- **Name**: Personnel Drift
- **Description**: Advising on how to discipline, manage out, or evaluate a specific person.
- **Why**: Individual employment decisions carry legal and HR obligations and rest on facts the skill cannot verify; it also turns a process engagement into a judgment about a colleague.
- **Instead**: Redirect that part to the manager chain, HR, or legal, and work the surrounding process issues.

---

- **Name**: Question Stacking
- **Description**: Asking several interview questions in one turn.
- **Why**: Callers answer the easiest one and skip the rest, leaving gaps the diagnosis then papers over.
- **Instead**: Ask one question per turn through the blocking question tool.
