# Corpus Search Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by corpus-search.

## Patterns

- **Name**: Schema Activation & Query Priming
- **Description**: Decompose complex user search prompts into entity, temporal, functional, and structural search dimensions before executing terminal queries.
- **When**: Initiating any new research task across a document corpus to reduce working memory load.
- **Example**:
```
Deconstruct query "19th century public health reforms" into:
- Creating Entities: General Board of Health, Sanitary Commission, Poor Law Guardians
- Temporal Bounds: 1848-1875
- Key Functional Terms: "quarantine", "sewerage", "cholera", "miasma"
```

---

- **Name**: Binary Document Pre-Extraction
- **Description**: Convert non-plain-text documents (PDF, DOCX) into temporary plain text or Markdown files stored in workspace scratch space before running `ripgrep`.
- **When**: Corpus search target directory contains PDF or DOCX files.
- **Example**:
```bash
# Convert PDF to text in scratch space before ripgrep search
pdftotext corpus/report.pdf .scratch/report.txt
rg "sanitary commission" .scratch/
```

---

- **Name**: Berrypicking Query Evolution
- **Description**: Continuously update search queries based on clues (names, citations, archival reference codes) discovered during preceding grep passes.
- **When**: Running multi-pass search loops to follow emergent research leads.
- **Example**:
```
Pass 1 grep for "cholera 1848" reveals recurring author "Dr. John Snow" and reference "Fonds 402".
Pass 2 grep evolves to target "Snow" AND "Fonds 402" across related series files.
```

---

- **Name**: Diplomatic Criticism Analysis
- **Description**: Evaluate matched document excerpts by distinguishing extrinsic elements (physical form, script, layout) from intrinsic elements (author authority, protocol, disposition).
- **When**: Reading matched passages in context to determine evidentiary weight.
- **Example**:
```
Analyze excerpt:
- Extrinsic: Draft handwritten marginal note.
- Intrinsic: Author is Assistant Secretary; disposition is provisional recommendation, not binding policy.
```

---

- **Name**: Source Triangulation Matrix
- **Description**: Cross-verify all historical assertions across a matrix of at least three independent source categories (e.g., official record, private diary, press report).
- **When**: Synthesizing final findings and presenting conclusions to the user.
- **Example**:
```
Assertion: "Board of Health suppressed 1854 report."
- Source 1 (Official): Treasury minutes showing delayed printing budget.
- Source 2 (Private): Letter from Board member acknowledging hold.
- Source 3 (Media): Times editorial criticizing withheld findings.
Status: Confirmed via Triangulation.
```

---

- **Name**: Structured Stop-Loss Pivot
- **Description**: When a search query pass produces null or low-yield results, classify the failure (theory, data, or method) and execute a structured Zoom, Source, or Question pivot.
- **When**: Facing null grep results or stalled research trajectories.
- **Example**:
```
Null result for "Quarantine Act 1852 amendment".
Pivot Action:
- Zoom Pivot: Expand search window from 1852 to 1850-1855.
- Source Pivot: Switch from legislative records to Board of Trade correspondence.
```

---

- **Name**: Toulmin Counterfactual Validation
- **Description**: Validate causal claims by framing arguments with Claims, Data, Warrants, and testing minimal-rewrite counterfactuals ("If not X, then not Y").
- **When**: Asserting causal relationships between historical events in synthesis reports.
- **Example**:
```
Claim: "1848 Act caused municipal sanitary reforms."
Counterfactual Check: Test whether cities with existing local acts enacted identical reforms without the 1848 Act.
```

---

## Anti-Patterns

- **Name**: Sequential Fact Ingestion
- **Description**: Reading entire document files sequentially without pre-filtering via grep or schema activation.
- **Why**: Floods the agent's active context window, causing instruction drift and severe latency.
- **Instead**: Use targeted `ripgrep` searches with line limits (`rg -C 3`) to ingest only high-relevance contextual windows.

---

- **Name**: Pertinence Trap
- **Description**: Searching solely for topical terms while ignoring archival provenance and record-creator organization.
- **Why**: Misses critical records created by administrative bodies that used contemporary or non-obvious terminology.
- **Instead**: Map the administrative history first and search within the fonds/series of the responsible creating entity.

---

- **Name**: Direct Binary Grep
- **Description**: Running `ripgrep` directly on raw PDF or DOCX binary files.
- **Why**: Binary encoding causes `ripgrep` to skip files or output unreadable garbled binary matches.
- **Instead**: Convert binary files to temporary plain text/markdown in scratch space prior to running grep.

---

- **Name**: Static Query Anchoring
- **Description**: Re-running the exact same original user query repeatedly without incorporating new leads or terms found in previous passes.
- **Why**: Traps the agent in a static loop, failing to discover deeper contextual connections.
- **Instead**: Practice Berrypicking — extract new names, dates, and terms from each pass to refine subsequent queries.

---

- **Name**: Single-Source Claim Stating
- **Description**: Stating historical claims as absolute facts based on a single isolated document passage.
- **Why**: Leads to biased or unverified conclusions due to potential author bias or unrepresentative sampling.
- **Instead**: Construct a Source Triangulation Matrix to verify claims across multiple independent sources before stating them.

---

- **Name**: Sunk Cost Search Persistence
- **Description**: Persisting in a non-yielding keyword search path simply because time was already spent on it.
- **Why**: Wastes search turns and user interaction time on dead-end inquiries.
- **Instead**: Apply the Stop-Loss Pivot heuristic — switch strategy (Zoom, Source, or Question) immediately upon encountering a null result.

---
