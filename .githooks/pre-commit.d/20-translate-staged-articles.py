#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
        text=True,
    )
    return Path(result.stdout.strip())


def load_translator(root_dir: Path):
    translator_dir = root_dir / ".kb-tools" / "translator"
    sys.path.insert(0, str(translator_dir))
    from workflow import (  # pylint: disable=import-outside-toplevel
        PartiallyStagedArticleError,
        find_staged_candidates,
    )
    from translate import run_translation_jobs  # pylint: disable=import-outside-toplevel

    return PartiallyStagedArticleError, find_staged_candidates, run_translation_jobs


def git_add(root_dir: Path, path: Path) -> None:
    subprocess.run(
        ["git", "-C", str(root_dir), "add", "--", str(path.relative_to(root_dir))],
        check=True,
    )


def worker_count_for(total: int) -> int:
    configured = os.environ.get("KB_TRANSLATOR_JOBS")
    if not configured:
        return total

    try:
        return min(max(int(configured), 1), total)
    except ValueError:
        print(
            f"[pre-commit:translate] ignoring invalid KB_TRANSLATOR_JOBS={configured!r}",
            file=sys.stderr,
        )
        return total


def main() -> int:
    root_dir = repo_root()
    (
        partially_staged_error,
        find_staged_candidates,
        run_translation_jobs,
    ) = load_translator(root_dir)

    print("[pre-commit:translate] checking staged articles...")
    try:
        candidates = find_staged_candidates(root_dir, limit=None)
    except partially_staged_error as exc:
        print(f"[pre-commit:translate] {exc}", file=sys.stderr)
        print(
            "[pre-commit:translate] commit stopped; stage the article fully or "
            "commit unstaged edits separately",
            file=sys.stderr,
        )
        return 1

    if not candidates:
        print("[pre-commit:translate] ok: no staged articles need translation")
        return 0

    model = os.environ.get("KB_TRANSLATOR_MODEL")
    total = len(candidates)
    indexed_candidates = list(enumerate(candidates, start=1))

    for index, candidate in indexed_candidates:
        relative_source = candidate.source_md.relative_to(root_dir).as_posix()
        print(
            f"[pre-commit:translate] [{index}/{total}] "
            f"{candidate.status}\t{relative_source}"
        )

    worker_count = worker_count_for(total)
    print(f"[pre-commit:translate] starting {worker_count} worker(s)")
    results = run_translation_jobs(
        repo_root=root_dir,
        indexed_candidates=indexed_candidates,
        worker_count=worker_count,
        model=model,
    )

    success_count = 0
    failure_count = 0
    for result in results:
        if result.error or not result.translation_path:
            failure_count += 1
            continue
        success_count += 1
        git_add(root_dir, root_dir / result.translation_path)

    if failure_count:
        print(
            f"[pre-commit:translate] translated {success_count}, failed {failure_count}",
            file=sys.stderr,
        )
        print("[pre-commit:translate] commit stopped; please review errors and run git commit again")
        return 1

    print("[pre-commit:translate] updated staging area after translating articles")
    print("[pre-commit:translate] commit stopped; please review changes and run git commit again")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
