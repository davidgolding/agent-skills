# Research Search

This file governs the lexical stage of a research pass — everything from receiving the question to holding a ranked candidate set. Traversal of the link graph continues in `references/research_traversal.md`.

---

## 1. Frame the question before querying

Two things are established before any command runs, both internally.

**The governing field.** Name the primary discipline, the sub-specialty where the question actually lives, and any contributing field with a real claim on it. Narrow until one field governs: "fermentation kinetics" over "baking", "Indo-European phonology" over "language". A list of adjacent fields means the sub-specialty is still unlocated — narrow again.

Check the question's surface vocabulary against the operative one, because questions arrive in the wrong field's words: a starter that will not rise is microbiology, a team "motivation" problem is usually incentive design. The operative field supplies query terms the user's phrasing never would, and where the divergence is itself news, it belongs in the answer.

**The failure catalogue.** Ask how a fluent, confident, non-expert answer to *this* question would go wrong, and enumerate concretely:

- the plausible claim that is actually contested
- the rule whose exception governs this case
- the number that would get estimated in place of looked up
- the distinction that collapses under a careless reading
- the question a practitioner would ask first
- the false assumption already inside the user's framing

Most questions yield three or four items. This catalogue is the pass's target: it decides which queries are worth issuing, which hits are worth reading, and — in `research_traversal.md` — which leads are worth a hop. Retrieval without it degrades into keyword matching.

---

## 2. Establish the corpus

Run these before the first query, and name the vault in every command afterward.

```bash
obsidian vaults verbose                      # which vaults exist
obsidian vault="<name>" vault info=files     # how large the corpus is
obsidian vault="<name>" folders              # how it is organized
```

`vaults` and `version` answer from configuration with the app closed; every retrieval command needs a running instance. Confirm the app is live by issuing one broad query whose result cannot be empty — a common word, or `files total` — before treating any empty result as meaningful.

The file count also sets expectations for traversal: it decides whether a full graph dump is practical, and it scales the note budget.

---

## 3. Probe the query grammar

Obsidian's in-app search supports operators — `tag:`, `path:`, `file:`, `line:`, `section:`, `block:`, `/regex/`, `OR`, and leading-dash negation. Whether they survive the `query=` parameter boundary is a property of the installed CLI, so probe rather than assume:

```bash
obsidian vault="<name>" search query="tag:#<a-tag-that-exists>" limit=3
obsidian vault="<name>" tag name="<the same tag>" total
```

A non-empty first result with a matching count means operators pass through; use them. An empty first result against a non-zero count means they do not — fall back to:

- plain-text `query=` values, with `path=<folder>` for scoping,
- structural commands (`tag`, `aliases`, `properties`, `base:query`) for what the operator would have done,
- post-filtering of results in the pass itself.

Record the outcome and say in the report which grammar the pass used. Probe once per pass, not once per query.

---

## 4. Build the query set

A single query built from the user's phrasing retrieves the notes that happen to share today's wording. A vault written over years drifts, so plan a ladder and work down it:

1. **The user's terms**, verbatim — this is what they will look for in the output.
2. **The vault's likely vocabulary** — the phrasing the user would have used when writing about this, including older terminology, project names, and personal shorthand. `aliases` and high-count `tags` reveal it.
3. **The field's technical terms** — from §1's operative field, including proper names of theories, methods, and figures the notes would cite rather than name.
4. **The failure catalogue's own terms** — the contested claim's keywords, the exception's name, the collapsed distinction's two sides.

Prefer `search:context` throughout: the matching line is what supports the judgment of whether a hit is relevant, and a filename alone does not.

```bash
obsidian vault="<name>" search:context query="<terms>" limit=20 format=json
obsidian vault="<name>" search query="<terms>" total          # true match count
```

Pair a capped query with `total`. `limit` bounds the files returned, not the matches that exist, so a broad subject and a marginal one both return a short list; the count is what distinguishes them and what tells you to raise the cap or scope by folder.

---

## 5. Pivot through structure

The vault's own organizing structures are retrieval paths, not filters on text search. Reach for them when text queries return too little, too much, or hits clustered in one corner of the vault.

```bash
obsidian vault="<name>" tag name="<tag>" verbose          # every file carrying a tag
obsidian vault="<name>" tags sort=count counts            # the vault's real topic map
obsidian vault="<name>" aliases verbose                   # alternate names notes travel under
obsidian vault="<name>" properties name="<prop>" counts    # notes declaring a property
obsidian vault="<name>" property:read name="<prop>" file="<note>"
obsidian vault="<name>" bases                             # saved structured views
obsidian vault="<name>" base:query file="<base>" view="<view>" format=json
obsidian vault="<name>" files folder="<folder>"            # folder as a topic proxy
obsidian vault="<name>" outline file="<note>" format=tree  # where inside a long note to read
```

`tags sort=count counts` is the cheapest map of what the vault is actually about, and often supplies the vocabulary rung §4 was missing. `outline` decides where to read inside a long note, which keeps a hit from costing a full read.

---

## 6. Rank the candidates

Fold the query set's results into one candidate list before any traversal begins:

- **De-duplicate** by path; a note retrieved by three rungs of the ladder is a strong signal, not three candidates.
- **Score against the failure catalogue** — which item of it could this note supply? A note matching no item is a keyword hit, not a candidate, however many times it matched.
- **Prefer argument over inventory.** A note that makes a claim outranks a bibliography, reading list, or index that merely mentions the terms. Those become routing tables for traversal, not evidence.
- **Read the strongest few in full**; leave the rest as seeds for traversal to reach or drop.

The output of this stage is a small seed set with a reason attached to each seed. Hand it to `references/research_traversal.md`.

---

## 7. Check sufficiency before continuing

Before moving to traversal, state to yourself what would change this answer, which parts rest on solid reading as against inference, and what still needs looking up. Where any of the three comes back empty, the query set was too narrow — return to §4 and add a rung.

---

## 8. Report silence as a finding

A genuinely empty result is evidence about the vault, and useful. Report it as such only once §2 confirmed the app and vault and §3 verified the query grammar; otherwise the silence is a capability failure wearing a finding's clothes.

When the vault is genuinely silent, say so and name what was tried — the query set, the pivots, and the folders scoped — so the user can see the difference between a vault that holds nothing on the subject and a search that missed. A named gap is something they can act on.
