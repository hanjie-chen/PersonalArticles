---
Title: A Guide to Using AGENTS.md and README.md
SourceBlob: 4dc2c4cd6140f3d2d672b543fabc2828e2043de4
---

```
BriefIntroduction: Some personal experience with AI agent-assisted programming
```

<!-- split -->

When we use coding agents (Claude Code, Codex), we often run into a problem like this: how do we help AI quickly understand a relatively complex project and start making changes?

In practice, the problem can be divided into two parts:

1. Help AI understand the project
2. Help AI know how to modify it

# Understand the project

To help AI understand a project faster, the most effective method I have found so far is to split the documentation into three layers:

- project root README.md
- sub-folder README.md
- project root docs/

## project root README.md

The README.md at the repository root should serve as the entry page for the entire repo. Its contents can include:

- project overview
- overall architecture diagram / main execution flow
- repository structure
- most commonly used commands
- an index pointing to more detailed documentation

This README.md is meant for both humans and AI, so depending on the team or personal preference, I usually choose a mix of Chinese and English.

## sub-folder README.md

For directories that contain their own independent subsystem logic, we can place a separate README.md inside the directory to explain:

- what responsibilities this subsystem has
- where the entry file is
- what the key files each do
- which files common changes usually touch

If all of this is stuffed into the project root README.md, the root README will quickly become bloated. Moving these explanations down into their respective directories helps keep the root README lightweight.

The cost is also obvious: when the directory structure or subsystem logic changes, the corresponding sub-folder README.md must be maintained as well.

At the same time, the README.md here is mainly intended for AI to read and maintain, so it is best to keep it aligned with the code and use pure English.

## project root docs/

When a document spans multiple directories, or is itself a longer topic-specific explanation, it is more suitable to place it in the `docs/` directory.

For example:

1. architecture documentation spanning multiple subsystems
2. online incident troubleshooting runbooks
3. architecture decision records (ADR)

# Modify the project

Once we solve the problem of “helping AI understand the project,” the next step is to help AI know how to modify it safely.

At this point, we need another kind of document: an agent instruction file. For example, Codex uses `AGENTS.md`, and Claude Code uses `CLAUDE.md`. Next, we will use `AGENTS.md` as an example to explain this.

`AGENTS.md` is not “another README.” It is more of an action guide than a project introduction.

The simplest distinction is:

- `README.md` answers: what this project is, how to run it, and roughly how it is structured
- `AGENTS.md` answers: if you are about to change this repository, what should you read first, what constraints should you follow, and what pitfalls should you avoid

And `AGENTS.md` is also divided into three layers:

- global `AGENTS.md`
- project root `AGENTS.md`
- sub-folder `AGENTS.md`
