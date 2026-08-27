# Sharp Edges

This document defines the sharp edges used by lit-review-compiler.

---

## Verification API Unavailable Mid-Run

- **Id**: api-unavailable-mid-run
- **Summary**: Crossref, OpenAlex, or Semantic Scholar can time out, rate-limit, or return errors independent of whether a source actually exists.
- **Severity**: high
- **Situation**: Occurs during long compilation runs with many candidate citations queried in succession, especially against Semantic Scholar's stricter unauthenticated rate limits.
- **Why**: A transient network or rate-limit failure looks identical, from the script's output, to "no matching record was found" — both return no match for that source. Treating every no-match as a genuine non-existence signal pushes real, well-known sources into the Tier 3 caveat bucket for no good reason.
- **Solution**:
    - Check the script's `errors` field before accepting a `tier: unverified` result; if a tier-1 or tier-2 source reported a transient error rather than a clean no-match, retry that source once before finalizing the tier.
    - Space out verification calls for large bibliographies rather than firing them in a tight burst.
- **Symptoms**:
    - A high proportion of well-known, easily-findable sources land in Tier 3 within a single run.
    - The script's `errors` field is non-empty for multiple sources in a row.
- **Detection Pattern**: A verification result marked unverified where the errors field for one or more tier-1 or tier-2 sources contains a timeout, rate-limit, or connection-failure message rather than a clean empty response.

---

## SerpApi Quota, Auth, or Rate-Limit Failure

- **Id**: serpapi-failure-mid-run
- **Summary**: A configured `serpapi_key` can still fail at request time — expired key, exhausted monthly quota, or rate-limited — independent of whether Google Scholar actually has a matching record.
- **Severity**: high
- **Situation**: Occurs mid-run on a key that was valid at the start of the session (quota exhausted partway through a long compilation) or on a key that was never valid (typo, revoked, expired trial).
- **Why**: Both `search_scholar.py` and `verify_citation.py`'s Tier 0 check treat a SerpApi failure the same way they'd treat "no key configured" from the caller's perspective — no results, not an exception — which is correct for silent fallback, but if the run never notices the pattern (every Tier 0 check erroring out the same way in a row), it will burn a request per candidate for no benefit.
- **Solution**:
    - Treat a run of identical SerpApi errors across several consecutive Tier 0 checks as a signal to stop attempting Tier 0 for the rest of the run and fall through directly to Tier 1 — don't keep retrying a dead key candidate by candidate.
    - Never surface the raw SerpApi error (which may echo back the key) to the user or into the report; log it only in the verification record's `errors` field.
- **Symptoms**:
    - Every Tier 0 (`googlescholar`) check in a run returns an error rather than a clean no-match, and no candidate ever lands at `scholar_confirmed`.
- **Detection Pattern**: `scripts/verify_citation.py`'s `errors` field contains a `googlescholar` entry with an HTTP 401/403/429 or quota-related message on more than one consecutive candidate.

---

## Fuzzy-Match False Positive

- **Id**: fuzzy-match-false-positive
- **Summary**: Title-similarity matching can confirm the wrong paper when two different works share a near-identical title.
- **Severity**: medium
- **Situation**: Common in fields with formulaic titles (e.g., many papers titled "A Systematic Review of X") or when an author has published multiple works with iterative titles ("X: Part I" / "X: Part II").
- **Why**: The verification script's similarity threshold is deliberately permissive enough to tolerate minor formatting differences (subtitle punctuation, "&" vs "and"), which means it can also match a same-titled but different work by a different author or in a different year, silently miscrediting a citation as confirmed for the wrong record.
- **Solution**:
    - Always pass both author and year to the script, not title alone — the matcher requires author and year agreement in addition to title similarity before confirming.
    - When a matched record's authors or year look off from what was found during search, treat it as unverified and fall through the tiers rather than accepting the match.
- **Symptoms**:
    - A citation is marked `api_confirmed` but the matched record, when spot-checked, points to a different author or publication year than the source found during search.
- **Detection Pattern**: A verified record whose matched author list or publication year, on inspection, does not correspond to the source as it was found during search.

---

## Broad Topic Without a Scoping Round

- **Id**: broad-topic-skipped-scoping
- **Summary**: Proceeding straight to search on a broad topic, field, or discipline input produces an unfocused, sprawling bibliography with no coherent boundary.
- **Severity**: medium
- **Situation**: Happens when the specificity classification misjudges an input as narrow when it is actually broad (e.g., "trauma theory" read as specific because it sounds like a named school of thought, when it in fact spans literary criticism, psychology, and history).
- **Why**: Without an elicited or clearly-stated boundary, search returns an undifferentiated mass of tangentially related work, and citation chaining amplifies the sprawl by chaining outward from sources that shouldn't have been in scope to begin with.
- **Solution**:
    - When in doubt about an input's specificity, treat it as broad and elicit boundaries — the cost of one extra clarifying round is far lower than the cost of a sprawling, unusable bibliography.
- **Symptoms**:
    - The candidate source list spans clearly incompatible disciplinary framings with no unifying thread.
    - The user's original input maps to more than one plausible discourse community.
- **Detection Pattern**: An input phrase that plausibly maps to two or more distinct discourse communities or disciplines with no disambiguating context, proceeding directly to search without a scoping round.

---

## Seed Corpus Treated as Ceiling

- **Id**: seed-corpus-as-ceiling
- **Summary**: Treating a user-supplied seed bibliography as the boundary of the search rather than a floor to expand from.
- **Severity**: medium
- **Situation**: Occurs when a user provides an existing reading list or database export as a starting point.
- **Why**: A user-supplied seed list reflects what the user already knew to look for, not the full current horizon of the field — deferring entirely to it reproduces the user's existing blind spots instead of correcting them, which defeats the purpose of running the compilation at all.
- **Solution**:
    - Always chain outward (backward and forward) from every seed source and run independent searches on the topic regardless of seed-list size.
- **Symptoms**:
    - The final report's source list is a strict subset of the user-supplied seed list, with no newly discovered sources.
- **Detection Pattern**: A completed compilation whose cited sources are entirely contained within the user-supplied seed corpus, with zero sources introduced from independent search or citation chaining.

---

## Verification Tier Read As Quality Endorsement

- **Id**: verification-tier-read-as-quality
- **Summary**: A reader treats a Tier 1 or Tier 2 verification result as an endorsement of a source's scholarly significance or methodological soundness, when the tier only confirms the source mechanically exists.
- **Severity**: high
- **Situation**: Arises whenever the report reaches a reader who was not part of the compilation process — an advisor, exam committee, or downstream researcher who sees the tier label on the citation line and nothing more.
- **Why**: Existence-confirmation and significance are orthogonal, but presenting both on the same citation line with no distinguishing signal invites the reader to conflate them — a mechanically confirmed source reads as a vetted, important one, which is a subtler recurrence of the same fluency-as-competence problem the verification script exists to prevent.
- **Solution**: Apply Verification-Significance Separation on every entry — state consensus, centrality, or contested status in the cluster's framing paragraph or the entry's annotation, kept visibly distinct from the tier caveat; close the report with a Coverage & Confidence section stating the tier distribution across all cited sources.
- **Symptoms**: A cluster's framing paragraph or an entry's annotation states no consensus/significance context at all; the report has no closing section naming the tier distribution.
- **Detection Pattern**: An entry or report section stating a citation's verification tier with no adjacent, separate note on the source's centrality or consensus status.

---

## Domain Map Built Entirely From Self-Generated Chaining

- **Id**: domain-map-self-referential
- **Summary**: The compiled thematic clusters and their foundational/turning-point/consolidator/frontier sources are chained entirely from the model's own seed searches, with no check against a structure the model did not itself generate.
- **Severity**: high
- **Situation**: Occurs on unfamiliar or interdisciplinary domains, where the model's initial keyword and seed choices already reflect a partial view of the field before chaining even begins.
- **Why**: Citation chaining only ever deepens the map it starts from; it cannot surface an entire lineage, school, or language tradition that the seed sources never touched, and nothing in the chaining process itself signals that this happened — the model's domain map can be confidently wrong in a way the process has no way to detect from the inside.
- **Solution**: Apply External Benchmark Cross-Check at the end of Discovery & Verification — check the compiled clusters against a handbook table of contents, encyclopedia entry, or flagship review journal's recent contents, and carry any named gap into the report's Coverage & Confidence section.
- **Symptoms**: A single disciplinary lineage, methodology, or language tradition dominates the compiled clusters with no acknowledgment that others exist.
- **Detection Pattern**: Report assembly begins with no record, in the working matrix or conversation, of a cross-check against an externally authored domain structure.

---

## Scoping Round Presumes User's Domain Knowledge

- **Id**: broad-topic-user-cant-specify
- **Summary**: The scoping round asks the user to name sub-fields, lenses, and exclusions for a topic broad enough that the user may not yet know what those boundaries are.
- **Severity**: medium
- **Situation**: Arises specifically for the users most likely to need this skill on a genuinely broad topic — a student or newcomer surveying a field before they know its internal map.
- **Why**: An open-ended scoping question presumes the user already has the domain knowledge the compilation exists to supply; asking them to self-report boundaries reproduces the same self-assessment gap the skill is meant to correct for, on the human side instead of the model's.
- **Solution**: Apply Model-Proposed Scoping Options — run a quick preliminary scan and offer a short candidate list of sub-fields/lenses/schools for the user to confirm or edit, rather than a blank ask.
- **Symptoms**: The user's scoping answers are vague, single-word, or defer entirely back to the model ("whatever's standard").
- **Detection Pattern**: A scoping round issued as an open free-text question with no candidate options attached.

---

## Report Tone Outpacing Evidence

- **Id**: report-tone-outpacing-evidence
- **Summary**: Matching the Oxford Bibliographies series' confident, authoritative register can bleed into overclaiming comprehensiveness the underlying search doesn't support.
- **Severity**: high
- **Situation**: Arises when the report's framing language ("the definitive account," "settles the debate," "the complete literature on X") is drawn from stylistic convention rather than an actual claim backed by what was retrieved.
- **Why**: The instruction to sound like a confident, professional bibliography is about register, not about license to assert completeness or certainty beyond the compilation's actual scope and verification tier mix.
- **Solution**:
    - Keep the confident tone in sentence-level prose and word choice, but keep completeness claims scoped to the stated boundaries (from the Specificity-Calibrated Scoping pattern), qualifying any claim of exhaustiveness with that stated scope.
- **Symptoms**:
    - The report's introduction or framing language asserts totality ("the complete," "exhaustive," "settles") without a corresponding scope statement to bound the claim.
- **Detection Pattern**: Superlative or totalizing language in the report's framing prose (e.g., "the definitive," "the complete literature," "settles the debate") that is not immediately qualified by the report's own stated scope boundaries.

---
