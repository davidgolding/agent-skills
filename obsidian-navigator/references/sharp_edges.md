# Obsidian Navigator - Sharp Edges and Gotchas

This reference lists critical failures, risks, and edge cases to watch out for during vault traversal.

## 1. Cyclical Reference Loops
* **The Risk**: Notes in Obsidian frequently cross-reference each other in cycles (e.g., Note A links to Note B, which links to Note A).
* **Prevention**: Maintain a set/list of visited note paths in memory. Never revisit a note path that has already been read during the same query session.

## 2. Unresolved Links (Ghost Notes)
* **The Risk**: Obsidian allows linking to notes that do not exist yet (e.g., `[[Uncreated Note]]`). Running `read` on these will fail or return empty content.
* **Handling**: If `obsidian-cli` returns an error or empty content for a note, log it as unresolved, remove it from the traversal frontier, and choose the next best candidate.

## 3. Obsidian App / Connection Failures
* **The Risk**: `obsidian-cli` relies on a running Obsidian instance with local server connections. If the app is closed, or if the targeted vault is not active/open, commands will fail.
* **Handling**: Catch execution errors. If a command fails, check if the app is open. Output a helpful error message to the user asking them to open Obsidian and load the vault.

## 4. Spaces in Arguments
* **The Risk**: Note names, paths, and vault names often contain spaces. Failing to quote them properly in the terminal command will cause syntax errors.
* **Handling**: Always quote arguments for `vault`, `file`, and `path`.
  * *Correct*: `vault="My Vault" file="Research/Notebase Philosophy.md"`
  * *Incorrect*: `vault=My Vault file=Research/Notebase Philosophy.md`

## 5. Large Notes and Attachments
* **The Risk**: Some notes may contain huge embedded tables, logs, base64 data, or very long text, which could bloat the LLM's context window.
* **Handling**: If note content exceeds a reasonable size (e.g., 20,000 characters), truncate the text or scan it for header lines first to navigate to sections, rather than feeding the entire raw dump directly into the LLM context.
