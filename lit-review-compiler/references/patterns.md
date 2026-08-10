# Lit Review Compiler Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by lit-review-compiler.

## Patterns

- **Name**: Specificity-Calibrated Scoping
- **Description**: Before searching, classify the input's specificity. Broad topics, fields, or disciplines (e.g., "the ethics of algorithmic bias," "cognitive linguistics") get a short scoping round with the user — time range, sub-fields or theoretical lenses, language, explicit exclusions — before any search begins. Precise, already-bounded research questions (e.g., "Does implicit-bias training measurably reduce hiring discrimination, per RCT evidence since 2015?") skip the round; infer boundaries and state them explicitly near the top of the final report instead.
- **When**: At the start of every compilation run, before the first search query is issued.
- **Example**:
```
    Input: "phenomenology of grief"
    -> Broad. Ask: What time range? Which lineage (Husserl/Heidegger vs. analytic
       philosophy of emotion vs. clinical/psychological)? Any language restriction?

    Input: "Has open-access mandate policy changed citation rates for mandated
    authors, 2010-present?"
    -> Precise. Proceed to search; state in the report opening: "Scope: empirical
       studies of citation-rate effects from OA mandates, 2010-present, excluding
       purely legal/policy-design literature."
```

---

- **Name**: Four-Part Citation Chaining
- **Description**: Supplement keyword search with citation chaining rather than relying on keywords alone — keywords miss historical terminology shifts and recent unindexed work. For every thematic cluster, deliberately populate all four source types: Foundational (the work that introduced the field's core framework), Turning Point (interventions that reframed the debate or exposed a fatal limitation), Consolidator (systematic reviews, meta-analyses, handbooks that stabilize consensus), and Current Frontier (work from roughly the last 24-36 months). Use backward chaining (reference lists of consolidator/seminal texts) to find Foundational and Turning Point sources, and forward chaining (citation indexes) to find who has responded to them since.
- **When**: During the discovery phase, for every thematic cluster identified in the domain.
- **Example**:
```
    Seed: a 2022 meta-analysis on X.
    Backward chain its reference list -> surfaces the 1994 paper that first proposed
    the mechanism (Foundational) and a 2008 paper that overturned the initial
    measure (Turning Point).
    Forward chain (citation index) on both the meta-analysis and the 2008 paper ->
    surfaces 2024-2025 replications and critiques (Current Frontier).
```

---

- **Name**: Tiered Citation Verification
- **Description**: No citation is written into the report until it has cleared `scripts/verify_citation.py`. Run the script with the candidate's title, author, and year. Tier 1 (`api_confirmed`): a scholarly API (Crossref, OpenAlex, or Semantic Scholar) returns a matching record — cite normally. Tier 2 (`secondary_confirmed`): none of the tier-1 APIs match, but Open Library or Google Books confirms it (common for books) — cite normally. Tier 3 (`unverified`): nothing confirms it — still include it, but visibly mark the entry, e.g. "(verified by search evidence only; not independently confirmed)". Run the script against every candidate, including sources that seem "obviously" real, and carry every real-seeming source through to at least its Tier 3 caveated inclusion rather than a silent drop.
- **When**: Immediately before any citation is added to the draft report — treat it as a gate, not a final cleanup pass.
- **Example**:
```
    $ python3 scripts/verify_citation.py --title "Domain Analysis in Information Science" --author "Hjorland" --year 2002
    {"tier": "api_confirmed", "matched": {"source": "crossref", "title": "...", "year": 2002, "id": "10.xxxx/..."}, ...}

    $ python3 scripts/verify_citation.py --title "An obscure 1971 conference proceeding" --author "Doe"
    {"tier": "unverified", "matched": null, "checked": [...], "errors": []}
    -> Include with a visible caveat, per Tier 3.
```

---

- **Name**: Retrieval-Grounded Annotation
- **Description**: Write each entry's annotation only from what was actually retrieved — the abstract, the metadata, snippet text from search results, or full text if it was actually fetched and read. Fill any gap in the retrieved material by shortening the annotation, not by paraphrasing from training knowledge of "what a paper like this probably argues." If all that was retrieved is a title and a one-line abstract, the annotation is necessarily shorter — that is correct behavior, not a defect to compensate for.
- **When**: While drafting every annotated entry, especially for sources where full text was not accessible (common with paywalled journal articles).
- **Example**:
```
    Retrieved: title + abstract only.
    Write: "Argues, based on [the abstract's stated claim], that X; the abstract
    does not specify [whatever it leaves out]."
    Leave out: invented detail about the paper's methodology, sample size, or
    specific findings the abstract never mentioned.
```

---

- **Name**: Oxford-Bibliographies Report Shape
- **Description**: Structure the single deliverable report as: (1) a short introduction stating the topic's ontological/epistemological boundaries and the scope decided by the Specificity-Calibrated Scoping pattern; (2) thematically organized subsections (historical, conceptual, or methodological — whichever the domain's structure calls for), each opening with a brief framing paragraph before its annotated entries; (3) entries ordered to make foundational-to-frontier progression legible within each subsection, not alphabetically.
- **When**: When assembling the final report, after discovery and verification are complete.
- **Example**:
```
    # <Topic>: A Bibliographic Guide

    ## Scope
    [stated boundaries]

    ## Foundational Debates
    [framing paragraph]
    - Author (Year). *Title*. [annotation]

    ## Current Frontier
    [framing paragraph]
    - Author (Year). *Title*. [annotation]
```

---

## Anti-Patterns

- **Name**: Memory-Cited "Obvious" Source
- **Description**: Including a well-known or "surely real" citation without running it through `scripts/verify_citation.py`, on the assumption that a famous work doesn't need checking.
- **Why**: This is exactly the failure mode the skill exists to prevent — plausible-sounding citations (right author style, right era, right journal) are the specific shape hallucination takes, and "obviously real" is not evidence.
- **Instead**: Run the verification script on every candidate citation without exception, including ones you are highly confident about.

---

- **Name**: Flat Keyword Search
- **Description**: Running a single or narrow set of keyword queries and treating whatever comes back as the literature.
- **Why**: Keyword search alone systematically misses terminology shifts, older foundational works that predate current vocabulary, and unindexed recent preprints — producing a bibliography that looks plausible but is missing entire lineages.
- **Instead**: Apply the Four-Part Citation Chaining pattern — backward/forward chain from seed texts to deliberately surface all four source types.

---

- **Name**: Confidence-Driven Over-Annotation
- **Description**: Writing an annotation with specific claims about a source's methodology, findings, or argument that go beyond what was actually retrieved, because the Oxford-Bibliographies tone calls for confident, authoritative prose.
- **Why**: The report's confident tone is a stylistic register, not license to invent content; an annotation that states false specifics about a real source is a subtler form of the same fabrication problem the verification script is built to prevent.
- **Instead**: Apply Retrieval-Grounded Annotation — let annotation length and specificity vary honestly with what was retrieved.

---

- **Name**: Matrix Leakage
- **Description**: Surfacing the internal Literature Matrix or Synthesis Matrix (or a similarly-shaped raw extraction table) as part of the deliverable, alongside or instead of the narrative report.
- **Why**: These are working tools for your own synthesis process; exposing them changes the deliverable's shape into something the user did not ask for and duplicates content already synthesized into the narrative.
- **Instead**: Use the matrices as private working method only; the single deliverable is the narrative report.

---

- **Name**: Silent Drop on Verification Failure
- **Description**: Leaving a source out of the report entirely because it failed tier-1 and tier-2 verification, without telling the reader it was ever considered or including it with a caveat.
- **Why**: Silent drops create an invisible gap — a source you found plausible enough to draft disappears with no trace, and the reader can't tell the difference between "never found" and "found but suppressed."
- **Instead**: Follow the Tiered Citation Verification pattern through to its Tier 3 outcome — include with a visible caveat rather than dropping.

---
