# Sharp Edges

This document defines the sharp edges used by sharepoint-search.

---

## Unmapped Top Level Documents Folder

- **Id**: unmapped-documents-folder
- **Summary**: The SharePoint agent host may not explicitly register `/Documents` as a distinct named folder path, causing path-scoped queries to fail.
- **Severity**: high
- **Situation**: Searching for files when the host SharePoint site uses non-standard library names (e.g. `Shared Documents` or custom document libraries).
- **Why**: SharePoint site templates vary across tenants and site types (Team sites vs Communication sites vs custom drives).
- **Solution**:
    - Always implement a fallback to drive-root index search when `/Documents` path query returns zero results or an invalid path error.
- **Symptoms**:
    - Zero search results returned even when target files exist in the site library.
    - Graph API errors indicating `itemNotFound` or invalid path target `/Documents`.
- **Detection Pattern**: Search queries returning zero items or path error responses when target scope is restricted to `/Documents`.

---

## M365 Semantic Index Delay

- **Id**: semantic-index-indexing-delay
- **Summary**: Newly uploaded or modified SharePoint documents may not be immediately searchable via vector embeddings due to indexing latency.
- **Severity**: medium
- **Situation**: Users querying for files created or modified within the last few minutes.
- **Why**: M365 Semantic Index background processing and vector embedding extraction run asynchronously.
- **Solution**:
    - Use Pass 1 lexical keyword search as an immediate fallback to catch recently created files by exact name or metadata tags.
- **Symptoms**:
    - Semantic search misses recently added files, while direct filename lookup succeeds.
- **Detection Pattern**: Recent file modification timestamp combined with missing semantic search match in query results.

---

## Paraphrase Evidence Distortion

- **Id**: paraphrase-evidence-distortion
- **Summary**: Summarizing or altering quoted text from primary sources during retrieval destroys orthographic fidelity and historical nuance.
- **Severity**: high
- **Situation**: Presenting evidence passages from retrieved SharePoint documents to the user or downstream research agent.
- **Why**: LLM default summarization tendencies overwrite exact historical wording with modern paraphrases.
- **Solution**:
    - Enforce verbatim quote extraction for all evidence passages, preserving exact punctuation, spelling, and capitalization, while placing synthesis in a separate Interpretation section.
- **Symptoms**:
    - Quoted passages contain modernized phrasing, corrected archaic spelling, or missing punctuation.
- **Detection Pattern**: Quoted evidence string differing from source document text snippet.

---

## Sunk Cost Search Looping

- **Id**: sunk-cost-search-looping
- **Summary**: Persisting in minor keyword variations of a failed query without executing a structural pivot.
- **Severity**: medium
- **Situation**: When initial searches return zero hits or irrelevant files.
- **Why**: Sunk cost fallacy leads agents to retry similar queries rather than changing scale, genre, or query formulation.
- **Solution**:
    - Enforce a Stop-Loss heuristic after 1-2 failed attempts, triggering a Zoom, Source, or Question pivot.
- **Symptoms**:
    - Agent executes 3+ sequential searches with near-identical keyword variations.
- **Detection Pattern**: Repeated search log entries with >80% keyword overlap following zero-result responses.

---

## Unbacked Absence Claim

- **Id**: unbacked-absence-claim
- **Summary**: Asserting that a document or record does not exist in SharePoint without logging the specific exhaustive searches executed.
- **Severity**: high
- **Situation**: Answering user queries where no matching document was found in the library.
- **Why**: Absence of evidence is only valid if backed by recorded search coverage accounting.
- **Solution**:
    - Explicitly report null results alongside the exact search queries ran, distinguishing between "corpus contains no record" and "search was non-exhaustive".
- **Symptoms**:
    - Agent states "No record exists" without providing a search audit log.
- **Detection Pattern**: Declarative negative claim lacking supporting search log inventory.

---
