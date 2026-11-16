# Agent Skills

A collection of agent skills that run according to the [agent skills protocol](https://agentskills.io) in such apps as Claude Code, Antigravity, Codex, etc.

## Installation

1. Use `cd` to the desired project folder on the file system, e.g., `cd ~/Projects/anon-project`.
2. Run the [Skills.sh](https://skills.sh) tool with this repository as the address: `npx skills add davidgolding/agent-skills`.
3. Select the skill or skills to load into the project folder.
4. Within the agent environment, activate the skill using `/` syntax, e.g., `/skill-creator`.
### Claude Code plugin marketplace

This repository is also a Claude Code plugin marketplace, with each skill published as its own plugin. Add the marketplace once:

```
/plugin marketplace add davidgolding/agent-skills
```

Then install any skill:

```
/plugin install advanced-research-assistant --marketplace davidgolding/agent-skills
/plugin install anything-tutor --marketplace davidgolding/agent-skills
/plugin install apple-pages --marketplace davidgolding/agent-skills
/plugin install campaign-builder --marketplace davidgolding/agent-skills
/plugin install car-purchaser --marketplace davidgolding/agent-skills
/plugin install conlang-linguist --marketplace davidgolding/agent-skills
/plugin install corpus-curator --marketplace davidgolding/agent-skills
/plugin install corpus-search --marketplace davidgolding/agent-skills
/plugin install critical-reader --marketplace davidgolding/agent-skills
/plugin install data-scientist --marketplace davidgolding/agent-skills
/plugin install educator --marketplace davidgolding/agent-skills
/plugin install expert-researcher --marketplace davidgolding/agent-skills
/plugin install frontend-designer --marketplace davidgolding/agent-skills
/plugin install german-practice --marketplace davidgolding/agent-skills
/plugin install gmeu-copyeditor --marketplace davidgolding/agent-skills
/plugin install language-tutor --marketplace davidgolding/agent-skills
/plugin install lit-review-compiler --marketplace davidgolding/agent-skills
/plugin install meal-planner --marketplace davidgolding/agent-skills
/plugin install obsidian-assistant --marketplace davidgolding/agent-skills
/plugin install obsidian-navigator --marketplace davidgolding/agent-skills
/plugin install personal-trainer --marketplace davidgolding/agent-skills
/plugin install prose-fingerprinter --marketplace davidgolding/agent-skills
/plugin install reading-interlocutor --marketplace davidgolding/agent-skills
/plugin install rhetorician --marketplace davidgolding/agent-skills
/plugin install skill-auditor --marketplace davidgolding/agent-skills
/plugin install skill-creator --marketplace davidgolding/agent-skills
/plugin install spanish-practice --marketplace davidgolding/agent-skills
```
