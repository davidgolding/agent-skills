# TCG Designer Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by tcg-designer.

## Patterns

- **Name**: The 30/30/30 Loop Design
- **When**: Starting any game design or evaluating if the core loop generates intrinsic player satisfaction across time scales.
- **Example**:
```md
Design three interlocking loops across timescales:

1. 30-Second Loop (Micro): Moment-to-moment gameplay action. Validate that this action generates intrinsic satisfaction without progression or rewards.
2. 30-Minute Loop (Meso): Session structure and match rhythm. Provide natural pause points and compelling next-session hooks.
3. 30-Hour Loop (Macro): Long-term progression, card collection, ranking, and strategic mastery.

Reinforce alignment: Micro success fuels Meso progress, which drives Macro advancement.
```

---

- **Name**: Meaningful Decisions Framework
- **When**: Designing player choices in combat, deck building, or resource allocation to ensure every decision carries strategic weight.
- **Example**:
```md
Structure decisions around five core criteria:
1. Situational Trade-offs: Ensure options excel under distinct game contexts rather than offering a single dominant choice.
2. Incomplete Information: Include managed probability or hidden information so choices require weighing risks.
3. Contextual Value: Change optimal play dynamically as game state evolves.
4. Consequential Choices: Require players to commit to choices with lasting board or resource impact.
5. Multiple Valid Paths: Provide distinct strategic approaches with balanced costs and benefits.
```

---

- **Name**: Vlambeer Juice Philosophy
- **When**: Polishing gameplay feel to make card plays, attacks, and board interactions feel impactful and responsive.
- **Example**:
```md
Layer visual, auditory, and kinetic feedback onto every action:
- Visual: Particle effects, card impact flashes, dynamic damage numbers, subtle screen shake or zoom pulses.
- Audio: Layered impact sounds with pitch randomization, vocalizations, and environmental responses.
- Kinetic/Timing: Brief hit-stop micro-pauses on heavy hits, card recoil animations, and weight-based motion curves.
Result: Feedback makes interactions feel intuitive, tactile, and powerful.
```

---

- **Name**: Flow Channel Design
- **When**: Calibrating difficulty progression, dynamic handicaps, and adaptive challenges to sustain player engagement.
- **Example**:
```md
Sustain players in the optimal flow zone between boredom and anxiety:
1. Dynamic Difficulty Adjustment: Silently tune parameters (draw recovery, catch-up mechanics) to maintain tension.
2. Mastery-Gated Progression: Unlock advanced card sets or complex game modes as player skill develops.
3. Accessible Depth: Provide clear surface rules for beginners while rewarding advanced positioning and card synergies.
4. Rapid Restart: Keep loss recovery fast so players immediately re-engage and learn through iteration.
```

---

- **Name**: Friction vs. Flow Design
- **When**: Evaluating mechanics that introduce resistance or slow player actions.
- **Example**:
```md
Distinguish meaningful resistance from frustrating obstacles:
- Meaningful Resistance: Resource management, turn timers, positioning constraints, and deck size limits that force tactical decisions.
- Resistance Audit: Verify that resistance creates interesting decisions, serves the game fantasy, and makes success feel earned. Streamline UI tedium, unskippable animations, and redundant confirmation prompts.
```

---

- **Name**: Player Motivation Frameworks
- **When**: Defining player personas, reward systems, and playstyle incentives.
- **Example**:
```md
Target core intrinsic needs and player archetypes:
- Self-Determination Theory: Fulfill Autonomy (player choices), Competence (visible skill growth), and Relatedness (community and competition).
- Archetype Alignment: Support Dominance/PvP (Killers), Completion/Unlocks (Achievers), Social/Guilds (Socializers), and Secret Discovery/Lore (Explorers).
Master 2-3 core types of fun rather than attempting universal coverage.
```

---

- **Name**: MDA Framework Application
- **When**: Architecting new game systems from emotional goals down to concrete rule parameters.
- **Example**:
```md
Design in reverse from Aesthetics down to Mechanics:
1. Aesthetics: Define the target emotional experience (e.g., tension, tactical triumph, wonder).
2. Dynamics: Determine emergent player behaviors that generate those emotions (e.g., bluffing, resource hoarding, aggressive pushing).
3. Mechanics: Specify exact rule verbs, card stats, draw rates, and resource costs that induce those dynamics.
```

---

- **Name**: Onboarding Without Tutorials
- **When**: Designing the first-time user experience and initial match progressions.
- **Example**:
```md
Teach mechanics through structured gameplay environment:
1. Safe Practice: Introduce fundamental mechanics in low-stakes scenarios where initial mistakes carry minimal penalty.
2. Progressive Escalation: Introduce one new rule or card mechanic at a time, requiring mastery before layering complexity.
3. Environmental Guidance: Use visual highlights, mandatory interaction gates, and contextual prompts at the exact moment of relevance.
```

---

- **Name**: Risk-Reward Calibration
- **When**: Designing high-stakes card effects, resource investments, and tactical push-your-luck mechanics.
- **Example**:
```md
Calibrate risk tiers so high-stakes choices feel fair and exciting:
- Low Risk / Low Reward: Safe, steady options suitable for stabilizing board state.
- Medium Risk / Medium Reward: Core tactical plays forming standard gameplay.
- High Risk / High Reward: Dramatic plays with significant failure potential paired with game-turning payoffs.
Ensure all high-risk choices are opt-in and transparent regarding potential stakes.
```

---

- **Name**: Emergence vs. Authored Design
- **When**: Balancing structured campaign scenarios with open-ended sandbox play and systemic card interactions.
- **Example**:
```md
Combine authored structure with emergent systemic depth:
- Authored Elements: Story set-pieces, tutorial scenarios, and curated boss challenges for reliable emotional beats.
- Emergent Elements: Modular card mechanics and environmental interactions that allow players to discover unique combos and unscripted solutions.
```

---

- **Name**: Skill Ceiling vs. Skill Floor
- **When**: Architecting mechanic inputs and card text to ensure accessibility for beginners alongside depth for experts.
- **Example**:
```md
Aim for low skill floor paired with high skill ceiling:
- Accessible Entry: Provide simple card text and straightforward action verbs so novice players participate immediately.
- Strategic Depth: Design subtle card synergies, timing nuances, and positioning interactions that allow experienced players to optimize outcomes continuously.
```

---

- **Name**: Feedback Loop Design
- **When**: Balancing competitive stability, catch-up mechanics, and game-ending momentum.
- **Example**:
```md
Structure positive and negative feedback loops across match phases:
- Positive Feedback (Reinforcing): Allow early tactical leads to build momentum toward decisive match completion.
- Negative Feedback (Balancing): Introduce catch-up resource boosts or comeback mechanics to sustain match tension until late game.
- Synthesis: Combine early positive momentum, mid-game balancing tension, and late-game decisive resolution.
```

---

## Anti-Patterns

- **Name**: Designing for Yourself
- **Why**: Designing exclusively for your own familiarity blinds you to beginner learning curves, hidden assumptions, and unintuitive mechanics.
- **Instead**: Conduct blind playtests with fresh players, observe without interrupting or explaining, and refine design based on empirical player actions.

---

- **Name**: Feature Before Core
- **Why**: Adding meta-progression, narrative, or secondary features to an unproven core loop wastes effort on a weak foundation.
- **Instead**: Validate the core 30-second loop using simple prototypes, ensuring intrinsic satisfaction before building meta-systems.

---

- **Name**: Complexity as Depth
- **Why**: Adding excessive rules or sub-systems increases cognitive load and analysis paralysis without expanding strategic decision space.
- **Instead**: Streamline rule counts and enhance depth through rich, emergent interactions between simple, elegant mechanics.

---

- **Name**: Tutorial as Band-Aid
- **Why**: Relying on intrusive tutorial text to fix unintuitive rules frustrates players who skip or forget instructional popups.
- **Instead**: Redesign early levels and UI layout so mechanics are learned intuitively through self-evident gameplay.

---

- **Name**: Balanced Equals Fair
- **Why**: Homogenizing card stats and outcomes eliminates strategic distinction, discovery moments, and dynamic meta-game evolution.
- **Instead**: Create situational power spikes and contextual advantages that reward strategic foresight and dynamic play.

---

- **Name**: Punishing Failure, Not Teaching
- **Why**: Severe loss penalties and delayed resets discourage experimentation and induce player frustration.
- **Instead**: Provide rapid restarts, clear feedback on defeat causes, and immediate opportunities to re-engage with revised strategies.

---

- **Name**: Engagement Through Obligation
- **Why**: Utilizing aggressive FOMO, expiring rewards, and artificial lockouts breeds player resentment and eventual abandonment.
- **Instead**: Build intrinsic motivation through rewarding gameplay, flexible progression schedules, and respect for player time.

---

- **Name**: Designing for 100% Completion
- **Why**: Concentrating top-tier content exclusively in end-game stages starves the majority of players who experience primarily early-to-mid gameplay.
- **Instead**: Front-load quality into initial play sessions so every player experiences compelling content immediately.

---

- **Name**: Ignoring Playtest Data
- **Why**: Dismissing consistent playtest friction as player error preserves design flaws and damages user adoption.
- **Instead**: Treat recurring playtest struggles as empirical proof of design defects, adapting mechanics to align with actual player behavior.