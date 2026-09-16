# Validations

This document defines the validations used by obsidian-assistant.

---

## Vault Flag Must Lead

- **Id**: vault-flag-first-parameter
- **Severity**: warning
- **Type**: syntax
- **Pattern**: A command including `vault=` anywhere other than as the first parameter.
- **Message**: `vault=` must be the first parameter for the CLI to apply it correctly.
- **Fix Action**: Move `vault="<name>"` to immediately follow the command name.
- **Applies To**:
    - obsidian CLI commands

---

## Research Pass Must Name Its Vault

- **Id**: research-pass-vault-explicit
- **Severity**: error
- **Type**: instruction
- **Pattern**: Two or more retrieval commands issued as one research pass with `vault=` absent from any of them.
- **Message**: Every command in a research pass must carry `vault="<name>"`, since focus can shift between commands and a pass against the wrong vault is indistinguishable from a correct one.
- **Fix Action**: Resolve the vault with `vaults`, confirm it with the user when the request does not name one, and prefix every command in the pass with `vault="<name>"`.
- **Applies To**:
    - obsidian CLI research passes

---

## Tag Cannot Start With A Digit

- **Id**: tag-first-character
- **Severity**: error
- **Type**: regex
- **Pattern**: `#[0-9]`
- **Message**: A tag cannot start with a digit.
- **Fix Action**: Prefix the tag with a letter or underscore, or move the digit later in the tag.
- **Applies To**:
    - inline tags
    - frontmatter `tags` values

---

## Multiline Content Must Use Escapes

- **Id**: multiline-content-escaping
- **Severity**: warning
- **Type**: syntax
- **Pattern**: A CLI `content=` value containing a literal newline or tab character instead of `\n`/`\t`.
- **Message**: Multiline CLI content must use `\n` and `\t` escapes, not literal newlines or tabs.
- **Fix Action**: Replace literal newlines/tabs in the parameter value with `\n`/`\t`.
- **Applies To**:
    - obsidian CLI `create`/`append` and similar content parameters

---

## Embed Requires The `!` Prefix

- **Id**: embed-vs-link-prefix
- **Severity**: error
- **Type**: syntax
- **Pattern**: A wikilink intended to embed content that is missing the leading `!`.
- **Message**: Embedding a note, image, or PDF requires the `!` prefix before the wikilink; without it, the syntax produces a link, not an embed.
- **Fix Action**: Add `!` immediately before `[[`.
- **Applies To**:
    - OFM embed syntax

---

## Empty Result Requires A Verified Retrieval Path

- **Id**: empty-result-unverified-path
- **Severity**: error
- **Type**: instruction
- **Pattern**: A report characterizing the vault as silent on a subject without a prior command in the same pass having returned non-empty output.
- **Message**: An empty result is evidence about the vault only once the retrieval path is verified; a closed app, an unsupported operator, and a mistargeted vault all produce the same silence.
- **Fix Action**: Confirm the app is running and the vault is correct, probe the query form against a value known to exist, then report the empty result as a finding and name the queries and pivots tried.
- **Applies To**:
    - research pass reports

---

## Operator Queries Require A Probe

- **Id**: operator-query-unprobed
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A `query=` value containing `tag:`, `path:`, `file:`, `line:`, `section:`, `/regex/`, ` OR `, or leading-dash negation, with no prior probe of that operator in the pass.
- **Message**: Operator support inside `query=` is a property of the installed CLI and must be probed before a pass depends on it.
- **Fix Action**: Probe the operator against a value known to exist; on an empty probe, fall back to plain-text queries with `path=` scoping and post-filtering, and record the operator as unavailable in the report.
- **Applies To**:
    - obsidian CLI `search`/`search:context` queries

---

## Single-Query Retrieval

- **Id**: single-query-retrieval
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A research pass whose lexical stage issued one query, or issued only queries using the user's own phrasing.
- **Message**: One literal query retrieves the notes that share the user's current phrasing and misses the notes that say the same thing in the vault's older or the field's technical vocabulary.
- **Fix Action**: Issue a planned query set spanning the user's terms, the vault's likely vocabulary, and the field's technical terms, and pivot through tags, aliases, properties, and bases before concluding.
- **Applies To**:
    - research pass retrieval stages

---

## Vault Claim Without A Resolving Citation

- **Id**: vault-claim-uncited
- **Severity**: error
- **Type**: instruction
- **Pattern**: A claim about what the vault says, carrying no `[[note]]`, `[[note#heading]]`, or `[[note#^block]]` citation, or carrying one whose target was never read in the pass.
- **Message**: Every vault claim must carry a citation that resolves, copied from the note's own text or its `outline` output rather than composed from memory.
- **Fix Action**: Attach a citation to the note actually read, verifying the heading or block ID against that note's content, or move the claim into the labeled background section if it is not vault evidence.
- **Applies To**:
    - research pass syntheses

---

## Background Knowledge Blended With Vault Evidence

- **Id**: background-blended-with-evidence
- **Severity**: error
- **Type**: instruction
- **Pattern**: Uncited subject-matter claims appearing among cited vault findings rather than under their own labeled section.
- **Message**: Uncited background positioned among cited findings inherits their authority, leaving the user unable to tell their notes from the agent's knowledge.
- **Fix Action**: Move background scholarship and practice into an explicitly labeled section outside the vault findings, and name the vault's gap it is covering.
- **Applies To**:
    - research pass syntheses

---

## Unvouched Bibliographic Specific

- **Id**: unvouched-specific
- **Severity**: error
- **Type**: instruction
- **Pattern**: An author, title, year, journal, DOI, statistic, or standard figure stated without having been read from a vault note or otherwise verified.
- **Message**: A well-formed reference persuades in proportion to how little the reader can check it, which makes an invented specific the costliest available error.
- **Fix Action**: State only specifics read in the pass; where confidence falls short, describe the source by type ("the major replication attempts in the mid-2010s") so the user can locate it.
- **Applies To**:
    - research pass syntheses
    - OFM notes written from a research pass

---

## Stopping Condition Unreported

- **Id**: stopping-condition-unreported
- **Severity**: warning
- **Type**: instruction
- **Pattern**: A research pass report that omits which of saturation, lead floor, or budget ended the traversal.
- **Message**: A pass that stopped on budget and a pass that stopped on saturation warrant different trust, and the output is otherwise identical.
- **Fix Action**: Name the stopping condition, and when it was the budget, list the leads that would have been followed next.
- **Applies To**:
    - research pass reports

---

## Write During A Read-Only Pass

- **Id**: write-during-research-pass
- **Severity**: error
- **Type**: instruction
- **Pattern**: A `create`, `append`, `prepend`, `property:set`, `rename`, `move`, `delete`, or `template:insert` command issued during a research pass before the user accepted the research note.
- **Message**: A research pass is read-only; the research note is a single explicit write the user accepts or declines after the synthesis.
- **Fix Action**: Remove the write from the pass, hold pass state in the report, and offer the research note once the synthesis is delivered.
- **Applies To**:
    - obsidian CLI research passes

---
