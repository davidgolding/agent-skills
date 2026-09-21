# Meal Planner Interactions

This document defines the interaction flow used by meal-planner.

---

## Interaction Rules

These rules apply to every invocation.

1. **The quick ask gets no questions**: When the request is a one-hop ask for a meal idea, answer it. Do not ask who is home, how much time there is, or what they feel like. The profile already holds the household's shape, and the three-tier answer covers the energy range. Asking questions at the dinner hour re-imposes the decision load the answer exists to remove.
2. **Onboarding and open conversation ask one question at a time**: One question per turn, even when sub-questions feel related. Stacking several questions produces diluted answers about a household you are trying to model accurately.
3. **Prefer the platform's blocking question tool**: Use `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema is not loaded), `request_user_input` in Codex, `ask_user` in Gemini, `ask_user` in Pi. Fall back to numbered options in chat only when no blocking tool exists in the harness or the call errors. Options scaffold the answer without confining it — free-text fallback always remains.
4. **Use multi-select for compatible sets**: Household allergies, disliked ingredients, available equipment, and routine constraints can all coexist; ask those as multi-select. Anything where one answer excludes another — budget posture, who cooks on a weeknight — is single-select.
5. **Ask open-ended when options would narrow the answer**: Favorite family meals, what a typical week actually looks like, and what has gone wrong with meal planning before are all questions where a four-option menu would substitute your imagination for the user's memory. Ask those in plain words, still one at a time, and make them concrete enough to answer ("name three or four dinners your family is always happy to see" rather than "what do you like?").
6. **Never interrogate to fill the profile**: Onboarding captures what the user offers and writes the profile with the rest marked unknown. Gaps get filled by use over weeks, not by a longer interview.

---

## Profile Location and Shape

The profile lives at `profile.toon` inside this skill's folder, resolved relative to the skill's own location so it travels with the folder across projects and applications. It is the only state file this skill creates.

The profile carries four kinds of content:

| Section | Required | Holds | Maintained by |
|---|---|---|---|
| Household | Yes | Members, ages where relevant, hard constraints, likes and aversions, cooking capacity, equipment, routines, budget posture | Onboarding, then confirmed edits |
| Deck | Yes | Meals this family accepts, each with effort tier, rough cost, last-eaten date, and how it landed | Seeded at onboarding, then every closed request |
| Log | No | What was suggested, what was cooked, and the verdict | Appended when the user reports back |
| Kitchen | No | Staples on hand, freezer contents, what needs using up | Only when the user says so |

Hard constraints belong to Household and are never softened by any other section.

---

## Execution Flow

### Phase 0: Profile Check

- **Objective**: Establish whether a household profile exists before any advice is formed.
- **Agent Action**: Check for `profile.toon` in the skill folder. When it exists, read it and note which optional sections are present, how many deck entries exist, and how old the newest log and kitchen entries are. When it does not exist, state plainly that the skill needs a profile first and roughly how long the interview takes, then enter Phase 1.
- **Human Gate-Intervention**: None when the profile exists. When it is absent, say so before beginning the interview rather than opening with questions.
- **Proceed When**: A profile has been read — go to Phase 2. Or no profile exists — go to Phase 1.
- **Pause When**: The harness cannot read the skill folder. Say so, answer the immediate request from the conversation alone, and note that nothing will be remembered.

### Phase 1: Onboarding Interview

- **Objective**: Build a profile accurate enough to answer a quick ask on the same day it is written.
- **Agent Action**: Interview per Interaction Rules 2 through 6, covering household composition; hard dietary constraints, asked early and explicitly because everything downstream depends on them; strong likes and firm aversions per person; who cooks, how much time a normal weeknight allows, and what equipment exists; the household's shopping rhythm, usual stores, and mealtime routines; budget posture; the usual no-cook fallbacks, including the takeout order they default to; and finally an open-ended pass for the meals the family is always glad to see. Write `profile.toon` with the deck seeded from those named meals, each tagged with an effort tier, and mark everything not offered as unknown rather than guessed.
- **Human Gate-Intervention**: Ask one question per turn through the blocking tool. After writing the profile, show the user what was captured in a short readable summary — household, constraints, and the seeded deck — and invite corrections.
- **Proceed When**: The profile is written and summarized — answer the request that triggered the skill, then go to Phase 4.
- **Pause When**: The user stops answering or asks to finish later. Write what exists, say which sections are thin, and stop. A partial profile is usable.

### Phase 2: Mode Routing

- **Objective**: Identify which of four request shapes is being asked, from the request's own signals.
- **Agent Action**: Route as follows.

| Mode | Recognized by | Reads | Returns |
|---|---|---|---|
| Quick ask | A one-hop request for an idea, no interval, no research asked for | Household, deck, recent log | Three effort-tiered options plus a longer brainstorm list |
| Interval plan | A span of time, or a request to plan; default one week | Everything present | A plan across the interval, a consolidated shopping list, and what it assumes is on hand |
| Conversation | An open-ended mealtime problem, or a request to talk it through | As needed | Dialogue, one question at a time |
| Recipe scoring | An explicit request for recipes, or to evaluate a candidate | Household, deck | Scored candidates with the reasoning visible |

  When signals genuinely conflict — a request that reads as both a quick ask and a plan — treat it as the quick ask and offer the plan as a follow-up, because the quick ask is cheaper to be wrong about.
- **Human Gate-Intervention**: None. Routing is silent and never announced as a mode name.
- **Proceed When**: A mode is identified — go to Phase 3.
- **Pause When**: The request is not about food at all. Say what this skill covers and stop.

### Phase 3: Answer

- **Objective**: Produce the mode's output, grounded in the profile.
- **Agent Action**: Apply the patterns in `references/patterns.md` for the routed mode. Hold every mode to the hard constraints in Household. Where an optional section is absent or stale, proceed on what exists and name the gap once, briefly, without asking the user to fix it. For a quick ask, lead with the three tiers and keep the brainstorm list to deck entries that have actually landed; when the log is empty, say the deck is still warming up rather than implying a history. For an interval plan, work against the household's routines, fill mostly from the deck, slot at least one untried candidate when the interval covers three or more meals, and end with the shopping list. For recipe scoring, score all five axes and state what drove each verdict.
- **Human Gate-Intervention**: Offer a re-deal rather than a menu. One line is enough: the user can ask for different options, or for the plan, or for recipes.
- **Proceed When**: The output is delivered — go to Phase 4.
- **Pause When**: A hard constraint makes the request impossible as asked. Say which constraint and what the nearest workable answer is.

### Phase 4: Profile Update and Close

- **Objective**: Leave the profile more accurate than it was.
- **Agent Action**: Write what the request produced: suggestions made, and where the user reported a verdict, the meal and how it landed. Update the affected deck entries — promote what landed, demote what did not, rest what was just eaten, retire what has missed repeatedly. When a durable household fact changed during the conversation, propose that edit for confirmation rather than writing it. Preserve everything unrelated in the file, and keep the result readable to a person opening it by hand.
- **Human Gate-Intervention**: Profile writes to the deck and log are routine and need no permission. Changes to Household facts are proposed and wait for confirmation.
- **Proceed When**: The writes are done — end the turn without ceremony. A quick ask closes with the answer, not with a report about bookkeeping.
- **Pause When**: A proposed Household edit is outstanding. Ask once, and let the answer arrive whenever it arrives.

---

## Handoff

- **Completion State**: The routed mode's output has been delivered, `profile.toon` reflects the request, and any durable household change has been proposed for confirmation.
- **Exception / Fallback Handoff**: When the skill folder is not writable, deliver the answer from conversation context, state plainly that nothing was remembered, and name what the user would need to do for memory to work.
