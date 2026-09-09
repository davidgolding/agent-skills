# skill-creator — PEV-M Audit Report

Audited against the Pattern-Edge-Validation Matrix standard as defined in `skill-auditor/references/`.
Scope: `skill-creator/` — 12 files, 1451 lines.

---

## Executive Summary

`skill-creator` is a structurally strong skill. Every always-required reference file is present, all four reference-file shapes validate cleanly (12 sharp edges, 14 validations, 20 patterns/anti-patterns, 6 fully-formed interaction phases), progressive disclosure is intact, and no file is orphaned — every reference and template is reachable from `SKILL.md` through at most two hops.

Findings concentrate in one place: **`SKILL.md`'s `## Identity` section**. It is a pure persona assignment ("You are an expert agent architect…") and carries no statement of the criteria the skill judges against. This fires two rules — one error, one warning — and is the audit's only error-severity finding besides an incomplete Reference System Usage list.

Three lower-severity items follow: inert runtime notation in `interactions.md`, unlabeled principle bullets, and moderate verbosity in `interactions.md`'s Interaction Rules.

**Verdict:** compliant in structure, non-compliant in identity language. Four errors and warnings warrant a refactor; nothing here is a behavioral defect.

---

## Scorecard

Scores are rubric judgments derived from the countable signals listed under each axis. No value here is a computation of PEV-M's `U_t` formula.

| Axis | Score | Basis |
|---|---|---|
| PEV-M structural compliance | 4 / 5 | 7 of 8 shape rules pass; `skill-md-required-shape` fails on two counts |
| Affirmative-language quality | 4 / 5 | 25 negative-polarity tokens across 1451 lines (~1.7 per 100 lines) |
| Identity-language freedom | 1 / 5 | Persona section present, no Mandate section, discriminative-task skill |
| Description discoverability | 5 / 5 | 326 chars — inside the 200–500 band, well under the 1024 cap, carries "Use when" |
| Token efficiency | 4 / 5 | Clean lazy loading; verbosity concentrated in three `interactions.md` rules |

---

## Findings

### E1 — `mandate-section-task-framed` · error · SKILL.md:8-10

`SKILL.md` has `## Identity`, not `## Mandate`, and its content is entirely persona:

> You are an expert agent architect designed to guide the end-to-end lifecycle of an agent skill. Your objective is to help the user build, refine, and optimize high-leverage skills using a rigid, progressive evaluation loop.

Nothing here names the decision scope, the criteria source, or the success condition. Sharp edge `persona-degrades-discriminative-accuracy` fires alongside it: `skill-creator`'s own stated work includes running evals, measuring trigger accuracy, benchmarking with variance analysis, and validating against `references/validations.md` — discriminative tasks, the class where persona framing measurably costs accuracy.

**Fix:** replace with a `## Mandate` section stating what `skill-creator` decides (which skill to create or modify, and whether a draft meets the standard), the criteria source (`references/patterns.md`, `sharp_edges.md`, `validations.md`, `interactions.md`), and what a correct output contains (a skill whose files match the templates in `references/handoff.md` and pass the validations).

### E2 — `skill-md-required-shape` · error · SKILL.md:26-33

Two sub-failures:

1. The required heading is `## Mandate`; the file has `## Identity`. (Same site as E1.)
2. Reference System Usage carries a bullet for 4 of the 8 files in `references/`. Missing: `handoff.md`, `requirements_capture.md`, `synthesis_summary.md`, `visual_communication.md`.

The four uncited files are reachable — `interactions.md` points to the first three, `requirements_capture.md` points to the fourth — so this is a disclosure gap, not a dead-file problem. The rule requires a bullet for every reference file the skill actually has.

**Fix:** add `## Mandate`, then add four bullets. Given the depth, consider grouping: the four PEV-M files as the standing grounding set, the four workflow files under a "For the brainstorm workflow" bullet naming when each loads.

### W1 — `persona-identity-language` · warning · SKILL.md:10

Matches `^You are an?\b`. Single occurrence in the folder; every other file is clean. Resolved by the E1 fix.

Sharp edge `out-of-domain-persona-refusal` does **not** fire — the persona's domain ("agent architect") is at least as wide as the skill's trigger conditions, so no in-scope request falls outside it.

### W2 — `no-fictional-runtime-tokens` · error-severity rule, low practical impact · references/interactions.md:20

```
<feature_description> #$ARGUMENTS </feature_description>
```

`$ARGUMENTS` is real Claude Code syntax **in a slash-command file** — it is not interpreted inside a skill reference file, and the `#` prefix is not part of that syntax in any case. The `<feature_description>` wrapper is inert markup. The surrounding prose already handles the empty case correctly ("If the feature description above is empty, ask the user…"), so behavior is unaffected; the notation just implies substitution machinery that does not run here.

**Fix:** state it as prose — read the skill or feature description from the user's invoking message, and ask the opening question when none is present.

### W3 — Category-Guided, Label-Free Principles pattern · warning · SKILL.md:13-24

0 of 11 principle bullets carry a bold descriptive name. Several are bare fragments ("Explain why, not just what", "Stop when feedback is silent") that read as slogans rather than instructions. The `no-numbered-principle-labels` rule passes — there are no `P1`-style prefixes — but the pattern's positive requirement is unmet.

**Fix:** give each principle a short bold name and a full instruction clause, keeping the existing core → efficiency → gatekeeping → downstream ordering.

### W4 — `negative-polarity-instruction` · warning · 8 files, 25 occurrences

| File | Count |
|---|---|
| `references/synthesis_summary.md` | 9 |
| `references/patterns.md` | 4 |
| `references/sharp_edges.md` | 3 |
| `references/validations.md` | 2 |
| `references/interactions.md` | 2 |
| `references/handoff.md` | 2 |
| `references/requirements_capture.md` | 1 |
| `SKILL.md` | 1 |

Density is low (~1.7 per 100 lines) and a share of these sit inside anti-pattern and sharp-edge entries, where naming the thing to avoid is the entry's purpose. `synthesis_summary.md` is the real concentration.

**Fix:** rewrite the `synthesis_summary.md` occurrences per the Affirmative Rewrite pattern; leave occurrences that are the subject of an anti-pattern or sharp edge intact.

### W5 — Token efficiency · advisory

Two signals, neither severe:

- **Rule verbosity.** `interactions.md` Rules 4–6 run roughly 1100 words for three rules, and Rules 5 and 6 overlap substantially — both govern when a question should be open-ended. Merging them would cut length without losing a constraint.
- **Cross-file restatement.** The one-question-at-a-time constraint appears in five places (`SKILL.md:24`, `patterns.md:74`, `interactions.md:11`, `interactions.md:44`, `validations.md:117`). Each is a different register — principle, pattern, rule, phase gate, validation — which is how PEV-M is meant to work, so this is noted rather than flagged.

Phase 2.5's Agent Action also restates much of what it says lives in `synthesis_summary.md`, which partly defeats the deferral.

### H1 — Hygiene · advisory

- `references/patterns.md:13` — "Princoples" (typo for "Principles").
- 6 lines use typographic apostrophes (`’`), including the frontmatter `description`. Cosmetic; ASCII apostrophes are safer in YAML.

---

## Passing Checks

| Rule | Result |
|---|---|
| `required-reference-files-present` | pass — `patterns.md`, `sharp_edges.md`, `validations.md` all present |
| `interactions-conditional` | pass — heavily interactive skill, `interactions.md` present |
| `patterns-md-required-shape` | pass — 12 patterns, 8 anti-patterns, all fields, `---`-separated (the extra `Description` field is additive) |
| `sharp-edges-md-required-shape` | pass — 12 entries, all 8 fields, all severities in range |
| `validations-md-required-shape` | pass — 14 entries, all 7 fields, all severities and types in range |
| `interactions-md-required-shape` | pass — all 3 sections; 6 phases each carrying Objective / Agent Action / Human Gate / Proceed When / Pause When; Handoff complete |
| `skill-md-progressive-disclosure` | pass — `SKILL.md` carries only frontmatter and the three body sections |
| `description-length-over-cap` | pass — 326 chars |
| `description-length-out-of-band` | pass — 326 chars, inside 200–500 |
| `skill-assertive-trigger-missing` (skill's own rule) | pass — description contains "Use when" |
| `skill-absolute-path` (skill's own rule) | pass — every `/Users/` occurrence is inside rule-pattern or example text |
| File reachability | pass — all 8 references and 3 templates cited from `SKILL.md` within two hops |

---

## Change Script

Sequenced; each step is independently revertible.

1. **`SKILL.md`** — replace `## Identity` (lines 8-10) with `## Mandate`, task-framed per E1. *(resolves E1, W1, and sub-failure 1 of E2)*
2. **`SKILL.md`** — add Reference System Usage bullets for `handoff.md`, `requirements_capture.md`, `synthesis_summary.md`, `visual_communication.md`. *(resolves E2 sub-failure 2)*
3. **`SKILL.md`** — give all 11 principle bullets bold descriptive names and full instruction clauses; preserve current order and meaning. *(resolves W3)*
4. **`references/interactions.md`** — replace the `#$ARGUMENTS` / `<feature_description>` block at line 20 with prose. *(resolves W2)*
5. **`references/synthesis_summary.md`** — apply Affirmative Rewrite to its 9 negative-polarity instructions. *(resolves the bulk of W4)*
6. **`references/interactions.md`** — merge Rules 5 and 6 into one rule on open-ended questions. *(resolves half of W5)*
7. **`references/patterns.md`** — fix "Princoples" → "Principles" at line 13; normalize typographic apostrophes to ASCII across the folder. *(resolves H1)*

Steps 1–4 clear every error and warning. Steps 5–7 are quality improvements you may want to scope down or defer.

**Behavior parity:** no step removes an instruction, phase, gate, or trigger condition. Step 3 rewords principles without changing their meaning; step 6 merges two rules whose combined constraint set is preserved in full.

---

## Status

**Migrated.** The user approved the full change script; all 7 steps are applied.

### Post-migration re-audit

| Axis | Before | After |
|---|---|---|
| PEV-M structural compliance | 4 / 5 | 5 / 5 |
| Affirmative-language quality | 4 / 5 | 5 / 5 |
| Identity-language freedom | 1 / 5 | 5 / 5 |
| Description discoverability | 5 / 5 | 5 / 5 |
| Token efficiency | 4 / 5 | 5 / 5 |

Every error and warning is cleared: `## Mandate` replaces `## Identity` and is task-framed; all 8 reference files carry a Reference System Usage bullet; 11 of 11 principles are bold-named; no identity language, no runtime notation. Structural shapes revalidate unchanged — 12 sharp edges, 14 validations, 6 complete interaction phases.

**Behavior parity confirmed.** All 11 original principle concepts survive the rewrite. The six Interaction Rules become five by merging Rules 5 and 6, with both rules' constraint sets preserved in full and the (a)/(b)/(c) lettering kept intact so existing cross-references still resolve. All six execution phases, both handoff states, and every gate condition are unchanged.

**Amendment to W4.** The pre-migration count of 25 negative-polarity tokens was a regex tally, not an instruction count. On inspection only 4 of the 9 hits in `synthesis_summary.md` were negative-polarity *instructions* (lines 49, 72, 93, 250); the other 5 are descriptive prose ("the user never saw the whole", "a rule-grouping concept we don't have") where the negation is the meaning rather than a prohibition. The 4 instructions were rewritten; the descriptive occurrences were left intact. Folder total went 25 → 18, and the residue is anti-pattern and sharp-edge text where naming the avoided thing is the entry's purpose.

### New findings — surfaced during step 6, fixed on follow-up approval

Both were pre-existing and unaffected by the migration; the user approved them separately after the main script landed.

- **Mis-numbered rule citation** *(fixed)* — `references/synthesis_summary.md` lines 126, 132, and 168 cited "Interaction Rule 5(a)" to justify asking open-ended because an option menu would unintentionally influence the user's answer. That justification is case **(b)** of Rule 5; case (a) is the inherently-narrative one. All three now cite 5(b).
- **Wrong file cited** *(fixed)* — `synthesis_summary.md` lines 168 and 234, plus `handoff.md:9`, located the Interaction Rules "in `SKILL.md`". They live in `references/interactions.md`, which all five citations now name. Same-file references at `interactions.md:44` ("the Interaction Rules above") and `interactions.md:77` were already correct and are unchanged.

Rule 5's (a)/(b)/(c) lettering was preserved through the step 6 merge, so these citations resolve against the merged rule exactly as they would have against the original Rule 5.
