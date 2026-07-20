# Validations

This document defines the validations used by corpus-search.

---

## Binary Format Pre-Conversion Requirement

- **Id**: binary-format-preconversion
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Direct grep execution on binary extensions (.pdf, .docx, .doc, .xlsx) without prior text extraction
- **Message**: Target search path contains binary files (PDF/DOCX) that have not been pre-converted to text scratch space
- **Fix Action**: Run a pre-conversion script or tool to extract plain text to `.scratch/` before executing `ripgrep`
- **Applies To**:
    - *.pdf
    - *.docx
    - *.doc

---

## Absolute Path Detection

- **Id**: absolute-path-prevention
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - \b/Users/[a-zA-Z0-9_\-\.]+
    - \b/home/[a-zA-Z0-9_\-\.]+
    - \b/var/folders/[a-zA-Z0-9_\-\.]+
- **Message**: Absolute path detected - breaks portability across workspace environments
- **Fix Action**: Replace hardcoded machine paths with relative workspace paths or relative scratch directories
- **Applies To**:
    - *.md
    - *.json
    - *.sh
    - *.py

---

## Single-Source Claim Prevention

- **Id**: single-source-claim-prevention
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Stating major historical claims as definitive facts when supported by only a single source passage
- **Message**: Historical claim is backed by a single source without multi-source triangulation
- **Fix Action**: Construct a Source Triangulation Matrix and verify the claim across at least two additional independent sources or passages
- **Applies To**:
    - *.md

---

## Stop-Loss Pivot Trigger

- **Id**: stop-loss-pivot-trigger
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - Re-executing a search query pass after a preceding null result without changing search strategy
- **Message**: Null result encountered without executing a structured Zoom, Source, or Question pivot
- **Fix Action**: Apply a Stop-Loss Pivot (Zoom scale, Source type, or Question frame) before running the next search pass
- **Applies To**:
    - *.md

---

## Question Stacking Prevention

- **Id**: question-stacking-prevention
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:ask|pose)\b.*\b(?:multiple|several|many|two|three)\b.*\bquestions?\b
- **Message**: Instructions or prompts advocate asking multiple questions in a single interaction turn
- **Fix Action**: Restructure interaction turns to ask exactly one question at a time, using blocking question tools where available
- **Applies To**:
    - SKILL.md
    - *.md

---
