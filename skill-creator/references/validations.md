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
- **Fix Action**: Add a 'Reference System Usage' section to the SKILL.md file pointing to the four reference files as the source of truth for Creation, Diagnosis, Review, and Brainstorming
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
    - ^(?s)(?!.*##\s+Identity\b).*$
    - ^(?s)(?!.*##\s+Principles\b).*$
    - ^(?s)(?!.*##\s+Reference\s+System\s+Usage\b).*$
    - ^(?s)(?!.*ground\s+your\s+responses\s+in\s+the\s+provided\s+reference\s+files).*$
- **Message**: SKILL.md does not adhere to the strict template layout (frontmatter, level-1 title heading, or Level-2 headings: Identity, Principles, Reference System Usage verbatim)
- **Fix Action**: Reformat SKILL.md to include name and description frontmatter, a Level-1 title in Title Case, and the required Level-2 sections (Identity, Principles, and Reference System Usage verbatim)
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
