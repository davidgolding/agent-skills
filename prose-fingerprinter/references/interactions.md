# Prose Fingerprinter Interactions

This document defines the interaction flow used by prose-fingerprinter.

## Interaction Rules

1. **The Turn-Taking Paradigm**: End the turn and wait for the user's reply whenever the passage is too short to fingerprint or an oversized input needs a sampling decision. Route the sampling choice through the platform's blocking question tool (e.g. `AskUserQuestion`) so the options surface as a first-class prompt rather than plain text.
2. **Validation Gatekeeping**: Begin the analysis once the passage clears the 150-word minimum and its sampling basis is settled, and present the fingerprint once each dimension carries its measurement basis and each metric its stylistic function.
3. **State Retention**: Carry the sample's size and location forward in the conversation and restate them in the report, so every figure in the fingerprint remains traceable to the text it was drawn from.

## Execution Flow

### Phase 01: Intake

- **Objective**: Establish that the passage supports a fingerprint, and settle what text the analysis will rest on.
- **Agent Action**: Measure the passage's length; where it runs past roughly 3,000 words, present the sampling options from the Representative Sampling pattern — a single 1,000-to-2,000-word span across the text's range, or several chunks averaged together.
- **Human Gate/Intervention**: The user supplies a longer passage, or chooses the sampling approach for an oversized one.
- **Proceed When**: The passage runs at least 150 words and its sampling basis is settled.
- **Pause When**: The passage falls under 150 words — ask for a larger sample, ideally 300 to 1,000 words; or it runs past roughly 3,000 words — ask which sampling approach to take.

### Phase 02: Analyze

- **Objective**: Measure the five dimensions from the established text.
- **Agent Action**: Profile syntactic architecture, prosodic scansion, etymological register, presentation-mode mix, and thematic clustering by close inspection, recording for each figure whether it was counted exhaustively or estimated from a sample, and checking each against the fabricated-scansion and invented-etymology sharp edges before carrying it forward.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: All five dimensions carry a measurement and a disclosed basis, or a stated reason the passage cannot support one.
- **Pause When**: The passage turns out to be a mix of several distinct voices — ask the user which voice to fingerprint, or whether to profile them separately for comparison.

### Phase 03: Synthesize and Report

- **Objective**: Deliver the fingerprint in the skill's report shape.
- **Agent Action**: Pair each metric with the stylistic function it performs, lay the dimensions out per the Fingerprint Report Shape pattern — or the Comparison Table Construction pattern for multiple texts — and close with the consciousness-engine synthesis, which reads the five dimensions together as one worldview.
- **Human Gate/Intervention**: The user accepts the fingerprint, asks for a dimension in more depth, or supplies a second text for comparison.
- **Proceed When**: Every dimension is reported with its basis, every metric carries its function, and the synthesis is present.
- **Pause When**: The user supplies an additional text — return to Phase 01 for that text, then present both through the comparison table.

## Handoff

- **The Completion State**: All five dimensions are reported with their measurement bases disclosed, every quantitative finding is paired with its stylistic function, and the consciousness-engine synthesis closes the fingerprint.
- **Exception/Fallback Handoff**: When a dimension is not measurable from the passage supplied, report the gap and what further text would close it, rather than estimating past it.
