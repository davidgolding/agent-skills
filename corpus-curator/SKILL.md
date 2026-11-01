---
name: corpus-curator
description: Convert PDF, DOCX, DOC, ODT, RTF, EPUB, HTML, TXT, MD, or page-image documents into source files that conform to the Markdown Source Corpus Specification, then validate and audit them. Use when the user wants to add, ingest, transcribe, or curate a document or a folder of documents into a Markdown source corpus.
---

# Corpus Curator

## Mandate

Convert one input (a single document or a folder of documents) into spec-compliant source files in one Markdown Source Corpus per invocation, after collecting any missing input path or corpus path from the user. For each source, decide its kind (born-digital text, existing transcription, or scan), its mode, key, collection, and frontmatter, which characters come from deterministic extraction and which from reading page images, which readings are uncertain, and whether a key collision is a distinct source or a duplicate. Ground every judgment in `references/patterns.md`, `references/sharp_edges.md`, `references/validations.md`, and `references/interactions.md`, which encode the specification's D, N, F, B, M, E, and A rules. A correct run leaves every written file passing `scripts/validate_corpus.py` with zero errors and `scripts/fidelity_check.py` with zero unexplained differences, copies scan images into `Assets/`, leaves all changes uncommitted, and ends with a report that accounts for every input.

## Principles

- **Verbatim Fidelity**: Take every source character from the file's own text layer or, for image-only pages, from a careful reading of the image, and keep the source's spelling, punctuation, and typographic characters exactly, because exact-string search and citation verification fail silently on any drift.
- **Structure From the Source**: Add only the structure the source itself has (its lines or paragraphs, printed headings, pages, notes), since editorial structure misrepresents the witness and breaks line citations.
- **Marked Uncertainty**: Record every doubtful reading, gap, or inferred metadata value with the specification's marks or EDTF qualifiers, so readers can see where the text is the agent's judgment.
- **Deterministic Tools First**: Run the bundled scripts for extraction, validation, and fidelity diffing, and stop with install instructions when a required tool is missing, because a weaker fallback would void the fidelity guarantee.
- **Sequential, Bounded Context**: Process sources one at a time and read long extractions in ranges, so a large folder or a long book stays within working context.
- **Review Only the Uncertain**: Bring the user only the rows with uncertain fields or likely duplicates, and proceed without stopping when there are none, so large runs stay reviewable.
- **Audit Before Report**: Treat a run as finished only when the validator and the fidelity check are clean for every written file, fixing and re-running until they are.
- **Account for Every Input**: End with a verbose report of what was processed, skipped, inferred, corrected, and copied, so the user can trust the corpus without opening each file.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
- **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.
- **For Interacting:** Always consult **`references/interactions.md`**. This file governs human-in-the-loop checkpoints, approval gates, and handoffs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
