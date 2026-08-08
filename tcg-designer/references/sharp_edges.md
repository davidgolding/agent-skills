# TCG Designer Sharp Edges

This document defines the sharp edges used by tcg-designer.

## Core Loop Afterthought

- **Id**: core-loop-afterthought
- **Summary**: Building meta-systems, progression, or polish before proving the core moment-to-moment gameplay is engaging.
- **Severity**: critical
- **Situation**: Designing progression, economy, narrative, or art polish for a game whose core 30-second interaction loop remains unvalidated.
- **Why**: The core loop forms the foundation of playability; meta-systems cannot salvage an unengaging core interaction.
- **Solution**: Execute the Gray Box Test — isolate the core mechanic with minimal assets, remove rewards and progression, playtest for 10 minutes, and iterate until moment-to-moment play is intrinsically satisfying.
- **Symptoms**: Reliance on future progression to generate fun, lack of standalone core loop playtesting, or adding features to mask core engagement gaps.
- **Detection Pattern**: Proposals or implementations adding progression, economy, or narrative layers while the 30-second micro loop lacks standalone playtest validation.

---

## Feature Creep Spiral

- **Id**: feature-creep-spiral
- **Summary**: Continually adding features without cutting scope or assessing systemic interaction costs.
- **Severity**: critical
- **Situation**: Proposing new card types, extra sub-systems, or additional game modes while scope continuously expands.
- **Why**: Every feature introduces hidden costs in balancing, testing, UI real estate, rule cognitive load, and release pacing.
- **Solution**: Enforce the Three-Feature Rule and Feature Test — for every proposed addition, identify its direct benefit to the core loop and cut an equivalent feature from the scope.
- **Symptoms**: Feature lists expanding continuously without cuts, slipped milestones, or team hesitation to prune mechanics.
- **Detection Pattern**: Design updates adding mechanics or sub-systems without documenting corresponding scope reductions or core loop enhancements.

---

## Designing for Yourself

- **Id**: designing-for-yourself
- **Summary**: Prioritizing designer familiarity over empirical playtest feedback and target audience needs.
- **Severity**: critical
- **Situation**: Overriding playtest observations with personal design preferences or assuming players possess designer domain knowledge.
- **Why**: Designers possess complete rule knowledge, muscle memory, and strategic intent, rendering them unrepresentative of actual players.
- **Solution**: Execute the Stranger Test — observe fresh playtesters silently, record struggles without explaining choices, and design for defined player personas.
- **Symptoms**: Dismissing player confusion, insisting players read documentation, or relying primarily on internal designer testing.
- **Detection Pattern**: Design justifications citing designer intent or expected player behavior while disregarding observed playtest difficulty.

---

## Complexity Masquerading as Depth

- **Id**: complexity-masquerading-as-depth
- **Summary**: Multiplying rules and sub-systems under the assumption that rule count creates strategic depth.
- **Severity**: high
- **Situation**: Introducing complex rule interactions when strategic choices remain obvious or repetitive.
- **Why**: Excessive complexity causes cognitive overload and analysis paralysis rather than meaningful decision space.
- **Solution**: Execute the Simplification Test — remove individual sub-systems, evaluate whether strategic depth remains intact, and foster depth through rich interactions between simple mechanics.
- **Symptoms**: Overwhelmed new players, reliance on external guides for basic play, or dominant strategies persisting despite rule density.
- **Detection Pattern**: Rule sets expanding mechanical parameters without increasing situational choice variations or emergent playstyles.

---

## Tutorial as Band-Aid

- **Id**: tutorial-as-band-aid
- **Summary**: Relying on instructional popups or text dumps to fix unintuitive mechanics.
- **Severity**: high
- **Situation**: Adding tutorial explanatory text when playtesters struggle with complex rules.
- **Why**: Players frequently skip or forget instructional popups; unintuitive design cannot be solved by text explanations.
- **Solution**: Execute the No-Tutorial Test — remove explanatory text, restructure early gameplay environments with safe practice spaces and progressive gating, and teach mechanics through play.
- **Symptoms**: Expanding tutorial text, high player error after tutorial steps, or adding repetitive instructional popups.
- **Detection Pattern**: Adding instructional text blocks or popups to resolve playtester confusion instead of streamlining the underlying mechanic.

---

## Balanced Means Boring

- **Id**: balanced-means-boring
- **Summary**: Pursuing total mathematical homogenization at the expense of distinct playstyles and dynamic choices.
- **Severity**: high
- **Situation**: Equalizing all card stats and effects until choices feel cosmetic and power spikes disappear.
- **Why**: Complete symmetry eliminates strategic decision weight, discovery moments, and dynamic meta-game evolution.
- **Solution**: Architect strategic imbalance — implement rock-paper-scissors relationships, situational power spikes, and dynamic meta-rotations that reward tactical adaptation.
- **Symptoms**: Identical option performance, absent meta-game discussions, or exclusive reliance on numerical nerfing.
- **Detection Pattern**: Homogenizing card stats or resource costs across distinct factions/types to eliminate situational advantage variance.

---

## Punishment Over Teaching

- **Id**: punishment-over-teaching
- **Summary**: Imposing severe penalties or delayed resets on failure instead of guiding mastery.
- **Severity**: high
- **Situation**: Design layouts featuring long setback loops, heavy resource loss, or slow restarts upon loss.
- **Why**: Severe punishment discourages experimentation, suppresses risk-taking, and induces player attrition.
- **Solution**: Implement rapid restarts, clear cause-of-defeat feedback, room-by-room or turn-by-turn checkpoints, and progressive learning loops.
- **Symptoms**: Protracted respawn/reset times, heavy progress loss upon defeat, or frequent playtest abandonment.
- **Detection Pattern**: Mechanics imposing heavy resource wipes or long delay penalties following player errors instead of rapid iteration loops.

---

## Engagement Through Obligation

- **Id**: engagement-through-obligation
- **Summary**: Utilizing artificial lockouts, expiring rewards, and aggressive FOMO to drive player retention.
- **Severity**: high
- **Situation**: Designing daily expiring rewards, streak penalties, or artificial wait timers to force daily logins.
- **Why**: Retention driven by obligation creates player resentment and long-term churn once streaks break.
- **Solution**: Design for intrinsic motivation — provide rewarding gameplay, flexible progression schedules, and positive return incentives that respect player autonomy.
- **Symptoms**: Expiring reward mechanics, player feedback expressing forced play, or sharp retention drops following broken streaks.
- **Detection Pattern**: Inclusion of expiring streak mechanics or punitive missed-day resets within game design specifications.

---

## Ignoring Playtest Data

- **Id**: ignoring-playtest-data
- **Summary**: Dismissing playtest friction as player error rather than addressing underlying design flaws.
- **Severity**: critical
- **Situation**: Playtesters repeatedly encounter obstacles or misinterpret rules, but design remains unmodified.
- **Why**: Recurring player friction reflects genuine design defects; designer intent is invisible to players.
- **Solution**: Follow the Observation Rule — document playtest patterns, treat three identical player struggles as a definitive design bug, and adapt mechanics to actual player behavior.
- **Symptoms**: Explaining away negative feedback, defending choices during observation, or leaving identified playtest issues unaddressed.
- **Detection Pattern**: Playtest reports documenting recurring friction points without corresponding rule refactors in subsequent revisions.

---

## Over-Designing Before Prototyping

- **Id**: over-designing-before-prototyping
- **Summary**: Writing extensive design documentation before validating core ideas in playable prototypes.
- **Severity**: high
- **Situation**: Authoring long GDDs and complete card manifests before testing core mechanics in a prototype.
- **Why**: Unvalidated documentation rests on assumptions that frequently collapse once mechanics are played.
- **Solution**: Prototype first — create low-fidelity playable builds within one week, validate the fun through play, and maintain living documentation that records proven mechanics.
- **Symptoms**: Exhaustive GDDs without playable code, weeks of documentation preceding testing, or documentation un-updated post-playtest.
- **Detection Pattern**: Detailed card lists or rule manifests generated prior to basic prototype playtesting.

---

## Optimizing for Completionists

- **Id**: optimizing-for-completionists
- **Summary**: Allocating equal design effort to end-game content at the expense of early-to-mid player experience.
- **Severity**: medium
- **Situation**: Reserving primary set-pieces, mechanics, or polish exclusively for late-stage gameplay.
- **Why**: The majority of players experience early gameplay, while only a small percentage reach full completion.
- **Solution**: Front-load quality — ensure the first 30 minutes deliver maximum polish and engaging mechanics, while using modular systems for late-stage content.
- **Symptoms**: Rushed early-game onboarding, delayed mechanical payoff, or high player drop-off in initial stages.
- **Detection Pattern**: Concentrating unique mechanics or major visual polish in late-game stages while early stages remain basic.

---

## Progression as Fun-Substitute

- **Id**: progression-as-fun-substitute
- **Summary**: Relying on unlocks and numerical progression to mask an unengaging core loop.
- **Severity**: high
- **Situation**: Players demonstrate interest primarily during unlock screens while experiencing boredom during active play.
- **Why**: Progression systems extend engagement with fun games but cannot make a boring core loop enjoyable.
- **Solution**: Execute the Core Loop Test — unlock all content or remove progression entirely, verify that moment-to-moment play remains engaging, and use progression to add variety.
- **Symptoms**: Player engagement spiking only at unlock milestones, grinding complaints, or core play lacking appeal without rewards.
- **Detection Pattern**: Adding unlock tracks or level-up rewards to address feedback that core play feels repetitive or unengaging.

---

## Kitchen Sink Design

- **Id**: kitchen-sink-design
- **Summary**: Accumulating disparate mechanics without establishing a unified design focus.
- **Severity**: high
- **Situation**: Incorporating multiple unrelated mini-games, resource types, or combat modes into a single game.
- **Why**: Disparate mechanics compete for player attention, complicate onboarding, and dilute core game identity.
- **Solution**: Apply the Focus Test — state the core game identity in one sentence, enforce the Three-Feature Rule, and remove sub-systems that do not support the core identity.
- **Symptoms**: Difficulty summarizing the game in one sentence, competing mechanics, or player confusion over core objectives.
- **Detection Pattern**: Combining multiple distinct genre mechanics without a singular unifying core loop or thematic anchor.