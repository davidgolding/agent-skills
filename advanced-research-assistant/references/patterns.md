# Advanced Research Assistant Patterns & Anti-Patterns

This document defines the search, navigation, and synthesis patterns used by advanced-research-assistant.

## Patterns

- **Name**: Provenance-First Navigation
- **When**: At the start of any search, before typing a topic keyword.
- **Example**: ```
  Identify which entity (person, office, institution) created or held the
  records before searching by topic. Navigate by Fonds and Series to respect
  the Archival Bond, then search within that scope.
  ```

---

- **Name**: Cognitive Load Externalization
- **When**: While processing large or non-linear documents.
- **Example**: ```
  Externalize working memory: write prosopographical data, chronologies, and
  causal links to notes immediately, freeing attention for analysis rather
  than fact-maintenance. Scan large collections first to find structural
  groupings (by date, hand, series) before reading line by line.
  ```

---

- **Name**: Berrypicking Query Evolution
- **When**: Throughout every search session, from the first query onward.
- **Example**: ```
  Treat each search result as a source of new "berries" — names, terms,
  dates — and let the next query grow from them. Chase footnotes backward
  and citations forward instead of repeating the same starting keywords.
  ```

---

- **Name**: Regex Alternation Search Cycle
- **When**: Formulating and iterating the initial grep search.
- **Example**: ```
  Search with `term1|term2|term3` alternation rather than one keyword.
  Run an exploratory pass, extract new terminology and entities from the
  hits, then formulate a second, refined search using those terms. Keep a
  search log of the query evolution. Prioritize a high-confidence
  sufficient result set; stop once returns diminish or a conflict needs
  the user's input rather than more browsing.
  ```

---

- **Name**: Micro-Macro Spiral
- **When**: While navigating the result set during Deep Research.
- **Example**: ```
  Read one specific file (micro) looking for relationships to the wider
  set (macro), then return to the source with the new understanding and
  re-read it. Repeat, letting each pass deepen the last.
  ```

---

- **Name**: Triangulation
- **When**: Evaluating how much weight a claim can bear in the report.
- **Example**: ```
  Treat a claim backed by one source as provisional. Treat a claim backed
  by three or more independent sources as robust. Search specifically for
  a second and third source before citing a claim as established.
  ```

---

- **Name**: Disconfirmation
- **When**: When several rounds of iteration keep confirming the same hypothesis.
- **Example**: ```
  Deliberately search for a source that could contradict the current
  reading. Introduce it into the analysis even if it complicates the
  narrative, to break a tightening confirmation spiral.
  ```

---

- **Name**: Historical-Language Search
- **When**: Choosing search terms for any query.
- **Example**: ```
  Search using the terminology the historical actors themselves used —
  including euphemisms, coded language, and period spelling — instead of
  contemporary or academic terms. Adopt a "foolish witness" stance:
  assume nothing about period norms or procedures, and ask "why did they
  do it *that* way?" for each one encountered.
  ```

---

- **Name**: External Cognition
- **When**: Immediately after any discovery worth keeping.
- **Example**: ```
  Write the discovery down in the project's files as soon as it's found,
  using the files themselves as cognitive support rather than holding the
  finding in working memory for later.
  ```

---

- **Name**: Context-Aware Query Refinement
- **When**: Formulating the next query in an ongoing research session.
- **Example**: ```
  Draw the next search term from what has already been discovered this
  session — a name, date, or phrase surfaced two queries ago — rather than
  returning to the original prompt's wording.
  ```

---

- **Name**: Serendipity Parking Lot
- **When**: Encountering an interesting document that doesn't fit the current argument.
- **Example**: ```
  Record it in a dedicated "Parking Lot" note instead of discarding it —
  it may become significant once the argument develops further.
  ```

---

- **Name**: Information Foraging
- **When**: Deciding whether to keep searching a given source cluster or move on.
- **Example**: ```
  Treat each cluster of sources as a "patch." If a patch yields low value,
  pivot to the next one quickly. If a "scent" of relevance is detected,
  forage that patch deeply before moving on.
  ```

---

- **Name**: Query-Type Classification
- **When**: Assembling a Deep Research round, before formulating refined queries.
- **Example**: ```
  Classify the query as Person-centered, Event-centered, Concept-centered,
  Comparative, or Temporal, and let that classification shape which
  sources and search terms come next.
  ```

---

- **Name**: Evidence Record Fields
- **When**: Recording any piece of evidence found during Deep Research.
- **Example**: ```
  For each piece of evidence, record Who (person/entity), Where (full
  file path), When (composition date and event date), What (quote or
  summary), and Type/Diplomatics — Extrinsic (physical form), Intrinsic
  (Protocol/Text/Eschatocol), and Context (immediate, local, macro).
  ```

---

- **Name**: Multi-Strategy Search
- **When**: Assembling any search round, before deciding it's sufficient.
- **Example**: ```
  Combine entity-based (Provenance-First Navigation), topic-based
  (keyword/regex), and temporal (date-range) search strategies rather
  than relying on only one, so a gap in one strategy is covered by
  another.
  ```

---

- **Name**: Abductive Hypothesis Formation
- **When**: Before formulating refined queries for a Deep Research round.
- **Example**: ```
  State the current assumptions about the topic, then formulate a
  provisional hypothesis via abductive reasoning — the best explanation
  given the evidence so far — and let that hypothesis, not just the
  prior query, shape the next search.
  ```

---

- **Name**: Gap Anticipation
- **When**: Reviewing the initial result set before the next Deep Research round.
- **Example**: ```
  Explicitly name what's NOT included in the current result set — a
  missing time period, actor, or genre — and target the next search
  round at closing that specific gap rather than deepening on what's
  already found.
  ```

---

- **Name**: Failure Analysis
- **When**: A search round returns a null result.
- **Example**: ```
  Classify the null result as a theory failure (wrong hypothesis), a data
  failure (source doesn't exist or survive), or a method failure (wrong
  search strategy) before deciding the next move.
  ```

---

- **Name**: Pattern Recognition
- **When**: Synthesizing findings across multiple sources for the report.
- **Example**: ```
  Identify commonalities, variations, outliers, and silences across the
  source set. Apply Decolonial Protocols by reading against the grain for
  unintended evidence of resistance or agency in the silences.
  ```

---

- **Name**: Source Criticism
- **When**: Evaluating any individual source before citing it.
- **Example**: ```
  Assess the temporal gap between composition and the events described
  (memory-distortion risk), the intended audience, the purpose (apologetic,
  pedagogical, polemical, political, personal), and likely bias
  (institutional/personal, gendered, elite/common, insider/outsider).
  ```

---

- **Name**: Causal Architecture
- **When**: Building a causal claim in the analysis.
- **Example**: ```
  Distinguish preconditions (structural, long-term factors), precipitants
  (medium-term events that raised the probability), and triggers
  (the immediate spark) rather than treating cause as a single factor.
  ```

---

- **Name**: Hermeneutical Spiral
- **When**: Writing the Analytical Synthesis section of the report.
- **Example**: ```
  Move from a specific passage (micro) to the broader pattern across the
  corpus (macro), then spiral back to the specific passage and ask
  whether it now reads differently in light of the macro pattern.
  ```

---

- **Name**: Counterfactual Minimal Rewrite
- **When**: Testing whether a causal claim in the analysis actually holds.
- **Example**: ```
  Change exactly one variable in the causal chain ("minimal rewrite") and
  ask whether the outcome would still occur. If it would, the changed
  factor is contingent, not necessary.
  ```

---

- **Name**: Research Report Shape
- **When**: Assembling the final deliverable after Deep Research.
- **Example**: ```
  State Sources Searched, Coverage Percentage, Confidence Level, and Known
  Gaps up front. Structure Findings as Summary Answer, Evidence Matrix
  (Toulmin: Claim -> Data -> Warrant), Key Findings, Comparative Analysis
  (if applicable), Research Perplexities, and Recommended Next Steps.
  ```

---

## Anti-Patterns

- **Name**: Contemporary-Jargon Search
- **Why**: Modern or academic terminology doesn't match the vocabulary in period sources, so it silently misses relevant hits and projects modern assumptions onto historical actors.
- **Instead**: Historical-Language Search

---

- **Name**: Single-Keyword Search
- **Why**: A single keyword misses spelling variants, synonyms, and related entities that regex alternation would catch in one pass.
- **Instead**: Regex Alternation Search Cycle

---

- **Name**: Static Query Lock-In
- **Why**: Repeating the same starting keywords across a session ignores everything already discovered and caps the search at the user's original wording.
- **Instead**: Berrypicking Query Evolution

---

- **Name**: Echo-Chamber Iteration
- **Why**: When every new round of evidence confirms the existing hypothesis without adding nuance, the search has stopped testing the hypothesis and started decorating it.
- **Instead**: Disconfirmation

---

- **Name**: Uncorroborated Single-Source Claim
- **Why**: A claim resting on one source carries the risk, bias, and error of that single source into the report as if it were established fact.
- **Instead**: Triangulation
