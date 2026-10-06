# Validations

This document defines the validations used by apple-pages.

---

## Target Is a Pages Document

- **Id**: pages-target-extension
- **Severity**: error
- **Type**: regex
- **Pattern**: `\.pages/?$`
- **Message**: The target path must name a `.pages` document.
- **Fix Action**: Ask the user for the correct `.pages` path, or route other formats (`.docx`, `.key`, `.numbers`) to a skill that handles them.
- **Applies To**:
    - Target paths for read, update, delete, and export

---

## Preflight Passed

- **Id**: pages-preflight-passed
- **Severity**: error
- **Type**: semantic
- **Pattern**: An operation that touches a file before confirming Pages.app is installed, Automation permission works, and the target exists and is downloaded.
- **Message**: Run the Preflight Check before any file operation.
- **Fix Action**: Run the Preflight Check from `references/patterns.md`, resolve or report each failure, then begin the operation.
- **Applies To**:
    - Every operation

---

## Backup Exists Before In-Place Write

- **Id**: pages-backup-before-write
- **Severity**: error
- **Type**: semantic
- **Pattern**: An in-place update script run against a document with no timestamped backup beside it from this operation, or with a backup much smaller than the original.
- **Message**: Every in-place write needs a complete backup made first.
- **Fix Action**: Copy the original with `cp -R` to a timestamped backup, confirm it exists at a comparable size, then run the update.
- **Applies To**:
    - Update operations

---

## Open Documents Routed to a Copy

- **Id**: pages-open-doc-copy
- **Severity**: error
- **Type**: semantic
- **Pattern**: A write against a document whose path matches a document open in Pages.
- **Message**: Documents open in Pages receive changes through a separate copy.
- **Fix Action**: Run Open-Document Detection, and on a match apply the change through Separate Copy Edit and report the copy's path.
- **Applies To**:
    - Update operations

---

## Recoverable Delete

- **Id**: pages-recoverable-delete
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `\brm\s+(-[a-zA-Z]+\s+)*[^|;&]*\.pages\b`
    - `\bunlink\b[^|;&]*\.pages\b`
- **Message**: Deletes move the document to the Trash.
- **Fix Action**: Replace the command with Trash-Based Delete from `references/patterns.md`.
- **Applies To**:
    - Shell commands the skill runs

---

## No Binary Format Edits

- **Id**: pages-no-iwa-edits
- **Severity**: error
- **Type**: regex
- **Pattern**:
    - `Index/[^\s]*\.iwa`
    - `\bzip\b[^|;&]*\.pages\b`
- **Message**: Pages documents change only through Pages scripting.
- **Fix Action**: Rewrite the operation with the scripting patterns in `references/patterns.md`.
- **Applies To**:
    - Shell commands the skill runs

---

## Arguments Passed Through argv

- **Id**: pages-argv-arguments
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An osascript invocation whose AppleScript source contains a file path or user-supplied text pasted into a quoted string.
- **Message**: Paths and user text reach AppleScript as arguments.
- **Fix Action**: Move the value into an `on run argv` argument per Arguments Through argv.
- **Applies To**:
    - osascript invocations

---

## Export Format Supported

- **Id**: pages-export-format
- **Severity**: error
- **Type**: schema
- **Pattern**: An export request whose format is outside {PDF, DOCX, EPUB, plain text}.
- **Message**: The skill exports to PDF, DOCX, EPUB, or plain text.
- **Fix Action**: Ask the user to choose one of the four supported formats.
- **Applies To**:
    - Export operations

---

## No-Overwrite Create

- **Id**: pages-create-no-overwrite
- **Severity**: error
- **Type**: semantic
- **Pattern**: A create or export whose output path already exists.
- **Message**: New files take a non-conflicting name.
- **Fix Action**: Append a number or timestamp to the file name until the path is free, and report the final name.
- **Applies To**:
    - Create operations
    - Export operations

---

## Write Verified by Read-Back

- **Id**: pages-read-back
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A create or update reported as complete without an Export-Based Read confirming the change.
- **Message**: Confirm each write by reading the file back.
- **Fix Action**: Run Read-Back Verification and report any mismatch.
- **Applies To**:
    - Create operations
    - Update operations

---

## Closing Report Complete

- **Id**: pages-closing-report
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A final report missing the file changed, the backup or copy path, or any unsupported part of the request.
- **Message**: The closing report names every file touched and every limitation hit.
- **Fix Action**: Add the missing items to the report.
- **Applies To**:
    - Every operation
