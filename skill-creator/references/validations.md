# Validations

This document defines the validations used by skill-creator.

---

## Absolute Path Detection

- **Id**: skill-absolute-path
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \b/Users/[a-zA-Z0-9_\-\.]+
    - \b/home/[a-zA-Z0-9_\-\.]+
    - \b/var/folders/[a-zA-Z0-9_\-\.]+
- **Message**: Absolute path detected - breaks portability across environments and machines
- **Fix Action**: Replace absolute paths with relative or workspace-relative paths (e.g., use 'skill-creator/references/patterns.md' instead of '/Users/name/repo/skill-creator/references/patterns.md')
- **Applies To**:
    - *.md
    - *.json
    - *.py
    - *.sh

---

## Assertive Trigger Missing

- **Id**: skill-assertive-trigger-missing
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)description:\s*(?!.*(?:use\s+when|triggers\s+when|triggers\s+on|activate\s+when|trigger\s+on)).*$
- **Message**: Skill description is missing assertive triggering constraints (e.g., 'Use when...')
- **Fix Action**: Add explicit trigger rules and keywords to the frontmatter description to guide the agent router (e.g., 'Use when the user says X or wants to perform Y')
- **Applies To**:
    - SKILL.md
    - *.md

---

## Reference System Mapping Missing

- **Id**: skill-reference-system-missing
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?!.*patterns\.md)(?!.*sharp_edges\.md)(?!.*validations\.md)(?!.*interactions\.md).*$
- **Message**: Skill does not define or link to the reference system usage files (patterns.md, sharp_edges.md, validations.md, interactions.md)
- **Fix Action**: Add a 'Reference System Usage' section to the SKILL.md file pointing to patterns.md, sharp_edges.md, and validations.md as the source of truth for Creation, Diagnosis, and Review, plus interactions.md for Interacting when the skill has one
- **Applies To**:
    - SKILL.md

---

## Placeholder Usage

- **Id**: skill-placeholder-usage
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - \b(?:TODO|FIXME|XXX)\b
    - <[^>]*insert[^>]*>
    - \b[a-zA-Z0-9_\-]*placeholder[a-zA-Z0-9_\-]*\b
- **Message**: Unresolved placeholder, TODO, or FIXME comment found in skill documentation
- **Fix Action**: Replace the placeholder with concrete, production-ready instructions or patterns
- **Applies To**:
    - *.md
    - *.json
    - *.py
    - *.sh

---

## Silent Command Instructions

- **Id**: skill-silent-command-instructions
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - \b(?i)(?:run|execute|apply|modify)\s+(?:without\s+asking|directly|silently|automatically)\b
    - \b(?i)do\s+not\s+(?:ask|prompt|confirm)\b
- **Message**: Instructions advocate executing commands or modifications without user confirmation
- **Fix Action**: Ensure instructions state that the agent must explain actions and obtain user consent before running mutating commands or modifying files
- **Applies To**:
    - SKILL.md
    - *.md

---

## Hardcoded Dev Domains

- **Id**: skill-hardcoded-domains
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - \b(?:localhost|127\.0\.0\.1|0\.0\.0\.0)(?::\d+)?\b
    - \b[a-zA-Z0-9\-]+\.local\b
- **Message**: Hardcoded local server URLs or development domains found
- **Fix Action**: Parameterize server addresses or use environment-relative configurations instead of hardcoded dev domains
- **Applies To**:
    - *.json
    - *.py
    - *.sh
    - *.md

---

## Question Stacking Detection

- **Id**: skill-question-stacking
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:ask|pose)\b.*\b(?:multiple|several|many|two|three)\b.*\bquestions?\b
    - (?i)\bstack\b.*\bquestions?\b
- **Message**: Prompt contains instructions advocating question stacking (asking multiple questions at once)
- **Fix Action**: Ensure the prompt instructs the agent to ask exactly one question at a time
- **Applies To**:
    - SKILL.md
    - *.md

---

## Granularity Leakage Detection

- **Id**: skill-granularity-leakage
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:database\s+schema|table\s+name|column\s+name|class\s+name|file\s+path|json\s+key)\b.*\bin\b.*\bbrainstorm\b
- **Message**: Brainstorming instructions should not mention code-level architecture details
- **Fix Action**: Defer code architecture and implementation details to the planning phase
- **Applies To**:
    - SKILL.md
    - *.md

---

## Temporary File Directory Violation

- **Id**: skill-temp-dir-violation
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:write|save|create|put)\b.*\btemporary\b.*\b(?:inside|in|under|to)\b.*\b(?:sub-?directories|folders|nested|docs|brainstorms)\b
    - \bdocs/brainstorms/temp-requirements\.md\b
- **Message**: Temporary brainstorming files should not be written to nested subdirectories or create new directories; they must be stored in the workspace root
- **Fix Action**: Write temporary requirements or intermediate files directly to temp-requirements.md in the workspace root, and delete them immediately after use
- **Applies To**:
    - SKILL.md
    - *.md

---

## Skill SKILL.md Template Violation

- **Id**: skill-structure-skill-md
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?s)(?!.*---\r?\nname:\s*\S+).*$
    - ^(?s)(?!.*description:\s*\S+).*$
    - ^(?s)(?!.*^#\s+[A-Za-z\s\-]+).*$
    - ^(?s)(?!.*##\s+Mandate\b).*$
    - ^(?s)(?!.*##\s+Principles\b).*$
    - ^(?s)(?!.*##\s+Reference\s+System\s+Usage\b).*$
    - ^(?s)(?!.*##\s+Mandate\b.*##\s+Principles\b.*##\s+Reference\s+System\s+Usage\b).*$
    - ^(?s)(?!.*ground\s+your\s+responses?\s+in\s+the\s+provided\s+reference\s+files).*$
- **Message**: SKILL.md does not adhere to the strict template layout (frontmatter, level-1 title heading, or Level-2 headings Mandate, Principles, and Reference System Usage, in that order)
- **Fix Action**: Reformat SKILL.md to include name and description frontmatter, a Level-1 title in Title Case, and the required Level-2 sections in order — Mandate, Principles, and Reference System Usage (verbatim grounding directive plus one bullet per reference file the skill has)
- **Applies To**:
    - SKILL.md

---

## Skill patterns.md Template Violation

- **Id**: skill-structure-patterns
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?s)(?!.*#\s+[A-Za-z\s\-]+\s+Patterns\s+&\s+Anti-Patterns).*$
    - ^(?s)(?!.*This\s+document\s+defines\s+the\s+patterns\s+and\s+anti-patterns\s+used\s+by).*$
    - ^(?s)(?!.*##\s+Patterns\b).*$
    - ^(?s)(?!.*##\s+Anti-Patterns\b).*$
    - (?s)##\s+Patterns\b(?:(?!##\s+Anti-Patterns).)*\bName\b(?!.*\bDescription\b)(?!.*\bWhen\b)(?!.*\bExample\b).*$
    - (?s)##\s+Anti-Patterns\b.*\bName\b(?!.*\bDescription\b)(?!.*\bWhy\b)(?!.*\bInstead\b).*$
- **Message**: patterns.md does not adhere to the strict template layout (Level-1 heading, introductory sentence, Level-2 Patterns/Anti-Patterns headings, or the required keys Name/Description/When/Example for Patterns and Name/Description/Why/Instead for Anti-Patterns)
- **Fix Action**: Restructure patterns.md to have the Level-1 heading, introductory sentence, Level-2 headings, and define all Patterns with Name, Description, When, Example, and Anti-Patterns with Name, Description, Why, Instead
- **Applies To**:
    - *patterns.md

---

## Skill sharp_edges.md Template Violation

- **Id**: skill-structure-sharp-edges
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?s)(?!.*#\s+Sharp\s+Edges).*$
    - (?s)##\s+[A-Za-z\s\-]+\b(?:(?!##).)*\bId\b(?!.*\bSummary\b)(?!.*\bSeverity\b)(?!.*\bSituation\b)(?!.*\bWhy\b)(?!.*\bSolution\b)(?!.*\bSymptoms\b)(?!.*\bDetection\s+Pattern\b).*$
- **Message**: sharp_edges.md does not adhere to the strict template layout or is missing required keys (Id, Summary, Severity, Situation, Why, Solution, Symptoms, Detection Pattern)
- **Fix Action**: Structure sharp_edges.md with Level-2 headings for each sharp edge, ensuring every edge defines Id, Summary, Severity, Situation, Why, Solution, Symptoms, and Detection Pattern
- **Applies To**:
    - *sharp_edges.md

---

## Sharp Edge Detection Pattern Format

- **Id**: skill-sharp-edge-detection-format
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - (?i)-\s*\*\*Detection\s+Pattern\*\*:\s*`?[a-zA-Z0-9_\-]+`?\s*$
- **Message**: Detection Pattern in sharp_edges.md should be a natural language description of what to detect, not a shorthand identifier, function name, or code snippet
- **Fix Action**: Rewrite the Detection Pattern to be a clear natural language description (e.g., 'Registry entries with page ranges spanning 1 page or less containing incomplete sentences.' instead of 'incomplete_sentences')
- **Applies To**:
    - *sharp_edges.md

---


## Skill validations.md Template Violation

- **Id**: skill-structure-validations
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - ^(?s)(?!.*#\s+Validations).*$
    - (?s)##\s+[A-Za-z\s\-]+\b(?:(?!##).)*\bId\b(?!.*\bSeverity\b)(?!.*\bType\b)(?!.*\bPattern\b)(?!.*\bMessage\b)(?!.*\bFix\s+Action\b)(?!.*\bApplies\s+To\b).*$
- **Message**: validations.md does not adhere to the strict template layout or is missing required keys (Id, Severity, Type, Pattern, Message, Fix Action, Applies To)
- **Fix Action**: Structure validations.md with Level-2 headings for each validation, ensuring every validation defines Id, Severity, Type, Pattern, Message, Fix Action, and Applies To
- **Applies To**:
    - *validations.md

---

## Mandate Section Not Task-Framed

- **Id**: skill-mandate-task-framed
- **Severity**: error
- **Type**: semantic
- **Pattern**: A `## Mandate` section describing who the agent is, what it has experienced, or how skilled it is, or omitting the unit of work, the decisions or axes judged, the reference files those judgments ground in, or what a correct output contains.
- **Message**: The Mandate section states the task the skill performs and the criteria it performs it against, not an identity the agent adopts.
- **Fix Action**: Rewrite the section per the Task-Criteria Mandate pattern: name the unit of work, the axes judged, the reference files the judgments ground in, and what a correct output contains.
- **Applies To**:
    - SKILL.md

---

## Persona or Identity Language

- **Id**: skill-persona-identity-language
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Generated text that assigns the agent a role, occupation, career history, length of tenure, or claimed expertise level, or asks it to imagine or pretend to be someone, in place of stating criteria.
- **Message**: This text assigns an identity instead of stating criteria; personas cost accuracy on the discriminative work — judging, classifying, verifying — that most skills perform.
- **Fix Action**: Convert the implied competence into the explicit decision scope, criteria source, and success condition it stands for, per the Task-Criteria Mandate pattern.
- **Applies To**:
    - SKILL.md
    - references/*.md

---

## Numbered Principle Labels

- **Id**: skill-numbered-principle-labels
- **Severity**: warning
- **Type**: regex
- **Pattern**: `^-\s+\*\*P[1-4]`
- **Message**: This principle is rendered with a literal P-number label instead of a plain descriptive name.
- **Fix Action**: Replace the P-number prefix with a short bold descriptive name; use the principle categories only to choose order.
- **Applies To**:
    - SKILL.md

---

## SKILL.md Progressive Disclosure

- **Id**: skill-md-progressive-disclosure
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Generated SKILL.md body sections beyond Mandate, Principles, and Reference System Usage, or pattern, sharp-edge, validation, or interaction entries inlined into SKILL.md.
- **Message**: SKILL.md should contain only frontmatter, Mandate, Principles, and Reference System Usage — deeper content belongs in its dedicated reference file.
- **Fix Action**: Move the inlined content into the matching reference file and leave the standard Reference System Usage pointer in SKILL.md.
- **Applies To**:
    - SKILL.md

---

## Description Over Specification Cap

- **Id**: skill-description-over-cap
- **Severity**: error
- **Type**: schema
- **Pattern**: Frontmatter `description` value exceeding 1024 characters.
- **Message**: The Agent Skills specification caps `description` at 1024 characters; past the cap the skill fails to register and stops triggering.
- **Fix Action**: Cut the description to one clause naming what the skill does and one naming when to use it, moving procedural detail into SKILL.md or a reference file.
- **Applies To**:
    - SKILL.md

---

## Description Outside Discovery Band

- **Id**: skill-description-out-of-band
- **Severity**: warning
- **Type**: schema
- **Pattern**: Frontmatter `description` value shorter than 200 characters or longer than 500 characters.
- **Message**: Under 200 characters a description carries too few trigger cues; over 500 it pays index cost in every session without improving the trigger decision.
- **Fix Action**: Restate the description as one clause naming what the skill does and one naming when to use it, landing between 200 and 500 characters.
- **Applies To**:
    - SKILL.md

---

## Reference Field Values Out of Range

- **Id**: skill-reference-field-enums
- **Severity**: error
- **Type**: schema
- **Pattern**: A validations.md entry whose Severity is outside {error, warning} or whose Type is outside {regex, schema, semantic, syntax}; a sharp_edges.md entry whose Severity is outside {critical, high, medium, low}.
- **Message**: Validation Severity must be error or warning and Type one of regex/schema/semantic/syntax; sharp-edge Severity must be critical, high, medium, or low.
- **Fix Action**: Replace the value with the closest allowed one (e.g. a judgment-based `instruction` rule becomes `semantic`; a structural check becomes `schema`).
- **Applies To**:
    - *validations.md
    - *sharp_edges.md

---

## Interactions File Missing for Interactive Skill

- **Id**: skill-interactions-conditional
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Generated SKILL.md or references contain mid-task prompts, multi-turn confirmation, approval gates, or gated state transitions, but `references/interactions.md` is absent; or interactions.md is present for a skill with none of these.
- **Message**: interactions.md is required exactly when the skill shows human-in-the-loop behavior; an empty or fabricated one is scaffolding filler.
- **Fix Action**: Add `references/interactions.md` from `templates/interactions_template.md`, move embedded interaction logic into it, and add the "For Interacting" bullet to Reference System Usage — or remove the file when the skill has no interaction loop.
- **Applies To**:
    - SKILL.md
    - references/*.md

---

## Skill interactions.md Template Violation

- **Id**: skill-structure-interactions
- **Severity**: error
- **Type**: schema
- **Pattern**: interactions.md missing `## Interaction Rules`, `## Execution Flow`, or `## Handoff`; a phase block missing Objective, Agent Action, Human Gate/Intervention, Proceed When, or Pause When; Handoff missing The Completion State or Exception/Fallback Handoff.
- **Message**: interactions.md does not adhere to the template layout in `templates/interactions_template.md`.
- **Fix Action**: Add the missing section or field following `templates/interactions_template.md`.
- **Applies To**:
    - *interactions.md

---

## Fictional Runtime Tokens

- **Id**: skill-fictional-runtime-tokens
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `\[AWAIT_HUMAN\]`
    - `<state_context>`
    - `STOP_AND_PROMPT`
    - `GO_PROCEED`
    - `#\$\[`
- **Message**: This text uses runtime-machinery notation the agent runtime does not interpret.
- **Fix Action**: Rewrite with turn-ending waits, the platform's blocking question tool, and plain Proceed-When / Pause-When conditions.
- **Applies To**:
    - SKILL.md
    - references/interactions.md

---

## Negative-Polarity Instructions

- **Id**: skill-negative-polarity-instruction
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A generated instruction phrased as a prohibition rather than as the action to take and its trigger condition.
- **Message**: This instruction names what to skip rather than what to do; affirmative instructions route the agent toward the correct action.
- **Fix Action**: Rewrite the instruction to name the required action and its trigger condition, keeping the original constraint's scope.
- **Applies To**:
    - SKILL.md
    - references/*.md

---

## Frontmatter Is Valid YAML

- **Id**: skill-frontmatter-valid-yaml
- **Severity**: error
- **Type**: syntax
- **Pattern**:
    - First line of the file is anything other than exactly `---`, including a leading byte-order mark or whitespace
    - No closing `---` line after the frontmatter keys
    - A frontmatter line that is not a single `key: value` pair, such as a value continued onto a second line
    - A duplicate key
    - A tab anywhere in the frontmatter
    - An invisible character in the frontmatter: non-breaking space (U+00A0), zero-width space or joiner (U+200B–U+200D), word joiner (U+2060), or any other control or format character
    - An unquoted value containing `: ` or ` #`, or ending in `:`
    - An unquoted value starting with any of `` ` `` `"` `'` `[` `{` `>` `|` `*` `&` `!` `%` `@` `-` `?` `,` `#`
    - A double-quoted value with an unescaped inner `"`, or a single-quoted value with an undoubled inner `'`
- **Message**: The frontmatter is not valid YAML, so the skill fails to load or loses its name and description.
- **Fix Action**: Strip the invisible character or tab; rejoin the value onto one line; reword the value to remove the `: ` or ` #` or the leading indicator character — or, when the wording needs it, wrap the whole value in double quotes and escape inner `"` as `\"`.
- **Applies To**:
    - SKILL.md
