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
2. Scan `relationship_graph.toon` to find second-degree entity connections (e.g., if searching "John Smith", find who John Smith corresponded with or worked with, and add those names to the query candidate pool).
3. Compile a list of candidate `segment_id`s.
### **When**
Restricting the query space using hard metadata filters or graph relations.
### **Example**
Searching `document_registry.toon` for `controlled_topics` matching "plural-marriage" and filtering the matching list to files in `1877`.

---

### **Name**
Mode B: Semantic Concept Matching
### **Description**
Match conceptual queries and handle vocabulary mismatches using semantic summaries and claims.
1. Translate the user's natural language question into 2-3 declarative semantic claims.
2. Scan `semantic_cache.toon` to locate blocks containing similar claims or summaries.
3. Output a list of candidate `segment_id`s ranked by relevance.
### **When**
The user's query uses abstract concepts or modern terminology that might not match the exact wording of historical records.
### **Example**
Translating "how did they handle custody disputes" into claims: "children belong to their respective fathers" and searching `semantic_cache.toon`.

---

### **Name**
Mode C: Target-Constrained Keyword Excerpt Search
### **Description**
Execute exact-string or regex searches against raw text files, restricted to a pre-filtered metadata subset.
1. **Do not run keyword searches across the entire raw corpus blindly.**
2. Narrow the search files first to a subset of `segment_id`s using Mode A or Mode B (e.g., limit search to files within box 4, reel 2).
3. Execute exact-string or regex matches against the raw text of that subset.
### **When**
Locating specific names, unique phrases, or numerical values in raw corpus files.
### **Example**
Filtering files to the "Glenwood RS Minutes" for the year "1883", then grepping for the term "welfare" inside only those files.

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
