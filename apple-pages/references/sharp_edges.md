# Sharp Edges

This document defines the sharp edges used by apple-pages.

---

## Clobbered Unsaved Work

- **Id**: clobbered-unsaved-work
- **Summary**: Editing a document that is already open in Pages commits or discards the user's unsaved changes.
- **Severity**: critical
- **Situation**: The user has `report.pages` open with unsaved edits and asks the agent to change a paragraph; the skill opens the same file, which Pages resolves to the existing window.
- **Why**: Pages returns the open document object rather than a fresh copy from disk, so a save writes the user's half-finished work, and a close without saving throws it away. A backup copied from disk holds neither.
- **Solution**:
    - Run Open-Document Detection before every write.
    - On a match, apply the change through Separate Copy Edit and tell the user the copy's path.
- **Symptoms**:
    - The user finds edits in the file they had not finished or meant to save.
    - The user's open window closes or loses changes.
- **Detection Pattern**: A write to a document whose path matches the file of any document open in Pages at the time of the write.

---

## Missing Pages or Automation Permission

- **Id**: missing-pages-or-permission
- **Summary**: Pages.app is not installed, or macOS denies the agent's host process permission to control it.
- **Severity**: high
- **Situation**: The skill runs on a Mac without Pages, or the terminal or agent app has never been approved under System Settings > Privacy & Security > Automation.
- **Why**: Every operation runs through Pages scripting; without the app or the permission, osascript fails with an application-not-found error or error -1743.
- **Solution**:
    - Run the Preflight Check before touching any file.
    - When Pages is missing, tell the user Pages.app is required and stop.
    - When error -1743 appears, tell the user to allow the host app to control Pages under Privacy & Security > Automation, then retry.
- **Symptoms**:
    - "Can't get application id" or "Application isn't running" errors.
    - "Not authorized to send Apple events to Pages" (-1743).
- **Detection Pattern**: Any osascript call to Pages returning an application-not-found error or error number -1743.

---

## Dataless iCloud File

- **Id**: dataless-icloud-file
- **Summary**: A `.pages` file in iCloud Drive exists in the listing but its contents have been evicted from the Mac.
- **Severity**: high
- **Situation**: The user references a document in iCloud Drive with Optimize Mac Storage enabled.
- **Why**: Copies of a dataless file produce an empty or broken backup, and Pages may stall while it downloads.
- **Solution**:
    - Check for the dataless flag in the Preflight Check and run `brctl download` on the file, then wait until the flag clears before backing up.
- **Symptoms**:
    - A backup far smaller than the original.
    - Pages hangs or times out opening the file.
- **Detection Pattern**: A target file whose extended listing shows the dataless flag, or a backup whose size is a small fraction of the original's.

---

## Package-Directory Pages Files

- **Id**: package-directory-pages
- **Summary**: Some `.pages` documents are package directories rather than single files, so file-only copy commands fail.
- **Severity**: medium
- **Situation**: The target was saved by an older Pages version or with package format, and the backup uses `cp` without `-R`.
- **Why**: A package directory needs a recursive copy; a plain `cp` errors out or copies nothing, leaving the edit with no backup.
- **Solution**:
    - Copy with `cp -R` for every backup and separate copy, and confirm the backup exists before writing.
- **Symptoms**:
    - "is a directory (not copied)" from `cp`.
    - An edit proceeds with no backup on disk.
- **Detection Pattern**: A target path that is a directory, or a copy command for a `.pages` path that lacks the recursive flag.

---

## Unscriptable Footnotes

- **Id**: unscriptable-footnotes
- **Summary**: Footnotes and endnotes appear in reads but are likely unreachable for writing through Pages scripting.
- **Severity**: medium
- **Situation**: The user asks the agent to add, change, or remove a footnote.
- **Why**: The DOCX export carries footnotes, so reads show them, but Pages' scripting dictionary has not been confirmed to expose them as writable objects.
- **Solution**:
    - Run the Dictionary Check for a footnote class; when it is absent, tell the user footnote edits are outside what Pages scripting supports and offer the remaining parts of the request.
- **Symptoms**:
    - A script referencing footnotes fails with "Can't get footnote".
    - The user expects a footnote change that never lands.
- **Detection Pattern**: A write request that names a footnote or endnote, made without a prior dictionary check confirming a footnote class.

---

## Layout Missing From Reads

- **Id**: layout-missing-from-reads
- **Summary**: The DOCX export flattens or drops text boxes and image or shape placement, so reads understate the document's layout.
- **Severity**: medium
- **Situation**: The agent reads a document with floating images or text boxes, then plans an edit or describes the document to the user.
- **Why**: Pages' DOCX export approximates free-floating objects; their position and sometimes their text are absent from the parsed result.
- **Solution**:
    - Flag layout content as approximate in every read report.
    - When an operation targets images, shapes, or text boxes, enumerate them through Pages scripting instead of the export.
- **Symptoms**:
    - The agent reports no images in a document that visibly has them.
    - Text-box contents are missing from a summary.
- **Detection Pattern**: A read report about a document containing images, shapes, or text boxes that makes no note of layout being approximate.

---

## Wrong Paragraph Index

- **Id**: wrong-paragraph-index
- **Summary**: Paragraph numbers from the DOCX read drift from Pages' own paragraph numbering, so an edit lands on the wrong paragraph.
- **Severity**: high
- **Situation**: The agent locates a paragraph in the exported DOCX, then edits `paragraph N of body text` in Pages.
- **Why**: Empty paragraphs, tables, and text boxes can count differently in the export and in Pages' body text, shifting indexes.
- **Solution**:
    - Before writing, read the target paragraph's text through Pages scripting and confirm it matches the text the user meant.
- **Symptoms**:
    - A neighboring paragraph changes instead of the intended one.
    - Read-Back Verification shows the new text in an unexpected position.
- **Detection Pattern**: A paragraph edit whose target index came from the DOCX export without a matching text check against Pages' own paragraph at that index.

---

## Accumulating Backups

- **Id**: accumulating-backups
- **Summary**: Timestamped backups pile up beside the original over many edits.
- **Severity**: low
- **Situation**: The user asks for a long run of small edits to the same document.
- **Why**: Each in-place write makes a new backup, and the skill performs no automatic cleanup.
- **Solution**:
    - Name each backup in the closing report so the user can see the count, and mention cleanup once backups for a file pass a handful.
- **Symptoms**:
    - A folder full of "(backup ...)" files.
- **Detection Pattern**: More than five backup files for the same document in its folder.
