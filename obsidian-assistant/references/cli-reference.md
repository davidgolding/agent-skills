# CLI Reference

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open — `vaults` and `version` answer from configuration with the app closed, but every content-bearing command returns empty.

## Command reference

Run `obsidian help` to see all available commands, and `obsidian help <command>` for one command's parameters. This is always up to date and takes precedence over this file. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

Focus can change between commands, so a multi-command pass names its vault on every command rather than relying on the default.

## Output formats

Many list commands accept `format=json|tsv|csv` (and `properties` accepts `yaml`), which is what makes their output usable as data rather than as display text. Two more modifiers matter for research:

- `total` — return the count instead of the items; the true match count, unaffected by `limit`
- `limit=<n>` — cap the files returned; caps the result set, not the matches that exist
- `--copy` — copy output to the clipboard

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `silent` to prevent files from opening, and `total` on list commands to get a count.

## Research surface

These are the commands a research pass draws on. Procedure for using them lives in `references/research_search.md` and `references/research_traversal.md`.

### Retrieval

```bash
obsidian search query="<text>" limit=20 case format=json    # files matching text
obsidian search query="<text>" total                        # true match count
obsidian search:context query="<text>" limit=20 format=json  # matching lines, with context
obsidian search query="<text>" path="<folder>"              # scope to a folder
```

`search:context` returns the matching line, which is what supports a relevance judgment; `search` alone returns files. Obsidian's in-app query operators (`tag:`, `path:`, `file:`, `line:`, `section:`, `block:`, `/regex/`, `OR`, leading-dash negation) may or may not pass through `query=` on a given installation — probe one against a known value before relying on them.

### Graph

```bash
obsidian links file="<note>" format=json      # outgoing links
obsidian backlinks file="<note>" counts       # incoming links, with counts
obsidian outline file="<note>" format=tree    # headings, to decide where to read
obsidian orphans                              # notes nothing links to
obsidian deadends                             # notes with no outgoing links
obsidian unresolved verbose                   # links to notes that do not exist
```

The whole link graph is available in one call through `eval` (see below), which is the difference between ranking leads globally and ranking them within one note's neighborhood.

### Structure

```bash
obsidian tags sort=count counts               # the vault's topic map
obsidian tag name="<tag>" verbose             # files carrying a tag
obsidian aliases verbose                      # alternate names notes travel under
obsidian properties name="<prop>" counts      # notes declaring a property
obsidian property:read name="<prop>" file="<note>"
obsidian bases                                # base files in the vault
obsidian base:query file="<base>" view="<view>" format=json
obsidian files folder="<folder>" ext=md
obsidian folders
obsidian recents                              # recently opened files
obsidian random:read folder="<folder>"        # sample the corpus
obsidian wordcount file="<note>" words
obsidian vault info=files                     # corpus size
obsidian vaults verbose                       # every registered vault and its path
```

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
obsidian eval code="Object.keys(app.metadataCache.resolvedLinks).length"
obsidian eval code="JSON.stringify(app.metadataCache.resolvedLinks)"
```

`eval` reaches the app's own metadata cache, which is how a research pass acquires the full link graph in one call rather than one call per note. It is subject to the app's restrictions, so size the result first and keep a per-note fallback ready.

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
