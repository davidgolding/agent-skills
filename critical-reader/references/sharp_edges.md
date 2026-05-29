# Sharp Edges

This document defines the sharp edges used by the critical-reader skill.

## Scanned PDF Empty Text

- **Id**: scanned-pdf-empty-text
- **Summary**: Scanned or image-only PDFs yield empty text during extraction.
- **Severity**: critical
- **Situation**: The user provides a PDF file that does not contain a digital text layer (e.g., direct book scans without OCR).
- **Why**: The Python helper script extracts text using standard PDF parsers which cannot read pixel data or image blocks.
- **Solution**: Check the character length of the extracted text; if it is less than 100 characters, warn the user and suggest performing OCR or providing a text version.
- **Symptoms**: PDF text extraction finishes immediately and returns an empty or extremely short string.
- **Detection Pattern**: Extracted text length is near zero or contains only non-alphanumeric control characters.

---

## Large Context Truncation

- **Id**: large-context-truncation
- **Summary**: Extremely large books can exceed the context window or cause processing timeouts.
- **Severity**: high
- **Situation**: The user provides an entire multi-hundred-page book for analysis.
- **Why**: Large files consume vast numbers of tokens and may exceed the model's single-turn context window or run out of generation tokens.
- **Solution**: Encourage the user to analyze the document in parts (e.g., chapter by chapter) or use summary representations if the file size exceeds 1MB.
- **Symptoms**: The model cuts off mid-report or fails with a token limit error.
- **Detection Pattern**: File sizes greater than 1,000,000 bytes.
