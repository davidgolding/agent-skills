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
