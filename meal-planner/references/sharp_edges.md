# Sharp Edges

This document defines the sharp edges used by meal-planner.

---

## Hard Constraint Dropped In The No-Cook Option

- **Id**: constraint-drop-in-fallback
- **Summary**: Allergy and medical filters get applied to the cooked options and skipped on the takeout or leftovers fallback.
- **Severity**: critical
- **Situation**: A quick ask produces three tiers, and the no-cook tier is filled from the household's usual takeout order or from whatever is in the fridge.
- **Why**: The fallback is retrieved as a remembered habit rather than constructed from ingredients, so it never passes through the ingredient-level constraint check the cooked options go through. The habit predates the constraint, or covers a restaurant whose menu the check was never run against.
- **Solution**:
    - Apply the Household hard constraints to all three tiers as a single filter step, before any tier is written.
    - For a remembered takeout fallback, name the specific safe order rather than the restaurant, or state which item the constrained eater takes.
    - When the usual fallback cannot be made safe, replace the tier rather than omitting it — a no-cook option must still be present.
- **Symptoms**:
    - The cooked options carry constraint notes and the no-cook option carries none.
    - The fallback names a restaurant or "the usual" with no item-level detail in a household with an allergy on file.
- **Detection Pattern**: A three-tier answer in a household with hard constraints on file where the no-cook tier names a source of food but no specific dish or item.

---

## Advice Before Profile

- **Id**: advice-before-profile
- **Summary**: A plausible generic answer gets produced for a household the skill knows nothing about.
- **Severity**: critical
- **Situation**: The skill is invoked with a direct question — what should we have for dinner — and no `profile.toon` exists yet.
- **Why**: The question is answerable from general knowledge, and answering feels more helpful than opening with an interview. The answer is fluent enough that the user may not notice it was not about their family, and may act on it against an allergy the skill was never told about.
- **Solution**:
    - Check for the profile before forming any candidate answer, not after.
    - State that a profile is needed and roughly how long the interview takes, then interview.
    - When the user declines the interview, answer with explicit generic framing and ask directly about allergies before naming any dish.
- **Symptoms**:
    - Dinner suggestions appear in a session where no profile was read and no interview happened.
    - The response contains no reference to household members, constraints, or routines.
- **Detection Pattern**: Meal suggestions produced in an invocation with no preceding profile read and no onboarding interview.

---

## Seeded Deck Mistaken For History

- **Id**: seeded-deck-as-history
- **Summary**: Meals named during onboarding get described as proven favorites the family loved.
- **Severity**: high
- **Situation**: The first weeks of use, when the deck holds only interview-seeded entries and the log is empty.
- **Why**: Seeded entries and verdict-bearing entries live in the same deck section and read identically. The brainstorm list is specified as drawing on past successes, which invites describing whatever is in the deck as a past success.
- **Solution**:
    - Distinguish seeded entries from verdict-bearing entries in the profile, and say which kind is being dealt.
    - During the warm-up period, frame the brainstorm list as meals the user named rather than as past hits.
    - Ask for verdicts lightly as meals get cooked, since that is what converts the deck from a list into a record.
- **Symptoms**:
    - Phrases like "a past hit" or "your family loved this" appear while the log section is absent.
    - Confidence in suggestions does not change between week one and month three.
- **Detection Pattern**: Language asserting past household approval in a response where the profile's log section is absent or empty.

---

## Stale Kitchen State Trusted As Current

- **Id**: stale-kitchen-trust
- **Summary**: An old kitchen section gets treated as an accurate inventory, producing plans that assume food which is gone.
- **Severity**: medium
- **Situation**: The user updated the kitchen section once, weeks or months ago, and now asks for a plan built around what is on hand.
- **Why**: The section is present and well-formed, and nothing in the data announces its age unless the entries are dated. Optional-by-design means it will usually be old, which is exactly the condition under which it looks most authoritative.
- **Solution**:
    - Date kitchen entries on write and weigh them by age.
    - Treat anything beyond roughly two weeks as a hint about habits and staples rather than a statement of current stock.
    - Say once that the list is old, and build the plan so a missing item costs a substitution rather than the whole meal.
- **Symptoms**:
    - A plan depends on a specific perishable item recorded long ago.
    - The shopping list omits staples because the kitchen section claims they are present.
- **Detection Pattern**: A plan that relies on perishable kitchen entries whose recorded date is more than about two weeks before the current request.

---

## Fabricated Sale Prices

- **Id**: fabricated-prices
- **Summary**: Specific prices or sale figures get asserted with no supplied ad and no cited lookup.
- **Severity**: high
- **Situation**: The user asks for a cheap week, and cost reasoning drifts from relative economics into concrete numbers.
- **Why**: Plausible prices are easy to produce and make advice feel concrete and authoritative. The heuristic-by-default design means no lookup happened, so there is no source to contradict the invented figure.
- **Solution**:
    - Keep default cost reasoning comparative and unquantified.
    - Quote a number only from material the user supplied or from a lookup performed in this session, and attribute and date it.
    - When the user wants real figures, say that it requires research and offer to do it rather than estimating.
- **Symptoms**:
    - Currency amounts appear in a response where no ad was supplied and no search was run.
    - A total cost for the week is given without a stated source.
- **Detection Pattern**: Currency figures or per-unit costs in a response with no user-supplied price material and no research step in the same session.

---

## Profile Overwritten Rather Than Amended

- **Id**: profile-overwrite
- **Summary**: A routine update rewrites the whole file and silently drops content it did not understand.
- **Severity**: high
- **Situation**: Closing a request that added a log entry or changed a deck verdict, where the simplest write is to regenerate the file.
- **Why**: Regenerating from the sections currently in context is easier than amending in place, and anything the user hand-edited, commented, or added outside the expected shape is not in that context and therefore disappears without an error.
- **Solution**:
    - Amend the specific sections a request touched and leave the rest of the file byte-for-byte alone.
    - Preserve unrecognized content rather than normalizing it away, since the file is meant to be hand-editable.
    - When a structural rewrite is genuinely needed, say so and show what changes before writing.
- **Symptoms**:
    - Hand-written notes or user-added fields vanish after an ordinary session.
    - The file's ordering or formatting changes on requests that only appended a log entry.
- **Detection Pattern**: A profile write that replaces the whole file when the request only added or altered a log entry or a deck verdict.

---

## Log Growth Crowding The Quick Path

- **Id**: log-growth-bloat
- **Summary**: Months of accumulated log entries make the single-file profile expensive to read on exactly the request that must be fastest.
- **Severity**: medium
- **Situation**: Sustained use, where every quick ask loads a file that now carries a long meal history.
- **Why**: The single-file design was chosen for portability and hand-editability, and its accepted cost is that the whole profile loads every time. The log is the only section that grows without bound.
- **Solution**:
    - Keep log entries terse — meal, date, verdict — and push durable conclusions into deck state rather than leaving them implied by history.
    - Compact the log periodically by summarizing older entries into the deck verdicts they produced, proposing the compaction rather than doing it silently.
    - Read recent log entries for a quick ask and the full log only for interval planning.
- **Symptoms**:
    - The profile is dominated by log volume relative to household and deck content.
    - Quick asks slow noticeably as months accumulate.
- **Detection Pattern**: A profile whose log section substantially exceeds the combined size of its household and deck sections.

---

## Malformed TOON On Write

- **Id**: toon-write-malformation
- **Summary**: An incremental write produces a profile the next invocation cannot parse, silently costing the household's memory.
- **Severity**: high
- **Situation**: Appending a log entry or a deck field, particularly one containing a colon, quote, comma, or a multi-line note.
- **Why**: TOON's compactness depends on delimiter and indentation discipline, and free-text verdicts are the content most likely to carry a delimiter character. The damage surfaces on the next invocation rather than at write time, so the failing session looks successful.
- **Solution**:
    - Keep free-text fields short and escape or quote delimiter characters on write.
    - Re-read the profile after writing it and confirm the section just written parses back.
    - When a profile fails to parse, say so, work from what can be recovered, and offer to repair the file rather than starting a new one.
- **Symptoms**:
    - A section reads as empty on the next invocation despite having been written.
    - Verdict text appears merged into an adjacent field.
- **Detection Pattern**: Profile sections that fail to parse, or fields containing unescaped delimiter characters introduced by a previous write.

---

## Effort Tier Mismatched To Actual Energy

- **Id**: effort-tier-mismatch
- **Summary**: The tiers are labeled by cooking time while the real constraint is attention and cleanup, so the "fast" option is not actually easy.
- **Severity**: medium
- **Situation**: A quick ask from someone with no energy, answered with a twenty-minute dish requiring active work at three stages and two pans.
- **Why**: Time is the measurable proxy and gets used as the tier definition, but the thing in short supply at the end of a workday is attention and willingness to clean up. A short recipe with constant attention is harder than a long one that sits in the oven.
- **Solution**:
    - Tier by active attention and cleanup burden, not elapsed time, and say which when it differs.
    - Prefer one-pan and hands-off constructions for the fast tier even when total time is longer.
    - Record why an entry earned its tier so the distinction survives into later deals.
- **Symptoms**:
    - The fast option requires multiple pans or continuous attention.
    - The user repeatedly declines the fast tier and takes the no-cook tier.
- **Detection Pattern**: Fast-tier deck entries requiring multiple pans or more than about two active attention points.

---

## Unverified Recipe Claims

- **Id**: unverified-recipe-claims
- **Summary**: Researched recipes get scored on remembered or assumed content rather than on what the source actually says.
- **Severity**: medium
- **Situation**: A recipe scoring request, where a well-known dish is scored from general knowledge while a specific source is named alongside the score.
- **Why**: Familiar dishes feel knowable without reading the source, and a score with a citation next to it reads as though the citation was the basis. Ingredient lists and method vary enough between versions to move the ease and nutrition axes substantially.
- **Solution**:
    - Score only what was actually read, and say when a score reflects the dish generally rather than a specific recipe.
    - Attribute each named source to the score it produced.
    - Prefer scoring fewer candidates properly over ranking more from assumption.
- **Symptoms**:
    - Scores cite sources whose content does not appear anywhere in the reasoning.
    - Ease or nutrition scores do not reflect the method described in the linked version.
- **Detection Pattern**: Scored candidates naming a source where the stated reasoning contains no detail specific to that source's ingredients or method.

---

## Onboarding Interview Overreach

- **Id**: onboarding-overreach
- **Summary**: The interview tries to capture everything up front and exhausts the user before a profile exists.
- **Severity**: medium
- **Situation**: Onboarding, where more questions plausibly improve the profile and the completeness checks invite thoroughness.
- **Why**: Each additional question is individually justifiable, and the cost is borne entirely at the moment the user has the least invested in the skill. An abandoned interview leaves no profile at all, which is strictly worse than a thin one.
- **Solution**:
    - Cover constraints, composition, capacity, routines, and favorite meals, and mark everything else unknown.
    - Accept partial answers and write the profile with gaps rather than pressing.
    - Let use fill the profile over weeks, since observed verdicts are better data than interview answers anyway.
- **Symptoms**:
    - The interview passes roughly a dozen questions with no profile written.
    - The user's answers get shorter as the interview proceeds.
- **Detection Pattern**: An onboarding interview extending well beyond the named coverage areas, or continuing after the user's answers have become minimal.

---
