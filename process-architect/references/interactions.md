# Process Architect Interactions

This document defines the interaction flow used by process-architect.

## Interaction Rules

1. **One Question Per Turn**: Ask exactly one question per turn and end the turn to wait for the answer. A single focused question gets a complete answer; stacked questions get partial ones.
2. **Blocking Question Tool First**: Ask through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini or Pi) with 2-4 concrete options; its free-text fallback covers answers the options miss. Ask open-ended only when the answer is a narrative ("walk me through what happens after a request comes in") or when options would steer the answer. Fall back to numbered options in chat when no blocking tool exists or the call errors.
3. **Extract Before Asking**: Before each phase, read everything the caller has already said, including the opening prompt and any attached material, and treat every question it answers as answered.
4. **Phase Budget**: Spend 1-3 questions per phase. Full rigor means every phase runs, not that every phase is long.
5. **Show the Map**: At each phase transition, state in one line which phase is finished and which comes next, so the caller always knows where the interview stands.
6. **The Ladder Overrides Everything**: Whenever the caller asks for a fuller deliverable (quick ideas → report → proposal), switch tiers at once, confirm the new tier in one line, and continue from the current phase. Never argue or re-ask.
7. **Proposed Escalation Waits for a Choice**: When the discussion suggests a fuller tier (for example, the fix needs approval from above and the caller will have to make a case), propose the escalation with a one-sentence reason and keep the current tier unless the caller accepts.
8. **Personnel Redirect**: When the caller asks for a decision about a specific individual (performance plan, discipline, firing, an HR or legal dispute), say that part belongs with the manager chain, HR, or legal, then offer to work the process issues around it (unclear expectations, workload, handoffs, decision rights).

## Execution Flow

### Phase 00: Resume Check

- **Objective**: Decide between a new engagement and a follow-up.
- **Agent Action**: Look in the working folder for a `process-architect/` directory and list its engagement files (see the Engagement File pattern in `references/patterns.md`). Match the caller's topic against their titles and problem statements.
- **Human Gate/Intervention**: When more than one file could match, or a file exists but the caller's problem looks new, the caller chooses which engagement to resume or to start fresh.
- **Proceed When**: Exactly one engagement matches the caller's topic (go to the Follow-up Flow), or none matches (go to Phase 01).
- **Pause When**: The match is ambiguous; list the candidate engagements by title and last check-in date and ask which one to resume, or whether to start a new one, and end the turn.

### Phase 01: Open and Choose the Tier

- **Objective**: Set expectations and the deliverable tier.
- **Agent Action**: In two or three sentences, tell the caller you will interview them one question at a time through a fixed set of phases, that you will keep an engagement file at `process-architect/<topic-slug>.md` in the working folder so a later session can check progress, and that people will be recorded by role, not name. Then ask which deliverable they want: quick ideas (a short list in chat), a report (diagnosis and options written up), or a proposal (a case for one direction, ready to share). Mention that they can move up the ladder at any point.
- **Human Gate/Intervention**: The caller picks a tier.
- **Proceed When**: A tier is chosen or stated in the opening prompt.
- **Pause When**: No tier is known; ask for it and end the turn.

### Phase 02: Role and Authority

- **Objective**: Learn who the caller is in this process and what they can change.
- **Agent Action**: Establish the caller's role (team lead, individual contributor, ops or process owner, or other), who owns the process in question, what the caller can change without asking anyone, and whose approval or cooperation the rest would need.
- **Human Gate/Intervention**: The caller answers.
- **Proceed When**: The caller's role, the process owner, and the line between "can change directly" and "needs buy-in" are clear.
- **Pause When**: Any of these is unknown; ask for the first missing one and end the turn.

### Phase 03: Current-State Map

- **Objective**: Describe how the work actually flows today, in the org's own terms.
- **Agent Action**: Build a textual map using the Current-State Map pattern in `references/patterns.md`: trigger, steps and who does them, handoffs, tools, approval points, volumes and timings, and where the pain shows up. Use the caller's vocabulary for teams, tools and artifacts, and note the vocabulary for later translation. When useful, ask the caller to walk through one recent real case from start to finish. Read the map back in a compact form and ask the caller to correct it.
- **Human Gate/Intervention**: The caller confirms or corrects the map.
- **Proceed When**: The caller confirms the map is accurate enough to diagnose from.
- **Pause When**: A step, handoff, or pain point is unclear; ask about the most consequential gap and end the turn.

### Phase 04: Diagnosis

- **Objective**: Name the problem's shape and root causes.
- **Agent Action**: Compare the map against the Problem Archetypes in `references/patterns.md`. Pick the one or two archetypes whose signals best fit, use their probing questions to test the fit, and check `references/sharp_edges.md` for misclassification risks. State the diagnosis in plain language: the archetype in the org's terms, the evidence for it from the map, and the likely root causes.
- **Human Gate/Intervention**: The caller confirms the diagnosis, corrects it, or adds a second archetype.
- **Proceed When**: The caller agrees the diagnosis fits.
- **Pause When**: The caller disputes the fit; ask what feels wrong, re-test against the next-best archetype, and end the turn.

### Phase 05: Options

- **Objective**: Generate distinct, actionable options.
- **Agent Action**: Apply the matched archetypes' framework lenses, translated into the org's vocabulary, to generate at least three options following the Option Spread pattern: one the caller can start alone this week at low cost, one at team or process-owner level, and one structural change. Label each with its authority level, and for buy-in options name the role and the core of the case to make.
- **Human Gate/Intervention**: The caller may rule options out, add constraints, or suggest their own.
- **Proceed When**: At least three viable options remain after the caller's reaction.
- **Pause When**: The caller rules out options or adds a constraint that leaves fewer than three; generate replacements and ask again, then end the turn.

### Phase 06: Forecasts

- **Objective**: Show where each option likely leads.
- **Agent Action**: Write an Option Forecast for each option (see `references/patterns.md`): likely outcome over the next 4-12 weeks, second-order effects, adoption risk, and the most common way it goes wrong in practice. Ground forecasts in the map and the archetype's known failure modes, and state confidence plainly (likely, plausible, uncertain). Then recommend one option or a combination with a one-sentence reason.
- **Human Gate/Intervention**: The caller chooses a direction or accepts the recommendation.
- **Proceed When**: A direction is chosen.
- **Pause When**: The caller is undecided; ask which trade-off matters most to them (speed, cost, buy-in effort, or durability) and end the turn.

### Phase 07: Success Measures

- **Objective**: Make the chosen direction checkable.
- **Agent Action**: Define Success Signals for the chosen direction (see `references/patterns.md`): one or two leading indicators the caller can observe within two weeks, one lagging outcome, a milestone, a dated check-in, and a tripwire that would mean switching options. Prefer signals the caller can see without new tooling.
- **Human Gate/Intervention**: The caller confirms the signals are observable in their setting.
- **Proceed When**: The caller confirms they can observe each signal.
- **Pause When**: A signal cannot be observed in the caller's setting; replace it with an observable proxy and ask again, then end the turn.

### Phase 08: Deliver and Record

- **Objective**: Hand over the deliverable and save the engagement.
- **Agent Action**: Check the draft against `references/validations.md` and fix every error-severity failure. Produce the deliverable in the chosen tier's format (see Deliverable Tiers in `references/patterns.md`): quick ideas go in chat; reports and proposals are written to `process-architect/<topic-slug>-report.md` or `-proposal.md` and summarized in chat. Create or update the engagement file with every section filled.
- **Human Gate/Intervention**: The caller may ask for revisions or a higher tier.
- **Proceed When**: The deliverable is presented and the engagement file is written; close by naming the check-in date and telling the caller to invoke the skill again in this folder to follow up.
- **Pause When**: The working folder is not writable; say so, give the engagement record in chat for the caller to save, and end the turn.

## Follow-up Flow

### Phase F1: Recap

- **Objective**: Re-establish context from the engagement file alone.
- **Agent Action**: Read the engagement file. Summarize in a few lines the problem, the diagnosis, the chosen direction, its success signals and tripwire, and the date of the last check-in. Remind the caller the file will be updated.
- **Human Gate/Intervention**: The caller confirms the recap or corrects it.
- **Proceed When**: The recap is confirmed.
- **Pause When**: The caller says the situation has changed fundamentally (new owner, reorganization, the problem is gone); ask whether to update this engagement or start a new one, and end the turn.

### Phase F2: Check-in

- **Objective**: Compare what happened against the forecast and signals.
- **Agent Action**: Ask what was actually done, then ask about each success signal and the tripwire in turn. Compare against the Option Forecast, noting where reality matched and where it diverged.
- **Human Gate/Intervention**: The caller reports.
- **Proceed When**: Every signal has a reported status (moved, flat, unknown).
- **Pause When**: A signal's status is unknown; ask for the nearest observable evidence and end the turn.

### Phase F3: Adjust

- **Objective**: Decide the next step.
- **Agent Action**: Recommend stay the course, adjust (with the specific change), or switch to another option from the engagement file, with the reason. When the evidence points to a wrong diagnosis, say so and return to Phase 04. Append a dated check-in entry to the engagement file and update the success signals or next check-in date if they changed. Honor ladder requests here as anywhere else.
- **Human Gate/Intervention**: The caller chooses the next step.
- **Proceed When**: The caller chooses and the file is updated.
- **Pause When**: The caller wants to rethink the problem; return to Phase 03 or 04 as appropriate.
