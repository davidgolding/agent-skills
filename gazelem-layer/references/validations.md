# Gazelem Layer Validations

This document defines the validation rules and regex constraints to enforce structured correctness, schema compliance, and safety when generating the knowledge layer.

---

## TOON Syntax Validation

### **Id**
toon-syntax-check
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!.*(?:people|places|dates|organizations|roles|ordinances)\[\d+\]:.*$).*$`
- `^(?!.*(?:controlled_topics|free_tags)\[\d+\]:.*$).*$`
### **Message**
Incorrect TOON formatting syntax. Categories must match 'name[count]: val1, val2' or 'name[0]:'.
### **Fix Action**
Reformat the line to explicitly state category type, count of entities/topics in brackets, a colon, and comma-separated values.
### **Applies To**
- *.toon
- document_registry.toon

---

## Required Registry Fields

### **Id**
registry-fields-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!.*date:).*$`
- `^(?!.*sender:).*$`
- `^(?!.*recipient:).*$`
- `^(?!.*document_type:).*$`
- `^(?!.*page_range:).*$`
- `^(?!.*provenance:).*$`
### **Message**
One or more required metadata fields are missing from the document segment.
### **Fix Action**
Extract and add the missing header field to the segment output in `document_registry.toon`.
### **Applies To**
- document_registry.toon

---

## Empty Output Prevention

### **Id**
empty-knowledge-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
- `^\s*claims:\s*\[\]\s*$`
- `^\s*summary:\s*""\s*$`
### **Message**
Extracted claims list or document summary is empty.
### **Fix Action**
Re-process the segment to draft natural language claims and a 2-3 sentence abstract summarizing the text.
### **Applies To**
- document_registry.toon

---

## Vector Cache Format Validation

### **Id**
vector-cache-non-vector-leak
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!segment_\w+:\s*vector\[\d+\]:\s*[-?\d\.]+(?:,[-?\d\.]+)*$).+$`
### **Message**
Raw text, claims, or malformed entries detected in semantic_cache.toon. It must strictly contain segment_id mapped to a float vector declaration.
### **Fix Action**
Remove the raw text entries and re-run the vectorizer to output only float vectors in the format 'segment_id: vector[dimensions]: float,float,...'.
### **Applies To**
- semantic_cache.toon

---

## Relationship Graph Traceability Validation

### **Id**
graph-traceability-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!\s*-\s*\[4\]:\s*[^,]+,[^,]+,[^,]+,segment_\w+$)(?!\s*\[\d+\]:).+$`
### **Message**
Malformed relationship tuple. Every relationship record in relationship_graph.toon must be a 4-element tuple containing a valid segment_id (e.g. '[4]: subject,predicate,object,segment_id').
### **Fix Action**
Re-extract relationships to include the fourth element (source segment_id) in the tuple.
### **Applies To**
- relationship_graph.toon

---

## Write Mode Safety

### **Id**
overwrite-violation
### **Severity**
error
### **Type**
regex
### **Pattern**
- `(?i)Overwrite:\s*true`
### **Message**
Write operation is set to overwrite, which risks erasing pre-existing pre-compiled knowledge indices.
### **Fix Action**
Configure the file system writer to use append mode, ensuring output records are appended to existing files without truncating.
### **Applies To**
- *.json
- *.py
- *.sh
