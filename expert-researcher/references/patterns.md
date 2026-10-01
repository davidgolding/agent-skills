# Expert Researcher Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by expert-researcher.

## Patterns

- **Name**: Faceted Query Decomposition
- **Description**: Break the prompt into facets before searching: the core question; the implicit sub-questions an expert would need answered first; the key concepts, each with its controlled vocabulary, synonyms and field-specific terms of art; the time scope (settled history, current consensus, live frontier); and the kind of evidence that would answer it (formal proof, experiment, observational data, historical record, practitioner consensus). Each sub-question becomes a candidate line of inquiry.
- **When**: The first step on every prompt in research mode, before any search call.
- **Example**:
```
    Prompt: "What are the ramifications of the amplituhedron for physics?"
    Core question: what does the amplituhedron change about how physics is formulated?
    Sub-questions: what it computes (scattering amplitudes in planar N=4 SYM);
      how it relates to positive geometry and the positive Grassmannian;
      what "locality and unitarity emerge" means and how strong that claim is;
      whether it extends beyond N=4 SYM (non-planar, QCD, gravity, cosmology);
      what remains open or disputed.
    Vocabulary: amplituhedron, positive Grassmannian, on-shell diagrams,
      BCFW recursion, canonical forms, positive geometry, associahedron.
    Time scope: 2013 origin through the current frontier.
    Evidence: mathematical proofs and computations; theoretical physics argument.
```

---

- **Name**: Discipline Corridor Mapping
- **Description**: Assign each line of inquiry to the discipline, subfield or cross-disciplinary corridor where primary research on that exact question is published and peer-reviewed. Prefer the specific subfield over its umbrella (hep-th over "physics", algebraic combinatorics over "math"). Add an adjacent corridor when a second field holds a distinct, relevant expertise, such as philosophy of physics on emergence claims. Each line carries one precise question and one named home.
- **When**: Turning decomposed facets into the set of lines of inquiry.
- **Example**:
```
    L1  What the amplituhedron computes and how          -> hep-th, scattering amplitudes
    L2  Positive geometry as a mathematical object        -> algebraic combinatorics, positive geometry
    L3  Emergent locality and unitarity: what is claimed  -> hep-th + philosophy of physics
    L4  Extensions beyond planar N=4 SYM                  -> hep-th; cosmology (cosmological polytopes)
```

---

- **Name**: Depth Scaling
- **Description**: Choose a depth tier from the prompt and apply its default budget. A depth or time budget the user states replaces the tier ("quick take" means shallow; "exhaustive" means deep with a raised hop cap).
- **When**: After decomposition, before the plan statement.
- **Example**:
```
    Tier     | Prompt shape                                   | Lines | Hops per line | Plan gate
    shallow  | single fact, definition, date, quick check     | 1-2   | up to 2       | state and continue
    medium   | how/why question within one field              | 2-4   | up to 4       | state and continue
    deep     | ramifications, state of a field, cross-field   | 3-7   | up to 8       | present and wait
    Ambiguous prompts take the plan gate at any tier.
```

---

- **Name**: Source Precedence
- **Description**: Choose the source base in this order: a corpus the user supplies; model knowledge alone when the user directs it; otherwise live web and scholarly sources. Within live sources, seed from review articles, handbooks and reference works (for example, Stanford Encyclopedia of Philosophy, Annual Reviews, Living Reviews), then move to primary peer-reviewed papers and preprints, then expert commentary. Use scholarly indexes with citation graphs, such as OpenAlex, Semantic Scholar, arXiv, PubMed and Crossref, for traversal.
- **When**: Opening each line of inquiry and choosing where each hop goes next.
- **Example**:
```
    L2 seed: a recent review of positive geometry (via Semantic Scholar search)
    Hop 1: its key cited papers (backward) -> Arkani-Hamed & Trnka 2013; Postnikov on the positive Grassmannian
    Hop 2: recent papers citing the seed (forward) -> canonical forms; amplituhedron triangulation proofs
```

---

- **Name**: Snowball Hop
- **Description**: Each hop takes the current frontier of sources and expands it along one or more trails: backward (works it cites), forward (works citing it), author (other work by its key authors), and term (new vocabulary it introduces, searched afresh). Read abstracts and key sections first and open full text when a claim needs its exact support. Record the hop's yield in the ledger before the next hop.
- **When**: Every gathering step within a line of inquiry.
- **Example**:
```
    Hop 3 (L3): forward trail from the emergent-unitarity paper
      -> 2 new papers: one proof extending the claim, one critique of "emergence" wording
      Ledger: +1 novelty (proof extension), +1 perplexity (what counts as emergence)
```

---

- **Name**: Novelty-Perplexity Ledger
- **Description**: Keep one ledger per line, or one shared ledger in sequential mode. A novelty is a finding not yet recorded; a perplexity is an open problem, dispute, unexplained result or contradiction between sources. Record each entry as one sentence with its source and a certainty mark. Treat an entry that restates an existing one in different words as a duplicate. A line is saturated when two consecutive hops add no new entries, and stopped at budget when it reaches the tier's hop cap first.
- **When**: After every hop, and as the stop test for each line.
- **Example**:
```
    N4  [settled]      Amplituhedron volume form reproduces tree-level planar N=4 amplitudes  (Arkani-Hamed & Trnka 2013)
    P2  [contested]    Whether locality and unitarity "emerge" or are encoded in positivity     (critique, 2021)
    Hop 5: +0 new   Hop 6: +0 new   -> L3 saturated
```

---

- **Name**: Line Brief
- **Description**: Have each line of inquiry return a compressed brief of at most about 600 words: the line's question and discipline; its findings, each with a citation and certainty mark; its open perplexities; the expert-register phrasing of its two or three central claims; its status (saturated, or stopped at budget with the hop count); and its source limitations, such as abstract-only access or a thin literature.
- **When**: The return format for every line-of-inquiry subagent, and the record kept per line in sequential mode.
- **Example**:
```
    L3 - Emergent locality/unitarity (hep-th + philosophy of physics)
    Findings: ... [settled] (cite) ... [contested] (cite)
    Perplexities: P2 ...
    Expert phrasing: "Locality and unitarity follow from the positivity of the geometry"
    Status: saturated after 6 hops
    Limits: one critique paywalled; abstract only
```

---

- **Name**: Fan-Out with Sequential Fallback
- **Description**: When the harness can spawn subagents, give each line of inquiry its own subagent. Pass it the line's question, discipline, vocabulary, depth budget, source precedence, the ledger and saturation rules, and the Line Brief format, and run the subagents in parallel. When the harness cannot spawn them, run the lines one after another in a single agent with one shared ledger, so overlap between lines registers as duplicates as soon as it appears.
- **When**: Starting the gathering phase.
- **Example**:
```
    Harness has Agent/Task tool -> 4 subagents (L1-L4) in one batch -> 4 briefs
    No subagent tool            -> L1, then L2, ... with one ledger; L2 hops that repeat L1 entries count as duplicates
```

---

- **Name**: Cross-Line Merge
- **Description**: Combine the briefs into one body of findings. Collapse duplicate findings across lines and keep the strongest citation. Reconcile conflicts by naming them as perplexities rather than picking a side silently. Surface connections where one discipline's finding explains or constrains another's. Use the combined perplexities to identify where the frontier lies.
- **When**: After every line has saturated or stopped at budget, before presentation.
- **Example**:
```
    L2 and L4 both report canonical forms of positive geometries -> one finding, two citations
    L1 says "unitarity emerges"; L3 critique contests the wording -> one contested perplexity, both cited
    Connection: L2's positivity theorems are the mathematical content of L3's emergence claim
```

---

- **Name**: Audience Level Inference
- **Description**: Infer the reader's level from the prompt itself: its vocabulary (terms of art versus lay terms), its question shape (asking what something is versus asking about a technical relation), and any self-description. Default to a sophomore undergraduate level when the prompt gives no signal. Move off the inferred level only when learning science clearly favors another, for example when the inferred level would need prerequisites the content cannot supply in the space available. State the level in the plan for deep prompts.
- **When**: During planning, and again when composing the presentation.
- **Example**:
```
    "What's the amplituhedron and why do physicists care?"                -> sophomore undergraduate
    "How does the amplituhedron's canonical form relate to BCFW cells?"  -> specialist (graduate / researcher)
    "Why does bread rise?"                                               -> sophomore undergraduate, lifted:
                                                                            fermentation chemistry, CO2 trapping in the gluten network
```

---

- **Name**: Pedagogical Structure Selection
- **Description**: Choose the answer's structure from the content's shape rather than a fixed template. Open with an advance organizer (the answer in two or three sentences, then a map of what follows). Introduce an abstract idea through a concrete instance before generalizing it. Build from what the reader already knows toward the frontier, and close with what remains open. Match each content shape to its form: a mechanism becomes a causal chain or Mermaid diagram; a comparison becomes a table; a contested frontier becomes a map of positions with their proponents; a procedure becomes a worked example; a quantity becomes a scale or order-of-magnitude anchor. Use markdown, tables and Mermaid or ASCII diagrams only.
- **When**: Composing every presentation the user has not given a format for.
- **Example**:
```
    Amplituhedron, sophomore level:
      1. The answer in 3 sentences (advance organizer)
      2. Concrete anchor: what a scattering amplitude is, with one Feynman-diagram count
      3. The shift: from summing diagrams to computing a volume (Mermaid: old path vs new path)
      4. What it buys: table of claims x certainty
      5. The frontier: map of open problems and who is working on them
```

---

- **Name**: Inline Citation and Certainty Marking
- **Description**: Attach a citation to each substantive claim where it appears, as a markdown link with author and year, such as `([Arkani-Hamed & Trnka 2013](https://arxiv.org/abs/1312.2007))`. Mark each claim's certainty with one of three tags: **[settled]** for broad expert agreement, **[contested]** for live expert disagreement (name the positions), and **[speculative]** for proposals without strong support. Label claims drawn from model knowledge as `(model knowledge, uncited)`. When the user's requested format calls for a different citation style, or for none, follow it.
- **When**: Writing every substantive claim in the presentation.
- **Example**:
```
    The amplituhedron reproduces tree-level planar N=4 amplitudes [settled]
    ([Arkani-Hamed & Trnka 2013](https://arxiv.org/abs/1312.2007)). Whether this
    shows locality "emerging" is [contested]: proponents read it as fundamental,
    critics as a reformulation ([critique, 2021](link)).
```

---

- **Name**: Coverage Note
- **Description**: Close each answer with a short coverage note: the depth tier used, each line with its status (saturated or stopped at budget), the source base (live, corpus or model knowledge), and its limitations, such as paywalled sources, a thin literature, or a recency cutoff.
- **When**: The last section of every research answer.
- **Example**:
```
    Coverage: deep - L1 saturated (5 hops), L2 saturated (4), L3 saturated (6), L4 stopped at budget (8).
    Sources: live web + arXiv/Semantic Scholar. Limits: two papers read as abstracts only.
```

---

- **Name**: Research Mode Persistence
- **Description**: After invocation, treat each subsequent prompt as a research query, including requests phrased as operations ("fix this test" becomes research into the failure and its likely causes, reported back). Leave research mode when the user says to stop, exit or leave research mode, or plainly asks to return to normal assistance, and confirm the exit in one line.
- **When**: Every prompt after invocation.
- **Example**:
```
    User (in research mode): "rename this variable to something clearer"
    Agent: researches naming conventions for that kind of value in the language's style
    guides and literature, reports recommended names with sources, and leaves the file untouched.
```

---

## Anti-Patterns

- **Name**: Register Mirroring
- **Description**: Presenting findings in the register of the sources they came from, so a specialist field's answer reaches a non-specialist in specialist prose.
- **Why**: The reader gets accurate text they cannot use, which defeats the point of gathering expert knowledge.
- **Instead**: Audience Level Inference, then Pedagogical Structure Selection, keeping the expert phrasing in the brief and translating it for the reader.

---

- **Name**: Lowest-Common-Denominator Flattening
- **Description**: Presenting a familiar or non-technical subject as a generic listicle or simplistic tips, without mechanisms, sources or nuance.
- **Why**: It ignores the expert knowledge that exists on everyday subjects and produces answers indistinguishable from low-effort content.
- **Instead**: Audience Level Inference with upward adaptation: name the mechanisms, cite the relevant fields, and keep the rigor at the inferred level.

---

- **Name**: Fabricated Citation
- **Description**: Producing a citation, title, DOI, URL or author list that was not retrieved in the session, including plausible reconstructions from memory.
- **Why**: Fabricated citations look authoritative and are hard for readers to detect, so they do more harm than an honest uncited claim.
- **Instead**: Inline Citation and Certainty Marking with `(model knowledge, uncited)` for anything not retrieved.

---

- **Name**: Umbrella-Discipline Decomposition
- **Description**: Mapping lines of inquiry to broad fields ("physics", "psychology") or to the prompt's surface topics rather than to the subfields where the sub-questions are researched.
- **Why**: Broad mappings pull general-audience sources and miss the specialist literature that holds the strongest knowledge.
- **Instead**: Discipline Corridor Mapping.

---

- **Name**: First-Page Stopping
- **Description**: Ending a line of inquiry after the first few search results, or because the answer already seems sufficient, before the ledger has saturated.
- **Why**: The first results favor popular and older sources, which hides recent work and live disputes.
- **Instead**: Novelty-Perplexity Ledger, run until two consecutive hops add nothing new or the tier's budget is reached.

---

- **Name**: Raw Source Dumping
- **Description**: Returning full abstracts, page text or long quotations from a line of inquiry into the main context, or into the answer.
- **Why**: It floods the orchestrating context, dilutes attention during the merge, and buries findings under source text.
- **Instead**: Line Brief.

---

- **Name**: False Consensus
- **Description**: Presenting a contested or speculative claim as settled, or omitting the expert disagreement the gathering surfaced.
- **Why**: Readers take unmarked claims as established fact, so a missing certainty mark misrepresents the state of the field.
- **Instead**: Cross-Line Merge, keeping conflicts as named perplexities, and Inline Citation and Certainty Marking.

---

- **Name**: Silent Knowledge Fallback
- **Description**: Answering from model knowledge when web tools are unavailable or fail, without telling the user.
- **Why**: The user assumes current, sourced research and cannot weigh the answer's recency or reliability.
- **Instead**: Source Precedence with a plain statement at the top of the output that no live sources were consulted.

---

- **Name**: Operational Drift
- **Description**: Editing files, running code or otherwise acting on an operational prompt while research mode is active.
- **Why**: The user invoked a research mode; acting on their workspace is a side effect they did not ask this skill for.
- **Instead**: Research Mode Persistence: research the prompt and report back.
