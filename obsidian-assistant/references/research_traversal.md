# Research Traversal

This file governs the traversal stage of a research pass — from the seed set produced by `references/research_search.md` through the stopping decision, the synthesis, and the offered research note.

A pass runs autonomously: it plans, snowballs, stops on its own judgment, and reports once. The user steers by re-running with a sharper question, which means the stopping rule and the report carry the weight that a mid-pass checkpoint would otherwise carry.

---

## 1. Acquire the graph

Prefer the whole graph in one call, so leads can be ranked globally rather than by whatever the current note happens to link to.

```bash
obsidian vault="<name>" eval code="Object.keys(app.metadataCache.resolvedLinks).length"
obsidian vault="<name>" eval code="JSON.stringify(app.metadataCache.resolvedLinks)"
obsidian vault="<name>" eval code="JSON.stringify(app.metadataCache.unresolvedLinks)"
```

Size it before dumping it. `resolvedLinks` maps every source path to its targets and their counts; on a large vault the full payload can crowd out the notes the pass still has to read. Dump it when the vault is small enough to hold; otherwise walk.

**Fallback — per-note walking.** When `eval` returns nothing (restricted mode) or the graph is too large:

```bash
obsidian vault="<name>" links file="<note>" format=json
obsidian vault="<name>" backlinks file="<note>" counts
```

Lead ranking is then local: leads compete only against the current note's neighbors, not against the whole frontier. That is a real loss of judgment quality, so **state which mode the pass ran in** and let the user weigh the result accordingly.

Two graph-wide commands are worth running in either mode, because they characterize the corpus rather than a note:

```bash
obsidian vault="<name>" orphans        # notes nothing links to — invisible to traversal
obsidian vault="<name>" unresolved verbose   # links to notes that do not exist yet
```

Orphans never appear as leads, so a subject held mostly in orphaned notes is reachable only through the lexical stage — worth saying in the report. Unresolved links are the user's own record of intended-but-unwritten notes: a map of where they know their thinking is incomplete.

---

## 2. Seed and expand

Seeds come from `research_search.md` §6, each carrying the reason it was chosen.

Expand each seed over **outgoing links and backlinks together**. A note that cites the seed is as much a lead as one the seed cites, and backlinks are where a vault records "this later thought bears on that earlier one" — the direction in which understanding accumulated.

For each candidate before reading it in full:

```bash
obsidian vault="<name>" outline file="<candidate>" format=tree
obsidian vault="<name>" backlinks file="<candidate>" counts
```

`outline` tells you which section to read; `counts` tells you how heavily the vault leans on this note.

---

## 3. Score every lead

A lead earns a hop by supplying something the question still needs. Score against the failure catalogue from `research_search.md` §1 — not against generic relevance, and never by link order.

| Signal | Reading |
|---|---|
| Can supply an open item of the failure catalogue | Follow — this is the only positive signal that matters |
| Reached by several independent paths (co-citation, shared tag, and search) | Follow — convergence from unrelated directions is the strongest structural evidence |
| Makes a claim, argues, or records a decision | Follow ahead of notes that only mention the terms |
| Collects links without arguing (index, MOC, daily note) | Harvest its candidates, then decline to expand from it again |
| Restates what is already gathered | Drop — this is saturation arriving one note at a time |
| Matched on keyword alone, no catalogue item | Drop, however many times it matched |

Record the drop reasons. They are half the report: the user needs to see what was passed over and why, not only what was read.

---

## 4. Stop on the first condition to fire

Three conditions run concurrently. The pass ends when any one fires, and the report names which.

**Novelty saturation** — newly visited notes stop changing the answer. Measured against the failure catalogue, not against note count: a hop that adds five notes, none of which touches an open catalogue item, is saturation even though the frontier grew.

**Lead-quality floor** — the best remaining lead cannot supply an open catalogue item. Abandoning a weak branch early is the point; exhausting it is `Graph Exhaustion` in `references/patterns.md`.

**Budget ceiling** — the hop and note allowance is spent. Default to **3 hops from seed** and **25 notes read**, scaled by the `vault info=files` count from `research_search.md` §2: a vault of a few hundred notes warrants less, a vault of several thousand warrants more. The ceiling exists so a pass terminates even when the two quality conditions never fire.

When the budget is what ended the pass, **list the leads that would have been followed next**. That is the difference between a pass the user can resume and one they must redo.

---

## 5. Compose the synthesis

Reconstruction is scaffolding; the answer is the building. Measure the synthesis by how much of what was gathered actually reaches the user's question — keep what changes the answer, drop the rest — and answer at the scope and in the form the user asked for. A request for one sentence gets the whole pass and one sentence.

Open with the answer. Then, in three parts:

**Vault findings.** Every claim carries a citation that resolves — `[[note]]`, `[[note#heading]]`, or `[[note#^block]]` — with the heading or block ID copied from the note's own text or its `outline` output, never composed from memory. Where the vault disagrees with itself, report the disagreement as a disagreement and name what would decide it. Where a note's claim is dated and the question is present-tense, say which it is.

**Outside the vault.** Background scholarship and current practice go here, under their own label, covering the gaps the vault leaves. Uncited background positioned among cited findings inherits their authority, which is the failure this separation exists to prevent. Vouch for every specific before stating it — author, title, year, journal, DOI, statistic — and where confidence falls short, describe the source by type ("the major replication attempts in the mid-2010s") so the user can locate it themselves.

**The pass.** Vault name, graph mode (dump or walk), query grammar (operators or fallback), stopping condition, notes read, and the unfollowed frontier. Short — a few lines.

Pitch the register to the person: infer their level from the vocabulary and precision of the question, then hold the content constant and adjust the language. Where the pass exposes a false premise in the question, say so briefly and answer both the question asked and the one that should have been.

---

## 6. Offer the research note

The pass is read-only. No note is created, appended to, or modified — not for progress, not for link repair, not for tag normalization. State plainly that nothing was written, then offer the note and write it only on acceptance.

The note carries what a future pass needs to resume rather than repeat:

```markdown
---
tags:
  - research
date: <YYYY-MM-DD>
---

# Research — <subject>

## Question

<the question as asked, and the operative field it turned out to belong to>

## Findings

<the synthesis, citations intact>

## Outside the vault

<the labeled background, gaps named>

## Pass

- Vault: <name> · Graph: dump | walk · Grammar: operators | plain-text fallback
- Stopped: saturation | lead floor | budget
- Notes read: <n> · Hops: <n>

## Queries tried

<the query set, by rung, with which rungs produced hits>

## Leads not followed

- [[<note>]] — <why it was dropped, or that the budget ran out first>

## Open

<what the vault does not cover, and what would change the answer>
```

Save it with `create ... silent` so the vault does not jump to a new tab, and offer a tag or folder consistent with the vault's own conventions rather than imposing one.
