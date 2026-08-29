# Sharp Edges

This document defines the sharp edges used by data-scientist. It is the stable core of the canon — statistical and methodological failure modes that have held for decades and are checked as a pre-flight before starting analysis, design, or critique, and a post-flight review before delivering it. Apply the same catalogue at both points.

---

## Train/Test Leakage

- **Id**: train-test-leakage
- **Summary**: Information from the evaluation set influences the model or the analysis before evaluation happens, inflating apparent performance.
- **Severity**: critical
- **Situation**: Preprocessing (scaling, imputation, feature selection, target encoding) is fit on the full dataset before splitting; or rows that belong together (same user, same patient, same time window) end up split across train and test.
- **Why**: The evaluation set stops measuring generalization once any information from it has shaped the model, even indirectly. Grouped structure is the most common vector — a model that has seen a user's other rows in training can look accurate on that user's held-out row for reasons that won't hold on a genuinely new user.
- **Solution**:
    - Fit every preprocessing step only on the training fold, then apply it to validation/test.
    - Split at the level of the grouping unit (user, patient, session) when rows share structure, not at the row level.
    - Re-derive any feature that used future information relative to its row's timestamp.
- **Symptoms**:
    - Held-out performance far exceeds what the deployed system later achieves.
    - Performance drops sharply when the model is retrained on a new time window or population.
- **Detection Pattern**: A preprocessing or feature-selection step fit before the train/test split, or a split performed at the row level when rows share a natural grouping key.

---

## Look-Ahead Bias (Temporal Leakage)

- **Id**: look-ahead-bias
- **Summary**: A feature or label uses information that would not have been available at the decision time being modeled.
- **Severity**: critical
- **Situation**: A backtest or forecasting model includes a feature computed using data from after the prediction timestamp — a revised statistic, a future aggregate, or a label computed with hindsight.
- **Why**: Models trained this way learn a relationship that cannot exist at deployment time, since the future information simply won't be available yet. Performance looks strong in backtest and collapses in production.
- **Solution**:
    - Reconstruct every feature as of the exact decision timestamp, using only data that would have existed then.
    - Use time-respecting cross-validation (walk-forward, expanding window) rather than random k-fold for any temporally ordered problem.
- **Symptoms**:
    - Backtested performance is implausibly strong relative to the problem's known difficulty.
    - A feature's definition includes a window that spans the prediction date.
- **Detection Pattern**: A feature or label whose computation window extends past the timestamp being predicted from, or random (non-time-respecting) cross-validation applied to sequential data.

---

## Uncorrected Multiplicity (p-Hacking)

- **Id**: uncorrected-multiplicity
- **Summary**: Running many comparisons, metrics, or subgroup analyses and reporting whichever came out significant, without correcting for how many chances significance had to appear.
- **Severity**: high
- **Situation**: Testing dozens of subgroups, metrics, or model variants and highlighting the handful that cross a significance threshold, or repeatedly peeking at an experiment's results and stopping once significance appears.
- **Why**: At a 5% significance threshold, roughly one in twenty unrelated comparisons will appear significant by chance alone. Without a correction or a pre-registered analysis plan, "significant" results are frequently noise dressed as signal.
- **Solution**:
    - Pre-specify the primary metric and the comparisons that will be made before looking at the data.
    - Apply a multiple-comparison correction (Bonferroni, Holm, FDR) when many hypotheses are genuinely being tested.
    - Use sequential-testing-aware stopping rules for experiments monitored over time, not fixed-threshold peeking.
- **Symptoms**:
    - A results table with many comparisons and only a few flagged as significant, with no correction mentioned.
    - An experiment that was "stopped early because it hit significance."
- **Detection Pattern**: Multiple hypotheses, subgroups, or metrics tested with no stated multiple-comparison correction, or a significance claim reached by stopping an experiment as soon as a threshold was crossed.

---

## Causal Claim Without Identification

- **Id**: causal-claim-without-identification
- **Summary**: Asserting or implying that X causes Y from associational data without an identification strategy that rules out confounding, reverse causation, or selection.
- **Severity**: critical
- **Situation**: A correlation, regression coefficient, or observed pattern in observational data is described in causal language ("X drives Y," "X improves Y") without randomization, an instrument, a natural experiment, or another identification strategy.
- **Why**: Association alone cannot distinguish X causing Y from Y causing X, from a third variable causing both, or from the sample itself being selected in a way that manufactures the pattern. Causal language commits the reader to a claim the data cannot support.
- **Solution**:
    - Name the identification strategy explicitly (RCT, instrumental variable, difference-in-differences, regression discontinuity, matching with stated assumptions) or state plainly that the claim is associational only.
    - Enumerate the confounders the design does or doesn't handle.
    - Downgrade causal language to associational language when no identification strategy is present.
- **Symptoms**:
    - Causal verbs ("causes," "drives," "improves," "leads to") attached to a coefficient from observational data with no design discussion.
    - A design decision (e.g., a launch) justified by an association that could equally be explained by who self-selected into treatment.
- **Detection Pattern**: Causal language applied to observational or correlational evidence without a named identification strategy and its assumptions.

---

## Simpson's Paradox / Aggregation Reversal

- **Id**: simpsons-paradox
- **Summary**: A trend that holds within every subgroup reverses or disappears when the subgroups are pooled, or vice versa.
- **Severity**: high
- **Situation**: Comparing an aggregate metric across two populations (e.g., overall conversion rate, overall recovery rate) without checking whether the populations differ in composition on a variable that also affects the outcome.
- **Why**: A confounding variable correlated with both the grouping and the outcome can make the pooled comparison say the opposite of what every subgroup says. Aggregation hides this unless it's explicitly checked for.
- **Solution**:
    - When comparing an aggregate metric across groups, also check the metric within relevant strata.
    - If the strata disagree with the aggregate, report both and identify the confounding composition difference.
- **Symptoms**:
    - A pooled comparison that contradicts domain intuition or contradicts every visible subgroup.
    - Group sizes or compositions differ substantially across the populations being compared.
- **Detection Pattern**: An aggregate-level comparison across groups with materially different subgroup compositions, reported without a stratified check.

---

## Survivorship and Selection Bias

- **Id**: survivorship-selection-bias
- **Summary**: The sample analyzed systematically excludes cases that dropped out, failed, or were never observed, and the exclusion correlates with the outcome being studied.
- **Severity**: high
- **Situation**: Analyzing only customers who are still active, companies that are still in business, users who completed a funnel, or records that passed a data-quality filter — without accounting for what dropped out and why.
- **Why**: If the process that removed cases from the sample is related to the outcome, the remaining sample no longer represents the population the conclusion is being generalized to. Conclusions look robust but only describe the survivors.
- **Solution**:
    - Characterize what was excluded and whether the exclusion mechanism is independent of the outcome.
    - When it isn't independent, model the selection process explicitly (e.g., inverse probability weighting, Heckman-style correction) or scope the conclusion to the observed population only.
- **Symptoms**:
    - A population defined by "still present at time of measurement" with no attrition analysis.
    - Strong effects that disappear or reverse when previously-excluded cases are added back.
- **Detection Pattern**: A conclusion drawn from a sample implicitly filtered by an outcome-correlated survival, completion, or data-quality criterion, with no attrition analysis stated.

---

## Non-Stationarity / Distribution Shift

- **Id**: non-stationarity-distribution-shift
- **Summary**: A model, metric, or rule is deployed on the assumption that the data-generating process at deployment time matches the process it was built or validated on.
- **Severity**: high
- **Situation**: A model trained on historical data is deployed without monitoring, or a system design assumes the input distribution, label definition, or user behavior at serving time will match training time indefinitely.
- **Why**: Real-world processes drift — user behavior changes, upstream systems change, seasons change, definitions change. A model or rule with no drift detection degrades silently, and the degradation is often invisible until an unrelated downstream failure surfaces it.
- **Solution**:
    - State the stationarity assumption explicitly and its expected validity window.
    - Build drift detection (input distribution monitoring, label delay handling, periodic retraining triggers) into the system design, not as an afterthought.
- **Symptoms**:
    - No monitoring plan mentioned for a model or rule expected to run in production over time.
    - Performance degrades gradually with no corresponding code change.
- **Detection Pattern**: A deployed model, metric, or business rule with no stated plan for detecting or responding to drift in its input or target distribution.

---

## Proxy-Target Mismatch

- **Id**: proxy-target-mismatch
- **Summary**: Optimizing a metric that is easy to measure as a stand-in for an outcome that is hard to measure, without checking how well the two actually track each other.
- **Severity**: high
- **Situation**: A model or system optimizes clicks as a proxy for satisfaction, engagement time as a proxy for value, or a leading indicator as a proxy for a lagging business outcome, with no validation that improving the proxy improves the real target.
- **Why**: Optimization pressure exploits any gap between the proxy and the true objective — the system gets very good at the proxy while the outcome it was meant to serve stagnates or degrades (Goodhart's law in practice).
- **Solution**:
    - State the true objective and the proxy separately, and validate the correlation between them before committing to the proxy as the optimization target.
    - Monitor the true objective alongside the proxy after deployment, not just the proxy.
- **Symptoms**:
    - The optimized metric improves steadily while a downstream business outcome it was meant to reflect is flat or declining.
    - No validation study exists connecting the proxy to the outcome it stands in for.
- **Detection Pattern**: A system or model whose objective function is a proxy metric with no stated or validated relationship to the actual outcome of interest.

---

## Spurious Precision

- **Id**: spurious-precision
- **Summary**: Reporting a point estimate, metric, or forecast with more decimal places or narrower uncertainty than the data and method actually support.
- **Severity**: medium
- **Situation**: A result is reported as a single number ("conversion rate is 3.472%") or a tight interval without acknowledging sample size, measurement error, or model uncertainty that would widen it substantially.
- **Why**: False precision manufactures confidence the analysis didn't earn, and downstream decisions treat a noisy estimate as if it were exact.
- **Solution**:
    - Report uncertainty (confidence/credible intervals, standard errors, or a stated margin) alongside every point estimate that will inform a decision.
    - Round to the precision the sample size and method actually justify.
- **Symptoms**:
    - Point estimates reported with no interval, standard error, or sample size context.
    - Decisions justified by differences smaller than the estimate's plausible error.
- **Detection Pattern**: A quantitative claim or forecast presented as a bare point value with no accompanying uncertainty statement, where the underlying sample or method would produce a materially wide interval.

---

## Base-Rate Neglect

- **Id**: base-rate-neglect
- **Summary**: Interpreting a metric like accuracy, precision, or a positive test result without accounting for the underlying prevalence of the outcome.
- **Severity**: high
- **Situation**: Reporting classifier accuracy on a heavily imbalanced dataset without a baseline comparison, or interpreting a positive detection/test result without weighing how rare the condition being detected actually is.
- **Why**: On an imbalanced problem, a trivial always-predict-majority-class rule can post high accuracy while being useless; a rare-condition test with high sensitivity can still produce mostly false positives if the condition's base rate is low enough. Ignoring the base rate makes an unhelpful result look impressive.
- **Solution**:
    - Report a baseline (majority-class rate, or a naive rule's performance) alongside any accuracy-like metric on imbalanced data.
    - For rare-event detection, report precision, positive predictive value, or a Bayesian update using the actual base rate — not sensitivity/specificity alone.
- **Symptoms**:
    - A headline accuracy or "success rate" number with no class-balance or baseline context.
    - A detection or alerting system praised for sensitivity with no mention of false-positive volume given the true prevalence.
- **Detection Pattern**: An accuracy, precision, or detection-rate claim on an imbalanced or rare-outcome problem with no stated base rate or baseline comparison.

---

## Silent Upstream Schema or Assumption Drift

- **Id**: silent-schema-drift
- **Summary**: A data pipeline, feature store, or downstream system assumes an upstream schema, unit, or semantic definition that can change without the change being surfaced to consumers.
- **Severity**: high
- **Situation**: Designing or reviewing a pipeline where a downstream feature, join, or model input depends on an upstream table's column meaning, unit, or nullability convention, with no contract or validation enforcing that dependency.
- **Why**: Upstream systems change for reasons unrelated to any single downstream consumer — a currency unit changes, a null convention changes, a category gets renamed. Without an explicit contract and validation, these changes silently corrupt downstream features and models long before anyone notices.
- **Solution**:
    - Specify data contracts (schema, units, semantics, nullability) at pipeline boundaries, not just at the storage layer.
    - Add validation checks (schema checks, distribution checks, referential checks) at ingestion points that fail loudly rather than propagating silently.
- **Symptoms**:
    - A pipeline or feature-store design with no schema/contract validation step between stages owned by different teams.
    - A metric or model quietly degrades and the root cause traces back to an upstream definition change with no record of when it happened.
- **Detection Pattern**: A data-system design or refactor that depends on an upstream schema, unit, or semantic convention with no validation or contract enforcing that dependency at the boundary.
