# Validations

This document defines the validations used by the critical-reader skill.

## File Must Exist

- **Id**: file-must-exist
- **Severity**: error
- **Type**: instruction
- **Pattern**: Input file path does not point to a valid file on the filesystem
- **Message**: The specified input file path could not be found or is not readable.
- **Fix Action**: Verify the path spelling and ensure it is an absolute path or relative to the workspace.
- **Applies To**:
  - `*`

---

## Valid Report Sections

- **Id**: valid-report-sections
- **Severity**: warning
- **Type**: instruction
- **Pattern**: The output analysis report is missing one or more of the required headings (Exigency, Response, Architecture, Speculation, Evaluation)
- **Message**: The generated report does not contain all five standard critical sections.
- **Fix Action**: Re-generate the report ensuring that all five headings are included.
- **Applies To**:
  - `*.md`

---

## Empty Extracted Text

- **Id**: empty-extracted-text
- **Severity**: error
- **Type**: instruction
- **Pattern**: Extracted text contains less than 100 characters of content
- **Message**: The document text appears empty or could not be parsed.
- **Fix Action**: Check if the PDF is scanned/image-only, or check if the text file is empty.
- **Applies To**:
  - `*.pdf`
  - `*.txt`
  - `*.md`
