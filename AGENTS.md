# AGENTS.md

This repository is the source and staging area for a collection of agent skills. It produces skills for other projects to install; it consumes none itself. Every rule below applies whenever this folder is the workspace, in any agent harness.

## What counts as a skill here

- Each top-level directory that contains a `SKILL.md` file is one skill. The directory name is the skill's name (for example, `skill-creator/` is the `skill-creator` skill).
- Only those directories are skills. Treat `.git/`, `.claude/`, other dotfolders, and root files such as `README.md` as repository infrastructure.
- To see which skills exist, list `*/SKILL.md` at the root at the moment you need the answer. Skills are added and renamed often, so the current listing is the authority over any remembered list.

## Resolving skill names

Any reference to a skill by name means the local folder of that name:

- `skill-creator`, "the skill-creator skill", "Use `/skill-creator`" in a prompt → `./skill-creator/`
- A namespaced name such as `anthropic-skills:obsidian-assistant` or `some-plugin:educator` → the local folder with the same base name (`./obsidian-assistant/`, `./educator/`).

## "Use the `X` skill…" means load the local folder

When asked to use, run, apply, or follow a skill named `X`, load it by reading files, in this order:

1. Read `./X/SKILL.md` in full. This file read is the load: it replaces your harness's skill loader, skill tool, or plugin mechanism for `X`, including when an installed skill shares the name.
2. Follow it exactly as if it had been loaded as a skill. Its frontmatter `description` says when it applies; its body is the instructions.
3. Resolve every relative path it mentions (`references/…`, `scripts/…`, `assets/…`, `evals/…`) against `./X/`. Read each of those files at the point the instructions call for it, as a real skill load would.
4. Run bundled scripts from their location inside `./X/`.

To confirm the load was correct, check that every file you read for `X` sits under `./X/`.

## Local folders are the only skills

- In this workspace, the folders in this root make up the complete set of skills. Skills provided by your harness, plugins, user-level config, or global config are out of scope here, including ones that share a name with a folder here; those are older or different builds.
- Select a skill only when the request names it or clearly calls for one of the local skills, and then load it from its folder as described above. Leave installed skills dormant even when a request matches their descriptions.
- If a named skill has no folder here, report that the folder is missing and ask how to proceed. Wait for that answer before using any other version of the skill.

## Using a skill vs. working on a skill

A request can name a skill as the instructions to follow, as the thing being changed, or both:

- "Use the `skill-creator` skill to improve `educator`" → follow `./skill-creator/SKILL.md`; the files under `./educator/` are what you edit.
- "Audit `rhetorician`" → `./rhetorician/` is the target; follow whatever process the request (or a named skill) gives.

Limit your reading to the skill folders the request names. Open a sibling skill for context or examples only when the request asks for it.

## Keep the root a source for installs elsewhere

- Keep the root's directories limited to skill folders and existing repository infrastructure (`.git/`, `.claude/`). Install or mirror folders such as `.agents/`, `.claude/skills/`, or `skills/` belong in consuming projects, outside this repository.
- Run skill installers (such as `npx skills add`) only in consuming projects, outside this repository.
- Create each new skill as a new top-level folder named for the skill, containing its `SKILL.md`.
