# Apple Pages Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by apple-pages.

Script examples use AppleScript through `osascript`. Pages' scripting dictionary varies by version, so confirm each class and property with the Dictionary Check pattern before relying on it.

## Patterns

- **Name**: Preflight Check
- **Description**: Before any operation, confirm that Pages.app is installed, that the agent's host process may control it, and that the target path exists, is a Pages document, and is fully downloaded.
- **When**: At the start of every operation, before reading, copying, or opening any file.
- **Example**:
```
    # 1. Pages.app installed (bundle id lookup works wherever the app lives)
    osascript -e 'id of application id "com.apple.iWork.Pages"' \
      || echo "Pages.app is not installed"

    # 2. Automation permission (error -1743 means access was denied)
    osascript -e 'tell application id "com.apple.iWork.Pages" to count documents'

    # 3. Target exists and is a Pages document (file or package directory)
    [ -e "$TARGET" ] && [[ "$TARGET" == *.pages ]]

    # 4. iCloud file is downloaded (dataless files report the SF_DATALESS flag)
    ls -lO "$TARGET" | grep -q dataless && brctl download "$TARGET"
```

---

- **Name**: Dictionary Check
- **Description**: Read the installed Pages scripting dictionary and confirm that the class or property an operation needs exists before building the script around it.
- **When**: The first time in a session that an operation depends on a class or property beyond documents, body text, paragraphs, and export (for example paragraph styles, footnotes, tables, images, or shapes).
- **Example**:
```
    sdef "$(mdfind 'kMDItemCFBundleIdentifier == "com.apple.iWork.Pages"' | head -1)" \
      | grep -iE 'class name="(table|image|shape|text item|paragraph)"|property name="(paragraph style|font|size|color)"'
```

---

- **Name**: Arguments Through argv
- **Description**: Pass file paths and user text into AppleScript as `on run argv` arguments, so quotes, backslashes, and non-ASCII characters in paths or content reach Pages intact.
- **When**: Every script that receives a path or user-supplied text.
- **Example**:
```
    osascript - "$TARGET" "$NEW_TEXT" <<'APPLESCRIPT'
    on run argv
      set targetPath to item 1 of argv
      set newText to item 2 of argv
      tell application id "com.apple.iWork.Pages"
        set doc to open (POSIX file targetPath)
        set paragraph 2 of body text of doc to newText
        save doc
        close doc saving no
      end tell
    end run
    APPLESCRIPT
```

---

- **Name**: Open-Document Detection
- **Description**: Before writing, compare the target's path against the files of every document already open in Pages, and route to the Separate Copy Edit pattern on a match.
- **When**: Before every update to an existing document.
- **Example**:
```
    osascript - "$TARGET" <<'APPLESCRIPT'
    on run argv
      set targetPath to item 1 of argv
      tell application id "com.apple.iWork.Pages"
        repeat with d in documents
          try
            if POSIX path of (file of d as alias) is targetPath then return "open"
          end try
        end repeat
      end tell
      return "closed"
    end run
    APPLESCRIPT
```

---

- **Name**: Backup Then Edit In Place
- **Description**: When the target is closed in Pages, copy it to a timestamped backup beside the original, then open, edit, save, and close the original.
- **When**: Every update to a document that Open-Document Detection reports as closed.
- **Example**:
```
    STAMP=$(date +%Y%m%d-%H%M%S)
    BACKUP="${TARGET%.pages} (backup $STAMP).pages"
    cp -R "$TARGET" "$BACKUP"   # -R handles package-directory .pages bundles
    # then run the edit script against "$TARGET"
```

---

- **Name**: Separate Copy Edit
- **Description**: When the target is open in Pages, copy the file on disk to a sibling named for the edit, apply the change to that copy, close only the copy, and tell the user the copy's path and that it lacks any unsaved work in their open window.
- **When**: Every update to a document that Open-Document Detection reports as open.
- **Example**:
```
    STAMP=$(date +%Y%m%d-%H%M%S)
    COPY="${TARGET%.pages} (edited $STAMP).pages"
    cp -R "$TARGET" "$COPY"
    # run the edit script against "$COPY"; it closes only the copy's window
    # Report: "report.pages is open in Pages, so I left it alone and applied
    #  the change to 'report (edited 20261006-141500).pages'. That copy reflects
    #  the last saved version and lacks any unsaved edits in your open window."
```

---

- **Name**: Export-Based Read
- **Description**: Read a document by exporting it to a temporary DOCX, then parsing the DOCX package for paragraphs with their heading styles, tables, footnotes, and endnotes; delete the temporary export afterward.
- **When**: Every read, and every verification read after a write.
- **Example**:
```
    TMP=$(mktemp -d)
    osascript - "$TARGET" "$TMP/read.docx" <<'APPLESCRIPT'
    on run argv
      tell application id "com.apple.iWork.Pages"
        set doc to open (POSIX file (item 1 of argv))
        export doc to (POSIX file (item 2 of argv)) as Microsoft Word
        close doc saving no
      end tell
    end run
    APPLESCRIPT
    # Body with styles: word/document.xml (w:pStyle gives Heading1, Title, ...)
    # Notes: word/footnotes.xml and word/endnotes.xml
    unzip -p "$TMP/read.docx" word/document.xml > "$TMP/document.xml"
    # Quick text-only fallback: textutil -convert txt -stdout "$TMP/read.docx"
    rm -rf "$TMP"
```

---

- **Name**: Paragraph-Addressed Body Edit
- **Description**: Address body text edits by paragraph index, located from a fresh read, and apply insert, append, replace, and delete as operations on `paragraph N of body text`; implement find-and-replace by locating matching paragraphs and rewriting only those.
- **When**: Every body-text update, the skill's primary capability.
- **Example**:
```
    tell application id "com.apple.iWork.Pages"
      set bt to body text of doc
      set paragraph 3 of bt to "Replacement paragraph text."          -- replace
      set paragraph 3 of bt to (paragraph 3 of bt) & return & "New."   -- insert after
      delete paragraph 5 of bt                                         -- delete
      make new paragraph at end of bt with data (return & "Appended.") -- append
    end tell
```

---

- **Name**: Template-Based Create
- **Description**: Create a new document from a named Pages template (Blank when none is named), then fill it with drafted content whose headings and body map to the template's paragraph styles, saving under a non-conflicting name.
- **When**: Every create request.
- **Example**:
```
    tell application id "com.apple.iWork.Pages"
      set templateNames to name of every template   -- match the user's request here
      set doc to make new document with properties {document template:template "Blank"}
      set body text of doc to draftedText
      -- apply heading styles per paragraph only after Dictionary Check confirms
      -- the installed version exposes paragraph styles
      save doc in (POSIX file targetPath)
      close doc saving no
    end tell
```

---

- **Name**: Export To Requested Format
- **Description**: Export the document to PDF, DOCX, EPUB, or plain text at the user's location (beside the original by default), opening and closing the source unchanged.
- **When**: Every export request.
- **Example**:
```
    -- format keywords: PDF, Microsoft Word, EPUB, unformatted text
    export doc to (POSIX file outPath) as PDF
    close doc saving no
```

---

- **Name**: Trash-Based Delete
- **Description**: Delete a document by moving it to the Trash through Finder, after the user confirms the exact path, so it stays recoverable.
- **When**: Every delete request.
- **Example**:
```
    osascript - "$TARGET" <<'APPLESCRIPT'
    on run argv
      tell application "Finder" to delete (POSIX file (item 1 of argv) as alias)
    end run
    APPLESCRIPT
```

---

- **Name**: Read-Back Verification
- **Description**: After every write, run an Export-Based Read of the written file and confirm the requested change appears, reporting any difference to the user.
- **When**: After every create and update.
- **Example**: "Verified: paragraph 3 of report.pages now reads 'Replacement paragraph text.' Backup saved as 'report (backup 20261006-141500).pages'."

---

## Anti-Patterns

- **Name**: Binary Format Surgery
- **Description**: Unzipping a `.pages` bundle and editing its `Index/*.iwa` files, or writing a `.pages` file by hand.
- **Why**: IWA is Apple's private, compressed binary format with no public specification; hand edits corrupt documents in ways Pages may refuse to open.
- **Instead**: Native Writes Only, through Paragraph-Addressed Body Edit and the other scripting patterns.

---

- **Name**: DOCX Round-Trip Edit
- **Description**: Exporting to DOCX, editing the DOCX, and importing it back into Pages to save over the original.
- **Why**: Each round trip strips Pages-only layout, template details, and object placement, so the document degrades with every edit.
- **Instead**: Use DOCX only for reads (Export-Based Read); apply every write through Pages scripting.

---

- **Name**: Saving Over an Open Window
- **Description**: Editing and saving the document object already open in the user's Pages window.
- **Why**: The save commits the user's unsaved, possibly half-finished work alongside the skill's change, and the backup copied from disk lacks that work.
- **Instead**: Separate Copy Edit.

---

- **Name**: Permanent Removal
- **Description**: Deleting a document with `rm`, `rm -rf`, or any command that bypasses the Trash.
- **Why**: Removes the only recoverable path for the user's document.
- **Instead**: Trash-Based Delete.

---

- **Name**: Inline String Interpolation
- **Description**: Building AppleScript source by pasting paths or user text into a quoted string.
- **Why**: A quote, backslash, or line break in the path or text breaks the script or alters what it does.
- **Instead**: Arguments Through argv.

---

- **Name**: Assumed Dictionary Support
- **Description**: Writing a script against a Pages class or property (such as paragraph styles or footnotes) without confirming the installed version exposes it.
- **Why**: Pages' dictionary changes between versions; the script fails mid-operation after the backup is made, or silently skips the change.
- **Instead**: Dictionary Check, then report the operation as unsupported when the dictionary lacks it.

---

- **Name**: Whole-Body Rewrite for a Small Edit
- **Description**: Replacing `body text` wholesale to change one paragraph or phrase.
- **Why**: Resetting the full body discards per-paragraph styles, inline formatting, and anchored objects throughout the document.
- **Instead**: Paragraph-Addressed Body Edit on only the paragraphs that change.
