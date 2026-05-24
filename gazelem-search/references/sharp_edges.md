# Gazelem Search Sharp Edges

This document details common failures, diagnosing symptoms, and mitigation strategies when performing search operations over historical corpora.

---

## Single-Modality Bias

### **Id**
single-modality-bias
### **Summary**
Relying strictly on a single search method (e.g., keyword only or semantic only), leading to vocabulary mismatches or noisy results.
### **Severity**
high
### **Situation**
The agent only runs semantic search for the term "welfare" and misses documents that contain the exact word "donations" but have low semantic similarity scores in the embedding model.
### **Why**
Failing to triangulate and cross-reference multiple search types.
### **Solution**
- Enforce the use of at least two distinct modes (e.g., metadata filter + keyword scan) for complex queries.
- Cross-reference candidate lists generated from different modes.
### **Symptoms**
- Incomplete answers that miss obvious relevant documents containing spelling variations.
- High volume of irrelevant search matches in semantic results.
### **Detection Pattern**
Search logs containing only one type of search invocation (e.g., only semantic lookups).

---

## Blind Corpus Scanning

### **Id**
blind-corpus-scanning
### **Summary**
Executing keyword searches across the entire raw text corpus before narrowing the search space down via metadata.
### **Severity**
critical
### **Situation**
The agent performs a grep search for "Brigham" across all raw files in a 10GB corpus, causing the tool to hang, timeout, or consume millions of tokens.
### **Why**
Searching raw texts without using the pre-compiled registry or cache layers first.
### **Solution**
- Use Mode A or Mode B to filter the document registry by date ranges, authors, or topics.
- Restrict raw file reads and grep searches to the isolated subset of candidate files.
### **Symptoms**
- Command timeouts or heavy read latencies.
- Large context sizes filled with irrelevant documents.
### **Detection Pattern**
File-reading or text-searching commands targeting the root of the raw corpus directory.

---

## Missing Raw Text Deep-Dive

### **Id**
missing-raw-text-deep-dive
### **Summary**
Drafting the final answer using only the pre-compiled metadata summaries or cache excerpts without reading the raw document text.
### **Severity**
high
### **Situation**
The agent reads the summary in `document_registry.toon` stating a letter discusses "plural marriage sealing practices", and answers the user's doctrinal query based on that summary, missing crucial details in the letter body.
### **Why**
Failing to perform Phase 3 (Deep-Dive) file retrieval.
### **Solution**
- Once candidate segment IDs are found, the agent must fetch and read the raw text of the segment from the source file.
### **Symptoms**
- Superficial answers that lack quotes or specific historical details.
- Hallucinated answers based on vague metadata summaries.
### **Detection Pattern**
Responding to a search query without invoking `view_file` on the source document path listed in the provenance.

---

## Citation Drift

### **Id**
citation-drift
### **Summary**
Formulating answers containing historical facts or quotes without appending exact source citations.
### **Severity**
high
### **Situation**
The agent writes a detailed explanation of Relief Society activities but provides no references, or provides a vague citation like "Glenwood records".
### **Why**
Neglecting to map the source provenance coordinates to the synthesized assertions.
### **Solution**
- Check every sentence of the final response and append a citation matching `(Source: <file_name>, Page <page>, Date <date>, Author <author>)`.
### **Symptoms**
- Unverifiable historical claims.
- Rejection of findings by researchers due to lack of source tracing.
### **Detection Pattern**
Responses containing historical facts that do not end with a structured `(Source: ...)` block.

---

## Query Literalism

### **Id**
query-literalism
### **Summary**
Failing to find documents because search terms are matched literally, ignoring historical language changes.
### **Severity**
medium
### **Situation**
The user searches for "mental illness" in a 19th-century corpus. The agent searches literally for "mental illness" and finds nothing, missing entries using the terms "insane", "lunatic", or "distempered".
### **Why**
Failing to expand the query vocabulary with historical synonyms.
### **Solution**
- Include a query deconstruction phase where historical synonyms are mapped prior to executing searches.
### **Symptoms**
- Search returning zero results for modern concepts that are historically documented under different vocabulary.
### **Detection Pattern**
No vocabulary expansion or synonym listing in the search planning thoughts.
