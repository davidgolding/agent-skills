# Gazelem Layer Sharp Edges

This document details common failures, diagnosing symptoms, and mitigation strategies for compiling a structured knowledge layer from historical corpora.

## Boundary Fragmentation

- **Id**: boundary-fragmentation
- **Summary**: Splitting a logical document (e.g., a letter) across a chunk boundary, causing contextual meaning to be severed or date headers to be separated from body text.
- **Severity**: high
- **Situation**: An 8,000-token window cuts off in the middle of a letter's arguments, and the next window starts processing without the context of the sender or recipient.
- **Why**: Relying strictly on token counts for chunking instead of evaluating logical layout markers.
- **Solution**: Always scan the 1,000-token overlap region to determine if a document is continuing. Output a segment once its closing signature or a clear new date header confirms the boundary.
- **Symptoms**: Sender/recipient names mapped as "unknown". Short, incoherent document fragments in `document_registry.toon`.
- **Detection Pattern**: Registry entries with page ranges spanning 1 page or less containing incomplete sentences.

---

## Cache Overwriting

- **Id**: cache-overwriting
- **Summary**: Accidentally overwriting or truncating existing `.toon` files in the destination folder instead of appending new segments.
- **Severity**: critical
- **Situation**: The agent processes a new batch of documents and overwrites `document_registry.toon` with only the new items, erasing the previous history of processed texts.
- **Why**: Using write modes that overwrite (`w` or `write`) instead of append modes (`a` or `append`) during file system writes.
- **Solution**: Enforce append-only modes in all output generation steps. Read existing destination files or verify file existence before writing.
- **Symptoms**: Drastic reduction in the line count or file size of output files in the destination folder. Loss of previously compiled search indices.
- **Detection Pattern**: File creation tool calls with `Overwrite: true` directed at the destination `.toon` files.

---

## Entity Identity Dispersal

- **Id**: entity-identity-dispersal
- **Summary**: Creating multiple separate entity nodes for the same person or concept due to variations in names or titles.
- **Severity**: high
- **Situation**: A letterbook contains references to "Brigham Young", "President Young", and "B. Young". They are extracted as three distinct people.
- **Why**: Extracting named entities literally without performing coreference resolution or entity normalization.
- **Solution**: Perform co-reference resolution and check names against the existing `relationship_graph.toon` registry. Normalize names to their full standard historical form when known.
- **Symptoms**: Knowledge graph queries returning fragmented, disconnected subgraphs. Inflated entity counts in TOON output blocks.
- **Detection Pattern**: Entity lists containing highly similar names or titles in the same TOON segment block.

---

## Provenance Loss

- **Id**: provenance-loss
- **Summary**: Failing to compile or carry the hierarchical metadata trail from the source document to the output registries.
- **Severity**: medium
- **Situation**: A segment is successfully extracted, but its location within the archive (Collection name, Box number, Folder name) is omitted.
- **Why**: Treating the source corpus as flat text and ignoring folder structure or header metadata during parsing.
- **Solution**: Extract collection hierarchy tags from the file paths and document headers first. Require a non-empty `provenance` metadata field in all generated segment entries.
- **Symptoms**: Search queries returning matching passages but no way to trace them back to physical archives.
- **Detection Pattern**: `provenance` field set to empty string or missing entirely in `document_registry.toon`.

---

## Ungrounded Assertion (Hallucination)

- **Id**: ungrounded-assertion
- **Summary**: Extracting claims, facts, or doctrinal statements that are not explicitly stated or logically implied in the text.
- **Severity**: critical
- **Situation**: An entry about sealing practices is parsed, and the agent extracts the claim: "Joseph Smith introduced plural marriage in 1843", but the letter only mentions sealing authority generally.
- **Why**: Allowing the language model's pre-trained weights to supplement historical details not present in the active text segment.
- **Solution**: Keep knowledge extraction strictly grounded in the document context. Trace every introduced historical context, date, or name back to the segment's text before including it.
- **Symptoms**: Discrepancy between the content of `semantic_cache.toon` and the corresponding source page.
- **Detection Pattern**: Assertions referencing entities or dates not mentioned in the source segment.

---

## Semantic Cache Bloat

- **Id**: semantic-cache-bloat
- **Summary**: Storing raw text claims, summaries, or paragraphs inside `semantic_cache.toon` instead of vector-only floats.
- **Severity**: high
- **Situation**: The semantic cache file contains full-text strings of claims and descriptions, leading to rapid storage expansion and context window saturation.
- **Why**: Failing to split raw text metadata (stored in `document_registry.toon`) from pure mathematical embeddings (stored in `semantic_cache.toon`).
- **Solution**: Enforce that `semantic_cache.toon` contains strictly float array vector declarations mapped to their `segment_id`. Map all natural-language claims and summaries to `document_registry.toon` instead.
- **Symptoms**: Unusually large `semantic_cache.toon` file sizes containing natural language strings.
- **Detection Pattern**: Regex matches matching alphabetic letters (e.g. `[a-zA-Z]{4,}`) inside lines that should contain only segment ID and float lists in `semantic_cache.toon`.

---

## Sparse Graph Extraction

- **Id**: sparse-graph-extraction
- **Summary**: Extracting too few relationships or failing to link relationship tuples to their source segment IDs, producing an empty or untraceable knowledge graph.
- **Severity**: high
- **Situation**: The agent processes a page packed with interactions but only extracts one relationship (e.g. sender-recipient), or writes triples without appending the `segment_id`, preventing search agents from traversing the graph to locate source documents.
- **Why**: Lazy extraction logic (stopping after the most obvious connection is mapped) and ignoring segment lineage links in tuples.
- **Solution**: Enforce the 4-element tuple pattern: `[subject, predicate, object, segment_id]`. Enforce exhaustive relational scans targeting connections between every named entity, topic, and event in the segment.
- **Symptoms**: Relationship graph file has very few lines compared to the document registry. Search queries traversing the graph fail to return any matching segment IDs.
- **Detection Pattern**: Lines in `relationship_graph.toon` containing only 3 elements (e.g. `[3]:`) instead of 4 elements (`[4]:`).

---
