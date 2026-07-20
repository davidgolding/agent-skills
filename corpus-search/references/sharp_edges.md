# Sharp Edges

This document defines the sharp edges used by corpus-search.

---

## Hermeneutical Echo Chamber

- **Id**: hermeneutical-echo-chamber
- **Summary**: The search iteration loop repeatedly confirms existing hypotheses without seeking disconfirming evidence or negative cases.
- **Severity**: high
- **Situation**: The agent searches exclusively for terms supporting a user's initial assumption, ignoring contradictory documents in the corpus.
- **Why**: Cognitive confirmation bias causes search query refinement to narrow into a self-reinforcing feedback loop.
- **Solution**:
    - Force falsification checks by running explicit searches for disconfirming terms or counter-arguments.
    - Conduct a pre-understanding audit to list assumptions before initiating iterative passes.
- **Symptoms**:
    - Subsequent search passes yield 100% agreement with initial hypothesis without surfacing any conflicting context.
    - Zero negative cases or alternative explanations included in reports.
- **Detection Pattern**: Search passes that only use positive confirmation terms while omitting disconfirming or opposing search terms.

---

## Pertinence Trap

- **Id**: pertinence-trap
- **Summary**: Searching strictly by modern topical keywords rather than creator provenance and administrative structures.
- **Severity**: medium
- **Situation**: A search for historical "public welfare" fails to find records because 19th-century archives categorized them under "Poor Law Board".
- **Why**: Modern terminology often differs significantly from historical institutional classifications.
- **Solution**:
    - Perform administrative history reconnaissance to identify creating agencies before executing grep queries.
    - Map topical terms to period-accurate institutional vocabularies.
- **Symptoms**:
    - Low query yield despite known historical presence of the subject in the corpus.
    - Searching modern jargon in primary source collections.
- **Detection Pattern**: Grep queries using modern technical jargon against historical record sets without mapping to historical institutional creators.

---

## Binary Grep Failure

- **Id**: binary-grep-failure
- **Summary**: Executing `ripgrep` directly on raw PDF or DOCX files, resulting in skipped files or garbled binary output.
- **Severity**: critical
- **Situation**: The agent runs `rg "term" docs/` where `docs/` contains `.pdf` or `.docx` files, missing critical content.
- **Why**: `ripgrep` is optimized for plain-text streams and treats binary files as unsearchable unless pre-converted.
- **Solution**:
    - Automatically scan target directories for PDF/DOCX files prior to searching.
    - Extract text into temporary scratch files (`.scratch/`) and direct `ripgrep` to search the converted plain text.
- **Symptoms**:
    - `ripgrep` outputs "Binary file matches" or silently ignores PDF/DOCX contents.
    - Empty search results on document sets known to contain matching text.
- **Detection Pattern**: Invocations of ripgrep targeting paths with binary extensions without prior conversion steps.

---

## Sunk Cost Persistence

- **Id**: sunk-cost-persistence
- **Summary**: Continuing to execute minor variations of a failing search query after multiple null or low-yield passes.
- **Severity**: medium
- **Situation**: The agent spends 4 consecutive turns slightly tweaking spelling on a dead-end search query.
- **Why**: Reluctance to abandon an unproductive search path due to effort already invested.
- **Solution**:
    - Enforce a strict stop-loss heuristic: if a query yields no relevant results on pass 1, execute an explicit Zoom, Source, or Question pivot on pass 2.
- **Symptoms**:
    - Multiple consecutive search turns with near-identical queries and zero match yields.
- **Detection Pattern**: Repeated search query executions with minimal keyword variation following consecutive null results.

---

## Anachronistic Causal Assertion

- **Id**: anachronistic-causal-assertion
- **Summary**: Asserting simple direct causality between historical events without testing counterfactuals or checking temporal order.
- **Severity**: high
- **Situation**: The agent claims document A caused event B when document A was created after event B or by an unrelated entity.
- **Why**: Over-attributing causality based on topical proximity rather than rigorous causal chaining (preconditions, precipitants, triggers).
- **Solution**:
    - Apply Toulmin counterfactual reasoning and verify chronological sequence before stating causal relationships.
- **Symptoms**:
    - Causal claims in synthesis reports lacking supporting warrants or temporal verification.
- **Detection Pattern**: Statements claiming historical causality without chronological verification or counterfactual minimal-rewrite testing.

---

## Algorithmic Black-Box Reliance

- **Id**: algorithmic-black-box-reliance
- **Summary**: Blindly trusting automated OCR or search index results without verifying raw text matches in context.
- **Severity**: medium
- **Situation**: OCR errors convert "1848" to "1818", leading the agent to construct an inaccurate timeline.
- **Why**: Assuming digital text conversions are 100% accurate representations of original primary sources.
- **Solution**:
    - Maintain epistemic vigilance by inspecting surrounding lines (`rg -C 5`) and noting potential OCR artifacts.
- **Symptoms**:
    - Anomalous dates or corrupted words cited as factual evidence in research summaries.
- **Detection Pattern**: Uncritical citation of obvious OCR garble or corrupted characters as factual evidence.

---
