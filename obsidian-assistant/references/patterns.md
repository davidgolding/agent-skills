# Obsidian Assistant Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by obsidian-assistant.

## Patterns

- **Name**: Vault Targeting Default
- **Description**: Let a single ad-hoc command fall through to the most recently focused vault, and name the vault explicitly as the first parameter whenever the choice matters.
- **When**: Running any CLI command, and always at the start of a research pass.
- **Example**:
```
    obsidian search query="test"
    # targets the most recently focused vault

    obsidian vault="My Vault" search query="test"
    # vault= must lead, before any other parameter
```

---

- **Name**: Active-File Default
- **Description**: Omit `file` and `path` to operate on whatever file is currently active in the app.
- **When**: A command accepts `file` or `path` and the user means the note in front of them.
- **Example**:
```
    obsidian read
    # reads the currently active file
```

---

- **Name**: Wikilink-Style File Resolution
- **Description**: Target a note by bare name and let Obsidian resolve it the way it resolves a wikilink, reserving `path=` for cases where the exact vault-root path is known.
- **When**: Targeting a file whose folder or extension is not known for certain.
- **Example**:
```
    obsidian read file="My Note"
    # name only — no folder, no .md extension

    obsidian read path="folder/note.md"
    # exact path from the vault root
```

---

- **Name**: Reload-Verify Loop
- **Description**: Treat a plugin or theme change as unapplied until a reload is followed by an error check and a visual or DOM confirmation.
- **When**: After editing plugin or theme code.
- **Example**:
```
    obsidian plugin:reload id=my-plugin
    obsidian dev:errors
    obsidian dev:screenshot path=screenshot.png
    obsidian dev:console level=error
    # repeat from plugin:reload whenever dev:errors reports a problem
```

---

- **Name**: Wikilink Over Markdown Link
- **Description**: Link notes inside the vault with `[[wikilinks]]`, which Obsidian rewrites automatically when the target is renamed.
- **When**: Linking to another note within the same vault.
- **Example**:
```
    Before: [Project Alpha](Project%20Alpha.md)
    After:  [[Project Alpha]]
```

---

- **Name**: Block-ID Anchoring
- **Description**: Anchor a link to a specific paragraph, list, or quote by giving the block an ID, placing it inline for a paragraph and on its own following line for a list or quote.
- **When**: Citing a passage rather than a whole note or a heading section.
- **Example**:
```
    This paragraph can be linked to. ^my-block-id

    > A quote block

    ^quote-id

    Link to either with [[Note#^my-block-id]]
```

---

- **Name**: Progressive Property Disclosure
- **Description**: Write the three default properties inline on a new note and consult the property reference only when a typed property is needed.
- **When**: Adding frontmatter to a new note.
- **Example**:
```
    ---
    tags:
      - project
    aliases:
      - Alternative Name
    ---
    # consult references/properties.md for date, number, checkbox, and link-typed properties
```

---

- **Name**: Field-First Question Framing
- **Description**: Establish the discipline and sub-specialty that govern a research question before composing any query, narrowing until one field governs and checking the question's surface vocabulary against the operative one.
- **When**: Opening any research pass over the vault.
- **Example**:
```
    Question: "what do my notes say about why the starter keeps failing?"
    Surface field:   baking
    Operative field: microbiology — fermentation kinetics
    Query vocabulary follows the operative field: hydration, inoculation,
    acetic vs lactic, ambient temperature — alongside the user's own words.
```

---

- **Name**: Failure Catalogue As Retrieval Target
- **Description**: Enumerate how a fluent, confident non-expert answer to this specific question would go wrong, then treat that catalogue as the definition of what queries must retrieve and what a lead must contribute.
- **When**: After framing the field, before the first query, and again whenever a lead is scored.
- **Example**:
```
    Catalogue for this question:
      - the plausible claim that is actually contested in the vault
      - the rule whose exception governs this case
      - the number the answer would estimate instead of look up
      - the false assumption already inside the user's framing

    A lead earns a hop when it can supply one of these. A lead that only
    restates what is already gathered does not.
```

---

- **Name**: Reformulation Ladder
- **Description**: Issue a planned set of queries rather than one, covering the user's phrasing, the vault's likely vocabulary for the same idea, and the field's technical terms, and record which rungs produced hits.
- **When**: The lexical stage of any research pass.
- **Example**:
```
    obsidian vault="Repository" search:context query="horizon of expectation" limit=20
    obsidian vault="Repository" search:context query="reception theory" limit=20
    obsidian vault="Repository" search:context query="Gadamer" limit=20
    # user's phrasing, the vault's likely phrasing, the field's proper names
```

---

- **Name**: Structural Pivot Retrieval
- **Description**: Retrieve through the vault's own organizing structures — tags, aliases, properties, folders, bases — as first-class paths rather than as filters on text search.
- **When**: Text queries return too few hits, too many, or hits that cluster in one corner of the vault.
- **Example**:
```
    obsidian tag name="hermeneutics" verbose      # every file carrying the tag
    obsidian aliases verbose                      # alternate names notes travel under
    obsidian properties name="status" counts      # which notes declare the property
    obsidian base:query file="Reading" view="Unread" format=json
```

---

- **Name**: Capability Probe With Fallback
- **Description**: Confirm that an operator, flag, or `eval` capability behaves as expected against the installed CLI before a pass depends on it, and switch to a documented fallback when the probe comes back empty.
- **When**: Before the first operator query and before the graph dump of any pass.
- **Example**:
```
    obsidian search query="tag:#project" limit=3     # probe
    # empty result on a vault known to carry the tag means the operator is
    # unsupported — fall back to plain-text queries plus path= scoping
    # and post-filter the results, and say so in the report
```

---

- **Name**: Graph-Dump-First Traversal
- **Description**: Acquire the whole link graph in one `eval` call so leads can be ranked globally, and fall back to per-note `links` and `backlinks` walking when `eval` is unavailable or the graph is too large to hold.
- **When**: Beginning the traversal stage of a research pass.
- **Example**:
```
    obsidian vault="Repository" eval code="Object.keys(app.metadataCache.resolvedLinks).length"
    obsidian vault="Repository" eval code="JSON.stringify(app.metadataCache.resolvedLinks)"
    # too large or unavailable:
    obsidian vault="Repository" links file="Seed Note"
    obsidian vault="Repository" backlinks file="Seed Note" counts
    # state in the report which mode the pass ran in
```

---

- **Name**: Bidirectional Seed Expansion
- **Description**: Expand each seed over outgoing links and backlinks together, since a note that cites the seed is as much a lead as one the seed cites.
- **When**: Every hop of a traversal.
- **Example**:
```
    obsidian links file="Seed Note" format=json        # what the seed cites
    obsidian backlinks file="Seed Note" counts         # what cites the seed
    obsidian outline file="Candidate" format=tree      # where inside the note to read
```

---

- **Name**: Need-Scored Lead Selection
- **Description**: Score each frontier lead against what the question still needs from the failure catalogue, and follow leads in that order rather than in link order.
- **When**: Choosing the next hop, at every hop.
- **Example**:
```
    Frontier after hop 1:
      [[Reception Theory]]     — supplies the contested claim        → follow
      [[Gadamer Notes]]        — supplies the governing exception    → follow
      [[Reading List 2019]]    — bibliography, no argument           → drop
      [[Daily 2019-04-02]]     — one passing mention, already seen   → drop
```

---

- **Name**: First-To-Fire Stopping
- **Description**: Run a traversal under three stopping conditions at once — novelty saturation, a lead-quality floor, and a hop and note budget — and end the pass on whichever fires first, naming it in the report.
- **When**: Every autonomous research pass.
- **Example**:
```
    Stopped: saturation — hops 3-4 added 6 notes, none of which changed the answer.
    Stopped: lead floor — best remaining lead was a bibliography with no argument.
    Stopped: budget — 3 hops / 25 notes spent. Would have followed next:
             [[Wirkungsgeschichte]], [[Jauss - Literary History]].
```

---

- **Name**: Cited Synthesis With Labeled Background
- **Description**: Compose one synthesis in which every vault claim carries a resolving citation, and keep background scholarship in its own labeled section so uncited context never reads as vault evidence.
- **When**: Reporting the result of a research pass.
- **Example**:
```
    ## What the vault holds
    You frame reception as reader-side completion ([[Reception Theory#^r3]]),
    and your Gadamer notes push back on that ([[Gadamer Notes#Fusion]]).

    ## Outside the vault
    The vault has nothing post-2015 here; the field has largely moved to
    empirical reception studies. Not vault evidence — flagging the gap.

    ## Pass
    Vault: Repository. Mode: graph dump. Stopped: saturation.
```

---

- **Name**: Offered Research Note
- **Description**: Keep the pass read-only, then offer to save a research note carrying the synthesis, the unfollowed frontier, the spent budget, and the queries already tried, so a later pass resumes instead of repeating.
- **When**: After delivering the synthesis of any research pass.
- **Example**:
```
    "Nothing written. Want me to save this as a research note? It would
     carry the two leads I didn't follow and the queries already run."
    # on yes:
    obsidian vault="Repository" create name="Research — Reception 2026-09-16" content="..." silent
```

---

## Anti-Patterns

- **Name**: Guessed Path Resolution
- **Description**: Typing an exact `path=` value from memory instead of resolving the note by name.
- **Why**: The remembered folder, letter case, or extension is often wrong, producing a not-found error that wikilink-style resolution would have avoided.
- **Instead**: Target the note by bare name with `file="My Note"`, and use `path=` only after the exact vault-root path has been confirmed with `files` or `file`.

---

- **Name**: Skipping the Error Check
- **Description**: Reloading a plugin or theme and treating the change as applied without running `dev:errors`.
- **Why**: `plugin:reload` reports success even when the reloaded code throws at runtime, so a broken change passes unnoticed until a later, harder-to-diagnose failure.
- **Instead**: Run `dev:errors` immediately after every reload, fix anything it reports, and reload again before claiming the change works.

---

- **Name**: Markdown-Linking In-Vault Notes
- **Description**: Linking to a note inside the vault with `[text](path.md)`.
- **Why**: A standard Markdown link is not rewritten when the target note is renamed, so the link breaks silently.
- **Instead**: Write `[[Note Name]]`, and keep `[text](url)` for external URLs.

---

- **Name**: Single-Query Retrieval
- **Description**: Running one literal query built from the user's phrasing and treating its hits as the vault's answer.
- **Why**: A vault written over years drifts in vocabulary, so a single query retrieves the notes that happen to share today's phrasing and silently misses the ones that say the same thing in older or more technical terms.
- **Instead**: Plan a query set across the user's phrasing, the vault's likely vocabulary, and the field's technical terms, then pivot through tags, aliases, and properties before concluding.

---

- **Name**: Empty Probe Read As Empty Vault
- **Description**: Taking an empty command result as evidence that the vault holds nothing, when the cause is a closed app, an unsupported operator, or a mistargeted vault.
- **Why**: The two situations are indistinguishable in the output, and reporting a capability failure as a substantive finding tells the user their notes are silent when they are not.
- **Instead**: Confirm the app is running and the vault is correct, probe the operator against a value known to exist, and report an empty result as a finding only once the retrieval path itself is verified.

---

- **Name**: Graph Exhaustion
- **Description**: Following every link and backlink outward until the graph runs out, rather than scoring leads and stopping.
- **Why**: Note-to-note connectivity in a mature vault reaches most of the vault within a few hops, so exhaustive expansion spends the whole pass on notes that never bore on the question while burying the ones that did.
- **Instead**: Score each frontier lead against what the question still needs, follow the best ones, and end the pass on saturation, the lead floor, or the budget — whichever fires first.

---

- **Name**: Blended Evidence
- **Description**: Weaving background knowledge of the field into the synthesis alongside vault findings without distinguishing the two.
- **Why**: An uncited claim positioned among cited ones inherits their authority, leaving the user unable to tell what their notes actually say from what the agent knows.
- **Instead**: Cite every vault claim to a resolving `[[note]]`, `[[note#heading]]`, or `[[note#^block]]` reference, and confine background context to its own labeled section.

---

- **Name**: Invented Specifics
- **Description**: Supplying an author, title, year, journal, DOI, or figure that was not read from a vault note or independently verified.
- **Why**: A well-formed reference persuades in proportion to how little the reader can check it, which makes a fabricated one the costliest error available in a research pass.
- **Instead**: Vouch for each specific before stating it, and where confidence falls short, describe the source by type — "the major replication attempts in the mid-2010s" — so the user can locate it themselves.

---

- **Name**: Writing During a Pass
- **Description**: Creating, appending to, or modifying notes over the course of a research pass — adding links, normalizing tags, saving progress files.
- **Why**: The user agreed to an investigation, not an edit; a pass that leaves changes behind makes its own findings unreproducible and mixes agent writing into the corpus being studied.
- **Instead**: Hold the entire pass read-only, keep state in the report, and offer the research note as a single explicit write the user accepts or declines.

---

- **Name**: Inherited Vault Targeting
- **Description**: Running a multi-command research pass without `vault=`, letting each command follow whichever vault was most recently focused.
- **Why**: With several vaults registered, a pass against the wrong corpus produces output identical in shape to a correct one, and focus can shift mid-pass so a single pass straddles two vaults.
- **Instead**: Resolve the vault once with `vaults`, confirm it with the user when the request is ambiguous, and pass `vault="<name>"` as the first parameter of every command in the pass.

---
