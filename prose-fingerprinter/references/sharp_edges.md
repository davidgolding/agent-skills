# Prose Fingerprinter Sharp Edges

This document defines the sharp edges used by prose-fingerprinter.

## Context Window Exhaustion on Large Inputs

- **Id**: context-exhaustion
- **Summary**: Attempting to process and analyze massive raw text files in a single context run, causing high token usage or output truncation.
- **Severity**: high
- **Situation**: The user provides an entire chapter or book (e.g., 20,000+ words) to extract a fingerprint.
- **Why**: Multi-dimensional linguistic parsing — syntax, syllables, etymology, modes — requires dense context space per word. Processing huge files directly will exceed context limits or dilute attention.
- **Solution**: Limit the analysis to a representative sample of 1,000 to 2,000 words spanning the text's range, per the Representative Sampling pattern; for longer documents, fingerprint several chunks and average the extracted metrics across them, disclosing how many chunks the average rests on.
- **Symptoms**: The analysis fails to finish, or the output arrives incomplete or with repetitive metrics.
- **Detection Pattern**: Analyzing input texts containing more than 3,000 words without applying sampling or chunking.

---

## Fabricated Scansion

- **Id**: fabricated-scansion
- **Summary**: Stress patterns and syllable counts asserted as measured when they were produced by impression rather than by scanning the line.
- **Severity**: high
- **Situation**: While reporting the prosodic dimension, particularly on a long passage where scanning every line is costly and a plausible-sounding count is cheap.
- **Why**: Scansion is checkable — a spondee count, unlike a thematic reading, is falsifiable by anyone who scans the same lines. A wrong count therefore discredits the dimensions around it that a reader cannot verify as easily, and the consciousness-engine synthesis built on the wrong rhythm inherits the error.
- **Solution**: Scan the specific lines the figure rests on and quote them alongside the count, or report the rhythm qualitatively — "spondaic braking dominates the closing sentences" — and mark the figure as estimated, naming the lines inspected.
- **Symptoms**: A precise syllable or foot count appears with no lines quoted, and the count does not survive a recount of the passage.
- **Detection Pattern**: A numeric scansion figure reported for a passage with no scanned lines cited and no estimation basis disclosed.

---

## Invented Etymology

- **Id**: invented-etymology
- **Summary**: Root-language attributions assigned by how a word sounds Germanic or Latinate rather than by its actual derivation.
- **Severity**: high
- **Situation**: While reporting the etymological register, especially for words whose phonetic character runs against their history.
- **Why**: The register reading is built on top of the attributions, so an inverted classification inverts the conclusion — a passage read as sensory and Anglo-Saxon grounded may in fact be running on Latinate abstraction, and the consciousness-engine synthesis then describes a text that does not exist. Short punchy words are not reliably Germanic, and polysyllables are not reliably Latinate.
- **Solution**: Classify only words whose derivation is known with confidence, report the register as a proportion of the words actually classified, and state how many words the proportion rests on; leave uncertain words in an unclassified count rather than assigning them by sound.
- **Symptoms**: A register proportion covering every word in the passage, or an attribution that reverses under a dictionary check.
- **Detection Pattern**: An etymological proportion reported without a classified-word count, or a classification tracking word length and phonetic weight rather than derivation.

---

## Single-Author Projection

- **Id**: single-author-projection
- **Summary**: The fingerprint collapses onto a famous exemplar instead of describing the passage in front of it.
- **Severity**: medium
- **Situation**: While synthesizing the consciousness engine, whenever the passage resembles a widely-known style on one or two dimensions.
- **Why**: A recognized signature arrives with a full set of associated traits, so naming it early imports mechanics absent from the passage and stops the analysis of the ones present in it. The failure reads as insight, which makes it easy to miss.
- **Solution**: Complete all five dimensions from the passage's own evidence before any comparison; where a resemblance is worth naming, attach it to the specific dimensions that support it and present it as a resemblance rather than an identification.
- **Symptoms**: An author's name appears before the five dimensions are reported, or the synthesis attributes traits with no supporting measurement in the fingerprint.
- **Detection Pattern**: An exemplar author named in the synthesis with no dimension-level evidence cited for the resemblance.

---
