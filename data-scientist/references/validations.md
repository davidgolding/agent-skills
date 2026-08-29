# Validations

This document defines the validations used by data-scientist.

---

## Frontier Claim Without Verification

- **Id**: frontier-claim-unverified
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - A claim naming a specific software library, package, framework, or a version number.
    - A claim naming a specific model family, architecture, or release identifier.
    - A claim reporting a benchmark result, leaderboard ranking, or "state of the art" figure.
    - A claim naming a standard, protocol, or regulation that revises on a public cadence.
    - A claim using recency superlatives ("latest," "current," "newest," "most recent") about tooling, ecosystem support, or defaults.
- **Message**: A frontier-class claim is being asserted without having been checked against a current source in this session.
- **Fix Action**: Verify the claim against current documentation, search, or another live source before asserting it. If verification is unavailable or inconclusive, assert the claim explicitly as an unverified prior (see Fabricated or Reconstructed Citation below for what not to do instead) and state that it may be stale.
- **Applies To**:
    - *.md
    - Any response containing a frontier-class claim

---

## Fabricated or Reconstructed Citation

- **Id**: fabricated-citation
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Presenting an author, year, title, DOI, or link for a claim that was not actually retrieved or verified during this session.
    - Reconstructing a plausible-sounding source only after the user asks "where's that from," for a claim whose provenance was never tracked while it was made.
- **Message**: A citation or source is being presented as retrieved when it was not actually verified this session.
- **Fix Action**: State the claim's real provenance tier — canon, retrieved, or unverified prior — from what was tracked while making the claim. If provenance was never tracked for a claim, say so plainly rather than inventing a source retroactively.
- **Applies To**:
    - Any response disclosing sources or provenance on request

---

## Knowledge-Cutoff Self-Check Missing

- **Id**: missing-cutoff-check
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - A frontier-class claim (see Frontier Claim Without Verification) is asserted with no acknowledgment that training data is a dated snapshot rather than a live source.
- **Message**: A claim that could have changed since training was made without first recognizing training data as a dated source.
- **Fix Action**: Before asserting a frontier claim from memory, explicitly weigh whether it could be stale, then verify or apply Unverified-Prior Labelling.
- **Applies To**:
    - Any response containing a frontier-class claim

---

## Stale-Confidence Phrasing Unflagged

- **Id**: stale-confidence-phrasing
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:as\s+of\s+my\s+(?:last\s+update|training|knowledge)|as\s+far\s+as\s+I\s+know|I\s+believe\s+the\s+latest|the\s+current\s+best\s+(?:library|model|practice|tool)\s+is)\b
- **Message**: Phrasing that hedges on currency is present without an explicit unverified-prior label or a verification step alongside it.
- **Fix Action**: Either verify the claim against a current source, or convert the hedge into an explicit Unverified-Prior label stating the claim may be stale and why it wasn't verified.
- **Applies To**:
    - *.md

---

## Empirical Question Answered Without Execution

- **Id**: empirical-question-not-executed
- **Severity**: error
- **Type**: instruction
- **Pattern**:
    - Attached or reachable data exists (files, database, query results) and the response makes a specific claim about what that data shows, without having actually run code against it.
- **Message**: A claim about real attached data was made without executing analysis against the actual data.
- **Fix Action**: Profile and analyze the actual data before making claims about its contents; describe what was observed, not what was expected.
- **Applies To**:
    - Any response making a claim about attached or reachable data

---

## Failure-Mode Canon Bypassed

- **Id**: failure-mode-review-skipped
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - A substantive analysis, system design, or critique is delivered with no evidence that the plan or the output was checked against `references/sharp_edges.md`.
- **Message**: The failure-mode canon was not visibly applied as a pre-flight or post-flight check on this piece of work.
- **Fix Action**: Before delivering, check the plan and the output against the relevant entries in `references/sharp_edges.md` and address anything that applies.
- **Applies To**:
    - Any substantive analysis, design, or critique deliverable

---

## Over-Citation of Settled Basics

- **Id**: over-citation-default
- **Severity**: warning
- **Type**: instruction
- **Pattern**:
    - A citation, reference, or provenance note is attached by default to a settled, canon-level methodological choice when the user did not ask where it came from.
- **Message**: Provenance is being surfaced by default for a claim that should read as plain practitioner judgment until asked.
- **Fix Action**: Remove the default citation; keep provenance tracked internally and reveal it only when the user asks where a claim comes from.
- **Applies To**:
    - Any default (non-provenance-requested) response
