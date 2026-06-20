# Gazelem Search Patterns

This document details the patterns and protocols required to execute tri-modal corpus searches, iterate on leads, and synthesize cited historical findings.

---

### **Name**
Query Deconstruction and Strategy
### **Description**
Before running any search, analyze the user's query to identify constraints and expand terminology.
1. **Isolate constraints:** Map temporal (dates), geographic (places), and social (people/organizations) parameters.
2. **Expand vocabulary:** List historical synonyms and spelling variants of key query terms.
3. **Establish primary vector:** Select which search mode (Mode A, B, or C) is the most precise starting point.
### **When**
Beginning any search session on a corpus.
### **Example**
For the query "did the relief society help poor families in Glenwood in 1883":
- Constraints: date = 1883, place = Glenwood, organization = Relief Society.
- Synonyms: "Relief Society" -> "RS", "sisterhood"; "help poor" -> "welfare", "alms", "relief", "donations", "charity".
- Primary Vector: Mode A (narrow metadata index by year 1883 and organization Relief Society).

---

### **Name**
Mode A: Metadata and Graph Precision Filtering
### **Description**
Narrow down the search scope by scanning index files and traversing entity connections.
1. Scan `document_registry.toon` for authors, recipients, dates, and `controlled_topics` matching your strategy.
2. Scan `relationship_graph.toon` to find connections. Since relations are stored as 4-element tuples (`[subject, predicate, object, segment_id]`), you can extract matching connections for entities (e.g. John Smith) and directly read their source `segment_id`s from the fourth element.
3. Traverse second-degree connections to expand the query candidate pool and collect all related `segment_id`s.
### **When**
Restricting the query space using hard metadata filters or graph relations.
### **Example**
Searching `relationship_graph.toon` for tuples containing "plural-marriage" and directly extracting their associated source coordinates (e.g., `segment_101`).

---

### **Name**
Mode B: Semantic Vector Similarity Matching
### **Description**
Match conceptual queries and resolve vocabulary mismatches by comparing mathematical vector embeddings of queries against pre-computed vectors in the semantic cache.
1. Translate the user's natural language question into 2-3 declarative semantic search query strings.
2. Call the embedding generator API or tool to compute a vector embedding for these query strings.
3. Compute the cosine similarity between the query vectors and the float vectors stored in `semantic_cache.toon`.
4. Rank the `segment_id`s by their similarity scores and output the top candidates.
5. Reconstruct the candidate records' text context by reading their matching claims/summaries from `document_registry.toon`.
### **When**
The user's query uses abstract concepts or modern terminology that might not match the exact wording of historical records.
### **Example**
Translating "how did they handle custody disputes" into the query string "children belong to their respective fathers", generating its float embedding vector, and running similarity matching against `semantic_cache.toon` to find matching segment IDs.

---

### **Name**
Mode C: Target-Constrained Keyword Excerpt Search
### **Description**
Execute exact-string or regex searches against raw text files, restricted to a pre-filtered metadata subset.
1. **Do not run keyword searches across the entire raw corpus blindly.**
2. Narrow the search files first to a subset of `segment_id`s using Mode A or Mode B (e.g., limit search to files within box 4, reel 2).
3. Execute exact-string or regex matches against the raw text of that subset using native tools (e.g., `grep_search` or running `grep` via `run_command`) directly instead of generating and running custom python scripts.
### **When**
Locating specific names, unique phrases, or numerical values in raw corpus files.
### **Example**
Filtering files to the "Glenwood RS Minutes" for the year "1883", then using `grep_search` or a native `grep` command to search for the term "welfare" inside only those files.

---

### **Name**
Reasoning and Iteration Loop
### **Description**
Evaluate the initial results, identify gaps/leads, and perform nested loops.
1. Read the summaries/excerpts of candidates returned by Phase 2.
2. Check for missing details. If a document references another letter, order, or date, treat that as a new lead.
3. Formulate a new strategy for the lead, return to Phase 2, and run a nested search pass.
### **When**
Processing search candidate lists before finalizing answers.
### **Example**
A letter dated March 9, 1877, mentions "the decision of the council last Thursday". Run a follow-up Mode A search for council minutes dated March 1, 1877.

---

### **Name**
Sourced Synthesis and Citation
### **Description**
Compile final responses using context retrieved *only* during the raw text deep-dive phase, formatting every claim with a structured citation.
- Cite using the format: `(Source: <file_name>, Page <page>, Date <date>, Author <author>)` based on the segment provenance.
### **When**
Formatting the final response for the user.
### **Example**
"In Glenwood, the Relief Society distributed wheat to families in need. (Source: LR 3227 14 - Glenwood RS 1883.docx, Page 3, Oct 4, 1883)."
