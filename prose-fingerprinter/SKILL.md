---
name: prose-fingerprinter
description: Analyze a passage of text to extract and synthesize its unique stylistic, prosodic, etymological, and thematic patterns into a cohesive prose fingerprint profile. Use when the user requests a stylistic analysis, voice profiling, or author signature extraction from a text passage.
---

# Prose Fingerprinter

## Mandate

Extract one prose fingerprint per invocation from a user-supplied passage, profiling five dimensions: syntactic architecture, prosodic scansion, etymological register, presentation-mode mix, and thematic clustering. Ground every judgment in `references/patterns.md`, `references/sharp_edges.md`, `references/validations.md`, and `references/interactions.md`. A correct fingerprint reports each dimension with its measurement basis stated, pairs every quantitative finding with the stylistic function it performs, synthesizes the dimensions into a single consciousness-engine reading rather than a metrics list, and marks any figure estimated by inspection rather than counted exhaustively.

## Principles

- **Mechanics Alongside Meaning**: Deconstruct the text into its functional engineering — syntactic structures, scansion rhythm, presentation modes — and read that engineering alongside vocabulary and themes, so the fingerprint describes how the prose works rather than only what it says.
- **Measurement Basis Disclosure**: Analyze the passage by close inspection, and state for each reported figure whether it was counted exhaustively across the passage or estimated from a sample — naming the sample's size and location whenever a figure rests on one. Hold each count to what the passage on the page supports.
- **Consciousness-Engine Synthesis**: Translate the raw metrics into a cohesive description of the consciousness or worldview the prose style transmits, presenting that synthesis as the fingerprint's conclusion rather than leaving the dimensions as separate readings.
- **Structured Comparison**: Present the fingerprint metrics of multiple texts in the comparison table defined in `references/patterns.md`, one row per dimension and one column per text, so differences read at a glance.

## Reference System Usage

You must ground your response in the provided reference files, treating them as the source of truth for this domain, and resolve any conflict between a user's request and their guidance by explaining the reference guidance to the user:

- **For Creation [State 01]**: Always consult `references/patterns.md`. This file dictates *how* a fingerprint must be built, sampled, and laid out. Ignore generic approaches if a specific pattern exists here.
- **For Diagnosis [State 02]**: Always consult `references/sharp_edges.md`. This file indexes the critical failure modes and why they happen. Use it to map and explain risks during an analysis.
- **For Review [State 03]**: Always consult `references/validations.md`. This file contains the strict rules and constraints. Use it to verify the fingerprint objectively before presenting it.
- **For Interacting [State 04]**: Always consult `references/interactions.md`. This file governs passage intake, the sampling decision on oversized inputs, and the points where the user supplies more text.
