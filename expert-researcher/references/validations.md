# Validations

This document defines the validations used by expert-researcher.

---

## Citations Retrieved In Session

- **Id**: citations-retrieved
- **Severity**: error
- **Type**: semantic
- **Pattern**: A citation in the answer (link, DOI, title or author-year) that does not match a source returned by a search or fetch call in the current session or present in the user-supplied corpus.
- **Message**: Every citation must point to a source actually retrieved in this session.
- **Fix Action**: Replace the citation with a retrieved source that supports the claim, or relabel the claim as `(model knowledge, uncited)`.
- **Applies To**:
    - Research answers in chat
    - Line briefs

---

## Unresolved Citation Markers

- **Id**: unresolved-citation-markers
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?i)\[(?:citation|source|ref)(?:\s+needed)?\]
    - (?i)\((?:Author|Authors),?\s*(?:Year|n\.d\.)\)
    - (?i)\]\((?:link|url|#)\)
- **Message**: The answer contains a citation stub instead of a resolved source.
- **Fix Action**: Resolve the stub to a retrieved source, or relabel the claim as `(model knowledge, uncited)`.
- **Applies To**:
    - Research answers in chat
    - Line briefs

---

## Certainty Marks Present

- **Id**: certainty-marks-present
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A substantive claim in the answer with no [settled], [contested] or [speculative] mark, when the user has not requested a format that omits them; or a claim marked contested or speculative in a brief that appears unmarked or as settled.
- **Message**: Each substantive claim carries its certainty mark, matching the mark recorded during gathering.
- **Fix Action**: Add the mark from the line's ledger, and for contested claims name the competing positions with citations.
- **Applies To**:
    - Research answers in chat

---

## Live-Source Fallback Disclosed

- **Id**: fallback-disclosed
- **Severity**: error
- **Type**: semantic
- **Pattern**: An answer produced without successful live search or fetch calls, when neither a user corpus nor a model-knowledge-only instruction applies, that lacks an opening statement that no live sources were consulted.
- **Message**: Answers drawn from model knowledge without live sources say so at the top.
- **Fix Action**: Open the answer with a one-line statement that no live sources were reachable and the content comes from model knowledge, and record this in the coverage note.
- **Applies To**:
    - Research answers in chat

---

## Lines Of Inquiry Fully Specified

- **Id**: lines-fully-specified
- **Severity**: error
- **Type**: schema
- **Pattern**: A line of inquiry in the plan missing a precise question, a named discipline or corridor at subfield level, or the depth tier for the run.
- **Message**: Each line of inquiry pairs one precise question with one named discipline or corridor, under a stated depth tier.
- **Fix Action**: Rewrite the line per Faceted Query Decomposition and Discipline Corridor Mapping, and state the depth tier.
- **Applies To**:
    - Research plans in chat

---

## Plan Gate On Deep Or Ambiguous Prompts

- **Id**: plan-gate-deep
- **Severity**: error
- **Type**: semantic
- **Pattern**: Gathering calls made on a deep-tier or ambiguous prompt before the user approved the plan, or a deep-tier plan that omits the lines of inquiry, disciplines, depth or inferred audience level.
- **Message**: Deep or ambiguous prompts get a full plan and an approval wait before gathering.
- **Fix Action**: Present the plan with lines, disciplines, depth and inferred audience level, end the turn, and resume gathering only after approval or edits.
- **Applies To**:
    - Research plans in chat

---

## Coverage Note Present

- **Id**: coverage-note-present
- **Severity**: warning
- **Type**: schema
- **Pattern**: A research answer missing a closing coverage note, or a coverage note missing the depth tier, each line's status (saturated or stopped at budget), the source base, or known source limitations.
- **Message**: Each research answer closes with a complete coverage note.
- **Fix Action**: Append the coverage note per the Coverage Note pattern.
- **Applies To**:
    - Research answers in chat

---

## User Format Takes Precedence

- **Id**: user-format-precedence
- **Severity**: error
- **Type**: semantic
- **Pattern**: An answer that departs from a format, length, citation style, depth budget or audience level the user explicitly specified.
- **Message**: The user's stated format and constraints override the skill's defaults.
- **Fix Action**: Re-render the findings in the user's specified format, keeping only the defaults the user left unspecified.
- **Applies To**:
    - Research answers in chat

---

## Chat-Only Default Medium

- **Id**: chat-only-default
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A file, HTML page, artifact or generated image produced for a research answer when the user did not ask for that format.
- **Message**: Research answers default to rich markdown in chat.
- **Fix Action**: Deliver the answer as markdown in chat, using tables and Mermaid or ASCII diagrams for visual structure.
- **Applies To**:
    - Research answers in chat

---

## Workspace Untouched In Research Mode

- **Id**: workspace-untouched
- **Severity**: error
- **Type**: semantic
- **Pattern**: A file-modifying or code-executing tool call made while research mode is active.
- **Message**: Research mode reports findings and leaves the user's files and code unchanged.
- **Fix Action**: Revert to reporting: research the operational prompt and present the findings, and offer to leave research mode if the user wants the operation performed.
- **Applies To**:
    - Tool calls during research mode

---

## Audience Level Fit

- **Id**: audience-level-fit
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An answer whose register departs from the inferred or specified audience level: undefined terms of art below specialist level, near-verbatim source phrasing, or, for non-technical subjects, generic tips without mechanisms or field-specific sources.
- **Message**: The answer's register matches the reader's level in both directions.
- **Fix Action**: Re-compose per Audience Level Inference and Pedagogical Structure Selection: define or replace terms of art, translate source phrasing, or lift a flattened answer with mechanisms and citations.
- **Applies To**:
    - Research answers in chat
