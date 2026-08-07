# Advanced Research Assistant Sharp Edges

This document defines the sharp edges used by advanced-research-assistant.

## Cognitive Overload

- **Id**: cognitive-overload
- **Summary**: The agent gets buried in document-level detail and loses the thread of the original research question.
- **Severity**: medium
- **Situation**: Mid-way through Deep Research, after several rounds of source reading.
- **Why**: Cognitive Load Externalization only helps if the agent notices when it's failing; without a checkpoint, detail accumulates until synthesis becomes impossible.
- **Solution**: Return to the topic level and re-state the research question before continuing, using notes already externalized rather than re-deriving them from memory.
- **Symptoms**: The agent starts restating raw facts rather than drawing connections between them.
- **Detection Pattern**: Several consecutive turns citing new facts with no connecting analysis between them.

---

## Contemporary-Language Drift

- **Id**: contemporary-language-drift
- **Summary**: Search terms drift toward modern or academic phrasing instead of the historical actors' own vocabulary.
- **Severity**: medium
- **Situation**: While formulating any search query.
- **Why**: Sources use period-specific terms, euphemisms, and spelling; a modern-phrasing query silently misses hits and imports modern assumptions onto the past.
- **Solution**: Apply the Historical-Language Search pattern — search with the actors' own terms and period spelling before falling back to modern synonyms.
- **Symptoms**: A search returns few or no hits for a topic the user says is well-documented in the source set.
- **Detection Pattern**: A query using an academic or contemporary term with no attempt at a period-language variant.

---

## Single-Keyword Lock-In

- **Id**: single-keyword-lock-in
- **Summary**: A search relies on one keyword instead of regex alternation across synonyms, spelling variants, and related entities.
- **Severity**: medium
- **Situation**: Formulating the initial or a follow-up grep search.
- **Why**: A single keyword misses everything phrased or spelled differently, understating the true coverage of the source set.
- **Solution**: Apply the Regex Alternation Search Cycle pattern — build a `term1|term2|term3` query before running it.
- **Symptoms**: A search pattern with no `|` alternation despite known synonyms or spelling variants existing for the term.
- **Detection Pattern**: A grep invocation using a bare literal string where multiple plausible variants of the term are known.

---

## Single-Strategy Search

- **Id**: single-strategy-search
- **Summary**: A search round relies on only one of entity-based, topic-based, or temporal strategies.
- **Severity**: medium
- **Situation**: While deciding whether the current search round is sufficient.
- **Why**: Each strategy surfaces a different slice of the source set; relying on one alone leaves whatever the other strategies would have found undiscovered.
- **Solution**: Apply the Multi-Strategy Search pattern — combine entity-based, topic-based, and temporal search before treating a round as sufficient.
- **Symptoms**: Every query in the search log uses the same strategy type.
- **Detection Pattern**: Search log entries all sharing one strategy category with no entity-based or temporal variant attempted.

---

## Coverage Blind Spot

- **Id**: coverage-blind-spot
- **Summary**: The report relies on the initial search result set without a backup pass, leaving true source coverage below 50%.
- **Severity**: high
- **Situation**: Before finalizing the report's Coverage Percentage figure.
- **Why**: An unverified assumption that the first search caught everything relevant produces a confidently wrong coverage claim.
- **Solution**: Run a Grep backup search whenever computed coverage is below 50%, and only report the coverage figure after that backup pass.
- **Symptoms**: A Coverage Percentage is stated without evidence of a second search pass over the same source set.
- **Detection Pattern**: Report contains a Coverage Percentage field with no corresponding backup-search log entry.

---

## Confirmation-Bias Spiral

- **Id**: confirmation-bias-spiral
- **Summary**: Successive search rounds only surface evidence that supports the existing hypothesis.
- **Severity**: high
- **Situation**: During Deep Research, once a working hypothesis has formed.
- **Why**: Without a deliberate disconfirmation step, an evolving query (via Berrypicking) can narrow toward whatever already confirms the hypothesis instead of testing it.
- **Solution**: Apply the Disconfirmation pattern — actively search for evidence that would contradict the current hypothesis before treating it as settled.
- **Symptoms**: Several consecutive findings all support the same reading with no contradicting source considered.
- **Detection Pattern**: Research Perplexities section of the report contains no contradictions, gaps, or surprises despite multiple search rounds.

---

## Single-Genre Tunnel Vision

- **Id**: single-genre-tunnel-vision
- **Summary**: Analysis draws only on one type or genre of source (e.g., only personal notes) when other genres exist in the project.
- **Severity**: medium
- **Situation**: While assembling the source set for the report.
- **Why**: A single genre carries a single perspective and bias profile; Source Criticism cannot surface bias the source set doesn't vary enough to reveal.
- **Solution**: Search across genres where the project's files allow it, before treating the source set as sufficient.
- **Symptoms**: Every citation in the Evidence Matrix comes from the same file type or author role.
- **Detection Pattern**: Evidence Matrix entries share an identical source genre with no attempt to search other genres noted.

---

## Unattributed Claim

- **Id**: unattributed-claim
- **Summary**: A statement in the report has no explicit file-path citation.
- **Severity**: high
- **Situation**: While drafting any Findings statement in the Research Report.
- **Why**: An unattributed claim can't be verified by the user against the project's own files, which breaks the report's core evidentiary contract.
- **Solution**: Attach an explicit file path from the project to every statement or assertion before including it in the report.
- **Symptoms**: A Findings bullet states a fact with no accompanying file reference.
- **Detection Pattern**: A sentence in the Findings section containing a factual claim with no adjacent file path.

---

## Uncorroborated Assumption Carried Forward

- **Id**: uncorroborated-assumption-carried-forward
- **Summary**: An interpretation or hypothesis is treated as fact before project-file evidence corroborates it.
- **Severity**: high
- **Situation**: While reasoning about a claim mid-research, before it reaches the report.
- **Why**: Carrying an unverified interpretation forward lets it silently harden into a stated finding by the time the report is written.
- **Solution**: Suspend the interpretation explicitly — mark it provisional — until project-file evidence corroborates it.
- **Symptoms**: A hypothesis stated early in the session reappears later in the report without an intervening corroboration step.
- **Detection Pattern**: A Key Finding phrased with certainty that traces back to an early-session assumption rather than a cited source.

---

## Scope Escape

- **Id**: scope-escape
- **Summary**: The agent reads or reasons from information outside the current project's files without an explicit user request to do so.
- **Severity**: critical
- **Situation**: At any point during search, Deep Research, or synthesis.
- **Why**: The report's credibility depends on every claim tracing to the project's own files; reaching outside that scope silently breaks the Containment guarantee the user is relying on.
- **Solution**: Confine all `grep`/`ls`/read operations to the current project and its subdirectories, and treat outside information as usable only for general context or firmly established consensus facts, never as cited evidence.
- **Symptoms**: A citation or claim in the report has no corresponding file inside the project.
- **Detection Pattern**: An Evidence Matrix row or Key Finding whose "Where" field is empty, external, or not resolvable to a project file path.

---

## Premature Mode-3 Execution

- **Id**: premature-mode-3-execution
- **Summary**: Deep Research begins before the user has explicitly approved a Mode 2 Research Plan.
- **Severity**: critical
- **Situation**: Immediately after classifying a message as a deep-report request.
- **Why**: Skipping the approval gate removes the user's chance to redirect methodology, search strategy, or scope before expensive research work starts.
- **Solution**: Stay in Mode 2 — present the Proposed Research Plan and ask for explicit approval — until the user's next message is an unambiguous approval (e.g., "yes," "proceed," "looks good").
- **Symptoms**: Grep searches or a Research Report appear in the transcript with no preceding approved plan.
- **Detection Pattern**: A Deep Research or Research Report action occurring before an explicit-approval message in the transcript.

---

## Metacognitive Wrapper Skipped

- **Id**: metacognitive-wrapper-skipped
- **Summary**: The report is delivered with no reflection on why the search strategy worked or which pivot unlocked the answer.
- **Severity**: low
- **Situation**: After delivering the Research Report.
- **Why**: Skipping reflection loses a chance to notice a strategy worth reusing (or a false start worth avoiding) on the next research round.
- **Solution**: Add a brief reflection noting which pivot, berrypicking moment, or genre switch produced the key finding.
- **Symptoms**: The report ends immediately after Recommended Next Steps with no process reflection.
- **Detection Pattern**: Report output containing a Findings section but no closing reflection on search-strategy effectiveness.
