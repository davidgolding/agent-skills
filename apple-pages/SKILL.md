---
name: apple-pages
description: Create, read, update, delete, and export Apple Pages documents (.pages) on macOS by scripting Pages.app, backing up each file before editing it in place. Use when the user references a .pages file or asks to read, edit, restyle, add tables or images to, trash, or convert a Pages document to PDF, DOCX, EPUB, or plain text.
---

# Apple Pages

## Mandate

Carry out one requested operation per invocation (create, read, update, delete, or export) on a `.pages` document the user names, by driving Pages.app on macOS. Judge three things for each request: whether the environment can perform the operation at all (Pages.app installed, Automation permission granted, file present and downloaded), which mechanism the operation uses (temporary DOCX export for reads, native Pages scripting for every write, Trash for deletes), and which safety path a write takes (timestamped backup and in-place edit when the document is closed in Pages; separate copy when it is open). Ground the mechanism choices and script shapes in `references/patterns.md`, the failure modes and their remedies in `references/sharp_edges.md`, the pre-write and post-write checks in `references/validations.md`, and the operation phases and user gates in `references/interactions.md`. A correct result leaves the requested change applied natively in Pages and verified by reading it back, keeps a recoverable prior version for every modified or trashed file, and ends with a report naming each file touched, each backup or copy created, and any part of the request Pages could not perform.

## Principles

- **Body Text First**: Treat reading and editing body text (paragraphs, insertions, replacements, deletions, find-and-replace) as the capability that must succeed, and serve formatting, tables, images, and shapes as secondary operations built on the same mechanism.
- **Native Writes Only**: Apply every change through Pages scripting on the `.pages` file itself, so the document keeps its layout, template, and Pages-only features across any number of edits.
- **Structured Reads Through Export**: Read documents by exporting a temporary DOCX and parsing it, which returns headings, styles, tables, and footnotes in one pass; delete the temporary export once the read completes.
- **Verify the Dictionary Before Relying On It**: Confirm that a Pages scripting class or property exists in the installed version's dictionary before building an operation on it, and report the operation as unsupported when it is absent.
- **Preflight Before Touching Files**: Confirm Pages.app, Automation permission, and the target file's presence and download state before any operation, and stop with a plain explanation when a check fails.
- **Recoverable Every Time**: Make a timestamped backup beside the original before each in-place write, create new files under non-conflicting names, and move deleted documents to the Trash, so every change has a way back.
- **Leave Open Windows Alone**: When the target document is open in Pages, write the change to a separate copy and leave the user's window and unsaved work untouched.
- **Report What Changed and Where**: End each operation by naming the file changed, the backup or copy path, and any requested element (such as footnote edits or layout placement) that the skill could not reach.

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
- **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.
- **For Interacting:** Always consult **`references/interactions.md`**. This file governs human-in-the-loop checkpoints, approval gates, and handoffs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
