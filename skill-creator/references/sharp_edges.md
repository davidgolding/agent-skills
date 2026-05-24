# Skill Creator - Sharp Edges

## Context Flood

### **Id**
context-flood
### **Summary**
Flooding the agent's context window with large raw files, long database schemas, or verbose logs, causing it to lose tracking of instructions.
### **Severity**
critical
### **Situation**
  The agent loads a 5,000-line CSV file or dumps a whole JSON API payload directly into the active prompt context, causing it to ignore system instructions.
### **Why**
  LLM attention gets diluted when the context window is filled with raw, unformatted, or irrelevant data. It reduces instruction adherence and increases latency.
### **Solution**
  - Use progressive loading: read file headers first, summarize schemas, or truncate logs.
  - Keep reference templates and scripts out of `SKILL.md` and load them lazily using tools only when required.
  - Utilize search tools (`grep_search`) to query specific patterns instead of reading whole directories.
### **Symptoms**
  - Agent starts ignoring negative constraints.
  - Unusually long response times and higher token usage.
  - Output becomes repetitive or cuts off mid-sentence.
### **Detection Pattern**
Reading entire logs or dumping raw database structures.


## Trigger Dilution

### **Id**
trigger-dilution
### **Summary**
The skill description is too broad, leading to accidental triggering (false positives) or missing trigger prompts (false negatives).
### **Severity**
critical
### **Situation**
  A skill for "git commit" has a description like "Use this when you want to write text". It gets triggered when the user wants to write a markdown document.
### **Why**
  The routing agent relies on specific keywords, commands, and scenarios in the description to match the user's prompt. Fuzzy descriptions confuse the router.
### **Solution**
  - Write a highly specific, keyword-dense frontmatter description.
  - Explicitly list commands (e.g., `git commit`) and target tasks (e.g., "create git commit").
  - Test the description against a trigger eval set containing near-miss negative prompts.
### **Symptoms**
  - Skill is activated for unrelated user requests.
  - Skill is not activated when the user specifically requests its function.
### **Detection Pattern**
Description contains overly broad phrases like "helps with coding", "general purpose tool", or "assists the user".


## Silent Side-Effects

### **Id**
silent-side-effects
### **Summary**
Performing destructive file modifications or executing system commands without informing the user or getting explicit approval.
### **Severity**
critical
### **Situation**
  A cleanup skill runs `git clean -fdx` or deletes a subdirectory in the background without telling the user first, causing them to lose uncommitted changes.
### **Why**
  Automated tool execution without human-in-the-loop validation creates security risks and risks data loss.
### **Solution**
  - Always outline the planned actions (which files will be modified, what commands will run) to the user in a short text summary.
  - Ask for explicit user approval before executing any command or making file modifications.
  - Use sandbox environments or dry-run flags when available.
### **Symptoms**
  - Unexpected file modifications in the git tree.
  - Command execution logs appearing in the output without prior discussion.
  - User confusion about how a certain state was reached.
### **Detection Pattern**
Executing commands directly without a preceding output explaining the action.


## Absolute Path Leak

### **Id**
absolute-path-leak
### **Summary**
Hardcoding machine-specific absolute file paths inside instructions, scripts, or configurations.
### **Severity**
high
### **Situation**
  An instruction says: "Read patterns from /Users/david/Development/agent-skills/skill-creator/references/patterns.md". When another user runs it, it fails because their username is not `david`.
### **Why**
  Absolute paths depend on the local system architecture, directory hierarchy, and usernames. This breaks skill portability.
### **Solution**
  - Always use workspace-relative paths (e.g., `skill-creator/references/patterns.md`).
  - Read active directory paths dynamically from environment variables or runtime context tools.
  - Never include user home directories (`/Users/...`, `/home/...`) in skill files.
### **Symptoms**
  - "File not found" errors when the skill is run by another developer.
  - Path resolution errors in CI/CD pipelines.
### **Detection Pattern**
/Users/\w+|/home/\w+|/var/folders/


## Overfitted Evals

### **Id**
overfitted-evals
### **Summary**
Modifying prompt instructions specifically to pass a single failing test case, which breaks generality and causes regressions elsewhere.
### **Severity**
high
### **Situation**
  The agent modifies a coding skill to handle a single syntax quirk of python 3.11, but in doing so, breaks compatibility for python 3.10 and JS files.
### **Why**
  Prompts optimized for a narrow, specific test case can lose their general reasoning capability or create strict rules that clash with other scenarios.
### **Solution**
  - Before committing prompt changes, run the full validation/test suite.
  - Look for convergent behaviors: if multiple tests fail in the same way, fix the underlying pattern; if only one fails, check if it's an edge case that can be handled dynamically.
  - Keep test cases diverse and maintain a baseline metric.
### **Symptoms**
  - Passing one test causes another previously green test to turn red.
  - Prompt instructions become bloated with hyper-specific edge case rules.
### **Detection Pattern**
Prompt contains highly specific rules for single files or single lines of code.


## Missing Boundaries

### **Id**
missing-boundaries
### **Summary**
Failing to specify non-goals or boundary exclusions, causing the skill to handle out-of-scope tasks.
### **Severity**
medium
### **Situation**
  A "code review" skill attempts to fix the lint errors and refactor the code themselves instead of just listing the findings.
### **Why**
  Without strict boundary constraints, agents tend to over-execute, performing secondary tasks that drift away from the core goal.
### **Solution**
  - Explicitly define "Non-Goals" or "Exclusions" in the plan or instructions.
  - State what the skill does *not* do (e.g., "This skill only reviews and reports; it does not modify files").
### **Symptoms**
  - Agent takes many turns trying to solve a problem that should be handled by a different skill.
  - Scope creep during execution.
### **Detection Pattern**
No exclusions or non-goals listed in the skill's README or planning docs.


## No-Verification Claims

### **Id**
no-verification-claims
### **Summary**
Claiming that a component, route, schema, or configuration is missing or behaves in a certain way without checking the codebase first.
### **Severity**
high
### **Situation**
  The agent tells the user "You don't have python-dotenv installed, so we must add it to requirements.txt", without checking the file first (which already had it).
### **Why**
  Making assumptions instead of executing verification tools leads to redundant changes, bugs, and developer frustration.
### **Solution**
  - Verify every assumption about the project configuration or code by using `view_file` or `grep_search`.
  - If a file or configuration is unverified, label it clearly as an "unverified assumption" in plans.
### **Symptoms**
  - Redundant packages added to dependencies.
  - Duplicate functions or configurations created.
  - Failed builds due to conflicting setups.
### **Detection Pattern**
Stating file properties or package existence without matching tool calls in the history.
