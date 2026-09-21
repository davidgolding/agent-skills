# Validations

This document defines the validations used by meal-planner.

---

## Profile Read Before Advice

- **Id**: profile-read-first
- **Severity**: error
- **Type**: instruction
- **Pattern**: A response containing meal suggestions, a plan, or recipe scores where no profile read and no onboarding interview occurred earlier in the invocation.
- **Message**: Meal advice was produced without reading the household profile.
- **Fix Action**: Read `profile.toon` from the skill folder before forming candidates; when it is absent, run the onboarding interview and write the profile first, or state explicitly that the answer is generic and ask about allergies before naming a dish.
- **Applies To**:
    - Every invocation, before any suggestion is written

---

## Single Profile File

- **Id**: single-state-file
- **Severity**: error
- **Type**: instruction
- **Pattern**: Creation of any state file in the skill folder other than `profile.toon`, including separate log, deck, kitchen, cache, or notes files.
- **Message**: All household state belongs in `profile.toon` as optional sections.
- **Fix Action**: Fold the content into the appropriate section of `profile.toon` and remove the extra file.
- **Applies To**:
    - `*.toon`
    - `*.json`
    - `*.md` written into the skill folder as state

---

## Hard Constraints Applied To Every Tier

- **Id**: constraints-all-tiers
- **Severity**: error
- **Type**: instruction
- **Pattern**: A multi-option answer in a household with hard constraints on file where any option — particularly a no-cook, leftovers, or takeout option — was not checked against those constraints.
- **Message**: A hard dietary constraint was not applied to every option offered.
- **Fix Action**: Filter all options against the Household hard constraints as one step before writing any of them; for a remembered takeout fallback, name the specific safe item rather than the restaurant.
- **Applies To**:
    - Quick ask answers
    - Interval plans
    - Recipe scores

---

## Three Tiers Including Zero Cooking

- **Id**: three-tier-shape
- **Severity**: error
- **Type**: instruction
- **Pattern**: A quick ask answered with fewer than three options, with options that all require comparable cooking effort, or with no option requiring no cooking at all.
- **Message**: A quick ask must span real effort levels and include a genuinely no-cook option.
- **Fix Action**: Restructure into a fast option, a real-cooking option, and a no-cook option, tiering by active attention and cleanup rather than elapsed time.
- **Applies To**:
    - Quick ask answers

---

## No Questions On A Quick Ask

- **Id**: quick-ask-no-questions
- **Severity**: error
- **Type**: instruction
- **Pattern**: A one-hop request for a meal idea answered with clarifying questions about who is home, available time, energy level, or what the user feels like, in place of an answer.
- **Message**: A quick ask was answered with questions instead of suggestions.
- **Fix Action**: Answer from the profile with the three-tier triple, which already spans the energy range, and offer a re-deal instead of asking.
- **Applies To**:
    - Quick ask answers

---

## Past Success Claims Require A Log

- **Id**: past-success-requires-log
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `(?i)\b(past hit|your favorite|family favorite|always a hit|you loved|they loved|went over well last)\b` asserted while the profile's log section is absent or empty
- **Message**: Past household approval was claimed with no log to support it.
- **Fix Action**: Frame seeded entries as meals the user named during onboarding, and say the deck is still warming up rather than implying observed history.
- **Applies To**:
    - Every response drawing on deck entries

---

## No Unsourced Prices

- **Id**: no-unsourced-prices
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `\$\s?\d` in a response where the user supplied no ad or price list and no lookup was performed in this session
    - `(?i)\b\d+(\.\d+)?\s*(cents|dollars)\s+(a|per)\b` under the same condition
- **Message**: A specific price was asserted with no supplied material and no cited lookup.
- **Fix Action**: Keep default cost reasoning comparative and unquantified; quote figures only from user-supplied material or an in-session lookup, attributed and dated.
- **Applies To**:
    - Every cost-aware response

---

## Nutrition Numbers Only On Request

- **Id**: macros-on-request-only
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - `(?i)\b\d+\s*(kcal|calories)\b` where the user did not ask for nutritional figures
    - `(?i)\b\d+\s*g\s+(of\s+)?(protein|carbs|carbohydrates|fat|fiber)\b` under the same condition
- **Message**: Unrequested nutritional quantification was volunteered.
- **Fix Action**: Keep nutrition food-shaped — vegetables present, protein at every meal, variety across the week — and produce numbers only when asked.
- **Applies To**:
    - Every response other than one answering an explicit nutrition question

---

## Interval Defaults To One Week

- **Id**: interval-default-week
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A planning request with no stated span answered for a different interval, or answered without saying which interval was chosen.
- **Message**: A planning request with no stated span should default to one week and say so.
- **Fix Action**: Plan one week and state that one week was assumed.
- **Applies To**:
    - Interval plans

---

## Untried Candidate Present

- **Id**: untried-candidate-slot
- **Severity**: warning
- **Type**: instruction
- **Pattern**: An interval plan covering three or more meals composed entirely of existing deck entries.
- **Message**: The plan introduces nothing new, which lets the deck ossify.
- **Fix Action**: Slot at least one untried candidate into the interval, placed on a low-stakes occasion where a miss costs little.
- **Applies To**:
    - Interval plans of three or more meals

---

## Shopping List With On-Hand Assumptions

- **Id**: shopping-list-assumptions
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A plan covering more than one meal presented with no consolidated shopping list, or with a list that does not state what it assumes is already in the house.
- **Message**: A multi-meal plan needs a consolidated list and an explicit on-hand assumption.
- **Fix Action**: Consolidate ingredients across the plan into one list and name in a single line what the plan assumes is already on hand.
- **Applies To**:
    - Interval plans

---

## Complete Score Axes

- **Id**: score-axes-complete
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A recipe score missing any of flavor, ease of preparation, cost, nutritional value, or overall quality, omitting the one-to-five-star scale, or stating scores without the reasoning that produced them.
- **Message**: A score is incomplete or unexplained.
- **Fix Action**: Score all five axes on the one-to-five-star scale and state which household facts drove each verdict.
- **Applies To**:
    - Recipe scoring responses

---

## Michelin Restraint

- **Id**: michelin-restraint
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A Michelin-level distinction attached to a weeknight family recipe or to any candidate whose reasoning does not support the claim.
- **Message**: The Michelin-level note is being used as a superlative rather than a distinction.
- **Fix Action**: Reserve it for candidates that genuinely merit it and omit it otherwise; the five-star axes carry ordinary praise.
- **Applies To**:
    - Recipe scoring responses

---

## Household Edits Proposed Not Written

- **Id**: household-edit-confirmation
- **Severity**: error
- **Type**: instruction
- **Pattern**: A change to household composition, hard constraints, likes, aversions, routines, or budget written to the profile without the user confirming it.
- **Message**: A durable household fact was changed without confirmation.
- **Fix Action**: Write deck and log state routinely, but surface household changes as a proposal and wait for the user's answer.
- **Applies To**:
    - Profile writes

---

## Amend Rather Than Regenerate

- **Id**: amend-not-regenerate
- **Severity**: error
- **Type**: instruction
- **Pattern**: A profile write that replaces the whole file when the request only added a log entry, altered a deck verdict, or touched a single section.
- **Message**: A targeted update rewrote the entire profile and may have dropped hand-edited content.
- **Fix Action**: Amend only the sections the request touched, preserve unrecognized content, and re-read the file afterward to confirm the written section parses.
- **Applies To**:
    - `profile.toon`

---

## Degradation Named Once

- **Id**: single-degradation-notice
- **Severity**: warning
- **Type**: instruction
- **Pattern**: More than one mention per response of a missing, thin, or stale optional section, or any request that the user update the log or kitchen state before an answer is given.
- **Message**: A missing optional section is being raised repeatedly or treated as a prerequisite.
- **Fix Action**: Name the gap once in a single clause, answer on what is present, and never require an update to proceed.
- **Applies To**:
    - Every response where an optional section is absent or stale

---

## Relative Paths Only

- **Id**: relative-paths-only
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `(/Users/|/home/|[A-Z]:\\\\)` appearing in this skill's files or in its output as the location of the profile or of any skill resource
- **Message**: An absolute or machine-specific path would break this skill when loaded from another project or application.
- **Fix Action**: Resolve the profile and all resources relative to the skill folder.
- **Applies To**:
    - `SKILL.md`
    - `references/*.md`
    - Every response naming a file location

---
