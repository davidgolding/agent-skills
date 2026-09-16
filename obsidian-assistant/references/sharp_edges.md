# Sharp Edges

This document defines the sharp edges used by obsidian-assistant.

---

## Vault Ambiguity Without Explicit Target

- **Id**: vault-ambiguity-without-target
- **Summary**: A command runs against the wrong vault when several vaults are open and `vault=` is omitted.
- **Severity**: high
- **Situation**: Multi-vault setups, and any research pass that issues more than one command.
- **Why**: Commands follow the most recently focused vault, which can differ from the vault the user means and can change between commands in the same pass.
- **Solution**:
    - Resolve the vault once with `vaults` and confirm it with the user when the request does not name one.
    - Pass `vault="<name>"` as the first parameter of every command in the pass.
- **Symptoms**:
    - A create, search, or append command succeeds but touches the wrong vault.
    - A research pass returns thin results that look identical to a correct pass over a sparse subject.
- **Detection Pattern**: Command output referencing a vault name the user did not intend, or a multi-command pass in which some commands carry `vault=` and others do not.

---

## Empty Results From A Closed App

- **Id**: empty-results-app-not-running
- **Summary**: Every retrieval command returns nothing because Obsidian is not running, which is indistinguishable from a vault that holds nothing.
- **Severity**: high
- **Situation**: Any command issued before confirming the app is open — especially the first query of a research pass.
- **Why**: The CLI drives a running Obsidian instance; `vaults` and `version` read configuration and answer without one, so a sanity check on those two succeeds while every search, link, and read command comes back empty.
- **Solution**:
    - Confirm the app is running before the first retrieval command by issuing a query whose result is known to be non-empty.
    - Treat an empty result as a capability failure until the retrieval path itself is verified, then report it as a finding.
- **Symptoms**:
    - `vaults` lists vaults normally while `search`, `read`, and `links` all return nothing.
    - Every query in a planned set comes back empty, including the broadest one.
- **Detection Pattern**: A run in which `vaults` or `version` returns output while every content-bearing command returns an empty result.

---

## Unverified Search Operators

- **Id**: unverified-search-operators
- **Summary**: A query built on Obsidian's search operators returns nothing because the CLI does not pass that operator through, and the silence is read as a fact about the vault.
- **Severity**: high
- **Situation**: Composing `query=` values that use `tag:`, `path:`, `file:`, `line:`, `section:`, `/regex/`, `OR`, or leading-dash negation.
- **Why**: The CLI documents `query=` as a text search with its own `path=`, `case`, and `limit` parameters; whether the in-app query grammar survives the parameter boundary is a property of the installed version, not a guarantee.
- **Solution**:
    - Probe one operator against a value known to exist in the vault before the pass relies on it.
    - On an empty probe, fall back to plain-text queries with `path=` scoping and post-filter the results, and say in the report that the operator was unavailable.
- **Symptoms**:
    - An operator query returns nothing while the equivalent plain-text query returns hits.
    - A tag query is empty although `tag name=<tag> verbose` lists files.
- **Detection Pattern**: An operator-bearing query returning zero results in the same pass where a plain-text or structural equivalent returns results.

---

## Graph Dump Unavailable Or Oversized

- **Id**: graph-dump-unavailable-or-oversized
- **Summary**: The traversal plan assumes a full `resolvedLinks` dump that the vault or the app will not deliver.
- **Severity**: medium
- **Situation**: Starting a traversal with `eval` on a large vault, or on a vault in restricted mode.
- **Why**: `eval` is a developer command subject to the app's restrictions, and a mature vault's link graph can exceed what is practical to hold and reason over in one response.
- **Solution**:
    - Size the graph first with a count before requesting the full dump.
    - Fall back to per-note `links` and `backlinks` walking, accept that lead ranking is then local rather than global, and state which mode the pass ran in.
- **Symptoms**:
    - `eval` returns nothing or an error while other commands work normally.
    - A dump succeeds but consumes the context the pass needed for reading notes.
- **Detection Pattern**: An `eval` call against `app.metadataCache` returning empty, an error, or a payload large enough to crowd out the notes the pass still has to read.

---

## Hub Note Expansion Blowup

- **Id**: hub-note-expansion-blowup
- **Summary**: A traversal hits an index, MOC, or daily note and its frontier explodes with leads that share no subject.
- **Severity**: medium
- **Situation**: Expanding links and backlinks from a note whose purpose is to collect links rather than to argue anything.
- **Why**: Hub notes are adjacent to large parts of the vault by design, so graph distance stops tracking topical relevance the moment a hub enters the visited set.
- **Solution**:
    - Score leads against what the question still needs rather than by graph adjacency, so a hub's neighbors compete on substance.
    - Treat a note with high out-degree and no argument as a routing table: harvest its candidates, and decline to expand from it a second time.
- **Symptoms**:
    - One hop multiplies the frontier several times over.
    - Frontier leads span unrelated subjects with no connection to the question.
- **Detection Pattern**: A single expansion contributing an order of magnitude more frontier leads than the hops before it, from a note whose body is predominantly links.

---

## Stale Vault Note Reported As Current

- **Id**: stale-vault-note-as-current
- **Summary**: A note's claim is reported as what is known, when the note records what was known at the time it was written.
- **Severity**: high
- **Situation**: Synthesizing from notes on a subject where practice or scholarship has moved since the notes were taken.
- **Why**: The vault is a record of the user's understanding at a series of past moments, and nothing in a note's text marks it as superseded; a faithful synthesis of the corpus can therefore be a wrong answer to a present-tense question.
- **Solution**:
    - Check note dates and property metadata against the currency the question requires.
    - Where the vault's coverage lags, supply current scholarship or practice in the labeled background section and name the gap rather than silently modernizing the vault's claim.
- **Symptoms**:
    - The synthesis states a position in the present tense that the cited note frames as provisional or recent.
    - Every citation on a fast-moving subject predates the last several years.
- **Detection Pattern**: Present-tense claims in the synthesis citing notes whose dates cluster well before the question's relevant horizon.

---

## Fabricated Or Unresolvable Citation

- **Id**: fabricated-or-unresolvable-citation
- **Summary**: The synthesis carries a citation that does not resolve, or a bibliographic specific that was never read from a note.
- **Severity**: critical
- **Situation**: Composing the synthesis, particularly when a note paraphrases a source without full bibliographic detail.
- **Why**: A well-formed reference persuades in proportion to how little the reader can check it, and a heading or block anchor typed from memory is exactly as plausible on the page as one that resolves.
- **Solution**:
    - Cite only notes actually read in the pass, and copy the heading or block ID from the note's own text or its `outline` output.
    - Where a specific cannot be vouched for, describe the source by type and let the user locate it.
- **Symptoms**:
    - A `[[note#heading]]` or `[[note#^block]]` link fails to resolve in the vault.
    - The synthesis carries an author, year, or DOI that appears nowhere in the notes read.
- **Detection Pattern**: Citations in the synthesis whose target note, heading, or block ID does not appear in the pass's own read output.

---

## Result Cap Mistaken For Corpus Breadth

- **Id**: result-cap-mistaken-for-breadth
- **Summary**: A capped search result set is treated as the full extent of what the vault holds.
- **Severity**: medium
- **Situation**: Any search where `limit` is set or where the default cap applies, on a subject the vault covers widely.
- **Why**: `limit` bounds the files returned, not the matches that exist, so a broad subject and a narrow one both come back as a short list.
- **Solution**:
    - Run `total` alongside a capped query to learn the real match count before drawing conclusions about breadth.
    - Raise the cap or scope by folder when the total indicates the returned set is a slice.
- **Symptoms**:
    - A result set lands exactly at the requested limit.
    - A subject the user describes as well-covered returns the same small number of files as a marginal one.
- **Detection Pattern**: A search returning precisely `limit` files with no accompanying `total` count.

---

## Tag Leading Digit

- **Id**: tag-leading-digit
- **Summary**: A tag beginning with a digit fails to register as a tag.
- **Severity**: medium
- **Situation**: Writing an inline tag or a frontmatter `tags` entry.
- **Why**: Obsidian tag syntax allows numbers within a tag but not as the first character.
- **Solution**:
    - Ensure the first character of any tag is a letter or underscore.
- **Symptoms**:
    - `#2024` renders as plain text instead of a clickable tag.
- **Detection Pattern**: A tag token whose first character after `#` is a digit.

---

## Block ID On Same Line As List Or Quote

- **Id**: block-id-same-line-lists-quotes
- **Summary**: Placing a block ID on the same line as the last item of a list or quote fails to anchor it.
- **Severity**: low
- **Situation**: Adding a `^block-id` to a list or blockquote.
- **Why**: Obsidian requires the block ID on its own line immediately after a list or quote block, unlike a paragraph, where it can trail on the same line.
- **Solution**:
    - Put `^block-id` on a new line directly after the list or quote block.
- **Symptoms**:
    - `[[Note#^block-id]]` fails to resolve to the intended list or quote.
- **Detection Pattern**: A `^block-id` token appearing at the end of a list-item or blockquote line rather than on its own following line.

---

## Plugin Reload Without Error Check

- **Id**: plugin-reload-without-error-check
- **Summary**: A plugin or theme change appears to apply but leaves a silent runtime error unaddressed.
- **Severity**: high
- **Situation**: The develop/test cycle immediately after a code change.
- **Why**: `plugin:reload` reports success even when the reloaded code throws at runtime; only `dev:errors` surfaces that failure.
- **Solution**:
    - Run `dev:errors` immediately after every reload, before treating the change as verified.
- **Symptoms**:
    - A feature does not work in the UI despite `plugin:reload` returning success.
- **Detection Pattern**: `dev:errors` invoked zero times between a `plugin:reload` and a claim that the change works.

---
