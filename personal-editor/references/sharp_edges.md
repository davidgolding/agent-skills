# Sharp Edges

This document defines the sharp edges used by personal-editor.

---

## Context Bloat and Word Count Limit

- **Id**: context-bloat-limit
- **Summary**: Processing texts larger than 2000 words degrades analysis quality and triggers context/performance issues.
- **Severity**: high
- **Situation**: When the user submits a text passage larger than 2000 words.
- **Why**: The multi-pass analysis requires deep reasoning and multiple internal passes; larger texts exceed performance boundaries and dilute feedback.
- **Solution**:
    - Count the words upfront, and past the limit, report the count and request a shorter passage or offer to split it before any pass runs.
- **Symptoms**:
    - Slow response times, generic critiques, missing citations, or incomplete runs.
- **Detection Pattern**: Text inputs where the word count exceeds 2000 words.

---

## In-Scope Request Declined as Out of Domain

- **Id**: in-scope-request-declined
- **Summary**: The skill hedges on or declines a request its own description names as a trigger, treating the literary framing as a scope boundary.
- **Severity**: medium
- **Situation**: When the submitted passage sits outside literary fiction — a history monograph judged against Bancroft or Parkman standards, a plain copyediting request on technical or business prose, or a passage whose genre sits at a distance from the four passes' usual literary subject.
- **Why**: The skill's adjudication register names literary prizes, and a request that reads as belonging to another field can be mistaken for one outside the skill's remit. The description's triggers are the scope — line edits, style analysis, rhetorical analysis, and caliber verdicts across all five named prizes, two of which are history prizes — so any passage matching a trigger is in scope regardless of genre.
- **Solution**:
    - Treat the frontmatter description's trigger conditions as the operative scope, and run all four passes on any passage matching one, calibrating the adjudication to the prize standard that fits the passage's genre.
- **Symptoms**:
    - The skill asks whether it is the right tool for a request its description already covers, or delivers a truncated report on non-fiction prose.
- **Detection Pattern**: A response declining, hedging on, or narrowing a request whose subject matches a trigger condition in the frontmatter `description`.

---

## CriticMarkup Rendered as Literal Text

- **Id**: criticmarkup-literal-render
- **Summary**: The annotated passage reaches a surface that does not interpret CriticMarkup, so the writer reads brace delimiters instead of tracked changes.
- **Severity**: medium
- **Situation**: When the report is delivered anywhere other than a CriticMarkup-aware editor — a terminal, a plain chat surface, a rendered Markdown preview without the extension.
- **Why**: CriticMarkup is a plain-text convention, not a Markdown feature; unsupported surfaces pass the delimiters straight through. Dense annotation is legible when rendered and close to unreadable when not, so the same report can be clear or opaque depending only on where it lands.
- **Solution**:
    - Keep each annotation scoped to the shortest segment that carries the change, so the delimiters stay readable unrendered, and state in the report that suggestions are marked in CriticMarkup.
- **Symptoms**:
    - Report text showing `{--`, `{++`, or `{>>` delimiters inline; the writer asking what the braces mean.
- **Detection Pattern**: Annotated segments running longer than roughly a clause, or nested annotations stacked on one segment.

---

## Orchestrated Sub-Skill Unavailable

- **Id**: sub-skill-unavailable
- **Summary**: One of `gmeu-copyeditor`, `prose-fingerprinter`, or `rhetorician` is absent at runtime, and its pass proceeds ungrounded.
- **Severity**: high
- **Situation**: During the pass that depends on the missing sub-skill's rules.
- **Why**: Each of the first three passes grounds its claims in a specific sub-skill's rule set. When one is unavailable, the pass still produces plausible output — general copyediting instinct, generic style vocabulary, commonly known figures — so the grounding loss surfaces as thinner, more generic findings rather than as an error.
- **Solution**:
    - Confirm each sub-skill is available before its pass runs, and when one is missing, state in that section which grounding was unavailable and that its findings are ungrounded rather than presenting them as rule-derived.
- **Symptoms**:
    - A pass section citing no specific rule, naming only well-known rhetorical figures, or describing style in adjectives without structural evidence.
- **Detection Pattern**: A report section attributing no finding to its named sub-skill's rules while the other sections do.

---
