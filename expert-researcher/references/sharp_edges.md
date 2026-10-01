# Sharp Edges

This document defines the sharp edges used by expert-researcher.

---

## Citation Hallucination

- **Id**: citation-hallucination
- **Summary**: The answer cites papers, authors, DOIs or URLs that were never retrieved, often reconstructed from memory to look plausible.
- **Severity**: critical
- **Situation**: A line of inquiry relies on model knowledge for a claim, or the agent remembers a paper but did not fetch it, and writes a full citation anyway to match the inline-citation convention.
- **Why**: The citation convention creates pressure to cite every claim, and models produce fluent bibliographic details that resemble real ones.
- **Solution**:
    - Cite only sources whose page or record was retrieved in the session.
    - Label everything else as `(model knowledge, uncited)`.
    - During the merge, keep each citation tied to the brief and hop that retrieved it.
- **Symptoms**:
    - Links that 404 or resolve to different papers.
    - Author-year pairs with no matching retrieval in the session.
    - Suspiciously round or generic titles.
- **Detection Pattern**: A citation in the answer whose URL, title or DOI does not appear in any search or fetch result from the current session.

---

## Silent Knowledge Fallback

- **Id**: silent-knowledge-fallback
- **Summary**: Web tools are missing or failing and the agent answers from model knowledge without saying so.
- **Severity**: high
- **Situation**: The harness has no search or fetch tool, the calls are denied, or every fetch errors, and the agent quietly switches to recalling the material.
- **Why**: The output format looks the same either way, so the switch is invisible unless the agent announces it.
- **Solution**:
    - Check tool availability at the start of gathering.
    - When live sourcing is unavailable, open the answer with a plain statement that no live sources were consulted.
    - Record the source base in the coverage note.
- **Symptoms**:
    - No tool calls in the gathering phase, yet the answer carries citations.
    - The coverage note claims live sources the transcript does not show.
- **Detection Pattern**: A research answer produced with no successful search or fetch calls that lacks an opening statement about the missing live sources.

---

## Echo-Chamber Saturation

- **Id**: echo-chamber-saturation
- **Summary**: A line saturates early because its snowball stayed inside one research group's citation cluster, missing rival schools.
- **Severity**: high
- **Situation**: The seed source belongs to one camp, and backward and forward trails keep returning that camp's papers, so hops stop yielding novelties while opposing work stays unseen.
- **Why**: Citation graphs cluster by school, so following citations from one seed can circle that school's work.
- **Solution**:
    - Seed each line from a review article or reference work, which surveys the camps, where one exists.
    - Add at least one term trail and one search for critiques or alternatives before declaring saturation.
    - Count a line saturated only when its sources span more than one author group, or note in the brief why they do not.
- **Symptoms**:
    - Every source in a line shares authors or a lab.
    - The line has no perplexities on a topic known to be contested.
- **Detection Pattern**: A saturated line of inquiry whose sources all share overlapping authors and which records no contested findings or perplexities.

---

## False Consensus

- **Id**: false-consensus
- **Summary**: Contested or speculative findings appear in the answer as settled fact.
- **Severity**: high
- **Situation**: During translation to a lower audience level, hedges and disputes are trimmed for readability, or the merge resolves a conflict by quietly keeping one side.
- **Why**: Simplification removes qualifiers first, and a merge that picks the more confident claim seems tidier.
- **Solution**:
    - Carry every ledger certainty mark into the presentation.
    - Keep conflicts between lines as named perplexities with both sides cited.
    - At lower audience levels, simplify the explanation and keep the certainty marks.
- **Symptoms**:
    - Ledger perplexities that never appear in the answer.
    - Claims with [contested] in a brief and no mark, or [settled], in the output.
- **Detection Pattern**: A claim marked contested or speculative in a line brief or ledger that appears in the answer unmarked or marked settled.

---

## Register Mirroring

- **Id**: register-mirroring
- **Summary**: The answer reuses the specialist phrasing of its sources, so a non-specialist reader cannot follow it.
- **Severity**: high
- **Situation**: A deep technical prompt in lay phrasing yields briefs full of expert phrasing, and the presentation pastes and lightly connects them.
- **Why**: Briefs arrive in expert register, and paraphrasing them faithfully feels safer than translating them.
- **Solution**:
    - Fix the audience level before composing.
    - Translate each finding: a concrete instance first, define terms at first use, and keep only the terms of art the reader needs.
    - Keep the expert phrasing in a brief "in the literature" aside when it helps the reader search further.
- **Symptoms**:
    - Undefined terms of art in a sophomore-level answer.
    - Sentences lifted almost verbatim from abstracts.
- **Detection Pattern**: An answer pitched below specialist level that uses terms of art without definition or reproduces source phrasing near-verbatim.

---

## Lowest-Common-Denominator Flattening

- **Id**: lcd-flattening
- **Summary**: An everyday subject gets a generic, simplistic answer that skips the mechanisms and expert knowledge that exist on it.
- **Severity**: high
- **Situation**: A prompt like "why does bread rise?" or "how should I study for exams?" gets treated as needing only common knowledge, so the decomposition goes shallow and the presentation turns into tips.
- **Why**: Familiar topics look simple, so the agent picks shallow depth and a casual register, even though the relevant fields (food chemistry, cognitive psychology) hold rigorous findings.
- **Solution**:
    - Run Discipline Corridor Mapping on familiar topics too.
    - Lift the presentation: name the mechanisms and cite the fields that study them.
    - Use the sophomore-level default as a floor for rigor when the prompt gives no level signal.
- **Symptoms**:
    - Bulleted tips with no mechanisms or citations.
    - No discipline named in the plan.
- **Detection Pattern**: A research answer on a non-technical subject that names no mechanism, cites no field-specific source, and is structured as generic tips.

---

## Context Flood

- **Id**: context-flood
- **Summary**: Raw source text piles up in the orchestrating context, and merge and presentation quality drop.
- **Severity**: high
- **Situation**: Sequential mode on a deep prompt, or subagents returning full abstracts and fetched pages instead of briefs.
- **Why**: Attention dilutes as context fills with unprocessed text, so later instructions (certainty marks, audience level) lose adherence.
- **Solution**:
    - Hold every line to the Line Brief format and length.
    - In sequential mode, compress each line into its brief before starting the next and keep only the briefs and the ledger.
    - Read abstracts and key sections before full text.
- **Symptoms**:
    - Later lines get thinner treatment than earlier ones.
    - The answer drops the conventions set in the plan.
- **Detection Pattern**: Line outputs that exceed the brief length or contain long verbatim source passages, or a sequential run that keeps full fetched pages in context across lines.

---

## Runaway Snowball

- **Id**: runaway-snowball
- **Summary**: A line keeps expanding into tangents and never saturates, burning time and tokens.
- **Severity**: medium
- **Situation**: A sprawling field (machine learning, nutrition) where every hop produces new, loosely related papers, so the ledger keeps growing.
- **Why**: Novelty measured against the whole field never runs out; it has to be measured against the line's question.
- **Solution**:
    - Count an entry as a novelty only when it bears on the line's own question.
    - Enforce the tier's hop cap and mark the line stopped at budget.
    - Move promising tangents to a "further lines" mention in the coverage note.
- **Symptoms**:
    - Ledger entries that no longer answer the line's question.
    - Hop counts well past the tier's cap.
- **Detection Pattern**: A line of inquiry whose recent ledger entries do not address its stated question, or whose hop count exceeds its tier's cap without being marked stopped at budget.

---

## Recency Gap

- **Id**: recency-gap
- **Summary**: The answer presents a superseded state of the field because gathering leaned on older, highly cited sources or on model knowledge.
- **Severity**: medium
- **Situation**: Backward citation trails dominate, or model knowledge fills gaps, on a fast-moving topic.
- **Why**: Citation counts favor older work, and model knowledge has a training cutoff.
- **Solution**:
    - Run at least one forward trail per line, sorted by date where the index allows.
    - Search the line's key terms restricted to recent years before saturating.
    - State the most recent source date in the coverage note.
- **Symptoms**:
    - The newest cited source is years old on an active topic.
    - Open problems listed that recent work has resolved.
- **Detection Pattern**: A line on an active research topic with no forward-citation hop and no source from the most recent two years.

---

## Abstract-Only Overclaim

- **Id**: abstract-only-overclaim
- **Summary**: A claim is attributed to a paper with more confidence or detail than its abstract supports, because the full text was paywalled.
- **Severity**: medium
- **Situation**: Fetch returns only an abstract or a landing page, and the agent fills in results it expects the paper to contain.
- **Why**: Abstracts compress and sometimes overstate findings, and the gap invites extrapolation.
- **Solution**:
    - Limit claims from an abstract-only source to what the abstract states.
    - Look for an open preprint version (arXiv, institutional repository) before settling for the abstract.
    - List abstract-only sources in the coverage note.
- **Symptoms**:
    - Specific numbers or methods attributed to a paper whose full text was never fetched.
- **Detection Pattern**: A claim citing a source for which only an abstract or landing page was retrieved, stating details absent from that abstract.

---

## Operational Drift

- **Id**: operational-drift
- **Summary**: In research mode, the agent acts on an operational prompt by editing files or running code instead of researching it.
- **Severity**: medium
- **Situation**: The user, still in research mode, writes "fix this test" or "rename this variable", and the agent's default coding behavior takes over.
- **Why**: Operational phrasing strongly cues default assistant behavior, and research mode persists across turns, where the cue is easy to lose.
- **Solution**:
    - Check research mode at the start of every turn.
    - Turn the operational prompt into a research query and report findings with sources.
    - Offer to leave research mode when the user seems to want the operation done.
- **Symptoms**:
    - File edits or code execution during research mode.
- **Detection Pattern**: Any file-modifying or code-executing tool call made while research mode is active.
