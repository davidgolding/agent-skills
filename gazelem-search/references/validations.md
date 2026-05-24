# Gazelem Search Validations

This document defines validation rules and regex constraints to enforce strategy compliance, tri-modal search checking, and citation formatting.

---

## Citation Syntax Validation

### **Id**
citation-syntax-check
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!.*\(Source:\s*[^,]+,\s*Page\s*\d+,\s*Date\s*[^,]+,\s*Author\s*[^)]+\)).*$`
### **Message**
Missing or malformed source citation. Citing structure must exactly match '(Source: <file>, Page <page>, Date <date>, Author <author>)'.
### **Fix Action**
Reformat the citation to match the exact pattern using the provenance metadata from the segment.
### **Applies To**
- walkthrough.md
- *.md

---

## Strategy Stage Requirement

### **Id**
strategy-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
- `^(?!.*(?:Temporal bounds|Geographic bounds|Social bounds|Synonyms|Primary Vector)).*$`
### **Message**
The search strategy has not been formulated. You must define constraints and synonyms before executing search queries.
### **Fix Action**
Formulate a strategy block outlining Temporal, Geographic, and Social bounds, synonyms, and the primary vector.
### **Applies To**
- *.md

---

## Tri-Modal Coverage Verification

### **Id**
insufficient-search-modes
### **Severity**
warning
### **Type**
regex
### **Pattern**
- `^(?!.*(?:Mode A|Mode B|Mode C).*(?:Mode A|Mode B|Mode C)).*$`
### **Message**
Less than two search modes were utilized. For complex queries, you must combine at least two modalities (Metadata/Graph, Semantic Cache, and Keyword search).
### **Fix Action**
Execute an additional search modality (e.g., Mode B or Mode C) and cross-reference the candidate sets.
### **Applies To**
- *.md
