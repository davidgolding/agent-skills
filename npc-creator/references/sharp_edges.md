# Sharp Edges

This document defines the sharp edges used by npc-creator.

---

## System Edition Drift

- **Id**: edition-drift
- **Summary**: Confusing rules and terminology between The One Ring TTRPG 1st Edition and 2nd Edition.
- **Severity**: high
- **Situation**: When generating character skills or combat stats without verifying the intended edition.
- **Why**: The two editions have different common skill lists (e.g., 2e uses Scan/Enhearten; 1e uses Search/Inspire) and different formulas for Parry and Endurance.
- **Solution**:
    - Default to 2nd Edition rules unless 1st Edition is explicitly requested.
    - Explicitly state the system edition at the top of the character profile.
- **Symptoms**:
    - Skills like "Inspire" or "Search" appearing in a profile labeled as 2e, or "Scan" appearing in a 1e profile.
- **Detection Pattern**: `(Search|Inspire|Persuade)` appearing alongside `(Scan|Enhearten|Hunting)`

---
