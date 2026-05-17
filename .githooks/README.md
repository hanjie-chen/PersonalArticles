# Git Hooks

This directory stores repository-managed Git hooks.

Configure Git once in the repository root:

```shell
git config core.hooksPath .githooks
```

## Structure

```text
.githooks/
├── pre-commit
├── pre-commit.d/
│   ├── 10-normalize-image-extensions.py
│   └── 20-translate-staged-articles.py
└── tests/
    ├── test_pre_commit.py
    ├── test_normalize_image_extensions.py
    └── test_translate_staged_articles.py
```

## Pre-Commit

`pre-commit` is the only file Git executes directly.

It works as a runner and executes files in `pre-commit.d/` by filename order. Use numeric prefixes to make ordering explicit.

Current order:

1. `10-normalize-image-extensions.py`
   - lowercases staged image file extensions
   - stops the commit if it changes staged files
2. `20-translate-staged-articles.py`
   - checks staged publishable articles
   - translates missing or outdated English sidecars
   - stages generated translation files
   - stops the commit so changes can be reviewed

## Translation Hook

The translation hook reuses `.kb-tools/translator/` instead of duplicating translation logic.

Useful environment variables:

```shell
KB_TRANSLATOR_MODEL=gpt-5.4 git commit
KB_TRANSLATOR_JOBS=2 git commit
```

By default, the staged translation hook starts one worker per staged article that needs translation.

## Tests

Tests live in `.githooks/tests/` because they cover the hook system as a whole, not only one `pre-commit.d/` script.

Run them from the repository root:

```shell
python3 -m unittest discover -s .githooks/tests
```

If future hooks such as `pre-push` are added, keep their tests in `.githooks/tests/` and name them clearly, for example `test_pre_push.py` or `test_pre_push_<feature>.py`.
