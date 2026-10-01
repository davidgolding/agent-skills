# Expert Researcher Interactions

This document defines the interaction flow used by expert-researcher.

## Interaction Rules

1. **Explicit Entry**: Enter research mode only when the user invokes expert-researcher by name. Confirm entry in one line together with the first plan statement.
2. **One Question Per Turn**: When the agent needs a decision from the user, such as resolving an ambiguous prompt, ask a single question through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini or Pi). Fall back to numbered options in chat only when no blocking tool exists.
3. **What Counts as Approval**: At the plan gate, an explicit go-ahead ("go", "approved", "looks good") approves the plan as presented. Edits to lines, disciplines, depth or audience level revise it; integrate them, re-present the revised plan, and wait again. A reply that changes the topic is a new prompt and restarts at Phase 01.
4. **Persistent Mode**: Keep research mode active across turns until the user asks to stop, exit or leave it, or plainly asks for normal assistance. Confirm the exit in one line.

## Execution Flow

### Phase 01: Decompose and Plan

- **Objective**: Turn the prompt into a set of lines of inquiry with a depth tier and an audience level.
- **Agent Action**: Apply Faceted Query Decomposition and Discipline Corridor Mapping, choose the tier with Depth Scaling, honor any budget the user stated, infer the audience level, and determine the source base per Source Precedence, including whether live web tools are available.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Every line of inquiry has a precise question and a named discipline, and the tier and audience level are chosen.
- **Pause When**: The prompt is too ambiguous to decompose into a single coherent query; ask one clarifying question through the blocking question tool and end the turn.

### Phase 02: Plan Gate

- **Objective**: Make the research plan legible before expensive gathering begins.
- **Agent Action**: For shallow or medium prompts that are unambiguous, state the plan in one or two lines (lines of inquiry, tier) and continue in the same turn. For deep or ambiguous prompts, present the full plan: lines of inquiry with their disciplines, depth tier, inferred audience level, and source base. Then end the turn.
- **Human Gate/Intervention**: For deep or ambiguous prompts, the user approves the plan or edits lines, disciplines, depth or audience level.
- **Proceed When**: The prompt is shallow or medium and unambiguous, or the user has approved the presented plan.
- **Pause When**: The prompt is deep or ambiguous and the plan has been presented or revised without approval yet.

### Phase 03: Gather

- **Objective**: Snowball each line of inquiry until it saturates or reaches its budget.
- **Agent Action**: Run Fan-Out with Sequential Fallback. Each line follows Snowball Hop, records yields in the Novelty-Perplexity Ledger, and returns a Line Brief. When live tools are unavailable or fail, continue from model knowledge and flag the fallback for the opening of the answer.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Every line has returned a brief marked saturated or stopped at budget.
- **Pause When**: The user interrupts with a redirect; return to Phase 01 with the redirect integrated.

### Phase 04: Merge and Present

- **Objective**: Deliver the findings at the right level, in the right format, with evidence and certainty intact.
- **Agent Action**: Apply Cross-Line Merge, then compose the answer in the user's format, or by default with Pedagogical Structure Selection in rich markdown. Apply Inline Citation and Certainty Marking, open with the fallback statement when it applies, and close with the Coverage Note. Check the answer against `references/validations.md` before sending it.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The answer passes the validations.
- **Pause When**: The answer is delivered; end the turn and wait for the next prompt.

### Phase 05: Continue or Exit

- **Objective**: Handle the next prompt within research mode, or leave it.
- **Agent Action**: Treat a follow-up as a new research query and return to Phase 01. It may build on the session's briefs when it extends the same topic. Treat an operational prompt per Research Mode Persistence. When the user asks to leave, confirm the exit in one line.
- **Human Gate/Intervention**: The user decides whether to continue researching or leave research mode.
- **Proceed When**: A new prompt arrives (return to Phase 01) or the user asks to exit (complete).
- **Pause When**: Waiting for the user's next prompt.

## Handoff

- **The Completion State**: The user has received a validated answer for each prompt in the session, and has either left research mode with a one-line confirmation or ended the session.
- **Exception/Fallback Handoff**: When gathering cannot produce findings, for example because tools fail and model knowledge is thin, deliver what was found with its limitations stated in the coverage note. Name the specific sources or corpus that would let a rerun succeed, and stay in research mode for the user's next prompt.
