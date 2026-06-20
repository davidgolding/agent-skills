# Obsidian Navigator - Validation Plan

This document outlines how to verify the correctness, triggering precision, and performance of the obsidian-navigator skill.

## Triggering Validations

Ensure that the skill triggers only when appropriate:

* **Positive Triggers (Should Trigger)**:
  * "Navigate my Obsidian vault to find what we decided about cognitive load."
  * "Search my Obsidian vault and trace the links to explain the notebase philosophy."
  * "Answer my question by traversing the links in my Obsidian notes: How do working memory and long-term memory interact?"
* **Negative Triggers (Should NOT Trigger)**:
  * "Open the Obsidian app." (Triggers a general app opening action/command).
  * "Search the web for Obsidian wiki." (Triggers a web search skill).
  * "Create a new note in my vault." (Triggers a note creation/modification skill).

---

## Execution Validations

Verify that the navigation behaves correctly in an active environment:

### Test Case: Multi-hop Traversal
1. Target the `Starter` vault.
2. Ask: "According to my notes, how should the notebase scale with memory, and what rule helps enforce this?"
3. **Expected Behavior**:
   - The skill selects the `Starter` vault.
   - It searches for "memory" or "notebase".
   - It reads `Home.md` or `Research/Notebase Philosophy.md`.
   - It discovers the link/backlink connections (e.g., `Home.md` -> `Research/Notebase Philosophy.md`).
   - It reads the philosophy document, recognizing the core concepts (shallow pool vs deep net, working vs long-term memory) and the essential rule (never create a new note without linking it to at least one other note).
   - It outputs a synthesized summary explaining how it scales (cross-referencing captured content, simplifying capture to avoid working memory overload) and the rule (never create an unlinked note), citing both `Home.md` and `Research/Notebase Philosophy.md`.
   - The total notes traversed must be less than 15.
   - No modifications are made to the vault.
