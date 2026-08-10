# Lit Review Compiler Interactions

This document defines the interaction flow used by lit-review-compiler.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn whenever the scoping round needs the user's input, and let the conversation's natural back-and-forth carry the wait. Route the scoping questions through the platform's blocking question tool (e.g. `AskUserQuestion`) so they surface as a first-class prompt instead of plain text.
2. **Specificity Gate**: Advance from scoping to search only once a broad input's boundaries are known — either the user answered the scoping round, or the input was classified as precise and its inferred boundaries are ready to state in the report opening.
3. **State Retention**: Carry the classification, scope boundaries, verification tiers, and drafted entries forward in the conversation itself — not in an internal registry the runtime tracks on its own.

## Execution Flow

### Phase 01: Classify & Scope

- **Objective**: Classify the input's specificity and establish the scope boundaries the rest of the run depends on.
- **Agent Action**: Apply Specificity-Calibrated Scoping. For broad topics, fields, or disciplines, ask the user for time range, sub-fields/theoretical lenses, language, and exclusions. For precise, already-bounded research questions, infer the boundaries directly and prepare them for the report's opening statement.
- **Human Gate/Intervention**: For broad inputs, the user answers the scoping questions.
- **Proceed When**: The input was classified as precise, or the user has answered the scoping questions.
- **Pause When**: The input was classified as broad and the scoping questions have just been asked — end the turn and wait for the user's answers before searching.

### Phase 02: Discovery & Verification

- **Objective**: Populate the domain's foundational-through-frontier literature and mechanically confirm every candidate before it can be cited.
- **Agent Action**: Run Four-Part Citation Chaining (backward and forward) for every thematic cluster; run `scripts/verify_citation.py` against each candidate's title/author/year and record its tier; draft each entry's annotation from what was actually retrieved, per Retrieval-Grounded Annotation.
- **Human Gate/Intervention**: None; this phase runs autonomously once scope is established.
- **Proceed When**: Phase 01's scope boundaries are set.
- **Pause When**: A tier-1/tier-2 verification call reports a transient error rather than a clean no-match (per the `api-unavailable-mid-run` sharp edge) — retry that source once before finalizing its tier; this is an internal retry, not a user-facing pause.

### Phase 03: Report Assembly

- **Objective**: Assemble the single narrative deliverable per the Oxford-Bibliographies Report Shape.
- **Agent Action**: Write the scope statement near the opening; organize thematically with framing paragraphs; order entries foundational-to-frontier within each subsection; attach a visible caveat to every Tier-3 entry; keep any internal matrix out of the delivered report.
- **Human Gate/Intervention**: None.
- **Proceed When**: Every candidate citation in the draft has a recorded verification tier.
- **Pause When**: N/A — this phase completes once Phase 02's verification records are complete.

## Handoff

- **The Completion State**: The report states its scope near the opening, every cited source carries a known verification tier with Tier-3 entries visibly caveated, no internal matrix appears in the delivered text, and the report's framing language stays scoped to what was actually retrieved.
- **Exception/Fallback Handoff**: If a source's verification tier is still ambiguous after one retry of a transient API error, present that source to the user directly — stating what was found and what failed to confirm — rather than guessing its tier or silently dropping it.
