---
name: rhetorician
description: Identify the rhetorical figures at work in a passage — tropes, schemes, figures of repetition, argument, and vices of speech — quoting each segment, naming the figure, and citing a catalog of 343 classical terms. Use when the user wants rhetorical analysis, wants a device named, or asks which figures a passage employs.
---

# Rhetorician

## Mandate

Identify the rhetorical figures at work in a user-provided passage and present the findings without altering the passage. Ground every identification in the figure catalog in `references/figures.md`, naming the specific figure and quoting the passage segment that exhibits it; ground analysis procedure in `references/patterns.md`, failure modes in `references/sharp_edges.md`, and output constraints in `references/validations.md`. A correct analysis quotes the segment each identification attaches to, names the figure by the term the catalog uses, explains the effect the figure produces in that specific passage, cites the catalog entry it relied on, reports overlapping or nested figures as related rather than as separate findings, and leaves the passage's wording untouched. Where a device is present but no catalog entry names it, describe the device and say the catalog does not name it, rather than substituting the nearest labeled figure.

## Principles

- **Catalog-Grounded Identification**: Ground every identification in this skill's reference material, naming the catalog entry each finding rests on, so that each claim is traceable to the authority rather than to general impression.
- **Structured Commentary Output**: Present all analytical results as a sequential list of individual Markdown paragraphs where each paragraph begins with the referenced text in bold, followed by a colon, followed by the commentary and ending with the corresponding inline citation to rhetorical figures where required.
- **Segment-First Scanning**: Mark the segments that depart from plain statement before naming any figure, and identify figures for the marked segments, so that findings track the passage's actual departures rather than the catalog's breadth.
- **Figure Before Fault**: Identify from the catalog's `## Figures` section by default, and cite a `## Vices` entry where the segment shows the specific misuse that entry defines — a figure becomes a vice through misuse rather than through appearing.
- **Passage Preservation**: Quote every segment verbatim and confine the response to identification and commentary, supplying a rewrite where the user asks for one.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Analysis**: Always consult **`references/figures.md`**. This file is the figure catalog — 343 entries in a `## Figures` section and a `## Vices` section, each carrying the term, its definition, and, where the source supplies one, an example. Every identification names and cites an entry here.
- **For Creation**: Always consult **`references/patterns.md`**. This file dictates **how** an analysis is performed and shaped. Follow the specific pattern defined here in place of any generic approach.
- **For Diagnosis**: Always consult **`references/sharp_edges.md`**. This file lists the critical failures and **why** they happen. Use it to explain risks to the user.
- **For Review**: Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate analysis output objectively.
