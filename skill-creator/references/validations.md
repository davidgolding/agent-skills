# Skill Creator - Validations

## Absolute Path Detection

### **Id**
skill-absolute-path
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b/Users/[a-zA-Z0-9_\-\.]+
  - \b/home/[a-zA-Z0-9_\-\.]+
  - \b/var/folders/[a-zA-Z0-9_\-\.]+
### **Message**
Absolute path detected - breaks portability across environments and machines
### **Fix Action**
Replace absolute paths with relative or workspace-relative paths (e.g., use 'skill-creator/references/patterns.md' instead of '/Users/name/repo/skill-creator/references/patterns.md')
### **Applies To**
  - *.md
  - *.json
  - *.py
  - *.sh


## Assertive Trigger Missing

### **Id**
skill-assertive-trigger-missing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)description:\s*(?!.*(?:use\s+when|triggers\s+when|triggers\s+on|activate\s+when|trigger\s+on)).*$
### **Message**
Skill description is missing assertive triggering constraints (e.g., 'Use when...')
### **Fix Action**
Add explicit trigger rules and keywords to the frontmatter description to guide the agent router (e.g., 'Use when the user says X or wants to perform Y')
### **Applies To**
  - SKILL.md
  - *.md


## Reference System Mapping Missing

### **Id**
skill-reference-system-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*patterns\.md)(?!.*sharp_edges\.md)(?!.*validations\.md)(?!.*interactions\.md).*$
### **Message**
Skill does not define or link to the reference system usage files (patterns.md, sharp_edges.md, validations.md, interactions.md)
### **Fix Action**
Add a 'Reference System Usage' section to the SKILL.md file pointing to the four reference files as the source of truth for Creation, Diagnosis, Review, and Brainstorming
### **Applies To**
  - SKILL.md


## Placeholder Usage

### **Id**
skill-placeholder-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?:TODO|FIXME|XXX)\b
  - <[^>]*insert[^>]*>
  - \b[a-zA-Z0-9_\-]*placeholder[a-zA-Z0-9_\-]*\b
### **Message**
Unresolved placeholder, TODO, or FIXME comment found in skill documentation
### **Fix Action**
Replace the placeholder with concrete, production-ready instructions or patterns
### **Applies To**
  - *.md
  - *.json
  - *.py
  - *.sh


## Silent Command Instructions

### **Id**
skill-silent-command-instructions
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?i)(?:run|execute|apply|modify)\s+(?:without\s+asking|directly|silently|automatically)\b
  - \b(?i)do\s+not\s+(?:ask|prompt|confirm)\b
### **Message**
Instructions advocate executing commands or modifications without user confirmation
### **Fix Action**
Ensure instructions state that the agent must explain actions and obtain user consent before running mutating commands or modifying files
### **Applies To**
  - SKILL.md
  - *.md


## Hardcoded Dev Domains

### **Id**
skill-hardcoded-domains
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?:localhost|127\.0\.0\.1|0\.0\.0\.0)(?::\d+)?\b
  - \b[a-zA-Z0-9\-]+\.local\b
### **Message**
Hardcoded local server URLs or development domains found
### **Fix Action**
Parameterize server addresses or use environment-relative configurations instead of hardcoded dev domains
### **Applies To**
  - *.json
  - *.py
  - *.sh
  - *.md


## Question Stacking Detection

### **Id**
skill-question-stacking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)\b(?:ask|pose)\b.*\b(?:multiple|several|many|two|three)\b.*\bquestions?\b
  - (?i)\bstack\b.*\bquestions?\b
### **Message**
Prompt contains instructions advocating question stacking (asking multiple questions at once)
### **Fix Action**
Ensure the prompt instructs the agent to ask exactly one question at a time
### **Applies To**
  - SKILL.md
  - *.md


## Granularity Leakage Detection

### **Id**
skill-granularity-leakage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)\b(?:database\s+schema|table\s+name|column\s+name|class\s+name|file\s+path|json\s+key)\b.*\bin\b.*\bbrainstorm\b
### **Message**
Brainstorming instructions should not mention code-level architecture details
### **Fix Action**
Defer code architecture and implementation details to the planning phase
### **Applies To**
  - SKILL.md
  - *.md


## Temporary File Directory Violation

### **Id**
skill-temp-dir-violation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)\b(?:write|save|create|put)\b.*\btemporary\b.*\b(?:inside|in|under|to)\b.*\b(?:sub-?directories|folders|nested|docs|brainstorms)\b
  - \bdocs/brainstorms/temp-requirements\.md\b
### **Message**
Temporary brainstorming files should not be written to nested subdirectories or create new directories; they must be stored in the workspace root
### **Fix Action**
Write temporary requirements or intermediate files directly to temp-requirements.md in the workspace root, and delete them immediately after use
### **Applies To**
  - SKILL.md
  - *.md
