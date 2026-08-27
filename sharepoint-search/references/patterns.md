# SharePoint Search Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by sharepoint-search.

## Patterns

- **Name**: Two-Pass Retrieval Strategy
- **Description**: Formulate two distinct search passes for every user query—Pass 1 extracts specific keywords, entities, file extensions, and metadata tags; Pass 2 queries M365 Semantic Index vector embeddings for conceptual matches.
- **When**: Executing any natural language search query against Microsoft Graph or SharePoint documents.
- **Example**:
```
Pass 1 (Lexical): Extract keywords=["Treaty of Versailles", "reparations"], extension=".docx", tags=["diplomatic-history"]
Pass 2 (Semantic): Query intent="Interwar economic settlement agreements and financial strain" against M365 vector index
```

---

- **Name**: Berrypicking Evolving Queries
- **Description**: Treat search as a dynamic, bit-at-a-time process (Marcia Bates Berrypicking model). Each retrieved document ("berry") yields new entities, historical terms, or citations that trigger subsequent refined queries.
- **When**: Conducting deep historical research where an initial query is insufficient to uncover obscure or scattered evidence.
- **Example**:
```
Initial Query: "1919 economic negotiations" -> Returns hit mentioning "Commission on Reparation of Damage"
Evolving Query 1: Search exact phrase "Commission on Reparation of Damage"
Evolving Query 2: Search entity "Monnet" OR "Keynes" within document library /Documents/1919_Diplomacy
```

---

- **Name**: Provenance-Based Entity Querying
- **Description**: Map the administrative or organizational creators (departments, offices, authors) responsible for producing records before running abstract topic searches.
- **When**: Searching large SharePoint tenant libraries with complex folder structures or multi-departmental files.
- **Example**:
```
Target Subject: "Health policy during 1918 flu"
Provenance Step: Identify creator agency -> "Department of Public Health" or "Surgeon General Office"
Query: Scope search to creator metadata or sub-folder "Dept_Public_Health" combined with M365 Semantic Index
```

---

- **Name**: Verbatim Citation & Location Anchoring
- **Description**: Extract exact verbatim quotes from matching documents, preserving original spelling, capitalization, and punctuation, paired with stable location anchors (file name, webUrl, path, heading, or line/offset anchor).
- **When**: Returning search evidence for historical analysis and verification.
- **Example**:
```
Evidence: "The decision was reached at 0400 hours without consensus."
Location Anchor:
  - File: /Documents/Minutes_1918_11_11.docx
  - WebUrl: https://tenant.sharepoint.com/sites/archive/Documents/Minutes_1918_11_11.docx
  - Anchor: Section "Executive Session", Paragraph 3
```

---

- **Name**: Source Triangulation Matrix
- **Description**: Cross-verify substantive historical claims across multiple independent source genres (e.g. official minutes vs. private diaries vs. published reports) in SharePoint.
- **When**: Evaluating conflicting or contested historical claims retrieved from document libraries.
- **Example**:
```
Claim: "Order was dispatched on Nov 10"
Triangulation Check:
  - Source 1 (Official Telegraph Log): Matches (Nov 10, 23:15)
  - Source 2 (Private Journal entry): Matches ("Received telegraph late Sunday night")
  - Source 3 (Secondary Report): Disagrees (claims Nov 11) -> Surface disagreement explicitly
```

---

- **Name**: Null Result Accounting & Stop-Loss Pivot
- **Description**: Explicitly log zero-hit searches ("Searched term X across /Documents, returned 0 hits"). When a search path hits a dead end, apply a Stop-Loss heuristic and execute a structured pivot (Zoom, Source, or Question pivot).
- **When**: A query strategy yields no relevant results after 1-2 attempts.
- **Example**:
```
Null Result: Search for "Plan West 1939" returned 0 hits in /Documents/Military_Plans.
Pivot Action (Source Pivot): Shift genre search from "Military_Plans" to "Cabinet_Minutes" or search creator entity "General Staff".
```

---

## Anti-Patterns

- **Name**: Paraphrased Evidence Distortion
- **Description**: Loose paraphrasing or summarizing of primary source text during evidence extraction, losing exact wording, orthography, or nuance.
- **Why**: Distorts historical evidence, obscures original tone, and prevents precise scholarly verification.
- **Instead**: Quote primary source passages verbatim in full, placing synthesis separately under an "Interpretation" label.

---

- **Name**: Pertinence Trap (Ignoring Provenance)
- **Description**: Relying exclusively on global subject keyword queries while ignoring folder provenance, file creator metadata, or administrative hierarchy.
- **Why**: Mixes unrelated creators, loses original order context, and misses records indexed under agency names rather than topic keywords.
- **Instead**: Map creator entities and folder provenance first, then apply two-pass lexical and semantic queries within those functional scopes.

---

- **Name**: Sunk Cost Search Looping
- **Description**: Repeating minor variations of the same failed keyword query repeatedly without pivoting strategy.
- **Why**: Wastes API quota, increases search latency, and produces frustration without uncovering missing documents.
- **Instead**: Apply a Stop-Loss heuristic after zero hits and execute a structured Zoom, Source, or Question pivot.

---

- **Name**: Single-Pass Keyword Monoculture
- **Description**: Relying purely on exact keyword matching without leveraging M365 Semantic Index vector embeddings.
- **Why**: Misses relevant documents that use historical synonyms, alternate spelling, or related conceptual topics.
- **Instead**: Always execute the two-pass strategy combining lexical keyword extraction and semantic vector embedding lookup.

---

- **Name**: Directory Traversal Crawling
- **Description**: Crawling or listing individual SharePoint folders and files sequentially instead of querying Microsoft Graph and M365 Semantic Index.
- **Why**: High latency, high API call overhead, and fails to catch conceptual matches that lack exact keyword matches in filenames.
- **Instead**: Always query the M365 Semantic Index and Graph search endpoints as the primary retrieval engines.

---

- **Name**: Full Document Ingestion on Search
- **Description**: Downloading complete document bodies during a search pass.
- **Why**: Exhausts agent context window, increases token cost dramatically, and degrades response speed.
- **Instead**: Restrict search return payloads to metadata and verbatim evidence snippets with stable location anchors.

---
