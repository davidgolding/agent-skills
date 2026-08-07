# Advanced Research Assistant Validations

This document defines the validations used by advanced-research-assistant.

## Fixed Ready-State Reply Present

- **Id**: fixed-ready-state-reply-present
- **Severity**: error
- **Type**: semantic
- **Pattern**: The first reply after initialization does not exactly match "What is your research question? I'll write a report based on your prompt."
- **Message**: The ready-state reply must match the required greeting exactly.
- **Fix Action**: Replace the reply with the exact required string before sending.
- **Applies To**:
    - initialization reply

---

## Mode Classification Exhaustive And Gated

- **Id**: mode-classification-exhaustive-and-gated
- **Severity**: error
- **Type**: semantic
- **Pattern**: A user message is treated as Mode 3 (Execution) without an explicit approval message following a presented Mode 2 Research Plan.
- **Message**: Mode 3 requires an explicit user approval of a previously presented Research Plan.
- **Fix Action**: Reclassify the message as Mode 2 and present or re-present the Research Plan instead of executing.
- **Applies To**:
    - mode classification step

---

## Research Plan Required Parts

- **Id**: research-plan-required-parts
- **Severity**: error
- **Type**: schema
- **Pattern**: A Proposed Research Plan is missing one of: Refined Research Question, Proposed Methodology, Initial Search Strategy, Assumptions & Pre-understanding Audit.
- **Message**: A Research Plan must include all four required parts before being presented for approval.
- **Fix Action**: Add the missing part before presenting the plan to the user.
- **Applies To**:
    - Mode 2 output

---

## Evidence Entry Required Fields

- **Id**: evidence-entry-required-fields
- **Severity**: error
- **Type**: schema
- **Pattern**: An evidence record is missing one of: Who, Where, When, What, Type/Diplomatics.
- **Message**: Every evidence record must carry Who, Where, When, What, and Type/Diplomatics fields.
- **Fix Action**: Return to the source and fill in the missing field before adding the record to the evidence set.
- **Applies To**:
    - Deep Research evidence records

---

## Report Required Fields

- **Id**: report-required-fields
- **Severity**: error
- **Type**: schema
- **Pattern**: The Research Report is missing one of: Sources Searched, Coverage Percentage, Confidence Level, Known Gaps, or one of the Findings sub-sections (Summary Answer, Evidence Matrix, Key Findings, Research Perplexities, Recommended Next Steps).
- **Message**: The Research Report must state Sources Searched, Coverage Percentage, Confidence Level, Known Gaps, and the full Findings structure.
- **Fix Action**: Add the missing field or sub-section before delivering the report.
- **Applies To**:
    - Research Report output

---

## Citation Traces To File Path

- **Id**: citation-traces-to-file-path
- **Severity**: error
- **Type**: semantic
- **Pattern**: A claim, quote, or Evidence Matrix row has no explicit, resolvable project file path attached.
- **Message**: Every claim must trace to an explicit file path from the project.
- **Fix Action**: Locate and attach the source file path, or remove the claim if no project file supports it.
- **Applies To**:
    - Research Report output
    - Mode 1 brief output

---

## Scope Containment

- **Id**: scope-containment
- **Severity**: error
- **Type**: semantic
- **Pattern**: A search, read, or cited fact originates from outside the current project and its subdirectories without an explicit user request to expand scope.
- **Message**: Reads and citations must stay confined to the current project unless the user explicitly asked to expand scope.
- **Fix Action**: Remove the out-of-scope content, or ask the user to explicitly authorize expanding scope before using it.
- **Applies To**:
    - all search and read operations
    - Research Report output
