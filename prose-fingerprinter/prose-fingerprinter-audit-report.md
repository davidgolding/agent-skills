# prose-fingerprinter — PEV-M Audit Report

Audited by `skill-auditor` against the PEV-M standard defined in
`skill-auditor/references/patterns.md`, `sharp_edges.md`, `validations.md`, and `interactions.md`.
Status: **plan only — no file in this skill has been modified except this report.**

---

## Executive Summary

`prose-fingerprinter` has an unusually good core idea — deconstruct prose into syntactic, prosodic,
etymological, presentation-mode, and thematic machinery, then synthesize a "consciousness engine"
reading rather than a metrics dump. The anti-pattern *Flat Metric Reporting* is the sharpest single
entry in the folder and states exactly the failure this kind of skill falls into. What the folder
lacks is coverage: five analytic dimensions and a stated comparison-table output are supported by
one pattern, one anti-pattern, one sharp edge, and one validation.

Five issues, one of which is blocking in the practical sense rather than the structural one:

1. **The mandated helper script does not exist.** SKILL.md:15 instructs *"Use the helper script to
   compute syllable scansion, sentence structures, and etymological roots for exact, reproducible
   metrics."* The folder contains `SKILL.md` and three reference files — no `scripts/` directory, no
   executable of any kind. The principle that carries the skill's whole claim to determinism points
   at nothing. This is the highest-value finding in the audit and it needs your decision (see
   step 2 below), because the two available repairs produce materially different skills.
2. **`## Identity` replaces `## Mandate`** (SKILL.md:8–10): *"You are an expert literary stylist and
   quantitative text analyst."* Fingerprinting is discriminative work — measuring, classifying,
   attributing a signature — which is precisely where `persona-degrades-discriminative-accuracy`
   applies. No section states what makes a fingerprint correct.
3. **`Type: instruction`** on the sole validation (validations.md:11) is outside the permitted set
   `{regex, schema, semantic, syntax}`.
4. **Reference coverage is thin against the skill's own claims.** No pattern defines the fingerprint
   output shape or the comparison table that Principle 4 promises; no validation enforces the
   metric-plus-explanation contract that the folder's best anti-pattern establishes; and no sharp
   edge covers the dominant real risk in this domain — fabricated scansion and invented etymological
   roots stated with the confidence of computed output.
5. **Progressive disclosure**: a trailing `**Note:**` section sits outside the four permitted
   SKILL.md sections, and every `patterns.md` entry carries a non-blueprint `Description` field.

The description is the folder's strongest compliance point: 280 characters, inside both the 1024 cap
and the 200–500 discovery band, with a clean what-clause and when-clause.

---

## Scorecard

| Axis | Score | Basis |
|---|---|---|
| PEV-M structural compliance | **2 / 5** | Three required files present; `## Mandate` absent (replaced by `## Identity`); `Type: instruction` invalid; `interactions.md` missing despite a mid-task user prompt; trailing `**Note:**` section; Reference System Usage names no bullet for the script the skill mandates |
| Affirmative-language quality | **4 / 5** | One negative-polarity match (patterns.md:21, *"do not reveal"*) — and it sits in an anti-pattern `Why` field, which is explanatory rather than instructional, so the cost is low |
| Identity-language freedom | **1 / 5** | `## Identity` assigns role and expertise (SKILL.md:10); *"Your objective is to…"*; no criteria-framed Mandate |
| Description discoverability | **5 / 5** | 280 chars — inside the 1024 cap and the 200–500 band; names both what and when |
| Token efficiency | **4 / 5** | Low redundancy and no cross-file repetition at 5.1 KB total; deductions for the non-blueprint `Description` field on every pattern entry and the trailing `**Note:**`. No fabricated $U_t$ value present — this is a heuristic rubric score |

**Rules fired**

| Id | Severity | Location |
|---|---|---|
| `persona-identity-language` | warning | SKILL.md:10 |
| `mandate-section-task-framed` | error | SKILL.md:8–10 |
| `persona-degrades-discriminative-accuracy` | high | SKILL.md:8–10 |
| `skill-md-required-shape` | error | SKILL.md:8 (`## Identity` where `## Mandate` belongs); Reference System Usage carries no bullet for the mandated script |
| `validations-md-required-shape` | error | validations.md:11 (`Type: instruction`) |
| `interactions-conditional` | warning | folder structure (validations.md:14 prompts the user mid-task) |
| `skill-md-progressive-disclosure` | warning | SKILL.md:27 |
| `negative-polarity-instruction` | warning | patterns.md:21 |
| `description-length-out-of-band` | — | **passes** at 280 chars |
| `required-reference-files-present` | — | **passes** — all three present |
| `no-fictional-runtime-tokens` | — | **passes** — none found |
| `no-numbered-principle-labels` | — | **passes** — no `P1`-style prefixes |

Note on the `interactions.md` requirement: this skill sits near the line. Its only human-in-the-loop
behavior is the `min-passage-length` fix action asking the user for a longer sample, plus the implied
sampling decision on oversized inputs. That is a genuine mid-task prompt, so the requirement holds —
but the resulting file should stay small and describe two real gates rather than being padded into a
four-phase flow the skill does not have.

---

## Change Script

Ordered; each step names its source and destination so behavior parity can be checked afterward.

**1. Replace `## Identity` with `## Mandate`** (SKILL.md:8–10)

> ## Mandate
>
> Extract one prose fingerprint per invocation from a user-supplied passage, profiling five
> dimensions: syntactic architecture, prosodic scansion, etymological register, presentation-mode
> mix, and thematic clustering. Ground every judgment in `references/patterns.md`,
> `references/sharp_edges.md`, `references/validations.md`, and `references/interactions.md`. A
> correct fingerprint reports each dimension with its measurement basis stated, pairs every
> quantitative finding with the stylistic function it performs, synthesizes the dimensions into a
> single consciousness-engine reading rather than a metrics list, and marks any figure estimated by
> inspection rather than computed.

**2. Resolve the missing helper script — needs your decision.** Two repairs, materially different:

- **Option A — Write the script** (`scripts/fingerprint.py`): a deterministic analyzer taking text
  on stdin and emitting JSON — syllable counts and stress scansion, sentence-boundary and
  clause-structure counts (parataxis vs. hypotaxis ratio), and etymological classification by root
  language. Keeps Principle 2's determinism claim true and makes fingerprints reproducible across
  runs. Costs real implementation work, and the etymological classifier needs a bundled root
  lexicon to avoid becoming a guess in a trench coat.
- **Option B — Restate the principle honestly** (recommended if you want this closed today):
  rewrite Principle 2 as **Measurement Basis Disclosure** — the agent performs the analysis by
  inspection and states, for each reported figure, whether it was counted exhaustively or estimated
  from a sample. Add the sharp edge in step 4 to govern the fabrication risk this option carries.

Option B is the smaller change and removes a false claim immediately. Option A is the better skill
if you intend to invest in it. I recommend **B now, A later** — they compose: adopting A afterward
means swapping the principle back and adding a `scripts/` bullet to Reference System Usage.
Either way, the current state — mandating an asset that does not exist — is the one option to rule out.

**3. Add patterns for the skill's undocumented output contract** (`references/patterns.md`)

- *Fingerprint Report Shape* — the five dimensions in fixed order, each with measurement, basis, and
  stylistic function; the consciousness-engine synthesis last.
- *Comparison Table Construction* — realizes Principle 4, which currently has no pattern behind it:
  one row per dimension, one column per text, synthesis row at the bottom.
- *Representative Sampling* — realizes the `context-exhaustion` solution as a positive procedure:
  select 1,000–2,000 words spanning the text's range, disclose the sample size and location, and
  average across chunks for longer works.
- Remove the non-blueprint `Description` field from pattern entries, folding its content into
  `When` or `Example`.
- Add anti-pattern *Undisclosed Estimation* — reporting an inspected figure in the register of a
  computed one.

**4. Add sharp edges for the domain's real failure modes** (`references/sharp_edges.md`)

- `fabricated-scansion` (severity **high**) — stress patterns and syllable counts asserted as
  measured when they were produced by inspection; a spondee count is checkable, so a wrong one is
  falsifiable in a way a thematic reading is not.
- `invented-etymology` (severity **high**) — root-language attributions assigned by how a word
  *sounds* Germanic or Latinate rather than by its actual derivation, which inverts the register
  reading built on top of it.
- `single-author-projection` (severity **medium**) — the fingerprint collapsing onto a famous
  exemplar (the folder's own example reaches for Hemingway) instead of describing the passage in
  front of it.
- Rename the H1 from `# Sharp Edges` to `# Prose Fingerprinter Sharp Edges` for consistency with
  `patterns.md`.

**5. Fix and extend `references/validations.md`**

- `min-passage-length`: `Type: instruction` → `Type: semantic`; replace `Applies To: *.txt / *.md`
  with the analytic surface (`input passage`), since the check applies to pasted text as much as to
  files.
- Add `metric-paired-with-function` (error, semantic) — a quantitative finding reported without the
  stylistic function it performs, enforcing the folder's own *Flat Metric Reporting* anti-pattern,
  which currently has no validation behind it.
- Add `measurement-basis-disclosed` (error, semantic) — a figure reported without stating whether it
  was counted or estimated.
- Add `all-five-dimensions-reported` (warning, schema) — a fingerprint omitting one of the five
  dimensions without saying why the passage does not support it.
- Rename the H1 to `# Prose Fingerprinter Validations`.

**6. Add `references/interactions.md`**, kept deliberately small — two real gates:

- **Interaction Rules** — end the turn and wait when the passage is too short to fingerprint or
  when an oversized input needs a sampling decision; route the sampling choice through the
  platform's blocking question tool; carry the stated sample size and location forward.
- **Execution Flow** — Phase 01 Intake (Proceed When: the passage is at least 150 words and under
  the sampling threshold; Pause When: it is shorter, or long enough to need a sampling decision),
  Phase 02 Analyze, Phase 03 Synthesize and Report.
- **Handoff** — Completion State: five dimensions reported with bases disclosed, every metric paired
  with its function, synthesis present. Exception/Fallback: when a dimension is not measurable from
  the passage, report the gap rather than estimating past it.

**7. Drop the trailing `**Note:**` section** (SKILL.md:27), folding its intent into the Reference
System Usage grounding directive; add the `interactions.md` bullet; label the bullets
`[State 01]`–`[State 04]`.

**8. Rewrite the one negative-polarity clause** (patterns.md:21): *"Raw numbers alone do not reveal
the 'music' or the 'consciousness' of the text"* → *"The music and the consciousness of a text
surface only once each number is paired with the effect it produces."*

**9. Behavior parity check** — confirm all four original principles, the original pattern, the
original anti-pattern, the original sharp edge, and the original validation have destinations in the
migrated set, with no clause dropped. Note that step 2 is the one deliberate behavior *change* rather
than a relocation, and it is the change you are approving.

---

## Migration Status

**Complete.** All nine steps applied after user approval. Step 2 resolved as **Option B** — the
helper-script references were removed and the skill now performs its analysis by close inspection
with the measurement basis disclosed for every figure.

### Post-migration scorecard

| Axis | Before | After | Basis |
|---|---|---|---|
| PEV-M structural compliance | 2 / 5 | **5 / 5** | `## Mandate` / `## Principles` / `## Reference System Usage` in order; all four reference files present; 4 patterns (Name/When/Example) and 3 anti-patterns (Name/Why/Instead); 4 sharp edges carrying all eight fields with Severity in `{high, medium}`; 4 validations carrying all seven fields with Severity in `{error, warning}` and Type in `{semantic, schema}`; interactions.md with Interaction Rules, three phase blocks, and Handoff |
| Affirmative-language quality | 4 / 5 | **5 / 5** | 0 negative-polarity matches across SKILL.md and all four reference files |
| Identity-language freedom | 1 / 5 | **5 / 5** | 0 identity-pattern matches; `## Identity` replaced by a criteria-framed `## Mandate` naming the five dimensions, the grounding files, and the success condition |
| Description discoverability | 5 / 5 | **5 / 5** | 280 characters, unchanged — inside the 1024 cap and the 200–500 band, and it made no reference to the removed script |
| Token efficiency | 4 / 5 | **4 / 5** | Non-blueprint `Description` field removed from all pattern entries; trailing `**Note:**` folded into the grounding directive. The folder grew from 5.1 KB to roughly 18 KB, all of it new coverage — three patterns, three sharp edges, three validations, and an interactions file the skill's own claims required. Score held rather than raised: the added material is warranted, and the sampling thresholds and word-count bands now appear in two or three files each as intended cross-state reinforcement |

### Changes applied

1. `## Identity` → `## Mandate`, criteria-framed (SKILL.md).
2. **Helper-script references removed.** Principle 2 *"Rely on Deterministic Processing — use the
   helper script to compute syllable scansion, sentence structures, and etymological roots"* became
   **Measurement Basis Disclosure**: analyze by close inspection, and state for each figure whether
   it was counted exhaustively or estimated from a named sample. Verified: no reference to a helper
   script, a `scripts/` path, or an executable remains anywhere outside this report.
3. Patterns added to `patterns.md` — *Fingerprint Report Shape*, *Comparison Table Construction*
   (realizing Principle 4, which previously had no pattern behind it), and *Representative Sampling*
   (turning the `context-exhaustion` solution into a positive procedure). The `Description` field was
   removed from every pattern entry, folded into `When`. Anti-patterns *Undisclosed Estimation* and
   *Single-Author Projection* added.
4. Sharp edges added — `fabricated-scansion` (high), `invented-etymology` (high),
   `single-author-projection` (medium); `context-exhaustion` retained and pointed at the new sampling
   pattern; H1 renamed to name the skill.
5. `min-passage-length`: `Type: instruction` → `Type: semantic`, `Applies To: *.txt / *.md` →
   `input passage`. Validations added — `metric-paired-with-function` (enforcing the folder's own
   *Flat Metric Reporting* anti-pattern, previously unenforced), `measurement-basis-disclosed`
   (enforcing the new Principle 2), and `all-five-dimensions-reported`. H1 renamed.
6. `references/interactions.md` created — Interaction Rules, three phase blocks (Intake, Analyze,
   Synthesize and Report) each with Objective / Agent Action / Human Gate-Intervention / Proceed When
   / Pause When, and Handoff with Completion State plus Exception/Fallback. Kept to the skill's real
   gates: the short-passage prompt, the sampling decision, and a mixed-voice passage.
7. Trailing `**Note:**` folded into the Reference System Usage grounding directive; `interactions.md`
   bullet added; bullets labeled `[State 01]`–`[State 04]`.
8. The negative-polarity clause at the old patterns.md:21 rewritten affirmatively; two further
   `never` clauses introduced during drafting were caught by the verification sweep and rewritten.
9. Behavior parity confirmed — all four original principles, the original pattern, the original
   anti-pattern, the original sharp edge, and the original validation have destinations in the
   migrated set, with the original's distinctive material (parataxis and spondaic examples, the
   Germanic/Anglo-Saxon register reading, the coordinate-ratio explanation, the 150-word floor, the
   300-to-1,000-word request, the 1,000-to-2,000-word sample, the 3,000-word and 20,000-word
   thresholds) verified present. Step 2 is the one deliberate behavior change rather than a
   relocation: the skill no longer claims computed determinism, and discloses its measurement basis
   instead.

### Final file set

```
prose-fingerprinter/
├── SKILL.md
├── prose-fingerprinter-audit-report.md
└── references/
    ├── patterns.md        4 patterns, 3 anti-patterns
    ├── sharp_edges.md     4 sharp edges
    ├── validations.md     4 validations
    └── interactions.md    3 phases
```
