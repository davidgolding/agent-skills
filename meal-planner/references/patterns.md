# Meal Planner Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by meal-planner.

## Patterns

- **Name**: Profile-First Invocation
- **Description**: Resolve `profile.toon` relative to the skill folder and read it before forming any advice; when it is missing, run onboarding and write it before answering.
- **When**: Every invocation, ahead of mode routing.
- **Example**:
```
    Request: "what's for dinner?"
    Step 1: read <skill folder>/profile.toon
    Step 2a: present -> route the request
    Step 2b: absent -> "I need a household profile first; this takes about ten minutes." -> interview
```

---

- **Name**: Single-File TOON Profile
- **Description**: Keep household facts, deck, log, and kitchen state in one TOON file with the optional sections simply absent when unused, rather than splitting state across files.
- **When**: Writing or updating any profile content.
- **Example**:
```
    household: members, constraints, likes, aversions, capacity, routines, budget
    deck:      one entry per accepted meal
    log:       present only once the user has reported back
    kitchen:   present only when the user has volunteered it
```

---

- **Name**: Rotation Deck Retrieval
- **Description**: Answer from deck entries the household has already accepted, treating fresh invention as the exception rather than the default path.
- **When**: Quick asks and the bulk of any interval plan.
- **Example**:
```
    Deal from deck where: no hard-constraint conflict
                          AND last-eaten is outside the rest window
                          AND effort tier matches the slot being filled
```

---

- **Name**: Effort-Tiered Triple
- **Description**: Answer a quick ask with three options spanning real effort levels — a fast version, a genuine cooking version, and one requiring no cooking at all — followed by a longer brainstorm list of deck entries that have landed before.
- **When**: Any one-hop request for a meal idea.
- **Example**:
```
    Fast (about 20 min):  [deck entry]
    Real cooking:         [deck entry]
    No cooking:           [leftovers, breakfast-for-dinner, or the household's usual takeout]

    Also in rotation: [6-10 past hits, names only]
```

---

- **Name**: Seeded Deck At Onboarding
- **Description**: Populate the deck from the meals named in the onboarding interview so the central mechanism is non-empty on first use, and say plainly that early answers reflect the interview rather than observed history.
- **When**: Writing the profile at the end of onboarding.
- **Example**: "Your deck starts with the nine meals you named. It gets sharper as you tell me how things land."

---

- **Name**: Graceful Layer Degradation
- **Description**: Treat the log and kitchen sections as optional and possibly stale, answering on whatever is present and naming the gap at most once per request in a single clause.
- **When**: Any mode that would benefit from a section that is absent, thin, or old.
- **Example**:
```
    Good: "Working from the deck only — the log is still empty."
    Good: "Your kitchen list is about six weeks old, so I treated it as a hint."
    Bad:  "Please update your pantry inventory before I can plan."
```

---

- **Name**: Resting And Retiring
- **Description**: Hold recently-eaten entries out of circulation for a rest window, and drop entries that have missed repeatedly, so variety and pruning both come from state rather than from the user asking.
- **When**: Dealing any suggestion, and when closing a request that produced a verdict.
- **Example**:
```
    Ate it two days ago  -> resting, not dealt
    Landed well          -> promoted, dealt more readily
    Missed twice         -> retired from the deal, kept in the file with its verdict
```

---

- **Name**: Untried Candidate Slotting
- **Description**: Introduce at least one meal the family has not tried into any interval covering three or more meals, so the deck keeps growing instead of narrowing to the same rotation.
- **When**: Building an interval plan.
- **Example**: "Six from your rotation, plus one new one on Thursday — the sheet-pan gnocchi — since Thursday is your low-stakes night."

---

- **Name**: Heuristic Cost By Default
- **Description**: Reason about cost through ingredient economics, seasonality, pantry-first construction, and stretch meals, without asserting specific prices.
- **When**: Any cost-aware request where the user has not asked for real deal research and has supplied no ad or price list.
- **Example**: "Chicken thighs over breasts, dried beans doing the stretching, cabbage because it is in season and cheap all winter."

---

- **Name**: Sourced Deal Research
- **Description**: Look up real prices only on an explicit request for a budget-driven shop or against material the user supplies, and attribute and date whatever is found.
- **When**: The user asks for the actual deals, names a store to check, or pastes a circular.
- **Example**: "Per this week's circular you pasted (dated the 18th): pork shoulder at the sale price, so carnitas stretch across two dinners."

---

- **Name**: Advisory Nutrition With Absolute Constraints
- **Description**: Keep nutritional guidance food-shaped — vegetables present, protein at every meal, variety across the week — while enforcing allergies, medical restrictions, and dietary rules without exception in every mode including the no-cook option.
- **When**: Every suggestion, plan, and score.
- **Example**:
```
    Advisory: "Three of these lean beige, so Wednesday's is the vegetable-forward one."
    Absolute: the no-cook fallback is checked against the nut allergy too, not just the cooked options
```

---

- **Name**: Five-Axis Scoring With Visible Reasoning
- **Description**: Score a candidate recipe on flavor, ease of preparation, cost, nutritional value, and overall quality on a one-to-five-star scale, stating which household facts drove each verdict, and reserving a Michelin-level note for cases that genuinely merit it.
- **When**: The user asks for recipes or for a candidate to be evaluated.
- **Example**:
```
    Flavor      4/5  - your household likes acid and heat; this has both
    Ease        2/5  - two pans and a 40-minute braise, wrong for a weeknight
    Cost        4/5  - cheap cut, long cook
    Nutrition   3/5  - good protein, light on vegetables as written
    Quality     4/5  - a genuinely good version of the dish
```

---

- **Name**: Proposed Household Edits
- **Description**: Write deck and log changes as ordinary completion of a request, but surface any change to durable household facts for the user to confirm before it lands.
- **When**: Closing any request in which a household fact appeared to change.
- **Example**: "You mentioned Ellis has stopped eating eggs — want me to put that in the profile as an aversion, or is it a phase?"

---

- **Name**: Shopping List With On-Hand Assumptions
- **Description**: End any multi-meal plan with a consolidated shopping list and an explicit short statement of what the plan assumes is already in the house.
- **When**: Any plan covering more than a single meal.
- **Example**: "Assuming you have rice, soy sauce, garlic, and olive oil. Everything else is on the list."

---

## Anti-Patterns

- **Name**: Dinner-Hour Interrogation
- **Description**: Responding to "what's for dinner" with clarifying questions about who is home, how much time there is, or what the user feels like.
- **Why**: It hands the decision load straight back to a person who asked precisely because they had none left, which is the failure this skill exists to prevent.
- **Instead**: Answer from the profile with the three-tier triple, which already spans the energy range, and let the user re-deal if none of it fits.

---

- **Name**: Fresh Generation At Dinner Time
- **Description**: Inventing plausible new meals for a quick ask instead of dealing from the deck.
- **Why**: Untested suggestions carry no evidence this family will eat them, take longer to produce, and surface the same generic options any recipe site would.
- **Instead**: Deal from the deck, and confine new candidates to interval plans and explicit research requests.

---

- **Name**: Inventing Past Successes
- **Description**: Describing meals as household favorites, past hits, or things the family loved when the log holds no such record.
- **Why**: It fabricates the one thing the profile exists to hold, and the user cannot tell fabricated history from real history until a suggestion lands badly.
- **Instead**: Say the deck is still warming up and mark seeded entries as coming from the interview rather than from observed verdicts.

---

- **Name**: Inventory Gatekeeping
- **Description**: Requiring an updated kitchen state or log before answering, or repeating the request for one across a response.
- **Why**: The optional sections were made optional because they will be maintained irregularly at best; a skill that demands upkeep to function will simply stop being used.
- **Instead**: Answer on what is present, name the gap once in a clause, and move on.

---

- **Name**: Constraint Trade-Off
- **Description**: Weighing a hard dietary constraint against convenience, cost, variety, or the appeal of a particular dish, including in the no-cook fallback.
- **Why**: Allergies and medical restrictions are safety boundaries, not preferences, and the no-cook path is exactly where a default takeout order slips past the check.
- **Instead**: Filter against hard constraints first in every mode, then optimize within what remains.

---

- **Name**: Asserting Current Prices
- **Description**: Quoting specific prices, sale amounts, or per-unit costs without a supplied ad or a cited, dated lookup.
- **Why**: Grocery pricing is local, volatile, and poorly represented online, so a confident number is likely wrong and will be discovered wrong at the register.
- **Instead**: Reason about relative cost heuristically, and attribute and date any real price that came from research or from the user.

---

- **Name**: Silent Profile Rewrite
- **Description**: Changing household facts, dropping deck entries, or restructuring the profile without telling the user.
- **Why**: The profile is the user's own record of their household and is meant to be hand-editable; silent edits destroy their ability to trust or correct it.
- **Instead**: Write deck and log state routinely, propose household changes for confirmation, and preserve unrelated content on every write.

---

- **Name**: Menu Sprawl
- **Description**: Returning a long undifferentiated list of options to a quick ask, or three options that all require comparable real cooking.
- **Why**: Both re-create the deliberation the three-tier shape was designed to eliminate — one by volume, the other by leaving the no-energy case unanswered.
- **Instead**: Three options at genuinely different effort levels, one of which requires no cooking, with the longer list clearly secondary and for browsing.

---

- **Name**: Deck Ossification
- **Description**: Letting the deck settle into the same dozen meals by never slotting untried candidates.
- **Why**: A deck that stops growing converges on the household's existing habits, at which point the skill adds nothing they could not do from memory.
- **Instead**: Slot at least one untried candidate into any interval of three or more meals, and use research requests to earn new entries.

---

- **Name**: Macro Lecture
- **Description**: Volunteering calorie counts, macro breakdowns, or nutritional correction the user did not ask for.
- **Why**: The household asked for dinner, and unrequested quantification converts a helpful answer into a judgment about their eating.
- **Instead**: Keep nutrition food-shaped and implicit in what gets suggested; produce numbers when the user asks for numbers.

---

- **Name**: Extra State Files
- **Description**: Creating additional files for the log, kitchen state, deck, caches, or notes alongside `profile.toon`.
- **Why**: It breaks the portability the single-file design exists for and gives the user more than one place where their household's truth lives.
- **Instead**: Keep all state in `profile.toon` as optional sections.

---

- **Name**: Hardcoded Local Paths
- **Description**: Writing an absolute path to the profile, a project directory, or a harness-specific tool into the skill's instructions or output.
- **Why**: This skill is loaded from other project folders and other applications; an absolute path or an assumed tool breaks it the first time it travels.
- **Instead**: Resolve the profile relative to the skill folder, and name platform-native question tools with a plain-chat fallback.

---
