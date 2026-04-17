<!-- source_blob: 4dc2c4cd6140f3d2d672b543fabc2828e2043de4 -->

When we use coding agents (`claude code`, `codex`), we often run into a common problem: how do we help AI quickly understand a relatively complex project and start modifying it?

This problem can actually be split into two parts:

1. Help AI understand the project
2. Help AI know how to modify it

# Understand the project

To help AI understand a project faster, the most effective approach I have found so far is to split the documentation into three layers:

- project root README.md
- sub-folder README.md
- project root docs/

## project root README.md

The `README.md` in the root directory should serve as the entry page for the entire repository. Its content can include:

- project overview
- overall architecture diagram / main flow
- repository structure
- most commonly used commands
- an index pointing to more detailed documentation

This `README.md` is for both humans and AI, so depending on team or personal habits, I usually choose a mix of Chinese and English.

## sub-folder README.md

For directories that have their own independent subsystem logic, we can place a separate `README.md` inside the directory to explain:

- what this subsystem is responsible for
- where the entry file is
- what the key files do
- which files common changes usually touch

If all of this content is stuffed into the project root `README.md`, the root README will quickly become bloated. Moving the explanations down into their respective directories keeps the root README lightweight.

The tradeoff is also obvious: when the directory structure or subsystem logic changes, the corresponding sub-folder `README.md` must be maintained as well.

At the same time, the `README.md` here is mainly for AI to read and maintain, so it is best to keep it aligned with the code and written in pure English.

## project root docs/

When a document spans multiple directories at the same time, or is itself a longer topic-focused explanation, it is better suited for the `docs/` directory.

For example:

1. architecture documents spanning multiple subsystems
2. production incident troubleshooting runbooks
3. architectural decision records (ADR)

# Modify the project

Once we solve the problem of "helping AI understand the project," the next step is to help AI know how to modify it safely.

This is where another type of document is needed: the agent instruction file. For example, Codex uses `AGENTS.md`, and Claude Code uses `CLAUDE.md`. Next, we will use `AGENTS.md` as the example to explain this.

`AGENTS.md` is not "another README." It is more of an action guide than a project introduction.

The simplest distinction is:

- `README.md` answers: what this project is, how to run it, and what its structure roughly looks like
- `AGENTS.md` answers: if you are about to work on this repository right now, what should you read first, what constraints should you follow, and what pitfalls should you avoid

And `AGENTS.md` is also divided into three layers:

- global `AGENTS.md`
- project root `AGENTS.md`
- sub-floder `AGENTS.md`
