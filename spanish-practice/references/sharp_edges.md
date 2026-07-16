# Sharp Edges

This document defines the sharp edges used by spanish-practice.

---

## Dialect Drift

- **Id**: dialect-drift
- **Summary**: The agent introduces regional vocabulary or grammatical structures from a different dialect than the user's selected preference.
- **Severity**: high
- **Situation**: The student is practicing Argentine Spanish (voseo) but the agent accidentally suggests European Spanish verbs (vosotros) or Mexican vocabulary (e.g., using "pluma" instead of "lapicera" or "bolígrafo").
- **Why**: Dialect boundaries are complex, and the model's base training averages Spanish dialects, causing it to fall back to general Spanish unless heavily guided.
- **Solution**:
    - Explicitly query the user's dialect preference from the profile at the beginning of each prompt generation and double-check regional vocabulary before suggesting corrections.
- **Symptoms**:
    - The agent uses voseo and vosotros interchangeably in the same output, or corrects regionalisms that are perfectly natural in the target dialect.
- **Detection Pattern**: Dialogue responses containing grammatical conjugations or idiomatic words inconsistent with the active dialectPreference key in the profile.

---
