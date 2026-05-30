# NPC Creator Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by npc-creator.

## Patterns

- **Name**: Dynamic Hope/Hate Selection
- **Description**: Select Hope for player-ally NPCs and Hate (or Malice/Shadow) for adversaries/enemies.
- **When**: Generating combat and resource stats for NPCs.
- **Example**:
```
| Stat | Value |
| --- | --- |
| Endurance | 18 |
| Hate | 4 (Adversary) |
```

---

- **Name**: Thematic Skill Mapping
- **Description**: Select common skills and ratings that match the standard cultural strengths and callings of the NPC.
- **When**: Assigning skill values to ensure thematic correctness.
- **Example**:
```
A Hobbit Shire-sheriff has:
- Courtesy: 2
- Riddle: 3
- Search: 2
```

---

## Anti-Patterns

- **Name**: Generic Fantasy Names
- **Description**: Generating names that do not match the linguistic style of the character's Culture.
- **Why**: Breaks the specific Middle-earth tone and cultural immersion.
- **Instead**: Use Tolkien-appropriate naming conventions (e.g., Old English styles for Rohirrim, Norse styles for Bardings/Dwarves).

---

- **Name**: Monolithic Block Output
- **Description**: Printing character attributes and combat stats in a single continuous text block or bulleted list.
- **Why**: Makes it difficult for Game Masters to quickly reference stats during prep or live play.
- **Instead**: Organize the profile using distinct Markdown tables for Attributes/Skills and Combat Stats.

---
