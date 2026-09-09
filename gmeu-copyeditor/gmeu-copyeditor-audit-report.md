# gmeu-copyeditor — PEV-M Audit Report

Audited by `skill-auditor` against the PEV-M standard defined in
`skill-auditor/references/patterns.md`, `sharp_edges.md`, `validations.md`, and `interactions.md`.
Status: **plan only — no file in this skill has been modified except this report.**

---

## Executive Summary

`gmeu-copyeditor` is a substantive, well-researched skill with a clear domain (GMEU for usage,
CGG for grammar), a real output contract, and a genuine three-level rubric. Its content quality is
high; its PEV-M conformance is not. Four issues are blocking:

1. **`## Identity` replaces `## Mandate`** (SKILL.md:8–10). The section opens `You are an expert
   copyeditor…` — the exact shape `persona-degrades-discriminative-accuracy` warns about. Copyediting
   is discriminative work (judging whether a construction is an error, which authority governs it,
   whether a rewrite preserves voice), so this is the case where the persona cost lands hardest.
   Nothing in SKILL.md states the success condition the skill's output is measured against.
2. **`interactions.md` is missing** while the skill is clearly human-in-the-loop: Principle 1 prompts
   the user to choose a copyediting level, and Principle 7 asks the user to resolve usage problems or
   pick among alternatives. Its interaction loop currently lives as two clauses inside Principles.
3. **`validations.md` uses `Type: instruction`**, which is outside the permitted set
   `{regex, schema, semantic, syntax}`, on both entries. It also covers only output formatting —
   the level-selection and voice-statement contracts have no validation at all.
4. **Progressive disclosure is violated.** Principle 5 inlines the entire Light/Medium/Heavy rubric
   (SKILL.md:21–31) — reference-file-shaped content in the always-loaded file — and a trailing
   `**Note:**` section sits outside the four permitted SKILL.md sections.

The description is genuinely good: 474 characters, inside both the 1024 cap and the 200–500 discovery
band, with a what-it-does clause and a when-to-use clause. It carries one negative-polarity clause
worth rewriting, but no length action is needed.

---

## Scorecard

| Axis | Score | Basis |
|---|---|---|
| PEV-M structural compliance | **2 / 5** | Three required files present; `## Mandate` absent (replaced by `## Identity`); `interactions.md` missing despite detected human-in-the-loop behavior; `Type: instruction` invalid on both validations; rubric content inlined in SKILL.md; extra `**Note:**` section |
| Affirmative-language quality | **3 / 5** | 5 negative-polarity lines: SKILL.md:3, 16, 20, 25, 32. Low density for the file size, and each has a clean affirmative rewrite |
| Identity-language freedom | **1 / 5** | `## Identity` section assigns role, expertise, and specialization (SKILL.md:10); `Your role is to…`; no criteria-framed Mandate anywhere |
| Description discoverability | **5 / 5** | 474 chars — inside the 1024 cap and the 200–500 band; names both what and when |
| Token efficiency | **3 / 5** | Voice-preservation stated in 5 places (SKILL.md Identity, P2, P6; patterns.md pattern + anti-pattern; sharp_edges.md); citation format stated in 4 (SKILL.md P4, patterns.md, validations.md, sharp_edges.md). Non-blueprint `Description` field on every patterns.md entry. No fabricated $U_t$ value present — this is a heuristic rubric score |

**Rules fired**

| Id | Severity | Location |
|---|---|---|
| `persona-identity-language` | warning | SKILL.md:10 |
| `mandate-section-task-framed` | error | SKILL.md:8–10 |
| `persona-degrades-discriminative-accuracy` | high | SKILL.md:8–10 |
| `skill-md-required-shape` | error | SKILL.md:8 (`## Identity` where `## Mandate` belongs) |
| `interactions-conditional` | warning | folder structure (SKILL.md:14, 33 show the interaction loop) |
| `validations-md-required-shape` | error | validations.md:11, 24 (`Type: instruction`) |
| `skill-md-progressive-disclosure` | warning | SKILL.md:21–31, 45 |
| `negative-polarity-instruction` | warning | SKILL.md:3, 16, 20, 25, 32 |
| `description-length-out-of-band` | — | **passes** at 474 chars |
| `required-reference-files-present` | — | **passes** — all three present |
| `no-fictional-runtime-tokens` | — | **passes** — none found |
| `no-numbered-principle-labels` | — | **passes** — no `P1`-style prefixes |

---

## Change Script

Ordered; each step names its source and destination so behavior parity can be checked afterward.

**1. Replace `## Identity` with `## Mandate`** (SKILL.md:8–10)

Convert the persona into the criteria it stands in for — unit of work, authorities, success condition:

> ## Mandate
>
> Perform one copyediting or proofreading pass per invocation on user-provided text at a stated
> Light, Medium, or Heavy level. Evaluate usage against Garner's *Modern English Usage* (GMEU) and
> grammar against Garner's *The Chicago Guide to Grammar, Usage, and Punctuation* (CGG), grounding
> every judgment in `references/patterns.md`, `references/sharp_edges.md`,
> `references/validations.md`, and `references/interactions.md`. A correct pass states the author's
> identified voice before any suggestion, holds every change within the selected level's rubric,
> preserves that voice, and emits each suggestion as a bolded quotation of the referenced text, a
> colon, the commentary, and the governing inline citation.

**2. Add `references/interactions.md`** housing the interaction loop now embedded in Principles 1 and 7:

- **Interaction Rules** — turn-taking (end the turn and wait when the level is unstated or an
  alternative needs choosing); route level selection and alternative selection through the platform's
  blocking question tool; carry the identified voice and selected level forward in the conversation.
- **Execution Flow** — Phase 01 Establish Level (Proceed When: a level is stated or chosen; Pause
  When: the prompt names no level), Phase 02 Identify Voice (Proceed When: the voice has been stated
  to the user), Phase 03 Edit (Proceed When: every suggestion carries its citation and stays inside
  the level rubric; Pause When: a usage problem admits several defensible resolutions), Phase 04
  Report.
- **Handoff** — Completion State: every suggestion formatted and cited, voice statement present.
  Exception/Fallback: when no GMEU entry or CGG section governs a suspected problem, present it to
  the user as an unresolved query rather than citing an unverified entry.

**3. Move the level rubric out of SKILL.md** (Principle 5, SKILL.md:21–31)

Relocate the Mechanical / Correlating Parts / Language / Content editing rubric into
`references/patterns.md` as three patterns — *Light Level Rubric*, *Medium Level Rubric*,
*Heavy Level Rubric* (each Name/When/Example) — plus one *Mechanical and Correlating-Parts Sweep*
pattern covering the all-levels rows. Principle 5 becomes a one-line pointer:
"**Level-Bounded Editing**: Hold every suggestion inside the rubric for the selected level, as
defined in `references/patterns.md`."

**4. Rewrite the five negative-polarity instructions**

| Line | Before | After |
|---|---|---|
| SKILL.md:3 | "Do not use for general content rewriting, formatting, indexing, or deep stylistic reviews." | "Scope this skill to copyediting and proofreading passes; route content rewriting, formatting, indexing, and deep stylistic review elsewhere." |
| SKILL.md:16 | "Do not apply generic AI writing styles or personal stylistic preferences." | "Ground every usage and grammar judgment in a GMEU entry or CGG section, so each suggestion traces to a cited authority rather than a stylistic preference." |
| SKILL.md:20 | "Proofreading suggestions (spelling/typos) do not require citations." | "Emit proofreading suggestions (spelling, typos) as commentary alone; reserve citations for usage and grammar suggestions." |
| SKILL.md:25 | "Point out (do not revise) egregiously wordy paragraphs." | "Point out egregiously wordy paragraphs, leaving the prose itself for the author to revise." |
| SKILL.md:32 | "Do not machete or rewrite a manuscript unless explicitly applying Heavy language editing. If sentences are clear, correct, and serviceable, leave them be." | "Reserve wholesale rewriting for Heavy language editing, and leave clear, correct, serviceable sentences as the author wrote them." |

**5. Fix `validations.md`** — change `Type: instruction` to `Type: syntax` on `output-format-compliance`
and `source-citation-format-compliance`; replace `Applies To: *` with the concrete surface
(`copyediting commentary output`). Add three validations the skill's own contract implies but that are
currently unenforced:

- `copyediting-level-established` (error, semantic) — an editing pass proceeding with no Light/Medium/Heavy level stated or chosen.
- `voice-statement-precedes-suggestions` (error, semantic) — suggestions emitted before the identified voice has been stated.
- `level-rubric-scope-respected` (warning, semantic) — a suggestion exceeding the selected level's rubric (e.g. a rewrite offered under Light).

**6. Drop the trailing `**Note:**` section** (SKILL.md:45) and fold its intent into the Reference
System Usage grounding directive; add the `interactions.md` bullet there for the new file, and label
the four bullets as states to match the reference-usage template.

**7. Tidy `references/patterns.md` and `references/sharp_edges.md`**

- Remove the non-blueprint `Description` field from pattern entries, folding its content into
  `When` or `Example` (anti-pattern entries keep Name/Why/Instead).
- Add a `## Patterns` / `## Anti-Patterns` check on the two new-rubric patterns' placement.
- Add one sharp edge, `level-scope-creep` (severity medium): Light or Medium passes drifting into
  Heavy-level rewriting because a convoluted sentence invites it.
- Add sharp edge `unstated-voice` (severity medium): editing begins before the author's voice is
  identified and stated, so voice preservation has no baseline to check against.

**8. Behavior parity check** — confirm all nine original principles, both original patterns, both
original anti-patterns, both original sharp edges, and both original validations have a destination in
the migrated file set, with no clause dropped.

---

## Migration Status

**Complete.** All eight steps applied after user approval.

### Post-migration scorecard

| Axis | Before | After | Basis |
|---|---|---|---|
| PEV-M structural compliance | 2 / 5 | **5 / 5** | `## Mandate` / `## Principles` / `## Reference System Usage` in order; all four reference files present; every sharp edge carries its eight fields, every validation its seven, every pattern Name/When/Example, every anti-pattern Name/Why/Instead; Severity values in `{high, medium}`, validation Severity in `{error, warning}`, Type in `{syntax, semantic}` |
| Affirmative-language quality | 3 / 5 | **5 / 5** | 0 negative-polarity matches across SKILL.md and all four reference files |
| Identity-language freedom | 1 / 5 | **5 / 5** | 0 identity-pattern matches; `## Identity` replaced by a criteria-framed `## Mandate` naming unit of work, authorities, grounding files, and success condition |
| Description discoverability | 5 / 5 | **5 / 5** | 496 characters — inside the 1024 cap and the 200–500 band |
| Token efficiency | 3 / 5 | **4 / 5** | Level rubric now stated once (patterns.md) rather than inlined in SKILL.md; non-blueprint `Description` field removed from pattern entries; trailing `**Note:**` folded into the grounding directive. Voice preservation and citation format remain stated across several files, which is the intended cross-state reinforcement rather than redundancy |

### Changes applied

1. `## Identity` → `## Mandate`, criteria-framed (SKILL.md).
2. `references/interactions.md` created — Interaction Rules, four phase blocks (Establish Level, Identify Voice, Edit, Report) each with Objective / Agent Action / Human Gate-Intervention / Proceed When / Pause When, and Handoff with Completion State plus Exception/Fallback.
3. Level rubric moved from SKILL.md Principle 5 into patterns.md as four patterns — Mechanical and Correlating-Parts Sweep, Light Level Rubric, Medium Level Rubric, Heavy Level Rubric. Principle 5 became the pointer **Level-Bounded Editing**.
4. All five negative-polarity instructions rewritten affirmatively, per the plan's table.
5. `Type: instruction` → `Type: syntax` on both original validations; `Applies To: *` replaced with concrete surfaces; four validations added — `copyediting-level-established`, `voice-statement-precedes-suggestions`, `level-rubric-scope-respected`, and `proofreading-pass-scope` (added to cover Principle 8, which had no validation).
6. Trailing `**Note:**` section folded into the Reference System Usage grounding directive; `interactions.md` bullet added; the four bullets labeled `[State 01]`–`[State 04]`.
7. `Description` field removed from patterns.md pattern entries (folded into `When`); sharp edges `unstated-voice` and `level-scope-creep` added; anti-pattern `Level Scope Creep` added; sharp_edges.md H1 corrected to name the skill.
8. Behavior parity confirmed — all nine original principles, both original patterns, both original anti-patterns, both original sharp edges, and both original validations have destinations in the migrated set, with distinctive original phrasing (voice definition, Hemingway/Steinbeck exemplars, mechanical and correlating-parts detail, both citation examples, the level rubrics, the "clear, correct, and serviceable" clause, and the conflict-resolution note) verified present.

### Final file set

```
gmeu-copyeditor/
├── SKILL.md
├── gmeu-copyeditor-audit-report.md
└── references/
    ├── patterns.md        6 patterns, 3 anti-patterns
    ├── sharp_edges.md     4 sharp edges
    ├── validations.md     6 validations
    └── interactions.md    4 phases
```
