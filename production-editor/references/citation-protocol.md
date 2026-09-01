# Citation Protocol

Four citation classes, one per kind of authority:

| Class | Format | Example |
|---|---|---|
| Usage | `(<AUTHORITY>, "entry")` | `(GMEU, "contemporary; contemporaneous")` |
| Grammar | `(<AUTHORITY>, "Topic," section_number)` | `(CGG, "Pronouns: case," 5.12)` |
| Style manual | `(<MANUAL> <locator>)` | `(CMOS 18, ch. 9)`, `(APA 7, section 6.32)` |
| Style sheet | `(Style sheet: "<entry>")` | `(Style sheet: "e-mail")` |

Every reference, copyedit, or mechanical suggestion ends with exactly one citation from the class that actually governs it. Proofreading suggestions are exempt from citation. Developmental and substantive commentary may cite a usage authority when relevant but is not required to.

## Anti-hallucination rules

These rules exist because citing five possible style systems and multiple usage authorities multiplies the chance of an invented or misattributed reference--the single highest-severity failure mode of this skill (see `references/sharp_edges.md`).

1. **Cite a precise section/locator only when it appears in the loaded profile or the user-supplied manual.** If the precise number isn't in what you've actually loaded, cite by chapter or rule name instead (e.g. `(CMOS 18, hyphenation table)`)--always verifiable, always traceable to a loaded source.
2. **Keep the four classes strictly separate.** A grammar ruling is cited only to a grammar authority, and vice versa for usage. A style-manual formatting rule is cited only to the style manual, not to a usage or grammar authority.
3. **Consistency calls with no manual basis cite the style sheet**, not an invented manual entry. If the manual is silent and no prior style-sheet entry exists, make the call, cite it to the style sheet, and record the new entry (see `references/stylesheet.md`).
4. **Label a suggestion `(editorial judgment)` when no authority supports it**, and present it as a query rather than a correction.
5. **Cite only entries, sections, or examples that actually appear in a loaded reference.** When you're not confident an entry exists as stated, query it as uncertain rather than asserting it.
