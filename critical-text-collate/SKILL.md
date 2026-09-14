---
name: critical-text-collate
description: Parse, analyze, and collate transcription witnesses (.docx) using text-critical methodology. Use when users want to align a corpus of transcription witnesses, perform variant analysis, and generate a multi-way collation Excel spreadsheet (.xlsx) aligning witnesses along columns and shared nodes along rows.
---

# Critical Text Collate

## Mandate

Parse a corpus of `.docx` transcription witnesses, analyze their variants, perform hierarchical multi-way collation, and emit a formatted `.xlsx` aligning witnesses along columns and shared nodes along rows. Ground every parsing, alignment, and formatting decision in `references/patterns.md`, `references/sharp_edges.md`, `references/validations.md`, and `references/interactions.md`. A correct collation treats all witnesses as peers with no base text, preserves run-level `.docx` formatting in the output cells, joins multi-word nodes with `•` (U+2022), leaves a cell blank where a witness has no node for that row, scrubs `//` and `/* */` comments from collation text, and numbers sentence groups in a `segment` integer column.

## Principles

- **Preserve Formatting**: Carry native `.docx` run formatting — strikethrough, bold, italics — into the output Excel cells at the run/character level.
- **Scrub Comments**: Treat multi-line `/* ... */` and inline `// ...` comments as metadata, stripping them from collation text and routing Word footnotes to their segment as separate annotations.
- **Hierarchical Alignment**: Split the text into sentences automatically, align the sentence segments first, then perform detailed word-by-word alignment within those groups.
- **Peer Witnesses**: Collate through multi-way alignment that treats every witness as a peer, letting the alignment itself determine row layout.
- **Space Bullet Join**: Join multiple words or entities inside a single node with the bullet character `•` (U+2022), so every collation cell carries bullets in place of space characters.
- **Blank Gaps**: Leave the Excel cell completely blank when a witness has no node for that alignment row.
- **Text-Critical Variance Insight**: Analyze variance (additive, correctional, lexical, morphological, ordinal, orthographical, punctuational, semantical, subtractive, syntactical) to guide alignment decisions and match nodes.
- **Durable Reference Mapping**: Maintain segment numbering in a dedicated `segment` integer column.

## Reference System Usage

You must ground your response in the provided reference files, treating them as the absolute source of truth for this domain:

- **For Creation [State 01]**: Always consult `references/patterns.md`. This file dictates the patterns for parsing transcription sources and aligning them into a collation. Ignore generic boilerplate choices if a specific pattern exists here.
- **For Diagnosis [State 02]**: Always consult `references/sharp_edges.md`. This file indexes the critical failure modes of alignment, parsing, and spreadsheet generation. Use it to map risks during execution.
- **For Review [State 03]**: Always consult `references/validations.md`. This file contains the strict formatting constraints and validations for collation outputs. Use it to force a rigorous chain-of-verification loop before emitting state output.
- **For Interacting [State 04]**: Always consult `references/interactions.md`. This file governs requirement gathering, the plan-approval gate, and the collation run's phase progression.
