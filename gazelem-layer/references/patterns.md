# Gazelem Layer Patterns

This document details the patterns and protocols required to segment documents, extract metadata/knowledge, format the output in TOON, and manage the destination database files.

## Patterns

- **Name**: Overlapping Context Segmentation
- **When**: Executing Phase 1 (Document Segmentation) on a raw text corpus.
- **Example**: ```
  Read the source corpus text in overlapping windows of 8,000 tokens with a 1,000-token
  overlap to ensure that no boundaries are missed or split at window edges.

  For a source corpus containing a continuous transcription of historical letters:
  - Window 1: Tokens 0 to 8,000. Detect boundaries and extract metadata for documents
    ending in this range.
  - Window 2: Tokens 7,000 to 15,000. Identify the continuation of the final document
    from Window 1 and locate subsequent document boundaries.
  ```

---

- **Name**: Logical Boundary Identification
- **When**: Scanning text windows to partition the corpus.
- **Example**: ```
  Inspect text structure to detect transitions between separate logical documents
  (e.g., individual letters or entries) using specific textual markers:
  - Date headers: e.g., "March 9, 1877" or "Salt Lake City, May 1st 1882".
  - Salutations & Closings: e.g., "Dear Brother:", "Your brother in the Gospel,".
  - Subject Shifts: a transition from an administrative letter to a journal entry.
  - Page Cues: document breaks matching page headers in the source publication.
  ```

---

- **Name**: Structured Entity Serialization (TOON Format)
- **When**: Formatting extracted entities in Phase 2.
- **Example**: ```
  Write all extracted named entities using the typed TOON format. Specify the count of
  items in brackets next to the category name, followed by a colon and a comma-separated
  list.

  people[2]: Brigham Young,unnamed woman
  places[0]:
  dates[1]: 1877-03-09
  organizations[1]: The Church
  roles[2]: church leader,questioner
  ordinances[1]: sealing
  ```

---

- **Name**: Topics and Themes Serialization (TOON Format)
- **When**: Formatting extracted thematic concepts in Phase 2.
- **Example**: ```
  Represent topics under two categories: controlled_topics (from a taxonomy) and
  free_tags (free-form tags capturing specific nuances). Specify counts in brackets.

  controlled_topics[5]: sealing-practices,plural-marriage,family-relationships,children-custody,ecclesiastical-questions
  free_tags[3]: woman sealed to multiple men,children's patriarchal lineage,Q&A format
  ```

---

- **Name**: Provenance Mapping
- **When**: Recording segment metadata.
- **Example**: ```
  Track the precise hierarchy mapping of each segment back to its archival or
  publication source (Collection > Box > Reel > Volume > Page).

  provenance: "George Albert Smith Papers > Box 4 > Reel 2 > Volume 1 > Page 142"
  ```

---

- **Name**: Semantic Vector Cache Serialization
- **When**: Writing the pre-compiled semantic cache in Phase 2.
- **Example**: ```
  Serialize semantic representations inside semantic_cache.toon solely as float vector
  arrays mapped to segment_ids. Restrict this file's contents to float vector arrays
  mapped to segment_ids — generate each vector by passing the combined claims and
  summaries to an embedding generator, and save the raw claims/summaries in
  document_registry.toon instead, for retrieval-phase reconstruction.

  segment_101: vector[1536]: 0.0123,-0.0456,0.1221,0.0891,-0.1102
  segment_102: vector[1536]: -0.0512,0.0883,-0.0112,-0.0345,0.0092
  ```

---

- **Name**: Traceable Relationship Tuple Extraction
- **When**: Building the relationship graph payload in Phase 2.
- **Example**: ```
  Extract direct relationships between entities and concepts as standard 4-element
  [subject, predicate, object, segment_id] tuples to build a queryable, traceable
  knowledge graph.
  - Traceability: every tuple must append the exact segment_id as its fourth element.
  - Suggested Taxonomy of Predicates:
    - Interpersonal: spoke_to, relative_of, associated_with, ordained_by, instructed,
      corresponded_with
    - Conceptual/Organizational: member_of, held_office_in, located_in,
      defines_practice_of, refers_to, administered
  - Extraction Density: extract exhaustively, identifying every connection between
    people, places, organizations, topics, and events mentioned in the text segment,
    building a dense net of connections beyond sender/recipient names alone.

  [2]:
    - [4]: Brigham Young,spoke_to,unnamed woman,segment_101
    - [4]: sealing,defines_practice_of,plural-marriage,segment_101
  ```

---

- **Name**: Incremental Append-Only Output
- **When**: Writing the final pre-compiled knowledge layer outputs.
- **Example**: ```
  Append the output records to the destination files (document_registry.toon,
  semantic_cache.toon, and relationship_graph.toon) instead of overwriting them. If a
  file does not exist, initialize it; otherwise, append a blank line followed by the
  new records.

  When writing to document_registry.toon:
  1. Check if the file exists.
  2. Read the end of the file.
  3. Append a newline.
  4. Write the new document record block in TOON format.
  ```

---

## Anti-Patterns

- **Name**: Single-Pass Extraction
- **Why**: Combining segmentation and extraction into one ad-hoc step causes boundary fragmentation — a segment gets extracted before its closing signature or a new date header confirms where it actually ends.
- **Instead**: Multi-Phase Pipeline — establish document boundaries in Phase 1 before extracting semantic/relational knowledge in Phase 2.

---

- **Name**: Destructive Overwrite
- **Why**: Writing destination `.toon` files in overwrite mode erases previously compiled history and search indices instead of extending them.
- **Instead**: Incremental Append-Only Output.

---

- **Name**: Ungrounded Extrapolation
- **Why**: Letting the model's pre-trained weights supplement historical details not present in the active text segment produces claims that cannot be traced back to the source, undermining the reasoning cache's reliability.
- **Instead**: Traceable Relationship Tuple Extraction, grounded strictly in the segment's text.

---

- **Name**: Literal Name Matching
- **Why**: Treating name variants ("Brigham Young", "President Young", "B. Young") as distinct entities instead of resolving coreference fragments the knowledge graph into disconnected subgraphs.
- **Instead**: Normalize names to their full standard historical form and cross-check against existing entities before writing a new one, per Structured Entity Serialization.
