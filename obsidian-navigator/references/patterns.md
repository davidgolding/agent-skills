# Obsidian Navigator - CLI and Traversal Patterns

This reference specifies how to target vaults, execute commands via `obsidian-cli`, and execute step-by-step traversal.

## CLI Execution and Target Selection

### Command Location
The `obsidian-cli` command is usually located at:
`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`

If this path doesn't exist, check the system PATH for `obsidian` or `obsidian-cli`.

### Vault List & Choice
To find which vaults are currently running or registered:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vaults verbose
```
Present the list of names and paths to the user and prompt them to choose a vault before proceeding.

### Targeting a Specific Vault
Prepend `vault=<name>` as an option for all commands to target a specific vault:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vault="Starter" search query="cognitive overhead"
```

---

## Command Patterns

### 1. Keyword Search (Finding Entry Points)
To identify the starting note(s) for a query:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vault="<vault>" search query="<search-text>"
```
This returns a list of matching note paths. Select the top 1-3 most relevant notes as starting points.

### 2. Reading Note Contents
To read the text of a note:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vault="<vault>" read file="<note-name-or-path>"
```

### 3. Listing Outgoing Links
To find what notes are linked inside the current note:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vault="<vault>" links file="<note-name-or-path>"
```

### 4. Listing Backlinks
To find what notes link *to* the current note:
```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian-cli vault="<vault>" backlinks file="<note-name-or-path>"
```

---

## Dynamic Traversal Pattern

When traversing the vault, execute the following state loop:

1. **Query & Search**: Run a text search to find starting notes.
2. **Retrieve Links**: For the current note, fetch both outgoing links and backlinks.
3. **LLM Decision Step**:
   - Compare the original user query, the collected context so far, and the candidate links (both outgoing and incoming).
   - Choose the link that has the highest probability of containing the missing information.
4. **Mark Visited**: Add the chosen note to a `visited` list to avoid loops.
5. **Read & Check**: Read the note content. Check if we have enough context to answer the query. If yes, stop. If no, repeat from step 2.
6. **Limit Check**: Stop traversing if the total notes read hits 15 notes.

---

## Output Citation Pattern

Format the final response focusing strictly on the synthesized summary. Cite all source notes dynamically using footnotes or inline bracket references:

```markdown
The Notebase Philosophy encourages minimizing cognitive load during capture by utilizing a "Shallow Pool" structure where notes are dropped into generic buckets without upfront categorization [1]. For retrieval, a "Deep Net" approach relies on keyword search and internal links to dynamically trace connections rather than folder hierarchies [2].

### References
- [1] Research/Notebase Philosophy.md
- [2] Home.md
```
