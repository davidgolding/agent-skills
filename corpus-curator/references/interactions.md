# Corpus Curator Interactions

This document defines the interaction flow used by corpus-curator.

## Interaction Rules

1. **One Question per Turn**: Ask for one missing fact at a time, through the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini and Pi) when the answer has a few distinct options, and in plain chat when it is a path or free text. End the turn after asking and continue only once the user answers.
2. **Review Table Is the Only Mid-Run Gate**: After extraction and drafting, the review table of uncertain rows is the one point where the run waits for the user. Corrections the user gives there are final for that run; apply them exactly.
3. **Approval Means an Explicit Reply**: Treat the user's reply to the review table as approval only when it answers each listed row (accept, correct, skip, replace, or suffix) or says to accept all as drafted. For any row left unanswered, ask about that row alone before writing it.
4. **State Writes Before Making Them**: Before writing to the corpus, state in one or two sentences how many files go into which collections, which assets will be copied, and whether `CONVENTIONS.md` or `Assets/` will be created.

## Execution Flow

### Phase 01: Intake

- **Objective**: Have both an input (file or folder) and a corpus root path.
- **Agent Action**: Read the paths from the invoking message. When the input path is missing, ask: "Which document or folder of documents should I add to the corpus?" When the corpus path is missing, ask: "Where is the corpus root folder (the folder that holds `CONVENTIONS.md` and the collection folders)?" Confirm each path exists.
- **Human Gate/Intervention**: The user supplies any missing path.
- **Proceed When**: Both paths are known and exist, or the corpus path is a new empty folder the user named for a new corpus.
- **Pause When**: Either path is missing or does not exist; ask for it and end the turn.

### Phase 02: Preflight

- **Objective**: Confirm the corpus root and the tools are ready.
- **Agent Action**: Run `scripts/extract.py` on the input into a fresh temporary work directory outside the corpus. Check the corpus root with `scripts/validate_corpus.py` to learn its existing keys and any pre-existing errors (record those as pre-existing, outside this run's scope). Note whether `CONVENTIONS.md` and `Assets/` exist.
- **Human Gate/Intervention**: None when tools are present. When `extract.py` exits with status 3, report each missing tool and its install command.
- **Proceed When**: Extraction finished with status 0.
- **Pause When**: A required tool is missing; report the install commands and end the turn without converting anything.

### Phase 03: Convert and Draft

- **Objective**: Produce a draft file and a confidence assessment for every extracted source.
- **Agent Action**: For each source in turn, classify it, choose its mode, structure the extracted text, read any image-only pages, assemble key, collection, and frontmatter, and mark each field confident or uncertain per the Confidence Triage pattern in `references/patterns.md`. Check each key against existing keys and earlier keys in this run, judging collisions per the Collision Judgment pattern. Hold drafts in the work directory.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: Every supported input has a draft or a recorded failure reason.
- **Pause When**: Not applicable; failures are recorded and carried to the report.

### Phase 04: Review Uncertain Rows

- **Objective**: Resolve every uncertain field and likely duplicate with the user.
- **Agent Action**: When at least one row is uncertain, present one table containing only those rows: input file, proposed key, proposed collection, and each uncertain field with its drafted value and the reason for doubt. State the count of confident rows not shown. Ask the user to accept, correct, skip, replace, or suffix each row.
- **Human Gate/Intervention**: The user answers each row in the table.
- **Proceed When**: No row is uncertain, or every listed row has an answer.
- **Pause When**: Uncertain rows exist and the user has not yet answered them; end the turn after presenting the table.

### Phase 05: Write

- **Objective**: Place the approved sources in the corpus.
- **Agent Action**: Apply the user's corrections, then state the planned writes per Interaction Rule 4. Create `CONVENTIONS.md` from `templates/CONVENTIONS.md` when it is absent, create `Assets/` when scans need it, write each source file into its collection, and copy scan and page-image originals into `Assets/` under `{key} {label}.{ext}`. Leave text-native originals untouched and leave every change uncommitted.
- **Human Gate/Intervention**: None beyond the Phase 04 answers.
- **Proceed When**: All approved files and assets are written.
- **Pause When**: A write fails (permissions, missing folder); report the failing path and end the turn.

### Phase 06: Audit

- **Objective**: Prove every written file is spec-compliant and faithful.
- **Agent Action**: Run `scripts/validate_corpus.py CORPUS --files <written files>` and `scripts/fidelity_check.py` for each file with an extraction. For image-only sources, re-read each page image against the written lines. Fix each error or unexplained difference in the file, then re-run both checks until clean.
- **Human Gate/Intervention**: None; this phase runs autonomously.
- **Proceed When**: The validator reports zero errors for the written files and every fidelity check exits 0.
- **Pause When**: A failure persists after three fix attempts on the same file; report the remaining findings for that file and ask the user how to proceed.

### Phase 07: Report

- **Objective**: Account for every input.
- **Agent Action**: Present the run report per the Verbose Run Report pattern, then delete the temporary work directory.
- **Human Gate/Intervention**: None; the user reads the report.
- **Proceed When**: The report is shown.
- **Pause When**: Not applicable.

## Handoff

- **The Completion State**: Every supported input is either written to the corpus, validated clean, and fidelity-checked, or listed in the report with the reason it was skipped or failed; scan images are in `Assets/`; nothing is committed; the work directory is deleted.
- **Exception/Fallback Handoff**: When the run stops early (missing tool, write failure, persistent audit failure, or the user cancels), report what was written so far, which files still fail and why, and where the work directory is, so the user can resume or remove the partial output.
