# Validations

This document defines the validations used by npc-creator.

---

## Valid Culture and Calling

- **Id**: valid-culture-calling
- **Severity**: warning
- **Type**: regex
- **Pattern**: `Culture:\s*(Barding|Dwarf|Elf|Hobbit|Bree-land|Ranger|Barding|Woodman|Rider of Rohan|Dunlending|Orc|Troll|Warg|Spectre|Wight)`
- **Message**: NPC culture does not match a standard Middle-earth culture.
- **Fix Action**: Align the NPC with a recognized culture from The One Ring core rulebook or supplements.
- **Applies To**:
    - `*.md`

---

## Dynamic Stats Correctness

- **Id**: dynamic-stats-check
- **Severity**: error
- **Type**: instruction
- **Pattern**: Ensure that adversary profiles (Orcs, Wargs, Trolls, Undead) feature a "Hate" or "Malice" attribute, whereas friendly/neutral NPCs feature a "Hope" attribute.
- **Message**: Adversary profile is missing Hate/Malice, or Friendly NPC is missing Hope.
- **Fix Action**: Update the stats table to feature the appropriate reserve stat depending on the NPC's faction.
- **Applies To**:
    - `*.md`

---
