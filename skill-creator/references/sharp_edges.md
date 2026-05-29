# Sharp Edges

This document defines the sharp edges used by skill-creator.

---

## Context Flood

- **Id**: context-flood
- **Summary**: Flooding the agent's context window with large raw files, long database schemas, or verbose logs, causing it to lose tracking of instructions.
- **Severity**: critical
- **Situation**: The agent loads a 5,000-line CSV file or dumps a whole JSON API payload directly into the active prompt context, causing it to ignore system instructions.
- **Why**: LLM attention gets diluted when the context window is filled with raw, unformatted, or irrelevant data. It reduces instruction adherence and increases latency.
- **Solution**:
    - Use progressive loading: read file headers first, summarize schemas, or truncate logs.
    - Keep reference templates and scripts out of `SKILL.md` and load them lazily using tools only when required.
    - Utilize search tools (`grep_search`) to query specific patterns instead of reading whole directories.
- **Symptoms**:
    - Agent starts ignoring negative constraints.
    - Unusually long response times and higher token usage.
    - Output becomes repetitive or cuts off mid-sentence.
- **Detection Pattern**: Reading entire logs or dumping raw database structures.

---

## Trigger Dilution

**Id**: trigger-dilution
**Summary**: The skill description is too broad, leading to accidental triggering (false positives) or missing trigger prompts (false negatives).
**Severity**: critical
**Situation**: A skill for "git commit" has a description like "Use this when you want to write text". It gets triggered when the user wants to write a markdown document.
**Why**: The routing agent relies on specific keywords, commands, and scenarios in the description to match the user's prompt. Fuzzy descriptions confuse the router.
**Solution**:
    - Write a highly specific, keyword-dense frontmatter description.
    - Explicitly list commands (e.g., `git commit`) and target tasks (e.g., "create git commit").
    - Test the description against a trigger eval set containing near-miss negative prompts.
**Symptoms**:
    - Skill is activated for unrelated user requests.
    - Skill is not activated when the user specifically requests its function.
**Detection Pattern**: Description contains overly broad phrases like "helps with coding", "general purpose tool", or "assists the user".

---

## Silent Side-Effects

- **Id**: silent-side-effects
- **Summary**: Performing destructive file modifications or executing system commands without informing the user or getting explicit approval.
- **Severity**: critical
- **Situation**: A cleanup skill runs `git clean -fdx` or deletes a subdirectory in the background without telling the user first, causing them to lose uncommitted changes.
- **Why**: Automated tool execution without human-in-the-loop validation creates security risks and risks data loss.
- **Solution**:
    - Always outline the planned actions (which files will be modified, what commands will run) to the user in a short text summary.
    - Ask for explicit user approval before executing any command or making file modifications.
    - Use sandbox environments or dry-run flags when available.
- **Symptoms**:
    - Unexpected file modifications in the git tree.
    - Command execution logs appearing in the output without prior discussion.
    - User confusion about how a certain state was reached.
- **Detection Pattern**: Executing commands directly without a preceding output explaining the action.

---

## Absolute Path Leak

- **Id**: absolute-path-leak
- **Summary**: Hardcoding machine-specific absolute file paths inside instructions, scripts, or configurations.
- **Severity**: high
- **Situation**: An instruction says: "Read patterns from /Users/david/Development/agent-skills/skill-creator/references/patterns.md". When another user runs it, it fails because their username is not `david`.
- **Why**: Absolute paths depend on the local system architecture, directory hierarchy, and usernames. This breaks skill portability.
- **Solution**:
    - Always use workspace-relative paths (e.g., `skill-creator/references/patterns.md`).
    - Read active directory paths dynamically from environment variables or runtime context tools.
    - Never include user home directories (`/Users/...`, `/home/...`) in skill files.
- **Symptoms**:
    - "File not found" errors when the skill is run by another developer.
    - Path resolution errors in CI/CD pipelines.
- **Detection Pattern**: /Users/\w+|/home/\w+|/var/folders/

---

## Overfitted Evals

- **Id**: overfitted-evals
- **Summary**: Modifying prompt instructions specifically to pass a single failing test case, which breaks generality and causes regressions elsewhere.
- **Severity**: high
- **Situation**: The agent modifies a coding skill to handle a single syntax quirk of python 3.11, but in doing so, breaks compatibility for python 3.10 and JS files.
- **Why**: Prompts optimized for a narrow, specific test case can lose their general reasoning capability or create strict rules that clash with other scenarios.
- **Solution**:
    - Before committing prompt changes, run the full validation/test suite.
    - Look for convergent behaviors: if multiple tests fail in the same way, fix the underlying pattern; if only one fails, check if it's an edge case that can be handled dynamically.
    - Keep test cases diverse and maintain a baseline metric.
- **Symptoms**:
    - Passing one test causes another previously green test to turn red.
    - Prompt instructions become bloated with hyper-specific edge case rules.
- **Detection Pattern**: Prompt contains highly specific rules for single files or single lines of code.

---

## Missing Boundaries

- **Id**: missing-boundaries
- **Summary**: Failing to specify non-goals or boundary exclusions, causing the skill to handle out-of-scope tasks.
- **Severity**: medium
- **Situation**: A "code review" skill attempts to fix the lint errors and refactor the code themselves instead of just listing the findings.
- **Why**: Without strict boundary constraints, agents tend to over-execute, performing secondary tasks that drift away from the core goal.
- **Solution**:
    - Explicitly define "Non-Goals" or "Exclusions" in the plan or instructions.
    - State what the skill does *not* do (e.g., "This skill only reviews and reports; it does not modify files").
- **Symptoms**:
    - Agent takes many turns trying to solve a problem that should be handled by a different skill.
    - Scope creep during execution.
- **Detection Pattern**: No exclusions or non-goals listed in the skill's README or planning docs.

---

## No-Verification Claims

- **Id**: no-verification-claims
- **Summary**: Claiming that a component, route, schema, or configuration is missing or behaves in a certain way without checking the codebase first.
- **Severity**: high
- **Situation**: The agent tells the user "You don't have python-dotenv installed, so we must add it to requirements.txt", without checking the file first (which already had it).
- **Why**: Making assumptions instead of executing verification tools leads to redundant changes, bugs, and developer frustration.
- **Solution**:
    - Verify every assumption about the project configuration or code by using `view_file` or `grep_search`.
    - If a file or configuration is unverified, label it clearly as an "unverified assumption" in plans.
- **Symptoms**:
    - Redundant packages added to dependencies.
    - Duplicate functions or configurations created.
    - Failed builds due to conflicting setups.
- **Detection Pattern**: Stating file properties or package existence without matching tool calls in the history.

---

## Question Stacking

- **Id**: question-stacking
- **Summary**: Asking multiple questions or sub-questions in a single turn, diluting user responses.
- **Severity**: medium
- **Situation**: The agent asks the user three separate clarification questions in the same message, causing the user to give incomplete or shallow answers.
- **Why**: Eliciting requirements works best with a highly structured, single-focus dialogue. Stacking questions raises cognitive load.
- **Solution**:
    - Ask exactly one question per turn.
    - Pick the single most critical unknown, present clear options, and wait for the response.
- **Symptoms**:
    - User only answers one of the questions.
    - User ignores options and gives a short response.
- **Detection Pattern**: Multiple question marks in the agent response.

---

## Granularity Leakage

- **Id**: granularity-leakage
- **Summary**: Introducing code-level implementation specifics (file paths, database schemas, classes) during the brainstorming or requirements phase.
- **Severity**: medium
- **Situation**: The agent documents specific table names or database column names in the scoping synthesis or requirements document before the product shape has been confirmed.
- **Why**: Forces the user to evaluate architecture rather than behavior, and makes the requirements fragile and over-detailed.
- **Solution**:
    - Focus on mechanism and product shape.
    - Defer code structure, column names, and APIs to the planning phase.
- **Symptoms**: Scoping synthesis contains paths, database tables, or method names.
- **Detection Pattern**: File paths, class names, schema/column patterns in requirements or synthesis.

---

## Announce-Mode on Deep Scope

- **Id**: announce-mode-deep-scope
- **Summary**: Proceeding straight to writing the requirements document on Standard or Deep tiers without obtaining explicit confirmation of the scope.
- **Severity**: high
- **Situation**: The agent generates a scoping synthesis for a Deep-tier feature, says "no open decisions", and writes the requirements document in the same turn without allowing the user to redirect or confirm.
- **Why**: Standard and Deep tiers have significant ambiguity. Proceeding without a confirmation checkpoint leads to misaligned requirements that are expensive to revise.
- **Solution**: Always use Path B (with a confirmation gate) for Standard and Deep tiers, even if no questions were asked during dialogue.
- **Symptoms**: Requirements document written immediately without user feedback on the synthesis summary.
- **Detection Pattern**: Skipping confirmation and writing the document on high-complexity scopes.

---

## Fuzzy Open Probes

- **Id**: fuzzy-open-probes
- **Summary**: Using overly vague or conversational open-ended questions that fail to elicit concrete product constraints.
- **Severity**: medium
- **Situation**: The agent asks "What's your take on this?" or "What are you thinking?" instead of anchoring the prompt on observable metrics or workarounds.
- **Why**: Vague prompts yield vague answers, wasting the turn and failing to uncover real user pain points.
- **Solution**:
    - Anchor open-ended questions in concrete scenarios (e.g., "What do they do today when this fails?").
    - Avoid AI-slop warmth wrappers and framings that imply a short answer.
- **Symptoms**: User gives a one-liner like "looks good" or "not sure" without adding new requirements.
- **Detection Pattern**: Generics like "how does that sound", "what do you think", "any thoughts".

---

## Temporary File Pollution

- **Id**: temporary-file-pollution
- **Summary**: Leaving intermediate requirements or design files behind in the workspace, or creating new directories for temporary files.
- **Severity**: medium
- **Situation**: The agent performs a brainstorming session, writes the requirements to a temporary file, compiles the skill, but terminates without deleting the temporary file, or creates a nested subdirectory like `docs/brainstorms` that is left behind.
- **Why**: Pollutes the user's repository with untracked git files and nested directories, violating the constraint that brainstorming should not persist requirements docs.
- **Solution**:
    - Save the temporary requirements document directly in the workspace root (e.g. `temp-requirements.md`), avoiding directory creation.
    - Explicitly delete the temporary file immediately after drafting/writing the skill or if the session is cancelled.
- **Symptoms**: Untracked `temp-requirements.md` or new folders remaining in the workspace git status.
- **Detection Pattern**: Writing temporary files to nested folders or failing to call delete/remove on temporary files before exiting.
