# Intake

Six parameters must be resolved before any editing begins.

| Parameter | Values | Default if unspecified |
|---|---|---|
| Edit type | developmental / substantive / reference / copyedit / mechanical / proofread | Always ask |
| Intensity | Light / Medium / Heavy | Medium, where the type admits intensity (see `references/edit-types.md`) |
| Citation & style system | Chicago (notes-bib or author-date), Turabian, MLA, APA, AP, house | Ask if the requested pass needs one |
| Usage authority | GMEU, CGG, Fowler, Merriam-Webster, American Heritage, house | GMEU (usage) + CGG (grammar) |
| Dialect / spelling | US, UK, Canadian, Australian; Merriam-Webster vs. Oxford spelling | US + Merriam-Webster |
| Deliverable format | inline commentary list / clean revised text / both / editorial memo | Per edit-type default (see `references/edit-types.md`) |

## Procedure

1. **Parse the opening prompt.** Extract every parameter the user already supplied. Accept anything explicit as-is, resolved.
2. **Identify gaps.** Determine which of the six parameters remain unresolved for the requested (or inferred) edit type. Some parameters apply only to some types--e.g. developmental editing needs no citation/style system; proofreading needs no usage authority.
3. **Ask once, batched.** If gaps remain, ask for all of them together in a single round, always batched rather than serial.
4. **State inferences as assumptions, not facts.** You may read a sample of the document and propose values--e.g., "the existing notes use author-date citations, so I'll assume Chicago 18 (author-date)"--but present these as assumptions for the user to confirm or correct, not as resolved parameters. Only parameters the user has actually confirmed (explicitly stated, or accepted your proposal) count as resolved.
5. **Record.** Write the resolved parameter set at the top of the active project's section in `references/stylesheet.md`, keyed by document title, so a later pass on the same project can skip intake and go straight to Phase 2.

## Skipping intake

If the active project section in `references/stylesheet.md` already contains a resolved parameter set for this document, and the current request doesn't name a different edit type or contradict a recorded parameter, skip straight to Phase 2 (Load authorities). Confirm briefly what's being reused, e.g.: "Continuing the mechanical pass on *Chapter 4* under Chicago 18 / Merriam-Webster, as recorded."
