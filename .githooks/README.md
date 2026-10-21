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
│   └── 10-normalize-image-extensions.py
└── tests/
    ├── test_pre_commit.py
    └── test_normalize_image_extensions.py
```

## Pre-Commit

`pre-commit` is the only file Git executes directly.

It works as a runner and executes files in `pre-commit.d/` by filename order. Use numeric prefixes to make ordering explicit.

Hook scripts use this exit-code contract:

- `0`: check passed
- `1`: hard failure; stop immediately
- `2`: generated or staged changes; continue running later hooks, then stop before the commit is created

Current order:

1. `10-normalize-image-extensions.py`
   - lowercases staged image file extensions
   - asks for review if it changes staged files

Typical successful output:

```text
[pre-commit]
└─ 10-normalize-image-extensions.py
   └─ [ok] image: no uppercase image extensions found
```

Some hooks may ask for review after changing staged files. In that case, the runner keeps going and stops once at the end:

```text
[pre-commit]
└─ 10-normalize-image-extensions.py
   ├─ [fix] image: resources/images/Cover.PNG -> resources/images/Cover.png
   └─ [add] image: staged renamed image paths

[pre-commit] review required: generated changes were staged
```

If a hook exits with a hard failure before creating its own detailed message, the runner renders
the exit status as a child node under the failed script:

```text
[pre-commit]
└─ 10-normalize-image-extensions.py
   └─ [fail] hook: exited with status 1
```

## Tests

Tests live in `.githooks/tests/` because they cover the hook system as a whole, not only one `pre-commit.d/` script.

Run them from the repository root:

```shell
python3 -m unittest discover -s .githooks/tests
```

If future hooks such as `pre-push` are added, keep their tests in `.githooks/tests/` and name them clearly, for example `test_pre_push.py` or `test_pre_push_<feature>.py`.
