# Critical Reader Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by the critical-reader skill.

## Patterns

- **Name**: Academic Impetus Grounding
- **Description**: Locate and frame the author's work within the wider landscape of academic literature and ongoing scholarly debates.
- **When**: Writing the Exigency section of the critique.
- **Example**: "Rather than viewing the text in isolation, identify that the author is responding to the post-structuralist critiques of language pioneered by Derrida, specifically addressing the instability of the signifier."

---

- **Name**: External Helper for PDF Parsing
- **Description**: Delegate the parsing of binary PDF file types to a dedicated Python helper script in the skill's scripts directory rather than attempting to read raw PDF bytes directly.
- **When**: The input file has a `.pdf` extension.
- **Example**: Execute `python3 scripts/parse_pdf.py /path/to/input.pdf` and capture the stdout to read the document.

---

- **Name**: Interactive Destination Elicitation
- **Description**: Always ask the user where to write the final analysis report instead of making assumptions about the output file path.
- **When**: Starting the execution flow after verifying the input document.
- **Example**: "Input file verified. Where would you like me to save the final analysis report? Please provide an absolute or relative path."

## Anti-Patterns

- **Name**: High-Level Superficial Summary
- **Description**: Providing a simple, generic summary of what chapters are about instead of a deep critique of the work's theoretical architecture.
- **Why**: Fails the "world-renowned scholar" persona and does not help the researcher uncover the underlying thesis, method, or gaps.
- **Instead**: Dissect the structural choices, underlying methodology, and critical shortcomings of the text.

---

- **Name**: Hardcoded Output Paths
- **Description**: Writing the report to a default hardcoded path without prompting the user.
- **Why**: Can overwrite existing files or write reports to unexpected locations, cluttering the user's workspace.
- **Instead**: Prompt the user explicitly for the destination path before starting the analysis.

---

- **Name**: OCR Failure Assumption
- **Description**: Failing to check if the PDF contains readable text before starting the analysis.
- **Why**: Will result in an empty string and a failed analysis report if the PDF is scanned.
- **Instead**: Check the length of the extracted text from the PDF script, and warn the user if it appears empty or scanned.
